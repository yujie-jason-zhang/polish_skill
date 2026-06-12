# Academic Paper Skills

语言：[English](README.md) | [简体中文](README.zh-CN.md)

这是一个平台无关的学术写作 skill 套件。现在不再把所有流程塞进单个 `paper-polisher`，而是拆成六个职责更清晰的 skill：

- `idea-novelty-auditor`：写论文前先做 idea 新颖性风险审查。
- `problem-driven-literature-review`：按问题驱动逻辑写综述、相关工作和参考文献选择。
- `paper-argument-reconstructor`：重构论文论证主线和章节逻辑。
- `paper-polisher`：做 TeX-safe 英文润色和保全检查。
- `paper-cover-letter`：在论文定稿后组织期刊投稿信（cover letter），不过度声称。
- `paper-response-to-reviewers`：返修时逐条撰写审稿意见回复（response letter），承诺与正文一致。

这样拆分后，每个 skill 只在对应任务下触发，避免“润色一句话”时加载过多 novelty audit 或论文结构设计逻辑。

## 六个 Skill

### idea-novelty-auditor

适合在包装论文前使用。

它用于检查：

- 这个 idea 抽象后像哪些经典算法范式；
- 哪些直接相关工作或相邻领域工作会威胁 novelty；
- 哪些 dangerous baseline 必须比较；
- 审稿人最可能怎样攻击；
- 哪些 claim 不能说；
- 哪些 claim 可以谨慎说；
- 需要哪些实验和 ablation 才能支撑贡献。

### paper-argument-reconstructor

适合在已有论文草稿但整体逻辑、结构、贡献表达或实验支撑关系不清楚时使用。

它用于处理：

- 摘要；
- 引言；
- 方法叙述；
- 公式解释；
- 理论与证明；
- 实验设计逻辑；
- 结果与讨论；
- 结论；
- 全文 problem-driven storyline 诊断。

### problem-driven-literature-review

适合处理 literature review、related work、引言背景、research gap、参考文献选择和 citation-role assignment。

它用于：

- 按目标场景需求组织文献，而不是按方法名堆叠；
- 识别文献路线背后的 hidden assumptions；
- 综合 structural gap；
- 给参考文献分配 claim 角色；
- 公平覆盖直接竞争方法；
- 避免 citation dump、装饰性引用和过度 novelty claim。

### paper-polisher

适合做忠实于原文的 TeX-safe 英文润色。

它重点保留：

- 公式和 TeX 环境；
- label、ref、eqref、cite、bibitem 和 BibTeX key；
- 变量、函数名、模块名、数据集、指标和 baseline；
- 数值、单位、表格值、图中报告值和实验结果；
- 技术含义和 claim 边界。

它保留了 `scripts/check_preservation.py`，用于本地全文或大章节润色后的 TeX key 和数值 token 检查。

### paper-cover-letter

适合在论文基本定稿、需要写期刊投稿信（cover letter）时使用。

它用于：

- 投稿声明（标题、稿件类型、目标期刊）；
- 不超过论文支撑范围的贡献陈述；
- 与目标期刊 scope 和读者群的契合说明；
- 原创性与伦理声明（由作者确认，或留占位待填）；
- 推荐/回避审稿人和通讯作者信息。

它复用论文已有的贡献，不新造贡献；未确认的具体信息一律留 `[...]` 占位，不编造。

### paper-response-to-reviewers

适合返修阶段逐条撰写审稿意见回复（point-by-point response）。

它用于：

- 按编辑、副编辑、各审稿人组织意见；
- 给每条意见定策略：接受并修改 / 澄清误解 / 有据反驳 / scope 让步 / 补实验；
- 每条按“引用意见 → 致谢 → 表态 → 说明改动 → 精确指向正文位置”撰写；
- 核对回复里承诺的每处改动是否真的落在正文里；
- 被指 overstatement 时主动软化 claim，而不是硬撑。

它只陈述作者真正做了的修改，未确认的指向留 `[Section X, page Y]` 占位。

## 检验模式（Verification Mode）

每个 skill 都有两种模式。默认是生成或修改——润色、重构论证、起草综述或投稿信、撰写回复。当输入是其他工具或 skill 已经产出的文本时，skill 转入检验模式：不重写，而是按自己的保真规则核对这份草稿，只报告偏差——TeX 或 key 被破坏、数字被改、claim 被夸大、术语不一致、回复里承诺却没落实的改动等等。

这让整个套件成为一个保真检验层，与更强的生成型 skill 互补而非竞争：让别的 skill 负责写，再用本套件对应的 skill 检验它产出的内容，除非违反硬规则，否则不覆盖其措辞。

这一行为写在 `SKILL.md` 里，所以任何能加载 SKILL.md 的 agent（Claude Code、Codex）都能用，无需额外配置。

如果想让“别的工具产出草稿后自动检验”，需要在你的 agent 指令文件里加一条规则。这部分是各 agent 各自的、放在你本地配置里，不在克隆的仓库内。

Claude Code，加到 `CLAUDE.md`：

