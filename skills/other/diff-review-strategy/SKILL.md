---
name: diff-review-strategy
description: PR size-based review depth, performance review checklist, architecture conformance checks, and framework-specific review patterns.
---

# Diff Review Strategy

## PR Size Categories and Review Depth

| Category | Lines Changed | Review Depth | Action |
|----------|--------------|--------------|--------|
| XS | 1–10 | Quick scan | Auto-approve if tests pass, typo/doc fixes |
| S | 11–50 | Focused | Check edge cases, naming, one logic path |
| M | 51–200 | Thorough | Full logic review, design check, test coverage |
| L | 201–500 | Walkthrough | Request author explanation, check design first |
| XL | 500+ | Split required | Block merge, ask to split into logical units |

### XS/S review checklist
```
[ ] Does the change do exactly what the title says?
[ ] Are edge cases handled (null, empty, out-of-range)?
[ ] Are variable names clear?
[ ] Are tests updated or added?
```

### M review checklist
```
[ ] Is the design the simplest solution?
[ ] Are error paths handled?
[ ] Is there duplication that should be extracted?
[ ] Does it follow existing patterns in the codebase?
[ ] Are there security implications (user input, auth)?
[ ] Is the test coverage meaningful (not just happy path)?
```

### L/XL protocol
```
1. Read the PR description and linked ticket first
2. Review architecture/design before line-by-line reading
3. Request a walkthrough if intent is unclear
4. If XL: comment "Please split by [feature / layer / file]"
```

## Performance Review Checklist

### Database
```
[ ] N+1 query? (loop calling DB inside a loop)
[ ] Missing index on filtered/sorted column?
[ ] SELECT * where only specific columns needed?
[ ] Missing pagination on list endpoints?
[ ] Transaction missing on multi-step writes?
```

### React / Frontend
```
[ ] Unnecessary re-renders? (missing memo/useCallback/useMemo)
[ ] Large component re-renders on every keystroke?
[ ] Images missing width/height (layout shift)?
[ ] Heavy dependency imported at top level (should be lazy)?
[ ] Bundle size impact? (check with next build or vite --report)
```

### General backend
```
[ ] Synchronous I/O inside async handler?
[ ] Missing cache for repeated identical queries?
[ ] Large payload returned when only summary needed?
[ ] Polling where event/webhook would be better?
```

## Architecture Conformance Checks

### Layer violation detection
```
Controller → Service → Repository → DB     (ALLOWED)
Controller → Repository → DB               (VIOLATION: skip service)
Service → Controller                       (VIOLATION: wrong direction)
Repository → Service                       (VIOLATION: wrong direction)
```

Red flags in the diff:
- `import { db } from '../db'` inside a route handler file
- `import { Router } from 'express'` inside a service file
- Direct `fetch()` calls inside a React component (should be in a hook or service)

### Dependency direction (clean architecture)
```
Entities (innermost) — no imports from outer rings
Use Cases — import Entities only
Adapters — import Use Cases and Entities
Frameworks — import everything, imported by nothing
```

### Feature coupling detection
```
[ ] Does feature A import from feature B's internals?
[ ] If yes, should this be a shared utility or event instead?
[ ] Are feature-specific types leaking into shared modules?
```

## Framework-Specific Review Patterns

### React
```
[ ] Hooks called conditionally? (rules of hooks violation)
[ ] Missing key prop in lists? Or key is array index?
[ ] useEffect missing cleanup return for subscriptions/timers?
[ ] State mutation instead of new object? ({ ...prev, field: val })
[ ] Prop drilling 3+ levels deep? (consider context or composition)
```

### Next.js
```
[ ] Data fetching happening client-side when it could be server-side?
[ ] 'use client' added unnecessarily to a component with no interactivity?
[ ] Large third-party lib imported in a Server Component?
[ ] Dynamic route missing generateStaticParams for static generation?
[ ] API route missing input validation?
```

### Express
```
[ ] Middleware added in wrong order? (auth before body-parser?)
[ ] Error handler missing 4-argument signature (err, req, res, next)?
[ ] Async handler missing try/catch or asyncHandler wrapper?
[ ] User input used directly in SQL/file path/shell command?
[ ] Missing rate limiter on public endpoints?
```

## Review Comment Templates

### Nitpick (non-blocking)
```
nit: Consider renaming `data` to `userProfile` for clarity — easy to
confuse with the raw API response above.
```

### Suggestion (non-blocking, better approach available)
```
suggestion: This could use `Promise.all` to run both requests in
parallel instead of sequentially. Would save ~300ms per call.

  // instead of:
  const a = await fetchA()
  const b = await fetchB()

  // consider:
  const [a, b] = await Promise.all([fetchA(), fetchB()])
```

### Blocker (must fix before merge)
```
blocker: This passes `req.params.id` directly into the SQL query
string — SQL injection risk. Use a parameterized query:

  db.query('SELECT * FROM users WHERE id = $1', [req.params.id])
```

### Praise (leave these too — morale matters)
```
nice: Clean separation of concerns here. The service layer staying
unaware of the HTTP layer makes this easy to test.
```

## Review Anti-Patterns to Avoid

- Bike-shedding on style that the linter already enforces
- Asking "why not X?" without explaining why X would be better
- Leaving blockers with no suggested fix
- Reviewing XL PRs line by line without first understanding the design
- Approving without reading tests
