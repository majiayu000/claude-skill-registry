---
name: deploy-and-ops
description: Build, deploy, configure, and troubleshoot the site on Cloudflare Workers — manage secrets, configure wrangler, set up custom domains, and diagnose common errors. Use when the user mentions "deploy", "build", "wrangler", "production", "custom domain", "secrets", "environment variables", "CI/CD", "errors", "not working", "broken", "debug", or "troubleshoot".
---

# Deploy and Operations

## Deploy Pipeline

```bash
bun run deploy    # Runs: astro build && wrangler deploy
```

This builds the Astro site and deploys the output to Cloudflare Workers.

## Pre-Deploy Verification

Always run before deploying:

```bash
bun run check     # TypeScript type checking
bun run test      # 42 tests across 7 files
bun run build     # Production build
```

## Wrangler Configuration

`wrangler.jsonc` defines the Worker name, bindings, compatibility settings, and asset serving. See [wrangler config reference](references/wrangler-config.md).

## Managing Secrets

**Local** (`.dev.vars`):
```env
CONTACT_EMAIL=you@domain.com
POLICY_AUD=aud-tag
TEAM_DOMAIN=yourteam
```

**Production**:
```bash
bunx wrangler secret put CONTACT_EMAIL
bunx wrangler secret put POLICY_AUD
bunx wrangler secret put TEAM_DOMAIN
```

## Custom Domains

1. Deploy the Worker first
2. Go to **Workers & Pages > your worker > Settings > Domains & Routes**
3. Add a custom domain (Cloudflare handles DNS + SSL)
4. Update `site` in `astro.config.mjs` to match

## Troubleshooting

See [troubleshooting reference](references/troubleshooting.md) for common errors and fixes.
