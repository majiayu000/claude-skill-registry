---
name: react
description: "React component patterns, hooks, and best practices for modern React development. Functional components, proper hook usage, memoization, and performance optimization. Trigger: When creating React components, implementing hooks, managing state, or optimizing React performance."
skills:
  - conventions
  - a11y
  - typescript
  - javascript
  - architecture-patterns
  - humanizer
dependencies:
  react: ">=17.0.0 <19.0.0"
allowed-tools:
  - documentation-reader
  - web-search
---

# React Skill

## Overview

Modern React patterns using hooks, functional components, and best practices for building maintainable UIs.

## Objective

Guide developers in building React applications with proper component architecture, state management, and performance optimization.

---

## When to Use

Use this skill when:

- Creating React functional components or refactoring class components
- Implementing hooks (useState, useEffect, useMemo, useCallback)
- Managing component state and side effects
- Optimizing React performance and preventing unnecessary re-renders
- Building component composition patterns
- Integrating with React ecosystem libraries

Don't use this skill for:

- Non-React JavaScript patterns (use javascript skill)
- React Native mobile development (use react-native skill)
- Redux state management (use redux-toolkit skill)
- Server-side framework specifics (use astro or relevant framework skill)

---

## 📚 Extended Mandatory Read Protocol

**This skill has a `references/` directory with detailed guides for complex React patterns.**

### Reading Rules

**Read references/ when:**

- **MUST read [hooks-advanced.md](references/hooks-advanced.md)** when:
  - Deciding useState vs useReducer (4+ related state values)
  - Creating custom hooks or composing hooks
  - Dealing with stale closures or hook dependencies
- **MUST read [useEffect-patterns.md](references/useEffect-patterns.md)** when:
  - Implementing data fetching, subscriptions, or side effects
  - Handling cleanup, race conditions, or async operations
  - Debugging dependency array issues

- **MUST read [performance.md](references/performance.md)** when:
  - Components re-rendering unnecessarily
  - Working with expensive computations or large lists
  - Profiling and optimizing React applications

- **MUST read [context-patterns.md](references/context-patterns.md)** when:
  - Sharing state across multiple components
  - Building compound components or component APIs
  - Optimizing context performance (preventing re-renders)

- **MUST read [forms-state.md](references/forms-state.md)** when:
  - Building forms with validation
  - Choosing controlled vs uncontrolled inputs
  - Implementing multi-step forms or file uploads

**Quick reference only:** Use this SKILL.md for simple components and quick lookups. Decision Tree below directs you to specific references when needed.

### Reading Priority

| Situation                           | Read This                            | Why                                 |
| ----------------------------------- | ------------------------------------ | ----------------------------------- |
| Simple component (<3 state values)  | SKILL.md only                        | No deep dive needed                 |
| Complex state (useReducer decision) | **hooks-advanced.md** (REQUIRED)     | 40+ patterns for state management   |
| Data fetching or subscriptions      | **useEffect-patterns.md** (REQUIRED) | Race conditions, cleanup patterns   |
| Performance optimization            | **performance.md** (REQUIRED)        | Profile first, optimize correctly   |
| State sharing across components     | **context-patterns.md** (REQUIRED)   | Performance pitfalls avoided        |
| Form implementation                 | **forms-state.md** (REQUIRED)        | Controlled vs uncontrolled decision |

**See [references/README.md](references/README.md)** for complete navigation guide.

---

## Critical Patterns

### ✅ REQUIRED: Use Functional Components with Hooks

```typescript
// ✅ CORRECT: Functional component with hooks
const Counter: React.FC = () => {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(count + 1)}>{count}</button>;
};

// ❌ WRONG: Class component (legacy pattern)
class Counter extends React.Component {
  state = { count: 0 };
  render() { /* ... */ }
}
```

### ✅ REQUIRED: Proper useEffect Dependencies

```typescript
// ✅ CORRECT: All dependencies included
useEffect(() => {
  fetchData(userId);
}, [userId]);

// ❌ WRONG: Missing dependencies (causes stale closures)
useEffect(() => {
  fetchData(userId);
}, []); // userId missing
```

### ✅ REQUIRED: Stable Keys for Lists

```typescript
// ✅ CORRECT: Use unique IDs
{items.map(item => <li key={item.id}>{item.name}</li>)}

// ❌ WRONG: Using array index (causes bugs on reorder/delete)
{items.map((item, index) => <li key={index}>{item.name}</li>)}
```

### ❌ NEVER: Conditional Hook Calls

```typescript
// ❌ WRONG: Hooks must not be conditional
if (condition) {
  const [value, setValue] = useState(0); // Breaks React rules
}

// ✅ CORRECT: Hooks at top level, conditional logic inside
const [value, setValue] = useState(0);
const shouldUse = condition ? value : defaultValue;
```

---

## Conventions

Refer to conventions for:

- Code organization
- Naming patterns

Refer to a11y for:

- Semantic HTML in JSX
- Keyboard navigation
- ARIA attributes

### React Specific

- Use functional components with hooks
- Implement proper component composition
- Memoize expensive computations with useMemo
- Use useCallback for event handlers in optimized components
- Handle side effects with useEffect
- Provide keys for lists

## Decision Tree

