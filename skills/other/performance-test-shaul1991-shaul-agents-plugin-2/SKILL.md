---
name: performance-test
description: Performance Test Agent. 성능 테스트 계획 및 실행을 담당합니다. Load Test, Lighthouse, Core Web Vitals 측정을 수행합니다.
allowed-tools: Bash(npm:*, npx:lighthouse*, k6:*, artillery:*), Read, Write, Edit, Grep, Glob
---

# Performance Test Agent

## 역할

애플리케이션의 성능을 측정하고 최적화 포인트를 식별합니다.

## 성능 테스트 유형

```
┌─────────────────────────────────────────────────────────────────┐
│                      성능 테스트 피라미드                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                         /\                                      │
│                        /  \                                     │
│                       / 부하 \       ← Stress/Load Test         │
│                      /  테스트 \        (시스템 한계 확인)         │
│                     /----------\                                │
│                    /   성능     \    ← Performance Test         │
│                   /   테스트     \      (응답 시간, 처리량)        │
│                  /--------------\                               │
│                 /   프론트엔드   \  ← Frontend Performance       │
│                /    성능 측정     \    (Lighthouse, CWV)         │
│               /------------------\                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Frontend 성능 측정

### Lighthouse

```bash
# CLI 실행
npx lighthouse https://example.com --output=json --output-path=./lighthouse-report.json

# 특정 카테고리만
npx lighthouse https://example.com --only-categories=performance,accessibility

# 모바일/데스크톱
npx lighthouse https://example.com --preset=desktop
npx lighthouse https://example.com --preset=mobile

# CI 통합
npx lhci autorun
```

### Lighthouse CI 설정

```js
// lighthouserc.js
module.exports = {
  ci: {
    collect: {
      url: ['http://localhost:3000/', 'http://localhost:3000/products'],
      numberOfRuns: 3,
    },
    assert: {
      assertions: {
        'categories:performance': ['error', { minScore: 0.9 }],
        'categories:accessibility': ['error', { minScore: 0.9 }],
        'categories:best-practices': ['error', { minScore: 0.9 }],
        'categories:seo': ['error', { minScore: 0.9 }],
        'first-contentful-paint': ['error', { maxNumericValue: 1500 }],
        'largest-contentful-paint': ['error', { maxNumericValue: 2500 }],
        'cumulative-layout-shift': ['error', { maxNumericValue: 0.1 }],
        'total-blocking-time': ['error', { maxNumericValue: 200 }],
      },
    },
    upload: {
      target: 'temporary-public-storage',
    },
  },
};
```

### Core Web Vitals 기준

| 지표 | Good | Needs Improvement | Poor |
|------|------|-------------------|------|
| **LCP** (Largest Contentful Paint) | ≤ 2.5s | ≤ 4.0s | > 4.0s |
| **FID** (First Input Delay) | ≤ 100ms | ≤ 300ms | > 300ms |
| **CLS** (Cumulative Layout Shift) | ≤ 0.1 | ≤ 0.25 | > 0.25 |
| **INP** (Interaction to Next Paint) | ≤ 200ms | ≤ 500ms | > 500ms |
| **TTFB** (Time to First Byte) | ≤ 800ms | ≤ 1800ms | > 1800ms |

### Web Vitals 측정 코드

```typescript
// src/utils/web-vitals.ts
import { onCLS, onFID, onLCP, onTTFB, onINP } from 'web-vitals';

const sendToAnalytics = (metric: any) => {
  console.log(metric);
  // 분석 서비스로 전송
};

export const measureWebVitals = () => {
  onCLS(sendToAnalytics);
  onFID(sendToAnalytics);
  onLCP(sendToAnalytics);
  onTTFB(sendToAnalytics);
  onINP(sendToAnalytics);
};
```

## Backend 성능 테스트

### k6 Load Test

```javascript
// load-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  // 단계별 부하
  stages: [
    { duration: '1m', target: 50 },   // Ramp up
    { duration: '3m', target: 50 },   // Steady state
    { duration: '1m', target: 100 },  // Spike
    { duration: '2m', target: 100 },  // Steady high
    { duration: '1m', target: 0 },    // Ramp down
  ],

  // 성능 기준
  thresholds: {
    http_req_duration: ['p(95)<500'],  // 95% 요청이 500ms 이내
    http_req_failed: ['rate<0.01'],    // 실패율 1% 미만
    http_reqs: ['rate>100'],           // 초당 100 요청 이상
  },
};

export default function () {
  // API 호출
  const response = http.get('http://localhost:3000/api/users');

  // 검증
  check(response, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });

  sleep(1);
}

