# TeX-Safe Academic Polishing Guide

## Core Goal

Turn unpolished Chinese or English TeX manuscript text into formal, restrained, professional engineering-journal English without changing the paper's technical truth.

This reference is for faithful expression improvement. It is not a novelty-audit guide and not a full argument-redesign guide.

The polished text should show:

- clear and concise academic expression;
- stable terminology;
- objective tone;
- preserved TeX structure;
- preserved numerical data and experimental facts;
- no unsupported claims.

## Preservation Rules

Always preserve:

- inline and display math, including `$...$`, `\(...\)`, `\[...\]`, `equation`, `align`, `gather`, and similar environments;
- figure, table, algorithm, theorem, proof, lemma, definition, and remark environments;
- `\label{...}`, `\ref{...}`, `\eqref{...}`, `\autoref{...}`, `\cref{...}`, `\cite{...}`, `\citep{...}`, `\citet{...}`, `\bibitem{...}`, and BibTeX entry keys;
- variable names, function names, module names, model names, dataset names, metric names, baseline names, and abbreviations;
- numerical values, units, percentages, sample sizes, parameter settings, table values, figure-reported values, and significance markers.

Preserving TeX means preserving command arguments and keys exactly. For example:

```latex
\label{sec:method}
\ref{sec:method}
\eqref{eq:risk}
\cite{smith2023,chen2024}
```

must not become:

```latex
\label{sec:methodology}
\ref{method}
\eqref{eq:risk_metric}
\cite{Smith2023}
```

Do not silently fix suspicious values, inconsistent units, duplicated citations, malformed bibliography entries, or possible author-name order problems. Report them for user review unless the user explicitly authorizes reference or data cleanup.

## Faithfulness Rules

Allowed edits:

- reorder clauses or sentences for readability;
- split overly long sentences;
- merge repeated phrases;
- add light transitions when the relation is already implied by the source;
- replace colloquial wording with formal academic wording;
- make implicit local logic explicit without adding new technical content.

Forbidden edits:

- changing definitions, assumptions, algorithms, proof steps, formulas, or experimental settings;
- adding new experiments, guarantees, limitations, applications, or deployment claims;
- presenting correlation as causation;
- expanding a local result into a general superiority claim;
- converting a heuristic into a theoretical guarantee;
- altering baselines, datasets, metrics, numerical values, or reported results.

## Terminology Control

For each important concept, choose a canonical term or term family and use it consistently.

Build a small terminology ledger when the text is long or terminology-dense:

| Source term | Technical concept | Canonical term/family | Allowed contextual forms | Avoid/reserve for |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

Check for two common failures:

- the same concept is translated into multiple English terms for stylistic variety;
- different technical concepts are collapsed into one vague English term.

Examples:

- Do not mix `open-vocabulary`, `open-set`, and `open-world` unless the manuscript distinguishes them.
- Use `heading angle`, `heading`, or `yaw angle` according to the defined quantity; reserve `orientation` for broader pose or attitude when needed.
- Distinguish `risk-aware`, `safety-aware`, and `uncertainty-aware` by their actual roles in the method.

## Academic Style

Avoid colloquial, subjective, or exaggerated expressions:

- `get`
- `deal with`
- `a lot of`
- `very good`
- `obviously`
- `clearly`
- `as we all know`
- `has important significance`
- `plays a very important role`

Prefer precise, mechanism-oriented expression:

```text
Not recommended: This method can get very good results.
Recommended: The proposed method achieves consistent performance improvements under different scenarios.
```

Useful academic verbs and structures:

- `to address`, `to mitigate`, `to characterize`, `to quantify`, `to evaluate`;
- `is introduced`, `is formulated`, `is designed`, `is used to`;
- `the results indicate`, `the comparison suggests`, `the ablation study shows`;
- `under the tested conditions`, `in the evaluated scenarios`, `within this setting`.

## Local Polishing Workflow

1. Identify whether the input is a sentence, paragraph, section, caption, table note, or mixed TeX block.
2. Identify the local function: background, problem, method, formula explanation, result, discussion, or conclusion.
3. Preserve all TeX structures, keys, variables, numerical data, and technical facts.
4. Polish for objective academic English.
5. Check terminology consistency.
6. Check whether any claim became stronger than the source.

## Full-Text Polishing Workflow

1. Identify the core problem, application scenario, technical bottleneck, main method, and main claim from the manuscript.
2. Build a terminology ledger for methods, modules, datasets, metrics, variables, baselines, and abbreviations.
3. Polish section by section while preserving source meaning and TeX structures.
4. Keep cross-section terminology and claim boundaries consistent.
5. Run the preservation script when original and polished TeX files are available.
6. Produce the required output mode and review report.

## Review Checklist

Before returning, verify:

- TeX commands, environments, protected keys, variables, and math are unchanged.
- Numerical values, units, datasets, baselines, metrics, parameter settings, and reported results are unchanged.
- Bibliography and citation issues are reported rather than silently modified.
- No unsupported claims, experiments, guarantees, or deployment value were introduced.
- Technical terms are consistent.
- Tone is formal, objective, and restrained.
- Output format matches the task scope.

## Output Patterns

For short local edits:

```text
Polished version:
...

Brief note:
...
```

Omit the brief note when nothing needs to be flagged.

For major sections or full manuscripts:

```text
Markdown version:
...

TeX version:
...

Review report:
- TeX preservation: PASS
- Technical fidelity: PASS
- Numerical/data preservation: PASS
- Terminology consistency: PASS
- Citation and bibliography consistency: PASS / ISSUE REPORTED / NOT PRESENT
- Objective tone and claim boundaries: PASS
- Output completeness: PASS

Compliance note:
- TeX structures, equations, labels, references, citations, bibliography keys, variables, and original command keys are preserved.
- Numerical values, units, datasets, baselines, metrics, and reported results are preserved.
- Terminology has been checked for consistency.
- Bibliography-entry issues are reported for review rather than edited automatically.
- No unsupported technical claims or experimental results have been introduced.
```
