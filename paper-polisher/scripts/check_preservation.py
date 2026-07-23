#!/usr/bin/env python3
"""Check TeX preservation and hard polishing constraints between two TeX files."""

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

PROHIBITED_UNICODE_DASHES = "\u2012\u2013\u2014\u2015\u2e3a\u2e3b"
PROHIBITED_DASH_RE = re.compile(rf"[{PROHIBITED_UNICODE_DASHES}]|-{{2,}}")

BEGIN_ENVIRONMENT_RE = re.compile(r"\\begin\s*\{\s*(?P<name>[^{}\s]+)\s*\}")
INLINE_LITERAL_COMMAND_RE = re.compile(r"\\(?P<name>verb|lstinline)(?:\*)?(?![A-Za-z@])")
TEX_COMMAND_RE = re.compile(r"\\(?P<name>[A-Za-z@]+)(?:\*)?")

LITERAL_ENVIRONMENTS = {
    "BVerbatim",
    "LVerbatim",
    "SaveVerbatim",
    "Verbatim",
    "alltt",
    "asy",
    "filecontents",
    "filecontents*",
    "lstlisting",
    "luacode",
    "luacode*",
    "minted",
    "pgfpicture",
    "pspicture",
    "pycode",
    "sageblock",
    "tikzpicture",
    "verbatim",
    "verbatim*",
}

OPAQUE_ENVIRONMENTS = {"thebibliography"}

MATH_ENVIRONMENTS = {
    "Bmatrix",
    "IEEEeqnarray",
    "IEEEeqnarray*",
    "Vmatrix",
    "align",
    "align*",
    "alignat",
    "alignat*",
    "aligned",
    "alignedat",
    "array",
    "bmatrix",
    "cases",
    "displaymath",
    "equation",
    "equation*",
    "eqnarray",
    "eqnarray*",
    "flalign",
    "flalign*",
    "gather",
    "gather*",
    "gathered",
    "math",
    "matrix",
    "multline",
    "multline*",
    "pmatrix",
    "smallmatrix",
    "split",
    "vmatrix",
}

# These arguments contain protected keys, identifiers, URLs, paths, or source-code
# metadata rather than prose. Counts refer to required brace arguments. For
# commands such as \href, only the opaque target is masked; visible link text is
# deliberately left available for the prose check.
OPAQUE_COMMAND_ARGUMENT_COUNTS = {
    "addbibresource": 1,
    "autocite": 1,
    "autoref": 1,
    "begin": 1,
    "bibliography": 1,
    "bibliographystyle": 1,
    "bibitem": 1,
    "cite": 1,
    "citealp": 1,
    "citealt": 1,
    "citeauthor": 1,
    "citep": 1,
    "citet": 1,
    "citeyear": 1,
    "cpageref": 1,
    "cref": 1,
    "declaregraphicsextensions": 1,
    "documentclass": 1,
    "doi": 1,
    "end": 1,
    "eqref": 1,
    "footcite": 1,
    "graphicspath": 1,
    "href": 1,
    "hyperlink": 1,
    "hypertarget": 1,
    "include": 1,
    "includegraphics": 1,
    "includeonly": 1,
    "includefrom": 2,
    "input": 1,
    "inputfrom": 2,
    "inputminted": 2,
    "label": 1,
    "lstinputlisting": 1,
    "nocite": 1,
    "nolinkurl": 1,
    "pageref": 1,
    "parencite": 1,
    "path": 1,
    "ref": 1,
    "requirepackage": 1,
    "subfile": 1,
    "subimport": 2,
    "subref": 1,
    "textcite": 1,
    "url": 1,
    "usepackage": 1,
    "vref": 1,
}

VISIBLE_OPTION_ARGUMENT_COMMANDS = {
    "autocite",
    "cite",
    "citealp",
    "citealt",
    "citeauthor",
    "citep",
    "citet",
    "citeyear",
    "footcite",
    "parencite",
    "textcite",
}

UNBRACED_PATH_COMMANDS = {"include", "input", "subfile"}

