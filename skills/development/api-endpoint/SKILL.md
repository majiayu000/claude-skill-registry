---
name: api-endpoint
description: Create REST or GraphQL API endpoints with proper validation, error handling, authentication, and documentation. Use when building backend APIs or serverless functions.
---

# API Endpoint Development

Best practices for building secure, maintainable REST APIs.

## Endpoint Structure

### Express/Node.js Template

```typescript
import { Router, Request, Response, NextFunction } from 'express';
import { z } from 'zod';
import { authenticate, authorize } from '../middleware/auth';
import { validate } from '../middleware/validation';
import { asyncHandler } from '../utils/asyncHandler';
import { ApiError } from '../utils/ApiError';

const router = Router();

// Schema definitions
const createUserSchema = z.object({
  body: z.object({
    name: z.string().min(1).max(100),
    email: z.string().email(),
    role: z.enum(['user', 'admin']).default('user'),
  }),
});

const getUserSchema = z.object({
  params: z.object({
    id: z.string().uuid(),
  }),
});

// Endpoints
router.post(
  '/users',
  authenticate,
  authorize('admin'),
  validate(createUserSchema),
  asyncHandler(async (req: Request, res: Response) => {
    const user = await UserService.create(req.body);
    res.status(201).json({
      success: true,
      data: user,
    });
  })
);

router.get(
  '/users/:id',
  authenticate,
  validate(getUserSchema),
  asyncHandler(async (req: Request, res: Response) => {
    const user = await UserService.findById(req.params.id);
    if (!user) {
      throw new ApiError(404, 'User not found');
    }
    res.json({
      success: true,
      data: user,
    });
  })
);

export default router;
```

## Input Validation

### Zod Schema Validation

```typescript
import { z } from 'zod';

// Basic schemas
const emailSchema = z.string().email().toLowerCase();
const passwordSchema = z.string().min(8).max(100);
const uuidSchema = z.string().uuid();

// Complex object schema
const createPostSchema = z.object({
  body: z.object({
    title: z.string().min(1).max(255).trim(),
    content: z.string().min(10).max(10000),
    tags: z.array(z.string()).max(10).optional(),
    status: z.enum(['draft', 'published']).default('draft'),
    publishAt: z.string().datetime().optional(),
  }),
});

// Query params schema
const listPostsSchema = z.object({
  query: z.object({
    page: z.coerce.number().int().positive().default(1),
    limit: z.coerce.number().int().min(1).max(100).default(20),
    status: z.enum(['draft', 'published', 'all']).default('all'),
    sortBy: z.enum(['createdAt', 'updatedAt', 'title']).default('createdAt'),
    order: z.enum(['asc', 'desc']).default('desc'),
    search: z.string().max(100).optional(),
  }),
});

// Validation middleware
function validate(schema: z.ZodSchema) {
  return async (req: Request, res: Response, next: NextFunction) => {
    try {
      const validated = await schema.parseAsync({
        body: req.body,
        query: req.query,
        params: req.params,
      });
      req.body = validated.body ?? req.body;
      req.query = validated.query ?? req.query;
      req.params = validated.params ?? req.params;
      next();
    } catch (error) {
      if (error instanceof z.ZodError) {
        return res.status(400).json({
          success: false,
          error: {
            code: 'VALIDATION_ERROR',
            message: 'Validation failed',
            details: error.errors.map(e => ({
              field: e.path.join('.'),
              message: e.message,
            })),
          },
        });
      }
      next(error);
    }
  };
}
```

### Input Sanitization

```typescript
import sanitizeHtml from 'sanitize-html';
import xss from 'xss';

// Sanitize HTML content
function sanitizeContent(content: string): string {
  return sanitizeHtml(content, {
    allowedTags: ['b', 'i', 'em', 'strong', 'a', 'p', 'br', 'ul', 'ol', 'li'],
    allowedAttributes: {
      'a': ['href', 'title'],
    },
    allowedSchemes: ['http', 'https', 'mailto'],
  });
}

// Prevent XSS in plain text
function sanitizeText(text: string): string {
  return xss(text);
}

// Sanitize file names
function sanitizeFileName(fileName: string): string {
  return fileName
    .replace(/[^a-zA-Z0-9.-]/g, '_')
    .replace(/\.{2,}/g, '.')
    .substring(0, 255);
}
```

## Authentication

### JWT Authentication

