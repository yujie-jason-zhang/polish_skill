# Paper Polisher Skill

A Codex skill for polishing TeX academic papers into formal, objective engineering-journal English.

The skill focuses on argument reconstruction, terminology consistency, and TeX-safe polishing. It is designed for abstracts, introductions, related work, methodology sections, formula explanations, theory/proof sections, experiments, results, discussion, and conclusions.

## Features

- Preserves TeX equations, environments, labels, references, citations, variables, and technical meanings.
- Keeps the exact keys inside commands such as `\label{...}`, `\ref{...}`, `\eqref{...}`, `\cite{...}`, `\citep{...}`, and `\citet{...}`.
- Reconstructs papers around a problem-driven storyline instead of a module-stacking structure.
- Improves academic tone while avoiding unsupported claims or exaggerated conclusions.
- Checks terminology consistency across modules, variables, metrics, and claims.
- Runs a post-polishing review against the bundled style guide before returning the final result.

## Structure

```text
paper-polisher/
|-- SKILL.md
`-- references/
    `-- polish_integrated.md
```

## Install

### Codex

Clone this repository and copy the skill folder into your Codex skills directory:

```bash
git clone https://github.com/MercuryZzz-123/polish_skill.git
mkdir -p ~/.codex/skills
cp -r polish_skill/paper-polisher ~/.codex/skills/
```

The installed skill should be located at:

```text
~/.codex/skills/paper-polisher/SKILL.md
```

### Claude Code

For a personal Claude Code skill, copy the same skill folder into the Claude skills directory:

```bash
git clone https://github.com/MercuryZzz-123/polish_skill.git
mkdir -p ~/.claude/skills
cp -r polish_skill/paper-polisher ~/.claude/skills/
```

The installed skill should be located at:

```text
~/.claude/skills/paper-polisher/SKILL.md
```

For a project-specific Claude Code install, copy `paper-polisher` into `.claude/skills/` inside the target project.

### Claude.ai

Claude.ai uses uploaded skill ZIP files rather than a local skills directory. Package the skill folder:

```bash
git clone https://github.com/MercuryZzz-123/polish_skill.git
cd polish_skill
zip -r paper-polisher.zip paper-polisher
```

Then upload `paper-polisher.zip` in Claude.ai:

```text
Customize > Skills > Create skill > Upload a skill
```

## Usage

Ask the agent to use the skill when polishing a TeX paper or section:

```text
Please use the paper-polisher skill to polish the following TeX section into formal engineering-journal English.
Preserve all equations, labels, references, citations, variables, and technical meanings.
After polishing, run the post-polishing review against the style guide.
```

For full papers or major sections, the skill will use `references/polish_integrated.md` as the detailed style and workflow guide.

## Recommended Workflow

For submission-oriented polishing, use the skill with a full-paper view and a section-level editing process:

1. First provide the full manuscript and ask the agent to identify the core problem, terminology map, main storyline, and section-level issues.
2. Then polish the manuscript section by section while preserving consistency with the full-paper diagnosis.
3. Finally run a full-paper review to check TeX preservation, terminology consistency, problem-driven structure, claim boundaries, and output completeness.

Avoid polishing isolated paragraphs without manuscript context when consistency matters. For short papers or quick drafts, a single full-paper polishing pass can be acceptable, but the final review should still be performed.

## License

This project is released under the MIT License.
