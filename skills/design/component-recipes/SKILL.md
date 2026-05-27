---
name: component-recipes
description: Tailwind CSS component recipes. Use when building UI components with consistent styling. Provides copy-paste patterns for cards, badges, buttons, modals, inputs, and more.
---

# Component Recipes

## Overview
Ready-to-use Tailwind CSS patterns for demo components.

## Card Recipes

### Basic Card
```tsx
<div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
  {children}
</div>
```

### Clickable Card
```tsx
<button className="w-full text-left bg-white rounded-lg shadow-md p-6 hover:shadow-lg hover:ring-2 hover:ring-brand-primary/20 transition-all focus:outline-none focus:ring-2 focus:ring-brand-primary">
  {children}
</button>
```

### Selected Card
```tsx
<div className="bg-white rounded-lg shadow-md p-6 ring-2 ring-brand-primary">
  {children}
</div>
```

## Badge Recipes

### Severity Badges
```tsx
// Safety Hazard
<span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
  {label}
</span>

// Repair Needed
<span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-orange-100 text-orange-800">
  {label}
</span>

// Maintenance Item
<span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
  {label}
</span>

// Monitor
<span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
  {label}
</span>

// Informational
<span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
  {label}
</span>
```

### Condition Badges
```tsx
// Excellent
<span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
  {label}
</span>

// Good
<span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-lime-100 text-lime-800">
  {label}
</span>

// Fair / Poor (use yellow-100/orange-100)
```

### Badge Sizes
```tsx
// Small
className="px-2 py-0.5 text-xs"

// Medium (default)
className="px-2.5 py-0.5 text-xs"

// Large
className="px-3 py-1 text-sm"
```

## Button Recipes

### Primary Button
```tsx
<button className="px-4 py-2 bg-brand-primary text-white rounded-md font-medium hover:bg-brand-secondary focus:outline-none focus:ring-2 focus:ring-brand-primary focus:ring-offset-2 transition-colors">
  {label}
</button>
```

### Secondary Button
```tsx
<button className="px-4 py-2 bg-white text-neutral-700 border border-neutral-300 rounded-md font-medium hover:bg-neutral-50 focus:outline-none focus:ring-2 focus:ring-brand-primary focus:ring-offset-2 transition-colors">
  {label}
</button>
```

### Ghost Button
```tsx
<button className="px-4 py-2 text-brand-primary rounded-md font-medium hover:bg-brand-primary/10 focus:outline-none focus:ring-2 focus:ring-brand-primary transition-colors">
  {label}
</button>
```

### Icon Button
```tsx
<button className="p-2 text-neutral-500 rounded-md hover:bg-neutral-100 hover:text-neutral-700 focus:outline-none focus:ring-2 focus:ring-brand-primary transition-colors">
  <Icon className="w-5 h-5" />
</button>
```

## Modal Recipes

### Modal Overlay
```tsx
<div className="fixed inset-0 bg-black/50 backdrop-blur-sm" />
```

### Modal Content
```tsx
<div className="fixed inset-0 flex items-center justify-center p-4">
  <div className="bg-white rounded-xl shadow-xl max-w-lg w-full max-h-[90vh] overflow-auto">
    <div className="p-6">
      {children}
    </div>
  </div>
</div>
```

### Modal Header
```tsx
<div className="flex items-center justify-between pb-4 border-b border-neutral-200">
  <h2 className="text-xl font-semibold text-neutral-900">{title}</h2>
  <button className="p-1 text-neutral-400 hover:text-neutral-600 rounded">
    <X className="w-5 h-5" />
  </button>
</div>
```

## Input Recipes

### Text Input
```tsx
<input
  type="text"
  className="w-full px-3 py-2 border border-neutral-300 rounded-md text-neutral-900 placeholder:text-neutral-400 focus:outline-none focus:ring-2 focus:ring-brand-primary focus:border-transparent transition-shadow"
  placeholder="Enter text..."
/>
```

### Input with Error
```tsx
<input
  className="w-full px-3 py-2 border border-red-500 rounded-md text-neutral-900 focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent"
/>
<p className="mt-1 text-sm text-red-600">{errorMessage}</p>
```

## Progress Recipes

### Progress Bar
```tsx
<div className="w-full h-2 bg-neutral-200 rounded-full overflow-hidden">
  <div
    className="h-full bg-brand-primary transition-all duration-500"
    style={{ width: `${percentage}%` }}
  />
</div>
```

### Colored Progress (Condition-based)
```tsx
// className based on condition
const progressColor = {
  excellent: 'bg-green-500',
  good: 'bg-lime-500',
  fair: 'bg-yellow-500',
  poor: 'bg-orange-500',
}[condition];
```

## Layout Recipes

### Page Container
```tsx
<div className="min-h-screen bg-neutral-50">
  <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    {children}
  </div>
</div>
```

### Card Grid
```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
  {items.map(item => <Card key={item.id} {...item} />)}
</div>
```

### Section Header
```tsx
<div className="flex items-center justify-between mb-6">
  <h2 className="text-2xl font-semibold text-neutral-900">{title}</h2>
  <div className="flex items-center gap-2">
    {actions}
  </div>
</div>
```

## Best Practices

- Use semantic color tokens (brand-primary, severity-*, condition-*)
- Maintain consistent spacing (4px grid)
- Include focus states for accessibility
- Use transition classes for smooth interactions

## Anti-Patterns

- NO hardcoded hex colors
- NO inconsistent border-radius
- NO missing focus states
- NO arbitrary spacing values
