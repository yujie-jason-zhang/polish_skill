---
name: experiment-section-auditor
description: Audit and constrain a paper's experiment section — experiment and ablation design, plus results narration — without leading the design. Use when the user is building or revising experiments, ablations, or results writeup and wants a check that (1) every experiment and ablation maps to a main claim, (2) the set is the minimal one that argues that line under the user's real equipment, data, and time, and (3) results are narrated as claim-tied argument rather than a flat report of numbers. This skill audits the user's plan or draft and proposes only minimal additions needed to close gaps; it does not invent experiments, assume feasibility it cannot verify, fabricate results, or explain away anomalies. It assesses feasibility only against resources the user states. Defer abstract/introduction contribution framing to paper-argument-reconstructor, novelty and claim boundaries to idea-novelty-auditor, and language polishing to paper-polisher.
---

# Experiment Section Auditor

## Scope

Use this skill when the user is designing, revising, or writing the experiment section and wants a constraint layer — not an author. It covers two things and only these two:

- experiment and ablation design: whether the study actually argues the paper's main line, and what the minimal set is under real resource limits;
- results narration: whether results are written as argument tied to claims rather than as a report of numbers.

Read `references/experiment_section_guide.md` for the claim–evidence mapping method, the minimal-set-under-constraints procedure, the ablation discipline, the report-style-versus-argument checklist with rewrite examples, and the output template. For a quick check, the rules below are enough.

Use another skill when the task is primarily:

- how the contribution — including the one-line results summary in the abstract or introduction — is framed: use `paper-argument-reconstructor` (if available). Pull the paper's claims from there and audit the experiments against them. That skill owns the abstract/intro wording; this one owns the results narration inside the experiment section. They must stay consistent: the abstract's results sentence must not claim more, or under looser conditions, than the section supports;
- whether the idea is novel or what can be claimed at all: use `idea-novelty-auditor` (if available). That fixes the defensible claims; this checks the experiments that support them;
- TeX-safe or final-language polishing of the section: use `paper-polisher` (if available);
- choosing a target journal: use `journal-recommender` (if available).

This skill does not lead the experiment design and does not write the section for the user. It audits, flags, and proposes the minimum needed to support the claims. The user drives.

## Verification Mode

This skill is audit-first in both modes; what changes is how much it proposes.

