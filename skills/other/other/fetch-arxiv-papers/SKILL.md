---
name: fetch-arxiv-papers
version: 2.0.0
description: 'Fetch recent AI/ML research papers from arXiv RSS feeds and store them
  in memory. Uses RSS tool for fetching and memory MCP for storage and deduplication.

  '
license: MIT
allowed-tools:
- rss
- memory/add
- memory/check_seen
- memory/mark_seen
metadata:
  domain: news
  category: collection
  requires-approval: false
  confidence: 0.85
  mcp-servers: []
---

# Fetch ArXiv Papers

Fetch and store AI/ML research papers from arXiv with deduplication.

## When to Use

Use this skill when you need to:
- Collect recent AI/ML research papers from arXiv
- Store papers in memory for later analysis
- Avoid processing duplicate papers

## Instructions

### Step 1: Define ArXiv Categories

Target these arXiv categories for AI/ML papers:
- `cs.AI` - Artificial Intelligence
- `cs.LG` - Machine Learning
- `cs.CL` - Computation and Language (NLP)
- `cs.CV` - Computer Vision
- `cs.NE` - Neural and Evolutionary Computing

### Step 2: Fetch ArXiv RSS Feeds

Use the `rss` tool to fetch papers from each category feed.

**Feed URL pattern:**
- `https://export.arxiv.org/rss/{category}`
- Example: `https://export.arxiv.org/rss/cs.AI`

**For each feed:**
1. Call the `rss` tool with the feed URL
2. Extract: title, link (abstract URL), description (abstract), dc:creator (authors), published date
3. Parse the arXiv ID from the link URL (e.g., `2401.12345` from `https://arxiv.org/abs/2401.12345`)

### Step 3: Check for Duplicates

For each paper from the feeds:

1. **Check if already seen:**
   - Call `memory/check_seen` with key=arXiv ID, namespace="news/papers"
   - If seen=true, skip this paper

2. **Validate required fields:**
   - Paper must have: title, arXiv ID, abstract
   - Skip papers missing required fields

### Step 4: Store New Papers

For each new (unseen) paper:

1. **Store in memory:**
   - Call `memory/add` with:
     - type: "document"
     - namespace: "news/papers"
     - data: {arxiv_id, title, authors, abstract, categories, published_date, pdf_url, abstract_url}
     - metadata: {fetched_at, source_category}

2. **Mark as seen:**
   - Call `memory/mark_seen` with:
     - key: arXiv ID
     - namespace: "news/papers"
     - ttl_seconds: 2592000 (30 days)

### Step 5: Return Results

Return a summary including:
- Number of papers stored
- Number of duplicates skipped
- Number of categories processed
- Any failed feeds

## Tool Usage Guidance

### rss tool
- Use to fetch arXiv RSS feed content
- Handles XML parsing and entry extraction
- Returns list of entries with title, link, description, published

### memory/check_seen
- Call before processing each paper
- Key should be the arXiv ID (e.g., "2401.12345")
- Returns {seen: true/false}

### memory/add
- Store each new paper
- Include all extracted metadata
- Type should be "document"

### memory/mark_seen
- Call after successfully storing
- Use 30-day TTL for papers (longer than news articles)

## Paper Data Schema

```json
{
  "arxiv_id": "2401.12345",
  "title": "Advances in Large Language Model Reasoning",
  "authors": ["Alice Smith", "Bob Jones"],
  "abstract": "We present a novel approach to...",
  "categories": ["cs.AI", "cs.CL"],
  "published_date": "2026-01-25",
  "pdf_url": "https://arxiv.org/pdf/2401.12345.pdf",
  "abstract_url": "https://arxiv.org/abs/2401.12345"
}
```

## Error Handling

- If a feed fails to fetch, log the error and continue with other feeds
- If memory operations fail, log but don't crash
- Return partial results if some feeds succeed

## Success Criteria

- At least one category feed successfully fetched
- New papers stored in memory
- Duplicates correctly identified and skipped by arXiv ID
- Failed feeds logged but don't stop collection
