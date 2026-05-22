---
name: deduplication
description: Event deduplication with canonical selection, reputation scoring, and hash-based grouping for multi-source data aggregation. Handles both ID-based and content-based deduplication.
license: MIT
compatibility: TypeScript/JavaScript
metadata:
  category: data-access
  time: 4h
  source: drift-masterguide
---

# Event Deduplication

Canonical selection with reputation scoring and hash-based grouping for multi-source data.

## When to Use This Skill

- Aggregating data from multiple sources (news, events, products)
- Same content appears from different outlets/sources
- Need to pick the "best" version from duplicates
- Tracking deduplication metrics for optimization

## Core Concepts

Simple URL deduplication isn't enough. Production needs:
- Grouping by semantic similarity (same story, different outlets)
- Canonical selection (pick the "best" version)
- Reputation scoring (prefer authoritative sources)
- Both ID-based and content-based deduplication

Two modes:
1. ID-based: When sources have unique IDs, keep the "best" version when IDs collide
2. Content-based: Group by semantic similarity, select canonical from each group

## Implementation

### TypeScript

```typescript
import { createHash } from 'crypto';

interface DeduplicationResult<T> {
  items: T[];
  originalCount: number;
  dedupedCount: number;
  reductionPercent: number;
  duplicateGroups?: number;
}

// ============================================
// ID-Based Deduplication
// ============================================

function deduplicateById<T extends { id: string }>(
  items: T[],
  preferFn: (existing: T, candidate: T) => T
): DeduplicationResult<T> {
  const seen = new Map<string, T>();
  
  for (const item of items) {
    const existing = seen.get(item.id);
    if (existing) {
      seen.set(item.id, preferFn(existing, item));
    } else {
      seen.set(item.id, item);
    }
  }
  
  const dedupedItems = Array.from(seen.values());
  const reductionPercent = items.length > 0
    ? Math.round((1 - dedupedItems.length / items.length) * 100)
    : 0;
  
  return {
    items: dedupedItems,
    originalCount: items.length,
    dedupedCount: dedupedItems.length,
    reductionPercent,
  };
}

// ============================================
// Content-Based Deduplication
// ============================================

interface Article {
  title: string;
  url: string;
  domain: string;
  publishedAt: string;
  tone?: number;
}

/**
 * Generate deduplication key from content
 * Groups by: normalized title + source country + date
 */
function generateDedupKey(article: Article): string {
  const normalizedTitle = article.title
    .toLowerCase()
    .replace(/[^\w\s]/g, '')
    .trim()
    .slice(0, 50);

  const dateStr = article.publishedAt?.slice(0, 10).replace(/-/g, '') || 'unknown';

  return `${normalizedTitle}|${dateStr}`;
}

/**
 * Generate unique ID from URL
 */
function generateEventId(url: string): string {
  return createHash('md5').update(url).digest('hex').slice(0, 12);
}

/**
 * Source reputation scoring
 */
function getReputationScore(domain: string): number {
  // Tier 1: Wire services and major international
  const tier1 = ['reuters.com', 'apnews.com', 'bbc.com', 'bbc.co.uk', 
                 'aljazeera.com', 'france24.com', 'dw.com'];
  if (tier1.some(r => domain.includes(r))) return 100;
  
  // Tier 2: Major newspapers
  const tier2 = ['nytimes.com', 'washingtonpost.com', 'theguardian.com', 
                 'ft.com', 'economist.com', 'wsj.com'];
  if (tier2.some(r => domain.includes(r))) return 75;
  
  // Tier 3: Regional/national
  const tier3 = ['cnn.com', 'foxnews.com', 'nbcnews.com', 'abcnews.go.com'];
  if (tier3.some(r => domain.includes(r))) return 50;
  
  return 10;
}

/**
 * Select canonical article from duplicate group
 */
function selectCanonical<T extends Article>(
  group: { item: T; source: string }[]
): { item: T; source: string } {
  return group.reduce((best, current) => {
    const bestScore = getReputationScore(best.item.domain) + 
                      Math.abs(best.item.tone || 0);
    const currentScore = getReputationScore(current.item.domain) + 
                         Math.abs(current.item.tone || 0);
    
    return currentScore > bestScore ? current : best;
  });
}

/**
 * Deduplicate articles from multiple sources
 */
function deduplicateArticles<T extends Article>(
  sourceResults: { sourceName: string; articles: T[] }[]
): DeduplicationResult<T & { source: string }> {
  const groups = new Map<string, { item: T; source: string }[]>();
  let totalArticles = 0;

  // Group articles by dedup key
  for (const { sourceName, articles } of sourceResults) {
    for (const article of articles) {
      totalArticles++;
      const key = generateDedupKey(article);
      
      if (!groups.has(key)) {
        groups.set(key, []);
      }
      groups.get(key)!.push({ item: article, source: sourceName });
    }
  }

  // Select canonical article from each group
  const items: (T & { source: string })[] = [];
  
  for (const group of groups.values()) {
    const canonical = selectCanonical(group);
    items.push({ ...canonical.item, source: canonical.source });
  }

  const reductionPercent = totalArticles > 0 
    ? Math.round((1 - items.length / totalArticles) * 100)
    : 0;

  console.log(`[Dedup] ${totalArticles} → ${items.length} (${reductionPercent}% reduction)`);

  return {
    items,
    originalCount: totalArticles,
    dedupedCount: items.length,
    reductionPercent,
    duplicateGroups: groups.size,
  };
}
```

## Usage Examples

### ID-Based Deduplication

```typescript
const events = await fetchEvents();

const result = deduplicateById(events, (existing, candidate) => {
  // Prefer events with coordinates
  if (!existing.lat && candidate.lat) return candidate;
  // Prefer higher sentiment magnitude
  if (Math.abs(candidate.sentiment) > Math.abs(existing.sentiment)) {
    return candidate;
  }
  return existing;
});

console.log(`Reduced ${result.reductionPercent}% duplicates`);
```

### Multi-Source Aggregation

```typescript
const results = await Promise.all([
  fetchFromSourceA(),
  fetchFromSourceB(),
  fetchFromSourceC(),
]);

const { items, reductionPercent } = deduplicateArticles([
  { sourceName: 'source-a', articles: results[0] },
  { sourceName: 'source-b', articles: results[1] },
  { sourceName: 'source-c', articles: results[2] },
]);

// items now contains canonical articles with source attribution
```

## Best Practices

1. Semantic grouping - Group by normalized content, not just URL
2. Reputation scoring - Prefer authoritative sources as canonical
3. Best version selection - When IDs collide, keep version with most data
4. Reduction tracking - Log how much deduplication helped
5. Source attribution - Track which source the canonical came from

## Common Mistakes

- Simple URL deduplication (misses same story from different outlets)
- Random selection from duplicates (lose quality signal)
- No normalization (case/punctuation differences create false negatives)
- Not tracking reduction metrics (can't optimize)
- Hardcoded source lists (make configurable)

## Related Patterns

- batch-processing - Process deduplicated items efficiently
- validation-quarantine - Validate before deduplication
- checkpoint-resume - Track which files have been deduplicated