- Default (the user's own plan or draft): audit against the rules below, flag gaps and report-style narration, and propose only the minimal experiment or ablation needed to close each gap. Do not rewrite the section or design a full campaign.
- Strict verification (an experiment plan or narration another tool or skill already produced): do not propose a competing design; check claim-coverage, feasibility assumptions, over-claims, and report-style, and report only the deviations. Fix one in place only if it breaks a non-negotiable rule (a fabricated result, an experiment assumed feasible or presented as done, an invented anomaly cause, or an unconditional over-claim).

The suite's value is bounded, claim-anchored, feasible experiments, not a competing design. Audit and constrain rather than take over.

## Non-Negotiable Rules

The experiment section is where a paper is most tempting to gild — with experiments that sound easy, results that read cleanly, and anomalies quietly dropped. This skill exists to resist that. Hold the line:

- **Do not fabricate experiments, results, or feasibility.** Never present an experiment as easy or doable on your own judgment. Assess feasibility only against the equipment, data, and time the user states; where those are unknown, leave a placeholder and say the assessment is subject to their actual conditions. Do not assume a dataset is obtainable, a baseline is runnable, or a run is cheap.
- **Never invent or alter results.** Do not produce numbers, do not change values the user reports, and require that every figure in the narration match the tables. Do not treat a planned experiment as if it were done.
- **Do not explain away anomalies.** Where the method loses, plateaus, or behaves oddly, an explanation is required — but if the user has not supplied one, flag that it is needed rather than inventing a plausible-sounding cause.
- **Anchor everything to a claim.** Every experiment and ablation must map to a claim in the main line; every results paragraph must serve a claim. Flag orphans both ways — claims with no supporting evidence, and experiments or paragraphs that support no claim.
- **Minimal necessary set, not gold-plating.** Recommend the least that argues the main line under the stated resources. When an ideal experiment is not feasible with those resources, propose the strongest feasible proxy and name the residual reviewer-risk instead of demanding the ideal.
- **Keep claims bounded.** Tie every comparative result to its conditions; do not let narration generalize a tested result into unconditional superiority. Mirror the claim boundaries the manuscript already sets.
- **State the feasibility disclaimer in the output.** Every design or feasibility assessment ends with the disclaimer in the Output Format section, so the limits of the assessment are on the record.

## Rule-Conflict Escalation

If the user asks you to confirm an experiment is feasible, to state a result or an anomaly explanation you cannot support, or to treat a planned experiment as done, stop and say what you cannot verify — you have not run it and cannot see the lab. If the user asks for narration that claims more than the conditions support, flag it before writing. If your own draft drifts into report-style narration, an invented anomaly cause, or an assumed-feasible experiment, correct it without asking.

## Intake

Gather these before auditing. Ask in one compact pass; if the user leaves something blank, proceed with a stated assumption and echo it back — except feasibility inputs, where an unknown becomes a placeholder rather than a guess. See the guide for the full question bank.

- The main line and claims: the one-sentence thesis plus the specific claims the experiments must support. Reuse `paper-argument-reconstructor` or `idea-novelty-auditor` output if it exists rather than re-deriving.
- The experiments themselves: the draft experiment section, or the planned and available experiments, ablations, baselines, datasets, and metrics.
- What is done versus planned — so nothing planned is audited as if completed.
- Resource constraints (the feasibility inputs): available equipment and compute, datasets you can and cannot access, time budget or deadline, and any hardware or sensor specifics that bear on feasibility.

## Workflow

1. Run intake. Get the claims, the experiments/draft, the done-versus-planned split, and the resource constraints. Placeholder any feasibility input the user cannot give.
2. Build the claim–evidence map: for each claim, list the experiment, ablation, comparison, or analysis that would support it, and mark whether it is present, planned, weak, or missing.
3. Flag design gaps and padding: claims with no support, and experiments or ablations that support no claim.
4. For each gap, propose the minimal experiment or ablation that would close it, assessed against the stated resources. Where the ideal is not feasible, give the strongest feasible proxy and the residual reviewer-risk. Placeholder feasibility where resources are unknown.
5. Audit the ablations: each must isolate one factor and tie to a claim; flag non-discriminating ablations and missing ones a reviewer would demand.
6. Audit the results narration against the report-style checklist: each paragraph anchored to a claim, numbers interpreted not just stated, comparisons bounded to conditions, anomalies explained or flagged for explanation, trends summarized not enumerated.
7. Assemble the output: the claim–evidence map, design gaps and cuts with minimal feasible additions, ablation notes, narration issues with rewrite directions, and the feasibility disclaimer.

## Experiment & Ablation Design Review

Work from the claims, not from the experiments. For each claim ask what kind of evidence would make a skeptical reviewer believe it: a demonstration that the effect exists, an ablation that isolates the component or mechanism responsible, a comparison that establishes the advantage under stated conditions, or an analysis that explains why. Map the existing and planned study onto that, and the gaps and the padding both fall out.

Under resource limits, prioritize. The goal is the minimal set that argues the main line given the user's equipment, data, and time — not the exhaustive set. When the evidence a claim really needs is out of reach with the stated resources, do not demand it: propose the strongest feasible substitute, and state plainly what a reviewer could still attack, so the user chooses with eyes open. Never decide the substitute is "good enough" on feasibility you cannot see.

Ablation discipline: an ablation earns its place only if removing or changing one factor changes the conclusion and that conclusion maps to a claim. Flag ablations that would leave the story unchanged (they are padding) and ablations a reviewer would demand but that are absent (they are gaps).

## Results Narration Review

The failure mode is report-style narration: prose that recites the tables — "Table X shows we achieve Y, which is Z higher than the baseline" — without saying what it means. Replace recitation with argument. See the guide for the full checklist and before/after rewrites; the executable standards are:

- every results paragraph names the claim it supports, not just the numbers;
- the text says what a number implies, not only its value; a sentence whose entire content is "Table/Figure X shows we reach Y" is report-style and must be reworked;
- comparisons are tied to the claim and to the conditions they hold under; no unconditional-superiority phrasing;
- anomalies, plateaus, and cases where the method loses are explained by mechanism — or, if the user has not given a reason, flagged as needing one, never given an invented cause;
- trends across a table are summarized and explained, not enumerated cell by cell;
- numbers match the tables exactly.

When giving a rewrite, use the user's actual numbers if provided and placeholders otherwise; never substitute invented values or an invented explanation.

This review covers the results narration *inside* the experiment section. If the abstract's or introduction's one-line results summary is also in view, do not rewrite it here — but do flag it when it claims more, or under looser conditions, than the section supports, and hand the wording to `paper-argument-reconstructor`. The section and the abstract must state the same conclusion at the same strength.

## Output Format

For a full audit, return, in this order:

```text
Claim–evidence map:
- Claim 1 -> [supporting experiment/ablation: present | planned | weak | missing]
- ...

Design gaps and cuts:
- gap: <claim> has no/weak support -> minimal addition: <experiment/ablation>, feasibility vs stated resources: <note or placeholder>, residual risk if proxy: <...>
- cut/re-justify: <experiment> supports no claim
- ...

Ablation notes:
- non-discriminating: ... | missing but expected: ...

Narration issues:
- <passage> is report-style -> should serve <claim>; rewrite direction: <...>
- <anomaly> needs an explanation the draft does not give (do not invent one)

Feasibility note:
- This assessment is based only on the equipment, data, and time you described. It cannot verify your lab's actual conditions, and none of the proposed experiments have been run here. Treat feasibility, cost, and expected outcomes as subject to your real setup; confirm before committing.
```

For a quick check, return only the claim–evidence map, the top gap with its minimal feasible addition, the most report-style passage with a rewrite direction, and the feasibility note.
