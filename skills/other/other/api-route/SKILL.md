---
name: api-route
description: Generate API route handlers for Express or Analog.js
argument-hint: <framework> <route-name>
---

# Generate API Route

Create API route handlers for either Express (Angular SSR) or Analog.js.

## Arguments

- First argument: Framework - "express" or "analog"
- Second argument: Route name (e.g., "health", "custom-endpoint")

## For Express (Angular SSR)

Create handler in `apps/cms-admin/src/api/<route-name>.ts`:

```typescript
import { Router, Request, Response } from 'express';
import type { CollectionConfig } from '@momentumcms/core';

export function create<PascalName>Routes(collections: CollectionConfig[]): Router {
  const router = Router();

  router.get('/<route-name>', async (req: Request, res: Response) => {
    try {
      // Implementation
      res.json({ success: true });
    } catch (error) {
      res.status(500).json({ error: 'Internal server error' });
    }
  });

  return router;
}
```

Register in `apps/cms-admin/src/server.ts`:

```typescript
import { create<PascalName>Routes } from './api/<route-name>';

app.use('/api', create<PascalName>Routes(collections));
```

## For Analog.js

Create file-based route in `src/server/routes/api/<route-name>.get.ts`:

```typescript
import { defineEventHandler, getQuery } from 'h3';

export default defineEventHandler(async (event) => {
	const query = getQuery(event);

	try {
		// Implementation
		return { success: true };
	} catch (error) {
		throw createError({
			statusCode: 500,
			statusMessage: 'Internal server error',
		});
	}
});
```

## HTTP Method Suffixes (Analog.js)

- `index.get.ts` - GET request
- `index.post.ts` - POST request
- `[id].get.ts` - GET with dynamic param
- `[id].patch.ts` - PATCH with dynamic param
- `[id].delete.ts` - DELETE with dynamic param
- `[...].ts` - Catch-all route

## h3 Utilities

```typescript
import {
	defineEventHandler,
	getQuery,
	readBody,
	getRouterParam,
	createError,
	setResponseStatus,
} from 'h3';
```
