---
name: tailwindcss-performance
description: Tailwind CSS performance optimization including v4 improvements and best practices
---

# Tailwind CSS Performance Optimization

## v4 Performance Improvements

Tailwind CSS v4 features a completely rewritten engine in Rust:

| Metric | v3 | v4 |
|--------|----|----|
| Full builds | Baseline | Up to 5x faster |
| Incremental builds | Milliseconds | Microseconds (100x+) |
| Engine | JavaScript | Rust |

## JIT (Just-In-Time) Compilation

### How JIT Works

JIT generates styles on-demand as classes are discovered in your files:

1. Scans source files for class names
2. Generates only the CSS you use
3. Produces minimal, optimized output

### v4: Always JIT

Unlike v3, JIT is always enabled in v4—no configuration needed:

```css
@import "tailwindcss";
/* JIT is automatic */
```

## Content Detection

### Automatic Detection (v4)

v4 automatically detects template files—no content configuration required:

```css
/* v4 - Works automatically */
@import "tailwindcss";
```

### Explicit Content (v4)

If automatic detection fails, specify sources explicitly:

```css
@import "tailwindcss";
@source "./src/**/*.{html,js,jsx,ts,tsx,vue,svelte}";
@source "./components/**/*.{js,jsx,ts,tsx}";
```

### Excluding Paths

```css
@source not "./src/legacy/**";
```

## Tree Shaking

### How It Works

Tailwind's build process removes unused CSS:

```
Source: All possible utilities (~15MB+)
↓
Scan: Find used class names
↓
Output: Only used styles (~10-50KB typical)
```

### Production Build

```bash
# Vite - automatically optimized for production
npm run build

# PostCSS - ensure NODE_ENV is set
NODE_ENV=production npx postcss input.css -o output.css
```

## Dynamic Class Names

### The Problem

Tailwind can't detect dynamically constructed class names:

```javascript
// BAD - Classes won't be generated
const color = 'blue'
className={`text-${color}-500`}  // ❌ Not detected

const size = 'lg'
className={`text-${size}`}  // ❌ Not detected
```

### Solutions

#### 1. Use Complete Class Names

```javascript
// GOOD - Full class names
const colorClasses = {
  blue: 'text-blue-500',
  red: 'text-red-500',
  green: 'text-green-500',
}
className={colorClasses[color]}  // ✓ Detected
```

#### 2. Use Data Attributes

```javascript
// GOOD - Style based on data attributes
<div data-color={color} className="data-[color=blue]:text-blue-500 data-[color=red]:text-red-500">
```

#### 3. Safelist Classes

```css
/* In your CSS for v4 */
@source inline("text-blue-500 text-red-500 text-green-500");
```

#### 4. CSS Variables

```css
@theme {
  --color-dynamic: oklch(0.6 0.2 250);
}
```

```html
<div class="text-[var(--color-dynamic)]">Dynamic color</div>
```

## Optimizing Transitions

### Use Specific Transitions

```html
<!-- SLOW - Transitions all properties -->
<button class="transition-all duration-200">

<!-- FAST - Only transitions specific properties -->
<button class="transition-colors duration-200">
<button class="transition-transform duration-200">
<button class="transition-opacity duration-200">
```

### GPU-Accelerated Properties

Prefer `transform` and `opacity` for smooth animations:

```html
<!-- GOOD - GPU accelerated -->
<div class="transform hover:scale-105 transition-transform">

<!-- GOOD - GPU accelerated -->
<div class="opacity-100 hover:opacity-80 transition-opacity">

<!-- SLOW - May cause repaints -->
<div class="left-0 hover:left-4 transition-all">
```

## CSS Variable Usage

### Prefer Native Variables

In v4, use CSS variables directly instead of `theme()`:

```css
/* v3 - Uses theme() function */
.element {
  color: theme(colors.blue.500);
}

/* v4 - Use CSS variables (faster) */
.element {
  color: var(--color-blue-500);
}
```

### Static Theme Values

For performance-critical paths:

```css
@import "tailwindcss/theme.css" theme(static);
```

This inlines theme values instead of using CSS variables.

## Build Optimization

### Vite Configuration

```javascript
// vite.config.js
import tailwindcss from '@tailwindcss/vite'
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [tailwindcss()],
  build: {
    // Minify CSS
    cssMinify: 'lightningcss',
    // Optimize chunks
    rollupOptions: {
      output: {
        manualChunks: {
          // Split vendor CSS if needed
        }
      }
    }
  }
})
```

### PostCSS with cssnano

```javascript
// postcss.config.mjs
export default {
  plugins: {
    '@tailwindcss/postcss': {},
    cssnano: process.env.NODE_ENV === 'production' ? {} : false
  }
}
```

## Reducing Bundle Size

### 1. Avoid Unused Plugins

```css
/* Only load what you need */
@plugin "@tailwindcss/typography";
/* Don't load unused plugins */
```

### 2. Limit Color Palette

```css
@theme {
  /* Disable default colors */
  --color-*: initial;

  /* Define only needed colors */
  --color-primary: oklch(0.6 0.2 250);
  --color-secondary: oklch(0.7 0.15 180);
  --color-gray-100: oklch(0.95 0 0);
  --color-gray-900: oklch(0.15 0 0);
}
```

### 3. Limit Breakpoints

```css
@theme {
  /* Remove unused breakpoints */
  --breakpoint-2xl: initial;

  /* Keep only what you use */
  --breakpoint-sm: 640px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
}
```

## Caching Strategies

### Development

- v4's incremental builds are already extremely fast
- No additional caching needed in most cases

### CI/CD

```yaml
# GitHub Actions example
- name: Cache node_modules
  uses: actions/cache@v4
  with:
    path: node_modules
    key: ${{ runner.os }}-node-${{ hashFiles('package-lock.json') }}

- name: Build
  run: npm run build
```

## Measuring Performance

### Build Time Analysis

```bash
# Time your build
time npm run build

# Verbose output
DEBUG=tailwindcss:* npm run build
```

### Bundle Analysis

```bash
# Install analyzer
npm install -D vite-bundle-analyzer

# Analyze bundle
npm run build -- --analyze
```

### CSS Size Check

```bash
# Check output CSS size
ls -lh dist/assets/*.css

# Gzipped size
gzip -c dist/assets/main.css | wc -c
```

## Performance Checklist

### Development

- [ ] JIT is working (styles update instantly)
- [ ] No console warnings about large files
- [ ] Hot reload is fast

### Production

- [ ] `NODE_ENV=production` is set
- [ ] CSS is minified
- [ ] Unused CSS is removed
- [ ] No dynamic class name issues
- [ ] CSS size is reasonable (<50KB typical)

### Common Issues

| Issue | Solution |
|-------|----------|
| Large CSS output | Check for dynamic classes, safelist issues |
| Slow builds | Ensure v4, check file globs |
| Missing styles | Check content detection, class names |
| Slow animations | Use GPU-accelerated properties |

## Lazy Loading CSS

For very large apps, consider code-splitting CSS:

```javascript
// Dynamically import CSS for routes
const AdminPage = lazy(() =>
  import('./admin.css').then(() => import('./AdminPage'))
)
```

## Best Practices Summary

1. **Let JIT do its work** - Don't safelist unnecessarily
2. **Use complete class names** - Avoid dynamic concatenation
3. **Specific transitions** - Not `transition-all`
4. **GPU properties** - Prefer `transform` and `opacity`
5. **Minimal theme** - Only define what you use
6. **Production builds** - Always use production mode
7. **Measure** - Check your actual CSS size
