---
name: applying-clean-code
description: General syntax and naming rules to keep the codebase maintainable. Use for all code generation.
---

# Clean Code Principles

## When to use this skill
- Naming variables, functions, and files.
- Deciding on function size and complexity.

## Principles
- **Self-Documenting Names**: `isBookingPending` > `status === 1`.
- **DRY (Don't Repeat Yourself)**: If logic is duplicated, move it to a utility or hook.
- **KISS (Keep It Simple, Stupid)**: Avoid over-engineering complex solutions for simple tasks.
- **Constants**: Use `const` over `let`. Use uppercase constants for magic numbers/IDs: `const MAX_GUESTS = 20;`.

## Naming Conventions
- **Components**: PascalCase (`TourCard.tsx`).
- **Functions/Variables**: camelCase (`handleSubmit`).
- **Interfaces**: PascalCase (`TourInfo`).
- **Files**: kebab-case or PascalCase (stay consistent with project structure).

## Instructions
- **Avoid Comments**: Write code so clear that comments are mostly unnecessary. Only comment the "why," not the "what."
