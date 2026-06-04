# TeX Paper Polishing and Argument Reconstruction Guide

## 1. Core Goal

Rewrite an unpolished TeX manuscript into formal, restrained, professional engineering-journal English. The goal is not word-by-word translation or superficial vocabulary upgrading. The goal is to reorganize the source material into a clear argument centered on the paper's core research problem.

The polished manuscript should show:

- a problem-driven structure;
- a clear main storyline;
- natural logical progression;
- consistent terminology;
- objective expression;
- formulas, methods, experiments, and conclusions that all serve the core problem;
- both theoretical rigor and engineering deployment value;
- intact TeX structure.

The basic judgment criterion is:

```text
Every paragraph, module, formula, and experiment should answer or support the problem the paper is trying to solve.
```

---

## 2. Non-Negotiable Rules

### 2.1 Understand Before Polishing

Before rewriting, first identify the function of each sentence and paragraph. Do not directly rewrite sentence by sentence without understanding its role.

Common paragraph functions include:

- application background;
- core problem;
- technical gap;
- method motivation;
- module mechanism;
- theoretical analysis;
- experimental validation;
- result interpretation;
- engineering implication.

Do not perform word-by-word translation.  
Do not merely replace Chinese sentence patterns with English words.  
Do not polish local language before understanding the paragraph function.

---

### 2.2 Preserve TeX Structure

Always preserve:

- `$...$`
- `\begin{equation}...\end{equation}`
- `\begin{align}...\end{align}`
- `\ref{...}`
- `\eqref{...}`
- `\cite{...}`
- `\citep{...}`
- `\citet{...}`
- `\label{...}`
- figure, table, formula, algorithm, theorem, and proof environments;
- variable names, function names, module names, and abbreviations.

Preserving TeX structure means preserving not only the command form but also the arguments and keys inside structural commands. For example:

```latex
\label{sec:method}
\ref{sec:method}
\eqref{eq:risk}
\cite{smith2023,chen2024}
```

After polishing, these should remain exactly unchanged. They must not become:

```latex
\label{sec:methodology}
\ref{method}
\eqref{eq:risk_metric}
\cite{Smith2023}
```

In particular, keys inside `\label{...}`, `\ref{...}`, `\eqref{...}`, `\cite{...}`, `\citep{...}`, and `\citet{...}` must not be translated, renamed, merged, deleted, or reordered.

Do not change the meaning of formulas.  
Do not delete references, labels, or environments.  
Do not change mathematical definitions, algorithm steps, or experimental settings for the sake of language polishing.
Do not alter source data, including numerical values, units, percentages, statistics, table entries, figure-reported values, metric names, parameter settings, baselines, dataset names, sample sizes, or significance markers. If a value appears inconsistent, suspicious, or poorly formatted, flag it explicitly rather than correcting, rounding, converting, or normalizing it silently.

---

### 2.3 Keep Terminology Consistent

Once terms, abbreviations, module names, and variable meanings are established, keep them consistent throughout the manuscript.

Do not alternate technical synonyms for stylistic variety. Technical English values stable naming more than lexical variety. For each important technical concept, choose a canonical term or term family based on the domain, technical object, intended function, grammatical role, and established collocations in the target field.

For full papers, long sections, or terminology-dense passages, build a small terminology ledger before drafting. For short paragraphs, infer the ledger mentally and still apply the same consistency check.

| Source term | Technical concept | Canonical term/family | Allowed contextual forms | Avoid or reserve for |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

After drafting, run a consistency pass:

- Check whether the same technical concept was expressed with different English terms in equivalent contexts.
- Check whether different technical concepts were collapsed into the same English term.
- Keep contextual variants only when they reflect different grammatical roles or technical roles, such as task name, adjective modifier, output property, metric, or module name.
- Replace non-canonical variants unless the context clearly indicates a different technical concept or role.
- If two English terms must both appear, make the distinction explicit.

For example:

- Do not mix `open-vocabulary` with `open-set` or `open-world` unless the concepts are intentionally different.
- Choose either `false obstacles` or `pseudo obstacles` and use it consistently.
- Distinguish `risk-aware`, `safety-aware`, and `uncertainty-aware` according to their actual meanings.
- Keep module names, function names, and variable explanations consistent.

If the source manuscript uses multiple expressions for the same concept, choose the most accurate canonical term or term family and unify it throughout the paper.

Contrastive terminology examples:

