---
name: paper-polisher
description: Polish, rewrite, or restructure Chinese or English TeX academic papers and manuscript sections into formal, objective engineering-journal English. Use for abstracts, introductions, related work, methodology, formula explanations, theory/proof sections, experiments, results, discussion, conclusions, terminology consistency, problem-driven argument reconstruction, and TeX-safe editing that preserves equations, labels, references, citations, variables, environments, and technical meaning.
---

# Paper Polisher

## Use This Skill For

Use this skill when the user asks to polish, translate, rewrite, restructure, or improve an academic paper, TeX manuscript, or manuscript section. The expected output is formal engineering-journal English with a clear problem-driven argument.

For full-paper polishing, section-level rewriting, or any request that asks for strict style-guide compliance, read `references/polish_integrated.md` before rewriting. For short paragraph polishing, use the core rules below and consult the reference when terminology, structure, or claim boundaries are uncertain.

## Non-Negotiable Rules

- Preserve all TeX structures, equations, environments, citations, labels, references, variables, function names, module names, and technical meanings.
- Preserve the exact original arguments and keys inside structural commands, including `\label{...}`, `\ref{...}`, `\eqref{...}`, `\cite{...}`, `\citep{...}`, and `\citet{...}`. Do not translate, rename, merge, delete, reorder, or normalize these keys.
- Do not change mathematical definitions, algorithm steps, experimental settings, theorem conditions, proof logic, or reported results.
- Do not alter source data, including numerical values, units, percentages, statistics, table entries, figure-reported values, metric names, parameter settings, baselines, dataset names, sample sizes, or significance markers. If a value appears inconsistent, flag it instead of correcting it silently.
- Do not require or invent missing bibliography entries. When references, `\bibitem` entries, BibTeX entries, or `.bib` content are present, preserve them and check consistency of citation keys, author names, title spelling, venue names, years, pages, DOI/URL/arXiv identifiers, and publishers. Report any bibliography-entry or reference-list formatting issue for user review; do not modify bibliography entries, author names, reference-list formatting, or BibTeX fields unless the user explicitly approves that reference cleanup after reviewing the issue.
- Do not invent contributions, claims, experiments, guarantees, or deployment value that the source text does not support.
- Do not polish by word-for-word translation. First identify the function of each paragraph and its role in the paper's argument.
- Do not vary technical terms for stylistic variety. For each key technical concept, choose a canonical term or term family based on the domain context, and use the same form in equivalent contexts unless the text explicitly distinguishes different concepts or technical roles.

## Rule-Conflict Escalation

If a requested edit or seemingly necessary correction would conflict with any non-negotiable rule, stop and ask the user before making that edit. Do not silently override the rule. This includes changing protected TeX keys, formulas, algorithms, experimental settings, numerical data, reported results, bibliography entries, BibTeX fields, or unsupported claims.

If the agent's own draft violates a rule, revise the draft to restore compliance without asking the user. Ask the user only when the desired change would require breaking a rule, when the correct technical or bibliographic form cannot be determined from the source, or when the user explicitly requests a protected change.

## Workflow

1. Identify the core research problem, application scenario, technical bottleneck, and main claim.
2. Mark each paragraph's function: background, problem, gap, motivation, method, mechanism, theory, experiment, result interpretation, or implication.
3. Build or infer a terminology map for key methods, modules, metrics, variables, and abbreviations; choose canonical terms or term families for ambiguous source terms and keep them consistent across equivalent contexts.
4. Reconstruct the argument before sentence-level polishing. Use a storyline such as:

```text
Core problem -> Specific challenge -> Required capability -> Proposed module -> Mechanism -> Evidence -> Implication
```

5. Rewrite in formal, objective academic English. Prefer precise mechanism-oriented language over exaggerated or subjective claims.
6. Check every formula, module, experiment, and conclusion against the core problem. Remove module-stacking phrasing when possible.
7. Run the post-polishing review before responding. If any violation is found, revise the polished text first and review it again.
8. Verify TeX preservation, terminology consistency, claim fidelity, objective tone, and style-guide compliance before responding.

## Preservation Script

When both original and polished TeX files are available, run `scripts/check_preservation.py original.tex polished.tex` before finalizing full-paper or major-section polishing. If the script reports changed TeX keys or numeric tokens, revise the polished text or flag the discrepancy explicitly. Use this script only on the original TeX content and the polished TeX content, not on a full assistant response that also contains review reports or notes.

