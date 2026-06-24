# Problem-Driven Literature Review Protocol

Full protocol for the problem-driven-literature-review skill; the one-sentence principle and the S-R-L-H-G-M-C-V table are summarized in SKILL.md.

## 1. Infer Before Asking

Before writing or revising a review, identify the following variables, but do not interrupt the user by default.

Infer conservatively when possible:

- target venue or venue family;
- paper type: method, theory, benchmark, system, application, or survey;
- main contribution type: algorithm, controller, framework, protocol, dataset, metric, theorem, or system implementation;
- target audience: narrow domain experts or broader interdisciplinary readers;
- review length: short introduction background or full Related Work section;
- available validation: theorem, simulation, ablation, benchmark, real-system experiment, or case study.

Ask at most one compact clarification question only when the missing information would materially change the review structure, tone, citation strategy, or claim strength.

## 2. Core Protocol: S-R-L-H-G-M-C-V

| Step | Meaning | Question to answer |
|---|---|---|
| S | Scenario | What target task, environment, and constraints define the paper? |
| R | Requirements | What must a credible solution satisfy? |
| L | Literature lines | Which functional routes does prior work follow? |
| H | Hidden assumptions | What must be true for each route to work well? |
| G | Structural gap | Why do existing routes fail to jointly satisfy R? |
| M | Missing object | Is the missing object a representation, mechanism, interface, theory, metric, benchmark, or framework? |
| C | Contributions | Which gap component does each contribution address? |
| V | Validation | Which experiment, theorem, ablation, or benchmark validates each claim? |

## 3. Minimum Worksheet

Fill this worksheet before drafting. If it cannot be filled, do not rush into prose.

| Item | Content |
|---|---|
| Target scenario S | What task is addressed, and under what constraints? |
| Key requirements R | Which 3-5 requirements must the method satisfy? |
| Literature routes L | Which routes address parts of the requirements? |
| Hidden assumptions H | What does each route assume? |
| Structural gap G | What is jointly missing across the routes? |
| Missing object M | Is the paper adding a mechanism, interface, representation, theory, benchmark, or metric? |
| Contributions C | Which gap does each contribution address? |
| Validation V | Which evidence supports each claim? |

## 4. Five-Move Paragraph Template

Each review paragraph should usually perform five moves.

1. Requirement:

```text
A deployable solution must satisfy X while maintaining Y.
```

2. Existing capability:

```text
Existing methods based on A provide an effective way to handle X.
```

3. Hidden assumption:

```text
Their effectiveness typically relies on the assumption that H holds.
```

4. Boundary:

```text
However, in the target setting, H becomes restrictive because ...
```

5. Bridge:

```text
This motivates a mechanism / representation / framework that can ...
```

Use this as reasoning scaffolding, not as prose to copy mechanically.

## 5. Writing a Structural Gap

Do not end the review with a defect list.

Weak pattern:

```text
Method A has problems, method B is computationally expensive, and method C lacks theoretical guarantees. Therefore, a new method is needed.
```

Stronger pattern:

```text
Existing studies have advanced A, B, and C separately. However, they typically treat X, Y, and Z in isolation, or rely on assumptions that are difficult to satisfy in the target scenario. As a result, current methods still face a persistent trade-off among R1, R2, and R3. What remains missing is M.
```

The missing object M must be named. Examples include:

- a risk-aware representation;
- an auditable intermediate interface;
- an uncertainty-aware calibration loop;
- a task-coupled evaluation protocol;
- a real-time safety-certified controller;
- a multimodal-to-executable transformation pipeline.

## 6. Contribution Mapping

Contributions must not be a module list. Each contribution should answer:

```text
Without this contribution, which gap component cannot be closed?
```

Use this mapping table:

| Gap component | Contribution | Validation |
|---|---|---|
| G1 | C1 | theorem / experiment / ablation |
| G2 | C2 | baseline comparison / benchmark |
| G3 | C3 | robustness / runtime / real-world test |

Recommended wording:

```text
To address [gap component], we propose [contribution], which enables [capability].
```

## 7. Reference Selection: Claim First

Do not pile up papers first and then assemble a review. First write the claims that must be supported, then find references for those claims.

