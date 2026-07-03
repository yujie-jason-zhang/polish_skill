# Experiment Section Guide

## Contents

- Goal
- Core principle
- Intake question bank
- Claim–evidence mapping
- Minimal set under constraints
- Ablation discipline
- Report-style vs argument-style narration
- Anomalies and failures
- Output template
- Worked example

## Goal

Keep a paper's experiment section honest and load-bearing: every experiment and ablation exists to argue a claim in the main line, the set is the minimum that does so under the author's real resources, and the results are written as argument rather than as a recital of numbers. This is a constraint layer. The author designs and writes; the skill audits, flags, and proposes only the minimum needed to close a gap.

It is not a design service. It does not invent a study, decide what is feasible in a lab it cannot see, produce or alter results, or explain away anomalies.

## Core principle

```text
start from the claims -> map evidence to each claim -> find gaps and padding -> propose the minimal feasible fix under real resources -> check narration argues the claims -> state feasibility limits
```

Two failure modes to avoid:

- gilding: experiments that sound easy but were never run, results that read cleanly because losses were dropped, ablations that change nothing;
- reciting: results prose that reports numbers without saying what they mean or which claim they support.

## Intake question bank

Ask in one pass. Blanks get a stated assumption — except feasibility inputs, where a blank becomes a placeholder, never a guess.

- Main line: the one-sentence thesis the experiments must support.
- Claims: the specific claims (e.g., "component A causes the gain", "the method holds under condition B", "it beats prior work on task C"). Reuse `paper-argument-reconstructor` / `idea-novelty-auditor` output if it exists.
- Study: the draft experiment section, or the planned and available experiments, ablations, baselines, datasets, and metrics.
- Done vs planned: which parts are completed and which are intended. [never audit planned work as done]
- Resources (feasibility inputs): equipment and compute available; datasets accessible and not accessible; time budget or deadline; hardware/sensor specifics that bear on feasibility. [placeholder any unknown]

## Claim–evidence mapping

Work from the claims, not the experiments. For each claim, ask what a skeptical reviewer would need to believe it, choosing among:

- existence: a result showing the effect is real;
- isolation: an ablation removing or changing one factor to show that factor is responsible;
- comparison: a baseline or prior-work comparison establishing the advantage under stated conditions;
- explanation: an analysis, case study, or diagnostic showing why the effect occurs.

Then map the existing and planned study onto the claims. Mark each claim's support as present, planned, weak, or missing. Two things fall out: claims with no or weak support (gaps), and experiments or ablations that map to no claim (padding — cut or re-justify).

## Minimal set under constraints

The target is the smallest study that argues the main line under the author's real resources, not the exhaustive one.

- For each gap, propose the minimal experiment or ablation that closes it.
- Assess that proposal against the stated equipment, data, and time. If a resource is unknown, write a placeholder ("feasibility depends on whether dataset D is obtainable") rather than assuming.
- When the evidence a claim truly needs is out of reach with the stated resources, do not demand it. Propose the strongest feasible proxy and state the residual reviewer-risk it leaves, so the author decides knowingly.
- Never rate a proxy "good enough" on feasibility you cannot see. The author confirms feasibility; the skill only reasons about what they reported.

## Ablation discipline

An ablation earns its place only if both hold: removing or changing one factor changes the conclusion, and that conclusion maps to a claim.

- Flag non-discriminating ablations — ones whose result would not change the story. They are padding.
- Flag missing ablations a reviewer would demand to accept a claim — especially the ablation that isolates the component the paper credits for its main gain. Their absence is a gap, not a detail.
- Each ablation should vary one factor at a time; note confounded ablations that move several factors at once.

## Report-style vs argument-style narration

Report-style prose recites the tables; argument-style prose uses the tables to support claims. The executable checklist:

- every results paragraph names the claim it serves;
- the text states what a number implies, not only its value;
- comparisons are bounded to their conditions — no unconditional-superiority phrasing;
- anomalies and losses are explained by mechanism, or flagged as needing explanation;
- trends across a table are summarized and explained, not enumerated cell by cell;
- numbers match the tables exactly.

Rewrites use the author's real numbers when given and placeholders otherwise; never invent values or causes.

Example 1 — headline result.

- Report-style: "Table 2 shows our method achieves [X]% accuracy, which is [a] points higher than baseline A and [b] points higher than baseline B."
- Argument-style: "The [a]-point gain over A, concentrated on [the hard subset], supports our claim that [mechanism] handles [failure mode] that A cannot; the wider margin over B, which lacks [component], is consistent with [component] being the source of the improvement rather than [confound]." (Same numbers, now tied to a claim and a mechanism.)

