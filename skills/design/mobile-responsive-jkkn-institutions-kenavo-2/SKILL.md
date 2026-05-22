---
name: mobile-responsive
description: Comprehensive mobile-first responsive design skill for converting desktop pages to mobile-friendly layouts. Use when implementing mobile views, fixing responsive issues, or batch-converting multiple pages to mobile-responsive. Automates the mobile-view workflow for Next.js/React applications with Tailwind CSS. (project)
---

# Mobile Responsive Skill

## Purpose

This skill provides a systematic, automated approach to implementing mobile-responsive designs across entire applications. Instead of converting pages one-by-one manually, this skill provides batch processing workflows, reusable patterns, and automated checks to rapidly make all pages mobile-friendly.

## When to Use This Skill

Use this skill when:
- **Converting multiple pages to mobile-responsive** - Batch process entire applications
- **Fixing responsive issues** - Debug and fix mobile layout problems
- **Creating new mobile-first pages** - Build pages with mobile-first approach
- **Auditing mobile responsiveness** - Check all pages for mobile issues
- **Implementing bottom navigation** - Add mobile navigation patterns
- **Optimizing touch interactions** - Improve mobile UX

## Quick Start - Batch Mobile Conversion

### Step 1: Audit All Pages

First, scan the application to identify pages needing mobile work:

```bash
# Find all page.tsx files in the app directory
find app -name "page.tsx" -type f
```

### Step 2: Run Mobile Audit

For each page, check:
1. Does it have responsive classes (`sm:`, `md:`, `lg:`)?
2. Does it use fixed widths that break on mobile?
3. Are touch targets at least 44x44px?
4. Does it have mobile navigation?

### Step 3: Apply Mobile Patterns

Use the conversion patterns in `references/conversion-patterns.md`.

## Core Mobile Patterns

### 1. Container Pattern

**Before (Desktop-only)**:
```tsx
<div className="max-w-7xl mx-auto p-8">
```

**After (Mobile-first)**:
```tsx
<div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 sm:py-6 lg:py-8">
```

### 2. Grid Pattern

**Before**:
```tsx
<div className="grid grid-cols-4 gap-6">
```

**After**:
```tsx
<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 sm:gap-6">
```

### 3. Table to Card Pattern

**Before**:
```tsx
<table className="w-full">
  <thead><tr><th>Name</th><th>Email</th><th>Actions</th></tr></thead>
  <tbody>
    <tr><td>John</td><td>john@example.com</td><td>Edit</td></tr>
  </tbody>
</table>
```

**After**:
```tsx
{/* Desktop Table */}
<div className="hidden md:block">
  <table className="w-full">...</table>
</div>

{/* Mobile Cards */}
<div className="md:hidden space-y-4">
  <div className="bg-white rounded-lg p-4 shadow-sm border">
    <div className="flex justify-between items-start mb-2">
      <span className="font-semibold">John</span>
      <button className="p-2">Edit</button>
    </div>
    <p className="text-sm text-gray-600">john@example.com</p>
  </div>
</div>
```

### 4. Form Pattern

**Before**:
```tsx
<div className="flex gap-4">
  <input className="w-64" />
  <button>Submit</button>
</div>
```

**After**:
```tsx
<div className="flex flex-col sm:flex-row gap-3 sm:gap-4">
  <input className="w-full sm:w-64" />
  <button className="w-full sm:w-auto min-h-[44px]">Submit</button>
</div>
```

### 5. Header/Navigation Pattern

**Before**:
```tsx
<header className="flex justify-between items-center p-4">
  <Logo />
  <nav className="flex gap-4">
    <Link>Home</Link>
    <Link>Products</Link>
    <Link>Settings</Link>
  </nav>
</header>
```

**After**:
```tsx
<header className="flex justify-between items-center p-4">
  <Logo />

  {/* Desktop Nav */}
  <nav className="hidden md:flex gap-4">
    <Link>Home</Link>
    <Link>Products</Link>
    <Link>Settings</Link>
  </nav>

  {/* Mobile Menu Button */}
  <button className="md:hidden p-2 min-w-[44px] min-h-[44px]">
    <MenuIcon />
  </button>
</header>

{/* Mobile Bottom Navigation */}
<nav className="md:hidden fixed bottom-0 left-0 right-0 bg-white border-t flex justify-around py-2 z-50">
  <Link className="flex flex-col items-center p-2 min-w-[64px]">
    <HomeIcon className="w-6 h-6" />
    <span className="text-xs">Home</span>
  </Link>
  <Link className="flex flex-col items-center p-2 min-w-[64px]">
    <ProductsIcon className="w-6 h-6" />
    <span className="text-xs">Products</span>
  </Link>
  <Link className="flex flex-col items-center p-2 min-w-[64px]">
    <SettingsIcon className="w-6 h-6" />
    <span className="text-xs">Settings</span>
  </Link>
</nav>

{/* Add padding to main content to prevent bottom nav overlap */}
<main className="pb-20 md:pb-0">
```

