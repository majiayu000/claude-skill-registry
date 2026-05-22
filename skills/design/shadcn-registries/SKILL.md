---
name: shadcn-registries
description: Configure shadcn/ui registries, components.json, and CLI commands. Covers default Radix registry, Base UI registry, and custom registries.
versions:
  shadcn-ui: "2.x"
  shadcn-cli: "latest"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, mcp__shadcn__search_items_in_registries, mcp__shadcn__view_items_in_registries, mcp__shadcn__get_add_command_for_items
references: references/registry-config.md, references/templates/registry-setup.md
related-skills: shadcn-components, shadcn-detection
---

# shadcn Registries

## Agent Workflow (MANDATORY)

Before registry configuration, use `TeamCreate`:

1. **fuse-ai-pilot:explore-codebase** - Find existing components.json
2. **fuse-ai-pilot:research-expert** - Verify latest CLI options via Context7

After: Run **fuse-ai-pilot:sniper** for validation.

---

## Overview

| Registry | Primitives | Style |
|----------|-----------|-------|
| `@shadcn` (default) | Radix UI | `new-york`, `default` |
| `@basecn` | Base UI | `base-vega` |
| Custom | Any | Custom |

---

## Critical Rules

1. **ALWAYS detect PM** before any CLI command (use {runner})
2. **ALWAYS consult MCP** before adding components
3. **NEVER mix** registries in same project
4. **KEEP** components.json in sync with actual primitive
5. **USE CLI** for adding components, never manual copy

---

## Architecture

```
project/
├── components.json         # shadcn/ui configuration
├── components/ui/          # Generated components
└── lib/utils.ts            # Utility functions (cn)
```

-> See [registry-setup.md](references/templates/registry-setup.md) for complete setup

---

## CLI Commands

**ALWAYS use detected package manager** (run `shadcn-detection` first).
`{runner}` = `bunx` | `npx` | `pnpm dlx` | `yarn dlx`

```bash
# Initialize
{runner} shadcn@latest init
{runner} shadcn@latest init --style new-york

# Add components (default registry = Radix)
{runner} shadcn@latest add button dialog select

# Add from Base UI registry
{runner} shadcn@latest add --registry=basecn button dialog
```

### MCP (MANDATORY)

```
mcp__shadcn__search_items_in_registries -> find component
mcp__shadcn__get_add_command_for_items  -> get exact CLI command
```

---

## components.json Structure

```json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "new-york",
  "tailwind": { "config": "tailwind.config.ts", "css": "app/globals.css" },
  "aliases": { "components": "@/components", "utils": "@/lib/utils" }
}
```

-> See [registry-config.md](references/registry-config.md) for full schema

---

## Reference Guide

### Concepts

| Topic | Reference | When to Consult |
|-------|-----------|-----------------|
| **Registry Config** | [registry-config.md](references/registry-config.md) | Setting up components.json |

### Templates

| Template | When to Use |
|----------|-------------|
| [registry-setup.md](references/templates/registry-setup.md) | Initial project setup |

---

## Best Practices

### DO
- Use MCP to check registry before adding
- Keep components.json in sync with actual primitive
- Use CLI for adding, not manual copy

### DON'T
- Mix registries in same project
- Edit component internals without checking registry source
- Skip components.json configuration