- `避障`: Do not translate it mechanically as `obstacle avoidance` in every context. If the manuscript is about a mobile robot maneuvering around obstacles, the canonical family may be `obstacle avoidance`, `obstacle-avoidance planner`, and `obstacle-avoiding behavior`. If the manuscript is about vehicles, UAVs, safety systems, or preventing impacts, the canonical family may be `collision avoidance`, `collision-avoidance system`, and `collision-free trajectory`. These forms can coexist when they express task, modifier, and output property within the same concept family. Do not switch between `obstacle avoidance` and `collision avoidance` in equivalent contexts unless the text distinguishes obstacle-centered maneuvering from impact prevention.
- `航向角`: Do not alternate `heading`, `orientation`, and `yaw` casually. If the manuscript treats it as a planar navigation angle, the canonical family may be `heading angle`, `heading`, and `heading-angle error`. In vehicle or robot kinematics, if the paper defines the quantity as rotation about the vertical axis, `yaw angle` may be the canonical term instead. Reserve `orientation` for broader pose or attitude descriptions. If both must appear, distinguish them explicitly, such as: `The orientation includes roll, pitch, and yaw, whereas the heading angle refers only to the yaw component.`

---

### 2.4 Avoid Colloquial and Subjective Language

Avoid colloquial, subjective, or exaggerated expressions such as:

- `get`
- `deal with`
- `a lot of`
- `very good`
- `obviously`
- `clearly`
- `as we all know`
- `has important significance`
- `plays a very important role`

Prefer objective, restrained, academic expression.

Example:

```text
Not recommended: This method can get very good results.
Recommended: The proposed method achieves consistent performance improvements under different scenarios.
```

---

### 2.5 Maintain a Problem-Driven Storyline

Polishing should not turn the manuscript into a collection of independent modules. The entire paper should be organized around a clear core problem.

When polishing, check whether each paragraph, module, formula, experiment, and result analysis answers the following questions:

- Which core problem or technical gap does this content serve?
- Why is this module necessary rather than an additional component?
- Which part of the problem does this formula or mechanism address?
- Does this experiment validate the problem the paper claims to solve?
- Does this result connect back to safety, robustness, real-time performance, accuracy, efficiency, deployment value, or another core objective?

Recommended storyline:

```text
Core problem -> Specific challenge -> Required capability -> Proposed module -> Mechanism -> Evidence -> Implication
```

Avoid writing:

```text
Module A is introduced.
Module B is introduced.
Module C is introduced.
Experiments are conducted.
```

Prefer writing:

```text
To address [specific challenge], [module A] is introduced to provide [required capability].
Building on this, [module B] further mitigates [remaining limitation].
Finally, [module C] enables [system-level objective], thereby supporting [core problem].
```

If a module only describes what was done, but does not explain why it is needed and how it serves the core problem, rewrite its introduction, transition, and result interpretation so that it is embedded back into the paper's main storyline.

---

### 2.6 Stay Faithful to the Source

Polishing may reorganize expression and strengthen logic, but it must not invent contributions, exaggerate results, or change technical meaning.

Do not:

- add experimental conclusions not supported by the source manuscript;
- present correlation as causation;
- present local improvement as comprehensive superiority;
- present a heuristic method as a theoretical guarantee;
- present unverified deployment value as a validated conclusion;
- change methods, formulas, or experimental facts to make the argument smoother.

Allowed edits include:

- reordering sentences;
- merging repeated expressions;
- splitting overly long sentences;
- adding necessary logical transitions;
- making implicit logic explicit;
- rewriting module descriptions into problem-driven explanations.

Basic principle:

```text
Improve clarity and argumentation without changing the technical truth.
```

---

## 3. Recommended Writing Style

The paper should generally follow this argument chain:

```text
Application background -> Core problem -> Existing methods -> Key gap -> Paper motivation -> Method design -> Theoretical analysis -> Experimental validation -> Application implication
```

A more detailed storyline can be:

```text
Real-world demand -> Technical bottleneck -> Limitation of existing methods -> Required capability -> Proposed framework -> Mechanism -> Validation -> Deployment implication
```

Prefer:

- `to address`
- `to mitigate`
- `is introduced`
- `is formulated`
- `is designed`
- `is validated`
- `enhance`
- `preserve`
- `mitigate`
- `enable`
- `deployment value`
- `practical applicability`
- `theoretical guarantee`

