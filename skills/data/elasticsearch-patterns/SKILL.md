---
name: elasticsearch-patterns
description: Mapping design, query optimization, aggregation patterns, index lifecycle management, and search relevance tuning.
---

# Elasticsearch Patterns

Search and analytics patterns for Elasticsearch deployments.

## Mapping Design

```json
{
  "mappings": {
    "dynamic": "strict",
    "properties": {
      "id": { "type": "keyword" },
      "title": {
        "type": "text",
        "analyzer": "standard",
        "fields": {
          "keyword": { "type": "keyword" },
          "autocomplete": {
            "type": "text",
            "analyzer": "autocomplete_analyzer"
          }
        }
      },
      "description": {
        "type": "text",
        "analyzer": "standard"
      },
      "price": { "type": "scaled_float", "scaling_factor": 100 },
      "category": { "type": "keyword" },
      "tags": { "type": "keyword" },
      "location": { "type": "geo_point" },
      "created_at": { "type": "date" },
      "metadata": {
        "type": "object",
        "enabled": false
      }
    }
  },
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 1,
    "analysis": {
      "analyzer": {
        "autocomplete_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": ["lowercase", "autocomplete_filter"]
        }
      },
      "filter": {
        "autocomplete_filter": {
          "type": "edge_ngram",
          "min_gram": 2,
          "max_gram": 20
        }
      }
    }
  }
}
```

## Query Patterns

```typescript
import { Client } from '@elastic/elasticsearch'

const client = new Client({ node: process.env.ELASTICSEARCH_URL })

// Full-text search with boosting and highlighting
async function searchProducts(query: string, filters: ProductFilters) {
  const result = await client.search({
    index: 'products',
    body: {
      query: {
        bool: {
          must: [
            {
              multi_match: {
                query,
                fields: ['title^3', 'description', 'tags^2'],  // Title 3x boost
                type: 'best_fields',
                fuzziness: 'AUTO',         // Typo tolerance
                prefix_length: 2,          // First 2 chars must match exactly
              }
            }
          ],
          filter: [
            ...(filters.category ? [{ term: { category: filters.category } }] : []),
            ...(filters.minPrice || filters.maxPrice ? [{
              range: {
                price: {
                  ...(filters.minPrice && { gte: filters.minPrice }),
                  ...(filters.maxPrice && { lte: filters.maxPrice }),
                }
              }
            }] : []),
            ...(filters.tags?.length ? [{ terms: { tags: filters.tags } }] : []),
          ],
        }
      },
      highlight: {
        fields: {
          title: { number_of_fragments: 0 },       // Full field highlight
          description: { fragment_size: 150 },      // Snippet
        },
        pre_tags: ['<mark>'],
        post_tags: ['</mark>'],
      },
      sort: [
        { _score: 'desc' },
        { created_at: 'desc' },
      ],
      from: filters.offset ?? 0,
      size: filters.limit ?? 20,
    }
  })

  return {
    hits: result.hits.hits.map(hit => ({
      ...hit._source,
      score: hit._score,
      highlights: hit.highlight,
    })),
    total: (result.hits.total as { value: number }).value,
  }
}

// Autocomplete search (edge_ngram)
async function autocomplete(prefix: string) {
  const result = await client.search({
    index: 'products',
    body: {
      query: {
        match: {
          'title.autocomplete': {
            query: prefix,
            operator: 'and',
          }
        }
      },
      _source: ['title', 'category'],
      size: 10,
    }
  })
  return result.hits.hits.map(h => h._source)
}
```

## Aggregation Patterns

```typescript
// Faceted search: get filter counts alongside results
async function searchWithFacets(query: string) {
  const result = await client.search({
    index: 'products',
    body: {
      query: { match: { title: query } },
      size: 20,
      aggs: {
        // Category facets
        categories: {
          terms: { field: 'category', size: 20 }
        },
        // Price ranges
        price_ranges: {
          range: {
            field: 'price',
            ranges: [
              { key: 'budget', to: 50 },
              { key: 'mid', from: 50, to: 200 },
              { key: 'premium', from: 200 },
            ]
          }
        },
        // Price statistics
        price_stats: {
          stats: { field: 'price' }
        },
        // Date histogram
        created_over_time: {
          date_histogram: {
            field: 'created_at',
            calendar_interval: 'month',
          }
        },
      }
    }
  })

  return {
    hits: result.hits.hits,
    facets: {
      categories: result.aggregations?.categories,
      priceRanges: result.aggregations?.price_ranges,
      priceStats: result.aggregations?.price_stats,
      timeline: result.aggregations?.created_over_time,
    }
  }
}
```

## Index Lifecycle Management (ILM)

```json
{
  "policy": {
    "phases": {
      "hot": {
        "min_age": "0ms",
        "actions": {
          "rollover": {
            "max_primary_shard_size": "50gb",
            "max_age": "7d"
          },
          "set_priority": { "priority": 100 }
        }
      },
      "warm": {
        "min_age": "30d",
        "actions": {
          "shrink": { "number_of_shards": 1 },
          "forcemerge": { "max_num_segments": 1 },
          "set_priority": { "priority": 50 },
          "allocate": {
            "number_of_replicas": 0,
            "require": { "data": "warm" }
          }
        }
      },
      "cold": {
        "min_age": "90d",
        "actions": {
          "set_priority": { "priority": 0 },
          "freeze": {},
          "allocate": {
            "require": { "data": "cold" }
          }
        }
      },
      "delete": {
        "min_age": "365d",
        "actions": {
          "delete": {}
        }
      }
    }
  }
}
```

## Bulk Indexing

```typescript
async function bulkIndex(documents: Product[]): Promise<void> {
  const body = documents.flatMap(doc => [
    { index: { _index: 'products', _id: doc.id } },
    doc,
  ])

  const result = await client.bulk({ body, refresh: false })  // No refresh for throughput

  if (result.errors) {
    const erroredItems = result.items.filter((item: any) => item.index?.error)
    console.error(`Bulk indexing errors: ${erroredItems.length}/${documents.length}`)
    for (const item of erroredItems.slice(0, 5)) {
      console.error(item.index?.error)
    }
  }
}

// Reindex with zero downtime using aliases
async function reindexWithAlias(oldIndex: string, newIndex: string, alias: string) {
  // 1. Create new index with updated mappings
  await client.indices.create({ index: newIndex, body: newMappings })

  // 2. Reindex data
  await client.reindex({
    body: { source: { index: oldIndex }, dest: { index: newIndex } },
    wait_for_completion: true,
  })

  // 3. Atomic alias swap
  await client.indices.updateAliases({
    body: {
      actions: [
        { remove: { index: oldIndex, alias } },
        { add: { index: newIndex, alias } },
      ]
    }
  })
}
```

## Checklist

- [ ] Explicit mappings with `dynamic: strict` (no surprise field types)
- [ ] Multi-field mappings: keyword for filtering, text for search
- [ ] Edge n-gram analyzer for autocomplete fields
- [ ] Boost important fields in multi_match (title > description)
- [ ] Use filter context for non-scoring queries (cacheable, faster)
- [ ] ILM policy for hot/warm/cold/delete lifecycle
- [ ] Alias-based indexing for zero-downtime reindexing
- [ ] Bulk API for batch writes (never single-document in loops)

## Anti-Patterns

- Dynamic mapping in production: unexpected field types cause search failures
- Searching keyword fields with full-text queries (no tokenization)
- Refreshing after every write: kills indexing throughput
- Single huge index instead of time-based indices with ILM
- Deep pagination with from/size beyond 10,000 (use search_after)
- Storing data only in ES without a source-of-truth database
