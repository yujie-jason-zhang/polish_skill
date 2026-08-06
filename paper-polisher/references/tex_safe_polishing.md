# TeX-Safe Academic Polishing Guide

## Contents

- [Core Goal](#core-goal)
- [Source-to-Output Preservation](#source-to-output-preservation)
- [Structural Keys and Referenceable Objects](#structural-keys-and-referenceable-objects)
- [Faithful Language Revision](#faithful-language-revision)
- [Terminology Consistency](#terminology-consistency)
- [Mathematical Notation Consistency](#mathematical-notation-consistency)
- [Source-Internal Numerical Consistency](#source-internal-numerical-consistency)
- [Full-Manuscript Coverage](#full-manuscript-coverage)
- [Sentence Architecture and Dash Policy](#sentence-architecture-and-dash-policy)
- [Mode Workflows](#mode-workflows)
- [Preservation Checker](#preservation-checker)
- [Output Examples](#output-examples)

## Core Goal

Produce formal, restrained engineering-journal English without changing the manuscript's technical truth. Depending on the mode selected in `SKILL.md`, either polish the prose, verify a candidate against its source, audit terminology/notation/numerical consistency without editing, or apply only an exact author-approved notation mapping.

Keep four questions separate:

1. Did the candidate preserve protected source content?
2. Is the source internally consistent in terminology?
3. Is the source internally consistent in mathematical notation?
4. Does the source report each numerical fact, unit, and sign consistently?

A preservation pass does not answer the three semantic consistency questions. A source-level inconsistency does not authorize a correction.

## Source-to-Output Preservation

Preserve exactly:

- inline and display math, including `$...$`, `\(...\)`, `\[...\]`, and named math environments;
- figure, table, algorithm, theorem, proof, lemma, definition, and remark environments;
- structural commands and their arguments, including labels, references, citations, bibliography keys, and image paths;
- comments and literal or code-like source, including comment/verbatim/listing environments and inline literal commands, together with inline-versus-whole-line comment boundaries and their order relative to protected math and TeX;
- variable and function notation unless an exact substitution appears in an author-approved symbol mapping;
- numerical values, numerical-token order, units, percentages, dimensions, sample sizes, parameter settings, table values, figure-reported values, significance markers, and positive, negative, or plus-minus signs;
- technical meaning, conditions, assumptions, algorithms, proof steps, experiments, baselines, datasets, metrics, and results.

This hard numerical rule applies in polishing, translation, ordinary prose addition, verification, consistency auditing, and notation normalization. It covers digits embedded in identifiers and numerical tokens inside comments, literal examples, URLs, and protected command arguments. Do not insert, delete, change, or reorder a number merely to improve prose flow. Reorder a clause or sentence only when its protected math and numerical tokens remain in the same document order. This skill has no numerical-edit exception. If a value must be corrected, ask the user to revise it outside paper-polisher and provide the corrected TeX as a new author-approved baseline.

The preservation checker treats each recognized comment and literal/code region as exact protected source in every mode. Do not turn active prose into a comment, move text into or out of a literal region, change an inline `%` into a whole-line comment, or move such a region across protected math or TeX structures. This protects TeX comment-newline semantics as well as the visible source payload. Manually compare custom or unrecognized literal macros.

Preserve command arguments and keys exactly. For example:

```latex
\label{sec:method}
\ref{sec:method}
\eqref{eq:risk}
\cite{smith2023,chen2024}
```

must not become:

```latex
\label{sec:methodology}
\ref{method}
\eqref{eq:risk_metric}
\cite{Smith2023}
```

Do not silently repair a suspicious value, unit, sign, citation, bibliography entry, or author-name order. Report it. Never change numerical content in this skill or infer the intended value from a neighboring table, trend, conversion, or expected result. Ask the user to supply externally corrected TeX as a new baseline.

## Structural Keys and Referenceable Objects

When the user explicitly requests a new referenceable object, first follow the manuscript's label convention. If none exists, use a semantic typed label:

| Object | Prefix | Example |
|---|---|---|
| Section | `sec:` | `\label{sec:method}` |
| Subsection | `subsec:` | `\label{subsec:ablation_setup}` |
| Figure | `fig:` | `\label{fig:framework}` |
| Table | `tab:` | `\label{tab:diff_methods}` |
| Equation | `eq:` | `\label{eq:loss_function}` |
| Algorithm | `alg:` | `\label{alg:training}` |
| Theorem | `thm:` | `\label{thm:convergence}` |
| Appendix | `app:` | `\label{app:implementation}` |

Keep an established underscore convention when present, such as `\label{tab_diff_methods}`. Never emit bare placeholders such as `\label{tab}`, `\ref{tab}`, `\label{fig}`, `\ref{fig}`, `\label{tmp}`, or `\label{label}`.

After the user approves a new label, reference, image path, sizing option, or cropping option, protect it exactly. A newly requested table, figure, equation, citation, asset, or other structural object does not become permissible under `--allow-additions`; approve the resulting manuscript as a new baseline before subsequent strict comparison.

When referring to an existing object, inspect its exact label. If a manuscript contains:

```latex
\label{tab:ablation}
\label{tab:errors}
\label{tab:torwic_errors}
```

then a paragraph about the controlled indoor evaluation may use:

```latex
Tables~\ref{tab:ablation} and~\ref{tab:errors}
```

Do not replace the exact targets with generic labels or include an unrelated table.

Use the manuscript or journal's established reference-name style, such as `Fig.` versus `Figure`, `Eq.` versus `Equation`, and `Sec.` versus `Section`. Never hard-code displayed numbers such as `Figure 1` or `Table 1`. Captions must also omit the generated object name and number:

```latex
\caption{Overall framework of the proposed method.}
```

For a new figure, protect both the approved label and asset signature:

```latex
\begin{figure}
  \centering
  \includegraphics[width=0.85\linewidth]{figures/framework.pdf}
  \caption{Overall framework of the proposed method.}
  \label{fig:framework}
\end{figure}
```

Do not simplify the path, replace the file, or alter approved image options without explicit authorization and a new baseline.

## Faithful Language Revision

Allowed prose edits include:

- splitting an overlong sentence;
- merging redundant wording;
- adding a light transition already implied by the source;
- replacing colloquial wording with formal academic language;
- making local logic explicit without adding technical content;
- reordering prose-only clauses or sentences when no protected math, structural key, number, unit, or sign changes order.

Forbidden edits include:

- changing definitions, assumptions, algorithms, proofs, formulas, or experimental settings;
- adding experiments, guarantees, limitations, applications, or deployment claims;
- presenting correlation as causation;
- expanding a local result into a general superiority claim;
- converting a heuristic into a theoretical guarantee;
- altering baselines, datasets, metrics, values, units, signs, or reported results.

## Terminology Consistency

Build a terminology ledger for a terminology-dense section or full manuscript:

| Entity or concept | Canonical term/family | Definition locations | Use locations | Allowed contextual forms | Avoid or reserve for |
|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... |

Check both directions:

- one entity expressed through multiple terms without an explicit distinction;
- one term used for different entities in the same or overlapping scope.

Do not replace a technical term merely for stylistic variety. Distinguish related but non-equivalent terms such as `open-vocabulary`, `open-set`, and `open-world`, or `risk-aware`, `safety-aware`, and `uncertainty-aware`, according to the manuscript's definitions.

Report terminology findings with `TERM-*` identifiers and use the shared Coverage/Result protocol from `SKILL.md`. A recommended term is provisional unless the manuscript clearly establishes it or the author approves it.

## Mathematical Notation Consistency

Treat notation as a bidirectional mapping between mathematical entities and rendered symbols. Build a ledger:

| Mathematical entity | Symbol | Definition locations | Use locations | Scope | Type/dimensions | Frame | Explicit aliases |
|---|---|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... | ... | ... |

Check both directions:

- **Entity to symbol:** the same object appears under multiple symbols, such as one transform denoted by `M` in one section and `N` in another.
- **Symbol to entity:** the same rendered symbol denotes different objects in the same or overlapping scopes.

Compare explicit definitions, descriptive prose, operand roles, types, dimensions, frames, units, and equation dependencies. Inspect case, font family or weight, accents, primes, subscripts, and superscripts because these may encode identity rather than cosmetic style.

Do not report a conflict merely because a glyph is reused as:

- a local dummy variable, loop index, or summation index;
- an explicitly defined alias;
- a deliberately distinct time step or coordinate-frame quantity;
- a value in a clearly nonoverlapping local scope.

When the evidence establishes a conflict, report it as `ISSUE REPORTED` even if the author must choose the preferred symbol. Use `AUTHOR DECISION REQUIRED` when the entity identity or intended notation itself is ambiguous. Keep the proposed canonical choice in a separate field.

### Applying an Approved Mapping

Before editing, record the exact authorization:

| Finding | Entity | Old symbol | Approved symbol | Included locations/scope | Aliases or exclusions |
|---|---|---|---|---|---|
| `SYM-...` | ... | ... | ... | ... | ... |

Then:

1. Change only mapped symbol occurrences.
2. Update every affected TeX-visible definition and use in equations, prose, algorithms, captions, tables, and appendices.
3. Keep numbers, units, dimensions, signs, structural keys, and unrelated math unchanged and in order.
4. List every substitution as `AUTHORIZED CHANGE` and fail or report every unmapped difference.
5. Inspect affected notation embedded in figures. If editable source is unavailable, report the unresolved asset and do not claim complete normalization.
6. Use mapping-aware validation when supported. Otherwise, have the author approve the normalized TeX as a new baseline before any later polishing, then compare later drafts strictly against that baseline.

For a combined normalization-and-polishing request, finish and approve this mapping-only stage first. Use its approved output as the source for a separate prose-polishing stage; never present a combined prose and symbol diff as mapping-only validation.

Do not use ordinary additions-aware checking to excuse notation edits.

## Source-Internal Numerical Consistency

Build a numerical ledger for every important reported or configured quantity:

| Quantity or fact | Value | Unit | Sign/direction | Condition or experiment | Locations | Related table/figure |
|---|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... | ... |

Check whether the same quantity and condition are reported consistently across:

- abstract, main text, conclusion, and appendix;
- method settings and experiment settings;
- prose, tables, captions, and supplied figures;
- sample counts, splits, epochs, dimensions, thresholds, and hyperparameters;
- raw values, percentages, deltas, confidence intervals, uncertainty notation, and significance markers;
- units, unit prefixes, positive/negative direction, and `\pm` or equivalent signs.

Do not compare numbers without first matching the metric, dataset, split, condition, aggregation, and rounding convention. A rounded summary, unit conversion, per-split result, or differently signed convention may be legitimate. If equivalence cannot be established, use `AUTHOR DECISION REQUIRED` rather than guessing.

Use `NUM-*` for findings. A clear mismatch, such as the same test-set accuracy reported as `91.2\%` in a table and `92.1\%` in the prose under the same condition, is `ISSUE REPORTED`. Do not change either value. Ask the user to correct and confirm the source outside this skill, then provide the corrected TeX as a new baseline.

Numerical consistency auditing is source-internal. It does not weaken source-to-output preservation: even a visibly suspicious number must remain unchanged in a polish or notation-normalization output.

## Full-Manuscript Coverage

Use the completeness gate in `SKILL.md` before claiming `Coverage: FULL MANUSCRIPT`.

Start from an authoritative root file and retain resolved document order. Follow statically resolvable `\input`, `\include`, `\subfile`, `\import`, and project-specific equivalents. Record unresolved conditional includes, macro-generated paths, missing generated tables, separate supplements, and cycles as coverage gaps.

Inspect all notation-producing macro definitions and uses, not only macros changed between two drafts. Identify custom math environments and notation embedded in algorithms or diagram code. A checker that preserves macro text still cannot determine whether the source uses the rendered entity consistently.

For supplied figure assets, inspect visible variable names, units, legends, and reported values when they are part of the requested audit. If relevant embedded content cannot be inspected, use partial coverage. If normalization requires editing embedded labels but an editable source asset is unavailable, leave the asset unchanged and report that normalization is incomplete.

Use root-relative `file:line` locations. If the input is pasted text, anchor findings to section/equation/table labels and a short identifying excerpt. Assign `TERM-*`, `SYM-*`, and `NUM-*` in deterministic source order within each prefix.

## Sentence Architecture and Dash Policy

Avoid mechanically repeating the same opener, subject-predicate frame, clause order, voice, transition, result template, or paragraph opening. Preserve intentional parallelism when it supports comparison or enumeration. Vary structure according to logic without replacing canonical technical terms or moving protected math and numerical tokens.

Do not use dash punctuation in author-written manuscript prose, including titles, headings, abstracts, captions, notes, footnotes, acknowledgments, and appendices. Replace an em dash or en dash according to its role with apposition, a content clause, relative clause, colon, semicolon, parentheses, conjunction, or separate sentence.

Do not confuse prose dashes with protected forms. Preserve lexical hyphens in established compounds, hyphens in keys/URLs/DOIs/filenames/citation keys, and every mathematical minus or signed value. For example, keep `risk-aware`, `$a-b$`, `$-1$`, `-3.2 dB`, and `mean \pm std` exactly when they appear in the source.

## Mode Workflows

### Local Polishing

1. Identify the local rhetorical function.
2. Preserve TeX, math, keys, numbers, units, signs, and facts.
3. Polish for objective academic English without moving protected tokens.
4. Check visible terminology, notation, and numerical consistency.
5. Report local findings with `Coverage: PARTIAL`; a locally clean scope may still have `Result: PASS`.

### Full-Manuscript Polishing

1. Resolve the project and apply the completeness gate.
2. Build terminology, notation, numerical, and structural ledgers.
3. Polish section by section while maintaining protected-token order.
4. Run all three source-internal consistency audits.
5. Run manuscript-wide style, claim-boundary, and dash checks over the assessed scope.
6. Run strict source comparison, using project mode for a multi-file manuscript.
7. Return one authoritative TeX artifact plus the review report. Add Markdown only if explicitly requested.

### Verification

1. Record whether both original and candidate are available.
2. If both exist, compare protected TeX/math, structural keys, numbers/units/signs, technical meaning, and claims.
3. If the original is missing, mark all comparative fields `NOT ASSESSED` and perform only intrinsic candidate checks.
4. Separate candidate-introduced deviations from source-internal `TERM-*`, `SYM-*`, and `NUM-*` findings.
5. Report only. Do not modify the candidate.

### Consistency-Only Audit

1. Apply the completeness gate and state assessed scope.
2. Build only the ledgers relevant to the request.
3. Return Coverage and Result separately for terminology, notation, and numerical consistency as applicable.
4. Provide findings and author questions without editing source content.

### Approved Notation Normalization

1. Require an exact approved mapping; otherwise remain in audit mode.
2. Apply only mapped substitutions and retain an authorization ledger.
3. Report unresolved macros, custom environments, generated files, or figure assets.
4. Validate all differences, listing approved substitutions as `AUTHORIZED CHANGE`.
5. Return one authoritative TeX artifact and no independent rewrite.

## Preservation Checker

For a single file, run strict comparison:

```bash
python3 paper-polisher/scripts/check_preservation.py original.tex candidate.tex
```

For ordinary prose additions only:

```bash
python3 paper-polisher/scripts/check_preservation.py original.tex candidate.tex --allow-additions
```

`--allow-additions` does not permit structural-key, image-asset, math-region, numerical-token, unit, or sign additions, deletions, changes, or reordering. It is not a notation-normalization mode.

For a multi-file manuscript, pass both authoritative root TeX files:

```bash
python3 paper-polisher/scripts/check_preservation.py original/main.tex candidate/main.tex --project
```

Project mode follows statically reachable `\input`, `\include`, `\subfile`, `\subfileinclude`, `\import`, `\subimport`, `\inputfrom`, `\subinputfrom`, `\includefrom`, and `\subincludefrom` directives from each root and preserves current and previous import-directory context. Missing, dynamic, or cyclic includes fail and must also be recorded as semantic coverage gaps.

The automated numerical scan covers only recognized decimal, English textual, contextual Roman, and Unicode numeric representations, plus recognized signs, significance markers, currencies, common units, and unit-like compounds in supported numeric/math/literal/macro anchors, TeX connectors, delimited forms, or explicit cue phrases. This is syntactic coverage, not a global semantic unit lexer. Manually compare every form or context the checker does not recognize, including ambiguous standalone unit-like glyphs. A checker pass never replaces this manual preservation review or the quantity-to-unit semantic audit required above.

For a mapping that applies globally throughout the checked scope, repeat the normalization-only mapping option as needed and quote TeX backslashes:

```bash
python3 paper-polisher/scripts/check_preservation.py original.tex normalized.tex \
  --approved-symbol-map 'M=N' \
  --approved-symbol-map '\mathbf{P}=\mathbf{Q}'
```

With any `--approved-symbol-map`, non-math prose and every unmapped math token must remain unchanged; numeric, currency, percentage, unit, and sign content is never authorized. The parser rejects unambiguous numeric, currency, percentage, and sign mappings, while ambiguous bare glyphs still require the entity-aware ledger and manual unit review. Do not combine this normalization-only option with `--allow-additions`. The CLI mapping is global within the checked scope, so use the location-aware authorization ledger and an author-approved baseline instead when a glyph has intentional exclusions or unrelated reuse.

Do not concatenate a report or commentary with the TeX input.

Checker success establishes only syntactic source-to-output preservation within the checker's supported constructs. Apply the semantic audits and coverage gate independently.

## Output Examples

Use the status meanings defined once in `SKILL.md`. Do not redefine them locally or emit slash-separated template choices.

Example consistency finding:

```text
Symbol/notation consistency:
Coverage: PARTIAL
Result: ISSUE REPORTED

SYM-001 | ISSUE REPORTED
Entity: camera-to-world homogeneous transform
Locations: sections/method.tex:84; sections/evaluation.tex:31
Evidence: both definitions have the same direction, dimensions, frame, and downstream role, but use \mathbf{M} and \mathbf{N}
Suggested canonical choice: unresolved; author selection required
Action: REPORT ONLY
```

Example numerical finding:

```text
Source-internal numerical consistency:
Coverage: FULL MANUSCRIPT
Result: ISSUE REPORTED

NUM-001 | ISSUE REPORTED
Quantity: test-set accuracy under the full-data setting
Locations: tables/main.tex:22 reports 91.2\%; sections/results.tex:47 reports 92.1\%
Evidence: same dataset, split, method variant, metric, and aggregation
Required author action: correct and confirm the source externally, then provide a new baseline
Action: REPORT ONLY
```

Example verification without an original:

```text
Verification inputs:
- Candidate: available
- Original: unavailable

Source-to-output TeX/math preservation: NOT ASSESSED
Technical and claim fidelity: NOT ASSESSED
Numerical-token/unit/sign preservation: NOT ASSESSED
Candidate modification: NONE
```
