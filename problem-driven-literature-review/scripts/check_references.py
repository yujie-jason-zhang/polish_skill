#!/usr/bin/env python3
"""Validate BibTeX reference metadata before it is used in a manuscript."""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date
from difflib import SequenceMatcher
from pathlib import Path


KNOWN_ENTRY_TYPES = {
    "article",
    "book",
    "booklet",
    "conference",
    "inbook",
    "incollection",
    "inproceedings",
    "manual",
    "mastersthesis",
    "misc",
    "online",
    "phdthesis",
    "proceedings",
    "techreport",
    "unpublished",
}

REQUIRED_FIELDS: dict[str, tuple[tuple[str, ...], ...]] = {
    "article": (("author",), ("title",), ("journal",), ("year", "date")),
    "book": (("author", "editor"), ("title",), ("publisher",), ("year", "date")),
    "inproceedings": (("author",), ("title",), ("booktitle",), ("year", "date")),
    "conference": (("author",), ("title",), ("booktitle",), ("year", "date")),
    "incollection": (("author",), ("title",), ("booktitle",), ("publisher",), ("year", "date")),
    "inbook": (("author", "editor"), ("title",), ("chapter", "pages"), ("publisher",), ("year", "date")),
    "phdthesis": (("author",), ("title",), ("school",), ("year", "date")),
    "mastersthesis": (("author",), ("title",), ("school",), ("year", "date")),
    "techreport": (("author",), ("title",), ("institution",), ("year", "date")),
    "manual": (("title",),),
    "proceedings": (("title",), ("year", "date")),
    "unpublished": (("author",), ("title",), ("note", "year", "date")),
    "online": (("title",), ("url", "doi"), ("year", "date", "urldate")),
    "misc": (("title",),),
}

DOI_RE = re.compile(r"10\.\d{4,9}/[-._;()/:A-Z0-9]+", re.IGNORECASE)
YEAR_RE = re.compile(r"\b(1[89]\d{2}|20\d{2}|21\d{2})\b")
HTML_ENTITY_RE = re.compile(r"&(?:amp|lt|gt|quot|apos|nbsp|[a-zA-Z]+|#\d+);")
GOOGLE_SCHOLAR_MARKER_RE = re.compile(r"\[[JCMDR]\]")
UPPERCASE_TOKEN_RE = re.compile(r"\b[A-Z][A-Z0-9+/-]{1,}\b")
URL_RE = re.compile(r"^https?://", re.IGNORECASE)
CONFERENCE_LIKE_RE = re.compile(
    r"\b(proceedings|conference|symposium|workshop|cvpr|iccv|eccv|neurips|nips|icml|"
    r"iclr|aaai|ijcai|siggraph|sigir|kdd|www|chi|iros|icra|cdc|acc|ifac|"
    r"ieee international|acm international)\b",
    re.IGNORECASE,
)
ROMAN_NUMERALS = {"II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"}


@dataclass(frozen=True)
class Field:
    name: str
    raw: str
    value: str
    line: int


@dataclass(frozen=True)
class Entry:
    entry_type: str
    key: str
    fields: dict[str, Field]
    line: int


@dataclass(frozen=True)
class Issue:
    severity: str
    code: str
    key: str
    line: int
    message: str
    hint: str = ""


class BibTeXParseError(ValueError):
    def __init__(self, message: str, index: int):
        super().__init__(message)
        self.index = index


def line_number(text: str, index: int) -> int:
    return text.count("\n", 0, max(index, 0)) + 1


def skip_space(text: str, index: int) -> int:
    while index < len(text) and text[index].isspace():
        index += 1
    return index


def find_matching_delimiter(text: str, index: int, opening: str, closing: str) -> int:
    depth = 0
    in_quote = False
    escaped = False
    cursor = index
    while cursor < len(text):
        char = text[cursor]
        if in_quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_quote = False
            cursor += 1
            continue
        if char == '"':
            in_quote = True
        elif char == opening:
            depth += 1
        elif char == closing:
            depth -= 1
            if depth == 0:
                return cursor
        cursor += 1
    raise BibTeXParseError(f"unclosed BibTeX entry starting with {opening!r}", index)


