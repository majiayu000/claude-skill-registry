---
name: ui-design
description: Enforces consistent UI within shadcn-svelte + TailwindCSS 4 design system. Use when building ANY app UI — pages, components, forms, dashboards, settings, data display. Prevents style drift and ensures design system compliance.
---

# UI Design System Enforcement

This skill enforces consistency across all application UI. It is the default for all app interface work — dashboards, forms, settings, CRUD, data display. For creative/marketing work, use ultra-frontend instead.

## Hard Rules

1. **shadcn-svelte first.** Never build custom components when shadcn-svelte has one. Before creating anything, check `src/lib/components/ui/` for existing components.
2. **Theme tokens only.** Use CSS variables (`bg-primary`, `text-muted-foreground`, `border-border`) — never raw Tailwind colors (`bg-blue-500`, `text-gray-500`). See the Color section below.
3. **Scan before building.** Before creating any new page or component, find and read an existing similar one in the project. Match its structure, spacing, and patterns. State what you're matching.
4. **One way to do things.** If the project already does X a certain way, do it that way. Don't introduce a second pattern.
5. **Svelte 5 only.** Use `$state`, `$derived`, `$bindable`, `$props`, snippets. No legacy Svelte 4 patterns (stores, `export let`, slots).

## Pre-Build Checklist

Before writing any UI code:

1. **Glob** for similar existing pages/components in the project
2. **Read** at least one to understand established patterns
3. **State** which patterns you're following and why
4. **Check** `src/lib/components/ui/` for relevant shadcn components
5. If no similar code exists, state the conventions you'll establish and why

## Colors & Theme Tokens

### Always Use Semantic Tokens

```
bg-background, bg-foreground
bg-primary, text-primary, bg-primary-foreground
bg-secondary, text-secondary
bg-muted, text-muted-foreground
bg-accent, text-accent-foreground
bg-destructive, text-destructive
bg-success, text-success
border-border, border-input
ring-ring
```

### Status Colors — Use Semantic Tokens with Opacity

```svelte
<!-- CORRECT -->
<span class="bg-success/10 text-success">Active</span>
<span class="bg-destructive/10 text-destructive">Failed</span>
<span class="bg-warning/10 text-warning">Pending</span>
<span class="bg-muted text-muted-foreground">Draft</span>

<!-- WRONG — raw Tailwind colors -->
<span class="bg-green-100 text-green-700">Active</span>
<span class="bg-red-100 text-red-700">Failed</span>
<span class="bg-amber-100 text-amber-700">Pending</span>
```

### Exceptions

- **Email/brand preview components** that render non-themed UI may use hardcoded colors
- **Charts** may use `--chart-1` through `--chart-5` tokens or raw colors for data series differentiation
- **Dynamic brand colors** from database/API (e.g., customer portal branding) use inline `style:` bindings

## Layout Conventions

### Dashboard Content Wrapper

The dashboard layout provides `p-4` padding. Pages within it follow this structure:

```svelte
<div class="flex flex-1 flex-col overflow-auto">
  <div class="w-full px-6 lg:px-8 py-6 space-y-6">
    <!-- Page content -->
  </div>
</div>
```

### Max-Width by Page Type

| Page Type | Max-Width | Example |
|-----------|-----------|---------|
| Forms / Settings | `max-w-3xl mx-auto` | Profile settings, edit forms |
| Detail pages | `max-w-6xl mx-auto` | Organization page, subscription detail |
| Data tables / Dashboards | No max-width | Subscriptions list, dashboard overview |
| Catalog / Grid views | `max-w-7xl mx-auto` or `max-w-screen-xl mx-auto` | Product catalog, feature grid |

### Section Spacing

- **Between major page sections**: `space-y-6`
- **Grid gaps between cards/items**: `gap-6`
- **Tight item groups** (form fields, button groups, related items): `gap-4` or `space-y-4`
- **Within a component** (label to input, icon to text): `gap-2` or `space-y-2`

### Responsive Breakpoints

- `md:` (768px) — two-column layouts
- `lg:` (1024px) — three-column layouts, sidebar shows
- Use `@container` queries when component responsiveness is independent of viewport

## Component Patterns

### Button Variants

| Variant | Use Case |
|---------|----------|
| `default` | Primary action (one per visible area) |
| `outline` | Secondary actions (most common) |
| `ghost` | Tertiary/icon-only actions |
| `destructive` | Danger/delete actions |
| `secondary` | Alternative secondary styling |
| `link` | Text-only navigation-style actions |

### Button Sizes

