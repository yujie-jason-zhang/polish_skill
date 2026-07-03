# Academic Paper Skills

语言：[English](README.md) | [简体中文](README.zh-CN.md)

Academic Paper Skills 是一组面向学术论文写作、投稿和返修流程的本地 AI agent 技能。仓库按任务边界拆成七个独立 skill，每个 skill 都有明确的适用范围、检验模式和保全规则。

它面向已经在处理论文草稿、TeX 文件、审稿意见、投稿信和期刊格式要求的用户；目标不是做一个泛化的“论文助手”，而是把论文工作流中容易失真、过度声称或漏改的部分拆成可复用的专业流程。

## Skill 目录

| Skill | 适用场景 | 主要输出 |
|---|---|---|
| `idea-novelty-auditor` | 研究想法、贡献陈述或论文主线在包装前需要做新颖性风险审查。 | 新颖性风险、危险基线、审稿人攻击点、可防守的主张边界、所需实验。 |
| `problem-driven-literature-review` | 文献综述、相关工作、引言背景、研究缺口或引用计划需要重构。 | 问题驱动的综述逻辑、S-R-L-H-G-M-C-V 工作表、参考文献角色、缺口与贡献映射。 |
| `paper-argument-reconstructor` | 已有草稿，但摘要、引言、章节逻辑、方法叙述或实验支撑关系不清楚。 | 章节逻辑重构、贡献表达、论文主线诊断、论文结构调整建议。 |
| `paper-polisher` | 中文或英文 TeX 论文文本需要忠实的学术英文润色或局部修改。 | TeX-safe 润色稿、术语一致性检查、保真报告、可选本地保全检查。 |
| `journal-recommender` | 已完成或接近完成的论文需要推荐目标期刊、快速审稿选项，或验证已有期刊 shortlist 是否合适。 | 四档期刊推荐，包含官网、LetPub、索引、预警风险和期刊近期相关文章证据。 |
| `paper-cover-letter` | 论文基本定稿，需要写期刊投稿信。 | 投稿信、受论文证据约束的贡献陈述、期刊范围匹配说明、未确认信息占位。 |
| `paper-response-to-reviewers` | 收到编辑或审稿意见后，需要制定返修计划并逐条回复。 | 意见拆解、严重程度和证据等级、返修计划、逐条回复信、一致性检查。 |

## 配套视频