```text
对论文文本，把这套学术论文 skill 当作检验层。
当某段已由其他 skill 或工具起草、润色或改写，定稿前用本套件对应 skill 以检验模式过一遍：
核对保真（TeX/公式/引用/key、数字、claim 边界、术语、承诺的改动）并报告偏差，
除非违反硬规则，否则不覆盖其措辞。
```

Codex，把同样的规则加到 `AGENTS.md`。

## 项目结构

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

## 安装方式

根据你的 AI 环境选择安装方式即可。

### Codex 本地 Skills

克隆仓库，并把六个 skill 文件夹复制到 Codex 的 skills 目录：

```bash
git clone https://github.com/MercuryZzz-123/polish_skill.git
mkdir -p ~/.codex/skills
cp -r polish_skill/idea-novelty-auditor ~/.codex/skills/
cp -r polish_skill/problem-driven-literature-review ~/.codex/skills/
cp -r polish_skill/paper-argument-reconstructor ~/.codex/skills/
cp -r polish_skill/paper-polisher ~/.codex/skills/
cp -r polish_skill/paper-cover-letter ~/.codex/skills/
cp -r polish_skill/paper-response-to-reviewers ~/.codex/skills/
```

如果只需要其中一个，也可以只复制对应文件夹。

### Claude Code 本地 Skills

个人级 Claude Code skill 可以安装到：

```bash
git clone https://github.com/MercuryZzz-123/polish_skill.git
mkdir -p ~/.claude/skills
cp -r polish_skill/idea-novelty-auditor ~/.claude/skills/
cp -r polish_skill/problem-driven-literature-review ~/.claude/skills/
cp -r polish_skill/paper-argument-reconstructor ~/.claude/skills/
cp -r polish_skill/paper-polisher ~/.claude/skills/
cp -r polish_skill/paper-cover-letter ~/.claude/skills/
cp -r polish_skill/paper-response-to-reviewers ~/.claude/skills/
```

如果只想在某个项目中使用，也可以把需要的 skill 文件夹复制到目标项目的 `.claude/skills/` 目录下。

### 网页 AI 平台

对于支持上传 skill、项目文件或知识文件的网页 AI 平台，可以打包全部 skill：

```bash
git clone https://github.com/MercuryZzz-123/polish_skill.git
cd polish_skill
zip -r academic-paper-skills.zip idea-novelty-auditor problem-driven-literature-review paper-argument-reconstructor paper-polisher paper-cover-letter paper-response-to-reviewers
```

也可以只打包单个 skill：

```bash
zip -r paper-polisher.zip paper-polisher
```

## 推荐工作流

早期 idea 阶段：

```text
idea-novelty-auditor -> paper-argument-reconstructor -> paper-polisher
```

需要写 related work 或 literature review 的论文：

```text
idea-novelty-auditor -> problem-driven-literature-review -> paper-argument-reconstructor -> paper-polisher
```

已有论文草稿且需要处理 related work 或 gap framing 时：

```text
problem-driven-literature-review -> paper-argument-reconstructor -> paper-polisher
```

已有论文草稿但不需要处理综述时：

```text
paper-argument-reconstructor -> paper-polisher
```

只做局部或全文英文润色：

```text
paper-polisher
```

论文定稿后写期刊投稿信：

```text
paper-cover-letter
```

返修阶段逐条回复审稿意见：

```text
paper-response-to-reviewers
```

## 使用示例

新颖性风险审查：

```text
Use idea-novelty-auditor to audit this research idea before packaging it. Identify the dangerous baselines, claims I cannot make, cautious defensible claims, and experiments required.
```

论证重构：

```text
Use paper-argument-reconstructor to diagnose the introduction and rebuild it around a problem-driven storyline. Do not invent new claims or results.
```

综述与相关工作：

```text
Use problem-driven-literature-review to revise the related work section. Organize the literature by scenario requirements, hidden assumptions, structural gaps, direct competitors, and claim-first citation roles.
```

TeX-safe 润色：

```text
Use paper-polisher to polish the following TeX section into formal engineering-journal English. Preserve all equations, labels, references, citations, variables, numerical values, and technical meaning.
```

投稿信：

```text
Use paper-cover-letter to draft a submission cover letter for the target journal. Summarize the contribution without overclaiming, keep novelty hedged, and leave placeholders for the journal name, editor, and ethics declarations.
```

审稿意见回复：

```text
Use paper-response-to-reviewers to draft a point-by-point response. Classify each comment, reply with quote-thank-position-change-pointer, flag any promised change I still need to confirm is in the manuscript, and do not fabricate results or pointers.
```

检验（核对别的工具已产出的草稿）：

```text
Use paper-polisher in verification mode to check this already-polished TeX against the original. Report any broken keys, changed numbers, strengthened claims, or terminology drift, but do not rewrite it.
```

## 可选保全检查

对于本地全文或大章节润色流程，可以在最终确认前比较原始 TeX 文件和润色后的 TeX 文件：

```bash
python3 paper-polisher/scripts/check_preservation.py original.tex polished.tex
```

这个脚本会报告结构性 TeX key 和数值 token 是否发生变化。它只应运行在原始 TeX 内容和润色后的 TeX 内容上，不应运行在包含 review report 或 notes 的完整 AI 回复上。

## License

本项目使用 MIT License。
