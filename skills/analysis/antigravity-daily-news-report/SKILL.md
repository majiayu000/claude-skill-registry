---
name: daily-news-report
description: 基于预设 URL 列表抓取内容，筛选高质量技术信息并生成每日 Markdown 报告。
argument-hint: [可选: 日期]
disable-model-invocation: false
user-invocable: true
allowed-tools: Task, WebFetch, Read, Write, Bash(mkdir*), Bash(date*), Bash(ls*), mcp__chrome-devtools__*
---

# Daily News Report v3.0

> **架构升级**：主 Agent 调度 + SubAgent 执行 + 浏览器抓取 + 智能缓存

## 核心架构

```
┌─────────────────────────────────────────────────────────────────────┐
│                        主 Agent (Orchestrator)                       │
│  职责：调度、监控、评估、决策、汇总                                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐     │
│   │ 1. 初始化 │ → │ 2. 调度   │ → │ 3. 监控   │ → │ 4. 评估   │     │
│   │ 读取配置  │    │ 分发任务  │    │ 收集结果  │    │ 筛选排序  │     │
│   └──────────┘    └──────────┘    └──────────┘    └──────────┘     │
│         │               │               │               │           │
│         ▼               ▼               ▼               ▼           │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐     │
│   │ 5. 决策   │ ← │ 够20条？  │    │ 6. 生成   │ → │ 7. 更新   │     │
│   │ 继续/停止 │    │ Y/N      │    │ 日报文件  │    │ 缓存统计  │     │
│   └──────────┘    └──────────┘    └──────────┘    └──────────┘     │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
         ↓ 调度                              ↑ 返回结果
┌─────────────────────────────────────────────────────────────────────┐
│                        SubAgent 执行层                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐              │
│   │ Worker A    │   │ Worker B    │   │ Browser     │              │
│   │ (WebFetch)  │   │ (WebFetch)  │   │ (Headless)  │              │
│   │ Tier1 Batch │   │ Tier2 Batch │   │ JS渲染页面   │              │
│   └─────────────┘   └─────────────┘   └─────────────┘              │
│         ↓                 ↓                 ↓                        │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │                    结构化结果返回                             │   │
│   │  { status, data: [...], errors: [...], metadata: {...} }    │   │
│   └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## 配置文件

本 Skill 使用以下配置文件：

| 文件 | 用途 |
|------|------|
| `sources.json` | 信息源配置、优先级、抓取方法 |
| `cache.json` | 缓存数据、历史统计、去重指纹 |

## 执行流程详解

### Phase 1: 初始化

```yaml
步骤:
  1. 确定日期（用户参数或当前日期）
  2. 读取 sources.json 获取源配置
  3. 读取 cache.json 获取历史数据
  4. 创建输出目录 NewsReport/
  5. 检查今日是否已有部分报告（追加模式）
```

### Phase 2: 调度 SubAgent

**策略**：并行调度，分批执行，早停机制

```yaml
第1波 (并行):
  - Worker A: Tier1 Batch A (HN, HuggingFace Papers)
  - Worker B: Tier1 Batch B (OneUsefulThing, Paul Graham)

等待结果 → 评估数量

如果 < 15 条高质量:
  第2波 (并行):
    - Worker C: Tier2 Batch A (James Clear, FS Blog)
    - Worker D: Tier2 Batch B (HackerNoon, Scott Young)

如果仍 < 20 条:
  第3波 (浏览器):
    - Browser Worker: ProductHunt, Latent Space (需要JS渲染)
```

### Phase 3: SubAgent 任务格式

每个 SubAgent 接收的任务格式：

```yaml
task: fetch_and_extract
sources:
  - id: hn
    url: https://news.ycombinator.com
    extract: top_10
  - id: hf_papers
    url: https://huggingface.co/papers
    extract: top_voted

output_schema:
  items:
    - source_id: string      # 来源标识
      title: string          # 标题
      summary: string        # 2-4句摘要
      key_points: string[]   # 最多3个要点
      url: string            # 原文链接
      keywords: string[]     # 关键词
      quality_score: 1-5     # 质量评分

constraints:
  filter: "前沿技术/高深技术/提效技术/实用资讯"
  exclude: "泛科普/营销软文/过度学术化/招聘帖"
  max_items_per_source: 10
  skip_on_error: true

return_format: JSON
```

### Phase 4: 主 Agent 监控与反馈

主 Agent 职责：

```yaml
监控:
  - 检查 SubAgent 返回状态 (success/partial/failed)
  - 统计收集到的条目数量
  - 记录每个源的成功率

反馈循环:
  - 如果某 SubAgent 失败，决定是否重试或跳过
  - 如果某源持续失败，标记为禁用
  - 动态调整后续批次的源选择

决策:
  - 条目数 >= 25 且高质量 >= 20 → 停止抓取
  - 条目数 < 15 → 继续下一批
  - 所有批次完成但 < 20 → 用现有内容生成（宁缺毋滥）
```

### Phase 5: 评估与筛选

```yaml
去重:
  - 基于 URL 完全匹配
  - 基于标题相似度 (>80% 视为重复)
  - 检查 cache.json 避免与历史重复

评分校准:
  - 统一各 SubAgent 的评分标准
  - 根据来源可信度调整权重
  - 手动标注的高质量源加分

排序:
  - 按 quality_score 降序
  - 同分按来源优先级排序
  - 截取 Top 20
