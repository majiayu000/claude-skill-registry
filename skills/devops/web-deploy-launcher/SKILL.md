---
name: web-deploy-launcher
description: Prepare deployment configs, final checks, and pre-launch readiness artifacts for production release.
compatibility: codex, claude-code, claude-ai, agent-skills
license: Apache-2.0
allowed-tools:
  - read_file
  - write_file
  - run_terminal_cmd
  - web_search
metadata:
  category: web-builder
  stage: 10-deployment
  pipeline: web-builder
---

# Web Deploy Launcher

## Objective

Prepare deployment configuration and final production readiness checks based on
`project-config.json`.

## Required Workflow

1. Read deployment target from `project-config.json`.
2. Generate target-specific config:
   - Vercel: `vercel.json`
   - Netlify: `netlify.toml`
   - Fly.io: `fly.toml` and `Dockerfile`
   - Railway/Render: `Dockerfile` plus deployment instructions
   - Cloudflare Pages: `wrangler.toml`
3. Run production build checks (`npm run build` or `python -m build`) and capture errors.
4. Run bundle size analysis (`@next/bundle-analyzer`, `vite-bundle-analyzer`, or `source-map-explorer`).
5. Verify environment variable coverage in `.env.example` and flag hardcoded secrets.
6. Generate pre-deploy checklist covering HTTPS, monitoring, logging, backups, feature flags, and rollback plan.
7. Generate `DEPLOYMENT.md`.
8. Output deployment configs and `deploy-report.json`.

## Execution

```bash
python skills/web-deploy-launcher/scripts/deploy_launcher.py --input <workspace> --output <out.json> --format json
```

## References

- `references/tools.md`
