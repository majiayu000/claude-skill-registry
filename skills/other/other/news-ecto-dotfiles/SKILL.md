---
name: news
description: Poll favorite RSS feeds including Hacker News and Lobsters. Fetches latest tech headlines and provides a summary of current news. Use when you want to catch up on tech news or see what's trending.
allowed-tools: WebFetch
---

# News

Fetches and summarizes the latest headlines from your favorite RSS feeds.

## Usage

- `/news` - Fetch all feeds and show top stories
- `/news hn` or `/news hackernews` - Hacker News only
- `/news lobsters` - Lobsters only

## Feeds

> **Note:** WebFetch has restrictions on many mainstream news domains (CNN, NYT, Reddit, etc.).
> The feeds below are confirmed to work.

### Hacker News
- **URL:** https://news.ycombinator.com/rss
- **Focus:** Tech, startups, programming, science

### Lobsters
- **URL:** https://lobste.rs/rss
- **Focus:** Programming, technology, computing (more curated than HN)

## Workflow

1. **Fetch feeds** using WebFetch for each RSS URL
2. **Parse** the XML to extract titles, links, and descriptions
3. **Summarize** the top 10 stories from each feed
4. **Present** in a clean, scannable format

## Output Format

Present news in this format:

```
## Hacker News
1. **[Title]**
   [link]

2. **[Title]**
   [link]

## Lobsters
1. **[Title]**
   [link]
```

## Instructions

When `/news` is invoked:

1. Fetch all configured RSS feeds in parallel using WebFetch
2. For each feed, extract the top 10 items
3. Present stories grouped by source
4. Highlight any particularly notable/trending stories

When a specific source is requested (e.g., `/news hn`):
- Only fetch that source's feed(s)
- Show up to 15 items instead of 10

## Adding New Feeds

To add a new feed, the user can ask to update this skill with:
- Feed name
- RSS URL
- Category (tech, news, general, etc.)

**Note:** Test new feeds first - WebFetch blocks many news domains.