CLI_LONG_OPTION_RE = re.compile(
    r"(?<![A-Za-z0-9_-])"
    r"--[A-Za-z][A-Za-z0-9]*(?:-[A-Za-z0-9]+)*"
    r"(?:=(?:\"[^\"\r\n]*\"|'[^'\r\n]*'|[^\s,;)}\]]+))?"
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


def is_escaped(text: str, index: int) -> bool:
    """Return whether the token starting at index is escaped by a backslash."""
    backslashes = 0
    cursor = index - 1
    while cursor >= 0 and text[cursor] == "\\":
        backslashes += 1
        cursor -= 1
    return backslashes % 2 == 1


def mask_span(buffer: list[str], start: int, end: int) -> None:
    """Blank a span without changing offsets or line numbers."""
    for index in range(max(start, 0), min(end, len(buffer))):
        if buffer[index] not in "\r\n":
            buffer[index] = " "


def find_balanced_end(text: str, start: int, opening: str, closing: str) -> int | None:
    """Return the exclusive end of a balanced TeX argument."""
    if start >= len(text) or text[start] != opening:
        return None

    depth = 0
    for index in range(start, len(text)):
        if is_escaped(text, index):
            continue
        if text[index] == opening:
            depth += 1
        elif text[index] == closing:
            depth -= 1
            if depth == 0:
                return index + 1
    return None


def find_environment_end(text: str, name: str, start: int) -> int:
    end_re = re.compile(rf"\\end\s*\{{\s*{re.escape(name)}\s*\}}")
    match = end_re.search(text, start)
    return match.end() if match else len(text)


def find_inline_literal_end(text: str, match: re.Match[str]) -> int | None:
    """Find the end of a \\verb or \\lstinline command."""
    command = match.group("name")
    cursor = match.end()

    if command == "lstinline":
        while cursor < len(text) and text[cursor] in " \t":
            cursor += 1
        if cursor < len(text) and text[cursor] == "[":
            option_end = find_balanced_end(text, cursor, "[", "]")
            if option_end is None:
                return text.find("\n", cursor) if "\n" in text[cursor:] else len(text)
            cursor = option_end
            while cursor < len(text) and text[cursor] in " \t":
                cursor += 1

    if cursor >= len(text) or text[cursor] in "\r\n" or text[cursor].isspace():
        return None

    delimiter = text[cursor]
    if delimiter == "{" and command == "lstinline":
        return find_balanced_end(text, cursor, "{", "}")

    line_end = text.find("\n", cursor + 1)
    search_end = len(text) if line_end == -1 else line_end
    closing = text.find(delimiter, cursor + 1, search_end)
    return closing + 1 if closing != -1 else search_end


def mask_comments_and_literal_regions(text: str, buffer: list[str]) -> None:
    """Mask comments, literal code, listings, and source-only environments."""
    cursor = 0
    while cursor < len(text):
        if text[cursor] == "\\" and not is_escaped(text, cursor):
            environment = BEGIN_ENVIRONMENT_RE.match(text, cursor)
            if environment and environment.group("name") in LITERAL_ENVIRONMENTS:
                end = find_environment_end(text, environment.group("name"), environment.end())
                mask_span(buffer, cursor, end)
                cursor = end
                continue

            inline_literal = INLINE_LITERAL_COMMAND_RE.match(text, cursor)
            if inline_literal:
                end = find_inline_literal_end(text, inline_literal)
                if end is not None:
                    mask_span(buffer, cursor, end)
                    cursor = end
                    continue

        if text[cursor] == "%" and not is_escaped(text, cursor):
            line_end = text.find("\n", cursor)
            end = len(text) if line_end == -1 else line_end
            mask_span(buffer, cursor, end)
            cursor = end
            continue

        cursor += 1


def mask_named_environments(buffer: list[str], names: set[str]) -> None:
    text = "".join(buffer)
    cursor = 0
    while True:
        environment = BEGIN_ENVIRONMENT_RE.search(text, cursor)
        if environment is None:
            return
        if environment.group("name") not in names:
            cursor = environment.end()
            continue

        end = find_environment_end(text, environment.group("name"), environment.end())
        mask_span(buffer, environment.start(), end)
        cursor = end


def find_unescaped_token(text: str, token: str, start: int) -> int:
    cursor = text.find(token, start)
    while cursor != -1 and is_escaped(text, cursor):
        cursor = text.find(token, cursor + 1)
    return cursor


def mask_delimited_regions(buffer: list[str], opening: str, closing: str) -> None:
    text = "".join(buffer)
    cursor = 0
    while True:
        start = find_unescaped_token(text, opening, cursor)
        if start == -1:
            return
        end_start = find_unescaped_token(text, closing, start + len(opening))
        end = len(text) if end_start == -1 else end_start + len(closing)
        mask_span(buffer, start, end)
        cursor = end


def mask_math_regions(buffer: list[str]) -> None:
    mask_named_environments(buffer, MATH_ENVIRONMENTS)
    mask_delimited_regions(buffer, r"\[", r"\]")
    mask_delimited_regions(buffer, r"\(", r"\)")
    mask_delimited_regions(buffer, "$$", "$$")
    mask_delimited_regions(buffer, "$", "$")


def skip_tex_whitespace(text: str, start: int) -> int:
    cursor = start
    while cursor < len(text) and text[cursor].isspace():
        cursor += 1
    return cursor


def mask_opaque_command_arguments(buffer: list[str]) -> None:
    text = "".join(buffer)
    spans: list[tuple[int, int]] = []

    for match in TEX_COMMAND_RE.finditer(text):
        if is_escaped(text, match.start()):
            continue
        command = match.group("name").lower()
        argument_count = OPAQUE_COMMAND_ARGUMENT_COUNTS.get(command)
        if argument_count is None:
            continue

        cursor = skip_tex_whitespace(text, match.end())
        while cursor < len(text) and text[cursor] == "[":
            option_end = find_balanced_end(text, cursor, "[", "]")
            if option_end is None:
                spans.append((cursor, len(text)))
                cursor = len(text)
                break
            if command not in VISIBLE_OPTION_ARGUMENT_COMMANDS:
                spans.append((cursor, option_end))
            cursor = skip_tex_whitespace(text, option_end)

        for _ in range(argument_count):
            if cursor >= len(text):
                break
            if text[cursor] == "{":
                argument_end = find_balanced_end(text, cursor, "{", "}")
                if argument_end is None:
                    spans.append((cursor, len(text)))
                    break
                spans.append((cursor, argument_end))
                cursor = skip_tex_whitespace(text, argument_end)
                continue

            if command in UNBRACED_PATH_COMMANDS:
                argument_end = cursor
                while argument_end < len(text) and not text[argument_end].isspace():
                    argument_end += 1
                spans.append((cursor, argument_end))
            break

    for start, end in spans:
        mask_span(buffer, start, end)


def mask_cli_long_options(buffer: list[str]) -> None:
    text = "".join(buffer)
    for match in CLI_LONG_OPTION_RE.finditer(text):
        mask_span(buffer, match.start(), match.end())


def mask_nonprose_for_dash_check(text: str) -> str:
    """Return a same-length copy with non-prose TeX regions blanked."""
    buffer = list(text)
    mask_comments_and_literal_regions(text, buffer)
    mask_named_environments(buffer, OPAQUE_ENVIRONMENTS)
    mask_math_regions(buffer)
    mask_opaque_command_arguments(buffer)
    mask_cli_long_options(buffer)
    return "".join(buffer)


def line_context(text: str, index: int, width: int = 120) -> tuple[int, str]:
    line_number = text.count("\n", 0, index) + 1
    line_start = text.rfind("\n", 0, index) + 1
    line_end = text.find("\n", index)
    if line_end == -1:
        line_end = len(text)

    half_width = max(width // 2, 1)
    context_start = max(line_start, index - half_width)
    context_end = min(line_end, index + half_width)
    context = " ".join(text[context_start:context_end].strip().split())
    if context_start > line_start:
        context = "... " + context
    if context_end < line_end:
        context += " ..."
    return line_number, context


def collect_prohibited_dashes(text: str) -> list[tuple[int, str, str]]:
    masked_text = mask_nonprose_for_dash_check(text)
    issues: list[tuple[int, str, str]] = []
    for match in PROHIBITED_DASH_RE.finditer(masked_text):
        line_number, context = line_context(text, match.start())
        issues.append((line_number, match.group(0), context))
    return issues


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


def check_dash_free_prose(polished_text: str, limit: int) -> bool:
    issues = collect_prohibited_dashes(polished_text)
    if not issues:
        print("Dash-free prose: PASS")
        return True

    print("Dash-free prose: FAIL")
    print(
        "  Replace dash punctuation with commas, semicolons, parentheses, appositive or relative clauses, "
        "or explicit wording such as 'from ... to ...'."
    )
    for line_number, token, context in issues[:limit]:
        print(f"    line {line_number}: {token!r} in {context}")
    remaining = len(issues) - limit
    if remaining > 0:
        print(f"    ... {remaining} more")
    return False


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check TeX preservation and hard polishing constraints."
    )
    parser.add_argument("original", type=Path, help="Original TeX file")
    parser.add_argument("polished", type=Path, help="Polished TeX file")
    parser.add_argument("--limit", type=int, default=20, help="Maximum issues to print per category")
    parser.add_argument(
        "--allow-additions",
        action="store_true",
        help=(
            "Allow added structural keys and numeric tokens while still failing missing original keys, "
            "missing numeric tokens, placeholder keys, changed existing image signatures, and dash-containing prose."
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
    dash_pass = check_dash_free_prose(polished_text, args.limit)

    original_numbers = collect_numbers(original_text)
    polished_numbers = collect_numbers(polished_text)
    missing_numbers, added_numbers = counter_delta(original_numbers, polished_numbers)
    numbers_pass = not missing_numbers and (args.allow_additions or not added_numbers)
    print(f"Numeric tokens: {'PASS' if numbers_pass else 'FAIL'}{mode_note}")
    reported_added_numbers = Counter() if args.allow_additions else added_numbers
    print_counter_delta("Numeric tokens changed:", missing_numbers, reported_added_numbers, args.limit)

    return (
        0
        if keys_pass
        and placeholder_pass
        and numbering_pass
        and reference_style_pass
        and dash_pass
        and numbers_pass
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
