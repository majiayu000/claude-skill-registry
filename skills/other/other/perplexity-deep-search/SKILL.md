---
name: perplexity-deep-search
version: 1.0.0
description: Deep research using Perplexity AI. Comprehensive reports with citations and analysis.
metadata:
  openclaw:
    emoji: 🔍
    category: research
---

# Perplexity Deep Search

Deep research using Perplexity AI. Comprehensive reports with citations and analysis.

## When to Use

| Use Case | Example |
|----------|---------|
| **Market research** | "Competitive analysis of AI coding assistants" |
| **Technology evaluation** | "Compare vector databases for production use" |
| **Trend analysis** | "State of MCP ecosystem 2025" |
| **Due diligence** | "Company X funding, team, product overview" |
| **Learning** | "Explain quantum computing to a programmer" |

## vs Other Research Tools

| Tool | Best For | Depth |
|------|----------|-------|
| **Perplexity** | Quick, cited answers | Medium |
| **Pokee Deep Research** | Comprehensive reports | Deep (25+ min) |
| **Web Search** | Specific facts | Shallow |
| **arXiv Watcher** | Academic papers | Deep |

## Workflow

### 1. Targeted Query

Be specific:

```
"Compare Supabase vs Firebase for real-time apps in 2025. 
Focus on: scalability, pricing, self-hosting options."
```

### 2. Follow-Up Questions

Drill deeper:

```
"What are the specific limitations of Firebase's real-time 
sync at 10k+ concurrent users?"
```

### 3. Synthesis

Combine multiple sources:

```
"Based on the above, which is better for a startup with 
< 1000 users planning to scale to 100k?"
```

## Output Format

Request structured output:

```markdown
## Summary
2-3 sentence overview

## Key Findings
- Point 1 (with citation)
- Point 2 (with citation)

## Comparison Table
| Criteria | Option A | Option B |
|----------|----------|----------|

## Recommendations
1. Best for X
2. Best for Y

## Sources
- [Title](URL)
```

## Automation

```json
{
  "name": "weekly-tech-digest",
  "schedule": {"kind": "cron", "expr": "0 9 * * 1"},
  "payload": {
    "kind": "agentTurn",
    "message": "Use perplexity to research: 'AI agent frameworks 2025'. Focus on new releases, emerging standards, key players."
  },
  "sessionTarget": "isolated",
  "notify": true
}
```

## Best Practices

1. **Be specific** — Narrow queries get better results
2. **Request citations** — Verify claims
3. **Follow up** — One query rarely tells the full story
4. **Save findings** — Add to MEMORY.md for future reference
5. **Cross-check** — Confirm critical facts with primary sources
