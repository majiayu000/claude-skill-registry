---
name: angular-best-practices
description: Angular and frontend development guidelines for PastCare. Use when writing or reviewing Angular code.
user-invocable: false
---

# Angular Best Practices for PastCare

## Project Location
- Frontend: `/home/reuben/Documents/workspace/past-care-spring-frontend/`
- NEVER create Angular files in the backend directory

## Mobile-First & Responsive Design (MANDATORY)

All components MUST be:
1. **Mobile-first**: CSS for mobile first, then media queries for larger screens
2. **Responsive**: Work across mobile, tablet, desktop
3. **Theme-aware**: Support light and dark themes using CSS variables

```css
/* Mobile styles first (default) */
.component {
  padding: 1rem;
  flex-direction: column;
}

/* Tablet and up */
@media (min-width: 768px) {
  .component {
    padding: 1.5rem;
    flex-direction: row;
  }
}

/* Desktop and up */
@media (min-width: 1024px) {
  .component {
    padding: 2rem;
  }
}
```

## Color Palette (EXACT COLORS ONLY)

**Primary Colors:**
- Primary Purple Gradient: `linear-gradient(135deg, #667eea 0%, #764ba2 100%)` - buttons, FAB, main actions
- Secondary Purple: `linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%)` - advanced features
- Accent Green: `#10b981`, `#34d399` - success states, verified badges
- Accent Orange: `#f59e0b`, `#f97316` - warnings, pending states
- Accent Blue: `#3b82f6`, `#2563eb` - information
- Danger Red: `#ef4444`, `#dc2626` - delete, errors

**Neutral Colors:**
- Text primary: `#1f2937`
- Text secondary: `#6b7280`
- Text muted: `#9ca3af`
- Border default: `#e5e7eb`
- Background light: `#f9fafb`

## Border Radius Hierarchy

- Page containers: `1.25rem` (20px)
- Cards: `1rem` (16px)
- Form inputs/buttons: `0.75rem` (12px)
- Tags/badges: `0.5rem` (8px)
- Pills: `9999px`
- Circular: `50%`

## Spacing System

**Padding:**
- Page container: `1.5rem`
- Cards: `1.25rem` to `1.5rem`
- Form fields: `0.75rem`
- Primary buttons: `0.75rem 1.5rem`

**Gaps:**
- Primary: `1rem` (default)
- Compact: `0.5rem`
- Wide: `1.5rem` to `2rem`

## Form Field Validation Pattern

```typescript
// Signal for backend errors
backendFieldErrors = signal<Record<string, string[]>>({});

private parseAndSetBackendFieldErrors(error: any): void {
  const fieldErrors: Record<string, string[]> = {};
  if (error.error && typeof error.error === 'object') {
    for (const key of Object.keys(error.error)) {
      if (['message', 'status', 'timestamp', 'path', 'error'].includes(key)) continue;
      const value = error.error[key];
      if (Array.isArray(value) && value.length > 0 && typeof value[0] === 'string') {
        fieldErrors[key] = value;
      }
    }
  }
  this.backendFieldErrors.set(fieldErrors);
}

getBackendFieldErrors(fieldName: string): string[] {
  return this.backendFieldErrors()[fieldName] || [];
}
```

```html
@for (error of getBackendFieldErrors('fieldName'); track error) {
  <div class="error-message backend-error">{{ error }}</div>
}
```

## CSS Class Naming (BEM)

- Block: `.member-card`
- Element: `.member-card__header`
- Modifier: `.member-card--selected`
- State: `.is-active`, `.is-disabled`, `.has-error`

## PrimeNG Overrides

```css
::ng-deep .p-focus {
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1) !important;
}
```

## Critical Rules

1. ALWAYS use purple gradient for primary actions
2. ALWAYS maintain 1rem base gap
3. NEVER create custom colors
4. ALWAYS include focus states
5. NEVER exceed 0.3s for animations
6. ALWAYS follow border-radius hierarchy
7. ALWAYS use flexbox/grid gaps (not margins)
8. NEVER use inline styles
