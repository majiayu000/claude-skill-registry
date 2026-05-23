---
name: scaffold-hook
description: Scaffold a new custom React hook inside an existing feature module, with templates for data fetching, state management, or utility hooks, and update the feature hooks barrel export.
---

# Scaffold Hook

Scaffold a new custom React hook within an existing feature module.

## Usage

```
/scaffold-hook <hook-name>
```

Example: `/scaffold-hook user-profile`

## Instructions

Follow these steps to scaffold a new hook:

### Step 1: Parse Hook Name

The hook name is provided in `$ARGUMENTS`. If `$ARGUMENTS` is empty or missing, use `AskUserQuestion` to prompt:

```
What is the name of the hook? (use kebab-case, e.g., user-profile)
```

### Step 2: Validate Hook Name

Ensure the hook name:
- Uses kebab-case (lowercase letters and hyphens only)
- Does not start or end with a hyphen
- Is not empty

If invalid, inform the user and ask for a valid name.

### Step 3: Select Target Feature

List all existing features by scanning `features/` directory.

If no features exist, inform the user they need to create a feature first using `/scaffold-feature`.

If only one feature exists, confirm with the user that they want to add the hook to that feature.

If multiple features exist, use `AskUserQuestion` to ask which feature to add the hook to:

**Question:** "Which feature should this hook belong to?"
**Header:** "Feature"
**Options:** List existing feature names (up to 4). If more than 4 features exist, show the 4 most recently modified and include guidance to specify "Other" for unlisted features.

### Step 4: Ask Hook Category

Use `AskUserQuestion` to ask which type of hook to create:

**Question:** "What type of hook should be created?"
**Header:** "Hook Type"
**Options:**
1. **Data Fetching (Recommended)** - "useSWR pattern with loading/error states and refresh capability"
2. **State Management** - "useState/useReducer pattern for local or shared state"
3. **Utility** - "Reusable logic hook like useDebounce or useLocalStorage"

### Step 5: Ensure hooks Directory Exists

Check if `features/{feature-name}/hooks/` directory exists. If not, create it.

### Step 6: Generate Hook File

Create the hook file at `features/{feature-name}/hooks/use-{hook-name}.ts`.

Use the appropriate template based on the selected category:

#### Data Fetching Template

```typescript
"use client";

import { useMemo } from "react";
import useSWR from "swr";

export interface Use{HookName}Params {
  id: string;
}

export interface Use{HookName}ReturnValue {
  data: unknown;
  isLoading: boolean;
  error: Error | null;
  refresh: () => void;
}

export function use{HookName}(
  params: Use{HookName}Params
): Use{HookName}ReturnValue {
  const { id } = params;

  const { data, error, isLoading, mutate } = useSWR<unknown>(
    `/api/{hook-name}/${id}`,
    (url: string) => fetch(url).then((res) => res.json())
  );

  const memoizedData = useMemo(() => data ?? null, [data]);

  return {
    data: memoizedData,
    isLoading,
    error: error ?? null,
    refresh: mutate,
  };
}
```

#### State Management Template

```typescript
"use client";

import { useCallback, useState } from "react";

export interface Use{HookName}State {
  value: unknown;
}

export interface Use{HookName}Params {
  initialValue?: unknown;
}

export interface Use{HookName}ReturnValue {
  state: Use{HookName}State;
  setValue: (value: unknown) => void;
  reset: () => void;
}

export function use{HookName}(
  params: Use{HookName}Params = {}
): Use{HookName}ReturnValue {
  const { initialValue = null } = params;

  const [state, setState] = useState<Use{HookName}State>({
    value: initialValue,
  });

  const setValue = useCallback((value: unknown) => {
    setState({ value });
  }, []);

  const reset = useCallback(() => {
    setState({ value: initialValue });
  }, [initialValue]);

  return {
    state,
    setValue,
    reset,
  };
}
```

#### Utility Template

```typescript
"use client";

import { useEffect, useState } from "react";

export interface Use{HookName}Params {
  // Add parameters here
}

export interface Use{HookName}ReturnValue {
  // Add return values here
}

export function use{HookName}(
  params: Use{HookName}Params
): Use{HookName}ReturnValue {
  // Implement hook logic here

  return {
    // Return values
  } as Use{HookName}ReturnValue;
}
```

### Step 7: Update Feature Index

Check if `features/{feature-name}/hooks/index.ts` exists.

**If it exists**, append the new export:

```typescript
export { use{HookName} } from "./use-{hook-name}";
export type {
  Use{HookName}Params,
  Use{HookName}ReturnValue,
} from "./use-{hook-name}";
```

**If it doesn't exist**, create it with the export:

```typescript
export { use{HookName} } from "./use-{hook-name}";
export type {
  Use{HookName}Params,
  Use{HookName}ReturnValue,
} from "./use-{hook-name}";
```

For State Management hooks, also export the State type:

```typescript
export { use{HookName} } from "./use-{hook-name}";
export type {
  Use{HookName}Params,
  Use{HookName}ReturnValue,
  Use{HookName}State,
} from "./use-{hook-name}";
```

### Step 8: Output Summary

After creating all files, output a summary:

```
Created hook: use-{hook-name} in {feature-name}

features/{feature-name}/hooks/
├── use-{hook-name}.ts
└── index.ts

Hook type: {Data Fetching | State Management | Utility}

Next steps:
1. Update the Params interface with your hook parameters
2. Update the ReturnValue interface with your return types
3. Implement the hook logic
4. Add unit tests in __tests__/use-{hook-name}.test.tsx
```

## Naming Conventions

- **hook-name**: kebab-case (e.g., `user-profile`)
- **HookName**: PascalCase (e.g., `UserProfile`)
- **hookName**: camelCase (e.g., `userProfile`)

Convert kebab-case to PascalCase by:
1. Splitting on hyphens
2. Capitalizing the first letter of each word
3. Joining without separators

Example: `user-profile` → `UserProfile`

The hook function name uses camelCase with `use` prefix: `useUserProfile`

## File Naming

| Element          | Format                           | Example                   |
|------------------|----------------------------------|---------------------------|
| Hook file        | use-{hook-name}.ts               | use-user-profile.ts       |
| Hook function    | use{HookName}                    | useUserProfile            |
| Params interface | Use{HookName}Params              | UseUserProfileParams      |
| Return interface | Use{HookName}ReturnValue         | UseUserProfileReturnValue |
| State interface  | Use{HookName}State               | UseUserProfileState       |