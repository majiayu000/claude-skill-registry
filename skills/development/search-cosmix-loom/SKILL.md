---
name: search
description: Full-text search and search engine implementation. Use when implementing search functionality, autocomplete, faceted search, relevance tuning, or working with search indexes. Keywords: search, full-text search, Elasticsearch, OpenSearch, Meilisearch, Typesense, fuzzy search, autocomplete, faceted search, facets, inverted index, relevance, ranking, scoring, tokenizer, analyzer, search-as-you-type, aggregations, synonyms, indexing, query, filtering, highlighting, search UI, typeahead, suggestions.
---

# Search

## Overview

Search functionality is a critical component of modern applications, enabling users to find relevant content quickly. This skill covers Elasticsearch fundamentals, full-text search patterns, indexing strategies, and advanced features like faceted search and autocomplete.

## Key Concepts

### Elasticsearch Fundamentals

Elasticsearch is a distributed search and analytics engine built on Apache Lucene.

**Core Components:**

- **Index**: A collection of documents with similar characteristics
- **Document**: A JSON object that is indexed and searchable
- **Mapping**: Schema definition for documents in an index
- **Shard**: A subdivision of an index for horizontal scaling
- **Replica**: Copy of a shard for redundancy and read scaling

**Basic Index Operations:**

```json
// Create an index with settings
PUT /products
{
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 2,
    "analysis": {
      "analyzer": {
        "custom_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": ["lowercase", "snowball"]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "name": { "type": "text", "analyzer": "custom_analyzer" },
      "description": { "type": "text" },
      "price": { "type": "float" },
      "category": { "type": "keyword" },
      "created_at": { "type": "date" }
    }
  }
}
```

### Full-Text Search Patterns

**Match Query** - Standard full-text search:

```json
GET /products/_search
{
  "query": {
    "match": {
      "description": {
        "query": "wireless bluetooth headphones",
        "operator": "and",
        "fuzziness": "AUTO"
      }
    }
  }
}
```

**Multi-Match Query** - Search across multiple fields:

```json
GET /products/_search
{
  "query": {
    "multi_match": {
      "query": "wireless headphones",
      "fields": ["name^3", "description", "category^2"],
      "type": "best_fields",
      "tie_breaker": 0.3
    }
  }
}
```

**Bool Query** - Combine multiple conditions:

```json
GET /products/_search
{
  "query": {
    "bool": {
      "must": [
        { "match": { "name": "headphones" } }
      ],
      "filter": [
        { "range": { "price": { "gte": 50, "lte": 200 } } },
        { "term": { "category": "electronics" } }
      ],
      "should": [
        { "match": { "description": "noise cancelling" } }
      ],
      "must_not": [
        { "term": { "status": "discontinued" } }
      ]
    }
  }
}
```

### Indexing Strategies

**Bulk Indexing:**

```json
POST /_bulk
{ "index": { "_index": "products", "_id": "1" } }
{ "name": "Wireless Headphones", "price": 99.99 }
{ "index": { "_index": "products", "_id": "2" } }
{ "name": "Bluetooth Speaker", "price": 49.99 }
```

**Index Aliases** - Zero-downtime reindexing:

```json
// Create alias
POST /_aliases
{
  "actions": [
    { "add": { "index": "products_v2", "alias": "products" } },
    { "remove": { "index": "products_v1", "alias": "products" } }
  ]
}
```

### Relevance Tuning and Boosting

**Field Boosting:**

```json
GET /products/_search
{
  "query": {
    "multi_match": {
      "query": "headphones",
      "fields": ["name^5", "description^2", "tags"]
    }
  }
}
```

**Function Score** - Custom scoring:

```json
GET /products/_search
{
  "query": {
    "function_score": {
      "query": { "match": { "name": "headphones" } },
      "functions": [
        {
          "filter": { "term": { "featured": true } },
          "weight": 2
        },
        {
          "field_value_factor": {
            "field": "popularity",
            "factor": 1.2,
            "modifier": "sqrt"
          }
        },
        {
          "gauss": {
            "created_at": {
              "origin": "now",
              "scale": "30d",
              "decay": 0.5
            }
          }
        }
      ],
      "score_mode": "multiply",
      "boost_mode": "multiply"
    }
  }
}
```

### Faceted Search and Aggregations

**Terms Aggregation** - Category facets:

```json
GET /products/_search
{
  "size": 0,
  "aggs": {
    "categories": {
      "terms": { "field": "category", "size": 10 }
    },
    "price_ranges": {
      "range": {
        "field": "price",
        "ranges": [
          { "to": 50, "key": "budget" },
          { "from": 50, "to": 100, "key": "mid-range" },
          { "from": 100, "key": "premium" }
        ]
      }
    },
    "avg_price": {
      "avg": { "field": "price" }
    }
  }
}
```

**Nested Aggregations:**

```json
GET /products/_search
{
  "aggs": {
    "categories": {
      "terms": { "field": "category" },
      "aggs": {
        "avg_price": { "avg": { "field": "price" } },
        "top_products": {
          "top_hits": { "size": 3, "_source": ["name", "price"] }
        }
      }
    }
  }
}
```

### Search-as-You-Type and Autocomplete

**Completion Suggester Setup:**

```json
PUT /products
{
  "mappings": {
    "properties": {
      "name_suggest": {
        "type": "completion",
        "contexts": [
          { "name": "category", "type": "category" }
        ]
      }
    }
  }
}
```

**Autocomplete Query:**

```json
GET /products/_search
{
  "suggest": {
    "product_suggest": {
      "prefix": "wire",
      "completion": {
        "field": "name_suggest",
        "size": 5,
        "fuzzy": { "fuzziness": 1 },
        "contexts": {
          "category": ["electronics"]
        }
      }
    }
  }
}
```

**Edge N-gram Analyzer** - Alternative approach:

```json
PUT /products
{
  "settings": {
    "analysis": {
      "filter": {
        "edge_ngram_filter": {
          "type": "edge_ngram",
          "min_gram": 2,
          "max_gram": 20
        }
      },
      "analyzer": {
        "autocomplete": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": ["lowercase", "edge_ngram_filter"]
        },
        "autocomplete_search": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": ["lowercase"]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "name": {
        "type": "text",
        "analyzer": "autocomplete",
        "search_analyzer": "autocomplete_search"
      }
    }
  }
}
```

### Synonyms and Analyzers

**Synonym Configuration:**

```json
PUT /products
{
  "settings": {
    "analysis": {
      "filter": {
        "synonym_filter": {
          "type": "synonym",
          "synonyms": [
            "laptop, notebook, portable computer",
            "phone, mobile, cellphone, smartphone",
            "tv, television, telly"
          ]
        },
        "synonym_graph_filter": {
          "type": "synonym_graph",
          "synonyms_path": "synonyms.txt"
        }
      },
      "analyzer": {
        "synonym_analyzer": {
          "tokenizer": "standard",
          "filter": ["lowercase", "synonym_filter"]
        }
      }
    }
  }
}
```

**Custom Analyzer with Multiple Filters:**

```json
PUT /products
{
  "settings": {
    "analysis": {
      "char_filter": {
        "html_strip": { "type": "html_strip" }
      },
      "filter": {
        "english_stop": { "type": "stop", "stopwords": "_english_" },
        "english_stemmer": { "type": "stemmer", "language": "english" }
      },
      "analyzer": {
        "english_analyzer": {
          "type": "custom",
          "char_filter": ["html_strip"],
          "tokenizer": "standard",
          "filter": ["lowercase", "english_stop", "english_stemmer"]
        }
      }
    }
  }
}
```

### Elasticsearch Patterns

**Connection Management:**

```javascript
// Singleton client pattern
class ElasticsearchClient {
  static instance = null;

  static getInstance() {
    if (!this.instance) {
      this.instance = new Client({
        node: process.env.ES_URL,
        auth: {
          apiKey: process.env.ES_API_KEY,
        },
        maxRetries: 3,
        requestTimeout: 30000,
      });
    }
    return this.instance;
  }
}
```

**Index Templates** - Consistent mappings across time-series indices:

```json
PUT /_index_template/logs_template
{
  "index_patterns": ["logs-*"],
  "template": {
    "settings": {
      "number_of_shards": 1,
      "number_of_replicas": 1
    },
    "mappings": {
      "properties": {
        "@timestamp": { "type": "date" },
        "message": { "type": "text" },
        "level": { "type": "keyword" }
      }
    }
  }
}
```

**Reindexing Pattern** - Schema migrations:

```json
POST /_reindex
{
  "source": { "index": "products_v1" },
  "dest": { "index": "products_v2" },
  "script": {
    "source": "ctx._source.category = ctx._source.category.toLowerCase()"
  }
}
```

### Search UI Patterns

**Debounced Search Input:**

