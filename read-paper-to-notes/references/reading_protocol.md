# Paper Reading Protocol

Use this protocol for full-paper reading and for focused requests that require technical or experimental interpretation.

## 1. Fix the Evidence Boundary

Choose one source mode before analysis:

- **Paper only:** Use the supplied PDF or full text, including appendices embedded in it.
- **Paper plus supplied material:** Add supplements, code, notes, or context explicitly supplied by the user.
- **Verified enrichment:** Search authoritative external sources for requested metadata, code, datasets, or related papers and label the additions as external.

Never blend these modes without marking the boundary. Record missing or inaccessible material.

Use these labels when a statement's origin matters:

- `[作者陈述]`: Explicitly stated or directly reported by the paper.
- `[阅读推断]`: A reasoned interpretation that is not stated verbatim by the authors.
- `[外部核验]`: Confirmed from a source outside the supplied paper.

## 2. Validate the Input

Before claiming to have read the paper:

1. Confirm that all expected PDF pages are present and readable.
2. Check whether text extraction preserves columns, symbols, tables, and captions.
3. Detect scanned pages and use OCR or visual inspection when available.
4. Note inaccessible appendices, supplements, or linked artifacts.
5. Compare PDF page indices with printed page labels. Cite `PDF p.N` when no printed label is visible.

If extraction is unreliable, inspect the affected page visually. If reliable inspection is impossible, state the limitation instead of guessing.

## 3. Read in Four Passes

### Pass A: Map the Paper

Identify:

- title, authors, year, venue, and paper type;
- abstract-level research problem, proposed method, main evidence, and claimed contribution;
- section structure and the location of appendices;
- figures and tables that summarize the method or results.

Do not finalize the summary from the abstract alone.

### Pass B: Reconstruct the Research Logic

Answer:

1. What concrete task and setting does the paper study?
2. What limitation or unmet requirement motivates the work?
3. What capability does the proposed approach introduce?
4. Through what mechanism should it improve the outcome?
5. Which experiment, theorem, or analysis supports each major claim?

Separate the paper's explicit reasoning from an inferred reconstruction.

### Pass C: Inspect the Technical Content

Trace the method as:

```text
Input -> Representation -> Core modules or operations -> Objective or decision rule -> Output
```

For each important module, record its purpose, necessity, input, operation, output, and connection to the main claim.

For each important equation:

- preserve the original symbols and equation number;
- explain why the equation is needed, not only what each symbol means;
- define variables from the paper rather than guessing;
- record assumptions, constraints, and optimization direction;
- cite the equation and page or section.

Include pseudocode only when the paper provides it or when a reconstruction materially improves understanding. Mark every reconstruction as non-original.

### Pass D: Audit the Evidence

For the experiment section, extract:

- research question or claim being tested;
- datasets, splits, environments, and sample sizes;
- baselines and whether comparisons are directly comparable;
- metrics, units, and whether higher or lower is better;
- main quantitative results and uncertainty values;
- ablations, sensitivity tests, qualitative results, and failure cases;
- implementation details needed to interpret the comparison.

State what each result supports and what remains untested. Do not treat correlation, one benchmark, or a narrow ablation as universal proof.

## 4. Maintain an Evidence Ledger

Track important content during reading with fields equivalent to:

| Item | Concise interpretation | Source status | Location | Confidence or caveat |
|---|---|---|---|---|
| Main claim | What the authors claim | 作者陈述 | PDF p.N / Sec. X | Scope condition |
| Method mechanism | Why it should work | 作者陈述 or 阅读推断 | Eq. X / Fig. Y | Interpretation limit |
| Result | Exact reported outcome | 作者陈述 | Table X | Metric and setting |

The ledger may remain internal, but use it to place evidence anchors in the final note.

## 5. Fill Each Note Section Carefully

### Information Card and Quick Conclusion

Copy bibliographic facts from the paper. Write the quick conclusion as problem, method, evidence, and boundary in two to four sentences. Avoid promotional wording that is stronger than the paper.

### Research Position

Place the work in a field and subfield using the paper's own framing. Establish relationships to background, predecessor, concurrent, or follow-up work only from supplied or verified evidence. If the relationship cannot be established, say so.

### Problems, Framework, and Modules

Describe the actual technical obstacles rather than broad social motivation. Connect every module to a problem requirement, and preserve the direction of data flow.

### Equations and Pseudocode

Select only equations needed to understand the method. If extraction could corrupt notation, cite and explain the equation without reproducing uncertain symbols. Never fabricate runnable code from a vague method description.

### Experiments

Transcribe only comparable results into one table. Keep dataset, setting, metric, units, and uncertainty attached to each value. Split main results, ablations, and qualitative findings when combining them would be misleading.

### Limitations

Separate:

- limitations explicitly acknowledged by the authors;
- limitations inferred from assumptions, datasets, comparisons, or missing validation;
- possible improvements proposed by the reader.

Do not attribute an inferred limitation to the authors.

### Research Implications

Use the user's stated research context. For each implication, show the paper-derived basis, the assumption required for transfer, and the next validation step. Without user context, provide only general implications and label them accordingly.

### Questions and Sources

Prefer questions that test assumptions, clarify mechanisms, or identify missing evidence. List only source links found in the paper or externally verified. Mark unverified links rather than guessing them.

## 6. Handle Difficult PDF Content

- Inspect figures visually when their geometry, legend, or qualitative examples carry meaning not recoverable from the caption.
- Treat multi-column extraction order as suspect until checked against the page.
- Verify minus signs, subscripts, superscripts, Greek letters, and inequality directions in equations.
- Verify decimal points, percentages, confidence intervals, and bold or underlined best-result markings in tables.
- Read appendices when a central proof, algorithm, implementation detail, or additional experiment depends on them.

## 7. Run Quality Gates

Before finalizing, confirm:

- **Coverage:** The note reflects the full accessible paper, not only its abstract and conclusion.
- **Traceability:** Major factual and numerical claims have source anchors.
- **Fidelity:** Names, values, units, symbols, and metric directions match the paper.
- **Boundary:** Author statements, reader inferences, and external facts are distinguishable.
- **Restraint:** Missing content is marked instead of invented.
- **Utility:** Method logic and evidence are explained, not merely copied.
- **Clean output:** No instructional placeholders remain, navigation matches the headings, and the Markdown renders coherently.
