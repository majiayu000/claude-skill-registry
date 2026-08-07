---
name: design-minimal
description: Use when the user explicitly asks for a standalone HTML page in a restrained minimal style, especially reading-first dashboards, briefs, handouts, maps, or internal reports. User-invoked only; do not auto-trigger.
---

# Design Minimal

Generate one standalone HTML page with a restrained minimal visual system: clear hierarchy, strong spacing, explicit structure, limited palette, and no decorative effects.

## Language

- Match the visible interface language to the user's language and artifact context.
- For Russian pages, write visible UI labels, headings, section names, status explanations, and footer copy in Russian.
- Keep English only for file paths, commands, code identifiers, schema fields, API names, model/tool names, and literal values that must remain copyable.
- If an English technical term is useful for teaching, pair it with a plain-language local label once, then use the local label in the interface.

## Hard Contract

1. Use one self-contained HTML file.
2. Use Tailwind CDN only for layout and component styling.
3. Do not write custom CSS rules for components, layout, typography, states, cards, grids, buttons, headers, or sections.
4. The only allowed CSS is design tokens as CSS variables in `:root`.
5. Do not add mobile adaptation: no responsive Tailwind prefixes (`sm:`, `md:`, `lg:`, `xl:`, `2xl:`), no media queries, no alternate mobile layout.
6. Do not use external fonts, JavaScript frameworks, icon libraries, SVG icons, gradients, shadows, rounded corners, or accent colors.
7. Use typography, color, spacing, and layout through Tailwind classes plus token variables.

Allowed `<style>` shape:

```html
<style>
  :root {
    --bg: #f5f4ef;
    --ink: #1a1a1a;
    --muted: #77736b;
    --hair: #d4d2cc;
    --paper-soft: #eeece4;
    --font-main: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    --font-mono: ui-monospace, "SF Mono", Menlo, monospace;
  }
</style>
```

Forbidden CSS shape:

```css
.card { ... }
@media (...) { ... }
body { ... }
button:hover { ... }
```

## Tailwind Usage

Use Tailwind classes directly on elements. Reference tokens through arbitrary values:

```html
<body class="m-0 bg-[var(--bg)] text-[var(--ink)] font-[var(--font-main)] text-[14px] leading-[1.55]">
  <main class="mx-auto w-[1120px] px-8 py-8 pb-20">
    <header class="border-y-2 border-[var(--ink)] py-4">
      <p class="text-[11px] uppercase tracking-[0.14em] text-[var(--muted)]">BRIEF 042 · INTERNAL</p>
      <h1 class="mt-3 text-[28px] leading-tight font-normal">Page Title</h1>
    </header>
  </main>
</body>
```

Use fixed desktop-oriented widths such as `w-[960px]`, `w-[1120px]`, `max-w-[1200px]`, `grid-cols-[...]`, `min-h-[...]`. Do not add mobile fallbacks. One-column, two-column, and dense multi-panel layouts are allowed when the content benefits from them.

## Visual Vocabulary

| Element | Tailwind Pattern |
|---|---|
| Page | `bg-[var(--bg)] text-[var(--ink)] font-[var(--font-main)] text-[14px] leading-[1.55]` |
| Shell | `mx-auto w-[1120px] px-8 py-8 pb-20` |
| Grid | `grid grid-cols-[1fr_320px] gap-6` or `grid grid-cols-3 gap-4` |
| Header | `border-y-2 border-[var(--ink)] py-4` |
| Meta | `text-[11px] uppercase tracking-[0.14em] text-[var(--muted)]` |
| Section label | `[ <span class="bg-[var(--ink)] text-[var(--bg)] px-1">MAIN</span> ]` |
| Panel | `border border-[var(--ink)] p-4` |
| Soft panel | `border border-dashed border-[var(--ink)] p-4` |
| Divider | Text dashes inside HTML, styled with muted mono text |
| Entry | `border-t border-[var(--hair)] pt-5 mt-5` |
| Link | `underline decoration-[var(--hair)] underline-offset-4 hover:bg-[var(--ink)] hover:text-[var(--bg)]` |
| Badge | `border border-[var(--hair)] px-1 text-[10px] uppercase text-[var(--muted)]` |

## Skeleton

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=900">
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    :root {
      --bg: #f5f4ef;
      --ink: #1a1a1a;
      --muted: #77736b;
      --hair: #d4d2cc;
      --paper-soft: #eeece4;
      --font-main: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      --font-mono: ui-monospace, "SF Mono", Menlo, monospace;
    }
  </style>
  <title>Design Minimal</title>
</head>
<body class="m-0 bg-[var(--bg)] text-[var(--ink)] font-[var(--font-main)] text-[14px] leading-[1.55]">
  <main class="mx-auto w-[1120px] px-8 py-8 pb-20">
    <header class="border-y-2 border-[var(--ink)] py-4">
      <p class="text-[11px] uppercase tracking-[0.14em] text-[var(--muted)]">BRIEF 042 · INTERNAL</p>
      <h1 class="mt-3 text-[28px] leading-tight font-normal">Page Title</h1>
      <p class="mt-2 text-[var(--muted)]">Short one-line description.</p>
    </header>

    <div class="mt-6 grid grid-cols-[1fr_320px] gap-6">
      <section class="border border-[var(--ink)] p-4">
        <div class="text-[10px] uppercase tracking-[0.14em] text-[var(--muted)]">
          [ <span class="bg-[var(--ink)] text-[var(--bg)] px-1">MAIN</span> ] important
        </div>
        <p class="mt-3">...</p>
      </section>
      <aside class="border border-dashed border-[var(--ink)] p-4">
        <div class="text-[10px] uppercase tracking-[0.14em] text-[var(--muted)]">[ SIDE ]</div>
        <p class="mt-3">...</p>
      </aside>
    </div>

    <div class="mt-8 text-[10px] uppercase tracking-[0.14em] text-[var(--muted)]">──── entries ──────────────────────────────</div>

    <article class="mt-5 border-t border-[var(--hair)] pt-5">
      <div class="text-[10px] uppercase tracking-[0.14em] text-[var(--muted)]">[ 01 / 05 ] signal</div>
      <h2 class="mt-2 text-[20px] leading-tight font-normal">Section Title</h2>
      <p class="mt-3">...</p>
    </article>
  </main>
</body>
</html>
```

## Common Mistakes

- Adding component selectors in `<style>` instead of Tailwind classes.
- Adding `sm:` / `md:` / `lg:` classes.
- Adding `@media` for mobile.
- Importing Google Fonts or icon libraries.
- Using rounded corners, shadows, gradients, or color-coded statuses.
- Using English UI labels in a Russian page when a clear Russian label exists.
- Treating any specific layout pattern as mandatory when the content needs another structure.
