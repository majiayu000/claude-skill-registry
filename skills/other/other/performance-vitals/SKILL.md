---
name: performance-vitals
description: Enforce Core Web Vitals optimization. Use when building user-facing features, reviewing performance, or when Lighthouse scores drop. Covers LCP, FID/INP, CLS, and optimization techniques.
allowed-tools: Read, Glob, Grep, Edit, Write, Bash
license: MIT
metadata:
  author: antigravity-team
  version: "1.0"
---

# Performance & Core Web Vitals

Core Web Vitals 최적화를 강제하는 스킬입니다.

## 2025 Context

> **2024년 3월: INP(Interaction to Next Paint)가 FID를 대체**
> **Google Search 랭킹에 Core Web Vitals 영향**

## Core Web Vitals 목표

| 지표 | Good | Needs Improvement | Poor |
|------|------|-------------------|------|
| **LCP** (Largest Contentful Paint) | ≤ 2.5s | 2.5s - 4s | > 4s |
| **INP** (Interaction to Next Paint) | ≤ 200ms | 200ms - 500ms | > 500ms |
| **CLS** (Cumulative Layout Shift) | ≤ 0.1 | 0.1 - 0.25 | > 0.25 |

## LCP 최적화 (Largest Contentful Paint)

### 문제 원인

- 느린 서버 응답
- 렌더 차단 리소스 (CSS, JS)
- 느린 리소스 로딩
- 클라이언트 사이드 렌더링

### 해결 방법

#### 1. 이미지 최적화

```tsx
// ❌ BAD: 최적화 없는 이미지
<img src="/hero.jpg" alt="Hero" />

// ✅ GOOD: Next.js Image 컴포넌트
import Image from 'next/image';

<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  priority  // LCP 이미지는 priority 추가
  placeholder="blur"
  blurDataURL={blurDataUrl}
/>
```

#### 2. 폰트 최적화

```tsx
// ✅ GOOD: Next.js 폰트 최적화
import { Inter } from 'next/font/google';

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',  // FOIT 방지
  preload: true,
});

// CSS
@font-face {
  font-family: 'Custom Font';
  src: url('/fonts/custom.woff2') format('woff2');
  font-display: swap;
}
```

#### 3. Critical CSS 인라인

```tsx
// next.config.js
module.exports = {
  experimental: {
    optimizeCss: true,
  },
};
```

#### 4. 프리로드

```html
<!-- 중요 리소스 프리로드 -->
<link rel="preload" href="/hero.jpg" as="image" />
<link rel="preload" href="/fonts/main.woff2" as="font" crossorigin />
<link rel="preconnect" href="https://api.example.com" />
```

## INP 최적화 (Interaction to Next Paint)

### 문제 원인

- 긴 JavaScript 태스크
- 과도한 DOM 크기
- 비효율적인 이벤트 핸들러

### 해결 방법

#### 1. 긴 태스크 분할

```typescript
// ❌ BAD: 긴 동기 작업
function processLargeData(items: Item[]) {
  items.forEach(item => {
    heavyComputation(item);  // 메인 스레드 블로킹
  });
}

// ✅ GOOD: 청크 분할 + yield
async function processLargeData(items: Item[]) {
  const CHUNK_SIZE = 100;

  for (let i = 0; i < items.length; i += CHUNK_SIZE) {
    const chunk = items.slice(i, i + CHUNK_SIZE);
    chunk.forEach(item => heavyComputation(item));

    // 브라우저에 제어권 반환
    await new Promise(resolve => setTimeout(resolve, 0));
  }
}
```

#### 2. 이벤트 핸들러 최적화

```tsx
// ❌ BAD: 무거운 핸들러
<input onChange={(e) => {
  const value = e.target.value;
  validateAllFields();  // 무거운 연산
  updateUI();
  sendAnalytics();
}} />

// ✅ GOOD: 디바운스 + 분리
import { useDeferredValue, useTransition } from 'react';

function SearchInput() {
  const [input, setInput] = useState('');
  const deferredInput = useDeferredValue(input);
  const [isPending, startTransition] = useTransition();

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    setInput(e.target.value);  // 즉시 업데이트

    startTransition(() => {
      // 덜 급한 업데이트는 transition으로
      performSearch(e.target.value);
    });
  };

  return <input value={input} onChange={handleChange} />;
}
```

#### 3. Web Worker 활용

```typescript
// worker.ts
self.onmessage = (e) => {
  const result = heavyComputation(e.data);
  self.postMessage(result);
};

// main.ts
const worker = new Worker(new URL('./worker.ts', import.meta.url));

worker.postMessage(data);
worker.onmessage = (e) => {
  setResult(e.data);
};
```

## CLS 최적화 (Cumulative Layout Shift)

### 문제 원인

- 크기 미지정 이미지/비디오
- 동적 콘텐츠 삽입
- 웹폰트 FOIT/FOUT
- 애니메이션

### 해결 방법

#### 1. 이미지/비디오 크기 지정

