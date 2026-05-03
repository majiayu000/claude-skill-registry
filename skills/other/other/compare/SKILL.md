---
name: compare-masters
description: Use when user asks to compare masters, compare schools, compare perspectives, 对比, 各宗怎么看, 不同宗派, 禅净之争, 性相之辩, 空有之争, or wants multiple masters to answer the same question. Triggers include "对比"、"比较"、"各宗"、"不同宗派怎么看"、"禅宗和净土"、"天台和华严"、"唯识和中观"、"空有之争"、"性相之辩"、"各位祖师"、"多个角度"、"compare"、"comparison" — invoke whenever user's question implicitly or explicitly seeks multi-tradition perspectives on a Buddhist topic.
version: 0.3.0
license: MIT
kind: meta-skill
verified_by: xr843
verified_at: 2026-04-06
---

# 多祖师对比 (Compare Masters) — 元 Skill

> 本内容依据历史佛教文献生成，仅供学习参考。对比旨在展现多元视角，不评判优劣。

## 决策树：选择哪些祖师？

### 优先级 1 — 用户显式指定

用户指定 2-3 位祖师 → 直接使用。

### 优先级 2 — 关键词智能匹配

从用户问题提取佛学关键词，与各祖师 `meta.json` 的 `search_scope.keywords` 匹配：
- 强匹配（关键词直接出现在 keywords 中）：权重 3
- 相关匹配（属于该传承核心领域）：权重 2
- 弱匹配（部分字面重叠）：权重 1

取 top 2-3 位，优先选不同宗派以呈现多元视角。

### 优先级 3 — 主题映射兜底

| 问题主题 | 配对祖师 | 说明 |
|---------|---------|------|
| 念佛 / 往生 / 净土 | master-yinguang + master-ouyi | 净土专精 + 跨宗派 |
| 参禅 / 话头 / 开悟 | master-huineng + master-xuyun | 古今禅宗对比 |
| 唯识 / 中观 / 空有 | master-xuanzang + master-kumarajiva | 唯识 vs 中观 |
| 判教 / 圆融 / 止观 | master-zhiyi + master-fazang | 天台 vs 华严 |
| 修行次第 / 综合法门 | master-ouyi + master-yinguang | 综合 vs 专修 |
| 戒律 / 行持 / 日常 | master-xuyun + master-yinguang + master-ajahn-chah | 禅门戒律 vs 净土行持 vs 上座部律仪 |
| 般若 / 空性 | master-kumarajiva + master-tsongkhapa + master-huineng | 早期中观译师 · 应成中观精确分判 · 禅宗直指 |
| 中观 / 缘起性空 / 应成 | master-kumarajiva + master-tsongkhapa | 印度中观东渡 vs 藏地后期精确化 |
| 道次第 / 三士道 / lam rim | master-atisha + master-tsongkhapa | 印藏桥梁源头 vs 格鲁派系统化 |
| 心识 / 阿赖耶 / 心所 | master-xuanzang + master-buddhaghosa + master-huineng | 唯识 vs 上座部阿毗达摩 vs 禅宗直指 |
| 戒律 / 持戒 / 律仪 | master-xuyun + master-atisha + master-buddhaghosa | 汉传禅门律 vs 印藏菩萨律 vs 上座部律藏注释 |
| 苦行 / 闭关 / 山中修行 | master-xuyun + master-milarepa | 汉传禅门头陀 vs 藏传瑜伽士传统 |
| 正念 / 观心 / 觉知 | master-huineng + master-ajahn-chah + master-mahasi-sayadaw | 禅宗自性 vs 南传 sati 朴素 vs 缅甸标记法 |
| 禅修方法 / 业处 / 所缘 | master-buddhaghosa + master-mahasi-sayadaw + master-ajahn-chah | 论藏四十种业处 vs 标记法腹部起伏 vs 朴素观心 |
| 七清净 / 十六观智 / 道次第 | master-buddhaghosa + master-mahasi-sayadaw | 《清净道论》原典 vs 现代缅甸应用 |
| 出离心 / 暇满 / 无常 | master-yinguang + master-atisha + master-ajahn-chah | 净土 · 噶当 · 上座部三大传统出离观对比 |
| 菩提心 / 慈悲 | master-atisha + master-ouyi | 印藏自他相换 vs 跨宗派融通 |
| 上师 / 善知识 / 依止 | master-xuyun + master-atisha + master-tsongkhapa | 汉传善知识 vs 噶当依止论 vs 格鲁视师如佛 |
| 论师风格 / 经院严密 | master-xuanzang + master-tsongkhapa + master-buddhaghosa | 唯识 · 应成中观 · 上座部三大论师传统 |
| 三大传统对比（明确要求） | master-huineng + master-tsongkhapa + master-buddhaghosa | 禅 · 应成中观 · 上座部论藏，三方系统对照 |
| 三大传统禅修对比 | master-huineng + master-milarepa + master-ajahn-chah | 禅 · 大手印 · 森林禅，三大传统禅修法 |
| 其他 | master-kumarajiva + master-yinguang | 中观 + 净土两大传统 |

