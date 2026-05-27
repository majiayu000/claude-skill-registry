---
name: data-service
description: Use when scaffolding, auditing, or validating MetaSaver data service packages. Covers feature-based structure, service/controller/routes pattern, middleware integration, and API endpoint setup. Requires @metasaver/core-service-utils, {project}-contracts, {project}-database packages. File types: .ts, package.json.
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Data Service Package Structure for MetaSaver

## Purpose

This skill documents the complete file and folder organization for MetaSaver data service packages (e.g., rugby-crm-service). Data services are Express-based API packages that coordinate between database clients and HTTP handlers using a feature-based structure.

Data services provide:

- Feature-based organization with service/controller/routes per feature
- Service classes handling Prisma database operations
- Controllers coordinating validation and error handling
- Route definitions with JWT auth and permission checking
- Health check and API versioning
- Environment configuration and initialization

**Use when:**

- Scaffolding a new data service package
- Auditing an existing data service for compliance
- Adding a new feature (service + controller + routes)
- Setting up middleware (auth, logging, error handling)
- Creating health checks and API versioning structure

## Directory Structure Reference

### Package Root Files

```
packages/services/{project}-service/
├── package.json              # Package metadata and scripts
├── tsconfig.json             # TypeScript configuration
├── README.md                 # Package documentation
├── .env.example              # Environment variable template
├── eslint.config.js          # ESLint configuration (flat config)
├── Dockerfile                # Docker build configuration
└── dist/                     # Build output (generated)
```

### Source Directory Structure

```
src/
├── index.ts                  # Service entry point
├── env.ts                    # Environment configuration
├── server.ts                 # Express app factory
├── routes/
│   └── register.ts           # Route registration
├── middleware/
│   ├── auth.ts               # JWT auth middleware
│   ├── error.ts              # Error handling middleware
│   └── logging.ts            # Request logging middleware
└── features/
    └── {feature}/
        ├── {feature}.service.ts      # Service class (Prisma operations)
        └── {feature}.controller.ts   # Controller (validation + response)
```

**Complete Example:**

```
packages/services/rugby-crm-service/
├── package.json
├── tsconfig.json
├── .env.example
├── eslint.config.js
├── README.md
├── Dockerfile
├── src/
│   ├── index.ts
│   ├── env.ts
│   ├── server.ts
│   ├── routes/
│   │   └── register.ts
│   ├── middleware/
│   │   ├── auth.ts
│   │   ├── error.ts
│   │   └── logging.ts
│   └── features/
│       ├── users/
│       │   ├── users.service.ts
│       │   └── users.controller.ts
│       └── teams/
│           ├── teams.service.ts
│           └── teams.controller.ts
└── dist/                     # Build output (generated)
```

## Key Packages

| Package                         | Purpose                             | Key Exports                                 |
| ------------------------------- | ----------------------------------- | ------------------------------------------- |
| `@metasaver/core-service-utils` | Service factory and utilities       | `createService`, `ApiError`, `asyncHandler` |
| `{project}-contracts`           | Zod validation schemas and types    | Validation schemas, types                   |
| `{project}-database`            | Prisma client and database types    | `prisma`, Prisma types                      |
| `express`                       | HTTP framework                      | Express Router, middleware                  |
| `jsonwebtoken`                  | JWT token creation and verification | `sign`, `verify`                            |

## File Organization Rules

### Package.json Structure

**Required Fields:**

- `name`: `@metasaver/{project}-service` (always scoped)
- `version`: `0.1.0` (start with patch version)
- `type`: `"module"` (ESM packages)
- `main`: `"./dist/index.js"`
- `types`: `"./dist/index.d.ts"`

**Required Scripts:**

- `build`: TypeScript compilation (`tsc -b`)
- `clean`: Remove build artifacts
- `dev`: Run with tsx for development (`tsx watch src/index.ts`)
- `start`: Production server startup
- `lint`, `lint:fix`, `lint:tsc`, `prettier`, `prettier:fix`
- `test:unit`: Unit tests (stub or actual)

See `templates/package.json.template` for complete template.

### Environment Configuration

**Rule:** Export a single `env` object with all configuration, type-safe with defaults.

**Variable Naming:** `{PROJECT_UPPER}_{SETTING_NAME}` (e.g., `RUGBY_CRM_SERVICE_PORT`)

See `templates/env.ts.template` for implementation.

### TypeScript Configuration