Use with care:

- `solve`
- `show`
- `use`
- `good`
- `better`
- `a lot`

Useful logical transitions:

- `However`
- `Moreover`
- `Furthermore`
- `Specifically`
- `Therefore`
- `Accordingly`
- `In this context`
- `As a result`
- `Overall`
- `Taken together`

Replacement should always be context-sensitive. Clarity, accuracy, and natural expression are more important than formal vocabulary upgrades.

---

## 4. Standard Workflow

1. **Read the source manuscript and identify the core problem.**
   - Determine what problem the paper is trying to solve.
   - Clarify the target object, application scenario, and technical bottleneck.

2. **Mark paragraph functions.**
   - background;
   - problem;
   - gap;
   - method;
   - mechanism;
   - theory;
   - experiment;
   - implication.

3. **Lock terminology, abbreviations, variables, and module names.**
   - Build a terminology map.
   - Choose canonical terms or term families for ambiguous source terms.
   - Unify module names.
   - Unify metric names.
   - Unify variable explanations.
   - Do not alternate synonyms merely to avoid repetition.
   - Allow variants only when they reflect different grammatical roles or technical roles.

4. **Check storyline consistency.**
   - Does each module respond to the core problem?
   - Does each experiment validate a core claim?
   - Does each result support the paper's contribution?

5. **Reconstruct the argument before polishing sentences.**
   - First revise the logic.
   - Then revise paragraph organization.
   - Finally revise sentence expression and word choice.

6. **Handle the title, abstract, introduction, related work, method, proof, experiments, and conclusion section by section.**

7. **Run the post-polishing review.**
   - Check language, terminology, storyline, TeX compliance, technical fidelity, and output completeness.
   - If any item fails, revise the polished text and review it again.

8. **Return a Markdown version, a TeX version, a review report, and a compliance note.**

---

## 5. Section-Level Guidance

### 5.1 Title

The title should be concise and academic. Avoid translated or stacked title structures.

Preferred forms:

```text
A Risk-Aware Closed-Form Framework for ...
Safe Trajectory Planning Under ...
Open-Vocabulary Semantic Mapping for ...
Deployment-Oriented Robust Control of ...
```

Avoid:

```text
Research on ...
Study of ... Based on ...
Design and Implementation of ...
An Improved Method for ...
```

The title should ideally indicate:

- the core task;
- the key method;
- the constraint or condition;
- the application scenario.

---

### 5.2 Abstract

The abstract should usually follow five steps:

1. application background;
2. core problem or key gap;
3. proposed method;
4. core mechanism;
5. theoretical or experimental result and its implication.

Recommended structure:

```text
[Background and demand.]
However, [specific challenge] remains difficult because [reason].
To address this issue, this paper proposes [method/framework].
The proposed approach [core mechanism].
Experimental/theoretical results demonstrate that [evidence], indicating [implication].
```

Avoid:

- listing modules without a problem;
- saying only that a method is proposed without explaining what it addresses;
- giving numerical results without explaining their meaning;
- using exaggerated language.

---

### 5.3 Introduction

The introduction should usually contain 4-6 paragraphs:

1. application background and real-world demand;
2. definition of the core problem;
3. existing methods and limitations;
4. technical gap;
5. proposed solution and main storyline;
6. contributions and paper organization.

Contributions should use parallel structure, for example:

```text
A ... metric is introduced to ...
A ... function is formulated to ...
An ... mechanism is developed to ...
The proposed framework is validated through ...
```

Key requirements:

- Do not introduce technical details too early.
- Do not write related work as a citation list.
- Do not write contributions as a module list.
- Each contribution should correspond to a technical gap stated earlier.

Recommended wording:

```text
These limitations indicate the need for a framework that can [required capability].
Motivated by this gap, this paper proposes [method], which integrates [module] with [mechanism] to address [specific challenge].
```

---

### 5.4 Related Work

Related work should be organized by method paradigm, not by year or as a plain reference list.

Recommended structure:

```text
[Topic sentence.]
Methods such as A, B, and C have been widely applied to ...
However, these methods ...
Overall, existing studies still face [specific limitation], which motivates [direction of this paper].
```

Limitations should be written as structural problems, not vague criticism.

Not recommended:

```text
Many researchers have studied this problem.
Reference A proposed ...
Reference B proposed ...
Reference C proposed ...
```

Recommended:

