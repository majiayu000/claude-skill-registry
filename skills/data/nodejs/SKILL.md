---
name: nodejs
description: Core Node.js backend patterns for TypeScript applications including async/await error handling, middleware concepts, configuration management, testing strategies, and layered architecture principles. Use when building Node.js backend services, APIs, or microservices.
---

# Node.js Backend Patterns

## Purpose

Core patterns for building scalable Node.js backend applications with TypeScript, emphasizing clean architecture, error handling, and testability.

## When to Use This Skill

- Building Node.js backend services
- Implementing async/await patterns
- Error handling and logging
- Configuration management
- Testing backend code
- Layered architecture (routes → controllers → services → repositories)

---

## Quick Start

### Layered Architecture

```
src/
├── api/
│   ├── routes/         # HTTP route definitions
│   ├── controllers/    # Request/response handling
│   ├── services/       # Business logic
│   └── repositories/   # Data access
├── middleware/         # Express middleware
├── types/             # TypeScript types
├── config/            # Configuration
└── utils/             # Utilities
```

**Flow:** Route → Controller → Service → Repository → Database

---

## Async/Await Error Handling

### Basic Pattern

```typescript
async function fetchUser(id: string): Promise<User> {
  try {
    const user = await db.user.findUnique({ where: { id } });
    if (!user) {
      throw new Error('User not found');
    }
    return user;
  } catch (error) {
    console.error('Error fetching user:', error);
    throw error;
  }
}
```

### Async Controller Pattern

```typescript
class UserController {
  async getUser(req: Request, res: Response): Promise<void> {
    try {
      const { id } = req.params;
      const user = await this.userService.getById(id);

      res.json({
        success: true,
        data: user,
      });
    } catch (error) {
      console.error('Error in getUser:', error);
      res.status(500).json({
        success: false,
        error: 'Failed to fetch user',
      });
    }
  }
}
```

### Promise.all for Parallel Operations

```typescript
async function getUserDashboard(userId: string) {
  try {
    const [user, posts, followers] = await Promise.all([
      userService.getById(userId),
      postService.getByUser(userId),
      followerService.getByUser(userId),
    ]);

    return { user, posts, followers };
  } catch (error) {
    console.error('Error loading dashboard:', error);
    throw error;
  }
}
```

---

## TypeScript Patterns

### Request/Response Types

```typescript
// Request body
interface CreateUserRequest {
  email: string;
  name: string;
  password: string;
}

// Response
interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

// Usage
async function createUser(
  req: Request<{}, {}, CreateUserRequest>,
  res: Response<ApiResponse<User>>
): Promise<void> {
  const { email, name, password } = req.body;

  const user = await userService.create({ email, name, password });

  res.json({
    success: true,
    data: user,
  });
}
```

### Service Layer Types

```typescript
interface IUserService {
  getById(id: string): Promise<User>;
  create(data: CreateUserDto): Promise<User>;
  update(id: string, data: UpdateUserDto): Promise<User>;
  delete(id: string): Promise<void>;
}

class UserService implements IUserService {
  async getById(id: string): Promise<User> {
    // Implementation
  }

  async create(data: CreateUserDto): Promise<User> {
    // Implementation
  }

  async update(id: string, data: UpdateUserDto): Promise<User> {
    // Implementation
  }

  async delete(id: string): Promise<void> {
    // Implementation
  }
}
```

---

## Configuration Management

### Environment Variables

```typescript
// config/env.ts
import { z } from 'zod';

const envSchema = z.object({
  NODE_ENV: z.enum(['development', 'production', 'test']),
  PORT: z.string().transform(Number),
  DATABASE_URL: z.string().url(),
  JWT_SECRET: z.string().min(32),
  LOG_LEVEL: z.enum(['error', 'warn', 'info', 'debug']).default('info'),
});

export const env = envSchema.parse(process.env);
```

### Unified Config

```typescript
// config/index.ts
interface Config {
  server: {
    port: number;
    host: string;
  };
  database: {
    url: string;
  };
  auth: {
    jwtSecret: string;
    jwtExpiry: string;
  };
}

export const config: Config = {
  server: {
    port: parseInt(process.env.PORT || '3000'),
    host: process.env.HOST || 'localhost',
  },
  database: {
    url: process.env.DATABASE_URL || '',
  },
  auth: {
    jwtSecret: process.env.JWT_SECRET || '',
    jwtExpiry: process.env.JWT_EXPIRY || '7d',
  },
};
```

---

## Layered Architecture

### Controller Layer

```typescript
// controllers/UserController.ts
export class UserController {
  constructor(private userService: UserService) {}

  async getById(req: Request, res: Response): Promise<void> {
    const { id } = req.params;
    const user = await this.userService.getById(id);

    res.json({
      success: true,
      data: user,
    });
  }

  async create(req: Request, res: Response): Promise<void> {
    const userData = req.body;
    const user = await this.userService.create(userData);

    res.status(201).json({
      success: true,
      data: user,
    });
  }
}
```

