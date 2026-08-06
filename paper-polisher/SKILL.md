---
name: paper-polisher
description: Polish, translate, or faithfully revise Chinese or English TeX academic manuscripts; verify source-to-output TeX, math, citation, numerical, and claim preservation; audit cross-section terminology, mathematical notation, and numerical consistency; or apply an author-approved notation mapping. Use for sentence-level through full-manuscript engineering-journal language work when technical truth and protected TeX must remain fixed. For full manuscripts, run terminology, notation, and numerical-consistency audits by default. Do not use as the main skill for novelty review, literature selection, or argument redesign.
---

# Paper Polisher

## Scope and References

Use this skill for TeX-safe academic English polishing, translation, proofreading, source-to-output verification, terminology or notation review, numerical-consistency review, and explicitly authorized notation normalization.

For full papers, long sections, verification, consistency audits, normalization, or strict style-guide work, read `references/tex_safe_polishing.md` before acting. Read `references/tex_safe_polishing_zh.md` instead when Chinese-facing workflow guidance is materially useful; do not load both merely to duplicate context. For a short local polish, use the core rules below and consult a reference only when needed.

Do not use this skill as the main tool for:

- novelty, contribution-defensibility, dangerous-baseline, or reviewer-attack audits; use `idea-novelty-auditor` if available;
- literature review, gap framing, reference selection, or citation-role assignment; use `problem-driven-literature-review` if available;
- broad storyline, introduction structure, or experiment-to-claim redesign; use `paper-argument-reconstructor` if available.

When a request combines those tasks with polishing, complete the upstream reasoning task first and use this skill only for the final faithful language and consistency pass.

## Mode Selection and Precedence

Follow the user's explicit requested action before considering who produced the input. Provenance alone never overrides an explicit request to polish, audit, verify, or normalize. If more than one action is requested, keep their artifacts and reports separate unless the user asks for a combined deliverable.

Mode-specific output rules take precedence over output rules based on document length. In particular, a full-manuscript verification or consistency-only audit remains report-only.

If the user requests both notation normalization and prose polishing, perform and approve normalization first, treat the normalized TeX as the new baseline, and then polish against that baseline. Do not try to validate a combined prose-and-symbol change as one normalization comparison.

### Default Polishing Mode

Polish or translate the supplied text while preserving every protected element. For a full manuscript, also run terminology, notation, and source-internal numerical-consistency audits and report source-level issues without silently correcting them.

### Verification Mode

Use verification mode when the user asks to compare or quality-check a candidate against an original.

- Require both the original and the candidate for every comparative judgment about TeX, math, numbers, units, signs, citations, technical meaning, or claim strength.
- If the original is unavailable, inspect only intrinsic properties of the candidate and mark every source-comparative check `NOT ASSESSED`; never infer preservation from the candidate alone.
- Never rewrite or repair the candidate in verification mode, including hard-rule violations. Report each deviation and its location. Apply fixes only in a separate, explicitly requested editing turn or mode.
- Separate candidate-introduced deviations from terminology, notation, or numerical conflicts already present in the source.

### Consistency Audit Mode

When the user asks only for terminology, variable, symbol, notation, or numerical consistency, do not rewrite the manuscript. Audit the available scope and report `TERM-*`, `SYM-*`, and `NUM-*` findings as applicable. Keep source text, symbols, values, units, and signs unchanged.

### Approved Notation Normalization Mode

Use this mode only when the user explicitly requests normalization and has approved an exact symbol mapping. An approved mapping must identify the mathematical entity, old and new symbols, affected scope or locations, and any intentional aliases or exclusions.

- Apply only the approved symbol substitutions. Do not reinterpret definitions or choose a canonical symbol on the user's behalf.
- Record every applied substitution as `AUTHORIZED CHANGE`; treat every unmapped math, structural, textual, or numerical difference as an error.
- Keep all numbers, units, percentages, dimensions, sample sizes, ordering of numerical tokens, and positive, negative, or plus-minus signs unchanged.
- If an affected symbol occurs inside an unavailable or non-editable figure asset, custom environment, generated file, or unresolved macro expansion, report the unresolved location and do not claim complete normalization.
- Validate the normalized result against the approved mapping. If mapping-aware comparison is unavailable, obtain approval of the normalized TeX as a new author-approved baseline, then use strict comparison against that baseline for all subsequent polishing.

