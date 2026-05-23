---
name: performance-optimization
description: Comprehensive performance optimization strategies for Next.js 16 applications including Core Web Vitals, caching, image optimization, bundle analysis, database query optimization, and Lighthouse audits. Use when user wants to improve performance, fix slow pages, reduce load times, or optimize for production.
---

# Performance Optimization Skill

Complete guide for optimizing The Simpsons API application performance, targeting Core Web Vitals excellence and production-ready metrics.

## When to Use This Skill

Use this skill when the user requests:

✅ **Primary Use Cases**

- "Improve performance"
- "Fix slow page"
- "Optimize load time"
- "Reduce bundle size"
- "Improve Core Web Vitals"
- "Make it faster"

✅ **Secondary Use Cases**

- "Analyze bundle"
- "Check lighthouse score"
- "Optimize images"
- "Add caching"
- "Fix layout shift"
- "Reduce LCP"

❌ **Do NOT use when**

- Fixing functional bugs (use debugging)
- Adding new features (use component-development)
- Database schema changes (use neon-database-management)
- Security improvements (use security tools)

---

## Core Web Vitals Targets

| Metric | Target | Good | Needs Work | Poor |
|--------|--------|------|------------|------|
| **LCP** (Largest Contentful Paint) | < 2.0s | ≤ 2.5s | 2.5-4.0s | > 4.0s |
| **INP** (Interaction to Next Paint) | < 100ms | ≤ 200ms | 200-500ms | > 500ms |
| **CLS** (Cumulative Layout Shift) | < 0.05 | ≤ 0.1 | 0.1-0.25 | > 0.25 |
| **FCP** (First Contentful Paint) | < 1.0s | ≤ 1.8s | 1.8-3.0s | > 3.0s |
| **TTFB** (Time to First Byte) | < 200ms | ≤ 800ms | 800-1800ms | > 1800ms |

---

## Part 1: Next.js Optimization

### 1.1 Image Optimization

```tsx
// ✅ GOOD: Use Next.js Image component
import Image from "next/image";

export function CharacterImage({ src, name }: { src: string; name: string }) {
  return (
    <Image
      src={src}
      alt={name}
      width={400}
      height={300}
      priority={false}
      loading="lazy"
      placeholder="blur"
      blurDataURL="data:image/jpeg;base64,/9j/4AAQSkZJRg..."
      className="rounded-lg object-cover"
    />
  );
}

// ✅ GOOD: Priority for above-the-fold images
export function HeroImage() {
  return (
    <Image
      src="/hero.jpg"
      alt="The Simpsons"
      width={1920}
      height={1080}
      priority // Preloads the image
      fetchPriority="high"
      className="w-full"
    />
  );
}

// ✅ GOOD: Responsive images with sizes
export function ResponsiveImage({ src }: { src: string }) {
  return (
    <Image
      src={src}
      alt=""
      fill
      sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
      className="object-cover"
    />
  );
}
```

### 1.2 Font Optimization

```tsx
// app/layout.tsx
import { Inter } from "next/font/google";

// ✅ GOOD: Load subset and display swap
const inter = Inter({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-inter",
  preload: true,
});

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={inter.variable}>
      <body className="font-sans">{children}</body>
    </html>
  );
}
```

### 1.3 Script Optimization

```tsx
import Script from "next/script";

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <>
      {children}
      
      {/* ✅ GOOD: Load analytics after page is interactive */}
      <Script
        src="https://analytics.example.com/script.js"
        strategy="afterInteractive"
      />
      
      {/* ✅ GOOD: Load non-critical scripts on worker thread */}
      <Script
        src="https://widget.example.com/script.js"
        strategy="lazyOnload"
      />
      
      {/* ✅ GOOD: Inline critical scripts */}
      <Script id="critical-script" strategy="beforeInteractive">
        {`window.dataLayer = window.dataLayer || [];`}
      </Script>
    </>
  );
}
```

### 1.4 Metadata Optimization

```tsx
// app/layout.tsx
import { Metadata } from "next";

export const metadata: Metadata = {
  title: {
    template: "%s | The Simpsons API",
    default: "The Simpsons API",
  },
  description: "Explore characters, episodes, and more from The Simpsons",
  // Preconnect to external resources
  other: {
    "link": [
      { rel: "preconnect", href: "https://fonts.googleapis.com" },
      { rel: "dns-prefetch", href: "https://api.thesimpsonsapi.com" },
    ],
  },
};
```

