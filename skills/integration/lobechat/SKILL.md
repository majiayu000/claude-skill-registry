---
name: lobechat
description: Access LobeChat for AI chat, knowledge base queries, and multi-model routing.
metadata: {"moltbot":{"emoji":"🧠","requires":{"env":["LOBE_URL"]}}}
---

# LobeChat Integration Skill

Access LobeChat for AI chat, knowledge base queries (RAG), and multi-model routing.

## Quick Reference

```bash
# Health check
curl -s "$LOBE_URL/api/health"

# Check via internal network
curl -s "http://lobe-chat:3210/api/health"
```

**Required env var**: `LOBE_URL`

## Services

| Service | Internal URL | Purpose |
|---------|--------------|---------|
| LobeChat | http://lobe-chat:3210 | AI chat interface |
| Casdoor | http://lobe-casdoor:8000 | SSO authentication |
| MinIO | http://lobe-minio:9000 | S3-compatible storage |
| PostgreSQL | lobe-postgres:5432 | Database with pgvector |

## Use Cases

### 1. Knowledge Base Queries (RAG)

LobeChat has PostgreSQL with **pgvector** for semantic search:

```bash
# Query the knowledge base
bash /srv/paas/scripts/lobe-rag-query.sh "What is X?" 5
```

**Technical Details**:
- **Embedding Model**: Cloudflare Workers AI `@cf/baai/bge-large-en-v1.5` (1024 dimensions)
- **Vector Storage**: PostgreSQL with pgvector extension
- **File Storage**: MinIO (S3-compatible)

### 2. Multi-Model Routing

LobeChat supports 40+ model providers. Use when:
- Different tasks need different models (Claude for reasoning, GPT for coding)
- Comparing model outputs
- Cost optimization (route to cheaper models for simple tasks)

### 3. Image Generation & Vision

Supports:
- **DALL-E 3** for image generation
- **Vision models** (GPT-4V, Claude Vision, Gemini) for image analysis

## Health Checks

### Quick Status

```bash
# LobeChat
curl -s "$LOBE_URL/api/health" && echo " - LobeChat OK"

# MinIO
curl -s "http://lobe-minio:9000/minio/health/live" && echo " - MinIO OK"
```

### Full Status

```bash
bash /srv/paas/scripts/lobe-status.sh
```

## Database Operations

### Knowledge Base Stats

```bash
docker exec -i lobe-postgres psql -U postgres -d lobechat -c "
SELECT 
    (SELECT COUNT(*) FROM knowledge_bases) as kb_count,
    (SELECT COUNT(*) FROM files) as files,
    (SELECT COUNT(*) FROM chunks) as chunks;
"
```

### RAG Query Direct

```bash
# Usage: lobe-rag-query.sh "query" [limit]
bash /srv/paas/scripts/lobe-rag-query.sh "How does authentication work?" 5
```

## First-Time Setup

Before using RAG queries, upload documents to LobeChat:

1. **Sign in**: Go to `$LOBE_URL` in browser
2. **Create Knowledge Base**: Settings → Knowledge Base → Create
3. **Upload Files**: Add PDF, MD, TXT, or other documents
4. **Wait for Processing**: LobeChat will chunk and embed the documents
5. **Query**: Use the RAG query script

## API Endpoints

### Health

```bash
curl -s "$LOBE_URL/api/health"
```

### Internal Network Access

OpenClaw can reach LobeChat via internal Docker network:

```bash
# Internal URL (from containers)
curl -s "http://lobe-chat:3210/api/health"
```

## Scripts

| Script | Purpose |
|--------|---------|
| `/srv/paas/scripts/lobe-status.sh` | Full LobeChat status |
| `/srv/paas/scripts/lobe-rag-query.sh` | Query knowledge base |

## Configuration

LobeChat is configured with direct provider access:
- **OpenRouter**: Primary provider (access Claude, GPT, Gemini via single key)
- **Gemini**: Direct Google AI access
- **DeepSeek**: Direct DeepSeek access
- **Cloudflare Workers AI**: Embeddings for RAG

Add API keys in LobeChat: Settings → Language Model → Enable providers
