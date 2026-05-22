---
name: pinecone-vector
description: Pinecone vector database for similarity search and RAG
version: 1.0.0
category: database
allowed-tools: [Bash, Read, WebFetch]
required-agents: [llm-architect, database-architect]
recommended-agents: [developer, qa]
context-cost: medium
triggers:
  - 'vector search'
  - 'similarity search'
  - 'embedding storage'
  - 'RAG system'
  - 'semantic search'
  - 'pinecone'
  - 'vector database'
---

# Pinecone Vector Skill

## Purpose

Provides vector database operations for similarity search, semantic search, and Retrieval-Augmented Generation (RAG) systems using Pinecone. Enables efficient storage and retrieval of high-dimensional embeddings for AI/LLM applications.

## When to Use

- **Semantic Search**: Building search systems that understand meaning, not just keywords
- **RAG Systems**: Storing and retrieving context for LLM applications
- **Recommendation Engines**: Finding similar items based on vector embeddings
- **Document Retrieval**: Searching through large document collections
- **Embedding Storage**: Managing high-dimensional vectors from ML models

## Tool Categories

### Index Management

| Tool             | Purpose                           | Confirmation Required |
| ---------------- | --------------------------------- | --------------------- |
| `list-indexes`   | List all Pinecone indexes         | No                    |
| `describe-index` | Get index configuration and stats | No                    |
| `create-index`   | Create new vector index           | **YES**               |
| `delete-index`   | Delete vector index permanently   | **YES**               |

### Vector Operations

| Tool             | Purpose                     | Confirmation Required |
| ---------------- | --------------------------- | --------------------- |
| `upsert`         | Insert or update vectors    | No                    |
| `query`          | Similarity search by vector | No                    |
| `fetch`          | Retrieve vectors by ID      | No                    |
| `delete-vectors` | Delete specific vectors     | No                    |

### Index Statistics

| Tool              | Purpose                                         | Confirmation Required |
| ----------------- | ----------------------------------------------- | --------------------- |
| `describe-stats`  | Get index statistics (vector count, namespaces) | No                    |
| `list-namespaces` | List all namespaces in index                    | No                    |

### Collections

| Tool                | Purpose                               | Confirmation Required |
| ------------------- | ------------------------------------- | --------------------- |
| `list-collections`  | List all collections                  | No                    |
| `create-collection` | Create collection from index snapshot | **YES**               |
| `delete-collection` | Delete collection permanently         | **YES**               |

## Usage Patterns

### 1. Initialize Pinecone Connection

```typescript
import { Pinecone } from '@pinecone-database/pinecone';

const pinecone = new Pinecone({
  apiKey: process.env.PINECONE_API_KEY, // NEVER hardcode
});
```

### 2. Create Index for Embeddings

```typescript
// Create index with proper configuration
await pinecone.createIndex({
  name: 'semantic-search',
  dimension: 1536, // Match your embedding model (e.g., OpenAI ada-002)
  metric: 'cosine', // or 'euclidean', 'dotproduct'
  spec: {
    serverless: {
      cloud: 'aws',
      region: 'us-east-1',
    },
  },
});
```

### 3. Upsert Vectors

```typescript
const index = pinecone.index('semantic-search');

await index.upsert([
  {
    id: 'doc-1',
    values: [0.1, 0.2, ...], // 1536-dimensional vector
    metadata: {
      title: 'Getting Started Guide',
      category: 'documentation',
      url: '/docs/getting-started'
    }
  },
  {
    id: 'doc-2',
    values: [0.3, 0.4, ...],
    metadata: {
      title: 'API Reference',
      category: 'documentation',
      url: '/docs/api'
    }
  }
]);
```

### 4. Query for Similar Vectors

```typescript
const index = pinecone.index('semantic-search');

const results = await index.query({
  vector: queryEmbedding, // Your query vector
  topK: 10, // Return top 10 matches
  includeMetadata: true,
  filter: {
    category: { $eq: 'documentation' },
  },
});

// Process results
results.matches.forEach(match => {
  console.log(`Score: ${match.score}, Title: ${match.metadata.title}`);
});
```

### 5. Fetch Vectors by ID

```typescript
const index = pinecone.index('semantic-search');

const vectors = await index.fetch(['doc-1', 'doc-2']);

console.log(vectors.vectors['doc-1'].metadata);
```

### 6. Delete Vectors

```typescript
const index = pinecone.index('semantic-search');

// Delete by ID
await index.deleteOne('doc-1');

// Delete by filter
await index.deleteMany({
  category: { $eq: 'deprecated' },
});

// Delete all vectors in namespace
await index.deleteAll({ namespace: 'test' });
```

