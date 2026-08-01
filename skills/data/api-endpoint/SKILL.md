---
name: api-endpoint
description: Route (backend/src/api/routes/)     → DI setup + routing
---

---
name: api-endpoint
description: Create or modify API endpoints in IdeaForge backend. Triggers: new route, controller, service, repository, CRUD operation, Zod validation, API debugging. Pattern: Routes → Controller → Service → Repository.
---

# API Endpoints

## Architecture

```
Route (backend/src/api/routes/)     → DI setup + routing
Controller (backend/src/api/controllers/) → Zod validation + ApiResponse
Service (backend/src/services/)     → Business logic
Repository (backend/src/repositories/) → Database queries
```

## Quick Start

### 1. Route (`routes/{resource}.ts`)
```typescript
import { Router } from 'express';
const router = Router();

// Manual DI
const repo = new MyRepository();
const service = new MyService(repo);
const controller = new MyController(service);

router.get('/', (req, res, next) => controller.getAll(req, res, next));
router.post('/', (req, res, next) => controller.create(req, res, next));

export default router;
```

### 2. Controller (`controllers/{resource}Controller.ts`)
```typescript
const CreateSchema = z.object({
  name: z.string().min(1).max(255),
});

export class MyController {
  constructor(private service: MyService) {}

  async create(req: Request, res: Response, next: NextFunction) {
    try {
      const data = CreateSchema.parse(req.body);
      const result = await this.service.create(data);
      res.json({ success: true, data: result } as ApiResponse<typeof result>);
    } catch (error) {
      next(error);
    }
  }
}
```

### 3. Register (`index.ts`)
```typescript
import myRouter from './api/routes/my';
app.use('/api/my-resource', myRouter);
```

## Response Format

```typescript
// Success
{ success: true, data: { ... } }

// Error (via errorHandler middleware)
{ success: false, error: { message: "...", code: "ERROR_CODE" } }
```

## Rules

1. Controllers: validation + response only
2. Services: all business logic
3. Always use `ApiResponse<T>` wrapper
4. Always `next(error)` - never catch and format
5. Zod for all input validation
6. Manual DI in route files