**Rule:** Extend base config with proper ESM settings.

See `templates/tsconfig.json.template` for configuration.

### Service Class Pattern

**Key Points:**

- Class-based for organization and testability
- Methods return typed results (Prisma types from contracts)
- Use `include` for eager-loading relations
- No HTTP concerns (pure data layer)
- Standard methods: `getAll`, `getById`, `create`, `update`, `delete`

**Import pattern:**

```typescript
// Import order example
import { prisma } from "@metasaver/rugby-crm-database/client";
import type {
  User,
  CreateUserInput,
  UpdateUserInput,
} from "@metasaver/rugby-crm-contracts/users/types";

export class UsersService {
  // ... methods
}
```

See `templates/feature-service.ts.template` for implementation.

### Controller Pattern

**Key Points:**

- `asyncHandler` wraps async functions to catch errors automatically
- Uses Zod schemas from contracts package for validation
- `ApiError.notFound()` for consistent error responses
- Returns `{ data: {...} }` for consistent response format
- HTTP status codes follow REST conventions

**Import pattern:**

```typescript
// Import order example
import { Router } from "express";
import { asyncHandler, ApiError } from "@metasaver/core-service-utils";
import {
  CreateUserRequest,
  UpdateUserRequest,
} from "@metasaver/rugby-crm-contracts/users/validation";
import { UsersService } from "#/features/users/users.service.js";

export const router = Router();
const service = new UsersService();

// ... route definitions
```

See `templates/feature-controller.ts.template` for implementation.

### Routes Registration Pattern

**Key Points:**

- Health check at root level (no authentication)
- All API routes under `/api/v1` with versioning
- Auth middleware applied to all API routes
- Feature routers mounted with base paths

**Import pattern:**

```typescript
// Import order example
import type { Express } from "express";
import { authMiddleware } from "#/middleware/auth.js";
import { router as usersRouter } from "#/features/users/users.controller.js";
import { router as teamsRouter } from "#/features/teams/teams.controller.js";

export function registerRoutes(app: Express) {
  // Health check (no auth)
  app.get("/health", (req, res) => res.json({ status: "ok" }));

  // API routes (with auth)
  app.use("/api/v1/users", authMiddleware, usersRouter);
  app.use("/api/v1/teams", authMiddleware, teamsRouter);
}
```

See `templates/register.ts.template` for implementation.

### Server Initialization Pattern

**Key Points:**

- Factory function returns app instance
- Middleware order: JSON → Logging → Routes → Error handling
- Error middleware must be last in stack

See `templates/server.ts.template` and `templates/index.ts.template`.

### Feature Import Pattern

**Rule:** Always use direct imports from specific files with `#/` alias for internal imports.

```typescript
// CORRECT - Direct imports with #/ alias
import { UsersService } from "#/features/users/users.service.js";
import { router as usersRouter } from "#/features/users/users.controller.js";

// INCORRECT - Do not use barrel exports (index.ts)
import { UsersService, UsersRoutes } from "#/features/users/index.js";
```

**Key principles:**

- Always use direct exports - do not create barrel export files (index.ts) in feature folders
- Always use `#/` alias for internal imports within service package
- Always import workspace packages with full paths: `from "@metasaver/{pkg}/{path}"`

## Workflow: Scaffolding New Data Service Package

1. **Create Package Directory**

   ```bash
   mkdir -p packages/services/{project}-service/src/{features,middleware,routes}
   ```

2. **Create Configuration Files** (use templates)
   - `package.json`, `tsconfig.json`, `.env.example`, `eslint.config.js`, `Dockerfile`

3. **Create Core Service Files** (use templates)
   - `src/env.ts`, `src/server.ts`, `src/index.ts`

4. **Create Middleware Files** (use templates)
   - `src/middleware/auth.ts`, `src/middleware/error.ts`, `src/middleware/logging.ts`

5. **Create Route Registration** (use template)
   - `src/routes/register.ts`

6. **Create Features** (repeat per feature)
   - `src/features/{feature}/{feature}.service.ts`
   - `src/features/{feature}/{feature}.controller.ts`
   - NO index.ts barrel export files

7. **Test Build and Run**

   ```bash
   pnpm --filter @metasaver/{project}-service build
   pnpm --filter @metasaver/{project}-service dev
   ```

## Workflow: Adding New Feature

