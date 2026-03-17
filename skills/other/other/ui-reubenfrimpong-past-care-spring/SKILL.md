---
name: ui
description: UI component patterns, colors, typography, and styling for PastCare Angular components
disable-model-invocation: true
argument-hint: [component or pattern to implement]
---

# UI Design Skill

Implement UI for: $ARGUMENTS

## Color Palette (USE EXACT VALUES)

### Primary Colors
```css
/* Primary Purple - buttons, FAB, main actions, toolbars */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Secondary Purple - advanced features, secondary actions */
background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);

/* Accent Green - success, quick add, verified badges */
background: linear-gradient(135deg, #34d399 0%, #10b981 100%);
/* Solid: #10b981, #34d399 */

/* Accent Orange - warnings, bulk import, pending */
color: #f59e0b; /* or #f97316 */

/* Accent Blue - information, location features */
color: #3b82f6; /* or #2563eb */

/* Danger Red - delete, errors, critical actions */
color: #ef4444; /* or #dc2626 */
```

### Neutral Colors
```css
--text-primary: #1f2937;
--text-secondary: #6b7280;
--text-muted: #9ca3af;
--border-default: #e5e7eb;
--border-light: #d1d5db;
--bg-light: #f9fafb;
--bg-lighter: #f3f4f6;
```

## Typography

```css
/* Page titles */
font-size: 1.875rem; /* 30px */
font-weight: 700;
color: #1f2937;

/* Section titles */
font-size: 1.125rem; /* 18px */
font-weight: 600;

/* Subtitles */
font-size: 0.875rem; /* 14px */
color: #6b7280;

/* Form labels */
font-size: 0.875rem;
font-weight: 500;
color: #374151;

/* Body text */
font-size: 0.9375rem; /* 15px */

/* Small text */
font-size: 0.75rem; /* 12px */
color: #6b7280;

/* Tags/badges */
font-size: 0.625rem; /* 10px */
font-weight: bold;
```

## Border Radius Hierarchy

```css
/* Page containers/sections */
border-radius: 1.25rem; /* 20px */

/* Cards */
border-radius: 1rem; /* 16px */

/* Form inputs, buttons */
border-radius: 0.75rem; /* 12px */

/* Tags/badges */
border-radius: 0.5rem; /* 8px */

/* Pills (status badges) */
border-radius: 9999px;

/* Circular (avatars) */
border-radius: 50%;
```

## Shadows

```css
/* Subtle (default) */
box-shadow: 0 1px 3px rgba(0,0,0,0.05), 0 4px 12px rgba(0,0,0,0.04);

/* Card hover */
box-shadow: 0 8px 20px rgba(102, 126, 234, 0.15);

/* Dialog/panel */
box-shadow: 0 4px 12px rgba(0,0,0,0.1);

/* Focus state */
box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1);
```

## Button Patterns

### Primary Button
```css
.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 0.75rem;
  border: none;
  font-weight: 500;
  transition: all 0.2s ease;
}
.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}
.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}
```

### Secondary Button
```css
.btn-secondary {
  background: #f3f4f6;
  color: #4b5563;
  border: 1px solid #e5e7eb;
  padding: 0.625rem 1.25rem;
  border-radius: 0.75rem;
}
.btn-secondary:hover {
  background: #e5e7eb;
}
```

### Danger Button
```css
.btn-danger {
  background: #fef2f2;
  color: #ef4444;
  border: 1px solid #fee2e2;
}
.btn-danger:hover {
  background: #ef4444;
  color: white;
}
```

### Icon Button
```css
.btn-icon {
  width: 36px;
  height: 36px;
  border: 2px solid #e5e7eb;
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
}
.btn-icon:hover {
  border-color: #667eea;
  background: rgba(102, 126, 234, 0.1);
}
```

## Card Patterns

### Standard Card
```css
.card {
  background: white;
  border-radius: 1rem;
  padding: 1.25rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05), 0 4px 12px rgba(0,0,0,0.04);
  transition: all 0.2s ease;
}
.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.15);
}
```

### Card Actions (3-Column Grid)
```css
.card-actions {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.5rem;
}
```

## Avatar Patterns

### Member Avatar (Card)
```css
.avatar-card {
  width: 64px;
  height: 64px;
  border-radius: 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-weight: bold;
  font-size: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
}
```

### Profile Avatar (Large)
```css
.avatar-profile {
  width: 80px; /* or up to 150px */
  height: 80px;
  border-radius: 50%;
  border: 3px solid #667eea;
}
```

## Badge Patterns

### Fellowship Tag
```css
.tag-fellowship {
  background: #eff6ff;
  color: #2563eb;
  padding: 0.25rem 0.625rem;
  border-radius: 0.5rem;
  font-size: 0.625rem;
  font-weight: bold;
}
```

### Status Badge (Pill)
```css
.badge-status {
  background: linear-gradient(135deg, var(--color1) 0%, var(--color2) 100%);
  color: white;
  padding: 0.375rem 0.875rem;
  border-radius: 9999px;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.75rem;
}
```

## Empty State
```css
.empty-state {
  background: linear-gradient(to bottom, #ffffff, #f9fafb);
  border: 2px dashed #e5e7eb;
  border-radius: 1.25rem;
  padding: 4rem 2rem;
  text-align: center;
}
.empty-icon {
  width: 120px;
  height: 120px;
  background: linear-gradient(135deg, rgba(102,126,234,0.1) 0%, rgba(118,75,162,0.1) 100%);
  border-radius: 50%;
  margin: 0 auto 1.5rem;
}
```

## Dialog Standards

```css
/* Widths: Small 450px, Medium 600px, Large 900px, Max 95vw */
.dialog-header {
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}
.dialog-content {
  padding: 1.5rem;
}
.dialog-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid #e5e7eb;
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
}
```

## PrimeNG Overrides

```css
::ng-deep .p-inputswitch {
  width: 3rem;
  height: 1.75rem;
}
::ng-deep .p-select,
::ng-deep .p-chips {
  font-size: 0.9375rem;
}
::ng-deep .p-focus {
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1) !important;
}
```

## Critical Rules

1. ALWAYS use purple gradient for primary actions
2. NEVER create custom colors - use defined palette only
3. ALWAYS follow border-radius hierarchy
4. NEVER exceed 0.3s for animations
5. NEVER use inline styles - use component CSS