```typescript
import jwt from 'jsonwebtoken';
import { Request, Response, NextFunction } from 'express';

interface JwtPayload {
  userId: string;
  role: string;
  iat: number;
  exp: number;
}

// Generate tokens
function generateTokens(user: User) {
  const accessToken = jwt.sign(
    { userId: user.id, role: user.role },
    process.env.JWT_SECRET!,
    { expiresIn: '15m' }
  );

  const refreshToken = jwt.sign(
    { userId: user.id, tokenVersion: user.tokenVersion },
    process.env.REFRESH_SECRET!,
    { expiresIn: '7d' }
  );

  return { accessToken, refreshToken };
}

// Authentication middleware
async function authenticate(req: Request, res: Response, next: NextFunction) {
  const authHeader = req.headers.authorization;

  if (!authHeader?.startsWith('Bearer ')) {
    return res.status(401).json({
      success: false,
      error: { code: 'UNAUTHORIZED', message: 'Missing token' },
    });
  }

  const token = authHeader.split(' ')[1];

  try {
    const payload = jwt.verify(token, process.env.JWT_SECRET!) as JwtPayload;
    req.user = { id: payload.userId, role: payload.role };
    next();
  } catch (error) {
    if (error instanceof jwt.TokenExpiredError) {
      return res.status(401).json({
        success: false,
        error: { code: 'TOKEN_EXPIRED', message: 'Token expired' },
      });
    }
    return res.status(401).json({
      success: false,
      error: { code: 'INVALID_TOKEN', message: 'Invalid token' },
    });
  }
}

// Authorization middleware
function authorize(...roles: string[]) {
  return (req: Request, res: Response, next: NextFunction) => {
    if (!req.user || !roles.includes(req.user.role)) {
      return res.status(403).json({
        success: false,
        error: { code: 'FORBIDDEN', message: 'Insufficient permissions' },
      });
    }
    next();
  };
}
```

### API Key Authentication

```typescript
import crypto from 'crypto';

// Generate API key
function generateApiKey(): { key: string; hash: string } {
  const key = crypto.randomBytes(32).toString('hex');
  const hash = crypto.createHash('sha256').update(key).digest('hex');
  return { key, hash };
}

// Verify API key middleware
async function verifyApiKey(req: Request, res: Response, next: NextFunction) {
  const apiKey = req.headers['x-api-key'] as string;

  if (!apiKey) {
    return res.status(401).json({
      success: false,
      error: { code: 'MISSING_API_KEY', message: 'API key required' },
    });
  }

  const hash = crypto.createHash('sha256').update(apiKey).digest('hex');
  const client = await ApiKeyService.findByHash(hash);

  if (!client || !client.active) {
    return res.status(401).json({
      success: false,
      error: { code: 'INVALID_API_KEY', message: 'Invalid API key' },
    });
  }

  req.client = client;
  next();
}
```

## Rate Limiting

```typescript
import rateLimit from 'express-rate-limit';
import RedisStore from 'rate-limit-redis';
import { redis } from '../config/redis';

// Global rate limit
const globalLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 1000, // requests per window
  standardHeaders: true,
  legacyHeaders: false,
  message: {
    success: false,
    error: {
      code: 'RATE_LIMIT_EXCEEDED',
      message: 'Too many requests, please try again later',
    },
  },
});

// Strict limit for sensitive endpoints
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5, // 5 attempts per 15 minutes
  skipSuccessfulRequests: true,
  store: new RedisStore({
    client: redis,
    prefix: 'rl:auth:',
  }),
  message: {
    success: false,
    error: {
      code: 'TOO_MANY_ATTEMPTS',
      message: 'Too many failed attempts, please try again later',
    },
  },
});

// Apply
app.use('/api', globalLimiter);
app.use('/api/auth/login', authLimiter);
app.use('/api/auth/register', authLimiter);
```

## Error Handling

### Custom Error Class

```typescript
export class ApiError extends Error {
  constructor(
    public statusCode: number,
    message: string,
    public code?: string,
    public details?: unknown
  ) {
    super(message);
    this.name = 'ApiError';
    Error.captureStackTrace(this, this.constructor);
  }

  static badRequest(message: string, details?: unknown) {
    return new ApiError(400, message, 'BAD_REQUEST', details);
  }

  static unauthorized(message = 'Unauthorized') {
    return new ApiError(401, message, 'UNAUTHORIZED');
  }

  static forbidden(message = 'Forbidden') {
    return new ApiError(403, message, 'FORBIDDEN');
  }

  static notFound(resource = 'Resource') {
    return new ApiError(404, `${resource} not found`, 'NOT_FOUND');
  }

  static conflict(message: string) {
    return new ApiError(409, message, 'CONFLICT');
  }

  static internal(message = 'Internal server error') {
    return new ApiError(500, message, 'INTERNAL_ERROR');
  }
}
```

### Error Handler Middleware

