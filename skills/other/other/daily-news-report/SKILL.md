---
name: daily-news-report
description: Automated news aggregation and reporting agent.
category: automation
version: 4.1.0-fractal
layer: master-skill
---

# Daily News Report Agent

> **Goal**: Generate high-quality, curated news digests from various internet sources (RSS, APIs, Search).

## 1. Information Gathering

- **Sources**:
    - **RSS Feeds**: TechCrunch, Hacker News, Verges, specialized industry blogs.
    - **APIs**: NewsAPI, GNews, Reddit API.
    - **Direct Scrape**: Use with caution and respect `robots.txt` (using `firecrawl-scraper`).
- **Filtering**:
    - Keywords: Filter by relevant topics (e.g., "AI", "Rust", "Global Economy").
    - Recency: Only fetch items < 24h.
    - Popularity: Filter by score/upvotes/comments if available (e.g., HN > 100 points).

## 2. Processing Pipeline

1.  **Deduplication**: Use similarity check (Title/Content embeddings) to group same stories from different sources.
2.  **Summarization**: Use LLM to summarize content into 3-5 bullet points. Focus on "Why it matters".
3.  **Classification**: Tag articles with categories (Tech, Business, Politics, Science).

## 3. Reporting Output

- **Format**: Markdown, HTML email, or Slack/Discord payload.
- **Structure**:
    - **Headline**: Catchy but accurate.
    - **TL;DR**: 1 sentence summary.
    - **Key Points**: Bulleted list.
    - **Source Link**: Direct link to original article.
    - **Sentiment**: Neutral/Positive/Negative tag (optional).

## 4. Scheduled Automation

- **Trigger**: Cron job (e.g., every morning at 8:00 AM).
- **Environment**: GitHub Actions (Scheduled workflow) or a persistent background worker (Node.js/Python).

## 5. Example Workflow (GitHub Action)

```yaml
name: Daily News
on:
  schedule:
    - cron: '0 8 * * *'
jobs:
  report:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run News Agent
        run: npx antigravity-ide run-skill daily-news-report
        env:
            NEWS_API_KEY: ${{ secrets.NEWS_API_KEY }}
            LLM_API_KEY: ${{ secrets.GEMINI_API_KEY }}
```

---

**Prompt Strategy for Summarization**:
> "You are a professional news editor. Summarize the following text for a technical audience. Focus on facts, release numbers, and technical implications. Remove fluff."
