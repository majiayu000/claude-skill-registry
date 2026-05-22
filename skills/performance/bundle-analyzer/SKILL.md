---
name: bundle-analyzer
description: Analyzes JavaScript bundle sizes, identifies large dependencies, and suggests optimizations for webpack, vite, rollup. Use when user asks to "analyze bundle", "optimize bundle size", "reduce bundle", "webpack analysis", or "tree shaking".
allowed-tools: [Read, Write, Bash, Glob, Grep]
---

# Bundle Analyzer

Analyzes JavaScript bundle sizes, identifies optimization opportunities, and helps reduce bundle size for faster page loads.

## When to Use

- "Analyze my bundle size"
- "Why is my bundle so large?"
- "Optimize webpack bundle"
- "Reduce bundle size"
- "Find large dependencies"
- "Setup bundle analysis"

## Instructions

### 1. Detect Build Tool

Check which bundler is being used:

```bash
# Check package.json
grep -E "(webpack|vite|rollup|parcel|esbuild)" package.json

# Check config files
[ -f "webpack.config.js" ] && echo "Webpack"
[ -f "vite.config.js" ] && echo "Vite"
[ -f "rollup.config.js" ] && echo "Rollup"
```

### 2. Install Analysis Tool

**For Webpack:**
```bash
npm install --save-dev webpack-bundle-analyzer
```

**For Vite:**
```bash
npm install --save-dev rollup-plugin-visualizer
```

**For Rollup:**
```bash
npm install --save-dev rollup-plugin-visualizer
```

**Cross-platform:**
```bash
npm install --save-dev source-map-explorer
```

### 3. Configure Analysis

## Webpack

**webpack.config.js:**
```javascript
const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer')

module.exports = {
  // ... other config
  plugins: [
    new BundleAnalyzerPlugin({
      analyzerMode: 'static',
      reportFilename: 'bundle-report.html',
      openAnalyzer: true,
      generateStatsFile: true,
      statsFilename: 'bundle-stats.json'
    })
  ]
}
```

**Or for conditional analysis:**
```javascript
const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer')

module.exports = {
  plugins: [
    process.env.ANALYZE && new BundleAnalyzerPlugin()
  ].filter(Boolean)
}
```

**package.json scripts:**
```json
{
  "scripts": {
    "build": "webpack",
    "build:analyze": "ANALYZE=true webpack",
    "analyze": "webpack-bundle-analyzer dist/stats.json"
  }
}
```

## Vite

**vite.config.js:**
```javascript
import { defineConfig } from 'vite'
import { visualizer } from 'rollup-plugin-visualizer'

export default defineConfig({
  plugins: [
    visualizer({
      open: true,
      gzipSize: true,
      brotliSize: true,
      filename: 'dist/stats.html'
    })
  ],
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          utils: ['lodash', 'date-fns']
        }
      }
    }
  }
})
```

## Next.js

**next.config.js:**
```javascript
const { ANALYZE } = process.env

module.exports = {
  webpack: (config, { isServer }) => {
    if (ANALYZE) {
      const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer')
      config.plugins.push(
        new BundleAnalyzerPlugin({
          analyzerMode: 'static',
          reportFilename: isServer
            ? '../analyze/server.html'
            : './analyze/client.html'
        })
      )
    }
    return config
  }
}
```

**Or use @next/bundle-analyzer:**
```bash
npm install --save-dev @next/bundle-analyzer
```

```javascript
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true'
})

module.exports = withBundleAnalyzer({
  // Next.js config
})
```

**package.json:**
```json
{
  "scripts": {
    "analyze": "ANALYZE=true next build"
  }
}
```

## Create React App

```bash
npm install --save-dev source-map-explorer
```

**package.json:**
```json
{
  "scripts": {
    "analyze": "source-map-explorer 'build/static/js/*.js'"
  }
}
```

### 4. Analyze Bundle

Run analysis:

```bash
npm run build:analyze
# or
npm run analyze
```

Generate report showing:
- Total bundle size
- Breakdown by module
- Treemap visualization
- Gzipped sizes
- Duplicate dependencies

### 5. Identify Issues

**Common issues to look for:**

1. **Large Dependencies**
   - Moment.js (use date-fns or dayjs instead)
   - Lodash (use lodash-es or individual functions)
   - Full libraries when only using small parts

