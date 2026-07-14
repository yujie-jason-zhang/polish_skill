---
name: read-paper-to-notes
description: Read an academic-paper PDF or supplied full text and turn it into a faithful, structured Markdown deep-reading note. Use when the user provides a research paper and asks to read, explain, summarize, take notes, extract its problem, method, equations, experiments, results, limitations, or research implications, or fill a paper-note template. Use paper-only analysis by default and verified enrichment when the user requests code, datasets, metadata, or related-paper context. Do not use for rewriting the user's own manuscript or synthesizing multiple papers into a literature review.
---

# Read Paper to Notes

## Scope

Read one academic paper closely and produce a reusable Markdown note grounded in the supplied source.

For a complete paper note, read `references/reading_protocol.md` before drafting and use `assets/paper-note-template.md` as the output structure. Adapt the number of method, equation, and experiment subsections to the paper; keep the core headings and evidence conventions.

Use another skill when the main task is:

- synthesizing several papers into related work or a literature review: use `problem-driven-literature-review` if available;
- diagnosing or rewriting the argument of the user's manuscript: use `paper-argument-reconstructor` if available;
- polishing manuscript language or preserving TeX: use `paper-polisher` if available;
- auditing novelty claims or an experiment plan: use the corresponding audit skill if available.

## Modes

- **Full-note mode:** Read the complete paper and fill the bundled Markdown template. Use this by default when the user asks to read a paper or create paper notes.
- **Focused mode:** Analyze only the requested element, such as one equation, method module, figure, experiment, or limitation. Do not force the complete template.
- **Enriched mode:** Add verified publisher metadata, project code, datasets, or related-paper context when the user requests them or explicitly permits outside research. Keep outside information separate from paper-derived content.

Default to paper-only mode. Do not silently add web knowledge to a note presented as a summary of the supplied paper.

## Workflow

1. Establish the source boundary, requested output language, desired depth, and user research context. Infer obvious preferences from the request; ask only when missing information would materially change the note.
2. Verify that the PDF or text is readable. Identify missing pages, failed extraction, scans requiring OCR, inaccessible supplements, or unreadable equations before claiming full coverage.
3. Read in multiple passes: map the paper structure, reconstruct its problem-to-method chain, inspect technical details, and audit the evidence. Follow `references/reading_protocol.md`.
4. Track important claims in an evidence ledger with the claim type and source location. Use printed page labels when visible; otherwise use `PDF p.N`. Add section, equation, table, or figure identifiers when available.
5. Produce the note with `assets/paper-note-template.md`. Replace every placeholder, retain `论文未报告`, `不适用`, or `无法可靠读取` where appropriate, and never fill a section by invention.
6. Check numerical values, units, metric directions, equation symbols, baseline names, dataset names, and claim boundaries against the source before finalizing.

## Evidence and Fidelity Rules

- Mark source status where ambiguity matters: `[作者陈述]`, `[阅读推断]`, or `[外部核验]`.
- Keep author claims distinct from the reader's interpretation. Do not turn a plausible interpretation into a fact attributed to the paper.
- Anchor substantive claims to a page, section, equation, table, or figure whenever the source permits it.
- Preserve reported numbers, units, uncertainty values, metric directions, equation notation, and experimental conditions exactly.
- If an equation cannot be transcribed reliably, cite its identifier and explain its role instead of reconstructing it from memory.
- Label reconstructed pseudocode as `阅读者重构，非论文原文`. Do not present it as an algorithm printed by the authors.
- Do not invent novelty, motivations, limitations, code links, datasets, citations, related-paper relationships, or practical impact.
- Do not claim that an experiment proves more than its design supports. State both what the evidence supports and what it does not establish.
- Treat inaccessible appendices, supplements, figures, and scan regions as coverage limits and record them in the note.

## Template Behavior

- Use the user's language. If unspecified, use the language of the request; the bundled template is Chinese and its headings may be translated while preserving their meaning.
- Keep sections useful rather than mechanically full. Use fewer than three memory points or questions when the source does not support three meaningful items.
- Derive recommendation priority and research implications from the user's stated goal. If no research context is available, label them as general reading guidance or state that personalization is unavailable.
- List a code repository or dataset only when the paper supplies it or an external source has been verified. Otherwise write `论文未提供` or `未核验`.
- Remove all instructional placeholder text from the final note.

## Output Handling

Return Markdown directly unless the user asks for a file. When a file is requested without a path, create `<paper-title>-notes.md` in the working directory using a filesystem-safe title. Do not overwrite an existing note without explicit permission.

Finish with a compact coverage statement when any part of the paper could not be read or verified. Do not describe the note as a full-paper reading when only an abstract, excerpt, or partial extraction was available.
