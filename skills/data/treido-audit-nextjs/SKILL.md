---
name: treido-audit-nextjs
description: "Read-only Next.js 16 App Router auditor for Treido (RSC vs client, caching rules, proxy.ts, route boundaries). Returns structured payload for ORCH merge. Trigger: NEXTJS-AUDIT"
---

# Treido Next.js Auditor (Read-only)

Read-only specialist. Do not patch files. Do not edit `TASKS.md`.
Contract: `.claude/skills/treido-orchestrator/references/audit-payload.md`

## Focus (Treido)

- Server Components by default; keep `"use client"` minimal.
- Cached server code (`'use cache'`): always `cacheLife()` + `cacheTag()`; never `cookies()`/`headers()` inside cached functions.
- Route boundaries: don’t import route-private code across route groups.
- Request hook: `proxy.ts` (avoid reintroducing middleware patterns).

## Audit Steps (Read-only)

```bash
rg -n "\"use client\"" app components
rg -n "'use cache'|\"use cache\"" app lib
rg -n "\\b(cookies|headers)\\(" app lib
rg -n "\\b(cacheLife|cacheTag)\\b" app lib
rg -n "from ['\"]@/app/|from ['\"]\\.{1,2}/.*app/" components lib app
rg -n "\\bmiddleware\\.ts\\b|\\bproxy\\.ts\\b" .
```

## Output (Required)

- Header: `## NEXTJS`
- IDs: `NEXTJS-001`, `NEXTJS-002`, ...
- Include acceptance checks: `pnpm -s typecheck`, and “no cookies()/headers() in cached functions”

