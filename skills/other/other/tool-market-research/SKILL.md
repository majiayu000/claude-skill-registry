---
name: tool-market-research
description: >
  Web Toolbox 市场调研与用户痛点挖掘。通过搜索 Reddit、Hacker News、TikTok、Product Hunt、
  Google Trends 等平台，发现高流量在线工具机会、用户吐槽的痛点、竞品流量数据，生成可落地的
  新工具建议报告。使用此 skill 当用户提到：(1) 调研新工具机会 (2) 挖掘用户痛点 (3) 分析
  竞品流量 (4) 更新工具箱 ROADMAP (5) "做一次市场调研" (6) "今天有什么新发现"
  (7) /research 或 /调研
---

# Web Toolbox 市场调研 Skill

## 项目背景

Web Toolbox (https://www.heyuan110.com/web-toolbox/) 是一套纯前端在线工具集，核心竞争力：
- 纯浏览器端运行，无后端
- 无广告、无注册、无水印
- 免费、开源

ROADMAP 位于项目的 `docs/ROADMAP.md`，包含已上线和待开发工具列表。

## 调研执行流程

按以下 6 个阶段顺序执行，每阶段内的搜索尽量并行发起以提高效率。

### 阶段 1：用户痛点挖掘（Reddit + HN）

同时发起以下搜索（用 WebSearch 工具）：

```
搜索 1: Reddit "I wish there was" OR "is there a free" online tool {当前年份}
搜索 2: Reddit "too many ads" OR "forced to sign up" OR "watermark" free online tool
搜索 3: site:news.ycombinator.com "what tool do you wish existed" {当前年份}
搜索 4: Reddit r/webdev OR r/SideProject "built a free" tool launched {当前年份}
搜索 5: Reddit "why is there no free" tool converter editor {当前年份}
```

**关注信号**：用户抱怨（广告多、要注册、有水印、功能阉割）、工具请求、高赞帖子

### 阶段 2：趋势与热度（Google Trends + 搜索量）

```
搜索 1: most searched free online tools {当前年份} trending Google Trends
搜索 2: "online tool" highest search volume keywords {当前年份}
搜索 3: Google Trends rising searches "free tool" {当前年份} categories
搜索 4: top 100 Google searches {当前年份} worldwide tools
```

**关注信号**：搜索量上升的工具类目、新兴需求、AI 相关工具趋势

### 阶段 3：竞品流量分析

```
搜索 1: ilovepdf smallpdf competitor traffic {当前年份} SimilarWeb
搜索 2: most popular online tools websites traffic canva tinypng {当前年份}
搜索 3: "{具体竞品}" traffic analytics SimilarWeb {当前年份}
```

**重点竞品列表**（需追踪）：
- PDF 工具: iLovePDF, SmallPDF, Sejda, PDF2Go
- 图片工具: TinyPNG, remove.bg, Canva, Photopea
- 开发者工具: JSON Editor Online, regex101, CodePen
- 综合工具: 10015.io, toolpix, freeconvert

**关注信号**：各竞品月访问量变化、流量来源（organic 占比）、热门工具品类

### 阶段 4：新产品动态（Product Hunt + 社交媒体）

```
搜索 1: ProductHunt trending free online tools {当前月份} {当前年份}
搜索 2: TikTok viral online tools productivity hacks {当前年份}
搜索 3: Reddit r/InternetIsBeautiful free tool popular {当前年份}
搜索 4: "I made" OR "just launched" free tool {当前年份} site:reddit.com
```

**关注信号**：获得高票的新工具、TikTok 上病毒传播的工具视频、r/InternetIsBeautiful 热帖

### 阶段 5：细分品类深挖

根据阶段 1-4 发现的热点，对以下重点品类进行针对性搜索：

```
品类 A - 文件处理: "PDF merge" OR "compress video" OR "convert file" free online {当前年份}
品类 B - 开发者工具: "JSON formatter" OR "regex tester" OR "diff tool" OR "CSS generator" free online
品类 C - AI 工具: "AI image" OR "AI writing" OR "text to speech" free browser tool {当前年份}
品类 D - 设计工具: "color picker" OR "gradient generator" OR "SVG editor" OR "favicon generator" free online
品类 E - 生活效率: "resume builder" OR "invoice generator" OR "calculator" free no signup
```

如果阶段 1-4 发现了新热点品类，追加对应搜索。

### 阶段 6：交叉验证与报告

1. **读取 ROADMAP**：Read `docs/ROADMAP.md`，获取已上线和已计划工具列表
2. **去重**：排除已上线和已在 ROADMAP 中的工具
3. **评估**：对每个新发现的机会评估：
   - 搜索量级（千万/百万/十万/万）
   - 开发难度（⭐~⭐⭐⭐）
   - 纯前端可行性（是否需要后端）
   - 与现有工具的互补性
4. **输出报告**

## 报告输出格式

```markdown
## 用户痛点深度挖掘报告 ({日期})

### 核心发现
- 用户最常吐槽的 3 个痛点
- 今日调研的关键洞察

### 新工具机会矩阵（ROADMAP 之外的增量）

#### S 级（百万级搜索量，必做）
| # | 工具名 | 搜索量级 | 痛点来源 | 用户痛点 | 难度 | 纯前端可行 |

#### A 级（十万级搜索量，高性价比）
| # | 工具名 | 搜索量级 | 痛点来源 | 用户痛点 | 难度 | 纯前端可行 |

#### B 级（万级搜索量，差异化竞争）
| # | 工具名 | 搜索量级 | 痛点来源 | 用户痛点 | 难度 | 纯前端可行 |

### 竞品流量情报
| 竞品 | 月访问量 | 核心品类 | 变化趋势 | 可学习点 |

### 趋势信号
- 上升中的工具品类
- AI 相关新机会
- 社交媒体热议话题

### 战略建议
1. 立即可做的（低难度高回报）
2. ROADMAP 优先级调整建议
3. 推广策略建议

### Sources
- [来源标题](URL)
```

## 调研频率建议

| 频率 | 内容侧重 |
|------|---------|
| 每日 | 阶段 1 + 阶段 4（痛点 + 新品），快速扫描 |
| 每周 | 全部 6 阶段完整执行 |
| 每月 | 完整执行 + 更新 ROADMAP + 竞品深度分析 |

用户说"快速调研"时只执行阶段 1 + 4，说"完整调研"时执行全部 6 阶段。默认执行全部。

## 搜索技巧

- 优先使用英文搜索（覆盖面更广）
- Reddit 搜索加 `site:reddit.com` 前缀提高精准度
- HN 搜索可直接 WebFetch `https://hn.algolia.com/api/v1/search?query=...`
- 搜索量数据优先引用 SimilarWeb、Semrush、Ahrefs 的公开数据
- 对找到的 HN 讨论帖，用 WebFetch 抓取完整评论提取具体工具需求
- 搜索词中加入当前年份以获取最新结果
