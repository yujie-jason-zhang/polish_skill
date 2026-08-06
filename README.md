# Academic Paper Skills

Languages: [English](README.md) | [简体中文](README.zh-CN.md)

Academic Paper Skills is a set of local AI-agent skills for paper reading, manuscript preparation, and revision. The repository is organized around nine narrow skills, each with explicit scope boundaries, evidence behavior, verification behavior, or preservation rules.

The suite is designed for users who work with research-paper PDFs, manuscript drafts, TeX files, reviewer comments, and journal submission material. It does not try to be a single general paper-writing assistant.

## Skill Catalog

| Skill | Use When | Primary Output |
|---|---|---|
| `read-paper-to-notes` | A supplied academic-paper PDF needs close reading, explanation, or conversion into a structured note. | Evidence-anchored Markdown note covering the problem, method, equations, experiments, results, limitations, and research implications. |
| `idea-novelty-auditor` | A research idea, contribution claim, or paper storyline needs novelty-risk review before packaging. | Novelty-risk audit, dangerous baselines, reviewer attack points, defensible claim boundaries, required validation. |
| `problem-driven-literature-review` | A literature review, related work section, introduction background, research gap, or citation plan needs structure. | Problem-driven review logic, S-R-L-H-G-M-C-V worksheet, reference roles, gap and contribution mapping. |
| `paper-argument-reconstructor` | A draft exists, but the abstract, introduction, section logic, method narrative, or experiment-to-claim relation is weak. | Rebuilt section logic, contribution framing, storyline diagnosis, revised manuscript structure. |
| `experiment-section-auditor` | An experiment section, ablation plan, or results writeup needs an audit against fixed claims and real resource limits. | Claim-evidence map, minimal experiment or ablation gaps, padding cuts, results-narration issues, feasibility disclaimer. |
| `paper-polisher` | Chinese or English TeX manuscript text needs faithful academic English polishing, source comparison, terminology/notation/numerical-consistency auditing, or an author-approved notation normalization. | One authoritative TeX result or a report-only audit, with preservation, coverage, and consistency findings kept separate. |
| `journal-recommender` | A finished or near-finished manuscript needs realistic target journals, fast-review options, or fit verification for a journal shortlist. | Four-tier journal shortlist with live official-site, LetPub, indexing, red-flag, and recent related-paper evidence. |
| `paper-cover-letter` | The manuscript is ready for submission and needs a journal cover letter. | Submission cover letter with bounded contribution claims, scope-fit argument, placeholders for unconfirmed details. |
| `paper-response-to-reviewers` | Reviewer or editor comments need a revision plan and point-by-point response. | Comment decomposition, severity/evidence grading, revision plan, response letter, consistency audit. |

## Companion Video