```text
Existing studies can be broadly grouped into [category A], [category B], and [category C].
Although these approaches improve [aspect], they still face limitations in [specific scenario].
```

The end of Related Work should return naturally to the paper's problem rather than stopping at a literature summary.

---

### 5.5 Methodology

The methodology section should first state the core problem and design objective, then present the overall framework, and finally explain each module.

Each module should answer:

- which specific challenge in the core problem it addresses;
- what it does;
- how it is implemented;
- why it is necessary;
- how it forms a logical connection with preceding and following modules;
- how it ultimately supports the paper's claim or contribution.

Avoid writing the method section as a module list. Each module should be introduced from a problem requirement rather than from implementation details.

Not recommended:

```text
First, module A is constructed.
Then, module B is designed.
Finally, module C is used.
```

Recommended:

```text
To mitigate [challenge], module A is first constructed to provide [capability].
Since [remaining issue] still affects [objective], module B is further designed to [function].
Finally, module C integrates these outputs into [system-level mechanism], enabling [core objective].
```

The methodology section should reflect:

```text
problem requirement -> module design -> mechanism -> expected effect
```

---

### 5.6 Formula Explanation

Formulas should not appear in isolation. Before a formula, explain why it is needed. After the formula, explain the symbols and the mechanism it supports.

Recommended order:

```text
To model/quantify/convert ..., ... is defined as
[formula]
where ...
Specifically, ...
Through this mechanism, ...
```

Formula explanation should include at least:

- the purpose of the formula;
- the meaning of each key variable;
- how the formula participates in the method mechanism;
- how the formula relates to the core problem.

Not recommended:

```text
The formula is as follows:
[formula]
where x is ...
```

Recommended:

```text
To quantify the risk induced by uncertain obstacles, the following risk metric is defined:
[formula]
where ...
This formulation converts spatial uncertainty into a differentiable risk representation, which enables the planner to account for safety constraints during trajectory generation.
```

---

### 5.7 Theory / Proof

The theory or proof section should be objective, standard, and verifiable.

Recommended expressions:

```text
Choosing the Lyapunov function candidate ...
Taking its time derivative, we obtain ...
Substituting Eq.~\eqref{...} into Eq.~\eqref{...} yields ...
Therefore, it follows that ...
The proof is thus completed.
```

Avoid:

```text
Obviously
Clearly
It is known that
We can easily see that
```

The theory section should state:

- the proof objective;
- the assumptions;
- the derivation steps;
- the relationship between the conclusion and the method claim.

If a theoretical conclusion supports safety, stability, convergence, or feasibility, explicitly state how it supports the core problem.

---

### 5.8 Experiments

The experiments section should usually follow this order:

1. experiment objective;
2. scenario or platform;
3. comparison methods;
4. parameter settings;
5. metric definitions;
6. result interpretation.

Experimental design should correspond to the paper's claims. Each experiment should state which problem, module, or contribution it validates.

Recommended expression:

```text
This experiment is designed to evaluate whether the proposed framework can [claim] under [condition].
```

Avoid:

```text
We conduct many experiments to verify the effectiveness of the method.
```

Prefer:

```text
The experiments are designed to evaluate safety, robustness, and real-time performance under dynamic and uncertain scenarios.
```

---

### 5.9 Results and Discussion

Result analysis should not merely repeat numbers. It should follow four steps:

1. describe the observation;
2. explain the reason;
3. connect back to the core problem;
4. elevate the result to its implication.

Recommended structure:

```text
As shown in Table~\ref{...}, the proposed method achieves [result].
This improvement can be attributed to [mechanism].
These results indicate that the proposed framework effectively addresses [specific challenge].
Therefore, the method provides practical value for [application scenario].
```

Focus discussion on:

- safety;
- real-time performance;
- robustness;
- trajectory quality;
- generalization ability;
- engineering deployment value.

Avoid writing only:

```text
The value is higher than other methods, so the method is better.
```

Prefer:

```text
Compared with the baseline methods, the proposed approach achieves lower collision rates while maintaining comparable computation time. This indicates that the risk-aware formulation improves safety without introducing substantial deployment overhead.
```

---

### 5.10 Conclusion

The conclusion should usually follow this order:

1. return to the core problem;
2. summarize the method composition;
3. summarize key results;
4. state theoretical or engineering significance;
5. give specific future work.

Recommended structure:

