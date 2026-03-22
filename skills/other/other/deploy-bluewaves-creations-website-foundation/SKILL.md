---
name: deploy
description: Builds and deploys the site to Cloudflare Workers with pre-flight checks including TypeScript, tests, and production build. Use when deploying, publishing, or shipping to production.
argument-hint: ""
disable-model-invocation: true
---

Build and deploy the site to Cloudflare Workers with pre-flight checks.

## Steps

### 1. Pre-flight Checks

Run verification sequentially, stopping on first failure:

1. `bun run check` — TypeScript type checking
2. `bun run test` — Run all tests
3. `bun run build` — Production build

If any step fails, **stop** and report the error with a fix suggestion. Do not proceed to deploy.

### 2. Deploy

If all checks pass, run:

```bash
bun run deploy
```

This executes `astro build && wrangler deploy`.

### 3. Report Results

After deployment completes, report:
- The Worker URL from wrangler output
- Any warnings from the build or deploy process
- Remind the user to verify the live site

If deployment fails:
- Check if wrangler is authenticated (`bunx wrangler whoami`)
- Check if the worker name in `wrangler.jsonc` is correct
- Report the specific error message
