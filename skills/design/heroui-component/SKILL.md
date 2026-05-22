---
name: heroui-component
description: Scaffolds new HeroUI v3 React components using compound component patterns. Enforces named exports, onPress handlers, and direct imports from @heroui/react. Use when creating new UI components.
---

# HeroUI Component Scaffolding Skill

Creates new components following HeroUI v3 Beta 3 compound patterns.

## Before Creating Any Component

**MANDATORY**: Use HeroUI MCP tools first:

1. `mcp_heroui-react_list_components` — Check if component exists
2. `mcp_heroui-react_get_component_info` — Understand compound anatomy
3. `mcp_heroui-react_get_component_props` — Get TypeScript types
4. `mcp_heroui-react_get_component_examples` — See correct usage

## Decision Tree

```text
Does HeroUI v3 have it?
├─ YES → Import directly from @heroui/react (NO wrappers!)
├─ ALMOST → Extend with tv() variants or composition
└─ NO → Only then build custom (with justification)
```

## Component Template

```tsx
// src/components/{ComponentName}.tsx

import { Card, Button } from "@heroui/react";
import { tv } from "tailwind-variants";

interface {ComponentName}Props {
    title: string;
    onAction?: () => void;
}

const styles = tv({
    base: "p-4",
    variants: {
        variant: {
            default: "",
            highlighted: "ring-2 ring-primary",
        },
    },
});

export function {ComponentName}({ title, onAction }: {ComponentName}Props) {
    return (
        <Card className={styles()}>
            <Card.Content>
                <h3 className="text-lg font-semibold">{title}</h3>
                {onAction && (
                    <Button onPress={onAction} variant="primary">
                        Action
                    </Button>
                )}
            </Card.Content>
        </Card>
    );
}
```

## Rules (from dev_instruction_v3.md)

| Rule | Example |
|------|---------|
| Named exports only | `export function ComponentName()` |
| Use onPress | `<Button onPress={handler}>` |
| Direct imports | `import { Button } from "@heroui/react"` |
| Compound patterns | `<Card.Content>`, `<Modal.Body>` |
| Strict typing | Define `interface Props` |
| No any types | Use proper TypeScript types |

## Examples

See `resources/` for reference implementations:

- `resources/card-example.tsx` — Card compound pattern
- `resources/modal-example.tsx` — Modal compound pattern
