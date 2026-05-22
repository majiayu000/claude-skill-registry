---
name: Refactor/Slice File
description: Use this skill when a file exceeds ~350 lines (target) / approaches the 500-line hard cap, or has mixed responsibilities (UI + Logic + Types).
---

# Refactor / Slice File

This skill applies the "Slicing" pattern to reduce complexity and context usage.

## Triggers
- File > ~350 lines (target) or approaching the 500-line hard cap.
- User says "Refactor this large file".
- `AGENTS.md` Mode E.

## Recipe

Don't just move code. Split by responsibility.

### 1. Extract Types
- Create `{ComponentName}.types.ts`
- Move interfaces/enums there.

### 2. Extract Logic (Custom Hook)
- Create `use{ComponentName}.ts`
- Move `useEffect`, `useState`, handlers, and complex logic there.
- Return only what the UI needs (`{ data, handlers, state }`).

### 3. Extract Sub-components
- Identify independent UI blocks (Modals, Lists, Cards).
- Move to separate files in the same folder or `components/subparts`.

### 4. Reassemble
- The main file should look like a "View": mainly JSX/TSX with a single hook call.
- Validates that imports allow the app to run without circular dependencies.

## Example Output Structure
```text
/MyComponent
  /index.tsx       (The main export)
  /MyComponent.tsx (The View)
  /useMyComponent.ts (The Logic)
  /MyComponent.types.ts (The Contract)
```
