---
name: stitch-html-components
description: Converts Stitch designs into clean, platform-agnostic HTML5 + CSS — semantic markup, CSS custom properties for theming, dark mode via prefers-color-scheme, mobile-first responsive, zero framework dependencies. Works in browsers, WebViews, Capacitor, and Ionic.
allowed-tools:
  - "stitch*:*"
  - "Bash"
  - "Read"
  - "Write"
---

# Stitch → HTML5 + CSS (Platform-Agnostic)

You are a frontend engineer specializing in clean, dependency-free HTML and CSS. You convert Stitch designs into semantic HTML5 with CSS custom properties — no React, no Svelte, no build step. The output runs anywhere: desktop browsers, mobile browsers, iOS WebView, Android WebView, Capacitor apps, and Ionic shells.

## When to use this skill

Use this skill when:
- The user wants **platform-agnostic** output — "just HTML", "no framework", "works everywhere"
- The target is a **WebView** in a mobile app (Capacitor, Ionic, Cordova)
- Building a **static site** or embedding in a CMS
- The user hasn't chosen a framework yet and wants a working prototype
- Generating the **HTML base** before wrapping with Capacitor for native mobile

## Prerequisites

- Access to Stitch MCP server
- A Stitch project with at least one generated screen

## Step 1: Retrieve the design

1. **Namespace discovery** — `list_tools` to find the Stitch MCP prefix
2. **Fetch metadata** — `[prefix]:get_screen` for the design JSON
3. **Download HTML** — GCS URLs need the reliable downloader:
   ```bash
   bash scripts/fetch-stitch.sh "[htmlCode.downloadUrl]" "temp/source.html"
   ```
4. **Visual audit** — check `screenshot.downloadUrl` before rewriting

## Step 2: File structure

```
output/
├── index.html           ← Main page (or rename per screen)
├── css/
│   ├── tokens.css       ← CSS custom properties (light + dark)
│   ├── base.css         ← Reset, body defaults, typography
│   └── components.css   ← Component styles
├── js/
│   └── main.js          ← Minimal JS (theme toggle, mobile menu only)
└── assets/
    └── images/
```

For multi-screen projects, each screen gets its own HTML file. Shared CSS lives in `tokens.css` and `base.css`.

## Step 3: CSS custom properties

Map Stitch colors to semantic tokens. Always generate **both light and dark** at the same time.

```css
/* css/tokens.css */

:root {
  /* Extract these from the Stitch HTML's tailwind.config in <head> */
  --color-background: [hex];
  --color-surface: [hex];
  --color-primary: [hex];
  --color-primary-fg: [hex];
  --color-text: [hex];
  --color-text-muted: [hex];
  --color-border: [hex];

  --font-sans: [font-stack];
  --font-mono: ui-monospace, monospace;

  --radius-sm: [value];
  --radius-md: [value];
  --radius-lg: [value];

  --shadow-sm: 0 1px 3px rgb(0 0 0 / 0.1);
  --shadow-md: 0 4px 12px rgb(0 0 0 / 0.1);

  --transition: 150ms cubic-bezier(0.4, 0, 0.2, 1);
}

/* Dark mode — system preference */
@media (prefers-color-scheme: dark) {
  :root {
    --color-background: [dark-hex];
    --color-surface: [dark-hex];
    --color-primary: [dark-adjusted-hex];
    --color-primary-fg: [dark-hex];
    --color-text: [dark-hex];
    --color-text-muted: [dark-hex];
    --color-border: [dark-hex];
  }
}

/* Dark mode — manual toggle via data-theme="dark" on <html> */
[data-theme="dark"] {
  --color-background: [dark-hex];
  --color-surface: [dark-hex];
  /* ... same values as above */
}
```

If the project already has a `design-tokens.css` (from `stitch-design-system`), import it instead of recreating tokens.

## Step 4: Base CSS

```css
/* css/base.css */

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html {
  font-size: 16px;
  /* Safe area insets for notched phones */
  padding: env(safe-area-inset-top) env(safe-area-inset-right)
           env(safe-area-inset-bottom) env(safe-area-inset-left);
  -webkit-text-size-adjust: 100%; /* Prevent font scaling on iOS rotation */
}

body {
  font-family: var(--font-sans);
  background-color: var(--color-background);
  color: var(--color-text);
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
}

/* Skip link for accessibility */
.sr-only {
  position: absolute; width: 1px; height: 1px;
  padding: 0; margin: -1px; overflow: hidden;
  clip: rect(0,0,0,0); white-space: nowrap; border-width: 0;
}

.skip-link { /* ... see stitch-a11y skill */ }

/* Focus ring — keyboard only */
*:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
  border-radius: 2px;
}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

## Step 5: Semantic HTML structure

Convert Stitch layout to semantic HTML5. Never use `<div>` where a semantic element fits:

| Stitch element | → HTML element |
|---|---|
| Page shell / app chrome | `<body>` → `<header>` + `<main>` + `<footer>` |
| Navigation bar | `<nav aria-label="Main navigation">` |
| Primary content area | `<main id="main-content">` |
| Article/post/card content | `<article>` |
| Sidebar | `<aside>` |
| Section of page | `<section aria-labelledby="section-id">` |
| Button (no href) | `<button type="button">` |
| Link with navigation | `<a href="...">` |
| Form container | `<form>` with `<label>` for every input |
| Images | `<img alt="descriptive text">` |

**Mobile HTML template:**
```html
<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
  <meta charset="UTF-8">
  <!-- Critical for mobile: prevent zoom, respect viewport -->
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <!-- iOS PWA meta tags -->
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="default">
  <!-- Theme color (top browser bar on Android) -->
  <meta name="theme-color" content="[--color-background hex]">

  <title>[Screen title]</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="stylesheet" href="css/tokens.css">
  <link rel="stylesheet" href="css/base.css">
  <link rel="stylesheet" href="css/components.css">