```tsx
// ❌ BAD: 크기 미지정
<img src="/photo.jpg" alt="Photo" />

// ✅ GOOD: 크기 명시
<img
  src="/photo.jpg"
  alt="Photo"
  width={800}
  height={600}
/>

// ✅ GOOD: aspect-ratio 사용
<div style={{ aspectRatio: '16/9' }}>
  <img src="/video-thumb.jpg" alt="Video" style={{ width: '100%' }} />
</div>
```

#### 2. 동적 콘텐츠 공간 확보

```tsx
// ❌ BAD: 공간 없이 동적 삽입
{isLoaded && <Banner />}

// ✅ GOOD: 스켈레톤으로 공간 확보
{isLoaded ? <Banner /> : <BannerSkeleton />}

// ✅ GOOD: min-height로 공간 확보
<div style={{ minHeight: '200px' }}>
  {isLoaded && <DynamicContent />}
</div>
```

#### 3. 폰트 로딩

```css
/* ✅ GOOD: font-display: swap */
@font-face {
  font-family: 'CustomFont';
  src: url('/font.woff2') format('woff2');
  font-display: swap;
}

/* ✅ GOOD: 폴백 폰트 크기 조정 */
@font-face {
  font-family: 'CustomFont';
  src: url('/font.woff2') format('woff2');
  font-display: swap;
  size-adjust: 105%;  /* 폴백 폰트와 크기 맞춤 */
}
```

#### 4. 애니메이션

```css
/* ❌ BAD: 레이아웃 속성 애니메이션 */
.animate {
  transition: width 0.3s, height 0.3s, margin 0.3s;
}

/* ✅ GOOD: transform, opacity만 사용 */
.animate {
  transition: transform 0.3s, opacity 0.3s;
}
```

## 측정 도구

### Lighthouse CI

```yaml
# .github/workflows/lighthouse.yml
name: Lighthouse CI

on: [push]

jobs:
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Lighthouse CI
        uses: treosh/lighthouse-ci-action@v10
        with:
          urls: |
            https://example.com/
            https://example.com/dashboard
          budgetPath: ./lighthouse-budget.json
          uploadArtifacts: true
```

### lighthouse-budget.json

```json
[
  {
    "path": "/*",
    "timings": [
      { "metric": "largest-contentful-paint", "budget": 2500 },
      { "metric": "cumulative-layout-shift", "budget": 0.1 },
      { "metric": "interaction-to-next-paint", "budget": 200 }
    ]
  }
]
```

### web-vitals 라이브러리

```tsx
import { onCLS, onINP, onLCP } from 'web-vitals';

function sendToAnalytics(metric: Metric) {
  console.log(metric.name, metric.value);

  // Analytics 전송
  gtag('event', metric.name, {
    value: metric.delta,
    metric_id: metric.id,
    metric_value: metric.value,
    metric_delta: metric.delta,
  });
}

onCLS(sendToAnalytics);
onINP(sendToAnalytics);
onLCP(sendToAnalytics);
```

## 빠른 최적화 체크리스트

### LCP 개선

- [ ] LCP 이미지에 `priority` 또는 `preload`
- [ ] 이미지 포맷 최적화 (WebP/AVIF)
- [ ] 서버 응답 시간 < 600ms
- [ ] Critical CSS 인라인
- [ ] 렌더 차단 리소스 제거

### INP 개선

- [ ] Long Task > 50ms 제거
- [ ] 이벤트 핸들러 최적화
- [ ] 무거운 연산 Web Worker로 이동
- [ ] `useTransition`, `useDeferredValue` 활용
- [ ] Third-party 스크립트 지연 로딩

### CLS 개선

- [ ] 모든 이미지/비디오 크기 지정
- [ ] 동적 콘텐츠 공간 확보 (스켈레톤)
- [ ] `font-display: swap` 설정
- [ ] transform/opacity만 애니메이션

## Workflow

### 1. 성능 측정

```bash
# Lighthouse CLI
npx lighthouse https://example.com --output=json --output-path=./lh-report.json

# 또는 Chrome DevTools > Lighthouse 탭
```

### 2. 문제 진단

```
LCP > 2.5s?
→ Network 탭에서 LCP 리소스 확인
→ 이미지 최적화 / 프리로드 적용

INP > 200ms?
→ Performance 탭에서 Long Task 확인
→ 태스크 분할 / Web Worker 적용

CLS > 0.1?
→ Layout Shift 원인 요소 확인
→ 크기 지정 / 스켈레톤 적용
```

### 3. 모니터링

```
프로덕션:
- Google Search Console Core Web Vitals
- Real User Monitoring (RUM)
- web-vitals 라이브러리

CI/CD:
- Lighthouse CI
- Performance Budget 설정
```

## References

- [web.dev Core Web Vitals](https://web.dev/vitals/)
- [Lighthouse](https://developer.chrome.com/docs/lighthouse/)
- [web-vitals library](https://github.com/GoogleChrome/web-vitals)
