---
name: scaffold-component
description: Scaffold a new presentational (dumb) component inside an existing feature module, with optional state variants, using shadcn/ui primitives.
---

# Scaffold Component

Scaffold a new component within an existing feature module.

## Usage

```
/scaffold-component <component-name>
```

Example: `/scaffold-component user-profile-card`

## Instructions

Follow these steps to scaffold a new component:

### Step 1: Parse Component Name

The component name is provided in `$ARGUMENTS`. If `$ARGUMENTS` is empty or missing, use `AskUserQuestion` to prompt:

```
What is the name of the component? (use kebab-case, e.g., user-profile-card)
```

### Step 2: Validate Component Name

Ensure the component name:

- Uses kebab-case (lowercase letters and hyphens only)
- Does not start or end with a hyphen
- Is not empty

If invalid, inform the user and ask for a valid name.

### Step 3: Select Target Feature

List all existing features by scanning `features/` directory.

If no features exist, inform the user they need to create a feature first using `/scaffold-feature`.

If only one feature exists, confirm with the user that they want to add the component to that feature.

If multiple features exist, use `AskUserQuestion` to ask which feature to add the component to:

**Question:** "Which feature should this component belong to?"
**Header:** "Feature"
**Options:** List existing feature names (up to 4). If more than 4 features exist, show the 4 most recently modified and include guidance to specify "Other" for unlisted features.

### Step 4: Ask Which State Files to Include

Use `AskUserQuestion` with multi-select to ask:

**Question:** "Which state files should be included?"
**Header:** "States"
**Options:**

1. **Loading** - "Skeleton/loading state shown while data is being fetched"
2. **Empty** - "Empty state shown when there is no data to display"
3. **Errored** - "Error state shown when data fetching fails"
4. **View** - "Separate view component for presentation logic"

### Step 5: Ensure Required shadcn Components Exist

**IMPORTANT:** All feature components MUST be built using shadcn/ui primitives.

#### Required shadcn components by state file:

| State File | Required shadcn Components |
|------------|----------------------------|
| Loading    | `skeleton`                 |
| Errored    | `button`                   |

#### Check and install missing components:

1. Check which shadcn components exist in `components/ui/`
2. For each missing required component, install it using the shadcn MCP server or CLI:
    ```bash
    npx shadcn@latest add <component-name> --yes
    ```
3. Common components to check: `card`, `skeleton`, `button`, `alert`

#### Example installation check:

```bash
# Check if card exists
ls components/ui/card.tsx

# If not found, add it
npx shadcn@latest add card --yes
```

### Step 6: Generate Component Files

Create the component directory at `features/{feature-name}/components/{component-name}/`.

#### Always create these files:

**{component-name}.tsx:**

```
import { type FC } from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

export interface {ComponentName}Props {
  // Add your props here
}

export function {ComponentName}(props: {ComponentName}Props) {
  const {} = props;

  return (
    <Card>
      <CardHeader>
        <CardTitle>{ComponentName}</CardTitle>
        <CardDescription>Component description</CardDescription>
      </CardHeader>
      <CardContent>
        {/* {ComponentName} content */}
      </CardContent>
    </Card>
  );
};
```

**index.ts:**

```
export { {ComponentName} } from "./{component-name}";
export type { {ComponentName}Props } from "./{component-name}";
```

#### Conditionally create state files:

**{component-name}-loading.tsx** (if Loading selected):

```
import { type FC } from "react";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";

export function {ComponentName}Loading() {
  return (
    <Card>
      <CardHeader>
        <Skeleton className="h-6 w-[200px]" />
        <Skeleton className="h-4 w-[300px]" />
      </CardHeader>
      <CardContent className="space-y-2">
        <Skeleton className="h-4 w-full" />
        <Skeleton className="h-4 w-[80%]" />
      </CardContent>
    </Card>
  );
};
```

**{component-name}-empty.tsx** (if Empty selected):

```
import { type FC } from "react";
import { Card, CardContent } from "@/components/ui/card";

export interface {ComponentName}EmptyProps {
  message?: string;
}

export const {ComponentName}Empty: FC<{ComponentName}EmptyProps> = (props: {ComponentName}EmptyProps) => {
  const { message = "No data available" } = props;

  return (
    <Card>
      <CardContent className="flex flex-col items-center justify-center py-12">
        <p className="text-muted-foreground text-center">{message}</p>
      </CardContent>
    </Card>
  );
};
```

**{component-name}-errored.tsx** (if Errored selected):

