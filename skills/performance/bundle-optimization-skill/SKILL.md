---
name: bundle-optimization
description: Bundle size reduction strategies, icon optimization, tree-shaking, and performance analysis. Use when reducing bundle size or optimizing imports.
---

# Bundle Optimization Skill

## Overview

This project achieved a **90% bundle reduction** (2.33MB → 236KB) through strategic optimizations. This skill documents proven patterns for maintaining optimal bundle size.

## Key Achievement: Icon Optimization

**Problem:** Wildcard imports caused massive bundle bloat
**Solution:** Icon manifest with build-time generation
**Result:** 90% reduction in bundle size

### The Problem

```typescript
// ❌ WRONG - Imports entire simple-icons library (2.33MB)
import * as Icons from 'simple-icons';

// This single line imports 2,000+ icons even if you only use 5
const reactIcon = Icons.siReact;
```typescript

### The Solution: Icon Manifest

**Location:** `src/lib/icon-manifest.ts`

### How it works

1. Curate list of needed icons (42 in this project)
2. Build script generates manifest with only those icons
3. Runtime imports from manifest instead of full library

```typescript
// ✅ CORRECT - Only includes curated icons
import { getIcon } from '@/lib/icon-manifest';

const reactIcon = getIcon('react');
// Bundle only includes 42 icons instead of 2,000+
```typescript

### Implementation

**1. Icon Manifest Generator Script**

**Location:** `scripts/generate-icons.js`

```javascript
// Runs during build process
// Reads curated icon list
// Generates optimized manifest
// Only includes icons actually used in project
```typescript

**2. Icon Manifest**

**Location:** `src/lib/icon-manifest.ts`

```typescript
// Auto-generated during build
import {
  siReact,
  siTypescript,
  siNextdotjs,
  // ... only 42 icons
} from 'simple-icons';

const iconManifest = {
  react: siReact,
  typescript: siTypescript,
  nextdotjs: siNextdotjs,
  // ...
};

export const getIcon = (name: string) => iconManifest[name];
```typescript

**3. Package.json Build Hook**

```json
{
  "scripts": {
    "prebuild": "node scripts/generate-icons.js",
    "build": "next build"
  }
}
```typescript

### Usage Pattern

```typescript
// Import the manifest function
import { getIcon } from '@/lib/icon-manifest';

function SkillIcon({ name }: { name: string }) {
  const icon = getIcon(name);

  if (!icon) return null;

  return (
    <div dangerouslySetInnerHTML={{ __html: icon.svg }} />
  );
}
```typescript

### Adding New Icons

1. Add icon name to curated list in `scripts/generate-icons.js`
2. Run build or `node scripts/generate-icons.js`
3. Manifest automatically regenerates
4. Use with `getIcon('newIconName')`

## Tree-Shaking Strategies

### 1. Named Imports Only

```typescript
// ✅ CORRECT - Tree-shakeable
import { Button } from '@/components/ui/button';
import { Camera, Settings } from 'lucide-react';

// ❌ WRONG - Imports everything
import * as Components from '@/components';
import * as Icons from 'lucide-react';
```typescript

### 2. Lucide Icons Configuration

**Location:** `next.config.ts`

```typescript
modularizeImports: {
  'lucide-react': {
    transform: 'lucide-react/dist/esm/icons/{{kebabCase member}}',
    skipDefaultConversion: true,
  },
}
```typescript

**Effect:** Each Lucide icon imports only its file, not entire library

### 3. Dynamic Imports for Large Dependencies

```typescript
// ✅ CORRECT - Load only when needed
const HeavyChart = dynamic(() => import('@/components/heavy-chart'), {
  loading: () => <Skeleton />,
  ssr: false, // Skip SSR if not needed
});

// Use in component
<HeavyChart data={data} />
```typescript

### 4. Code Splitting by Route

Next.js automatically code-splits by route, but you can optimize:

```typescript
// app/heavy-feature/page.tsx
import dynamic from 'next/dynamic';

// Split heavy components
const HeavyFeature = dynamic(() => import('@/components/heavy-feature'));

export default function Page() {
  return <HeavyFeature />;
}
```typescript

## Bundle Analysis Workflow

### Step 1: Enable Bundle Analyzer

```bash
# Install analyzer
npm install --save-dev @next/bundle-analyzer

# Run analysis
ANALYZE=true npm run build
```typescript

### Step 2: Review Results

Analyzer opens in browser showing:

- Chunk sizes
- Import paths
- Duplicate dependencies
- Optimization opportunities

### Step 3: Identify Issues

### Look for

- Large chunks (>500KB)
- Duplicate libraries (same lib in multiple chunks)
- Unused imports
- Large dependencies that could be lazy-loaded

### Step 4: Optimize

### Common fixes

1. Convert wildcard imports to named imports
2. Add dynamic imports for heavy components
3. Remove unused dependencies from package.json
4. Use smaller alternatives (e.g., date-fns instead of moment)

## Size Limit Configuration

**Location:** `package.json`

```json
{
  "size-limit": [
    {
      "path": ".next/static/chunks/app/page.js",
      "limit": "40 KB",
      "name": "Homepage"
    },
    {
      "path": ".next/static/chunks/app/skills/page.js",
      "limit": "40 KB",
      "name": "Skills Page"
    }
  ]
}
```typescript

### Running Size Checks

```bash
# Check all size limits
npm run size

# Output shows:
# ✓ Homepage: 7.73 KB / 40 KB (within limit)
# ✓ Skills: 6.31 KB / 40 KB (within limit)
```typescript

