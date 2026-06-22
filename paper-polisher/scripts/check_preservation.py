#!/usr/bin/env python3
"""Check TeX key and numeric-token preservation between two TeX files."""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path


STRUCTURAL_COMMAND_RE = re.compile(
    r"\\(label|ref|eqref|cref|Cref|autoref|subref|includegraphics|citep|citet|cite|nocite|bibitem|bibliography|addbibresource)\s*"
    r"(?:\[[^\[\]]*\]\s*)*\{([^{}]*)\}"
)

BIBTEX_ENTRY_RE = re.compile(r"@\s*([A-Za-z]+)\s*\{\s*([^,\s]+)\s*,")

INCLUDEGRAPHICS_RE = re.compile(r"\\includegraphics\s*((?:\[[^\[\]]*\]\s*)*)\{([^{}]*)\}")

CAPTION_RE = re.compile(r"\\caption\s*(?:\[[^\[\]]*\]\s*)?\{([^{}]*)\}", re.DOTALL)

DISPLAY_NUMBER_RE = r"(?:\d+(?:\.\d+)*|[IVXLCDM]+)"

NUMBERED_CAPTION_PREFIX_RE = re.compile(
    rf"^\s*(?:fig(?:ure)?\.?|table|tab\.?|algorithm|alg\.?)\s*~?\s*{DISPLAY_NUMBER_RE}\b",
    re.IGNORECASE,
)

HARDCODED_REFERENCE_RE = re.compile(
    rf"\b(?:fig(?:ure)?s?\.?|tables?|tabs?\.?|eq(?:uation)?s?\.?|sections?|secs?\.?|"
    rf"alg(?:orithm)?s?\.?|appendices|appendix)\s*~?\s*{DISPLAY_NUMBER_RE}\b",
    re.IGNORECASE,
)

MANUAL_REFERENCE_STYLE_RE = re.compile(
    r"\b(?P<name>figs?\.|figures?|tabs?\.|tables?|eqs?\.|equations?|secs?\.|sections?)"
    r"\s*~?\s*\\(?P<command>ref|eqref|autoref|cref|Cref|subref)\s*\{",
    re.IGNORECASE,
)

REFERENCE_NAME_STYLES = {
    "fig.": ("figure", "abbr"),
    "figs.": ("figure", "abbr"),
    "figure": ("figure", "full"),
    "figures": ("figure", "full"),
    "tab.": ("table", "abbr"),
    "tabs.": ("table", "abbr"),
    "table": ("table", "full"),
    "tables": ("table", "full"),
    "eq.": ("equation", "abbr"),
    "eqs.": ("equation", "abbr"),
    "equation": ("equation", "full"),
    "equations": ("equation", "full"),
    "sec.": ("section", "abbr"),
    "secs.": ("section", "abbr"),
    "section": ("section", "full"),
    "sections": ("section", "full"),
}

PLACEHOLDER_KEYS = {
    "",
    "alg",
    "algorithm",
    "app",
    "appendix",
    "eq",
    "equation",
    "fig",
    "figure",
    "image",
    "img",
    "label",
    "pic",
    "picture",
    "sec",
    "section",
    "subsec",
    "subsection",
    "tab",
    "table",
    "temp",
    "thm",
    "theorem",
    "tmp",
}

REFERENCE_COMMANDS = {"label", "ref", "eqref", "cref", "Cref", "autoref", "subref"}
MULTI_KEY_REFERENCE_COMMANDS = {"cref", "Cref"}

NUMBER_RE = re.compile(
    r"(?<![A-Za-z0-9_])"
    r"[+-]?(?:\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+\.\d+|\d+\.|\.\d+|\d+)"
    r"(?:[eE][+-]?\d+)?"
    r"(?:\\%|%|(?:\\,|\\;|\\:|\\!|~)?[A-Za-z\u00b5\u03bc\u00b0][A-Za-z\u00b5\u03bc\u00b0/%^{}+-]*)?"
    r"(?![A-Za-z0-9_])"
)


def strip_comments(text: str) -> str:
    """Remove TeX comments while preserving escaped percent signs."""
    cleaned_lines = []
    for line in text.splitlines():
        cut_at = None
        for idx, char in enumerate(line):
            if char != "%":
                continue
            backslashes = 0
            cursor = idx - 1
            while cursor >= 0 and line[cursor] == "\\":
                backslashes += 1
                cursor -= 1
            if backslashes % 2 == 0:
                cut_at = idx
                break
        cleaned_lines.append(line if cut_at is None else line[:cut_at])
    return "\n".join(cleaned_lines)


