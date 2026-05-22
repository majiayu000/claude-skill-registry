---
name: create-cloud-function
description: Step-by-step procedure for creating a new Firebase Cloud Function in the Nx monorepo. Use when adding a new function.
---

# Create a New Cloud Function

## When to Use

Use this skill when you need to add a new Firebase Cloud Function to the project. CI/CD will NOT deploy your function if the naming pattern is wrong.

## Instructions

Follow these steps exactly:

### 1. Copy an existing function library

```bash
# DO NOT use nx generate - it creates wrong structure
cp -r libs/firebase/maple-functions/get-artists libs/firebase/maple-functions/{my-new-function}
```

### 2. Update project.json

```json
{
  "name": "firebase-maple-functions-{my-new-function}",
  "$schema": "../../../../node_modules/nx/schemas/project-schema.json",
  "sourceRoot": "libs/firebase/maple-functions/{my-new-function}/src",
  "projectType": "library",
  "tags": ["scope:firebase", "type:feature"],
  "targets": {}
}
```

The project name **MUST** follow the pattern `firebase-maple-functions-{function-name}`. This is required for CI/CD detection.

### 3. Update tsconfig.lib.json

Point `include` to the new source directory.

### 4. Create the function

Write your function in `src/lib/{my-new-function}.ts`.

### 5. Add path alias to tsconfig.base.json

```json
"@maple/firebase-maple-functions/{my-new-function}": [
  "libs/firebase/maple-functions/{my-new-function}/src/index.ts"
]
```

### 6. Export from the functions entry point

In `apps/functions/src/index.ts`:

```typescript
export { myNewFunction } from '@maple/firebase-maple-functions/{my-new-function}';
```

### 7. Validate

```bash
npx nx show projects | grep firebase-maple-functions-{my-new-function}
```

## Common Mistakes

- **Wrong**: `my-new-function` (no prefix, CI won't deploy)
- **Wrong**: `maple-functions-my-new-function` (wrong prefix, CI won't deploy)
- **Correct**: `firebase-maple-functions-my-new-function`

## Post-Creation

After creating the function:
1. Add unit tests using `vi.mock()` to mock repositories (see ADR-017)
2. Update `docs/reference/deployed-functions.md` with the new function
3. Update `docs/reference/implementation-status.md` if part of a tracked feature
