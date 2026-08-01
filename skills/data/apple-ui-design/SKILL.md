---
name: apple-ui-design
description: 'Apple-inspired clean, minimal, premium UI design. Use when building
  modern interfaces requiring exceptional UX, clean aesthetics, or Apple-like polish.
  Triggers on: clean UI, modern design, Apple styl'
---

---
name: apple-ui-design
description: Apple-inspired clean, minimal, premium UI design. Use when building modern interfaces requiring exceptional UX, clean aesthetics, or Apple-like polish. Triggers on: clean UI, modern design, Apple style, minimal, premium, user-friendly, UX.
---

# Apple UI Design

Apple-inspired clean, minimal, premium UI design system.

## When to Use

- Building modern interfaces requiring exceptional UX
- Creating clean, minimal aesthetics
- Implementing Apple-like polish and animations
- Designing premium user experiences
- Reviewing UI/UX for design quality

## Workflow

### Step 1: Apply Typography System

Use SF Pro Display with proper hierarchy (hero, title, body, caption).

### Step 2: Apply Color Philosophy

Use light/dark mode variables with proper contrast.

### Step 3: Apply Spacing System

Follow 4/8/16/24/48/96px spacing rhythm.

### Step 4: Verify Checklist

Ensure touch targets, contrast, and animations meet standards.

---

## Core Principles

1. **Clarity** - Content is king, UI disappears
2. **Deference** - UI serves content, never competes
3. **Depth** - Layering creates hierarchy

## Typography
```css
font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', sans-serif;

/* Hierarchy */
--text-hero: 600 48px/1.1;      /* Bold statements */
--text-title: 600 32px/1.2;     /* Section headers */
--text-body: 400 17px/1.5;      /* Readable content */
--text-caption: 400 13px/1.4;   /* Secondary info */
```

## Color Philosophy
```css
/* Light mode */
--bg-primary: #ffffff;
--bg-secondary: #f5f5f7;
--text-primary: #1d1d1f;
--text-secondary: #86868b;
--accent: #0071e3;

/* Dark mode */
--bg-primary: #000000;
--bg-secondary: #1d1d1f;
--text-primary: #f5f5f7;
```

## Spacing System
```css
--space-xs: 4px;
--space-sm: 8px;
--space-md: 16px;
--space-lg: 24px;
--space-xl: 48px;
--space-2xl: 96px;   /* Section gaps */
```

## Key Patterns

### Cards
```css
.card {
  background: rgba(255,255,255,0.8);
  backdrop-filter: blur(20px);
  border-radius: 18px;
  border: 1px solid rgba(0,0,0,0.05);
  box-shadow: 0 4px 24px rgba(0,0,0,0.06);
}
```

### Buttons
```css
.btn-primary {
  background: var(--accent);
  color: white;
  padding: 12px 24px;
  border-radius: 980px;  /* Pill shape */
  font-weight: 500;
  transition: all 0.2s ease;
}
.btn-primary:hover {
  transform: scale(1.02);
  filter: brightness(1.1);
}
```

### Subtle Animations
```css
/* Micro-interactions */
transition: all 0.3s cubic-bezier(0.25, 0.1, 0.25, 1);

/* Page elements */
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
```

## UX Rules

| Do | Don't |
|----|-------|
| Generous whitespace | Cramped layouts |
| One primary action | Multiple competing CTAs |
| Progressive disclosure | Everything visible |
| Subtle feedback | Jarring animations |
| System fonts | Decorative fonts |

## Checklist

- [ ] Touch targets ≥ 44px
- [ ] Contrast ratio ≥ 4.5:1
- [ ] Max content width ~680px
- [ ] Consistent spacing rhythm
- [ ] Dark mode support
- [ ] Smooth 60fps animations