def collect_structural_keys(text: str) -> dict[str, Counter[str]]:
    text = strip_comments(text)
    keys: dict[str, Counter[str]] = defaultdict(Counter)
    for match in STRUCTURAL_COMMAND_RE.finditer(text):
        command, value = match.groups()
        keys[command][value.strip()] += 1
    for options, path in INCLUDEGRAPHICS_RE.findall(text):
        option_text = " ".join(options.split())
        signature = f"{option_text}{{{path.strip()}}}" if option_text else f"{{{path.strip()}}}"
        keys["includegraphics_options"][signature] += 1
    for entry_type, value in BIBTEX_ENTRY_RE.findall(text):
        keys[f"bibtex:{entry_type.lower()}"][value.strip()] += 1
    return dict(keys)


def split_reference_keys(command: str, value: str) -> list[str]:
    if command in MULTI_KEY_REFERENCE_COMMANDS:
        return [key.strip() for key in value.split(",")]
    return [value.strip()]


def collect_placeholder_reference_keys(text: str) -> dict[str, Counter[str]]:
    keys = collect_structural_keys(text)
    placeholders: dict[str, Counter[str]] = {}
    for command in sorted(REFERENCE_COMMANDS):
        command_placeholders: Counter[str] = Counter()
        for value, count in keys.get(command, Counter()).items():
            for key in split_reference_keys(command, value):
                if key.lower() in PLACEHOLDER_KEYS:
                    command_placeholders[key] += count
        if command_placeholders:
            placeholders[command] = command_placeholders
    return placeholders


def collect_numbered_caption_prefixes(text: str) -> Counter[str]:
    text = strip_comments(text)
    captions: Counter[str] = Counter()
    for caption in CAPTION_RE.findall(text):
        caption_text = " ".join(caption.split())
        if NUMBERED_CAPTION_PREFIX_RE.search(caption_text):
            captions[caption_text] += 1
    return captions


def remove_caption_commands(text: str) -> str:
    return CAPTION_RE.sub(r"\\caption", text)


def collect_hardcoded_display_references(text: str) -> Counter[str]:
    text = remove_caption_commands(strip_comments(text))
    return Counter(match.group(0) for match in HARDCODED_REFERENCE_RE.finditer(text))


def collect_reference_name_styles(text: str) -> dict[str, Counter[str]]:
    text = remove_caption_commands(strip_comments(text))
    styles: dict[str, Counter[str]] = defaultdict(Counter)
    for match in MANUAL_REFERENCE_STYLE_RE.finditer(text):
        name = match.group("name").lower()
        object_type, style = REFERENCE_NAME_STYLES[name]
        styles[object_type][style] += 1
    return dict(styles)


def remove_structural_command_arguments(text: str) -> str:
    return STRUCTURAL_COMMAND_RE.sub(lambda match: "\\" + match.group(1), text)


def collect_numbers(text: str) -> Counter[str]:
    text = strip_comments(text)
    text = remove_structural_command_arguments(text)
    return Counter(match.group(0) for match in NUMBER_RE.finditer(text))


def counter_delta(original: Counter[str], polished: Counter[str]) -> tuple[Counter[str], Counter[str]]:
    missing = original - polished
    added = polished - original
    return missing, added


def print_counter_delta(title: str, missing: Counter[str], added: Counter[str], limit: int) -> None:
    if not missing and not added:
        return
    print(title)
    for label, counter in (("Missing", missing), ("Added", added)):
        if not counter:
            continue
        print(f"  {label}:")
        for token, count in counter.most_common(limit):
            suffix = f" x{count}" if count > 1 else ""
            print(f"    {token}{suffix}")
        remaining = len(counter) - limit
        if remaining > 0:
            print(f"    ... {remaining} more")


def compare_structural_keys(
    original: dict[str, Counter[str]], polished: dict[str, Counter[str]], limit: int, allow_additions: bool
) -> bool:
    passed = True
    for command in sorted(set(original) | set(polished)):
        missing, added = counter_delta(original.get(command, Counter()), polished.get(command, Counter()))
        if missing or (added and not allow_additions):
            passed = False
            if command.startswith("bibtex:"):
                entry_type = command.split(":", 1)[1]
                title = f"BibTeX {entry_type} keys changed:"
            else:
                title = f"\\{command} keys changed:"
            reported_added = Counter() if allow_additions else added
            print_counter_delta(title, missing, reported_added, limit)
    return passed


def check_placeholder_reference_keys(polished_text: str, limit: int) -> bool:
    placeholders = collect_placeholder_reference_keys(polished_text)
    if not placeholders:
        print("Placeholder label/reference keys: PASS")
        return True

    print("Placeholder label/reference keys: FAIL")
    print("  Replace bare placeholder keys with semantic keys, such as tab:diff_methods or fig:framework.")
    for command in sorted(placeholders):
        print(f"  \\{command}:")
        for key, count in placeholders[command].most_common(limit):
            suffix = f" x{count}" if count > 1 else ""
            print(f"    \\{command}{{{key}}}{suffix}")
        remaining = len(placeholders[command]) - limit
        if remaining > 0:
            print(f"    ... {remaining} more")
    return False


