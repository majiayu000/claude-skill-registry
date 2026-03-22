---
name: meilisearch
description: >-
  Add fast, typo-tolerant full-text search with Meilisearch. Use when a user
  asks to add search to an app, implement full-text search, set up a search
  engine, replace Elasticsearch with something simpler, add autocomplete or
  instant search, build a product catalog search, index documents for search,
  configure search relevancy, add faceted filtering, or deploy a self-hosted
  search engine. Covers indexing, querying, facets, filtering, sorting,
  multi-tenancy, and integration with Node.js, Python, and REST API.
license: Apache-2.0
compatibility: 'Linux, macOS, Docker'
metadata:
  author: terminal-skills
  version: 1.0.0
  category: development
  tags:
    - meilisearch
    - search
    - full-text
    - autocomplete
    - indexing
---

# Meilisearch

## Overview

Meilisearch is a fast, open-source search engine designed for instant, typo-tolerant search experiences. Unlike Elasticsearch, it requires zero configuration to get started — add documents, start searching. This skill covers deployment, document indexing, search queries, faceted filtering, sorting, relevancy tuning, multi-tenancy with tenant tokens, and integration with frontend (InstantSearch) and backend (Node.js, Python) applications.

## Instructions

### Step 1: Installation and Deployment

```bash
# Docker (recommended for production)
docker run -d --name meilisearch \
  -p 7700:7700 \
  -v meili_data:/meili_data \
  -e MEILI_MASTER_KEY="your-master-key-min-16-chars" \
  getmeili/meilisearch:latest

# Binary install (Linux)
curl -L https://install.meilisearch.com | sh
./meilisearch --master-key="your-master-key-min-16-chars"

# Verify
curl http://localhost:7700/health
# {"status":"available"}
```

### Step 2: Index Documents

```bash
# Add documents via REST API
curl -X POST 'http://localhost:7700/indexes/products/documents' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your-master-key' \
  --data-binary '[
    {"id": 1, "title": "iPhone 15 Pro", "category": "phones", "brand": "Apple", "price": 999},
    {"id": 2, "title": "Galaxy S24 Ultra", "category": "phones", "brand": "Samsung", "price": 1199},
    {"id": 3, "title": "MacBook Pro M3", "category": "laptops", "brand": "Apple", "price": 1999}
  ]'
```

With the Node.js SDK:

```javascript
// index_products.js — Index documents from a database into Meilisearch
import { MeiliSearch } from 'meilisearch'

const client = new MeiliSearch({
  host: 'http://localhost:7700',
  apiKey: 'your-master-key',
})

const index = client.index('products')

// Add documents (Meilisearch auto-detects the primary key)
await index.addDocuments([
  { id: 1, title: 'iPhone 15 Pro', category: 'phones', brand: 'Apple', price: 999 },
  { id: 2, title: 'Galaxy S24 Ultra', category: 'phones', brand: 'Samsung', price: 1199 },
])

// Configure searchable attributes (which fields to search)
await index.updateSearchableAttributes(['title', 'brand', 'category'])

// Configure filterable attributes (for faceted search)
await index.updateFilterableAttributes(['category', 'brand', 'price'])

// Configure sortable attributes
await index.updateSortableAttributes(['price', 'title'])
```

### Step 3: Search Queries

```javascript
// search.js — Search with filters, facets, and highlighting
const results = await index.search('iphone', {
  limit: 20,
  offset: 0,
  filter: 'price < 1500 AND category = "phones"',
  sort: ['price:asc'],
  facets: ['category', 'brand'],
  attributesToHighlight: ['title'],
  attributesToCrop: ['description'],
  cropLength: 50,
})

// results.hits — matching documents with _formatted (highlighted) versions
// results.facetDistribution — { category: { phones: 2 }, brand: { Apple: 1, Samsung: 1 } }
// results.estimatedTotalHits — total matches
// results.processingTimeMs — typically <50ms
```

REST API equivalent:

```bash
curl -X POST 'http://localhost:7700/indexes/products/search' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your-search-key' \
  --data '{"q": "iphon", "filter": "price < 1500", "facets": ["category", "brand"]}'
# Note: "iphon" still matches "iPhone" — typo tolerance is on by default
```

### Step 4: Faceted Search and Filtering

```javascript
// faceted_search.js — Build an e-commerce filter sidebar
// First, configure filterable attributes
await index.updateFilterableAttributes(['category', 'brand', 'price', 'rating', 'in_stock'])

// Search with multiple filters
const results = await index.search('laptop', {
  filter: [
    'category = "laptops"',
    'brand IN ["Apple", "Lenovo", "Dell"]',
    'price >= 500 AND price <= 2000',
    'in_stock = true',
  ],
  facets: ['brand', 'category', 'rating'],
})

// Geo search (for store locators, nearby results)
await index.updateFilterableAttributes(['_geo'])
const nearby = await index.search('coffee', {
  filter: '_geoRadius(48.8566, 2.3522, 5000)',  // 5km radius from Paris center
  sort: ['_geoPoint(48.8566, 2.3522):asc'],
})
```

