#!/usr/bin/env python3
"""Check TeX key and numeric-token preservation between two TeX files."""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path


STRUCTURAL_COMMAND_RE = re.compile(
    r"\\(label|ref|eqref|cref|Cref|autoref|subref|citep|citet|cite|nocite|bibitem|bibliography|addbibresource)\s*"
    r"(?:\[[^\[\]]*\]\s*)*\{([^{}]*)\}"
)

BIBTEX_ENTRY_RE = re.compile(r"@\s*([A-Za-z]+)\s*\{\s*([^,\s]+)\s*,")

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
    for entry_type, value in BIBTEX_ENTRY_RE.findall(text):
        keys[f"bibtex:{entry_type.lower()}"][value.strip()] += 1
    return dict(keys)


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
    original: dict[str, Counter[str]], polished: dict[str, Counter[str]], limit: int
) -> bool:
    passed = True
    for command in sorted(set(original) | set(polished)):
        missing, added = counter_delta(original.get(command, Counter()), polished.get(command, Counter()))
        if missing or added:
            passed = False
            if command.startswith("bibtex:"):
                entry_type = command.split(":", 1)[1]
                title = f"BibTeX {entry_type} keys changed:"
            else:
                title = f"\\{command} keys changed:"
            print_counter_delta(title, missing, added, limit)
    return passed


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check whether structural TeX keys and numeric tokens were preserved."
    )
    parser.add_argument("original", type=Path, help="Original TeX file")
    parser.add_argument("polished", type=Path, help="Polished TeX file")
    parser.add_argument("--limit", type=int, default=20, help="Maximum changed tokens to print per category")
    args = parser.parse_args()

    try:
        original_text = read_text(args.original)
        polished_text = read_text(args.polished)
    except OSError as exc:
        print(f"Error reading input files: {exc}", file=sys.stderr)
        return 2

    original_keys = collect_structural_keys(original_text)
    polished_keys = collect_structural_keys(polished_text)
    keys_pass = compare_structural_keys(original_keys, polished_keys, args.limit)
    print(f"TeX keys: {'PASS' if keys_pass else 'FAIL'}")

    original_numbers = collect_numbers(original_text)
    polished_numbers = collect_numbers(polished_text)
    missing_numbers, added_numbers = counter_delta(original_numbers, polished_numbers)
    numbers_pass = not missing_numbers and not added_numbers
    print(f"Numeric tokens: {'PASS' if numbers_pass else 'FAIL'}")
    print_counter_delta("Numeric tokens changed:", missing_numbers, added_numbers, args.limit)

    return 0 if keys_pass and numbers_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
