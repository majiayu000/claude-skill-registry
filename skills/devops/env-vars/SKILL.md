---
name: env-vars
description: Manages environment variables and credentials securely. Use when configuring secrets or .env files.
user-invocable: true
triggers:
  - env
  - environment
  - credentials
  - secrets
  - api key
allowed-tools: Bash, Read, Write, Grep
model: opus
---

# Environment Variables Workflow

## On "env" or "credentials"

### Step 1: Determine Action
```
question: "What do you need?"
options:
  - { label: "Check current", description: "See what's configured" }
  - { label: "Add new", description: "Add a new environment variable" }
  - { label: "Debug missing", description: "Something isn't working" }
  - { label: "Setup .env.local", description: "Create project env file" }
```

### Step 2: Actions

**Check current (Windows):**
```powershell
# List relevant env vars
[Environment]::GetEnvironmentVariable("SUPABASE_ACCESS_TOKEN", "User")
[Environment]::GetEnvironmentVariable("GOOGLE_CLIENT_ID", "User")
# etc.
```

**Check current (Mac/Linux):**
```bash
echo $SUPABASE_ACCESS_TOKEN
echo $GOOGLE_CLIENT_ID
# etc.
```

**Add new:**
```
1. Ask for variable name
2. Ask for value
3. Store in system env vars:
   - Windows: setx NAME "value"
   - Mac/Linux: Add to ~/.zshrc or ~/.bashrc
4. Report success
```

**Debug missing:**
```
1. Run npm run build to surface errors
2. Check which env vars are referenced
3. Compare against what's set
4. Report missing vars
```

**Setup .env.local:**
```
1. Check project for env var usage
2. Generate .env.local with required vars
3. Pull values from system env vars where available
4. Mark missing vars for user to fill
```

## Security Rules

**Avoid:**
- Hardcode API keys in code
- Commit .env files to git
- Log secret values
- Store secrets in .env.example

**Do:**
- Use process.env.VAR_NAME
- Store secrets in system env vars
- Use .env.local for project-specific values
- Add .env* to .gitignore

## Common Variables

| Category | Variables |
|----------|-----------|
| **Supabase** | SUPABASE_ACCESS_TOKEN, NEXT_PUBLIC_SUPABASE_URL, NEXT_PUBLIC_SUPABASE_ANON_KEY |
| **Google OAuth** | GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET |
| **GitHub** | GITHUB_PAT |
| **AI/LLM** | OPENAI_API_KEY, ELEVENLABS_API_KEY, OPENROUTER_API_KEY |
| **Email** | RESEND_API_KEY |
| **Search** | BRAVE_API_KEY |

## .env.local Template

```env
# Project-specific (fill these in)
NEXT_PUBLIC_SUPABASE_URL=https://[ref].supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...

# These are read from system env vars automatically:
# - GOOGLE_CLIENT_ID
# - GOOGLE_CLIENT_SECRET
# - SUPABASE_ACCESS_TOKEN

# Project-specific overrides (optional)
YOUTUBE_REDIRECT_URI=http://localhost:3000/api/auth/youtube/callback
```

## Troubleshooting

**"Environment variable not found":**
1. Check if set: `echo $VAR_NAME` or `$env:VAR_NAME`
2. Restart terminal after setting
3. For Next.js, restart dev server

**"Invalid API key":**
1. Verify the key is correct (no extra spaces)
2. Check key hasn't expired
3. Verify key has required permissions

**".env.local not loading":**
1. File must be in project root
2. Restart dev server after changes
3. Check file encoding (should be UTF-8)