### 7. Get Index Statistics

```typescript
const index = pinecone.index('semantic-search');

const stats = await index.describeIndexStats();

console.log(`Total vectors: ${stats.totalRecordCount}`);
console.log(`Namespaces: ${Object.keys(stats.namespaces).join(', ')}`);
```

## Security Requirements

### API Key Protection

**CRITICAL: Never expose Pinecone API key**

```typescript
// ✅ CORRECT: Use environment variables
const pinecone = new Pinecone({
  apiKey: process.env.PINECONE_API_KEY,
});

// ❌ WRONG: Hardcoded API key
const pinecone = new Pinecone({
  apiKey: 'pk-abc123...', // NEVER DO THIS
});
```

### Environment Configuration

**.env.local** (local development):

```bash
PINECONE_API_KEY=your-api-key-here
PINECONE_ENVIRONMENT=us-east-1-aws
```

**.env.example** (committed to git):

```bash
PINECONE_API_KEY=your-pinecone-api-key
PINECONE_ENVIRONMENT=your-pinecone-environment
```

### Destructive Operations

**Require user confirmation before**:

- Creating indexes (costs apply)
- Deleting indexes (permanent data loss)
- Creating collections (costs apply)
- Deleting collections (permanent data loss)

**Confirmation Pattern**:

```typescript
// Before destructive operation
console.warn('⚠️ WARNING: This will permanently delete index "semantic-search"');
console.warn('All vectors and metadata will be lost.');
const confirmed = await askUserConfirmation('Proceed with deletion?');

if (!confirmed) {
  console.log('Operation cancelled');
  return;
}

await pinecone.deleteIndex('semantic-search');
```

## Agent Integration

### Primary Agents

**llm-architect** (Primary):

- Design RAG system architecture
- Choose index configuration (dimension, metric)
- Design metadata schema
- Optimize query patterns

**database-architect** (Primary):

- Index capacity planning
- Namespace strategy
- Performance optimization
- Cost optimization

### Supporting Agents

**developer**:

- Implement vector operations
- Integrate with embedding models
- Build search APIs
- Handle error cases

**qa**:

- Test similarity search accuracy
- Validate metadata filtering
- Performance testing
- Load testing

## Best Practices

### 1. Index Configuration

**Choose the right metric**:

- `cosine`: Most common for normalized embeddings (default)
- `euclidean`: For absolute distance
- `dotproduct`: For non-normalized embeddings

**Set correct dimension**:

- OpenAI ada-002: 1536
- OpenAI text-embedding-3-small: 1536
- OpenAI text-embedding-3-large: 3072
- Cohere embed-english-v3.0: 1024

### 2. Metadata Design

**Use metadata for filtering**:

```typescript
metadata: {
  category: 'documentation',
  language: 'en',
  published_date: '2024-01-15',
  author: 'john-doe',
  tags: ['api', 'tutorial']
}
```

**Filter during query**:

```typescript
await index.query({
  vector: queryVector,
  topK: 10,
  filter: {
    category: { $eq: 'documentation' },
    language: { $eq: 'en' },
    published_date: { $gte: '2024-01-01' },
  },
});
```

### 3. Batch Operations

**Upsert in batches (100-200 vectors)**:

```typescript
const BATCH_SIZE = 100;

for (let i = 0; i < vectors.length; i += BATCH_SIZE) {
  const batch = vectors.slice(i, i + BATCH_SIZE);
  await index.upsert(batch);
}
```

### 4. Namespace Strategy

**Use namespaces for multi-tenancy**:

```typescript
// Separate data by tenant
const tenantIndex = index.namespace('tenant-123');

await tenantIndex.upsert(vectors);
await tenantIndex.query({ vector: queryVector, topK: 10 });
```

### 5. Error Handling

**Handle rate limits and retries**:

```typescript
async function upsertWithRetry(index, vectors, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      await index.upsert(vectors);
      return;
    } catch (error) {
      if (error.status === 429) {
        // Rate limited - wait and retry
        await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)));
        continue;
      }
      throw error;
    }
  }
  throw new Error('Max retries exceeded');
}
```

## Common Workflows

### RAG System Setup

1. **Create index**: `create-index` with proper dimension and metric
2. **Generate embeddings**: Use OpenAI/Cohere to create vectors
3. **Upsert documents**: Store vectors with metadata
4. **Query for context**: Retrieve relevant documents for LLM prompts
5. **Monitor stats**: Track vector count and namespace usage