```

### Phase 6: 浏览器抓取 (MCP Chrome DevTools)

对于需要 JS 渲染的页面，使用无头浏览器：

```yaml
流程:
  1. 调用 mcp__chrome-devtools__new_page 打开页面
  2. 调用 mcp__chrome-devtools__wait_for 等待内容加载
  3. 调用 mcp__chrome-devtools__take_snapshot 获取页面结构
  4. 解析 snapshot 提取所需内容
  5. 调用 mcp__chrome-devtools__close_page 关闭页面

适用场景:
  - ProductHunt (403 on WebFetch)
  - Latent Space (Substack JS 渲染)
  - 其他 SPA 应用
```

### Phase 7: 生成日报

```yaml
输出:
  - 目录: NewsReport/
  - 文件名: YYYY-MM-DD-news-report.md
  - 格式: 标准 Markdown

内容结构:
  - 标题 + 日期
  - 统计摘要（源数量、收录数量）
  - 20条高质量内容（按模板）
  - 生成信息（版本、时间戳）
```

### Phase 8: 更新缓存

```yaml
更新 cache.json:
  - last_run: 记录本次运行信息
  - source_stats: 更新各源统计数据
  - url_cache: 添加已处理的 URL
  - content_hashes: 添加内容指纹
  - article_history: 记录收录文章
```

## SubAgent 调用示例

### 使用 general-purpose Agent

由于自定义 agent 需要 session 重启才能发现，可以使用 general-purpose 并注入 worker prompt：

```
Task 调用:
  subagent_type: general-purpose
  model: haiku
  prompt: |
    你是一个无状态的执行单元。只做被分配的任务，返回结构化 JSON。

    任务：抓取以下 URL 并提取内容

    URLs:
    - https://news.ycombinator.com (提取 Top 10)
    - https://huggingface.co/papers (提取高投票论文)

    输出格式：
    {
      "status": "success" | "partial" | "failed",
      "data": [
        {
          "source_id": "hn",
          "title": "...",
          "summary": "...",
          "key_points": ["...", "...", "..."],
          "url": "...",
          "keywords": ["...", "..."],
          "quality_score": 4
        }
      ],
      "errors": [],
      "metadata": { "processed": 2, "failed": 0 }
    }

    筛选标准：
    - 保留：前沿技术/高深技术/提效技术/实用资讯
    - 排除：泛科普/营销软文/过度学术化/招聘帖

    直接返回 JSON，不要解释。
```

### 使用 worker Agent（需重启 session）

```
Task 调用:
  subagent_type: worker
  prompt: |
    task: fetch_and_extract
    input:
      urls:
        - https://news.ycombinator.com
        - https://huggingface.co/papers
    output_schema:
      - source_id: string
      - title: string
      - summary: string
      - key_points: string[]
      - url: string
      - keywords: string[]
      - quality_score: 1-5
    constraints:
      filter: 前沿技术/高深技术/提效技术/实用资讯
      exclude: 泛科普/营销软文/过度学术化
```

## 输出模板

```markdown
# Daily News Report（YYYY-MM-DD）

> 本日筛选自 N 个信息源，共收录 20 条高质量内容
> 生成耗时: X 分钟 | 版本: v3.0
>
> **Warning**: Sub-agent 'worker' not detected. Running in generic mode (Serial Execution). Performance might be degraded.
> **警告**：未检测到 Sub-agent 'worker'。正在以通用模式（串行执行）运行。性能可能会受影响。

---

## 1. 标题

- **摘要**：2-4 行概述
- **要点**：
  1. 要点一
  2. 要点二
  3. 要点三
- **来源**：[链接](URL)
- **关键词**：`keyword1` `keyword2` `keyword3`
- **评分**：⭐⭐⭐⭐⭐ (5/5)

---

## 2. 标题
...

---

*Generated by Daily News Report v3.0*
*Sources: HN, HuggingFace, OneUsefulThing, ...*
```

## 约束与原则

1. **宁缺毋滥**：低质量内容不进入日报
2. **早停机制**：够 20 条高质量就停止抓取
3. **并行优先**：同一批次的 SubAgent 并行执行
4. **失败容错**：单个源失败不影响整体流程
5. **缓存复用**：避免重复抓取相同内容
6. **主 Agent 控制**：所有决策由主 Agent 做出
7. **Fallback Awareness**：检测 sub-agent 可用性，不可用时优雅降级

## 预期性能

| 场景 | 预期时间 | 说明 |
|------|----------|------|
| 最优情况 | ~2 分钟 | Tier1 足够，无需浏览器 |
| 正常情况 | ~3-4 分钟 | 需要 Tier2 补充 |
| 需要浏览器 | ~5-6 分钟 | 包含 JS 渲染页面 |

## 错误处理

| 错误类型 | 处理方式 |
|----------|----------|
| SubAgent 超时 | 记录错误，继续下一个 |
| 源 403/404 | 标记禁用，更新 sources.json |
| 内容提取失败 | 返回原始内容，主 Agent 决定 |
| 浏览器崩溃 | 跳过该源，记录日志 |

## 兼容性与兜底 (Compatibility & Fallback)

为了确保在不同 Agent 环境下的可用性，必须执行以下检查：

1.  **环境检查**:
    -   在 Phase 1 初始化阶段，尝试检测 `worker` sub-agent 是否存在。
    -   如果不存在（或未安装相关插件），自动切换到 **串行执行模式 (Serial Mode)**。

2.  **串行执行模式**:
    -   不使用 parallel block。
    -   主 Agent 依次执行每个源的抓取任务。
    -   虽然速度较慢，但保证基本功能可用。

3.  **用户提示**:
    -   必须在生成的日报开头（引用块部分）包含明显的警告信息，提示用户当前正在运行于降级模式。
