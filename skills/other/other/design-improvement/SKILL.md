---
name: design-improvement
description: |
  Systematic design optimization for young-personal-site following established design principles.
  Ensures consistent color palette, responsive layout, and professional appearance.
activation-keywords: [設計, design, UI, UX, 很醜, 不好看, 排版, layout, 顏色, color, 間距, spacing]
priority: high
allowed-tools: [Read, Edit, Write, Bash, Grep, Glob]
---

# Design Improvement Skill

## Purpose
Streamline design optimization with systematic improvements following project design principles.

**Prevents**: Inconsistent design, broken responsive layouts, brand violations
**Ensures**: Color palette consistency, mobile-first responsive design, professional appearance

---

## Design Principles

### Color Palette
```css
Primary:    slate-blue (#475569, #64748b)
Accent:     coral-orange (#fb923c, #f97316)
Background: warm-cream (#fef3c7, #fef9c3)
Gradients:  Smooth transitions for visual interest
```

### Typography
```
Hierarchy: h1 > h2 > h3 > p (clear distinction)
Body text: 16px+ for readability
Line-height: Consistent spacing
Hero sections: Center-aligned
```

### Layout
```
Approach: Mobile-first responsive
Spacing: Tailwind utilities (p-4, gap-6, etc.)
Animations: Framer Motion (smooth, not jarring)
```

---

## Workflow

### 1. Analyze Current Design

```markdown
Issues Checklist:
- [ ] Color consistency problems?
- [ ] Layout/alignment issues?
- [ ] Typography hierarchy unclear?
- [ ] Spacing inconsistent?
- [ ] Responsive breakpoints broken?
- [ ] Animations missing/excessive?
```

### 2. Propose Improvements (CARIO)

```yaml
📋 Context:
  - Page: [Home/Projects/About/Speaking]
  - Current state: [description]
  - Issue: [what looks bad]

❓ Problems:
  1. [Color inconsistency]
  2. [Poor spacing]
  3. [Weak hierarchy]

🎯 Options:
  A. Minor tweaks (15 min, low impact)
  B. Moderate redesign (30-45 min, medium impact)
  C. Major overhaul (1-2 hours, high impact)

💡 Recommendation: [Option B]
  - Changes: [color X→Y, spacing p-4→p-6, add gradient]
  - Reasoning: [balances improvement vs time]

⚡ Impact:
  - Files: [list]
  - Testing: [responsive + visual]
```

### 3. Get User Confirmation

```
Identified [N] design improvements for [Page] page:
1. [Change 1]
2. [Change 2]
3. [Change 3]

Proceed with these improvements?
```

### 4. Implement Changes

**Checklist**:
- [ ] Update Tailwind classes
- [ ] Ensure responsive (sm:, md:, lg: breakpoints)
- [ ] Add/update Framer Motion animations
- [ ] Maintain color palette
- [ ] Follow typography hierarchy

**Example**:
```tsx
// Before
<div className="p-4 bg-white">
  <h1 className="text-2xl">Title</h1>
</div>

// After
<div className="p-6 md:p-8 bg-gradient-to-br from-warm-cream to-white">
  <h1 className="text-3xl md:text-4xl font-bold text-slate-700 text-center mb-6">
    Title
  </h1>
</div>
```

### 5. Test Responsive Design

```bash
npm run dev
# Test at: Mobile (375px), Tablet (768px), Desktop (1280px)
```

**Visual checklist**:
- [ ] Mobile (< 640px): Readable, no overflow
- [ ] Tablet (640-1024px): Proper spacing
- [ ] Desktop (> 1024px): Optimal layout
- [ ] Animations: Smooth (60fps)

### 6. Commit and Deploy

```bash
npm run build  # Verify
git add .
git commit -m "style: improve [page] design with better spacing and colors"
git push  # Auto-deploys to Vercel
```

---

## Common Improvements

### Hero Section Enhancement
```tsx
// Before: Basic section
<section className="py-12">
  <h1 className="text-3xl">Welcome</h1>
</section>

// After: Enhanced with gradient + animation
<section className="py-16 md:py-24 bg-gradient-to-br from-warm-cream via-white to-blue-50">
  <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
    <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold bg-gradient-to-r from-slate-600 to-slate-800 bg-clip-text text-transparent mb-6">
      Welcome
    </h1>
  </motion.div>
</section>
```

### Card Grid Optimization
```tsx
// Before: Fixed 3-column grid
<div className="grid grid-cols-3 gap-4">
  {projects.map(p => <Card {...p} />)}
</div>

// After: Responsive grid with hover animation
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 md:gap-8">
  {projects.map(p => (
    <motion.div whileHover={{ scale: 1.03 }}>
      <Card {...p} />
    </motion.div>
  ))}
</div>
```

### Typography Hierarchy
```tsx
// Before: Flat hierarchy
<h1>Title</h1>
<p>Body text</p>

// After: Clear hierarchy
<h1 className="text-4xl md:text-5xl font-bold text-slate-800 mb-4 leading-tight">
  Title
</h1>
<p className="text-base md:text-lg text-slate-600 leading-relaxed max-w-prose">
  Body text
</p>
```

---

## Quality Checklist

**Before committing**:

```markdown
Visual:
- [ ] Colors match palette (slate-blue, coral-orange, warm-cream)
- [ ] Spacing consistent (4px increments: p-4, p-6, p-8)
- [ ] Typography hierarchy clear
- [ ] Contrast WCAG AA (4.5:1 for text)

Responsive:
- [ ] Mobile (< 640px): Works
- [ ] Tablet (640-1024px): Optimized
- [ ] Desktop (> 1024px): Polished
- [ ] No horizontal scroll
- [ ] Touch targets ≥ 44px (mobile)

Performance:
- [ ] Animations smooth (60fps)
- [ ] No layout shift (CLS < 0.1)
- [ ] Next.js Image component used

Consistency:
- [ ] Matches existing pages' style
- [ ] Follows Tailwind conventions
- [ ] Framer Motion patterns consistent
- [ ] Bilingual support maintained
```

---

## Anti-Patterns

### ❌ Breaking Responsive
```tsx
// Bad: Fixed width
<div className="w-[1200px]">Content</div>

// Good: Responsive width
<div className="w-full max-w-7xl mx-auto px-4">Content</div>
```

### ❌ Inconsistent Colors
```tsx
// Bad: Random colors
<div className="bg-red-500 text-purple-700">Content</div>

// Good: Follow palette
<div className="bg-warm-cream text-slate-700">Content</div>
```

### ❌ Poor Typography
```tsx
// Bad: Unreadable
<p className="text-xs">Important content</p>

// Good: Readable
<p className="text-base md:text-lg">Important content</p>
```

---

## Quick Reference

### Spacing Scale
```
p-4  = 16px   p-8  = 32px
p-6  = 24px   p-12 = 48px
```

### Typography Scale
```
text-base = 16px   text-2xl = 24px   text-4xl = 36px
text-lg   = 18px   text-3xl = 30px   text-5xl = 48px
```

### Responsive Breakpoints
```
sm: ≥ 640px (mobile landscape)
md: ≥ 768px (tablet)
lg: ≥ 1024px (desktop)
xl: ≥ 1280px (large desktop)
```

---

## Integration

- **content-update**: Content + design updates together
- **deploy-check**: Pre-deployment design verification

---

**Version**: v1.1 | **Updated**: 2025-12-31
**Project**: young-personal-site
**Philosophy**: "Design is not just what it looks like. Design is how it works." - Steve Jobs
