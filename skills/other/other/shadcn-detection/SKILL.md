---
name: shadcn-detection
description: Detect whether a project uses Radix UI or Base UI as shadcn/ui primitives. Analyzes package.json, components.json, imports, and data attributes to determine the primitive library in use.
versions:
  shadcn-ui: "2.x"
  radix-ui: "1.x"
  base-ui: "1.x"
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash
references: references/radix-patterns.md, references/baseui-patterns.md, references/detection-algorithm.md, references/templates/detection-script.md
related-skills: shadcn-components, shadcn-migration
---

# shadcn Detection

## Agent Workflow (MANDATORY)

Before detection, use `TeamCreate` to spawn agents:

1. **fuse-ai-pilot:explore-codebase** - Scan project structure
2. **fuse-ai-pilot:research-expert** - Verify latest primitive patterns

After: Use results to configure component workflow.

---

## Overview

| Feature | Description |
|---------|-------------|
| **Package scan** | Detect @radix-ui/* or @base-ui/react |
| **Config check** | Analyze components.json style field |
| **Import analysis** | Scan source for import patterns |
| **Attribute scan** | Check data-state vs data-[open] |
| **Package manager** | Detect bun/npm/pnpm/yarn via lockfile |

---

## Critical Rules

1. **ALWAYS run detection** before any component work
2. **CHECK all 5 signals** for maximum accuracy
3. **HANDLE mixed state** as migration case, never ignore
4. **CACHE result** for session duration, no re-detection needed
5. **DETECT package manager** via lockfile priority order

---

## Architecture

```
project/
├── package.json            # Step 1: deps scan
├── components.json         # Step 2: style field
├── bun.lockb|pnpm-lock.yaml|yarn.lock|package-lock.json  # Step 5: PM
└── src/|components/|app/   # Step 3-4: imports + attrs
```

→ See [detection-script.md](references/templates/detection-script.md) for complete example

---

## 5-Step Detection Algorithm

| Step | Signal | Weight |
|------|--------|--------|
| 1 | `package.json` deps (`@radix-ui/*`, `@base-ui/react`) | 40% |
| 2 | `components.json` style field | 20% |
| 3 | Import patterns in source files | 25% |
| 4 | Data attributes (`data-state` vs `data-[open]`) | 15% |
| 5 | Package manager (lockfile → `bunx`/`npx`/`pnpm dlx`/`yarn dlx`) | - |

---

## Decision Table

| Radix Score | Base UI Score | Result | Action |
|-------------|---------------|--------|--------|
| >50 | 0 | **Radix** | Use Radix patterns |
| 0 | >50 | **Base UI** | Use Base UI patterns |
| >0 | >0 | **Mixed** | Migration needed |
| 0 | 0 | **None** | Fresh setup |

---

## Best Practices

### DO
- Run detection BEFORE any component work
- Check all 5 signals for accuracy
- Handle "mixed" state as migration case

### DON'T
- Assume Radix without checking
- Skip components.json analysis
- Ignore data-attribute signals

---

## Reference Guide

### Concepts

| Topic | Reference | When to Consult |
|-------|-----------|-----------------|
| **Radix Patterns** | [radix-patterns.md](references/radix-patterns.md) | Identifying Radix UI signals |
| **Base UI Patterns** | [baseui-patterns.md](references/baseui-patterns.md) | Identifying Base UI signals |
| **Algorithm** | [detection-algorithm.md](references/detection-algorithm.md) | Understanding scoring logic |

### Templates

| Template | When to Use |
|----------|-------------|
| [detection-script.md](references/templates/detection-script.md) | Running detection on a project |
