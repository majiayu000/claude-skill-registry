---
name: Performance Regression Gates
description: Gates สำหรับตรวจจับ performance regression ผ่าน benchmarks, bundle size, และ load time monitoring
---

# Performance Regression Gates

## Overview

Gates สำหรับป้องกัน performance regression - bundle size, response time, load time - ต้องไม่แย่ลงเกิน threshold

## Why This Matters

- **User experience**: Slow app = bad UX
- **Prevent degradation**: จับก่อนถึง users
- **Accountability**: รู้ว่า PR ไหนทำให้ช้า
- **Automated**: ไม่ต้องทดสอบ manual

---

## Performance Metrics

### 1. Bundle Size
```bash
# Check bundle size
npm run build
npm run analyze

# Threshold: No >10% increase
Before: 250 KB
After:  260 KB (+4%) ✓ Pass
After:  280 KB (+12%) ✗ Fail
```

### 2. Response Time
```bash
# API benchmark
npm run benchmark:api

# Threshold: No >20% slower
GET /users: 50ms → 55ms (+10%) ✓ Pass
GET /users: 50ms → 65ms (+30%) ✗ Fail
```

### 3. Load Time
```bash
# Lighthouse CI
npm run lighthouse

# Threshold: Score ≥90
Performance: 95 ✓ Pass
Performance: 85 ✗ Fail
```

---

## CI Pipeline

```yaml
# .github/workflows/performance.yml
name: Performance Gates
on: [pull_request]

jobs:
  performance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build
        run: npm run build
      
      - name: Bundle Size Check
        uses: andresz1/size-limit-action@v1
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          limit: 10%  # Max 10% increase
      
      - name: Lighthouse CI
        uses: treosh/lighthouse-ci-action@v9
        with:
          runs: 3
          assertions:
            performance: 90
            accessibility: 90
      
      - name: API Benchmark
        run: npm run benchmark:api
```

---

## Configuration

### Bundle Size Limit
```json
{
  "size-limit": [
    {
      "path": "dist/bundle.js",
      "limit": "250 KB",
      "gzip": true
    }
  ]
}
```

### Lighthouse Thresholds
```json
{
  "ci": {
    "assert": {
      "assertions": {
        "performance": ["error", {"minScore": 0.9}],
        "first-contentful-paint": ["error", {"maxNumericValue": 2000}],
        "interactive": ["error", {"maxNumericValue": 3500}]
      }
    }
  }
}
```

---

## Summary

**Performance Gates:** ป้องกัน performance regression

**Metrics:**
- Bundle size: No >10% increase
- Response time: No >20% slower
- Lighthouse: Score ≥90

**Tools:**
- size-limit (bundle)
- Lighthouse CI (load time)
- Custom benchmarks (API)

**Action:** Block merge if regression detected