```text
This paper addressed [core problem] in [scenario].
To this end, [method/framework] was proposed by integrating [module/mechanism].
Theoretical analysis and experimental results demonstrated that [key finding].
These results suggest that [broader implication].
Future work will focus on [specific direction].
```

Avoid:

- simply repeating the abstract;
- mechanically listing modules;
- exaggerating contributions;
- writing overly broad future work.

---

## 6. Common Replacements

| Not Recommended | Recommended |
|---|---|
| solve | address / mitigate / handle |
| use | employ / utilize / integrate / adopt |
| show | demonstrate / indicate / illustrate |
| improve | enhance / increase / strengthen |
| problem | challenge / limitation / gap / issue |
| get | obtain / derive / acquire |
| a lot of | many / substantial / numerous |
| very effective | effective / robust / reliable |
| good performance | favorable / competitive / consistent performance |
| bad result | degraded performance / limited effectiveness |
| better than | outperforms / achieves higher ... than |
| important | critical / essential / significant |
| make sure | ensure |
| because of | due to / owing to |
| so | therefore / thus / accordingly |

Note:

```text
Do not replace words mechanically just to sound more advanced. Accuracy, clarity, and natural expression come first.
```

For example, `solve` may be correct in mathematical optimization, and `use` may be appropriate in simple instrumental expressions.

---

## 7. Figure, Table, and Citation Conventions

Follow the target journal, conference, or template convention first. `Figure~\ref{...}`, `Fig.~\ref{...}`, and other variants are style choices, not correctness rules. If the user specifies a venue or style guide, follow that convention. If no venue is specified, infer the convention from the existing manuscript and keep it consistent. If neither is available, choose one convention and use it consistently throughout the polished text.

Common valid conventions include:

```latex
Figure~\ref{...}
Fig.~\ref{...}
Table~\ref{...}
Eq.~\eqref{...}
Algorithm~\ref{...}
Section~\ref{...}
~\cite{...}
```

Do not mix conventions within the same manuscript unless the target template requires different forms for different contexts, such as caption labels, in-text references, and list-of-figures entries.

```latex
Figure~\ref{...} ... Fig.~\ref{...}
Table~\ref{...} ... Tab.~\ref{...}
Eq.~\eqref{...} ... equation (\ref{...})
```

For IEEE-style venues, including many T-ASE manuscripts, `Fig.~\ref{...}` may be the appropriate in-text form. Preserve and unify that style when it matches the target venue or the source manuscript.

Captions should preferably be complete phrases or complete sentences and end with a period.

Figure and table descriptions should not merely state what appears in the figure or table. They should explain what conclusion the figure or table supports.

Not recommended:

```text
Figure~\ref{...} shows the trajectory.
```

Recommended:

```text
Figure~\ref{...} illustrates the generated trajectory under dynamic obstacles, showing that the proposed planner maintains a safe clearance while preserving trajectory smoothness.
```

---

## 8. Storyline Checklist

After polishing, check whether the manuscript satisfies the following requirements:

- The abstract clearly states the core problem, method mechanism, and validation result.
- The technical gaps in the introduction are addressed one by one in the methodology section.
- Each contribution corresponds to a clear problem or gap.
- Each method module has a clear problem source.
- Each formula explains not only symbols but also its mechanism.
- Each experiment corresponds to a core claim.
- Result analysis explains the cause rather than merely repeating numbers.
- Discussion connects back to safety, robustness, real-time performance, accuracy, efficiency, or deployment value.
- The conclusion summarizes the problem, method, results, and significance rather than simply repeating module names.

Core check:

```text
If a paragraph, module, formula, or experiment is removed, will the argument chain for solving the core problem break?
```

If the answer is no, the content may be redundant or poorly integrated. Consider deleting, merging, or rewriting its logical function.

---

## 9. Post-Polishing Review Mechanism

After polishing, run a review pass before returning the final answer. The review is not a separate editing style; it is a verification step against this guide.

The review should check:

