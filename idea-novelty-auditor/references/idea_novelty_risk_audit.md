# Idea Novelty Risk Audit 模板

> 目的：先检查科研 idea 的新颖性风险，再谈包装。  
> 核心原则：**先拆穿，再修补，再定义边界，最后包装。** 🧭

---

## 0. 总原则

在评估一个科研 idea 时，不要一开始就问：

> 这个 idea 怎么包装成论文？

应该先问：

> 这个 idea 最可能已经被哪些经典方法或相邻工作做过？  
> 它的新意到底落在哪个不可替代的环节？

基本流程：

```text
抽象问题
↓
检查经典范式
↓
检查直接相关工作
↓
检查相邻领域工作
↓
列出危险 baseline
↓
明确不能声称什么
↓
明确可以谨慎声称什么
↓
设计能支撑贡献的实验
↓
最后再包装论文主线
```

---

## 1. 用一句话描述原始 idea

先用应用语言描述你的想法。

**模板：**

> 我想解决的问题是：在 `[具体场景]` 中，现有方法 `[已有方法]` 会因为 `[失败原因]` 出现 `[具体错误]`。我希望通过 `[你的方法]` 来提升 `[目标指标]`。

**例子：**

> 我想解决的问题是：在高同质、多遮挡的 BIM 室内环境中，Hough-based LiDAR-to-BIM registration 会产生多个错误候选位姿，甚至出现 180° 朝向翻转。我希望通过 BIM 房间—门—走廊拓扑、LIO 相对运动和多候选延迟决策来恢复正确定位。

---

## 2. 去掉应用名词，抽象成通用算法范式

这一步很关键。不要只盯着 BIM、LiDAR、Hough 这些具体名词，而要先问：

> 如果把应用背景去掉，这个问题本质上是什么？

**模板：**

```text
原始 idea 中的关键词：
- [应用名词 1]
- [应用名词 2]
- [算法模块 1]
- [问题现象 1]

抽象后可能对应：
- 多假设定位？
- 序列推理？
- 粒子滤波？
- HMM / Viterbi？
- 图匹配？
- SLAM 后端优化？
- 多模态分布估计？
- 对称性 / 可观测性分析？
```

**例子：**

```text
BIM + Hough + 多候选 + 机器人运动后消歧

抽象后是：
multi-hypothesis localization
sequential Bayesian filtering
HMM / Viterbi sequence inference
particle filter / AMCL
topological localization
symmetry-induced ambiguity resolution
```

如果抽象后发现它很像 AMCL、MCL、Viterbi、particle filter、factor graph，就必须主动比较。

---

## 3. 四层相关工作检查

不要只查直接相关论文。至少查四层。

### 3.1 第一层：直接相关工作

这是和你的任务、传感器、地图形式最直接相关的工作。

**模板：**

```text
我的直接相关工作包括：
- 方法 A：
- 方法 B：
- 方法 C：

它们已经做了什么：
- ...

它们没解决什么：
- ...
```

**例子：**

```text
LiDAR-to-BIM registration
Pose Hough Transform
LiDAR2BIM
Scan-to-BIM matching
BIM-aided localization
```

需要回答：

```text
它们是否已经产生多个候选？
它们是否已经有 candidate verification？
它们是否已经考虑重复结构？
它们是否已经承认 ambiguous scenario？
它们是否已经处理 top-1 错误？
```

---

### 3.2 第二层：相邻相关工作

这是和你的方法不完全一样，但问题结构接近的工作。

**模板：**

```text
相邻相关工作包括：
- [领域 1]
- [领域 2]
- [领域 3]

这些工作可能会威胁我的 novelty，因为：
- ...
```

**例子：**

```text
BIM topology localization
S-Graphs / A-Graphs
Architectural graph localization
Scene graph matching
Floor-plan-based localization
Semantic SLAM
Topological map localization
```

需要回答：

