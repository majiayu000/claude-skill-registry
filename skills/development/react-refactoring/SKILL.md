---
name: react-refactoring
description: Guide for refactoring complex React/Next.js components to be clean, modular, and maintainable. Use when code is too long (>200 lines), complex, or hard to maintain.
---

# React Component Refactoring Skill

This skill provides a systematic approach to refactoring complex React components. The goal is to transform monolithic, tangled code into clean, modular, and maintainable structures, specifically targeting code length and structure issues.

## When to Use

Trigger this skill when you encounter:
1.  **Excessive Length**: File size exceeds 200-300 lines.
2.  **Tangled Logic**: Business logic, API calls, and state management are mixed directly with UI rendering.
3.  **Complex State**: Multiple `useState` or `useEffect` calls make the flow hard to follow.
4.  **Deep Nesting**: Render methods contain deeply nested conditionals or loops.
5.  **Cognitive Overload**: The component is difficult to read or understand quickly.

## Core Principles

1.  **Single Responsibility**: Each component or hook should do one thing well.
2.  **Separation of Concerns**: Strictly separate View (JSX/UI) from Logic (State/Effects/Handlers).
3.  **Composition**: Build complex interfaces by composing smaller, focused sub-components.
4.  **Colocation**: Keep related styles, types, and helpers close to where they are used.

## Refactoring Workflow

Follow these steps to safely refactor functionality without breaking it.

### Step 1: Analyze & Audit

Before making changes, map out the component:
-   **Identify State**: usage of `useState`, `useReducer`.
-   **Identify Effects**: usage of `useEffect`, external API calls.
-   **Identify UI Sections**: Logically distinct parts of the render (e.g., Header, FilterBar, List, Modal).

### Step 2: Extract Logic (Custom Hooks)

Move logic out of the component to reduce lines of code and clarify intent.

**Goal**: The main component should mostly contain purely presentational logic and simple event handlers.

**Pattern**:
```tsx
// ❌ BEFORE: Monolithic
const Dashboard = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  useEffect(() => { /* fetch logic */ }, []);
  const handleSort = () => { /* sort logic */ };
  
  return <div>...</div>
}

// ✅ AFTER: Separated Logic
// hooks/useDashboardLogic.ts
export const useDashboardLogic = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  useEffect(() => { /* fetch logic */ }, []);
  const handleSort = () => { /* sort logic */ };
  
  return { data, loading, handleSort };
}

// Dashboard.tsx
const Dashboard = () => {
  const { data, loading, handleSort } = useDashboardLogic();
  return <div>...</div>
}
```

### Step 3: Decompose the UI

Break the `return (...)` JSX into smaller, named components.

**Goal**: The main component's render method should read like a table of contents.

**Strategy**:
1.  Identify a distinct section of JSX (e.g., a list item or a header).
2.  Extract it to a local variable or function first to verify isolation.
3.  Move it to a separate named component (e.g., `DashboardHeader`, `ProjectList`).

**Pattern**:
```tsx
// ❌ BEFORE: Deeply nested JSX
return (
  <div className="container">
     <div className="header">
        <h1>Title</h1>
        <button onClick={...}>Add</button>
     </div>
     <ul>
       {items.map(item => (
         <li key={item.id}>
            <span>{item.name}</span>
            {/* ... complex item logic ... */}
         </li>
       ))}
     </ul>
  </div>
)

// ✅ AFTER: Composed Components
return (
  <div className="container">
    <DashboardHeader onAdd={handleAdd} />
    <ProjectList items={items} />
  </div>
)
```

### Step 4: Organize Files

If the component is large enough to split into multiple files, create a dedicated directory.

**Recommended Structure**:
```text
/app/dashboard/plan/
  ├── page.tsx            # Main container (View + Hook integration)
  ├── hooks/
  │   └── usePlanLogic.ts # Business logic
  ├── components/
  │   ├── PlanHeader.tsx  # Sub-component
  │   ├── PlanList.tsx    # Sub-component
  │   └── types.ts        # Local types
```

## Refactoring Checklist

- [ ] **Type Safety**: Prop interfaces are defined for all new sub-components.
- [ ] **Naming**: Component and Hook names are descriptive (`useProjectData` vs `useData`).
- [ ] **Simplicity**: No component exceeds 150 lines after refactoring.
- [ ] **Maintainability**: Magic numbers/strings are extracted to constants.

## Example: Refactoring `PlannerPage`

If refactoring a complex page like `PlannerPage`:

1.  **Extract Data**: Move task fetching, Drag-and-Drop sensors, and optimistic updates to `hooks/usePlanner.ts`.
2.  **Split UI**:
    -   `PlannerToolbar`: Search, filters, view toggles.
    -   `PlannerBoard`: The main grid/list.
    -   `TaskItem`: Individual task rendering.
3.  **Result**: `page.tsx` becomes a clean coordinator of these parts.
