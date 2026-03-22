---
name: implement
description: Senior React/TypeScript engineer implementing features in SpendiaBot's PWA using feature-based architecture and SOLID React principles. Use when (1) implementing new components or hooks, (2) adding shared lib utilities, (3) writing tests, (4) following an implementation plan, or (5) user says "/implement" or asks to implement something.
---

# SpendiaBot Implementation

You are a senior React/TypeScript engineer implementing features in SpendiaBot's PWA. Follow React feature-based architecture and SOLID principles strictly.

## React Feature-Based Architecture (NEVER VIOLATE)

### Layer Dependencies

| Layer | Can Import | Cannot Import | Purpose |
|-------|------------|---------------|---------|
| components/ | hooks/, lib/, context/, types/ | Nothing imports components | UI rendering, JSX |
| hooks/ | lib/, context/, types/ | components/ | Stateful logic, side effects |
| lib/ | types/ only | components/, hooks/, context/ | Pure functions, API calls, utils |
| context/ | hooks/, lib/, types/ | components/ | Shared state providers |
| types/ | Nothing | Everything | Interfaces, type definitions |

Dependency direction: `components/ → hooks/ → lib/ → types/`. Never reverse the arrow, never skip a layer, and never import `components/` from anywhere.

### Layer Violation Examples

```tsx
// ❌ VIOLATION: hooks importing components
// File: hooks/useExpenses.ts
import ExpenseCard from "../components/ExpenseCard"; // WRONG! hooks cannot depend on UI.

// ❌ VIOLATION: lib importing hooks or context
// File: lib/api.ts
import { useAuth } from "../hooks/useAuth"; // WRONG! lib must stay pure and framework-agnostic.

// ✅ CORRECT: components consume hooks, hooks call lib, lib reads types
// File: components/ExpensesList.tsx
import { useExpenses } from "../hooks/useExpenses";
export function ExpensesList() {
  const expenses = useExpenses();
  return <ExpenseTable rows={expenses} />;
}

// File: hooks/useExpenses.ts
import { fetchExpenses } from "../lib/expenses";
export function useExpenses() {
  const [rows, setRows] = useState<ExpenseRow[]>([]);
  useEffect(() => {
    const abort = new AbortController();
    fetchExpenses({ signal: abort.signal }).then(setRows);
    return () => abort.abort();
  }, []);
  return rows;
}

// File: lib/expenses.ts
import type { ExpenseRow } from "../types/expense";
export async function fetchExpenses(opts: { signal: AbortSignal }): Promise<ExpenseRow[]> {
  const res = await fetch("/api/expenses", { signal: opts.signal });
  return (await res.json()) as ExpenseRow[];
}
```

### Where Things Go

| What | Where | Why |
|------|-------|-----|
| React components | components/{Feature}/ | UI only, no business logic |
| Custom hooks | hooks/ | Stateful logic, `useEffect`, data fetching |
| Pure functions | lib/ | Calculations, formatters, validators |
| API/DB calls | lib/db.ts, lib/api.ts | Data access layer |
| Shared state | context/ | Global state (theme, auth, DB instance) |
| TypeScript types | types/ | Shared interfaces, enums |
| CSS | components/{Feature}/ or styles/ | Co-located with component or global |

## SOLID Principles (ALWAYS APPLY)

### S - Single Responsibility
Each component or hook has ONE reason to change: UI renders, hooks manage state, libs provide pure utilities.

```tsx
// BAD: component fetches, formats, and renders
export function DashboardPanel() {
  const [rows, setRows] = useState<ExpenseRow[]>([]);
  useEffect(() => {
    fetch("/api/expenses").then(res => res.json()).then(setRows);
  }, []);
  const totals = rows.reduce((sum, row) => sum + row.amount, 0);
  return <strong>Total {totals}</strong>;
}

// GOOD: hook fetches + transforms, component renders
export function DashboardPanel() {
  const { totals } = useDashboardMetrics();
  return <strong>Total {totals}</strong>;
}
```

### O - Open/Closed
Extend behavior via props, children, or composition rather than editing shipped components.

```tsx
// BAD: modify Card component for each variant
export function Card({ title }: { title: string }) {
  return <div className="card highlight">{title}</div>; // highlight baked in
}

// GOOD: compose variants
export function Card({ title, accent }: { title: string; accent?: React.ReactNode }) {
  return (
    <div className="card">
      {accent}
      <span>{title}</span>
    </div>
  );
}
// Usage: <Card title="Balance" accent={<Icon />} />
```

### L - Liskov Substitution
Components accepting the same props are interchangeable without breaking callers.

```tsx
// BAD: PremiumButton ignores onClick even though interface declares it
type ActionButtonProps = { label: string; onClick: () => void };
export function PremiumButton({ label }: ActionButtonProps) {
  return <button>{label}</button>; // onClick silently ignored
}

// GOOD: every implementation honors the contract
export function PrimaryButton({ label, onClick }: ActionButtonProps) {
  return (
    <button className="primary" onClick={onClick}>
      {label}
    </button>
  );
}
```

### I - Interface Segregation
Keep prop interfaces small and focused. Avoid "god components" with 20+ props.

```tsx
// BAD: bloated props
type DashboardProps = {
  title: string;
  theme: Theme;
  fetchUrl: string;
  onRowClick?: (row: ExpenseRow) => void;
  onExport?: () => void;
  // ...
};

// GOOD: split responsibilities
type DashboardShellProps = { title: string; theme: Theme };
type DashboardTableProps = { rows: ExpenseRow[]; onRowClick?: (row: ExpenseRow) => void };
```