def split_top_level_once(text: str, delimiter: str) -> tuple[str, str]:
    brace_depth = 0
    paren_depth = 0
    in_quote = False
    escaped = False
    for index, char in enumerate(text):
        if in_quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_quote = False
            continue
        if char == '"':
            in_quote = True
        elif char == "{":
            brace_depth += 1
        elif char == "}":
            brace_depth = max(0, brace_depth - 1)
        elif char == "(":
            paren_depth += 1
        elif char == ")":
            paren_depth = max(0, paren_depth - 1)
        elif char == delimiter and brace_depth == 0 and paren_depth == 0:
            return text[:index], text[index + 1 :]
    return text, ""


def strip_outer_wrapper(value: str) -> str:
    value = value.strip()
    while len(value) >= 2:
        if value[0] == "{" and value[-1] == "}":
            try:
                if find_matching_delimiter(value, 0, "{", "}") == len(value) - 1:
                    value = value[1:-1].strip()
                    continue
            except BibTeXParseError:
                return value
        if value[0] == '"' and value[-1] == '"':
            value = value[1:-1].strip()
            continue
        break
    return value


def strip_single_outer_wrapper(value: str) -> str:
    value = value.strip()
    if len(value) < 2:
        return value
    if value[0] == "{" and value[-1] == "}":
        try:
            if find_matching_delimiter(value, 0, "{", "}") == len(value) - 1:
                return value[1:-1].strip()
        except BibTeXParseError:
            return value
    if value[0] == '"' and value[-1] == '"':
        return value[1:-1].strip()
    return value


