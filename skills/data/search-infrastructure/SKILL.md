---
name: search-infrastructure
description: Build search systems with Elasticsearch, vector search, and hybrid retrieval
---

# Search Infrastructure

## Search Engine Selection

| Engine | Best For | Scale | Hybrid Search | Managed Option |
|--------|----------|-------|---------------|----------------|
| **Elasticsearch** | Full-text + analytics | Billions of docs | Yes (8.0+ knn) | Elastic Cloud |
| **OpenSearch** | AWS-native, ES fork | Billions of docs | Yes (k-NN plugin) | AWS OpenSearch |
| **Meilisearch** | Typo-tolerant, quick setup | <10M docs | No native | Meilisearch Cloud |
| **Typesense** | Low-latency instant search | <100M docs | Yes (embedding) | Typesense Cloud |
| **Qdrant** | Pure vector search | Billions of vectors | Sparse+dense | Qdrant Cloud |

**Default:** Elasticsearch for general search. Meilisearch for <10M docs + fast prototyping. Qdrant for vector-first.

## Elasticsearch Index Design

```python
from elasticsearch import Elasticsearch
es = Elasticsearch("http://localhost:9200")

INDEX_SETTINGS = {
    "settings": {
        "number_of_shards": 3,                    # 1 shard per 20-50GB
        "number_of_replicas": 1,
        "analysis": {
            "analyzer": {
                "text_analyzer": {
                    "type": "custom", "tokenizer": "standard",
                    "filter": ["lowercase", "english_stop", "english_stemmer", "edge_ngram_filter"],
                },
                "search_analyzer": {               # Separate analyzer for queries
                    "type": "custom", "tokenizer": "standard",
                    "filter": ["lowercase", "english_stop", "english_stemmer"],
                },
            },
            "filter": {
                "english_stop": {"type": "stop", "stopwords": "_english_"},
                "english_stemmer": {"type": "stemmer", "language": "english"},
                "edge_ngram_filter": {"type": "edge_ngram", "min_gram": 2, "max_gram": 15},
            },
        },
    },
    "mappings": {
        "properties": {
            "title": {
                "type": "text", "analyzer": "text_analyzer", "search_analyzer": "search_analyzer",
                "fields": {"keyword": {"type": "keyword"}, "suggest": {"type": "completion"}},
            },
            "body": {"type": "text", "analyzer": "text_analyzer", "search_analyzer": "search_analyzer"},
            "embedding": {"type": "dense_vector", "dims": 768, "index": True, "similarity": "cosine"},
            "category": {"type": "keyword"},
            "price": {"type": "float"},
            "created_at": {"type": "date"},
            "tags": {"type": "keyword"},
        },
    },
}
es.indices.create(index="products", body=INDEX_SETTINGS)
```

## Search Query Patterns

### Bool Query with Boosting

```python
def search_products(query: str, category: str | None = None,
                    price_min: float = 0, price_max: float = 1e6) -> dict:
    must = [{"multi_match": {
        "query": query,
        "fields": ["title^3", "body", "tags^2"],   # Title 3x boost, tags 2x
        "type": "best_fields",
        "fuzziness": "AUTO",                         # 0 for 1-2 chars, 1 for 3-5, 2 for 6+
    }}]
    filters = [{"range": {"price": {"gte": price_min, "lte": price_max}}}]
    if category:
        filters.append({"term": {"category": category}})
    return es.search(index="products", body={
        "query": {"bool": {"must": must, "filter": filters}},
        "highlight": {"fields": {"body": {"fragment_size": 150, "number_of_fragments": 3}}},
        "size": 20,
    })
```

### Function Score for Relevance Tuning

```python
def search_with_scoring(query: str) -> dict:
    return es.search(index="products", body={
        "query": {"function_score": {
            "query": {"multi_match": {"query": query, "fields": ["title^3", "body"]}},
            "functions": [
                {"gauss": {"created_at": {"origin": "now", "scale": "30d", "decay": 0.5}}},
                {"field_value_factor": {
                    "field": "view_count", "modifier": "log1p", "factor": 0.5,
                }},
            ],
            "score_mode": "multiply", "boost_mode": "multiply",
        }},
    })
```

