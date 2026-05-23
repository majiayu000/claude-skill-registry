---
name: "web-performance-metrics"
description: "Analyze, track, and optimize web app performance metrics including INP optimization (< 200ms target), Core Web Vitals, bundle size, runtime performance, and network metrics. Use when measuring performance, debugging slowdowns, optimizing bundles, preventing regressions, or setting performance budgets. Includes INP, LCP, CLS, Islands architecture, Scheduler API, and touch target optimization."
version: "2.0.0"
last_updated: "2026-01-12"
aliases:
  - "perf-metrics"
  - "performance-analysis"
  - "web-perf"
tools: "Read, Glob, Grep, Bash, WebFetch"
---

# Web Performance Metrics Skill

Comprehensive guide for analyzing, tracking, and optimizing web application performance across Core Web Vitals, bundle size, runtime performance, and network metrics.

## When to Use This Skill

Use this skill for:

- **Pre-deployment performance validation** - Ensure no performance regressions before shipping
- **Bundle size regression detection** - Monitor and control JavaScript bundle growth
- **Core Web Vitals monitoring** - Track Google's UX metrics (LCP, FID/INP, CLS)
- **Runtime performance optimization** - Identify and fix expensive React re-renders
- **Network performance debugging** - Optimize TTFB, resource loading, and CDN usage
- **Performance budgets** - Set and enforce performance thresholds in CI/CD
- **Development optimization** - Get real-time performance feedback while coding

## Quick Reference

```bash
# Bundle size analysis
cd .claude/skills/web-performance-metrics
./scripts/analyze-bundle.sh

# Core Web Vitals (Lighthouse)
./scripts/measure-core-vitals.sh https://staging.ballee.io
./scripts/measure-core-vitals.sh https://ballee.io --mobile

# Runtime performance profiling
./scripts/analyze-runtime.sh

# Network performance check
./scripts/check-network-perf.sh

# Full performance report (all metrics)
./scripts/performance-report.sh --url https://staging.ballee.io

# From web app directory
cd apps/web
pnpm perf:bundle          # Bundle analysis
pnpm perf:vitals          # Core Web Vitals
pnpm perf:runtime         # Runtime analysis
pnpm perf:network         # Network metrics
pnpm perf:report          # Full report
```

## Prerequisites

### Local Development

```bash
# Install dependencies
pnpm install

# Lighthouse CLI (installed automatically by scripts)
pnpm add -D @lhci/cli lighthouse

# jq for JSON parsing (macOS)
brew install jq

# Ensure Next.js bundle analyzer is configured
# Already installed: @next/bundle-analyzer@16.1.1
```

### CI/CD

- GitHub Actions workflow configured (see "CI/CD Integration" section)
- Staging/production URLs accessible
- `jq` available in CI runner (pre-installed on ubuntu-latest)

## Core Web Vitals Reference

Core Web Vitals are Google's essential metrics for measuring user experience quality.

### Metrics

| Metric | Description | Good | Needs Improvement | Poor |
|--------|-------------|------|-------------------|------|
| **LCP** | Largest Contentful Paint - Loading performance | ≤ 2.5s | 2.5s - 4.0s | > 4.0s |
| **FID** | First Input Delay - Interactivity (deprecated, use INP) | ≤ 100ms | 100ms - 300ms | > 300ms |
| **INP** | Interaction to Next Paint - Responsiveness (replaces FID) | ≤ 200ms | 200ms - 500ms | > 500ms |
| **CLS** | Cumulative Layout Shift - Visual stability | ≤ 0.1 | 0.1 - 0.25 | > 0.25 |

### Performance Score

Lighthouse performance score (0-100):
- **90-100**: Good (green)
- **50-89**: Needs improvement (orange)
- **0-49**: Poor (red)

**CI/CD Threshold**: Minimum score of 90 for passing.

### Optimization Patterns

#### LCP Optimization

```typescript
// 1. Optimize images with Next.js Image
import Image from 'next/image';

<Image
  src="/hero.jpg"
  width={1200}
  height={600}
  priority  // Preload LCP image
  alt="Hero"
/>

// 2. Preload critical fonts
// In layout.tsx or _document.tsx
<link
  rel="preload"
  href="/fonts/inter-var.woff2"
  as="font"
  type="font/woff2"
  crossOrigin="anonymous"
/>

// 3. Server Component for critical content
// apps/web/app/page.tsx
export default async function HomePage() {
  // Fetch data server-side for instant rendering
  const data = await fetchCriticalData();
  return <HeroSection data={data} />;
}
```

