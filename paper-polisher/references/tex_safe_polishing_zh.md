# TeX-Safe 学术润色指南

## 核心目标

将中文或英文 TeX 论文文本润色为正式、客观、克制的工程期刊英文，同时不改变技术事实。

本文件只服务于忠实润色，不负责 novelty audit，也不负责大幅重构论文论证主线。

润色结果应满足：

- 英文表达清晰、正式、简洁；
- 术语稳定一致；
- 语气客观克制；
- TeX 结构完整保留；
- 数值、实验事实和技术含义不被改动；
- 不引入原文没有支撑的新 claim。

## 保全规则

必须保留：

- 行内和行间公式，包括 `$...$`、`\(...\)`、`\[...\]`、`equation`、`align` 等环境；
- figure、table、algorithm、theorem、proof、lemma、definition、remark 等环境；
- `\label{...}`、`\ref{...}`、`\eqref{...}`、`\autoref{...}`、`\cref{...}`、`\includegraphics{...}`、`\cite{...}`、`\citep{...}`、`\citet{...}`、`\bibitem{...}` 和 BibTeX key；
- 变量名、函数名、模块名、模型名、数据集名、指标名、baseline 名和缩写；
- 数值、单位、百分比、样本量、参数设置、表格值、图中报告值和显著性标记。

保留 TeX 结构不仅是保留命令形式，也包括原始 key。下面这些内容：

```latex
\label{sec:method}
\ref{sec:method}
\eqref{eq:risk}
\cite{smith2023,chen2024}
```

不能被改成：

```latex
\label{sec:methodology}
\ref{method}
\eqref{eq:risk_metric}
\cite{Smith2023}
```

如果发现可疑数值、单位不一致、重复引用、参考文献格式异常或作者姓名顺序问题，不要静默修正，应报告给用户确认。

新增可引用对象时，不要生成泛化占位 label。应先观察原稿已有命名习惯，并让 label 与对象语义绑定：

```latex
\label{tab:diff_methods}
\label{fig:framework}
\label{alg:training}
```

如果原稿没有明确命名习惯，默认使用 `type:semantic_name`：

| 对象类型 | 前缀 | 示例 |
|---|---|---|
| 章节 | `sec:` | `\label{sec:method}` |
| 小节 | `subsec:` | `\label{subsec:ablation_setup}` |
| 图片 | `fig:` | `\label{fig:framework}` |
| 表格 | `tab:` | `\label{tab:diff_methods}` |
| 公式 | `eq:` | `\label{eq:loss_function}` |
| 算法 | `alg:` | `\label{alg:training}` |
| 定理 | `thm:` | `\label{thm:convergence}` |
| 附录 | `app:` | `\label{app:implementation}` |

如果原稿已经使用下划线风格，应延续该风格：

```latex
\label{tab_diff_methods}
\label{fig_framework}
```

禁止输出 `\label{tab}`、`\ref{tab}`、`\label{fig}`、`\ref{fig}`、`\label{table}`、`\label{figure}`、`\label{img}`、`\label{image}`、`\label{tmp}`、`\label{label}` 这类裸占位 label 或 reference。一旦用户指定或确认了新增 label，后续应把它当作 protected key 处理；再次生成完整版时必须原样保留，并保持对应的 `\ref`、`\autoref`、`\cref` 目标一致。

引用已有对象时，应先识别正文里已经存在的 exact label keys。例如，若表格 label 是：

```latex
\label{tab:ablation}
\label{tab:errors}
\label{tab:torwic_errors}
```

那么 controlled indoor experiments 段落只能引用相关的 controlled-indoor 表格：

```latex
Tables~\ref{tab:ablation} and~\ref{tab:errors}
```

不要写成 `Tables~\ref{tab} and~\ref{tab}`，也不要在这句话里引用 `\ref{tab:torwic_errors}`，除非该句讨论的是 TorWIC evaluation。

不要混淆内部 label key 和最终显示编号。例如 `\label{fig:1}` 可以作为已有命名习惯被保留，但正文中仍应使用引用命令，并匹配目标期刊或原稿已有的 reference-name style：

```latex
Fig.~\ref{fig:1}
Figure~\ref{fig:1}
```

