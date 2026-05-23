---
name: build-and-deploy
description: Build and deploy this Next.js LangChain retrieval agent application with Supabase vector store. Use when building, deploying, setting up vector store, or preparing the project for production.
---

# Build and Deploy LangChain Retrieval Agent

> **CRITICAL: For Vercel, you MUST use `vercel build --prod` then `vercel deploy --prebuilt --prod`.**
> Do NOT use `vercel --prod` or `vercel deploy --prod` directly - these will fail due to Git author permission issues in VM environments.

## Workflow

### 1. Setup Environment Variables

**Read `.env.example` to see all required variables:**

```bash
cat .env.example
```

**Create `.env` by reading values from current environment:**

For each variable in `.env.example`, read the value from the current environment and write to `.env`. Example approach:

```bash
# Read .env.example and create .env with values from current environment
while IFS= read -r line || [[ -n "$line" ]]; do
  # Skip comments and empty lines
  [[ "$line" =~ ^#.*$ || -z "$line" ]] && continue
  # Extract variable name (before = sign)
  var_name=$(echo "$line" | cut -d'=' -f1)
  # Get value from environment
  var_value="${!var_name}"
  # Write to .env
  echo "${var_name}=${var_value}" >> .env
done < .env.example
```

Or manually inspect `.env.example` and create `.env` with the required values from environment variables.

### 2. Install Dependencies

```bash
yarn install
```

### 3. Setup Supabase Vector Store

Get the database connection URL from Supabase Dashboard:
- Go to Settings → Database → Connection string → URI
- Copy the URI and add it to `.env` as `SUPABASE_DB_URL`

```bash
yarn setup-db
```

This creates the pgvector extension, documents table, and match_documents function in your Supabase project.

### 4. Build

```bash
yarn build
```

### 5. Deploy

**Vercel:**

All vercel CLI commands require `-t <token>` or `--token <token>` for authentication.

```bash
# Pull project settings (also links project, creates .vercel/project.json)
vercel pull --yes -t $VERCEL_TOKEN

# Push env vars to Vercel (first time only)
# Must add to each environment separately
while IFS='=' read -r key value; do
  [[ "$key" =~ ^#.*$ || -z "$key" || -z "$value" ]] && continue
  for env in production preview development; do
    printf '%s' "$value" | vercel env add "$key" $env -t $VERCEL_TOKEN
  done
done < .env

# Build locally for production
vercel build --prod -t $VERCEL_TOKEN

# Deploy prebuilt
vercel deploy --prebuilt --prod --yes -t $VERCEL_TOKEN
```

**Netlify:**
```bash
# Import all env vars from .env (first time only)
netlify env:import .env

# Deploy
netlify deploy --prod
```

## Critical Notes

- **VERCEL PREBUILT MODE IS MANDATORY:** Always use `vercel build --prod` followed by `vercel deploy --prebuilt --prod`. Never use `vercel --prod` or `vercel deploy --prod` without `--prebuilt` flag.
- **Supabase Required:** Need a Supabase project (free tier works)
- **Vector Store Setup:** Run `yarn setup-db` to create tables automatically
- **Environment Variables:** All values come from current environment - inspect `.env.example` for required variables
- **OpenAI for Embeddings:** OPENAI_API_KEY is always required for vector embeddings
- **No Dev Server:** Never run `yarn dev` in VM environment
