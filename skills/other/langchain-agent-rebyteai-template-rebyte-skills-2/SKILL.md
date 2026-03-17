---
name: langchain-agent
description: AI agent with tools (search, calculator) using LangGraph and AI SDK.
---

# LangChain Agent

An AI agent with tools (search engine and calculator) powered by LangGraph and the Vercel AI SDK.

## Tech Stack

- **Framework**: Next.js
- **AI**: LangChain.js, LangGraph, AI SDK
- **Database**: PostgreSQL
- **Package Manager**: pnpm

## Prerequisites

- PostgreSQL database
- OpenAI API key

## Setup

### 1. Clone the Template

```bash
git clone --depth 1 https://github.com/Eng0AI/langchain-agent.git .
```

If the directory is not empty:

```bash
git clone --depth 1 https://github.com/Eng0AI/langchain-agent.git _temp_template
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
- `POSTGRES_URL` - PostgreSQL connection string
- `OPENAI_API_KEY` - OpenAI API key for the agent

## Build

```bash
pnpm build
```

## Development

```bash
pnpm dev
```
