# Response Letter Guide

> In one line: do not write the final reply first. Understand, decide, revise, and verify, then write. A formal response letter must correspond one-to-one with edits that are already made, marked, and locatable in the manuscript.

Every substantive reply states: what the reviewer truly worries about; whether the authors accept, partially accept, or politely clarify; what exactly changed in the manuscript; why that change suffices; where it is; and whether it is marked.

This skill produces the revision plan and the response letter. Editing the manuscript itself is higher-risk: confirm manuscript edits with the user, route structural rewrites to `paper-argument-reconstructor`, and final language to `paper-polisher`.

---

## Stage 1: Understand the paper + claim audit

Check:

- what the core contribution is;
- which assumptions the theoretical results depend on;
- which claims the experiments can support;
- whether the abstract / introduction / conclusion contain overstatements.

High-risk words include:

> guarantee, ensure, prove, always, global, optimal, robust, real-world, deployment, collision-free, universally

If the evidence is insufficient, weaken the strong claim into a conditional statement, for example:

- guarantees safety -> provides a conditional safety certificate under Assumptions X-Y
- ensures collision-free motion -> maintains collision avoidance in the considered scenarios
- validated in real-world scenarios -> evaluated in simulation with additional robustness tests

## Stage 2: Split and decompose the comments

First separate the raw review material into editor, associate editor, and each reviewer, and give every comment a stable ID (R1-C1, R1-C2, R2-C1, ...). Reviewer text often arrives as one undivided block; split it and number it before anything else, because every later stage, the revision plan, and the final letter all index by these IDs.

Then split each long comment into minimal problem units, and identify:

> explicit request + hidden concern

Common hidden concerns:

| Surface comment | Possible real concern |
|---|---|
| compare with method X | insufficient novelty / fairness |
| add hardware experiments | real-world claim too strong |
| proof unclear | theorem conditions too weak or conclusion too strong |
| add ablation | module contribution unclear |
| clarify parameters | insufficient reproducibility |
| discuss limitations | claim overreaching |

## Stage 3: Grade severity and required evidence

| Level | Type | Handling |
|---|---|---|
| S0 | no substantive comment | brief reply |
| S1 | language, format, figures | edit directly and give the location |
| S2 | clarity, reproducibility | add definitions, parameters, procedure, tables |
| S3 | insufficient evidence | add baseline, ablation, sensitivity, robustness, or quantitative experiments |
| S4 | core-validity risk | add proof, revise the method, reduce the claim; not future work alone |

Evidence strength:

| Level | Form |
|---|---|
| E0 | only thanks or a promise; usually insufficient |
| E1 | textual explanation / future work; weak |
| E2 | in-text clarification, definition, citation, remark |
| E3 | derivation, assumptions, proof, complexity analysis |
| E4 | new quantitative experiment, baseline, ablation, sensitivity analysis |
| E5 | hardware, real data, full theoretical strengthening |

Matching rules:

- S1 is usually satisfied by E2;
- S2 usually needs E2-E3;
- S3 usually needs E4, or at least E3 + claim reduction;
- S4 usually needs E3-E5, and cannot be answered by future work alone.

## Stage 4: Output the revision plan first

Before the manuscript is edited, output only a planned response / revision plan.

Recommended table:

| Comment | Core concern | Severity | Required evidence | Proposed manuscript action | Need user decision? |
|---|---|---|---|---|---|
| R1-C1 | baseline fairness | S3 | E4 | add baseline settings and fair comparison | No |
| R2-C2 | hardware validation | S3/S4 | E4/E5 or claim reduction | add robustness tests, reduce real-world claim, discuss future work | Yes |

At this stage do not write:

> In the revised manuscript, we have added...

Write instead:

> Suggested revision: add...

## Stage 5: Revise the manuscript and mark the changes

