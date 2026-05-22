---
name: faion-javascript-skill
user-invocable: false
description: ""
---

# JavaScript/TypeScript Coding Standards

**Universal guidelines for modern JS/TS development (2025-2026)**

---

## Quick Reference

**Supported Runtimes:**
- Node.js: 20 LTS, 22 LTS (prefer 22+)
- Bun: 1.x (for modern projects)
- Deno: 2.x (alternative runtime)
- Browser: ES2022+ with bundler

**Recommended Stack:**
- TypeScript 5.x with strict mode
- React 19.x / Next.js 15.x for frontend
- Express 5.x / Fastify 5.x for backend
- Vitest / Jest for testing
- ESLint 9.x (flat config) + Prettier

---

## Core Principles

### 1. TypeScript First

```typescript
// ALWAYS use TypeScript with strict mode
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitReturns": true,
    "exactOptionalPropertyTypes": true,
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler"
  }
}
```

### 2. Prefer `const` and Arrow Functions

```typescript
// Prefer const for immutability
const users = ['Alice', 'Bob'];

// Arrow functions for callbacks and short functions
const double = (n: number) => n * 2;
const getUser = async (id: string) => {
  return await db.users.findById(id);
};

// Regular functions for hoisting or `this` binding
function handleRequest(req: Request, res: Response) {
  // ...
}
```

### 3. Named Exports Over Default

```typescript
// Prefer named exports - easier to refactor and search
export function createUser(data: UserData): User { ... }
export const USER_ROLES = ['admin', 'user'] as const;
export type UserRole = typeof USER_ROLES[number];

// Default only for framework requirements (Next.js pages, etc.)
export default function Page() { ... }
```

### 4. Explicit Types for Public APIs

```typescript
// Function parameters and returns - always typed
function processOrder(
  order: Order,
  options?: ProcessOptions,
): Promise<ProcessResult> {
  // ...
}

// Internal variables - infer when obvious
const count = 0;  // inferred as number
const items = []; // use explicit type: Item[] = []
```

---

## Project Setup

### Package Manager Choice

| Manager | When to Use |
|---------|-------------|
| **pnpm** | Default choice - fast, disk-efficient, strict |
| **bun** | Bun runtime projects, maximum speed |
| **npm** | Legacy projects, maximum compatibility |
| **yarn** | Existing Yarn 4.x workspaces |

### pnpm Configuration

```yaml
# .npmrc
strict-peer-dependencies=true
auto-install-peers=true
shamefully-hoist=false

# pnpm-workspace.yaml (monorepo)
packages:
  - 'apps/*'
  - 'packages/*'
```

### ESLint 9.x Flat Config

```javascript
// eslint.config.js
import eslint from '@eslint/js';
import tseslint from 'typescript-eslint';
import react from 'eslint-plugin-react';
import reactHooks from 'eslint-plugin-react-hooks';

export default tseslint.config(
  eslint.configs.recommended,
  ...tseslint.configs.strictTypeChecked,
  {
    plugins: {
      react,
      'react-hooks': reactHooks,
    },
    rules: {
      'react-hooks/rules-of-hooks': 'error',
      'react-hooks/exhaustive-deps': 'warn',
      '@typescript-eslint/no-unused-vars': ['error', {
        argsIgnorePattern: '^_'
      }],
      '@typescript-eslint/explicit-function-return-type': ['error', {
        allowExpressions: true,
      }],
    },
  },
);
```

### Prettier Configuration

```json
// .prettierrc
{
  "semi": true,
  "singleQuote": true,
  "trailingComma": "all",
  "printWidth": 80,
  "tabWidth": 2,
  "useTabs": false,
  "arrowParens": "always",
  "endOfLine": "lf"
}
```

### TypeScript Configuration