```text
它们是否已经用房间、门、墙、走廊拓扑做定位？
它们是否已经做无初值 global localization？
它们是否已经做 graph-to-graph matching？
它们是否已经处理建筑对称性？
```

---

### 3.3 第三层：经典算法范式

这是最容易被忽略、但最容易被审稿人抓住的部分。

**模板：**

```text
这个 idea 抽象后类似哪些经典算法？
- 算法范式 A：
- 算法范式 B：
- 算法范式 C：

我的方法和它们的区别是：
- ...
```

**例子：**

```text
AMCL / MCL
Particle filter localization
Bayesian filtering
HMM / Viterbi
Multi-hypothesis tracking
Factor graph optimization
Loop closure / relocalization
```

需要回答：

```text
我是不是只是 AMCL 的变体？
我是不是只是 Viterbi 在新场景下的应用？
我是不是只是 particle filter 换了一个观测模型？
我是不是只是 factor graph 加了一个先验约束？
```

---

### 3.4 第四层：危险 baseline

这层最重要。不要只问“有没有相关工作”，要问：

> 哪些 baseline 一旦表现不错，就会让我的贡献显得不成立？

**模板：**

```text
必须比较的危险 baseline：
1. Baseline A：
2. Baseline B：
3. Baseline C：

如果我的方法不能明显超过这些 baseline，那么：
- 这个 idea 的贡献会变弱；
- 需要收缩 claim；
- 或者需要重新设计问题定义。
```

**例子：**

```text
BIM-to-occupancy-grid + AMCL
LiDAR2BIM Hough top-1
LiDAR2BIM top-K + occupancy-aware score
Hough top-K + LIO-only consistency
Hough top-K + topology-only consistency
S-Graph / A-Graph-like localization
Naive Viterbi over room adjacency graph
```

---

## 4. 相似性矩阵

对每个相关方法做结构化比较。

| 方法 | 和我的 idea 相似在哪里 | 和我的 idea 不同在哪里 | novelty 威胁程度 | 我必须怎么区分 |
|---|---|---|---|---|
| 方法 A |  |  | 高 / 中 / 低 |  |
| 方法 B |  |  | 高 / 中 / 低 |  |
| 方法 C |  |  | 高 / 中 / 低 |  |

**例子：**

| 方法 | 相似性 | 不同点 | novelty 威胁 | 区分方式 |
|---|---|---|---|---|
| AMCL / MCL | 多假设、运动传播、观测更新、运动中消歧 | 通常基于 occupancy grid 和粒子采样 | 高 | 强调 Hough-BIM 结构化候选、BIM 拓扑实体、180° yaw-flip 显式建模 |
| LiDAR2BIM / Pose Hough | Hough 候选、LiDAR-to-BIM registration | one-shot candidate verification | 高 | 强调序列级 delayed decision 和 topology-constrained candidate lattice |
| S-Graphs / A-Graphs | 建筑拓扑、无初值定位、图匹配 | 更偏完整 scene graph / architectural graph matching | 高 | 强调不是重建完整 scene graph，而是对 Hough candidates 做轻量序列消歧 |
| Viterbi / HMM | 候选序列推理 | 通用算法范式 | 中 | 不把 Viterbi 当贡献，只作为求解器 |
| LIO-BIM | LIO + BIM scan matching | 更偏连续 tracking / mapping | 中 | 强调无初值、多峰候选、wrong-top1 recovery |

---

## 5. 审稿人攻击模式

在包装 idea 前，先主动攻击它。

**模板：**

```text
最可能的审稿人质疑：

Q1: 这是不是已有方法 A 的简单变体？
回答：
- 是相似的地方：
- 不是简单变体的原因：
- 需要实验证明：

Q2: 为什么不直接用 baseline B？
回答：
- baseline B 的局限：
- 我的方法额外利用了什么信息：
- 需要实验证明：

Q3: 你的方法在哪些情况下无效？
回答：
- 失败条件 1：
- 失败条件 2：
- 失败条件 3：

Q4: 你的核心模块是不是只是工程组合？
回答：
- 哪些模块不是新贡献：
- 真正的新贡献在哪里：
```

