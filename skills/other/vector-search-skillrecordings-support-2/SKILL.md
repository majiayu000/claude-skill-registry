---
name: vector-search
description: Implement vector search for knowledge retrieval. Use when adding RAG, semantic search, knowledge base features, or context building for the agent.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Vector Search (Upstash Vector)

Context strategy is **retrieval-first**. The agent uses hybrid search (dense + sparse) to find relevant context.

## Upstash Vector Setup

```typescript
import { Index } from '@upstash/vector'

const index = new Index({
  url: process.env.UPSTASH_VECTOR_URL,
  token: process.env.UPSTASH_VECTOR_TOKEN,
})
```

## Document Types

Single index with type filters:

```typescript
interface VectorDocument {
  id: string
  data: string  // The text content (PII-redacted)
  metadata: {
    type: 'conversation' | 'knowledge' | 'response'
    appId: string

    // Conversation metadata
    category?: MessageCategory
    resolution?: 'refund' | 'transfer' | 'info' | 'escalated'
    customerSentiment?: 'positive' | 'neutral' | 'negative'
    touchCount?: number
    resolvedAt?: string

    // Knowledge metadata
    source?: 'docs' | 'faq' | 'policy' | 'canned-response'
    title?: string
    lastUpdated?: string

    // Response metadata
    trustScore?: number
    usageCount?: number
    conversationId?: string
  }
}
```

## PII Redaction (Required)

Always redact PII before embedding:

```typescript
function redactPII(text: string, knownNames: string[] = []): string {
  let redacted = text
    // Email
    .replace(/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g, '[EMAIL]')
    // Phone
    .replace(/(\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}/g, '[PHONE]')
    // Credit card
    .replace(/\b(?:\d{4}[-\s]?){3}\d{4}\b/g, '[CARD]')

  // Known names
  if (knownNames.length > 0) {
    redacted = redacted.replace(
      new RegExp(knownNames.map(escapeRegex).join('|'), 'gi'),
      '[NAME]'
    )
  }

  return redacted
}
```

## Upsert Pattern

```typescript
await index.upsert([{
  id: conversationId,
  data: redactPII(messageText),
  metadata: {
    type: 'conversation',
    appId,
    category,
    resolution
  }
}])
```

## Agent Context Building

Build context with parallel queries:

```typescript
async function buildAgentContext(message: string, appId: string) {
  const query = redactPII(message)

  const [similarTickets, knowledge, goodResponses] = await Promise.all([
    // Similar resolved tickets
    index.query({
      data: query,
      topK: 3,
      filter: `appId = '${appId}' AND type = 'conversation' AND resolution != 'escalated'`,
      includeData: true,
      includeMetadata: true,
    }),

    // Knowledge base articles
    index.query({
      data: query,
      topK: 5,
      filter: `appId = '${appId}' AND type = 'knowledge'`,
      includeData: true,
      includeMetadata: true,
    }),

    // High-trust responses
    index.query({
      data: query,
      topK: 3,
      filter: `appId = '${appId}' AND type = 'response' AND trustScore > 0.85`,
      includeData: true,
      includeMetadata: true,
    }),
  ])

  return { similarTickets, knowledge, goodResponses }
}
```

## Optional: Cohere Rerank

For higher quality results, use reranking:

```typescript
async function buildAgentContextWithRerank(message: string, appId: string) {
  const query = redactPII(message)

  // Get candidates from both dense and sparse search
  const [denseResults, sparseResults] = await Promise.all([
    index.query({ data: query, queryMode: 'DENSE', topK: 30, filter: `appId = '${appId}'`, includeData: true }),
    index.query({ data: query, queryMode: 'SPARSE', topK: 30, filter: `appId = '${appId}'`, includeData: true }),
  ])

  const candidates = dedupeById([...denseResults, ...sparseResults])

  // Rerank with Cohere
  const reranked = await cohere.rerank({
    model: 'rerank-v4.0-pro',
    query: message,
    documents: candidates.map(c => c.data),
    topN: 10,
  })

  const results = reranked.results.map(r => candidates[r.index])
  return {
    similarTickets: results.filter(r => r.metadata.type === 'conversation').slice(0, 3),
    knowledge: results.filter(r => r.metadata.type === 'knowledge').slice(0, 5),
    goodResponses: results.filter(r => r.metadata.type === 'response').slice(0, 3),
  }
}
```

## File Locations

- Vector client: `packages/core/src/vector/client.ts`
- Context building: `packages/core/src/vector/context.ts`
- PII redaction: `packages/core/src/vector/redact.ts`

## Reference Docs

For full details, see:
- `docs/support-app-prd/71-vector-search.md`
- `docs/support-app-prd/72-context-strategy.md`
