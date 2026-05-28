---
name: treido-shadcn-ui
description: shadcn/ui specialist for Treido. Use for Radix composition, CVA variants, component boundaries, and token-safe Tailwind v4 usage. Not for product/business logic.
---

# treido-shadcn-ui

## When to Apply

- Editing or adding `components/ui/*` primitives
- Composing Radix-based UI with variants, slots, and controlled/uncontrolled state
- Reviewing UI code for shadcn boundary drift (app logic leaking into primitives)

## Non-Negotiables (Treido)

- Tailwind v4 tokens only (no palette classes, gradients, arbitrary values)
- Keep `components/ui/*` primitives generic and composable
- App-specific wiring lives outside primitives (e.g. in `components/shared/*` or route components)

## Default Patterns

- Prefer shadcn/ui primitives first; only add bespoke primitives when strictly necessary
- Prefer CVA-style variants for component variants; avoid ad-hoc boolean prop explosion
- Prefer semantic token classes (`bg-background`, `text-foreground`, `border-border`, etc.)

## Output Format (Use This)

When asked to implement/review, respond with:

```md
## Decision
- <what pattern/primitives to use>

## Files
- <file paths to touch>

## Variant Plan
- <variants + defaults>

## Token Plan
- <semantic tokens to use>

## A11y
- <keyboard/focus/aria notes>
```

## References

- `docs/WORKFLOW.md`
- `app/globals.css` (token SSOT)
- `components/ui/AGENTS.md` (boundary rules)
