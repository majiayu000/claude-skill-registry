---
name: generic-feature-developer
description: Guide feature development with architecture patterns for any tech stack. Covers frontend, backend, full-stack, and automation projects. Use when adding new features, modifying systems, or planning changes.
---

# Generic Feature Developer

Guide feature development across any tech stack.

## When to Use This Skill

**Use for:**

- Adding new features to existing codebase
- Modifying or extending current systems
- Planning architectural changes
- Choosing between implementation approaches
- Designing data flow for new functionality

**Don't use when:**

- Pure UI/styling work → use `generic-design-system`
- UX design decisions → use `generic-ux-designer`
- Code review → use `generic-code-reviewer`

## Development Workflow

1. **Understand** - Read CLAUDE.md, identify affected files, list constraints
2. **Plan** - Choose patterns, design data flow, identify edge cases
3. **Implement** - Small testable changes, commit frequently
4. **Test & Document** - Write tests, update docs, performance check

## Architecture by Project Type

### Static Sites

```
project/
├── index.html
├── css/           # variables.css, style.css
├── js/            # main.js, utils.js
└── assets/
```

**Patterns:** CSS variables, ES modules, event delegation

### React/Next.js

```
src/
├── components/    # ui/, features/, layout/
├── hooks/
├── stores/
├── services/
└── types/
```

**Patterns:** Container/Presentational, custom hooks, Zustand/React Query

### NestJS Backend

```
src/
├── modules/[feature]/
│   ├── feature.module.ts
│   ├── feature.controller.ts
│   ├── feature.service.ts
│   └── dto/
└── common/        # guards, decorators
```

**Patterns:** Module organization, DTOs, Guards, Prisma

## Feature Decision Framework

### Scope Assessment (First)

| Scope                 | Action                                |
| --------------------- | ------------------------------------- |
| Single component      | Implement directly                    |
| Cross-cutting concern | Design interface first                |
| New subsystem         | Create architecture doc, get approval |

### Build vs Integrate

| Factor                   | Build Custom | Use Library |
| ------------------------ | ------------ | ----------- |
| Core to product          | Yes          |             |
| Commodity feature        |              | Yes         |
| Tight integration needed | Yes          |             |
| Time-critical            |              | Yes         |
| Long-term ownership      | Yes          |             |

### State Management Selection

| Scope           | Solution                 |
| --------------- | ------------------------ |
| Component-local | useState/useReducer      |
| Feature-wide    | Context or Zustand slice |
| App-wide        | Zustand/Redux store      |
| Server state    | React Query/SWR          |
| Form state      | React Hook Form          |

### API Design Checklist

- [ ] RESTful or GraphQL decision documented
- [ ] Authentication method chosen
- [ ] Error response format standardized
- [ ] Pagination strategy defined
- [ ] Rate limiting considered

## Common Features

### Adding UI Component

1. Create component → 2. Export → 3. Add tests → 4. Document

### Adding API Endpoint

1. Define route → 2. Add validation → 3. Implement service → 4. Test

### Adding State Management

1. Define shape → 2. Create store → 3. Add actions → 4. Connect components

### Database Changes

1. Design schema → 2. Create migration → 3. Update models → 4. Add service

## Data Flow Patterns

### Frontend Data Flow

```
User Action → Event Handler → State Update → Re-render → UI Feedback
```

- **Optimistic updates:** Update UI immediately, rollback on error
- **Pessimistic updates:** Wait for server confirmation
- **Decision:** Optimistic for low-risk (likes), pessimistic for high-risk (payments)

### API Request Flow

```
Request → Auth Check → Validation → Business Logic → Database → Response
```

- Early exit on validation failure
- Transaction boundaries around multi-step operations
- Consistent error response format

### Event-Driven Patterns

| Event Type       | Approach                    |
| ---------------- | --------------------------- |
| User events      | Immediate feedback          |
| Server events    | WebSocket/SSE for real-time |
| Background tasks | Queue for long operations   |

## Error Handling Strategy

| Error Type   | Frontend                  | Backend            |
| ------------ | ------------------------- | ------------------ |
| Validation   | Inline field errors       | 400 + field errors |
| Auth         | Redirect to login         | 401/403            |
| Not Found    | Empty state or redirect   | 404                |
| Server Error | Generic message + retry   | 500 + log          |
| Network      | Offline indicator + queue | N/A                |

### Frontend Pattern

```typescript
try {
  await apiCall();
} catch (error) {
  if (error instanceof ValidationError) showFieldErrors(error.fields);
  else showGenericError();
}
```

### Backend Pattern

```typescript
if (err instanceof ValidationError)
  return res.status(400).json({ errors: err.errors });
if (err instanceof AuthError)
  return res.status(401).json({ message: "Unauthorized" });
```

## Testing Strategy

| Layer | Type        | Tools           |
| ----- | ----------- | --------------- |
| UI    | Component   | Testing Library |
| Logic | Unit        | Jest, Vitest    |
| API   | Integration | Supertest       |
| E2E   | End-to-end  | Playwright      |

## Performance

**Frontend:** Code splitting, lazy loading, memoization, debounce
**Backend:** DB indexing, caching, connection pooling, background jobs

## Feature Implementation Checklist

Before marking feature complete:

- [ ] Works for happy path
- [ ] Error states handled
- [ ] Loading states implemented
- [ ] Edge cases tested
- [ ] TypeScript types complete
- [ ] Tests written
- [ ] Documentation updated

## See Also

- [Code Review Standards](./../_shared/CODE_REVIEW_STANDARDS.md) - Quality checks
- [Design Patterns](./../_shared/DESIGN_PATTERNS.md) - UI patterns
- `generic-design-system` - For styling and visual consistency
- `generic-ux-designer` - For UX flow decisions
- Project `CLAUDE.md` - Workflow rules

**READ shared standards when:**

- Complex feature design → CODE_REVIEW_STANDARDS.md (architecture section)
- UI component patterns → DESIGN_PATTERNS.md (component section)