**Simple state (<3 values)?** → Use `useState`. **[See hooks-advanced.md](references/hooks-advanced.md#usestate-patterns)** for patterns.

**Complex state (4+ related values)?** → Use `useReducer` for centralized logic. **MUST read [hooks-advanced.md](references/hooks-advanced.md#usereducer-patterns)** for reducer patterns.

**Side effect needed?** → Use `useEffect` with proper dependency array. **MUST read [useEffect-patterns.md](references/useEffect-patterns.md)** for cleanup, race conditions, and async patterns.

**Data fetching?** → Use `useEffect` with AbortController. **MUST read [useEffect-patterns.md#async-patterns](references/useEffect-patterns.md#async-patterns)** for race condition handling.

**Performance issue?** → Profile first with React DevTools Profiler. **MUST read [performance.md](references/performance.md)** for useMemo, useCallback, React.memo patterns.

**Expensive computation?** → Use `useMemo` if calculation is costly. **CHECK [performance.md#usememo](references/performance.md#usememo)** to decide if worth it.

**Passing callbacks to memoized children?** → Use `useCallback`. **CHECK [performance.md#usecallback](references/performance.md#usecallback)** for stable references.

**Sharing state across components?** → Use Context API or lift state. **MUST read [context-patterns.md](references/context-patterns.md)** for performance optimization and splitting contexts.

**Building component API?** → Use compound components pattern. **CHECK [context-patterns.md#compound-components](references/context-patterns.md#compound-components)** for implicit state sharing.

**Form with validation?** → Use controlled components. **MUST read [forms-state.md](references/forms-state.md)** for controlled vs uncontrolled and validation patterns.

**Multi-step form?** → Use wizard pattern with step state. **CHECK [forms-state.md#multi-step-forms](references/forms-state.md#multi-step-forms)**.

**File upload?** → Use controlled input with File API. **CHECK [forms-state.md#file-uploads](references/forms-state.md#file-uploads)** for single/multiple uploads with progress.

**List rendering?** → Always provide stable `key` prop (use unique IDs, not indices). For large lists (1000+), **MUST read [performance.md#list-rendering-optimization](references/performance.md#list-rendering-optimization)** for virtualization.

**Conditional rendering?** → Use `&&` for simple conditions, ternary `? :` for if-else, early return for complex logic.

---

## Example

```typescript
import { useState, useEffect, useMemo } from 'react';

interface TodoProps {
  items: string[];
}

const TodoList: React.FC<TodoProps> = ({ items }) => {
  const [filter, setFilter] = useState('');

  const filteredItems = useMemo(() =>
    items.filter(item => item.toLowerCase().includes(filter.toLowerCase())),
    [items, filter]
  );

  return (
    <div>
      <input value={filter} onChange={(e) => setFilter(e.target.value)} />
      <ul>
        {filteredItems.map((item, index) => (
          <li key={index}>{item}</li>
        ))}
      </ul>
    </div>
  );
};
```

---

## Edge Cases

**Stale closures in useEffect:** When state/props aren't in dependency array, closures capture old values. Always include all dependencies or use functional setState: `setState(prev => prev + 1)`.

**useEffect cleanup:** Return cleanup function for subscriptions, timers, event listeners to prevent memory leaks:

```typescript
useEffect(() => {
  const timer = setInterval(() => {}, 1000);
  return () => clearInterval(timer); // Cleanup
}, []);
```

**Ref vs State:** Use `useRef` for values that don't trigger re-renders (DOM elements, mutable values). Use `useState` for values that should trigger UI updates.

**Batching updates:** React batches multiple setState calls in event handlers. In async code (setTimeout, promises), use `flushSync` for immediate updates (rare cases).

**Children prop patterns:** When passing children, use `React.ReactNode` type. For render props, use function children: `{(data) => <Component data={data} />}`.

---

## Advanced Architecture Patterns

**⚠️ Read This First**: Most React projects do NOT need advanced architecture patterns. Apply only when:

1. **AGENTS.md explicitly specifies** architecture requirements
2. **Codebase already uses** domain/, application/, infrastructure/ folders
3. **User explicitly requests** architectural patterns

**If none apply** → Skip this section, use React best practices above.

### Quick Context Verification

```bash
# Check AGENTS.md
cat agents/your-project/AGENTS.md | grep -i "architecture\|solid\|clean\|ddd"

# Check codebase structure
ls src/domain src/application src/infrastructure
```

- **AGENTS.md mentions patterns OR folders exist OR user requests** → Apply patterns
- **None of above** → Use standard React patterns only

### Applicable Patterns

- **SRP**: Separate data fetching, logic, presentation (one responsibility per component/hook)
- **DIP**: Abstract services (use Context API or hooks, not direct imports)
- **Result Pattern**: Type-safe async error handling
- **Clean Architecture**: Layer separation when business logic is complex

### For Complete Guide

**MUST read** [architecture-patterns/references/frontend-integration.md](../architecture-patterns/references/frontend-integration.md) for:

- Complete React examples with Clean Architecture
- SRP for components and hooks
- DIP with Context API
- Result Pattern in hooks
- Layer separation (domain/, application/, infrastructure/, presentation/)
- When to apply and when to stop

**Also see**: [architecture-patterns/SKILL.md](../architecture-patterns/SKILL.md) for Decision Tree and pattern selection.

---

## References

- https://react.dev/
- https://react.dev/reference/react
