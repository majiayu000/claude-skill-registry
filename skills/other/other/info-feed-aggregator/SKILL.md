---
name: info-feed-aggregator
description: >
  多源信息聚合与精炼报告工具。从学术数据库（arXiv、Semantic Scholar、IEEE Xplore、Crossref）
  和社交媒体（微信公众号、小红书、RSS）聚合搜索结果，经去重评分后生成精炼分析报告（PDF），
  包含方向分类、核心贡献提炼、趋势分析与推荐精读。
  触发词：搜论文、学术搜索、信息聚合、论文监控、搜公众号、feed、aggregate
---

# Info Feed Aggregator

多源信息聚合 Skill —— 从学术论文到社交媒体，一站式搜集、去重、评分、报告。

## 能力概览

| 来源 | 状态 | 说明 |
|------|------|------|
| arXiv | 默认开启 | 免费 API，无需密钥 |
| Semantic Scholar | 默认开启 | 免费 API，1000次/5min |
| IEEE Xplore | 默认开启 | 直接搜索，无需密钥 |
| Crossref | 可选 | 免费，补充 DOI 元数据 |
| 微信公众号 | 默认开启 | 搜狗微信搜索，无需配置 |
| 小红书 | 暂停 | 搜索引擎索引有限，后续接入 |
| 通用 RSS | 可选 | 任意 RSSHub 路由 |

## 工作流

### 1. 即时搜索（Ad-hoc）

当用户请求搜索特定关键词时：

```bash
cd /Users/zhanglinghao/Documents/Code/Skills/skills/info-feed-aggregator
python3 scripts/search.py --keywords "关键词1" "关键词2" --max-results 20
```

读取 stdout 输出的 JSON 摘要，获取报告文件路径，然后读取 Markdown 报告并呈现给用户。

**参数说明：**
- `--keywords`：搜索关键词列表（支持中英文）
- `--sources`：指定数据源（默认使用所有已启用源），如 `--sources arxiv semantic_scholar`
- `--max-results`：最大结果数（默认 20）
- `--time-range`：时间范围，如 `7d`（7天）、`30d`（30天）、`1y`（1年）
- `--language`：报告语言 `zh` 或 `en`
- `--output-format`：原始报告输出格式 `json`、`markdown`、`pdf`、`both`（默认 `both` = JSON + MD）。注意：精炼报告 PDF 由 Section 4 流程单独生成，不受此参数控制

### 2. Profile 定时搜索

当用户要求按预设方案搜索时：

```bash
python3 scripts/search.py --profile daily_academic
```

Profile 文件位于 `config/profiles/` 目录，定义了多个搜索主题（topic），每个主题包含关键词、分类、时间范围等。

**列出可用 Profile：**
```bash
python3 scripts/search.py --list-profiles
```

### 3. 健康检查

检查各数据源连通性：

```bash
python3 scripts/search.py --health
```

### 4. 精炼报告生成（核心输出）

搜索完成后，基于原始聚合报告（raw MD），生成一份 **精炼分析报告**，这是本技能的最终交付物。

**流程：**

1. 读取 stdout JSON 获取 `output_files` 路径
2. 读取原始 Markdown 报告（分段读取，每段 200 行）
3. **通读全部论文**，理解每篇论文的核心贡献、方法和创新点
4. 按研究方向/主题 **重新分类** 论文（不使用原始 adhoc 分组）
5. **补充作者与机构信息**：对每篇重点论文，从原始报告提取主要作者；如机构信息不完整，通过 WebSearch 查询补全
6. 撰写精炼报告 Markdown，保存为 `reports/{timestamp}_briefing.md`
7. 渲染 PDF：
   ```bash
   cd /Users/zhanglinghao/Documents/Code/Skills/skills/info-feed-aggregator
   python3 scripts/render_pdf.py -i reports/{timestamp}_briefing.md -o reports/{timestamp}_briefing.pdf
   ```
8. 向用户呈现 PDF 路径和报告内容摘要

**精炼报告模板（必须严格遵循）**：

