---
name: frontend-bundle-analysis-and-optimization
version: "1.0"
description: >
  Bundle analysis and optimization strategies for Next.js applications using Webpack and Turbopack.
  PROACTIVELY activate for: (1) Analyzing bundle size, (2) Implementing code splitting,
  (3) Configuring tree shaking, (4) Dynamic imports, (5) Webpack/Turbopack configuration.
  Triggers: "bundle size", "webpack", "turbopack", "code splitting", "tree shaking", "lazy loading", "bundle analyzer", "dynamic import"
core-integration:
  techniques:
    primary: ["systematic_analysis"]
    secondary: ["structured_evaluation"]
  contracts:
    input: "none"
    output: "none"
  patterns: "none"
  rubrics: "none"
---

# Frontend Bundle Analysis and Optimization

This skill provides actionable strategies for analyzing and reducing JavaScript bundle size using Webpack or Turbopack, focusing on code splitting, tree shaking, and dependency analysis.

## Bundle Analysis with @next/bundle-analyzer

Visual bundle analysis is the first step in any optimization effort. It shows which modules contribute most to bundle size.

### Setup

```bash
npm install @next/bundle-analyzer --save-dev
```

```js
// next.config.js
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
})

module.exports = withBundleAnalyzer({
  // Your Next.js config
})
```

### Usage

```bash
ANALYZE=true npm run build
```

This opens an interactive treemap showing:
- Which dependencies are largest
- Duplicate packages across chunks
- Opportunities for code splitting

### Reading the Treemap

- **Large blocks**: Heavy dependencies (consider alternatives or lazy loading)
- **Duplicate colors**: Same package in multiple chunks (configure splitChunks)
- **Vendor chunks**: Third-party libraries (good candidates for caching)

## Dynamic Imports

Dynamic imports enable code splitting, loading JavaScript only when needed.

### Component-Based Code Splitting

```tsx
// BAD: Loads heavy component immediately
import HeavyChart from '@/components/HeavyChart'

export default function Dashboard() {
  return <HeavyChart data={data} />
}

// GOOD: Loads only when rendered
import dynamic from 'next/dynamic'

const HeavyChart = dynamic(() => import('@/components/HeavyChart'), {
  loading: () => <ChartSkeleton />,
  ssr: false, // Disable SSR if component uses browser APIs
})

export default function Dashboard() {
  return <HeavyChart data={data} />
}
```

### Conditional Loading

```tsx
// Load component only when needed
import dynamic from 'next/dynamic'
import { useState } from 'react'

const AdminPanel = dynamic(() => import('@/components/AdminPanel'))

export default function Dashboard({ isAdmin }: { isAdmin: boolean }) {
  const [showAdmin, setShowAdmin] = useState(false)

  return (
    <div>
      <h1>Dashboard</h1>

      {isAdmin && (
        <button onClick={() => setShowAdmin(true)}>
          Show Admin Panel
        </button>
      )}

      {/* Only loads when button is clicked */}
      {showAdmin && <AdminPanel />}
    </div>
  )
}
```

### Named Exports

```tsx
// For named exports, use an object with 'default'
const DynamicComponent = dynamic(() =>
  import('@/components/Hello').then((mod) => mod.Hello)
)
```

### Multiple Components

```tsx
// BAD: Import entire library
import { ComponentA, ComponentB } from 'heavy-library'

// GOOD: Split into separate chunks
const ComponentA = dynamic(() => import('heavy-library/ComponentA'))
const ComponentB = dynamic(() => import('heavy-library/ComponentB'))
```

### With Custom Loading State

```tsx
const HeavyEditor = dynamic(() => import('@/components/RichTextEditor'), {
  loading: () => (
    <div className="editor-skeleton">
      <div className="toolbar-skeleton" />
      <div className="content-skeleton" />
    </div>
  ),
  ssr: false,
})
```

## Route-Based Code Splitting

Next.js automatically code-splits by route, but you can optimize further.

### Lazy Route Components