</head>
<body>
  <!-- Skip nav for keyboard users -->
  <a href="#main-content" class="skip-link">Skip to content</a>

  <!-- App shell -->
  <div class="app-shell">
    <header class="app-header" role="banner">
      <nav aria-label="Main navigation">
        <!-- Nav content -->
      </nav>
    </header>

    <main id="main-content" class="app-main">
      <!-- Page content -->
    </main>

    <!-- Bottom nav (mobile) -->
    <nav class="bottom-nav" aria-label="Tab navigation">
      <!-- Tab items -->
    </nav>
  </div>

  <script src="js/main.js" type="module"></script>
</body>
</html>
```

## Step 6: Mobile-first CSS rules

Every component must follow these mobile constraints:

### Touch targets
```css
/* All interactive elements: minimum 44×44px tap area */
button, a, [role="button"] {
  min-height: 44px;
  min-width: 44px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
```

### Scrolling
```css
/* Smooth scroll on iOS */
.scrollable {
  overflow-y: scroll;
  -webkit-overflow-scrolling: touch;
  overscroll-behavior: contain; /* Prevent scroll chaining */
}
```

### Bottom navigation bar
```css
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  /* Account for iOS home indicator */
  padding-bottom: env(safe-area-inset-bottom);
  background: var(--color-surface);
  border-top: 1px solid var(--color-border);
  display: flex;
  justify-content: space-around;
  z-index: 100;
}

/* Push main content above bottom nav */
.app-main {
  padding-bottom: calc(60px + env(safe-area-inset-bottom));
}
```

### Responsive breakpoints
```css
/* Mobile-first: base styles are for mobile */

/* Tablet (768px+) */
@media (min-width: 768px) {
  .container { max-width: 720px; margin: 0 auto; }
}

/* Desktop (1024px+) */
@media (min-width: 1024px) {
  .container { max-width: 1200px; }
  .bottom-nav { display: none; } /* Hide bottom nav, use sidebar */
  .sidebar { display: block; }   /* Show desktop sidebar */
}
```

## Step 7: Minimal JavaScript

Keep JS to an absolute minimum. The only things that need JS:
1. Theme toggle (dark/light)
2. Mobile menu open/close
3. Accordion/tabs interactive behavior

```js
// js/main.js

// Dark mode toggle
const html = document.documentElement;
const savedTheme = localStorage.getItem('theme') || 'light';
html.setAttribute('data-theme', savedTheme);

document.getElementById('theme-toggle')?.addEventListener('click', () => {
  const next = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
  html.setAttribute('data-theme', next);
  localStorage.setItem('theme', next);
});

// Mobile menu toggle
document.getElementById('menu-toggle')?.addEventListener('click', () => {
  const nav = document.getElementById('mobile-nav');
  const expanded = nav.getAttribute('aria-expanded') === 'true';
  nav.setAttribute('aria-expanded', String(!expanded));
  nav.classList.toggle('is-open');
});
```

## Step 8: Capacitor / WebView notes

If this HTML will be embedded in a Capacitor or Ionic app:
- All asset paths must be **relative** (no `/` prefix): `./css/tokens.css`, `./assets/logo.png`
- Capacitor reads from the `www/` or `dist/` directory — output there
- Capacitor's `capacitor.config.json` sets the WebDir: `"webDir": "www"`
- To call native APIs (camera, filesystem), use the Capacitor plugin JS APIs — beyond this skill's scope

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Fonts look zoomed on iOS rotation | Add `-webkit-text-size-adjust: 100%` to `html` |
| Content under notch | Add `env(safe-area-inset-*)` padding |
| Scrolling feels laggy on iOS | Add `-webkit-overflow-scrolling: touch` |
| Bottom nav overlaps content | Add `padding-bottom` to `<main>` equal to nav height + safe area |
| Click delay on mobile (300ms) | Add `touch-action: manipulation` to buttons |

## Integration

- Run `stitch-design-system` first to generate `design-tokens.css` — import it instead of recreating tokens
- Run `stitch-a11y` after for an accessibility pass
- Run `stitch-animate` to add CSS-only transitions (zero JS needed for most animations)

## References

- `resources/mobile-template.html` — Full mobile HTML boilerplate
- `resources/architecture-checklist.md` — Pre-ship checklist
- `scripts/fetch-stitch.sh` — Reliable GCS HTML downloader