| Claim type | Required reference type |
|---|---|
| Problem importance | survey / application paper / deployment paper |
| A route is effective | representative method paper |
| A route has a limitation | limitation / failure / comparative paper |
| Current state of the art | recent high-quality paper |
| Direct competition | closest related method |
| Benchmark validity | dataset / benchmark / metric paper |
| Theory legitimacy | foundational theory / authoritative source |

Every reference must have a role:

| Role | Meaning |
|---|---|
| FND | Foundational theory or basic definition |
| SUR | Survey used for the field map |
| REP | Representative method for a route |
| SOTA | Recent strong or state-of-the-art method |
| COMP | Direct competitor a reviewer would naturally expect |
| BOUND | Evidence for a boundary or failure mode |
| BENCH | Dataset, benchmark, metric, or evaluation protocol |
| THEO | Theorem, proof tool, or mathematical foundation |
| APP | Engineering application or deployment context |
| ADJ | Adjacent-field inspiration |

Remove references with no clear role.

## 8. Simplified Literature Retrieval Flow

Use this flow when references must be selected or audited:

1. Start from seed papers: closest competitors, classical theory, recent surveys, and benchmarks.
2. Trace backward: inspect what the seed papers cite.
3. Trace forward: inspect recent papers that cite the seed papers.
4. Search by requirement, not only by method name.
   - Search not only `MPC`, but also `real-time constrained control under uncertainty`.
   - Search not only `VLM benchmark`, but also `executable multimodal evaluation`.
   - Search not only `calibration`, but also `online calibration uncertainty downstream fusion`.
5. Search direct competitors explicitly.
6. Cite a paper only after confirming that it supports the specific claim.

## 8.5 Reference Metadata Check

Do not treat Google Scholar BibTeX as authoritative. It is often useful for a first export, but it can misclassify conference papers as `@article`, omit DOI, abbreviate authors as `et al.`, lose capitalization braces, use a formatted author string instead of BibTeX `and`, or place venue metadata in the wrong field.

When a `.bib` file or BibTeX block is available, run:

```bash
python3 problem-driven-literature-review/scripts/check_references.py references.bib
```

Use stricter checks when finalizing references:

```bash
python3 problem-driven-literature-review/scripts/check_references.py references.bib --strict
python3 problem-driven-literature-review/scripts/check_references.py references.bib --online --title-search --strict
```

When the project has method names or proper nouns that must preserve capitalization, add them to the title-term check:

```bash
python3 problem-driven-literature-review/scripts/check_references.py references.bib \
  --protected-title-term "Reliable-loc" \
  --protected-title-term "Monte Carlo"
```

For longer project vocabularies, put one term per line in a UTF-8 text file and pass `--protected-title-terms-file terms.txt`.

The script checks entry structure, duplicate keys and DOIs, required fields by entry type, malformed DOI/URL/year fields, suspicious author separators, `et al.` in author lists, single-hyphen page ranges, Google Scholar source markers such as `[J]`, unprotected title acronyms, unprotected mixed-case terms such as `LiDAR`, configured title terms such as `Monte Carlo` or method names, and common conference/article field mismatches. With `--online`, it uses DOI metadata from Crossref and can search likely DOIs for entries without one.

If the script flags an entry, do not silently normalize it. Verify against the publisher page, DOI landing page, Crossref, DBLP, PubMed, arXiv, IEEE/ACM/Elsevier/Springer pages, or the target journal's bibliography style before finalizing. Keep unchecked entries marked as candidates.

## 9. Quality Gates

### 9.1 Direct Competitor Rule

The review must not avoid methods that reviewers will naturally think of.

For each direct competitor, state:

1. what it solves;
2. why it is a strong baseline;
3. why it remains insufficient in the target scenario;
4. whether the paper compares against it experimentally, and if not, why not.

### 9.2 Negative-Claim Hygiene

Avoid:

- `No existing work ...`
- `Existing methods cannot ...`
- `All previous studies ignore ...`

Prefer:

- `Few studies jointly consider ...`
- `This remains underexplored under ...`
- `Existing methods typically address X or Y, but not their coupling under Z ...`

### 9.3 Review-Experiment Alignment

If the review criticizes a property, the paper should test, prove, discuss, or explicitly scope that property.