```tsx
// app/dashboard/page.tsx
import dynamic from 'next/dynamic'

// Heavy components loaded only on this route
const Analytics = dynamic(() => import('@/components/Analytics'))
const UserTable = dynamic(() => import('@/components/UserTable'))

export default function DashboardPage() {
  return (
    <div>
      <Analytics />
      <UserTable />
    </div>
  )
}
```

### Shared Layouts

```tsx
// app/layout.tsx
// Common layout code shared across routes
export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <Header /> {/* Shared, in main bundle */}
        {children} {/* Route-specific, code-split */}
        <Footer /> {/* Shared, in main bundle */}
      </body>
    </html>
  )
}
```

## Webpack splitChunks Configuration

Fine-tune how code is divided into chunks for optimal caching and loading.

### Default Next.js Configuration

Next.js has sensible defaults, but you can customize:

```js
// next.config.js
module.exports = {
  webpack: (config, { isServer }) => {
    if (!isServer) {
      config.optimization.splitChunks = {
        chunks: 'all',
        cacheGroups: {
          default: false,
          vendors: false,
          // Vendor chunk for node_modules
          vendor: {
            name: 'vendor',
            chunks: 'all',
            test: /node_modules/,
            priority: 20,
          },
          // Common chunk for shared code
          common: {
            name: 'common',
            minChunks: 2,
            chunks: 'all',
            priority: 10,
            reuseExistingChunk: true,
            enforce: true,
          },
        },
      }
    }

    return config
  },
}
```

### Framework Chunk

```js
// Separate React/Next.js into their own chunk for better caching
cacheGroups: {
  framework: {
    name: 'framework',
    test: /[\\/]node_modules[\\/](react|react-dom|next)[\\/]/,
    priority: 40,
    enforce: true,
  },
}
```

### Library-Specific Chunks

```js
// Create separate chunk for a heavy library
cacheGroups: {
  charts: {
    name: 'charts',
    test: /[\\/]node_modules[\\/](recharts|d3|chart\.js)[\\/]/,
    priority: 30,
    enforce: true,
  },
}
```

### Size-Based Splitting

```js
splitChunks: {
  chunks: 'all',
  maxSize: 244 * 1024, // 244 KB max chunk size
  minSize: 20 * 1024,   // 20 KB min chunk size
}
```

## Tree Shaking and Side Effects

Tree shaking eliminates unused code, but requires proper configuration.

### Package.json sideEffects

```json
{
  "name": "my-library",
  "sideEffects": false
}
```

This tells bundlers that no files have side effects, enabling aggressive tree shaking.

### Specific Side Effects

```json
{
  "sideEffects": [
    "*.css",
    "*.scss",
    "./src/polyfills.ts"
  ]
}
```

### Import Best Practices

```ts
// BAD: Imports entire library
import _ from 'lodash'
const result = _.debounce(fn, 100)

// GOOD: Import specific function
import debounce from 'lodash/debounce'
const result = debounce(fn, 100)

// EVEN BETTER: Use tree-shakeable alternative
import { debounce } from 'lodash-es'
const result = debounce(fn, 100)
```

### Named Imports

```ts
// BAD: Entire date-fns library loaded
import * as dateFns from 'date-fns'
dateFns.format(new Date(), 'yyyy-MM-dd')

// GOOD: Only format function loaded
import { format } from 'date-fns'
format(new Date(), 'yyyy-MM-dd')
```

### Barrel File Issues

```ts
// utils/index.ts - BAD: Barrel file prevents tree shaking
export * from './stringUtils'
export * from './arrayUtils'
export * from './dateUtils'

// GOOD: Import directly from specific files
import { formatString } from '@/utils/stringUtils'
```

## Turbopack Considerations

Turbopack is Next.js's Rust-based bundler, significantly faster than Webpack.

### Enable for Development

```bash
next dev --turbo
```

### Current Status (as of Next.js 15)

- **Development**: Stable, recommended
- **Production**: Experimental, opt-in

### Enable for Production (Experimental)

```js
// next.config.js
module.exports = {
  experimental: {
    turbo: {},
  },
}
```

### Benefits

