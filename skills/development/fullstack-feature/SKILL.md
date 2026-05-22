---
name: fullstack-feature
description: Orchestrates creating a complete fullstack feature across backend and frontend. Use when adding new features that span both layers.
---

# Fullstack Feature

Orchestrates the creation of a complete feature across backend and frontend.

## Overview

A fullstack feature typically requires:
1. Backend API module (Clean Architecture)
2. Database migration
3. Frontend API types generation
4. Frontend hooks
5. Frontend page and components

## Workflow

### Phase 1: Backend

**Step 1: Create API Module**

Use the `create-api-module` skill or scaffold script:
```bash
python .claude/skills/create-api-module/scripts/scaffold_module.py {feature_name}
```

This creates:
- `back/src/api/{feature}/` with Clean Architecture structure
- `back/tests/api/{feature}/` with test files

**Step 2: Customize the Module**

1. Update models in `infrastructure/models.py`
2. Add repository methods in `infrastructure/repository.py`
3. Implement business logic in `domain/`
4. Create API endpoints in `api/router.py`
5. Register router in `back/src/api/routes.py`

**Step 3: Create Database Migration**

```bash
docker compose exec back uv run alembic revision --autogenerate -m "Add {feature} table"
```

**Step 4: Run Backend Tests**

```bash
cd back && task tests
```

### Phase 2: Frontend

**Step 5: Generate API Types**

Ensure backend is running, then:
```bash
cd front && pnpm run generate:api
```

**Step 6: Create Feature Hook**

Create `front/lib/hooks/use-{feature}.ts`:
- Query key factory
- `use{Feature}Suspense` for data fetching
- Mutation hooks for create/update/delete

See `add-feature-hook` skill for patterns.

**Step 7: Create Page and Components**

Create:
- `front/app/{feature}/page.tsx` - Auth wrapper
- `front/app/{feature}/loading.tsx` - Loading state
- `front/components/{feature}/{Feature}Content.tsx` - Data fetching + UI

See `add-protected-page` skill for patterns.

**Step 8: Update Middleware** (if needed)

```typescript
// front/middleware.ts
const isProtectedRoute = createRouteMatcher([
  '/dashboard(.*)',
  // ... existing routes
  '/{feature}(.*)', // Add new route
]);
```

### Phase 3: Quality Checks

**Step 9: Run All Quality Checks**

Backend:
```bash
cd back && task format && task tests
```

Frontend:
```bash
cd front && pnpm type-check && pnpm lint && pnpm test
```

## Checklist

- [ ] Backend module created with Clean Architecture
- [ ] Database migration created and applied
- [ ] Backend tests passing
- [ ] API types generated in frontend
- [ ] Feature hook created
- [ ] Page and components created
- [ ] Middleware updated (if protected route)
- [ ] All quality checks passing

## Related Skills

- `create-api-module` - Backend module creation
- `create-db-migration` - Database migrations
- `add-protected-page` - Frontend page creation
- `add-feature-hook` - Frontend API hooks
- `backend-quality` - Backend quality checks
- `frontend-quality` - Frontend quality checks