```javascript
import { useState, useEffect } from 'react';

function SearchBar({ onSearch }) {
  const [query, setQuery] = useState('');

  useEffect(() => {
    const timer = setTimeout(() => {
      if (query.length >= 2) {
        onSearch(query);
      }
    }, 300);

    return () => clearTimeout(timer);
  }, [query, onSearch]);

  return (
    <input
      type="text"
      value={query}
      onChange={(e) => setQuery(e.target.value)}
      placeholder="Search..."
    />
  );
}
```

**Faceted Search Component:**

```javascript
function FacetedSearch({ aggregations, selectedFilters, onFilterChange }) {
  return (
    <div className="facets">
      <div className="facet-group">
        <h3>Category</h3>
        {aggregations.categories.buckets.map(bucket => (
          <label key={bucket.key}>
            <input
              type="checkbox"
              checked={selectedFilters.category?.includes(bucket.key)}
              onChange={() => onFilterChange('category', bucket.key)}
            />
            {bucket.key} ({bucket.doc_count})
          </label>
        ))}
      </div>

      <div className="facet-group">
        <h3>Price Range</h3>
        {aggregations.price_ranges.buckets.map(bucket => (
          <label key={bucket.key}>
            <input
              type="radio"
              name="price_range"
              checked={selectedFilters.priceRange === bucket.key}
              onChange={() => onFilterChange('priceRange', bucket.key)}
            />
            {bucket.key} ({bucket.doc_count})
          </label>
        ))}
      </div>
    </div>
  );
}
```

**Search Results with Highlighting:**

```javascript
function SearchResult({ hit }) {
  const getHighlightedText = (text, highlights) => {
    if (!highlights) return text;
    return { __html: highlights.join('...') };
  };

  return (
    <div className="search-result">
      <h3
        dangerouslySetInnerHTML={
          getHighlightedText(hit.name, hit.highlight?.name)
        }
      />
      <p
        dangerouslySetInnerHTML={
          getHighlightedText(hit.description, hit.highlight?.description)
        }
      />
      <span className="score">Score: {hit._score.toFixed(2)}</span>
    </div>
  );
}
```

### Relevance Tuning Strategies

**Testing Relevance:**

```javascript
class RelevanceTest {
  async testQuery(query, expectedTopResults) {
    const results = await this.search(query);
    const topIds = results.hits.slice(0, 3).map(h => h._id);

    console.log(`Query: "${query}"`);
    console.log(`Expected: ${expectedTopResults.join(', ')}`);
    console.log(`Actual: ${topIds.join(', ')}`);

    const precision = topIds.filter(id =>
      expectedTopResults.includes(id)
    ).length / topIds.length;

    return { precision, topIds };
  }
}

// Test cases
const tests = [
  { query: 'wireless headphones', expected: ['prod-123', 'prod-456'] },
  { query: 'bluetooth speaker', expected: ['prod-789', 'prod-012'] },
];
```

**Multi-Field Scoring Strategy:**

```json
GET /products/_search
{
  "query": {
    "multi_match": {
      "query": "wireless headphones",
      "fields": [
        "exact_name^10",
        "name^5",
        "brand^3",
        "description^2",
        "tags"
      ],
      "type": "cross_fields",
      "operator": "and"
    }
  }
}
```

**Recency Boosting Pattern:**

```json
GET /articles/_search
{
  "query": {
    "function_score": {
      "query": { "match": { "content": "elasticsearch" } },
      "functions": [
        {
          "exp": {
            "published_at": {
              "origin": "now",
              "scale": "7d",
              "offset": "1d",
              "decay": 0.5
            }
          }
        }
      ]
    }
  }
}
```

**Popularity + Relevance Combination:**

```json
GET /products/_search
{
  "query": {
    "function_score": {
      "query": { "match": { "name": "laptop" } },
      "functions": [
        {
          "field_value_factor": {
            "field": "sales_count",
            "modifier": "log1p",
            "factor": 0.1
          }
        },
        {
          "field_value_factor": {
            "field": "rating",
            "modifier": "none",
            "factor": 2
          }
        }
      ],
      "score_mode": "sum",
      "boost_mode": "multiply"
    }
  }
}
```

## Best Practices

### Indexing

- Use bulk operations for large data imports
- Implement index aliases for zero-downtime reindexing
- Choose appropriate shard count based on data size
- Use explicit mappings instead of dynamic mapping in production

### Query Performance

- Use `filter` context for exact matches (cached, faster)
- Use `must` context only when scoring matters
- Limit result size and use pagination
- Avoid leading wildcards in queries

