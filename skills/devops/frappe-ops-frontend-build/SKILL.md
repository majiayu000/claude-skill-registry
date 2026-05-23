---
name: frappe-ops-frontend-build
description: >
  Use when configuring frontend asset bundling, migrating from build.json (v14) to esbuild (v15+), or troubleshooting SCSS/CSS compilation.
  Prevents build failures from mixing v14 and v15 build systems and misconfigured asset pipelines.
  Covers esbuild configuration (v15+), build.json (v14), asset bundling, SCSS compilation, bundle.js setup, bench build flags.
  Keywords: esbuild, build.json, frontend build, SCSS, CSS, asset bundling, bench build, bundle.js, webpack.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
metadata:
  author: OpenAEC-Foundation
  version: "2.0"
---

# Frontend Build System

Complete reference for Frappe's frontend asset bundling pipeline, from build configuration to production optimization.

**Versions**: v14 (build.json) / v15+ (esbuild)

---

## Quick Reference — Build Commands

| Task | Command |
|------|---------|
| Build all apps | `bench build` |
| Build specific app | `bench build --app myapp` |
| Build multiple apps | `bench build --apps frappe,erpnext` |
| Production build (minified) | `bench build --production` |
| Force rebuild | `bench build --force` |
| Watch mode (auto-rebuild) | `bench watch` |
| Hard link assets | `bench build --hard-link` |

---

## Decision Tree: Build System Selection

```
Which build system?
├── Frappe v14?
│   └── build.json — Concatenation-based bundling
├── Frappe v15+?
│   └── esbuild — ES module bundling with *.bundle.* convention
└── Migrating v14 → v15?
    └── Replace build.json with *.bundle.* files in public/
```

---

## Build Pipeline Overview

### v15+ (esbuild) — Current System

The v15+ build system uses esbuild for fast ES module bundling. It automatically discovers bundle entry points by scanning the `public/` directory for files matching `*.bundle.{js|ts|css|scss|sass|less|styl}`.

**How it works:**

1. `bench build` scans each app's `public/` directory recursively
2. Files matching `*.bundle.*` are treated as entry points
3. esbuild compiles, bundles, and optionally minifies each entry point
4. Output goes to `assets/dist/[app]/js/` or `assets/dist/[app]/css/`
5. Filenames include content hashes for cache-busting: `main.bundle.HASH.js`

**Supported file types:**
- `.js` — ES6 modules with import/export
- `.ts` — TypeScript
- `.vue` — Vue single-file components
- `.css` — Standard CSS
- `.scss` / `.sass` — SASS/SCSS stylesheets
- `.less` — Less stylesheets
- `.styl` — Stylus stylesheets

### v14 (build.json) — Legacy System

The v14 system uses `build.json` in the app root to define concatenation rules.

```json
{
  "js/myapp.min.js": [
    "public/js/file1.js",
    "public/js/file2.js"
  ],
  "css/myapp.min.css": [
    "public/css/style1.css",
    "public/css/style2.css"
  ]
}
```

**NEVER** use `build.json` in v15+ — it is ignored by the esbuild pipeline.

---

## Bundle Entry Points [v15+]

### Creating a Bundle

Place files in your app's `public/` directory with the `.bundle.` naming convention:

```
myapp/
└── public/
    ├── js/
    │   └── myapp.bundle.js       # → dist/myapp/js/myapp.bundle.HASH.js
    ├── css/
    │   └── myapp.bundle.scss     # → dist/myapp/css/myapp.bundle.HASH.css
    └── components/
        └── widget.bundle.js      # → dist/myapp/js/widget.bundle.HASH.js
```

### Bundle File Content

```javascript
// myapp/public/js/myapp.bundle.js
import { createApp } from "vue";
import MyComponent from "./components/MyComponent.vue";

// ES6 imports are resolved by esbuild
import "../css/myapp.bundle.scss";

// npm packages (installed via yarn) can be imported directly
import dayjs from "dayjs";

createApp(MyComponent).mount("#myapp-root");
```

### Output Mapping

| Input | Output |
|-------|--------|
| `public/js/main.bundle.js` | `assets/dist/[app]/js/main.bundle.[hash].js` |
| `public/css/style.bundle.scss` | `assets/dist/[app]/css/style.bundle.[hash].css` |
| `public/deep/nested/file.bundle.ts` | `assets/dist/[app]/js/file.bundle.[hash].js` |

---

## hooks.py Asset Inclusion

### Desk Assets (Backend Interface)

```python
# hooks.py — loads in /app (Desk)
app_include_js = "myapp.bundle.js"
app_include_css = "myapp.bundle.css"

# Multiple files
app_include_js = ["myapp.bundle.js", "extra.bundle.js"]
app_include_css = ["myapp.bundle.css", "extra.bundle.css"]
```

### Portal Assets (Public Website)

```python
# hooks.py — loads on web pages (portal)
web_include_js = "myapp-web.bundle.js"
web_include_css = "myapp-web.bundle.css"
```

### Page-Specific Assets

```python
# hooks.py — loads on specific Desk pages
page_js = {"page_name": "public/js/custom_page.js"}
```

### Web Form Assets (Standard Web Forms Only)

```python
# hooks.py — loads on specific Web Forms
webform_include_js = {"ToDo": "public/js/custom_todo.js"}
webform_include_css = {"ToDo": "public/css/custom_todo.css"}
```

### Critical Rules

- **ALWAYS** use the bundle filename (not the full path) in hooks.py for v15+
- **NEVER** include the hash in hooks.py — Frappe resolves the hashed filename automatically
- **ALWAYS** rebuild after changing hooks.py: `bench build --app myapp`
- Multiple apps can define the same hooks — assets accumulate across all installed apps

