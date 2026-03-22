---
name: performance-optimization
description: Optimize application performance for speed, efficiency, and scalability. Use when improving page load times, reducing bundle size, optimizing database queries, or fixing performance bottlenecks. Handles React optimization, lazy loading, caching, code splitting, and profiling.
tags: [performance, optimization, React, lazy-loading, caching, profiling, web-vitals]
platforms: [Claude, ChatGPT, Gemini]
---

# Performance Optimization


## When to use this skill

- **느린 페이지 로드**: Lighthouse 점수 낮음
- **느린 렌더링**: 사용자 인터랙션 지연
- **큰 번들 크기**: 다운로드 시간 증가
- **느린 쿼리**: 데이터베이스 병목

## Instructions

### Step 1: 성능 측정

**Lighthouse (Chrome DevTools)**:
```bash
# CLI
npm install -g lighthouse
lighthouse https://example.com --view

# CI에서 자동화
lighthouse https://example.com --output=json --output-path=./report.json
```

**Web Vitals 측정** (React):
```typescript
import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

function sendToAnalytics(metric: any) {
  // Google Analytics, Datadog 등으로 전송
  console.log(metric);
}

getCLS(sendToAnalytics);
getFID(sendToAnalytics);
getFCP(sendToAnalytics);
getLCP(sendToAnalytics);
getTTFB(sendToAnalytics);
```

### Step 2: React 최적화

**React.memo (불필요한 리렌더링 방지)**:
```tsx
// ❌ 나쁜 예: 부모가 리렌더링될 때마다 자식도 리렌더링
function ExpensiveComponent({ data }: { data: Data }) {
  return <div>{/* 복잡한 렌더링 */}</div>;
}

// ✅ 좋은 예: props 변경 시에만 리렌더링
const ExpensiveComponent = React.memo(({ data }: { data: Data }) => {
  return <div>{/* 복잡한 렌더링 */}</div>;
});
```

**useMemo & useCallback**:
```tsx
function ProductList({ products, category }: Props) {
  // ✅ 필터링 결과 메모이제이션
  const filteredProducts = useMemo(() => {
    return products.filter(p => p.category === category);
  }, [products, category]);

  // ✅ 콜백 메모이제이션
  const handleAddToCart = useCallback((id: string) => {
    addToCart(id);
  }, []);

  return (
    <div>
      {filteredProducts.map(product => (
        <ProductCard key={product.id} product={product} onAdd={handleAddToCart} />
      ))}
    </div>
  );
}
```

**Lazy Loading & Code Splitting**:
```tsx
import { lazy, Suspense } from 'react';

// ✅ Route-based code splitting
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Profile = lazy(() => import('./pages/Profile'));
const Settings = lazy(() => import('./pages/Settings'));

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Suspense>
  );
}

// ✅ Component-based lazy loading
const HeavyChart = lazy(() => import('./components/HeavyChart'));

function Dashboard() {
  return (
    <div>
      <h1>Dashboard</h1>
      <Suspense fallback={<Skeleton />}>
        <HeavyChart data={data} />
      </Suspense>
    </div>
  );
}
```

### Step 3: 번들 크기 최적화

**Webpack Bundle Analyzer**:
```bash
npm install --save-dev webpack-bundle-analyzer

# package.json
{
  "scripts": {
    "analyze": "webpack-bundle-analyzer build/stats.json"
  }
}
```

**Tree Shaking (사용하지 않는 코드 제거)**:
```typescript
// ❌ 나쁜 예: 전체 라이브러리 임포트
import _ from 'lodash';

// ✅ 좋은 예: 필요한 것만 임포트
import debounce from 'lodash/debounce';
```

**Dynamic Imports**:
```typescript
// ✅ 필요할 때만 로드
button.addEventListener('click', async () => {
  const { default: Chart } = await import('chart.js');
  new Chart(ctx, config);
});
```

### Step 4: 이미지 최적화

