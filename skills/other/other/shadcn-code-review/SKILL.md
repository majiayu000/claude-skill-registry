---
name: shadcn-code-review
description: Reviews shadcn/ui components for CVA patterns, composition with asChild, accessibility states, and data-slot usage. Use when reviewing React components using shadcn/ui, Radix primitives, or Tailwind styling.
---

# shadcn/ui Code Review

## Quick Reference

| Issue Type | Reference |
|------------|-----------|
| className in CVA, missing VariantProps, compound variants | [references/cva-patterns.md](references/cva-patterns.md) |
| asChild without Slot, missing Context, component composition | [references/composition.md](references/composition.md) |
| Missing focus-visible, aria-invalid, disabled states | [references/accessibility.md](references/accessibility.md) |
| Missing data-slot, incorrect CSS targeting | [references/data-slot.md](references/data-slot.md) |

## Review Checklist

- [ ] `cn()` receives className, not CVA variants
- [ ] `VariantProps<typeof variants>` exported for consumers
- [ ] Compound variants used for complex state combinations
- [ ] `asChild` pattern uses `@radix-ui/react-slot`
- [ ] Context used for component composition (Card, Accordion, etc.)
- [ ] `focus-visible:` states, not just `:focus`
- [ ] `aria-invalid`, `aria-disabled` for form states
- [ ] `disabled:` variants for all interactive elements
- [ ] `sr-only` for screen reader text
- [ ] `data-slot` attributes for targetable composition parts
- [ ] CSS uses `has()` selectors for state-based styling
- [ ] No direct className overrides of variant styles

## Valid Patterns (Do NOT Flag)

These are correct patterns that should NOT be flagged as issues:

- `max-h-(--var)` - correct Tailwind v4 CSS variable syntax (NOT v3 bracket notation)
- `text-[color:var(--x)]` - valid arbitrary value syntax
- Copying shadcn component code into project - intended usage pattern
- Not documenting copied shadcn components - library internals, not custom code
- Using cn() with many arguments - composition is the pattern
- Conditional classes in cn() arrays - valid Tailwind pattern
- Extending primitive components without additional docs - well-known base

## Context-Sensitive Rules

Apply these rules with appropriate context awareness:

- Flag accessibility issues ONLY IF not handled by Radix primitives underneath
- Flag missing aria labels ONLY IF component isn't using accessible radix primitive
- Flag variant proliferation ONLY IF variants could be composed from existing
- Flag component documentation ONLY IF it's custom code, not copied shadcn

## Library Convention Note

shadcn/ui components are designed to be copied and modified. Code review should focus on:
- Custom modifications made to copied components
- Integration with application state/data
- Accessibility in custom usage contexts

Do NOT flag:
- Standard shadcn component internals
- Radix primitive usage patterns
- Default variant implementations

## When to Load References

- Reviewing variant definitions → cva-patterns.md
- Reviewing component composition with asChild → composition.md
- Reviewing form components or interactive elements → accessibility.md
- Reviewing multi-part components (Card, Select, etc.) → data-slot.md

## Review Questions

1. Are CVA variants properly separated from className props?
2. Does asChild composition work correctly with Slot?
3. Are all accessibility states (focus, invalid, disabled) handled?
4. Are data-slot attributes used for component part targeting?
5. Can consumers extend variants without breaking composition?

## Before Submitting Findings

Load and follow [review-verification-protocol](../review-verification-protocol/SKILL.md) before reporting any issue.