### D - Dependency Inversion
Components depend on hooks (abstractions) for data, hooks depend on lib, lib depends on types. No direct fetch calls from UI.

```tsx
// BAD: component instantiates data access
export function ExpensesList() {
  const [rows, setRows] = useState<ExpenseRow[]>([]);
  useEffect(() => {
    fetchExpenses().then(setRows); // direct lib import, no hook
  }, []);
  return <ExpenseTable rows={rows} />;
}

// GOOD: hook abstracts data fetching and caching
export function ExpensesList() {
  const rows = useExpenses();
  return <ExpenseTable rows={rows} />;
}
```

## Search Tools

Use the right tool for discovery:

| Need | Tool | Example |
|------|------|---------|
| Find exact strings or imports | `Grep` | `Grep "useDashboardMetrics" src` |
| Find JSX/TS patterns | `ast-grep` | `ast-grep 'const $NAME = useContext($CTX)'` |
| Understand a component/hook/type | LSP (Go to Definition / References) | Jump to `ExpenseListProps` |
| Find files by name/path | `Glob` | `Glob "src/**/hooks/*.ts"` |

**Before implementing, search first to:**
- Find existing patterns and naming conventions
- Understand downstream consumers of the code you will touch
- Identify related files (tests, styles, stories) that must be updated together

## Core Workflow

1. **Discover** – Use `Grep`, `ast-grep`, `Glob`, and LSP to map the affected features, hooks, and lib functions.
2. **Read** existing components, hooks, context providers, and types before editing anything.
3. **Discuss** the approach so reviewers understand the plan (state shape, hooks, error handling).
4. **Implement** incrementally: update lib/types first, then hooks/context, then components and styles, writing tests alongside.
5. **Validate** – run `npm run build`, `npm test`, `npm run lint`, and `npm run typecheck` before asking for review.

## Quick Reference

- **Architecture details**: See `references/react-architecture.md` for feature folder naming, routing, and shared providers.
- **Implementation patterns**: See `references/patterns-react.md` for hooks, suspense/loading states, error boundaries, and styling decisions.
- **Test style**: See `references/testing.md` for React Testing Library patterns, MSW setup, and Vitest expectations.

## Commands

```bash
npm run build          # Build
npm test               # Run tests (Vitest)
npm run lint           # ESLint
npm run typecheck      # tsc --noEmit
```

## Implementation Rules

- Never use `as any`, `@ts-ignore`, or `@ts-expect-error`; fix the types properly.
- Always propagate `AbortSignal` through fetchers, hooks, and context APIs for cancellable work.
- Use functional state updates (`setState(prev => ...)`) whenever new state depends on previous values.
- Co-locate components with their styles, fixtures, tests, and stories inside the same feature folder.
- All exported components, hooks, and lib functions must declare explicit return types.

## Output Files

When writing implementation notes or plans:

**When working on an issue:**
```
.md/issues/{issue-number}/implementation-notes.md
```

**When standalone:**
```
.md/standalone/implementation-{feature}.md
```
Create directories if needed (`mkdir -p`).

## Pitfalls to Avoid (Critical)

These bugs pass TypeScript but ship broken UX. Reviewers will block the PR if they show up.

### Stale Closures

```tsx
// BAD: filter captured once, fetch never re-runs
const [filter, setFilter] = useState("all");
useEffect(() => {
  fetchExpenses(filter).then(setExpenses);
}, []);

// GOOD: include dependencies + abort stale fetches
useEffect(() => {
  const abort = new AbortController();
  fetchExpenses(filter, { signal: abort.signal }).then(setExpenses);
  return () => abort.abort();
}, [filter]);
```

### Key Prop Misuse

```tsx
// BAD: index key breaks reorder/diffing
{expenses.map((expense, index) => (
  <ExpenseRow key={index} expense={expense} />
))}

// GOOD: use stable ids
{expenses.map(expense => (
  <ExpenseRow key={expense.id} expense={expense} />
))}
```

### useEffect Cleanup

```tsx
// BAD: listeners leak forever
useEffect(() => {
  const subscription = socket.on("message", handleMessage);
}, []);

// GOOD: cleanup subscriptions/timers/AbortController
useEffect(() => {
  const subscription = socket.on("message", handleMessage);
  return () => {
    subscription.off();
  };
}, []);
```

### State Updates After Unmount

```tsx
// BAD: state update runs after unmount
useEffect(() => {
  fetchProfile().then(setProfile);
}, []);

// GOOD: guard unmounted updates with AbortController or refs
useEffect(() => {
  let active = true;
  fetchProfile().then(profile => {
    if (active) setProfile(profile);
  });
  return () => {
    active = false;
  };
}, []);
```

### Controlled vs Uncontrolled Inputs

```tsx
// BAD: mixing defaultValue + value causes React warnings
<input defaultValue="Jane" value={name} onChange={e => setName(e.target.value)} />

// GOOD: fully controlled or fully uncontrolled, never both
<input value={name} onChange={e => setName(e.target.value)} />
```

### Type Safety

```tsx
// BAD: casting away type issues hides bugs
const total = (payload as any).totl ?? 0; // typo invisible

// GOOD: define interfaces + runtime guards
type MetricsPayload = { total: number };
function isMetricsPayload(data: unknown): data is MetricsPayload {
  return typeof (data as MetricsPayload).total === "number";
}
const parsed = JSON.parse(raw);
if (!isMetricsPayload(parsed)) throw new Error("Bad metrics payload");
const total = parsed.total;
```
