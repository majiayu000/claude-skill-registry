---
name: "paper-search"
description: "Search academic papers via OpenAlex + AnySearch with cross-validation for math modeling references. Invoke when user needs literature search, paper references, or when writing papers requires citations."
---

# Paper Search Skill - 论文搜索技能

本技能通过 **OpenAlex API** + **AnySearch Academic** 双引擎并行搜索，实现学术论文的交叉验证式检索，为数学建模论文撰写提供更可靠的参考文献支持。

---

## 功能概述

| 功能 | 说明 |
|------|------|
| **双引擎并行搜索** | 同时调用 OpenAlex 和 AnySearch 两个独立数据源 |
| **交叉验证** | 同一篇论文同时被两个源收录时标记为交叉验证，可信度更高 |
| **单源回退** | 可单独使用 OpenAlex 或 AnySearch |
| **多条件过滤** | 按引用量、发表年份、研究领域筛选（OpenAlex） |
| **多方式排序** | 按相关性/引用量/发表年份排序 |
| **摘要获取** | 自动重建并返回论文摘要 |
| **引用格式化** | 生成标准的 APA 引用格式 |

---

## 使用场景

在以下情况下使用本技能：

1. **建模分析阶段**：查找模型相关的理论文献
2. **论文撰写阶段**：为论文添加参考文献引用
3. **算法验证阶段**：查找算法的原始论文
4. **用户请求**：用户明确要求搜索论文或文献
5. **引用可靠性要求高**：需要确认某篇论文确实存在且被多个索引收录

---

## 双引擎架构

```
                              ┌──────────────────────┐
                              │   论文手 / 建模手       │
                              │  (发起搜索请求)         │
                              └──────────┬───────────┘
                                         │
                              ┌──────────▼───────────┐
                              │   hybrid_scholar.py   │
                              │   (混合搜索调度器)      │
                              └──────┬──────────┬─────┘
                                     │          │
                          ┌──────────▼──┐  ┌───▼───────────┐
                          │  OpenAlex   │  │  AnySearch    │
                          │  论文数据库  │  │  Academic域   │
                          │ (结构化元数 │  │ (实时网络搜索) │
                          │  据丰富)    │  │               │
                          └─────────────┘  └───────────────┘
                                     │          │
                                     └────┬─────┘
                                          ▼
                              ┌──────────────────────┐
                              │   合并 · 去重 · 标记   │
                              │   → 交叉验证论文      │
                              │   → OpenAlex 独有     │
                              │   → AnySearch 独有    │
                              └──────────────────────┘
```

### 引擎对比

| 维度 | OpenAlex | AnySearch Academic |
|------|----------|-------------------|
| **数据源** | 开放学术图谱（结构化） | 实时网络学术搜索 |
| **覆盖范围** | 2.5亿+ 论文，结构化元数据 | 实时学术网页索引 |
| **引用数据** | 精确引用计数 | 估计值或无 |
| **摘要** | 有（倒排索引） | 可能有 |
| **领域过滤** | 支持（概念ID） | 不支持 |
| **排序** | 相关性/引用量/年份 | 相关性 |
| **API Key** | 不需要（需邮箱礼貌池） | 可选（匿名有速率限制） |
| **响应速度** | ~0.5-2s | ~1-3s |

### 交叉验证的好处

- 两个独立数据源同时返回的论文 → 可信度显著提高
- 适合挑选关键引用放入论文
- 降低引用了"不存在"或"检索错误"论文的风险

---

## 使用方法

### 方法一：混合搜索（推荐）

使用 `hybrid_scholar.py` 同时调用两个引擎：

```bash
# 基础混合搜索
python tools/paper_search/scripts/hybrid_scholar.py --query "grey prediction model" --email "your@email.com"

# 高级过滤 + 交叉验证
python tools/paper_search/scripts/hybrid_scholar.py --query "TOPSIS" --min-citations 10 --year-from 2020 --field mathematics --limit 10

# JSON 输出
python tools/paper_search/scripts/hybrid_scholar.py --query "LSTM" --json
```

输出分为三个区域：

```
============================================================
  交叉验证搜索结果: grey prediction model
============================================================
  数据源: OpenAlex + AnySearch
  统计: OpenAlex 8 篇 | AnySearch 6 篇 | 交叉验证 3 篇

  ★ 交叉验证 — OpenAlex + AnySearch 同时收录
  ────────────────────────────────────────────────────────
  [1] Grey Forecasting Model (2020) | 引用: 128 | DOI: 10.xxx

  ◆ OpenAlex 独有 — 仅来自 OpenAlex
  ────────────────────────────────────────────────────────
  [2] ...

  ◇ AnySearch 独有 — 仅来自 AnySearch
  ────────────────────────────────────────────────────────
  [3] ...
```

### 方法二：单引擎搜索

