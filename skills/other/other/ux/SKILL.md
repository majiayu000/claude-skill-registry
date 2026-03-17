---
name: ux
description: UX patterns including responsive design, accessibility, interactions, and user flows for PastCare
disable-model-invocation: true
argument-hint: [component or flow to implement]
---

# UX Design Skill

Implement UX for: $ARGUMENTS

## Mobile-First Responsive Design (MANDATORY)

All components MUST be:
1. **Mobile-first**: Write CSS for mobile, add media queries for larger screens
2. **Responsive**: Work across mobile, tablet, desktop
3. **Theme-aware**: Support light and dark themes

### Breakpoints
```css
/* Mobile (default) - ≤640px */
.component {
  padding: 1rem;
  flex-direction: column;
}

/* Tablet - ≥768px */
@media (min-width: 768px) {
  .component {
    padding: 1.5rem;
    flex-direction: row;
  }
}

/* Desktop - ≥1024px */
@media (min-width: 1024px) {
  .component {
    padding: 2rem;
  }
}
```

### Mobile Adjustments
- Single column layouts
- Full-width buttons
- Reduced padding (1rem)
- Stack flex layouts vertically
- Hide non-essential button text (show icons only)

### Tablet Adjustments
- Form rows → single column
- Adjust grid columns
- Show abbreviated labels

### Desktop
- Full multi-column layouts
- All features visible
- Hover states active

## Theme Support

```css
/* Light theme (default) */
.component {
  background: var(--bg-card);
  color: var(--text-primary);
  border: 1px solid var(--border-normal);
}

/* Dark theme */
[data-theme="dark"] .component {
  background: rgba(30, 41, 59, 0.95);
  border-color: rgba(255, 255, 255, 0.1);
}
```

### CSS Variables for Theming
```css
--bg-card: /* card background */
--bg-input: /* input field background */
--text-primary: /* primary text */
--text-secondary: /* secondary text */
--text-tertiary: /* muted text */
--border-normal: /* default border */
--color-primary: /* primary action */
--color-danger: /* danger/error */
--color-success: /* success */
--color-info: /* information */
--shadow-sm, --shadow-md, --shadow-lg, --shadow-xl: /* shadows */
--focus-ring: /* focus state */
```

## Spacing System

### Padding
```css
/* Page container */ padding: 1.5rem;
/* Cards/sections */ padding: 1.25rem to 1.5rem;
/* Form fields */ padding: 0.75rem;
/* Primary buttons */ padding: 0.75rem 1.5rem;
/* Secondary buttons */ padding: 0.625rem 1.25rem;
/* Dialog content */ padding: 1rem to 1.5rem;
```

### Margins
```css
/* Page header bottom */ margin-bottom: 2rem;
/* Section spacing */ margin: 1.5rem to 2rem;
/* Form field spacing */ margin-bottom: 1.25rem;
/* Item spacing */ margin: 0.625rem to 1rem;
```

### Gaps (Flexbox/Grid)
```css
gap: 1rem;    /* Primary - DEFAULT */
gap: 0.5rem;  /* Compact - icon+text */
gap: 1.5rem;  /* Wide - major sections */
```

## Layout Patterns

### Page Container
```css
.page-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 1.5rem;
}
```

### Stats Grid (Auto-Responsive)
```css
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}
```

### Card Grid
```css
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.25rem;
}
```

### Form Row (2-Column)
```css
.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}
@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}
```

## Interaction Patterns

### Transitions
```css
transition: all 0.2s ease;  /* Standard */
transition: all 0.3s ease;  /* Important states */
/* NEVER exceed 0.3s */
```

### Hover Effects
```css
/* Lift effect */
transform: translateY(-2px);  /* Subtle */
transform: translateY(-4px);  /* Cards */

/* Scale (FAB only) */
transform: scale(1.1);
```

### Focus States
```css
/* Always visible focus ring */
:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1);
  border-color: #8b5cf6;
}
```

### Loading States
```css
.loading {
  opacity: 0.7;
  pointer-events: none;
}
.spinner {
  animation: spin 1s linear infinite;
}
```

### Animations
```css
@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
```

## Accessibility Requirements

### Form Labels
```html
<!-- Always associate labels with inputs -->
<label for="email">Email <span class="required">*</span></label>
<input id="email" type="email" aria-required="true">
```

### Required Fields
- Red asterisk (`*`) after label
- `aria-required="true"` on input
- Clear validation messages

### Focus Management
- All interactive elements focusable
- Visible focus indicators
- Logical tab order
- Skip links for navigation

### Screen Readers
```html
<!-- Announce dynamic content -->
<div role="alert" aria-live="polite">
  {{ statusMessage }}
</div>

<!-- Descriptive buttons -->
<button aria-label="Delete member John Doe">
  <i class="pi pi-trash"></i>
</button>
```

### Color Contrast
- Text on backgrounds: minimum 4.5:1 ratio
- Large text: minimum 3:1 ratio
- Interactive elements: clearly distinguishable

### ARIA for PrimeNG
```html
<p-table aria-label="Members list">
<p-dialog [ariaLabel]="'Edit member'">
<p-dropdown [ariaLabel]="'Select fellowship'">
```

## User Feedback Patterns

### Success Feedback
```typescript
// Toast notification
this.messageService.add({
  severity: 'success',
  summary: 'Success',
  detail: 'Member saved successfully'
});
```

### Error Feedback
```typescript
// Show in form AND toast for critical errors
this.messageService.add({
  severity: 'error',
  summary: 'Error',
  detail: 'Failed to save member'
});
```

### Confirmation Dialogs
```typescript
// Always confirm destructive actions
this.confirmationService.confirm({
  message: 'Are you sure you want to delete this member?',
  header: 'Confirm Delete',
  icon: 'pi pi-exclamation-triangle',
  acceptButtonStyleClass: 'p-button-danger',
  accept: () => this.deleteMember()
});
```

### Progress Indicators
- Show spinner for operations > 300ms
- Show progress bar for uploads/long operations
- Disable submit buttons while processing

## Navigation Patterns

### Breadcrumbs
```html
<nav aria-label="Breadcrumb">
  <ol class="breadcrumb">
    <li><a routerLink="/dashboard">Dashboard</a></li>
    <li><a routerLink="/members">Members</a></li>
    <li aria-current="page">John Doe</li>
  </ol>
</nav>
```

### Back Navigation
- Always provide way to go back
- Preserve form state when navigating away
- Warn before losing unsaved changes

## Critical UX Rules

1. ALWAYS design mobile-first
2. ALWAYS provide loading feedback
3. ALWAYS confirm destructive actions
4. ALWAYS maintain visible focus states
5. ALWAYS use semantic HTML
6. NEVER remove content without confirmation
7. NEVER disable back navigation
8. NEVER auto-submit forms
9. NEVER hide errors from users
10. ALWAYS preserve user input on errors