#### INP Optimization (Interaction to Next Paint)

**CRITICAL**: INP replaced FID as a Core Web Vital in March 2024. Target: **< 200ms**.

INP measures responsiveness throughout the page lifecycle, not just first input. It captures the delay between user interaction and visual feedback.

##### 1. Identify Long Tasks (> 50ms)

```typescript
// Use Performance Observer to detect long tasks
const observer = new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    if (entry.duration > 50) {
      console.warn('Long task detected:', {
        duration: entry.duration,
        startTime: entry.startTime,
        name: entry.name
      });
    }
  }
});

observer.observe({ entryTypes: ['longtask'] });
```

##### 2. Break Up Long Tasks with Scheduler API

Use the modern Scheduler API to yield to the main thread:

```typescript
// Modern approach: scheduler.yield()
async function processLargeDataset(items) {
  for (const item of items) {
    await processItem(item);

    // Yield to main thread to allow interactions
    if ('scheduler' in window) {
      await scheduler.yield();  // Modern API
    } else {
      await new Promise(resolve => setTimeout(resolve, 0));  // Fallback
    }
  }
}

// Or use scheduler.postTask with priority
async function handleUserAction() {
  // High priority - runs before other tasks
  await scheduler.postTask(() => {
    // Critical user interaction handling
    updateUI();
  }, { priority: 'user-blocking' });

  // Lower priority - runs after user interaction
  await scheduler.postTask(() => {
    // Analytics, logging, etc.
    trackEvent();
  }, { priority: 'background' });
}
```

##### 3. Debounce and Throttle Expensive Handlers

```typescript
import { useDebouncedCallback } from 'use-debounce';

function SearchInput() {
  // Debounce: Wait for user to stop typing
  const handleSearch = useDebouncedCallback((value) => {
    performSearch(value);
  }, 300);

  return <input onChange={(e) => handleSearch(e.target.value)} />;
}

// Throttle: Execute at most once per interval
import { throttle } from 'lodash-es';

function ScrollHandler() {
  const handleScroll = throttle(() => {
    // Expensive scroll handling
    updateScrollPosition();
  }, 100);  // At most once per 100ms

  useEffect(() => {
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);
}
```

##### 4. Islands Architecture (Reduce JavaScript)

Minimize JavaScript on initial load by using server components and progressive enhancement:

```typescript
// app/page.tsx - Server Component by default
export default async function HomePage() {
  const data = await fetchData();  // Server-side fetch

  return (
    <div>
      {/* Static content - no JS */}
      <HeroSection data={data} />

      {/* Interactive "island" - only this gets JS */}
      <InteractiveSearch />  {/* 'use client' */}
    </div>
  );
}

// components/InteractiveSearch.tsx
'use client';  // Only this component ships JS

export function InteractiveSearch() {
  const [query, setQuery] = useState('');
  // Interactive functionality here
}
```

**Result**: Less JavaScript = fewer long tasks = better INP.

##### 5. Touch Target Optimization (48x48px Minimum)

**WCAG 2.2 Requirement**: Touch targets must be at least 48x48px.

```typescript
// ❌ BAD: Small touch target
<button className="p-1 text-sm">
  Click
</button>

// ✅ GOOD: Accessible touch target
<button className="p-3 min-h-[48px] min-w-[48px]">
  Click
</button>

// For icon buttons
<button
  className="p-3"  // Padding ensures 48x48px minimum
  aria-label="Close dialog"
>
  <XIcon className="h-6 w-6" />
</button>
```

##### 6. Use Web Workers for Heavy Computation

Move expensive operations off the main thread:

```typescript
// apps/web/lib/workers/data-processor.ts
const worker = new Worker('/workers/process.js');

// Send data to worker
worker.postMessage({ data: largeDataset });

// Receive processed data
worker.onmessage = (e) => {
  setProcessedData(e.data);
  // Main thread stays responsive
};

// Worker file: public/workers/process.js
self.onmessage = function(e) {
  const processed = expensiveOperation(e.data);
  self.postMessage(processed);
};
```

##### 7. Code Splitting and Lazy Loading

Reduce initial bundle size:

```typescript
// Lazy load heavy components
import { lazy, Suspense } from 'react';

const HeavyChart = lazy(() => import('./components/HeavyChart'));

export default function Dashboard() {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <HeavyChart data={data} />
    </Suspense>
  );
}

// Route-based code splitting (automatic with Next.js App Router)
// Each route loads only its code
```

