---
name: commerce-vector-search
description: Perform semantic and keyword search across products, customers, orders, and inventory. Use when searching by natural language queries, finding similar items, or doing hybrid semantic plus keyword search.
---

# Commerce Vector Search

Hybrid semantic and keyword search across commerce entities using OpenAI embeddings and BM25 full-text search.

## How It Works

1. Generate embeddings for products, customers, orders, and inventory items.
2. Store embeddings in dedicated tables with metadata.
3. Search using natural language queries that combine semantic similarity and keyword matching.
4. Results are ranked by combined relevance score.
5. Filter by entity type and minimum score threshold.

## Usage

- MCP tools: `search_products`, `search_customers`, `search_orders`, `search_inventory`, `get_embedding_stats`.
- Embedding model: OpenAI `text-embedding-3-small` (1536 dimensions).
- BM25 full-text via SQLite FTS5.

## Searchable Entities

- **Products**: name, description, attributes, category
- **Customers**: name, email, company, notes
- **Orders**: order details, item names, notes
- **Inventory**: SKU, product name, location, notes

## Scoring

- Semantic similarity: cosine distance converted to score (1.0 = exact match)
- BM25 keyword: traditional term-frequency scoring
- Combined ranking for hybrid search results
- `min_score` threshold to filter low-relevance results

## Output

```json
{"results":[{"entity_type":"product","entity_id":"prod_456","score":0.92,"name":"Wireless Bluetooth Headphones"},{"entity_type":"product","entity_id":"prod_789","score":0.87,"name":"Noise Cancelling Earbuds"}]}
```

## Present Results to User

- Ranked list of matching entities with relevance scores.
- Entity type and key details (name, SKU, email, etc.).
- Total results found and search query used.
- Embedding statistics (total embeddings by entity type).

## Troubleshooting

- No results: check that embeddings have been generated for the entity type.
- Low relevance scores: refine the search query or lower the min_score threshold.
- Missing embeddings: run embedding generation for new or updated entities.
- API key error: verify OpenAI API key in embedding configuration.

## References
- references/vector-search-config.md
- /home/dom/stateset-icommerce/crates/stateset-core/src/models/vector.rs
- /home/dom/stateset-icommerce/crates/stateset-embedded/src/vector.rs
