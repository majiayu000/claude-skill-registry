---
name: tailwind
description: >-
  Tailwind CSS styling for FTC Metrics with official FIRST colors and component patterns.
  Use when styling React components, creating responsive layouts, or implementing dark mode.
license: MIT
compatibility: [Claude Code]
metadata:
  author: ftcmetrics
  version: "1.0.0"
  category: frontend
---

# FTC Metrics Tailwind CSS Styling Guide

This skill provides Tailwind CSS patterns and the FTC branding color palette for the FTC Metrics scouting platform.

## FTC Color Palette

Custom colors defined in `packages/web/tailwind.config.ts`:

```typescript
colors: {
  ftc: {
    orange: "#f57e25",  // Primary brand - buttons, links, accents
    blue: "#0066b3",    // Secondary brand - teleop scores, alt actions
    dark: "#1a1a2e",    // Dark backgrounds
  },
}
```

### Color Usage Patterns

| Element | Light Mode | Dark Mode |
|---------|------------|-----------|
| Primary button | `bg-ftc-orange text-white` | Same |
| Secondary button | `bg-ftc-blue text-white` | Same |
| Accent icon bg | `bg-ftc-orange/10` | Same |
| Accent text | `text-ftc-orange` | Same |
| Positive value | `text-green-500` | Same |
| Negative value | `text-red-500` | Same |

## Dark Mode Configuration

The project uses `prefers-color-scheme` media query for automatic dark mode. CSS variables in `globals.css`:

```css
:root {
  --foreground: #171717;
  --background: #ffffff;
}

@media (prefers-color-scheme: dark) {
  :root {
    --foreground: #ededed;
    --background: #0a0a0a;
  }
}
```

### Dark Mode Class Pattern

Always pair light and dark variants:

```jsx
// Backgrounds
className="bg-white dark:bg-gray-900"
className="bg-gray-50 dark:bg-gray-950"
className="bg-gray-100 dark:bg-gray-800"

// Text
className="text-gray-600 dark:text-gray-400"
className="text-gray-700 dark:text-gray-200"

// Borders
className="border-gray-200 dark:border-gray-800"
className="border-gray-300 dark:border-gray-700"

// Hover states
className="hover:bg-gray-100 dark:hover:bg-gray-800"
```

## Responsive Breakpoints

Standard Tailwind breakpoints used in the project:

| Breakpoint | Min Width | Usage |
|------------|-----------|-------|
| `sm:` | 640px | Padding adjustments |
| `md:` | 768px | 2-3 column grids, nav visibility |
| `lg:` | 1024px | 4 column grids, larger padding |

### Common Responsive Patterns

```jsx
// Container with responsive padding
className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"

// Responsive grid
className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4"
className="grid grid-cols-2 md:grid-cols-4 gap-4"
className="grid gap-6 md:grid-cols-2"
className="grid gap-4 md:grid-cols-3"

// Hide on mobile, show on desktop
className="hidden md:flex"

// Responsive text
className="text-2xl font-bold" // Same across breakpoints (common pattern)
```

## Component Patterns

### Card Component

```jsx
<div className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 p-6">
  {/* Card content */}
</div>
```

With hover state for clickable cards:

```jsx
<Link className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 p-6 hover:border-ftc-orange dark:hover:border-ftc-orange transition-colors">
```

### Page Layout

```jsx
<div className="min-h-screen bg-gray-50 dark:bg-gray-950">
  <Header />
  <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    {children}
  </main>
</div>
```

### Page Header

```jsx
<div className="mb-8">
  <h1 className="text-2xl font-bold">Page Title</h1>
  <p className="text-gray-600 dark:text-gray-400 mt-1">
    Description text
  </p>
</div>
```

### Primary Button

```jsx
<button className="px-4 py-2 bg-ftc-orange text-white rounded-lg font-medium hover:opacity-90 transition-opacity disabled:opacity-50">
  Button Text
</button>

// Full width variant
<button className="w-full py-4 bg-ftc-orange text-white rounded-xl font-medium hover:opacity-90 transition-opacity disabled:opacity-50 text-lg">
```

### Secondary Button

```jsx
<button className="px-4 py-2 bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-white rounded-lg font-medium hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors">
```

### Ghost/Outline Button

```jsx
<button className="px-8 py-4 border border-gray-300 dark:border-gray-700 rounded-lg font-semibold text-lg hover:bg-gray-100 dark:hover:bg-gray-900 transition-colors">
```

### Form Input

```jsx
<input
  className="w-full px-4 py-2 bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-ftc-orange focus:border-transparent"
/>
```

### Select Dropdown

```jsx
<select className="w-full px-4 py-3 bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-ftc-orange">
```

### Tab Buttons

```jsx
<button
  className={`px-4 py-2 rounded-lg font-medium transition-colors ${
    isActive
      ? "bg-ftc-orange text-white"
      : "bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700"
  }`}
>
```

### Toggle Button (Two Options)

```jsx
<div className="flex gap-2">
  <button
    className={`flex-1 py-2 rounded-lg font-medium transition-colors ${
      selected === "A"
        ? "bg-red-500 text-white"
        : "bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-300"
    }`}
  >
    Option A
  </button>
  <button
    className={`flex-1 py-2 rounded-lg font-medium transition-colors ${
      selected === "B"
        ? "bg-blue-500 text-white"
        : "bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-300"
    }`}
  >
    Option B
  </button>
</div>
```

### Toggle Switch