---

## Part 2: Caching Strategies

### 2.1 Route Segment Config

```tsx
// app/characters/page.tsx

// Static generation (cached at build time)
export const dynamic = "force-static";
export const revalidate = 3600; // Revalidate every hour

// For dynamic data
export const dynamic = "force-dynamic";

// For streaming
export const runtime = "edge";
```

### 2.2 Data Caching with unstable_cache

```tsx
import { unstable_cache } from "next/cache";
import { findAllCharacters } from "@/app/_lib/repositories";

const getCachedCharacters = unstable_cache(
  async () => {
    return findAllCharacters();
  },
  ["all-characters"],
  {
    revalidate: 3600, // 1 hour
    tags: ["characters"],
  }
);

export default async function CharactersPage() {
  const characters = await getCachedCharacters();
  return <CharacterList characters={characters} />;
}
```

### 2.3 Request Memoization

```tsx
// Next.js automatically dedupes fetch requests in the same render
async function getCharacter(id: number) {
  const res = await fetch(`/api/characters/${id}`, {
    next: { revalidate: 3600 },
  });
  return res.json();
}

// These calls are deduplicated - only 1 request made
export default async function Page() {
  const [character1, character2] = await Promise.all([
    getCharacter(1), // Same request
    getCharacter(1), // Deduplicated!
  ]);
  return <div>{character1.name}</div>;
}
```

### 2.4 Static Generation with generateStaticParams

```tsx
// app/characters/[id]/page.tsx
import { findAllCharacterIds } from "@/app/_lib/repositories";

export async function generateStaticParams() {
  const ids = await findAllCharacterIds();
  return ids.map((id) => ({ id: String(id) }));
}

export default async function CharacterPage({
  params,
}: {
  params: { id: string };
}) {
  const character = await findCharacterById(Number(params.id));
  return <CharacterDetail character={character} />;
}
```

---

## Part 3: Bundle Optimization

### 3.1 Bundle Analysis

```bash
# Install analyzer
pnpm add -D @next/bundle-analyzer

# Update next.config.ts
```

```typescript
// next.config.ts
import type { NextConfig } from "next";

const withBundleAnalyzer = require("@next/bundle-analyzer")({
  enabled: process.env.ANALYZE === "true",
});

const nextConfig: NextConfig = {
  // ... your config
};

export default withBundleAnalyzer(nextConfig);
```

```bash
# Analyze bundle
ANALYZE=true pnpm build
```

### 3.2 Dynamic Imports

```tsx
import dynamic from "next/dynamic";

// ✅ GOOD: Lazy load heavy components
const HeavyChart = dynamic(() => import("@/components/HeavyChart"), {
  loading: () => <div className="h-64 animate-pulse bg-muted rounded" />,
  ssr: false, // Client-only component
});

// ✅ GOOD: Lazy load below-the-fold content
const Comments = dynamic(() => import("@/components/Comments"));

export function CharacterPage({ character }) {
  return (
    <div>
      <CharacterHeader character={character} />
      <Suspense fallback={<CommentsSkeleton />}>
        <Comments characterId={character.id} />
      </Suspense>
    </div>
  );
}
```

### 3.3 Tree Shaking

```typescript
// ❌ BAD: Imports entire library
import _ from "lodash";
_.debounce(fn, 300);

// ✅ GOOD: Import specific function
import debounce from "lodash/debounce";
debounce(fn, 300);

// ❌ BAD: Import all icons
import * as Icons from "lucide-react";

// ✅ GOOD: Import specific icons
import { Home, User, Settings } from "lucide-react";
```

### 3.4 Package Import Optimization

```typescript
// next.config.ts
const nextConfig: NextConfig = {
  experimental: {
    optimizePackageImports: [
      "lucide-react",
      "@radix-ui/react-icons",
      "date-fns",
    ],
  },
};
```

---

## Part 4: Rendering Optimization

### 4.1 Streaming with Suspense

