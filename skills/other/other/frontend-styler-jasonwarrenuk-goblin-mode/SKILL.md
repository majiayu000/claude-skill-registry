---
name: frontend-styler
description: Frontend styling: layout debugging, style consistency, CSS best practices for Svelte/SvelteKit.
user-invocable: false
effort: medium
paths:
  - "**/*.svelte"
  - "**/*.css"
allowed-tools:
  - Read
  - Glob
  - Grep
---

# Frontend Styling

Comprehensive guidance for debugging layout issues, ensuring style consistency, and applying best practices in frontend development, with emphasis on Svelte/SvelteKit projects.

---

## When This Skill Applies

Use this skill when:
- Fixing layout problems (alignment, spacing, positioning, responsive issues)
- Unifying component styling to match project conventions
- Debugging visual inconsistencies or CSS bugs
- Implementing new UI components
- Refactoring styling approaches
- Questions about CSS organization or best practices

---

## Core Principles

### 1. Accessibility First
Accessibility is not a polish step — it's a structural requirement. Every styling decision should pass the accessibility check before considering aesthetics.

**Non-negotiable**:
- Colour contrast meets WCAG 2.1 AA (4.5:1 normal text, 3:1 large text)
- Focus indicators visible on all interactive elements
- No information conveyed by colour alone (use icons, text, patterns too)
- Reduced motion support via `prefers-reduced-motion`
- Touch targets at least 44×44px on mobile
- Text remains readable at 200% zoom

```css
/* Always include focus styles */
:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
}

/* Respect motion preferences */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}

/* Never rely on colour alone */
.error-field {
  border-color: var(--color-error);
  border-width: 2px; /* Visual indicator beyond colour */
}
.error-message {
  color: var(--color-error);
}
.error-message::before {
  content: "⚠ "; /* Icon reinforces the colour */
}
```

### 2. Plan Before Execute
For non-trivial styling changes:
1. **Analyse** - Understand the current implementation
2. **Plan** - Outline proposed changes in logical order
3. **Confirm** - Get user approval before execution
4. **Execute** - Apply changes methodically

### 3. Consistency Over Cleverness
- Match the project's established patterns
- Don't introduce new approaches without discussion
- Preserve existing styling architecture
- Keep component styles predictable

### 4. Hierarchy and Order
When fixing multiple issues:
1. Fix parent containers before children
2. Address layout structure before fine-tuning
3. Edit CSS files before component files when possible
4. Work through child components before parent components

---

## Svelte-Specific Guidelines

### Component-Scoped Styles
Svelte's `<style>` blocks are scoped by default - leverage this:

```svelte
<style>
  /* Scoped automatically - no class name collisions */
  .button {
    padding: 0.5rem 1rem;
    border-radius: 0.25rem;
  }
  
  .button--primary {
    background: var(--color-primary);
  }
</style>
```

### Global Styles
Use `:global()` sparingly and intentionally:

```svelte
<style>
  /* Only when deliberately styling external elements */
  :global(.markdown-content h1) {
    margin-top: 2rem;
  }
</style>
```

### CSS Custom Properties
Prefer CSS variables for theming and consistency:

```svelte
<style>
  .card {
    background: var(--card-bg, #fff);
    border: 1px solid var(--card-border, #e5e7eb);
    border-radius: var(--radius-md, 0.5rem);
  }
</style>
```

### Reactive Classes
Use Svelte's class directive for dynamic styling:

```svelte
<button 
  class="btn" 
  class:btn--active={isActive}
  class:btn--disabled={disabled}
>
  Click me
</button>
```

---

## Layout Debugging Workflow

### Step 1: Identify Root Cause
Common layout issues and their causes:

**Alignment Problems:**
- Check parent container's `display` property (flex/grid/block)
- Verify `align-items`, `justify-content`, `align-self`
- Check for unexpected margins/padding
- Look for `position: absolute` breaking flow

**Spacing Issues:**
- Examine margin collapse behaviour
- Check for inconsistent spacing units
- Look for `box-sizing` mismatches
- Verify padding vs margin usage