```json
// tsconfig.json
{
  "compilerOptions": {
    // Type Checking (strict mode)
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "exactOptionalPropertyTypes": true,

    // Modules
    "target": "ES2022",
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "verbatimModuleSyntax": true,

    // Emit
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "outDir": "./dist",

    // Paths (monorepo)
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"],
      "@components/*": ["./src/components/*"],
      "@utils/*": ["./src/utils/*"]
    },

    // Interop
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "forceConsistentCasingInFileNames": true,
    "skipLibCheck": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

---

## React Patterns

### Component Architecture

```
src/
├── components/           # Shared/reusable components
│   ├── ui/              # Base UI primitives (Button, Input)
│   │   ├── Button.tsx
│   │   ├── Button.test.tsx
│   │   └── index.ts
│   ├── forms/           # Form-related components
│   └── layout/          # Layout components (Header, Footer)
├── features/            # Feature-based modules
│   ├── auth/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── api.ts
│   │   └── types.ts
│   └── dashboard/
├── hooks/               # Shared custom hooks
├── utils/               # Pure utility functions
├── types/               # Shared TypeScript types
├── lib/                 # Third-party wrappers
└── app/                 # Next.js app directory / routes
```

### Functional Components

```tsx
// Always use function declarations for components
interface UserCardProps {
  user: User;
  onEdit?: (id: string) => void;
  className?: string;
}

export function UserCard({
  user,
  onEdit,
  className
}: UserCardProps): React.ReactElement {
  const handleEdit = () => {
    onEdit?.(user.id);
  };

  return (
    <div className={cn('card', className)}>
      <h3>{user.name}</h3>
      <p>{user.email}</p>
      {onEdit && (
        <button onClick={handleEdit}>Edit</button>
      )}
    </div>
  );
}
```

### Hooks Patterns

```tsx
// Custom hook with proper typing
interface UseUserResult {
  user: User | null;
  isLoading: boolean;
  error: Error | null;
  refetch: () => Promise<void>;
}

export function useUser(userId: string): UseUserResult {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const refetch = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await fetchUser(userId);
      setUser(data);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Unknown error'));
    } finally {
      setIsLoading(false);
    }
  }, [userId]);

  useEffect(() => {
    void refetch();
  }, [refetch]);

  return { user, isLoading, error, refetch };
}
```

### Context Pattern

```tsx
// types.ts
interface AuthContextValue {
  user: User | null;
  isAuthenticated: boolean;
  login: (credentials: Credentials) => Promise<void>;
  logout: () => void;
}

// context.tsx
const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);

  const login = useCallback(async (credentials: Credentials) => {
    const userData = await authService.login(credentials);
    setUser(userData);
  }, []);

  const logout = useCallback(() => {
    authService.logout();
    setUser(null);
  }, []);

  const value = useMemo(() => ({
    user,
    isAuthenticated: user !== null,
    login,
    logout,
  }), [user, login, logout]);

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

// Custom hook with runtime check
export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}
```

### State Management Decision Tree

```
What kind of state?
│
├─► Server state (API data)?
│   └─► TanStack Query / SWR
│
├─► Form state?
│   └─► React Hook Form
│
├─► Global UI state (theme, sidebar)?
│   └─► Zustand (simple) / Jotai (atomic)
│
├─► Component-local state?
│   └─► useState / useReducer
│
└─► Cross-component state (same feature)?
    └─► Context + useReducer
```

### Performance Patterns

```tsx
// Memoize expensive computations
const sortedItems = useMemo(() => {
  return items.slice().sort((a, b) => a.name.localeCompare(b.name));
}, [items]);

// Memoize callbacks passed to children
const handleItemClick = useCallback((id: string) => {
  setSelectedId(id);
}, []);

// Memoize components with stable props
const MemoizedList = memo(function List({
  items,
  onItemClick
}: ListProps) {
  return (
    <ul>
      {items.map((item) => (
        <li key={item.id} onClick={() => onItemClick(item.id)}>
          {item.name}
        </li>
      ))}
    </ul>
  );
});

// Avoid: inline objects in JSX
<Component style={{ color: 'red' }} />  // Creates new object each render

// Prefer: stable reference
const redStyle = { color: 'red' };
<Component style={redStyle} />
```

---

## Node.js Patterns

### Express Application Structure

```
src/
├── app.ts               # Express app setup
├── server.ts            # Server entry point
├── config/
│   └── env.ts           # Environment variables
├── routes/
│   ├── index.ts         # Route aggregator
│   ├── users.ts
│   └── products.ts
├── controllers/
│   ├── users.controller.ts
│   └── products.controller.ts
├── services/
│   ├── users.service.ts
│   └── products.service.ts
├── middleware/
│   ├── auth.ts
│   ├── errorHandler.ts
│   └── validate.ts
├── models/
│   └── user.model.ts
├── types/
│   └── express.d.ts     # Express type extensions
└── utils/
    ├── logger.ts
    └── errors.ts
