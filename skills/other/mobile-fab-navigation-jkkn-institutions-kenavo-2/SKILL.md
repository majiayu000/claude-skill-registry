---
name: mobile-fab-navigation
description: Complete workflow for implementing mobile bottom navigation with FAB (Floating Action Button) for Next.js/React applications. Use when creating mobile-responsive navigation with bottom nav bar, FAB menu, active state indicators, and glassmorphism styling. Supports customizable nav items, expandable FAB menus, and proper hydration handling.
---

# Mobile FAB Navigation Builder

Build production-ready mobile bottom navigation with FAB button following modern UI patterns for Next.js and React applications.

## Architecture Overview

The mobile navigation system consists of 3 main parts:

1. **Bottom Navigation Bar** - Fixed bar with 4 primary nav items
2. **FAB Button** - Floating action button for secondary actions
3. **FAB Menu** - Expandable menu triggered by FAB

## Quick Start

To implement mobile FAB navigation:

1. Copy the template from `assets/MobileBottomNav.tsx`
2. Customize `navItems` array with your routes
3. Customize `fabMenuItems` array with secondary actions
4. Import and add component to your layout
5. Adjust colors to match your brand

## Component Structure

```
components/
└── MobileBottomNav.tsx    # Main component (copy from assets/)
```

## Implementation Guide

### Step 1: Create the Component

Copy the template from `assets/MobileBottomNav.tsx` to your `components/` folder.

### Step 2: Configure Navigation Items

Edit the `navItems` array:

```typescript
const navItems = [
  { href: '/', icon: Home, label: 'Home' },
  { href: '/products', icon: Package, label: 'Products' },
  { href: '/cart', icon: ShoppingCart, label: 'Cart' },
  { href: '/profile', icon: User, label: 'Profile' },
];
```

**Rules:**
- Maximum 4 items for optimal UX
- Use Lucide React icons
- Keep labels short (1 word preferred)

### Step 3: Configure FAB Menu Items

Edit the `fabMenuItems` array for secondary navigation:

```typescript
const fabMenuItems = [
  { href: '/settings', icon: Settings, label: 'Settings' },
  { href: '/help', icon: HelpCircle, label: 'Help' },
  { href: '/about', icon: Info, label: 'About' },
];
```

### Step 4: Add to Layout

In your root layout or app layout:

```typescript
import MobileBottomNav from '@/components/MobileBottomNav';

export default function Layout({ children }) {
  return (
    <>
      {children}
      <MobileBottomNav />
    </>
  );
}
```

### Step 5: Add Bottom Padding

Add padding to main content to prevent overlap:

```typescript
<main className="pb-20 lg:pb-0">
  {children}
</main>
```

## Customization Options

### Color Themes

**Default (Purple/Pink):**
```css
/* Nav bar gradient */
from-[rgba(78,46,140,0.85)] to-[rgba(108,66,160,0.75)]

/* FAB button */
from-[rgba(217,81,100,1)] to-[rgba(217,81,100,0.8)]

/* Active pill */
bg-[rgba(50,30,90,0.8)]
```

**Blue Theme:**
```css
/* Nav bar gradient */
from-[rgba(37,99,235,0.85)] to-[rgba(59,130,246,0.75)]

/* FAB button */
from-[rgba(234,88,12,1)] to-[rgba(234,88,12,0.8)]

/* Active pill */
bg-[rgba(30,58,138,0.8)]
```

**Dark Theme:**
```css
/* Nav bar gradient */
from-[rgba(24,24,27,0.95)] to-[rgba(39,39,42,0.9)]

/* FAB button */
from-[rgba(139,92,246,1)] to-[rgba(139,92,246,0.8)]

/* Active pill */
bg-[rgba(63,63,70,0.9)]
```

### Size Adjustments

**Compact (default):**
- Nav bar height: `h-10`
- Icon size: `size={16}`
- FAB size: `w-10 h-10`

**Standard:**
- Nav bar height: `h-14`
- Icon size: `size={20}`
- FAB size: `w-12 h-12`

**Large:**
- Nav bar height: `h-16`
- Icon size: `size={24}`
- FAB size: `w-14 h-14`

## Key Features

### 1. Hydration-Safe Rendering

The component handles SSR/hydration properly:

```typescript
const [isMounted, setIsMounted] = useState(false);

useEffect(() => {
  setIsMounted(true);
}, []);

if (!isMounted) return null;
```

### 2. Active State Detection

Smart path matching for nested routes:

```typescript
const isActive = (href: string) => {
  if (href === '/') return pathname === '/';
  return pathname.startsWith(href);
};
```

### 3. Glassmorphism Styling

