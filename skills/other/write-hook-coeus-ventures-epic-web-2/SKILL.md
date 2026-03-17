---
name: write-hook
description: Write React hooks following the Epic architecture patterns. Use when creating custom hooks for state management, server action calls, optimistic updates, and validation. Triggers on "create a hook", "add a hook", or "write a hook for".
---

# Write Hook

## Overview

This skill creates React hooks that follow the Epic three-layer architecture. Hooks belong to the **Frontend layer** and handle state management, validation, server action calls, and optimistic updates.

## Architecture Context

```
Frontend (Browser): Components -> Hooks -> State (Jotai)
                          |
                          v
Backend (Server): Actions (atomic) OR Routes (streaming)
```

Hooks:
- Run in the browser (Frontend layer)
- Manage state with Jotai atoms
- Validate inputs with Zod
- Call ONE backend entry point (Action or Route, never both)
- Handle optimistic updates and rollback
- NEVER access database or import server-only code

### Backend Entry Point Rule

Each hook calls exactly ONE backend entry point:

**Action** (default):
- Import and call directly
- Most behaviors
- Simpler mental model

**Route**:
- Call via `fetch` or `fetchEventSource`
- Streaming/SSE, webhooks, HTTP semantics needed
- Supports both request/response and streaming

Never call both. Never call multiple endpoints.

## Hook Location and Naming

```
app/[role]/[page]/behaviors/[behavior-name]/
  hooks/
    use-[behavior-name].ts    # Hook file
  actions/
    [action-name].action.ts   # Server action it calls
```

- File names start with `use-` and match the exported function
- Behavior folders use kebab-case

## Hook Specification Format

Follow the Epic Hook specification format:

```markdown
## useHookName(params?: ParamType)

[Short description of what stateful logic this hook encapsulates]

### Parameters
- paramName: Type - description

### State
- stateName: Type
- anotherState: Type

### Returns
- value: Type - description
- action: () => void - description

### Dependencies
- useOtherHook - why it's needed
```

## Implementation Pattern

```typescript
import { useAtom } from 'jotai';
import { useState } from 'react';
import { z } from 'zod';
import { actionName } from './actions/action-name.action';
import { itemsAtom } from '@/app/[role]/[page]/state';

// Validation schema
const InputSchema = z.object({
  name: z.string().min(1).max(100),
});

export function useBehaviorName() {
  const [items, setItems] = useAtom(itemsAtom);
  const [isPending, setIsPending] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAction = async (data: unknown) => {
    // 1. Validate input
    const result = InputSchema.safeParse(data);
    if (!result.success) {
      setError(result.error.errors[0].message);
      return;
    }

    setIsPending(true);
    setError(null);

    // 2. Optimistic update
    const optimisticItem = {
      ...result.data,
      id: crypto.randomUUID(),
      pending: true,
    };
    setItems(prev => [...prev, optimisticItem]);

    try {
      // 3. Call server action
      const response = await actionName(result.data);

      if (response.success && response.data) {
        // 4. Replace optimistic with real data
        setItems(prev =>
          prev.map(item =>
            item.id === optimisticItem.id ? response.data : item
          )
        );
      } else {
        // 5. Rollback on failure
        setItems(prev => prev.filter(item => item.id !== optimisticItem.id));
        setError(response.error || 'Operation failed');
      }
    } catch (err) {
      // 6. Rollback on error
      setItems(prev => prev.filter(item => item.id !== optimisticItem.id));
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsPending(false);
    }
  };

  return {
    items,
    isPending,
    error,
    handleAction,
  };
}
```

## Route Consumption Patterns

### Non-Streaming Route

```typescript
import { useAtom } from 'jotai';
import { useState } from 'react';

export function useRouteBehavior() {
  const [result, setResult] = useAtom(resultAtom);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (input: Input) => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch(`/page/behaviors/behavior-name`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(input),
      });

      const data = await response.json();

      if (data.success) {
        setResult(data.data);
      } else {
        setError(data.error);
      }
    } catch (err) {
      setError('Request failed');
    } finally {
      setIsLoading(false);
    }
  };

  return { result, isLoading, error, handleSubmit };
}
```

### Streaming Route (SSE)

```typescript
import { fetchEventSource } from '@microsoft/fetch-event-source';
import { useAtom } from 'jotai';
import { useState, useRef } from 'react';

export function useStreamingBehavior() {
  const [result, setResult] = useAtom(resultAtom);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const abortControllerRef = useRef<AbortController | null>(null);

  const handleGenerate = async (input: Input) => {
    setIsLoading(true);
    setError(null);
    setResult('');

    abortControllerRef.current = new AbortController();

    await fetchEventSource(`/page/behaviors/behavior-name`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(input),
      signal: abortControllerRef.current.signal,

      onmessage(event) {
        switch (event.event) {
          case 'token':
            setResult(prev => prev + event.data);
            break;
          case 'complete':
            setIsLoading(false);
            break;
          case 'error':
            setError(event.data);
            setIsLoading(false);
            break;
        }
      },

      onclose() {
        setIsLoading(false);
      },

      onerror(err) {
        setError('Connection failed');
        setIsLoading(false);
      },
    });
  };

  const handleCancel = () => {
    abortControllerRef.current?.abort();
    setIsLoading(false);
  };

  return { result, isLoading, error, handleGenerate, handleCancel };
}
```

