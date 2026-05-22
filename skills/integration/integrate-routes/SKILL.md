---
name: integrate-routes
description: Mount routes in app.ts with dependency injection. Use after creating routes to wire them into the application. Triggers on "mount routes", "add to app", "wire routes", "integrate routes".
---

# Integrate Routes

Mounts newly created routes into `src/app.ts` with proper dependency injection chain.

## Quick Reference

**File to modify**: `src/app.ts`
**When to use**: After creating routes with `create-routes` skill

## Prerequisites

Before integrating routes, ensure you have:

1. Schema created (`src/schemas/{entity}.schema.ts`)
2. Repository implementation (`src/repositories/mockdb/{entity}.mockdb.repository.ts`)
3. Service created (`src/services/{entity}.service.ts`)
4. Controller created (`src/controllers/{entity}.controller.ts`)
5. Routes created (`src/routes/{entity}.router.ts`)

## Instructions

### Step 1: Add Imports

Add imports at the top of `src/app.ts`:

```typescript
// Route factory
import { create{Entity}Routes } from "@/routes/{entity-name}.router";

// Controller
import { {Entity}Controller } from "@/controllers/{entity-name}.controller";

// Service
import { {Entity}Service } from "@/services/{entity-name}.service";

// Repository (choose one based on environment)
import { MockDb{Entity}Repository } from "@/repositories/mockdb/{entity-name}.mockdb.repository";
// OR for production:
// import { MongoDb{Entity}Repository } from "@/repositories/mongodb/{entity-name}.mongodb.repository";
```

### Step 2: Create Dependency Chain

Add the dependency instantiation in the appropriate section of `app.ts`:

```typescript
// =============================================================================
// {Entity} Resource Dependencies
// =============================================================================
const {entity}Repository = new MockDb{Entity}Repository();
// OR for production: const {entity}Repository = new MongoDb{Entity}Repository();

const {entity}Service = new {Entity}Service({entity}Repository);
const {entity}Controller = new {Entity}Controller({entity}Service);
```

### Step 3: Mount Routes

Add the route mounting after other routes:

```typescript
// =============================================================================
// Routes
// =============================================================================
// ... existing routes ...

// {Entity} routes
app.route("/{entities}", create{Entity}Routes({ {entity}Controller }));
```

### Step 4: Verify Order

Ensure the following order in `app.ts`:

1. Imports
2. App creation (`const app = new Hono<AppEnv>()`)
3. Global middleware (CORS, etc.)
4. Dependency instantiation
5. Route mounting
6. Error handler (`app.onError(globalErrorHandler)`)
7. Export

## Patterns & Rules

### Dependency Chain Order

Always create dependencies in this order:

```typescript
// 1. Repository (lowest level)
const repository = new MockDbEntityRepository();

// 2. Service (depends on repository)
const service = new EntityService(repository);

// 3. Controller (depends on service)
const controller = new EntityController(service);

// 4. Routes (depends on controller)
app.route("/entities", createEntityRoutes({ entityController: controller }));
```

### Route Path Convention

- Use **plural** for entity routes: `/notes`, `/users`, `/projects`
- Use **kebab-case** for multi-word: `/course-registrations`
- Match the entity name (singular) to path (plural)

### Environment-Based Repository

For production-ready code, use environment-based selection:

```typescript
import { env } from "@/env";
import { MockDbNoteRepository } from "@/repositories/mockdb/note.mockdb.repository";
import { MongoDbNoteRepository } from "@/repositories/mongodb/note.mongodb.repository";

const noteRepository =
  env.NODE_ENV === "production"
    ? new MongoDbNoteRepository()
    : new MockDbNoteRepository();
```

### Grouping Dependencies

Group related dependencies with comments:

```typescript
// =============================================================================
// Note Resource
// =============================================================================
const noteRepository = new MockDbNoteRepository();
const noteService = new NoteService(noteRepository);
const noteController = new NoteController(noteService);

// =============================================================================
// Project Resource
// =============================================================================
const projectRepository = new MockDbProjectRepository();
const projectService = new ProjectService(projectRepository);
const projectController = new ProjectController(projectService);
```

## Complete Example

```typescript
import { Hono } from "hono";
import { cors } from "hono/cors";
import type { AppEnv } from "@/schemas/app-env.schema";
import { globalErrorHandler } from "@/errors";

// Route factories
import { createNoteRoutes } from "@/routes/note.router";
import { createProjectRoutes } from "@/routes/project.router";
import { createEventsRoutes } from "@/routes/events.router";

// Controllers
import { NoteController } from "@/controllers/note.controller";
import { ProjectController } from "@/controllers/project.controller";

// Services
import { NoteService } from "@/services/note.service";
import { ProjectService } from "@/services/project.service";

// Repositories
import { MockDbNoteRepository } from "@/repositories/mockdb/note.mockdb.repository";
import { MockDbProjectRepository } from "@/repositories/mockdb/project.mockdb.repository";

// =============================================================================
// App Setup
// =============================================================================
const app = new Hono<AppEnv>();

// Global middleware
app.use("*", cors());

// =============================================================================
// Note Resource
// =============================================================================
const noteRepository = new MockDbNoteRepository();
const noteService = new NoteService(noteRepository);
const noteController = new NoteController(noteService);

// =============================================================================
// Project Resource
// =============================================================================
const projectRepository = new MockDbProjectRepository();
const projectService = new ProjectService(projectRepository);
const projectController = new ProjectController(projectService);

// =============================================================================
// Routes
// =============================================================================
app.route("/notes", createNoteRoutes({ noteController }));
app.route("/projects", createProjectRoutes({ projectController }));
app.route("/", createEventsRoutes());

// =============================================================================
// Error Handler
// =============================================================================
app.onError(globalErrorHandler);

export { app };
```

## Troubleshooting

### Route Not Found (404)

- Check the path prefix matches your request
- Verify routes are mounted before the error handler
- Check for typos in route path

### Type Errors

- Ensure controller is passed with correct property name
- Verify all imports use correct casing
- Check that route factory expects the correct dependency interface

### Circular Dependencies

- Never import app.ts from other modules
- Keep dependency chain one-directional
- Use interface imports (`import type`) where possible

## What NOT to Do

- Do NOT mount routes after `app.onError()`
- Do NOT create dependencies inside route handlers
- Do NOT use `require()` - use ES modules
- Do NOT hardcode repository implementations - use DI
- Do NOT forget to export the app

## See Also

- `create-routes` - Creating the route factory
- `create-controller` - Creating the controller
- `create-resource-service` - Creating the service
- `create-resource` - Complete resource workflow
