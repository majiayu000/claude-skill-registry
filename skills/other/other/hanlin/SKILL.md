---
name: hanlin
description: 联网查证 Claude Code 官方文档、GitHub Issues、Changelog，确认 API 或功能的最新状态并评估对架构的影响
---

# Skill: 翰林院

> **适用 Agent**：太子（Lead）
> **加载时机**：太子自主查证，或三省通过 SendMessage 请求太子代为查证时

## 功能

充当系统的"知识顾问"，通过联网搜索确认 Claude Code 的最新能力状态，避免基于过时信息做出错误架构决策。

## 调用方式

| 调用方 | 流程 |
|--------|------|
| 太子 | 直接加载 Skill 执行查证 |
| 三省 | SendMessage 向太子提出查证请求（附具体问题）→ 太子执行查证 → 太子将结果回传请求方 |

三省不得直接使用 WebSearch/WebFetch 工具，须经太子中转。

## 查证流程

### 第一步：明确查证问题

调用方须明确要查证的具体问题，例如：
- "Agent tool 是否支持 Teammate 调用？"
- "TaskCreate 是否支持自定义 metadata 字段？"
- "最新版本是否修复了 Teammate 存活检测问题？"

### 第二步：多源搜索

太子使用 WebSearch / WebFetch 工具，按优先级搜索以下来源：

| 优先级 | 来源 | 搜索方式 |
|--------|------|---------|
| 1 | Claude Code 官方文档 | WebSearch: `site:docs.anthropic.com claude code {关键词}` |
| 2 | GitHub Issues | WebSearch: `site:github.com/anthropics/claude-code issues {关键词}` |
| 3 | GitHub Changelog/Releases | WebFetch: `https://github.com/anthropics/claude-code/releases` |
| 4 | 社区讨论 | WebSearch: `claude code {关键词} site:github.com OR site:stackoverflow.com` |

### 第三步：输出查证报告

```json
{
  "type": "hanlin_report",
  "query": "查证的具体问题",
  "verdict": "confirmed | denied | uncertain | deprecated",
  "summary": "一段话结论",
  "sources": [
    { "title": "来源标题", "url": "...", "relevance": "摘要" }
  ],
  "impact_assessment": "对当前三省六部架构的影响评估（无影响/需调整/需重新设计）",
  "recommendations": "建议的后续行动"
}
```

### verdict 含义

| verdict | 含义 |
|---------|------|
| confirmed | 官方确认支持/存在 |
| denied | 官方确认不支持/不存在 |
| uncertain | 无明确官方说明，需谨慎处理 |
| deprecated | 曾支持但已废弃或计划废弃 |

## 约束

1. 必须附带来源链接，不得凭记忆断言
2. 查证结果为 uncertain 时，须建议保守方案
3. 不替代决策——翰林只提供信息，决策权在调用方
4. 影响评估须具体到受影响的模块/流程，不得泛泛而谈
5. 三省不得直接执行联网查证，须经太子中转（遵守"三省不做执行"纪律）