- TeX preservation: equations, environments, labels, references, citations, variables, and structural command keys are unchanged.
- Technical fidelity: mathematical definitions, algorithm steps, theorem conditions, proof logic, experimental settings, source data, numerical values, reported results, and claim boundaries are preserved.
- Terminology consistency: key terms, module names, function names, metrics, variables, and abbreviations are used consistently.
- Problem-driven storyline: every section, paragraph, module, formula, experiment, result interpretation, and conclusion serves the core research problem.
- Section-level guidance: the title, abstract, introduction, related work, methodology, formula explanations, theory/proof, experiments, results, discussion, and conclusion follow their relevant guidance when present.
- Formula mechanism: formulas are introduced by their purpose and followed by symbol meanings and mechanism-level explanations.
- Experiment alignment: each experiment is linked to a claim, module, metric, or deployment requirement.
- Result interpretation: results explain observations, mechanisms, connection to the core problem, and practical or theoretical implication.
- Objective tone: the text avoids colloquial wording, subjective claims, exaggerated conclusions, and unsupported deployment value.
- Output completeness: the Markdown version, TeX version, review report, and compliance note are present unless the user requested a different output format.

If a review item fails, revise the polished text before returning the answer and then review it again. If a review item cannot be fully verified because the source text is incomplete, mark it as `NOT FULLY VERIFIABLE` and briefly explain why. Do not mark unverifiable items as `PASS`.

Recommended review report:

```text
Review report:
- TeX preservation: PASS
- Technical fidelity: PASS
- Terminology consistency: PASS
- Problem-driven storyline: PASS
- Section-level guidance: PASS
- Formula and mechanism explanation: PASS
- Experiment and result alignment: PASS
- Objective tone and claim boundaries: PASS
- Output completeness: PASS
```

---

## 10. Output Requirements

By default, an actual polishing task should return four parts:

### 10.1 Markdown Version

- easy to read and revise;
- preserves section hierarchy;
- presents the polished manuscript content in natural paragraphs;
- may include brief revision notes when necessary.

### 10.2 TeX Version

- ready to paste back into the manuscript;
- preserves formulas, references, labels, structure, and the arguments or keys inside structural TeX commands;
- does not break TeX environments;
- does not change mathematical, algorithmic, or experimental meaning.

### 10.3 Review Report

- states the result of the post-polishing review;
- uses `PASS`, `REVISED`, or `NOT FULLY VERIFIABLE` for each check;
- briefly explains any unresolved limitation;
- does not hide failed or unverifiable checks.

### 10.4 Compliance Note

After polishing, state whether:

- this style guide was followed;
- TeX structure and the arguments or keys inside commands such as `\label{...}`, `\ref{...}`, `\eqref{...}`, and `\cite{...}` were preserved;
- terminology was unified;
- objective tone was checked;
- storyline consistency was checked;
- unsupported contributions or exaggerated results were avoided.

Recommended format:

```text
Compliance note:
- TeX structures, equations, labels, references, citations, and their original keys are preserved.
- Terminology has been checked for consistency.
- The language has been revised toward an objective engineering-journal style.
- The problem-driven storyline has been checked across the abstract, introduction, methodology, experiments, and conclusion.
- No unsupported technical claims or experimental results have been introduced.
```

---

## 11. One-Sentence Execution Prompt

```text
Please polish the given TeX paper into formal engineering-journal English consistent with my integrated style guide. Use a problem-driven storyline rather than a module-stacking structure. Ensure that each section, paragraph, module, formula, experiment, and conclusion serves the core research problem. Use explicit logical transitions, objective academic tone, moderate nominalization and passive voice, and clear mechanism-oriented explanations after formulas. Preserve all TeX structures, equations, labels, references, citations, variables, and technical meanings, including the exact original keys inside \label{...}, \ref{...}, \eqref{...}, \cite{...}, \citep{...}, and \citet{...}. Ensure terminology consistency, theorem objectivity, faithful claim boundaries, and a balanced emphasis on theoretical rigor and deployment value. After polishing, run a post-polishing review against the style guide and revise the text if any item fails. Return a Markdown version, a TeX version, a review report, and a compliance note, and explicitly state whether the polishing strictly follows the guide.
```

---

## 12. Final Principle

The core of this guide is not to translate Chinese into English, nor to make English unnecessarily complex. The goal is to turn the source manuscript into an English paper organized around a core research problem.

The final manuscript should have:

- complete logic;
- a clear storyline;
- objective tone;
- coherent structure;
- consistent terminology;
- modules that serve the problem;
- formula explanations at the mechanism level;
- experiments that validate contributions;
- result analysis that reaches the implication level;
- a conclusion that returns to the core problem;
- both theoretical rigor and engineering value.

The most important principle is:

```text
Do not polish a collection of modules. Reconstruct a problem-driven argument.
```
