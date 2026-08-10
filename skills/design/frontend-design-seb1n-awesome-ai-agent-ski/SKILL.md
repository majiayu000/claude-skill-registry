---
name: frontend-design
description: Design and build production-ready frontend interfaces with design systems, responsive layouts, accessible components, and dark mode support. Use when the user requests frontend design or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: AI Agent Skills Community
  version: 1.0.0
---

# Frontend Design

This skill enables the agent to design and implement frontend interfaces that are visually polished, responsive, accessible, and maintainable. The agent works with design systems — component libraries, spacing scales, color tokens, and typography scales — to produce consistent UI code. It outputs production-ready HTML, CSS (including Tailwind CSS), and framework components (React, Vue, Svelte) with WCAG-compliant accessibility and dark mode support built in.

## Workflow

1. **Analyze Requirements and Constraints**: Identify the target platforms (desktop, tablet, mobile), the framework in use (React, Vue, plain HTML), the styling approach (Tailwind, CSS Modules, styled-components), and any existing design tokens or brand guidelines. Determine the key pages or components needed and their priority order.

2. **Establish the Design System Foundation**: Define the core tokens before writing any component code. This includes a spacing scale (4px base: 4, 8, 12, 16, 24, 32, 48, 64), a type scale (xs through 4xl with corresponding line-heights), a color palette with semantic tokens (primary, secondary, success, warning, error, neutral) in both light and dark variants, and border-radius and shadow tokens. These tokens ensure every component is visually consistent.

3. **Build Components with Variants**: Implement each component with clearly defined variants (size, color, state). Use props or CSS classes to control variants rather than duplicating markup. Include all interactive states: default, hover, focus-visible, active, disabled. Ensure every interactive element has a visible focus ring for keyboard navigation.

4. **Implement Responsive Layouts**: Use CSS Grid for two-dimensional page layouts and Flexbox for one-dimensional component alignment. Define breakpoints (sm: 640px, md: 768px, lg: 1024px, xl: 1280px) and design mobile-first, layering complexity at larger breakpoints. Test that no horizontal scrolling occurs and that tap targets meet the 44x44px minimum on touch devices.

5. **Integrate Accessibility from the Start**: Apply semantic HTML elements (nav, main, article, section, aside) before adding ARIA attributes. Ensure color contrast meets WCAG 2.1 AA (4.5:1 for normal text, 3:1 for large text). Add `aria-label`, `aria-describedby`, and `role` attributes only where semantic HTML is insufficient. Test keyboard navigation order with Tab and Shift+Tab.

6. **Add Dark Mode Support**: Implement dark mode using a CSS custom property strategy or Tailwind's `dark:` variant. Swap background, text, and border tokens while preserving sufficient contrast ratios. Avoid pure black (`#000`) backgrounds — use a dark gray (`#0f172a` or `#1e293b`) for reduced eye strain. Ensure images, shadows, and elevation levels adapt appropriately.

## Usage

Provide the agent with a description of the interface you need, including the framework, styling approach, and any existing design tokens. The agent will produce component code with responsive behavior, accessibility attributes, and dark mode support included.

## Examples

### Example 1: React Card Component with Tailwind CSS Variants

**User Request**: "Create a reusable Card component in React with Tailwind CSS. I need default, elevated, and outlined variants, plus support for dark mode."

**Agent Response**:

```jsx
function Card({ variant = 'default', children, className = '' }) {
  const base = 'rounded-lg p-6 transition-colors duration-200';

  const variants = {
    default:
      'bg-white text-gray-900 dark:bg-slate-800 dark:text-gray-100',
    elevated:
      'bg-white text-gray-900 shadow-lg hover:shadow-xl dark:bg-slate-800 dark:text-gray-100 dark:shadow-slate-900/30',
    outlined:
      'bg-transparent text-gray-900 border border-gray-200 dark:text-gray-100 dark:border-slate-700',
  };

  return (
    <div className={`${base} ${variants[variant]} ${className}`}>
      {children}
    </div>
  );
}

function CardHeader({ title, subtitle }) {
  return (
    <div className="mb-4">
      <h3 className="text-lg font-semibold leading-tight">{title}</h3>
      {subtitle && (
        <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
          {subtitle}
        </p>
      )}
    </div>
  );
}

function CardFooter({ children }) {
  return (
    <div className="mt-6 flex items-center gap-3 pt-4 border-t border-gray-100 dark:border-slate-700">
      {children}
    </div>
  );
}
```