| Review claim | Expected validation |
|---|---|
| Computationally heavy | runtime / complexity |
| Unsafe | safety margin / violation / proof |
| Overly conservative | detour / energy / activation frequency |
| Not robust | noise / disturbance / domain shift |
| Not executable | execution success / downstream acceptance |
| Not auditable | intermediate inspection / failure attribution |
| Insufficient calibration quality | parameter error / uncertainty / downstream task result |

### 9.4 Citation Integrity

- Do not invent references, years, titles, DOIs, datasets, model names, or conclusions.
- Mark unchecked papers as candidates only.
- In fast-moving fields, verify recent models, benchmarks, and versions.
- A citation must support the specific claim in the sentence, not merely relate to the broad topic.
- BibTeX/reference-list metadata must be checked before final use; Google Scholar BibTeX is a draft export, not an authority.
- For final references, resolve DOI/title/year/venue/author discrepancies instead of hiding them with manual formatting.

## 10. Example Use Rules

Examples are analogies, not mandatory taxonomies.

Wrong:

```text
This is a control paper, so the review must be organized by APF, MPC, event-triggered control, and AI.
```

Better:

```text
First identify the contribution type. If the paper is about safety-critical multi-agent control, the review may be organized around coordination, safety certification, real-time feasibility, and robustness. If it is about adaptive control, the review should revolve around uncertainty, adaptation, disturbance rejection, and stability proof.
```

Wrong:

```text
This is a VLM paper, so the review must be organized by semantic interface, VLM understanding, and execution planning.
```

Better:

```text
First identify whether the paper is a benchmark, model, agent system, application, or safety/reliability paper. The review categories should be determined by the output objective and contribution type.
```

## 11. Quick Examples by Contribution Type

### Method / Algorithm Paper

Organize around:

```text
task requirements -> main routes -> assumptions and trade-offs -> how the proposed method changes the trade-off -> experimental or theoretical validation
```

Typical gap:

```text
Existing methods improve A, B, or C separately, but the joint satisfaction of R1, R2, and R3 remains limited under the target setting.
```

### Theory Paper

Organize around:

```text
what existing theorems cover -> what assumptions they require -> which assumptions this paper relaxes -> where the new theorem applies
```

Typical gap:

```text
Existing results establish guarantees under assumptions H1 and H2, but these assumptions exclude the class of systems considered here.
```

### Benchmark / Dataset Paper

Organize around:

```text
what existing benchmarks measure -> what real capability remains unmeasured -> how the new benchmark defines tasks, metrics, and baselines
```

Typical gap:

```text
Existing benchmarks evaluate whether systems can answer, classify, or predict, but they do not evaluate whether outputs satisfy the operational requirements of the target task.
```

### System / Framework Paper

Organize around:

```text
breakpoint in the real workflow -> what upstream methods solve -> what downstream methods require -> missing interface -> how the paper defines module boundaries and validation loops
```

Typical gap:

```text
Prior work improves individual components, but the interface between these components remains underspecified, limiting deployability, auditability, or error attribution.
```

### Application / Deployment Paper

Organize around:

```text
scenario constraints -> why general methods do not transfer directly -> what adaptation the paper makes -> how realistic experiments prove deployment value
```

Typical gap:

```text
Although existing methods perform well under standard assumptions, their direct deployment in the target environment is limited by S1, S2, and S3.
```

## 12. Final Checklist

Before finalizing the review, check:

- Does the first paragraph start from the target scenario and core conflict?
- Are 3-5 key requirements clear?
- Are literature categories driven by function and assumptions rather than method-name stacking?
- Does each literature route state capability, assumption, and boundary?
- Is there one sentence that synthesizes the structural gap?
- Is the missing object M named?
- Does each contribution correspond to a gap component?
- Is each major claim supported by validation or discussion?
- Are direct competitors covered?
- Does the review avoid overcritical `nobody has done this` phrasing?
- Does every reference have a clear role?
- Are there no invented, misused, or decorative citations?
- Have BibTeX or reference-list entries been checked for metadata errors, especially if exported from Google Scholar?

## 13. Shortest Version

```text
Define scenario S.
Derive requirements R.
Organize literature L by function and assumptions H.
Compress limitations into structural gap G.
Name the missing object M.
Make contributions C respond to G.
Support each claim with validation V.
```

The review should convince readers that:

```text
The paper does not propose an arbitrary method. It fills a missing object that existing routes leave unresolved under the target scenario.
```