Modern glass effect with:
- `backdrop-blur-xl`
- Semi-transparent backgrounds
- Border with `border-white/20`
- Drop shadows

### 4. Responsive Visibility

Desktop hiding with `lg:hidden`:
```typescript
<nav className="... lg:hidden z-50">
```

### 5. Accessibility

Built-in ARIA labels:
```typescript
role="navigation"
aria-label="Mobile navigation"
aria-label="More options"
```

## Common Patterns

### Pattern A: E-commerce App

```typescript
const navItems = [
  { href: '/', icon: Home, label: 'Home' },
  { href: '/shop', icon: Store, label: 'Shop' },
  { href: '/cart', icon: ShoppingCart, label: 'Cart' },
  { href: '/account', icon: User, label: 'Account' },
];

const fabMenuItems = [
  { href: '/wishlist', icon: Heart, label: 'Wishlist' },
  { href: '/orders', icon: Package, label: 'Orders' },
  { href: '/support', icon: HeadphonesIcon, label: 'Support' },
];
```

### Pattern B: Social App

```typescript
const navItems = [
  { href: '/', icon: Home, label: 'Feed' },
  { href: '/search', icon: Search, label: 'Search' },
  { href: '/notifications', icon: Bell, label: 'Alerts' },
  { href: '/profile', icon: User, label: 'Profile' },
];

const fabMenuItems = [
  { href: '/create', icon: PlusCircle, label: 'Create Post' },
  { href: '/messages', icon: MessageCircle, label: 'Messages' },
  { href: '/settings', icon: Settings, label: 'Settings' },
];
```

### Pattern C: Content/Blog App

```typescript
const navItems = [
  { href: '/', icon: Home, label: 'Home' },
  { href: '/articles', icon: FileText, label: 'Articles' },
  { href: '/bookmarks', icon: Bookmark, label: 'Saved' },
  { href: '/profile', icon: User, label: 'Profile' },
];

const fabMenuItems = [
  { href: '/write', icon: Edit, label: 'Write' },
  { href: '/topics', icon: Hash, label: 'Topics' },
  { href: '/about', icon: Info, label: 'About' },
];
```

### Pattern D: Directory/Alumni App (Kenavo Style)

```typescript
const navItems = [
  { href: '/', icon: Home, label: 'Home' },
  { href: '/directory', icon: Users, label: 'Directory' },
  { href: '/gallery', icon: Image, label: 'Gallery' },
  { href: '/contact', icon: Mail, label: 'Contact' },
];

const fabMenuItems = [
  { href: '/about', icon: Info, label: 'About' },
];
```

## Troubleshooting

### Issue: Hydration Mismatch

**Solution:** Ensure `isMounted` check is implemented and returns `null` during SSR.

### Issue: Navigation Not Visible

**Solution:** Check `z-index` values. Nav should be `z-50`. Ensure no parent has `overflow: hidden`.

### Issue: Content Hidden Behind Nav

**Solution:** Add `pb-20` (or appropriate padding) to main content container for mobile.

### Issue: FAB Menu Not Closing

**Solution:** Ensure backdrop click handler calls `setShowMenu(false)` and FAB menu has `onClick={(e) => e.stopPropagation()}`.

## Dependencies

- Next.js 13+ (App Router)
- React 18+
- Tailwind CSS 3+
- Lucide React icons

Install Lucide if not present:
```bash
npm install lucide-react
```

## Mobile Responsive Pages

When implementing pages with mobile FAB navigation, ensure responsive design:

### Essential Rules

1. **Bottom padding** - Add `pb-20 lg:pb-0` to main content
2. **Container** - Use `container mx-auto px-4 sm:px-6 lg:px-8`
3. **Grid** - Use responsive grids: `grid-cols-1 sm:grid-cols-2 lg:grid-cols-3`
4. **Typography** - Scale text: `text-sm sm:text-base lg:text-lg`
5. **Spacing** - Responsive gaps: `gap-3 sm:gap-4 lg:gap-6`

### Page Template

```typescript
export default function Page() {
  return (
    <main className="min-h-screen pb-20 lg:pb-0">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8 lg:py-12">
        {/* Hero - responsive height */}
        <section className="h-[50vh] sm:h-[60vh] lg:h-[70vh]">
          ...
        </section>

        {/* Grid - responsive columns */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
          {items.map(item => <Card key={item.id} />)}
        </div>
      </div>
    </main>
  );
}
```

**Detailed patterns:** See `references/responsive-layouts.md`

## Reference Files

- `assets/MobileBottomNav.tsx` - Complete ready-to-use component template
- `references/styling-guide.md` - Detailed styling customization options
- `references/animation-patterns.md` - Animation and transition configurations
- `references/responsive-layouts.md` - Mobile responsive page layouts and patterns
