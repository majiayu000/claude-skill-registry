---
name: fetch-rss-feeds
version: "2.0.0"
description: >
  Fetch articles from RSS/Atom feeds and store them in memory for analysis.
  Uses the rss tool for fetching and memory MCP for storage and deduplication.
license: MIT
allowed-tools:
  - rss                    # Strands built-in RSS tool
  - memory/add             # Store fetched articles
  - memory/check_seen      # Check if article already processed
  - memory/mark_seen       # Mark article as processed
metadata:
  kubani:
    domain: news
    category: collection
    requires_approval: false
    confidence: 0.95
    version: "2.0.0"
---

# Fetch RSS Feeds

Fetch and store articles from RSS/Atom feeds with deduplication.

## When to Use

Use this skill when you need to:
- Collect articles from RSS or Atom feeds
- Store articles in memory for later analysis
- Avoid processing duplicate articles

## Instructions

### Step 1: Check for Duplicates Before Fetching

Before fetching each feed, prepare to deduplicate articles:
- Use `memory/check_seen` with the article URL as the key
- Namespace: `news/articles`

### Step 2: Fetch RSS Feeds

Use the `rss` tool to fetch articles from configured feeds.

**Feed sources to fetch:**
- Company blogs (OpenAI, Anthropic, Google DeepMind, etc.)
- AI-focused tech news (TechCrunch AI, VentureBeat AI, The Verge AI)
- Research feeds (arXiv, Papers with Code)

**For each feed:**
1. Call the `rss` tool with the feed URL
2. Extract: title, url, published_date, summary, author

### Step 3: Filter and Deduplicate

For each article from the feed:

1. **Check if already seen:**
   - Call `memory/check_seen` with key=URL hash, namespace="news/articles"
   - If seen=true, skip this article

2. **Validate required fields:**
   - Article must have: title, url
   - Skip articles missing required fields

3. **Filter by age (optional):**
   - If max_age_hours is specified, skip articles older than threshold

### Step 4: Store New Articles

For each new (unseen) article:

1. **Store in memory:**
   - Call `memory/add` with:
     - type: "document"
     - namespace: "news/articles"
     - data: {title, url, summary, author, source, published_at}
     - metadata: {fetched_at, source_feed}

2. **Mark as seen:**
   - Call `memory/mark_seen` with:
     - key: URL hash
     - namespace: "news/articles"
     - ttl_seconds: 1209600 (14 days)

### Step 5: Return Results

Return a summary including:
- Number of articles stored
- Number of duplicates skipped
- Number of feeds processed
- Any failed feeds

## Tool Usage Guidance

### rss tool
- Use to fetch feed content
- Handles XML parsing and date extraction
- Returns list of entries with title, link, summary, published

### memory/check_seen
- Call before processing each article
- Key should be a hash or the URL itself
- Returns {seen: true/false}

### memory/add
- Store each new article
- Include all extracted metadata
- Type should be "document"

### memory/mark_seen
- Call after successfully storing
- Use 14-day TTL to allow re-processing after expiry

## Error Handling

- If a feed fails to fetch, log the error and continue with other feeds
- If memory operations fail, log but don't crash
- Return partial results if some feeds succeed

## Success Criteria

- At least one feed successfully fetched
- New articles stored in memory
- Duplicates correctly identified and skipped
- Failed feeds logged but don't stop collection
