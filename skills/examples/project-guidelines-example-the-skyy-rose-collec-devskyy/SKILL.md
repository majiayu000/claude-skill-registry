---
name: project-guidelines-example
description: Template for project-specific skills with architecture and patterns.
---

# Project Guidelines (Example Template)

## Architecture

```
Frontend: Next.js 15 + TypeScript → Backend: FastAPI + Pydantic → DB: Supabase
```

## Code Patterns

**API Response** (Python):
```python
class ApiResponse(BaseModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    error: Optional[str] = None
```

**API Call** (TypeScript):
```typescript
const result = await fetch(`/api${endpoint}`)
return result.success ? result.data : throw new Error(result.error)
```

## Testing Requirements

```bash
pytest tests/ --cov=. --cov-report=html  # Backend (80%+ coverage)
npm run test -- --coverage              # Frontend
npm run test:e2e                        # Playwright
```

## Critical Rules

1. No emojis in code
2. Immutability - never mutate
3. TDD - tests first
4. 80% coverage minimum
5. Files < 800 lines

## Related Tools
- **Skill**: `coding-standards`, `backend-patterns`, `frontend-patterns`, `tdd-workflow`
- **Agent**: `planner`, `code-reviewer`
