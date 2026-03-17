---
name: research-by-reddit
description: 基于 Reddit API 进行深度调研并生成研究报告。支持搜索、获取帖子、评论分析、情感分析等功能
allowed-tools:
  - Bash(python:*)
  - Read
  - Write
model: sonnet
---

# Reddit 深度调研技能

基于 Reddit API (PRAW) 进行市场调研、用户反馈收集、技术方案研究等任务。

## 环境配置

需要设置以下环境变量（在 `.env` 文件中）：

```bash
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=your_app_name/1.0
OPENROUTER_API_KEY=your_openrouter_key  # 用于 AI 分析
```

## 核心脚本

### 1. search_reddit.py - Reddit 搜索

搜索 Reddit 全站或特定 subreddit 的内容。

```bash
python scripts/search_reddit.py --query "关键词" [选项]
```

**参数：**
- `--query`: 搜索关键词（必需）
- `--subreddit`: 限定搜索的 subreddit（可选，不指定则全站搜索）
- `--limit`: 返回结果数量（默认 25，最大 100）
- `--time_filter`: 时间范围 [all, year, month, week, day, hour]（默认 all）
- `--sort`: 排序方式 [relevance, hot, top, new, comments]（默认 relevance）
- `--output`: 输出文件路径（可选，默认输出到 stdout）

**示例：**
```bash
# 搜索 AI 相关讨论
python scripts/search_reddit.py --query "AI productivity tools" --limit 50 --time_filter month

# 在特定 subreddit 搜索
python scripts/search_reddit.py --query "团建" --subreddit "China_irl" --limit 30
```

### 2. fetch_posts.py - 获取 Subreddit 帖子

获取指定 subreddit 的热门/最新帖子及评论。

```bash
python scripts/fetch_posts.py --subreddit "subreddit名称" [选项]
```

**参数：**
- `--subreddit`: 目标 subreddit（必需）
- `--sort`: 排序方式 [hot, new, top, rising, controversial]（默认 hot）
- `--limit`: 帖子数量（默认 25）
- `--time_filter`: 时间范围，仅对 top/controversial 有效（默认 week）
- `--include_comments`: 是否包含评论（默认 false）
- `--comment_limit`: 每个帖子的评论数量（默认 10）
- `--output`: 输出文件路径

**示例：**
```bash
# 获取 startup subreddit 热门帖子
python scripts/fetch_posts.py --subreddit "startups" --sort hot --limit 20

# 获取帖子及评论
python scripts/fetch_posts.py --subreddit "smallbusiness" --include_comments --comment_limit 20
```

### 3. analyze_reddit.py - 深度分析

对收集的 Reddit 数据进行 AI 分析，生成研究报告。

```bash
python scripts/analyze_reddit.py --input "数据文件" --analysis_type "分析类型" [选项]
```

**参数：**
- `--input`: 输入数据文件（JSON 格式，来自 search 或 fetch）
- `--analysis_type`: 分析类型 [sentiment, topic, summary, competitive, pain_points]
- `--model`: AI 模型（默认 gemini，可选 claude, gpt-4）
- `--output`: 输出报告路径
- `--format`: 输出格式 [json, markdown]（默认 markdown）

**分析类型说明：**
- `sentiment`: 情感分析，识别正面/负面/中性观点
- `topic`: 主题聚类，识别讨论热点
- `summary`: 内容摘要，提取关键信息
- `competitive`: 竞品分析，识别提及的竞品及评价
- `pain_points`: 痛点分析，识别用户抱怨和需求

**示例：**
```bash
# 情感分析
python scripts/analyze_reddit.py --input data/search_results.json --analysis_type sentiment

# 生成 Markdown 报告
python scripts/analyze_reddit.py --input data/posts.json --analysis_type pain_points --format markdown --output reports/pain_points.md
```

## 调研工作流

### 典型调研流程

1. **定义调研目标**
   - 明确要研究的问题
   - 确定目标 subreddit 列表
   - 设定时间范围和样本量

2. **数据收集**
   ```bash
   # 1. 搜索相关讨论
   python scripts/search_reddit.py --query "your topic" --limit 100 --output data/search.json

   # 2. 获取热门帖子
   python scripts/fetch_posts.py --subreddit "relevant_sub" --include_comments --output data/posts.json
   ```

3. **数据分析**
   ```bash
   # 3. 运行 AI 分析
   python scripts/analyze_reddit.py --input data/search.json --analysis_type pain_points --output reports/analysis.md
   ```

4. **报告生成**
   - 整合多个分析结果
   - 添加结论和建议
   - 输出最终报告

### 常用调研场景

#### 场景1：市场调研
```bash
# 了解目标用户对某类产品的看法
python scripts/search_reddit.py --query "team building software" --limit 100 --time_filter year
python scripts/analyze_reddit.py --input results.json --analysis_type competitive
```

#### 场景2：用户反馈收集
```bash
# 收集特定产品的用户反馈
python scripts/search_reddit.py --query "Notion alternative" --subreddit "productivity" --limit 50
python scripts/analyze_reddit.py --input results.json --analysis_type pain_points
```

#### 场景3：技术方案调研
```bash
# 了解技术选型讨论
python scripts/fetch_posts.py --subreddit "programming" --sort top --time_filter month --include_comments
python scripts/analyze_reddit.py --input posts.json --analysis_type topic
```

## 输出格式

### JSON 格式（结构化数据）
```json
{
  "query": "搜索词",
  "timestamp": "2024-01-15T10:30:00Z",
  "total_results": 50,
  "results": [
    {
      "id": "post_id",
      "title": "帖子标题",
      "author": "用户名",
      "subreddit": "subreddit名",
      "score": 1234,
      "num_comments": 56,
      "created_utc": 1705312200,
      "url": "https://reddit.com/...",
      "selftext": "帖子内容...",
      "comments": [...]
    }
  ]
}
```

### Markdown 格式（可读报告）
```markdown
# Reddit 调研报告：[主题]

## 概述
- 数据来源：[subreddit 列表]
- 时间范围：[开始] - [结束]
- 样本量：[N] 条帖子

## 关键发现
1. ...
2. ...

## 详细分析
### 主题分布
...

### 情感倾向
...

## 结论与建议
...
```

## 注意事项

1. **API 限制**：Reddit API 有速率限制（约 60 请求/分钟），大量数据收集需分批进行
2. **数据隐私**：不要收集或存储用户个人信息
3. **内容版权**：引用 Reddit 内容时注明来源
4. **合规使用**：遵守 Reddit API 使用条款

## 依赖安装

```bash
cd .claude/skills/research-by-reddit/scripts
pip install -r requirements.txt
```

## 故障排除

### 常见问题

1. **认证失败**
   - 检查 REDDIT_CLIENT_ID 和 REDDIT_CLIENT_SECRET 是否正确
   - 确保 Reddit 应用类型为 "script"

2. **搜索结果为空**
   - 尝试放宽时间范围
   - 检查关键词拼写
   - 尝试不同的 subreddit

3. **AI 分析失败**
   - 检查 OPENROUTER_API_KEY 是否有效
   - 确保输入文件格式正确