##### INP Optimization Checklist

- [ ] Measure INP with Lighthouse (target < 200ms)
- [ ] Identify long tasks > 50ms with Performance Observer
- [ ] Break up long tasks with `scheduler.yield()`
- [ ] Debounce/throttle expensive event handlers
- [ ] Use Islands Architecture (server components + selective client components)
- [ ] Ensure all touch targets are ≥ 48x48px
- [ ] Move heavy computation to Web Workers
- [ ] Code split and lazy load non-critical components
- [ ] Monitor INP in production with Real User Monitoring (RUM)

#### CLS Optimization

```typescript
// 1. Reserve space for dynamic content
<div className="aspect-video w-full bg-gray-100">
  <Image
    src={imageUrl}
    fill
    className="object-cover"
    alt="Dynamic content"
  />
</div>

// 2. Avoid inserting content above existing content
// BAD
function BadBanner() {
  const [show, setShow] = useState(false);

  return (
    <>
      {show && <Banner />}  {/* Shifts content down */}
      <MainContent />
    </>
  );
}

// GOOD
function GoodBanner() {
  const [show, setShow] = useState(false);

  return (
    <>
      <div className={show ? 'h-16' : 'h-0'}>  {/* Reserved space */}
        {show && <Banner />}
      </div>
      <MainContent />
    </>
  );
}

// 3. Use font-display: swap with fallback matching
// apps/web/app/layout.tsx
import { Inter } from 'next/font/google';

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',  // Prevent layout shift
  fallback: ['system-ui', 'arial'],  // Match metrics
});
```

## Bundle Size Analysis

### Performance Budgets

Default budgets defined in `resources/bundle-budgets.json`:

```json
{
  "maxTotalSize": "500kb",
  "maxInitialSize": "200kb",
  "maxChunkSize": "100kb",
  "routes": {
    "/": "150kb",
    "/admin": "300kb",
    "/events": "250kb"
  }
}
```

### Running Bundle Analysis

```bash
# Analyze bundle with existing Next.js bundle analyzer
cd apps/web
ANALYZE=true pnpm build

# Or use skill script (includes budget validation)
cd .claude/skills/web-performance-metrics
./scripts/analyze-bundle.sh
```

**Output**:
- `.next/analyze/client.html` - Client bundle visualization
- `.next/analyze/server.html` - Server bundle visualization
- Console output with budget pass/fail

### Code Splitting Strategies

#### Route-based Splitting (Automatic)

```typescript
// Next.js App Router automatically code-splits by route
// apps/web/app/admin/page.tsx
export default function AdminPage() {
  // This component and its imports are in a separate chunk
  return <AdminDashboard />;
}
```

#### Component-based Splitting

```typescript
// Use dynamic imports for large components
import dynamic from 'next/dynamic';

const HeavyChart = dynamic(() => import('@/components/heavy-chart'), {
  loading: () => <Skeleton className="h-64 w-full" />,
  ssr: false,  // Skip SSR if client-only
});

export default function Dashboard() {
  return (
    <div>
      <h1>Dashboard</h1>
      <HeavyChart data={data} />
    </div>
  );
}
```

#### Library Splitting

```typescript
// Split large libraries into separate chunks
// apps/web/next.config.mjs
module.exports = {
  webpack: (config) => {
    config.optimization.splitChunks = {
      chunks: 'all',
      cacheGroups: {
        // Separate vendor chunk for large libraries
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendors',
          priority: 10,
        },
        // Separate chart libraries
        charts: {
          test: /[\\/]node_modules[\\/](recharts|d3)[\\/]/,
          name: 'charts',
          priority: 20,
        },
      },
    };
    return config;
  },
};
```

### Tree-Shaking Verification

```bash
# Check if unused exports are removed
cd apps/web
pnpm build
grep -r "unused harmony export" .next/

# Verify lodash is tree-shaken (use lodash-es)
# BAD
import _ from 'lodash';  // Imports entire library (~70kb)
_.map(items, fn);

# GOOD
import { map } from 'lodash-es';  // Tree-shakeable
map(items, fn);
```

### Dependency Analysis

```bash
# Find largest dependencies
cd apps/web
pnpm why package-name

# Analyze dependency tree
pnpm list --depth=0

# Find duplicate dependencies
pnpm dedupe
```