Example 2 — a loss the draft is tempted to hide.

- Report-style (or omission): "Our method reaches [X] on most datasets." (Dataset C, where it is [c] points lower, is dropped.)
- Argument-style: "On C our method is [c] points lower; this is expected because C violates [assumption the method relies on], which both bounds the scope of our claim and indicates when [alternative] is preferable." (Only if the author supplies the reason. If not, flag: "the drop on C needs an explanation you have not given — do not leave it unaddressed.")

Example 3 — table walk.

- Report-style: enumerating every cell — "On task 1 we get [..], on task 2 [..], on task 3 [..]."
- Argument-style: "Across tasks 1–3 the gain grows with [factor], which supports [claim]; the exception is [task], explained by [reason/flag]."

## Anomalies and failures

Losses, plateaus, high variance, and cases where a baseline wins are load-bearing, not embarrassments — they set the scope of the claim. The rule is strict: every one needs an explanation, and the skill never supplies an invented one. If the author has given a mechanism, check it is consistent with the claim's boundary. If not, flag exactly which result needs an explanation and refuse to paper over it.

## Output template

```text
Claim–evidence map:
- <claim> -> <experiment/ablation>: present | planned | weak | missing
- ...

Design gaps and cuts:
- gap: <claim> unsupported/weak -> minimal addition: <experiment/ablation>
  feasibility vs stated resources: <note, or placeholder if unknown>
  residual risk if a proxy is used: <what a reviewer could still attack>
- cut/re-justify: <experiment> maps to no claim
- ...

Ablation notes:
- non-discriminating: <...>
- missing but expected: <...>
- confounded: <...>

Narration issues:
- <passage> is report-style -> should serve <claim>; rewrite direction: <...>
- <result> needs an explanation the draft lacks (not invented here)

Feasibility note:
- This assessment is based only on the equipment, data, and time you described.
  It cannot verify your lab's actual conditions, and none of the proposed
  experiments have been run here. Treat feasibility, cost, and expected outcomes
  as subject to your real setup; confirm before committing.
```

## Worked example

Illustrative and schematic — placeholders stand in for the author's real claims, numbers, and resources. Not a real audit.

Intake (as gathered):

- main line: "a lightweight [module] makes [task] robust to [condition] without extra runtime cost."
- claims: (1) the module improves robustness under [condition]; (2) the gain comes from the module, not from more parameters; (3) runtime is unchanged.
- study: main comparison against two baselines on two datasets; one ablation removing the module. Done: the main comparison. Planned: the ablation.
- resources: [GPU type] available; dataset D2 access uncertain; ~3 weeks; no extra annotation budget.

Claim–evidence map:

- Claim 1 (robustness) -> main comparison: present, but only on clean splits — weak for "under [condition]".
- Claim 2 (gain is the module, not parameters) -> module-removal ablation: planned; but it does not control for parameter count — weak as designed.
- Claim 3 (runtime unchanged) -> no timing experiment: missing.

Design gaps and cuts:

- gap: Claim 1 needs results under [condition], not just clean data -> minimal addition: evaluate the existing models on a [condition]-perturbed split of the datasets you already have. Feasibility: likely within resources since it reuses trained models and needs no new annotation [confirm on your setup]. Residual risk: none major if the perturbation is standard.
- gap: Claim 2 -> the module-removal ablation should be matched for parameters (a same-size variant without the module), or the claim must be narrowed. Feasibility: depends on whether a parameter-matched variant trains within 3 weeks on [GPU type] [placeholder]. Residual risk if you keep the unmatched ablation: a reviewer attributes the gain to capacity.
- gap: Claim 3 -> add a runtime/throughput measurement on fixed hardware. Feasibility: cheap.
- note: dataset D2 is uncertain; if unobtainable, narrow the datasets in the claim rather than implying coverage you do not have.

Ablation notes:

- non-discriminating: none listed.
- missing but expected: the parameter-matched ablation isolating Claim 2.

Narration issues:

- a passage reporting the main table cell-by-cell -> should serve Claim 1; rewrite to state that the gain appears specifically under [condition] and why.
- if the method loses on any perturbation, that result needs an explanation you have not yet given — flag, do not fill in.

Feasibility note: this assessment is based only on the equipment, data, and time you described. It cannot verify your lab's actual conditions, and none of the proposed experiments have been run here. Treat feasibility, cost, and expected outcomes as subject to your real setup; confirm before committing.
