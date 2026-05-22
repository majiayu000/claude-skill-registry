---
name: express
description: Builds APIs with Express including routing, middleware, error handling, and security. Use when creating Node.js APIs, building REST services, or adding middleware-based server functionality.
---

# Express

Fast, unopinionated, minimalist web framework for Node.js.

## Quick Start

**Install:**
```bash
npm install express
npm install -D @types/express typescript
```

**Create server:**
```typescript
// src/index.ts
import express from 'express';

const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());

app.get('/', (req, res) => {
  res.json({ message: 'Hello World!' });
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
```

## Project Structure

```
src/
  index.ts           # App entry
  routes/            # Route handlers
    users.ts
    posts.ts
  middleware/        # Custom middleware
    auth.ts
    validation.ts
  controllers/       # Business logic
    userController.ts
  services/          # Data access
    userService.ts
  types/             # TypeScript types
    index.ts
```

## Routing

### Basic Routes

```typescript
import express from 'express';

const app = express();

// HTTP methods
app.get('/users', (req, res) => res.json({ users: [] }));
app.post('/users', (req, res) => res.status(201).json(req.body));
app.put('/users/:id', (req, res) => res.json({ id: req.params.id }));
app.patch('/users/:id', (req, res) => res.json({ patched: true }));
app.delete('/users/:id', (req, res) => res.status(204).send());

// All methods
app.all('/api/*', (req, res, next) => {
  console.log('API request');
  next();
});
```

### Route Parameters

```typescript
// Path parameters
app.get('/users/:id', (req, res) => {
  const { id } = req.params;
  res.json({ userId: id });
});

// Multiple params
app.get('/posts/:postId/comments/:commentId', (req, res) => {
  const { postId, commentId } = req.params;
  res.json({ postId, commentId });
});

// Optional params
app.get('/users/:id?', (req, res) => {
  if (req.params.id) {
    res.json({ userId: req.params.id });
  } else {
    res.json({ message: 'All users' });
  }
});

// Regex params
app.get('/user/:id(\\d+)', (req, res) => {
  // Only matches numeric IDs
  res.json({ id: req.params.id });
});
```

### Query Parameters

```typescript
app.get('/search', (req, res) => {
  const { q, page = '1', limit = '10' } = req.query;

  res.json({
    query: q,
    page: Number(page),
    limit: Number(limit),
  });
});
```

### Router Modules

```typescript
// routes/users.ts
import { Router } from 'express';

const router = Router();

router.get('/', (req, res) => {
  res.json({ users: [] });
});

router.get('/:id', (req, res) => {
  res.json({ id: req.params.id });
});

router.post('/', (req, res) => {
  res.status(201).json(req.body);
});

export default router;

// index.ts
import userRoutes from './routes/users';

app.use('/api/users', userRoutes);
```

## Middleware

### Built-in Middleware

```typescript
import express from 'express';

const app = express();

// Parse JSON bodies
app.use(express.json());

// Parse URL-encoded bodies
app.use(express.urlencoded({ extended: true }));

// Serve static files
app.use(express.static('public'));
```

### Third-party Middleware

```typescript
import cors from 'cors';
import helmet from 'helmet';
import morgan from 'morgan';
import compression from 'compression';

app.use(cors());                    // CORS
app.use(helmet());                  // Security headers
app.use(morgan('dev'));             // Logging
app.use(compression());             // Gzip compression
```

### Custom Middleware

```typescript
import { Request, Response, NextFunction } from 'express';

// Logging middleware
const logger = (req: Request, res: Response, next: NextFunction) => {
  console.log(`${req.method} ${req.path}`);
  next();
};

// Timing middleware
const timing = (req: Request, res: Response, next: NextFunction) => {
  const start = Date.now();
  res.on('finish', () => {
    console.log(`${req.method} ${req.path} - ${Date.now() - start}ms`);
  });
  next();
};

app.use(logger);
app.use(timing);
```

### Route-specific Middleware

```typescript
const requireAuth = (req: Request, res: Response, next: NextFunction) => {
  const token = req.headers.authorization?.split(' ')[1];

  if (!token) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  try {
    const decoded = verifyToken(token);
    req.user = decoded;
    next();
  } catch {
    return res.status(403).json({ error: 'Invalid token' });
  }
};

// Apply to specific routes
app.get('/profile', requireAuth, (req, res) => {
  res.json({ user: req.user });
});

// Apply to router
router.use(requireAuth);
```

## Request & Response

### Request Object

```typescript
app.post('/api/data', (req, res) => {
  // Body (requires express.json())
  const { name, email } = req.body;

  // Query params
  const { page } = req.query;

  // Route params
  const { id } = req.params;

  // Headers
  const authHeader = req.get('Authorization');
  const contentType = req.get('Content-Type');

  // Cookies (requires cookie-parser)
  const sessionId = req.cookies.sessionId;

  // IP address
  const ip = req.ip;

  // HTTP method
  const method = req.method;

  // Original URL
  const url = req.originalUrl;

  res.json({ received: true });
});
```

### Response Methods

```typescript
app.get('/api/examples', (req, res) => {
  // JSON response
  res.json({ message: 'Hello' });

  // With status code
  res.status(201).json({ created: true });

  // Text response
  res.send('Hello World');

  // HTML response
  res.send('<h1>Hello</h1>');

  // Redirect
  res.redirect('/new-path');
  res.redirect(301, '/permanent-redirect');

  // Download file
  res.download('/path/to/file.pdf');

  // Send file
  res.sendFile('/path/to/file.html');

  // Set headers
  res.set('X-Custom-Header', 'value');
  res.set({
    'Content-Type': 'application/json',
    'X-Custom': 'value',
  });

  // Set cookie
  res.cookie('name', 'value', { httpOnly: true, secure: true });

  // Clear cookie
  res.clearCookie('name');

  // Status only
  res.sendStatus(204); // No Content
});
```