def check_hardcoded_display_numbering(polished_text: str, limit: int) -> bool:
    numbered_captions = collect_numbered_caption_prefixes(polished_text)
    hardcoded_refs = collect_hardcoded_display_references(polished_text)
    if not numbered_captions and not hardcoded_refs:
        print("Hard-coded display numbering: PASS")
        return True

    print("Hard-coded display numbering: FAIL")
    print(
        "  Use LaTeX-generated numbering with the journal/manuscript style, "
        "such as Fig.~\\ref{fig:framework} or Figure~\\ref{fig:framework}, and omit Figure/Table numbers from captions."
    )
    if numbered_captions:
        print("  Numbered caption prefixes:")
        for caption, count in numbered_captions.most_common(limit):
            suffix = f" x{count}" if count > 1 else ""
            print(f"    \\caption{{{caption}}}{suffix}")
        remaining = len(numbered_captions) - limit
        if remaining > 0:
            print(f"    ... {remaining} more")
    if hardcoded_refs:
        print("  Hard-coded prose references:")
        for reference, count in hardcoded_refs.most_common(limit):
            suffix = f" x{count}" if count > 1 else ""
            print(f"    {reference}{suffix}")
        remaining = len(hardcoded_refs) - limit
        if remaining > 0:
            print(f"    ... {remaining} more")
    return False


def check_reference_name_style(original_text: str, polished_text: str, limit: int) -> bool:
    original_styles = collect_reference_name_styles(original_text)
    polished_styles = collect_reference_name_styles(polished_text)
    issues: dict[str, list[str]] = {}

    for object_type, polished_counter in polished_styles.items():
        polished_style_set = set(polished_counter)
        original_style_set = set(original_styles.get(object_type, Counter()))
        if original_style_set:
            introduced_styles = sorted(polished_style_set - original_style_set)
            if introduced_styles:
                issues[object_type] = [
                    f"introduced {', '.join(introduced_styles)} style; original uses {', '.join(sorted(original_style_set))}"
                ]
        elif len(polished_style_set) > 1:
            issues[object_type] = [f"mixed {', '.join(sorted(polished_style_set))} styles without an original style baseline"]

    if not issues:
        print("Reference-name style: PASS")
        return True

    print("Reference-name style: FAIL")
    print("  Match the target journal or manuscript style, such as Fig.~\\ref{...} versus Figure~\\ref{...}, and keep it consistent.")
    for object_type, object_issues in sorted(issues.items()):
        print(f"  {object_type}:")
        for issue in object_issues[:limit]:
            print(f"    {issue}")
        remaining = len(object_issues) - limit
        if remaining > 0:
            print(f"    ... {remaining} more")
    return False


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check whether structural TeX keys and numeric tokens were preserved."
    )
    parser.add_argument("original", type=Path, help="Original TeX file")
    parser.add_argument("polished", type=Path, help="Polished TeX file")
    parser.add_argument("--limit", type=int, default=20, help="Maximum changed tokens to print per category")
    parser.add_argument(
        "--allow-additions",
        action="store_true",
        help=(
            "Allow added structural keys and numeric tokens while still failing missing original keys, "
            "missing numeric tokens, placeholder keys, and changed existing image signatures."
        ),
    )
    args = parser.parse_args()

    try:
        original_text = read_text(args.original)
        polished_text = read_text(args.polished)
    except OSError as exc:
        print(f"Error reading input files: {exc}", file=sys.stderr)
        return 2

    original_keys = collect_structural_keys(original_text)
    polished_keys = collect_structural_keys(polished_text)
    keys_pass = compare_structural_keys(original_keys, polished_keys, args.limit, args.allow_additions)
    mode_note = " (additions allowed)" if args.allow_additions else ""
    print(f"TeX keys: {'PASS' if keys_pass else 'FAIL'}{mode_note}")
    placeholder_pass = check_placeholder_reference_keys(polished_text, args.limit)
    numbering_pass = check_hardcoded_display_numbering(polished_text, args.limit)
    reference_style_pass = check_reference_name_style(original_text, polished_text, args.limit)

    original_numbers = collect_numbers(original_text)
    polished_numbers = collect_numbers(polished_text)
    missing_numbers, added_numbers = counter_delta(original_numbers, polished_numbers)
    numbers_pass = not missing_numbers and (args.allow_additions or not added_numbers)
    print(f"Numeric tokens: {'PASS' if numbers_pass else 'FAIL'}{mode_note}")
    reported_added_numbers = Counter() if args.allow_additions else added_numbers
    print_counter_delta("Numeric tokens changed:", missing_numbers, reported_added_numbers, args.limit)

    return 0 if keys_pass and placeholder_pass and numbering_pass and reference_style_pass and numbers_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
