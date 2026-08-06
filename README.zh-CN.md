# Academic Paper Skills

语言：[English](README.md) | [简体中文](README.zh-CN.md)

Academic Paper Skills 是一组面向论文精读、学术写作、投稿和返修流程的本地 AI agent 技能。仓库按任务边界拆成九个独立 skill，每个 skill 都有明确的适用范围、证据边界、检验模式或保全规则。

它面向需要处理论文 PDF、论文草稿、TeX 文件、审稿意见、投稿信和期刊格式要求的用户；目标不是做一个泛化的“论文助手”，而是把论文工作流中容易失真、过度声称或漏改的部分拆成可复用的专业流程。

## Skill 目录

| Skill | 适用场景 | 主要输出 |
|---|---|---|
| `read-paper-to-notes` | 已提供一篇学术论文 PDF，需要精读、解释或整理成结构化笔记。 | 带证据定位的 Markdown 精读笔记，覆盖问题、方法、公式、实验、结果、局限和研究启发。 |
| `idea-novelty-auditor` | 研究想法、贡献陈述或论文主线在包装前需要做新颖性风险审查。 | 新颖性风险、危险基线、审稿人攻击点、可防守的主张边界、所需实验。 |
| `problem-driven-literature-review` | 文献综述、相关工作、引言背景、研究缺口或引用计划需要重构。 | 问题驱动的综述逻辑、S-R-L-H-G-M-C-V 工作表、参考文献角色、缺口与贡献映射。 |
| `paper-argument-reconstructor` | 已有草稿，但摘要、引言、章节逻辑、方法叙述或实验支撑关系不清楚。 | 章节逻辑重构、贡献表达、论文主线诊断、论文结构调整建议。 |
| `experiment-section-auditor` | 实验章节、消融计划或结果叙述需要根据既定 claims 和真实资源限制做审计。 | Claim-evidence map、最小实验或消融缺口、冗余实验删减建议、结果叙述问题、可行性免责声明。 |
| `paper-polisher` | 中文或英文 TeX 论文需要忠实学术英文润色、原稿对照核验、术语/记号/数值一致性审计，或执行作者确认的记号统一。 | 唯一 authoritative TeX 结果或只读审计报告，并将保全、覆盖范围和一致性 finding 分开。 |
| `journal-recommender` | 已完成或接近完成的论文需要推荐目标期刊、快速审稿选项，或验证已有期刊 shortlist 是否合适。 | 四档期刊推荐，包含官网、LetPub、索引、预警风险和期刊近期相关文章证据。 |
| `paper-cover-letter` | 论文基本定稿，需要写期刊投稿信。 | 投稿信、受论文证据约束的贡献陈述、期刊范围匹配说明、未确认信息占位。 |
| `paper-response-to-reviewers` | 收到编辑或审稿意见后，需要制定返修计划并逐条回复。 | 意见拆解、严重程度和证据等级、返修计划、逐条回复信、一致性检查。 |

## 配套视频

