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
| `paper-polisher` | Chinese or English TeX manuscript text needs faithful academic English polishing or local revision. | TeX-safe polished text, terminology consistency, fidelity review, optional preservation check. |
| `journal-recommender` | A finished or near-finished manuscript needs realistic target journals, fast-review options, or fit verification for a journal shortlist. | Four-tier journal shortlist with live official-site, LetPub, indexing, red-flag, and recent related-paper evidence. |
| `paper-cover-letter` | The manuscript is ready for submission and needs a journal cover letter. | Submission cover letter with bounded contribution claims, scope-fit argument, placeholders for unconfirmed details. |
| `paper-response-to-reviewers` | Reviewer or editor comments need a revision plan and point-by-point response. | Comment decomposition, severity/evidence grading, revision plan, response letter, consistency audit. |

## Companion Video

Chinese video: [Article Form 0 to 1](https://www.bilibili.com/video/BV1w9fCBGER1/)

The video covers a practical paper workflow in three modules:

| Video Module | Repository Mapping |
|---|---|
| Journal selection | Use `journal-recommender` before `paper-cover-letter` to narrow target venues by scope, level, indexing, OA/budget, review speed, red flags, and recent related-paper evidence. Do not infer the target venue from the current LaTeX template; reformat after choosing the journal. |
| LaTeX formatting and manuscript structure | Use `paper-argument-reconstructor` for section logic and contribution framing; use `experiment-section-auditor` for experiment-set minimality, ablation sufficiency, and results narration; use `paper-polisher` for TeX-safe language polishing and preservation checks. Journal-specific LaTeX formatting still follows the target journal template. |
| Response to reviewers | Use `paper-response-to-reviewers` after reviews arrive. The skill separates comments, plans manuscript revisions before claiming changes, drafts point-by-point replies, and checks that every promised edit exists in the revised manuscript. |

## Operating Model

Most drafting and auditing skills support two modes.

Generation mode is the default. The skill drafts, revises, audits, or plans according to its scope.

Verification mode is used when another tool or skill has already produced a draft. In this mode, the skill does not replace the wording by default. It checks for rule violations such as broken TeX keys, changed numbers, overclaimed novelty, unsupported citations, inconsistent terminology, fabricated manuscript changes, or response-letter promises not present in the revision.

This makes the suite useful both as a primary workflow and as a quality-control layer after other AI tools.

`read-paper-to-notes` instead separates full-note, focused-analysis, and verified-enrichment modes. It uses the supplied paper as the default evidence boundary and labels any reader inference or externally verified addition.

## Human Review

Treat all AI-generated notes and edits as draft material. Reading, polishing, and rewriting can still introduce subtle errors even when a skill applies evidence or preservation rules. Before submission or reuse, manually compare substantive content against the source paper or manuscript and verify technical meaning, numerical values, equations, citation support, reference metadata, and journal-specific formatting.

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
Use paper-polisher to polish this TeX section into formal engineering-journal English. Preserve equations, labels, references, citations, variables, numbers, and technical meaning.
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
Use paper-polisher in verification mode to compare this polished TeX against the original. Report broken keys, changed numbers, strengthened claims, or terminology drift without rewriting the whole text.
```

## Preservation Check

For local TeX polishing workflows, compare the original and polished files before finalizing:

```bash
python3 paper-polisher/scripts/check_preservation.py original.tex polished.tex
```

The script reports changed structural TeX keys and numeric tokens. Run it on the original TeX content and the polished TeX content, not on a complete AI response that also contains notes or review comments.

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
