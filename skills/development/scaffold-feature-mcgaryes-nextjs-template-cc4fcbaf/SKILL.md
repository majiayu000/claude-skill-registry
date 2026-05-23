---
name: scaffold-feature
description: Scaffold a new feature module with the standard directory structure and optional API, components, hooks, and context boilerplate.
---

# Scaffold Feature

Scaffold a new feature module with the standard directory structure and boilerplate files.

## Usage

```
/scaffold-feature <feature-name>
```

Example: `/scaffold-feature user-management`

## Instructions

Follow these steps to scaffold a new feature:

### Step 1: Parse Feature Name

The feature name is provided in `$ARGUMENTS`. If `$ARGUMENTS` is empty or missing, use `AskUserQuestion` to prompt:

```
What is the name of the feature? (use kebab-case, e.g., user-management)
```

### Step 2: Validate Feature Name

Ensure the feature name:
- Uses kebab-case (lowercase letters and hyphens only)
- Does not start or end with a hyphen
- Is not empty

If invalid, inform the user and ask for a valid name.

### Step 3: Ask Which Modules to Include

Use `AskUserQuestion` with multi-select to ask two questions (API layer and UI layer):

#### Question 1: API Layer Modules

**Question:** "Which API modules should be included?"
**Header:** "API"
**Options:**
1. **API Models** - "TypeScript types, interfaces, enums, and constants"
2. **API Logic** - "Server-side business logic and data fetching functions"

#### Question 2: UI Layer Modules

**Question:** "Which UI modules should be included?"
**Header:** "UI"
**Options:**
1. **Components** - "React UI components with loading, empty, and error states"
2. **Hooks** - "Custom React hooks for data fetching and state management"
3. **Contexts** - "React Context + useReducer for complex shared state"

### Step 4: Generate Directory Structure

Create the feature directory at `features/{feature-name}/`.

For each selected module, create the appropriate subdirectories and files:

#### API Models (if selected)
```
api/models/index.ts
```

**api/models/index.ts:**
```typescript
// {Feature Name} Models
//
// Add your TypeScript interfaces, types, enums, and constants here.
//
// Naming conventions:
// - {entity}.ts - Interface definitions (e.g., user.ts)
// - {entity}-type.ts - Enum definitions (e.g., user-type.ts)
// - {feature}-constants.ts - Constants (e.g., dashboard-constants.ts)
```

#### API Logic (if selected)
```
api/logic/index.ts
```

**api/logic/index.ts:**
```typescript
// {Feature Name} Logic
//
// Add your server-side business logic and data fetching functions here.
// Use `import "server-only"` for functions that access secrets or APIs.
//
// Naming conventions:
// - get-{resource}.ts - Fetch single resource
// - get-all-{resources}.ts - Fetch collections
// - {action}-{resource}.ts - Mutations (e.g., delete-session.ts)
```

#### Components (if selected)
```
components/index.ts
```

**components/index.ts:**
```typescript
// {Feature Name} Components
//
// Add your React components here. Each component should have its own directory:
//
// components/
// └── {component-name}/
//     ├── {component-name}.tsx         - Main component (orchestrator)
//     ├── {component-name}-view.tsx    - View component (optional)
//     ├── {component-name}-loading.tsx - Loading/skeleton state
//     ├── {component-name}-empty.tsx   - Empty state
//     ├── {component-name}-errored.tsx - Error state
//     └── index.ts                     - Barrel exports
```

#### Hooks (if selected)
```
hooks/index.ts
```

**hooks/index.ts:**
```typescript
// {Feature Name} Hooks
//
// Add your custom React hooks here.
//
// Naming conventions:
// - use-{feature}-{purpose}.ts (e.g., use-user-profile.ts)
// - Always include "use client" directive
// - Export params and return value interfaces
```

#### Contexts (if selected)
```
contexts/index.ts
```

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

### Step 5: Output Summary

After creating all files, output a summary:

```
Created feature: {feature-name}

features/{feature-name}/
├── api/
│   ├── logic/
│   │   └── index.ts
│   └── models/
│       └── index.ts
├── components/
│   └── index.ts
└── hooks/
    └── index.ts

Next steps:
1. Add your TypeScript types to api/models/
2. Add server-side logic to api/logic/
3. Create components in components/
4. Create hooks in hooks/
```

Adjust the tree output based on which modules were actually created.