---
name: vite-flare-starter
description: "Scaffold a full-stack Cloudflare app from vite-flare-starter — React 19, Hono, D1+Drizzle, better-auth, Tailwind v4+shadcn/ui, TanStack Query, R2, Workers AI. Run setup.sh to clone, configure, and deploy."
compatibility: claude-code-only
---

# Vite Flare Starter

Clone and configure Jez's batteries-included Cloudflare starter into a standalone project. Produces a fully rebranded, deployable full-stack app.

## What You Get

| Layer | Technology |
|-------|-----------|
| Frontend | React 19, Vite, Tailwind v4, shadcn/ui |
| Backend | Hono (on Cloudflare Workers) |
| Database | D1 (SQLite at edge) + Drizzle ORM |
| Auth | better-auth (Google OAuth + optional email/password) |
| Storage | R2 (S3-compatible object storage) |
| AI | Workers AI binding |
| Data Fetching | TanStack Query |
| Deployment | Cloudflare Workers with Static Assets |

See `references/tech-stack.md` for the full dependency list.

## Workflow

### Step 1: Gather Project Info

Ask for:

| Required | Optional |
|----------|----------|
| Project name (kebab-case) | Admin email |
| Description (1 sentence) | Google OAuth credentials |
| Cloudflare account (Jezweb Team or Personal) | Custom domain |

### Step 2: Run Setup Script

```bash
bash skills/vite-flare-starter/scripts/setup.sh
```

The script will:
1. Clone the repo and remove `.git`
2. Find-replace `vite-flare-starter` with project name (7 locations)
3. Generate `BETTER_AUTH_SECRET`
4. Create `.dev.vars` from template
5. Optionally create Cloudflare D1 + R2 resources
6. Run `pnpm install`
7. Run local database migration
8. Report remaining manual steps

### Step 3: Manual Configuration

After the script completes:

1. **Google OAuth** (if using):
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create OAuth 2.0 Client ID
   - Add redirect URI: `http://localhost:5173/api/auth/callback/google`
   - Copy Client ID and Secret to `.dev.vars`

2. **Favicon**: Replace `public/favicon.svg` with your own

3. **CLAUDE.md**: Update project description and remove vite-flare-starter references

4. **index.html**: Update `<title>` and meta description

### Step 4: Verify Locally

```bash
pnpm dev
```

Check:
- [ ] http://localhost:5173 loads
- [ ] Shows YOUR app name, not "Vite Flare Starter"
- [ ] Sign-up/sign-in works (if Google OAuth configured)

### Step 5: Deploy to Production

```bash
# Set production secrets
openssl rand -base64 32 | npx wrangler secret put BETTER_AUTH_SECRET
echo "https://PROJECT_NAME.SUBDOMAIN.workers.dev" | npx wrangler secret put BETTER_AUTH_URL
echo "http://localhost:5173,https://PROJECT_NAME.SUBDOMAIN.workers.dev" | npx wrangler secret put TRUSTED_ORIGINS

# If using Google OAuth
echo "your-client-id" | npx wrangler secret put GOOGLE_CLIENT_ID
echo "your-client-secret" | npx wrangler secret put GOOGLE_CLIENT_SECRET

# Migrate remote database
pnpm run db:migrate:remote

# Build and deploy
pnpm run build && pnpm run deploy
```

**Critical**: After first deploy, update BETTER_AUTH_URL with your actual Worker URL. Also add the production URL to Google OAuth redirect URIs.

## Common Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| Auth silently fails (redirect to homepage) | Missing TRUSTED_ORIGINS | Set TRUSTED_ORIGINS secret with all valid URLs |
| "Not authorized" on deploy | Wrong account_id | Remove account_id from wrangler.jsonc or set yours |
| Database operations fail | Using original database_id | Create YOUR database, use YOUR database_id |
| localStorage shows "vite-flare-starter" | Missing VITE_APP_ID | Set `VITE_APP_ID=yourapp` in .dev.vars |
| Auth fails in production | BETTER_AUTH_URL mismatch | Must match actual Worker URL exactly |

## What Gets Rebranded

The setup script handles these automatically:

| File | What Changes |
|------|-------------|
| `wrangler.jsonc` | Worker name, database name, bucket names |
| `package.json` | Package name, database references in scripts |
| `.dev.vars` | App name, secret, URL |
| `index.html` | Title, meta tags |

These need manual attention:
- `CLAUDE.md` — project description
- `public/favicon.svg` — your favicon
- Google OAuth — redirect URIs
- Production secrets — via `wrangler secret put`

See `references/customization-guide.md` for the complete rebranding checklist.