`Fig.` 还是 `Figure` 应根据目标期刊模板或原稿已有风格决定，并在全文保持一致。`Eq.`/`Equation`、`Sec.`/`Section` 也同理。不要硬编码为：

```latex
Figure 1
Fig. 1
```

caption 中也不要手写对象名和编号，因为 LaTeX 会自动生成 Figure/Table 编号。应写：

```latex
\caption{Overall framework of the proposed method.}
```

不要写：

```latex
\caption{Figure 1. Overall framework of the proposed method.}
\caption{Fig. 1. Overall framework of the proposed method.}
```

表格、算法、公式、章节和附录的引用或 caption 也遵循同一规则。

对于新插入的图片，同时保护语义化 figure label 和图片资源路径：

```latex
\begin{figure}
  \centering
  \includegraphics[width=0.85\linewidth]{figures/framework.pdf}
  \caption{Overall framework of the proposed method.}
  \label{fig:framework}
\end{figure}
```

后续生成完整版时，除非用户明确要求重命名、移动、缩放或替换图片，否则应保留 `figures/framework.pdf`、已确认的尺寸/裁剪参数和 `\label{fig:framework}`。不要把路径简化成 `framework.pdf`，不要虚构新文件名，也不要退回 `\label{fig}`。

## 忠实性规则

可以做：

- 调整句子顺序以改善可读性；
- 拆分过长句；
- 合并重复表达；
- 增加轻量逻辑连接；
- 将口语化表达改为正式学术表达；
- 在不增加新技术内容的前提下，使局部逻辑更明确。

不能做：

- 修改定义、假设、算法步骤、证明逻辑、公式或实验设置；
- 增加新实验、新保证、新应用、新部署价值或新限制；
- 把相关性写成因果性；
- 把局部结果扩大成全面优越性；
- 把启发式方法写成理论保证；
- 改动 baseline、数据集、指标、数值或报告结果。

## 术语控制

对于重要概念，应选择一个 canonical term 或 term family，并在等价语境中保持一致。

长文本或术语密集文本建议先建立小型术语表：

| 原文术语 | 技术概念 | 推荐英文术语族 | 允许的上下文形式 | 避免或保留给 |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

重点检查两类问题：

- 同一个概念为了追求“变化”被翻译成多个不同英文术语；
- 不同技术概念被压成同一个模糊英文词。

## 本地润色流程

1. 判断输入是句子、段落、章节、图表说明、表格注释还是混合 TeX。
2. 判断局部功能：背景、问题、方法、公式解释、结果、讨论或结论。
3. 保留所有 TeX 结构、key、变量、数值和技术事实。
4. 润色为客观正式的学术英文。
5. 检查术语一致性。
6. 检查 claim 是否强于原文。

## 全文润色流程

1. 识别核心问题、应用场景、技术瓶颈、主要方法和主要 claim。
2. 建立术语表。
3. 对新增或用户确认过的 label 建立结构清单，全文输出时沿用这些 exact labels。
4. 分章节润色，保持 TeX 结构和技术事实。
5. 统一跨章节术语和 claim 边界。
6. 如果有原始 TeX 和润色后 TeX 文件，运行保全检查脚本。纯润色使用默认严格模式；只有在用户明确新增正文内容、label、reference、图片资源或数值 token 时，才使用 `--allow-additions`。
7. 输出对应范围的结果和 review report。

## Review Checklist

返回前检查：

- TeX 命令、环境、protected keys、变量和公式未被改动。
- 新增 label 和 reference 具有语义、符合原稿命名习惯，且不是裸占位 key。
- caption 和正文引用不硬编码 `Figure 1` 这类显示编号，而是通过 label 与 reference 命令交给 LaTeX 自动编号，并让 `Fig.`/`Figure`、`Eq.`/`Equation` 等引用名称匹配目标期刊或原稿风格。
- 数值、单位、数据集、baseline、指标、参数设置和报告结果未被改动。
- 引用和参考文献问题是报告，而不是静默修改。
- 没有引入 unsupported claims、实验、理论保证或部署价值。
- 术语保持一致。
- 语气正式、客观、克制。
- 输出格式与任务范围匹配。
