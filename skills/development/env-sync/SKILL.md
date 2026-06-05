---
name: env-sync
description: Ensures .env.example is updated whenever .env files are modified. Use when adding environment variables, API keys, configuration values, or any secrets to .env files. Prevents configuration drift between .env and .env.example.
---

# Environment File Sync Guardrail

## Purpose

Ensure that `.env.example` is always updated when `.env` is modified, maintaining clear documentation of required environment variables for other developers.

## When to Use This Skill

This skill automatically activates when:
- Editing `.env` files
- Adding new environment variables
- Modifying existing environment variable names
- Removing environment variables
- Working with configuration that requires secrets

## The Problem

When developers add new environment variables to `.env` but forget to update `.env.example`:
- New team members don't know what variables are required
- CI/CD pipelines fail due to missing configuration
- Documentation becomes outdated
- Setup instructions become incomplete

## The Rule

**Whenever you modify `.env`, you MUST update `.env.example`**

### What to Include in `.env.example`:

✅ **DO include:**
- Variable names (exact same as `.env`)
- Placeholder/example values
- Comments explaining what each variable is for
- Format requirements (URLs, tokens, etc.)

❌ **DO NOT include:**
- Real API keys or secrets
- Production credentials
- Personal access tokens
- Any sensitive data

## Examples

### Adding a New API Key

**`.env` (actual secrets):**
```bash
# OpenAI Configuration
OPENAI_API_KEY=sk-proj-abc123...
OPENAI_MODEL=gpt-4
```

**`.env.example` (documentation):**
```bash
# OpenAI Configuration
OPENAI_API_KEY=YOUR_API_KEY
OPENAI_MODEL=gpt-4
```

### Adding Database Configuration

**`.env`:**
```bash
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/mydb
SUPABASE_URL=https://abcdefg.supabase.co
SUPABASE_ANON_KEY=eyJhbGc...real-key
```

**`.env.example`:**
```bash
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_ANON_KEY=your-supabase-anon-key
```

### Adding Feature Flags

**`.env`:**
```bash
# Feature Flags
ENABLE_AI_FEATURES=true
DEBUG_MODE=false
```

**`.env.example`:**
```bash
# Feature Flags
ENABLE_AI_FEATURES=true
DEBUG_MODE=false
```

## Checklist

When modifying `.env`, ensure:

- [ ] Every new variable in `.env` exists in `.env.example`
- [ ] Variable names are identical in both files
- [ ] `.env.example` has placeholder/example values (not real secrets)
- [ ] Comments explain what each variable is for
- [ ] Format/structure is documented (URLs, token prefixes, etc.)
- [ ] Both files are in the same order (easier to compare)
- [ ] Removed variables are also removed from `.env.example`

## Current Project Structure

```
backend/
├── .env              # Real secrets (git-ignored)
└── .env.example      # Documentation (committed to git)
```

## Common Patterns

### API Keys Pattern
```bash
# Service Name API Configuration
SERVICE_API_KEY=your-api-key-here
SERVICE_API_URL=https://api.service.com
```

### Database Pattern
```bash
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=database_name
DB_USER=db_user
DB_PASSWORD=db_password
```

### Optional Variables Pattern
```bash
# Optional: Analytics (leave empty to disable)
ANALYTICS_KEY=your-analytics-key-or-leave-empty
```

## Quick Reference

```bash
# View differences between .env and .env.example
diff backend/.env backend/.env.example

# Copy structure from .env to .env.example (then replace secrets with placeholders)
cp backend/.env backend/.env.example
# Then manually replace real values with placeholders
```

---

**Remember:** `.env.example` is documentation for other developers. Keep it updated!
