---
name: paper-argument-reconstructor
description: Diagnose, restructure, or rewrite academic manuscript arguments into a problem-driven paper storyline. Use for abstracts, introductions, methodology narratives, formula explanations, theory/proof exposition, experiments, results, discussion, conclusions, contribution statements, section outlines, and full-paper diagnosis when the main task is argument design rather than pure language polishing, literature-review construction, or novelty-risk auditing.
---

# Paper Argument Reconstructor

## Scope

Use this skill when the user asks to improve a manuscript's logic, storyline, contribution framing, section structure, paragraph function, or experiment-to-claim alignment.

For full papers, major sections, introduction rewrites, contribution statements, or experiment-logic redesign, read `references/argument_reconstruction.md`. For Chinese-facing workflow guidance, `references/argument_reconstruction_zh.md` is available as a companion reference.

Use another skill when the task is primarily:

- TeX-safe expression polishing, proofreading, translation, or preservation checking: use `paper-polisher` (if available);
- idea novelty risk, dangerous baselines, reviewer attacks, or whether a contribution is defensible before manuscript writing: use `idea-novelty-auditor` (if available);
- literature review, related work, introduction background, research-gap synthesis, reference selection, citation-role assignment, or direct-competitor coverage: use `problem-driven-literature-review` (if available).

If the user asks for novelty audit, literature review, and manuscript reconstruction together, use `idea-novelty-auditor` (if available) first, then `problem-driven-literature-review` (if available), then reconstruct only the defensible claims.

## Verification Mode

This skill has two modes. By default it reconstructs as described above. When the input is an argument or section another tool or skill has already drafted or rewritten, switch to verification mode instead of regenerating:

- do not overwrite the other tool's wording;
- check it against this skill's rules: claim boundaries, contribution-to-evidence alignment, and whether any claim was strengthened beyond what the source supports;
- report only the deviations and their locations; fix one in place only if it breaks a hard rule.

The suite's value is faithful, bounded output, not a competing rewrite. Verify rather than replace what a stronger generator already produced.

## Non-Negotiable Rules

- Do not invent contributions, experiments, results, theory, guarantees, deployment value, limitations, or related-work facts.
- Preserve TeX structures, command keys, equations, citations, labels, variables, numerical values, datasets, metrics, baselines, and reported results when present.
- Do not rewrite a paper into a stronger claim than the source can support.
- Do not present an algorithm family, solver, or standard pipeline component as a new contribution unless the source explicitly supports that positioning.
- If novelty or related-work factual accuracy is uncertain, phrase claims cautiously or request/search for evidence instead of asserting priority.

## Workflow

1. Identify the core research problem, application scenario, technical bottleneck, and main claim.
2. Mark each paragraph's function: background, problem, gap, motivation, method, mechanism, theory, experiment, result interpretation, implication, or transition.
3. Build the paper's main chain:

```text
Real-world demand -> Technical bottleneck -> Limitation of existing methods -> Required capability -> Proposed framework -> Mechanism -> Evidence -> Implication
```

4. Check whether each section, module, formula, experiment, and result supports the core problem.
5. Reconstruct the target section around problem, gap, mechanism, evidence, and implication rather than a list of modules.
6. Keep claim boundaries faithful to the source. Flag missing evidence instead of filling it in.
7. If final language polishing is required, run a TeX-safe polishing pass with `paper-polisher` (if available).

## Section Targets

- Abstract: background, gap, proposed method, core mechanism, evidence, implication.
- Introduction: demand, bottleneck, gap, proposed approach, contributions, paper structure.
- Related Work: delegate detailed related-work drafting, citation selection, and literature-route synthesis to `problem-driven-literature-review` (if available).
- Methodology: each module introduced from a problem requirement, then mechanism and expected effect.
- Formula Explanation: why the formula is needed, what it defines, how it supports the method.
- Theory/Proof: assumptions, derivation logic, conclusion, and scope.
- Experiments: each experiment tied to a claim, module, metric, or deployment requirement.
- Results and Discussion: observation, mechanism, comparison, implication, limitation.
- Conclusion: return to the core problem, summarize evidence, state bounded future work.

## Output Modes

For diagnosis requests, return:

1. Core problem and main claim.
2. Current storyline issues.
3. Recommended argument chain.
4. Section-level revision plan.
5. Claim/evidence gaps to resolve.

For rewrite requests, return:

1. Reconstructed version.
2. Brief rationale for major structural changes.
3. Claim-boundary or missing-evidence notes, if needed.

For TeX manuscripts, preserve all protected TeX content and use `paper-polisher` (if available) for the final preservation-oriented pass if the user needs paste-ready polished TeX.
