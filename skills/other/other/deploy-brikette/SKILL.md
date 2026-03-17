---
name: deploy-brikette
description: Deploy brikette to staging or production with pre-flight checks and decision awareness.
---

# Deploy Brikette

Deploy the brikette app to Cloudflare with mandatory pre-flight checks.

## MANDATORY: Read Decision Doc First

Before ANY deploy action, read `docs/brikette-deploy-decisions.md`. This contains:
- Current deploy architecture (static Pages staging vs Worker production)
- Static export build mechanics (route hiding, env vars, gotchas)
- Upgrade path to Workers Paid ($5/month) and what it unlocks
- Size budget constraints

**Summarise the key limitations to the user before proceeding.**

## Pre-Flight Checklist

1. **Branch check** — Confirm which branch to deploy (staging or main)
2. **Decision doc** — Read and summarise `docs/brikette-deploy-decisions.md`
3. **Pending changes** — Check `git status` for uncommitted work
4. **Tests** — Run `pnpm --filter @apps/brikette test` (or confirm CI will run them)
5. **Typecheck** — Run `pnpm --filter @apps/brikette typecheck` (or confirm CI will run it)

## Deploy to Staging

```bash
# Push to staging branch (CI handles build + deploy)
git push origin <branch>:staging
```

CI workflow: `.github/workflows/brikette.yml` → `reusable-app.yml`

**Build**: Static export (`OUTPUT_EXPORT=1`) → `out/` directory
**Deploy**: `wrangler pages deploy out --project-name brikette-website --branch staging`
**URL**: `https://staging.brikette-website.pages.dev/en/`

### Post-Deploy Verification
- Check `https://staging.brikette-website.pages.dev/en/` (root `/` redirects via `_redirects`)
- Verify key pages: `/en/rooms`, `/en/experiences`, a guide detail page
- Check images load (should be raw `/img/...` paths, not `/cdn-cgi/image/...`)
- Note: localised slugs (e.g. `/fr/chambres`) do NOT work without the Worker

## Deploy to Production

Production deploy requires `workflow_dispatch` with `publish_to_production: true` on the `main` branch.

**Build**: `@opennextjs/cloudflare` → `.open-next/` directory
**Deploy**: `wrangler deploy` (reads `wrangler.toml`)

**WARNING**: Ensure the staging deploy has been verified first.

## Troubleshooting

| Issue | Cause | Fix |
|---|---|---|
| Build fails: "missing generateStaticParams" | Catch-all `[...slug]` or dynamic API routes | Hide the directory during build (see decision doc §Route Hiding) |
| Build fails: "Unsupported node type ConditionalExpression" | Ternary in `dynamic`/`revalidate` export | Use plain string literal, or hide the route during build |
| Build fails: "Invalid config value exports" | Accumulated ConditionalExpression warnings | Fix all conditional config exports in non-hidden routes |
| Images 404 on staging | `/cdn-cgi/image/` not on free tier | Ensure `NEXT_PUBLIC_OUTPUT_EXPORT=1` is in build command |
| Root URL 404 | No middleware on static deploy | Check `public/_redirects` has `/  /en/  302` |
| Cache headers check fails | No Worker to set headers | Check is skipped for staging (`environment-name != 'production'`) |
| Worker exceeds 3 MiB | Free plan compressed limit | Upgrade to paid ($5/mo) or use static export |
| `_headers` exceeds 100 rules | Too many header rules | Keep `public/_headers` minimal; full rules in `config/_headers` |
| esbuild version conflict | `@cloudflare/next-on-pages` residue | Remove `@cloudflare/next-on-pages` from all `package.json` files |
| Upload artifact empty | `.open-next` starts with dot | Ensure `include-hidden-files: true` in upload-artifact step |

## Key Files

- `.github/workflows/brikette.yml` — CI/CD workflow (staging + production)
- `.github/workflows/reusable-app.yml` — Shared workflow template
- `packages/next-config/index.mjs` — Shared Next.js config (reads `OUTPUT_EXPORT`)
- `packages/ui/src/lib/buildCfImageUrl.ts` — Image URL builder (reads `NEXT_PUBLIC_OUTPUT_EXPORT`)
- `apps/brikette/wrangler.toml` — Cloudflare Worker config (production only)
- `apps/brikette/public/_redirects` — Edge redirects for static deploy
- `docs/brikette-deploy-decisions.md` — Architecture decisions and upgrade path
