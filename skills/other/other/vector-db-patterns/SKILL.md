---
name: vector-db-patterns
description: Embedding strategies, ANN algorithms, hybrid search, RAG chunking strategies, and reranking for semantic search and retrieval.
---

# Vector DB Patterns

Semantic search and retrieval-augmented generation (RAG) patterns with vector databases.

## Embedding Strategies

```typescript
import { OpenAI } from 'openai'

const openai = new OpenAI()

// Batch embedding for efficiency (max 2048 inputs per request for text-embedding-3-small)
async function embedTexts(texts: string[]): Promise<number[][]> {
  const BATCH_SIZE = 2048
  const allEmbeddings: number[][] = []

  for (let i = 0; i < texts.length; i += BATCH_SIZE) {
    const batch = texts.slice(i, i + BATCH_SIZE)
    const response = await openai.embeddings.create({
      model: 'text-embedding-3-small',  // 1536 dimensions, good cost/quality
      input: batch,
      dimensions: 512,                  // Reduce dims for speed (Matryoshka)
    })
    allEmbeddings.push(...response.data.map(d => d.embedding))
  }

  return allEmbeddings
}

// Embed with prefix for asymmetric retrieval
async function embedForSearch(query: string): Promise<number[]> {
  const [embedding] = await embedTexts([`search_query: ${query}`])
  return embedding
}

async function embedForStorage(document: string): Promise<number[]> {
  const [embedding] = await embedTexts([`search_document: ${document}`])
  return embedding
}
```

## Chunking Strategies for RAG

```typescript
interface Chunk {
  id: string
  text: string
  metadata: {
    sourceId: string
    chunkIndex: number
    startChar: number
    endChar: number
  }
}

// Recursive character splitting with overlap
function chunkText(
  text: string,
  chunkSize: number = 512,
  overlap: number = 50
): Chunk[] {
  const separators = ['\n\n', '\n', '. ', ' ']
  return recursiveSplit(text, separators, chunkSize, overlap)
}

function recursiveSplit(
  text: string,
  separators: string[],
  chunkSize: number,
  overlap: number
): Chunk[] {
  if (text.length <= chunkSize) {
    return [{ id: crypto.randomUUID(), text, metadata: {} as any }]
  }

  const separator = separators.find(s => text.includes(s)) ?? ''
  const parts = text.split(separator)
  const chunks: Chunk[] = []
  let current = ''

  for (const part of parts) {
    const candidate = current ? current + separator + part : part
    if (candidate.length > chunkSize && current) {
      chunks.push({ id: crypto.randomUUID(), text: current.trim(), metadata: {} as any })
      // Overlap: keep last N chars of previous chunk
      const overlapText = current.slice(-overlap)
      current = overlapText + separator + part
    } else {
      current = candidate
    }
  }
  if (current.trim()) {
    chunks.push({ id: crypto.randomUUID(), text: current.trim(), metadata: {} as any })
  }

  return chunks
}

// Semantic chunking: split at topic boundaries using embeddings
async function semanticChunk(text: string, threshold: number = 0.3): Promise<Chunk[]> {
  const sentences = text.match(/[^.!?]+[.!?]+/g) ?? [text]
  const embeddings = await embedTexts(sentences)
  const chunks: string[][] = [[sentences[0]]]

  for (let i = 1; i < sentences.length; i++) {
    const similarity = cosineSimilarity(embeddings[i - 1], embeddings[i])
    if (similarity < threshold) {
      // Low similarity = topic boundary = new chunk
      chunks.push([sentences[i]])
    } else {
      chunks[chunks.length - 1].push(sentences[i])
    }
  }

  return chunks.map((sentences, i) => ({
    id: crypto.randomUUID(),
    text: sentences.join(' ').trim(),
    metadata: { sourceId: '', chunkIndex: i, startChar: 0, endChar: 0 }
  }))
}
```

## Vector Search with Metadata Filtering

