---
name: pinecone
description: Implements vector search with Pinecone for semantic similarity and RAG applications. Use when building embeddings-based search, recommendation systems, or retrieval-augmented generation.
---

# Pinecone

Vector database for similarity search. Store embeddings and query by semantic meaning for RAG, recommendations, and search.

## Quick Start

```bash
npm install @pinecone-database/pinecone
```

### Setup

```typescript
import { Pinecone } from '@pinecone-database/pinecone';

const pinecone = new Pinecone({
  apiKey: process.env.PINECONE_API_KEY!,
});

const index = pinecone.index('my-index');
```

## Index Management

### Create Index

```typescript
await pinecone.createIndex({
  name: 'my-index',
  dimension: 1536,  // OpenAI embedding dimension
  metric: 'cosine',  // cosine, euclidean, dotproduct
  spec: {
    serverless: {
      cloud: 'aws',
      region: 'us-east-1',
    },
  },
});
```

### List Indexes

```typescript
const indexes = await pinecone.listIndexes();
console.log(indexes);
```

### Describe Index

```typescript
const description = await pinecone.describeIndex('my-index');
console.log(description);
```

### Delete Index

```typescript
await pinecone.deleteIndex('my-index');
```

## Upsert Vectors

### Basic Upsert

```typescript
const index = pinecone.index('my-index');

await index.upsert([
  {
    id: 'doc-1',
    values: [0.1, 0.2, 0.3, ...],  // 1536 dimensions
    metadata: {
      title: 'Introduction to AI',
      category: 'technology',
      url: 'https://example.com/intro-ai',
    },
  },
  {
    id: 'doc-2',
    values: [0.4, 0.5, 0.6, ...],
    metadata: {
      title: 'Machine Learning Basics',
      category: 'technology',
      url: 'https://example.com/ml-basics',
    },
  },
]);
```

### With Namespace

```typescript
const namespace = index.namespace('articles');

await namespace.upsert([
  {
    id: 'article-1',
    values: embedding,
    metadata: { title: 'Article 1' },
  },
]);
```

### Batch Upsert

```typescript
const batchSize = 100;
const vectors = [...]; // Large array of vectors

for (let i = 0; i < vectors.length; i += batchSize) {
  const batch = vectors.slice(i, i + batchSize);
  await index.upsert(batch);
}
```

## Query Vectors

### Basic Query

```typescript
const queryEmbedding = [0.1, 0.2, 0.3, ...];

const results = await index.query({
  vector: queryEmbedding,
  topK: 10,
  includeMetadata: true,
  includeValues: false,
});

for (const match of results.matches) {
  console.log(`ID: ${match.id}, Score: ${match.score}`);
  console.log(`Metadata:`, match.metadata);
}
```

### With Metadata Filter

```typescript
const results = await index.query({
  vector: queryEmbedding,
  topK: 10,
  includeMetadata: true,
  filter: {
    category: { $eq: 'technology' },
  },
});
```

### Complex Filters

```typescript
const results = await index.query({
  vector: queryEmbedding,
  topK: 10,
  includeMetadata: true,
  filter: {
    $and: [
      { category: { $eq: 'technology' } },
      { year: { $gte: 2020 } },
      { tags: { $in: ['ai', 'ml'] } },
    ],
  },
});
```

### Filter Operators

| Operator | Description |
|----------|-------------|
| $eq | Equal to |
| $ne | Not equal to |
| $gt | Greater than |
| $gte | Greater than or equal |
| $lt | Less than |
| $lte | Less than or equal |
| $in | In array |
| $nin | Not in array |
| $exists | Field exists |
| $and | Logical AND |
| $or | Logical OR |

### Query by ID

```typescript
const results = await index.query({
  id: 'doc-1',
  topK: 10,
  includeMetadata: true,
});
```

### In Namespace

```typescript
const namespace = index.namespace('articles');

const results = await namespace.query({
  vector: queryEmbedding,
  topK: 5,
  includeMetadata: true,
});
```

## Fetch Vectors

```typescript
const fetchResult = await index.fetch(['doc-1', 'doc-2']);

for (const [id, record] of Object.entries(fetchResult.records)) {
  console.log(`ID: ${id}`);
  console.log(`Values: ${record.values}`);
  console.log(`Metadata: ${record.metadata}`);
}
```

## Update Vectors

```typescript
await index.update({
  id: 'doc-1',
  metadata: {
    title: 'Updated Title',
    lastModified: new Date().toISOString(),
  },
});
```

### Update Values

```typescript
await index.update({
  id: 'doc-1',
  values: newEmbedding,
  metadata: { updated: true },
});
```

## Delete Vectors

### By ID

```typescript
await index.deleteOne('doc-1');

// Or multiple
await index.deleteMany(['doc-1', 'doc-2', 'doc-3']);
```

### By Filter

```typescript
await index.deleteMany({
  filter: {
    category: { $eq: 'deprecated' },
  },
});
```

### Delete All in Namespace

```typescript
const namespace = index.namespace('temp');
await namespace.deleteAll();
```

