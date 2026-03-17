---
name: backend-api
description: Create Express.js API endpoints for IntelliFill following established patterns (Prisma, Supabase auth, Joi validation, Bull queues). Use when creating new API routes, services, or middleware.
---

# Backend API Development Skill

This skill provides comprehensive guidance for creating Express.js API endpoints in the IntelliFill backend (`quikadmin/`).

## Table of Contents

1. [Route Factory Pattern](#route-factory-pattern)
2. [Validation with Joi](#validation-with-joi)
3. [Service Layer](#service-layer)
4. [Authentication Middleware](#authentication-middleware)
5. [Error Handling](#error-handling)
6. [Rate Limiting](#rate-limiting)
7. [Background Jobs with Bull](#background-jobs-with-bull)
8. [Testing Patterns](#testing-patterns)

## Route Factory Pattern

IntelliFill uses a modular route pattern where each domain has its own route file.

### File Structure

```
quikadmin/src/api/
├── routes.ts                 # Main route registry
├── auth.routes.ts            # Authentication routes
├── documents.routes.ts       # Document management
├── templates.routes.ts       # Template CRUD
├── knowledge.routes.ts       # Knowledge base
└── users.routes.ts           # User profile
```

### Route File Template

```typescript
// quikadmin/src/api/[domain].routes.ts
import { Router, Request, Response, NextFunction } from 'express';
import { validateRequest } from '../middleware/validation';
import { authMiddleware } from '../middleware/supabaseAuth';
import { rateLimiter } from '../middleware/rateLimiter';
import * as schemas from '../validators/schemas/[domain].schemas';
import logger from '../utils/logger';

const router = Router();

/**
 * GET /api/[domain]
 * List all items with pagination
 */
router.get(
  '/',
  authMiddleware,
  rateLimiter('standard'),
  async (req: Request, res: Response, next: NextFunction) => {
    try {
      const userId = req.user?.id;
      const { page = 1, limit = 20 } = req.query;

      // Service call
      const items = await domainService.list({
        userId,
        page: Number(page),
        limit: Number(limit),
      });

      res.json({
        success: true,
        data: items,
        meta: {
          page: Number(page),
          limit: Number(limit),
        },
      });
    } catch (error) {
      next(error);
    }
  }
);

/**
 * POST /api/[domain]
 * Create new item with validation
 */
router.post(
  '/',
  authMiddleware,
  rateLimiter('strict'),
  validateRequest(schemas.createSchema),
  async (req: Request, res: Response, next: NextFunction) => {
    try {
      const userId = req.user?.id;
      const data = req.body;

      const item = await domainService.create({
        userId,
        data,
      });

      logger.info('[domain] Created', { userId, itemId: item.id });

      res.status(201).json({
        success: true,
        data: item,
      });
    } catch (error) {
      next(error);
    }
  }
);

export default router;
```

### Registering Routes

Register new routes in `quikadmin/src/api/routes.ts`:

```typescript
import express from 'express';
import authRoutes from './auth.routes';
import documentsRoutes from './documents.routes';
import newDomainRoutes from './newDomain.routes'; // Your new routes

const router = express.Router();

router.use('/auth/v2', authRoutes);
router.use('/documents', documentsRoutes);
router.use('/new-domain', newDomainRoutes); // Register here

export default router;
```

## Validation with Joi

IntelliFill uses Joi for request validation.

### Schema Location

```
quikadmin/src/validators/schemas/
├── auth.schemas.ts
├── documents.schemas.ts
├── templates.schemas.ts
└── [domain].schemas.ts
```

### Validation Schema Pattern

```typescript
// quikadmin/src/validators/schemas/[domain].schemas.ts
import Joi from 'joi';

/**
 * Create item schema
 */
export const createSchema = Joi.object({
  name: Joi.string().min(1).max(255).required(),
  description: Joi.string().max(1000).optional(),
  type: Joi.string().valid('type1', 'type2', 'type3').required(),
  metadata: Joi.object({
    category: Joi.string().optional(),
    tags: Joi.array().items(Joi.string()).optional(),
  }).optional(),
  isPublic: Joi.boolean().default(false),
});

/**
 * Update item schema (all fields optional)
 */
export const updateSchema = Joi.object({
  name: Joi.string().min(1).max(255).optional(),
  description: Joi.string().max(1000).optional(),
  type: Joi.string().valid('type1', 'type2', 'type3').optional(),
  metadata: Joi.object().optional(),
  isPublic: Joi.boolean().optional(),
}).min(1); // At least one field required

/**
 * Query parameters schema
 */
export const listQuerySchema = Joi.object({
  page: Joi.number().integer().min(1).default(1),
  limit: Joi.number().integer().min(1).max(100).default(20),
  search: Joi.string().max(255).optional(),
  type: Joi.string().valid('type1', 'type2', 'type3').optional(),
  sortBy: Joi.string().valid('name', 'createdAt', 'updatedAt').default('createdAt'),
  sortOrder: Joi.string().valid('asc', 'desc').default('desc'),
});

/**
 * ID parameter schema
 */
export const idParamSchema = Joi.object({
  id: Joi.string().uuid().required(),
});
```

### Using Validation Middleware

```typescript
import { validateRequest } from '../middleware/validation';
import * as schemas from '../validators/schemas/domain.schemas';

// Body validation
router.post('/', validateRequest(schemas.createSchema), handler);

// Query validation
router.get('/', validateRequest(schemas.listQuerySchema, 'query'), handler);

// Param validation
router.get('/:id', validateRequest(schemas.idParamSchema, 'params'), handler);

// Multiple validations
router.patch(
  '/:id',
  validateRequest(schemas.idParamSchema, 'params'),
  validateRequest(schemas.updateSchema),
  handler
);
```

## Service Layer

Services contain business logic and are injected with dependencies.

### Service Location

```
quikadmin/src/services/
├── [domain].service.ts
└── __tests__/
    └── [domain].service.test.ts
```

### Service Pattern

```typescript
// quikadmin/src/services/[domain].service.ts
import { PrismaClient } from '@prisma/client';
import logger from '../utils/logger';
import { AppError } from '../utils/errors';

export interface DomainServiceDeps {
  prisma: PrismaClient;
}

export class DomainService {
  private prisma: PrismaClient;

  constructor(deps: DomainServiceDeps) {
    this.prisma = deps.prisma;
  }

  /**
   * List items with pagination
   */
  async list(params: {
    userId: string;
    page: number;
    limit: number;
    search?: string;
  }) {
    const { userId, page, limit, search } = params;
    const skip = (page - 1) * limit;

    const where = {
      userId,
      ...(search && {
        OR: [
          { name: { contains: search, mode: 'insensitive' as const } },
          { description: { contains: search, mode: 'insensitive' as const } },
        ],
      }),
    };

    const [items, total] = await Promise.all([
      this.prisma.domain.findMany({
        where,
        skip,
        take: limit,
        orderBy: { createdAt: 'desc' },
      }),
      this.prisma.domain.count({ where }),
    ]);

    return {
      items,
      total,
      page,
      limit,
      totalPages: Math.ceil(total / limit),
    };
  }

  /**
   * Get single item by ID
   */
  async getById(id: string, userId: string) {
    const item = await this.prisma.domain.findFirst({
      where: { id, userId },
    });

    if (!item) {
      throw new AppError('Item not found', 404);
    }

    return item;
  }

  /**
   * Create new item
   */
  async create(params: { userId: string; data: CreateData }) {
    const { userId, data } = params;

    const item = await this.prisma.domain.create({
      data: {
        ...data,
        userId,
      },
    });

    logger.info('Domain item created', { userId, itemId: item.id });

    return item;
  }

  /**
   * Update existing item
   */
  async update(id: string, userId: string, data: UpdateData) {
    // Verify ownership
    await this.getById(id, userId);

    const item = await this.prisma.domain.update({
      where: { id },
      data,
    });

    logger.info('Domain item updated', { userId, itemId: item.id });

    return item;
  }

  /**
   * Delete item
   */
  async delete(id: string, userId: string) {
    // Verify ownership
    await this.getById(id, userId);

    await this.prisma.domain.delete({
      where: { id },
    });

    logger.info('Domain item deleted', { userId, itemId: id });
  }
}

// Export singleton instance
import prisma from '../utils/prisma';

export const domainService = new DomainService({ prisma });
```

## Authentication Middleware

IntelliFill uses Supabase for authentication.

### Auth Middleware Usage

```typescript
import { authMiddleware } from '../middleware/supabaseAuth';

// Protected route
router.get('/protected', authMiddleware, async (req, res) => {
  const userId = req.user?.id; // Type-safe user object
  const userEmail = req.user?.email;

  // Your logic here
});

// Public route (no authMiddleware)
router.get('/public', async (req, res) => {
  // Your logic here
});
```

### User Object Type

```typescript
// Available in req.user after authMiddleware
interface User {
  id: string;
  email: string;
  role?: string;
  // Other Supabase user fields
}
```

## Error Handling

IntelliFill uses a centralized error handling system.

### Error Classes

```typescript
import { AppError } from '../utils/errors';

// Validation error
throw new AppError('Invalid input', 400);

// Not found
throw new AppError('Resource not found', 404);

// Unauthorized
throw new AppError('Unauthorized', 401);

// Forbidden
throw new AppError('Forbidden', 403);

// Internal server error (will be logged)
throw new AppError('Something went wrong', 500);
```

### Error Handler

All routes should use `next(error)` to pass errors to the global error handler:

```typescript
router.get('/example', async (req, res, next) => {
  try {
    // Your logic
  } catch (error) {
    next(error); // Passes to error handler
  }
});
```

## Rate Limiting

IntelliFill uses Redis-backed rate limiting with in-memory fallback.

### Rate Limiter Usage

```typescript
import { rateLimiter } from '../middleware/rateLimiter';

// Standard rate limit (100 requests/15min)
router.get('/', rateLimiter('standard'), handler);

// Strict rate limit (10 requests/15min)
router.post('/sensitive', rateLimiter('strict'), handler);

// Lenient rate limit (1000 requests/15min)
router.get('/public', rateLimiter('lenient'), handler);
```

### Custom Rate Limits

```typescript
import { createRateLimiter } from '../middleware/rateLimiter';

const customLimiter = createRateLimiter({
  windowMs: 60 * 1000, // 1 minute
  max: 5, // 5 requests per minute
  keyGenerator: (req) => req.user?.id || req.ip, // Rate limit by user
});

router.post('/expensive-operation', customLimiter, handler);
```

## Background Jobs with Bull

IntelliFill uses Bull queues for async processing.

### Queue Setup

```typescript
// quikadmin/src/queues/[domain]Queue.ts
import Queue from 'bull';
import logger from '../utils/logger';

export interface JobData {
  userId: string;
  itemId: string;
  // Other job data
}

export const domainQueue = new Queue<JobData>('domain-processing', {
  redis: {
    host: process.env.REDIS_HOST || 'localhost',
    port: Number(process.env.REDIS_PORT) || 6379,
  },
});

// Job processor
domainQueue.process(async (job) => {
  const { userId, itemId } = job.data;

  logger.info('Processing domain job', { userId, itemId });

  try {
    // Your processing logic
    await processItem(itemId);

    logger.info('Domain job completed', { userId, itemId });
  } catch (error) {
    logger.error('Domain job failed', { userId, itemId, error });
    throw error; // Retry based on queue settings
  }
});

// Error handling
domainQueue.on('failed', (job, err) => {
  logger.error('Queue job failed', { jobId: job.id, error: err });
});
```

### Adding Jobs

```typescript
import { domainQueue } from '../queues/domainQueue';

// In your route handler
const job = await domainQueue.add(
  {
    userId: req.user?.id,
    itemId: item.id,
  },
  {
    attempts: 3,
    backoff: {
      type: 'exponential',
      delay: 2000,
    },
  }
);

res.json({
  success: true,
  jobId: job.id,
});
```

## Testing Patterns

### API Route Test Template

```typescript
// quikadmin/src/api/__tests__/[domain].routes.test.ts
import request from 'supertest';
import app from '../../app';
import prisma from '../../utils/prisma';

describe('Domain API Routes', () => {
  const mockUser = {
    id: 'user-123',
    email: 'test@example.com',
  };

  // Mock auth middleware
  jest.mock('../../middleware/supabaseAuth', () => ({
    authMiddleware: (req: any, res: any, next: any) => {
      req.user = mockUser;
      next();
    },
  }));

  afterEach(async () => {
    await prisma.domain.deleteMany();
  });

  describe('GET /api/domain', () => {
    it('should list items', async () => {
      const response = await request(app)
        .get('/api/domain')
        .set('Authorization', 'Bearer fake-token')
        .expect(200);

      expect(response.body).toHaveProperty('success', true);
      expect(response.body).toHaveProperty('data');
    });
  });

  describe('POST /api/domain', () => {
    it('should create item', async () => {
      const response = await request(app)
        .post('/api/domain')
        .set('Authorization', 'Bearer fake-token')
        .send({
          name: 'Test Item',
          type: 'type1',
        })
        .expect(201);

      expect(response.body.data).toHaveProperty('id');
      expect(response.body.data.name).toBe('Test Item');
    });

    it('should validate input', async () => {
      const response = await request(app)
        .post('/api/domain')
        .set('Authorization', 'Bearer fake-token')
        .send({}) // Missing required fields
        .expect(400);

      expect(response.body).toHaveProperty('success', false);
    });
  });
});
```

## Best Practices

1. **Always use TypeScript types** - Define interfaces for all request/response shapes
2. **Validate all inputs** - Use Joi schemas for validation
3. **Use service layer** - Keep route handlers thin, move logic to services
4. **Error handling** - Always use try/catch and pass errors to next()
5. **Logging** - Log important operations with structured context
6. **Rate limiting** - Apply appropriate rate limits to all routes
7. **Authentication** - Use authMiddleware for protected routes
8. **Testing** - Write tests for happy path and error cases
9. **Documentation** - Add JSDoc comments to routes and services
10. **Transactions** - Use Prisma transactions for multi-step operations

## Common Patterns

### Batch Operations

```typescript
router.post('/batch', authMiddleware, async (req, res, next) => {
  try {
    const { ids } = req.body;
    const userId = req.user?.id;

    const results = await prisma.$transaction(
      ids.map((id: string) =>
        prisma.domain.update({
          where: { id },
          data: { processed: true },
        })
      )
    );

    res.json({ success: true, data: results });
  } catch (error) {
    next(error);
  }
});
```

### File Upload

```typescript
import multer from 'multer';

const upload = multer({
  dest: 'uploads/',
  limits: { fileSize: 10 * 1024 * 1024 }, // 10MB
});

router.post(
  '/upload',
  authMiddleware,
  upload.single('file'),
  async (req, res, next) => {
    try {
      const file = req.file;
      const userId = req.user?.id;

      // Process file
      const result = await processFile(file, userId);

      res.json({ success: true, data: result });
    } catch (error) {
      next(error);
    }
  }
);
```

### Soft Delete

```typescript
async softDelete(id: string, userId: string) {
  await this.getById(id, userId);

  return this.prisma.domain.update({
    where: { id },
    data: { deletedAt: new Date() },
  });
}

// Exclude soft-deleted in queries
async list(params: ListParams) {
  const where = {
    userId: params.userId,
    deletedAt: null, // Exclude soft-deleted
  };

  return this.prisma.domain.findMany({ where });
}
```

## References

- [Express.js Documentation](https://expressjs.com/)
- [Prisma Client API](https://www.prisma.io/docs/reference/api-reference/prisma-client-reference)
- [Joi Validation](https://joi.dev/api/)
- [Bull Queue](https://github.com/OptimalBits/bull)
- [Supabase Auth](https://supabase.com/docs/guides/auth)