```typescript
import { Request, Response, NextFunction } from 'express';
import { Prisma } from '@prisma/client';
import { ZodError } from 'zod';
import { logger } from '../utils/logger';

function errorHandler(
  error: Error,
  req: Request,
  res: Response,
  next: NextFunction
) {
  // Log error
  logger.error({
    error: error.message,
    stack: error.stack,
    path: req.path,
    method: req.method,
    ip: req.ip,
    userId: req.user?.id,
  });

  // API Error (intentional)
  if (error instanceof ApiError) {
    return res.status(error.statusCode).json({
      success: false,
      error: {
        code: error.code,
        message: error.message,
        details: error.details,
      },
    });
  }

  // Zod validation error
  if (error instanceof ZodError) {
    return res.status(400).json({
      success: false,
      error: {
        code: 'VALIDATION_ERROR',
        message: 'Validation failed',
        details: error.errors,
      },
    });
  }

  // Prisma errors
  if (error instanceof Prisma.PrismaClientKnownRequestError) {
    if (error.code === 'P2002') {
      return res.status(409).json({
        success: false,
        error: {
          code: 'DUPLICATE_ENTRY',
          message: 'Resource already exists',
        },
      });
    }
    if (error.code === 'P2025') {
      return res.status(404).json({
        success: false,
        error: {
          code: 'NOT_FOUND',
          message: 'Resource not found',
        },
      });
    }
  }

  // Unknown error (don't leak details)
  return res.status(500).json({
    success: false,
    error: {
      code: 'INTERNAL_ERROR',
      message: process.env.NODE_ENV === 'production'
        ? 'An unexpected error occurred'
        : error.message,
    },
  });
}

// Async handler wrapper
function asyncHandler(fn: Function) {
  return (req: Request, res: Response, next: NextFunction) => {
    Promise.resolve(fn(req, res, next)).catch(next);
  };
}
```

## Response Format

### Consistent Response Structure

```typescript
// Success response
interface SuccessResponse<T> {
  success: true;
  data: T;
  meta?: {
    page?: number;
    limit?: number;
    total?: number;
    totalPages?: number;
  };
}

// Error response
interface ErrorResponse {
  success: false;
  error: {
    code: string;
    message: string;
    details?: unknown;
  };
}

// Response helpers
function sendSuccess<T>(res: Response, data: T, status = 200) {
  return res.status(status).json({
    success: true,
    data,
  });
}

function sendPaginated<T>(
  res: Response,
  data: T[],
  meta: { page: number; limit: number; total: number }
) {
  return res.json({
    success: true,
    data,
    meta: {
      ...meta,
      totalPages: Math.ceil(meta.total / meta.limit),
    },
  });
}

function sendError(res: Response, error: ApiError) {
  return res.status(error.statusCode).json({
    success: false,
    error: {
      code: error.code,
      message: error.message,
      details: error.details,
    },
  });
}
```

### HTTP Status Codes

| Code | Usage |
|------|-------|
| 200 | Success (GET, PUT, PATCH) |
| 201 | Created (POST) |
| 204 | No Content (DELETE) |
| 400 | Bad Request (validation failed) |
| 401 | Unauthorized (not authenticated) |
| 403 | Forbidden (not authorized) |
| 404 | Not Found |
| 409 | Conflict (duplicate) |
| 422 | Unprocessable Entity |
| 429 | Too Many Requests |
| 500 | Internal Server Error |

## Pagination

```typescript
interface PaginationParams {
  page: number;
  limit: number;
  sortBy?: string;
  order?: 'asc' | 'desc';
}

async function paginate<T>(
  model: any,
  params: PaginationParams,
  where?: object
): Promise<{ data: T[]; meta: PaginationMeta }> {
  const { page, limit, sortBy = 'createdAt', order = 'desc' } = params;

  const [data, total] = await Promise.all([
    model.findMany({
      where,
      skip: (page - 1) * limit,
      take: limit,
      orderBy: { [sortBy]: order },
    }),
    model.count({ where }),
  ]);

  return {
    data,
    meta: {
      page,
      limit,
      total,
      totalPages: Math.ceil(total / limit),
      hasNext: page * limit < total,
      hasPrev: page > 1,
    },
  };
}

// Usage
router.get('/posts', asyncHandler(async (req, res) => {
  const { page, limit, search } = req.query;

  const result = await paginate<Post>(prisma.post, {
    page: Number(page) || 1,
    limit: Number(limit) || 20,
  }, {
    ...(search && { title: { contains: search, mode: 'insensitive' } }),
  });

  res.json({ success: true, ...result });
}));
```

## Security Best Practices

### Security Headers