| Size | Use Case |
|------|----------|
| `default` (h-9) | Standard buttons |
| `sm` (h-8) | Toolbars, table rows, compact areas |
| `lg` (h-10) | Hero/primary call-to-action |
| `icon` (h-9 w-9) | Icon-only buttons |
| `icon-sm` (h-8 w-8) | Compact icon buttons |

### Icons

- **In menus/dropdowns**: `h-4 w-4` with `mr-2` spacing
- **Standalone/page-level**: `h-5 w-5`
- **Feature/empty-state illustrations**: `h-6 w-6` or larger
- **Source**: `@tabler/icons-svelte` (project standard)

### Feedback Patterns

| Feedback Type | Component | When |
|---------------|-----------|------|
| Async operation result | `toast.success()` / `toast.error()` | After API calls, saves, sends |
| Reversible confirmation | `ConfirmationModal` (variant="default") | Pause, resume, send |
| Destructive confirmation | `ConfirmationModal` (variant="destructive") | Delete, cancel, disable |
| Complex confirmation | Custom Dialog with options | Actions requiring reason selection |
| Creation flow | `Sheet` with step tabs | Creating new entities |
| Inline editing | Direct in-page form | Quick field edits |

### Data Display

| Pattern | Component | When |
|---------|-----------|------|
| Tabular data | TanStack Table + shadcn Table primitives | Lists with sorting/selection/pagination |
| Metric cards | Card with header + content | Dashboard KPIs |
| Detail view | DetailPageLayout with sidebar | Entity detail pages |
| Empty state | Empty.Root + Empty.Title + Empty.Description | No data / first-time use |
| Loading | Skeleton components with staggered animation | Initial data load |
| Loading overlay | InlineLoadingOverlay | Refreshing existing data |
| Status indicators | Badge with semantic token colors | Row status, entity state |

### Dropdown Menus

```svelte
<DropdownMenu.Root bind:open={dropdownOpen}>
  <DropdownMenu.Trigger>
    {#snippet child({ props })}
      <Button variant="ghost" size="icon" {...props}>
        <DotsVerticalIcon />
        <span class="sr-only">Open menu</span>
      </Button>
    {/snippet}
  </DropdownMenu.Trigger>
  <DropdownMenu.Content align="end" class="w-48">
    <DropdownMenu.Group>
      <!-- Standard actions first -->
      <DropdownMenu.Item>
        <EyeIcon class="mr-2 h-4 w-4" />View Details
      </DropdownMenu.Item>
      <DropdownMenu.Separator />
      <!-- Destructive actions last -->
      <DropdownMenu.Item variant="destructive">
        <TrashIcon class="mr-2 h-4 w-4" />Delete
      </DropdownMenu.Item>
    </DropdownMenu.Group>
  </DropdownMenu.Content>
</DropdownMenu.Root>
```

## Form Patterns

### When to Use Which

| Context | Pattern | Validation |
|---------|---------|------------|
| Simple inline (login, quick edit) | Native `$state` + manual | Inline checks |
| Creation in Sheet/Dialog | State object + `errorsByPath` | Zod schema, submit-first |
| Settings pages | Store-based + `updateField()` | Store-level validation |
| Server-validated | Formsnap + SvelteKit form actions | Server-side + `fail()` |

### Form Field Spacing

```svelte
<!-- Standard form layout -->
<div class="grid gap-6 md:grid-cols-2">
  <div class="space-y-2">
    <Form.Field>
      <Form.Control>
        {#snippet children({ props })}
          <Form.Label>Field Name</Form.Label>
          <Input {...props} />
        {/snippet}
      </Form.Control>
      <Form.Description>Helper text</Form.Description>
      <Form.FieldErrors />
    </Form.Field>
  </div>
</div>
```

- **Label to input**: `space-y-2` (via Form.Field)
- **Between form fields**: `gap-6` (in grid) or `space-y-4` (in stack)
- **Form sections**: `space-y-6`
- **Submit buttons**: Full-width `w-full` in modals/sheets, right-aligned in page forms

## Page Headers

```svelte
<!-- Standard page header -->
<div class="flex items-center justify-between">
  <div>
    <h1 class="text-2xl font-semibold tracking-tight">{title}</h1>
    <p class="text-muted-foreground">{description}</p>
  </div>
  <div class="flex items-center gap-2">
    <!-- Action buttons -->
  </div>
</div>
```

## What This Skill Does NOT Cover

- **Creative/marketing UI** — use ultra-frontend instead
- **Architectural decisions** (folder structure, service patterns, data layer)
- **Business logic** in components
- **Accessibility beyond what shadcn provides** (shadcn handles ARIA by default)