Do not use `--allow-additions` to authorize symbol changes. Do not modify a number, unit, or numerical sign in any paper-polisher mode, even after reporting a `NUM-*` conflict. Ask the user to correct the source outside this skill and provide the corrected TeX as a new author-approved baseline; never infer or apply a replacement value.

## Shared Coverage and Result Protocol

Report coverage and result separately for every terminology, notation, and numerical-consistency audit.

- `Coverage: FULL MANUSCRIPT` means the completeness gate below passed.
- `Coverage: PARTIAL` means only the stated local or resolvable scope was audited.
- `Result: PASS` means no conflict or unresolved ambiguity was found within the assessed scope.
- `Result: ISSUE REPORTED` means at least one clear inconsistency was found and no finding still requires an author decision.
- `Result: AUTHOR DECISION REQUIRED` means at least one plausible finding cannot be resolved from the manuscript alone. Confirmed issues remain individually labeled `ISSUE REPORTED`.
- `Result: NOT ASSESSED` means that audit or comparison could not be performed at all. Do not use it merely because coverage is partial.

Assign deterministic finding identifiers in root-relative file and source order: `TERM-001`, `SYM-001`, and `NUM-001`. Give each finding an exact file-and-line location when files are available; otherwise use the most stable section, equation, table, algorithm, caption, or quoted-text anchor available.

Use `ISSUE REPORTED` for a confirmed inconsistency. Use `AUTHOR DECISION REQUIRED` when the evidence cannot establish whether the compared usages refer to the same entity, concept, quantity, or experimental condition, or whether their difference is intentional. Keep conflict certainty separate from remediation: a confirmed conflict remains `ISSUE REPORTED` even when the author must still choose the replacement term, symbol, or value.

### Full-Manuscript Completeness Gate

Claim `FULL MANUSCRIPT` coverage only after all of the following are true:

1. Identify the authoritative root TeX file and resolve every statically reachable `\input`, `\include`, `\subfile`, `\import`, and equivalent include in document order.
2. Account for missing, conditional, macro-generated, generated, or cyclic includes and every notation-bearing appendix or supplement.
3. Inspect notation-producing user macros and custom math environments; do not rely on a preservation-script pass to expand or understand them.
4. Inspect notation and numerical claims in prose, equations, algorithms, captions, tables, and supplied figure assets. If an asset contains relevant embedded text but cannot be inspected, coverage is partial. If normalization affects a figure but editable source is unavailable, normalization is incomplete.
5. Retain root-relative file and line locations for findings and verify that no requested scope was skipped.

If any condition fails, state the coverage gap and use `Coverage: PARTIAL`. A complete file upload does not by itself establish full analytical coverage.

## Non-Negotiable Rules

- Preserve TeX structures, environments, citations, labels, references, bibliography keys, function names, module names, dataset names, metric names, and technical meaning.
- Preserve exact arguments and keys inside structural commands such as `\label{...}`, `\ref{...}`, `\eqref{...}`, `\includegraphics{...}`, citation commands, `\bibitem{...}`, and BibTeX keys. Do not rename, merge, delete, reorder, or normalize them.
- Treat comments and literal or code-like source, including `comment`, `verbatim`, listing environments, and inline literal commands, as exact protected source in every mode. Do not move prose into or out of these regions, change an inline comment into a whole-line comment, or move them across protected math or TeX structures.
- Preserve every original mathematical region and its document order during polishing, translation, prose addition, and verification. The only exception is an exact substitution listed in an author-approved notation mapping.
- Preserve every number, unit, percentage, dimension, parameter, sample size, table value, figure-reported value, significance marker, numerical-token order, and positive, negative, or plus-minus sign during polishing, translation, prose addition, verification, consistency auditing, and notation normalization. This includes digits embedded in identifiers and numerical tokens inside comments, literal examples, URLs, or protected command arguments. There is no numerical-edit exception in this skill, and `--allow-additions` does not relax this rule.
- Treat source-to-output preservation and source-internal consistency as separate checks. Source-internal terminology, symbol, value, unit, or sign conflicts are findings, not permission to edit.
- Never correct a suspicious value in this skill. After reporting a `NUM-*` finding, ask the user to revise the source externally and return an author-approved baseline.
- Do not alter mathematical definitions, theorem conditions, proof logic, algorithm steps, experimental settings, reported results, baselines, or datasets.
- Do not modify bibliography records or identifiers in this skill. A reference-cleanup request may authorize only non-numerical, non-identifier metadata edits that do not conflict with another protected rule; years, pages, volumes, issue numbers, DOI/URL/arXiv identifiers, and every other numerical token must be corrected outside paper-polisher and returned as an author-approved baseline.
- Do not invent claims, experiments, guarantees, deployment value, limitations, or conclusions.
- Do not vary technical terms merely for stylistic variety. Use canonical terms only when their entity mapping is supported.
- Avoid mechanical repetition in sentence openings, clause order, voice, transitions, and paragraph structure without changing protected content.
- Do not use dash punctuation in author-written manuscript prose. Preserve lexical hyphens, mathematical minus signs, signed values, protected keys, URLs, DOI strings, filenames, citation keys, and bibliography metadata exactly.

