# Academic Paper Skills

Languages: [English](README.md) | [Simplified Chinese](README.zh-CN.md)

A platform-neutral set of reusable AI skills for academic research writing. The project is split into six focused skills instead of one broad paper assistant:

- `idea-novelty-auditor`: audits research ideas before packaging.
- `problem-driven-literature-review`: writes and audits related work through problem-driven literature routes and claim-first citation selection.
- `paper-argument-reconstructor`: rebuilds manuscript logic and section-level storylines.
- `paper-polisher`: performs TeX-safe academic English polishing.
- `paper-cover-letter`: assembles the journal submission cover letter without overclaiming.
- `paper-response-to-reviewers`: writes the point-by-point response to reviewers for a revision.

The split keeps each skill narrow enough to trigger only when its workflow is needed.

## Skills

### idea-novelty-auditor

Use this before writing or packaging a paper idea.

It helps identify:

- classic algorithmic paradigms that may already cover the idea;
- direct and adjacent related work that may threaten novelty;
- dangerous baselines;
- reviewer attack points;
- claims that should not be made;
- cautious defensible claims;
- experiments and ablations required to support the contribution.

### paper-argument-reconstructor

Use this when the manuscript exists but the overall logic, section structure, contribution framing, or experiment-to-claim alignment needs work.

It helps with:

- abstracts;
- introductions;
- methodology narratives;
- formula explanations;
- theory/proof exposition;
- experiments;
- results and discussion;
- conclusions;
- full-paper diagnosis.

### problem-driven-literature-review

Use this for literature review, related work, introduction background, research-gap synthesis, reference selection, and citation-role assignment.

It helps with:

- organizing literature by target-scenario requirements instead of method-name lists;
- deriving hidden assumptions and structural gaps;
- mapping references to claim roles;
- covering direct competitors fairly;
- aligning review criticisms with baselines, metrics, ablations, or limitations;
- avoiding citation dumps, decorative citations, and overclaiming.

### paper-polisher

Use this for faithful TeX-safe academic English polishing.

It preserves:

- equations and TeX environments;
- labels, references, citations, and bibliography keys;
- variables, function names, module names, datasets, metrics, and baselines;
- numerical values, units, table values, figure-reported values, and reported results;
- technical meaning and claim boundaries.

It includes `scripts/check_preservation.py` for comparing original and polished TeX files in local full-paper workflows.

### paper-cover-letter

Use this once the manuscript is essentially complete and you need the letter that accompanies a journal submission.

It helps with:

- the submission statement (title, article type, target journal);
- a contribution summary that does not exceed what the manuscript supports;
- scope-fit argument for the target journal and its readership;
- originality and ethics declarations, confirmed by the author or left as flagged placeholders;
- suggested or opposed reviewers and corresponding-author details.

It reuses the manuscript's established contributions instead of inventing new ones, and leaves unconfirmed specifics as `[...]` placeholders.

### paper-response-to-reviewers

Use this for the point-by-point response that accompanies a journal revision.

It helps with:

- organizing comments by editor, associate editor, and reviewer;
- classifying each comment as accept-and-revise, clarify, evidence-based rebuttal, scope concession, or added experiment;
- writing each reply as quote, thank, position, change, and pointer to the manuscript;
- checking that every promised change is actually in the revised manuscript;
- softening overstated claims a reviewer flags instead of defending them.

It reports the revisions the authors actually made, and leaves unconfirmed pointers as `[Section X, page Y]` placeholders.

## Verification Mode

Each skill runs in two modes. By default it generates or revises — polishing, reconstructing an argument, drafting a review or a letter, writing a reply. When the input is text another tool or skill has already produced, the skill switches to verification mode: instead of rewriting, it checks the draft against its own fidelity rules and reports only the deviations — broken TeX or keys, changed numbers, strengthened claims, inconsistent terminology, promised-but-missing edits, and so on.

This makes the suite a faithful-output check layer that complements stronger generative skills instead of competing with them: let another skill write, then have the matching skill here verify what it produced, without overwriting the wording unless a rule is violated.

This behavior ships inside the `SKILL.md` files, so it works in any agent that loads them (Claude Code, Codex) with no extra setup.

To run the check automatically after another skill or tool produces a draft, add a rule to your agent's instruction file. This part is per-agent and lives in your own config, not in the cloned repository.

For Claude Code, add to `CLAUDE.md`:

```text
For academic manuscript text, treat these academic-paper skills as a verification layer.
When a section has been drafted, polished, or rewritten by another skill or tool, run it
through the matching skill here in verification mode before finalizing: check fidelity
(TeX/equations/citations/keys, numbers, claim boundaries, terminology, promised changes)
and report the deviations, without overwriting the wording unless a rule is violated.
```

For Codex, add the same rule to `AGENTS.md`.

## Structure