Chinese video: [Article Form 0 to 1](https://www.bilibili.com/video/BV1w9fCBGER1/)

The video covers a practical paper workflow in three modules:

| Video Module | Repository Mapping |
|---|---|
| Journal selection | Use `journal-recommender` before `paper-cover-letter` to narrow target venues by scope, level, indexing, OA/budget, review speed, red flags, and recent related-paper evidence. Do not infer the target venue from the current LaTeX template; reformat after choosing the journal. |
| LaTeX formatting and manuscript structure | Use `paper-argument-reconstructor` for section logic and contribution framing; use `experiment-section-auditor` for experiment-set minimality, ablation sufficiency, and results narration; use `paper-polisher` for TeX-safe language polishing, preservation checks, and source-internal terminology, notation, and numerical-consistency audits. Journal-specific LaTeX formatting still follows the target journal template. |
| Response to reviewers | Use `paper-response-to-reviewers` after reviews arrive. The skill separates comments, plans manuscript revisions before claiming changes, drafts point-by-point replies, and checks that every promised edit exists in the revised manuscript. |

## Operating Model

Most drafting and auditing skills support generation and verification workflows. Some skills expose narrower audit or authorized-edit modes when those actions need different safety boundaries.

Generation mode is the default. The skill drafts, revises, audits, or plans according to its scope.

Verification mode is used when the user asks to compare or quality-check an existing draft. Explicit user intent takes precedence over who produced the text. Verification focuses on reporting deviations and does not replace wording unless the user separately requests an edit.

For `paper-polisher`, source-to-output verification requires both the original and candidate; if the original is missing, comparison fields are `NOT ASSESSED`, and the candidate is never repaired in verification mode. The skill also has a consistency-only mode for terminology, mathematical notation, and source-internal numerical facts, plus an authorized notation-normalization mode that applies only an exact author-approved mapping. These modes report audit `Coverage` separately from the assessed-scope `Result`.

This makes the suite useful both as a primary workflow and as a quality-control layer after other AI tools.

`read-paper-to-notes` instead separates full-note, focused-analysis, and verified-enrichment modes. It uses the supplied paper as the default evidence boundary and labels any reader inference or externally verified addition.

## Human Review

Treat all AI-generated notes and edits as draft material. Reading, polishing, and rewriting can still introduce subtle errors even when a skill applies evidence or preservation rules. Before submission or reuse, manually compare substantive content against the source paper or manuscript and verify technical meaning, numerical values and their order, units, positive/negative or plus-minus signs, equations, citation support, reference metadata, and journal-specific formatting.

## Recommended Workflows

Single-paper deep reading:

```text
research-paper PDF -> read-paper-to-notes -> Markdown note
```

Early-stage idea screening:

```text
idea-novelty-auditor -> paper-argument-reconstructor -> paper-polisher
```

Related work or introduction gap framing:

```text
problem-driven-literature-review -> paper-argument-reconstructor -> paper-polisher
```

Full manuscript preparation:

```text
idea-novelty-auditor -> problem-driven-literature-review -> paper-argument-reconstructor -> experiment-section-auditor -> paper-polisher
```

Experiment section audit:

```text
paper-argument-reconstructor / idea-novelty-auditor claims -> experiment-section-auditor -> paper-polisher
```

Journal submission package:

```text
journal-recommender -> paper-cover-letter -> paper-polisher
```

Revision after peer review:

```text
paper-response-to-reviewers -> paper-argument-reconstructor / paper-polisher as needed -> paper-response-to-reviewers verification
```

## Installation

Clone the repository:

```bash
git clone https://github.com/yujie-jason-zhang/polish_skill.git
cd polish_skill
```

### Codex

Install all skills:

```bash
mkdir -p ~/.codex/skills
cp -r read-paper-to-notes idea-novelty-auditor problem-driven-literature-review paper-argument-reconstructor experiment-section-auditor paper-polisher journal-recommender paper-cover-letter paper-response-to-reviewers ~/.codex/skills/
```

Install one skill:

```bash
mkdir -p ~/.codex/skills
cp -r paper-polisher ~/.codex/skills/
```

### Claude Code

Install all skills as personal skills:

```bash
mkdir -p ~/.claude/skills
cp -r read-paper-to-notes idea-novelty-auditor problem-driven-literature-review paper-argument-reconstructor experiment-section-auditor paper-polisher journal-recommender paper-cover-letter paper-response-to-reviewers ~/.claude/skills/
```

For project-level use, copy the required skill folders into the target project's `.claude/skills/` directory.

### ZIP Upload

For platforms that accept uploaded skills, project files, or knowledge files:

```bash
zip -r academic-paper-skills.zip read-paper-to-notes idea-novelty-auditor problem-driven-literature-review paper-argument-reconstructor experiment-section-auditor paper-polisher journal-recommender paper-cover-letter paper-response-to-reviewers
```

Package one skill:

```bash
zip -r paper-polisher.zip paper-polisher
```

## Repository Layout

```text
read-paper-to-notes/
|-- SKILL.md
|-- agents/
|   `-- openai.yaml
|-- assets/
|   `-- paper-note-template.md
`-- references/
    `-- reading_protocol.md

idea-novelty-auditor/
|-- SKILL.md
`-- references/
    `-- idea_novelty_risk_audit.md

problem-driven-literature-review/
|-- SKILL.md
|-- scripts/
|   `-- check_references.py
`-- references/
    `-- literature_review_protocol.md

paper-argument-reconstructor/
|-- SKILL.md
`-- references/
    |-- argument_reconstruction.md
    `-- argument_reconstruction_zh.md

experiment-section-auditor/
|-- SKILL.md
`-- references/
    `-- experiment_section_guide.md

paper-polisher/
|-- SKILL.md
|-- scripts/
|   `-- check_preservation.py
|-- tests/
|   `-- test_check_preservation.py
`-- references/
    |-- tex_safe_polishing.md
    `-- tex_safe_polishing_zh.md

paper-cover-letter/
|-- SKILL.md
`-- references/
    `-- cover_letter_guide.md

journal-recommender/
|-- SKILL.md
`-- references/
    `-- journal_recommendation_guide.md

paper-response-to-reviewers/
|-- SKILL.md
`-- references/
    `-- response_letter_guide.md
```

## Prompt Examples

Single-paper deep reading:

```text
Use read-paper-to-notes to read the attached paper and create a Chinese Markdown note. Distinguish author statements, reader inferences, and externally verified facts, and anchor important claims to pages, sections, equations, figures, or tables.
```

Novelty audit:

```text
Use idea-novelty-auditor to audit this research idea before packaging it. Identify dangerous baselines, claims I cannot make, defensible claims, and required validation.
```

Problem-driven related work:

```text
Use problem-driven-literature-review to revise this related work section. Organize it by scenario requirements, hidden assumptions, structural gaps, direct competitors, and citation roles.
```

TeX-safe polishing:

```text
Use paper-polisher to polish this TeX section into formal engineering-journal English. Preserve equations, labels, references, citations, variables, every number and unit, numerical-token order, positive/negative or plus-minus signs, and technical meaning.
```

Mathematical-notation audit:

```text
Use paper-polisher to audit mathematical notation across this full TeX manuscript. Resolve the root and included files, report Coverage separately from Result, and create SYM-* findings for the same entity using multiple symbols or one symbol denoting different entities. Give exact locations and evidence. Do not rename anything.
```

Source-internal numerical-consistency audit:

```text
Use paper-polisher to audit whether each metric, experiment setting, sample count, table/prose value, unit, and sign is consistent throughout this manuscript. Return NUM-* findings with exact conditions and locations. Do not change or infer any value.
```

Author-approved notation normalization:

```text
Use paper-polisher in approved notation-normalization mode with this exact entity-to-symbol mapping. Apply only the listed substitutions, record each as AUTHORIZED CHANGE, keep every number, unit, sign, key, and unrelated formula unchanged, and report any unresolved macro or figure-asset occurrence.
```

Experiment section audit:

```text
Use experiment-section-auditor to audit this experiment section against the paper's claims. Flag unsupported claims, unnecessary experiments, missing ablations, report-style results narration, and feasibility assumptions under my stated resources.
```

Journal recommendation:

```text
Use journal-recommender to recommend target journals for this finished manuscript. Verify official sites, LetPub, indexing, OA/APC, red flags, and recent related papers in each journal; do not decide by the current LaTeX template.
```

Response to reviewers:

```text
Use paper-response-to-reviewers to plan and draft a point-by-point response. Do not claim any manuscript change unless it is present or left as a placeholder for confirmation.
```

Verification:

```text
Use paper-polisher in verification mode to compare this polished TeX against the original. Report candidate-introduced broken keys, changed math, changed or reordered numbers/units/signs, strengthened claims, and terminology drift. Report source-internal TERM-*, SYM-*, and NUM-* findings separately. Do not modify the candidate. If the original is unavailable, mark all comparative checks NOT ASSESSED.
```

## Preservation Check

For a single-file TeX workflow, compare the original and candidate before finalizing:

```bash
python3 paper-polisher/scripts/check_preservation.py original.tex candidate.tex
```

Use `--allow-additions` only for explicitly authorized ordinary prose additions. It does not permit any structural-key, image-asset, math-region, numerical-token, unit, or sign addition, deletion, change, or reordering, and it is not a notation-normalization mode. Numerical protection also covers digits in identifiers, comments, literal examples, URLs, and protected arguments. Recognized comments and literal/code regions remain exact protected source, including comment line-boundary semantics and their order relative to protected math and TeX; custom unrecognized literal macros require manual comparison.

For a multi-file manuscript, pass both authoritative root TeX files:

```bash
python3 paper-polisher/scripts/check_preservation.py original/main.tex candidate/main.tex --project
```

Project mode follows static `input`/`include`/`subfile`/`subfileinclude` directives and the `import`/`subimport`/`inputfrom`/`includefrom` families while preserving the current and previous import-directory contexts. Missing, dynamic, or cyclic paths fail closed.

For a globally applicable, exact author-approved math-token mapping, repeat `--approved-symbol-map` as needed:

```bash
python3 paper-polisher/scripts/check_preservation.py original.tex normalized.tex \
  --approved-symbol-map 'M=N'
```

This option is normalization-only, rejects unambiguous numeric, currency, percentage, and sign mappings, and permits no unrelated prose or math change. A mapping never authorizes a unit change; ambiguous bare glyphs require the entity-aware authorization ledger and manual unit review. For a scope-limited mapping or one with intentional glyph reuse, use the location-aware authorization ledger and an author-approved baseline instead.

Run the checker on manuscript files, not on a complete AI response containing notes or review comments. A pass confirms only supported source-to-output preservation. The numerical scanner covers recognized decimal, English textual, contextual Roman, and Unicode numbers plus recognized signs, markers, currencies, common units, and unit-like compounds in supported anchored, TeX-connected, delimited, or explicit-cue contexts. Manually compare every unrecognized form or context, including ambiguous standalone unit-like glyphs. Source-internal terminology, notation, and numerical consistency require the audits and completeness gate defined by the skill.

## Reference Metadata Check

For related-work or reference-selection workflows, validate BibTeX before finalizing a bibliography:

```bash
python3 problem-driven-literature-review/scripts/check_references.py references.bib
python3 problem-driven-literature-review/scripts/check_references.py references.bib --online --title-search --strict
```

Add project-specific method names or proper nouns that must preserve capitalization:

```bash
python3 problem-driven-literature-review/scripts/check_references.py references.bib \
  --protected-title-term "Reliable-loc" \
  --protected-title-term "Monte Carlo"
```

The checker catches common Google Scholar BibTeX problems such as missing required fields, duplicate DOI/key values, malformed DOI/year/page ranges, `et al.` in author fields, conference papers exported as `@article`, and title capitalization that needs BibTeX braces, including all-caps acronyms, mixed-case terms such as `LiDAR`, and configured title terms such as `Monte Carlo` or method names.

## License

MIT License.
