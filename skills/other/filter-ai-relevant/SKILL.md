---
name: filter-ai-relevant
version: 2.0.0
description: 'DEPRECATED: This skill has been replaced by the analyze-article skill
  which provides more accurate AI-relevance filtering through LLM analysis rather
  than simple keyword matching.

  '
license: MIT
deprecated: true
deprecated_by: analyze-article
deprecated_reason: LLM-based analysis provides better relevance filtering than keyword
  matching
metadata:
  domain: news
  category: collection
  requires-approval: false
  confidence: 0.0
  mcp-servers: []
  status: deprecated
---

# Filter AI-Relevant Articles (DEPRECATED)

> **⚠️ DEPRECATED**: This skill has been deprecated as of v2.0.0.
>
> AI relevance filtering is now handled by the `analyze-article` skill, which uses LLM analysis to accurately categorize and filter articles rather than simple keyword matching.

## Migration Guide

### Before (v1.0)
Filtering used keyword matching:
1. `fetch-rss-feeds` - Collect articles
2. `filter-ai-relevant` - Keyword-based filtering
3. `analyze-article` - LLM analysis

### After (v2.0)
LLM analysis handles relevance determination:
1. `fetch-rss-feeds` - Collect articles (with dedup)
2. `analyze-article` - LLM categorizes AND filters for relevance

### How to Migrate

If you were using `filter-ai-relevant`, update your workflow to rely on `analyze-article` for relevance filtering.

**The new approach:**
- `analyze-article` categorizes articles as: research, business, product, security, policy, general
- Articles can be filtered by category after analysis
- LLM provides more nuanced relevance determination than keywords

## Replacement Skill

| Old Approach | New Approach |
|--------------|--------------|
| Keyword matching | LLM-based analysis |
| Binary AI/not-AI | Category classification |
| Hardcoded keyword list | Context-aware analysis |
| False positives on "meta" | Semantic understanding |

## Why Deprecated

1. **Better accuracy**: LLM understands context, not just keywords
2. **Richer output**: Categories instead of binary relevance
3. **No maintenance**: No keyword list to maintain
4. **Semantic matching**: Understands synonyms and related concepts

## Example Comparison

**Keyword approach (old):**
- "Meta releases new AI model" → filtered (contains "AI")
- "Facebook updates metadata API" → filtered (contains "meta")
- "Novel transformer architecture for proteins" → missed (no exact keyword)

**LLM approach (new):**
- "Meta releases new AI model" → category: product, AI-relevant
- "Facebook updates metadata API" → category: general, not AI-focused
- "Novel transformer architecture for proteins" → category: research, AI-relevant

## See Also

- [analyze-article](../../analysis/analyze-article/SKILL.md) - v2.0 with LLM categorization