If a requested edit would violate these rules and is not covered by an exact approved mapping, stop that edit and report what authorization or source information is missing. If your own draft violates a rule, revise it before returning.

## Workflow

1. Select the mode from the user's explicit intent and identify the supplied scope.
2. For full-manuscript work, apply the completeness gate and preserve the resolved document order.
3. Build the relevant ledgers:
   - terminology: entity, canonical term, allowed contextual forms, definitions, and locations;
   - notation: mathematical entity, symbol, definitions and uses, scope, type or dimensions, frame, and aliases;
   - numerical: measured or configured quantity, value, unit, sign, condition, source location, and matching prose/table/figure uses.
4. In polishing mode, revise prose while keeping protected math and numerical-token order fixed. Reorder clauses or sentences only when doing so does not reorder protected math, numbers, units, or signs.
5. Run bidirectional consistency checks: entity to term or symbol, term or symbol to entity, and quantity or experimental condition to reported value, unit, and sign.
6. Run sentence-architecture, dash-free prose, objective-tone, and claim-boundary checks across the assessed scope.
7. When original and candidate files are available, run the preservation checker. Use project mode for a multi-file manuscript.
8. Return the mode-specific output and distinguish authorized changes, source-level findings, candidate-introduced deviations, and unassessed checks.

## Preservation Checker

For one original and candidate TeX file, run strict comparison:

```bash
python3 paper-polisher/scripts/check_preservation.py original.tex candidate.tex
```

Use `--allow-additions` only when the user authorized ordinary prose additions:

```bash
python3 paper-polisher/scripts/check_preservation.py original.tex candidate.tex --allow-additions
```

This option does not permit new, deleted, changed, or reordered structural keys, math regions, numerical tokens, units, or signs. Recognized comments and literal or code-like regions remain exact protected source, including their inline-versus-whole-line comment boundary and their order relative to protected math and TeX. Manually compare any custom or unrecognized literal macro. It does not authorize new figures, tables, equations, references, image assets, or symbol mappings. Establish an author-approved baseline for intentional protected structural changes, or use externally corrected and author-approved TeX as the new baseline when numerical content had to be corrected outside paper-polisher.

For a multi-file manuscript, pass the two authoritative root TeX files and enable project traversal:

```bash
python3 paper-polisher/scripts/check_preservation.py original/main.tex candidate/main.tex --project
```

Project mode resolves statically reachable `\input`, `\include`, `\subfile`, `\subfileinclude`, `\import`, `\subimport`, `\inputfrom`, `\subinputfrom`, `\includefrom`, and `\subincludefrom` directives from each root, including current and previous import-directory context. A missing, dynamic, or cyclic include fails the check and is also a completeness-gate gap.

For an approved notation mapping that is global throughout the checked scope, repeat `--approved-symbol-map` for each exact math-token substitution and protect TeX backslashes with shell single quotes:

```bash
python3 paper-polisher/scripts/check_preservation.py original.tex normalized.tex \
  --approved-symbol-map 'M=N' \
  --approved-symbol-map '\mathbf{P}=\mathbf{Q}'
```

This flag is normalization-only: non-math prose and every unmapped math token must remain unchanged, and numeric, currency, percentage, unit, or sign content is never authorized by a mapping. The parser rejects unambiguous numeric, currency, percentage, and sign mappings; ambiguous bare glyphs such as `m` still require the entity-aware authorization ledger and manual unit review. Do not combine it with `--allow-additions`. Because the CLI mapping is global within the checked scope, do not use it for an entity mapping with excluded or intentionally reused occurrences; validate those edits against the location-aware authorization ledger and establish an author-approved baseline instead.

Run the checker on manuscript files only, not on a response containing reports or commentary.

The checker cannot establish semantic source-internal consistency and may not understand notation or literal content generated by arbitrary user macros, unrecognized literal commands, custom math environments, figure assets, or unrecognized natural-language numerical and unit forms. Its numerical scan is fail-closed only for recognized decimal, English textual, contextual Roman, and Unicode numeric representations, plus recognized signs, significance markers, currencies, common units, and unit-like compounds when they occur in supported numeric/math/literal/macro anchors, TeX connectors, delimited forms, or explicit cue phrases. This is syntactic coverage, not a global semantic unit lexer. Manually compare every expression or context the checker does not recognize, including ambiguous standalone unit-like glyphs, and run the semantic numerical audit for every quantity-to-unit relationship. Apply the completeness gate and semantic audits separately.

## Output Formats

### Consistency-Only Audit

Return, regardless of manuscript length:

1. Audited scope and coverage gaps.
2. Separate terminology, notation, and numerical sections as applicable, each with `Coverage` and `Result`.
3. `TERM-*`, `SYM-*`, and `NUM-*` findings with locations, evidence, and a suggested mapping or author question when supportable.
4. A statement that no source content was changed.

### Verification

Return, regardless of manuscript length:

1. Inputs and comparison coverage, including whether the original was available.
2. Candidate-introduced deviations with locations and evidence.
3. Source-internal consistency findings in a separate section.
4. Comparative checks marked `NOT ASSESSED` when the original was unavailable.
5. A statement that the candidate was not modified.

### Approved Notation Normalization

Return the authoritative normalized TeX, an `AUTHORIZED CHANGE` list tied to the approved mapping, unresolved locations, and a strict unexpected-difference report. Do not produce a second rewritten version.

### Default Polishing

For a sentence, paragraph, or small excerpt, return the polished TeX-safe version and add a brief note only when a finding or limitation needs attention.

For a major section or full manuscript, return:

1. The authoritative TeX version.
2. A concise review report covering source preservation, technical fidelity, terminology, notation, numerical consistency, citations, sentence structure, dash-free prose, claim boundaries, and coverage.
3. A concise compliance note.

Generate a separate Markdown reading version only when the user explicitly requests it. The TeX artifact remains authoritative, and any Markdown rendering must not be treated as an independently editable manuscript version.

For comparative preservation and fidelity fields, select `PASS`, `ISSUE REPORTED`, or `NOT ASSESSED`. For citation/bibliography, also permit `NOT PRESENT`. For intrinsic style and output-completeness fields, select `PASS` or `ISSUE REPORTED`.

Use this core report structure and select one value per field:

```text
Review report:
- Source-to-output TeX/math preservation: <selected status>
- Technical and claim fidelity: <selected status>
- Numerical-token/unit/sign preservation: <selected status>
- Terminology consistency:
  Coverage: <selected coverage>
  Result: <selected result>
- Symbol/notation consistency:
  Coverage: <selected coverage>
  Result: <selected result>
- Source-internal numerical consistency:
  Coverage: <selected coverage>
  Result: <selected result>
- Citation and bibliography consistency: <selected status>
- Sentence structure, dash-free prose, and objective tone: <selected status>
- Output completeness: <selected status>
```

Replace every angle-bracket placeholder with one valid value from the shared protocol and the field-specific choices described above; never emit a placeholder or a list of alternatives. Report all comparative fields as `NOT ASSESSED` when no original exists.