## Hybrid Keyword + Vector Search

```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")

def hybrid_search(query: str, k: int = 20) -> dict:
    """Combine BM25 keyword search with kNN vector search using RRF."""
    query_vec = model.encode(query).tolist()
    return es.search(index="products", body={
        "size": k,
        "query": {"bool": {"should": [
            {"multi_match": {"query": query, "fields": ["title^3", "body"]}},
        ]}},
        "knn": {                                      # ES 8.0+ native kNN
            "field": "embedding", "query_vector": query_vec,
            "k": k, "num_candidates": k * 10,         # More candidates = better recall
        },
        "rank": {"rrf": {
            "window_size": k * 5,
            "rank_constant": 60,                       # Lower = more weight to top ranks
        }},
    })

def index_with_embedding(doc: dict):
    text = f"{doc['title']} {doc['body']}"
    doc["embedding"] = model.encode(text).tolist()
    es.index(index="products", body=doc)
```

## Faceted Search and Aggregations

```python
def faceted_search(query: str, filters: dict | None = None) -> dict:
    filter_clauses = []
    if filters:
        for field, values in filters.items():
            filter_clauses.append({"terms": {field: values}})
    return es.search(index="products", body={
        "query": {"bool": {"must": [{"match": {"body": query}}], "filter": filter_clauses}},
        "aggs": {
            "categories": {"terms": {"field": "category", "size": 20}},
            "price_ranges": {"range": {"field": "price", "ranges": [
                {"to": 25}, {"from": 25, "to": 100}, {"from": 100, "to": 500}, {"from": 500},
            ]}},
            "avg_price": {"avg": {"field": "price"}},
            "tags": {"terms": {"field": "tags", "size": 50}},
        },
        "size": 20,
    })
```

## Autocomplete with Completion Suggester

```python
def autocomplete(prefix: str, size: int = 5) -> list[str]:
    """Fast prefix completion using FST-based suggester."""
    resp = es.search(index="products", body={
        "suggest": {"title_suggest": {
            "prefix": prefix,
            "completion": {"field": "title.suggest", "size": size, "fuzzy": {"fuzziness": 1}},
        }},
    })
    return [opt["text"] for opt in resp["suggest"]["title_suggest"][0]["options"]]
```

## Meilisearch Quick Setup

```python
import meilisearch

client = meilisearch.Client("http://localhost:7700", "MASTER_KEY")
index = client.index("products")

index.update_settings({
    "searchableAttributes": ["title", "body", "tags"],          # Priority order
    "filterableAttributes": ["category", "price", "tags"],
    "sortableAttributes": ["price", "created_at"],
    "typoTolerance": {"minWordSizeForTypos": {"oneTypo": 4, "twoTypos": 8}},
})
index.add_documents(documents, primary_key="id")

results = index.search("wireless headphones", {
    "filter": "category = electronics AND price < 200",
    "sort": ["price:asc"], "limit": 20,
    "attributesToHighlight": ["title", "body"],
})
```

## Gotchas

- **Shard sizing**: 20-50GB per shard; too many small shards waste overhead, too few large shards slow queries -- reindex to resize
- **Mapping explosion**: Dynamic mappings on nested JSON create thousands of fields; always set `"dynamic": "strict"` in production
- **Analyzer at index vs query time**: Use `edge_ngram` at index time only; applying at query time doubles partial matches and kills precision
- **Vector dimension mismatch**: Embedding model change requires full reindex; pin model version and validate dimension on ingest
- **RRF window_size**: Must be >= `size`; too small truncates candidates before fusion, silently degrading hybrid results
- **Completion suggester limitations**: Only prefix-based; for infix matching, use `edge_ngram` on a separate field
- **Refresh interval**: Default 1s creates a new segment per second; for bulk indexing, set `"refresh_interval": "-1"` then refresh manually
- **Memory for kNN**: Dense vectors loaded into memory; 1M docs x 768 dims x 4 bytes = ~3GB RAM per shard
