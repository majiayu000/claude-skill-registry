---
name: design-dna-skill
description: >
  Skill describing how to interpret, enforce, and evolve design-dna.json across
  projects. Used by design-system-architect, builders, and gate agents.
---

# Design-DNA Skill – Tokens & Patterns

This skill provides shared understanding of **design-dna** for all lanes.

It is used by:
- `design-system-architect`
- Implementation agents (e.g. `nextjs-builder`, `expo-builder`) when applying tokens
- Gate agents (`nextjs-standards-enforcer`, design QA) when checking usage

## Core Concepts

- `design-dna.json` encodes:
  - Color palette + semantic roles,
  - Typography scale and roles,
  - Spacing grid,
  - Named patterns (cards, layouts, shells, etc.).
- It is the **law** for UI work: where tokens exist, ad-hoc values are forbidden.

## Usage Pattern

1. When reading design-dna:
   - Identify available roles for:
     - Colors (primary, secondary, accent, surface, etc.),
     - Typography (display, heading, body, caption),
     - Spacing (base grid, section spacing, gaps),
     - Patterns (hero, card grid, dashboard shell, etc.).
   - Note any documented minimums or constraints (e.g., minimum font size).

2. When applying tokens in implementation:
   - Map design-dna roles to the project's styling tools:
     - CSS variables,
     - Utility classes,
     - Component variants.
   - Avoid creating new arbitrary values when tokens already cover the need.

3. When enforcing tokens in gates:
   - Treat:
     - Inline styles and raw hex values as hard violations when tokens exist,
     - Spacing and typography outside the defined scales as violations,
     - Overuse/misuse of accent colors as design-dna violations if documented.

This skill ensures all agents reason about design-dna in a consistent way and
know when to consult project design documentation for deeper schema and examples.
