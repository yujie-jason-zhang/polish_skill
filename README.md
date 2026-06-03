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

Clone this repository and copy the skill folder into your Codex skills directory:

```bash
git clone https://github.com/YOUR_NAME/polish-skill.git
mkdir -p ~/.codex/skills
cp -r polish-skill/paper-polisher ~/.codex/skills/
```

Replace `YOUR_NAME` with your GitHub username after creating the repository.

## Usage

Ask Codex to use the skill when polishing a TeX paper or section:

```text
Please use the paper-polisher skill to polish the following TeX section into formal engineering-journal English.
Preserve all equations, labels, references, citations, variables, and technical meanings.
After polishing, run the post-polishing review against the style guide.
```

For full papers or major sections, the skill will use `references/polish_integrated.md` as the detailed style and workflow guide.

## License

This project is released under the MIT License.