### 6. Modal/Dialog Pattern

**Before**:
```tsx
<Dialog className="w-[600px]">
```

**After**:
```tsx
<Dialog className="w-full max-w-[600px] mx-4 sm:mx-auto max-h-[90vh] overflow-y-auto">
```

### 7. Text/Typography Pattern

**Before**:
```tsx
<h1 className="text-4xl">Title</h1>
<p className="text-lg">Description</p>
```

**After**:
```tsx
<h1 className="text-2xl sm:text-3xl lg:text-4xl">Title</h1>
<p className="text-base sm:text-lg">Description</p>
```

### 8. Button Group Pattern

**Before**:
```tsx
<div className="flex gap-2">
  <button>Cancel</button>
  <button>Save</button>
</div>
```

**After**:
```tsx
<div className="flex flex-col-reverse sm:flex-row gap-2 sm:gap-3">
  <button className="w-full sm:w-auto min-h-[44px] px-4 py-2">Cancel</button>
  <button className="w-full sm:w-auto min-h-[44px] px-4 py-2">Save</button>
</div>
```

### 9. Sidebar Layout Pattern

**Before**:
```tsx
<div className="flex">
  <aside className="w-64">Sidebar</aside>
  <main className="flex-1">Content</main>
</div>
```

**After**:
```tsx
<div className="flex flex-col lg:flex-row">
  {/* Mobile: Collapsible sidebar */}
  <aside className="
    lg:w-64 lg:block
    fixed lg:relative inset-y-0 left-0 z-50
    w-64 bg-white shadow-lg lg:shadow-none
    transform -translate-x-full lg:translate-x-0
    transition-transform duration-200 ease-in-out
    data-[open=true]:translate-x-0
  ">
    Sidebar
  </aside>

  {/* Overlay for mobile */}
  <div className="lg:hidden fixed inset-0 bg-black/50 z-40 hidden data-[open=true]:block" />

  <main className="flex-1 min-h-screen lg:ml-0">Content</main>
</div>
```

### 10. Image/Media Pattern

**Before**:
```tsx
<img src="/image.jpg" width={400} height={300} />
```

**After**:
```tsx
<div className="relative w-full aspect-[4/3] sm:w-[400px]">
  <Image
    src="/image.jpg"
    fill
    className="object-cover rounded-lg"
    sizes="(max-width: 640px) 100vw, 400px"
  />
</div>
```

## Batch Conversion Workflow

### Automated Page Scanner

Use this checklist for each page:

```markdown
## Mobile Audit Checklist for: [PAGE_NAME]

### Layout
- [ ] Container has responsive padding (px-4 sm:px-6 lg:px-8)
- [ ] Grids collapse to single column on mobile
- [ ] Sidebars are collapsible on mobile
- [ ] No horizontal scroll on mobile (320px-428px)

### Typography
- [ ] Headings scale down on mobile (text-2xl sm:text-3xl)
- [ ] Body text is readable (min 16px on mobile)
- [ ] Line lengths don't exceed 75 characters

### Navigation
- [ ] Has mobile navigation (hamburger or bottom nav)
- [ ] Desktop nav hidden on mobile (hidden md:flex)
- [ ] Mobile nav visible on mobile (md:hidden)

### Interactive Elements
- [ ] Touch targets minimum 44x44px
- [ ] Buttons stack vertically on mobile
- [ ] Form inputs are full-width on mobile

### Tables
- [ ] Converted to cards on mobile OR
- [ ] Has horizontal scroll wrapper

### Images
- [ ] Responsive sizing with aspect-ratio
- [ ] Proper srcset/sizes attributes

### Modals/Dialogs
- [ ] Full-width with margin on mobile
- [ ] Max-height with scroll
```

## Common CSS Utilities

### Mobile-First Responsive Classes