```jsx
<button
  className={`w-12 h-7 rounded-full transition-colors ${
    enabled ? "bg-ftc-orange" : "bg-gray-300 dark:bg-gray-600"
  }`}
>
  <div
    className={`w-5 h-5 bg-white rounded-full transition-transform mx-1 ${
      enabled ? "translate-x-5" : ""
    }`}
  />
</button>
```

### Icon Container

```jsx
// For feature icons
<div className="w-16 h-16 bg-ftc-orange/10 rounded-2xl flex items-center justify-center mx-auto mb-4">
  <svg className="w-8 h-8 text-ftc-orange" />
</div>

// For smaller action icons
<div className="w-12 h-12 bg-ftc-orange/10 rounded-lg flex items-center justify-center">
  <svg className="w-6 h-6 text-ftc-orange" />
</div>
```

### Counter Control

```jsx
<div className="flex items-center gap-3">
  <button className="w-10 h-10 bg-gray-200 dark:bg-gray-700 rounded-lg flex items-center justify-center text-xl font-bold hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors">
    -
  </button>
  <span className="w-8 text-center text-xl font-bold">{count}</span>
  <button className="w-10 h-10 bg-ftc-orange text-white rounded-lg flex items-center justify-center text-xl font-bold hover:opacity-90 transition-opacity">
    +
  </button>
</div>
```

### Alert/Notice Box

```jsx
// Success
<div className="p-4 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg text-green-600 dark:text-green-400">
  Success message
</div>

// Error
<div className="p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg text-red-600 dark:text-red-400">
  Error message
</div>
```

### Loading Spinner

```jsx
<div className="animate-spin rounded-full h-8 w-8 border-2 border-ftc-orange border-t-transparent" />
```

### Skeleton Loading

```jsx
<div className="h-12 bg-gray-100 dark:bg-gray-800 rounded-lg animate-pulse" />
```

### Status Badge/Pill

```jsx
// Role badges
<span className="px-3 py-1 rounded-full text-sm font-medium bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300">
  Admin
</span>

// Status indicators
<span className="px-3 py-1 rounded-full text-xs bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300">
  Public
</span>
```

### Data Table

```jsx
<div className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 overflow-hidden">
  <div className="overflow-x-auto">
    <table className="w-full">
      <thead className="bg-gray-50 dark:bg-gray-800">
        <tr>
          <th className="px-4 py-3 text-left text-sm font-medium text-gray-600 dark:text-gray-300">
            Column
          </th>
        </tr>
      </thead>
      <tbody className="divide-y divide-gray-200 dark:divide-gray-800">
        <tr className="hover:bg-gray-50 dark:hover:bg-gray-800/50">
          <td className="px-4 py-3 text-sm">Data</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>
```

### Gradient Banner

```jsx
<div className="bg-gradient-to-r from-ftc-orange to-ftc-blue rounded-2xl p-8 text-white text-center">
  <h2 className="text-3xl font-bold mb-2">Title</h2>
  <p className="text-white/80 text-lg">Subtitle text</p>
</div>
```

### Stat Card

```jsx
<div className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 p-4 text-center">
  <p className="text-2xl font-bold text-ftc-orange">{value}</p>
  <p className="text-sm text-gray-600 dark:text-gray-400">Label</p>
</div>
```

### Empty State

```jsx
<div className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 p-12 text-center">
  <svg className="w-16 h-16 mx-auto mb-4 text-gray-300 dark:text-gray-600" />
  <h3 className="text-lg font-semibold mb-2">No data</h3>
  <p className="text-gray-600 dark:text-gray-400 mb-6">Description</p>
  <button className="px-4 py-2 bg-ftc-orange text-white rounded-lg">
    Action
  </button>
</div>
```

### Back Link

```jsx
<Link
  href="/previous"
  className="text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white flex items-center gap-2 mb-4"
>
  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
  </svg>
  Back
</Link>
```

### Navigation Link

```jsx
<Link className="text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition-colors">
  Nav Item
</Link>
```

### Dropdown Menu

```jsx
<div className="absolute right-0 mt-2 w-56 bg-white dark:bg-gray-900 rounded-lg shadow-lg border border-gray-200 dark:border-gray-800 py-1 z-20">
  <div className="px-4 py-2 border-b border-gray-200 dark:border-gray-800">
    <p className="font-medium truncate">Title</p>
    <p className="text-sm text-gray-500 dark:text-gray-400 truncate">Subtitle</p>
  </div>
  <button className="block w-full text-left px-4 py-2 text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-800">
    Menu Item
  </button>
</div>
```

## Typography Scale

| Element | Classes |
|---------|---------|
| Page title | `text-2xl font-bold` or `text-5xl font-bold tracking-tight` (hero) |
| Section title | `text-lg font-semibold` |
| Card title | `font-semibold text-lg` |
| Body text | Default or `text-sm` |
| Label | `text-sm font-medium` |
| Helper text | `text-sm text-gray-500 dark:text-gray-400` |
| Tiny text | `text-xs text-gray-500` |

## Spacing Conventions

- Page padding: `py-8` for main content
- Section margin: `mb-8` for page sections, `mb-6` for cards
- Card padding: `p-6` standard, `p-4` for compact, `p-8` or `p-12` for empty states
- Grid gap: `gap-4` standard, `gap-6` for larger cards
- Element spacing: `space-y-4` for form fields, `space-y-2` for lists

## Transition Classes

Always include transitions for interactive elements:

- Color changes: `transition-colors`
- Opacity changes: `transition-opacity`
- Transform changes: `transition-transform`

## Font Family

System font stack defined in `globals.css`:

```css
font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
  "Helvetica Neue", Arial, sans-serif;
```

Use `font-mono` for numeric data displays (scores, statistics).