```tsx
import { Suspense } from "react";

export default function Page() {
  return (
    <div>
      {/* Critical content - renders immediately */}
      <h1>Characters</h1>
      
      {/* Streamed content - loads progressively */}
      <Suspense fallback={<CharacterListSkeleton />}>
        <CharacterList />
      </Suspense>
      
      {/* Lower priority content */}
      <Suspense fallback={<RecommendationsSkeleton />}>
        <Recommendations />
      </Suspense>
    </div>
  );
}
```

### 4.2 Parallel Data Fetching

```tsx
// ✅ GOOD: Parallel data fetching
export default async function Page() {
  // These run in parallel
  const [characters, episodes, stats] = await Promise.all([
    getCharacters(),
    getEpisodes(),
    getStats(),
  ]);

  return (
    <div>
      <Characters data={characters} />
      <Episodes data={episodes} />
      <Stats data={stats} />
    </div>
  );
}

// ❌ BAD: Sequential data fetching
export default async function Page() {
  const characters = await getCharacters(); // Wait...
  const episodes = await getEpisodes(); // Wait...
  const stats = await getStats(); // Wait...
  // Total time = sum of all requests
}
```

### 4.3 Avoid Layout Shifts

```tsx
// ✅ GOOD: Reserve space for dynamic content
export function ImageCard() {
  return (
    <div className="relative aspect-video"> {/* Fixed aspect ratio */}
      <Image
        src="/image.jpg"
        alt=""
        fill
        className="object-cover"
      />
    </div>
  );
}

// ✅ GOOD: Skeleton with matching dimensions
export function CardSkeleton() {
  return (
    <div className="w-full h-48 bg-muted animate-pulse rounded-lg" />
  );
}

// ✅ GOOD: Font display swap
const font = Inter({
  display: "swap", // Shows fallback font immediately
});
```

### 4.4 Reduce Client-Side JavaScript

```tsx
// ✅ GOOD: Server Component (default)
// No "use client" = 0 JS sent to client
export function StaticContent() {
  return <div>This sends no JavaScript</div>;
}

// ⚠️ Use sparingly: Client Component
"use client";
// Only use when you need:
// - useState, useEffect
// - Event handlers (onClick, onChange)
// - Browser APIs
export function InteractiveContent() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}
```

---

## Part 5: Database Optimization

### 5.1 Query Optimization

```typescript
// ❌ BAD: N+1 Query Problem
for (const character of characters) {
  const episodes = await query(
    `SELECT * FROM ${TABLES.episodes} WHERE character_id = $1`,
    [character.id]
  );
}

// ✅ GOOD: Single JOIN query
const data = await query(`
  SELECT c.*, json_agg(e.*) as episodes
  FROM ${TABLES.characters} c
  LEFT JOIN ${TABLES.character_episodes} ce ON ce.character_id = c.id
  LEFT JOIN ${TABLES.episodes} e ON e.id = ce.episode_id
  GROUP BY c.id
`);

// ✅ GOOD: Batch query with ANY
const characterIds = characters.map(c => c.id);
const allEpisodes = await query(`
  SELECT * FROM ${TABLES.episodes}
  WHERE character_id = ANY($1)
`, [characterIds]);
```

### 5.2 Indexing Strategy

```sql
-- Check slow queries first
SELECT 
  query,
  calls,
  mean_time,
  total_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;

-- Add indexes for common query patterns
CREATE INDEX CONCURRENTLY idx_characters_name 
ON the_simpson.characters(name);

CREATE INDEX CONCURRENTLY idx_episodes_season_episode 
ON the_simpson.episodes(season, episode_number);

-- Partial index for common filter
CREATE INDEX CONCURRENTLY idx_active_users 
ON the_simpson.users(id) 
WHERE deleted_at IS NULL;
```

### 5.3 Connection Optimization

```typescript
// Already optimized in db.ts
import { neonConfig } from "@neondatabase/serverless";

// HTTP mode for serverless - best performance
neonConfig.poolQueryViaFetch = true;
```

---

## Part 6: Monitoring & Measurement

### 6.1 Lighthouse CI