**例子：**

```text
Q1: 这是不是 AMCL？
A: 抽象上类似，都是多假设序列定位。但 AMCL 主要在 occupancy grid 上维护连续粒子分布，而本方法关注 Hough-based LiDAR-to-BIM 产生的结构化候选，并显式关联 BIM 房间、门、走廊拓扑节点和 180° yaw-flip 模式。

Q2: 为什么不直接从 BIM 生成 occupancy grid 后跑 AMCL？
A: 需要实验说明 AMCL 在高同质、重复房间、长走廊或 180° 对称场景下容易错误收敛或长期多峰，而 BIM topometric graph 可以更早利用门连接、房间序列、穿墙约束和 directed door crossing 排除错误候选。
```

---

## 6. 三档贡献判断

每个 idea 都要分成三档：最弱版本、可防守版本、增强版本。

### 6.1 最弱版本

**模板：**

> 如果只做 `[最简单实现]`，这个 idea 可能会被认为只是 `[已有方法]` 的变体。

**例子：**

> 如果只做 top-K Hough candidates + LIO + 后续选择最优候选，这很可能被认为是 AMCL / MCL 思想在 BIM-Hough 场景中的工程改写。

---

### 6.2 可防守版本

**模板：**

> 如果加入 `[关键区别模块]`，并用 `[针对性实验]` 证明它解决了 `[具体 failure case]`，则可以作为一篇短文或应用型论文。

**例子：**

> 如果显式建模 Hough-BIM 的 wrong-room、cross-floor 和 180° yaw-flip 候选，并利用 BIM topometric graph 做候选序列消歧，同时设计 wrong-top1 recovery benchmark，则可以作为一篇合理短文。

---

### 6.3 增强版本

**模板：**

> 如果进一步加入 `[分析型贡献]`、`[强实验]` 和 `[可解释失败边界]`，则有机会撑成完整 journal paper。

**例子：**

> 如果进一步加入 symmetry-aware delayed decision、false commitment detection、topological ambiguity index、多建筑真实实验和 AMCL/S-Graph/LiDAR2BIM 的系统对比，则有机会成为完整 journal paper。

---

## 7. 明确“不能声称什么”

这一节非常重要。很多论文风险来自 claim 过大。

**模板：**

```text
这个 idea 不能声称：
1. 我们首次提出 ...
2. 我们首次使用 ...
3. 我们解决所有 ...
4. 我们不需要 ...
5. 我们完全优于 ...
```

**例子：**

```text
不能声称：
1. 首次使用 BIM 拓扑进行定位。
2. 首次提出多假设定位。
3. 首次利用运动消除定位歧义。
4. 任意错误初值都可以恢复。
5. 180° 歧义在所有场景下都能解决。
6. 不需要任何相对运动估计。
```

---

## 8. 明确“可以谨慎声称什么”

**模板：**

```text
这个 idea 可以谨慎声称：
1. 我们针对 [具体问题] 提出 ...
2. 与 [已有方法] 不同，我们 ...
3. 在 [具体条件] 下，我们能够 ...
4. 我们显式分析了 [失败条件 / 歧义条件]。
```

**例子：**

```text
可以谨慎声称：
1. 针对 Hough-based LiDAR-to-BIM registration 在重复建筑中的 wrong-top1 问题，提出多候选序列消歧框架。
2. 将 Hough 输出的多个 pose candidates 建模为结构化候选分布，而不是立即选取 top-1。
3. 利用 BIM room-door-corridor topometric graph 和 LIO 相对运动约束进行候选路径推理。
4. 显式处理 wrong-room、cross-floor 和 180° yaw-flip 等 Hough-BIM 特有歧义模式。
5. 在正确位姿存在于 top-K 且后续轨迹包含足够拓扑事件时，可以从错误 top-1 中恢复。
6. 当环境拓扑和几何完全对称时，系统可以检测 remaining ambiguity，而不是过早提交错误位姿。
```