**Usage of the component**:
```jsx
<Card variant="elevated">
  <CardHeader title="Monthly Revenue" subtitle="Jan 2026" />
  <p className="text-3xl font-bold">$48,250</p>
  <CardFooter>
    <span className="text-sm text-green-600 dark:text-green-400">+12.5% from last month</span>
  </CardFooter>
</Card>
```

### Example 2: Responsive Dashboard Layout with CSS Grid

**User Request**: "Build a responsive dashboard layout with a sidebar, top nav, and main content area. Sidebar should collapse on mobile."

**Agent Response**:

```html
<div class="dashboard">
  <nav class="dashboard__topbar" role="navigation" aria-label="Primary">
    <button class="sidebar-toggle" aria-label="Toggle sidebar" aria-expanded="false">☰</button>
    <h1 class="topbar-title">Dashboard</h1>
    <div class="topbar-actions"><!-- user avatar, notifications --></div>
  </nav>
  <aside class="dashboard__sidebar" role="navigation" aria-label="Sidebar">
    <ul role="list">
      <li><a href="/overview" aria-current="page">Overview</a></li>
      <li><a href="/analytics">Analytics</a></li>
      <li><a href="/settings">Settings</a></li>
    </ul>
  </aside>
  <main class="dashboard__content" id="main-content" role="main">
    <!-- page content -->
  </main>
</div>
```

```css
.dashboard {
  display: grid;
  grid-template-columns: 1fr;
  grid-template-rows: 56px 1fr;
  min-height: 100vh;
}
.dashboard__topbar { grid-column: 1 / -1; }
.dashboard__sidebar { display: none; }

@media (min-width: 768px) {
  .dashboard {
    grid-template-columns: 240px 1fr;
    grid-template-rows: 56px 1fr;
  }
  .dashboard__sidebar { display: flex; flex-direction: column; }
  .sidebar-toggle { display: none; }
}
```

On screens below 768px the sidebar is hidden and a hamburger toggle button appears in the top bar. On tablet and desktop the sidebar is persistently visible at 240px wide, and the main content fills the remaining space.

## Best Practices

- **Start with semantic HTML before styling**: A `<button>` is always better than a styled `<div onClick>`. Semantic elements provide keyboard handling, screen reader announcements, and form submission behavior for free.
- **Use design tokens, not hard-coded values**: Every color, spacing value, font-size, and shadow should reference a token. This makes theme changes and dark mode a matter of swapping token sets rather than hunting through component files.
- **Design mobile-first, then enhance**: Write base styles for the smallest viewport. Add complexity at larger breakpoints with `min-width` media queries. This prevents desktop assumptions from breaking mobile layouts.
- **Test with a keyboard before shipping**: Navigate every interactive flow using only Tab, Enter, Space, Escape, and arrow keys. If you cannot complete a task without a mouse, the component has an accessibility gap.
- **Keep component APIs minimal**: A component with 15 props is hard to use correctly. Favor composition (children, slots) over configuration (flags, mode strings). Split large components into smaller composable pieces.
- **Measure performance on real devices**: Test on a mid-range Android phone over a throttled connection. Large DOM trees, unoptimized images, and excessive JavaScript bundles cause visible jank on constrained hardware.

## Edge Cases

- **User provides no design tokens or brand guidelines**: Default to a neutral system: Inter or system-ui font stack, a slate gray neutral palette, and a blue primary accent. These are professional and inoffensive while remaining easy to customize later.
- **Content length varies wildly between instances**: Use `min-height` instead of fixed `height`, `text-overflow: ellipsis` with `-webkit-line-clamp` for card descriptions, and test with both a single word and a full paragraph to verify layout stability.
- **Dark mode images look washed out or too bright**: Apply a subtle `brightness(0.9)` filter to photographic images in dark mode. For decorative SVGs, swap fill colors using `currentColor` or CSS custom properties.
- **Right-to-left (RTL) language support required**: Use logical CSS properties (`margin-inline-start` instead of `margin-left`, `padding-inline-end` instead of `padding-right`). Set `dir="rtl"` on the root element and verify layout mirrors correctly.
- **Target framework is unknown or the user wants plain HTML**: Default to semantic HTML with vanilla CSS custom properties. The output can be adopted into any framework without refactoring.
