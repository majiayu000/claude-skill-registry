---
name: research-nextjs
description: Research Next.js 15 patterns, examples, and documentation using Exa code search and Ref documentation
---

# Research Next.js Patterns

Use this skill when you need to:
- Learn about Next.js 15 App Router patterns
- Find real-world implementation examples
- Research Server Components vs Client Components
- Understand caching and revalidation strategies
- Learn about metadata, routing, or middleware patterns

## Process

1. **Identify Research Need**
   - What specific Next.js pattern or feature do you need?
   - Is it about routing, data fetching, performance, or configuration?

2. **Search Documentation (Ref)**
   ```
   Use ref_search_documentation with query focused on:
   - "Next.js 15 app router [specific topic]"
   - "Next.js server components"
   - "Next.js [feature name]"
   ```

3. **Find Code Examples (Exa)**
   ```
   Use get_code_context_exa with query:
   - "Next.js 15 app router [pattern] implementation example"
   - "Next.js server component with [feature]"
   - "Next.js API route [specific use case]"
   ```

4. **Read Full Documentation**
   ```
   Use ref_read_url to get complete docs from search results
   ```

5. **Synthesize Learning**
   - Compare documentation with real code examples
   - Identify best practices
   - Note any version-specific considerations
   - Document patterns in .claude/memory/org/patterns.json

## Example Queries

### Server Components
```typescript
// Documentation search
Query: "Next.js 15 server components data fetching patterns"

// Code context search
Query: "Next.js 15 server component async data fetch database example"
```

### API Routes
```typescript
// Documentation search
Query: "Next.js 15 route handlers API routes"

// Code context search
Query: "Next.js 15 route handler POST validation authentication example"
```

### Caching
```typescript
// Documentation search
Query: "Next.js 15 caching revalidation strategies"

// Code context search
Query: "Next.js 15 revalidatePath revalidateTag implementation example"
```

## Output

After research, provide:
1. **Summary of findings** - Key concepts and patterns
2. **Code examples** - Real implementations from Exa
3. **Best practices** - From documentation and examples
4. **Implementation guide** - How to apply in this project
5. **Common pitfalls** - What to avoid based on examples

## When to Use

- Starting a new feature with unfamiliar Next.js patterns
- Debugging Next.js-specific issues
- Optimizing performance (caching, streaming, etc.)
- Learning about new Next.js 15 features
- Before making architectural decisions

## Related Skills

- research-react (for React patterns)
- research-typescript (for type patterns)
- research-performance (for optimization)
