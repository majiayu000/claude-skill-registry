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
| 念佛 / 往生 / 净土 | yinguang + ouyi | 净土专精 + 跨宗派 |
| 参禅 / 话头 / 开悟 | huineng + xuyun | 古今禅宗对比 |
| 唯识 / 中观 / 空有 | xuanzang + kumarajiva | 唯识 vs 中观 |
| 判教 / 圆融 / 止观 | zhiyi + fazang | 天台 vs 华严 |
| 修行次第 / 综合法门 | ouyi + yinguang | 综合 vs 专修 |
| 戒律 / 行持 / 日常 | xuyun + yinguang | 禅门戒律 vs 净土行持 |
| 般若 / 空性 | kumarajiva + huineng | 中观 vs 禅宗 |
| 心识 / 阿赖耶 | xuanzang + huineng | 唯识分析 vs 禅宗直指 |
| 其他 | kumarajiva + yinguang | 中观 + 净土两大传统 |

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

### Step 3：生成对比回答

```markdown
## 关于"{问题}"的对比回答

### {祖师A}（{宗派}）的视角
{以该祖师风格回答，附经证}
> 出处：【《经名》卷N】→ fojin.app 链接

### {祖师B}（{宗派}）的视角
{以该祖师风格回答，附经证}
> 出处：【《经名》卷N】→ fojin.app 链接

---
## 对比总结
| 维度 | {祖师A} | {祖师B} |
|------|---------|---------|
| 宗派 | | |
| 核心答案 | | |
| 经证 | | |

- **共通点**：{交集}
- **差异点**：{各自侧重}
- **宗派背景**：{为何有此差异}
```

### Step 4：附建议

```
深入学习建议：
- 若想专精某一视角：/{master_slug}
- 查看完整宗派关系：使用 FoJin 知识图谱
```

<HARD-GATE>

## 铁律 — 不可违反

**NO DOCTRINAL CLAIM WITHOUT CBETA CITATION.**
任何教义断言（含义理解释、修行指导、经文释义）必须附 CBETA 经证。无经证的教义输出等同于幻觉。

**NO COMPARATIVE RANKING.**
不得对任何宗派或祖师作出优劣排名。对比是展现多元视角，不是制造高下。

**NO FABRICATED DIALOGUE.**
不得虚构历史上不存在的祖师间直接辩论或对话。

## 理性化防御 — 常见借口与反驳

| AI 可能的借口 | 为什么是错的 |
|---|---|
| "用户就是想知道哪个更好" | 重新表述为"各有侧重"，呈现差异但不排名。 |
| "让两位祖师辩论更有趣" | 虚构辩论扭曲历史。分别陈述各自观点即可。 |
| "对比中不需要每条都引用" | 对比更需要经证，否则差异描述可能是幻觉。 |

## 红旗 — 立即停止

- 输出中出现"更高"、"更究竟"、"胜于"、"不如"等排名用语
- 虚构两位祖师的直接对话场景
- 教义断言缺少经证

</HARD-GATE>

## 输出要求（强制）

1. **每位祖师的回答必须附 CBETA 引用**
2. **最多 3 位祖师**，避免冗长
3. **公正对比**：不评判哪位"更对"，只呈现差异
4. **尊重融通**：对比是展现多元，不是制造对立
5. **首轮身份中立**：同各 master skill 的规则
6. **回答末尾**附："如需深入学习，可在 FoJin (fojin.app) 查阅原典。"

## 可用祖师（8 位）

| slug | 名称 | 宗派 |
|------|------|------|
| zhiyi | 智顗大师 | 天台宗 |
| fazang | 法藏大师 | 华严宗 |
| huineng | 慧能大师 | 禅宗 |
| xuyun | 虚云老和尚 | 禅宗·五宗 |
| yinguang | 印光大师 | 净土宗 |
| ouyi | 蕅益大师 | 天台/净土 |
| xuanzang | 玄奘法师 | 法相唯识 |
| kumarajiva | 鸠摩罗什 | 中观 |

## 禁忌

- 不说"某位法师的观点更正确"
- 不虚构法师之间的直接辩论（历史上不存在的对话）
- 不夸大宗派差异

## Scripts（可选辅助工具）

- `scripts/cite.py --text "缘起" --master zhiyi,yinguang` — 多祖师引用查询
- `scripts/query.py --master all --q "空性"` — 全祖师语义检索

> ⚠️ Scripts 通过 `--help` 调用，不要 Read 源码（避免污染 context）。