```

### Express Setup

```typescript
// app.ts
import express, { type Express } from 'express';
import cors from 'cors';
import helmet from 'helmet';
import compression from 'compression';
import { errorHandler } from './middleware/errorHandler';
import { requestLogger } from './middleware/requestLogger';
import routes from './routes';

export function createApp(): Express {
  const app = express();

  // Security
  app.use(helmet());
  app.use(cors({ origin: process.env.CORS_ORIGIN }));

  // Parsing
  app.use(express.json({ limit: '10kb' }));
  app.use(express.urlencoded({ extended: true }));

  // Compression
  app.use(compression());

  // Logging
  app.use(requestLogger);

  // Routes
  app.use('/api/v1', routes);

  // Health check
  app.get('/health', (_req, res) => {
    res.json({ status: 'ok', timestamp: new Date().toISOString() });
  });

  // Error handling (MUST be last)
  app.use(errorHandler);

  return app;
}
```

### Middleware Pattern

```typescript
// middleware/auth.ts
import { type RequestHandler } from 'express';
import { verifyToken } from '../utils/jwt';
import { UnauthorizedError } from '../utils/errors';

export const authenticate: RequestHandler = async (req, _res, next) => {
  try {
    const authHeader = req.headers.authorization;

    if (!authHeader?.startsWith('Bearer ')) {
      throw new UnauthorizedError('Missing authorization header');
    }

    const token = authHeader.slice(7);
    const payload = await verifyToken(token);

    req.user = payload;
    next();
  } catch (error) {
    next(error);
  }
};

// Extend Express Request type
declare global {
  namespace Express {
    interface Request {
      user?: TokenPayload;
    }
  }
}
```

### Controller Pattern

```typescript
// controllers/users.controller.ts
import { type Request, type Response, type NextFunction } from 'express';
import * as usersService from '../services/users.service';
import { CreateUserSchema, UpdateUserSchema } from '../schemas/users';

export async function getUsers(
  req: Request,
  res: Response,
  next: NextFunction,
): Promise<void> {
  try {
    const users = await usersService.findAll();
    res.json({ data: users });
  } catch (error) {
    next(error);
  }
}

export async function createUser(
  req: Request,
  res: Response,
  next: NextFunction,
): Promise<void> {
  try {
    const data = CreateUserSchema.parse(req.body);
    const user = await usersService.create(data);
    res.status(201).json({ data: user });
  } catch (error) {
    next(error);
  }
}
```

### Error Handling

```typescript
// utils/errors.ts
export class AppError extends Error {
  constructor(
    message: string,
    public statusCode: number = 500,
    public code: string = 'INTERNAL_ERROR',
    public isOperational: boolean = true,
  ) {
    super(message);
    this.name = this.constructor.name;
    Error.captureStackTrace(this, this.constructor);
  }
}

export class NotFoundError extends AppError {
  constructor(message = 'Resource not found') {
    super(message, 404, 'NOT_FOUND');
  }
}

export class UnauthorizedError extends AppError {
  constructor(message = 'Unauthorized') {
    super(message, 401, 'UNAUTHORIZED');
  }
}

export class ValidationError extends AppError {
  constructor(
    message = 'Validation failed',
    public errors: Record<string, string[]> = {},
  ) {
    super(message, 400, 'VALIDATION_ERROR');
  }
}

// middleware/errorHandler.ts
import { type ErrorRequestHandler } from 'express';
import { AppError } from '../utils/errors';
import { ZodError } from 'zod';
import { logger } from '../utils/logger';

export const errorHandler: ErrorRequestHandler = (err, _req, res, _next) => {
  // Log error
  logger.error(err);

  // Zod validation error
  if (err instanceof ZodError) {
    res.status(400).json({
      error: 'Validation failed',
      code: 'VALIDATION_ERROR',
      details: err.flatten().fieldErrors,
    });
    return;
  }

  // Known operational error
  if (err instanceof AppError && err.isOperational) {
    res.status(err.statusCode).json({
      error: err.message,
      code: err.code,
    });
    return;
  }

  // Unknown error - don't leak details
  res.status(500).json({
    error: 'Internal server error',
    code: 'INTERNAL_ERROR',
  });
};
```

### Logging with Pino

```typescript
// utils/logger.ts
import pino from 'pino';

