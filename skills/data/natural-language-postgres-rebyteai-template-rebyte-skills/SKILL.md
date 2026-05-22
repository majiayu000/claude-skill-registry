---
name: natural-language-postgres
description: Chat app that lets you ask questions in plain English and query your PostgreSQL database.
---

# Natural Language Postgres

A demo app that lets you ask questions in plain English and get answers from your database.

## Tech Stack

- **Framework**: Next.js
- **AI**: AI SDK
- **Database**: PostgreSQL
- **Package Manager**: pnpm

## Prerequisites

- PostgreSQL database
- OpenAI API key or other LLM provider

## Setup

### 1. Clone the Template

```bash
git clone --depth 1 https://github.com/Eng0AI/natural-language-postgres.git .
```

If the directory is not empty:

```bash
git clone --depth 1 https://github.com/Eng0AI/natural-language-postgres.git _temp_template
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
- `OPENAI_API_KEY` or other LLM provider key

## Build

```bash
pnpm build
```

## Development

```bash
pnpm dev
```