B 站视频：[Article Form 0 to 1](https://www.bilibili.com/video/BV1w9fCBGER1/)

视频围绕论文从准备到返修的三个实务模块展开：

| 视频模块 | 与本仓库的对应关系 |
|---|---|
| 找期刊 | 在 `paper-cover-letter` 之前使用 `journal-recommender`，根据期刊范围、论文层级、索引、开放获取/预算、审稿速度、预警风险和期刊近期相关文章证据缩小目标期刊。不要根据当前 LaTeX 模板推断目标出版社；选定期刊后再重排格式。 |
| LaTeX 与论文结构 | 论文结构部分对应 `paper-argument-reconstructor`，用于处理章节逻辑、贡献表达和实验支撑关系；LaTeX 保全部分对应 `paper-polisher`，用于 TeX-safe 润色和保全检查。具体格式仍以目标期刊模板和投稿指南为准。 |
| 回复审稿意见 | 对应 `paper-response-to-reviewers`。该 skill 用于拆分审稿意见、先制定修改计划、再撰写逐条回复，并核对每一个承诺的改动是否真的出现在修订稿中。 |

## 运行方式

每个 skill 都支持两种模式。

默认是生成模式：根据各自范围进行起草、修改、审查或规划。

当输入是其他工具或 skill 已经产出的草稿时，切换为检验模式：默认不重写全文，而是检查是否违反硬规则，例如 TeX key 被破坏、数字被改动、新颖性过度声称、引用支撑不足、术语漂移、审稿回复信承诺了正文中不存在的修改等。

因此，这套 skill 既可以作为主工作流使用，也可以作为其他 AI 工具后的质量控制层。

## 人工核对

所有 AI 生成的修改都应先视为草稿。即使 skill 已经尽量保留 TeX key、citation、reference、数字和专业术语，润色或改写仍可能引入细微错误。投稿或复用前，建议人工对照原稿核对实质性修改，重点检查技术含义、数值、公式、引用支撑、参考文献元数据和目标期刊格式要求。

## 推荐工作流

早期想法风险审查：

```text
idea-novelty-auditor -> paper-argument-reconstructor -> paper-polisher
```

综述、相关工作或引言缺口梳理：

```text
problem-driven-literature-review -> paper-argument-reconstructor -> paper-polisher
```

完整论文准备：

```text
idea-novelty-auditor -> problem-driven-literature-review -> paper-argument-reconstructor -> paper-polisher
```

期刊投稿材料：

```text
journal-recommender -> paper-cover-letter -> paper-polisher
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
cp -r idea-novelty-auditor problem-driven-literature-review paper-argument-reconstructor paper-polisher journal-recommender paper-cover-letter paper-response-to-reviewers ~/.codex/skills/
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
cp -r idea-novelty-auditor problem-driven-literature-review paper-argument-reconstructor paper-polisher journal-recommender paper-cover-letter paper-response-to-reviewers ~/.claude/skills/
```

如果只在某个项目中使用，把需要的 skill 文件夹复制到目标项目的 `.claude/skills/` 目录即可。

### ZIP 上传

对于支持上传 skill、项目文件或知识文件的平台，可以打包全部 skill：

```bash
zip -r academic-paper-skills.zip idea-novelty-auditor problem-driven-literature-review paper-argument-reconstructor paper-polisher journal-recommender paper-cover-letter paper-response-to-reviewers
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

journal-recommender/
|-- SKILL.md
`-- references/
    `-- journal_recommendation_guide.md

paper-response-to-reviewers/
|-- SKILL.md
`-- references/
    `-- response_letter_guide.md
```

## 提示词示例

新颖性风险审查：

```text
使用 idea-novelty-auditor 审查这个研究想法在包装成论文前的新颖性风险。请指出危险基线、不能声称的内容、可以防守的贡献边界，以及还需要补充的验证。
```

问题驱动综述：

```text
使用 problem-driven-literature-review 修改这段 related work。请按场景需求、隐藏假设、结构性缺口、直接竞争工作和引用角色来重组。
```

TeX-safe 润色：

```text
使用 paper-polisher 将这段 TeX 润色成正式工程期刊英文。请保留公式、label、ref、citation、变量、数字和技术含义。
```

期刊推荐：

```text
使用 journal-recommender 为这篇接近定稿的论文推荐目标期刊。请联网核验期刊官网、LetPub、索引、OA/APC、预警风险和该期刊近期相关文章；不要根据当前 LaTeX 模板决定目标期刊。
```

审稿意见回复：

```text
使用 paper-response-to-reviewers 制定返修计划并起草逐条回复。除非正文中已经完成相应修改，或明确留下待确认占位，否则不要声称已经修改。
```

检验模式：

```text
使用 paper-polisher 的检验模式，对比润色后的 TeX 和原文。请只报告被破坏的 key、被改动的数字、被加强的主张或术语漂移，不要重写全文。
```

## 保全检查

对于本地 TeX 润色流程，定稿前比较原始文件和润色文件：

```bash
python3 paper-polisher/scripts/check_preservation.py original.tex polished.tex
```

该脚本会报告结构性 TeX key 和数值 token 是否变化。它应运行在原始 TeX 内容和润色后 TeX 内容上，不应运行在包含说明、审查报告或备注的完整 AI 回复上。

## 参考文献元数据检查

在 related work 或参考文献选择流程中，定稿前先检查 BibTeX：

```bash
python3 problem-driven-literature-review/scripts/check_references.py references.bib
python3 problem-driven-literature-review/scripts/check_references.py references.bib --online --title-search --strict
```

如需检查项目自己的方法名或必须保留大小写的专有名，可以额外指定术语：

```bash
python3 problem-driven-literature-review/scripts/check_references.py references.bib \
  --protected-title-term "Reliable-loc" \
  --protected-title-term "Monte Carlo"
```

该脚本会捕捉 Google Scholar BibTeX 常见问题，例如必填字段缺失、重复 key/DOI、DOI/year/page range 格式异常、author 字段里出现 `et al.`、会议论文被导出成 `@article`，以及标题中需要 BibTeX 大括号保护的大小写，包括全大写缩写、`LiDAR` 这类 mixed-case 术语，以及 `Monte Carlo` 或方法名这类已配置 title 术语。

## 许可证

MIT License.
