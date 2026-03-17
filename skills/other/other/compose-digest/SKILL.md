---
name: compose-digest
version: "2.0.0"
description: >
  Compose a formatted news digest from analyzed articles and trends. Uses memory
  search to retrieve articles and LLM to generate formatted output.
license: MIT
allowed-tools:
  - use_llm                # Strands built-in LLM tool for formatting
  - memory/search          # Search for articles and trends
metadata:
  kubani:
    domain: news
    category: publishing
    requires_approval: false
    confidence: 0.95
    version: "2.0.0"
---

# Compose Digest

Compose a formatted news digest from analyzed articles and trends.

## When to Use

Use this skill when you need to:
- Create daily or weekly news digests
- Format articles for publication
- Group articles by category or topic
- Highlight trending topics
- Generate human-readable summaries

## Instructions

### Step 1: Retrieve Articles from Memory

Use `memory/search` to get recent analyzed articles:
- namespace: "news/analyses"
- query: "AI news articles" (or date-specific query)
- limit: 50 (adjust for daily/weekly)

Filter by date range if specified.

### Step 2: Retrieve Trends from Memory

Use `memory/search` to get current trends:
- namespace: "news/trends"
- query: "trending topics"
- limit: 20

### Step 3: Group Articles by Category

Organize articles into sections:
- **security** - Security vulnerabilities and updates
- **product** - New releases and product updates
- **research** - Latest research papers and breakthroughs
- **business** - Company news and market developments
- **policy** - Regulations and policy changes
- **general** - Other AI news and updates

Sort articles within each category by importance_score (highest first).

### Step 4: Format with LLM

Use `use_llm` to compose the final digest:

**Digest composition prompt:**
```
Compose a news digest from these articles and trends.

ARTICLES BY CATEGORY:
{categorized_articles}

TRENDING TOPICS:
{trends}

Format as Markdown with:
1. Header with title and date
2. Breaking news section (importance >= 9)
3. Trending topics section
4. Category sections in order: security, product, research, business, policy, general

For each article include:
- Title with importance indicator (🔴 critical, 🟠 important, 🟡 notable, ⚪ minor)
- Source name
- 2-3 sentence summary
- Link to source

Keep summaries concise. Use emojis for section headers.
```

### Step 5: Return Formatted Digest

Return the composed digest in Markdown format.

## Tool Usage Guidance

### memory/search
- Search "news/analyses" for recent articles
- Search "news/trends" for trending topics
- Filter by date range as needed

### use_llm
- Use for final formatting and composition
- Provide all articles and trends as context
- Request structured Markdown output

## Digest Structure

```markdown
# AI News Digest

**Date:** 2026-01-31
**Articles:** 25 | **Trends:** 8

---

## 🚨 Breaking News

### GPT-5 Released with AGI Capabilities

*Major model release from leading AI company*

OpenAI has released GPT-5, claiming significant advances...

[Read more](https://...)

---

## 🔥 Trending Topics

### Breaking
- **GPT-5** (15 mentions)
- **AGI** (12 mentions)

### Hot
- **Claude 4** (8 mentions)
- **Gemini Pro** (7 mentions)

---

## 🔒 Security

### 1. 🔴 Critical Vulnerability in Popular AI Framework

**Source:** Security Research Blog

Researchers have discovered a critical vulnerability...

[Read more](https://...)

---
```

## Category Order (Priority)

1. **Security** - Most urgent (vulnerabilities, incidents)
2. **Product** - Time-sensitive (launches, releases)
3. **Research** - Valuable but not urgent
4. **Business** - Market context
5. **Policy** - Regulatory updates
6. **General** - Everything else

## Importance Indicators

| Score | Indicator | Meaning |
|-------|-----------|---------|
| 9-10 | 🔴 | Critical - Major news |
| 7-8 | 🟠 | Important - Significant impact |
| 5-6 | 🟡 | Notable - Meaningful development |
| 1-4 | ⚪ | Minor - Incremental update |

## Length Guidelines

| Digest Type | Articles | Pages |
|-------------|----------|-------|
| Daily | 10-20 | 2-3 |
| Weekly | 30-50 | 5-10 |
| Breaking | 1-3 | 1 |

## Error Handling

- If search returns no articles, return empty digest with explanation
- If LLM formatting fails, return raw article list
- Log but continue if individual articles have issues

## Success Criteria

- Digest is well-structured and readable
- Articles grouped logically by category
- Important stories prominently featured
- Trending topics highlighted
- Length reasonable for consumption