## Statistics

```typescript
const stats = await index.describeIndexStats();

console.log('Total vectors:', stats.totalRecordCount);
console.log('Namespaces:', stats.namespaces);
```

## With OpenAI Embeddings

```typescript
import { Pinecone } from '@pinecone-database/pinecone';
import OpenAI from 'openai';

const pinecone = new Pinecone();
const openai = new OpenAI();
const index = pinecone.index('my-index');

// Create embedding
async function embed(text: string) {
  const response = await openai.embeddings.create({
    model: 'text-embedding-3-small',
    input: text,
  });
  return response.data[0].embedding;
}

// Upsert document
async function upsertDocument(id: string, text: string, metadata: object) {
  const embedding = await embed(text);
  await index.upsert([
    {
      id,
      values: embedding,
      metadata: { text, ...metadata },
    },
  ]);
}

// Search
async function search(query: string, topK = 5) {
  const queryEmbedding = await embed(query);
  const results = await index.query({
    vector: queryEmbedding,
    topK,
    includeMetadata: true,
  });
  return results.matches;
}
```

## RAG Pattern

```typescript
import { Pinecone } from '@pinecone-database/pinecone';
import OpenAI from 'openai';

const pinecone = new Pinecone();
const openai = new OpenAI();
const index = pinecone.index('knowledge-base');

async function ragQuery(question: string) {
  // 1. Embed the question
  const embedding = await openai.embeddings.create({
    model: 'text-embedding-3-small',
    input: question,
  });

  // 2. Search for relevant documents
  const results = await index.query({
    vector: embedding.data[0].embedding,
    topK: 5,
    includeMetadata: true,
  });

  // 3. Build context from results
  const context = results.matches
    .map((match) => match.metadata?.text)
    .filter(Boolean)
    .join('\n\n');

  // 4. Generate answer with context
  const completion = await openai.chat.completions.create({
    model: 'gpt-4o',
    messages: [
      {
        role: 'system',
        content: `Answer based on this context:\n\n${context}`,
      },
      { role: 'user', content: question },
    ],
  });

  return completion.choices[0].message.content;
}
```

## Next.js API Routes

```typescript
// app/api/search/route.ts
import { Pinecone } from '@pinecone-database/pinecone';
import OpenAI from 'openai';
import { NextRequest, NextResponse } from 'next/server';

const pinecone = new Pinecone();
const openai = new OpenAI();

export async function POST(request: NextRequest) {
  const { query } = await request.json();

  // Embed query
  const embedding = await openai.embeddings.create({
    model: 'text-embedding-3-small',
    input: query,
  });

  // Search
  const index = pinecone.index('my-index');
  const results = await index.query({
    vector: embedding.data[0].embedding,
    topK: 10,
    includeMetadata: true,
  });

  return NextResponse.json({
    results: results.matches.map((match) => ({
      id: match.id,
      score: match.score,
      ...match.metadata,
    })),
  });
}
```

### Upsert Endpoint

```typescript
// app/api/upsert/route.ts
import { Pinecone } from '@pinecone-database/pinecone';
import OpenAI from 'openai';
import { NextRequest, NextResponse } from 'next/server';

const pinecone = new Pinecone();
const openai = new OpenAI();

export async function POST(request: NextRequest) {
  const { id, text, metadata } = await request.json();

  // Create embedding
  const embedding = await openai.embeddings.create({
    model: 'text-embedding-3-small',
    input: text,
  });

  // Upsert to Pinecone
  const index = pinecone.index('my-index');
  await index.upsert([
    {
      id,
      values: embedding.data[0].embedding,
      metadata: { text, ...metadata },
    },
  ]);

  return NextResponse.json({ success: true, id });
}
```

## TypeScript Types

```typescript
import { Pinecone, RecordMetadata } from '@pinecone-database/pinecone';

interface ArticleMetadata extends RecordMetadata {
  title: string;
  content: string;
  category: string;
  publishedAt: string;
}

const pinecone = new Pinecone();
const index = pinecone.index<ArticleMetadata>('articles');

// Type-safe metadata
await index.upsert([
  {
    id: 'article-1',
    values: embedding,
    metadata: {
      title: 'My Article',
      content: 'Article content...',
      category: 'tech',
      publishedAt: new Date().toISOString(),
    },
  },
]);

// Type-safe query results
const results = await index.query({
  vector: queryEmbedding,
  topK: 5,
  includeMetadata: true,
});

for (const match of results.matches) {
  console.log(match.metadata?.title);  // TypeScript knows this is string
}
```

## Environment Variables

```bash
PINECONE_API_KEY=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

## Best Practices

1. **Batch upserts** - Use batches of 100 vectors
2. **Use namespaces** - Organize vectors logically
3. **Include metadata** - Store text for retrieval
4. **Choose right dimension** - Match your embedding model
5. **Use filters** - Reduce search space
6. **Cache embeddings** - Avoid redundant API calls
7. **Monitor usage** - Track vector count and queries