```text
idea-novelty-auditor/
|-- SKILL.md
`-- references/
    `-- idea_novelty_risk_audit.md

paper-argument-reconstructor/
|-- SKILL.md
`-- references/
    |-- argument_reconstruction.md
    `-- argument_reconstruction_zh.md

problem-driven-literature-review/
`-- SKILL.md

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

## Install

Use whichever installation path your AI environment supports.

### Codex Local Skills

Clone this repository and copy all six skill folders into your Codex skills directory:

```bash
git clone https://github.com/yujie-jason-zhang/polish_skill.git
mkdir -p ~/.codex/skills
cp -r polish_skill/idea-novelty-auditor ~/.codex/skills/
cp -r polish_skill/problem-driven-literature-review ~/.codex/skills/
cp -r polish_skill/paper-argument-reconstructor ~/.codex/skills/
cp -r polish_skill/paper-polisher ~/.codex/skills/
cp -r polish_skill/paper-cover-letter ~/.codex/skills/
cp -r polish_skill/paper-response-to-reviewers ~/.codex/skills/
```

You can also install only the skill you need by copying only that folder.

### Claude Code Local Skills

For personal Claude Code skills:

```bash
git clone https://github.com/yujie-jason-zhang/polish_skill.git
mkdir -p ~/.claude/skills
cp -r polish_skill/idea-novelty-auditor ~/.claude/skills/
cp -r polish_skill/problem-driven-literature-review ~/.claude/skills/
cp -r polish_skill/paper-argument-reconstructor ~/.claude/skills/
cp -r polish_skill/paper-polisher ~/.claude/skills/
cp -r polish_skill/paper-cover-letter ~/.claude/skills/
cp -r polish_skill/paper-response-to-reviewers ~/.claude/skills/
```

For a project-specific Claude Code install, copy the desired skill folders into `.claude/skills/` inside the target project.

### Web AI Platforms

Web AI platforms that support uploaded skills, project files, or knowledge files usually use a ZIP upload.

Package all skills:

```bash
git clone https://github.com/yujie-jason-zhang/polish_skill.git
cd polish_skill
zip -r academic-paper-skills.zip idea-novelty-auditor problem-driven-literature-review paper-argument-reconstructor paper-polisher paper-cover-letter paper-response-to-reviewers
```

Or package one skill:

```bash
zip -r paper-polisher.zip paper-polisher
```

## Recommended Workflow

For early-stage ideas:

```text
idea-novelty-auditor -> paper-argument-reconstructor -> paper-polisher
```

For papers that need a related-work or literature-review section:

```text
idea-novelty-auditor -> problem-driven-literature-review -> paper-argument-reconstructor -> paper-polisher
```

For existing manuscripts with related-work or gap-framing issues:

```text
problem-driven-literature-review -> paper-argument-reconstructor -> paper-polisher
```

For existing manuscripts without a literature-review task:

```text
paper-argument-reconstructor -> paper-polisher
```

For local TeX language polishing only:

```text
paper-polisher
```

For the journal submission cover letter, after the manuscript is finalized:

```text
paper-cover-letter
```

For the point-by-point response when revising after review:

```text
paper-response-to-reviewers
```

## Example Prompts

Novelty audit:

```text
Use idea-novelty-auditor to audit this research idea before packaging it. Identify the dangerous baselines, claims I cannot make, cautious defensible claims, and experiments required.
```

Argument reconstruction:

```text
Use paper-argument-reconstructor to diagnose the introduction and rebuild it around a problem-driven storyline. Do not invent new claims or results.
```

Literature review:

```text
Use problem-driven-literature-review to revise the related work section. Organize the literature by scenario requirements, hidden assumptions, structural gaps, direct competitors, and claim-first citation roles.
```

TeX-safe polishing:

```text
Use paper-polisher to polish the following TeX section into formal engineering-journal English. Preserve all equations, labels, references, citations, variables, numerical values, and technical meaning.
```

Cover letter:

```text
Use paper-cover-letter to draft a submission cover letter for the target journal. Summarize the contribution without overclaiming, keep novelty hedged, and leave placeholders for the journal name, editor, and ethics declarations.
```

Response to reviewers:

```text
Use paper-response-to-reviewers to draft a point-by-point response. Classify each comment, reply with quote-thank-position-change-pointer, flag any promised change I still need to confirm is in the manuscript, and do not fabricate results or pointers.
```

Verification (check a draft another tool already produced):

```text
Use paper-polisher in verification mode to check this already-polished TeX against the original. Report any broken keys, changed numbers, strengthened claims, or terminology drift, but do not rewrite it.
```

## Optional Preservation Check

For local full-paper or major-section polishing workflows:

```bash
python3 paper-polisher/scripts/check_preservation.py original.tex polished.tex
```

The script reports changed structural TeX keys and numeric tokens. Run it only on the original TeX content and the polished TeX content, not on a full AI response that also contains review reports or notes.

## License

This project is released under the MIT License.
