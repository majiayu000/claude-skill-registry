---
name: ui-layout-guide
description: UI layout optimization guide for Angular pages. Use when reviewing or creating page layouts, dashboard cards, info grids, or any UI component that needs consistent styling.
---

UI layout optimization guide for Angular pages. This skill provides guidance on using shared styles and creating consistent, clean layouts.

## Arguments

- `$ARGUMENTS` - Query or command:
  - `review <path>` - Review component for layout optimization
  - `dashboard` - Dashboard card layout patterns
  - `card` - Card component patterns
  - `grid` - Grid and info-grid patterns
  - `spacing` - Margin and padding utilities
  - `text` - Text styling classes
  - `form` - Form layout patterns
  - Or ask any question about UI layout

## Shared Styles Location

All shared styles are in `libs/mxsecurity/shared/styles/`:

| File | Purpose |
|------|---------|
| `_layout.scss` | Margin/padding utilities (.mr-4, .mt-8, .p-16, etc.) |
| `_text.scss` | Text color classes (.text-on-surface-variant) |
| `_form.scss` | Form layout (.form-row, .form-column) |
| `_shared.scss` | Main entry point, includes .content-wrapper |
| `_table.scss` | Table-specific styles |
| `_material-custom.scss` | Material UI overrides |
| `_formoxa-custom.scss` | FormOXA UI overrides |

## Layout Utilities Reference

### Margin Classes (from _layout.scss)

Generated for sizes 4, 8, 12, 16, 20, 24, 28, 32, 36, 40 (px):

```scss
.mr-{size}  // margin-right
.ml-{size}  // margin-left
.mt-{size}  // margin-top
.mb-{size}  // margin-bottom
.mx-{size}  // margin left + right
.my-{size}  // margin top + bottom
.m-{size}   // margin all sides
```

### Padding Classes (from _layout.scss)

Generated for sizes 4, 8, 12, 16, 20, 24, 28, 32 (px):

```scss
.pr-{size}  // padding-right
.pl-{size}  // padding-left
.pt-{size}  // padding-top
.pb-{size}  // padding-bottom
.px-{size}  // padding left + right
.py-{size}  // padding top + bottom
.p-{size}   // padding all sides
```

### Text Classes (from _text.scss)

```scss
.text-on-surface-variant     // Secondary text color
.text-on-surface-variant-op-38  // Disabled text (38% opacity)
```

### Form Layout Classes (from _form.scss)

```scss
.form-row {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  gap: 8px;
}

.form-column {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
```

## Dashboard Card Patterns

### Standard Card Structure

```html
<mat-card class="dashboard-card">
  <mat-card-header>
    <mat-card-title class="card-title-row">
      <span class="card-title">{{ title }}</span>
      <div class="header-actions">
        <!-- Optional: refresh button, menu, etc. -->
      </div>
    </mat-card-title>
  </mat-card-header>
  <mat-card-content>
    <!-- Card content -->
  </mat-card-content>
  <mat-card-actions align="end">
    <!-- Optional: action buttons -->
  </mat-card-actions>
</mat-card>
```

### Card Grid Layout

```scss
.card-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;

  @media (max-width: 900px) {
    grid-template-columns: 1fr;
  }
}
```

### Key-Value Pattern (for key-value displays)

Use FormOXA's `mx-key-value` component instead of raw `<dt>` / `<dd>` elements:

**Import in component:**
```typescript
import { MxKeyValueComponent, MxKeyValueGroupDirective } from '@moxa/formoxa/mx-key-value';

@Component({
  imports: [MxKeyValueComponent, MxKeyValueGroupDirective],
  // ...
})
```

**Template usage:**
```html
<mx-key-value-group>
  <mx-key-value
    [key]="t('features.example.label')"
    keySize="md"
    [value]="data().value"
    valueSize="md"
    direction="horizontal"
  ></mx-key-value>
  <mx-key-value
    [key]="t('features.example.another_label')"
    keySize="md"
    [value]="data().anotherValue"
    valueSize="md"
    direction="horizontal"
  ></mx-key-value>
</mx-key-value-group>
```

**Properties:**
- `key` - Label text (supports i18n)
- `value` - Display value
- `keySize` - Key font size: `'sm'` | `'md'` | `'lg'`
- `valueSize` - Value font size: `'sm'` | `'md'` | `'lg'`
- `direction` - Layout direction: `'horizontal'` | `'vertical'`

## Best Practices

### DO

- Use shared utility classes for spacing (`.mt-16`, `.mb-8`)
- Use CSS Grid for card layouts
- Use Flexbox for single-direction layouts
- Use Material Design color tokens via `one-theme`
- Keep consistent gap sizes (8px, 16px)
- Use responsive breakpoints (900px for 2-col, 600px for 1-col)

### DON'T

- Hardcode colors - use theme variables
- Mix margin/padding in component styles when utilities exist
- Create duplicate layout classes that exist in shared styles
- Use different gap sizes across similar components

## Color Usage

Always use theme colors from `one-theme`:

```scss
@use 'sass:map';
@use 'one-theme' as *;

.label {
  color: map.get($mx-light, onSurfaceVariant);  // Secondary text
}

.value {
  color: map.get($mx-light, onSurface);  // Primary text
}

.background {
  background-color: map.get($mx-light, surface);
}
```

## Review Checklist

When reviewing a component for layout optimization:

1. [ ] Uses shared spacing utilities where appropriate
2. [ ] Uses theme colors instead of hardcoded values
3. [ ] Grid layouts are responsive
4. [ ] Consistent gap sizes (8px or 16px)
5. [ ] Card headers use `.card-title-row` for flex layout
6. [ ] Info displays use `mx-key-value` component from FormOXA
7. [ ] No duplicate styles that exist in shared files
