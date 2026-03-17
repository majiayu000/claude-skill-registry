---
name: shadcn-migration
description: Migration guide between Radix UI and Base UI primitives for shadcn/ui. Covers step-by-step migration, API transformations, and validation checklists.
versions:
  shadcn-ui: "2.x"
  radix-ui: "1.x"
  base-ui: "1.x"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task
references: references/radix-to-baseui.md, references/baseui-to-radix.md, references/templates/migration-dialog.md
related-skills: shadcn-detection, shadcn-components
---

# shadcn Migration

## Agent Workflow (MANDATORY)

Before migration, use `TeamCreate` to spawn agents:

1. **fuse-ai-pilot:explore-codebase** - Inventory all affected components
2. **fuse-ai-pilot:research-expert** - Verify migration patterns via Context7

After: Run **fuse-ai-pilot:sniper** for validation.

---

## Overview

| Feature | Description |
|---------|-------------|
| **Radix -> Base UI** | Migrate from legacy to new primitives |
| **Base UI -> Radix** | Migrate to established primitives |
| **API mapping** | Complete transformation table |
| **Validation** | Post-migration checklist |

## Critical Rules

1. **ALWAYS run detection** before starting migration
2. **ALWAYS create backup** branch before migration
3. **MIGRATE one component** type at a time
4. **UPDATE CSS selectors** along with JSX changes
5. **RUN tests** after each component migration

## Architecture

```
Migration order (leaf components first):
1. Tooltip, Switch, Checkbox (simple)
2. Accordion, Tabs (medium)
3. Dialog, Select, Popover, Menu (complex)
```

-> See [migration-dialog.md](references/templates/migration-dialog.md) for complete example

---

## Pre-Migration Checklist

```
[ ] Run shadcn-detection to confirm current primitive
[ ] Create backup branch (git checkout -b pre-migration)
[ ] Inventory all affected files (Grep for imports)
[ ] Review component-specific API changes
[ ] Plan migration order (leaf components first)
```

---

## Migration Workflow

```
1. DETECT  -> Run shadcn-detection skill
2. BACKUP  -> Create git branch
3. INVENTORY -> List all affected components
4. TRANSFORM -> Apply API changes per component
5. VALIDATE -> Run tests + sniper check
```

---

## Key API Changes

| Aspect | Radix | Base UI |
|--------|-------|---------|
| Composition | `asChild` | `render` prop |
| Dialog content | `DialogContent` | `Dialog.Popup` |
| Dialog overlay | `DialogOverlay` | `Dialog.Backdrop` |
| Positioning | Built-in | Separate `Positioner` |
| Accordion body | `AccordionContent` | `Accordion.Panel` |
| Data attrs | `data-state="open"` | `data-[open]` |
| Package | Multiple `@radix-ui/*` | Single `@base-ui/react` |

---

## Best Practices

### DO
- Migrate one component type at a time
- Run tests after each component migration
- Update CSS selectors along with JSX
- Remove unused Radix packages after migration

### DON'T
- Migrate all components at once
- Skip detection step
- Leave mixed APIs in production
- Forget to update data-attribute CSS selectors

## Reference Guide

### Concepts

| Topic | Reference | When to Consult |
|-------|-----------|-----------------|
| **Radix -> Base UI** | [radix-to-baseui.md](references/radix-to-baseui.md) | Migrating from Radix |
| **Base UI -> Radix** | [baseui-to-radix.md](references/baseui-to-radix.md) | Migrating to Radix |

### Templates

| Template | When to Use |
|----------|-------------|
| [migration-dialog.md](references/templates/migration-dialog.md) | Complete migration example |
