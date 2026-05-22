---
name: ui-color-consistency
description: Audits and updates UI components across an app to ensure consistent theming using CSS custom properties and design system colors. Use when updating UI theme, ensuring color consistency, or applying a design system across pages.
---

# UI Color Consistency Skill

This skill helps audit and update UI components to ensure consistent theming across an application using CSS custom properties and a unified design system.

## When to Use This Skill

Use this skill when:
- Updating an app to use a new color theme
- Ensuring color consistency across multiple pages/components
- Migrating from hardcoded colors to CSS custom properties
- Applying a design system to an existing codebase
- Auditing for theme inconsistencies

## Prerequisites

Before starting, you MUST:
1. **Read the main CSS file** (typically `src/index.css` or `styles/globals.css`) to understand the canonical color palette
2. **Identify all CSS custom properties** defined (e.g., `--background`, `--foreground`, `--primary`, `--accent`, etc.)
3. **Document the color palette** with HSL values and their semantic meanings

## Step-by-Step Process

### 1. Read and Document Color Palette

First, locate and read the main CSS file to extract the color system:

```bash
# Common locations:
# - client/src/index.css
# - src/styles/globals.css
# - styles/index.css
```

Document each color variable with:
- HSL values
- Semantic meaning (e.g., "deep warm charcoal background")
- Usage context (backgrounds, text, accents, etc.)

Example color palette documentation:
```
--background: 45 30% 12%         /* Deep warm charcoal - main backgrounds */
--foreground: 40 20% 95%         /* Bright warm white - text */
--primary: 25 95% 58%            /* Bright sunset orange/gold - primary actions */
--secondary: 200 85% 55%         /* Vibrant sky blue - secondary elements */
--accent: 160 80% 50%            /* Electric teal/green - highlights */
--success: 142 85% 55%           /* Bright neon green - success states */
```

### 2. Identify Pages/Components to Audit

Search for all main pages and components that need auditing:

```bash
# Find all page components
find src/pages -name "*.tsx" -o -name "*.jsx"

# Find all components
find src/components -name "*.tsx" -o -name "*.jsx"
```

### 3. Audit Each File for Color Usage

For each file, check for:

#### ❌ Anti-patterns (things to fix):
- **Hardcoded hex colors**: `#1a1a1a`, `#ff6b6b`
- **Hardcoded RGB**: `rgb(26, 26, 26)`
- **Hardcoded HSL**: `hsl(0, 0%, 10%)`
- **Tailwind hardcoded colors**: `bg-gray-900`, `text-blue-500`
- **Inconsistent opacity values**: Random opacity like `bg-card/37`

#### ✅ Correct patterns (what to use):
- **CSS custom properties**: `hsl(var(--background))`, `hsl(var(--primary))`
- **Consistent Tailwind classes**: `bg-background`, `text-foreground`, `border-border`
- **Semantic opacity values**: `bg-background/40`, `text-foreground/60`, `border-foreground/10`
- **Inline styles with CSS variables**:
  ```tsx
  style={{
    background: `linear-gradient(135deg, hsl(var(--primary)), hsl(var(--accent)))`,
    borderColor: 'hsl(var(--primary) / 0.5)'
  }}
  ```

### 4. Common Pattern Library

Apply these consistent patterns across all components:

#### Glass Morphism Cards
```tsx
<div className="bg-background/40 backdrop-blur-xl border border-foreground/10 rounded-3xl shadow-xl">
  {/* content */}
</div>
```

#### Gradient Backgrounds
```tsx
<div
  className="rounded-2xl"
  style={{
    background: 'linear-gradient(135deg, hsl(var(--primary)), hsl(var(--accent)))'
  }}
>
  {/* content */}
</div>
```

#### Gradient Overlays
```tsx
<div className="absolute inset-0 opacity-10 pointer-events-none">
  <div
    className="absolute inset-0"
    style={{
      background: 'linear-gradient(135deg, hsl(var(--primary)), hsl(var(--accent)))'
    }}
  />
</div>
```

#### Progress Bars
```tsx
<div
  className="h-2 rounded-full transition-all duration-500"
  style={{
    width: `${percentage}%`,
    background: 'linear-gradient(90deg, hsl(var(--primary)), hsl(var(--accent)))'
  }}
/>
```

#### Buttons (Primary)
```tsx
<button
  className="px-6 py-3 rounded-2xl font-bold text-white shadow-lg hover:shadow-xl transition-all"
  style={{
    background: 'linear-gradient(135deg, hsl(var(--primary)), hsl(var(--accent)))'
  }}
>
  {/* button text */}
</button>
```

