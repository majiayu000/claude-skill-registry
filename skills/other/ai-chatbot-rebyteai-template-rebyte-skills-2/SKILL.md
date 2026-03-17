---
name: ai-chatbot
description: Full-featured AI chatbot with Next.js 15, Auth.js, Drizzle ORM, and multi-model support.
---

# AI Chatbot

A full-featured, hackable AI chatbot with authentication, file storage, and multi-model support.

## Tech Stack

- **Framework**: Next.js 15
- **React**: React 19
- **AI**: AI SDK, Vercel AI Gateway
- **Auth**: Auth.js
- **ORM**: Drizzle
- **Database**: PostgreSQL (Neon, Supabase, or Railway)
- **Styling**: Tailwind CSS, shadcn/ui
- **Package Manager**: pnpm
- **Dev Port**: 3000

## Setup

### 1. Clone the Template

```bash
git clone --depth 1 https://github.com/Eng0AI/ai-chatbot-template.git .
```

If the directory is not empty:

```bash
git clone --depth 1 https://github.com/Eng0AI/ai-chatbot-template.git _temp_template
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

```bash
cp .env.example .env
```

Required variables:
- `POSTGRES_URL` - PostgreSQL connection string
- `AUTH_SECRET` - Generate with `openssl rand -base64 32`
- `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` - LLM provider key

### 5. Run Database Migrations

```bash
pnpm db:migrate
```

## Build

```bash
pnpm build
```

Or run build without migration (if already migrated):
```bash
next build
```

## Deploy

### Vercel (Recommended)

```bash
# Pull project settings
vercel pull --yes -t $VERCEL_TOKEN

# Push env vars (first time only)
while IFS='=' read -r key value; do
  [[ "$key" =~ ^#.*$ || -z "$key" || -z "$value" ]] && continue
  for env in production preview development; do
    printf '%s' "$value" | vercel env add "$key" $env -t $VERCEL_TOKEN
  done
done < .env

# Build and deploy
vercel build --prod -t $VERCEL_TOKEN
vercel deploy --prebuilt --prod --yes -t $VERCEL_TOKEN
```

### Netlify

```bash
# Import env vars (first time only)
netlify env:import .env

# Deploy
netlify deploy --prod
```

## Critical Notes

- **Database Required:** Must have PostgreSQL database set up before building
- **Migration Required:** Run `pnpm db:migrate` before first build
- **Auth Secret:** Generate a secure random secret for AUTH_SECRET
- Never run `pnpm dev` in VM environment
