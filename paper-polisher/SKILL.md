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
- Do not invent contributions, claims, experiments, guarantees, or deployment value that the source text does not support.
- Do not polish by word-for-word translation. First identify the function of each paragraph and its role in the paper's argument.

## Workflow

1. Identify the core research problem, application scenario, technical bottleneck, and main claim.
2. Mark each paragraph's function: background, problem, gap, motivation, method, mechanism, theory, experiment, result interpretation, or implication.
3. Build or infer a terminology map for key methods, modules, metrics, variables, and abbreviations; keep terminology consistent.
4. Reconstruct the argument before sentence-level polishing. Use a storyline such as:

```text
Core problem -> Specific challenge -> Required capability -> Proposed module -> Mechanism -> Evidence -> Implication
```

5. Rewrite in formal, objective academic English. Prefer precise mechanism-oriented language over exaggerated or subjective claims.
6. Check every formula, module, experiment, and conclusion against the core problem. Remove module-stacking phrasing when possible.
7. Run the post-polishing review before responding. If any violation is found, revise the polished text first and review it again.
8. Verify TeX preservation, terminology consistency, claim fidelity, objective tone, and style-guide compliance before responding.

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

- TeX preservation: equations, environments, labels, references, citations, variables, and structural command keys are unchanged.
- Technical fidelity: no mathematical, algorithmic, experimental, or claim-level meaning has been changed.
- Terminology consistency: key terms, module names, metrics, variables, and abbreviations are used consistently.
- Problem-driven storyline: each section, paragraph, module, formula, experiment, and conclusion serves the core research problem.
- Section compliance: the rewritten title, abstract, introduction, methodology, formula explanations, experiments, results, and conclusion follow the relevant guidance.
- Tone and claims: language is objective, restrained, academic, and free of unsupported or exaggerated claims.
- Output completeness: Markdown version, TeX version, review report, and compliance note are present unless the user requested a different format.

If a check fails, correct the polished text before returning it. If a check cannot be fully verified because the source is incomplete, state the limitation explicitly instead of marking it as passed.

## Output Format

Unless the user requests another format, return:

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
- The language has been revised toward an objective engineering-journal style.
- The problem-driven storyline has been checked across the relevant sections.
- No unsupported technical claims or experimental results have been introduced.
```
