# 论文论证重构指南

## 核心目标

将论文或章节从“模块堆砌”重构为围绕核心问题展开的 problem-driven storyline。

重构后的论文应体现：

- 明确的核心问题；
- 可防守的技术 gap；
- 连贯的论文主线；
- 与 gap 对应的 contributions；
- 从问题需求引出的模块；
- 服务于方法逻辑的公式和理论；
- 能支撑具体 claim 的实验；
- 回到核心问题的结果解释。

基本判断标准：

```text
每个段落、模块、公式和实验，都应回答或支撑论文要解决的核心问题。
```

## 主线模型

默认使用：

```text
真实需求 -> 技术瓶颈 -> 现有方法限制 -> 所需能力 -> 提出框架 -> 机制解释 -> 实验验证 -> 实际意义
```

方法型论文可使用更局部的链条：

```text
核心问题 -> 具体挑战 -> 所需能力 -> 提出模块 -> 机制 -> 证据 -> 含义
```

避免写成：

```text
提出模块 A。
提出模块 B。
提出模块 C。
进行了实验。
```

应改成：

```text
为解决 [具体挑战]，本文引入 [模块 A] 以提供 [所需能力]。
在此基础上，[模块 B] 进一步缓解 [剩余限制]。
最后，[模块 C] 实现 [系统级目标]，从而支撑 [核心问题]。
```

## 诊断流程

1. 识别应用场景和核心研究问题。
2. 识别当前技术瓶颈或 failure mode。
3. 识别现有方法在该瓶颈下不能做到什么。
4. 识别 proposed method 必须提供的能力。
5. 将每个模块、公式、实验和结果映射到具体 claim。
6. 找出 unsupported claims、缺失过渡、重复 claim 和模块堆砌段落。
7. 先产出修订后的 storyline，再进行句子层面改写。

## 段落功能标签

重写前先判断每段的功能：

- 应用背景；
- 核心问题；
- 技术 gap；
- 方法动机；
- 模块机制；
- 公式定义；
- 理论分析；
- 实验设置；
- 结果观察；
- 结果解释；
- 限制；
- 实际意义；
- 过渡。

没有清晰功能的段落应被合并、移动或重写。

## Contribution 写法

每条 contribution 都应对应前文明确提出的 gap 或 challenge。

弱写法：

```text
The contributions are:
1. We propose module A.
2. We propose module B.
3. We conduct experiments.
```

更强的写法：

```text
The contributions are:
1. A [capability] formulation that addresses [specific gap].
2. A [mechanism/module] that mitigates [specific failure mode].
3. A targeted evaluation that verifies [claim] under [condition].
```

如果 related work 证据不足，不要轻易写 `first`、`novel`、`unprecedented`。可以使用更稳妥的边界表达：

- `we focus on`;
- `we develop`;
- `we investigate`;
- `we introduce a framework for`;
- `under the evaluated conditions`.

## 分节指导

### 摘要

推荐顺序：

1. 背景或问题场景。
2. 具体 gap 或 failure mode。
3. 提出的方法和核心机制。
4. 实验或分析证据。
5. 有边界的 implication。

### 引言

推荐顺序：

1. 真实需求。
2. 技术瓶颈。
3. 现有方法限制。
4. 所需能力。
5. 本文方法。
6. 贡献与组织结构。

### 相关工作

详细的 related work 写作、参考文献选择、直接竞争方法覆盖和 citation-role assignment 应使用 `problem-driven-literature-review`。在全文论证重构中，只检查 Related Work 是否支撑论文的主 gap 和贡献逻辑。

高层面上，它应按方法家族、假设或限制组织，而不是按时间顺序列文献：

- 方法家族 A 及其限制；
- 方法家族 B 及其限制；
- 与本文最接近的方法；
- 仍未解决的 gap。

不要在论证重构阶段虚构文献 claim 或 citation。

### 方法

每个模块都应从问题需求引出：

```text
To address [challenge], the method requires [capability]. Therefore, [module] is introduced to [mechanism/effect].
```

随后解释输入输出、机制、与其他模块的关系、假设或限制，以及在整体框架中的作用。

### 实验

每个实验应验证一个 claim、模块、指标或部署需求。

需要明确：

- 要验证的 claim；
- 数据集或场景；
- baseline；
- 指标；
- 诊断价值；
- 局限性。

不要只做最终平均性能。若贡献依赖某个机制，应设计 ablation 或 targeted scenario。

### 结果与讨论

好的结果段落通常包含：

1. 观察。
2. 对比。
3. 机制解释。
4. 与论文 claim 的关系。
5. 必要时说明条件或限制。

不要只复述表格数值。

## Claim-Evidence 对齐表

诊断时可使用：

| Claim | 所需证据 | 现有实验 | 缺失证据 | 风险 |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

常见问题：

- 声称某模块重要，但没有 ablation；
- 声称 robust，但只在简单场景测试；
- 声称 real-time 或 deployment，但缺少运行时间和资源分析；
- 声称 safety 或 reliability，但缺少 failure-case analysis；
- 声称优于现有方法，但没有危险 baseline。