// 시나리오 기반 테스트
export function scenario() {
  const loginRes = http.post('http://localhost:3000/api/auth/login', {
    email: 'test@test.com',
    password: 'password',
  });

  const token = loginRes.json('token');

  const usersRes = http.get('http://localhost:3000/api/users', {
    headers: { Authorization: `Bearer ${token}` },
  });

  check(usersRes, {
    'users fetched': (r) => r.json('data').length > 0,
  });
}
```

### k6 실행

```bash
# 기본 실행
k6 run load-test.js

# VU(Virtual Users) 지정
k6 run --vus 10 --duration 30s load-test.js

# 결과 출력
k6 run --out json=results.json load-test.js

# Cloud 실행
k6 cloud load-test.js
```

### Artillery 테스트

```yaml
# artillery-config.yml
config:
  target: 'http://localhost:3000'
  phases:
    - duration: 60
      arrivalRate: 10
      name: "Warm up"
    - duration: 120
      arrivalRate: 50
      name: "Sustained load"
    - duration: 60
      arrivalRate: 100
      name: "Peak load"

  defaults:
    headers:
      Content-Type: 'application/json'

scenarios:
  - name: "User flow"
    flow:
      - get:
          url: "/api/products"
          capture:
            - json: "$.data[0].id"
              as: "productId"

      - post:
          url: "/api/cart"
          json:
            productId: "{{ productId }}"
            quantity: 1
          expect:
            - statusCode: 201

      - get:
          url: "/api/cart"
          expect:
            - statusCode: 200
```

```bash
# Artillery 실행
artillery run artillery-config.yml

# 리포트 생성
artillery run --output results.json artillery-config.yml
artillery report results.json
```

## 성능 기준 정의

```markdown
## 성능 요구사항

### API 응답 시간
| 엔드포인트 | P50 | P95 | P99 |
|-----------|-----|-----|-----|
| GET /api/users | < 100ms | < 300ms | < 500ms |
| POST /api/users | < 200ms | < 500ms | < 1s |
| GET /api/products | < 150ms | < 400ms | < 800ms |

### 처리량 (Throughput)
- 최소: 100 RPS
- 목표: 500 RPS
- 피크: 1000 RPS

### Frontend
| 지표 | 목표 |
|------|------|
| LCP | < 2.5s |
| FID | < 100ms |
| CLS | < 0.1 |
| Lighthouse Score | > 90 |

### 에러율
- 목표: < 0.1%
- 허용: < 1%
```

## CI 통합

```yaml
# .github/workflows/performance.yml
name: Performance Test

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci
      - run: npm run build
      - run: npm start &
      - name: Lighthouse CI
        run: npx lhci autorun
        env:
          LHCI_GITHUB_APP_TOKEN: ${{ secrets.LHCI_GITHUB_APP_TOKEN }}

  load-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run k6 tests
        uses: grafana/k6-action@v0.3.1
        with:
          filename: tests/load/load-test.js
          flags: --out json=results.json
      - name: Upload results
        uses: actions/upload-artifact@v4
        with:
          name: k6-results
          path: results.json
```

## 리포트 템플릿

```markdown
# 성능 테스트 리포트

## 테스트 정보
- 날짜: 2024-01-15
- 환경: Staging
- 버전: v1.2.0

## Frontend 성능 (Lighthouse)

### Desktop
| 페이지 | Performance | Accessibility | Best Practices | SEO |
|--------|------------|---------------|----------------|-----|
| Home | 95 | 100 | 100 | 100 |
| Products | 88 | 98 | 100 | 95 |
| Checkout | 82 | 95 | 92 | 100 |

### Mobile
| 페이지 | Performance | LCP | FID | CLS |
|--------|------------|-----|-----|-----|
| Home | 78 | 2.1s | 45ms | 0.05 |
| Products | 65 | 3.2s | 120ms | 0.12 |

## Backend 성능 (k6)

### 부하 테스트 결과
| 지표 | 결과 | 목표 | 상태 |
|------|------|------|------|
| P95 응답시간 | 320ms | < 500ms | ✅ |
| P99 응답시간 | 480ms | < 1s | ✅ |
| 처리량 | 450 RPS | > 100 RPS | ✅ |
| 에러율 | 0.05% | < 1% | ✅ |

### 상세 결과
```
http_req_duration:
  avg: 125ms
  min: 12ms
  med: 98ms
  max: 890ms
  p(90): 250ms
  p(95): 320ms

http_reqs: 27000 total, 450/s
```

## 병목점 분석
1. Products 페이지 LCP 개선 필요
2. Checkout 페이지 Performance 점수 향상 필요

## 권장사항
1. 이미지 최적화 (WebP 적용)
2. 코드 스플리팅 적용
3. API 응답 캐싱 도입
```

## 산출물 위치

- Lighthouse 리포트: `docs/features/<기능명>/test-results/lighthouse-report.html`
- k6 결과: `docs/features/<기능명>/test-results/k6-results.json`
- 성능 리포트: `docs/features/<기능명>/test-results/performance-report.md`
