---
name: xata
description: Expert guidance for Xata, the serverless data platform that combines PostgreSQL, Elasticsearch, and AI capabilities in a single API. Helps developers build applications with full-text search, vector similarity search, file attachments, and branching — all through a type-safe TypeScript SDK.
license: Apache-2.0
compatibility: No special requirements
metadata:
  author: terminal-skills
  version: 1.0.0
  category: development
  tags:
  - database
  - serverless
  - search
  - postgres
  - ai
---

# Xata — Serverless Data Platform


## Overview


Xata, the serverless data platform that combines PostgreSQL, Elasticsearch, and AI capabilities in a single API. Helps developers build applications with full-text search, vector similarity search, file attachments, and branching — all through a type-safe TypeScript SDK.


## Instructions

### Setup and Schema

```bash
# Install Xata CLI
npm install -g @xata.io/cli

# Authenticate
xata auth login

# Initialize in your project
xata init --db https://your-workspace.xata.sh/db/my-app

# This generates a typed client: src/xata.ts
```

```typescript
// Schema defined in .xata/schema.json or via dashboard
// Example: Articles with full-text search and vector embeddings
{
  "tables": [
    {
      "name": "articles",
      "columns": [
        { "name": "title", "type": "string" },
        { "name": "content", "type": "text" },
        { "name": "author", "type": "link", "link": { "table": "users" } },
        { "name": "tags", "type": "multiple" },
        { "name": "published", "type": "bool", "defaultValue": "false" },
        { "name": "publishedAt", "type": "datetime" },
        { "name": "embedding", "type": "vector", "vector": { "dimension": 1536 } },
        { "name": "cover", "type": "file" }
      ]
    }
  ]
}
```

### Type-Safe CRUD

```typescript
// src/lib/db.ts — Xata client (auto-generated types)
import { getXataClient } from "./xata";

const xata = getXataClient();

// Create
async function createArticle(data: {
  title: string;
  content: string;
  authorId: string;
  tags: string[];
}) {
  const article = await xata.db.articles.create({
    title: data.title,
    content: data.content,
    author: data.authorId,       // Link to users table
    tags: data.tags,
    published: false,
  });
  return article;               // Fully typed: article.id, article.title, etc.
}

// Read with relationships
async function getArticle(id: string) {
  const article = await xata.db.articles.read(id, [
    "title", "content", "publishedAt",
    "author.name", "author.email",    // Resolve linked records
  ]);
  return article;
}

// Query with filters
async function getPublishedArticles(page = 1) {
  const results = await xata.db.articles
    .filter({
      published: true,
      publishedAt: { $ge: new Date("2026-01-01") },
    })
    .sort("publishedAt", "desc")
    .getPaginated({
      pagination: { size: 20, offset: (page - 1) * 20 },
    });

  return {
    articles: results.records,
    hasMore: results.hasNextPage(),
    total: results.totalCount,
  };
}

// Update
async function publishArticle(id: string) {
  await xata.db.articles.update(id, {
    published: true,
    publishedAt: new Date(),
  });
}

// Delete
async function deleteArticle(id: string) {
  await xata.db.articles.delete(id);
}
```

### Full-Text Search

```typescript
// Xata has built-in Elasticsearch — no separate search service needed

// Basic search
async function searchArticles(query: string) {
  const results = await xata.db.articles.search(query, {
    target: ["title", "content"],    // Which columns to search
    fuzziness: 1,                     // Allow 1 typo
    prefix: "phrase",                 // Prefix matching for autocomplete
    filter: { published: true },      // Combined with search
    highlight: { enabled: true },     // Return highlighted snippets
    page: { size: 10 },
  });

  return results.records.map((record) => ({
    id: record.id,
    title: record.title,
    snippet: record.getMetadata().highlight?.content ?? record.content?.slice(0, 200),
    score: record.getMetadata().score,
  }));
}

// Aggregate search results
async function searchWithFacets(query: string) {
  const results = await xata.db.articles.search(query, {
    target: ["title", "content"],
    filter: { published: true },
  });

  // Group results by tag
  const tagCounts: Record<string, number> = {};
  for (const record of results.records) {
    for (const tag of record.tags ?? []) {
      tagCounts[tag] = (tagCounts[tag] ?? 0) + 1;
    }
  }

  return { articles: results.records, facets: tagCounts };
}
```

### AI / Vector Search

```typescript
// Vector similarity search (RAG, recommendations)
async function findSimilar(articleId: string) {
  const article = await xata.db.articles.read(articleId);
  if (!article?.embedding) return [];

  // Find articles with similar embeddings
  const results = await xata.db.articles.vectorSearch("embedding", article.embedding, {
    size: 5,
    filter: {
      published: true,
      id: { $isNot: articleId },     // Exclude the source article
    },
  });

  return results.records;
}

// Ask AI (built-in RAG — search + LLM answer)
async function askQuestion(question: string) {
  const result = await xata.db.articles.ask(question, {
    searchType: "keyword",           // "keyword" | "vector" | "hybrid"
    rules: [
      "Answer based only on the provided context",
      "If uncertain, say you don't know",
      "Keep answers under 3 sentences",
    ],
  });

  return {
    answer: result.answer,
    records: result.records,         // Source articles used for the answer
  };
}
```

### File Attachments

```typescript
// Upload files directly to records
async function uploadCoverImage(articleId: string, file: File) {
  const base64 = await fileToBase64(file);
  await xata.db.articles.update(articleId, {
    cover: {
      name: file.name,
      mediaType: file.type,
      base64Content: base64,
    },
  });
}

// Get file URL
async function getCoverUrl(articleId: string) {
  const article = await xata.db.articles.read(articleId);
  return article?.cover?.url;         // Signed URL for the file
}
```

### Branching

```bash
# Create a branch (like git — isolated copy of schema + data)
xata branch create staging

# Make schema changes on the branch
xata schema edit --branch staging

# Merge branch to main (applies schema migration)
xata branch merge staging
```

## Installation

```bash
# CLI
npm install -g @xata.io/cli

# Client SDK
npm install @xata.io/client

# Initialize in project (generates typed client)
xata init
```


## Examples


### Example 1: Setting up Xata with a custom configuration

**User request:**

```
I just installed Xata. Help me configure it for my TypeScript + React workflow with my preferred keybindings.
```

The agent creates the configuration file with TypeScript-aware settings, configures relevant plugins/extensions for React development, sets up keyboard shortcuts matching the user's preferences, and verifies the setup works correctly.

### Example 2: Extending Xata with custom functionality

**User request:**

```
I want to add a custom type-safe crud to Xata. How do I build one?
```

The agent scaffolds the extension/plugin project, implements the core functionality following Xata's API patterns, adds configuration options, and provides testing instructions to verify it works end-to-end.


## Guidelines

1. **Use the generated client** — `xata init` creates a typed client; never construct queries manually
2. **Search over queries** — If users are looking for content, use `.search()` instead of `.filter()`; it's faster and supports fuzzy matching
3. **Vectors for recommendations** — Store embeddings for semantic search and "similar articles" features; Xata handles the vector index
4. **Ask for RAG** — The `.ask()` method does retrieval + generation in one call; no need to build RAG from scratch
5. **Branches for migrations** — Test schema changes on a branch before merging to main; matches the git workflow developers already know
6. **File attachments vs external storage** — Use Xata's file type for per-record files (avatars, covers); use S3 for bulk file storage
7. **Filters + search** — Combine `.search()` with `filter` for faceted search (search "react" filtered to "tutorial" tag)
8. **Pagination with cursors** — Use `getPaginated()` for cursor-based pagination; more efficient than offset for large datasets
