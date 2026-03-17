---
name: analyze-article
version: "2.0.0"
description: >
  Analyze news articles using LLM to extract insights, categorize content,
  identify key entities, and assess importance. Stores analysis in memory
  with links to source articles.
license: MIT
allowed-tools:
  - use_llm                # Strands built-in LLM tool for analysis
  - memory/get             # Get article from memory
  - memory/add             # Store analysis results
  - memory/link            # Link analysis to source article
metadata:
  kubani:
    domain: news
    category: analysis
    requires_approval: false
    confidence: 0.90
    version: "2.0.0"
---

# Analyze Article

Analyze news articles using LLM to extract insights and assess importance.

## When to Use

Use this skill when you need to:
- Generate concise summaries of news articles
- Categorize articles by topic (research, business, product, security, policy)
- Extract key entities (companies, people, technologies, models)
- Assess article importance on a 1-10 scale
- Detect breaking news that requires immediate notification

## Instructions

### Step 1: Retrieve Article from Memory

Use `memory/get` to retrieve the article to analyze by its ID.

The article should contain:
- title: Article title
- url: Source URL
- source: Publication name
- summary or content: Article text

### Step 2: Analyze with LLM

Use the `use_llm` tool to analyze the article with this prompt structure:

**Analysis prompt:**
```
Analyze the following news article and provide:

1. **Summary**: A concise 2-3 sentence summary highlighting the key points.
2. **Category**: One of: research, business, product, security, policy, general
3. **Entities**: List of key entities mentioned (companies, people, technologies, models)
4. **Importance Score**: 1-10 rating where:
   - 1-3: Minor news, incremental updates
   - 4-6: Notable news, meaningful developments
   - 7-8: Important news, significant impact
   - 9-10: Major news, industry-changing announcements
5. **Is Breaking**: True if this is major breaking news
6. **Breaking Reason**: If breaking, explain why

Article:
Title: {title}
Source: {source}
Content: {content}

Respond in JSON format.
```

**Importance scoring factors:**
- Source credibility and significance
- Novelty of the information
- Potential industry impact
- Whether from an official company announcement
- Security implications

### Step 3: Store Analysis in Memory

Use `memory/add` to store the analysis results:
- type: "analysis"
- namespace: "news/analyses"
- data: {summary, category, entities, importance_score, is_breaking, breaking_reason}
- metadata: {source_article_id, analyzed_at}

### Step 4: Link Analysis to Source

Use `memory/link` to create a relationship:
- source_id: analysis ID
- target_id: original article ID
- relation_type: "ANALYZED_FROM"

### Step 5: Return Results

Return the analysis including:
- Analysis ID for reference
- AI-generated summary
- Category classification
- Extracted entities
- Importance score
- Breaking news flag

## Tool Usage Guidance

### use_llm tool
- Use for structured content analysis
- Request JSON output format
- Use temperature 0.0 for consistency

### memory/get
- Retrieve article by ID
- Returns full article data

### memory/add
- Store analysis as type "analysis"
- Include source article ID in metadata

### memory/link
- Create ANALYZED_FROM relationship
- Links analysis to source article

## Importance Scoring Guidelines

### Score 1-3: Minor News
- Incremental product updates
- Minor bug fixes or patches
- Routine announcements

### Score 4-6: Notable News
- New features or capabilities
- Meaningful partnerships
- Research paper publications

### Score 7-8: Important News
- Major product launches
- Significant research breakthroughs
- Important policy changes

### Score 9-10: Major News
- Industry-changing announcements
- Major security vulnerabilities
- Breakthrough research results

## Breaking News Criteria

Mark as breaking if ANY of these apply:
- **Major model release** from leading AI companies (OpenAI, Anthropic, Google, Meta)
- **Critical security vulnerability** affecting widely-used AI systems
- **Regulatory action** with immediate industry impact
- **Breakthrough research** that changes fundamental understanding

## Analysis Data Schema

```json
{
  "id": "analysis-abc123",
  "summary": "OpenAI has released GPT-5 with significant improvements...",
  "category": "product",
  "entities": ["OpenAI", "GPT-5", "Sam Altman"],
  "importance_score": 9,
  "is_breaking": true,
  "breaking_reason": "Major model release from leading AI company",
  "source_article_id": "article-xyz789",
  "analyzed_at": "2026-01-31T12:00:00Z"
}
```

## Error Handling

- If article retrieval fails, log error and skip
- If LLM returns malformed JSON, retry with clearer prompt
- If memory operations fail, log but return analysis results

## Success Criteria

- All articles have valid summaries and categories
- Importance scores are calibrated and consistent
- Entities are accurately extracted
- Analysis is linked to source article
