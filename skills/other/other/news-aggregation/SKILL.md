---
name: news-aggregation
description: Aggregate and deduplicate recent news from multiple sources into concise topic summaries.
---

# News Aggregation (Multi-Source, 3-Day Window)

Collect latest news from multiple sites and aggregators, merge similar stories into short topics, and list all main source links under each topic.

## When to use
- You want one concise briefing from many outlets.
- You need deduplicated coverage (same story from multiple sites).
- You want source transparency (all original links shown).
- You want a default time window of the last 3 days unless specified otherwise.

## Required tools / APIs
- No API keys required for basic RSS workflow.
- Python 3.10+

Install:

```bash
pip install feedparser python-dateutil
```

## Sources (news sites + aggregators)

Use a mixed source list for better coverage.

### News sites (RSS)
- Reuters World: `https://feeds.reuters.com/Reuters/worldNews`
- AP Top News: `https://feeds.apnews.com/apnews/topnews`
- BBC World: `http://feeds.bbci.co.uk/news/world/rss.xml`
- Al Jazeera: `https://www.aljazeera.com/xml/rss/all.xml`
- The Guardian World: `https://www.theguardian.com/world/rss`
- NPR News: `https://feeds.npr.org/1001/rss.xml`

### Aggregators (RSS/API)
- Google News (topic feed): `https://news.google.com/rss/search?q=world`
- Bing News (RSS query): `https://www.bing.com/news/search?q=world&format=RSS`
- Hacker News (tech): `https://hnrss.org/frontpage`
- Reddit News (community signal): `https://www.reddit.com/r/news/.rss`

## Skills

### Node.js quick fetch + grouping starter

```javascript
// npm install rss-parser
const Parser = require('rss-parser');
const parser = new Parser();

const SOURCES = {
  Reuters: 'https://feeds.reuters.com/Reuters/worldNews',
  AP: 'https://feeds.apnews.com/apnews/topnews',
  BBC: 'http://feeds.bbci.co.uk/news/world/rss.xml',
  'Google News': 'https://news.google.com/rss/search?q=world'
};

async function fetchRecent(days = 3) {
  const cutoff = Date.now() - days * 24 * 60 * 60 * 1000;
  const all = [];

  for (const [source, url] of Object.entries(SOURCES)) {
    const feed = await parser.parseURL(url);
    for (const item of feed.items || []) {
      const ts = new Date(item.pubDate || item.isoDate || 0).getTime();
      if (!ts || ts < cutoff) continue;
      all.push({ source, title: item.title || '', link: item.link || '', ts });
    }
  }

  return all.sort((a, b) => b.ts - a.ts);
}

// Next step: add title-similarity clustering (same idea as Python section above)
```

## Agent prompt

```text
Use the News Aggregation skill.

Requirements:
1) Pull news from multiple predefined sources (news sites + aggregators).
2) Default to only the last 3 days unless user asks another time range.
3) Group similar headlines into one short topic.
4) Under each topic, list all main source links (not just one source).
5) If 3+ sources cover the same event, output one topic with all those links.
6) Keep summaries short and factual; avoid adding unsupported claims.
```

## Best practices
- Keep source diversity (wire + publisher + aggregator) to reduce bias.
- Rank grouped topics by number of independent sources.
- Include publication timestamps when possible.
- Keep the grouping threshold conservative to avoid merging unrelated stories.
- Allow custom source lists and time windows when user requests.

## Troubleshooting
- Empty results: some feeds may be unavailable; retry and rotate sources.
- Too many duplicates: increase similarity threshold (e.g., 0.35 -> 0.45).
- Under-grouping: decrease threshold (e.g., 0.35 -> 0.28).
- Rate limiting: fetch feeds sequentially with small delays.

## See also
- [Web Search API (Free)](./web-search-api.md)
- [Web Scraping (Chrome + DuckDuckGo)](./using-web-scraping.md)