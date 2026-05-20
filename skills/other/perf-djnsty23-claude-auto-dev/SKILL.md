---
name: perf
description: Web performance audit - Core Web Vitals, bundle analysis, Lighthouse patterns.
triggers:
  - perf
  - performance
  - lighthouse
  - bundle size
  - core web vitals
allowed-tools: Bash, Read, Grep, Glob
model: opus
user-invocable: true
---

# Performance Audit

## Quick Checks

Run in parallel:

```bash
# Bundle analysis
npx next build 2>&1 | tail -30     # Check bundle sizes
npx @next/bundle-analyzer           # Visual treemap (if installed)

# Lighthouse (requires Chrome)
npx lighthouse http://localhost:3000 --output=json --quiet
```

## Core Web Vitals Targets

| Metric | Good | Needs Work | Poor |
|--------|------|------------|------|
| **LCP** (Largest Contentful Paint) | < 2.5s | 2.5-4s | > 4s |
| **INP** (Interaction to Next Paint) | < 200ms | 200-500ms | > 500ms |
| **CLS** (Cumulative Layout Shift) | < 0.1 | 0.1-0.25 | > 0.25 |
| **FCP** (First Contentful Paint) | < 1.8s | 1.8-3s | > 3s |
| **TTFB** (Time to First Byte) | < 800ms | 800-1800ms | > 1800ms |

## Bundle Size Rules

| Category | Target | Action if Over |
|----------|--------|----------------|
| Total JS | < 200KB gzipped | Code split, lazy load |
| Single chunk | < 50KB | Dynamic import |
| Images | < 100KB each | WebP, compress, lazy load |
| Fonts | < 50KB per font | Subset, swap display |

## Common Fixes (Priority Order)

### 1. Images (Biggest Impact)

```tsx
// ❌ Bad
<img src="/hero.png" />

// ✅ Good - Next.js Image
import Image from 'next/image'
<Image src="/hero.png" width={1200} height={600} priority />
```

- Use `next/image` for automatic WebP, sizing, lazy load
- Add `priority` to above-the-fold images (LCP)
- Use `loading="lazy"` for below-fold

### 2. Code Splitting

```tsx
// ❌ Bad - imports everything upfront
import { HeavyChart } from '@/components/heavy-chart'

// ✅ Good - lazy load
import dynamic from 'next/dynamic'
const HeavyChart = dynamic(() => import('@/components/heavy-chart'), {
  loading: () => <Skeleton className="h-64" />
})
```

### 3. React Performance

```tsx
// Memo expensive components
const ExpensiveList = React.memo(({ items }) => (
  items.map(item => <Card key={item.id} {...item} />)
))

// useMemo for expensive calculations
const sorted = useMemo(() =>
  items.sort((a, b) => b.score - a.score),
  [items]
)

// useCallback for stable references
const handleClick = useCallback((id: string) => {
  setSelected(id)
}, [])
```

### 4. Font Loading

```tsx
// next/font - zero layout shift
import { Inter } from 'next/font/google'
const inter = Inter({ subsets: ['latin'], display: 'swap' })
```

### 5. Third-Party Scripts

```tsx
// Defer non-critical scripts
<Script src="https://analytics.com/script.js" strategy="lazyOnload" />
```

### 6. Database (Supabase)

```typescript
// ❌ Bad - fetches all columns
const { data } = await supabase.from('songs').select('*')

// ✅ Good - select only needed columns
const { data } = await supabase
  .from('songs')
  .select('id, title, artist_id, audio_url')
  .limit(20)
```

## Audit Report Format

```
Performance Audit
─────────────────
LCP: 1.8s ✅
INP: 150ms ✅
CLS: 0.05 ✅
FCP: 1.2s ✅

Bundle: 180KB gzipped ✅
Largest chunk: audio-player.js (45KB) ✅

Issues Found:
1. [HIGH] Unoptimized hero image (2.1MB PNG) → Convert to WebP
2. [MEDIUM] No code splitting on /studio page → Dynamic import
3. [LOW] Unused lodash import → Replace with native

Score: 85/100
```

## Integration

| Skill | How It Integrates |
|-------|-------------------|
| `audit` | Perf agent uses these patterns |
| `ship` | Pre-deploy perf check |
| `review` | Flag perf regressions in code review |
