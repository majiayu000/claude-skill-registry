---
name: ops-performance
description: Performance analysis for Expo + serverless backend projects. Runs Lighthouse audits, bundle size analysis, and k6 load tests.
allowed-tools:
  - Bash
  - Read
---

# Ops: Performance

Analyze application performance.

**Argument**: `$ARGUMENTS` — analysis type (`lighthouse`, `bundle`, `k6`, `all`; default: `all`) and optional target environment

## Path Convention

- **Frontend**: Current project directory (`.`)
- **Backend**: `${BACKEND_DIR:-../backend-v2}` — set `BACKEND_DIR` in `.claude/settings.local.json` if your backend is elsewhere

## Discovery

1. Read frontend `package.json` for `lighthouse:check`, `export:web`, `analyze:bundle` scripts
2. Read backend `package.json` for `k6:*` scripts
3. Read `e2e/constants.ts` or `.env.*` files for environment URLs

## Lighthouse Audit

### Against Local

```bash
npx lighthouse http://localhost:8081 \
  --output=json \
  --output-path=./lighthouse-local.json \
  --chrome-flags='--headless --no-sandbox'
```

### Against Deployed Environment

Discover frontend URLs from `e2e/constants.ts` or `.env.*` files:

```bash
npx lighthouse https://{env_url} \
  --output=json \
  --output-path=./lighthouse-{env}.json \
  --chrome-flags='--headless --no-sandbox'
```

### LHCI (Lighthouse CI — uses project config)

```bash
bun run lighthouse:check
```

### Parse Lighthouse Results

```bash
cat lighthouse-{env}.json | jq '{
  performance: .categories.performance.score,
  accessibility: .categories.accessibility.score,
  bestPractices: .categories["best-practices"].score,
  seo: .categories.seo.score,
  fcp: .audits["first-contentful-paint"].displayValue,
  lcp: .audits["largest-contentful-paint"].displayValue,
  tbt: .audits["total-blocking-time"].displayValue,
  cls: .audits["cumulative-layout-shift"].displayValue,
  si: .audits["speed-index"].displayValue
}'
```

## Bundle Analysis

### Full Analysis (export + source-map-explorer)

```bash
bun run export:web && bun run analyze:bundle
```

### Quick Size Check

```bash
bun run export:web
echo "=== Total Bundle Size ==="
du -sh dist/
echo ""
echo "=== Largest JS Files ==="
find dist -name "*.js" -exec ls -lhS {} + 2>/dev/null | head -20
```

## k6 Load Tests

Discover available k6 scripts from the backend `package.json` (matching `k6:*`).

### Smoke Test (minimal load, verify endpoints work)

```bash
cd "${BACKEND_DIR:-../backend-v2}"
bun run k6:smoke
```

### Load Test (normal traffic simulation)

```bash
cd "${BACKEND_DIR:-../backend-v2}"
bun run k6:load
```

### Stress Test (push beyond normal capacity)

```bash
cd "${BACKEND_DIR:-../backend-v2}"
bun run k6:stress
```

### Spike Test (sudden traffic burst)

```bash
cd "${BACKEND_DIR:-../backend-v2}"
bun run k6:spike
```

### Docker-based k6 (no local k6 install needed)

```bash
cd "${BACKEND_DIR:-../backend-v2}"
bun run k6:docker:smoke
bun run k6:docker:load
```

## Output Format

### Lighthouse Scores

| Metric | Score | Rating |
|--------|-------|--------|
| Performance | 0.85 | GOOD |
| Accessibility | 0.92 | GOOD |
| Best Practices | 0.88 | GOOD |
| SEO | 0.95 | GOOD |

### Core Web Vitals

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| FCP (First Contentful Paint) | 1.2s | < 1.8s | PASS |
| LCP (Largest Contentful Paint) | 2.1s | < 2.5s | PASS |
| TBT (Total Blocking Time) | 150ms | < 200ms | PASS |
| CLS (Cumulative Layout Shift) | 0.05 | < 0.1 | PASS |

### Bundle Size

| Category | Size | Notes |
|----------|------|-------|
| Total dist/ | 4.2 MB | |
| Largest chunk | 1.1 MB | vendor.js |

### k6 Results

| Metric | Value |
|--------|-------|
| Requests/sec | 450 |
| Avg response time | 120ms |
| p95 response time | 350ms |
| Error rate | 0.1% |

Include recommendations for any metrics that fall below thresholds.