B 站视频：[Article Form 0 to 1](https://www.bilibili.com/video/BV1w9fCBGER1/)

视频围绕论文从准备到返修的三个实务模块展开：

| 视频模块 | 与本仓库的对应关系 |
|---|---|
| 找期刊 | 在 `paper-cover-letter` 之前使用 `journal-recommender`，根据期刊范围、论文层级、索引、开放获取/预算、审稿速度、预警风险和期刊近期相关文章证据缩小目标期刊。不要根据当前 LaTeX 模板推断目标出版社；选定期刊后再重排格式。 |
| LaTeX 与论文结构 | 论文结构部分对应 `paper-argument-reconstructor`，用于处理章节逻辑和贡献表达；实验章节对应 `experiment-section-auditor`，用于审计实验集合最小性、消融充分性和结果叙述；`paper-polisher` 用于 TeX-safe 润色、保全检查，以及原稿内部术语、记号和数值一致性审计。具体格式仍以目标期刊模板和投稿指南为准。 |
| 回复审稿意见 | 对应 `paper-response-to-reviewers`。该 skill 用于拆分审稿意见、先制定修改计划、再撰写逐条回复，并核对每一个承诺的改动是否真的出现在修订稿中。 |

## 运行方式

大多数起草和审计类 skill 支持生成与检验工作流。部分 skill 还提供边界更窄的一致性审计或授权修改模式。

默认是生成模式：根据各自范围进行起草、修改、审查或规划。

用户要求对照或质量检查已有草稿时使用检验模式。用户明确意图优先于文本由谁生成。检验模式以报告偏差为主；只有用户另行要求修改时才替换原文。

对 `paper-polisher` 而言，source-to-output 检验必须同时提供 original 与 candidate；缺少 original 时，比较型字段标为 `NOT ASSESSED`，且 verification mode 绝不修复 candidate。该 skill 还提供术语、数学记号和原稿内部数值的一致性审计模式，以及只执行精确 author-approved mapping 的记号统一模式。这些模式分别输出审计 `Coverage` 与当前覆盖范围内的 `Result`。

因此，这套 skill 既可以作为主工作流使用，也可以作为其他 AI 工具后的质量控制层。

`read-paper-to-notes` 则区分完整精读、聚焦分析和外部核验三种模式。它默认以用户提供的论文为证据边界，并明确标记阅读推断和外部核验信息。

## 人工核对

所有 AI 生成的笔记和修改都应先视为草稿。即使 skill 已经应用证据或保全规则，阅读、润色和改写仍可能引入细微错误。投稿或复用前，建议人工对照源论文或原稿核对实质性内容，重点检查技术含义、数值及其顺序、单位、正号/负号或正负号标记、公式、引用支撑、参考文献元数据和目标期刊格式要求。

## 推荐工作流

单篇论文精读：

```text
论文 PDF -> read-paper-to-notes -> Markdown 笔记
```

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
idea-novelty-auditor -> problem-driven-literature-review -> paper-argument-reconstructor -> experiment-section-auditor -> paper-polisher
```

实验章节审计：

```text
paper-argument-reconstructor / idea-novelty-auditor 确定 claims -> experiment-section-auditor -> paper-polisher
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
cp -r read-paper-to-notes idea-novelty-auditor problem-driven-literature-review paper-argument-reconstructor experiment-section-auditor paper-polisher journal-recommender paper-cover-letter paper-response-to-reviewers ~/.codex/skills/
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
cp -r read-paper-to-notes idea-novelty-auditor problem-driven-literature-review paper-argument-reconstructor experiment-section-auditor paper-polisher journal-recommender paper-cover-letter paper-response-to-reviewers ~/.claude/skills/
```

如果只在某个项目中使用，把需要的 skill 文件夹复制到目标项目的 `.claude/skills/` 目录即可。

### ZIP 上传

对于支持上传 skill、项目文件或知识文件的平台，可以打包全部 skill：

```bash
zip -r academic-paper-skills.zip read-paper-to-notes idea-novelty-auditor problem-driven-literature-review paper-argument-reconstructor experiment-section-auditor paper-polisher journal-recommender paper-cover-letter paper-response-to-reviewers
```

也可以只打包单个 skill：

```bash
zip -r paper-polisher.zip paper-polisher
```

## 项目结构

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

## 提示词示例

单篇论文精读：

```text
使用 read-paper-to-notes 精读附件中的论文并生成中文 Markdown 笔记。请区分作者陈述、阅读推断和外部核验信息，并为重要结论标注页码、章节、公式、图或表格位置。
```

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
使用 paper-polisher 将这段 TeX 润色成正式工程期刊英文。请保留公式、label、ref、citation、变量、每一个数字和单位、数值 token 顺序、正号/负号或正负号标记，以及技术含义。
```

数学记号审计：

```text
使用 paper-polisher 审计这篇完整 TeX 论文的数学记号。请解析 root 与 included files，将 Coverage 和 Result 分开，并用 SYM-* 报告“同一对象使用多个符号”或“同一符号表示不同对象”的情况，给出准确位置与依据；不要修改任何内容。
```

原稿内部数值一致性审计：

```text
使用 paper-polisher 检查同一 metric、实验设置、样本量、表格/正文数值、单位和正负号是否在全文一致。请返回带精确条件与位置的 NUM-* finding，不要修改或推断任何数值。
```

作者确认的记号统一：

```text
使用 paper-polisher 的 approved notation-normalization mode 和这份精确 entity-to-symbol mapping。只执行 mapping 中的替换，将每项记录为 AUTHORIZED CHANGE，保持所有数字、单位、正负号、key 和无关公式不变，并报告无法解析的宏或图内 asset。
```

实验章节审计：

```text
使用 experiment-section-auditor 根据论文 claims 审计这段实验章节。请指出 unsupported claims、不必要实验、缺失消融、流水账式结果叙述，以及在我已说明资源条件下的可行性假设。
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
使用 paper-polisher 的检验模式，对比 candidate TeX 和 original。请报告 candidate 新引入的 broken key、公式变化、数字/单位/正负号的修改或调序、加强的 claim 和术语漂移，并将原稿自身的 TERM-*、SYM-*、NUM-* finding 分开。不要修改 candidate；缺少 original 时，所有比较型检查标为 NOT ASSESSED。
```

## 保全检查

对于单文件 TeX 流程，定稿前比较 original 与 candidate：

```bash
python3 paper-polisher/scripts/check_preservation.py original.tex candidate.tex
```

只有用户明确允许新增普通正文时才使用 `--allow-additions`。它不允许结构 key、图片 asset、数学区域、数值 token、单位或正负号的任何新增、删除、修改或调序，也不是记号统一模式。数值保护也覆盖标识符、注释、literal 示例、URL 和受保护参数中的数字。可识别的注释和 literal/code 区域在所有模式下仍是必须原样保留的源码，包括注释的行边界语义，以及它们相对受保护公式和 TeX 结构的顺序；自定义且未识别的 literal 宏仍须人工对照。

多文件论文传入双方 authoritative root TeX 文件：

```bash
python3 paper-polisher/scripts/check_preservation.py original/main.tex candidate/main.tex --project
```

Project mode 会跟踪静态 `input`/`include`/`subfile`/`subfileinclude` 指令以及 `import`/`subimport`/`inputfrom`/`includefrom` 系列，并保留当前及此前的 import 目录上下文；路径缺失、动态生成或形成循环时会直接失败。

对于在 checked scope 内全局成立的精确 author-approved math-token mapping，可重复使用 `--approved-symbol-map`：

```bash
python3 paper-polisher/scripts/check_preservation.py original.tex normalized.tex \
  --approved-symbol-map 'M=N'
```

该参数只用于 normalization，会拒绝明确的数字、货币、百分比和正负号 mapping，也不允许无关的 prose 或 math 变化。Mapping 永远不能授权单位修改；`m` 等歧义裸 glyph 必须结合 entity-aware authorization ledger 和人工单位复核。若 mapping 只适用于部分位置，或 glyph 存在有意复用，应改用 location-aware authorization ledger 和 author-approved baseline。

检查器应运行在论文文件上，不能包含说明、审查报告或备注。脚本通过只证明其支持范围内的原稿到输出稿保全。数值扫描覆盖可识别的十进制、英文文字数、带上下文的罗马数字和 Unicode 数字，以及处于受支持的数值/公式/literal/macro 锚点、TeX 连接、括号或明确提示语境中的正负号、标记、货币、常见单位和单位形式复合 token；所有无法识别的形式或语境，包括歧义的独立单位 glyph，仍须人工对照。原稿内部术语、记号和数值一致性仍需执行 skill 中定义的语义审计与 completeness gate。

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