The manuscript edits may be done by the user or by the agent (with the user's confirmation, since this changes the paper itself). Requirements:

- each substantive comment maps to at least one manuscript action;
- additions, rewrites, claim reductions, and added explanations should all be traceable;
- mark revisions per the journal policy. For LaTeX submissions, blue text or latexdiff; for Word submissions, tracked changes or a highlight color; some venues want no marking at all;
- do not edit only the response letter without editing the manuscript.

LaTeX setup (for color marking):

```latex
\usepackage{xcolor}
\newcommand{\rev}[1]{\textcolor{blue}{#1}}
```

In the text:

```latex
\rev{The proposed method provides a conditional safety certificate under Assumptions 1--3.}
```

For a longer paragraph:

```latex
{\color{blue}
Revised paragraph here.
}
```

Mark complex equations, tables, and cross-references carefully to avoid breaking compilation.

## Stage 6: Assess sufficiency

After editing, assess before writing the formal reply.

Assessment table:

| Comment | Required action | Actual change | Location | Evidence level | Sufficient? | Risk |
|---|---|---|---|---|---|---|
| R1-C2 | add baseline settings | added solver, horizon, weights | Sec. V-B, Table II | E4 | Yes | Low |

If an S3/S4 concern only reaches E1/E2, it is usually insufficient. If the manuscript has no corresponding edit location, do not write "we have revised".

## Stage 7: Write the formal response letter

Only after the edits are done, the locations confirmed, and the evidence sufficient. Write each reply in the five moves (quote -> thank+position -> change -> reason -> pointer).

Recommended structure:

> We agree that the previous manuscript did not sufficiently clarify [issue]. In the revised manuscript, we have [specific revision], and the corresponding changes are highlighted in blue. Technically, [reason / evidence]. This revision addresses the concern because [why]. Please refer to [Section X, Page Y, Eq. (Z), Fig. W, or Table V].

---

## Locations and marking rules

The formal reply should state, as far as possible: Section; Page; Paragraph; Equation; Figure; Table; Algorithm; Appendix; Assumption / Remark / Lemma / Theorem.

Maintain an internal tracking table:

| Comment ID | Manuscript change | Type | Location | Marked? | Verified? |
|---|---|---|---|---|---|
| R1-C1 | Added baseline parameter table | table/text | Sec. V-B, Table II | Yes | Yes |

At the top of the letter:

> In the revised manuscript, all major changes are highlighted in blue for clarity.

In each reply:

> The corresponding revision is highlighted in blue in Section V-B, Page 12, Table II.

Avoid writing only:

> Please see the blue text.

---

## Conflicting reviewer comments

When two reviewers ask for opposite changes (for example, R1 wants the method simplified while R2 wants more detail), do not quietly satisfy one and ignore the other.

- Identify the underlying goal behind each request; the conflict is often about presentation, not substance, and both can sometimes be met (e.g. main text stays concise, details move to an appendix).
- Choose the change that best serves the paper, and explicitly acknowledge the other reviewer's preference in that reply.
- If a real trade-off remains, state it transparently so the editor sees the reasoning, for example: "Following R2, we added [detail] in [location]; to also address R1's concern about length, we moved [content] to the appendix rather than removing it."
- Never tell one reviewer you made a change and the other the opposite. The editor reads all replies together; keep them mutually consistent.

## Multi-round revisions

For a second or later round, show progress relative to the previous round; do not restart.

- For each returning comment, briefly recall what the previous round did, then what this round adds.
- If a reviewer writes "the authors did not adequately address ...", treat it as an S3/S4 concern: find the missing evidence, add it, and point to the new location, rather than restating the previous reply.
- Do not reopen comments the reviewer already marked as resolved.
- Keep comment IDs stable across rounds so the editor can follow each thread.

---

## Common high-risk comments

### Hardware experiments

1. check for an overstated real-world / deployment claim;
2. if present, tone it down first;
3. add alternative validation: noise, delay, disturbance, sensitivity, Monte Carlo, runtime;
4. explain that hardware experiments need a platform, calibration, a safe site, or long-term testing;
5. write future work only after the user confirms.

### Ablation

Do not simply delete a core module. If the module is coupled with a theoretical assumption, design a diagnostic ablation, for example fix the safety layer and only swap the risk function or remove the adaptive term, keeping the initial conditions, constraints, and solver identical.

### Theoretical guarantee

If you cannot prove it, do not write "guarantee". Add assumptions, proof steps, or a remark, or change the conclusion into a conditional statement.

### Baseline comparison

Do not just add a citation. Specify the same initial conditions, constraints, safety radius, sampling time, solver, horizon, weights, tuning principle, and metrics.

### Reviewer misunderstanding

Do not write "the reviewer misunderstood". Write:

> We apologize for the unclear presentation in the original manuscript, which may have led to this interpretation. We have revised Section X to clarify...

---

## Reply templates (by the five strategies)

### Accept and revise

> We agree that the previous manuscript did not sufficiently explain [issue]. In the revised manuscript, we have rewritten [section] to clarify [specific content]. The corresponding changes are highlighted in blue. Please refer to [location].

### Partial accept (scope concession)

> We agree that [concern] is important. In this revision, we addressed the part directly related to the present contribution by [revision]. The broader issue of [extension] would require [additional model/data/experiment] and is therefore beyond the scope of the current manuscript. To avoid overstating the contribution, we have revised [claim/section] and added this point to the limitations and future-work discussion. The corresponding changes are highlighted in blue in [location].

### Clarify / evidence-based rebuttal

> We respectfully clarify that the proposed method does not rely on [reviewer's assumed condition]. The confusion may have resulted from our insufficient explanation in the original manuscript. We have revised [section] to make the distinction clearer and added [equation/figure/remark]. The revised clarification is highlighted in blue in [location].

### Added proof

> We agree that the original proof was not sufficiently detailed. We have added [Lemma/Remark/Appendix] to show how [key step] follows from [assumption/equation]. The revised result now explicitly holds under [assumptions]. Please refer to [location], where the added proof steps are highlighted in blue.

### Added experiment / baseline

> We agree that reproducible baseline settings are necessary for a fair comparison. We have added the implementation details of [baseline], including [solver], [horizon], [weights], [constraints], and [sampling time]. All methods are evaluated under the same conditions. The updated results are reported in [Table/Fig.], with the corresponding additions highlighted in blue.

### Future work

> We agree that [extension] would further strengthen the work. However, it requires [specific resource/theory/platform] and is outside the current manuscript scope. To avoid overstating the current contribution, we have revised [claim/section] and added [alternative validation/limitation]. We now discuss [extension] as future work in [location], with the corresponding changes highlighted in blue.

---

## Future-work decision gate

Future work is not a "hard-problem recycle bin". A problem must not be pushed to future work just because it is hard, large, or time-constrained.

Recommend future work only when most of these hold:

1. the problem does not directly determine whether the paper's core claim holds;
2. it is a reasonable extension, not something the paper already promised to solve;
3. it cannot be completed at high quality within the current revision cycle;
4. it requires new hardware, data, platform, theory, or assumptions;
5. doing it would change the paper's main storyline;
6. the user confirms the trade-off fits the time, feasibility, workload, and research direction;
7. it is paired with mitigation: reduce the claim, add a limitation, add alternative validation, or add a failure boundary.

Never push to future work when:

- the reviewer questions core validity;
- the abstract / introduction already claims to solve it;
- a theorem or main experimental conclusion depends on it;
- not addressing it makes the main contribution untenable;
- there is no claim reduction or alternative validation;
- the user has not confirmed the trade-off.

Not recommended:

> Due to time constraints, this issue will be considered in future work.

Recommended:

> We agree that [requested extension] is important for further assessing the applicability of the proposed method. The present manuscript focuses on [current objective], while addressing [extension] would require [new platform/data/theory/assumptions] and would substantially change the current revision scope. To avoid overstating the contribution, we have revised [Abstract/Introduction/Conclusion] and added [alternative validation / limitation]. We now discuss [extension] as future work in Section VI, with the corresponding changes highlighted in blue.

---

## Forbidden phrasings

| Not recommended | Reason | Replace with |
|---|---|---|
| We have revised accordingly. | vague | We revised Section X to clarify... |
| Due to time constraints... | reads as an insufficient revision | This requires [specific resource] and is outside the current scope; we added [alternative validation] and toned down [claim]. |
| Please refer to Comment X. | the reply is not self-contained | In brief, we have [core action]. Details are provided in Comment X. |
| The reviewer misunderstood. | offensive | Our previous presentation was not sufficiently clear. |
| This method guarantees safety. | overstated | The method provides a conditional safety certificate under... |
| Please see the blue text. | location unclear | The revision is highlighted in blue in Section X, Page Y. |

---

## Final checklist

Before submitting, confirm:

- [ ] every comment is split, ID'd, and its core concern identified;
- [ ] every substantive comment has a manuscript action;
- [ ] the manuscript edits are actually done, not only written in the letter;
- [ ] additions/changes are marked per the journal's policy;
- [ ] every "we have added/revised" in the letter is findable in the manuscript;
- [ ] every reply has a Section/Page/Eq/Fig/Table location;
- [ ] no S3/S4 concern is answered with future work alone;
- [ ] conflicting reviewer requests are reconciled and the replies are mutually consistent;
- [ ] (multi-round) each returning comment shows what changed since the last round;
- [ ] future work has passed the gate or been confirmed by the user;
- [ ] the abstract / introduction / conclusion claims match the evidence;
- [ ] baseline parameters, fairness, and reproducibility are sufficiently described;
- [ ] every theorem / guarantee has assumptions and a boundary;
- [ ] all TODOs and placeholder page/figure/table numbers are replaced;
- [ ] the LaTeX color marking does not break compilation.
