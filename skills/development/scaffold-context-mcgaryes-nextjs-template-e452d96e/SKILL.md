---
name: scaffold-context
description: Scaffold a new React Context module inside an existing feature using the Context + useReducer pattern (state, actions, reducer, context, provider, and barrel exports).
---

# Scaffold Context

Scaffold a new React Context module within an existing feature, following the Context + useReducer pattern.

## Usage

```
/scaffold-context <context-name>
```

Example: `/scaffold-context voice-recorder`

## Instructions

Follow these steps to scaffold a new context:

### Step 1: Parse Context Name

The context name is provided in `$ARGUMENTS`. If `$ARGUMENTS` is empty or missing, use `AskUserQuestion` to prompt:

```
What is the name of the context? (use kebab-case, e.g., voice-recorder)
```

### Step 2: Validate Context Name

Ensure the context name:
- Uses kebab-case (lowercase letters and hyphens only)
- Does not start or end with a hyphen
- Is not empty

If invalid, inform the user and ask for a valid name.

### Step 3: Select Target Feature

List all existing features by scanning `features/` directory.

If no features exist, inform the user they need to create a feature first using `/scaffold-feature`.

If only one feature exists, confirm with the user that they want to add the context to that feature.

If multiple features exist, use `AskUserQuestion` to ask which feature to add the context to:

**Question:** "Which feature should this context belong to?"
**Header:** "Feature"
**Options:** List existing feature names (up to 4). If more than 4 features exist, show the 4 most recently modified and include guidance to specify "Other" for unlisted features.

### Step 4: Ensure Contexts Directory Exists

Check if `features/{feature-name}/contexts/` directory exists. If not, create it along with an `index.ts` barrel file:

**contexts/index.ts:**
```typescript
// {Feature Name} Contexts
//
// Add your React Context modules here. Each context should have its own directory:
//
// contexts/
// └── {context-name}/
//     ├── {context-name}-state.tsx    - State interface and initial values
//     ├── {context-name}-actions.tsx  - Action types and interfaces
//     ├── {context-name}-reducer.tsx  - Reducer function
//     ├── {context-name}-context.tsx  - React Context creation
//     └── {context-name}-provider.tsx - Provider component
```

### Step 5: Generate Context Files

Create the context directory at `features/{feature-name}/contexts/{context-name}/`.

Generate the following 6 files:

#### {context-name}-state.tsx

```typescript
export interface {ContextName}State {
  // Add your state properties here
  isLoading: boolean;
  error?: string;
}

export const {contextName}InitialState: {ContextName}State = {
  isLoading: false,
  error: undefined,
};
```

#### {context-name}-actions.tsx

```typescript
export enum {ContextName}ActionType {
  setLoading = "SET_LOADING",
  setError = "SET_ERROR",
  reset = "RESET",
}

export interface SetLoadingAction {
  type: {ContextName}ActionType.setLoading;
  payload: boolean;
}

export interface SetErrorAction {
  type: {ContextName}ActionType.setError;
  payload: string | undefined;
}

export interface ResetAction {
  type: {ContextName}ActionType.reset;
}

export type {ContextName}Action =
  | SetLoadingAction
  | SetErrorAction
  | ResetAction;
```

#### {context-name}-reducer.tsx

```typescript
import { type {ContextName}State, {contextName}InitialState } from "./{context-name}-state";
import { type {ContextName}Action, {ContextName}ActionType } from "./{context-name}-actions";

export function {contextName}Reducer(
  state: {ContextName}State,
  action: {ContextName}Action
): {ContextName}State {
  switch (action.type) {
    case {ContextName}ActionType.setLoading:
      return {
        ...state,
        isLoading: action.payload,
      };

    case {ContextName}ActionType.setError:
      return {
        ...state,
        error: action.payload,
        isLoading: false,
      };

    case {ContextName}ActionType.reset:
      return {contextName}InitialState;

    default:
      return state;
  }
}
```

#### {context-name}-context.tsx

```typescript
import { createContext, type Dispatch } from "react";
import { type {ContextName}State, {contextName}InitialState } from "./{context-name}-state";
import { type {ContextName}Action } from "./{context-name}-actions";

export const {ContextName}Context = createContext<{
  state: {ContextName}State;
  dispatch: Dispatch<{ContextName}Action>;
}>({
  state: {contextName}InitialState,
  dispatch: () => {},
});
```

#### {context-name}-provider.tsx

```tsx
"use client";

import { useReducer, type ReactNode } from "react";
import { {ContextName}Context } from "./{context-name}-context";
import { {contextName}Reducer } from "./{context-name}-reducer";
import { type {ContextName}State, {contextName}InitialState } from "./{context-name}-state";

export interface {ContextName}ProviderProps {
  children: ReactNode;
  initialState?: Partial<{ContextName}State>;
}

export function {ContextName}Provider(props: {ContextName}ProviderProps) {
  const { children, initialState } = props;
  const [state, dispatch] = useReducer(
    {contextName}Reducer,
    { ...{contextName}InitialState, ...initialState }
  );

  return (
    <{ContextName}Context.Provider value={{ state, dispatch }}>
      {children}
    </{ContextName}Context.Provider>
  );
}
```

#### index.ts

```typescript
export { {ContextName}Context } from "./{context-name}-context";
export { {ContextName}Provider } from "./{context-name}-provider";
export type { {ContextName}ProviderProps } from "./{context-name}-provider";
export { {contextName}Reducer } from "./{context-name}-reducer";
export { type {ContextName}State, {contextName}InitialState } from "./{context-name}-state";
export {
  {ContextName}ActionType,
  type {ContextName}Action,
  type SetLoadingAction,
  type SetErrorAction,
  type ResetAction,
} from "./{context-name}-actions";
```

### Step 6: Output Summary

After creating all files, output a summary:

```
Created context: {context-name} in {feature-name}

features/{feature-name}/contexts/{context-name}/
├── {context-name}-state.tsx
├── {context-name}-actions.tsx
├── {context-name}-reducer.tsx
├── {context-name}-context.tsx
├── {context-name}-provider.tsx
└── index.ts

Next steps:
1. Define your state properties in {context-name}-state.tsx
2. Add action types and interfaces in {context-name}-actions.tsx
3. Implement state transitions in {context-name}-reducer.tsx
4. Create a custom hook in hooks/ for convenient context access:

   // hooks/use-{context-name}.ts
   export function use{ContextName}() {
     const { state, dispatch } = useContext({ContextName}Context);
     // Add helper methods that wrap dispatch calls
     return { ...state, /* methods */ };
   }
```

## Naming Conventions

- **context-name**: kebab-case (e.g., `voice-recorder`)
- **ContextName**: PascalCase (e.g., `VoiceRecorder`)
- **contextName**: camelCase (e.g., `voiceRecorder`)

Convert kebab-case to other cases:

| Input (kebab) | PascalCase | camelCase |
|---------------|------------|-----------|
| `voice-recorder` | `VoiceRecorder` | `voiceRecorder` |
| `user-auth` | `UserAuth` | `userAuth` |

Conversion rules:
1. Split on hyphens
2. For PascalCase: capitalize first letter of each word, join without separators
3. For camelCase: lowercase first word, capitalize first letter of subsequent words, join without separators