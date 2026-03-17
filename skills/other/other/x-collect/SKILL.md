---
name: x-collect
description: Collect and research materials for X (Twitter) content creation using multi-round web search strategy. Use when user wants to gather trending topics, research subjects for X posts, or mentions "collect materials", "research topic", "find content for X", "x-collect". Performs 4-round deep research mimicking human research workflow.
---

# X Collect

Collect trending topics and research materials for X content creation using a systematic 4-round web search strategy.

## Prerequisites

- WebSearch tool available
- Internet connection

## Workflow

### Input

User provides:
- **Topic** (required): The subject to research (e.g., "AI Agent最新进展", "Claude 4 发布")
- **Language** (optional): Output language, defaults to Chinese (zh-CN)

### 4-Round Search Strategy

Simulate human research thinking process with progressive depth:

**Round 1: Official Sources (权威信息)**
```
Search: "{topic} 官方文档"
Search: "{topic} GitHub"
Search: "{topic} official announcement"
```
Goal: Get authoritative first-hand information

**Round 2: Technical Analysis (技术解析)**
```
Search: "{topic} 详细介绍"
Search: "{topic} 教程 tutorial"
Search: "{topic} how it works"
```
Goal: Understand technical details and mechanisms

**Round 3: Comparison & Reviews (对比评测)**
```
Search: "{topic} vs {competitor}"
Search: "{topic} 评测 review"
Search: "{topic} pros cons"
```
Goal: Get different perspectives and comparisons

**Round 4: Supplementary Verification (补充验证)**
```
# Analyze gaps from previous rounds
missing_info = analyze_gaps(previous_results)
Search: "{missing_info}"
Search: "{topic} 最新 latest 2024 2025"
```
Goal: Fill information gaps and get latest updates

### Output Format

Generate structured material document:

```markdown
# {Topic} 素材收集报告

## 收集时间
{timestamp}

## 核心信息
- **官方定义**: ...
- **关键特性**: ...
- **最新动态**: ...

## 素材列表

### 素材 1
- **标题**: ...
- **来源**: {url}
- **摘要**: 2-3句话概括
- **关键点**:
  - 要点1
  - 要点2
- **潜在选题角度**: ...
- **推荐推文类型**: [高价值干货/犀利观点/热点评论/故事洞察/技术解析]

### 素材 2
...

## 热度分析
- **当前热度**: 高/中/低
- **趋势**: 上升/稳定/下降
- **讨论焦点**: ...

## 争议点
- 争议1: ...
- 争议2: ...

## 下一步建议
使用 `/x-filter` 对素材进行打分筛选
```

## Execution Steps

1. **Receive topic** from user
2. **Execute Round 1** searches (official sources)
3. **Execute Round 2** searches (technical analysis)
4. **Execute Round 3** searches (comparisons)
5. **Analyze gaps** from rounds 1-3
6. **Execute Round 4** searches (fill gaps)
7. **Synthesize results** into structured format
8. **Save to temp file** for x-filter to use
9. **Report summary** to user

## Example

User: `/x-collect Claude MCP协议`

Expected behavior:
1. Search "Claude MCP协议 官方文档"
2. Search "MCP Model Context Protocol GitHub"
3. Search "MCP协议 详细介绍"
4. Search "MCP协议 教程"
5. Search "MCP vs function calling"
6. Search "MCP协议 评测"
7. Identify gaps: need more about security, adoption rate
8. Search "MCP协议 安全性"
9. Search "MCP协议 最新 2025"
10. Generate structured material report

## Integration

After collection, suggest:
```
素材收集完成！共找到 X 条相关素材。

下一步：运行 /x-filter 对素材进行打分筛选，≥7分的选题将进入创作池。
```

## Tips

- For trending topics, prioritize recency (2024-2025)
- For technical topics, prioritize official docs and GitHub
- For controversial topics, collect multiple perspectives
- Always note the source URL for credibility