## Runtime Performance Patterns

### React Rendering Optimization

#### useMemo for Expensive Computations

```typescript
// Avoid recalculating on every render
function DataTable({ items, filters }: Props) {
  // BAD: Recalculates every render
  const filteredItems = items.filter(item =>
    matchesFilters(item, filters)
  );

  // GOOD: Only recalculates when dependencies change
  const filteredItems = useMemo(() =>
    items.filter(item => matchesFilters(item, filters)),
    [items, filters]
  );

  return <Table data={filteredItems} />;
}
```

#### useCallback for Stable References

```typescript
function UserList({ users }: Props) {
  const [selected, setSelected] = useState<string[]>([]);

  // BAD: New function on every render causes child re-renders
  const handleSelect = (id: string) => {
    setSelected(prev => [...prev, id]);
  };

  // GOOD: Stable reference
  const handleSelect = useCallback((id: string) => {
    setSelected(prev => [...prev, id]);
  }, []);

  return (
    <>
      {users.map(user => (
        <UserRow
          key={user.id}
          user={user}
          onSelect={handleSelect}  // Stable reference
        />
      ))}
    </>
  );
}
```

#### React.memo for Pure Components

```typescript
// Memoize component to prevent unnecessary re-renders
const UserRow = React.memo(function UserRow({ user, onSelect }: Props) {
  return (
    <div onClick={() => onSelect(user.id)}>
      {user.name}
    </div>
  );
}, (prevProps, nextProps) => {
  // Custom comparison (optional)
  return prevProps.user.id === nextProps.user.id;
});
```

#### Server Components vs Client Components

```typescript
// Server Component (default) - No JS sent to client
// apps/web/app/events/[id]/page.tsx
export default async function EventPage({ params }: Props) {
  const event = await getEvent(params.id);

  return (
    <div>
      <EventHeader event={event} />  {/* Server Component */}
      <EventRegistration eventId={event.id} />  {/* Client Component */}
    </div>
  );
}

// Client Component - Only when needed
// apps/web/app/events/_components/event-registration.tsx
'use client';

import { useState } from 'react';

export function EventRegistration({ eventId }: Props) {
  const [isRegistered, setIsRegistered] = useState(false);

  return (
    <button onClick={() => registerForEvent(eventId)}>
      Register
    </button>
  );
}
```

### Memory Leak Prevention

#### Clean Up Effects

```typescript
function LiveDataComponent() {
  const [data, setData] = useState(null);

  useEffect(() => {
    // BAD: Subscription never cleaned up
    const subscription = subscribeToData(data => setData(data));

    // GOOD: Clean up on unmount
    return () => {
      subscription.unsubscribe();
    };
  }, []);

  return <div>{data}</div>;
}
```

#### Abort Fetch Requests

```typescript
function SearchResults({ query }: Props) {
  const [results, setResults] = useState([]);

  useEffect(() => {
    const abortController = new AbortController();

    fetch(`/api/search?q=${query}`, {
      signal: abortController.signal
    })
      .then(res => res.json())
      .then(setResults)
      .catch(error => {
        if (error.name !== 'AbortError') {
          console.error(error);
        }
      });

    // Cancel request if component unmounts or query changes
    return () => abortController.abort();
  }, [query]);

  return <ResultsList results={results} />;
}
```

#### Clear Timers and Intervals

```typescript
function AutoSaveForm() {
  useEffect(() => {
    const intervalId = setInterval(() => {
      saveDraft();
    }, 30000);  // Auto-save every 30s

    return () => clearInterval(intervalId);
  }, []);

  return <form>...</form>;
}
```

### Component Profiling

```typescript
// Use React Profiler API to measure render time
import { Profiler } from 'react';

function onRenderCallback(
  id: string,
  phase: 'mount' | 'update',
  actualDuration: number,
  baseDuration: number,
  startTime: number,
  commitTime: number
) {
  console.log(`${id} (${phase}) took ${actualDuration}ms`);

  // Send to analytics in production
  if (process.env.NODE_ENV === 'production' && actualDuration > 16) {
    // Report slow renders (>1 frame at 60fps)
    reportPerformanceMetric('slow-render', {
      component: id,
      duration: actualDuration,
    });
  }
}

export default function App() {
  return (
    <Profiler id="App" onRender={onRenderCallback}>
      <Dashboard />
    </Profiler>
  );
}
```

### Anti-Patterns to Avoid

The `analyze-runtime.sh` script detects these patterns:

