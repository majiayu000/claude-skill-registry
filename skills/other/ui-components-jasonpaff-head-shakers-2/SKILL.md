---
name: ui-components
description: Enforces project UI component conventions when creating or modifying React components, forms, dialogs, and other UI elements. This skill ensures consistent patterns for Radix UI integration, form handling with TanStack Form, test IDs, accessibility, and component composition.
---

# UI Components Skill

## Purpose

This skill enforces the project UI component conventions automatically during UI development. It ensures consistent patterns for Radix UI integration, form handling with TanStack Form, test ID generation, accessibility, and component composition.

## Activation

This skill activates when:

- Creating new components in `src/components/`
- Working with Radix UI primitives
- Implementing forms with TanStack Form
- Building dialogs, dropdowns, or other interactive UI
- Working with UI component variants using CVA

## Workflow

1. Detect UI component work (file path contains `components/` or imports from Radix/form libraries)
2. Load `references/UI-Components-Conventions.md`
3. Also apply `react-coding-conventions` skill
4. Generate/modify code following all conventions
5. Scan for violations of UI patterns
6. Auto-fix all violations (no permission needed)
7. Report fixes applied

## Key Patterns

- Use arrow function components with named exports (`export const Button = () => {}`)
- Use `ComponentProps<'element'>` with `ComponentTestIdProps` for type definitions
- Include `data-slot` attribute on every component element
- Include `data-testid` using `generateTestId()` from `@/lib/test-ids`
- Use `is` prefix for boolean props (`isLoading`, `isDisabled`, `isCondition`)
- Use Radix UI primitives for accessible components
- Use TanStack Form hooks (`useFieldContext`, `useFormContext`) for form handling
- Use CVA for component variants
- Use `$path` from next-typesafe-url for links
- Use `cn` from `@/utils/tailwind-utils` for class merging
- Use `Conditional` component with `isCondition` prop for conditional rendering

## References

- `references/UI-Components-Conventions.md` - Complete UI component conventions
