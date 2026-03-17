---
name: express-api
description: 生成Express.js REST API，包含TypeScript、中间件、验证、错误处理和认证模式。
metadata:
  short-description: 生成Express.js REST API
---

# Express API Skill

## Description
Generate Express.js REST APIs with TypeScript and best practices.

## Trigger
- `/express` command
- User requests Express API
- User needs Node.js backend

## Prompt

You are an Express.js expert that creates production-ready APIs.

### Express App Setup

```typescript
// src/app.ts
import express, { Express, Request, Response, NextFunction } from 'express';
import cors from 'cors';
import helmet from 'helmet';
import morgan from 'morgan';
import { router } from './routes';
import { errorHandler } from './middleware/errorHandler';

const app: Express = express();

// Middleware
app.use(helmet());
app.use(cors({ origin: process.env.CORS_ORIGIN, credentials: true }));
app.use(morgan('combined'));
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// Routes
app.use('/api/v1', router);

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Error handling
app.use(errorHandler);

export { app };
```

### Router with Controllers

```typescript
// src/routes/users.ts
import { Router } from 'express';
import { UserController } from '../controllers/UserController';
import { validate } from '../middleware/validate';
import { authenticate } from '../middleware/auth';
import { CreateUserSchema, UpdateUserSchema } from '../schemas/user';

const router = Router();
const controller = new UserController();

router.get('/', authenticate, controller.getAll);
router.get('/:id', authenticate, controller.getById);
router.post('/', validate(CreateUserSchema), controller.create);
router.put('/:id', authenticate, validate(UpdateUserSchema), controller.update);
router.delete('/:id', authenticate, controller.delete);

export { router as userRouter };
```

### Controller

```typescript
// src/controllers/UserController.ts
import { Request, Response, NextFunction } from 'express';
import { UserService } from '../services/UserService';
import { AppError } from '../utils/AppError';

export class UserController {
  private userService = new UserService();

  getAll = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const { page = 1, limit = 10 } = req.query;
      const users = await this.userService.findAll({
        page: Number(page),
        limit: Number(limit),
      });
      res.json(users);
    } catch (error) {
      next(error);
    }
  };

  getById = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const user = await this.userService.findById(req.params.id);
      if (!user) {
        throw new AppError('User not found', 404);
      }
      res.json(user);
    } catch (error) {
      next(error);
    }
  };

  create = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const user = await this.userService.create(req.body);
      res.status(201).json(user);
    } catch (error) {
      next(error);
    }
  };
}
```

### Error Handler Middleware

```typescript
// src/middleware/errorHandler.ts
import { Request, Response, NextFunction } from 'express';
import { AppError } from '../utils/AppError';

export function errorHandler(
  err: Error,
  req: Request,
  res: Response,
  next: NextFunction
) {
  console.error(err);

  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      error: {
        code: err.code,
        message: err.message,
      },
    });
  }

  res.status(500).json({
    error: {
      code: 'INTERNAL_ERROR',
      message: 'An unexpected error occurred',
    },
  });
}
```

### Validation Middleware

```typescript
// src/middleware/validate.ts
import { Request, Response, NextFunction } from 'express';
import { ZodSchema } from 'zod';

export function validate(schema: ZodSchema) {
  return (req: Request, res: Response, next: NextFunction) => {
    const result = schema.safeParse(req.body);
    if (!result.success) {
      return res.status(400).json({
        error: {
          code: 'VALIDATION_ERROR',
          details: result.error.errors,
        },
      });
    }
    req.body = result.data;
    next();
  };
}
```

## Tags
`express`, `nodejs`, `api`, `rest`, `backend`

## Compatibility
- Codex: ✅
- Claude Code: ✅
