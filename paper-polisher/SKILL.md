---
name: paper-polisher
description: Polish, translate, or locally revise Chinese or English TeX academic manuscript text into formal, objective engineering-journal English while preserving equations, labels, references, citations, variables, environments, bibliography keys, numerical data, and technical meaning. Use for sentence-level, paragraph-level, section-level, or full-manuscript language polishing when the main task is faithful expression improvement rather than novelty audit, literature-review construction, or argument redesign.
---

# Paper Polisher

## Scope

Use this skill when the user asks for TeX-safe academic English polishing, translation, proofreading, terminology consistency, or faithful local revision.

For full papers, long sections, or strict style-guide requests, read `references/tex_safe_polishing.md` before rewriting. For Chinese-facing workflow guidance, `references/tex_safe_polishing_zh.md` is available as a companion reference. For short local edits, apply the core rules below and consult the reference only when preservation, terminology, or output format is uncertain.

Do not use this skill as the main tool for:

- research-idea novelty, contribution defensibility, dangerous baseline, or reviewer-attack audits; use `idea-novelty-auditor` (if available);
- literature review, related-work gap framing, reference selection, or citation-role assignment; use `problem-driven-literature-review` (if available);
- broad manuscript storyline, introduction structure, or experiment-to-claim redesign; use `paper-argument-reconstructor` (if available).

If the user asks for polishing plus literature review or argument reconstruction, preserve the source technical truth and use the relevant upstream skill first, then this skill for final TeX-safe language polishing.

## Verification Mode

This skill has two modes. By default it polishes as described above. When the input is text another tool or skill has already polished, translated, or rewritten, switch to verification mode instead of re-polishing:

- do not overwrite the other tool's wording;
- check it against this skill's rules: TeX/equation/citation/key preservation, numerical and data fidelity, terminology consistency, and claim boundaries (the same checks as the Review report);
- report only the deviations and their locations; fix one in place only if it breaks a hard rule.

The suite's value is faithful, bounded output, not a competing rewrite. Verify rather than replace what a stronger generator already produced.

## Non-Negotiable Rules

- Preserve all TeX structures, equations, environments, citations, labels, references, variables, function names, module names, dataset names, metric names, and technical meanings.
- Preserve the exact original arguments and keys inside structural commands, including `\label{...}`, `\ref{...}`, `\eqref{...}`, `\cite{...}`, `\citep{...}`, `\citet{...}`, `\bibitem{...}`, and BibTeX entry keys. Do not translate, rename, merge, delete, reorder, or normalize these keys.
- Do not change mathematical definitions, theorem conditions, proof logic, algorithm steps, experimental settings, reported results, baselines, dataset names, numerical values, units, percentages, table entries, figure-reported values, parameter settings, sample sizes, or significance markers.
- Do not modify bibliography entries, author names, reference-list formatting, BibTeX fields, DOI/URL/arXiv identifiers, venue names, years, pages, or publishers unless the user explicitly asks for reference cleanup after reviewing the issue.
- Do not invent contributions, claims, experiments, guarantees, deployment value, limitations, or conclusions that are not supported by the source text.
- Do not polish by word-for-word translation. First identify the sentence or paragraph function, then improve expression while preserving meaning.
- Do not vary technical terms for stylistic variety. Choose canonical terms for equivalent concepts and keep them consistent.

## Rule-Conflict Escalation

If a requested edit or seemingly necessary correction would violate a non-negotiable rule, stop and ask the user before making that edit.

If your own draft violates a rule, revise the draft to restore compliance without asking. Ask only when the desired change would require protected edits, unsupported claims, or technical interpretation that cannot be determined from the source.

## Workflow

1. Identify the text type: sentence, paragraph, named section, full manuscript, caption/table note, bibliography, or mixed TeX.
2. Identify each paragraph's local function: background, problem, method, formula explanation, result, discussion, conclusion, or transition.
3. Build a small terminology ledger for key methods, modules, metrics, variables, abbreviations, datasets, and baselines.
4. Rewrite in formal, restrained engineering-journal English while preserving all protected TeX structures, keys, data, and technical meaning.
5. Remove colloquial, subjective, exaggerated, and module-stacking phrasing when this can be done without adding unsupported content.
6. Run the post-polishing review before responding. If any violation is found, revise first.

## Preservation Script

When both original and polished TeX files are available, run:

```bash
python3 paper-polisher/scripts/check_preservation.py original.tex polished.tex
```

Use the script before finalizing full-paper or major-section polishing. Run it only on the original TeX content and the polished TeX content, not on an assistant response that also contains notes or review reports.

If the script reports changed TeX keys or numeric tokens, revise the polished text or flag the discrepancy explicitly.

## Output Format

For one sentence, one paragraph, or a small local excerpt, use:

1. Polished version.
2. Brief note only if needed for terminology, TeX preservation, data preservation, or claim fidelity.

For full papers, major sections, submission-oriented polishing, or strict style-guide requests, return:

1. Markdown version: polished text for reading and revision.
2. TeX version: TeX-safe version ready to paste back into the manuscript.
3. Review report: concise preservation and fidelity review.
4. Compliance note: concise confirmation of TeX preservation, terminology consistency, objective tone, and claim fidelity.

Use this review report pattern:

```text
Review report:
- TeX preservation: PASS
- Technical fidelity: PASS
- Numerical/data preservation: PASS
- Terminology consistency: PASS
- Citation and bibliography consistency: PASS / ISSUE REPORTED / NOT PRESENT
- Objective tone and claim boundaries: PASS
- Output completeness: PASS
```

Use this compliance note pattern:

```text
Compliance note:
- TeX structures, equations, labels, references, citations, bibliography keys, variables, and original command keys are preserved.
- Numerical values, units, datasets, baselines, metrics, and reported results are preserved.
- Terminology has been checked for consistency.
- Bibliography-entry issues are reported for review rather than edited automatically.
- No unsupported technical claims or experimental results have been introduced.
```
