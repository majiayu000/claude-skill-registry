---
name: ui-ux-audit
description: Automates UI/UX audits. Researches competitors, validates accessibility (WCAG 2.1), verifies responsiveness, audits design system consistency. Use when implementing any UI feature.
allowed-tools: Read, WebSearch, WebFetch, Grep, Glob
---

# UI/UX Audit - Interface Audit System

## Purpose

This skill automates UI/UX audits:

- **Research** competitors before implementing
- **Validate** accessibility (WCAG, contrast, touch targets)
- **Verify** responsiveness
- **Audit** design system consistency
- **Document** design decisions

---

## Workflow

```
1. IDENTIFY FEATURE → What type of UI? Mobile-first or desktop-first?
        ↓
2. RESEARCH COMPETITORS → 3-5 relevant competitors, screenshots
        ↓
3. DEFINE PATTERN → What do all do alike? Where to differentiate?
        ↓
4. IMPLEMENT → Follow accessibility and responsiveness checklists
        ↓
5. VALIDATE → Run final checklist, capture screenshots
```

---

## Competitor Research

### Required Search Queries

```
"[UI type] design examples 2025"
"[similar product] UI/UX"
"[functionality] best practices"
"[framework] [component] examples"
```

### Research Template

```markdown
## Research: [Feature Name]

### Competitors Analyzed

1. **[Name]** - [URL]
    - Strong points: [list]
    - Weak points: [list]

### Market Pattern

- [What everyone does alike]

### Our Approach

- **Decision:** [what we'll do]
- **Justification:** [why]
- **Differentiator:** [how we stand out]
```

---

## Accessibility Checklist (WCAG 2.1)

### Level A (Required)

- [ ] **Text contrast:** Minimum 4.5:1 normal, 3:1 large text
- [ ] **Alt text:** All images have descriptive alt
- [ ] **Keyboard navigation:** All interactive elements via Tab
- [ ] **Visible focus:** Clear outline on focused elements
- [ ] **Form labels:** All inputs have associated label
- [ ] **Error messages:** Clear and associated to field

### Level AA (Recommended)

- [ ] **Resize:** Works up to 200% zoom
- [ ] **Touch targets:** Minimum 44x44px (`h-11 w-11`)
- [ ] **Hover/Focus:** Content visible on hover also via focus

---

## Responsiveness Checklist

### Required Viewports

```typescript
const REQUIRED_VIEWPORTS = {
	mobile: { width: 375, height: 667 }, // iPhone SE
	tablet: { width: 768, height: 1024 }, // iPad
	desktop: { width: 1280, height: 800 }, // Laptop
	fullhd: { width: 1920, height: 1080 }, // Common monitor
};
```

### Mobile (375px)

- [ ] Vertical stack layout (flex-col)
- [ ] Hamburger menu or bottom nav
- [ ] Touch-friendly buttons (min 44px)
- [ ] Readable text without zoom
- [ ] Vertical scroll only

### Desktop (1280px+)

- [ ] Use horizontal space
- [ ] Expanded sidebar
- [ ] Can increase info density

---

## CRITICAL: Zero Horizontal Overflow

> **NEVER** should there be horizontal scroll.

### Required CSS Patterns

```tsx
// Main layout
<div className="flex h-screen w-screen overflow-hidden">
	{/* Sidebar */}
	<aside className="w-[260px] flex-shrink-0 overflow-y-auto">...</aside>

	{/* Main content */}
	<main className="flex-1 min-w-0 overflow-hidden">...</main>
</div>
```

### Overflow Checklist

- [ ] Main container has `overflow-hidden`?
- [ ] Sidebar has `flex-shrink-0`?
- [ ] Main content has `min-w-0`?
- [ ] No element with width larger than container?
- [ ] Tested at 1920x1080?

---

## Skeleton Loading

### Rule: Every Component HAS Skeleton

- [ ] Skeleton created with component
- [ ] Same dimensions as final content
- [ ] `animate-pulse` animation
- [ ] Same visual structure

### Structure

```
components/features/UserCard/
├── UserCard.tsx
└── UserCardSkeleton.tsx
```

### Template

```tsx
export function ComponentSkeleton() {
	return (
		<div className="animate-pulse">
			<div className="h-4 bg-gray-200 rounded w-3/4 mb-2" />
			<div className="h-4 bg-gray-200 rounded w-1/2" />
		</div>
	);
}
```

---

## Design System (Tailwind)

### Colors

- **Primary:** `indigo-600` (buttons, links)
- **Secondary:** `gray-600` (secondary text)
- **Success:** `green-600`
- **Error:** `red-600`
- **Warning:** `yellow-600`

### Spacing (4px scale)

```
p-1: 4px    p-2: 8px    p-4: 16px
p-6: 24px   p-8: 32px   p-12: 48px
```

### Border & Shadow

- **Border radius:** `rounded-lg` (8px) default
- **Shadows:** `shadow-sm` for cards, `shadow-lg` for modals

---

## Output Format

```markdown
## UI/UX AUDIT - Report

### Feature

- **Name:** [name]
- **Type:** [form/dashboard/list/etc]
- **Approach:** [mobile-first/desktop-first]

### Competitor Research

- [x] Researched 5 competitors
- **Pattern identified:** [description]

### Accessibility

- [x] Contrast validated (4.5:1+)
- [x] Touch targets 44x44px
- [x] Alt text on images
- [x] Labels on forms

### Responsiveness

- [x] Mobile (375px) - OK
- [x] Tablet (768px) - OK
- [x] Desktop (1280px) - OK
- [x] FullHD (1920px) - OK
- [x] Zero horizontal overflow

### Skeleton

- [x] Created
- [x] Correct dimensions
```

---

## Critical Rules

1. **ALWAYS research competitors** - Before implementing UI
2. **ALWAYS validate accessibility** - WCAG 2.1 Level AA
3. **ALWAYS test viewports** - Mobile, tablet, desktop, fullhd
4. **NEVER horizontal overflow** - Check all viewports
5. **ALWAYS create skeleton** - With the component

---

## Version

- **v2.0.0** - Generic template
