---
name: langchain-retrieval-agent
description: AI agent with retrieval tool for document Q&A using RAG and LangGraph.
---

# LangChain Retrieval Agent

An AI agent with retrieval tool for document Q&A using RAG, powered by LangGraph.

## Tech Stack

- **Framework**: Next.js
- **AI**: LangChain.js, LangGraph, AI SDK
- **Vector Store**: Supabase pgvector
- **Package Manager**: pnpm

## Prerequisites

- Supabase project with pgvector extension
- OpenAI API key

## Setup

### 1. Clone the Template

```bash
git clone --depth 1 https://github.com/Eng0AI/langchain-retrieval-agent.git .
```

If the directory is not empty:

```bash
git clone --depth 1 https://github.com/Eng0AI/langchain-retrieval-agent.git _temp_template
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

- `SUPABASE_URL` - Supabase project URL
- `SUPABASE_PRIVATE_KEY` - Supabase service role key
- `OPENAI_API_KEY` - For embeddings and LLM

## Build

```bash
pnpm build
```

## Development

```bash
pnpm dev
```
