# TeX-Safe 学术润色指南

## 目录

- [核心目标](#核心目标)
- [原稿到输出稿的保全](#原稿到输出稿的保全)
- [结构性 key 与可引用对象](#结构性-key-与可引用对象)
- [忠实语言修改](#忠实语言修改)
- [术语一致性](#术语一致性)
- [数学记号一致性](#数学记号一致性)
- [原稿内部数值一致性](#原稿内部数值一致性)
- [全文覆盖范围](#全文覆盖范围)
- [句式与破折号规则](#句式与破折号规则)
- [各模式流程](#各模式流程)
- [保全检查器](#保全检查器)
- [输出示例](#输出示例)

## 核心目标

在不改变论文技术事实的前提下，将中文或英文 TeX 论文文本处理为正式、客观、克制的工程期刊英文。具体操作由 `SKILL.md` 中的模式决定：可以润色正文、对照原稿核验候选稿、只审计术语/记号/数值一致性，或者只执行作者明确确认过的记号映射。

必须分开回答四个问题：

1. 候选稿是否保留了原稿中的受保护内容？
2. 原稿内部术语是否一致？
3. 原稿内部数学记号是否一致？
4. 同一数值事实、单位和正负号是否在原稿各处一致？

保全检查通过不能证明后三项语义一致；发现原稿自身不一致也不代表可以自动改稿。

## 原稿到输出稿的保全

下列内容必须原样保留：

- `$...$`、`\(...\)`、`\[...\]` 和命名数学环境中的全部行内、行间公式；
- figure、table、algorithm、theorem、proof、lemma、definition、remark 等环境；
- label、reference、citation、BibTeX key、图片路径等结构命令及其参数；
- comment、verbatim、listing 环境和 inline literal 命令等注释或 literal/code 源码，以及注释位于行内还是独立行的边界和它们相对受保护公式、TeX 结构的顺序；
- 变量与函数记号，除非某个替换已经出现在作者确认的精确 symbol mapping 中；
- 所有数值、数值 token 顺序、单位、百分比、维度、样本量、参数、表格值、图中数值、显著性标记，以及正号、负号和正负号；
- 技术含义、条件、假设、算法、证明步骤、实验、baseline、数据集、指标和结果。

数值硬保护适用于润色、翻译、普通正文新增、检验、一致性审计和记号统一，也覆盖标识符中的数字，以及注释、literal 示例、URL 和受保护命令参数中的数值 token。不得为了改善语序新增、删除、修改或调换任何数值。只有在受保护的公式、数字、单位和符号顺序均不变化时，才可调整句子或从句位置。本 skill 不设数值修改例外；若数值确需修正，应请用户在 paper-polisher 之外修改，并将修正后的 TeX 作为新的作者确认 baseline。

保全检查器在所有模式下都把每段可识别的注释和 literal/code 区域视为必须原样保留的源码。不得把正文变成注释，不得把文字移入或移出 literal 区域，不得把行内 `%` 改成独立行注释，也不得让这些区域跨过受保护公式或 TeX 结构。这样既保护可见内容，也保护 TeX 中注释吞掉换行的语义。自定义或未识别的 literal 宏仍须人工逐项对照。

结构命令的参数与 key 必须原样保留。例如：

```latex
\label{sec:method}
\ref{sec:method}
\eqref{eq:risk}
\cite{smith2023,chen2024}
```

不能变成：

```latex
\label{sec:methodology}
\ref{method}
\eqref{eq:risk_metric}
\cite{Smith2023}
```

不要静默修正可疑的数值、单位、正负号、引用、参考文献记录或作者姓名顺序，只报告问题。本 skill 不修改任何数值内容，也不得根据附近表格、走势、单位换算或预期结果猜测正确值。应请用户提供在外部修正并确认过的 TeX，作为新的 baseline。

## 结构性 key 与可引用对象

用户明确要求新增可引用对象时，应先沿用论文已有 label 规范。若没有规范，使用语义化 typed label：

| 对象 | 前缀 | 示例 |
|---|---|---|
| 章节 | `sec:` | `\label{sec:method}` |
| 小节 | `subsec:` | `\label{subsec:ablation_setup}` |
| 图片 | `fig:` | `\label{fig:framework}` |
| 表格 | `tab:` | `\label{tab:diff_methods}` |
| 公式 | `eq:` | `\label{eq:loss_function}` |
| 算法 | `alg:` | `\label{alg:training}` |
| 定理 | `thm:` | `\label{thm:convergence}` |
| 附录 | `app:` | `\label{app:implementation}` |

原稿使用下划线风格时，应继续使用 `\label{tab_diff_methods}` 一类形式。禁止生成 `\label{tab}`、`\ref{tab}`、`\label{fig}`、`\ref{fig}`、`\label{tmp}` 或 `\label{label}` 等裸占位 key。

用户确认一个新增 label、reference、图片路径、尺寸或裁剪参数后，应将其视为受保护内容。新增 table、figure、equation、citation、asset 或其他结构对象不能通过 `--allow-additions` 放行；应先让用户确认修改后的论文并将其作为新 baseline，后续再做严格比较。

引用已有对象时必须先定位 exact label。若原稿包含：

```latex
\label{tab:ablation}
\label{tab:errors}
\label{tab:torwic_errors}
```

讨论 controlled indoor evaluation 的段落可以写：

```latex
Tables~\ref{tab:ablation} and~\ref{tab:errors}
```

不要替换为泛化 label，也不要加入无关表格。

`Fig.`/`Figure`、`Eq.`/`Equation`、`Sec.`/`Section` 应匹配原稿或期刊既有风格。不得硬编码 `Figure 1` 或 `Table 1`。Caption 也不能重复 LaTeX 自动生成的对象名称和编号：

```latex
\caption{Overall framework of the proposed method.}
```

新增图片时，同时保护 label 和 asset signature：

```latex
\begin{figure}
  \centering
  \includegraphics[width=0.85\linewidth]{figures/framework.pdf}
  \caption{Overall framework of the proposed method.}
  \label{fig:framework}
\end{figure}
```

未经明确授权和新 baseline，不得简化路径、替换文件或修改用户确认过的图片参数。

## 忠实语言修改

允许的正文修改包括：

- 拆分过长句；
- 合并重复表达；
- 增加原文已经隐含的轻量逻辑连接；
- 将口语改为正式学术表达；
- 在不增加技术内容的前提下明确局部逻辑；
- 在公式、结构 key、数字、单位和正负号均不改变顺序时，调整纯正文从句或句子。

禁止的修改包括：

- 改动定义、假设、算法、证明、公式或实验设置；
- 新增实验、理论保证、限制、应用或部署价值；
- 把相关性写成因果性；
- 把局部结果扩大为全面优越性；
- 把启发式方法写成理论保证；
- 改动 baseline、数据集、指标、数值、单位、符号或报告结果。

## 术语一致性

对于术语密集章节或全文，建立术语表：

| 对象或概念 | Canonical term/family | 定义位置 | 使用位置 | 允许的上下文形式 | 避免或保留给 |
|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... |

双向检查：

- 同一对象是否在没有明示区分时使用了多个术语；
- 同一术语是否在相同或重叠作用域中表示不同对象。

不得为了词汇变化替换 canonical technical term。应根据原稿定义区分 `open-vocabulary`、`open-set`、`open-world`，以及 `risk-aware`、`safety-aware`、`uncertainty-aware` 等相关但不等价的术语。

术语问题使用 `TERM-*`，Coverage/Result 使用 `SKILL.md` 中的统一协议。除非原稿已经明确建立或作者确认，否则推荐术语只是 provisional choice。

## 数学记号一致性

将记号视为数学对象与显示符号之间的双向映射，建立记号表：

| 数学对象 | 符号 | 定义位置 | 使用位置 | 作用域 | 类型/维度 | 坐标系 | 明示别名 |
|---|---|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... | ... | ... |

双向检查：

- **对象到符号：** 同一对象是否使用多个符号，例如同一变换矩阵在不同章节被记作 `M` 和 `N`。
- **符号到对象：** 同一显示符号是否在相同或重叠作用域中表示不同对象。

判断时结合显式定义、正文描述、运算对象、类型、维度、坐标系、单位和公式依赖。大小写、字体、字重、重音、撇号、上下标都可能编码对象身份，不能当作纯排版差异。

以下情况不能仅因字形复用就报告冲突：

- 局部哑变量、循环或求和下标；
- 明确定义的别名；
- 不同时间步或坐标系中的有意区分；
- 作用域明显不重叠的合法复用。

证据已经证明冲突时，即使仍需作者选择最终符号，也应将 finding 标为 `ISSUE REPORTED`。只有对象身份或原意本身无法确定时才用 `AUTHOR DECISION REQUIRED`。Canonical choice 另设字段，不与冲突确定性混为一谈。

### 执行已确认映射

修改前记录精确授权：

| Finding | 数学对象 | 原符号 | 已确认符号 | 包含的位置/作用域 | 别名或排除项 |
|---|---|---|---|---|---|
| `SYM-...` | ... | ... | ... | ... | ... |

然后：

1. 只修改 mapping 中列出的符号。
2. 同步处理 TeX 可见的公式、正文、算法、caption、表格和附录中的相关定义与使用。
3. 保持数字、单位、维度、正负号、结构 key 和无关公式完全不变且顺序不变。
4. 将每一项替换记录为 `AUTHORIZED CHANGE`，所有 mapping 之外的差异都必须失败或报告。
5. 检查受影响图中的符号。没有可编辑源文件时，报告未完成的 asset，不得声称统一完成。
6. 有 mapping-aware validation 时直接使用；否则先让作者确认统一后的 TeX，将其设为新 baseline，后续润色再与该 baseline 严格比较。

如果用户同时要求记号统一和正文润色，应先完成并确认 mapping-only 阶段，再将其输出作为独立润色阶段的 source。不得把包含 prose 与 symbol 两类修改的 combined diff 当作 mapping-only validation。

不得用普通 additions-aware 检查为记号修改放行。

## 原稿内部数值一致性

为重要报告值和设置值建立数值表：

| 数量或事实 | 数值 | 单位 | 符号/方向 | 条件或实验 | 位置 | 对应表格/图片 |
|---|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... | ... |

检查同一数量与条件在以下位置是否一致：

- 摘要、正文、结论和附录；
- 方法设置与实验设置；
- 正文、表格、caption 和已提供图片；
- 样本数、数据划分、epoch、维度、阈值和超参数；
- 原始值、百分比、增量、置信区间、不确定性和显著性标记；
- 单位、单位前缀、正负方向，以及 `\pm` 等正负号形式。

比较前必须匹配 metric、dataset、split、condition、aggregation 和 rounding convention。四舍五入结果、单位换算、分 split 结果或不同符号约定可能合法；无法证明等价或冲突时使用 `AUTHOR DECISION REQUIRED`，不得猜测。

数值问题使用 `NUM-*`。例如，同一 test-set accuracy 在相同条件下分别写成 `91.2\%` 和 `92.1\%`，属于明确的 `ISSUE REPORTED`。两处都不能自动修改；应请用户在本 skill 之外修正并确认原稿，再提供新的 baseline。

数值一致性是原稿内部语义审计，不能削弱原稿到输出稿的硬保护。即使数值明显可疑，润色或记号统一时也必须原样保留。

## 全文覆盖范围

只有通过 `SKILL.md` 中的 completeness gate 后，才可使用 `Coverage: FULL MANUSCRIPT`。

从 authoritative root file 开始，保留解析后的文档顺序。跟踪静态可解析的 `\input`、`\include`、`\subfile`、`\import` 和项目特有等价结构。无法解析的条件 include、宏生成路径、缺失的生成表格、独立 supplement 和循环引用都属于 coverage gap。

必须检查所有生成记号的宏定义和使用，而不仅是两个版本之间发生变化的宏。还要识别 custom math environment，以及算法或 diagram code 中的记号。检查器即使保留了宏文本，也无法证明渲染后的对象使用一致。

审计范围需要覆盖图片时，检查已提供 asset 中可见的变量、单位、legend 和报告值。相关嵌入内容无法检查时使用 partial coverage。记号统一需要改图，但没有可编辑源文件时，应保持 asset 不变并明确报告统一未完成。

有文件时使用 root-relative `file:line`。输入为粘贴文本时，使用 section/equation/table label 和短原文片段定位。`TERM-*`、`SYM-*`、`NUM-*` 分别按照确定的 source order 编号。

## 句式与破折号规则

避免在相邻句、段首和同类章节中机械重复句首、主谓框架、从句顺序、语态、过渡、结果汇报模板或段落开头。比较或枚举需要时可以保留平行结构。句式变化必须服务于逻辑，不能替换 canonical technical term，也不能移动受保护的公式或数值 token。

作者撰写的论文文本中不得使用破折号，包括标题、摘要、正文、caption、图表注释、脚注、致谢和附录。根据逻辑改为同位语、同位语从句、定语从句、冒号、分号、括号、连词或独立句。

不要将正文破折号规则用于受保护形式。固定复合词、TeX key、URL、DOI、文件名、citation key 中的连字符，以及数学减号和带符号数值都必须保留。例如，原稿中的 `risk-aware`、`$a-b$`、`$-1$`、`-3.2 dB` 和 `mean \pm std` 不能改动。

## 各模式流程

### 局部润色

1. 判断局部修辞功能。
2. 保留 TeX、公式、key、数字、单位、正负号和技术事实。
3. 在不移动受保护 token 的前提下润色为客观正式英文。
4. 检查局部可见的术语、记号和数值一致性。
5. Finding 使用 `Coverage: PARTIAL`；局部未发现问题时仍可使用 `Result: PASS`。

### 全文润色

1. 解析项目并执行 completeness gate。
2. 建立术语、记号、数值和结构清单。
3. 分章节润色并保持受保护 token 顺序。
4. 执行三项原稿内部一致性审计。
5. 在实际覆盖范围内执行全文句式、claim boundary 和破折号检查。
6. 做严格 source comparison；多文件论文使用 project mode。
7. 只返回一个 authoritative TeX artifact 和 review report；只有用户明确要求时才增加 Markdown。

### 检验

1. 记录 original 与 candidate 是否都存在。
2. 两者都存在时，比较 TeX/公式、结构 key、数字/单位/正负号、技术含义和 claims。
3. 缺少 original 时，所有比较型字段标为 `NOT ASSESSED`，只做 candidate 自身检查。
4. 将 candidate 新引入的偏差与 source-internal `TERM-*`、`SYM-*`、`NUM-*` 分开。
5. 只报告，不修改 candidate。

### 仅一致性审计

1. 执行 completeness gate 并说明审计范围。
2. 只建立请求所需的 ledger。
3. 分别输出术语、记号和数值的 Coverage 与 Result。
4. 提供 finding 和 author question，不修改原稿。

### 已确认记号统一

1. 必须先有精确 approved mapping，否则保持 audit mode。
2. 只执行 mapping 内替换并保留 authorization ledger。
3. 报告无法解析的宏、自定义环境、生成文件和图内 asset。
4. 验证全部差异，将确认过的替换列为 `AUTHORIZED CHANGE`。
5. 返回唯一 authoritative TeX artifact，不生成独立改写版。

## 保全检查器

单文件严格比较：

```bash
python3 paper-polisher/scripts/check_preservation.py original.tex candidate.tex
```

仅新增普通正文：

```bash
python3 paper-polisher/scripts/check_preservation.py original.tex candidate.tex --allow-additions
```

`--allow-additions` 不允许结构 key、图片 asset、数学区域、数值 token、单位或正负号的新增、删除、修改或调序，也不是记号统一模式。

多文件论文传入双方 authoritative root TeX 文件：

```bash
python3 paper-polisher/scripts/check_preservation.py original/main.tex candidate/main.tex --project
```

Project mode 从双方 root 递归解析静态可达的 `\input`、`\include`、`\subfile`、`\subfileinclude`、`\import`、`\subimport`、`\inputfrom`、`\subinputfrom`、`\includefrom` 和 `\subincludefrom`，并保留当前及此前的 import 目录上下文。缺失、动态或循环 include 会使检查失败，也必须记为语义 coverage gap。

自动数值扫描只覆盖可识别的十进制、英文文字数、带上下文的罗马数字和 Unicode 数值表示，以及处于受支持的数值/公式/literal/macro 锚点、TeX 连接、括号或明确提示语境中的正负号、显著性标记、货币、常见单位和单位形式复合 token。这只是语法覆盖，不是全局语义单位词法器。所有无法识别的形式或语境，包括歧义的独立单位 glyph，都必须人工逐项对照原稿与输出稿；脚本通过不能替代这项人工保全复核，也不能替代前文要求的“数量到单位”语义审计。

只有 mapping 在整个 checked scope 内全局成立时，才可重复使用 normalization-only 参数；包含反斜杠的 TeX token 必须用 shell 单引号保护：

```bash
python3 paper-polisher/scripts/check_preservation.py original.tex normalized.tex \
  --approved-symbol-map 'M=N' \
  --approved-symbol-map '\mathbf{P}=\mathbf{Q}'
```

一旦使用 `--approved-symbol-map`，非数学正文和 mapping 之外的所有 math token 都必须不变；mapping 永远不能授权数字、货币、百分比、单位或正负号修改。Parser 会拒绝明确的数字、货币、百分比和正负号 mapping；歧义裸 glyph 仍须结合 entity-aware ledger 与人工单位复核。不要与 `--allow-additions` 组合。CLI mapping 在 checked scope 内全局生效；若某个 glyph 存在有意排除项或无关复用，应改用 location-aware authorization ledger 并建立 author-approved baseline。

不要把 report 或 commentary 与 TeX 输入拼在一起交给脚本。

脚本通过只能证明其支持范围内的语法级 source-to-output 保全。语义一致性和 coverage gate 必须独立执行。

## 输出示例

状态含义只使用 `SKILL.md` 中的统一定义，不在这里另建一套含义，也不要把模板中的斜线分隔选项原样输出。

记号 finding 示例：

```text
Symbol/notation consistency:
Coverage: PARTIAL
Result: ISSUE REPORTED

SYM-001 | ISSUE REPORTED
数学对象：相机坐标系到世界坐标系的齐次变换
位置：sections/method.tex:84；sections/evaluation.tex:31
依据：两处方向、维度、坐标系和下游用途相同，但分别使用 \mathbf{M} 与 \mathbf{N}
Canonical choice：尚未确定，需要作者选择
处理：仅报告
```

数值 finding 示例：

```text
Source-internal numerical consistency:
Coverage: FULL MANUSCRIPT
Result: ISSUE REPORTED

NUM-001 | ISSUE REPORTED
数量：full-data setting 下的 test-set accuracy
位置：tables/main.tex:22 为 91.2\%；sections/results.tex:47 为 92.1\%
依据：dataset、split、method variant、metric 和 aggregation 均相同
所需作者操作：在外部修正并确认原稿，然后提供新的 baseline
处理：仅报告
```

缺少 original 的检验示例：

```text
Verification inputs:
- Candidate: available
- Original: unavailable

Source-to-output TeX/math preservation: NOT ASSESSED
Technical and claim fidelity: NOT ASSESSED
Numerical-token/unit/sign preservation: NOT ASSESSED
Candidate modification: NONE
```
