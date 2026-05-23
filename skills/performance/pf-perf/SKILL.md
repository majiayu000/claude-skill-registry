---
name: pf-perf
description: 성능 최적화 제안. "성능", "최적화", "느림", "번들" 관련 요청 시 사용.
allowed-tools: Read, Bash, Glob, Grep
---

# PF 성능 최적화

$ARGUMENTS 성능 문제를 분석하고 최적화를 제안합니다.

---

## 1. 번들 크기 분석

### 번들 시각화

```bash
# vite-bundle-visualizer 설치
pnpm add -D rollup-plugin-visualizer

# vite.config.ts
import { visualizer } from "rollup-plugin-visualizer";

export default defineConfig({
  plugins: [
    visualizer({
      open: true,
      filename: "stats.html",
    }),
  ],
});

# 빌드 후 stats.html 확인
pnpm build
```

### 큰 패키지 확인

```bash
# 패키지 크기 확인
npx vite-bundle-analyzer
```

---

## 2. 코드 스플리팅

### 라우트 기반 분할

```tsx
import { lazy, Suspense } from "react";

// ❌ 정적 import (모든 페이지가 초기 번들에 포함)
import HomePage from "./pages/home";
import DashboardPage from "./pages/dashboard";

// ✅ 동적 import (필요할 때 로드)
const HomePage = lazy(() => import("./pages/home"));
const DashboardPage = lazy(() => import("./pages/dashboard"));

function Routes() {
  return (
    <Suspense fallback={<PageSkeleton />}>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
      </Routes>
    </Suspense>
  );
}
```

### 컴포넌트 분할

```tsx
// 무거운 컴포넌트 지연 로드
const HeavyChart = lazy(() => import("./components/HeavyChart"));
const MapViewer = lazy(() => import("@pf-dev/map").then(m => ({ default: m.MapViewer })));

function Dashboard() {
  return (
    <div>
      <Suspense fallback={<ChartSkeleton />}>
        <HeavyChart data={data} />
      </Suspense>
    </div>
  );
}
```

---

## 3. 의존성 최적화

### Barrel Import 피하기

```tsx
// ❌ 전체 패키지 import (tree-shaking 불가능할 수 있음)
import { Button, Input, Select, Dialog } from "@pf-dev/ui";

// ✅ 직접 import (확실한 tree-shaking)
import { Button } from "@pf-dev/ui/atoms/Button";
import { Input } from "@pf-dev/ui/atoms/Input";
```

### 무거운 패키지 대체

| 패키지 | 크기 | 대안 |
|--------|------|------|
| moment.js | 288KB | date-fns (30KB) |
| lodash | 71KB | lodash-es + 개별 import |
| chart.js | 200KB+ | lightweight-charts |

```tsx
// ❌ 전체 lodash
import _ from "lodash";
_.debounce(fn, 300);

// ✅ 개별 함수만
import debounce from "lodash-es/debounce";
debounce(fn, 300);
```

---

## 4. React 렌더링 최적화

### 불필요한 리렌더링 방지

```tsx
// React DevTools Profiler로 확인
// Components > Profiler > 녹화

// 1. Selector로 Zustand 구독 최적화
const user = useAuthStore(state => state.user);  // ✅ user만 구독
const { user, settings } = useAuthStore();       // ❌ 전체 구독

// 2. 객체/배열 props 메모이제이션 (필요시)
const columns = useMemo(() => [
  { key: "name", label: "이름" },
  { key: "email", label: "이메일" },
], []);

// 3. 콜백 메모이제이션 (필요시)
const handleClick = useCallback((id) => {
  deleteItem(id);
}, [deleteItem]);
```

### 큰 리스트 가상화

```tsx
import { useVirtualizer } from "@tanstack/react-virtual";

function VirtualList({ items }: { items: Item[] }) {
  const parentRef = useRef<HTMLDivElement>(null);

  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50,  // 예상 아이템 높이
  });

  return (
    <div ref={parentRef} className="h-[400px] overflow-auto">
      <div
        style={{
          height: `${virtualizer.getTotalSize()}px`,
          position: "relative",
        }}
      >
        {virtualizer.getVirtualItems().map((virtualItem) => (
          <div
            key={virtualItem.key}
            style={{
              position: "absolute",
              top: 0,
              left: 0,
              width: "100%",
              height: `${virtualItem.size}px`,
              transform: `translateY(${virtualItem.start}px)`,
            }}
          >
            <ItemRow item={items[virtualItem.index]} />
          </div>
        ))}
      </div>
    </div>
  );
}
```

---

## 5. 이미지 최적화

```tsx
// 1. lazy loading
<img src="/image.jpg" loading="lazy" alt="..." />

// 2. 적절한 크기
<img
  src="/image.jpg"
  srcSet="/image-400.jpg 400w, /image-800.jpg 800w"
  sizes="(max-width: 600px) 400px, 800px"
  alt="..."
/>

// 3. WebP 포맷
<picture>
  <source srcSet="/image.webp" type="image/webp" />
  <img src="/image.jpg" alt="..." />
</picture>
```

---

## 6. API 최적화

### 요청 병렬화

```tsx
// ❌ 순차 요청
const users = await fetchUsers();
const posts = await fetchPosts();
const comments = await fetchComments();

// ✅ 병렬 요청
const [users, posts, comments] = await Promise.all([
  fetchUsers(),
  fetchPosts(),
  fetchComments(),
]);
```

### 캐싱

```tsx
// React Query / SWR 사용
const { data } = useQuery({
  queryKey: ["users"],
  queryFn: fetchUsers,
  staleTime: 5 * 60 * 1000,  // 5분간 캐시
});
```

---

## 7. 측정 도구

### Lighthouse

```bash
# CLI로 실행
npx lighthouse http://localhost:3000 --view
```

**목표 점수:**
- Performance: 90+
- Accessibility: 90+
- Best Practices: 90+
- SEO: 90+

### Web Vitals

```tsx
import { onCLS, onFID, onLCP, onFCP, onTTFB } from "web-vitals";

onCLS(console.log);   // Cumulative Layout Shift
onFID(console.log);   // First Input Delay
onLCP(console.log);   // Largest Contentful Paint
onFCP(console.log);   // First Contentful Paint
onTTFB(console.log);  // Time to First Byte
```

**목표:**
- LCP: < 2.5초
- FID: < 100ms
- CLS: < 0.1

---

## 8. 빌드 최적화

### Vite 설정

```ts
// vite.config.ts
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ["react", "react-dom"],
          cesium: ["cesium"],
          three: ["three", "@react-three/fiber"],
        },
      },
    },
    chunkSizeWarningLimit: 500,  // KB
  },
});
```

### 압축

```ts
import viteCompression from "vite-plugin-compression";

export default defineConfig({
  plugins: [
    viteCompression({
      algorithm: "gzip",
    }),
    viteCompression({
      algorithm: "brotliCompress",
    }),
  ],
});
```

---

## 체크리스트

- [ ] 번들 크기 500KB 이하
- [ ] 라우트별 코드 스플리팅
- [ ] 불필요한 리렌더링 없음
- [ ] 이미지 lazy loading
- [ ] API 요청 병렬화/캐싱
- [ ] Lighthouse 성능 90+
- [ ] LCP < 2.5초
