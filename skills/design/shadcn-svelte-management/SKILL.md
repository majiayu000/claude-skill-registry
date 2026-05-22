---
name: shadcn-svelte-management
description: |
  Manage UI components using MCP tools with primary focus on Svelte ecosystem. Specialized in Svelte component libraries including shadcn-svelte, Skeleton UI, and Melt UI. Use when user needs to:
  (1) Add new Svelte UI components to a project
  (2) Build complex UI features requiring multiple components
  (3) Research component implementations and examples
  (4) Get component installation commands
  (5) Choose appropriate Svelte component library
  Triggers: "add components", "UI components", "build UI", "install component", "create form", "create dialog", "svelte components", "shadcn-svelte", "skeleton ui"
---

# Svelte Component Management

## Primary Focus: Svelte Ecosystem

Specialized in Svelte component libraries and their management:
- **shadcn-svelte**: Svelte adaptation of shadcn/ui
- **Skeleton UI**: Modern, accessible Svelte component library
- **Melt UI**: Headless components for Svelte
- **Custom components**: Built from scratch with Tailwind CSS

## Prerequisites

### For Svelte Projects

Verify project setup:
```bash
# Check if SvelteKit project
ls src/routes/ src/lib/
```

### For shadcn-svelte Projects
If using shadcn-svelte:
```bash
npx shadcn-svelte@latest init
```

### For Skeleton UI Projects
If using Skeleton UI:
```bash
npm install @skeletonlabs/skeleton
```

## Quick Add Workflow for Svelte

For simple component additions (e.g., "add a date picker"):

### Option 1: shadcn-svelte
```bash
npx shadcn-svelte@latest add button
npx shadcn-svelte@latest add card
npx shadcn-svelte@latest add dialog
```

### Option 2: Skeleton UI
```bash
npm install @skeletonlabs/skeleton
# Import in app.css: @import '@skeletonlabs/skeleton/theme';
```

### Option 3: Custom Component
Create custom component with Tailwind CSS:
```svelte
<!-- src/lib/components/DatePicker.svelte -->
<script lang="ts">
  import { createEventDispatcher } from 'svelte';

  export let value: Date = new Date();
  export let placeholder = 'Select date';

  const dispatch = createEventDispatcher();
</script>

<input
  type="date"
  bind:value
  {placeholder}
  on:change={(e) => dispatch('change', { value: e.target.value })}
  class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
/>
```

## Complex Build Workflow for Svelte

For multi-component features (e.g., "build a login form"), see [references/workflows.md](references/workflows.md).

**When to use Complex Build:**
- Feature requires 3+ components
- Need component hierarchy planning
- Building complete sections (forms, dashboards, modals)
- Integrating with SvelteKit's form actions and load functions

**Svelte-specific considerations:**
- Use SvelteKit's form actions for form handling
- Leverage progressive enhancement patterns
- Consider accessibility with Svelte's ARIA support
- Use Svelte stores for state management

## Svelte Component Patterns

### Common Component Categories
- **Forms**: `form`, `input`, `select`, `checkbox`, `radio-group`, `textarea`
- **Layout**: `card`, `dialog`, `sheet`, `drawer`, `tabs`, `container`
- **Feedback**: `alert`, `toast`, `skeleton`, `progress`, `spinner`
- **Navigation**: `button`, `dropdown-menu`, `navigation-menu`, `breadcrumb`
- **Data Display**: `table`, `badge`, `avatar`, `accordion`, `carousel`

### Svelte-specific Patterns
- **Form Actions**: Integration with SvelteKit's form handling
- **Progressive Enhancement**: Works without JavaScript, enhanced with it
- **Reactive Components**: Using Svelte's reactivity for dynamic UI
- **Transitions**: Built-in Svelte transitions for smooth animations

### Installation Examples
```bash
# shadcn-svelte
npx shadcn-svelte@latest add button card form

# Skeleton UI
npm install @skeletonlabs/skeleton
# Add to app.css: @import '@skeletonlabs/skeleton/theme';

# Melt UI
npm install @melt-ui/svelte
```

## After Implementation

Always run audit:
```
shadcn___get_audit_checklist
```

## Custom Styling & Theming

Shadcn provides **structural foundation** with default styling. For custom aesthetics:

## Svelte Component Library Ecosystem

### Primary Libraries

**1. shadcn-svelte**
```bash
npx shadcn-svelte@latest init
npx shadcn-svelte@latest add [component-name]
```
- Components in: `src/lib/components/ui/`
- Theme in: `src/app.css`
- Config: `components.json`

**2. Skeleton UI**
```bash
npm install @skeletonlabs/skeleton
```
- Import in: `src/app.css` → `@import '@skeletonlabs/skeleton/theme';`
- Components: Import from `@skeletonlabs/skeleton`
- Theme: CSS variables in `src/app.css`

**3. Melt UI**
```bash
npm install @melt-ui/svelte
```
- Headless components
- Build with Tailwind CSS
- Full accessibility support
- Works with SvelteKit

**4. Custom Components**
- Build from scratch with Tailwind CSS
- Use Svelte transitions and actions
- Integrate with SvelteKit patterns

### Customization Strategies

**For shadcn-svelte:**
1. Modify CSS variables in `src/app.css`
2. Extend Tailwind config for custom themes
3. Override component styles with `class:` directives

**For Skeleton UI:**
1. Use CSS custom properties for theming
2. Leverage Skeleton's theme system
3. Combine with custom Tailwind utilities

**For Custom Components:**
1. Build with Svelte's component syntax
2. Use Tailwind for styling
3. Add Svelte transitions for animations
4. Ensure accessibility with ARIA attributes

**Invoke `frontend-design` skill when:**
- User wants unique/distinctive visual style beyond default theme
- Need custom typography, color schemes, or motion effects
- Building landing pages or marketing sites requiring creative design
- User mentions "custom styling", "unique design", "not generic"

**Workflow for Svelte projects:**
1. Choose appropriate component library (shadcn-svelte, Skeleton, Melt, or custom)
2. Use `shadcn-svelte-management` patterns adapted for Svelte
3. Invoke `frontend-design` for visual customization:
   - Custom CSS variables in `src/app.css`
   - Tailwind theme extensions in `tailwind.config.js`
   - Svelte transitions and animations
   - Typography and color refinements

**Customization targets:**
- `src/app.css` - CSS variables, custom fonts, theme imports
- `tailwind.config.js` - theme colors, fonts, animations
- `src/lib/components/ui/` - component-level overrides
- Component-level `class:` directives for dynamic styling
