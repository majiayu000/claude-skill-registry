---
name: mithril-materialized
description: Mithril Materialized is a lightweight, TypeScript-first component library that brings Material Design to Mithril.js applications without any external JavaScript dependencies. It provides a comprehensive set of UI components, including forms, navigation, data displays, and utilities, all optimized for performance and accessibility. Built on CSS-only styling and Mithril's FactoryComponent pattern, it supports light/dark themes, controlled/uncontrolled modes, and modular imports for tree-shakable bundles. Ideal for building responsive, modern web apps with minimal overhead.
---
# Mithril Materialized UI Development Skill

**Description**: Expert skill for developing and maintaining the mithril-materialized library—a TypeScript-based Mithril.js component library implementing Material Design without external JavaScript dependencies.

**When to use**: When working with Mithril Materialized components, creating new ones, fixing bugs, implementing features, or helping users integrate the library.

## Project Overview

Mithril Materialized is a zero-external-JS-dependency component library wrapping Material Design in Mithril.js. This monorepo uses pnpm workspaces:

- **`packages/lib/`**: Core library (published as `mithril-materialized` on npm).
- **`packages/example/`**: Documentation and live demo site.

### Key Architectural Principles

1. **Zero External JS Dependencies**: Relies solely on CSS for styling; no Materialize.js or jQuery.
2. **CSS-Only Styling**: No JS initialization needed.
3. **Factory Component Pattern**: Uses Mithril's `FactoryComponent` for performance.
4. **Controlled/Uncontrolled Support**: Components handle both modes.
5. **TypeScript First**: Full types and JSDoc.
6. **Modular CSS**: Tree-shakable for optimal bundles.

## Component Architecture Patterns

### 1. Factory Component Pattern

All components follow this for lifecycle management:

```typescript
import m, { FactoryComponent, Attributes } from 'mithril';

export interface MyComponentAttrs extends Attributes {
  // Attributes here
}

export const MyComponent: FactoryComponent<MyComponentAttrs> = () => {
  const state = { /* Persistent state */ };
  return {
    oninit: ({ attrs }) => { /* Init */ },
    onremove: () => { /* Cleanup */ },
    view: ({ attrs }) => m('.my-component', { /* VNode */ }),
  };
};
```

### 2. Controlled vs Uncontrolled

Support both; detect via `isControlled(attrs)` (checks for `value` and handler).

- **Controlled**: Parent manages state via `value` and `oninput/onchange`.
- **Uncontrolled**: Use `defaultValue` and internal state.

Warn on misuse (e.g., `value` without handler).

### 3. Validation

Use `ValidatorFunction<T>` returning `true | false | '' | string`.

Validate on blur, track `hasInteracted`. Integrate with HTML5 validity.

Example:

```typescript
m(TextInput, {
  validate: (v) => v.length >= 3 || 'Too short',
});
```

### 4. Icons

- `Icon`: For material-icons font.
- `MaterialIcon`: For SVG icons.

### 5. Labels and Helpers

Use `Label` and `HelperText` for form elements.

## Component Categories

| Category     | Components | Key Files |
|--------------|------------|-----------|
| **Inputs**   | TextInput, TextArea, AutoComplete, Chips, etc. | input.ts, autocomplete.ts |
| **Selections** | Select, RadioButtons, Switch, LikertScale (v3.13) | select.ts, likert-scale.ts |
| **Buttons**  | Button, IconButton, FloatingActionButton | button.ts |
| **Pickers**  | DatePicker, TimePicker, TimeRangePicker | datepicker.ts |
| **Displays** | ModalPanel, Tooltip, Toast, Badge | modal.ts |
| **Navigation** | Sidenav, Breadcrumb, Tabs, Pagination | sidenav.ts |
| **Layouts**  | Masonry, ImageList, Timeline, Carousel | masonry.ts |
| **Data**     | DataTable, TreeView, Rating, Wizard | datatable.ts |
| **Collections** | Collection (rich content in v3.13), Collapsible | collection.ts |
| **Utilities** | ThemeSwitcher, FileUpload, CodeBlock | theme-switcher.ts |

### LikertScale (v3.13)

Purpose-built for surveys:

- Layouts: Horizontal/vertical/responsive.
- Anchors: Start/middle/end labels.
- Features: Tooltips, numbers, density/size variants.
- Alignment: Grid for multi-question surveys.

When to use:

| Component | Best For | Example |
|-----------|----------|---------|
| LikertScale | Semantic scales | Satisfaction surveys |
| RadioButtons | Choices | Favorite color |
| Rating | Icons | Product reviews |

## TypeScript Types

Core types in `types.ts`: `ComponentSize`, `ValidationResult`, etc.

Utilities: `RequiredKeys<T>`, `DeepReadonly<T>`.

## CSS Architecture

Modular files: core.css, forms.css, etc.

Theme via CSS vars (50+); supports light/dark/auto.

Programmatic: `ThemeManager.setTheme('dark')` or `toggle()`.

Custom overrides via CSS vars: Override variables like `--mm-primary-color` or `--mm-surface-color` in your global CSS.

## Development Workflow

Structure:

- lib/src: Components, types, SCSS.
- example/src: Demos.

Commands (root):

- `pnpm start`: Dev servers.
- `npm run build`: Build lib.

Releases: `npm run patch-release` (bumps, builds, publishes).

## Best Practices

- Structure: Imports → Types → Factory → State → Helpers → Lifecycle.
- Props: Standard names (label, value, oninput, etc.).
- Events: oninput (real-time), onchange (commit), onblur (validate).
- A11y: Semantics, ARIA, keyboard.
- Perf: Factory pattern, minimal redraws.

## Common Tasks

- **New Component**: Add TS/SCSS, export in index.ts, test in example.
- **Modify**: Check modes, types, backward compat.
- **Debug**: Validate on blur; check themes/responsiveness.

## Integration Examples

Basic form, data table, theme toggle (condensed; refer to full docs for details).

## Testing

Checklist: Modes, validation, themes, a11y, perf.

Pitfalls: Support uncontrolled; validate on blur; use uniqueId().

## Quick Reference

- Files: types.ts, utils.ts, index.ts.
- Functions: uniqueId(), ThemeManager.
- New in v3.13: LikertScale, rich Collection content, Rating tooltips.

This skill is a streamlined reference; consult source for implementation details.
