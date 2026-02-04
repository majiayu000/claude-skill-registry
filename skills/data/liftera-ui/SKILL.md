---
name: liftera-ui
description: >
  Liftera UI conventions: Gluestack UI + @acme/ui shared components.
  Trigger: When creating or modifying shared UI components, design system primitives, or cross-platform styling in packages/ui.
license: Apache-2.0
metadata:
  author: liftera
  version: "1.0"
  scope: [root, ui]
  auto_invoke: "Creating/modifying shared UI components"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Task
---

## Source of Truth (REQUIRED)

- **ALWAYS** treat `packages/ui` as the source of truth for reusable UI.
- **NEVER** duplicate components across `apps/web` and `apps/mobile`.

## Component Placement (REQUIRED)

- **ALWAYS** put Gluestack primitives/wrappers under `packages/ui/src/gluestack/*`.
- **ALWAYS** put project components under `packages/ui/src/components/*`.
- **ALWAYS** export components through stable entrypoints (avoid deep imports across apps/packages).

## Cross-Platform Constraints (REQUIRED)

- **ALWAYS** ensure components work in both React Native and React Native Web unless explicitly documented.
- **NEVER** use DOM-only APIs inside shared UI components.
- **ALWAYS** use platform files when needed (`*.native.tsx`, `*.web.tsx`).

## Styling Rules

- **ALWAYS** use NativeWind/Tailwind utility classes consistently.
- **ALWAYS** keep variants predictable (small set of variants, explicit defaults).

## Imports & Usage

- **ALWAYS** import shared components via the package name (example from README):
  - `@acme/ui/gluestack/*`
  - `@acme/ui/components/*`
