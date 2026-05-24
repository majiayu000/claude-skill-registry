---
name: vite
description: Vite performance optimization guidelines. This skill should be used when writing, reviewing, or refactoring Vite configuration and projects to ensure optimal performance patterns. Triggers on tasks involving Vite config, build optimization, dependency pre-bundling, plugin development, bundle analysis, or HMR issues.
---

# Vite Best Practices

Comprehensive performance optimization guide for Vite applications. Contains 42 rules across 8 categories, prioritized by impact to guide automated refactoring and code generation.

## When to Apply

Reference these guidelines when:
- Configuring Vite for a new project
- Troubleshooting slow dev server startup
- Optimizing production bundle size
- Debugging HMR issues
- Writing or evaluating Vite plugins
- Migrating from Webpack or other bundlers

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Dependency Pre-bundling | CRITICAL | `deps-` |
| 2 | Plugin Performance | CRITICAL | `plugin-` |
| 3 | Bundle Optimization | CRITICAL | `bundle-` |
| 4 | Import Resolution | HIGH | `import-` |
| 5 | Build Configuration | HIGH | `build-` |
| 6 | Development Server | MEDIUM-HIGH | `dev-` |
| 7 | CSS Optimization | MEDIUM | `css-` |
| 8 | Advanced Patterns | LOW-MEDIUM | `advanced-` |

## Quick Reference

### 1. Dependency Pre-bundling (CRITICAL)

- [`deps-include-large-cjs`](references/deps-include-large-cjs.md) - Include large dependencies with many modules
- [`deps-exclude-esm`](references/deps-exclude-esm.md) - Exclude small ESM dependencies
- [`deps-force-rebundle`](references/deps-force-rebundle.md) - Use --force flag for dependency changes
- [`deps-hold-until-crawl`](references/deps-hold-until-crawl.md) - Configure holdUntilCrawlEnd for startup behavior
- [`deps-entries`](references/deps-entries.md) - Configure custom entry points for discovery
- [`deps-linked-packages`](references/deps-linked-packages.md) - Handle linked dependencies in monorepos

### 2. Plugin Performance (CRITICAL)

- [`plugin-lazy-imports`](references/plugin-lazy-imports.md) - Use dynamic imports in plugin code
- [`plugin-avoid-long-hooks`](references/plugin-avoid-long-hooks.md) - Avoid long operations in startup hooks
- [`plugin-transform-early-return`](references/plugin-transform-early-return.md) - Early return in transform hooks
- [`plugin-audit-community`](references/plugin-audit-community.md) - Audit community plugins for performance
- [`plugin-swc-over-babel`](references/plugin-swc-over-babel.md) - Use SWC instead of Babel for React

### 3. Bundle Optimization (CRITICAL)

- [`bundle-manual-chunks`](references/bundle-manual-chunks.md) - Use manualChunks for vendor splitting
- [`bundle-dynamic-imports`](references/bundle-dynamic-imports.md) - Use dynamic imports for route-level splitting
- [`bundle-analyze`](references/bundle-analyze.md) - Analyze bundle composition
- [`bundle-tree-shaking`](references/bundle-tree-shaking.md) - Enable effective tree-shaking
- [`bundle-chunk-warning`](references/bundle-chunk-warning.md) - Address large chunk warnings
- [`bundle-compression`](references/bundle-compression.md) - Disable compressed size reporting for large projects
- [`bundle-asset-inlining`](references/bundle-asset-inlining.md) - Configure asset inlining threshold

### 4. Import Resolution (HIGH)

- [`import-avoid-barrel`](references/import-avoid-barrel.md) - Avoid barrel file imports
- [`import-explicit-extensions`](references/import-explicit-extensions.md) - Use explicit file extensions
- [`import-path-aliases`](references/import-path-aliases.md) - Configure path aliases for clean imports
- [`import-svg-strings`](references/import-svg-strings.md) - Import SVGs as strings instead of components
- [`import-glob-patterns`](references/import-glob-patterns.md) - Use glob imports carefully

### 5. Build Configuration (HIGH)

- [`build-modern-target`](references/build-modern-target.md) - Target modern browsers
- [`build-minification`](references/build-minification.md) - Use esbuild for minification
- [`build-sourcemaps`](references/build-sourcemaps.md) - Disable source maps in production
- [`build-css-code-split`](references/build-css-code-split.md) - Enable CSS code splitting
- [`build-rolldown`](references/build-rolldown.md) - Consider Rolldown for faster builds
- [`build-output-dir`](references/build-output-dir.md) - Configure output directory and caching

### 6. Development Server (MEDIUM-HIGH)

- [`dev-server-warmup`](references/dev-server-warmup.md) - Warm up frequently used files
- [`dev-browser-cache`](references/dev-browser-cache.md) - Keep browser cache enabled in DevTools
- [`dev-fs-limits`](references/dev-fs-limits.md) - Increase file descriptor limits on Linux
- [`dev-wsl-polling`](references/dev-wsl-polling.md) - Use polling for WSL file watching
- [`dev-https-proxy`](references/dev-https-proxy.md) - Configure HTTPS and proxy for development

### 7. CSS Optimization (MEDIUM)

- [`css-lightning`](references/css-lightning.md) - Use Lightning CSS instead of PostCSS
- [`css-avoid-preprocessors`](references/css-avoid-preprocessors.md) - Prefer CSS over preprocessors when possible
- [`css-modules`](references/css-modules.md) - Use CSS Modules for component styles
- [`css-inline-critical`](references/css-inline-critical.md) - Extract critical CSS for initial paint

### 8. Advanced Patterns (LOW-MEDIUM)

- [`advanced-ssr-externalize`](references/advanced-ssr-externalize.md) - Externalize dependencies for SSR
- [`advanced-env-static`](references/advanced-env-static.md) - Use static environment variables
- [`advanced-profiling`](references/advanced-profiling.md) - Profile build performance
- [`advanced-lib-mode`](references/advanced-lib-mode.md) - Configure library mode for package development

## How to Use

Read individual reference files for detailed explanations and code examples:

- [Section definitions](references/_sections.md) - Category structure and impact levels
- [Rule template](assets/templates/_template.md) - Template for adding new rules

## Reference Files

| File | Description |
|------|-------------|
| [AGENTS.md](AGENTS.md) | Complete compiled guide with all rules |
| [references/_sections.md](references/_sections.md) | Category definitions and ordering |
| [assets/templates/_template.md](assets/templates/_template.md) | Template for new rules |
| [metadata.json](metadata.json) | Version and reference information |
