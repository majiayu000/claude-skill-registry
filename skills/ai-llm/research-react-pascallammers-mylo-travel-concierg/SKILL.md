---
name: research-react
description: Research React 19 patterns, hooks, and best practices using Exa code search and Ref documentation
---

# Research React 19 Patterns

Use this skill when you need to:
- Learn about React 19 new features (Actions, useOptimistic, use())
- Find hook implementation patterns
- Research component composition patterns
- Understand performance optimization techniques
- Learn about Suspense and error boundaries

## Process

1. **Identify React Topic**
   - Which React feature or pattern?
   - New React 19 features or established patterns?
   - Performance, state management, or component design?

2. **Search Documentation (Ref)**
   ```
   Query patterns:
   - "React 19 [feature name]"
   - "React useOptimistic hook"
   - "React Actions form handling"
   - "React Suspense streaming"
   ```

3. **Find Real Implementations (Exa)**
   ```
   Query patterns:
   - "React 19 useOptimistic implementation example"
   - "React Actions form submission error handling"
   - "React use hook Promise example"
   - "React Suspense data fetching pattern"
   ```

4. **Compare with Project Patterns**
   - How does this fit with Next.js 15 Server Components?
   - Does this align with project standards?
   - Are there type safety considerations?

## React 19 Specific Research

### Actions
```typescript
// Documentation
Query: "React 19 Actions form handling"

// Code examples
Query: "React 19 useActionState form submission pending state example"
```

### useOptimistic
```typescript
// Documentation
Query: "React useOptimistic hook optimistic updates"

// Code examples
Query: "React useOptimistic todo list real-time updates implementation"
```

### use() Hook
```typescript
// Documentation
Query: "React use hook Promise Context"

// Code examples
Query: "React use hook async data fetching Suspense boundary example"
```

### Server Components Integration
```typescript
// Documentation
Query: "React Server Components async await"

// Code examples
Query: "Next.js React Server Component database query example"
```

## Common Research Topics

### Hooks
- useState with complex state
- useEffect cleanup patterns
- useMemo optimization
- useCallback dependencies
- Custom hooks design

### Performance
- React.memo usage
- Code splitting with lazy
- Virtual list implementations
- Debouncing and throttling

### Patterns
- Compound components
- Render props
- Higher-order components
- Context patterns
- Error boundaries

## Output Format

Provide:
1. **Feature explanation** - What it does and when to use it
2. **Code examples** - From Exa, showing real usage
3. **Type definitions** - TypeScript patterns from examples
4. **Integration notes** - How it works with Next.js/project stack
5. **Best practices** - Dos and don'ts from documentation
6. **Common mistakes** - What to avoid based on examples

## When to Use

- Implementing new React 19 features
- Refactoring existing components
- Performance optimization
- Learning new patterns
- Debugging React-specific issues
- Before code reviews

## Example Session

```
User: "How do I use React 19 Actions for form submission?"