**Next.js Image 컴포넌트**:
```tsx
import Image from 'next/image';

function ProductImage() {
  return (
    <Image
      src="/product.jpg"
      alt="Product"
      width={500}
      height={500}
      priority  // LCP 이미지인 경우
      placeholder="blur"  // 블러 플레이스홀더
      sizes="(max-width: 768px) 100vw, 50vw"
    />
  );
}
```

**WebP 포맷 사용**:
```html
<picture>
  <source srcset="image.webp" type="image/webp">
  <source srcset="image.jpg" type="image/jpeg">
  <img src="image.jpg" alt="Fallback">
</picture>
```

### Step 5: 데이터베이스 쿼리 최적화

**N+1 쿼리 문제 해결**:
```typescript
// ❌ 나쁜 예: N+1 queries
const posts = await db.post.findMany();
for (const post of posts) {
  const author = await db.user.findUnique({ where: { id: post.authorId } });
  // 101번 쿼리 (1 + 100)
}

// ✅ 좋은 예: JOIN 또는 include
const posts = await db.post.findMany({
  include: {
    author: true
  }
});
// 1번 쿼리
```

**인덱스 추가**:
```sql
-- 느린 쿼리 식별
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';

-- 인덱스 추가
CREATE INDEX idx_users_email ON users(email);

-- 복합 인덱스
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at);
```

**캐싱 (Redis)**:
```typescript
async function getUserProfile(userId: string) {
  // 1. 캐시 확인
  const cached = await redis.get(`user:${userId}`);
  if (cached) {
    return JSON.parse(cached);
  }

  // 2. DB 조회
  const user = await db.user.findUnique({ where: { id: userId } });

  // 3. 캐시 저장 (1시간)
  await redis.setex(`user:${userId}`, 3600, JSON.stringify(user));

  return user;
}
```

## Output format

### 성능 최적화 체크리스트

```markdown
## Frontend
- [ ] React.memo로 불필요한 리렌더링 방지
- [ ] useMemo/useCallback 적절히 사용
- [ ] Lazy loading & Code splitting
- [ ] 이미지 최적화 (WebP, lazy loading)
- [ ] 번들 크기 분석 및 감소

## Backend
- [ ] N+1 쿼리 제거
- [ ] 데이터베이스 인덱스 추가
- [ ] Redis 캐싱
- [ ] API Response 압축 (gzip)
- [ ] CDN 사용

## 측정
- [ ] Lighthouse 점수 90+
- [ ] LCP < 2.5s
- [ ] FID < 100ms
- [ ] CLS < 0.1
```

## Constraints

### 필수 규칙 (MUST)

1. **측정 먼저**: 추측하지 말고 프로파일링
2. **점진적 개선**: 한 번에 하나씩 최적화
3. **성능 모니터링**: 지속적으로 추적

### 금지 사항 (MUST NOT)

1. **조기 최적화**: 병목이 없는데 최적화하지 않음
2. **가독성 희생**: 성능을 위해 코드를 복잡하게 만들지 않음

## Best practices

1. **80/20 법칙**: 20% 노력으로 80% 개선
2. **사용자 중심**: 실제 사용자 경험 개선에 집중
3. **자동화**: CI에서 성능 회귀 테스트

## References

- [web.dev/vitals](https://web.dev/vitals/)
- [React Optimization](https://react.dev/learn/render-and-commit#optimizing-performance)
- [Webpack Bundle Analyzer](https://github.com/webpack-contrib/webpack-bundle-analyzer)

## Metadata

### 버전
- **현재 버전**: 1.0.0
- **최종 업데이트**: 2025-01-01
- **호환 플랫폼**: Claude, ChatGPT, Gemini

### 관련 스킬
- [database-schema-design](../../backend/database/SKILL.md)
- [ui-components](../../frontend/ui-components/SKILL.md)

### 태그
`#performance` `#optimization` `#React` `#caching` `#lazy-loading` `#web-vitals` `#code-quality`

## Examples

### Example 1: Basic usage
<!-- Add example content here -->

### Example 2: Advanced usage
<!-- Add advanced example content here -->
