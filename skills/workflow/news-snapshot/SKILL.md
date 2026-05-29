---
name: news-snapshot
description: Retrieve and summarize current international and Singapore news stories with headlines, brief context, and source links in a professional executive format. Use when you need a quick daily news briefing with verified sources.
---

# News Snapshot Skill

Retrieve top international and Singapore news stories for quick daily briefings.

## Overview

This skill provides a concise, scannable news summary with:
- **2 international news stories** with headline, 1-sentence context, and source link
- **2 Singapore-specific news stories** with headline, 1-sentence context, and source link
- **Professional format** optimized for executive reading

## When to Use

Use this skill when you need:
- A quick daily news briefing
- Current events context
- International and regional perspective
- A structured news snapshot for morning briefs or status updates

## Workflow

### Step 1: Search for Current News

Use web_search to find recent stories:
1. **International headlines**: Search for top news from major sources (Reuters, AP, BBC, Bloomberg)
2. **Singapore headlines**: Search for top Singapore news from CNA, Straits Times, TODAY

Suggested search queries:
- `"international news today"` or `"world news latest"`
- `"Singapore news today"` or `"latest Singapore headlines"`

### Step 2: Extract and Verify Information

For each story, gather these elements:
- **Headline**: Clear, concise story title (keep under 12 words)
- **Context**: 1-2 sentences maximum explaining the story's significance and why it matters
- **Source**: News organization name
- **URL**: Direct link to the full article

Selection criteria:
- Published within the last 24 hours (or most recent available)
- High-credibility sources (established news organizations)
- Stories with meaningful relevance or impact
- Mix of different topics for variety

### Step 3: Format as Executive Summary

Produce output in this professional format:
```markdown
# News Snapshot

*Generated: [Day, Month Date, Year at Time]*

## 🌍 International News

### 1. [Headline]
[1-2 sentence context explaining the story's significance.]

*Source: [Organization](URL)*

### 2. [Headline]
[1-2 sentence context explaining the story's significance.]

*Source: [Organization](URL)*

## 🇸🇬 Singapore News

### 1. [Headline]
[1-2 sentence context explaining the story's significance.]

*Source: [Organization](URL)*

### 2. [Headline]
[1-2 sentence context explaining the story's significance.]

*Source: [Organization](URL)*
```

## Best Practices

- **Keep context concise**: Maximum 1-2 sentences; focus on why the story matters, not every detail
- **Include direct links**: Always provide clickable source URLs for easy reference
- **Prioritize recency**: Prefer stories from today or yesterday; fall back to recent trending stories if nothing fresh available
- **Verify credibility**: Use established, reputable news sources only (avoid blogs, opinion pieces, or unknown sources)
- **Stick to facts**: Report what happened; avoid commentary or speculation
- **Balance coverage**: Include mix of business, politics, technology, and human interest stories
- **Use consistent formatting**: Maintain the structure above for easy scanning

## Automated Integration

The `scripts/fetch_news.py` script provides a template structure for integrating real news APIs. To activate:

1. Subscribe to a news API (NewsAPI.org, mediastack, Ezoic, etc.)
2. Update the `fetch_international_news()` and `fetch_singapore_news()` functions with actual API calls
3. Parse JSON responses to extract headlines, context, and URLs
4. Execute the script on a schedule (cron job, Lambda function, etc.)

## Tips for Quality Output

- If recent news is limited, include 1-2 day old stories rather than forcing outdated content
- Always verify URLs work before including them
- For Singapore news, prioritize CNA, Straits Times, and TODAY as primary sources
- For international news, Reuters, AP, and Bloomberg are most authoritative