## Error Handling

### Error Handler Middleware

```typescript
import { Request, Response, NextFunction } from 'express';

interface AppError extends Error {
  statusCode?: number;
  status?: string;
}

// Custom error class
class HttpError extends Error {
  statusCode: number;

  constructor(message: string, statusCode: number) {
    super(message);
    this.statusCode = statusCode;
  }
}

// Error handler middleware (must have 4 params)
const errorHandler = (
  err: AppError,
  req: Request,
  res: Response,
  next: NextFunction
) => {
  console.error(err.stack);

  const statusCode = err.statusCode || 500;
  const message = err.message || 'Internal Server Error';

  res.status(statusCode).json({
    error: {
      message,
      status: statusCode,
      ...(process.env.NODE_ENV === 'development' && { stack: err.stack }),
    },
  });
};

// Register after all routes
app.use(errorHandler);
```

### Async Error Handling

```typescript
// Wrapper for async handlers
const asyncHandler = (fn: Function) => {
  return (req: Request, res: Response, next: NextFunction) => {
    Promise.resolve(fn(req, res, next)).catch(next);
  };
};

// Usage
app.get('/users/:id', asyncHandler(async (req, res) => {
  const user = await findUser(req.params.id);

  if (!user) {
    throw new HttpError('User not found', 404);
  }

  res.json(user);
}));
```

### 404 Handler

```typescript
// Place after all routes
app.use((req, res) => {
  res.status(404).json({ error: 'Not Found' });
});
```

## Validation

### With Zod

```typescript
import { z } from 'zod';

const createUserSchema = z.object({
  body: z.object({
    name: z.string().min(1),
    email: z.string().email(),
    age: z.number().min(0).optional(),
  }),
});

const validate = (schema: z.ZodSchema) => {
  return (req: Request, res: Response, next: NextFunction) => {
    try {
      schema.parse({ body: req.body, query: req.query, params: req.params });
      next();
    } catch (error) {
      if (error instanceof z.ZodError) {
        return res.status(400).json({ errors: error.errors });
      }
      next(error);
    }
  };
};

app.post('/users', validate(createUserSchema), (req, res) => {
  // req.body is validated
  res.status(201).json(req.body);
});
```

## Authentication

### JWT Authentication

```typescript
import jwt from 'jsonwebtoken';

const JWT_SECRET = process.env.JWT_SECRET!;

// Login
app.post('/login', async (req, res) => {
  const { email, password } = req.body;

  const user = await authenticateUser(email, password);

  if (!user) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }

  const token = jwt.sign({ userId: user.id }, JWT_SECRET, { expiresIn: '7d' });

  res.json({ token });
});

// Auth middleware
const authenticate = (req: Request, res: Response, next: NextFunction) => {
  const token = req.headers.authorization?.replace('Bearer ', '');

  if (!token) {
    return res.status(401).json({ error: 'No token provided' });
  }

  try {
    const decoded = jwt.verify(token, JWT_SECRET) as { userId: string };
    req.userId = decoded.userId;
    next();
  } catch {
    res.status(401).json({ error: 'Invalid token' });
  }
};

// Protected route
app.get('/profile', authenticate, (req, res) => {
  res.json({ userId: req.userId });
});
```

## File Uploads

```typescript
import multer from 'multer';
import path from 'path';

const storage = multer.diskStorage({
  destination: 'uploads/',
  filename: (req, file, cb) => {
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1e9);
    cb(null, uniqueSuffix + path.extname(file.originalname));
  },
});

const upload = multer({
  storage,
  limits: { fileSize: 5 * 1024 * 1024 }, // 5MB
  fileFilter: (req, file, cb) => {
    const allowed = ['image/jpeg', 'image/png', 'image/gif'];
    cb(null, allowed.includes(file.mimetype));
  },
});

// Single file
app.post('/upload', upload.single('file'), (req, res) => {
  res.json({ file: req.file });
});

// Multiple files
app.post('/uploads', upload.array('files', 5), (req, res) => {
  res.json({ files: req.files });
});
```

## Testing

```typescript
import request from 'supertest';
import { describe, it, expect } from 'vitest';
import app from './app';

describe('Users API', () => {
  it('GET /users returns users', async () => {
    const response = await request(app)
      .get('/api/users')
      .expect('Content-Type', /json/)
      .expect(200);

    expect(response.body).toHaveProperty('users');
  });

  it('POST /users creates user', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ name: 'John', email: 'john@example.com' })
      .expect(201);

    expect(response.body.name).toBe('John');
  });
});
```

## Best Practices

1. **Use async/await with wrapper** - Catch errors properly
2. **Validate all input** - Use Zod or Joi
3. **Use helmet** - Security headers
4. **Centralize error handling** - Error middleware
5. **Structure by feature** - Not by type

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Forgetting express.json() | Add app.use(express.json()) |
| Not handling async errors | Use asyncHandler wrapper |
| Error handler with 3 params | Must have 4 params for Express |
| Sending response twice | Return after sending |
| Not using CORS | Add cors() middleware |

## Reference Files

- [references/middleware.md](references/middleware.md) - Middleware patterns
- [references/security.md](references/security.md) - Security best practices
- [references/testing.md](references/testing.md) - Testing with supertest
