---
name: ui-ux-principles
description: Apply core UI/UX design principles for intuitive, beautiful interfaces. Covers visual hierarchy, color theory, typography, spacing systems, Gestalt principles, usability heuristics, and user-centered design. Use for design decisions, layout planning, and creating polished user experiences.
---

# UI/UX Design Principles

Create intuitive, visually appealing interfaces based on proven design principles.

## Instructions

1. **Establish visual hierarchy** - Guide users to important content first
2. **Maintain consistency** - Reuse patterns, colors, and interactions
3. **Provide clear feedback** - Every action should have a visible response
4. **Reduce cognitive load** - Simplify choices and minimize complexity
5. **Design for errors** - Prevent, detect, and help users recover from mistakes

## Visual Hierarchy

### Size & Weight

```
PRIMARY ACTION     -> Largest, boldest, most prominent
Secondary Action   -> Medium size, less visual weight
tertiary action    -> Smallest, subtle styling
```

```tsx
// Clear hierarchy example
<div className="space-y-4">
  <h1 className="text-4xl font-bold text-gray-900">
    Main Headline
  </h1>
  <p className="text-xl text-gray-600">
    Supporting description that explains the headline
  </p>
  <div className="flex gap-4">
    <button className="px-6 py-3 bg-blue-600 text-white font-medium rounded-lg">
      Primary Action
    </button>
    <button className="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg">
      Secondary
    </button>
  </div>
</div>
```

### Spacing Scale

```css
/* Consistent spacing system (4px base) */
--space-1: 0.25rem;  /* 4px - tight spacing */
--space-2: 0.5rem;   /* 8px - related items */
--space-3: 0.75rem;  /* 12px */
--space-4: 1rem;     /* 16px - standard gap */
--space-6: 1.5rem;   /* 24px - section spacing */
--space-8: 2rem;     /* 32px - major sections */
--space-12: 3rem;    /* 48px - page sections */
--space-16: 4rem;    /* 64px - large gaps */
```

## Color Theory

### Color System

```tsx
// Semantic color usage
const colors = {
  // Primary - brand identity, main CTAs
  primary: {
    base: '#2563eb',   // Blue-600
    hover: '#1d4ed8',  // Blue-700
    light: '#dbeafe',  // Blue-100
  },

  // Success - confirmations, positive actions
  success: {
    base: '#16a34a',   // Green-600
    light: '#dcfce7',  // Green-100
  },

  // Warning - caution, non-critical issues
  warning: {
    base: '#d97706',   // Amber-600
    light: '#fef3c7',  // Amber-100
  },

  // Error - errors, destructive actions
  error: {
    base: '#dc2626',   // Red-600
    light: '#fee2e2',  // Red-100
  },

  // Neutral - text, backgrounds, borders
  neutral: {
    900: '#111827',    // Primary text
    700: '#374151',    // Secondary text
    500: '#6b7280',    // Placeholder, disabled
    300: '#d1d5db',    // Borders
    100: '#f3f4f6',    // Backgrounds
  },
};
```

### Color Accessibility

```
Text on white background:
- Gray-900 (#111827) -> Contrast 16:1 (excellent)
- Gray-700 (#374151) -> Contrast 10:1 (excellent)
- Gray-500 (#6b7280) -> Contrast 5.2:1 (minimum for text)
- Gray-400 (#9ca3af) -> Contrast 3.5:1 (fails for body text)

Large text (18pt+) can use 3:1 minimum contrast
```

## Typography

### Type Scale

```css
/* Modular scale (1.25 ratio) */
--text-xs: 0.75rem;    /* 12px */
--text-sm: 0.875rem;   /* 14px */
--text-base: 1rem;     /* 16px - body */
--text-lg: 1.125rem;   /* 18px */
--text-xl: 1.25rem;    /* 20px */
--text-2xl: 1.5rem;    /* 24px */
--text-3xl: 1.875rem;  /* 30px */
--text-4xl: 2.25rem;   /* 36px */
--text-5xl: 3rem;      /* 48px */
```

### Typography Best Practices

```tsx
// Readable line length (45-75 characters)
<article className="max-w-prose mx-auto">
  <h1 className="text-4xl font-bold tracking-tight">
    Headline with Tighter Tracking
  </h1>
  <p className="text-lg leading-relaxed text-gray-600">
    Body text with comfortable line height (1.625-1.75)
    for better readability. Keep paragraphs short.
  </p>
</article>

// Line heights
// Headings: 1.1-1.3 (tight)
// Body: 1.5-1.75 (relaxed)
// Small text: 1.4-1.5
```

## Gestalt Principles

### Proximity

```tsx
// Related items are grouped
<div className="space-y-8">
  {/* Group 1 - User Info */}
  <div className="space-y-2">
    <Input label="First Name" />
    <Input label="Last Name" />
    <Input label="Email" />
  </div>

  {/* Group 2 - Address (clearly separate) */}
  <div className="space-y-2">
    <Input label="Street" />
    <Input label="City" />
    <Input label="ZIP" />
  </div>
</div>
```

### Similarity