#### Buttons (Secondary/Ghost)
```tsx
<button className="px-4 py-2 rounded-xl bg-background/40 backdrop-blur-md border border-foreground/10 text-foreground hover:bg-background/60 transition-all">
  {/* button text */}
</button>
```

#### Text Hierarchy
```tsx
{/* Primary text */}
<h1 className="text-foreground font-bold">Title</h1>

{/* Secondary text */}
<p className="text-foreground/70">Description</p>

{/* Muted text */}
<span className="text-foreground/50">Meta info</span>
```

#### Badges
```tsx
<div
  className="inline-flex items-center gap-2 px-4 py-2 rounded-full font-bold shadow-md text-sm"
  style={{
    backgroundColor: 'hsl(var(--primary) / 0.15)',
    border: '2px solid hsl(var(--primary) / 0.5)',
    color: 'hsl(var(--primary))'
  }}
>
  {/* badge content */}
</div>
```

### 5. Update Files Systematically

For each file that needs updates:

1. **Read the file** completely first
2. **Identify all color-related code**:
   - Background colors
   - Text colors
   - Border colors
   - Shadow colors
   - Gradient definitions
3. **Replace anti-patterns with correct patterns** from the library above
4. **Verify consistency** with the color palette
5. **Test the changes** visually if possible

### 6. Testing and Verification

After updates:
- [ ] All pages use CSS custom properties instead of hardcoded colors
- [ ] Glass morphism effects are consistent (`bg-background/40 backdrop-blur-xl`)
- [ ] Gradients use the same pattern (`linear-gradient(135deg, hsl(var(--primary)), hsl(var(--accent)))`)
- [ ] Text hierarchy uses consistent opacity levels (100%, 70%, 50%)
- [ ] Borders use consistent opacity (`border-foreground/10`)
- [ ] No hardcoded hex, RGB, or HSL values remain
- [ ] Visual consistency across all pages

## Example Audit Report Format

When completing an audit, provide a report like:

```
## UI Color Consistency Audit Complete

### Color Palette (from index.css)
- --background: 45 30% 12% (deep warm charcoal)
- --foreground: 40 20% 95% (bright warm white)
- --primary: 25 95% 58% (bright sunset orange/gold)
- --accent: 160 80% 50% (electric teal/green)
- --success: 142 85% 55% (bright neon green)

### Files Audited: 4
1. ✅ Goals.tsx - Already perfect
2. 🔧 HabitsMountain.tsx - Updated
3. 🔧 Todos.tsx - Updated
4. 🔧 DreamScrollMountain.tsx - Updated

### Changes Made:

#### HabitsMountain.tsx
- Updated habit color palette from hex to CSS variables
- Weather badge: bg-card/40 → bg-background/40 backdrop-blur-xl
- Progress bars now use CSS variables
- Streak badges use inline styles with proper variables

#### Todos.tsx
- Page header: Added glass card with gradient overlay
- View tabs: Active state uses gradient backgrounds
- Todo cards: Consistent glass morphism styling
- Week view: Replaced hardcoded colors with CSS variables

#### DreamScrollMountain.tsx
- Page header: Enhanced backdrop blur and transparency
- Category tabs: Active state uses gradient backgrounds
- Goal cards: Dynamic gradient overlays with CSS variables
- Tag badges: Consistent styling with CSS variables

### Result:
All pages now use consistent theming with CSS custom properties.
No hardcoded colors remain. Glass morphism and gradients are uniform.
```

## Tips and Best Practices

1. **Always read the CSS file first** - Don't assume the color palette
2. **Use inline styles for gradients** - Tailwind can't handle CSS custom properties in gradients well
3. **Maintain semantic opacity levels** - Use 10%, 40%, 60%, 70% consistently
4. **Keep backdrop-blur consistent** - Use `backdrop-blur-xl` for major cards, `backdrop-blur-md` for smaller elements
5. **Test in both light and dark modes** if applicable
6. **Document any custom patterns** specific to the project

## Common Gotchas

- **Tailwind limitations**: `bg-[hsl(var(--primary))]` doesn't work well - use inline styles for complex colors
- **Opacity syntax**: Use `hsl(var(--primary) / 0.5)` not `hsl(var(--primary), 0.5)`
- **Border gradients**: Can't do gradient borders in Tailwind easily - may need custom CSS
- **Framer Motion**: Animation variants work fine with CSS variables
- **Type safety**: TypeScript may complain about inline styles - this is expected and OK
