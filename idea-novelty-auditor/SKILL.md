---
name: idea-novelty-auditor
description: Audit research ideas, contribution statements, manuscript positioning, and proposed paper storylines for novelty risk before packaging. Use for comparing an idea against classic algorithmic paradigms, direct related work, adjacent fields, dangerous baselines, reviewer attacks, defensible claim boundaries, required experiments, ablation design, and deciding whether an idea can support a short paper, conference paper, or journal paper.
---

# Idea Novelty Auditor

## Scope

Use this skill when the user asks whether a research idea is novel, defensible, worth writing, how to position it, what baselines may invalidate it, how reviewers may attack it, what claims should be avoided, or what experiments are required before packaging.

For a full audit, read `references/idea_novelty_risk_audit.md`.

Use another skill when the task is primarily:

- literature review, related work, reference selection, citation-role assignment, or direct-competitor coverage after the idea boundary is known: use `problem-driven-literature-review` (if available);
- manuscript structure or section rewriting after the defensible claims are known: use `paper-argument-reconstructor` (if available);
- TeX-safe academic English polishing: use `paper-polisher` (if available).

If the user asks for "packaging" before novelty has been checked, run the novelty-risk audit first.

## Verification Mode

This skill has two modes. By default it audits as described above. When the input is a positioning, claim, or contribution statement another tool or skill has already drafted, switch to verification mode instead of re-auditing from scratch:

- do not overwrite the other tool's wording;
- check it against this skill's discipline: whether novelty is overstated, whether a dangerous baseline was missed, and whether any claim is stronger than the evidence allows;
- report only the deviations; tighten an overclaim in place only if it breaks the evidence discipline.

The suite's value is bounded, defensible claims, not a competing rewrite. Verify rather than replace what a stronger generator already produced.

## Core Principle

Audit before packaging:

```text
break it down -> compare with known paradigms -> identify dangerous baselines -> define what cannot be claimed -> define cautious claims -> design evidence -> then package the paper story
```

## Workflow

1. Restate the idea in one application-level sentence.
2. Remove application nouns and abstract it into general algorithmic paradigms.
3. Check four related-work layers:
   - direct task/workflow competitors;
   - adjacent fields with similar problem structure;
   - classic algorithmic paradigms;
   - dangerous baselines that could make the contribution collapse.
4. Build a similarity matrix against the most threatening methods.
5. Attack the idea from a reviewer perspective.
6. Classify the idea into weakest version, defensible version, and strengthened version.
7. Define what the paper must not claim.
8. Define what it can cautiously claim under specific conditions.
9. Design experiments, baselines, ablations, and failure-case analysis that would support the defensible claim.
10. Recommend the paper positioning and next minimum validation.

## Evidence Discipline

Do not assert that an idea is novel merely because it sounds specialized. If current literature accuracy matters, verify with literature search or ask the user for the relevant related-work set.

Do not turn a standard solver, classic paradigm, or application-specific implementation into the main novelty unless the defensible distinction is explicit.

When evidence is incomplete, use risk language:

- `high novelty risk`;
- `likely incremental unless ...`;
- `defensible only if ...`;
- `cannot claim ...`;
- `can cautiously claim ...`.

## Output Format

For a full audit, return:

```text
Idea:
- ...

Abstract paradigm:
- ...

Closest classic methods:
- ...

Dangerous direct/adjacent work:
- ...

Novelty risk:
- High / Medium / Low

Weakest version:
- ...

Defensible version:
- ...

Strengthened version:
- ...

Cannot claim:
- ...

Can cautiously claim:
- ...

Must-beat baselines:
- ...

Required experiments and ablations:
- ...

Recommended paper positioning:
- ...

Next minimum validation:
- ...
```

For quick checks, return only the risk level, most dangerous baseline, defensible claim, and minimum experiment.