- **5-10x faster cold starts** in development
- **Faster HMR** (Hot Module Replacement)
- **Lower memory usage**

### Limitations

- Some Webpack plugins not yet supported
- Custom Webpack config requires migration

### Migration Strategy

1. Test in development first: `next dev --turbo`
2. Verify all features work correctly
3. Check for unsupported Webpack plugins
4. Migrate custom configurations
5. Test production builds thoroughly before deploying

## Dependency Analysis

### Find Heavy Dependencies

```bash
# Install dependency analyzer
npm install -g depcheck

# Find unused dependencies
depcheck

# Check bundle impact
npm install -g bundle-phobia-cli
bundle-phobia lodash
```

### Lighter Alternatives

| Heavy Library | Lighter Alternative | Savings |
|--------------|---------------------|---------|
| moment.js (288 KB) | date-fns (27 KB) | 261 KB |
| lodash (72 KB) | lodash-es (tree-shakeable) | ~50 KB |
| axios (13 KB) | fetch API (native) | 13 KB |
| jquery (87 KB) | Native DOM APIs | 87 KB |

### next/third-parties

Optimize third-party scripts:

```tsx
// BAD: Blocks rendering
<script src="https://www.googletagmanager.com/gtag/js" />

// GOOD: Optimized loading with next/third-parties
import { GoogleAnalytics } from '@next/third-parties/google'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>{children}</body>
      <GoogleAnalytics gaId="G-XYZ" />
    </html>
  )
}
```

## Performance Budgets

Set limits to prevent bundle size regression.

### Next.js Performance Budgets

```js
// next.config.js
module.exports = {
  webpack: (config) => {
    config.performance = {
      maxAssetSize: 250 * 1024, // 250 KB
      maxEntrypointSize: 400 * 1024, // 400 KB
      hints: 'error', // Fail build if exceeded
    }

    return config
  },
}
```

### CI Integration

```json
// package.json
{
  "scripts": {
    "build": "next build",
    "analyze": "ANALYZE=true next build",
    "check-bundle": "npm run build && bundlesize"
  },
  "bundlesize": [
    {
      "path": ".next/static/chunks/*.js",
      "maxSize": "250 KB"
    }
  ]
}
```

## Anti-Patterns

### No Code Splitting

```tsx
// BAD: Everything in one bundle
import HeavyChart from './HeavyChart'
import HeavyEditor from './HeavyEditor'
import HeavyMap from './HeavyMap'

export default function Page() {
  return (
    <>
      <HeavyChart />
      <HeavyEditor />
      <HeavyMap />
    </>
  )
}
```

### Importing Entire Libraries

```ts
// BAD: 100+ KB
import _ from 'lodash'

// GOOD: ~5 KB
import debounce from 'lodash/debounce'
```

### Too Many Small Chunks

```js
// BAD: Creates hundreds of tiny chunks
splitChunks: {
  minSize: 1 * 1024, // 1 KB minimum
}

// GOOD: Reasonable chunk sizes
splitChunks: {
  minSize: 20 * 1024, // 20 KB minimum
}
```

### No Bundle Analysis

Build without ever checking bundle composition. Always use bundle analyzer periodically.

### Ignoring Duplicate Dependencies

Multiple versions of the same package across chunks. Use `npm dedupe` or manage peer dependencies properly.

## Optimization Checklist

- [ ] Bundle analyzer configured and reviewed regularly
- [ ] Dynamic imports for heavy components
- [ ] Route-based code splitting utilized
- [ ] splitChunks configured for optimal caching
- [ ] sideEffects configured in package.json
- [ ] Direct imports from specific modules (not barrel files)
- [ ] Lighter alternatives evaluated for heavy dependencies
- [ ] next/third-parties used for external scripts
- [ ] Performance budgets set and enforced
- [ ] Bundle size monitored in CI/CD
- [ ] Turbopack tested in development

## Bundle Size Targets

- **Initial JS load**: < 170 KB (compressed)
- **Total page weight**: < 1 MB
- **Largest chunk**: < 250 KB
- **Number of chunks**: < 20 for most routes