### Step 5: Relevancy Tuning

```javascript
// relevancy.js — Fine-tune ranking rules and synonyms
// Default ranking: words → typo → proximity → attribute → sort → exactness
await index.updateRankingRules([
  'words',
  'typo',
  'proximity',
  'attribute',
  'sort',
  'exactness',
  'price:asc',           // custom: cheaper products rank higher
])

// Synonyms
await index.updateSynonyms({
  'phone': ['smartphone', 'mobile', 'cell phone'],
  'laptop': ['notebook', 'ultrabook'],
  'tv': ['television', 'monitor', 'display'],
})

// Stop words (ignored in search)
await index.updateStopWords(['the', 'a', 'an', 'is', 'at', 'of'])

// Typo tolerance settings
await index.updateTypoTolerance({
  enabled: true,
  minWordSizeForTypos: { oneTypo: 4, twoTypos: 8 },
  disableOnAttributes: ['sku', 'isbn'],    // exact match for codes
})
```

### Step 6: Multi-Tenancy with Tenant Tokens

```javascript
// tenant_tokens.js — Secure multi-tenant search
// Each tenant can only search their own data
import { MeiliSearch } from 'meilisearch'
import crypto from 'crypto'

function generateTenantToken(apiKeyUid, tenantId, searchRules) {
  /**
   * Generate a JWT token that restricts search to a specific tenant.
   * Args:
   *   apiKeyUid: UID of the API key (not the key itself)
   *   tenantId: The tenant/organization ID to restrict access to
   *   searchRules: Index-level filter rules
   */
  const client = new MeiliSearch({ host: 'http://localhost:7700', apiKey: 'your-master-key' })

  return client.generateTenantToken(apiKeyUid, searchRules, {
    expiresAt: new Date(Date.now() + 3600 * 1000),  // 1 hour
  })
}

// Usage: frontend gets a token that auto-filters by their org_id
const token = generateTenantToken('key-uid', 'org_123', {
  products: { filter: 'org_id = org_123' },
})
```

### Step 7: Frontend Integration with InstantSearch

```javascript
// SearchUI.jsx — React component with Meilisearch InstantSearch
import { InstantSearch, SearchBox, Hits, RefinementList, Pagination } from 'react-instantsearch'
import { instantMeiliSearch } from '@meilisearch/instant-meilisearch'

const { searchClient } = instantMeiliSearch('http://localhost:7700', 'your-search-key')

export function SearchPage() {
  return (
    <InstantSearch indexName="products" searchClient={searchClient}>
      <SearchBox placeholder="Search products..." />
      <div style={{ display: 'flex', gap: '2rem' }}>
        <div>
          <h3>Brand</h3>
          <RefinementList attribute="brand" />
          <h3>Category</h3>
          <RefinementList attribute="category" />
        </div>
        <div>
          <Hits hitComponent={ProductHit} />
          <Pagination />
        </div>
      </div>
    </InstantSearch>
  )
}

function ProductHit({ hit }) {
  return (
    <div>
      <h4>{hit.title}</h4>
      <p>${hit.price} — {hit.brand}</p>
    </div>
  )
}
```

## Examples

### Example 1: Add instant search to an e-commerce product catalog
**User prompt:** "I have a Next.js e-commerce app with 50,000 products in PostgreSQL. Add a search bar with instant results, typo tolerance, and category/brand filters."

The agent will:
1. Deploy Meilisearch via Docker with a master key.
2. Write a sync script that reads products from PostgreSQL and indexes them in Meilisearch.
3. Configure searchable, filterable, and sortable attributes.
4. Add synonyms for common product terms.
5. Build a React search component using InstantSearch and `@meilisearch/instant-meilisearch`.
6. Set up a cron job or webhook to re-sync products when the database changes.

### Example 2: Build a documentation search for a developer portal
**User prompt:** "Add search to our documentation site. We have 500+ markdown files. Users should be able to search by title and content with highlighted results."

The agent will:
1. Write a script to parse all markdown files, extract frontmatter and content, and index them as documents.
2. Configure searchable attributes with `title` ranked above `content`.
3. Enable highlighting and content cropping for search result snippets.
4. Build a search modal component that shows results as the user types.

## Guidelines

- Meilisearch is designed for end-user-facing search (product catalogs, documentation, content). For log analytics or time-series data, use Elasticsearch or ClickHouse instead.
- Always set a master key in production — without it, anyone can modify your indexes.
- Use the search API key (not master key) on the frontend. Generate it via the keys API or use tenant tokens for multi-tenant apps.
- Index updates are asynchronous — `addDocuments` returns a task ID. Poll the task status or use webhooks for sync confirmation.
- Meilisearch stores all data in memory-mapped files. For 1M documents with moderate fields, expect ~1-4 GB RAM. Plan capacity accordingly.
- Re-index from your source of truth (database) on a schedule rather than trying to keep Meilisearch in perfect sync — it's simpler and more reliable.