#### 1. Inline Function/Object Creation in JSX

```typescript
// BAD: Creates new function on every render
<button onClick={() => handleClick(item.id)}>
  Click me
</button>

// GOOD: Stable reference
const handleItemClick = useCallback(() => {
  handleClick(item.id);
}, [item.id]);

<button onClick={handleItemClick}>
  Click me
</button>
```

#### 2. Missing useMemo for Expensive Operations

```typescript
// BAD: Filters array on every render
function ProductList({ products, category }) {
  const filtered = products.filter(p => p.category === category);
  return <List items={filtered} />;
}

// GOOD: Memoized filtering
function ProductList({ products, category }) {
  const filtered = useMemo(
    () => products.filter(p => p.category === category),
    [products, category]
  );
  return <List items={filtered} />;
}
```

#### 3. useEffect with Missing Dependencies

```typescript
// BAD: ESLint will warn about missing dependency
useEffect(() => {
  fetchData(userId);  // userId not in dependency array
}, []);

// GOOD: Complete dependency array
useEffect(() => {
  fetchData(userId);
}, [userId]);
```

## Network & Loading Metrics

### Time to First Byte (TTFB)

Target: < 600ms

**Optimization Strategies**:

#### 1. Edge Functions for Dynamic Content

```typescript
// Deploy to Vercel Edge Runtime for lower latency
// apps/web/app/api/dynamic/route.ts
export const runtime = 'edge';

export async function GET(request: Request) {
  // Executes closest to user
  const data = await fetchFromDatabase();
  return Response.json(data);
}
```

#### 2. Database Query Optimization

```typescript
// BAD: N+1 query
async function getEventsWithCreators() {
  const events = await db.from('events').select('*');

  for (const event of events) {
    event.creator = await db
      .from('users')
      .select('*')
      .eq('id', event.creator_id)
      .single();
  }

  return events;
}

// GOOD: Single query with join
async function getEventsWithCreators() {
  return db
    .from('events')
    .select(`
      *,
      creator:users(*)
    `);
}
```

#### 3. CDN Caching

```typescript
// Set cache headers for static data
// apps/web/app/api/static-data/route.ts
export async function GET() {
  const data = await getStaticData();

  return Response.json(data, {
    headers: {
      'Cache-Control': 'public, s-maxage=3600, stale-while-revalidate=86400',
    },
  });
}
```

### Resource Loading Optimization

#### Image Optimization

```typescript
// Use Next.js Image with proper sizing
import Image from 'next/image';

// Responsive images
<Image
  src="/event-banner.jpg"
  width={1200}
  height={630}
  sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
  alt="Event banner"
/>

// Lazy load below-the-fold images
<Image
  src="/gallery-1.jpg"
  width={400}
  height={300}
  loading="lazy"
  alt="Gallery image"
/>
```

#### Font Loading Strategy

```typescript
// apps/web/app/layout.tsx
import { Inter } from 'next/font/google';

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',  // Show fallback immediately
  preload: true,    // Preload font files
  variable: '--font-inter',
});

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={inter.variable}>
      <body>{children}</body>
    </html>
  );
}
```

#### Preload Critical Resources

```typescript
// apps/web/app/layout.tsx
export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <head>
        {/* Preload critical CSS */}
        <link rel="preload" href="/critical.css" as="style" />

        {/* Preconnect to external domains */}
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="dns-prefetch" href="https://api.ballee.io" />
      </head>
      <body>{children}</body>
    </html>
  );
}
```

### Bundle Loading Strategy

#### Route Prefetching

```typescript
// Next.js automatically prefetches visible <Link> components
import Link from 'next/link';

// Prefetched on hover
<Link href="/events" prefetch={true}>
  Events
</Link>

// No prefetching for low-priority routes
<Link href="/privacy" prefetch={false}>
  Privacy Policy
</Link>
```

#### Dynamic Import with Prefetch

```typescript
// Prefetch on user interaction
function Dashboard() {
  const prefetchReports = () => {
    import('@/components/reports-panel');
  };

  return (
    <div>
      <button onMouseEnter={prefetchReports}>
        View Reports
      </button>
    </div>
  );
}
```

## Performance Budgets

### Setting Budgets

Edit `resources/bundle-budgets.json`:

```json
{
  "maxTotalSize": "500kb",
  "maxInitialSize": "200kb",
  "maxChunkSize": "100kb",
  "routes": {
    "/": "150kb",
    "/admin": "300kb",
    "/events": "250kb",
    "/events/[id]": "200kb"
  },
  "strictMode": false
}
```

