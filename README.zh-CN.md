# Academic Paper Skills

语言：[English](README.md) | [简体中文](README.zh-CN.md)

Academic Paper Skills 是一组面向学术论文写作、投稿和返修流程的本地 AI-agent skills。仓库按任务边界拆成六个独立 skill，每个 skill 都有明确的适用范围、检验模式和保全规则。

它面向已经在处理论文草稿、TeX 文件、审稿意见、投稿信和期刊格式要求的用户；目标不是做一个泛化的“论文助手”，而是把论文工作流中容易失真、过度声称或漏改的部分拆成可复用的专业流程。

## Skill 目录

| Skill | 适用场景 | 主要输出 |
|---|---|---|
| `idea-novelty-auditor` | idea、贡献陈述或论文 storyline 在包装前需要做新颖性风险审查。 | novelty 风险、dangerous baselines、审稿人攻击点、可防守 claim 边界、所需实验。 |
| `problem-driven-literature-review` | literature review、related work、引言背景、research gap 或 citation plan 需要重构。 | problem-driven 综述逻辑、S-R-L-H-G-M-C-V worksheet、参考文献角色、gap 与贡献映射。 |
| `paper-argument-reconstructor` | 已有草稿，但摘要、引言、章节逻辑、方法叙述或实验支撑关系不清楚。 | 章节逻辑重构、贡献表达、storyline 诊断、论文结构调整建议。 |
| `paper-polisher` | 中文或英文 TeX 论文文本需要忠实的学术英文润色或局部修改。 | TeX-safe 润色稿、术语一致性检查、保真报告、可选本地保全检查。 |
| `paper-cover-letter` | 论文基本定稿，需要写期刊投稿信。 | cover letter、受论文证据约束的贡献陈述、scope-fit 说明、未确认信息占位。 |
| `paper-response-to-reviewers` | 收到编辑或审稿意见后，需要制定返修计划并逐条回复。 | 意见拆解、严重程度和证据等级、revision plan、逐条 response letter、一致性检查。 |

## 配套视频

B 站视频：[Article Form 0 to 1](https://www.bilibili.com/video/BV1w9fCBGER1/)

视频围绕论文从准备到返修的三个实务模块展开：

| 视频模块 | 与本仓库的对应关系 |
|---|---|
| 找期刊 | 放在 `paper-cover-letter` 之前使用。本仓库的投稿信 skill 默认目标期刊已经确定或至少已缩小范围；找期刊阶段应先判断 scope、文章类型、读者群、格式和投稿限制。 |
| LaTeX 与论文结构 | 论文结构部分对应 `paper-argument-reconstructor`，用于处理章节逻辑、贡献表达和实验支撑关系；LaTeX 保全部分对应 `paper-polisher`，用于 TeX-safe 润色和保全检查。具体格式仍以目标期刊模板和投稿指南为准。 |
| 回复审稿意见 | 对应 `paper-response-to-reviewers`。该 skill 用于拆分审稿意见、先制定修改计划、再撰写逐条回复，并核对每一个承诺的改动是否真的出现在修订稿中。 |

## 运行方式

每个 skill 都支持两种模式。

默认是生成模式：根据各自范围进行起草、修改、审查或规划。

当输入是其他工具或 skill 已经产出的草稿时，切换为检验模式：默认不重写全文，而是检查是否违反硬规则，例如 TeX key 被破坏、数字被改动、novelty 过度声称、引用支撑不足、术语漂移、response letter 承诺了正文中不存在的修改等。

因此，这套 skill 既可以作为主工作流使用，也可以作为其他 AI 工具后的质量控制层。

## 推荐工作流

早期 idea 风险审查：

```text
idea-novelty-auditor -> paper-argument-reconstructor -> paper-polisher
```

综述、相关工作或引言 gap framing：

```text
problem-driven-literature-review -> paper-argument-reconstructor -> paper-polisher
```

完整论文准备：

```text
idea-novelty-auditor -> problem-driven-literature-review -> paper-argument-reconstructor -> paper-polisher
```

期刊投稿材料：

```text
已确定目标期刊 -> paper-cover-letter -> paper-polisher
```

返修和审稿意见回复：

```text
paper-response-to-reviewers -> 按需调用 paper-argument-reconstructor / paper-polisher -> paper-response-to-reviewers 检验
```

## 安装

克隆仓库：

```bash
git clone https://github.com/yujie-jason-zhang/polish_skill.git
cd polish_skill
```

### Codex

安装全部 skill：

```bash
mkdir -p ~/.codex/skills
cp -r idea-novelty-auditor problem-driven-literature-review paper-argument-reconstructor paper-polisher paper-cover-letter paper-response-to-reviewers ~/.codex/skills/
```

只安装单个 skill：

```bash
mkdir -p ~/.codex/skills
cp -r paper-polisher ~/.codex/skills/
```

### Claude Code

安装为个人级 skills：

```bash
mkdir -p ~/.claude/skills
cp -r idea-novelty-auditor problem-driven-literature-review paper-argument-reconstructor paper-polisher paper-cover-letter paper-response-to-reviewers ~/.claude/skills/
```

如果只在某个项目中使用，把需要的 skill 文件夹复制到目标项目的 `.claude/skills/` 目录即可。

### ZIP 上传

对于支持上传 skill、项目文件或知识文件的平台，可以打包全部 skill：

```bash
zip -r academic-paper-skills.zip idea-novelty-auditor problem-driven-literature-review paper-argument-reconstructor paper-polisher paper-cover-letter paper-response-to-reviewers
```

也可以只打包单个 skill：

```bash
zip -r paper-polisher.zip paper-polisher
```

## 项目结构

```text
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

## Prompt 示例

新颖性风险审查：

```text
Use idea-novelty-auditor to audit this research idea before packaging it. Identify dangerous baselines, claims I cannot make, defensible claims, and required validation.
```

问题驱动综述：

```text
Use problem-driven-literature-review to revise this related work section. Organize it by scenario requirements, hidden assumptions, structural gaps, direct competitors, and citation roles.
```

TeX-safe 润色：

```text
Use paper-polisher to polish this TeX section into formal engineering-journal English. Preserve equations, labels, references, citations, variables, numbers, and technical meaning.
```

审稿意见回复：

```text
Use paper-response-to-reviewers to plan and draft a point-by-point response. Do not claim any manuscript change unless it is present or left as a placeholder for confirmation.
```

检验模式：

```text
Use paper-polisher in verification mode to compare this polished TeX against the original. Report broken keys, changed numbers, strengthened claims, or terminology drift without rewriting the whole text.
```

## 保全检查

对于本地 TeX 润色流程，定稿前比较原始文件和润色文件：

```bash
python3 paper-polisher/scripts/check_preservation.py original.tex polished.tex
```

该脚本会报告结构性 TeX key 和数值 token 是否变化。它应运行在原始 TeX 内容和润色后 TeX 内容上，不应运行在包含说明、review report 或 notes 的完整 AI 回复上。

## 参考文献元数据检查

在 related work 或参考文献选择流程中，定稿前先检查 BibTeX：

```bash
python3 problem-driven-literature-review/scripts/check_references.py references.bib
python3 problem-driven-literature-review/scripts/check_references.py references.bib --online --title-search --strict
```

该脚本会捕捉 Google Scholar BibTeX 常见问题，例如必填字段缺失、重复 key/DOI、DOI/year/page range 格式异常、author 字段里出现 `et al.`、会议论文被导出成 `@article`，以及标题中的缩写未用 BibTeX 大括号保护。

## License

MIT License.
