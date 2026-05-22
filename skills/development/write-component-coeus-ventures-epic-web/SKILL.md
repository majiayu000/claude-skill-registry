---
name: write-component
description: Write React components following the Epic architecture patterns. Use when creating page components, UI components, or refactoring components to follow the three-layer architecture. Triggers on "create a component", "add a component", or "write a component for".
---

# Write Component

## Overview

This skill creates React components that follow the Epic three-layer architecture. Components belong to the **Frontend layer** and handle UI rendering only - all logic is delegated to hooks.

## Architecture Context

```
Frontend (Browser): Components -> Hooks -> State (Jotai)
```

Components:
- Only render UI and consume hooks
- NO direct server actions or data fetching
- NO business logic
- Use TypeScript interfaces for props
- MUST add `data-testid` attributes for testing

## Component Location

```
app/[role]/[page]/
  page.tsx                    # Next.js page
  state.ts                    # Jotai atoms
  components/                 # Page-specific components
    component-name.tsx
```

## Component Specification Format

Follow the Epic Component specification format from `docs/Epic.md`:

```markdown
# ComponentName

[Short description of what this component renders]

## Props
- propName: Type - description

## State

### Local
- localState: Type

### Shared
- sharedState: Type - via atomName

## Children
- ChildComponent
- AnotherChild
```

## Implementation Pattern

```typescript
'use client';

import { useBehaviorName } from './behaviors/behavior-name/hooks/use-behavior-name';

interface ComponentNameProps {
  onSuccess?: (data: DataType) => void;
}

export function ComponentName({ onSuccess }: ComponentNameProps) {
  const { items, isPending, error, handleAction } = useBehaviorName();

  if (isPending) {
    return <div data-testid="loading-spinner">Loading...</div>;
  }

  if (error) {
    return <div data-testid="error-message">{error}</div>;
  }

  return (
    <div data-testid="component-container">
      <div data-testid="items-list">
        {items.map(item => (
          <div key={item.id} data-testid={`item-card-${item.id}`}>
            {item.name}
          </div>
        ))}
      </div>
      <button
        data-testid="action-button"
        onClick={() => handleAction()}
      >
        Action
      </button>
    </div>
  );
}
```

## Test ID Guidelines

### Always Add data-testid To:

1. **Interactive Elements**:
```tsx
<button data-testid="add-item-button">Add</button>
<input data-testid="item-name-input" />
<select data-testid="item-status-select" />
```

2. **State-Dependent Elements**:
```tsx
<div data-testid="items-list">{/* list */}</div>
{isLoading && <div data-testid="loading-spinner" />}
{error && <div data-testid="error-message">{error}</div>}
<span data-testid="item-count">{items.length}</span>
```

3. **Form Elements and Containers**:
```tsx
<form data-testid="add-item-form" />
<dialog data-testid="edit-item-modal" />
```

### Test ID Naming Conventions

- **Buttons**: `[action]-[entity]-button` (e.g., `add-problem-button`)
- **Inputs**: `[entity]-[field]-input` (e.g., `problem-title-input`)
- **Lists**: `[entity-plural]-list` (e.g., `problems-list`)
- **Cards/Items**: `[entity]-card-[id]` (e.g., `problem-card-123`)
- **Modals**: `[action]-[entity]-modal` (e.g., `edit-problem-modal`)
- **Forms**: `[action]-[entity]-form` (e.g., `add-problem-form`)
- **States**: `loading-spinner`, `error-message`, `success-toast`
- **Counts**: `[entity]-count` (e.g., `problem-count`)

## State Management

Define Jotai atoms in page's `state.ts`:

```typescript
import { atom } from 'jotai';

export interface Item {
  id: string;
  name: string;
  pending?: boolean;  // For optimistic updates
}

export const itemsAtom = atom<Item[]>([]);
export const isLoadingAtom = atom(false);
```

## Constraints

- NEVER import database clients in components
- NEVER call server actions directly - use hooks
- NEVER put business logic in components
- NEVER access window object in server components
- ALWAYS delegate state management to hooks
- ALWAYS add data-testid for interactive and state elements

## Example Specification

```markdown
# CreateProjectForm

Renders the form used to create a new project with a name input and submit button.

## Props
- onSuccess: (project: Project) => void - optional callback after creation

## State

### Local
- (none - delegated to hook)

### Shared
- projects: Project[] - via useProjects atom

## Children
- TextInput
- SubmitButton
```