### Key Differences

| Aspect | Action | Route | Streaming Route |
|--------|--------|-------|-----------------|
| Import | Action function | `fetch` | `fetchEventSource` |
| Call | `await action(input)` | `await fetch(url)` | `await fetchEventSource(url)` |
| Response | Single result | Single result | Multiple events |
| Cancellation | Not supported | Not typical | Via `AbortController` |

---

## Key Patterns

### 1. Validation First
- Always validate input with Zod schemas before operations
- Use `safeParse` and handle validation errors gracefully
- Return early with error messages for invalid input

### 2. Optimistic Updates
- Add temporary records with `pending: true` flag
- Generate temporary IDs with `crypto.randomUUID()`
- Always rollback on failure
- Replace optimistic items with real data on success

### 3. Error Handling
- Set loading states appropriately
- Clear previous errors before new operations
- Provide descriptive error messages
- Use try/catch with proper error type checking

### 4. State Management
- Use Jotai atoms defined in page's `state.ts`
- Return consistent object shape: `{ data, isPending, error, handlers }`
- Keep state updates atomic and predictable

### 5. Server Action Calls
- Import actions from `./actions/[action-name].action`
- Handle standard response: `{ success: boolean, data?: T, error?: string }`
- Never call actions directly from components

## Constraints

- NEVER import database clients or models
- NEVER call more than one backend entry point (action or route)
- NEVER put business logic in hooks - that belongs in actions/routes
- ALWAYS include both loading and error states
- ALWAYS validate input before calling backend
- ALWAYS implement optimistic updates for better UX (actions)
- ALWAYS support cancellation for streaming behaviors (routes)

## Example Specification

```markdown
## useCreateProject()

Entry point for the Create Project behavior. Validates input, performs optimistic updates, and calls the server action.

### State
- isLoading: boolean
- error: string | null

### Returns
- handleCreateProject: (name: string) => Promise<void> - triggers the behavior
- isLoading: boolean - submission in progress
- error: string | null - current error message

### Dependencies
- useSetAtom(projectsAtom) - for optimistic updates

### Example: Create project successfully

#### PreState
projectsAtom: []
isLoading: false
error: null

#### Steps
* Call: handleCreateProject("New Project")
* Returns: void

#### PostState
projectsAtom: [{ id: "1", name: "New Project", status: "draft", pending: false }]
isLoading: false
error: null

### Example: Reject empty name

#### PreState
projectsAtom: []
isLoading: false
error: null

#### Steps
* Call: handleCreateProject("")
* Throws: "Name is required"

#### PostState
projectsAtom: []
isLoading: false
error: "Name is required"
```

## Test Generation

Generate test files at `[behavior-path]/tests/use-[behavior-name].test.tsx`.

### Test Structure

```typescript
import { describe, it, expect } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { Provider } from 'jotai';
import { useHydrateAtoms } from 'jotai/utils';
import { useBehaviorName } from '../use-[behavior-name]';
import { itemsAtom } from '@/app/[role]/[page]/state';

// Helper to set initial atom state
function TestProvider({ initialValues, children }) {
  return (
    <Provider>
      <HydrateAtoms initialValues={initialValues}>{children}</HydrateAtoms>
    </Provider>
  );
}

describe('useBehaviorName', () => {
  it('should [behavior] when [condition]', async () => {
    // PreState -> Initial atom values
    const wrapper = ({ children }) => (
      <TestProvider initialValues={[[itemsAtom, []]]}>
        {children}
      </TestProvider>
    );

    const { result } = renderHook(() => useBehaviorName(), { wrapper });

    // Steps -> Execute handler
    await act(async () => {
      await result.current.handleAction({ name: 'New Item' });
    });

    // PostState -> Verify state changes
    expect(result.current.isLoading).toBe(false);
    expect(result.current.error).toBeNull();
  });
});
```

### Translation Rules

| Spec | Test |
|------|------|
| PreState (atoms) | Initial atom values in TestProvider |
| `Call:` | `await result.current.handler(...)` |
| `Returns:` | Verify handler completes |
| `Throws:` | `expect(result.current.error).toBe(...)` |
| PostState (atoms) | `expect(result.current.state).toBe(...)` |

### Principles

- Test state transitions, not database
- Mock server actions if needed (hooks don't touch DB directly)
- Start with ONE test (happy path)