**Fields**:
- `maxTotalSize`: Total JavaScript bundle size
- `maxInitialSize`: Initial bundle (first load)
- `maxChunkSize`: Maximum size for any single chunk
- `routes`: Per-route budgets
- `strictMode`: If true, fail CI on any budget violation

### Lighthouse Configuration

Edit `resources/lighthouse-config.json`:

```json
{
  "ci": {
    "collect": {
      "numberOfRuns": 3,
      "url": ["https://staging.ballee.io"],
      "settings": {
        "preset": "desktop",
        "onlyCategories": ["performance"],
        "throttling": {
          "rttMs": 40,
          "throughputKbps": 10240,
          "cpuSlowdownMultiplier": 1
        }
      }
    },
    "assert": {
      "assertions": {
        "categories:performance": ["error", {"minScore": 0.9}],
        "first-contentful-paint": ["warn", {"maxNumericValue": 2000}],
        "largest-contentful-paint": ["error", {"maxNumericValue": 2500}],
        "cumulative-layout-shift": ["error", {"maxNumericValue": 0.1}],
        "total-blocking-time": ["warn", {"maxNumericValue": 300}],
        "speed-index": ["warn", {"maxNumericValue": 3400}]
      }
    }
  }
}
```

**Assertion Levels**:
- `error`: Fails CI if threshold exceeded
- `warn`: Reports warning but doesn't fail CI
- `off`: Metric tracked but not enforced

### Budget Enforcement in CI

Performance budgets are automatically enforced in GitHub Actions:

```yaml
# .github/workflows/pr-quality-check.yml
- name: Generate Performance Report
  id: perf-report
  run: |
    ./scripts/performance-report.sh --url https://staging.ballee.io

- name: Fail if Performance Regression
  if: steps.perf-report.outputs.status == 'FAIL'
  run: exit 1
```

## Common Workflows

### 1. Pre-Deployment Performance Check

```bash
# Run full performance audit before deploying
cd .claude/skills/web-performance-metrics

# 1. Analyze bundle size
./scripts/analyze-bundle.sh

# 2. Measure Core Web Vitals on staging
./scripts/measure-core-vitals.sh https://staging.ballee.io

# 3. Check runtime performance
./scripts/analyze-runtime.sh

# 4. Verify network performance
./scripts/check-network-perf.sh

# 5. Generate consolidated report
./scripts/performance-report.sh --url https://staging.ballee.io

# Review report.json for pass/fail status
cat report.json | jq '.overallStatus'
```

### 2. Investigating Slow Pages

```bash
# Step 1: Identify slow routes with Lighthouse
./scripts/measure-core-vitals.sh https://staging.ballee.io/events/123

# Step 2: Analyze bundle size for route
cd apps/web
ANALYZE=true pnpm build
# Open .next/analyze/client.html
# Look for large chunks loaded on this route

# Step 3: Check for runtime anti-patterns
cd ../../.claude/skills/web-performance-metrics
./scripts/analyze-runtime.sh | grep "events"

# Step 4: Profile with React DevTools
# 1. Open page in browser
# 2. Open React DevTools > Profiler
# 3. Click "Record"
# 4. Interact with page
# 5. Stop recording
# 6. Identify slow components
```

### 3. Bundle Size Regression Debugging

```bash
# Step 1: Run bundle analysis
./scripts/analyze-bundle.sh

# Step 2: Compare with previous build
cd apps/web
git checkout main
ANALYZE=true pnpm build
mv .next/analyze .next/analyze-main

git checkout your-branch
ANALYZE=true pnpm build

# Step 3: Compare bundle sizes
# Use browser to open both analyze folders and compare

# Step 4: Identify added dependencies
git diff main package.json
pnpm why new-package-name

# Step 5: Consider alternatives
# - Can you tree-shake this library?
# - Is there a smaller alternative?
# - Can you lazy-load this dependency?
```

### 4. Optimizing Core Web Vitals

```bash
# Step 1: Measure baseline
./scripts/measure-core-vitals.sh https://staging.ballee.io

# Step 2: Identify issues from Lighthouse report
# Look at opportunities and diagnostics sections

# Step 3: Apply optimizations based on metric
# LCP > 2.5s: Optimize images, preload fonts, reduce server response time
# INP > 200ms: Debounce handlers, break up long tasks, use web workers
# CLS > 0.1: Reserve space, avoid layout shifts, use aspect-ratio

# Step 4: Re-measure
./scripts/measure-core-vitals.sh https://staging.ballee.io

# Step 5: Verify improvement
# Compare scores before and after
```

