---
name: qdrant-memory
description: Use this skill for semantic search, long-term memory storage, and RAG (Retrieval Augmented Generation). Enables vector-based knowledge retrieval and persistent memory across sessions.
---

# Qdrant Vector Memory

This skill enables semantic search and long-term memory using Qdrant vector database.

## Problem Solved

Traditional keyword search:
- Exact match only
- Misses semantically similar content
- No context understanding

With Qdrant Vector Search:
- Semantic similarity matching
- Finds conceptually related information
- Understands context and meaning
- Persistent memory across sessions

## When to Use

- Storing knowledge for later retrieval
- Semantic code search across codebase
- Building RAG (Retrieval Augmented Generation) systems
- Long-term memory for AI agents
- Finding similar documents/code
- Knowledge base management

## Available Tools

### 1. qdrant-store
Stores text with vector embeddings for later retrieval.

```
Input: { "text": "React hooks are functions...", "metadata": { "topic": "react" } }
Output: Stored with vector embedding
```

### 2. qdrant-find
Finds semantically similar content.

```
Input: { "query": "how to manage state in React" }
Output: Related documents ranked by similarity
```

### 3. qdrant-delete
Removes stored memories by ID or filter.

```
Input: { "filter": { "topic": "outdated" } }
Output: Deleted matching entries
```

### 4. qdrant-list-collections
Lists all available collections.

```
Output: Collection names and stats
```

## Example Usage

### Store Knowledge

```
User: このReactパターンを覚えておいて

AI: [Calls qdrant-store]
    [Embeds content with sentence-transformers]
    [Stores in taisun_memory collection]

→ 永続的に保存され、後で検索可能
```

### Semantic Search

```
User: 以前話した状態管理のパターンは？

AI: [Calls qdrant-find with semantic query]
    [Returns top-k similar documents]
    [Provides context from stored memories]
```

### RAG for Code Generation

```
User: 前回実装したAPIパターンを参考に新しいエンドポイント作って

AI: [Searches for similar API implementations]
    [Retrieves relevant code patterns]
    [Generates new code based on retrieved context]
```

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                    TAISUN Agent                     │
└─────────────────────┬───────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│              Qdrant MCP Server                      │
│  ┌───────────────┐  ┌───────────────────────────┐  │
│  │ Embedding     │  │ Vector Store              │  │
│  │ (MiniLM-L6)   │──│ (taisun_memory collection)│  │
│  └───────────────┘  └───────────────────────────┘  │
└─────────────────────┬───────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│            Qdrant Server (localhost:6333)           │
│  - Persistent storage                               │
│  - Fast ANN search                                  │
│  - Metadata filtering                               │
└─────────────────────────────────────────────────────┘
```

## Required Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `QDRANT_URL` | Qdrant server URL | http://localhost:6333 |
| `QDRANT_COLLECTION_NAME` | Collection name | taisun_memory |
| `QDRANT_API_KEY` | API key (cloud only) | - |

## Setup

### Option 1: Local Docker (Recommended)

```bash
# Start Qdrant
docker run -p 6333:6333 -v $(pwd)/qdrant_data:/qdrant/storage qdrant/qdrant

# Verify
curl http://localhost:6333/health
```

### Option 2: Qdrant Cloud

1. Sign up at https://cloud.qdrant.io
2. Create a cluster
3. Get API key and URL
4. Set in .env:
   ```
   QDRANT_URL=https://xxx-xxx.aws.cloud.qdrant.io:6333
   QDRANT_API_KEY=your-api-key
   ```

## Integration with TAISUN

Qdrant MCP integrates with existing memory systems:

| Layer | System | Purpose |
|-------|--------|---------|
| 短期記憶 | taisun-proxy memory | セッション内コンテキスト |
| 長期記憶 | **Qdrant** | 永続的な知識・パターン |
| エピソード | claude-mem | 観察・決定の履歴 |

## Best Practices

1. **Store with meaningful metadata**
   ```
   { "topic": "react", "type": "pattern", "date": "2026-01-19" }
   ```

2. **Use specific queries**
   ```
   ❌ "前の話"
   ✅ "ReactのuseStateパターンについて"
   ```

3. **Regular cleanup**
   ```
   Outdated knowledge should be deleted to maintain relevance
   ```

4. **Combine with other tools**
   - Context7 for docs + Qdrant for project-specific knowledge
   - GPT Researcher for external + Qdrant for internal knowledge

## Sources

- [Qdrant MCP Server (Official)](https://github.com/qdrant/mcp-server-qdrant)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [mcp-server-qdrant PyPI](https://pypi.org/project/mcp-server-qdrant/)