```bash
# 仅用 OpenAlex（传统模式）
python tools/paper_search/scripts/hybrid_scholar.py --query "genetic algorithm" --openalex-only --email "your@email.com"

# 仅用 AnySearch（无需邮箱）
python tools/paper_search/scripts/hybrid_scholar.py --query "reinforcement learning" --anysearch-only

# OpenAlex 原生脚本（向后兼容）
python tools/paper_search/scripts/openalex_scholar.py --query "grey prediction model" --email "your@email.com"
```

### 方法三：在代码中调用

```python
from hybrid_scholar import HybridScholar

scholar = HybridScholar(
    email="your@email.com",
    anysearch_api_key="your_key_optional",
)

# 混合搜索 + 交叉验证
result = scholar.search_papers(
    query="grey prediction model",
    limit=10,
    sort="cited_by_count:desc",
    min_citations=10,
    year_from=2015,
    field_filter="mathematics",
)

# 打印结果
scholar.print_results(result)

# 获取结构化数据
for paper in result["cross_validated"]:
    print(f"[交叉验证] {paper.title} — {', '.join(paper.sources)}")

# 转为 JSON
json_str = scholar.results_to_json(result)
```

### 返回数据结构

```python
{
    "query": "grey prediction model",
    "cross_validated": [HybridPaper, ...],    # 同时被两个源收录
    "openalex_only": [HybridPaper, ...],      # 仅 OpenAlex 收录
    "anysearch_only": [HybridPaper, ...],     # 仅 AnySearch 收录
    "stats": {
        "openalex_total": 8,       # OpenAlex 返回总数
        "anysearch_total": 6,      # AnySearch 返回总数
        "cross_validated": 3,      # 交叉验证论文数
        "openalex_unique": 5,      # OpenAlex 独有
        "anysearch_unique": 3,     # AnySearch 独有
    }
}
```

### HybridPaper 属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `title` | str | 论文标题 |
| `authors` | List[str] | 作者列表 |
| `year` | int/None | 发表年份 |
| `citations` | int | 被引用次数 |
| `doi` | str/None | DOI 标识符 |
| `abstract` | str/None | 摘要 |
| `sources` | List[str] | 来源引擎：["openalex"], ["anysearch"], 或 ["openalex", "anysearch"] |
| `cross_validated` | bool | 是否交叉验证（两个源同时收录） |
| `source_tag` | str | 显示用标签："✓ 交叉验证" / "openalex" / "anysearch" |

---

## 经典文献搜索策略

**根据搜索目的选择搜索策略**：

| 目的 | 推荐参数 | 说明 |
|------|---------|------|
| 找经典理论文献 | `sort="cited_by_count:desc"` `min_citations=50` | 被引最高的该领域奠基性工作 |
| 找最新前沿进展 | `sort="publication_year:desc"` `year_from=2020` | 近年最新成果 |
| 找数学方法论论文 | `field_filter="mathematics"` | 限定数学领域 |
| 找算法应用案例 | `field_filter="engineering"` | 工程领域应用 |
| 找建模竞赛可用文献 | `min_citations=5` `year_from=2015` | 适中的引用量+时效性 |
| **高可信引用** | 混合搜索，优先选择交叉验证结果 | 两个源同时确认的论文 |

---

## 数学建模常用搜索关键词

### 优化算法
- `linear programming optimization`
- `genetic algorithm optimization`
- `particle swarm optimization`
- `simulated annealing`
- `vehicle routing problem`

### 预测模型
- `grey prediction model GM(1,1)`
- `ARIMA time series forecasting`
- `LSTM neural network prediction`
- `prophet forecasting`

### 评价方法
- `analytic hierarchy process AHP`
- `TOPSIS multi-criteria decision`
- `entropy weight method`
- `data envelopment analysis DEA`

### 图论与网络
- `shortest path algorithm`
- `minimum spanning tree`
- `maximum flow network`

---

## 配置说明

### OpenAlex 邮箱配置

```bash
# 所有 OpenAlex 搜索需提供邮箱
--email "your@email.com"
```

### AnySearch API Key（可选）

AnySearch 匿名可用（有限速），建议配置 API Key：

```bash
# 方式 1：环境变量
export ANYSEARCH_API_KEY="your_key_here"

# 方式 2：CLI 参数
python hybrid_scholar.py --query "..." --anysearch-api-key "your_key_here"

# 方式 3：.env 文件
# 在项目根目录或通过环境变量设置
# ANYSEARCH_API_KEY=your_key_here
```

---

## 相关文件

| 文件 | 说明 |
|------|------|
| `scripts/hybrid_scholar.py` | **混合搜索引擎（主入口，推荐使用）** |
| `scripts/openalex_scholar.py` | OpenAlex 搜索实现（hybrid_scholar 的后端之一） |
| `scripts/anysearch_academic.py` | AnySearch Academic 封装（hybrid_scholar 的后端之一） |

---

## 参考链接

- [OpenAlex API 文档](https://docs.openalex.org/)
- [OpenAlex 礼貌池规则](https://docs.openalex.org/how-to-use-the-api/rate-limits-and-authentication)
- [AnySearch 项目](https://github.com/anysearch-ai/anysearch-skill)
