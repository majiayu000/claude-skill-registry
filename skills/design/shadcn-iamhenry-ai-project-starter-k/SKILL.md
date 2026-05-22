---
name: shadcn
description: Add and manage shadcn/ui components via CLI. Use when installing new UI components, building forms with validation, creating modals/dialogs/sheets, adding navigation menus, setting up data tables or charts, or updating existing shadcn components.
---

# shadcn/ui CLI

Quickly add pre-built, customizable React components based on Radix UI and Tailwind CSS.

## Quick Reference

| Command                                | Purpose                          |
| -------------------------------------- | -------------------------------- |
| `npx shadcn@latest add <component>`    | Add single component             |
| `npx shadcn@latest add btn dialog`     | Add multiple components at once  |
| `npx shadcn@latest add -a`             | Add ALL components               |
| `npx shadcn@latest add -o <component>` | Overwrite existing component     |
| `npx shadcn@latest view <component>`   | Preview component before install |
| `npx shadcn@latest init`               | Initialize project (first-time)  |

## Common Component Groups

**Forms**: `button`, `input`, `label`, `select`, `checkbox`, `radio-group`, `switch`, `textarea`, `form`

**Layout**: `card`, `separator`, `tabs`, `accordion`, `collapsible`, `resizable`

**Feedback**: `alert`, `alert-dialog`, `dialog`, `drawer`, `sheet`, `toast`, `sonner`, `tooltip`, `popover`

**Navigation**: `dropdown-menu`, `menubar`, `navigation-menu`, `breadcrumb`, `pagination`, `command`

**Data Display**: `table`, `data-table`, `avatar`, `badge`, `calendar`, `carousel`, `chart`

## Usage Patterns

### Add a single component

```bash
npx shadcn@latest add button
```

### Add multiple related components

```bash
npx shadcn@latest add form input label select
```

### Skip confirmation prompts

```bash
npx shadcn@latest add -y dialog
```

### Overwrite existing component (after shadcn update)

```bash
npx shadcn@latest add -o button
```

### Preview before installing

```bash
npx shadcn@latest view chart
```

### Custom install path

```bash
npx shadcn@latest add button -p src/components/ui
```

## Key Flags

| Flag            | Short | Description              |
| --------------- | ----- | ------------------------ |
| `--yes`         | `-y`  | Skip confirmation prompt |
| `--overwrite`   | `-o`  | Overwrite existing files |
| `--all`         | `-a`  | Install all components   |
| `--path <path>` | `-p`  | Custom destination path  |
| `--silent`      | `-s`  | Suppress output          |

## Project Notes

- Components install to `src/ui/` in this project (configured in `components.json`)
- Uses `@/` path alias for imports
- Tailwind CSS + CVA (class-variance-authority) for variants
- All components are fully customizable after installation

## Troubleshooting

**Component already exists**: Use `-o` flag to overwrite

```bash
npx shadcn@latest add -o button
```

**Missing dependencies**: The CLI auto-installs peer deps, but if issues occur:

```bash
npm install @radix-ui/react-<primitive> class-variance-authority
```

**Path issues**: Check `components.json` for configured paths
