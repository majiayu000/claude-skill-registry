---
name: architecting-components
description: Defines rules for Atomic Design and separating logic from UI. Use when creating new components in the src directory.
---

# Component Design Architecture

## When to use this skill
- Structuring the `components/` directory.
- Deciding where to place logic (Server vs Client).

## Folder Structure
- `components/ui/`: Base shadcn/custom elements (Buttons, Inputs).
- `components/shared/`: Reusable across multiple pages (Navbar, Footer).
- `components/features/`: Complex logic-heavy components (TourCard, BookingForm).

## Design Rules
- **Dumb UI**: Pure presentational components with props.
- **Smart Logic**: Components or Server Pages that fetch data or handle state.
- **Colocation**: Keep test files and local styles near the component.

## Instructions
- **RSC First**: Use Server Components for data fetching. Use `'use client'` only when Interactivity (hooks, event listeners) is needed.