export const logger = pino({
  level: process.env.LOG_LEVEL ?? 'info',
  transport: process.env.NODE_ENV === 'development'
    ? { target: 'pino-pretty', options: { colorize: true } }
    : undefined,
  formatters: {
    level: (label) => ({ level: label }),
  },
  timestamp: pino.stdTimeFunctions.isoTime,
});

// Request logger middleware
import { type RequestHandler } from 'express';
import { randomUUID } from 'crypto';

export const requestLogger: RequestHandler = (req, res, next) => {
  const requestId = randomUUID();
  req.id = requestId;

  const start = Date.now();

  res.on('finish', () => {
    logger.info({
      requestId,
      method: req.method,
      url: req.originalUrl,
      statusCode: res.statusCode,
      duration: Date.now() - start,
    });
  });

  next();
};
```

---

## Bun Runtime

### When to Use Bun

| Use Bun | Use Node.js |
|---------|-------------|
| New projects | Legacy codebases |
| Maximum performance | Maximum compatibility |
| TypeScript-first | Complex native deps |
| Monorepos | AWS Lambda (check support) |
| Development tooling | Enterprise requirements |

### Bun Project Setup

```bash
# Initialize project
bun init

# Install dependencies
bun add express zod

# Run TypeScript directly
bun run src/index.ts

# Run tests
bun test
```

### Bun Configuration

```json
// bunfig.toml
[install]
registry = "https://registry.npmjs.org/"
lockfile = true

[run]
bun = true

[test]
coverage = true
coverageDir = "./coverage"
```

### Bun HTTP Server

```typescript
// Native Bun server (fastest)
const server = Bun.serve({
  port: 3000,
  fetch(request) {
    const url = new URL(request.url);

    if (url.pathname === '/api/users' && request.method === 'GET') {
      return Response.json({ users: [] });
    }

    if (url.pathname === '/api/users' && request.method === 'POST') {
      return handleCreateUser(request);
    }

    return new Response('Not Found', { status: 404 });
  },
});

console.log(`Server running at http://localhost:${server.port}`);

async function handleCreateUser(request: Request): Promise<Response> {
  const body = await request.json();
  // Process...
  return Response.json({ id: '1', ...body }, { status: 201 });
}
```

### Bun Testing

```typescript
// tests/users.test.ts
import { describe, it, expect, beforeEach } from 'bun:test';
import { createApp } from '../src/app';

describe('Users API', () => {
  let app: ReturnType<typeof createApp>;

  beforeEach(() => {
    app = createApp();
  });

  it('should return empty users list', async () => {
    const response = await app.request('/api/users');

    expect(response.status).toBe(200);

    const data = await response.json();
    expect(data.users).toEqual([]);
  });

  it('should create a user', async () => {
    const response = await app.request('/api/users', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: 'John', email: 'john@example.com' }),
    });

    expect(response.status).toBe(201);
  });
});
```

---

## TypeScript Patterns

### Strict Mode Benefits

```typescript
// strict: true enables all of these
{
  "noImplicitAny": true,        // No implicit any
  "strictNullChecks": true,      // null/undefined handling
  "strictFunctionTypes": true,   // Function param contravariance
  "strictBindCallApply": true,   // Correct bind/call/apply types
  "strictPropertyInitialization": true,  // Class property init
  "noImplicitThis": true,        // Explicit this types
  "alwaysStrict": true           // ES5 strict mode
}

// Additional strict options (enable manually)
{
  "noUncheckedIndexedAccess": true,  // Array access returns T | undefined
  "exactOptionalPropertyTypes": true, // undefined !== optional
  "noImplicitReturns": true          // All code paths must return
}
```

### Utility Types

```typescript
// Built-in utility types
type UserPartial = Partial<User>;           // All props optional
type UserRequired = Required<User>;         // All props required
type UserReadonly = Readonly<User>;         // All props readonly
type UserName = Pick<User, 'name' | 'email'>;
type UserWithoutPassword = Omit<User, 'password'>;
type IdType = User['id'];                   // Indexed access
type UserKeys = keyof User;                 // Union of keys
type StringUser = Record<string, User>;     // Index signature

