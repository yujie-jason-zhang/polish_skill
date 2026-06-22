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
- `\label{...}`, `\ref{...}`, `\eqref{...}`, `\autoref{...}`, `\cref{...}`, `\includegraphics{...}`, `\cite{...}`, `\citep{...}`, `\citet{...}`, `\bibitem{...}`, and BibTeX entry keys;
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

When adding a new referenceable object, do not create generic placeholder labels. Follow the manuscript's existing label convention and make the key semantically tied to the object:

```latex
\label{tab:diff_methods}
\label{fig:framework}
\label{alg:training}
```

If there is no clear manuscript convention, use `type:semantic_name`:

| Object type | Prefix | Example |
|---|---|---|
| Section | `sec:` | `\label{sec:method}` |
| Subsection | `subsec:` | `\label{subsec:ablation_setup}` |
| Figure | `fig:` | `\label{fig:framework}` |
| Table | `tab:` | `\label{tab:diff_methods}` |
| Equation | `eq:` | `\label{eq:loss_function}` |
| Algorithm | `alg:` | `\label{alg:training}` |
| Theorem | `thm:` | `\label{thm:convergence}` |
| Appendix | `app:` | `\label{app:implementation}` |

If the manuscript already uses underscore labels, keep that convention:

```latex
\label{tab_diff_methods}
\label{fig_framework}
```

Never emit bare labels or references such as `\label{tab}`, `\ref{tab}`, `\label{fig}`, `\ref{fig}`, `\label{table}`, `\label{figure}`, `\label{img}`, `\label{image}`, `\label{tmp}`, or `\label{label}`. Once the user specifies or approves a new label, treat it as protected in the same way as an original key. In later full-text generation, preserve that label exactly and keep any `\ref`, `\autoref`, or `\cref` targets consistent.

When referring to existing objects, first identify the exact label keys already present in the manuscript. For example, if the table labels are:

```latex
\label{tab:ablation}
\label{tab:errors}
\label{tab:torwic_errors}
```

then a controlled-indoor-experiment paragraph should refer only to the relevant controlled-indoor tables:

```latex
Tables~\ref{tab:ablation} and~\ref{tab:errors}
```

Do not write `Tables~\ref{tab} and~\ref{tab}`, and do not include `\ref{tab:torwic_errors}` unless the sentence is about the TorWIC evaluation.

Do not confuse internal label keys with displayed numbers. A label such as `\label{fig:1}` is acceptable if it is the manuscript's existing convention, but prose should still use a reference command with the target journal or manuscript's established reference-name style:

```latex
Fig.~\ref{fig:1}
Figure~\ref{fig:1}
```

Use `Fig.` or `Figure` according to the target journal template or the manuscript's existing style, and keep that choice consistent across the manuscript. The same applies to styles such as `Eq.` versus `Equation` and `Sec.` versus `Section`. Do not hard-code the displayed number:

```latex
Figure 1
Fig. 1
```

Captions must not include the displayed object name and number, because LaTeX generates them automatically. Use:

```latex
\caption{Overall framework of the proposed method.}
```

not:

```latex
\caption{Figure 1. Overall framework of the proposed method.}
\caption{Fig. 1. Overall framework of the proposed method.}
```

The same rule applies to tables, algorithms, equations, sections, and appendices when they are referenced or captioned in TeX source.

For newly inserted figures, protect both the semantic figure label and the image asset reference:

```latex
\begin{figure}
  \centering
  \includegraphics[width=0.85\linewidth]{figures/framework.pdf}
  \caption{Overall framework of the proposed method.}
  \label{fig:framework}
\end{figure}
```

In later full-text generation, keep `figures/framework.pdf`, the approved sizing/cropping options, and `\label{fig:framework}` unless the user explicitly asks to rename, move, resize, or replace the image. Do not simplify the path to `framework.pdf`, invent a new filename, or fall back to `\label{fig}`.

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
3. Build a structural ledger for any newly added or user-approved labels, then carry those exact labels into full-text output.
4. Polish section by section while preserving source meaning and TeX structures.
5. Keep cross-section terminology and claim boundaries consistent.
6. Run the preservation script when original and polished TeX files are available. Use strict mode for pure polishing, and use `--allow-additions` only when the user intentionally added new manuscript content, labels, references, image assets, or numeric tokens.
7. Produce the required output mode and review report.

## Review Checklist

Before returning, verify:

- TeX commands, environments, protected keys, variables, and math are unchanged.
- Newly added labels and references are semantic, convention-compatible, and not placeholders.
- Captions and prose references do not hard-code display numbers such as `Figure 1`; they use LaTeX-generated numbering through labels and reference commands, with reference-name wording (`Fig.`/`Figure`, `Eq.`/`Equation`, etc.) matched to the journal or manuscript style.
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
