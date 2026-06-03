# Paper Polisher Skill

一个用于 TeX 学术论文英文润色、论证重构和润色后审查的 Codex / Claude skill。

这个项目的目标不是简单把句子改得更像英文，也不是机械提升词汇复杂度，而是帮助论文形成更清晰的 problem-driven storyline。它适合用于摘要、引言、相关工作、方法、公式解释、理论证明、实验、结果分析、讨论和结论等部分。

> 注意：skill 本体仍然保持英文，包括 `SKILL.md` 和 `references/polish_integrated.md`。这个中文版 README 只是为了方便中文用户理解和安装。

## 功能

- 保留 TeX 公式、环境、标签、引用、变量和技术含义。
- 保留 `\label{...}`、`\ref{...}`、`\eqref{...}`、`\cite{...}`、`\citep{...}`、`\citet{...}` 中的原始 key。
- 避免把论文写成模块堆砌，而是围绕核心问题重构论证主线。
- 改善英文表达，使其更正式、客观、克制，符合工程期刊写作风格。
- 检查术语、模块名、变量、指标和贡献表述是否一致。
- 润色完成后执行 post-polishing review，并输出 review report 和 compliance note。

## 项目结构

```text
paper-polisher/
|-- SKILL.md
`-- references/
    `-- polish_integrated.md
```

其中：

- `paper-polisher/SKILL.md` 是 skill 的入口文件。
- `paper-polisher/references/polish_integrated.md` 是完整的论文润色和论证重构指南。

## 安装方式

### Codex

克隆仓库，并把 skill 文件夹复制到 Codex 的 skills 目录：

```bash
git clone https://github.com/MercuryZzz-123/polish_skill.git
mkdir -p ~/.codex/skills
cp -r polish_skill/paper-polisher ~/.codex/skills/
```

安装后应存在：

```text
~/.codex/skills/paper-polisher/SKILL.md
```

### Claude Code

个人级 Claude Code skill 可以安装到：

```bash
git clone https://github.com/MercuryZzz-123/polish_skill.git
mkdir -p ~/.claude/skills
cp -r polish_skill/paper-polisher ~/.claude/skills/
```

安装后应存在：

```text
~/.claude/skills/paper-polisher/SKILL.md
```

如果只想在某个项目中使用，也可以把 `paper-polisher` 复制到目标项目的 `.claude/skills/` 目录下。

### 网页 AI 平台

对于 Claude.ai、ChatGPT 等支持上传自定义 skill、项目文件或知识文件的网页 AI 平台，通常可以先打包 skill 文件夹：

```bash
git clone https://github.com/MercuryZzz-123/polish_skill.git
cd polish_skill
zip -r paper-polisher.zip paper-polisher
```

然后在对应的网页 AI 平台中上传 `paper-polisher.zip`。具体入口因平台而异；在 Claude.ai 中通常是：

```text
Customize > Skills > Create skill > Upload a skill
```

上传文件为：

```text
paper-polisher.zip
```

## 使用方式

可以这样调用：

```text
Please use the paper-polisher skill to polish the following TeX section into formal engineering-journal English.
Preserve all equations, labels, references, citations, variables, and technical meanings.
After polishing, run the post-polishing review against the style guide.
```

对于整篇论文或重要章节，skill 会使用 `references/polish_integrated.md` 作为详细风格指南。

## 推荐工作流

如果是投稿前润色，建议不要直接孤立地逐段润色，也不要一开始就一次性让模型改完整篇。更稳妥的流程是：

1. 先提供整篇论文，让 agent 识别 core problem、terminology map、main storyline 和 section-level issues。
2. 再按章节润色，并保持与整篇论文诊断结果一致。
3. 最后进行 full-paper review，检查 TeX preservation、terminology consistency、problem-driven structure、claim boundaries 和 output completeness。

推荐思路是：

```text
Full-paper diagnosis -> Section-level polishing -> Full-paper review
```

如果只是短论文、草稿或局部快速润色，也可以直接进行整篇或单节润色，但最后仍建议执行 review report 和 compliance note。

## 输出内容

默认情况下，skill 会输出四部分：

1. Markdown version  
   便于阅读和修改的润色版本。

2. TeX version  
   可回填论文的 TeX 安全版本。

3. Review report  
   润色后的审查报告，检查是否满足风格指南和结构要求。

4. Compliance note  
   简短说明是否保留 TeX 结构、是否统一术语、是否避免虚构贡献或夸大结果。

## 适用场景

适合：

- TeX 英文论文润色；
- 中文初稿改写为正式英文论文；
- 摘要、引言、方法和实验部分重构；
- 论文投稿前语言与逻辑审查；
- 检查公式解释、实验设计和结果分析是否服务于核心问题。

不适合：

- 编造实验结果；
- 重写技术方法本身；
- 修改公式、算法或实验设置；
- 在没有原文支持的情况下添加新贡献。

## License

本项目使用 MIT License。