---

## 9. 判断 idea 是否值得继续

可以用下面的 checklist。

### 9.1 技术可行性

```text
[ ] 输入数据是否能稳定获得？
[ ] 关键模块是否已有实现基础？
[ ] 需要的 ground truth 是否能获取？
[ ] 主要失败现象是否真实存在？
[ ] 正确答案是否经常存在于候选集合中？
[ ] 算法是否能在合理时间内运行？
```

---

### 9.2 新颖性可防守性

```text
[ ] 是否已经检查经典范式？
[ ] 是否已经检查直接竞品？
[ ] 是否已经检查相邻领域？
[ ] 是否已经列出危险 baseline？
[ ] 是否能说清楚和最危险 baseline 的区别？
[ ] 是否知道哪些 claim 不能说？
[ ] 是否有一个具体、狭窄、可验证的新贡献？
```

---

### 9.3 实验可证明性

```text
[ ] 是否有明确的 failure case？
[ ] 是否能构造 targeted benchmark？
[ ] 是否能设计 ablation study？
[ ] 是否能和危险 baseline 公平比较？
[ ] 是否有一个核心指标能直接证明贡献？
[ ] 是否能解释方法失败的条件？
```

---

## 10. 实验设计原则

不要只做“最终精度提高”。要做能支撑主贡献的实验。

**模板：**

```text
主贡献：
- ...

对应实验：
- ...

关键指标：
- ...

必须对比：
- ...
```

**例子：**

```text
主贡献 1：
Hough 多候选序列消歧。

实验：
在 Hough top-1 错误但 top-K 包含正确位姿的场景下测试恢复能力。

指标：
wrong-top1 recovery rate
candidate re-ranking accuracy
decision length
```

```text
主贡献 2：
180° yaw-flip 显式处理。

实验：
构造 yaw-flip ambiguity cases，包括长走廊、矩形房间、对称办公室。

指标：
180° yaw recovery rate
false commitment rate
remaining ambiguity detection accuracy
```

```text
主贡献 3：
BIM 拓扑约束有效。

实验：
比较 topology-only、odometry-only、topology + odometry、topology + odometry + symmetry-aware decision。

指标：
ATE / RPE
global localization success rate
false positive localization rate
runtime
```

---

## 11. Baseline-first 原则

在 idea 成熟前，先列 baseline，而不是先写贡献。

**模板：**

```text
这个 idea 必须打败的 baseline：

1. Baseline A：
   - 为什么危险：
   - 如何比较：

2. Baseline B：
   - 为什么危险：
   - 如何比较：

3. Baseline C：
   - 为什么危险：
   - 如何比较：
```

**例子：**

```text
1. BIM-to-occupancy-grid + AMCL
   - 危险原因：AMCL 已经具备多假设和运动消歧能力。
   - 比较方式：测试重复走廊、180° 歧义、wrong-room recovery、false commitment。

2. LiDAR2BIM top-K + occupancy-aware score
   - 危险原因：Hough 本身已经产生候选，并有 candidate verification。
   - 比较方式：测试 top-1 错误时是否能通过后续拓扑事件恢复。

3. Hough top-K + LIO-only
   - 危险原因：如果只靠 LIO 连续性已经够好，BIM 拓扑贡献就弱。
   - 比较方式：做 ablation，证明 topology constraints 额外提升。

4. Hough top-K + topology-only
   - 危险原因：如果只靠 topology 就够，LIO 和 topometric modeling 贡献变弱。
   - 比较方式：证明 topology + odometry + directed door constraints 更稳。

5. S-Graph / A-Graph-like localization
   - 危险原因：它们已经使用建筑拓扑进行全局定位。
   - 比较方式：强调你的方法是轻量 Hough-candidate lattice，而不是完整 graph-to-graph matching。
```

