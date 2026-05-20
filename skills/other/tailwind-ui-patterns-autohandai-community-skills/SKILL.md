---
name: tailwind-ui-patterns
description: Tailwind CSS v4 patterns, component styling, and responsive design
license: MIT
compatibility: tailwindcss 4+, react 18+, vite 6+
allowed-tools: read_file write_file apply_patch search_with_context
---

# Tailwind UI Patterns

## Tailwind v4 Setup

```css
/* app.css */
@import "tailwindcss";

/* Custom theme tokens */
@theme {
  --color-brand-50: oklch(0.97 0.01 250);
  --color-brand-500: oklch(0.55 0.15 250);
  --color-brand-900: oklch(0.25 0.08 250);

  --font-display: "Cal Sans", system-ui, sans-serif;
  --spacing-18: 4.5rem;
}
```

## Component Patterns

### Button Variants
```tsx
const buttonVariants = {
  base: "inline-flex items-center justify-center font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
  variant: {
    primary: "bg-brand-500 text-white hover:bg-brand-600 focus-visible:ring-brand-500",
    secondary: "bg-gray-100 text-gray-900 hover:bg-gray-200 focus-visible:ring-gray-500",
    outline: "border border-gray-300 bg-transparent hover:bg-gray-50 focus-visible:ring-gray-500",
    ghost: "hover:bg-gray-100 focus-visible:ring-gray-500",
    destructive: "bg-red-500 text-white hover:bg-red-600 focus-visible:ring-red-500",
  },
  size: {
    sm: "h-8 px-3 text-sm rounded-md",
    md: "h-10 px-4 text-sm rounded-lg",
    lg: "h-12 px-6 text-base rounded-lg",
    icon: "h-10 w-10 rounded-lg",
  },
};

function Button({ variant = "primary", size = "md", className, ...props }) {
  return (
    <button
      className={cn(
        buttonVariants.base,
        buttonVariants.variant[variant],
        buttonVariants.size[size],
        className
      )}
      {...props}
    />
  );
}
```

### Card Component
```tsx
function Card({ className, ...props }) {
  return (
    <div
      className={cn(
        "rounded-xl border border-gray-200 bg-white shadow-sm",
        "dark:border-gray-800 dark:bg-gray-950",
        className
      )}
      {...props}
    />
  );
}

function CardHeader({ className, ...props }) {
  return <div className={cn("p-6 pb-4", className)} {...props} />;
}

function CardContent({ className, ...props }) {
  return <div className={cn("p-6 pt-0", className)} {...props} />;
}

function CardFooter({ className, ...props }) {
  return (
    <div
      className={cn("flex items-center p-6 pt-0", className)}
      {...props}
    />
  );
}
```

### Input with Label
```tsx
function FormField({ label, error, children, className }) {
  return (
    <div className={cn("space-y-2", className)}>
      <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
        {label}
      </label>
      {children}
      {error && (
        <p className="text-sm text-red-500">{error}</p>
      )}
    </div>
  );
}

function Input({ className, ...props }) {
  return (
    <input
      className={cn(
        "flex h-10 w-full rounded-lg border border-gray-300 bg-white px-3 py-2",
        "text-sm placeholder:text-gray-400",
        "focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-transparent",
        "disabled:cursor-not-allowed disabled:opacity-50",
        "dark:border-gray-700 dark:bg-gray-900",
        className
      )}
      {...props}
    />
  );
}
```

## Responsive Patterns

### Mobile-First Grid
```tsx
<div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
  {items.map(item => <Card key={item.id} {...item} />)}
</div>
```

### Responsive Typography
```tsx
<h1 className="text-2xl font-bold sm:text-3xl lg:text-4xl xl:text-5xl">
  Responsive Heading
</h1>

<p className="text-sm sm:text-base lg:text-lg leading-relaxed">
  Body text that scales appropriately
</p>
```

### Container Queries
```tsx
<div className="@container">
  <div className="flex flex-col @md:flex-row @md:items-center gap-4">
    <img className="w-full @md:w-48 rounded-lg" src={image} alt="" />
    <div className="flex-1">
      <h3 className="text-lg @lg:text-xl font-semibold">{title}</h3>
      <p className="text-gray-600 @lg:text-lg">{description}</p>
    </div>
  </div>
</div>
```

## Animation Patterns

### Transitions
```tsx
// Hover transition
<button className="transition-colors duration-200 hover:bg-gray-100">
  Hover me
</button>

// Scale on hover
<div className="transition-transform duration-200 hover:scale-105">
  Card
</div>

// Combined transitions
<a className="transition-all duration-200 hover:text-brand-500 hover:translate-x-1">
  Link with arrow →
</a>
```

### Keyframe Animations
```css
@theme {
  --animate-fade-in: fade-in 0.3s ease-out;
  --animate-slide-up: slide-up 0.3s ease-out;
  --animate-spin-slow: spin 3s linear infinite;
}

@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slide-up {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
```

```tsx
<div className="animate-fade-in">Fading content</div>
<div className="animate-slide-up">Sliding content</div>
```

## Dark Mode

```tsx
// Toggle component
<div className="bg-white dark:bg-gray-900">
  <h1 className="text-gray-900 dark:text-gray-100">
    Adaptive heading
  </h1>
  <p className="text-gray-600 dark:text-gray-400">
    Adaptive text
  </p>
</div>

// Using CSS variables for theming
@theme {
  --color-surface: white;
  --color-on-surface: #111827;
}

@media (prefers-color-scheme: dark) {
  @theme {
    --color-surface: #111827;
    --color-on-surface: #f9fafb;
  }
}
```

## Layout Patterns

### Sticky Header
```tsx
<header className="sticky top-0 z-50 w-full border-b bg-white/80 backdrop-blur-sm">
  <nav className="container mx-auto flex h-16 items-center px-4">
    {/* Nav content */}
  </nav>
</header>
```

### Sidebar Layout
```tsx
<div className="flex min-h-screen">
  <aside className="hidden w-64 border-r bg-gray-50 lg:block">
    {/* Sidebar */}
  </aside>
  <main className="flex-1 p-6">
    {/* Main content */}
  </main>
</div>
```

### Centered Max-Width Content
```tsx
<main className="mx-auto max-w-3xl px-4 py-8 sm:px-6 lg:px-8">
  {/* Content */}
</main>
```

## Best Practices

1. **Use design tokens** via @theme for consistency
2. **Mobile-first** - start with mobile, add breakpoints up
3. **Compose with cn()** - merge classes cleanly
4. **Extract components** when patterns repeat 3+ times
5. **Use semantic colors** (brand, surface, error) over raw values
6. **Prefer utilities** over custom CSS when possible
7. **Group related utilities** logically for readability