### Service Layer

```typescript
// services/UserService.ts
export class UserService {
  constructor(private userRepository: UserRepository) {}

  async getById(id: string): Promise<User> {
    const user = await this.userRepository.findById(id);
    if (!user) {
      throw new Error('User not found');
    }
    return user;
  }

  async create(data: CreateUserDto): Promise<User> {
    // Business logic
    const hashedPassword = await this.hashPassword(data.password);

    return this.userRepository.create({
      ...data,
      password: hashedPassword,
    });
  }

  private async hashPassword(password: string): Promise<string> {
    // Hash implementation
    return password; // Placeholder
  }
}
```

### Repository Layer

```typescript
// repositories/UserRepository.ts
export class UserRepository {
  async findById(id: string): Promise<User | null> {
    // Database query
    return db.user.findUnique({ where: { id } });
  }

  async create(data: CreateUserData): Promise<User> {
    return db.user.create({ data });
  }

  async update(id: string, data: UpdateUserData): Promise<User> {
    return db.user.update({
      where: { id },
      data,
    });
  }

  async delete(id: string): Promise<void> {
    await db.user.delete({ where: { id } });
  }
}
```

---

## Dependency Injection

### Basic DI Pattern

```typescript
// Composition root
const userRepository = new UserRepository();
const userService = new UserService(userRepository);
const userController = new UserController(userService);

export { userController };
```

### Service Container

```typescript
// container.ts
class Container {
  private services: Map<string, any> = new Map();

  register<T>(name: string, factory: () => T): void {
    this.services.set(name, factory());
  }

  get<T>(name: string): T {
    const service = this.services.get(name);
    if (!service) {
      throw new Error(`Service ${name} not found`);
    }
    return service;
  }
}

export const container = new Container();

// Register services
container.register('userRepository', () => new UserRepository());
container.register('userService', () => new UserService(
  container.get('userRepository')
));
container.register('userController', () => new UserController(
  container.get('userService')
));
```

---

## Error Handling

### Custom Error Classes

```typescript
export class AppError extends Error {
  constructor(
    public message: string,
    public statusCode: number = 500,
    public isOperational: boolean = true
  ) {
    super(message);
    Object.setPrototypeOf(this, AppError.prototype);
  }
}

export class NotFoundError extends AppError {
  constructor(resource: string) {
    super(`${resource} not found`, 404);
  }
}

export class ValidationError extends AppError {
  constructor(message: string) {
    super(message, 400);
  }
}

// Usage
async function getUser(id: string): Promise<User> {
  const user = await userRepository.findById(id);
  if (!user) {
    throw new NotFoundError('User');
  }
  return user;
}
```

### Async Error Wrapper

```typescript
type AsyncHandler = (
  req: Request,
  res: Response,
  next: NextFunction
) => Promise<void>;

export const asyncHandler = (fn: AsyncHandler) => {
  return (req: Request, res: Response, next: NextFunction) => {
    Promise.resolve(fn(req, res, next)).catch(next);
  };
};

// Usage
router.get('/users/:id', asyncHandler(async (req, res) => {
  const user = await userService.getById(req.params.id);
  res.json({ data: user });
}));
```

---

---

## Best Practices

### 1. Always Use Async/Await

```typescript
// ✅ Good: async/await
async function getUser(id: string): Promise<User> {
  const user = await userRepository.findById(id);
  return user;
}

// ❌ Avoid: Promise chains
function getUser(id: string): Promise<User> {
  return userRepository.findById(id)
    .then(user => user)
    .catch(error => throw error);
}
```

### 2. Layer Separation

```typescript
// ✅ Good: Separated layers
// Controller handles HTTP
// Service handles business logic
// Repository handles data access

// ❌ Avoid: Business logic in controllers
class UserController {
  async create(req: Request, res: Response) {
    // ❌ Don't put business logic here
    const hashedPassword = await hash(req.body.password);
    const user = await db.user.create({...});
    res.json(user);
  }
}
```

### 3. Type Everything

```typescript
// ✅ Good: Full type coverage
async function updateUser(
  id: string,
  data: UpdateUserDto
): Promise<User> {
  return userService.update(id, data);
}

// ❌ Avoid: any types
async function updateUser(id: any, data: any): Promise<any> {
  return userService.update(id, data);
}
```

---

## Additional Resources

For more patterns, see:
- [async-and-errors.md](resources/async-and-errors.md) - Advanced error handling
- [testing-guide.md](resources/testing-guide.md) - Comprehensive testing
- [architecture-patterns.md](resources/architecture-patterns.md) - Architecture details
