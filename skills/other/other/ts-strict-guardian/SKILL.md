---
name: ts-strict-guardian
description: Enforce strict TypeScript guidelines and safety
version: 1.1.0
tags: [typescript, strict-mode, best-practices]
owner: platform
status: active
---

# Typescript Strict Guardian Skill

## Overview

Enforce strict TypeScript safety and eliminate unsafe typing.

## Usage

```
/ts-strict-guardian
```

## Identity
**Role**: TypeScript Linting Officer
**Objective**: Detect and eliminate type-safety violations such as `any`, implicit `any`, and unsafe casts.

## Policies

### 1. The "No Any" Policy
**Rule**: Explicit `any` is forbidden.
**Detection**: `grep -r ": any" src/`
**Fixes**:
- **Known Shape**: Define an `interface` or `type`.
- **Unknown Shape**: Use `unknown` + Type Guards (Zod parsing or `typeof` checks).
- **Generic**: Use generics `<T>`.

### 2. Strict Null Checks
**Rule**: All nullable fields must be explicit.
- Bad: `function(u: User) { ... } // what if u is null?`
- Good: `function(u: User | undefined) { ... }`

### 3. Exhaustiveness Checking
**Rule**: Unions must be discriminated, and `switch` statements must cover all cases.
**Pattern**:
```typescript
type Action = { type: 'A' } | { type: 'B' };
switch (action.type) {
  case 'A': ...
  case 'B': ...
  default:
    const _exhaustiveCheck: never = action; // Compile error if new type added
}
```

## Workflow

### Audit Mode
**Command**: `/ts-check`
1.  Run project type checker: `npm run typecheck` or `tsc --noEmit`.
2.  Parse output errors.
3.  Group by file.

### Repair Mode
**Command**: `/ts-fix <file>`
1.  Read file.
2.  Identify `any` or casting (`as`).
3.  **Refactor**:
    - **Infer**: Look at usage to derive the type definition.
    - **Define**: Create `interface` at top of file (or `types.ts`).
    - **Apply**: Replace `any` with new Type.

## Constraints
- **Do not** suppress lint errors with `// @ts-ignore` unless it is a compiler bug or specialized library issue (requires explanation comment).
- **Do not** change runtime logic; only type definitions.

## Outputs

- Type safety report and remediation checklist.

## Related Skills

- `/api-contracts-and-validation` - Define safe contracts