```typescript
import helmet from 'helmet';

app.use(helmet());
app.use(helmet.contentSecurityPolicy({
  directives: {
    defaultSrc: ["'self'"],
    scriptSrc: ["'self'"],
    styleSrc: ["'self'", "'unsafe-inline'"],
    imgSrc: ["'self'", 'data:', 'https:'],
  },
}));

// CORS configuration
import cors from 'cors';

app.use(cors({
  origin: process.env.ALLOWED_ORIGINS?.split(',') || ['http://localhost:3000'],
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization', 'X-API-Key'],
}));
```

### SQL Injection Prevention

```typescript
// BAD: String interpolation
const user = await prisma.$queryRaw`
  SELECT * FROM users WHERE email = '${email}'
`;

// GOOD: Parameterized query
const user = await prisma.$queryRaw`
  SELECT * FROM users WHERE email = ${email}
`;

// BETTER: Use ORM
const user = await prisma.user.findUnique({
  where: { email },
});
```

### File Upload Security

```typescript
import multer from 'multer';
import path from 'path';

const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/webp'];
const MAX_SIZE = 5 * 1024 * 1024; // 5MB

const upload = multer({
  storage: multer.memoryStorage(),
  limits: {
    fileSize: MAX_SIZE,
    files: 5,
  },
  fileFilter: (req, file, cb) => {
    if (!ALLOWED_TYPES.includes(file.mimetype)) {
      return cb(new Error('Invalid file type'));
    }

    // Check actual file extension
    const ext = path.extname(file.originalname).toLowerCase();
    if (!['.jpg', '.jpeg', '.png', '.webp'].includes(ext)) {
      return cb(new Error('Invalid file extension'));
    }

    cb(null, true);
  },
});

router.post('/upload', authenticate, upload.single('image'), asyncHandler(async (req, res) => {
  if (!req.file) {
    throw ApiError.badRequest('No file uploaded');
  }

  // Scan for malware (in production)
  // await scanFile(req.file.buffer);

  const url = await StorageService.upload(req.file);

  res.status(201).json({
    success: true,
    data: { url },
  });
}));
```

## Logging

```typescript
import winston from 'winston';

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  transports: [
    new winston.transports.File({ filename: 'logs/error.log', level: 'error' }),
    new winston.transports.File({ filename: 'logs/combined.log' }),
  ],
});

if (process.env.NODE_ENV !== 'production') {
  logger.add(new winston.transports.Console({
    format: winston.format.simple(),
  }));
}

// Request logging middleware
function requestLogger(req: Request, res: Response, next: NextFunction) {
  const start = Date.now();

  res.on('finish', () => {
    logger.info({
      method: req.method,
      path: req.path,
      status: res.statusCode,
      duration: Date.now() - start,
      ip: req.ip,
      userId: req.user?.id,
    });
  });

  next();
}
```

## Testing

```typescript
import request from 'supertest';
import { app } from '../app';
import { prisma } from '../config/database';

describe('POST /api/users', () => {
  let authToken: string;

  beforeAll(async () => {
    // Setup admin user and get token
    authToken = await getAdminToken();
  });

  afterEach(async () => {
    await prisma.user.deleteMany();
  });

  it('creates user with valid data', async () => {
    const response = await request(app)
      .post('/api/users')
      .set('Authorization', `Bearer ${authToken}`)
      .send({
        name: 'John Doe',
        email: 'john@example.com',
        role: 'user',
      });

    expect(response.status).toBe(201);
    expect(response.body.success).toBe(true);
    expect(response.body.data.email).toBe('john@example.com');
  });

  it('returns 400 for invalid email', async () => {
    const response = await request(app)
      .post('/api/users')
      .set('Authorization', `Bearer ${authToken}`)
      .send({
        name: 'John Doe',
        email: 'invalid-email',
      });

    expect(response.status).toBe(400);
    expect(response.body.success).toBe(false);
    expect(response.body.error.code).toBe('VALIDATION_ERROR');
  });

  it('returns 401 without auth token', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ name: 'John', email: 'john@example.com' });

    expect(response.status).toBe(401);
  });

  it('returns 403 for non-admin users', async () => {
    const userToken = await getUserToken(); // Regular user

    const response = await request(app)
      .post('/api/users')
      .set('Authorization', `Bearer ${userToken}`)
      .send({ name: 'John', email: 'john@example.com' });

    expect(response.status).toBe(403);
  });
});
```

## API Checklist

- [ ] Input validation on all endpoints
- [ ] Output sanitization
- [ ] Authentication required where needed
- [ ] Authorization checks for resources
- [ ] Rate limiting configured
- [ ] Consistent error responses
- [ ] Proper HTTP status codes
- [ ] Request/response logging
- [ ] Security headers enabled
- [ ] CORS properly configured
- [ ] SQL injection prevented
- [ ] File upload validation
- [ ] Pagination for lists
- [ ] API versioning strategy
- [ ] Documentation (OpenAPI/Swagger)
