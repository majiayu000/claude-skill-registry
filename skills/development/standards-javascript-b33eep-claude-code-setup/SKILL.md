---
name: standards-javascript
description: This skill provides JavaScript coding standards and is automatically loaded for JavaScript projects. It includes modern ES2025 patterns, async handling, and recommended tooling.
type: context
applies_to: [javascript, nodejs, express, fastify, hapi, npm, yarn, pnpm, bun, deno, vitest, jest, mocha]
file_extensions: [".js", ".mjs", ".cjs"]
---

# JavaScript Coding Standards

## Core Principles

1. **Simplicity**: Simple, understandable code
2. **Readability**: Readability over cleverness
3. **Maintainability**: Code that's easy to maintain
4. **Testability**: Code that's easy to test
5. **DRY**: Don't Repeat Yourself - but don't overdo it

## General Rules

- **Early Returns**: Use early returns to avoid nesting
- **Descriptive Names**: Meaningful names for variables and functions
- **Minimal Changes**: Only change relevant code parts
- **No Over-Engineering**: No unnecessary complexity
- **Minimal Comments**: Code should be self-explanatory. No redundant comments!
- **Async/Await**: Always use async/await for async operations

## Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Variables/Functions | camelCase | `getUserById`, `isActive` |
| Classes | PascalCase | `UserService`, `ApiClient` |
| Constants | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |
| Private | Prefix with `_` or `#` | `_internalMethod`, `#privateField` |
| Files | kebab-case or camelCase | `user-service.js`, `userService.js` |
| Event Handlers | Prefix with `handle` | `handleClick`, `handleSubmit` |

## Project Structure

```
myproject/
├── src/
│   ├── index.js              # Entry point
│   ├── config.js             # Settings, env vars
│   ├── models/
│   │   └── user.js           # Domain models
│   ├── services/
│   │   └── user-service.js   # Business logic
│   ├── routes/
│   │   └── user-routes.js    # API routes
│   └── utils/
│       └── helpers.js        # Utility functions
├── tests/
│   ├── services/
│   │   └── user-service.test.js
│   └── setup.js
├── package.json
└── README.md
```

## ES Modules (Preferred)

```javascript
// math.js - Named exports
export function add(a, b) {
    return a + b;
}

export function multiply(a, b) {
    return a * b;
}

// app.js - Import
import { add, multiply } from './math.js';

// Default export
export default class UserService {
    // ...
}

// Import default
import UserService from './user-service.js';
```

**package.json for ES Modules:**
```json
{
    "type": "module",
    "exports": {
        ".": "./src/index.js",
        "./utils": "./src/utils/index.js"
    }
}
```

## Async/Await Patterns

```javascript
// Always use async/await for async operations
async function fetchUserData(userId) {
    try {
        const response = await fetch(`https://api.example.com/users/${userId}`);

        if (!response.ok) {
            throw new Error(`API error: ${response.statusText}`);
        }

        return await response.json();
    } catch (error) {
        console.error('Fetch failed:', error);
        throw error;
    }
}

// Parallel execution with Promise.all
async function fetchMultipleUsers(userIds) {
    const users = await Promise.all(
        userIds.map(id => fetchUserData(id))
    );
    return users;
}

// Race with timeout
async function fetchWithTimeout(promise, timeout) {
    return Promise.race([
        promise,
        new Promise((_, reject) =>
            setTimeout(() => reject(new Error('Timeout')), timeout)
        ),
    ]);
}

// Get all results, including failures
async function fetchAllSettled(urls) {
    const results = await Promise.allSettled(
        urls.map(url => fetch(url).then(r => r.json()))
    );
    return results;
}
```

## Best Practices

```javascript
// Prefer const over let
const users = [];

// Use nullish coalescing and optional chaining
const name = user?.profile?.name ?? 'Anonymous';

// Prefer template literals
const message = `Hello, ${user.name}!`;

// Use destructuring
const { id, name, email } = user;
function processUser({ id, name }) { }

// Prefer array methods over loops
const activeUsers = users.filter(u => u.isActive);
const userNames = users.map(u => u.name);
const totalAge = users.reduce((sum, u) => sum + u.age, 0);

// Use Object.freeze for immutable constants
const CONFIG = Object.freeze({
    apiUrl: 'https://api.example.com',
    maxRetries: 3,
});

// Private class fields with #
class UserService {
    #apiClient;

    constructor(apiClient) {
        this.#apiClient = apiClient;
    }

    async getUser(id) {
        return this.#apiClient.get(`/users/${id}`);
    }
}
```

## Express Framework

```javascript
import express from 'express';

const app = express();
app.use(express.json());

// Routes
app.get('/users', (req, res) => {
    res.json([
        { id: 1, name: 'John' },
        { id: 2, name: 'Jane' },
    ]);
});

app.post('/users', (req, res) => {
    const { name } = req.body;
    res.status(201).json({ id: 3, name });
});