2. **Duplicate Dependencies**
   - Same package included multiple times
   - Different versions of same package

3. **Unused Code**
   - Dead code not tree-shaken
   - CSS/JS not actually used

4. **Large Images/Assets**
   - Images not optimized
   - SVGs not compressed

5. **Development Code in Production**
   - Console logs
   - Dev-only packages
   - Source maps in production

### 6. Suggest Optimizations

## Optimization Strategies

**1. Code Splitting**

```javascript
// Dynamic imports
const HeavyComponent = lazy(() => import('./HeavyComponent'))

// Route-based splitting
const Dashboard = lazy(() => import('./pages/Dashboard'))
const Settings = lazy(() => import('./pages/Settings'))

// Webpack magic comments
const module = import(
  /* webpackChunkName: "my-chunk" */
  /* webpackPrefetch: true */
  './module'
)
```

**2. Tree Shaking**

```javascript
// ❌ BAD: Imports entire library
import _ from 'lodash'

// ✅ GOOD: Import only what you need
import debounce from 'lodash/debounce'
import throttle from 'lodash/throttle'

// ✅ BETTER: Use lodash-es for tree-shaking
import { debounce, throttle } from 'lodash-es'
```

**3. Replace Large Libraries**

```javascript
// ❌ BAD: Moment.js (heavy)
import moment from 'moment'

// ✅ GOOD: date-fns (modular)
import { format, parseISO } from 'date-fns'

// ✅ GOOD: dayjs (lightweight)
import dayjs from 'dayjs'
```

**4. Lazy Load Routes (React Router)**

```javascript
import { lazy, Suspense } from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'

const Home = lazy(() => import('./pages/Home'))
const About = lazy(() => import('./pages/About'))
const Dashboard = lazy(() => import('./pages/Dashboard'))

function App() {
  return (
    <BrowserRouter>
      <Suspense fallback={<div>Loading...</div>}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/dashboard" element={<Dashboard />} />
        </Routes>
      </Suspense>
    </BrowserRouter>
  )
}
```

**5. Manual Chunks (Vite/Rollup)**

```javascript
// vite.config.js
export default {
  build: {
    rollupOptions: {
      output: {
        manualChunks(id) {
          // Vendor chunk for node_modules
          if (id.includes('node_modules')) {
            if (id.includes('react') || id.includes('react-dom')) {
              return 'react-vendor'
            }
            if (id.includes('@mui')) {
              return 'mui-vendor'
            }
            return 'vendor'
          }
        }
      }
    }
  }
}
```

**6. Externalize Dependencies (CDN)**

```javascript
// webpack.config.js
module.exports = {
  externals: {
    react: 'React',
    'react-dom': 'ReactDOM',
    lodash: '_'
  }
}
```

```html
<!-- index.html -->
<script src="https://cdn.jsdelivr.net/npm/react@18/umd/react.production.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/react-dom@18/umd/react-dom.production.min.js"></script>
```

**7. Optimize Images**

```javascript
// next.config.js
module.exports = {
  images: {
    formats: ['image/avif', 'image/webp'],
    deviceSizes: [640, 750, 828, 1080, 1200, 1920],
  }
}

// Use next/image
import Image from 'next/image'

<Image
  src="/photo.jpg"
  width={500}
  height={300}
  alt="Photo"
/>
```

**8. Remove Unused CSS**

```bash
# Install PurgeCSS
npm install --save-dev @fullhuman/postcss-purgecss
```

```javascript
// postcss.config.js
module.exports = {
  plugins: [
    require('@fullhuman/postcss-purgecss')({
      content: ['./src/**/*.{js,jsx,ts,tsx}'],
      defaultExtractor: content => content.match(/[\w-/:]+(?<!:)/g) || []
    })
  ]
}
```

**9. Compression**

```javascript
// webpack.config.js
const CompressionPlugin = require('compression-webpack-plugin')

module.exports = {
  plugins: [
    new CompressionPlugin({
      algorithm: 'gzip',
      test: /\.(js|css|html|svg)$/,
      threshold: 10240,
      minRatio: 0.8
    })
  ]
}
```

**10. Environment-Specific Code**