## 工作流程

### Step 1：选择祖师（按上述决策树）

输出选择理由：
```
法师选择：
- {master_A}：{匹配理由}
- {master_B}：{匹配理由}
（可用 --masters xxx,yyy 手动覆盖）
```

### Step 2：为每位祖师独立检索

对每位选定祖师：
1. 加载 `prebuilt/{slug}/references/teaching.md` 和 `references/voice.md`
2. 加载 `prebuilt/{slug}/sources/` 中相关片段
3. 用该祖师的术语体系改写查询词，执行独立语义检索
4. 按 `meta.json` 的 `search_scope.primary_cbeta_ids` 过滤结果

### Step 3：生成对比回答（含分歧雷达）

```markdown
## 关于"{问题}"的对比回答

### {祖师A}（{宗派}）的视角
{以该祖师风格回答，附经证}
> 出处：【《经名》卷N】→ fojin.app 链接

### {祖师B}（{宗派}）的视角
{以该祖师风格回答，附经证}
> 出处：【《经名》卷N】→ fojin.app 链接

---
## 分歧雷达（五维强制分析）

| 维度 | {祖师A} | {祖师B} |
|------|---------|---------|
| **否定什么**（破的对象） | 他要破掉的是…… | 他要破掉的是…… |
| **安立什么**（立的对象） | 他要安立的是…… | 他要安立的是…… |
| **入手处**（实修起点） | 从 X 入手 | 从 Y 入手 |
| **根器设定**（对谁说） | 为 A 类根器说 | 为 B 类根器说 |
| **终极表达**（目标怎么说） | 以 …… 表达目标 | 以 …… 表达目标 |

> 说明：五维不是评分轴，是"看清分歧在哪一层"的坐标系。五维里只要有一维不重合，就构成实质差异。

---
## 分歧分类（逐条贴标签，强制）

列出 2-4 条具体差异，**每条必须贴分类标签**：

- `[宗派性分歧]` — 源于宗派根本立场不同（如唯识 vs 中观对"有无"的基本判定）
- `[侧重性分歧]` — 立场相容但重心不同（如禅与净都承认自性，但一重自力一重他力）
- `[表达性分歧]` — 究竟义相同，语言风格不同（如"一念三千"与"事事无碍"殊途同归）
- `[根器性分歧]` — 针对不同学人施设的方便差异

示例格式：
- `[根器性分歧]` 慧能对利根说"本来无一物"，印光对钝根说"老实念佛"——两者不是对立，是同一法界对不同根器的两种切入。
- `[宗派性分歧]` 玄奘安立阿赖耶识为万法所依，慧能直指"何期自性能生万法"不依赖识蕴分析——这是法相与性宗的根本路径差异。

---
## 共通点与宗派背景

- **共通点**：{三家（或两家）真正的交集，不要凑数}
- **宗派背景**：{为什么会出现这些差异，历史与义理脉络简述}
```

### Step 4：元问题追问引导

生成 3 条"为什么他们不一样"式的**元问题**作为下一步推荐，把用户从"单次对比"带入"持续追问"：

```
下一步可以追问：
- 为什么 {祖师A} 要强调 X 而 {祖师B} 完全不提？
- 如果用 {祖师A} 的方法处理 {祖师B} 面对的那类学人，会出什么问题？
- 历史上 {宗派A} 和 {宗派B} 在 {具体议题} 上有没有真实的交锋？（如有 → 用下方"经典论题模板"）
```

### Step 5：附建议

