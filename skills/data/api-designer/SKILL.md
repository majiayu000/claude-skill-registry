---
name: api-designer
description: "API design and implementation. Use for 'API', 'endpoint', 'route' requests"
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Task
---

# API Designer Skill

## Role

Backend developer who designs and implements RESTful APIs

## API Design Principles

### RESTful Rules
| Method | Purpose | Path Pattern |
|--------|---------|--------------|
| GET | Retrieve | `/api/resources`, `/api/resources/:id` |
| POST | Create | `/api/resources` |
| PATCH | Partial update | `/api/resources/:id` |
| PUT | Full replace | `/api/resources/:id` |
| DELETE | Delete | `/api/resources/:id` |

### Response Format
```typescript
// Success
{ data: T }
{ data: T[], total?: number }

// Error
{ error: string, details?: unknown }
```

### HTTP Status Codes
| Code | Purpose |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad request |
| 404 | Not found |
| 500 | Server error |

## Implementation Order

### 1. Type Definition (packages/shared)
```typescript
// packages/shared/src/index.ts
export type CreateFeatureRequest = {
  name: string;
  description?: string;
};

export type FeatureResponse = {
  id: string;
  name: string;
  description: string | null;
  createdAt: string;
};
```

### 2. DB Schema (if needed)
```typescript
// packages/db/src/schema.ts
export const features = sqliteTable('features', {
  id: text('id').primaryKey(),
  name: text('name').notNull(),
  description: text('description'),
  createdAt: text('created_at').notNull(),
});
```

### 3. Route Implementation
```typescript
// apps/server/src/routes/features.ts
import { Router } from 'express';
import { db } from '@local-review/db';
import { features } from '@local-review/db/schema';
import { nanoid } from 'nanoid';

const router = Router();

// GET /api/features
router.get('/', async (req, res) => {
  try {
    const result = await db.select().from(features);
    res.json(result);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch features' });
  }
});

// POST /api/features
router.post('/', async (req, res) => {
  try {
    const { name, description } = req.body;

    if (!name) {
      return res.status(400).json({ error: 'Name is required' });
    }

    const newFeature = {
      id: nanoid(),
      name,
      description: description ?? null,
      createdAt: new Date().toISOString(),
    };

    await db.insert(features).values(newFeature);
    res.status(201).json(newFeature);
  } catch (error) {
    res.status(500).json({ error: 'Failed to create feature' });
  }
});

export default router;
```

### 4. Register Route
```typescript
// apps/server/src/index.ts
import featuresRouter from './routes/features';
app.use('/api/features', featuresRouter);
```

### 5. Frontend API Client
```typescript
// apps/web/src/lib/api.ts
export const featureApi = {
  list: () => fetchJson<FeatureResponse[]>('/api/features'),
  create: (data: CreateFeatureRequest) =>
    fetchJson<FeatureResponse>('/api/features', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
};
```

## Existing API Reference

Current project API structure:
- `GET /api/git/branches` - Branch list
- `GET/POST /api/sessions` - Session CRUD
- `GET/POST /api/sessions/:id/comments` - Comments
- `PATCH /api/sessions/:id/files/*/status` - File status
