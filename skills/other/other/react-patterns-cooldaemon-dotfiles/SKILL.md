---
name: react-patterns
description: React and Next.js development policies. Use when writing React components, hooks, or performance optimization. Do NOT use for Vue.js code -- use vue-patterns instead.
durability: encoded-preference
---

# React/Next.js Patterns

## State Management Policies

### Always Use Functional Updates

```typescript
// GOOD
setCount(prev => prev + 1)

// BAD: Can be stale in async
setCount(count + 1)
```

### Context Null Check Required

```typescript
const context = useContext(MyContext)
if (!context) throw new Error('Must be used within Provider')
```

## Conditional Rendering

```typescript
// GOOD: Clear conditions
{isLoading && <Spinner />}
{error && <ErrorMessage error={error} />}
{data && <DataDisplay data={data} />}

// BAD: Ternary hell
{isLoading ? <Spinner /> : error ? <ErrorMessage /> : data ? <DataDisplay /> : null}
```

## Performance Policies

### Memoization Guidelines

| Technique | When to Use |
|-----------|-------------|
| `useMemo` | Expensive computations with stable deps |
| `useCallback` | Functions passed to memoized children |
| `React.memo` | Pure components with frequent parent re-renders |

**Default: Let React Compiler handle memoization.** Manual `useMemo`/`useCallback`/`React.memo` only when precise control over re-render boundaries is needed.

### Code Splitting - Use for Heavy Components

```typescript
const HeavyChart = lazy(() => import('./HeavyChart'))

<Suspense fallback={<Spinner />}>
  <HeavyChart />
</Suspense>
```

### Virtualization - Use for 100+ Items

Use `@tanstack/react-virtual` for long lists.

## Accessibility Policies

### Always Use useId for Form Labels

```typescript
const hintId = useId()
<input aria-describedby={hintId} />
<p id={hintId}>Hint text</p>
```

### Modal Focus Management Required

- Save previous focus on open
- Focus modal on open
- Restore focus on close
- Handle Escape key

## Anti-Patterns

| Anti-Pattern | Correct Approach |
|--------------|------------------|
| `setCount(count + 1)` in async | Use functional update |
| Deeply nested ternaries | Use `&&` or early returns |
| Inline object/array in deps | Extract to stable reference |
| Missing key in lists | Always provide unique key |
| useEffect for derived state | Use useMemo or compute inline |

## Component Design Policies

### Prefer Composition

Composition over configuration — components should be assembled, not configured via props.

```typescript
// GOOD
<Card>
  <CardHeader>Title</CardHeader>
  <CardBody>Content</CardBody>
</Card>

// BAD: Props drilling
<Card header="Title" body="Content" footer="..." />
```

### Compound Components for Related UI

Use Context to share state between related components (Tabs, Accordion, etc.).