app.get('/users/:id', (req, res) => {
    const { id } = req.params;
    res.json({ id: parseInt(id), name: 'User' });
});

// Error handling middleware (must be last)
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ error: 'Internal Server Error' });
});

app.listen(3000, () => {
    console.log('Server running on :3000');
});
```

**Middleware Pattern:**
```javascript
// Logging middleware
const logger = (req, res, next) => {
    console.log(`${req.method} ${req.path}`);
    next();
};

// Authentication middleware
const authenticateToken = (req, res, next) => {
    const authHeader = req.headers['authorization'];
    const token = authHeader?.split(' ')[1];

    if (!token) {
        return res.status(401).json({ error: 'Missing token' });
    }

    // Verify token...
    req.user = decodedUser;
    next();
};

app.use(logger);
app.use('/api/protected', authenticateToken);
```

## Fastify Framework

```javascript
import Fastify from 'fastify';

const fastify = Fastify({ logger: true });

fastify.get('/users/:id', async (request, reply) => {
    const { id } = request.params;
    return { id: parseInt(id), name: 'User' };
});

fastify.post('/users', async (request, reply) => {
    const { name } = request.body;
    reply.code(201);
    return { id: 1, name };
});

fastify.listen({ port: 3000 }, (err, address) => {
    if (err) throw err;
    console.log(`Server listening at ${address}`);
});
```

## Error Handling

```javascript
// Custom error classes
class AppError extends Error {
    constructor(message, statusCode = 500) {
        super(message);
        this.name = 'AppError';
        this.statusCode = statusCode;
    }
}

class NotFoundError extends AppError {
    constructor(resource) {
        super(`${resource} not found`, 404);
        this.name = 'NotFoundError';
    }
}

// Result pattern for explicit error handling
function divide(a, b) {
    if (b === 0) {
        return { ok: false, error: 'Division by zero' };
    }
    return { ok: true, value: a / b };
}

const result = divide(10, 2);
if (result.ok) {
    console.log(result.value);
} else {
    console.error(result.error);
}
```

## Testing with Vitest

```javascript
import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { add, multiply } from './math.js';

describe('Math utils', () => {
    it('should add numbers', () => {
        expect(add(2, 3)).toBe(5);
    });

    it('should multiply numbers', () => {
        expect(multiply(2, 3)).toBe(6);
    });
});

// Integration test example
describe('API Endpoints', () => {
    let server;

    beforeEach(() => {
        server = createServer();
    });

    afterEach(() => {
        server.close();
    });

    it('GET /users returns user list', async () => {
        const response = await fetch('http://localhost:3000/users');
        const data = await response.json();

        expect(response.ok).toBe(true);
        expect(Array.isArray(data)).toBe(true);
    });
});
```

## Environment Configuration

```javascript
// config.js
const config = {
    development: {
        port: 3000,
        database: 'mongodb://localhost:27017/mydb',
        logLevel: 'debug',
    },
    production: {
        port: process.env.PORT || 8080,
        database: process.env.DATABASE_URL,
        logLevel: 'info',
    },
};

const env = process.env.NODE_ENV || 'development';
export default config[env];
```

## Comments - Less is More

```javascript
// BAD - redundant comment
// Get the user from database
const user = repository.getUser(userId);

// GOOD - self-explanatory code, no comment needed
const user = repository.getUser(userId);

// GOOD - comment explains WHY (not obvious)
// Rate limit: API allows max 1000 requests/min
await rateLimiter.acquire();
```

## Recommended Tooling

| Tool | Purpose |
|------|---------|
| `pnpm` or `bun` | Package manager (faster than npm) |
| `eslint` | Linting |
| `prettier` | Code formatting |
| `vitest` or `jest` | Testing framework |
| `node --watch` | Development with auto-reload |
| `dotenv` | Environment variable management |

## package.json Template

```json
{
    "name": "@org/myapp",
    "version": "1.0.0",
    "type": "module",
    "main": "src/index.js",
    "exports": {
        ".": "./src/index.js",
        "./utils": "./src/utils/index.js"
    },
    "engines": {
        "node": ">=22.0.0"
    },
    "scripts": {
        "dev": "node --watch src/index.js",
        "start": "node src/index.js",
        "test": "vitest",
        "lint": "eslint ."
    }
}
```

## Production Best Practices

1. **ES Modules** - Use `"type": "module"` in package.json
2. **Async/Await** - Always use async/await for async operations
3. **Error Handling** - Handle promise rejections properly
4. **Validation** - Validate input in API endpoints
5. **Environment Variables** - Use dotenv or similar for config
6. **Graceful Shutdown** - Handle SIGTERM for clean exit
7. **Testing** - Test with Vitest or Jest
8. **Linting** - Use ESLint with recommended rules
9. **Security** - Run `npm audit` regularly
10. **Process Management** - Use PM2 for production

---

## References

- Based on [moai-lang-javascript](https://github.com/AJBcoding/claude-skill-eval/tree/main/skills/moai-lang-javascript) by AJBcoding