def plain_text(value: str) -> str:
    value = strip_outer_wrapper(value)
    value = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?(?:\{([^{}]*)\})?", r"\1", value)
    value = re.sub(r"[{}]", "", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def parse_value(text: str, index: int) -> tuple[str, int]:
    index = skip_space(text, index)
    if index >= len(text):
        raise BibTeXParseError("expected a field value", index)

    parts: list[str] = []
    while True:
        index = skip_space(text, index)
        if index >= len(text):
            raise BibTeXParseError("expected a field value", index)
        char = text[index]
        if char == "{":
            end = find_matching_delimiter(text, index, "{", "}")
            parts.append(text[index : end + 1])
            index = end + 1
        elif char == '"':
            cursor = index + 1
            escaped = False
            brace_depth = 0
            while cursor < len(text):
                current = text[cursor]
                if escaped:
                    escaped = False
                elif current == "\\":
                    escaped = True
                elif current == "{":
                    brace_depth += 1
                elif current == "}":
                    brace_depth = max(0, brace_depth - 1)
                elif current == '"' and brace_depth == 0:
                    parts.append(text[index : cursor + 1])
                    index = cursor + 1
                    break
                cursor += 1
            else:
                raise BibTeXParseError("unclosed quoted field value", index)
        else:
            cursor = index
            while cursor < len(text) and text[cursor] not in ",#":
                cursor += 1
            parts.append(text[index:cursor].strip())
            index = cursor

        index = skip_space(text, index)
        if index < len(text) and text[index] == "#":
            parts.append(" # ")
            index += 1
            continue
        return "".join(parts).strip(), index


def parse_fields(body: str, body_start_index: int, source: str) -> tuple[str, dict[str, Field], list[Issue]]:
    key_part, fields_part = split_top_level_once(body, ",")
    key = key_part.strip()
    issues: list[Issue] = []
    fields: dict[str, Field] = {}
    if not key:
        issues.append(Issue("ERROR", "missing-key", "<unknown>", line_number(source, body_start_index), "missing BibTeX key"))

    index = 0
    while index < len(fields_part):
        index = skip_space(fields_part, index)
        while index < len(fields_part) and fields_part[index] == ",":
            index = skip_space(fields_part, index + 1)
        if index >= len(fields_part):
            break

        name_match = re.match(r"[A-Za-z][A-Za-z0-9_-]*", fields_part[index:])
        if not name_match:
            absolute = body_start_index + len(key_part) + 1 + index
            issues.append(
                Issue("ERROR", "parse-field", key or "<unknown>", line_number(source, absolute), "could not parse field name")
            )
            break
        field_name = name_match.group(0).lower()
        field_line = line_number(source, body_start_index + len(key_part) + 1 + index)
        index += len(name_match.group(0))
        index = skip_space(fields_part, index)
        if index >= len(fields_part) or fields_part[index] != "=":
            issues.append(
                Issue("ERROR", "parse-field", key or "<unknown>", field_line, f"field {field_name!r} is missing '='")
            )
            break
        index += 1
        try:
            raw_value, index = parse_value(fields_part, index)
        except BibTeXParseError as exc:
            absolute = body_start_index + len(key_part) + 1 + exc.index
            issues.append(Issue("ERROR", "parse-value", key or "<unknown>", line_number(source, absolute), str(exc)))
            break

        if field_name in fields:
            issues.append(
                Issue("ERROR", "duplicate-field", key or "<unknown>", field_line, f"duplicate field {field_name!r}")
            )
        fields[field_name] = Field(field_name, raw_value, plain_text(raw_value), field_line)

        index = skip_space(fields_part, index)
        if index < len(fields_part) and fields_part[index] == ",":
            index += 1

    return key, fields, issues


def parse_bibtex(text: str) -> tuple[list[Entry], list[Issue]]:
    entries: list[Entry] = []
    issues: list[Issue] = []
    cursor = 0
    while True:
        at_index = text.find("@", cursor)
        if at_index == -1:
            break
        type_match = re.match(r"@\s*([A-Za-z]+)", text[at_index:])
        if not type_match:
            cursor = at_index + 1
            continue
        entry_type = type_match.group(1).lower()
        cursor = at_index + type_match.end()
        cursor = skip_space(text, cursor)
        if cursor >= len(text) or text[cursor] not in "{(":
            issues.append(Issue("ERROR", "parse-entry", "<unknown>", line_number(text, at_index), "missing entry body"))
            continue

        opening = text[cursor]
        closing = "}" if opening == "{" else ")"
        try:
            end = find_matching_delimiter(text, cursor, opening, closing)
        except BibTeXParseError as exc:
            issues.append(Issue("ERROR", "parse-entry", "<unknown>", line_number(text, exc.index), str(exc)))
            break

        body_start = cursor + 1
        body = text[body_start:end]
        cursor = end + 1

        if entry_type in {"comment", "preamble", "string"}:
            continue

        key, fields, field_issues = parse_fields(body, body_start, text)
        issues.extend(field_issues)
        entries.append(Entry(entry_type, key, fields, line_number(text, at_index)))

    return entries, issues


def field(entry: Entry, name: str) -> Field | None:
    return entry.fields.get(name)


def has_any_field(entry: Entry, names: tuple[str, ...]) -> bool:
    return any(name in entry.fields and entry.fields[name].value for name in names)


def normalize_doi(raw: str) -> str:
    text = raw.strip()
    text = re.sub(r"^(?:doi\s*[:=]\s*)", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^https?://doi\.acm\.org/", "", text, flags=re.IGNORECASE)
    text = urllib.parse.unquote(text)
    text = text.strip(" .;,")
    match = DOI_RE.search(text)
    return match.group(0).lower() if match else ""


def doi_from_url(raw: str) -> str:
    return normalize_doi(raw)


def extract_year(entry: Entry) -> int | None:
    for name in ("year", "date"):
        current = field(entry, name)
        if current:
            match = YEAR_RE.search(current.value)
            if match:
                return int(match.group(1))
    return None


def protected_ranges(value: str) -> list[tuple[int, int]]:
    inner = strip_single_outer_wrapper(value)
    ranges: list[tuple[int, int]] = []
    stack: list[int] = []
    for index, char in enumerate(inner):
        if char == "{":
            stack.append(index)
        elif char == "}" and stack:
            start = stack.pop()
            ranges.append((start, index))
    return ranges


def is_in_range(index: int, ranges: list[tuple[int, int]]) -> bool:
    return any(start < index < end for start, end in ranges)


def unprotected_uppercase_tokens(raw_title: str) -> list[str]:
    inner = strip_single_outer_wrapper(raw_title)
    if inner.startswith("{") and inner.endswith("}"):
        return []
    ranges = protected_ranges(raw_title)
    tokens: list[str] = []
    for match in UPPERCASE_TOKEN_RE.finditer(inner):
        token = match.group(0)
        if token in ROMAN_NUMERALS:
            continue
        if not any(char.isalpha() for char in token):
            continue
        if not is_in_range(match.start(), ranges):
            tokens.append(token)
    return sorted(set(tokens))


def normalize_text_for_similarity(text: str) -> str:
    text = plain_text(text).lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def similarity(left: str, right: str) -> float:
    left_norm = normalize_text_for_similarity(left)
    right_norm = normalize_text_for_similarity(right)
    if not left_norm or not right_norm:
        return 0.0
    return SequenceMatcher(None, left_norm, right_norm).ratio()


def first_author_surname(author_value: str) -> str:
    first = re.split(r"\s+and\s+", author_value, maxsplit=1, flags=re.IGNORECASE)[0].strip()
    first = re.sub(r"\{|\}", "", first)
    if "," in first:
        return first.split(",", 1)[0].strip().lower()
    parts = first.split()
    return parts[-1].strip().lower() if parts else ""


def validate_entries(entries: list[Entry], current_year: int) -> list[Issue]:
    issues: list[Issue] = []

    keys = Counter(entry.key for entry in entries if entry.key)
    for entry in entries:
        if keys[entry.key] > 1:
            issues.append(Issue("ERROR", "duplicate-key", entry.key, entry.line, "duplicate BibTeX key"))

        if entry.entry_type not in KNOWN_ENTRY_TYPES:
            issues.append(
                Issue(
                    "WARN",
                    "unknown-type",
                    entry.key,
                    entry.line,
                    f"unknown entry type @{entry.entry_type}",
                    "Use a standard BibTeX type unless the target .bst/.bbx explicitly supports it.",
                )
            )

        for requirement in REQUIRED_FIELDS.get(entry.entry_type, (("title",),)):
            if not has_any_field(entry, requirement):
                readable = " or ".join(requirement)
                issues.append(
                    Issue("ERROR", "missing-required-field", entry.key, entry.line, f"missing required field: {readable}")
                )

        for current_field in entry.fields.values():
            if not current_field.value:
                issues.append(
                    Issue("ERROR", "empty-field", entry.key, current_field.line, f"empty field: {current_field.name}")
                )
            if HTML_ENTITY_RE.search(current_field.raw):
                issues.append(
                    Issue(
                        "WARN",
                        "html-entity",
                        entry.key,
                        current_field.line,
                        f"field {current_field.name!r} contains an HTML entity",
                        "Replace HTML entities with plain text or LaTeX-safe characters.",
                    )
                )

        title = field(entry, "title")
        if title:
            if GOOGLE_SCHOLAR_MARKER_RE.search(title.value):
                issues.append(
                    Issue(
                        "WARN",
                        "scholar-marker",
                        entry.key,
                        title.line,
                        "title contains source-type markers such as [J] or [C]",
                        "Remove Google Scholar or database export markers from the title.",
                    )
                )
            acronyms = unprotected_uppercase_tokens(title.raw)
            if acronyms:
                shown = ", ".join(acronyms[:5])
                suffix = "" if len(acronyms) <= 5 else f", ... {len(acronyms) - 5} more"
                issues.append(
                    Issue(
                        "WARN",
                        "unprotected-title-case",
                        entry.key,
                        title.line,
                        f"title may need brace-protected capitalization: {shown}{suffix}",
                        "Protect acronyms or proper nouns as {MPC}, {CNN}, {IEEE}, etc.",
                    )
                )

        author = field(entry, "author")
        if author:
            author_value = author.value
            if re.search(r"\bet\.?\s*al\.?\b", author_value, re.IGNORECASE):
                issues.append(
                    Issue(
                        "WARN",
                        "author-et-al",
                        entry.key,
                        author.line,
                        "author field contains et al.",
                        "List all authors in BibTeX when available; let the bibliography style abbreviate names.",
                    )
                )
            if ";" in author_value or " & " in author_value:
                issues.append(
                    Issue(
                        "WARN",
                        "author-separator",
                        entry.key,
                        author.line,
                        "author field uses a non-BibTeX separator",
                        "Separate authors with ' and ', not semicolons, ampersands, or a formatted reference string.",
                    )
                )
            if " and " not in author_value.lower() and author_value.count(",") >= 3:
                issues.append(
                    Issue(
                        "WARN",
                        "author-list-format",
                        entry.key,
                        author.line,
                        "author field looks like a formatted comma-separated list",
                        "Use 'Last, First and Last, First' form for multiple authors.",
                    )
                )

        pages = field(entry, "pages")
        if pages and re.search(r"\d\s*-\s*\d", pages.value) and "--" not in pages.raw:
            issues.append(
                Issue(
                    "WARN",
                    "page-range",
                    entry.key,
                    pages.line,
                    "page range uses a single hyphen",
                    "Use BibTeX page ranges such as 123--130.",
                )
            )

        year = extract_year(entry)
        if has_any_field(entry, ("year", "date")) and year is None:
            source_field = field(entry, "year") or field(entry, "date")
            issues.append(
                Issue(
                    "ERROR",
                    "bad-year",
                    entry.key,
                    source_field.line if source_field else entry.line,
                    "year/date does not contain a four-digit year",
                )
            )
        elif year is not None and (year < 1800 or year > current_year + 1):
            source_field = field(entry, "year") or field(entry, "date")
            issues.append(
                Issue(
                    "WARN",
                    "suspicious-year",
                    entry.key,
                    source_field.line if source_field else entry.line,
                    f"suspicious publication year: {year}",
                )
            )

        doi = field(entry, "doi")
        url = field(entry, "url")
        if doi:
            normalized = normalize_doi(doi.value)
            if not normalized:
                issues.append(Issue("ERROR", "bad-doi", entry.key, doi.line, f"malformed DOI: {doi.value}"))
            elif doi.value.strip().lower() != normalized:
                issues.append(
                    Issue(
                        "WARN",
                        "doi-format",
                        entry.key,
                        doi.line,
                        "DOI field is not stored as a bare DOI",
                        f"Use doi = {{{normalized}}}.",
                    )
                )
        elif url and doi_from_url(url.value):
            issues.append(
                Issue(
                    "WARN",
                    "doi-in-url",
                    entry.key,
                    url.line,
                    "URL contains a DOI but the DOI field is missing",
                    f"Add doi = {{{doi_from_url(url.value)}}}.",
                )
            )
        elif url and not URL_RE.search(url.value):
            issues.append(Issue("WARN", "bad-url", entry.key, url.line, f"URL may be malformed: {url.value}"))

        journal = field(entry, "journal")
        booktitle = field(entry, "booktitle")
        if entry.entry_type == "article" and journal and CONFERENCE_LIKE_RE.search(journal.value):
            issues.append(
                Issue(
                    "WARN",
                    "conference-as-article",
                    entry.key,
                    journal.line,
                    "conference-like venue stored as journal in an @article entry",
                    "Google Scholar often exports conference papers this way; verify against publisher metadata and use @inproceedings/booktitle when appropriate.",
                )
            )
        if entry.entry_type in {"inproceedings", "conference"} and journal:
            issues.append(
                Issue(
                    "WARN",
                    "journal-in-proceedings",
                    entry.key,
                    journal.line,
                    "proceedings entry has a journal field",
                    "Use booktitle for conference/proceedings venues unless the target style requires otherwise.",
                )
            )
        if entry.entry_type == "article" and booktitle:
            issues.append(
                Issue(
                    "WARN",
                    "booktitle-in-article",
                    entry.key,
                    booktitle.line,
                    "@article entry has a booktitle field",
                    "Verify whether this should be @inproceedings.",
                )
            )

    doi_to_entries: dict[str, list[Entry]] = defaultdict(list)
    for entry in entries:
        doi = field(entry, "doi")
        if doi:
            normalized = normalize_doi(doi.value)
            if normalized:
                doi_to_entries[normalized].append(entry)
    for normalized, doi_entries in doi_to_entries.items():
        if len(doi_entries) > 1:
            keys = ", ".join(entry.key for entry in doi_entries)
            issues.append(
                Issue("ERROR", "duplicate-doi", doi_entries[0].key, doi_entries[0].line, f"duplicate DOI {normalized}: {keys}")
            )

    return issues


def crossref_request(url: str, mailto: str, timeout: float) -> dict | None:
    user_agent = "reference-validator/1.0"
    if mailto:
        user_agent += f" (mailto:{mailto})"
    request = urllib.request.Request(url, headers={"User-Agent": user_agent, "Accept": "application/json"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def crossref_work_by_doi(doi: str, mailto: str, timeout: float) -> dict | None:
    encoded = urllib.parse.quote(doi, safe="")
    payload = crossref_request(f"https://api.crossref.org/works/{encoded}", mailto, timeout)
    if not payload:
        return None
    return payload.get("message")


def crossref_title_search(title: str, mailto: str, timeout: float) -> dict | None:
    query = urllib.parse.urlencode({"query.title": title, "rows": "1", "select": "DOI,title,issued,author,container-title"})
    payload = crossref_request(f"https://api.crossref.org/works?{query}", mailto, timeout)
    items = payload.get("message", {}).get("items", []) if payload else []
    return items[0] if items else None


def crossref_year(work: dict) -> int | None:
    for key in ("published-print", "published-online", "published", "issued"):
        date_parts = work.get(key, {}).get("date-parts", [])
        if date_parts and date_parts[0]:
            return int(date_parts[0][0])
    return None


def crossref_title(work: dict) -> str:
    titles = work.get("title") or []
    return titles[0] if titles else ""


def crossref_venue(work: dict) -> str:
    venues = work.get("container-title") or []
    return venues[0] if venues else ""


def crossref_first_surname(work: dict) -> str:
    authors = work.get("author") or []
    if not authors:
        return ""
    return (authors[0].get("family") or "").lower()


def validate_against_crossref(entries: list[Entry], online_title_search: bool, mailto: str, timeout: float) -> list[Issue]:
    issues: list[Issue] = []
    for entry in entries:
        doi_field = field(entry, "doi")
        title_field = field(entry, "title")
        local_doi = normalize_doi(doi_field.value) if doi_field else ""
        work: dict | None = None

        if local_doi:
            try:
                work = crossref_work_by_doi(local_doi, mailto, timeout)
            except urllib.error.HTTPError as exc:
                issues.append(
                    Issue("ERROR", "crossref-doi", entry.key, doi_field.line, f"Crossref could not resolve DOI {local_doi}: HTTP {exc.code}")
                )
                continue
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
                issues.append(
                    Issue("WARN", "crossref-network", entry.key, doi_field.line, f"Crossref check skipped for DOI {local_doi}: {exc}")
                )
                continue

            remote_title = crossref_title(work)
            if title_field and remote_title:
                score = similarity(title_field.value, remote_title)
                if score < 0.82:
                    issues.append(
                        Issue(
                            "ERROR",
                            "crossref-title",
                            entry.key,
                            title_field.line,
                            f"title differs from Crossref metadata for DOI {local_doi} (similarity {score:.2f})",
                            f"Crossref title: {remote_title}",
                        )
                    )

            remote_year = crossref_year(work)
            local_year = extract_year(entry)
            if local_year and remote_year and local_year != remote_year:
                issues.append(
                    Issue(
                        "WARN",
                        "crossref-year",
                        entry.key,
                        entry.line,
                        f"local year {local_year} differs from Crossref year {remote_year}",
                    )
                )

            author_field = field(entry, "author")
            remote_surname = crossref_first_surname(work)
            local_surname = first_author_surname(author_field.value) if author_field else ""
            if local_surname and remote_surname and local_surname != remote_surname:
                issues.append(
                    Issue(
                        "WARN",
                        "crossref-author",
                        entry.key,
                        author_field.line if author_field else entry.line,
                        f"first author surname differs from Crossref: local {local_surname!r}, Crossref {remote_surname!r}",
                    )
                )

            venue_field = field(entry, "journal") or field(entry, "booktitle")
            remote_venue = crossref_venue(work)
            if venue_field and remote_venue and similarity(venue_field.value, remote_venue) < 0.55:
                issues.append(
                    Issue(
                        "WARN",
                        "crossref-venue",
                        entry.key,
                        venue_field.line,
                        "venue differs from Crossref metadata",
                        f"Crossref venue: {remote_venue}",
                    )
                )
            continue

        if online_title_search and title_field:
            try:
                work = crossref_title_search(title_field.value, mailto, timeout)
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
                issues.append(
                    Issue("WARN", "crossref-network", entry.key, title_field.line, f"Crossref title search skipped: {exc}")
                )
                continue
            if not work:
                continue
            score = similarity(title_field.value, crossref_title(work))
            candidate_doi = normalize_doi(work.get("DOI", ""))
            if score >= 0.90 and candidate_doi:
                issues.append(
                    Issue(
                        "WARN",
                        "missing-doi",
                        entry.key,
                        title_field.line,
                        f"Crossref found a likely DOI for this title: {candidate_doi}",
                        "Verify the match and add the DOI field.",
                    )
                )

    return issues


def print_issues(issues: list[Issue], limit: int) -> None:
    for issue in issues[:limit]:
        location = f":{issue.line}" if issue.line else ""
        print(f"{issue.severity} [{issue.code}] {issue.key}{location}: {issue.message}")
        if issue.hint:
            print(f"  Hint: {issue.hint}")
    remaining = len(issues) - limit
    if remaining > 0:
        print(f"... {remaining} more issues not shown")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate BibTeX structure and reference metadata.")
    parser.add_argument("bibfile", type=Path, help="BibTeX file, TeX file, or text file containing BibTeX entries")
    parser.add_argument("--online", action="store_true", help="Verify DOI metadata against Crossref")
    parser.add_argument(
        "--title-search",
        action="store_true",
        help="With --online, search Crossref by title for entries that do not have a DOI",
    )
    parser.add_argument("--mailto", default="", help="Email address for polite Crossref API requests")
    parser.add_argument("--timeout", type=float, default=8.0, help="Crossref request timeout in seconds")
    parser.add_argument("--strict", action="store_true", help="Return a failing exit code for warnings as well as errors")
    parser.add_argument("--limit", type=int, default=80, help="Maximum number of issues to print")
    args = parser.parse_args()

    try:
        text = args.bibfile.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"Error reading input file: {exc}", file=sys.stderr)
        return 2

    entries, parse_issues = parse_bibtex(text)
    issues = parse_issues + validate_entries(entries, date.today().year)
    if args.online:
        issues.extend(validate_against_crossref(entries, args.title_search, args.mailto, args.timeout))

    severity_order = {"ERROR": 0, "WARN": 1}
    issues.sort(key=lambda item: (severity_order.get(item.severity, 9), item.line, item.key, item.code))

    counts = Counter(issue.severity for issue in issues)
    status = "PASS"
    if counts["ERROR"] or (args.strict and counts["WARN"]):
        status = "FAIL"
    elif counts["WARN"]:
        status = "PASS_WITH_WARNINGS"

    print(
        f"Reference metadata check: {status} "
        f"({len(entries)} entries, {counts['ERROR']} errors, {counts['WARN']} warnings)"
    )
    print_issues(issues, args.limit)

    if counts["ERROR"] or (args.strict and counts["WARN"]):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