```tsx
// Visibility
"hidden sm:block"      // Hide on mobile, show on sm+
"block sm:hidden"      // Show on mobile only
"md:hidden"            // Hide on md+

// Flex Direction
"flex-col sm:flex-row" // Stack on mobile, row on sm+

// Width
"w-full sm:w-auto"     // Full width mobile, auto on sm+
"w-full sm:w-1/2 lg:w-1/3" // Responsive widths

// Padding/Margin
"p-4 sm:p-6 lg:p-8"    // Responsive padding
"space-y-4 sm:space-y-6" // Responsive spacing

// Text
"text-sm sm:text-base lg:text-lg" // Responsive text

// Grid
"grid-cols-1 sm:grid-cols-2 lg:grid-cols-3" // Responsive grid
```

### Touch-Friendly Utilities

```tsx
// Minimum touch target
"min-h-[44px] min-w-[44px]"

// Larger tap area
"p-3 -m-3"  // Padding with negative margin

// Touch manipulation
"touch-manipulation"  // Prevents double-tap zoom
```

## Component Templates

### Mobile-Responsive Page Template

```tsx
export default function MobileResponsivePage() {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="sticky top-0 z-40 bg-white border-b">
        <div className="flex items-center justify-between px-4 py-3 sm:px-6">
          <h1 className="text-lg sm:text-xl font-semibold truncate">Page Title</h1>
          <div className="flex items-center gap-2">
            {/* Actions */}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="px-4 py-4 sm:px-6 sm:py-6 lg:px-8 pb-24 md:pb-6">
        <div className="max-w-7xl mx-auto">
          {/* Page content */}
        </div>
      </main>

      {/* Mobile Bottom Navigation */}
      <nav className="md:hidden fixed bottom-0 left-0 right-0 bg-white border-t safe-area-pb">
        <div className="flex justify-around py-2">
          {/* Nav items */}
        </div>
      </nav>
    </div>
  );
}
```

### Mobile-Responsive Data List Template

```tsx
interface DataListProps<T> {
  items: T[];
  renderDesktopRow: (item: T) => React.ReactNode;
  renderMobileCard: (item: T) => React.ReactNode;
  columns: string[];
}

export function ResponsiveDataList<T>({
  items,
  renderDesktopRow,
  renderMobileCard,
  columns
}: DataListProps<T>) {
  return (
    <>
      {/* Desktop Table */}
      <div className="hidden md:block overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gray-50">
            <tr>
              {columns.map(col => (
                <th key={col} className="px-4 py-3 text-left text-sm font-medium">
                  {col}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y">
            {items.map(renderDesktopRow)}
          </tbody>
        </table>
      </div>

      {/* Mobile Cards */}
      <div className="md:hidden space-y-3">
        {items.map(renderMobileCard)}
      </div>
    </>
  );
}
```

## Debugging Mobile Issues

### Common Problems & Solutions

**1. Horizontal scroll on mobile**
```tsx
// Add to parent container
"overflow-x-hidden"
// Or find the element causing overflow and add
"max-w-full overflow-hidden"
```

**2. Text too small on mobile**
```tsx
// Ensure minimum 16px base
"text-base" // 16px minimum
```

**3. Touch targets too small**
```tsx
// Add minimum size
"min-h-[44px] min-w-[44px] p-2"
```

**4. Fixed elements overlapping content**
```tsx
// Add padding to main content
"pb-20 md:pb-0" // For bottom nav
"pt-16" // For fixed header
```

**5. Images breaking layout**
```tsx
// Constrain images
"max-w-full h-auto"
// Or use aspect ratio
"aspect-video w-full"
```

## Best Practices

1. **Always test on real devices** - Simulators miss touch/scroll issues
2. **Use mobile-first approach** - Start with mobile, enhance for desktop
3. **Test at 320px, 375px, 428px** - Common mobile widths
4. **Check landscape orientation** - Often forgotten
5. **Test with keyboard visible** - Forms need proper viewport handling
6. **Use safe-area-inset** - For notched devices
7. **Consider thumb zones** - Important actions should be reachable

## Integration with Other Skills

- **brand-styling**: Use brand colors and spacing
- **ui-ux-designer**: Follow design system patterns
- **nextjs-module-builder**: Apply to new modules

## References

- `references/conversion-patterns.md` - Detailed conversion patterns
- `references/mobile-components.md` - Reusable mobile components
- `references/testing-checklist.md` - Mobile testing checklist