```tsx
// Similar items look alike
<div className="flex gap-4">
  {/* All primary actions look the same */}
  <button className="btn-primary">Save</button>
  <button className="btn-primary">Submit</button>

  {/* All secondary actions look the same */}
  <button className="btn-secondary">Cancel</button>
  <button className="btn-secondary">Skip</button>
</div>
```

### Continuity

```tsx
// Elements aligned create visual flow
<nav className="flex items-center space-x-6">
  <Logo />
  <NavLink>Home</NavLink>
  <NavLink>Products</NavLink>
  <NavLink>About</NavLink>
  <NavLink>Contact</NavLink>
</nav>
```

## Usability Heuristics

### 1. Visibility of System Status

```tsx
// Always show what's happening
<button disabled={isLoading}>
  {isLoading ? (
    <>
      <Spinner className="mr-2" />
      Saving...
    </>
  ) : (
    'Save Changes'
  )}
</button>

// Progress indicators
<div className="space-y-2">
  <div className="flex justify-between text-sm">
    <span>Uploading...</span>
    <span>{progress}%</span>
  </div>
  <div className="h-2 bg-gray-200 rounded-full">
    <div
      className="h-2 bg-blue-600 rounded-full transition-all"
      style={{ width: `${progress}%` }}
    />
  </div>
</div>
```

### 2. Match Real World

```tsx
// Use familiar icons and language
<button>
  <TrashIcon /> Delete  {/* Not "Remove instance" */}
</button>

<button>
  <SaveIcon /> Save     {/* Not "Persist changes" */}
</button>
```

### 3. Error Prevention

```tsx
// Confirm destructive actions
<AlertDialog>
  <AlertDialogTrigger asChild>
    <button className="text-red-600">Delete Account</button>
  </AlertDialogTrigger>
  <AlertDialogContent>
    <AlertDialogHeader>
      <AlertDialogTitle>Are you sure?</AlertDialogTitle>
      <AlertDialogDescription>
        This will permanently delete your account and all data.
        This action cannot be undone.
      </AlertDialogDescription>
    </AlertDialogHeader>
    <AlertDialogFooter>
      <AlertDialogCancel>Cancel</AlertDialogCancel>
      <AlertDialogAction className="bg-red-600">
        Yes, delete my account
      </AlertDialogAction>
    </AlertDialogFooter>
  </AlertDialogContent>
</AlertDialog>
```

### 4. Recognition Over Recall

```tsx
// Show options, don't make users remember
<Select>
  <SelectTrigger>
    <SelectValue placeholder="Select a category" />
  </SelectTrigger>
  <SelectContent>
    <SelectItem value="electronics">Electronics</SelectItem>
    <SelectItem value="clothing">Clothing</SelectItem>
    <SelectItem value="books">Books</SelectItem>
  </SelectContent>
</Select>

// Show recent/suggested items
<Combobox>
  <ComboboxInput placeholder="Search..." />
  <ComboboxOptions>
    <div className="text-xs text-gray-500 px-3 py-1">Recent</div>
    {recentItems.map(item => (
      <ComboboxOption key={item.id} value={item} />
    ))}
  </ComboboxOptions>
</Combobox>
```

## Layout Principles

### The Rule of Thirds

```
+---+---+---+
|   | X |   |   Place key elements at intersections
+---+---+---+
|   |   | X |
+---+---+---+
|   |   |   |
+---+---+---+
```

### F-Pattern for Content

```tsx
// Users scan in F pattern - put important content top-left
<div className="grid grid-cols-12 gap-6">
  <header className="col-span-12">
    {/* First scan: full-width header */}
  </header>
  <main className="col-span-8">
    {/* Second scan: main content left */}
  </main>
  <aside className="col-span-4">
    {/* Less important: sidebar right */}
  </aside>
</div>
```

### Z-Pattern for Marketing

```tsx
// Landing pages follow Z pattern
<div>
  <header className="flex justify-between">
    <Logo />                          {/* Top left - brand */}
    <nav>...</nav>                    {/* Top right - navigation */}
  </header>

  <main className="text-center">
    <h1>Main Message</h1>             {/* Diagonal - key content */}
    <p>Supporting content</p>
  </main>

  <footer className="flex justify-between">
    <p>More info</p>                  {/* Bottom left */}
    <button>Call to Action</button>   {/* Bottom right - CTA */}
  </footer>
</div>
```

## Feedback Patterns

### States and Transitions

```tsx
// Interactive element states
<button className="
  /* Default */
  bg-blue-600 text-white

  /* Hover - lighter */
  hover:bg-blue-500

  /* Active/Pressed - darker */
  active:bg-blue-700

  /* Focus - visible ring */
  focus:ring-2 focus:ring-blue-500 focus:ring-offset-2

  /* Disabled - muted */
  disabled:bg-gray-300 disabled:cursor-not-allowed

  /* Transition */
  transition-colors duration-150
">
  Click Me
</button>
```

## When to Use

- Planning UI layouts and component design
- Making design decisions without a designer
- Reviewing and improving existing interfaces
- Creating style guides and design systems
- Onboarding new team members to design principles

## Notes

- These principles apply across all platforms (web, mobile, desktop)
- User testing validates assumptions - principles are guidelines, not rules
- Accessibility is a core principle, not an afterthought
- Performance affects perceived usability
