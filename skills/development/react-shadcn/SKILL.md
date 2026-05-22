---
name: react-shadcn
description: shadcn/ui for React with TanStack Form. Use when building UI components, forms, dialogs, tables, toasts, or accessible components.
versions:
  shadcn-ui: 3.8.0
  react: 19
  tailwindcss: 4
user-invocable: true
references: references/installation.md, references/configuration.md, references/theming.md, references/button.md, references/input.md, references/label.md, references/textarea.md, references/card.md, references/select.md, references/checkbox.md, references/switch.md, references/radio-group.md, references/slider.md, references/toggle.md, references/toggle-group.md, references/input-otp.md, references/dialog.md, references/alert-dialog.md, references/sheet.md, references/drawer.md, references/popover.md, references/tooltip.md, references/hover-card.md, references/context-menu.md, references/collapsible.md, references/toast.md, references/alert.md, references/skeleton.md, references/progress.md, references/spinner.md, references/table.md, references/tabs.md, references/accordion.md, references/badge.md, references/avatar.md, references/separator.md, references/scroll-area.md, references/aspect-ratio.md, references/resizable.md, references/carousel.md, references/chart.md, references/dropdown.md, references/command.md, references/breadcrumb.md, references/navigation-menu.md, references/menubar.md, references/sidebar.md, references/pagination.md, references/calendar.md, references/field-patterns.md, references/form-examples.md
related-skills: react-19, react-forms, tailwindcss, solid-react
---

# shadcn/ui for React

Beautiful, accessible components built on Radix UI with Tailwind CSS styling.

## Agent Workflow (MANDATORY)

Before ANY implementation, launch in parallel:

1. **fuse-ai-pilot:explore-codebase** - Analyze existing components and patterns
2. **fuse-ai-pilot:research-expert** - Verify latest shadcn/ui docs via Context7/Exa
3. **mcp__shadcn__*** - Search registry for component availability

After implementation, run **fuse-ai-pilot:sniper** for validation.

---

## Overview

### When to Use

- Building UI components for React applications (Vite, CRA)
- Need accessible, customizable form components (inputs, selects, checkboxes)
- Implementing dialogs, sheets, drawers, or overlay patterns
- Creating data tables with sorting, filtering, and pagination
- Building navigation menus, sidebars, or command palettes
- Need toast notifications or alert feedback components

### Why shadcn/ui

| Feature | Benefit |
|---------|---------|
| Copy/paste model | Components copied to your project, full ownership |
| Radix UI foundation | Accessibility built-in, unstyled primitives |
| Tailwind CSS styling | Utility-first, easy customization |
| TanStack Form ready | Modern form library with Field pattern |
| Lucide icons | Consistent, customizable icon set |

---

## Critical Rules

1. **NEVER create components manually** - Always install with `bunx --bun shadcn@latest add`
2. **TanStack Form only** - NOT React Hook Form for all form implementations
3. **Radix UI primitives** - Components built on Radix (NOT Base UI)
4. **Lucide icons** - Default icon library, NOT Remix icons or others
5. **Field pattern** - Use Field, FieldLabel, FieldError for form fields
6. **SOLID paths** - Components at `@/modules/cores/shadcn/components/ui/`

---

## Architecture

### Component Foundation

- **Radix UI** - Headless, accessible primitives (Dialog, Select, Popover, Tabs)
- **Tailwind CSS v4** - Styling via utility classes, CSS-first config
- **class-variance-authority** - Variant management for component styles
- **clsx + tailwind-merge** - Conditional class composition via `cn()` utility

### Project Structure

Components installed to `@/modules/cores/shadcn/components/ui/` following SOLID architecture. Utils at `@/modules/cores/lib/utils.ts` with `cn()` helper function.

---

## MCP Server Integration

Create `.mcp.json` at project root for Claude Code integration with shadcn registry.

### Available MCP Tools

- `mcp__shadcn__search_items_in_registries` - Search available components
- `mcp__shadcn__view_items_in_registries` - View component source code
- `mcp__shadcn__get_item_examples_from_registries` - Get usage examples
- `mcp__shadcn__get_add_command_for_items` - Get installation commands

See [installation.md](references/installation.md) for complete MCP setup.

---

## Component Categories

| Category | Components | Primary Reference |
|----------|------------|-------------------|
| Setup | Init, configuration, theming, icons | [installation.md](references/installation.md) |
| Forms | Button, Input, Field, Select, Checkbox, Switch, Slider | [field-patterns.md](references/field-patterns.md) |
| Overlay | Dialog, Sheet, Drawer, Popover, Tooltip, HoverCard | [dialog.md](references/dialog.md) |
| Feedback | Alert, Toast (Sonner), Progress, Skeleton, Spinner | [toast.md](references/toast.md) |
| Data Display | Table, Badge, Avatar, Calendar, Chart, Carousel | [table.md](references/table.md) |
| Navigation | Breadcrumb, DropdownMenu, Command, Sidebar, Tabs | [sidebar.md](references/sidebar.md) |
| Layout | Card, Accordion, Separator, ScrollArea, Resizable | [card.md](references/card.md) |

---

## Best Practices

1. **Field components** - Use new Field pattern for consistent form field structure
2. **Client Components** - React apps are client-side by default
3. **Sonner for toasts** - Modern toast notifications over legacy toast
4. **MCP tools first** - Use `mcp__shadcn__*` to explore before implementing
5. **Theming via CSS variables** - Customize colors in `index.css` `:root`
6. **Accessibility** - Rely on Radix UI keyboard navigation and ARIA

---

## Reference Guide

| Need | Reference |
|------|-----------|
| Initial setup | [installation.md](references/installation.md), [configuration.md](references/configuration.md) |
| Form patterns | [field-patterns.md](references/field-patterns.md), [form-examples.md](references/form-examples.md) |
| Theme customization | [theming.md](references/theming.md) |
| Data tables | [table.md](references/table.md) |
| Modal dialogs | [dialog.md](references/dialog.md), [alert-dialog.md](references/alert-dialog.md) |
| Navigation | [sidebar.md](references/sidebar.md), [navigation-menu.md](references/navigation-menu.md) |