1. Create feature directory: `mkdir -p src/features/{feature}`
2. Create service class (from template): `{feature}.service.ts`
3. Create controller (from template): `{feature}.controller.ts`
4. Register in `src/routes/register.ts` with direct imports
5. Build and test

**Import example in register.ts:**

```typescript
import { router as newFeatureRouter } from "#/features/{feature}/{feature}.controller.js";
app.use("/api/v1/{feature}", authMiddleware, newFeatureRouter);
```

## Audit Checklist

### Package Structure

- [ ] Package directory at `packages/services/{project}-service/`
- [ ] All required subdirectories: `src/features`, `src/middleware`, `src/routes`
- [ ] Build output in `dist/` (git-ignored)

### package.json

- [ ] Name: `@metasaver/{project}-service` (scoped)
- [ ] Version: `0.1.0` (semantic versioning)
- [ ] Type: `"module"` (ESM)
- [ ] All required scripts: build, clean, dev, start, lint, prettier, test
- [ ] Correct dependencies: express, jsonwebtoken, @metasaver/core-service-utils
- [ ] Workspace dependencies: {project}-contracts, {project}-database

### TypeScript Configuration

- [ ] `tsconfig.json` extends `@metasaver/core-typescript-config/base`
- [ ] Proper module settings for ESM (`module: "ESNext"`)
- [ ] Correct `rootDir: "./src"` and `outDir: "./dist"`

### Environment Configuration

- [ ] `src/env.ts` exports single `env` object
- [ ] `.env.example` exists (committed)
- [ ] No hardcoded secrets in code

### Server Initialization

- [ ] `src/server.ts` exports `createServer()` function
- [ ] `src/index.ts` creates server and listens on env.PORT
- [ ] Graceful shutdown implemented

### Middleware

- [ ] `src/middleware/auth.ts` exists (JWT verification)
- [ ] `src/middleware/error.ts` exists (error response formatting)
- [ ] `src/middleware/logging.ts` exists (request logging)
- [ ] Error middleware captures async errors via asyncHandler

### Routes & Features

- [ ] `src/routes/register.ts` centralizes all route mounting
- [ ] `/health` check available without authentication
- [ ] `/api/v1` versioning prefix
- [ ] All API routes require authentication
- [ ] Each feature has: service, controller in own folder
- [ ] Always use direct exports - ensure no `index.ts` barrel files in features
- [ ] Always wrap controllers with `asyncHandler`
- [ ] Always use Zod validation from contracts in controllers
- [ ] Always use `#/` alias for internal paths
- [ ] Always use full paths for workspace imports: `from "@metasaver/{pkg}/{path}"`

### Service Classes

- [ ] Methods return properly typed results
- [ ] No HTTP concerns (pure data operations)
- [ ] Standard methods: getAll, getById, create, update, delete

### Controllers

- [ ] All async operations wrapped with `asyncHandler`
- [ ] Consistent response format: `{ data: {...} }`
- [ ] Proper HTTP status codes (200, 201, 204, 404)

### Build & Compilation

- [ ] `pnpm build` succeeds without errors
- [ ] dist/ folder contains compiled files
- [ ] No type errors in `pnpm lint:tsc`

## Common Violations & Fixes

**Violation:** Express handlers not wrapped with asyncHandler

```typescript
// INCORRECT
router.get("/:id", async (req, res) => { ... });

// CORRECT
router.get("/:id", asyncHandler(async (req, res) => { ... }));
```

**Violation:** Service class with HTTP concerns

```typescript
// INCORRECT - service knows about HTTP
async getUser(req: Request): Promise<Response> { ... }

// CORRECT - service is pure data layer
async getById(id: string): Promise<User | null> { ... }
```

**Violation:** Custom validation instead of Zod

```typescript
// INCORRECT
if (!req.body.name || typeof req.body.name !== "string") { ... }

// CORRECT
const validated = CreateUserSchema.parse(req.body);
```

**Violation:** Direct environment variable access throughout code

```typescript
// INCORRECT - scattered env access
const port = process.env.PORT;

// CORRECT - centralized env object
import { env } from "./env.js";
```

## Related Skills

- **prisma-database** - Prisma schema and database client setup
- **contracts-package** - Zod validation schemas and type definitions
- **typescript-configuration** - TypeScript configuration (tsconfig.json)
- **eslint-agent** - ESLint configuration (eslint.config.js)
- **monorepo-structure** - Monorepo organization (packages/services/\*)
