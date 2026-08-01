---
name: code-review-lewisperez999-v0-lewis-perez-p
description: Perform code reviews following project standards.
---

# Code Review

Perform code reviews following project standards.

## Description

Review code changes for quality, security, performance, and adherence to project conventions.

## Checklist

### TypeScript
- [ ] No `any` types without justification
- [ ] Interfaces defined for all props and data shapes
- [ ] Proper error handling with typed errors
- [ ] Exports include types alongside functions

### React/Next.js
- [ ] Server Components used by default
- [ ] `'use client'` only where necessary
- [ ] Proper use of Suspense for loading states
- [ ] No unnecessary re-renders
- [ ] Accessible (semantic HTML, ARIA)

### Security
- [ ] No hardcoded secrets or API keys
- [ ] Input validated with Zod
- [ ] SQL queries are parameterized
- [ ] Auth checks on protected endpoints
- [ ] XSS prevention (no dangerouslySetInnerHTML with user content)

### Performance
- [ ] Images optimized (next/image)
- [ ] Lazy loading for heavy components
- [ ] Database queries are indexed
- [ ] No N+1 query problems
- [ ] Appropriate caching

### Code Style
- [ ] Consistent naming conventions
- [ ] Files named correctly (PascalCase for components, kebab-case for utils)
- [ ] Imports use `@/` aliases
- [ ] No commented-out code
- [ ] Clear, descriptive variable names

### API Routes
- [ ] Proper HTTP status codes
- [ ] Error responses are consistent
- [ ] Rate limiting for public endpoints
- [ ] Request/response typed
- [ ] Logging for errors

### Database
- [ ] Migrations are reversible
- [ ] Indexes on frequently queried columns
- [ ] Foreign key constraints where appropriate
- [ ] No raw SQL concatenation

## Review Template

```markdown
## Code Review: [PR/Change Title]

### Summary
Brief description of the changes.

### Checklist
- [x] TypeScript types are correct
- [x] Security considerations addressed
- [ ] Performance optimized
- [x] Tests added/updated

### Issues Found

#### Critical
- None

#### Major
- [ ] Issue description - file:line

#### Minor
- [ ] Suggestion - file:line

### Suggestions
- Consider using X instead of Y
- Could extract into reusable function

### Approved: Yes/No
```

## Common Issues

### TypeScript
```typescript
// ❌ Bad: Using any
const data: any = await fetchData();

// ✅ Good: Typed response
interface ApiResponse {
  id: string;
  name: string;
}
const data: ApiResponse = await fetchData();
```

### Security
```typescript
// ❌ Bad: SQL injection risk
const result = await query(`SELECT * FROM users WHERE id = ${userId}`);

// ✅ Good: Parameterized query
const result = await query('SELECT * FROM users WHERE id = $1', [userId]);
```

### React
```typescript
// ❌ Bad: Unnecessary client component
'use client';
export function StaticContent() {
  return <div>Just static content</div>;
}

// ✅ Good: Server component (no directive needed)
export function StaticContent() {
  return <div>Just static content</div>;
}
```

### Performance
```typescript
// ❌ Bad: Fetching in loop
for (const id of ids) {
  const item = await query('SELECT * FROM items WHERE id = $1', [id]);
}

// ✅ Good: Batch query
const items = await query('SELECT * FROM items WHERE id = ANY($1)', [ids]);
```