### CI/CD Integration

Size limits run in GitHub Actions quality gates:

```yaml
- name: Check bundle size
  run: npm run size
```typescript

**Failure:** Blocks PR if any bundle exceeds limit

## Performance Optimization Patterns

### 1. Image Optimization

```typescript
// ✅ CORRECT - Next.js Image component
import Image from 'next/image';

<Image
  src="/assets/photo.jpg"
  alt="Description"
  width={800}
  height={600}
  priority={false} // Lazy load by default
  quality={85}
/>
```typescript

### Benefits

- Automatic WebP/AVIF conversion
- Lazy loading by default
- Responsive images
- Optimized serving

### 2. Font Optimization

```typescript
// app/layout.tsx
import { Inter } from 'next/font/google';

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  preload: true,
});

export default function RootLayout({ children }) {
  return (
    <html className={inter.className}>
      <body>{children}</body>
    </html>
  );
}
```typescript

### Benefits

- Self-hosted fonts (no external requests)
- Automatic font optimization
- Zero layout shift

### 3. Script Loading Strategies

```typescript
import Script from 'next/script';

// Load after page is interactive
<Script
  src="https://analytics.example.com/script.js"
  strategy="lazyOnload"
/>

// Load before page is interactive
<Script
  src="https://critical.example.com/script.js"
  strategy="beforeInteractive"
/>
```typescript

### 4. CSS Optimization

### Tailwind Configuration

```javascript
// tailwind.config.js
module.exports = {
  content: [
    './src/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  // Purges unused CSS in production
};
```typescript

**Result:** Only CSS actually used is included in bundle

## Monitoring Bundle Size

### Current Metrics (Production)

```typescript
Homepage:     7.73 KB / 40 KB (19% of limit) ✅
Skills Page:  6.31 KB / 40 KB (16% of limit) ✅
Shared:       102 KB (routes share this)
```typescript

### Bundle Size History

### Before Optimization (October 2024)

- Homepage: 2.33 MB (with wildcard icon import)
- Skills Page: 2.35 MB

### After Icon Manifest (October 2024)

- Homepage: 236 KB (90% reduction)
- Skills Page: 193 KB

### After Additional Optimizations (November 2024)

- Homepage: 7.73 KB
- Skills Page: 6.31 KB

### Tracking Over Time

```bash
# Run before making changes
npm run size > before.txt

# Make optimizations

# Run after changes
npm run size > after.txt

# Compare
diff before.txt after.txt
```typescript

## Common Optimization Mistakes

### Mistake 1: Over-Splitting

```typescript
// ❌ WRONG - Too aggressive splitting
const Button = dynamic(() => import('./button'));
const Text = dynamic(() => import('./text'));
const Icon = dynamic(() => import('./icon'));

// Network overhead > bundle savings
```typescript

**Fix:** Only split genuinely large components (>50KB)

### Mistake 2: Importing Dev Dependencies in Production

```typescript
// ❌ WRONG - Imports dev tool in production
import { faker } from '@faker-js/faker';

const mockData = faker.name.firstName();
```typescript

**Fix:** Use conditional imports or environment checks

```typescript
// ✅ CORRECT
const mockData = process.env.NODE_ENV === 'development'
  ? await import('@faker-js/faker').then(m => m.faker.name.firstName())
  : 'John';
```typescript

### Mistake 3: Duplicate Dependencies

```bash
# Check for duplicates
npm ls <package-name>

# Example: Multiple versions of same package
npm ls react
# ├── react@19.0.0
# └── some-lib
#     └── react@18.0.0  # ❌ Duplicate!
```typescript

**Fix:** Update dependencies to use same version

## Performance Budget

### Current Limits

- **Homepage:** 40 KB (first-party JavaScript)
- **Other Routes:** 40 KB each
- **Shared Chunks:** 150 KB total
- **Images:** Lazy-loaded, optimized format

### Adding New Features

### Before adding dependency

1. Check package size on Bundlephobia
2. Consider alternatives
3. Run size check after installation
4. Verify no significant increase

```bash
# Check package size before installing
npx bundlephobia <package-name>

# Install
npm install <package-name>

# Verify size impact
npm run size
```typescript

## Optimization Checklist

When adding new features:

- [ ] Use named imports only (no wildcards)
- [ ] Check if dependency can be dynamic import
- [ ] Verify icon added to manifest (if using icons)
- [ ] Run bundle analyzer to check impact
- [ ] Ensure size limits still pass
- [ ] Test production build size
- [ ] Consider server-side alternative
- [ ] Check for lighter alternatives

## Quick Reference Commands

```bash
# Bundle analysis
ANALYZE=true npm run build

# Size limit check
npm run size

# Check package size before install
npx bundlephobia <package>

# Find duplicate dependencies
npm ls <package>

# Production build test
npm run build && npm run start

# Generate icon manifest
node scripts/generate-icons.js
```typescript

## Related Files

- `scripts/generate-icons.js` - Icon manifest generator
- `src/lib/icon-manifest.ts` - Generated icon manifest
- `next.config.ts` - Lucide tree-shaking configuration
- `package.json` - Size limit configuration
- `.github/workflows/quality-gates.yml` - CI/CD size checks

## Resources

- [Bundlephobia](https://bundlephobia.com/) - Check package sizes
- [Next.js Bundle Analyzer](https://www.npmjs.com/package/@next/bundle-analyzer)
- [size-limit](https://github.com/ai/size-limit) - Size limit enforcement
