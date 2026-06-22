# Academic Paper Skills

Languages: [English](README.md) | [简体中文](README.zh-CN.md)

Academic Paper Skills is a set of local AI-agent skills for manuscript preparation and revision. The repository is organized around six narrow skills, each with explicit scope boundaries, verification behavior, and preservation rules.

The suite is designed for users who already work with manuscript drafts, TeX files, reviewer comments, and journal submission material. It does not try to be a single general paper-writing assistant.

## Skill Catalog

| Skill | Use When | Primary Output |
|---|---|---|
| `idea-novelty-auditor` | A research idea, contribution claim, or paper storyline needs novelty-risk review before packaging. | Novelty-risk audit, dangerous baselines, reviewer attack points, defensible claim boundaries, required validation. |
| `problem-driven-literature-review` | A literature review, related work section, introduction background, research gap, or citation plan needs structure. | Problem-driven review logic, S-R-L-H-G-M-C-V worksheet, reference roles, gap and contribution mapping. |
| `paper-argument-reconstructor` | A draft exists, but the abstract, introduction, section logic, method narrative, or experiment-to-claim relation is weak. | Rebuilt section logic, contribution framing, storyline diagnosis, revised manuscript structure. |
| `paper-polisher` | Chinese or English TeX manuscript text needs faithful academic English polishing or local revision. | TeX-safe polished text, terminology consistency, fidelity review, optional preservation check. |
| `paper-cover-letter` | The manuscript is ready for submission and needs a journal cover letter. | Submission cover letter with bounded contribution claims, scope-fit argument, placeholders for unconfirmed details. |
| `paper-response-to-reviewers` | Reviewer or editor comments need a revision plan and point-by-point response. | Comment decomposition, severity/evidence grading, revision plan, response letter, consistency audit. |

## Companion Video

Chinese video: [Article Form 0 to 1](https://www.bilibili.com/video/BV1w9fCBGER1/)

The video covers a practical paper workflow in three modules:

| Video Module | Repository Mapping |
|---|---|
| Journal selection | Use before `paper-cover-letter`. The skills assume the target journal is known or narrowed down; use the journal-selection workflow to decide fit, article type, scope, and submission constraints before drafting the cover letter. |
| LaTeX formatting and manuscript structure | Use `paper-argument-reconstructor` for section logic, contribution framing, and experiment-to-claim alignment; use `paper-polisher` for TeX-safe language polishing and preservation checks. Journal-specific LaTeX formatting still follows the target journal template. |
| Response to reviewers | Use `paper-response-to-reviewers` after reviews arrive. The skill separates comments, plans manuscript revisions before claiming changes, drafts point-by-point replies, and checks that every promised edit exists in the revised manuscript. |

## Operating Model

Each skill supports two modes.

Generation mode is the default. The skill drafts, revises, audits, or plans according to its scope.

Verification mode is used when another tool or skill has already produced a draft. In this mode, the skill does not replace the wording by default. It checks for rule violations such as broken TeX keys, changed numbers, overclaimed novelty, unsupported citations, inconsistent terminology, fabricated manuscript changes, or response-letter promises not present in the revision.

This makes the suite useful both as a primary workflow and as a quality-control layer after other AI tools.

## Recommended Workflows

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
idea-novelty-auditor -> problem-driven-literature-review -> paper-argument-reconstructor -> paper-polisher
```

Journal submission package:

```text
target journal selected -> paper-cover-letter -> paper-polisher
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
cp -r idea-novelty-auditor problem-driven-literature-review paper-argument-reconstructor paper-polisher paper-cover-letter paper-response-to-reviewers ~/.codex/skills/
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
cp -r idea-novelty-auditor problem-driven-literature-review paper-argument-reconstructor paper-polisher paper-cover-letter paper-response-to-reviewers ~/.claude/skills/
```

For project-level use, copy the required skill folders into the target project's `.claude/skills/` directory.

### ZIP Upload

For platforms that accept uploaded skills, project files, or knowledge files:

```bash
zip -r academic-paper-skills.zip idea-novelty-auditor problem-driven-literature-review paper-argument-reconstructor paper-polisher paper-cover-letter paper-response-to-reviewers
```

Package one skill:

```bash
zip -r paper-polisher.zip paper-polisher
```

## Repository Layout

```text
idea-novelty-auditor/
|-- SKILL.md
`-- references/
    `-- idea_novelty_risk_audit.md

problem-driven-literature-review/
|-- SKILL.md
`-- references/
    `-- literature_review_protocol.md

paper-argument-reconstructor/
|-- SKILL.md
`-- references/
    |-- argument_reconstruction.md
    `-- argument_reconstruction_zh.md

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

paper-response-to-reviewers/
|-- SKILL.md
`-- references/
    `-- response_letter_guide.md
```

## Prompt Examples

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

## License

MIT License.