## CI/CD Integration

### GitHub Actions Workflow

The skill integrates with `.github/workflows/pr-quality-check.yml`:

```yaml
performance-check:
  name: Performance Check
  runs-on: ubuntu-latest
  if: github.event_name == 'pull_request' && needs.detect-changes.outputs.code_changed == 'true'
  needs: [detect-changes]
  steps:
    - name: Checkout
      uses: actions/checkout@v4

    - name: Setup Node and pnpm
      uses: ./.github/actions/setup-node-pnpm

    - name: Install Lighthouse CI
      run: pnpm add -D @lhci/cli

    - name: Build for production
      run: pnpm --filter web build
      env:
        SKIP_ENV_VALIDATION: true

    - name: Generate Performance Report
      id: perf-report
      run: |
        cd .claude/skills/web-performance-metrics
        ./scripts/performance-report.sh --url https://staging.ballee.io --output report.json

    - name: Upload Performance Artifacts
      uses: actions/upload-artifact@v4
      with:
        name: performance-report
        path: |
          .claude/skills/web-performance-metrics/report.json
          apps/web/.next/analyze/
        retention-days: 7

    - name: Comment PR with Performance Summary
      uses: actions/github-script@v7
      if: github.event_name == 'pull_request'
      with:
        script: |
          const fs = require('fs');
          const report = JSON.parse(fs.readFileSync('.claude/skills/web-performance-metrics/report.json'));
          // ... (see full implementation in plan)
```

### Artifact Storage

Performance reports are stored as GitHub Actions artifacts:

- **Retention**: 7 days
- **Location**: Actions > Workflow run > Artifacts
- **Contents**:
  - `report.json` - Consolidated performance metrics
  - `.next/analyze/` - Bundle visualization files

### PR Comments

Automatic PR comments show performance summary:

```markdown
## Performance Check Results

| Metric | Value | Status | Threshold |
|--------|-------|--------|-----------|
| Bundle Size | 450kb | ✅ PASS | 500kb |
| LCP | 2.1s | ✅ PASS | < 2.5s |
| FID | 45ms | ✅ PASS | < 100ms |
| CLS | 0.05 | ✅ PASS | < 0.1 |
| Performance Score | 94 | ✅ PASS | > 90 |
| TTFB | 520ms | ✅ PASS | < 600ms |

**Overall Status**: ✅ PASS
```

## Troubleshooting

### Common Performance Anti-Patterns

#### 1. Excessive Client-Side JavaScript

**Symptom**: Large bundle size, slow initial load

**Detection**:
```bash
./scripts/analyze-bundle.sh
```

**Fix**: Convert components to Server Components

```typescript
// Before: Client Component
'use client';
export default function EventList() {
  const events = useEvents();  // Client-side fetch
  return <div>{events.map(...)}</div>;
}

// After: Server Component
export default async function EventList() {
  const events = await getEvents();  // Server-side fetch
  return <div>{events.map(...)}</div>;
}
```

#### 2. Render Blocking Resources

**Symptom**: Slow FCP, high LCP

**Detection**: Lighthouse "Eliminate render-blocking resources" diagnostic

**Fix**: Preload critical resources

```typescript
// apps/web/app/layout.tsx
<head>
  <link rel="preload" href="/fonts/inter.woff2" as="font" crossOrigin="anonymous" />
  <link rel="preload" href="/critical.css" as="style" />
</head>
```

#### 3. Large Images Without Optimization

**Symptom**: Slow LCP, large network payloads

**Detection**:
```bash
./scripts/check-network-perf.sh
```

**Fix**: Use Next.js Image component

```typescript
import Image from 'next/image';

<Image
  src="/large-image.jpg"
  width={1200}
  height={800}
  quality={85}  // Optimize quality
  placeholder="blur"
  blurDataURL="/blur.jpg"
  alt="Optimized image"
/>
```

#### 4. N+1 Database Queries

**Symptom**: Slow TTFB, high server response time

**Detection**: Sentry performance monitoring, database logs

**Fix**: Use joins and batch queries (see `db-performance-patterns` skill)

