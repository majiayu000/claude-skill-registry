---
name: shadcn-management
description: |
  Manage shadcn/ui components using MCP tools. Use when user needs to:
  (1) Add new shadcn components to a project
  (2) Build complex UI features requiring multiple components
  (3) Research component implementations and examples
  (4) Get component installation commands
  Triggers: "add shadcn", "shadcn component", "build UI with shadcn", "install component", "create form", "create dialog"
---

# Shadcn Component Management

## Prerequisites

Verify project setup:
```
shadcn___get_project_registries
```
If no components.json exists, instruct user: `npx shadcn@latest init`

## Quick Add Workflow

For simple component additions (e.g., "add a date picker"):

1. **Search** - Find component in registry:
   ```
   shadcn___search_items_in_registries(registries, query)
   ```

2. **View** - Get implementation details:
   ```
   shadcn___view_items_in_registries(items: ["@shadcn/component-name"])
   ```

3. **Examples** - Get usage demo:
   ```
   shadcn___get_item_examples_from_registries(registries, query: "component-demo")
   ```

4. **Install** - Get add command:
   ```
   shadcn___get_add_command_for_items(items: ["@shadcn/component-name"])
   ```

5. **Output** - Provide installation command and example code

## Complex Build Workflow

For multi-component features (e.g., "build a login form"), see [references/workflows.md](references/workflows.md).

**When to use Complex Build:**
- Feature requires 3+ components
- Need component hierarchy planning
- Building complete sections (forms, dashboards, modals)

## Component Naming Patterns

Common search queries:
- Forms: `form`, `input`, `select`, `checkbox`, `radio-group`
- Layout: `card`, `dialog`, `sheet`, `drawer`, `tabs`
- Feedback: `alert`, `toast`, `skeleton`, `progress`
- Navigation: `button`, `dropdown-menu`, `navigation-menu`

Example queries for demos: `form-demo`, `card-with-form`, `dialog-demo`

## After Implementation

Always run audit:
```
shadcn___get_audit_checklist
```

## Custom Styling & Theming

Shadcn provides **structural foundation** with default styling. For custom aesthetics:

**Invoke `frontend-design` skill when:**
- User wants unique/distinctive visual style beyond default shadcn theme
- Need custom typography, color schemes, or motion effects
- Building landing pages or marketing sites requiring creative design
- User mentions "custom styling", "unique design", "not generic"

**Workflow:**
1. Use `shadcn-management` for component structure and composition
2. Invoke `frontend-design` for visual customization:
   - Custom CSS variables in `globals.css`
   - Tailwind theme extensions in `tailwind.config.js`
   - Animation and micro-interaction enhancements
   - Typography and color refinements

**Customization targets:**
- `@/app/globals.css` - CSS variables, custom fonts
- `tailwind.config.js` - theme colors, fonts, animations
- Component-level className overrides
