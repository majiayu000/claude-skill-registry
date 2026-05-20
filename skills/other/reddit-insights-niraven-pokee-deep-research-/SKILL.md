---
name: reddit-insights
version: 1.0.0
description: Extract insights from Reddit discussions. Track communities, sentiment, and trends.
metadata:
  openclaw:
    emoji: 🔴
    category: research
---

# Reddit Insights

Extract insights from Reddit discussions. Track communities, sentiment, and trends.

## Key Subreddits for Tech/AI

| Subreddit | Focus |
|-----------|-------|
| r/MachineLearning | ML research, papers |
| r/LocalLLaMA | Local AI, open models |
| r/OpenAI | OpenAI products, API |
| r/ClaudeAI | Anthropic, Claude |
| r/selfhosted | Self-hosting, homelab |
| r/docker | Containers, DevOps |
| r/programming | General development |
| r/webdev | Web development |
| r/startups | Startup ecosystem |
| r/ExperiencedDevs | Senior perspectives |

## Workflow

### 1. Topic Search

Use `web_search`:

```
Search Reddit for:
- "OpenClaw OR 'Open Claw'" site:reddit.com
- "MCP server" site:reddit.com
- "self-hosted AI" site:reddit.com
```

### 2. Community Monitoring

Track specific threads:

```
Monitor r/LocalLLaMA for:
- New model releases
- Performance benchmarks
- Quantization techniques
```

### 3. Sentiment Analysis

Look for patterns:

| Signal | What to Track |
|--------|---------------|
| **Frustration** | Pain points, complaints |
| **Excitement** | New releases, features |
| **Confusion** | Documentation gaps |
| **Requests** | Feature requests |

## Insight Extraction

### Template

```markdown
## r/Subreddit - Topic

**Thread:** [Title](URL)
**Posted:** Date
**Engagement:** Upvotes, comments

**Key Insights:**
1. Main point
2. Counter-argument
3. Consensus

**Quotes:**
> "Important quote" — u/username

**Action Items:**
- [ ] Follow up on X
- [ ] Add to research queue
```

## Automated Monitoring

```json
{
  "name": "reddit-weekly-scan",
  "schedule": {"kind": "cron", "expr": "0 10 * * 1"},
  "payload": {
    "kind": "agentTurn",
    "message": "Search Reddit for: 'Claude', 'OpenClaw', 'MCP servers', 'autonomous agents'. Find 3 high-engagement threads. Extract insights."
  },
  "sessionTarget": "isolated"
}
```

## Best Practices

1. **Verify claims** — Reddit is opinion-heavy
2. **Check post dates** — Old info may be stale
3. **Read comments** — Often more valuable than posts
4. **Track OP credibility** — Check post history
5. **Cross-reference** — Confirm with primary sources
