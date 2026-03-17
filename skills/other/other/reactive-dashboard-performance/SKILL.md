---
name: reactive-dashboard-performance
description: Expert in building blazing-fast reactive dashboards with comprehensive testing. Masters React performance patterns, testing strategies for async components, and real-world patterns from Linear, Vercel, Notion.
version: "1.0.0"
category: Frontend Development
tags:
  - react
  - performance
  - testing
  - dashboard
  - optimization
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
triggers:
  - "dashboard performance"
  - "slow tests"
  - "reactive testing"
  - "integration tests timeout"
  - "dashboard optimization"
---

# Reactive Dashboard Performance

Expert in building production-grade reactive dashboards that load in &lt;100ms and have comprehensive test coverage.

## Core Expertise

### Performance Patterns (Linear, Vercel, Notion-grade)

1. **Skeleton-First Loading**
   - Render skeleton immediately (0ms perceived load)
   - Stream in data progressively
   - Never show spinners for &lt;200ms loads

2. **Aggressive Caching**
   - React Query with staleTime: 5min, cacheTime: 30min
   - Optimistic updates for mutations
   - Prefetch on hover/mount

3. **Code Splitting**
   - Route-based splitting (Next.js automatic)
   - Component-level lazy() for heavy widgets
   - Preload critical paths

4. **Memoization Strategy**
   - useMemo for expensive computations
   - React.memo for pure components
   - useCallback for stable references

### Testing Reactive Dashboards

1. **Mock Strategy**
   - Mock at service boundary (React Query, analytics)
   - Never mock UI components (test real DOM)
   - Use MSW for API mocking when possible

2. **Async Handling**
   ```typescript
   // WRONG - races with React
   render(<Dashboard />);
   const element = screen.getByText('Welcome');

   // RIGHT - waits for async resolution
   render(<Dashboard />);
   const element = await screen.findByText('Welcome');
   ```

3. **Timeout Debugging**
   - Timeouts mean: missing mock, wrong query, or component not rendering
   - Use screen.debug() to see actual DOM
   - Check console for unmocked errors

4. **Test Wrapper Pattern**
   ```typescript
   const TestProviders = ({ children }) => (
     <QueryClientProvider client={testQueryClient}>
       <AuthProvider>
         {children}
       </AuthProvider>
     </QueryClientProvider>
   );
   ```

### Real-World Examples

- **Linear Dashboard**: Skeleton → Stale data → Fresh data (perceived &lt;50ms)
- **Vercel Dashboard**: Prefetch on nav hover, optimistic deploys
- **Notion Pages**: Infinite cache, local-first, sync in background

## Diagnostic Protocol

### Integration Test Timeouts

1. **Check what's actually rendering**
   ```typescript
   render(<Component />);
   screen.debug(); // See actual DOM
   ```

2. **Find unmocked dependencies**
   - Check console for "not a function" errors
   - Look for network requests in test output
   - Verify all contexts are provided

3. **Fix async queries**
   - Use findBy* instead of getBy*
   - Increase timeout if needed: `waitFor(() =&gt; {...}, { timeout: 3000 })`
   - Mock React Query properly

4. **Simplify component tree**
   - Test widgets individually first
   - Add full integration tests last
   - Use data-testid for complex queries

## Performance Optimization

### Dashboard Load Budget

| Phase | Target |
|-------|--------|
| Skeleton render | 0-16ms (1 frame) |
| First data paint | &lt;100ms |
| Full interactive | &lt;200ms |
| Lazy widgets | &lt;500ms |

### React Query Config

```typescript
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5min
      cacheTime: 30 * 60 * 1000, // 30min
      refetchOnWindowFocus: false,
      refetchOnMount: false,
      retry: 1,
    },
  },
});
```

### Skeleton Pattern

```typescript
function Dashboard() {
  const { data, isLoading } = useQuery('dashboard', fetchDashboard);

  // Show skeleton immediately, no loading check
  return (
    <div>
      {data ? <RealWidget data={data} /> : <SkeletonWidget />}
    </div>
  );
}
```

## Common Pitfalls

1. **Spinners for fast loads** - Use skeletons instead
2. **Unmemoized expensive computations** - Wrap in useMemo
3. **Testing implementation details** - Test user behavior
4. **Mocking too much** - Mock at boundaries only
5. **Synchronous test expectations** - Everything is async

When debugging test timeouts, ALWAYS start with `screen.debug()` to see what actually rendered.