// Creating precise types
type Status = 'pending' | 'active' | 'inactive';
type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE';

// Template literal types
type EventName = `on${Capitalize<string>}`;  // 'onClick', 'onSubmit', etc.
type Endpoint = `/api/${string}`;

// Conditional types
type ArrayElement<T> = T extends (infer U)[] ? U : never;
type Awaited<T> = T extends Promise<infer U> ? U : T;
```

### Generic Patterns

```typescript
// Generic function with constraints
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

// Generic interface
interface Repository<T extends { id: string }> {
  findById(id: string): Promise<T | null>;
  findAll(): Promise<T[]>;
  create(data: Omit<T, 'id'>): Promise<T>;
  update(id: string, data: Partial<T>): Promise<T>;
  delete(id: string): Promise<void>;
}

// Generic React component
interface ListProps<T> {
  items: T[];
  renderItem: (item: T, index: number) => React.ReactNode;
  keyExtractor: (item: T) => string;
}

function List<T>({ items, renderItem, keyExtractor }: ListProps<T>) {
  return (
    <ul>
      {items.map((item, index) => (
        <li key={keyExtractor(item)}>{renderItem(item, index)}</li>
      ))}
    </ul>
  );
}
```

### Type Guards

```typescript
// Type predicate
function isUser(value: unknown): value is User {
  return (
    typeof value === 'object' &&
    value !== null &&
    'id' in value &&
    'email' in value
  );
}

// Discriminated union
type Result<T, E = Error> =
  | { success: true; data: T }
  | { success: false; error: E };

function handleResult<T>(result: Result<T>): T {
  if (result.success) {
    return result.data;  // TypeScript knows data exists
  }
  throw result.error;    // TypeScript knows error exists
}

// Assertion function
function assertDefined<T>(
  value: T | null | undefined,
  message = 'Value is null or undefined',
): asserts value is T {
  if (value === null || value === undefined) {
    throw new Error(message);
  }
}
```

### Zod Schema Validation

```typescript
import { z } from 'zod';

// Define schema
const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  name: z.string().min(2).max(100),
  age: z.number().int().positive().optional(),
  role: z.enum(['admin', 'user', 'guest']),
  createdAt: z.date(),
});

// Infer TypeScript type from schema
type User = z.infer<typeof UserSchema>;

// Create partial schema for updates
const UpdateUserSchema = UserSchema.partial().omit({ id: true });
type UpdateUserData = z.infer<typeof UpdateUserSchema>;

// Validation
function validateUser(data: unknown): User {
  return UserSchema.parse(data);  // Throws ZodError if invalid
}

function safeValidateUser(data: unknown): Result<User> {
  const result = UserSchema.safeParse(data);
  if (result.success) {
    return { success: true, data: result.data };
  }
  return { success: false, error: result.error };
}
```

---

## Testing Patterns

### Jest/Vitest Configuration

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.ts',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: ['node_modules/', 'src/test/'],
    },
  },
});
```

### Unit Testing

```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { calculateDiscount } from './pricing';

describe('calculateDiscount', () => {
  it('should apply percentage discount', () => {
    const result = calculateDiscount(100, { type: 'percentage', value: 10 });
    expect(result).toBe(90);
  });

  it('should apply fixed discount', () => {
    const result = calculateDiscount(100, { type: 'fixed', value: 15 });
    expect(result).toBe(85);
  });

  it('should not go below zero', () => {
    const result = calculateDiscount(10, { type: 'fixed', value: 20 });
    expect(result).toBe(0);
  });

  it('should throw for negative price', () => {
    expect(() => calculateDiscount(-10, { type: 'fixed', value: 5 }))
      .toThrow('Price must be positive');
  });
});
```

### Component Testing

```tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi } from 'vitest';
import { LoginForm } from './LoginForm';

describe('LoginForm', () => {
  it('should render email and password inputs', () => {
    render(<LoginForm onSubmit={vi.fn()} />);

    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
  });

  it('should call onSubmit with form data', async () => {
    const handleSubmit = vi.fn();
    const user = userEvent.setup();

    render(<LoginForm onSubmit={handleSubmit} />);

    await user.type(screen.getByLabelText(/email/i), 'test@example.com');
    await user.type(screen.getByLabelText(/password/i), 'password123');
    await user.click(screen.getByRole('button', { name: /sign in/i }));

    await waitFor(() => {
      expect(handleSubmit).toHaveBeenCalledWith({
        email: 'test@example.com',
        password: 'password123',
      });
    });
  });

  it('should show validation error for invalid email', async () => {
    const user = userEvent.setup();

    render(<LoginForm onSubmit={vi.fn()} />);

    await user.type(screen.getByLabelText(/email/i), 'invalid-email');
    await user.click(screen.getByRole('button', { name: /sign in/i }));

    expect(await screen.findByText(/valid email/i)).toBeInTheDocument();
  });
});
```

### Mocking

```typescript
import { vi, type Mock } from 'vitest';
import { fetchUsers } from './api';
import { getUsers } from './users.service';

// Mock module
vi.mock('./api', () => ({
  fetchUsers: vi.fn(),
}));

describe('getUsers', () => {
  const mockFetchUsers = fetchUsers as Mock;

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should return users from API', async () => {
    const mockUsers = [{ id: '1', name: 'John' }];
    mockFetchUsers.mockResolvedValue(mockUsers);

    const result = await getUsers();

    expect(result).toEqual(mockUsers);
    expect(mockFetchUsers).toHaveBeenCalledTimes(1);
  });

  it('should handle API error', async () => {
    mockFetchUsers.mockRejectedValue(new Error('Network error'));

    await expect(getUsers()).rejects.toThrow('Network error');
  });
});
```

### API Testing with MSW

