---
name: feature-impl
description: "New feature implementation. Use for 'add feature', 'implement', 'new feature' requests"
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Task
---

# Feature Implementation Skill

## Role

Developer who designs and implements new features

## Implementation Process

### 1. Requirements Analysis
- Understand feature purpose and scope
- Check relationship with existing code
- List files that need changes

### 2. Design
- Check if data model changes needed (packages/db/src/schema.ts)
- Design API endpoints (apps/server/src/routes/)
- Design UI components (apps/web/src/components/)
- Define shared types (packages/shared/src/index.ts)

### 3. Implementation Order
1. **DB Schema** - Add tables/columns if needed
2. **Shared Types** - Define API request/response types
3. **Backend API** - Implement routes and services
4. **Frontend Hooks** - Write React Query hooks
5. **UI Components** - Implement screens

### 4. Verification
- Ensure type check passes
- Test API
- Verify UI behavior

## File Creation Locations

| Type | Path |
|------|------|
| DB Schema | `packages/db/src/schema.ts` |
| Shared Types | `packages/shared/src/index.ts` |
| API Routes | `apps/server/src/routes/[name].ts` |
| Services | `apps/server/src/services/[name].service.ts` |
| React Hooks | `apps/web/src/hooks/use[Name].ts` |
| Pages | `apps/web/src/pages/[Name]Page.tsx` |
| Components | `apps/web/src/components/[feature]/[Name].tsx` |

## Code Patterns

### API Route Template
```typescript
import { Router } from 'express';
import { db } from '@local-review/db';

const router = Router();

router.get('/', async (req, res) => {
  try {
    const result = await db.query...
    res.json(result);
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
});

export default router;
```

### React Query Hook Template
```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '../lib/api';

export function useFeature() {
  return useQuery({
    queryKey: ['feature'],
    queryFn: () => api.get('/api/feature'),
  });
}
```