```bash
# Install Lighthouse CI
pnpm add -D @lhci/cli

# Create config
cat > lighthouserc.js << 'EOF'
module.exports = {
  ci: {
    collect: {
      url: ['http://localhost:3000/', 'http://localhost:3000/characters'],
      startServerCommand: 'pnpm start',
      numberOfRuns: 3,
    },
    assert: {
      assertions: {
        'categories:performance': ['error', { minScore: 0.9 }],
        'categories:accessibility': ['error', { minScore: 0.9 }],
        'categories:best-practices': ['error', { minScore: 0.9 }],
        'categories:seo': ['error', { minScore: 0.9 }],
        'first-contentful-paint': ['error', { maxNumericValue: 1800 }],
        'largest-contentful-paint': ['error', { maxNumericValue: 2500 }],
        'cumulative-layout-shift': ['error', { maxNumericValue: 0.1 }],
      },
    },
    upload: {
      target: 'temporary-public-storage',
    },
  },
};
EOF

# Run Lighthouse CI
pnpm lhci autorun
```

### 6.2 Web Vitals Monitoring

```tsx
// app/_components/WebVitals.tsx
"use client";

import { useReportWebVitals } from "next/web-vitals";

export function WebVitals() {
  useReportWebVitals((metric) => {
    // Log to console in development
    if (process.env.NODE_ENV === "development") {
      console.log(metric);
    }

    // Send to analytics in production
    if (process.env.NODE_ENV === "production") {
      // Example: Send to your analytics endpoint
      fetch("/api/vitals", {
        method: "POST",
        body: JSON.stringify(metric),
        headers: { "Content-Type": "application/json" },
      });
    }
  });

  return null;
}

// Add to app/layout.tsx
import { WebVitals } from "./_components/WebVitals";

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <WebVitals />
        {children}
      </body>
    </html>
  );
}
```

### 6.3 Chrome DevTools Performance

Using the webapp-testing skill:

```typescript
// Start performance trace
mcp_chrome_devtoo_performance_start_trace({
  reload: true,
  autoStop: true,
});

// Analyze specific insight
mcp_chrome_devtoo_performance_analyze_insight({
  insightSetId: "trace_id",
  insightName: "LCPBreakdown",
});
```

---

## Part 7: Production Checklist

### Pre-Deployment Optimization

- [ ] **Images**
  - [ ] All images use `next/image`
  - [ ] Hero/LCP images have `priority`
  - [ ] Images have correct `sizes` prop
  - [ ] Images are in modern formats (WebP/AVIF)

- [ ] **JavaScript**
  - [ ] Bundle analyzed for large dependencies
  - [ ] Heavy components dynamically imported
  - [ ] Tree shaking verified
  - [ ] No unnecessary client components

- [ ] **Caching**
  - [ ] Static pages are pre-rendered
  - [ ] Dynamic data has appropriate revalidation
  - [ ] API routes have cache headers
  - [ ] Database queries are optimized

- [ ] **Loading**
  - [ ] Suspense boundaries for streaming
  - [ ] Skeleton loaders match content dimensions
  - [ ] Fonts use `display: swap`
  - [ ] Critical CSS is inlined

- [ ] **Metrics**
  - [ ] Lighthouse score > 90 on all categories
  - [ ] LCP < 2.5s
  - [ ] INP < 200ms
  - [ ] CLS < 0.1

### Common Performance Fixes

| Issue | Solution |
|-------|----------|
| High LCP | Add `priority` to LCP image, preload critical resources |
| High CLS | Set explicit dimensions, use skeletons |
| High INP | Reduce JS bundle, use `useDeferredValue` |
| Slow TTFB | Add caching, use edge runtime |
| Large bundle | Dynamic imports, tree shaking |
| Slow images | Use next/image, optimize formats |
| Font flash | Use `display: swap`, preload fonts |

---

## Related Skills

- [webapp-testing](../webapp-testing/SKILL.md) - Performance measurement
- [neon-database-management](../neon-database-management/SKILL.md) - Query optimization
- [component-development](../component-development/SKILL.md) - Efficient components

---

## References

- [Next.js Performance](https://nextjs.org/docs/app/building-your-application/optimizing)
- [Web Vitals](https://web.dev/vitals/)
- [Lighthouse](https://developers.google.com/web/tools/lighthouse)
- [Core Web Vitals](https://web.dev/articles/vitals)

---

**Last Updated:** January 14, 2026  
**Maintained By:** Development Team  
**Status:** ✅ Production Ready