## Section Guidance

- Abstract: state background, gap, proposed method, core mechanism, evidence, and implication.
- Introduction: move from real-world demand to technical bottleneck, gap, proposed framework, contributions, and paper structure.
- Related Work: organize by method families or limitations, not as a chronological citation list.
- Methodology: introduce each module from a problem requirement, then explain mechanism and expected effect.
- Formula Explanation: explain why the formula is needed before the formula, then define symbols and mechanism after it.
- Theory/Proof: keep assumptions, derivations, and conclusions objective and verifiable.
- Experiments: connect each experiment to a claim, module, metric, or deployment requirement.
- Results and Discussion: report observations, explain mechanisms, connect back to the core problem, and state practical meaning.
- Conclusion: return to the core problem, summarize method and evidence, then give specific future work.

## Post-Polishing Review

After polishing, review the result against the source text and the style guide before returning the final answer.

Check:

- TeX preservation: equations, environments, labels, references, citations, bibliography keys, variables, and structural command keys are unchanged.
- Technical fidelity: no mathematical, algorithmic, experimental, numerical, data-level, or claim-level meaning has been changed.
- Citation and bibliography consistency: citation style follows the selected venue/source convention; existing bibliography entries are checked for inconsistent author names, title spelling, venue names, years, pages, DOI/URL/arXiv identifiers, and duplicate or conflicting entries, and bibliography-entry or reference-list formatting issues are reported for user review rather than edited automatically.
- Terminology consistency: key terms, module names, metrics, variables, and abbreviations are used consistently; variants are justified by distinct concepts, grammatical roles, or technical roles rather than stylistic variety.
- Problem-driven storyline: each section, paragraph, module, formula, experiment, and conclusion serves the core research problem.
- Section compliance: the rewritten title, abstract, introduction, methodology, formula explanations, experiments, results, and conclusion follow the relevant guidance.
- Tone and claims: language is objective, restrained, academic, and free of unsupported or exaggerated claims.
- Output completeness: the response follows the selected output mode. Short local edits use the lightweight format; full papers, major sections, submission-oriented polishing, and strict style-guide requests use the full four-part format unless the user requests otherwise.

If a check fails, correct the polished text before returning it. The exception is bibliography-entry or reference-list formatting issues: report those for user review and do not edit the bibliography entries unless the user explicitly approves reference cleanup. If a check cannot be fully verified because the source is incomplete, state the limitation explicitly instead of marking it as passed.

## Output Format

For short paragraph polishing, sentence-level polishing, or local revision requests, use a lightweight output format unless the user requests the full report.

Treat a request as a short local edit when the input is one sentence, one paragraph, or a small excerpt that is not a complete manuscript section and normally does not require section-level argument reconstruction. If the input is a complete abstract, introduction subsection, methodology subsection, experiment discussion, conclusion, or any named manuscript section, use the full-paper/major-section output mode even if the text is short.

1. Polished version.
2. Brief note, only if needed, on terminology, TeX preservation, data preservation, or claim fidelity.

Do not return the full Markdown version, TeX version, review report, and compliance note for short local edits unless explicitly requested. Still run the post-polishing review internally before responding.

For full papers, major sections, submission-oriented polishing, or strict style-guide compliance requests, return:

1. Markdown version: polished text for reading and revision.
2. TeX version: TeX-safe version ready to paste back into the manuscript.
3. Review report: a short post-polishing review against the style guide.
4. Compliance note: a short checklist confirming TeX preservation, terminology consistency, objective tone, problem-driven structure, and claim fidelity.

Use this review report pattern:

```text
Review report:
- TeX preservation: PASS
- Technical fidelity: PASS
- Terminology consistency: PASS
- Citation and bibliography consistency: PASS / ISSUE REPORTED / NOT PRESENT
- Problem-driven storyline: PASS
- Section-level guidance: PASS
- Objective tone and claim boundaries: PASS
- Output completeness: PASS
```

Use this compliance note pattern:

```text
Compliance note:
- TeX structures, equations, labels, references, citations, and their original keys are preserved.
- Terminology has been checked for consistency.
- Citation and bibliography consistency has been checked when reference content is present; bibliography-entry issues are reported for user review rather than edited automatically.
- The language has been revised toward an objective engineering-journal style.
- The problem-driven storyline has been checked across the relevant sections.
- No unsupported technical claims or experimental results have been introduced.
```
