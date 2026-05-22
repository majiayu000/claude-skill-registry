---
name: react-code-review
description: Provides comprehensive code review capability for React applications, validates component architecture, hooks usage, React 19 patterns, state management, performance optimization, accessibility compliance, and TypeScript integration. Use when reviewing React code changes, before merging pull requests, after implementing new features, or for component architecture validation. Triggers on "review React code", "React code review", "check my React components".
allowed-tools: Read, Edit, Grep, Glob, Bash
---

# React Code Review

## Overview

This skill provides structured, comprehensive code review for React applications. It evaluates code against React 19 best practices, component architecture patterns, hook usage, accessibility standards, and production-readiness criteria. The review produces actionable findings categorized by severity (Critical, Warning, Suggestion) with concrete code examples for improvements.

This skill delegates to the `react-software-architect-review` agent for deep architectural analysis when invoked through the agent system.

## When to Use

- Reviewing React components, hooks, and pages before merging
- Validating component composition and reusability patterns
- Checking proper hook usage (useState, useEffect, useMemo, useCallback)
- Reviewing React 19 patterns (use, useOptimistic, useFormStatus, Actions)
- Evaluating state management approaches (local, context, external stores)
- Assessing performance optimization (memoization, code splitting, lazy loading)
- Reviewing accessibility compliance (WCAG, semantic HTML, ARIA)
- Validating TypeScript typing for props, state, and events
- Checking Tailwind CSS and styling patterns
- After implementing new React features or refactoring component architecture

## Instructions

1. **Identify Scope**: Determine which React components and hooks are under review. Use `glob` to discover `.tsx`/`.jsx` files and `grep` to identify component definitions, hook usage, and context providers.

2. **Analyze Component Architecture**: Verify proper component composition — check for single responsibility, appropriate size, and reusability. Look for components that are too large (>200 lines), have too many props (>7), or mix concerns.

3. **Review Hook Usage**: Validate proper hook usage — check dependency arrays in `useEffect`/`useMemo`/`useCallback`, verify cleanup functions in `useEffect`, and identify unnecessary re-renders caused by missing or incorrect memoization.

4. **Evaluate State Management**: Assess where state lives — check for proper colocation, unnecessary lifting, and appropriate use of Context vs external stores. Verify that server state uses TanStack Query, SWR, or similar libraries rather than manual `useEffect` + `useState` patterns.

5. **Check Accessibility**: Review semantic HTML usage, ARIA attributes, keyboard navigation, focus management, and screen reader compatibility. Verify that interactive elements are accessible and form inputs have proper labels.

6. **Assess Performance**: Look for unnecessary re-renders, missing `React.memo` on expensive components, improper use of `useCallback`/`useMemo`, missing code splitting, and large bundle imports.

7. **Review TypeScript Integration**: Check prop type definitions, event handler typing, generic component patterns, and proper use of utility types. Verify that `any` is not used where specific types are possible.

8. **Produce Review Report**: Generate a structured report with severity-classified findings (Critical, Warning, Suggestion), positive observations, and prioritized recommendations with code examples.

## Examples

### Example 1: Hook Dependency Issues

```tsx
// ❌ Bad: Missing dependency causes stale closure
function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    fetchUser(userId).then(setUser);
  }, []); // Missing userId in dependency array

  return <div>{user?.name}</div>;
}

// ✅ Good: Proper dependencies with cleanup
function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    let cancelled = false;
    fetchUser(userId).then((data) => {
      if (!cancelled) setUser(data);
    });
    return () => { cancelled = true; };
  }, [userId]);

  return <div>{user?.name}</div>;
}

// ✅ Better: Use TanStack Query for server state
function UserProfile({ userId }: { userId: string }) {
  const { data: user, isLoading } = useQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUser(userId),
  });

  if (isLoading) return <Skeleton />;
  return <div>{user?.name}</div>;
}
```

### Example 2: Component Composition

```tsx
// ❌ Bad: Monolithic component mixing data fetching, filtering, and rendering
function Dashboard() {
  const [users, setUsers] = useState([]);
  const [filter, setFilter] = useState('');
  useEffect(() => { /* fetch + filter + sort all in one */ }, [filter]);
  return <div>{/* 200+ lines of mixed concerns */}</div>;
}

// ✅ Good: Composed from focused components with custom hooks
function Dashboard() {
  return (
    <div>
      <UserFilters />
      <Suspense fallback={<TableSkeleton />}>
        <UserTable />
      </Suspense>
      <UserPagination />
    </div>
  );
}
```

### Example 3: Accessibility Review