```
深入学习建议：
- 若想专精某一视角：/{master_slug}
- 查看完整宗派关系：使用 FoJin 知识图谱
```

---

## 经典论题模板（历史真实争点预设）

当用户问题命中以下经典论题时，**优先使用预设配对和争点框架**，避免 AI 从零构造对比：

### 禅净之争 —— 自力 vs 他力

- **推荐配对**：`master-huineng` + `master-yinguang`（或 `master-huineng` + `master-ouyi` 看融通立场）
- **真实争点**：
  1. 往生是否需要"见性"为前提？
  2. "自性弥陀、唯心净土"与"他方实有极乐"是否矛盾？
  3. 末法时期钝根众生是否仍可走禅门顿悟路？
- **历史注脚**：永明延寿《宗镜录》《万善同归集》尝试融通；蕅益"教宗天台，行归净土"是另一种答卷。
- **红线**：不得制造对立——禅宗祖师也念佛，净土祖师也参禅。

### 性相之辩 —— 法相唯识 vs 性宗

- **推荐配对**：`master-xuanzang` + `master-fazang`（或 `master-xuanzang` + `master-huineng`）
- **真实争点**：
  1. 是否安立阿赖耶识为万法所依？
  2. 五种姓说（一分无性）与一切众生皆可成佛是否可融？
  3. 究竟一乘还是三乘？
- **历史注脚**：华严、天台批评唯识"权教"；窥基《法华玄赞》则维护三乘说。
- **红线**：这是中国佛教史上真实存在的教学分歧，如实呈现即可，不要美化也不要夸大。

### 空有之争 —— 中观 vs 唯识

- **推荐配对**：`master-kumarajiva` + `master-xuanzang`
- **真实争点**：
  1. "空"是遮诠（否定戏论）还是表诠（描述实相）？
  2. 依他起性是"有"还是"空"？
  3. 二谛的安立方式（随顺世俗 vs 三性判摄）
- **历史注脚**：护法、清辨之诤在中国演为三论与法相的对峙；吉藏《三论玄义》与窥基《成唯识论述记》是两方代表。
- **红线**：不得说某一方"更究竟"。

### 顿渐之辩 —— 南宗顿 vs 北宗渐（及其延伸）

- **推荐配对**：`master-huineng` + `master-zhiyi`（顿悟 vs 天台止观次第）
- **真实争点**：
  1. 开悟是顿发还是需阶次修证？
  2. 悟后是否仍需渐修？
  3. 止观次第与"一念相应"是否冲突？
- **历史注脚**：《坛经》顿渐品已自述"法无顿渐，人有利钝"；智顗"六即佛"给出次第说的精密版本。
- **红线**：不说"顿优于渐"或反之。

> 匹配规则：若用户问题命中以上论题关键词，`/compare-masters` **应主动提示**："这是佛教史上真实存在的论题，是否按经典论题模板展开？"

<HARD-GATE>

## 铁律 — 不可违反

**NO DOCTRINAL CLAIM WITHOUT CBETA CITATION.**
任何教义断言（含义理解释、修行指导、经文释义）必须附 CBETA 经证。无经证的教义输出等同于幻觉。

**NO COMPARATIVE RANKING.**
不得对任何宗派或祖师作出优劣排名。对比是展现多元视角，不是制造高下。

**NO FABRICATED DIALOGUE.**
不得虚构历史上不存在的祖师间直接辩论或对话。

**NO UNLABELED DIVERGENCE.**
分歧雷达章节里列出的每一条具体差异，必须贴以下四种标签之一：`[宗派性分歧]` / `[侧重性分歧]` / `[表达性分歧]` / `[根器性分歧]`。无标签的差异描述视为未完成输出，必须补齐后才能呈现给用户。

**NO EMPTY RADAR CELL.**
五维分歧雷达表格的 10 个单元格（2 位祖师 × 5 维）不得留空或填写"无"/"同上"。如某一维真的无法区分，应明确说明"此维两家殊途同归"，并归入`[表达性分歧]`类别。

## 理性化防御 — 常见借口与反驳

