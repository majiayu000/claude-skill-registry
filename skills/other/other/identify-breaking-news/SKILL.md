---
name: identify-breaking-news
version: "2.0.0"
description: >
  Identify breaking news articles that require immediate notification based on
  importance scores, source credibility, and content analysis. Uses memory search
  to find high-importance articles.
license: MIT
allowed-tools:
  - memory/search          # Search for high-importance articles
  - memory/check_seen      # Check if already notified
  - memory/mark_seen       # Mark as notified
metadata:
  kubani:
    domain: news
    category: analysis
    requires_approval: false
    confidence: 0.92
    version: "2.0.0"
---

# Identify Breaking News

Identify articles that qualify as breaking news requiring immediate notification.

## When to Use

Use this skill when you need to:
- Filter analyzed articles for breaking news
- Determine which stories warrant immediate alerts
- Prioritize high-impact news for real-time notification
- Avoid alert fatigue from non-critical news

## Instructions

### Step 1: Search for High-Importance Articles

Use `memory/search` to find recent high-importance analyses:
- namespace: "news/analyses"
- query: "breaking news important announcement"
- limit: 50

Filter results for:
- importance_score >= 8
- is_breaking == true
- Recent timestamp (last 24 hours)

### Step 2: Check Notification History

For each potential breaking article, use `memory/check_seen`:
- key: article content hash or URL
- namespace: "news/breaking_alerts"

Skip articles that have already been notified.

### Step 3: Calculate Breaking Score

For articles not yet notified, calculate breaking score:

**Score components (0-100 total):**
- **Importance (0-50):** importance_score * 5
- **Source credibility (0-20):** +20 for authoritative sources
- **LLM breaking flag (0-20):** +20 if is_breaking=true
- **Category bonus (0-10):** +10 for security/product/research
- **Keyword bonus (0-10):** +2 per breaking keyword in title

**Authoritative sources:**
- OpenAI Blog, Anthropic Blog, Google AI Blog
- Meta AI Blog, Microsoft AI Blog, DeepMind
- arXiv, Nature, Science

**Breaking keywords:**
- release, launch, announce, breakthrough
- vulnerability, security, critical, urgent
- breaking, major, significant

### Step 4: Apply Threshold

Filter articles by breaking score threshold:
- Score 90-100: Critical breaking news - immediate notification
- Score 80-89: High-priority - notify within 15 minutes
- Score 70-79: Notable - notify within 1 hour
- Score <70: Not breaking - include in regular digest

### Step 5: Apply Rate Limiting

Prevent alert fatigue by limiting notifications:
- Maximum 5 per hour
- Maximum 20 per day

If rate limit exceeded, queue for later notification.

### Step 6: Mark as Notified

For each article being notified, use `memory/mark_seen`:
- key: article content hash or URL
- namespace: "news/breaking_alerts"
- ttl_seconds: 86400 (24 hours)

### Step 7: Return Results

Return breaking news articles including:
- Article details (title, source, summary, URL)
- Breaking score
- Notification priority
- Breaking reason (if available)

## Tool Usage Guidance

### memory/search
- Search for high-importance analyses
- Filter by importance_score and is_breaking
- Limit to recent timeframe

### memory/check_seen
- Check if article already notified
- Use content hash as key
- Prevents duplicate alerts

### memory/mark_seen
- Mark after sending notification
- Use 24-hour TTL
- Allows re-notification after window

## Breaking Score Components

| Component | Points | Criteria |
|-----------|--------|----------|
| Importance | 0-50 | importance_score * 5 |
| Source | 0-20 | Authoritative sources |
| LLM Flag | 0-20 | is_breaking == true |
| Category | 0-10 | security/product/research |
| Keywords | 0-10 | Breaking keywords (2 per) |

## Threshold Guidelines

### Score 90-100: Critical
- Major model releases (GPT-5, Claude 4)
- Critical security vulnerabilities
- Regulatory decisions with immediate impact
- **Action:** Immediate notification

### Score 80-89: High-Priority
- Significant product launches
- Important research breakthroughs
- Major partnerships or acquisitions
- **Action:** Notify within 15 minutes

### Score 70-79: Notable
- Meaningful product updates
- Interesting research results
- Industry developments
- **Action:** Notify within 1 hour

### Score <70: Not Breaking
- Regular news, incremental updates
- **Action:** Include in regular digest only

## Breaking News Data Schema

```json
{
  "url": "https://openai.com/blog/gpt-5",
  "title": "Introducing GPT-5",
  "source": "OpenAI Blog",
  "ai_summary": "OpenAI has released GPT-5 with major advances...",
  "importance_score": 10,
  "is_breaking": true,
  "breaking_reason": "Major model release from leading AI company",
  "breaking_score": 95,
  "category": "product",
  "content_hash": "abc123def456"
}
```

## Error Handling

- If search returns no results, return empty list
- If check_seen fails, proceed with notification (better duplicate than missed)
- If mark_seen fails, log warning but continue

## Success Criteria

- Breaking news identified within 15 minutes of publication
- False positive rate < 10%
- No duplicate alerts for the same story
- Rate limits prevent alert fatigue
- Critical stories (score >90) never missed
