---
name: container-view-pattern
description: This skill enforces the Container/View pattern for React components. It should be used when creating new components, validating existing components, or refactoring components to follow the separation of concerns pattern where Container handles logic and View handles presentation.
---

# Container/View Pattern

This skill provides guidance and validation for the Container/View component pattern used in this codebase.

## Pattern Overview

The Container/View pattern separates components into two distinct files:

- **Container** (`*Container.tsx`): Handles logic, state, API calls, data fetching, and event handlers
- **View** (`*View.tsx`): Handles rendering UI only, receiving all data and callbacks as props
- **Index** (`index.tsx`): Exports the Container as the default component

## Where This Pattern Applies

The Container/View pattern is **required** in these directories:

| Directory                | Applies | Notes                     |
| ------------------------ | ------- | ------------------------- |
| `features/*/components/` | Yes     | All feature components    |
| `features/*/screens/`    | Yes     | All feature screens       |
| `components/`            | Yes     | Shared components         |
| `screens/`               | Yes     | Shared screens            |
| `components/ui/`         | No      | UI primitives (GlueStack) |
| `components/shared/`     | No      | Simple shared utilities   |
| `components/icons/`      | No      | Icon components           |

## When to Use This Skill

- Creating a new component in any of the directories above
- Validating that existing components follow the pattern
- Refactoring a component to follow the pattern
- Reviewing code for pattern compliance

## Creating a New Component

### Option 1: Use the Skill Generator Script

Run the skill's generator script for any component type:

```bash
python3 .claude/skills/container-view-pattern/scripts/create_component.py <type> <name> [feature]
```

**Component Types:**

| Type              | Command                                                          | Creates in                                      |
| ----------------- | ---------------------------------------------------------------- | ----------------------------------------------- |
| Global component  | `create_component.py global-component PlayerCard`                | `components/PlayerCard/`                        |
| Feature component | `create_component.py feature-component PlayerCard player-kanban` | `features/player-kanban/components/PlayerCard/` |
| Global screen     | `create_component.py global-screen Settings`                     | `screens/Settings/`                             |
| Feature screen    | `create_component.py feature-screen Main dashboard`              | `features/dashboard/screens/Main/`              |


### Option 2: Manual Creation

Create the following directory structure:

```
ComponentName/
├── ComponentNameContainer.tsx
├── ComponentNameView.tsx
└── index.tsx
```

## Container Component Requirements

Container components handle all business logic:

1. **Single View render**: Container must ONLY render its corresponding View component - no other UI elements or components
2. **State management**: Use `useState`, `useReducer`
3. **Data fetching**: Use GraphQL hooks, API calls
4. **Memoization**: Wrap all computed values in `useMemo`
5. **Event handlers**: Wrap all handlers in `useCallback` with proper dependencies
6. **Formatting**: All data transformation and formatting logic
7. **Conditional logic**: Determine what state to pass to View (loading, error, empty flags)

### Container Code Order (enforced by ESLint)

Containers must follow this specific order:

```tsx
const ExampleContainer = () => {
  // 1. Variables, state, useMemo, useCallback (same group)
  const [state, setState] = useState();
  const computed = useMemo(() => state * 2, [state]);
  const handleClick = useCallback(() => {}, []);

  // 2. useEffect hooks
  useEffect(() => {
    // side effects
  }, []);

  // 3. Return statement (always last)
  return <ExampleView />;
};
```

### Container Template

```tsx
import { useCallback, useMemo, useState } from "react";
import ComponentNameView from "./ComponentNameView";

/**
 * Props for the ComponentName component.
 */
interface ComponentNameProps {
  readonly id: string;
}

/**
 * Container component that manages state and logic for ComponentName.
 * @param props - Component properties
 * @param props.id - The unique identifier
 */
const ComponentNameContainer = ({ id }: ComponentNameProps) => {
  // State
  const [isLoading, setIsLoading] = useState(false);

  // Memoized computed values
  const formattedData = useMemo(() => {
    return data?.toUpperCase() ?? "";
  }, [data]);

  // Event handlers wrapped in useCallback
  const handleSubmit = useCallback(() => {
    setIsLoading(true);
  }, []);

  return (
    <ComponentNameView
      formattedData={formattedData}
      isLoading={isLoading}
      onSubmit={handleSubmit}
    />
  );
};

export default ComponentNameContainer;
```

## View Component Requirements

View components are pure presentation:

1. **Arrow function shorthand**: Use `() => (...)` not `() => { return (...); }`
2. **No return statements**: The component body must be a single JSX expression
3. **memo wrapper**: Export with `memo()` for performance optimization
4. **displayName**: Set `ComponentName.displayName = "ComponentName"`
5. **Readonly props**: All props should be marked as `readonly`
6. **No hooks**: View should not contain `useState`, `useEffect`, `useMemo`, etc.
7. **No logic**: All conditional rendering should use ternary expressions in JSX

### View Template

```tsx
import { memo } from "react";

import { Box } from "@/components/ui/box";
import { Text } from "@/components/ui/text";

/**
 * Props for the ComponentNameView component.
 */
interface ComponentNameViewProps {
  readonly formattedData: string;
  readonly isLoading: boolean;
  readonly onSubmit: () => void;
}

/**
 * View component that renders the ComponentName UI.
 * @param props - Component properties
 * @param props.formattedData - Pre-formatted display data
 * @param props.isLoading - Loading state indicator
 * @param props.onSubmit - Submit handler callback
 */
const ComponentNameView = ({
  formattedData,
  isLoading,
  onSubmit,
}: ComponentNameViewProps) => (
  <Box testID="COMPONENT_NAME.CONTAINER">
    {isLoading ? <Text>Loading...</Text> : <Text>{formattedData}</Text>}
  </Box>
);

ComponentNameView.displayName = "ComponentNameView";

export default memo(ComponentNameView);
```

## Index File

Export the Container as the default:

```tsx
export { default } from "./ComponentNameContainer";
```

## Validation

### ESLint Rules

The following ESLint rules enforce the pattern:

| Rule                                              | Description                                   |
| ------------------------------------------------- | --------------------------------------------- |
| `component-structure/enforce-component-structure` | Validates directory structure and file naming |
| `component-structure/no-return-in-view`           | Ensures View uses arrow shorthand             |
| `component-structure/require-memo-in-view`        | Ensures View uses memo and displayName        |
| `component-structure/single-component-per-file`   | One component per file                        |

### Manual Validation

Run the validation script to check a component:

```bash
python3 .claude/skills/container-view-pattern/scripts/validate_component.py <path-to-component-directory>
```

Run ESLint to check all components:

```bash
bun run lint
```

> **Note:** Replace `bun` with your project's package manager (`npm`, `yarn`, `pnpm`) as needed.

## Common Violations

### Container Violations

| Issue                                | Resolution                                                  |
| ------------------------------------ | ----------------------------------------------------------- |
| Rendering UI elements besides View   | Container must ONLY return the corresponding View component |
| Rendering multiple components        | Move all UI to View; Container returns only View            |
| Missing `useMemo` for objects/arrays | Wrap computed values in `useMemo`                           |
| Missing `useCallback` for functions  | Wrap handlers in `useCallback`                              |
| Logic in View component              | Move logic to Container                                     |
| Inline function props                | Create memoized handler                                     |

### View Violations

| Issue                         | Resolution                                        |
| ----------------------------- | ------------------------------------------------- |
| Using block body `{ return }` | Convert to arrow shorthand `() => (...)`          |
| Missing `memo` wrapper        | Add `export default memo(ComponentView)`          |
| Missing `displayName`         | Add `ComponentView.displayName = "ComponentView"` |
| Contains hooks                | Move hooks to Container                           |
| Contains state                | Move state to Container                           |

## Extracting Helper Functions

When View components exceed ESLint's cognitive complexity threshold (28), extract render helper functions. For simple cases, prefer inline JSX:

```tsx
/**
 * Renders the loading skeleton state.
 * @param props - Helper function properties
 * @param props.isDark - Whether dark mode is active
 */
function renderLoadingState(props: { readonly isDark: boolean }) {
  const { isDark } = props;
  return <LoadingSkeleton isDark={isDark} />;
}

const ComponentView = ({ isLoading, isDark }: Props) => (
  <Box>{isLoading ? renderLoadingState({ isDark }) : <Content />}</Box>
);
```

## Event Handler Naming Convention

- **Container**: Use `handle*` prefix (e.g., `handleSubmit`, `handleClick`)
- **View props**: Use `on*` prefix (e.g., `onSubmit`, `onClick`)

```tsx
// Container
const handleSubmit = useCallback(() => { ... }, []);
return <ComponentView onSubmit={handleSubmit} />;

// View
const ComponentView = ({ onSubmit }: Props) => (
  <Button onPress={onSubmit}>Submit</Button>
);
```

## Reference Documentation

For detailed examples and edge cases, read:

- `references/patterns.md` - Common patterns and anti-patterns
- `references/examples.md` - Complete component examples