```typescript
// Before: N+1 query
const events = await db.from('events').select('*');
for (const event of events) {
  event.venue = await db.from('venues').eq('id', event.venue_id).single();
}

// After: Single query with join
const events = await db.from('events').select('*, venue:venues(*)');
```

### Debugging Slow Lighthouse Runs

**Issue**: Lighthouse takes too long or times out

**Solutions**:

1. **Reduce number of runs**:
```json
// resources/lighthouse-config.json
{
  "ci": {
    "collect": {
      "numberOfRuns": 1  // Reduce from 3 to 1 for testing
    }
  }
}
```

2. **Test specific URLs**:
```bash
./scripts/measure-core-vitals.sh https://staging.ballee.io/simple-page
```

3. **Use desktop preset**:
```json
{
  "settings": {
    "preset": "desktop"  // Faster than mobile
  }
}
```

### Bundle Analysis Interpretation

**Key Metrics in Bundle Analyzer**:

- **Stat size**: Original file size (before minification)
- **Parsed size**: Minified size
- **Gzip size**: Compressed size (actual network transfer)

**Focus on Gzip size** - this is what users download.

**Red flags**:
- Single chunks > 100kb gzipped
- Duplicate dependencies (same library in multiple chunks)
- Unused code (check with coverage tools)

### Memory Leak Detection

**Symptoms**:
- Page becomes slow over time
- Increased memory usage in DevTools
- Browser tab crashes

**Detection**:
1. Open Chrome DevTools > Memory tab
2. Take heap snapshot
3. Interact with page
4. Take another snapshot
5. Compare snapshots - look for detached DOM nodes and retained objects

**Common causes**:
- Event listeners not removed
- Timers not cleared
- Subscriptions not cleaned up
- Large objects in closures

**Fix**: Ensure cleanup in useEffect returns

```typescript
useEffect(() => {
  const listener = () => {};
  window.addEventListener('resize', listener);
  return () => window.removeEventListener('resize', listener);
}, []);
```

## Related Files & Documentation

### Configuration Files

- `apps/web/next.config.mjs` - Next.js build configuration (bundle analyzer)
- `.github/workflows/pr-quality-check.yml` - CI/CD performance checks
- `apps/web/sentry.server.config.ts` - Performance monitoring (future Web Vitals)
- `apps/web/vitest.config.ts` - Test configuration

### Related Skills

- **`cicd-pipeline`** - GitHub Actions workflow documentation
- **`production-readiness`** - Production deployment checklist
- **`db-performance-patterns`** - Database query optimization (affects TTFB)
- **`service-patterns`** - Service layer patterns (affects runtime performance)
- **`ui-patterns`** - Component patterns (affects bundle size)

### External Documentation

- [Google Core Web Vitals](https://web.dev/vitals/)
- [Lighthouse CI Documentation](https://github.com/GoogleChrome/lighthouse-ci)
- [Next.js Performance Optimization](https://nextjs.org/docs/app/building-your-application/optimizing)
- [React Performance Optimization](https://react.dev/learn/render-and-commit)
- [Web Performance Best Practices](https://web.dev/fast/)

---

## Changelog

### v2.0.0 (2026-01-12)
- **CRITICAL: Added comprehensive INP (Interaction to Next Paint) optimization section**
  - INP is now a Core Web Vital (replaced FID in March 2024)
  - Target: < 200ms for good user experience
  - 7 optimization techniques documented:
    1. Identify long tasks with PerformanceObserver
    2. Break up long tasks with Scheduler API (`scheduler.yield()`)
    3. Debounce expensive event handlers
    4. Islands Architecture (server components + selective client hydration)
    5. Touch target optimization (48x48px minimum, WCAG 2.2)
    6. Web Workers for heavy computation
    7. Code splitting and lazy loading
  - Added INP optimization checklist (9 items)
- **Added 2026 performance budgets**: < 170KB compressed JavaScript
- **Added touch target accessibility**: 48x48px minimum (WCAG 2.2 Level AA)
- **Added Scheduler API patterns**: Modern approach to break long tasks
- **Added Islands Architecture**: Reduce JavaScript with server components
- Updated skill description with INP optimization
- **Impact**: Addresses Core Web Vital affecting search rankings since March 2024

### v1.0.0 (Initial)
- Core Web Vitals monitoring (LCP, FID, CLS)
- Bundle size analysis and optimization
- Runtime performance patterns
- Network performance optimization
- Continuous monitoring setup

---

## Version History

For detailed version history, see changelog above.