### Semantic Search Implementation

1. **Design metadata schema**: Define filterable fields
2. **Create index**: Configure for search use case
3. **Index content**: Upsert vectors with rich metadata
4. **Build query API**: Expose search endpoint
5. **Optimize queries**: Use filters and adjust topK

### Document Collection Management

1. **Create collections**: Snapshot indexes for versioning
2. **Test with collections**: Experiment without affecting production
3. **Restore from collections**: Create new indexes from snapshots
4. **Delete old collections**: Clean up unused snapshots

## Performance Considerations

### Query Optimization

- **Use filters**: Reduce search space with metadata filters
- **Adjust topK**: Balance accuracy vs speed (typical: 10-100)
- **Use namespaces**: Isolate tenant data for faster queries

### Cost Optimization

- **Choose right plan**: Serverless (usage-based) vs Pod (fixed)
- **Monitor usage**: Track query count and storage
- **Delete unused indexes**: Avoid paying for idle indexes
- **Use collections wisely**: Snapshots cost storage

### Indexing Best Practices

- **Batch upserts**: Group vectors (100-200 per batch)
- **Async operations**: Don't block on upserts
- **Monitor quotas**: Track API rate limits
- **Use pagination**: For large fetch/delete operations

## Error Handling

### Common Errors

| Error                     | Cause                  | Solution                        |
| ------------------------- | ---------------------- | ------------------------------- |
| `404 Index not found`     | Index doesn't exist    | Create index first              |
| `400 Dimension mismatch`  | Vector dimension wrong | Match embedding model dimension |
| `429 Rate limit exceeded` | Too many requests      | Implement retry with backoff    |
| `401 Unauthorized`        | Invalid API key        | Check PINECONE_API_KEY          |

### Validation

**Before operations**:

```typescript
// Validate index exists
const indexes = await pinecone.listIndexes();
if (!indexes.indexes.some(i => i.name === 'semantic-search')) {
  throw new Error('Index "semantic-search" not found');
}

// Validate vector dimension
const indexInfo = await pinecone.describeIndex('semantic-search');
if (vector.length !== indexInfo.dimension) {
  throw new Error(
    `Vector dimension mismatch: expected ${indexInfo.dimension}, got ${vector.length}`
  );
}
```

## Integration Examples

### RAG with OpenAI

```typescript
import { Pinecone } from '@pinecone-database/pinecone';
import OpenAI from 'openai';

const pinecone = new Pinecone({ apiKey: process.env.PINECONE_API_KEY });
const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

async function ragQuery(question: string) {
  // 1. Generate embedding for question
  const embedding = await openai.embeddings.create({
    model: 'text-embedding-ada-002',
    input: question,
  });

  // 2. Query Pinecone for relevant context
  const index = pinecone.index('knowledge-base');
  const results = await index.query({
    vector: embedding.data[0].embedding,
    topK: 5,
    includeMetadata: true,
  });

  // 3. Build context from results
  const context = results.matches.map(match => match.metadata.text).join('\n\n');

  // 4. Generate answer with LLM
  const completion = await openai.chat.completions.create({
    model: 'gpt-4',
    messages: [
      { role: 'system', content: 'Answer based on the provided context.' },
      { role: 'user', content: `Context:\n${context}\n\nQuestion: ${question}` },
    ],
  });

  return completion.choices[0].message.content;
}
```

## Troubleshooting

### Index Creation Fails

**Check**:

- API key is valid
- Dimension matches embedding model
- Region is supported
- Account has quota available

### Query Returns No Results

**Check**:

- Vectors were successfully upserted
- Query vector dimension matches index
- Filters aren't too restrictive
- Namespace matches upserted data

### Slow Queries

**Optimize**:

- Add metadata filters to reduce search space
- Use appropriate topK value
- Check index stats for vector count
- Consider namespace partitioning

## References

- **Official Docs**: https://docs.pinecone.io/
- **Node.js Client**: https://github.com/pinecone-io/pinecone-ts-client
- **Best Practices**: https://docs.pinecone.io/docs/best-practices
- **Pricing**: https://www.pinecone.io/pricing/

## Related Skills

- `repo-rag`: Codebase semantic search
- `text-to-sql`: SQL query generation
- `memory-manager`: Conversation context storage
- `classifier`: Metadata categorization
- `summarizer`: Document summarization for embeddings

## Version History

- **1.0.0** (2026-01-05): Initial Pinecone vector skill documentation
