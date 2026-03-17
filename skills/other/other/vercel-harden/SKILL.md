---
name: vercel-harden
description: Harden a Vercel deployment with security headers, CSP, bot protection, and deployment configuration
arguments: "[--check-only] [--plan hobby|pro]"
---

# Vercel Deployment Hardening

## Purpose

Audit and harden a Next.js project deployed on Vercel. Applies security headers at the edge, configures CSP, blocks malicious bots, and provides a dashboard checklist for manual Vercel settings.

## Arguments

- `--check-only` — Audit current security posture without making changes
- `--plan hobby|pro` — Target Vercel plan (default: `pro`). Controls which features are available (WAF rules, bot protection, etc.)

## Workflow

### 1. Audit current posture

Scan the project for existing security configuration:

```
- next.config.ts: poweredByHeader, headers() (static headers only — NOT CSP)
- proxy.ts: CSP header, bot blocking, honeypot paths
- vercel.json: edge-level headers
- robots.ts: bot disallow rules
```

Report findings as a checklist with pass/fail for each item.

### 2. Apply code-level hardening

If not `--check-only`, apply these changes:

#### Static headers (next.config.ts)

- Set `poweredByHeader: false`
- Add `headers()` function applying **non-CSP** security headers to `/:path*`
- Required headers: see `reference/vercel-harden-reference.md`
- **CSP must NOT go here** — static headers cannot handle Next.js inline scripts

#### CSP configuration (proxy.ts)

> **WARNING: Nonce-based CSP and `'strict-dynamic'` are incompatible with Next.js.**
> Next.js generates inline `<script>` tags for hydration, routing, and RSC payloads
> that cannot receive nonces. Using nonces or `'strict-dynamic'` will break the app
> (white page, broken navigation, non-functional interactive elements).

- CSP must be applied in `proxy.ts` (not `next.config.ts headers()`) so it runs per-request
- Use `script-src 'self' 'unsafe-inline'` — this is the only approach compatible with Next.js
- Build remaining directives from project's actual dependencies (check for analytics, embeds, fonts, etc.)
- Add Vercel Analytics sources if `@vercel/analytics` or `@vercel/speed-insights` are installed
- Non-executable script types like `application/ld+json` must NOT receive nonces
- See reference doc for base directives and third-party allowlists

#### Bot protection (proxy.ts)

- Add blocked user agent check and honeypot path check in `proxy.ts`
- Update `robots.ts` to block AI scrapers and SEO bots
- See reference doc for recommended patterns

### 3. Verify headers

After changes, verify with:

```bash
curl -I https://<deployment-url>
```

Check for presence of all security headers and absence of `X-Powered-By`.

Also run:

```bash
pnpm test
pnpm build
pnpm test:e2e
```

After deployment, open the browser console and check for CSP violation errors. If any appear, update the CSP directives to allow the blocked resource.

### 4. Output Vercel dashboard checklist

Print actionable checklist for manual Vercel dashboard configuration. Include only items relevant to the `--plan` argument.

## TDD requirement

All code changes must follow red-green-refactor:
1. Write failing tests for new headers/bot protection
2. Implement to make tests pass
3. Refactor

## Reference

See `reference/vercel-harden-reference.md` for:
- Full header reference with recommended values
- CSP directive guide and third-party allowlists
- WAF rule templates
- Bot protection patterns
- Vercel plan feature matrix