---

## Including Assets in Templates

### Jinja Helpers

```html
<!-- Include script with correct hash -->
{{ include_script("myapp.bundle.js") }}

<!-- Include stylesheet with correct hash -->
{{ include_style("myapp.bundle.css") }}

<!-- Get path string only (no HTML tag) -->
<script src="{{ bundled_asset('myapp.bundle.js') }}"></script>
```

### Lazy Loading in Desk

```javascript
// Load asset on demand (returns Promise)
frappe.require("myapp.bundle.js", () => {
    // Asset loaded, initialize component
    myapp.init();
});

// Multiple assets
frappe.require(["widget.bundle.js", "widget.bundle.css"], () => {
    // Both loaded
});
```

---

## SCSS/CSS Compilation

### SCSS Bundle Example

```scss
// myapp/public/css/myapp.bundle.scss

// Import Frappe variables (available in all apps)
@import "frappe/public/scss/variables";

// Import partials (NOT bundles — no .bundle. in name)
@import "./components/header";
@import "./components/sidebar";

.myapp-container {
  padding: var(--padding-lg);
  background: var(--bg-color);
}
```

### Partial Files

Partials (files starting with `_` or without `.bundle.` in the name) are NOT compiled as entry points. They are only included via `@import`:

```
public/css/
├── myapp.bundle.scss        # Entry point — compiled
├── _variables.scss          # Partial — imported only
└── components/
    ├── _header.scss         # Partial — imported only
    └── _sidebar.scss        # Partial — imported only
```

---

## Development Workflow

### Watch Mode [v15+]

```bash
# Auto-rebuild on file changes
bench watch
```

- Watches all apps' `public/` directories for changes
- Rebuilds only affected bundles (incremental)
- Desk auto-reloads when assets change (if `live_reload` is enabled)

### Enabling Live Reload

```bash
# Via config
bench set-config -g live_reload true

# Via environment variable
export LIVE_RELOAD=1
```

### Development vs Production Build

| Feature | Development (`bench build`) | Production (`bench build --production`) |
|---------|---------------------------|---------------------------------------|
| Minification | No | Yes |
| Source maps | Yes | No |
| Bundle size | Larger | Optimized |
| Build speed | Fast | Slower |

---

## Frappe UI (Vue.js) Custom Pages [v15+]

### Setting Up a Vue Page

```javascript
// myapp/public/js/mypage.bundle.js
import { createApp } from "vue";
import { FrappeUI } from "frappe-ui";
import App from "./App.vue";

const app = createApp(App);
app.use(FrappeUI);
app.mount("#myapp-page");
```

### Registering the Page

```python
# Create a Page DocType or use www/ for web pages
# The bundle loads via hooks.py or include_script()
```

### npm Dependencies

```bash
# Install from app directory
cd apps/myapp
yarn add vue frappe-ui dayjs
```

Dependencies are resolved by esbuild from `node_modules/` during build.

---

## Common Build Errors and Fixes

### Error: "Could not resolve module"

```
ERROR: Could not resolve "some-package"
```

**Fix**: Install the missing npm package:
```bash
cd apps/myapp && yarn add some-package
```

### Error: "No bundle entry points found"

**Fix**: Ensure files use the `*.bundle.*` naming convention and are in the `public/` directory.

### Error: Stale Assets After Deployment

**Fix**: Force rebuild with cache clear:
```bash
bench build --force
bench clear-cache
```

### Error: CSS Not Updating

**Fix**: Check that SCSS files import correctly and the entry point has `.bundle.` in the name:
```bash
bench build --app myapp --force
```

### Error: "build.json" Ignored in v15

**Fix**: Migrate to `*.bundle.*` entry points. build.json is a v14-only feature.

---

## Asset Optimization for Production

### Pre-Deployment Checklist

1. **Build with production flag**: `bench build --production`
2. **Verify bundle sizes**: Check `assets/dist/` for unexpectedly large files
3. **Use lazy loading**: Split rarely-used features into separate bundles loaded via `frappe.require()`
4. **Minimize hook includes**: Only include essential assets in `app_include_js/css`
5. **Use CSS variables**: Leverage Frappe's built-in CSS custom properties instead of duplicating styles

### Bundle Splitting Strategy

```
public/
├── js/
│   ├── myapp.bundle.js          # Core — loaded on every page via hooks
│   ├── report-widget.bundle.js  # Lazy — loaded only on report pages
│   └── chart-tools.bundle.js    # Lazy — loaded only when charts needed
└── css/
    ├── myapp.bundle.scss        # Core — loaded on every page via hooks
    └── print.bundle.scss        # Lazy — loaded only for print views
```

---

## Version Differences

| Feature | v14 | v15+ |
|---------|:---:|:----:|
| Build system | build.json | **esbuild** |
| Entry point convention | Defined in JSON | `*.bundle.*` auto-discovery |
| TypeScript support | No | **Yes** |
| Vue SFC support | No | **Yes** |
| SCSS compilation | Via build pipeline | **Via esbuild** |
| Watch mode | `bench watch` | `bench watch` (faster) |
| Live reload | Manual | **Automatic** (configurable) |
| Source maps | Limited | **Full support** |
| Tree shaking | No | **Yes** |
| npm imports | Requires manual bundling | **Direct ES6 imports** |

---

## Reference Files

| File | Contents |
|------|----------|
| [examples.md](references/examples.md) | Complete build configuration examples |
| [anti-patterns.md](references/anti-patterns.md) | Common build mistakes and fixes |