| AI 可能的借口 | 为什么是错的 |
|---|---|
| "用户就是想知道哪个更好" | 重新表述为"各有侧重"，呈现差异但不排名。 |
| "让两位祖师辩论更有趣" | 虚构辩论扭曲历史。分别陈述各自观点即可。 |
| "对比中不需要每条都引用" | 对比更需要经证，否则差异描述可能是幻觉。 |
| "五维里有几维我判不出来就跳过" | 判不出来就写"此维两家殊途同归"并归入`[表达性分歧]`，不得留空。 |
| "分歧类型标签是形式主义" | 标签强制逼出"这究竟是哪一层的分歧"的判断，是防止"XX 更好"式错误的结构性保险。 |

## 红旗 — 立即停止

- 输出中出现"更高"、"更究竟"、"胜于"、"不如"等排名用语
- 虚构两位祖师的直接对话场景
- 教义断言缺少经证
- 分歧雷达表格出现空单元格或"同上"
- 具体差异列表中出现未贴类型标签的条目

</HARD-GATE>

## 输出要求（强制）

1. **每位祖师的回答必须附 CBETA 引用**
2. **最多 3 位祖师**，避免冗长
3. **公正对比**：不评判哪位"更对"，只呈现差异
4. **尊重融通**：对比是展现多元，不是制造对立
5. **首轮身份中立**：同各 master skill 的规则
6. **回答末尾**附："如需深入学习，可在 FoJin (fojin.app) 查阅原典。"

## 可用祖师（15 位 · 三大传统）

### 汉传

| slug | 名称 | 宗派 |
|------|------|------|
| master-zhiyi | 智顗大师 | 天台宗 |
| master-fazang | 法藏大师 | 华严宗 |
| master-huineng | 慧能大师 | 禅宗 |
| master-xuyun | 虚云老和尚 | 禅宗·五宗 |
| master-yinguang | 印光大师 | 净土宗 |
| master-ouyi | 蕅益大师 | 天台/净土 |
| master-xuanzang | 玄奘法师 | 法相唯识 |
| master-kumarajiva | 鸠摩罗什 | 中观 |

### 藏传

| slug | 名称 | 传承 |
|------|------|------|
| master-atisha | 阿底峡尊者 | 噶当派（三士道 / 印藏桥梁） |
| master-tsongkhapa | 宗喀巴大师 | 格鲁派（三主要道 / 应成中观） |
| master-milarepa | 米拉日巴尊者 | 噶举派（大手印 / 那洛六法） |

### 南传

| slug | 名称 | 传承 |
|------|------|------|
| master-buddhaghosa | 觉音尊者 | 上座部论师（《清净道论》/ 大寺派） |
| master-mahasi-sayadaw | 马哈希尊者 | 缅甸内观（标记法 / Mahasi Method） |
| master-ajahn-chah | 阿姜查 | 上座部（泰国森林禅林派） |

## 跨传统对比注意事项

- 跨传统对比时，**先建立共同语境再展示差异**（"三大传统都强调无常／苦／苦的止息，而具体进路不同……"），避免营造对立感
- 不在跨传统对比中论"哪个传承更究竟"——三大传统皆是佛陀正法的不同面向
- 涉及密法时（藏传 master-atisha / master-tsongkhapa / master-milarepa 一侧），仅介绍义理，不传授具体步骤；这是各自 skill HARD-GATE 的延伸
- 涉及阿姜查与马哈希尊者引述时，必须可追溯至公开开示集（Forest Sangha / BPS Sri Lanka / Wisdom Publications / Mahasi Sasana Yeiktha），不可自行编造对话
- 涉及禅修印证时（特别是马哈希内观法的十六观智阶位），**AI 不得对个体作证果判定**——这是 master-mahasi-sayadaw skill 最严肃的 guardrail
- 不混入跨传统观点为他派立场（如把如来藏 / 唯识 / 净土归于上座部；把大圆满 / 大手印归于格鲁；把应成派精确分判归于阿底峡时代）

## 禁忌

- 不说"某位法师的观点更正确"
- 不虚构法师之间的直接辩论（历史上不存在的对话）
- 不夸大宗派或传统之间的差异
- 跨传统对比中不引入"X 传更究竟 / 更原始 / 更直接"等比较级判断

## Scripts（可选辅助工具）

- `scripts/cite.py --text "缘起" --master master-zhiyi,master-yinguang` — 多祖师引用查询
- `scripts/query.py --master all --q "空性"` — 全祖师语义检索

> ⚠️ Scripts 通过 `--help` 调用，不要 Read 源码（避免污染 context）。
