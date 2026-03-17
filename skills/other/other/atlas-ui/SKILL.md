---
name: atlas-ui
description: Atlas design system knowledge - components, patterns, and theming
disable-model-invocation: true
---

# Atlas UI Design System

## Component Library

Atlas uses shadcn/ui as the base with custom branded components in `client/src/components/atlas/`.

### Available Base Components (shadcn/ui)

Accordion, AlertDialog, AspectRatio, Avatar, Checkbox, Collapsible, ContextMenu, Dialog, DropdownMenu, HoverCard, Label, Menubar, NavigationMenu, Popover, Progress, RadioGroup, ScrollArea, Select, Separator, Slider, Slot, Switch, Tabs, Toast, Toggle, ToggleGroup, Tooltip

### Custom Atlas Components

Located in `client/src/components/atlas/`:
- Custom branded variants of base components
- Enterprise-specific UI patterns

### Utility Functions

- `cn()` from `@/lib/utils` — merges Tailwind classes (clsx + tailwind-merge)
- `class-variance-authority` (cva) — component variant definitions

## Theming

- Dark/light mode via `next-themes`
- CSS custom properties for colors
- Tailwind config in `tailwind.config.ts`

## Icons

- Use `lucide-react` for all icons
- Import: `import { IconName } from "lucide-react"`

## Forms

- React Hook Form + Zod for validation
- Use `@hookform/resolvers/zod` for schema integration
- Pattern: define Zod schema → create form with useForm → render with Form components

## Data Display

- Charts: `recharts` library
- Tables: custom implementations with pagination
- PDF export: `jspdf` + `jspdf-autotable`
- Excel export: `xlsx` library
