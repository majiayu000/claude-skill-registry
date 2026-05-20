---
name: vite-react-ts-deploy
description: Explain and implement the production build + static deployment workflow for a Vite React-TS app (build output, base path, preview, common hosts).
argument-hint: "[host: vercel/netlify/github-pages/custom] [base path] [spa fallback]"
allowed-tools: Read, Grep, Glob
---

# Vite React-TS Build & Deploy Skill

Guide and implement production build and deployment settings.

## Rules / best practices

1) Use:
   - pnpm build (vite build)
   - pnpm preview to validate the production build locally
2) Static hosting:
   - Serve dist/ directory
3) If deploying under a subpath, set base in Vite config.
4) For SPAs, ensure the host is configured for history fallback routing.

## Deliverables

- Commands
- Relevant config changes (base, assets, etc.)
- Host-specific notes when requested

Use template.md as the default structure.