### Relevance

- Test relevance with representative queries
- Use field boosting to prioritize important fields
- Implement function_score for business logic (popularity, recency)
- Consider using `dis_max` for OR-style queries

### Autocomplete

- Use completion suggester for simple prefix matching
- Use edge n-grams for more flexible matching
- Implement debouncing on the client side (200-300ms)
- Return suggestions with highlighting

### Schema Design

- Use `keyword` type for exact matches and aggregations
- Use `text` type for full-text search
- Consider multi-fields for both use cases
- Use nested objects sparingly (performance impact)

## Examples

### Complete Search Implementation (Node.js)

```javascript
const { Client } = require("@elastic/elasticsearch");

class SearchService {
  constructor() {
    this.client = new Client({ node: "http://localhost:9200" });
  }

  async search(query, filters = {}, page = 1, pageSize = 20) {
    const must = [];
    const filter = [];

    if (query) {
      must.push({
        multi_match: {
          query,
          fields: ["name^3", "description", "tags^2"],
          type: "best_fields",
          fuzziness: "AUTO",
        },
      });
    }

    if (filters.category) {
      filter.push({ term: { category: filters.category } });
    }

    if (filters.priceMin || filters.priceMax) {
      filter.push({
        range: {
          price: {
            ...(filters.priceMin && { gte: filters.priceMin }),
            ...(filters.priceMax && { lte: filters.priceMax }),
          },
        },
      });
    }

    const response = await this.client.search({
      index: "products",
      body: {
        from: (page - 1) * pageSize,
        size: pageSize,
        query: {
          bool: {
            must: must.length ? must : [{ match_all: {} }],
            filter,
          },
        },
        aggs: {
          categories: { terms: { field: "category", size: 20 } },
          price_stats: { stats: { field: "price" } },
        },
        highlight: {
          fields: {
            name: {},
            description: { fragment_size: 150 },
          },
        },
      },
    });

    return {
      hits: response.hits.hits.map((hit) => ({
        ...hit._source,
        _score: hit._score,
        highlight: hit.highlight,
      })),
      total: response.hits.total.value,
      aggregations: response.aggregations,
    };
  }

  async autocomplete(prefix, limit = 5) {
    const response = await this.client.search({
      index: "products",
      body: {
        suggest: {
          suggestions: {
            prefix,
            completion: {
              field: "name_suggest",
              size: limit,
              fuzzy: { fuzziness: 1 },
            },
          },
        },
      },
    });

    return response.suggest.suggestions[0].options.map((opt) => ({
      text: opt.text,
      score: opt._score,
    }));
  }
}
```

### Python Implementation

```python
from elasticsearch import Elasticsearch, helpers
from typing import Dict, List, Optional

class SearchService:
    def __init__(self, hosts: List[str] = ['localhost:9200']):
        self.es = Elasticsearch(hosts)

    def bulk_index(self, index: str, documents: List[Dict]):
        actions = [
            {
                '_index': index,
                '_id': doc.get('id'),
                '_source': doc
            }
            for doc in documents
        ]
        helpers.bulk(self.es, actions)

    def search(
        self,
        index: str,
        query: str,
        filters: Optional[Dict] = None,
        page: int = 1,
        size: int = 20
    ) -> Dict:
        body = {
            'from': (page - 1) * size,
            'size': size,
            'query': {
                'bool': {
                    'must': [{
                        'multi_match': {
                            'query': query,
                            'fields': ['name^3', 'description'],
                            'fuzziness': 'AUTO'
                        }
                    }] if query else [{'match_all': {}}],
                    'filter': self._build_filters(filters or {})
                }
            },
            'aggs': {
                'categories': {'terms': {'field': 'category'}},
                'price_ranges': {
                    'range': {
                        'field': 'price',
                        'ranges': [
                            {'to': 50},
                            {'from': 50, 'to': 100},
                            {'from': 100}
                        ]
                    }
                }
            }
        }

        return self.es.search(index=index, body=body)

    def _build_filters(self, filters: Dict) -> List[Dict]:
        result = []
        if 'category' in filters:
            result.append({'term': {'category': filters['category']}})
        if 'price_min' in filters or 'price_max' in filters:
            price_range = {}
            if 'price_min' in filters:
                price_range['gte'] = filters['price_min']
            if 'price_max' in filters:
                price_range['lte'] = filters['price_max']
            result.append({'range': {'price': price_range}})
        return result
```
