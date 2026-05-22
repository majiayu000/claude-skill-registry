---
name: langchain-retrieval
description: Document Q&A with RAG using Supabase pgvector store.
---

# LangChain Retrieval

Document Q&A with RAG (Retrieval Augmented Generation) using Supabase vector store.

## Tech Stack

- **Framework**: Next.js
- **AI**: LangChain.js, AI SDK
- **Vector Store**: Supabase pgvector
- **Package Manager**: pnpm

## Prerequisites

- Supabase project with pgvector extension
- OpenAI API key

## Setup

### 1. Clone the Template

```bash
git clone --depth 1 https://github.com/Eng0AI/langchain-retrieval.git .
```

If the directory is not empty:

```bash
git clone --depth 1 https://github.com/Eng0AI/langchain-retrieval.git _temp_template
mv _temp_template/* _temp_template/.* . 2>/dev/null || true
rm -rf _temp_template
```

### 2. Remove Git History (Optional)

```bash
rm -rf .git
git init
```

### 3. Install Dependencies

```bash
pnpm install
```

### 4. Setup Environment Variables

Create `.env` with required variables:
- `SUPABASE_URL` - Supabase project URL
- `SUPABASE_PRIVATE_KEY` - Supabase service role key
- `OPENAI_API_KEY` - For embeddings and LLM
- `SUPABASE_DB_URL` - Direct PostgreSQL connection URL

### 5. Setup Vector Store

Initialize pgvector extension and create documents table in Supabase.

## Build

```bash
pnpm build
```

## Development

```bash
pnpm dev
```