---

## 12. 最终论文主线构造

经过上述检查后，再写论文主线。

**模板：**

```text
现有方法 A 已经可以 ...
但在 [具体场景] 中，由于 [具体原因]，它会出现 [具体 failure case]。
现有方法 B 虽然可以 ...
但它没有显式处理 [你的特殊问题]。
因此，本文关注 [狭窄问题定义]。
我们提出 [方法名称]，其核心是 [核心机制]。
在 [条件] 下，该方法可以 [谨慎 claim]。
```

**例子：**

> Existing Hough-based LiDAR-to-BIM registration methods can generate multiple pose candidates and select a final transformation using local geometric or occupancy consistency. However, in repetitive indoor environments, the top-ranked candidate may correspond to a wrong room or a 180° yaw-flipped pose. Although AMCL-style methods maintain multiple pose hypotheses over time, they operate mainly over occupancy-grid particles and do not explicitly reason over the structured Hough-BIM candidate modes. This paper focuses on ambiguity-aware LiDAR-to-BIM localization without a reliable initial pose. We propose a BIM topometric graph constrained candidate-lattice inference method that delays commitment, tracks wrong-location and yaw-flip hypotheses, and resolves them using room-door-corridor transitions, LIO motion consistency, and directed door-crossing constraints.

---

## 13. 可直接使用的提问模板

以后可以直接用这段：

> 请你对这个 idea 做 **novelty risk audit**，不要先包装它。  
> 1. 先把 idea 抽象成通用算法范式；  
> 2. 列出直接相关工作、相邻相关工作、经典算法范式、危险 baseline；  
> 3. 说明哪些已有方法最可能打掉它的新颖性；  
> 4. 给出相似性矩阵；  
> 5. 站在审稿人角度攻击这个 idea；  
> 6. 给出最弱版本、可防守版本、增强版本；  
> 7. 明确哪些贡献不能声称，哪些贡献可以谨慎声称；  
> 8. 设计必须完成的实验和 ablation；  
> 9. 最后再建议如何包装成论文。

---

## 14. 最简版 checklist

每次有新 idea，至少问这 10 个问题：

```text
[ ] 1. 去掉应用名词后，它像哪个经典算法？
[ ] 2. 有没有 AMCL / MCL / HMM / Viterbi / factor graph 这类经典方法已经覆盖其核心思想？
[ ] 3. 直接相关论文已经做到哪一步？
[ ] 4. 相邻领域是否已经解决类似问题？
[ ] 5. 最危险 baseline 是什么？
[ ] 6. 如果 baseline 表现很好，我的方法还剩什么贡献？
[ ] 7. 哪些 claim 绝对不能说？
[ ] 8. 哪些 claim 可以在特定条件下谨慎说？
[ ] 9. 有没有一个 targeted benchmark 能证明我的贡献？
[ ] 10. 方法失败条件是什么，是否能诚实解释？
```

---

## 15. 对 idea 的最终判定格式

每次检查后，可以用这个格式总结：

```text
Idea 名称：
- ...

抽象范式：
- ...

最相似经典方法：
- ...

最危险直接竞品：
- ...

novelty 风险：
- 高 / 中 / 低

最弱版本：
- ...

可防守版本：
- ...

增强版本：
- ...

不能声称：
- ...

可以谨慎声称：
- ...

必须打败的 baseline：
- ...

必须完成的实验：
- ...

推荐论文定位：
- short paper / conference paper / journal paper / 不建议继续

下一步最小验证：
- ...
```

---

## 16. 核心提醒

科研 idea 的检查顺序应该是：

```text
先拆穿
再修补
再定义边界
最后包装
```

不要反过来。

如果先包装，很容易把一个已有范式的应用改写误判成新方法。  
如果先做 novelty risk audit，即使 idea 最后只是增量，也能更早知道它该被定位成短文、应用论文，还是需要继续加厚。
