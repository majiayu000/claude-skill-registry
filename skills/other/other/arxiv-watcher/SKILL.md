---
name: arxiv-watcher
version: 1.0.0
description: Monitor arXiv for new papers in specific fields. Get alerts for relevant research.
metadata:
  openclaw:
    emoji: 📄
    category: research
---

# arXiv Watcher

Monitor arXiv for new papers in specific fields. Get alerts for relevant research.

## Search Queries

### CS/AI Topics

| Query | Description |
|-------|-------------|
| `cat:cs.AI` | Artificial Intelligence |
| `cat:cs.LG` | Machine Learning |
| `cat:cs.CL` | Computation and Language (NLP) |
| `cat:cs.CV` | Computer Vision |
| `cat:cs.RO` | Robotics |
| `cat:cs.SE` | Software Engineering |

### Combined Queries

```
cat:cs.AI OR cat:cs.LG OR cat:cs.CL
```

## Workflow

### 1. One-Time Search

Use `web_search` with arXiv queries:

```
Search arXiv for recent papers on:
- "multimodal AI" site:arxiv.org
- "agent orchestration" site:arxiv.org
```

### 2. RSS Feed Monitoring

arXiv provides RSS feeds:

```
http://export.arxiv.org/rss/cs.AI
http://export.arxiv.org/rss/cs.LG
http://export.arxiv.org/rss/cs.CL
```

Use with `blogwatcher` skill for automated monitoring.

### 3. Scheduled Digest

```json
{
  "name": "arxiv-weekly-digest",
  "schedule": {"kind": "cron", "expr": "0 9 * * 1"},
  "payload": {
    "kind": "agentTurn",
    "message": "Search arXiv for: 'agent orchestration', 'MCP servers', 'autonomous agents'. Summarize top 5 papers."
  },
  "sessionTarget": "isolated",
  "notify": true
}
```

## Paper Analysis Template

When reviewing a paper:

```markdown
## Title
**Authors:** 
**arXiv ID:** 
**Date:** 

**TL;DR:** One sentence summary

**Key Contribution:**
- Point 1
- Point 2

**Relevance to My Work:**
- How this applies
- Action items

**Code/Data:** Links if available
```

## Best Practices

1. **Focus on recent** — Last 6 months for fast-moving fields
2. **Track authors** — Follow key researchers
3. **Read abstracts first** — Don't download everything
4. **Build a reading list** — Queue papers in `tasks/reading-list.md`
5. **Summarize for others** — Share insights in MEMORY.md