**Responsive Breakage:**
- Check media query breakpoints
- Verify `min-width` vs `max-width` logic
- Look for fixed widths instead of flexible units
- Check for overflow issues

**Z-Index Conflicts:**
- Verify stacking context creation
- Check `position` property (relative/absolute/fixed)
- Look for competing `z-index` values
- Examine parent-child z-index relationships

### Step 2: Determine Fix Location
Ask: "Should this be fixed in the component or its parent?"

**Fix in Component When:**
- Issue is internal to component layout
- Component violates its own design contract
- Changes won't affect siblings or parent

**Fix in Parent When:**
- Issue involves multiple children
- Problem is container-level (flexbox/grid)
- Fix benefits component reusability

### Step 3: Apply Fixes Systematically
1. Start with structural changes (display, position, layout)
2. Then spacing (margin, padding, gap)
3. Then sizing (width, height, flex-grow/shrink)
4. Finally visual polish (borders, shadows, etc.)

---

## Style Consistency Workflow

### Step 1: Analyse Current Implementation
Check for:
- **Naming conventions** - BEM, utility classes, or other patterns
- **Styling location** - Component `<style>` vs external CSS
- **Value patterns** - Hard-coded vs CSS variables
- **Units** - rem, px, em usage patterns
- **Responsiveness** - Media query patterns

### Step 2: Identify Inconsistencies
Compare component styling against project patterns:

```
✗ Inconsistent: <div class="cardContainer">
✓ Consistent:   <div class="card-container">

✗ Inconsistent: padding: 8px;
✓ Consistent:   padding: 0.5rem;

✗ Inconsistent: background: #3B82F6;
✓ Consistent:   background: var(--color-primary); /* → --color-azure-3 */
```

### Step 3: Propose Changes
List specific changes needed to match project patterns:
- "Replace hard-coded colors with CSS variables"
- "Convert class names from camelCase to kebab-case"
- "Move inline styles to component `<style>` block"
- "Use rem units instead of px for spacing"

### Step 4: Execute After Approval
Apply changes in logical order:
1. CSS files first (if applicable)
2. Child components
3. Parent component last

---

## Project Preferences

### Naming Conventions
- **CSS classes**: `kebab-case` (e.g., `card-header`, `btn-primary`)
- **Component files**: `PascalCase.svelte` (e.g., `UserCard.svelte`)
- **BEM-like modifiers**: Double dash for variants (e.g., `btn--primary`, `card--elevated`)

### Spacing and Units
- Use `rem` for spacing (0.25rem, 0.5rem, 1rem, 1.5rem, 2rem)
- Use `em` for typography-relative spacing
- Avoid magic numbers - prefer CSS variables