```tsx
// ❌ Bad: Inaccessible interactive elements
function Menu({ items }: { items: MenuItem[] }) {
  const [open, setOpen] = useState(false);
  return (
    <div>
      <div onClick={() => setOpen(!open)}>Menu</div>
      {open && (
        <div>
          {items.map(item => (
            <div key={item.id} onClick={() => navigate(item.path)}>
              {item.label}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

// ✅ Good: Accessible with proper semantics and keyboard support
function Menu({ items }: { items: MenuItem[] }) {
  const [open, setOpen] = useState(false);
  return (
    <nav aria-label="Main navigation">
      <button
        onClick={() => setOpen(!open)}
        aria-expanded={open}
        aria-controls="menu-list"
      >
        Menu
      </button>
      {open && (
        <ul id="menu-list" role="menu">
          {items.map(item => (
            <li key={item.id} role="menuitem">
              <a href={item.path}>{item.label}</a>
            </li>
          ))}
        </ul>
      )}
    </nav>
  );
}
```

### Example 4: Performance Optimization

```tsx
// ❌ Bad: Unstable callback recreated every render causes child re-renders
{filtered.map(product => (
  <ProductCard
    key={product.id}
    product={product}
    onSelect={() => console.log(product.id)} // New function each render
  />
))}

// ✅ Good: Stable callback + memoized child
const handleSelect = useCallback((id: string) => {
  console.log(id);
}, []);

const filtered = useMemo(
  () => products.filter(p => p.name.toLowerCase().includes(search.toLowerCase())),
  [products, search]
);

{filtered.map(product => (
  <ProductCard key={product.id} product={product} onSelect={handleSelect} />
))}

const ProductCard = memo(function ProductCard({ product, onSelect }: Props) {
  return <div onClick={() => onSelect(product.id)}>{product.name}</div>;
});
```

### Example 5: TypeScript Props Review

```tsx
// ❌ Bad: Loose typing and missing prop definitions
function Card({ data, onClick, children, ...rest }: any) {
  return (
    <div onClick={onClick} {...rest}>
      <h2>{data.title}</h2>
      {children}
    </div>
  );
}

// ✅ Good: Strict typing with proper interfaces
interface CardProps extends React.ComponentPropsWithoutRef<'article'> {
  title: string;
  description?: string;
  variant?: 'default' | 'outlined' | 'elevated';
  onAction?: (event: React.MouseEvent<HTMLButtonElement>) => void;
  children: React.ReactNode;
}

function Card({
  title,
  description,
  variant = 'default',
  onAction,
  children,
  className,
  ...rest
}: CardProps) {
  return (
    <article className={cn('card', `card--${variant}`, className)} {...rest}>
      <h2>{title}</h2>
      {description && <p>{description}</p>}
      {children}
      {onAction && <button onClick={onAction}>Action</button>}
    </article>
  );
}
```

## Review Output Format

Structure all code review findings as follows:

### 1. Summary
Brief overview with an overall quality score (1-10) and key observations.

### 2. Critical Issues (Must Fix)
Issues causing bugs, security vulnerabilities, or broken functionality.

### 3. Warnings (Should Fix)
Issues that violate best practices, cause performance problems, or reduce maintainability.

### 4. Suggestions (Consider Improving)
Improvements for code organization, accessibility, or developer experience.

### 5. Positive Observations
Well-implemented patterns and good practices to acknowledge.

### 6. Recommendations
Prioritized next steps with code examples for the most impactful improvements.

## Best Practices

- Keep components focused — single responsibility, under 200 lines
- Colocate state with the components that use it
- Use custom hooks to extract reusable logic from components
- Apply `React.memo` only when measured re-render cost justifies it
- Use TanStack Query or SWR for server state instead of `useEffect` + `useState`
- Always include cleanup functions in `useEffect` when subscribing to external resources
- Write semantic HTML first, add ARIA only when native semantics are insufficient
- Use TypeScript strict mode and avoid `any` in component props
- Implement error boundaries for graceful failure handling
- Prefer composition over conditional rendering complexity

## Constraints and Warnings

- Respect the project's React version — avoid suggesting React 19 features for older versions
- Do not enforce a specific state management library unless the project has standardized on one
- Memoization is not always beneficial — only suggest it when re-render impact is measurable
- Accessibility recommendations should follow WCAG 2.1 AA as the baseline
- Focus on high-confidence issues — avoid false positives on subjective style choices
- Do not suggest rewriting working components without clear, measurable benefit

## References

See the `references/` directory for detailed review checklists and pattern documentation:
- `references/hooks-patterns.md` — React hooks best practices and common mistakes
- `references/component-architecture.md` — Component composition and design patterns
- `references/accessibility.md` — Accessibility checklist and ARIA patterns for React