```typescript
// Using Pinecone
import { Pinecone } from '@pinecone-database/pinecone'

const pinecone = new Pinecone()
const index = pinecone.index('documents')

// Upsert with metadata
async function indexDocument(doc: Document, chunks: Chunk[]): Promise<void> {
  const embeddings = await embedTexts(chunks.map(c => c.text))

  const vectors = chunks.map((chunk, i) => ({
    id: chunk.id,
    values: embeddings[i],
    metadata: {
      text: chunk.text,
      sourceId: doc.id,
      sourceTitle: doc.title,
      category: doc.category,
      createdAt: doc.createdAt.toISOString(),
      chunkIndex: i,
    }
  }))

  // Upsert in batches of 100
  for (let i = 0; i < vectors.length; i += 100) {
    await index.upsert(vectors.slice(i, i + 100))
  }
}

// Query with metadata filter
async function searchDocuments(
  query: string,
  filters?: { category?: string; after?: Date },
  topK: number = 10
): Promise<SearchResult[]> {
  const queryEmbedding = await embedForSearch(query)

  const filter: Record<string, any> = {}
  if (filters?.category) {
    filter.category = { $eq: filters.category }
  }
  if (filters?.after) {
    filter.createdAt = { $gte: filters.after.toISOString() }
  }

  const results = await index.query({
    vector: queryEmbedding,
    topK,
    includeMetadata: true,
    filter: Object.keys(filter).length > 0 ? filter : undefined,
  })

  return results.matches.map(m => ({
    id: m.id,
    score: m.score ?? 0,
    text: m.metadata?.text as string,
    sourceId: m.metadata?.sourceId as string,
    sourceTitle: m.metadata?.sourceTitle as string,
  }))
}
```

## Hybrid Search (Vector + Keyword)

```typescript
// Combine vector similarity with BM25 keyword matching
async function hybridSearch(
  query: string,
  topK: number = 10,
  alpha: number = 0.7  // 0.7 = 70% semantic, 30% keyword
): Promise<SearchResult[]> {
  // Run both searches in parallel
  const [vectorResults, keywordResults] = await Promise.all([
    vectorSearch(query, topK * 2),
    keywordSearch(query, topK * 2),  // BM25 via Elasticsearch
  ])

  // Reciprocal Rank Fusion (RRF)
  const k = 60  // RRF constant
  const scores = new Map<string, number>()

  vectorResults.forEach((r, rank) => {
    const current = scores.get(r.id) ?? 0
    scores.set(r.id, current + alpha * (1 / (k + rank + 1)))
  })

  keywordResults.forEach((r, rank) => {
    const current = scores.get(r.id) ?? 0
    scores.set(r.id, current + (1 - alpha) * (1 / (k + rank + 1)))
  })

  // Sort by combined score, return top K
  const allResults = [...vectorResults, ...keywordResults]
  const uniqueResults = new Map(allResults.map(r => [r.id, r]))

  return [...scores.entries()]
    .sort((a, b) => b[1] - a[1])
    .slice(0, topK)
    .map(([id, score]) => ({
      ...uniqueResults.get(id)!,
      score,
    }))
}
```

## Reranking

```typescript
// Cross-encoder reranking: slower but much more accurate than bi-encoder
async function rerankResults(
  query: string,
  results: SearchResult[],
  topK: number = 5
): Promise<SearchResult[]> {
  // Use Cohere Rerank or cross-encoder model
  const response = await fetch('https://api.cohere.ai/v1/rerank', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${process.env.COHERE_API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      model: 'rerank-english-v3.0',
      query,
      documents: results.map(r => r.text),
      top_n: topK,
      return_documents: false,
    }),
  })

  const data = await response.json()

  return data.results.map((r: any) => ({
    ...results[r.index],
    score: r.relevance_score,
  }))
}

// RAG pipeline: retrieve → rerank → generate
async function ragQuery(query: string): Promise<string> {
  // Step 1: Retrieve candidates (broad, fast)
  const candidates = await hybridSearch(query, 20)

  // Step 2: Rerank (narrow, accurate)
  const reranked = await rerankResults(query, candidates, 5)

  // Step 3: Generate answer with context
  const context = reranked.map(r => r.text).join('\n\n')
  const response = await openai.chat.completions.create({
    model: 'gpt-4o',
    messages: [
      { role: 'system', content: `Answer based on the context below.\n\nContext:\n${context}` },
      { role: 'user', content: query },
    ],
  })

  return response.choices[0].message.content!
}
```

## Checklist

- [ ] Chunk size 256-1024 tokens with 10-20% overlap
- [ ] Asymmetric embedding prefixes for query vs document
- [ ] Metadata stored alongside vectors for pre-filtering
- [ ] Hybrid search (vector + BM25) for best recall
- [ ] Reranking top-N candidates with cross-encoder
- [ ] Batch embedding calls (never one-by-one)
- [ ] Dimension reduction (Matryoshka) for cost/speed optimization
- [ ] Evaluation: hit rate, MRR, NDCG on test queries

## Anti-Patterns

- Embedding entire documents as single vectors (context lost, poor retrieval)
- Fixed-size chunking ignoring sentence/paragraph boundaries
- Only vector search without keyword fallback (misses exact matches)
- Embedding queries and documents identically (asymmetric retrieval needs prefixes)
- Not evaluating retrieval quality (building blind)
- Storing embeddings without source text (can't debug or rerank)