### Color Management
- Define colors as CSS variables in root/theme
- Never hard-code hex/rgb values in components
- Use semantic naming (`--color-primary`, not `--blue-500`)
- Use [Reasonable Colors](https://www.reasonable.work/colors/) as the base palette (`npm install reasonable-colors` or CDN `unpkg.com/reasonable-colors@0.4.0/reasonable-colors.css`)
- Map RC variables to semantic aliases in `:root`; components only reference semantic vars:

```css
:root {
  /* Map Reasonable Colors → semantic roles */
  --color-primary:      var(--color-azure-3);
  --color-primary-bg:   var(--color-azure-1);
  --color-on-primary:   var(--color-azure-6);
  --color-danger:       var(--color-red-3);
  --color-danger-bg:    var(--color-red-1);
  --color-surface:      var(--color-gray-1);
  --color-on-surface:   var(--color-gray-6);
}
```

### Responsive Design
- Mobile-first approach (min-width media queries)
- Common breakpoints:
  - `sm`: 640px
  - `md`: 768px
  - `lg`: 1024px
  - `xl`: 1280px

---

## Common Patterns

### Flexbox Layouts
```css
/* Center content */
.container {
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Responsive row to column */
.flex-container {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}
```

### Grid Layouts
```css
/* Responsive grid */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}
```

### Component Structure
```svelte
<script>
  // Logic
</script>

<div class="component">
  <!-- Template -->
</div>

<style>
  .component {
    /* Styles scoped to component */
  }
</style>
```

---

## Anti-Patterns to Avoid

### Don't: Mix Styling Approaches
```svelte
<!-- ✗ Bad: Mixing inline styles with classes -->
<div class="card" style="margin: 10px;">
```

### Don't: Over-Nest Selectors
```css
/* ✗ Bad: Deep nesting */
.container .wrapper .card .header .title {
  font-size: 1.5rem;
}

/* ✓ Good: Flat structure */
.card-title {
  font-size: 1.5rem;
}
```

### Don't: Use `!important` Without Cause
```css
/* ✗ Bad: Using important as a crutch */
.button {
  color: red !important;
}

/* ✓ Good: Increase specificity properly */
.card .button {
  color: red;
}
```

### Don't: Hard-Code Values Repeatedly
```css
/* ✗ Bad: Repeated magic numbers */
.card { padding: 16px; }
.modal { padding: 16px; }
.panel { padding: 16px; }

/* ✓ Good: Use variables */
:root {
  --spacing-md: 1rem;
}
.card, .modal, .panel {
  padding: var(--spacing-md);
}
```

---

## Accessibility Checklist

When building or reviewing UI components:

- [ ] Does every interactive element have a visible focus indicator?
- [ ] Does the colour contrast pass WCAG 2.1 AA? (Use browser DevTools audit — or use Reasonable Colors where shade diff ≥ 3 guarantees AA body text)
- [ ] Is information conveyed by more than just colour?
- [ ] Are all images/icons either decorative (`aria-hidden`) or labelled (`alt`/`aria-label`)?
- [ ] Do form inputs have associated `<label>` elements?
- [ ] Are error messages linked to inputs via `aria-describedby`?
- [ ] Does the component work with keyboard only (Tab, Enter, Escape)?
- [ ] Does `prefers-reduced-motion` disable animations?
- [ ] Are touch targets at least 44×44px?
- [ ] Is text readable at 200% zoom without horizontal scrolling?

---

## Debugging Checklist

When encountering styling issues, verify:

- [ ] Is `box-sizing: border-box` set globally?
- [ ] Are there competing CSS specificity issues?
- [ ] Is the element in the correct stacking context?
- [ ] Are flexbox/grid properties on the correct element (parent vs child)?
- [ ] Are units consistent (rem vs px vs em)?
- [ ] Does the issue exist at all breakpoints?
- [ ] Are CSS variables defined and accessible?
- [ ] Is the component's `<style>` block scoped correctly?
- [ ] Are there any typos in class names or property names?
- [ ] Is the browser's developer tools showing overridden styles?

---

## Permission and Confirmation

**Always ask permission before:**
- Editing multiple files (confirm per file or batch)
- Making structural changes to component architecture
- Introducing new styling patterns or conventions
- Making changes that affect parent/sibling components

**Always explain:**
- Why a particular approach is recommended
- What knock-on effects changes might have
- Which order changes will be applied
- Alternative approaches if multiple options exist

---

## References

For deeper dives into specific topics:
- [Svelte Style Docs](https://svelte.dev/docs/svelte-components#style)
- [CSS Tricks Flexbox Guide](https://css-tricks.com/snippets/css/a-guide-to-flexbox/)
- [CSS Tricks Grid Guide](https://css-tricks.com/snippets/css/complete-guide-grid/)
- [BEM Naming Convention](http://getbem.com/naming/)

---

## Success Criteria

A styling task is complete when:
- Visual issues are resolved across all target breakpoints
- Styling matches project conventions consistently
- No new bugs or regressions introduced
- Code is maintainable and follows project patterns
- User has confirmed the solution meets requirements
- Accessibility checklist passes (contrast, focus, keyboard, screen reader)
- Animations respect `prefers-reduced-motion`
