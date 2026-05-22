---
name: deploy-worker
description: Deploy Cloudflare Workers to production. Use when deploying main worker, search-consumer, or any Cloudflare Worker.
allowed-tools: Bash(npm:*), Bash(npx:*), Bash(wrangler:*), Read, Glob
---

# Cloudflare Worker Deployment

## Prerequisites
- Ensure CLOUDFLARE_API_TOKEN is set in environment
- Verify wrangler.toml exists in worker directory

## Deployment Steps

### Main Worker
```bash
cd workers/main
npm run build:worker
npx wrangler deploy
```

### Search Consumer Worker
```bash
cd workers/search-consumer
npm run build:consumer
npx wrangler deploy
```

### Verification
After deployment, tail logs to verify:
```bash
timeout 15 npx wrangler tail
```

## Common Issues
- **Authentication failed**: Check CLOUDFLARE_API_TOKEN
- **Build errors**: Run `npm install` first
- **Route conflicts**: Check wrangler.toml routes

## Rollback
If deployment fails:
```bash
npx wrangler rollback
```
