---
name: feed-reader
description: Aggregate news and social feeds to stay informed
user_invocable: true
---

# Feed Reader Skill

## Purpose
Consume content from various sources to stay informed about:
- Tech news and developments
- AI/ML updates
- Market movements
- Social media trends
- Internet culture

## Invocation
```
/feed-reader [source] [options]
```

### Arguments
- `source` (optional): Specific source to check (hn, techcrunch, x, all)
- `--summary`: Get condensed summary instead of full details
- `--since [time]`: Only show items since specified time

### Examples
```
/feed-reader              # Check all sources
/feed-reader hn           # Just Hacker News
/feed-reader --summary    # Quick overview
```

## Sources

### News Sites
| Source | Priority | Type |
|--------|----------|------|
| Hacker News | High | Tech/Startup |
| TechCrunch | Medium | Tech News |
| The Verge | Medium | Tech/Culture |
| Ars Technica | Low | Deep Tech |

### Social
| Source | Priority | Type |
|--------|----------|------|
| X Timeline | High | Real-time |
| Moltbook Feed | High | Community |

### Markets
| Source | Priority | Type |
|--------|----------|------|
| CoinGecko | Medium | Crypto |
| Yahoo Finance | Low | Stocks |

## Workflow

1. **Fetch** content from configured sources
2. **Filter** for relevance and quality
3. **Summarize** key items
4. **Identify** posting opportunities
5. **Update** `memory/context.md` with findings

## Output

Returns structured summary:
```markdown
## Feed Summary - [DATE]

### Top Stories
- [Story 1 with brief summary]
- [Story 2 with brief summary]

### Trending Topics
- [Topic 1]
- [Topic 2]

### Posting Opportunities
- [Potential content angle 1]
- [Potential content angle 2]

### Market Moves
- [Notable movement if any]
```

## Implementation Notes

Uses web search and fetch capabilities to:
- Scrape HN front page
- Check news site RSS/homepages
- Monitor X trends
- Track market data

Stores findings in `memory/context.md` for reference.