```markdown
# 学术前沿速报

**日期**: YYYY-MM-DD
**关键词**: keyword1, keyword2, keyword3
**覆盖来源**: arXiv, IEEE Xplore, Semantic Scholar, 微信公众号
**数据概览**: N 篇文献（M 学术论文 + K 资讯）

---

## 综述摘要

本次搜索围绕 [关键词] 三大方向，覆盖 [来源] 共 N 篇文献。

**主要发现：**

1. **[方向一名称]**：发现 X 篇相关论文。[2-3 句概括该方向的核心进展和趋势]
2. **[方向二名称]**：Y 篇新进展。[2-3 句概括]
3. **[方向三名称]**：Z 篇论文关注。[2-3 句概括]

**推荐精读：**

- [论文标题](链接) — [1 句推荐理由]
- [论文标题](链接) — [1 句推荐理由]

---

## 方向一：[方向名称]（X 篇）

> [1-2 段该方向的综合分析：当前研究热点是什么？主流方法是什么？有哪些新趋势？]

### 1. [论文标题](链接)

**作者**：First Author, Second Author et al. | **机构**：University/Institute Name
**核心贡献**：[2-3 句话概括论文的核心创新，不是摘要复制，而是提炼要点]
**方法亮点**：[1-2 句点出关键技术/算法]
**关键指标**：[如有量化结果，列出关键数字]

`ieee` | 被引: 7 | 相关度: ★★★☆☆

### 2. [论文标题](链接)

...（同上格式）

---

## 方向二：[方向名称]（Y 篇）

> [该方向综合分析]

### 1. ...

---

## 资讯动态概览

> [如有微信/RSS 等社交媒体内容，用 1-2 段概括业界动态。如无则省略此节]

- **[资讯标题]** — [1 句话概括]
- ...

---

## 研究趋势与建议

基于本次 N 篇文献的整体分析：

1. **[趋势一]**：[2-3 句分析]
2. **[趋势二]**：[2-3 句分析]
3. **[趋势三]**：[2-3 句分析]

**建议关注**：[1-2 句针对用户研究方向的具体建议]

---

*由 info-feed-aggregator 生成于 YYYY-MM-DD HH:MM*
```

**撰写要求：**

- **不要复制粘贴原始摘要** — 用自己的话提炼每篇论文的核心贡献和亮点
- **重新分类** — 根据论文内容按研究方向分组（如"MEC 任务卸载"、"AIGC 缓存与传输"、"新型天线架构"），而非使用原始的 adhoc 分组
- **综合分析** — 每个方向的开头要有 1-2 段整体分析，不只是论文罗列
- **标注作者与机构** — 每篇重点论文标注第一作者（或前 2-3 位）和所属机构，中国机构附加中文名
- **保留关键链接** — 每篇论文标题保留原始 URL 链接
- **低相关度论文可合并** — 相关度 ≤ 0.40 的论文可以合并为简要列表，不需逐一展开
- **资讯动态精简** — 微信等社交媒体内容如果质量不高（如摘要碎片化），可合并为概览
- **如用户提出了具体研究问题**，在综述摘要和趋势分析中融入对该问题的回应

### 5. 深度分析（可选后续步骤）

对搜索结果中感兴趣的条目，可以：
- 打开论文链接精读
- 使用 WebSearch 补充背景信息
- 基于搜索结果做领域综述或趋势分析

## 配置

### 数据源配置

编辑 `config/sources.json` 修改数据源连接参数：

```json
{
  "sources": {
    "ieee": {
      "enabled": true,
      "method": "web"
    },
    "wechat": {
      "enabled": true,
      "method": "sogou"
    }
  }
}
```

> 默认配置无需 API Key。IEEE 使用网页搜索，微信使用搜狗微信搜索。

### 搜索 Profile

在 `config/profiles/` 下创建 JSON 文件定义搜索方案：

```json
{
  "name": "my_research",
  "description": "我的研究方向监控",
  "topics": [
    {
      "id": "topic_1",
      "keywords": ["keyword1", "keyword2"],
      "time_range": "7d",
      "max_items": 15
    }
  ],
  "sources": ["arxiv", "semantic_scholar", "ieee"],
  "report": {
    "language": "zh",
    "group_by": "topic"
  }
}
```

## 输出示例

搜索完成后 stdout 输出：

```json
{
  "status": "ok",
  "total_raw": 45,
  "total_deduped": 32,
  "sources_used": ["arxiv", "semantic_scholar"],
  "output_files": {
    "json": "reports/20260312_feed.json",
    "markdown": "reports/20260312_feed.md"
  }
}
```

## 依赖安装

```bash
# 搜索脚本依赖
pip install requests feedparser

# PDF 渲染依赖（pandoc + xelatex）
brew install pandoc
brew install --cask mactex  # 或 basictex + 手动安装 CJK 包
```

> PDF 渲染使用 pandoc + xelatex，自动使用系统中文字体（PingFang SC）。

## 定时任务

- **Claude Code**：通过 `scheduled-tasks` 配置定时执行
- **OpenClaw**：通过 cron 任务调度（后续单独配置）