```javascript
// webpack.config.js
const webpack = require('webpack')

module.exports = {
  plugins: [
    new webpack.DefinePlugin({
      'process.env.NODE_ENV': JSON.stringify('production')
    })
  ]
}

// In code
if (process.env.NODE_ENV !== 'production') {
  // This will be removed in production build
  console.log('Development mode')
}
```

### 7. Size Budgets

**webpack.config.js:**
```javascript
module.exports = {
  performance: {
    maxEntrypointSize: 250000, // 250kb
    maxAssetSize: 250000,
    hints: 'warning'
  }
}
```

**package.json with size-limit:**
```bash
npm install --save-dev size-limit @size-limit/preset-app
```

```json
{
  "size-limit": [
    {
      "path": "dist/bundle.js",
      "limit": "300 KB"
    },
    {
      "path": "dist/vendor.js",
      "limit": "200 KB"
    }
  ]
}
```

### 8. CI/CD Integration

**GitHub Actions:**
```yaml
name: Bundle Size Check

on: [pull_request]

jobs:
  size:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm ci
      - run: npm run build

      - name: Check bundle size
        uses: andresz1/size-limit-action@v1
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
```

### 9. Monitoring

**Set up continuous monitoring:**

```javascript
// Report to analytics
if (typeof window !== 'undefined' && window.performance) {
  const perfData = window.performance.getEntriesByType('resource')

  perfData.forEach(entry => {
    if (entry.name.includes('.js')) {
      console.log(`${entry.name}: ${(entry.transferSize / 1024).toFixed(2)} KB`)
    }
  })
}
```

**Lighthouse CI:**
```yaml
# .lighthouserc.js
module.exports = {
  ci: {
    assert: {
      assertions: {
        'total-byte-weight': ['error', { maxNumericValue: 1000000 }],
        'resource-summary:script:size': ['error', { maxNumericValue: 500000 }]
      }
    }
  }
}
```

### 10. Generate Report

Create comprehensive report:

```markdown
# Bundle Analysis Report

## Summary
- Total bundle size: 450 KB (gzipped: 150 KB)
- Number of chunks: 5
- Largest chunk: vendor.js (200 KB)

## Top 10 Largest Dependencies
1. moment.js - 72 KB (❌ Consider replacing with date-fns)
2. lodash - 65 KB (⚠️ Use lodash-es for tree-shaking)
3. @mui/material - 120 KB (✅ Already code-split)
4. react-dom - 40 KB (✅ Essential)
5. chart.js - 35 KB (⚠️ Lazy load if not on first page)

## Optimization Opportunities
- [ ] Replace moment.js with date-fns (-50 KB)
- [ ] Use lodash-es instead of lodash (-30 KB)
- [ ] Lazy load chart.js (-35 KB)
- [ ] Code split routes (-80 KB initial load)
- [ ] Remove unused CSS (-15 KB)

## Estimated Savings
Total potential reduction: 210 KB (47% smaller)
New bundle size: 240 KB

## Action Items
1. Immediate: Replace moment.js
2. Short-term: Implement route-based code splitting
3. Long-term: Audit and remove unused dependencies
```

### Best Practices

**DO:**
- Analyze on every major release
- Set size budgets and enforce them
- Use code splitting for routes
- Lazy load below-the-fold content
- Tree-shake effectively
- Monitor bundle size in CI/CD

**DON'T:**
- Import entire libraries
- Ignore duplicate dependencies
- Skip production optimizations
- Forget to compress assets
- Include dev dependencies in production
- Use large polyfills unnecessarily

### Size Targets

**General Guidelines:**
- Main bundle: < 200 KB (gzipped)
- Vendor bundle: < 300 KB (gzipped)
- Total page weight: < 1 MB
- Time to Interactive: < 3 seconds on 3G

**Mobile-first:**
- First bundle: < 100 KB (gzipped)
- Critical CSS: < 14 KB (first TCP round)
- Above-fold images: < 200 KB

### Analysis Checklist

- [ ] Bundle analysis tool installed
- [ ] Baseline measurements taken
- [ ] Large dependencies identified
- [ ] Duplicate dependencies found
- [ ] Code splitting implemented
- [ ] Tree shaking verified
- [ ] Size budgets set
- [ ] CI/CD checks added
- [ ] Production build optimized
- [ ] Monitoring in place
