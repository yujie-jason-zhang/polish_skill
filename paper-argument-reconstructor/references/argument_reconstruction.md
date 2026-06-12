# Paper Argument Reconstruction Guide

## Core Goal

Rebuild a manuscript or section around a clear research problem rather than around a list of modules, datasets, or experiments.

The reconstructed paper should show:

- a clear core problem;
- a defensible technical gap;
- a coherent main storyline;
- contributions that correspond to stated gaps;
- methods introduced as necessary capabilities;
- formulas and theory tied to method logic;
- experiments that validate specific claims;
- results interpreted in relation to the problem.

Basic criterion:

```text
Every paragraph, module, formula, and experiment should answer or support the problem the paper is trying to solve.
```

## Main Storyline

Use this chain unless the paper's field strongly suggests a different structure:

```text
Real-world demand -> Technical bottleneck -> Limitation of existing methods -> Required capability -> Proposed framework -> Mechanism -> Validation -> Implication
```

For method-heavy papers, a more local chain is:

```text
Core problem -> Specific challenge -> Required capability -> Proposed module -> Mechanism -> Evidence -> Implication
```

Avoid:

```text
Module A is introduced.
Module B is introduced.
Module C is introduced.
Experiments are conducted.
```

Prefer:

```text
To address [specific challenge], [module A] is introduced to provide [required capability].
Building on this, [module B] mitigates [remaining limitation].
Finally, [module C] enables [system-level objective], thereby supporting [core problem].
```

## Diagnosis Workflow

1. Identify the application scenario and core research problem.
2. Identify the current technical bottleneck or failure mode.
3. Identify what existing methods cannot do under that bottleneck.
4. Identify the required capability that motivates the proposed method.
5. Map each module, formula, experiment, and result to a claim.
6. Identify unsupported claims, missing transitions, repeated claims, and module-stacking passages.
7. Produce a revised storyline before rewriting sentences.

## Paragraph Function Labels

Assign one role to each paragraph before rewriting:

- application background;
- core problem;
- technical gap;
- method motivation;
- module mechanism;
- formula definition;
- theoretical analysis;
- experimental setup;
- result observation;
- result interpretation;
- limitation;
- practical implication;
- transition.

A paragraph with no clear function should be merged, moved, or rewritten.

## Contribution Framing

Each contribution should correspond to a specific gap or challenge stated earlier.

Weak pattern:

```text
The contributions are:
1. We propose module A.
2. We propose module B.
3. We conduct experiments.
```

Stronger pattern:

```text
The contributions are:
1. A [capability] formulation that addresses [specific gap].
2. A [mechanism/module] that mitigates [specific failure mode].
3. A targeted evaluation that verifies [claim] under [condition].
```

Do not make priority claims such as `first`, `novel`, or `unprecedented` unless the source provides sufficient related-work support. When the evidence is incomplete, use bounded claims:

- `we focus on`;
- `we develop`;
- `we investigate`;
- `we introduce a framework for`;
- `under the evaluated conditions`.

## Section-Level Guidance

### Title

A strong title should identify the technical object, key capability, and application context without overclaiming.

Avoid titles that are only a module list or a broad promise.

### Abstract

Recommended structure:

1. Application background or problem context.
2. Specific gap or failure mode.
3. Proposed method and core mechanism.
4. Evidence from experiments or analysis.
5. Bounded implication.

Do not start with generic field importance. Do not claim broad superiority without evidence.

### Introduction

Recommended structure:

1. Real-world demand.
2. Technical bottleneck.
3. Limitations of current methods.
4. Required capability.
5. Proposed approach.
6. Contributions and organization.

The final contributions should not surprise the reader; they should answer gaps already established.

### Related Work

For detailed literature-review drafting, reference selection, direct-competitor coverage, and citation-role assignment, use `problem-driven-literature-review`. Within full-paper argument reconstruction, check only whether the Related Work section supports the paper's main gap and contribution logic.

At a high level, it should be organized by method families, assumptions, or limitations:

- family A and its limitation;
- family B and its limitation;
- methods closest to the proposed work;
- remaining gap that motivates this paper.

Avoid a chronological citation list. Avoid attacking prior work with vague language. Do not invent literature claims or citations during argument reconstruction.

### Methodology

Introduce each module from a problem requirement:

```text
To address [challenge], the method requires [capability]. Therefore, [module] is introduced to [mechanism/effect].
```

Then explain:

- input and output;
- mechanism;
- relation to other modules;
- assumption or limitation;
- role in the full framework.

### Formula Explanation

Before a formula, explain why it is needed. After the formula, define symbols and explain the mechanism it captures.

Avoid formula dumps where the reader cannot see the role of the equation in the method.

### Theory and Proof

State:

- assumptions;
- proposition/theorem meaning;
- proof logic;
- conclusion;
- scope and limitation.

Do not make the proof sound broader than the assumptions allow.

### Experiments

Each experiment should validate a claim, module, metric, or deployment requirement.

For each experiment, specify:

- claim being tested;
- dataset/scenario;
- baselines;
- metric;
- expected diagnostic value;
- limitation.

Avoid relying only on final aggregate performance. Include ablations or targeted scenarios when the paper's contribution depends on a specific mechanism.

### Results and Discussion

A strong result paragraph usually contains:

1. Observation.
2. Comparison.
3. Mechanistic explanation.
4. Relation to the paper's claim.
5. Limitation or condition when needed.

Do not simply restate table values.

### Conclusion

Return to the core problem, summarize the proposed mechanism and evidence, and state bounded future work.

Avoid introducing new claims or applications that were not evaluated.

## Experiment-to-Claim Alignment

Use this table during diagnosis:

| Claim | Required evidence | Existing experiment | Missing evidence | Risk |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

Common gaps:

- a module is claimed as important but has no ablation;
- a method is claimed as robust but is tested only on easy cases;
- a real-time or deployment claim lacks runtime or resource analysis;
- a safety or reliability claim lacks failure-case analysis;
- a superiority claim lacks dangerous baselines.

## Reconstruction Output

For diagnosis:

```text
Core problem:
- ...

Main storyline:
- ...

Section-level issues:
- ...

Recommended restructuring:
- ...

Claim/evidence gaps:
- ...
```

For rewrite:

```text
Reconstructed version:
...

Rationale:
- ...

Notes:
- ...
```

Keep notes short and focused on structural changes, claim boundaries, and missing evidence.
