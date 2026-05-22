---
name: "nestjs-modules-services-controllers"
description: "Use this skill whenever the user wants to design, create, refactor, or standardize NestJS modules, services, and controllers in a TypeScript NestJS project, following clean architecture, DI best practices, and consistent API patterns."
---

# NestJS Modules, Services & Controllers Skill

## Purpose

You are a specialized assistant for **structuring application features** in NestJS using:

- **Modules** to group related capabilities
- **Services** to implement business logic and data orchestration
- **Controllers** to expose HTTP (or other transport) APIs

Use this skill to:

- Create new **feature modules** (e.g. `users`, `auth`, `posts`, `billing`)
- Refactor or reorganize existing NestJS modules into a clean architecture
- Define **DTOs**, **interfaces**, and **service APIs** between layers
- Implement RESTful or RPC-like **controllers** with consistent patterns
- Wire features into `AppModule` or root modules appropriately
- Keep code testable, maintainable, and TypeORM/Supabase-ready

Do **not** use this skill for:

- Project-level scaffolding → use `nestjs-project-scaffold`
- Detailed authentication or security logic → use `nestjs-authentication`
- TypeORM entities/migrations → use `nestjs-typeorm-integration` / TypeORM skills
- Microservices transport-specific patterns → use dedicated microservices/queues skills

If `CLAUDE.md` exists, follow its guidelines on domain boundaries, naming, and architecture (e.g. “use hexagonal architecture”, “modules under src/modules”, etc.).

---

## When To Apply This Skill

Trigger this skill when the user says things like:

- “Create a `users` module with service and controller.”
- “Refactor this module structure, it’s messy.”
- “Add CRUD endpoints for this entity in NestJS.”
- “Split this monolithic module into smaller ones.”
- “Standardize how controllers and services are structured.”
- “Add a `billing` module with clear service APIs and controllers.”

Avoid this skill when:

- Only routing (Next.js) is being changed (that’s frontend).
- Only database entities or migrations are being touched.
- Only auth, JWT, guards are being worked on → use auth-focused skill.

---

## Default Conventions

Unless the project or `CLAUDE.md` specifies otherwise, assume:

- Feature modules live under `src/modules/<feature>/`.
- Each feature module contains at least:

  ```text
  src/modules/user/
    user.module.ts
    user.service.ts
    user.controller.ts
    dto/
      create-user.dto.ts
      update-user.dto.ts
    entities/          # if using TypeORM in same folder (or under domain layer)
      user.entity.ts
  ```

- Naming is singular for module & service (`UserModule`, `UserService`), plural for controller route path (`/users`).

- Controllers expose HTTP endpoints via `@Controller('users')` for REST by default.
- Services are injectable, stateless, and DI-friendly.

---

## High-Level Architecture Principles

When designing modules/services/controllers, follow these principles:

1. **Feature-first organization**
   - Group by domain feature (users, auth, billing, orders), not by technical layer only.
   - Each module should encapsulate its own controllers, services, and DTOs.

2. **Separation of concerns**
   - Controllers:
     - Handle HTTP specifics (params, query, body, response codes).
     - Call services and map results to HTTP responses.
   - Services:
     - Contain business logic, orchestration, and integration with repositories/other services.
     - Should **not** be aware of HTTP specifics.
   - Repositories / persistence:
     - Encapsulate DB access (TypeORM, Supabase, etc.).
     - Can be separate injectable providers or TypeORM repositories.

3. **Dependency injection & modularity**
   - Declare providers (services, repositories) in `providers` array of the module.
   - Export providers from a module only when they need to be used by other modules.
   - Avoid circular dependencies; if needed, consider interfaces or refactoring modules.

4. **DTOs & validation**
   - Use DTOs to define external API shapes (input/output).
   - Decorate DTOs with `class-validator` decorators (if validation is set up).
   - Avoid using entities directly as request DTOs.

5. **Consistent API patterns**
   - Use RESTful naming for controllers:
     - `GET /users`, `GET /users/:id`, `POST /users`, `PATCH /users/:id`, `DELETE /users/:id`.
   - Use HTTP status codes appropriately:
     - `201 Created` on successful creation.
     - `200 OK` for reads, updates that return actual data.
     - `204 No Content` for deletions when no body is returned.
   - Handle errors with Nest exceptions (`NotFoundException`, `BadRequestException`, etc.).

---

## Step-by-Step Workflow

When this skill is active, follow these steps:

### 1. Identify or define the feature

- Determine the **feature name** (e.g. `User`, `Auth`, `Post`, `Order`).
- Determine what operations are needed:
  - CRUD?
  - Search/filter?
  - Domain-specific actions (e.g. “activate user”, “cancel order”)?
- Determine how it fits into existing architecture:
  - Does it depend on other modules?
  - Will other modules depend on it?

### 2. Create the module structure

- Under `src/modules/<feature>/`, create:
  - `<feature>.module.ts`
  - `<feature>.service.ts`
  - `<feature>.controller.ts`
  - `dto/` and optionally `entities/` or other subfolders.

Example module file outline:

```ts
// src/modules/user/user.module.ts
import { Module } from "@nestjs/common";
import { UserService } from "./user.service";
import { UserController } from "./user.controller";

@Module({
  imports: [], // add other modules needed
  controllers: [UserController],
  providers: [UserService],
  exports: [UserService], // export only if other modules need this service
})
export class UserModule {}
```

### 3. Design the service API

- Start from **use-cases** (business operations), not raw DB operations.
- Define methods such as:

  ```ts
  // src/modules/user/user.service.ts
  import { Injectable } from "@nestjs/common";

  @Injectable()
  export class UserService {
    async create(dto: CreateUserDto) {
      // TODO: implement create logic
    }

    async findAll(options?: ListUsersOptions) {
      // TODO: implement listing logic
    }

    async findOne(id: string) {
      // TODO: implement single lookup
    }

    async update(id: string, dto: UpdateUserDto) {
      // TODO: implement update logic
    }

    async remove(id: string) {
      // TODO: implement delete logic
    }
  }
  ```

- Keep this layer free of HTTP-specific concerns.

### 4. Define DTOs

- Create `dto` folder and DTO classes/types:

  ```ts
  // src/modules/user/dto/create-user.dto.ts
  import { IsEmail, IsString, MinLength } from "class-validator";

  export class CreateUserDto {
    @IsEmail()
    email!: string;

    @IsString()
    @MinLength(8)
    password!: string;

    @IsString()
    name!: string;
  }
  ```

- Similarly, `UpdateUserDto` (typically with partials) and query/filter DTOs.
- This skill should ensure DTOs follow any validation rules set up in the project (e.g. using `ValidationPipe`).

### 5. Implement controller(s)

- Map HTTP verbs and paths to service methods:

  ```ts
  // src/modules/user/user.controller.ts
  import {
    Body,
    Controller,
    Delete,
    Get,
    Param,
    Patch,
    Post,
  } from "@nestjs/common";
  import { UserService } from "./user.service";
  import { CreateUserDto } from "./dto/create-user.dto";
  import { UpdateUserDto } from "./dto/update-user.dto";

  @Controller("users")
  export class UserController {
    constructor(private readonly userService: UserService) {}

    @Post()
    create(@Body() dto: CreateUserDto) {
      return this.userService.create(dto);
    }

    @Get()
    findAll() {
      return this.userService.findAll();
    }

    @Get(":id")
    findOne(@Param("id") id: string) {
      return this.userService.findOne(id);
    }

    @Patch(":id")
    update(@Param("id") id: string, @Body() dto: UpdateUserDto) {
      return this.userService.update(id, dto);
    }

    @Delete(":id")
    remove(@Param("id") id: string) {
      return this.userService.remove(id);
    }
  }
  ```

- This skill should also:
  - Add route-level decorators for auth, roles, etc., when combined with `nestjs-authentication` skill.
  - Use Nest’s parameter decorators for route params, queries, bodies, etc.

### 6. Wire module into the application

- Register modules in `AppModule` or a root module:

  ```ts
  // src/app.module.ts
  import { Module } from "@nestjs/common";
  import { UserModule } from "./modules/user/user.module";

  @Module({
    imports: [UserModule /*, other modules */],
  })
  export class AppModule {}
  ```

- For monorepo or large apps, consider feature root modules (e.g. `ApiModule`) grouping submodules.

### 7. Refactor messy code into modules

When refactoring:

- Identify “god modules” that contain many unrelated features.
- Split into smaller feature modules:
  - Move controllers, services, DTOs into their own `src/modules/<feature>/` subfolders.
  - Update imports and `AppModule` configuration.
- Ensure DI remains correct:
  - Move providers into their new modules.
  - Export providers from modules only when needed.

### 8. Keep testability in mind

- Structure services so they can be tested with mocks (e.g. mock repositories).
- Avoid static methods and global singletons in services.
- Controllers should depend only on service interfaces or concrete services, not DB clients directly.

---

## Advanced Options (Optional but Supported)

This skill can also support:

- **Multiple controllers per module** (e.g. public vs admin controllers).
- **Sub-modules** inside a feature folder (e.g. splitting read vs write API contracts).
- **CQRS pattern** (commands/queries) if the project or `CLAUDE.md` prefers it:
  - Register command/handler pairs and query/handler pairs.
- **GraphQL** controllers/resolvers if the project uses `@nestjs/graphql`. In that case:
  - Controllers may be replaced or complemented by resolvers.

This skill should adapt based on existing project conventions.

---

## Example Prompts That Should Use This Skill

- “Generate a `users` module with CRUD endpoints and DTOs.”
- “Split this `app` module into distinct `users`, `posts`, and `comments` modules.”
- “Create a `billing` module with a service and controller skeleton.”
- “Refactor existing services/controllers to follow best practice layering.”
- “Add DTOs and proper method signatures for this existing module.”

For these tasks, rely on this skill to design and organize NestJS modules, services, and controllers,
while leaving ORM-specific details, auth logic, and project-level scaffolding to their dedicated skills.