```typescript
// test/mocks/handlers.ts
import { http, HttpResponse } from 'msw';

export const handlers = [
  http.get('/api/users', () => {
    return HttpResponse.json({
      users: [
        { id: '1', name: 'John' },
        { id: '2', name: 'Jane' },
      ],
    });
  }),

  http.post('/api/users', async ({ request }) => {
    const body = await request.json();
    return HttpResponse.json(
      { id: '3', ...body },
      { status: 201 },
    );
  }),
];

// test/mocks/server.ts
import { setupServer } from 'msw/node';
import { handlers } from './handlers';

export const server = setupServer(...handlers);

// test/setup.ts
import { beforeAll, afterEach, afterAll } from 'vitest';
import { server } from './mocks/server';

beforeAll(() => server.listen({ onUnhandledRequest: 'error' }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

---

## Methodologies (8)

### M-JS-001: Component-First Architecture

**Problem:** Large React applications become hard to maintain without clear structure.

**Framework:**
1. Organize by feature, not by type
2. Colocate related files (component, tests, styles, types)
3. Use barrel exports (`index.ts`) for public API
4. Keep components pure when possible
5. Extract business logic to hooks and services

**Checklist:**
- [ ] Each feature folder is self-contained
- [ ] Components have single responsibility
- [ ] Custom hooks extract reusable logic
- [ ] Types are defined close to usage
- [ ] Tests are colocated with components

### M-JS-002: TypeScript Strict Mode

**Problem:** TypeScript without strict mode allows unsafe patterns.

**Framework:**
1. Enable `strict: true` in tsconfig.json
2. Enable `noUncheckedIndexedAccess`
3. Use explicit return types for public functions
4. Prefer `unknown` over `any`
5. Use type guards and assertion functions

**Checklist:**
- [ ] strict mode enabled
- [ ] No `any` types (use `unknown`)
- [ ] All function parameters typed
- [ ] Public functions have return types
- [ ] Arrays accessed safely

### M-JS-003: React Hooks Best Practices

**Problem:** Improper hook usage causes bugs and performance issues.

**Framework:**
1. Follow Rules of Hooks (top level, React functions only)
2. Use correct dependencies in useEffect/useCallback/useMemo
3. Custom hooks start with `use`
4. Return stable references when possible
5. Clean up effects properly

**Checklist:**
- [ ] No hooks in conditions or loops
- [ ] Effect dependencies are complete
- [ ] Memoization used appropriately
- [ ] Custom hooks are composable
- [ ] Effects have cleanup functions

### M-JS-004: Node.js Service Layer

**Problem:** Business logic mixed in controllers is hard to test and reuse.

**Framework:**
1. Controllers handle HTTP concerns only
2. Services contain business logic
3. Repositories handle data access
4. Use dependency injection for testability
5. Services are stateless

**Checklist:**
- [ ] Controllers are thin
- [ ] Services have no HTTP imports
- [ ] Database queries in repositories
- [ ] Each service has clear responsibility
- [ ] Services are unit testable

### M-JS-005: Error Handling Strategy

**Problem:** Inconsistent error handling leads to poor UX and debugging.

**Framework:**
1. Create custom error classes with codes
2. Centralize error handling in middleware
3. Log all errors with context
4. Return consistent error responses
5. Never expose internal errors to clients

**Checklist:**
- [ ] Custom AppError base class
- [ ] Specific error classes (NotFound, Validation, etc.)
- [ ] Central error handler middleware
- [ ] Structured logging with Pino/Winston
- [ ] Production errors sanitized

### M-JS-006: Testing Pyramid

**Problem:** Unbalanced test suites are slow or provide poor coverage.

**Framework:**
1. Unit tests: 70% - fast, isolated, focused
2. Integration tests: 20% - component interactions
3. E2E tests: 10% - critical user flows
4. Use MSW for API mocking
5. Focus on behavior, not implementation

**Checklist:**
- [ ] Core logic has unit tests
- [ ] API endpoints have integration tests
- [ ] Critical paths have E2E tests
- [ ] Tests run in CI/CD
- [ ] Coverage above 80% for business logic

### M-JS-007: Package Management

**Problem:** Poor dependency management causes version conflicts and security issues.

**Framework:**
1. Use lockfile (pnpm-lock.yaml, package-lock.json)
2. Pin direct dependencies
3. Audit regularly: `pnpm audit`
4. Update minor versions monthly
5. Major updates with testing

**Checklist:**
- [ ] Lockfile committed to repo
- [ ] No floating versions (^, ~)
- [ ] Security audit in CI
- [ ] Renovate/Dependabot configured
- [ ] Update schedule documented

### M-JS-008: Performance Optimization

**Problem:** React apps become slow without intentional optimization.

**Framework:**
1. Profile before optimizing (React DevTools)
2. Memoize expensive computations
3. Virtualize long lists
4. Code split routes and heavy components
5. Optimize bundle size

**Checklist:**
- [ ] Performance measured with Lighthouse
- [ ] React.memo for pure components
- [ ] useMemo/useCallback where needed
- [ ] react-virtual for long lists
- [ ] Bundle analyzer configured


> **Note:** Full methodology details available in `methodologies/` folder.

---

## Decision Tree: Where to Put Code

```
What does the code do?
│
├─► UI rendering?
│   └─► components/
│
├─► Shared state logic?
│   └─► hooks/
│
├─► API calls?
│   └─► services/ or api/
│
├─► Data transformation?
│   └─► utils/
│
├─► Type definitions?
│   └─► types/ or colocated
│
└─► Third-party wrapper?
    └─► lib/
```

---

## References

**Official Documentation:**
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [React Documentation](https://react.dev/)
- [Node.js Documentation](https://nodejs.org/docs/)
- [Bun Documentation](https://bun.sh/docs)

**Best Practices:**
- [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/)
- [Node.js Best Practices](https://github.com/goldbergyoni/nodebestpractices)
- [TypeScript Deep Dive](https://basarat.gitbook.io/typescript/)

**Tools:**
- [ESLint](https://eslint.org/)
- [Prettier](https://prettier.io/)
- [Vitest](https://vitest.dev/)
- [MSW](https://mswjs.io/)
- [TanStack Query](https://tanstack.com/query/)
- [Zustand](https://zustand-demo.pmnd.rs/)
- [Zod](https://zod.dev/)

---

## Sources

- [TypeScript Official Docs](https://www.typescriptlang.org/)
- [React Official Docs](https://react.dev/)
- [Node.js Official Docs](https://nodejs.org/)
- [Bun Official Docs](https://bun.sh/)
- [Vitest Official Docs](https://vitest.dev/)
- [ESLint Official Docs](https://eslint.org/)
