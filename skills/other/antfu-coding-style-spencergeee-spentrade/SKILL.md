---
name: antfu-coding-style
description: Opinionated coding style and tooling preferences by Anthony Fu.
category: development
version: 4.1.0-fractal
layer: master-skill
---

# Antfu Coding Style & Philosophy

> **Goal**: Maximal Developer Experience (DX) through minimalism and smart defaults. "Works out of the box."

## 1. Code Organization

- **Single Responsibility**: Keep files small. If you scroll too much, split it.
- **Export**: Use Named Exports for libraries, Default Exports for components.
- **Constants**: Extract magic strings/numbers to `constants.ts`.

## 2. TypeScript Preferences

- **Implicit over Explicit**: Let TS infer types when obvious.
    - *Bad*: `const count: number = 0`
    - *Good*: `const count = 0`
- **Return Types**: Explicitly type return values for library limits (public API), infer for internal functions.
- **No Enums**: Use `const assertion` object or String Unions.
    - `type Mode = 'dark' | 'light'` > `enum Mode { ... }`

## 3. Tooling Stack

- **Package Manager**: `pnpm` (Fast, disk efficient).
- **Runner**: `ni` (NPM/Yarn/PNPM/Bun Agnostic runner).
    - `ni` -> install
    - `nr dev` -> run dev
    - `nu` -> upgrade
- **Testing**: `Vitest` (Fast, Jest compatible, Native ESM).
    - Naming: `*.test.ts`.
    - Verification: Use `toMatchSnapshot()` sparingly, prefer `toMatchInlineSnapshot()`.

## 4. CSS / Styling

- **UnoCSS**: Atomic CSS engine.
- **Attributify**: Use attributes for styles to keep clean class strings.
    - `<div text="red 4xl" hover="text-blue">` (Controversial but preferred by Antfu for clean template).

## 5. Vue.js Specifics

- **Script Setup**: `<script setup lang="ts">`.
- **ReactivityTransform**: Previously experimental, now prefer `ref` with `.value` or explicit `.value` macros if configured.
- **Structure**:
    - `defineProps` and `defineEmits` at the top.
    - `watch` / `computed` grouped together.

---

**The "Antfu" Vibe**:
- Delete dead code immediately.
- If it can be automated, write a script.
- Aesthetics matter: Code should look beautiful.
