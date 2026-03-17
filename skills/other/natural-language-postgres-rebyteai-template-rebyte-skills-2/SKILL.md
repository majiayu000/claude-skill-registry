---
name: natural-language-postgres-presentation
description: Presentation-focused Natural Language to SQL app with PPT-style visualizations.
---

# Natural Language Postgres Presentation

A presentation-focused Natural Language to SQL app with PPT-style visualizations for showcasing data insights.

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
git clone --depth 1 https://github.com/Eng0AI/natural-language-postgres-presentation.git .
```

If the directory is not empty:

```bash
git clone --depth 1 https://github.com/Eng0AI/natural-language-postgres-presentation.git _temp_template
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