```
import { type FC } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

export interface {ComponentName}ErroredProps {
  error?: Error | null;
  onRetry?: () => void;
}

export function {ComponentName}Errored(props: {ComponentName}ErroredProps) {
  const { error, onRetry } = props;

  return (
    <Card>
      <CardContent className="flex flex-col items-center justify-center py-12 gap-4">
        <p className="text-destructive text-center">
          Something went wrong{error?.message ? `: ${error.message}` : ""}
        </p>
        {onRetry && (
          <Button onClick={onRetry} variant="outline">
            Try again
          </Button>
        )}
      </CardContent>
    </Card>
  );
};
```

**{component-name}-view.tsx** (if View selected):

```
"use client";

import { type FC } from "react";
import { useState } from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

// Presentational component - receives all data and callbacks via props
// No data-fetching hooks allowed here
export interface {ComponentName}ViewProps {
  // Data props (passed from main component)
  items: unknown[];
  // Callback props (passed from main component)
  onSelect?: (item: unknown) => void;
}

export function {ComponentName}View(props: {ComponentName}ViewProps) {
  const { items, onSelect } = props;

  // UI-only local state is allowed (hover, focus, dropdown visibility)
  const [hoveredIndex, setHoveredIndex] = useState<number | null>(null);

  return (
    <Card>
      <CardHeader>
        <CardTitle>{ComponentName}</CardTitle>
        <CardDescription>Component description</CardDescription>
      </CardHeader>
      <CardContent>
        {/* Presentation markup - render data from props */}
        {items.map((item, index) => (
          <div
            key={index}
            onMouseEnter={() => setHoveredIndex(index)}
            onMouseLeave={() => setHoveredIndex(null)}
            onClick={() => onSelect?.(item)}
          >
            {/* Render item */}
          </div>
        ))}
      </CardContent>
    </Card>
  );
};
```

#### Update index.ts exports

Add exports for all created state files to `index.ts`:

```
export { {ComponentName} } from "./{component-name}";
export type { {ComponentName}Props } from "./{component-name}";

// Add these based on selected states:
export { {ComponentName}Loading } from "./{component-name}-loading";
export { {ComponentName}Empty } from "./{component-name}-empty";
export type { {ComponentName}EmptyProps } from "./{component-name}-empty";
export { {ComponentName}Errored } from "./{component-name}-errored";
export type { {ComponentName}ErroredProps } from "./{component-name}-errored";
export { {ComponentName}View } from "./{component-name}-view";
export type { {ComponentName}ViewProps } from "./{component-name}-view";
```

### Step 7: Output Summary

After creating all files, output a summary:

```
Created component: {component-name} in {feature-name}

features/{feature-name}/components/{component-name}/
├── {component-name}.tsx
├── {component-name}-loading.tsx
├── {component-name}-empty.tsx
├── {component-name}-errored.tsx
├── {component-name}-view.tsx
└── index.ts

Next steps:
1. Define your component props in {component-name}.tsx
2. Implement the component UI using shadcn components
3. If this component needs data fetching, create a companion hook at:
   features/{feature-name}/hooks/use-{component-name}.ts
4. Remember: View components are presentational only - pass all data via props
```

Adjust the tree output based on which files were actually created.

## Naming Conventions

- **component-name**: kebab-case (e.g., `user-profile-card`)
- **ComponentName**: PascalCase (e.g., `UserProfileCard`)

Convert kebab-case to PascalCase by:

1. Splitting on hyphens
2. Capitalizing the first letter of each word
3. Joining without separators

Example: `user-profile-card` → `UserProfileCard`

---

## Dumb Component Pattern

**All scaffolded components must follow the "dumb component" (presentational) pattern.**

### Core Principles

1. **Components are presentational only** - They render UI based on props
2. **All data comes via props** - Data, callbacks, and state are passed down
3. **No data-fetching hooks in components** - No `useSWR`, `useQuery`, or custom data hooks inside view components
4. **Business logic lives in hooks** - Create a companion hook if the component needs data fetching

### Allowed Hooks in Components

View components may only use hooks for **UI-only state**:

- `useState` for local visual state (dropdown open/closed, hover, focus)
- `useRef` for DOM references
- `useCallback`/`useMemo` for UI performance optimization

### When to Create a Companion Hook

If the component needs business logic (data fetching, state management, API calls), create a companion hook in the feature's `hooks/` directory. Hooks
should be task specific. Dont overload hooks with unrelated logic.

```
features/{feature-name}/
├── components/{component-name}/
│   └── {component-name}.tsx          # Makes use of the hook
└── hooks/
    └── use-{hook}.ts                 # Business logic
```

### Example Pattern

```
// Main component calls hook and passes data to view
export function FeatureCard(props: FeatureCardProps) {
  const { itemId } = props;
  const { items, onSelect } = use {hook}({ itemId });
  return <FeatureCardView items={items} onSelect={onSelect} />;
};
```
