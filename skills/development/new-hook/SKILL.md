---
name: new-hook
description: Creates new custom React hooks following project conventions. Scaffolds TypeScript types, JSDoc documentation, and proper error handling in src/hooks/. References hook-patterns.md for layer-appropriate templates.
disable-model-invocation: true
argument-hint: "[hookName] or [subfolder/hookName]"
---

# Create New Hook

Create a new custom React hook following project conventions.

## Initialization

When invoked:

1. Read `.claude/skills/web3-implementer/hook-patterns.md` for layer-appropriate hook templates
2. Read `.claude/docs/project-rules.md` for project conventions (two-layer pattern, address safety, etc.)
3. Read `.claude/docs/data-patterns.md` for the two-layer hook architecture overview

## Instructions

1. Parse the hook name from `$ARGUMENTS`
2. Ensure the name starts with `use`
3. Determine the file path and layer:
   - `blockchain/useGet*Live.ts` — Transform hooks (Layer 2: wraps Ponder hook + transforms data)
   - `blockchain/useGet*.ts` — Contract read hooks (uses `useReadContract`)
   - `blockchain/use[Action].ts` — Contract write hooks (simulate → write → state machine)
   - `ponder/usePonder*.ts` — Raw Ponder hooks (Layer 1: `usePonderQuery`)
   - If includes `/`, use that subfolder under `src/hooks/`
   - Otherwise, place directly in `src/hooks/`
4. Create the hook file with:
   - Proper TypeScript return types
   - JSDoc documentation
   - `ChainContainer.useContainer()` for chain/wallet state (never wagmi directly)
   - `enabled` guards for conditional queries
   - Error handling where appropriate
5. If the hook needs shared types, add them to `src/types/`

## Template (General)

```tsx
import { useState, useEffect } from "react";

interface UseHookNameParams {
  // Add params here
}

interface UseHookNameReturn {
  // Add return type here
}

/**
 * Description of what this hook does
 * @param params - Hook parameters
 * @returns Hook return value
 */
export const useHookName = (params: UseHookNameParams): UseHookNameReturn => {
  // Hook implementation

  return {
    // Return values
  };
};
```

## Layer-Specific Patterns

See `.claude/skills/web3-implementer/hook-patterns.md` for complete templates for:

- Ponder query hooks (raw data layer)
- Transform hooks (typed domain objects)
- Contract read hooks
- Contract write hooks (simulate → write → state machine)

## Verification

After creating the hook:

```bash
yarn typecheck && yarn lint && yarn prettier && yarn build
```
