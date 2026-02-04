---
name: "nestjs-validation-and-pipes"
description: "Use this skill whenever the user wants to add, refine, or enforce request/response validation, transformation, and sanitization in a NestJS TypeScript backend using Pipes (e.g., ValidationPipe), DTOs, and custom pipes."
---

# NestJS Validation & Pipes Skill

## Purpose

You are a specialized assistant for **data validation, transformation, and sanitization** in NestJS
applications using **Pipes** and **DTOs**.

Use this skill to:

- Set up and configure **global validation** using `ValidationPipe`
- Design and maintain **DTOs** with `class-validator` and `class-transformer`
- Implement **custom pipes** for parsing, coercion, normalization, and security
- Enforce strict request payload shapes and reject invalid data
- Normalize query params, route params, and headers
- Safely transform incoming data into typed application models
- Provide consistent error responses for validation failures

Do **not** use this skill for:

- Auth logic (`nestjs-authentication`)
- Core app scaffolding (`nestjs-project-scaffold`)
- DB entity design (`nestjs-typeorm-integration`)
- Frontend form validation (this is server-side NestJS only)

If `CLAUDE.md` or existing project conventions describe DTO or validation rules, follow them.

---

## When To Apply This Skill

Trigger this skill when the user asks for:

- “Add validation to my NestJS endpoints.”
- “Make sure bad requests are rejected gracefully.”
- “Create DTOs for these request bodies.”
- “Normalize IDs from params to numbers/UUIDs.”
- “Sanitize input to prevent bad data getting into the system.”
- “Customize validation error messages.”

Avoid when:

- Only internal/domain logic is changing with no external input shape changes.
- Only frontend/Next.js validation is being discussed.

---

## Validation Philosophy

When using this skill, follow these principles:

1. **DTOs as API contracts**
   - All external inputs (body, query, params) should be represented by DTOs.
   - DTOs clearly define what is allowed and what is not.

2. **Fail fast & clearly**
   - Reject invalid input before it reaches business logic.
   - Provide structured, meaningful error responses.

3. **Separation of concerns**
   - Validation & transformation belong in pipes and DTOs.
   - Business logic in services should assume validated, typed data.

4. **Type safety ≠ validation**
   - TypeScript types are compile-time only; runtime validation needs `class-validator` + `ValidationPipe` or similar.

5. **Defense in depth**
   - Validate at boundaries even if frontend also validates.

---

## Basic Setup: Global Validation Pipe

This skill ensures global validation is enabled in `main.ts`:

```ts
// src/main.ts
import { ValidationPipe } from "@nestjs/common";
import { NestFactory } from "@nestjs/core";
import { AppModule } from "./app.module";

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  app.useGlobalPipes(
    new ValidationPipe({
      whitelist: true,
      forbidNonWhitelisted: true,
      transform: true,
      transformOptions: {
        enableImplicitConversion: true,
      },
    }),
  );

  await app.listen(process.env.PORT ?? 3000);
}
bootstrap();
```

Key options explained:

- `whitelist: true`
  - Strips unknown properties from the payload.
- `forbidNonWhitelisted: true`
  - Instead of stripping, it throws if unknown properties are present.
- `transform: true`
  - Transforms payloads into DTO class instances.
- `enableImplicitConversion: true`
  - Allows automatic type conversion based on DTO property types (e.g., strings to numbers).

This skill can adjust these based on project preferences (e.g., allowing extra fields in dev).

---

## DTO Design with class-validator & class-transformer

### Example DTO for CreateUser

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

### Example DTO for Query Params

```ts
// src/modules/user/dto/list-users.dto.ts
import { IsBoolean, IsInt, IsOptional, IsString, Min, Max } from "class-validator";
import { Type } from "class-transformer";

export class ListUsersDto {
  @IsOptional()
  @IsInt()
  @Min(1)
  @Type(() => Number)
  page?: number = 1;

  @IsOptional()
  @IsInt()
  @Min(1)
  @Max(100)
  @Type(() => Number)
  limit?: number = 20;

  @IsOptional()
  @IsString()
  search?: string;

  @IsOptional()
  @IsBoolean()
  @Type(() => Boolean)
  includeInactive?: boolean = false;
}
```

This skill should:

- Use `@Type(() => ...)` when implicit conversion is not enough or needs to be explicit.
- Define sensible defaults.
- Keep DTOs focused and reusable.

---

## Using DTOs in Controllers

This skill ensures controllers are wired to use DTOs correctly:

```ts
// src/modules/user/user.controller.ts
import { Body, Controller, Get, Post, Query } from "@nestjs/common";
import { UserService } from "./user.service";
import { CreateUserDto } from "./dto/create-user.dto";
import { ListUsersDto } from "./dto/list-users.dto";

@Controller("users")
export class UserController {
  constructor(private readonly userService: UserService) {}

  @Post()
  create(@Body() dto: CreateUserDto) {
    return this.userService.create(dto);
  }

  @Get()
  findAll(@Query() query: ListUsersDto) {
    return this.userService.findAll(query);
  }
}
```

This skill can also adapt to `@Param()` DTOs for route parameters.

---

## Custom Pipes

Use custom pipes when you need to:

- Parse IDs (UUID vs numeric)
- Coerce or sanitize strings
- Enforce custom logic like “must be one of these enums”
- Fetch entities from DB and inject them into handlers (careful with performance)

### Example: ParseIntIdPipe

```ts
import {
  ArgumentMetadata,
  BadRequestException,
  Injectable,
  PipeTransform,
} from "@nestjs/common";

@Injectable()
export class ParseIntIdPipe implements PipeTransform<string, number> {
  transform(value: string, metadata: ArgumentMetadata): number {
    const val = parseInt(value, 10);
    if (isNaN(val) || val <= 0) {
      throw new BadRequestException("Invalid ID");
    }
    return val;
  }
}
```

Use in controller:

```ts
@Get(":id")
findOne(@Param("id", ParseIntIdPipe) id: number) {
  return this.userService.findOne(id);
}
```

### Example: TrimStringPipe (simplified)

```ts
@Injectable()
export class TrimStringPipe implements PipeTransform {
  transform(value: any) {
    if (typeof value === "string") {
      return value.trim();
    }
    return value;
  }
}
```

Attach at parameter or controller level where appropriate.

This skill should:

- Suggest custom pipes when global validation is too generic.
- Avoid overusing DB-dependent pipes except in clearly beneficial scenarios.

---

## Sanitization & Security

This skill can add light sanitization strategies, such as:

- Trimming user inputs
- Limiting string lengths
- Using allowlists/enums

For more complex sanitization (XSS/HTML), it may recommend dedicated libraries and carefully placed custom pipes or service-level logic.

---

## Error Handling & Messages

This skill should help configure error responses for validation failures, e.g.:

- Using default NestJS `BadRequestException` responses from `ValidationPipe`.
- Customizing `exceptionFactory` in `ValidationPipe` to return a consistent error format:

```ts
new ValidationPipe({
  exceptionFactory: (errors) => {
    const messages = errors.map((err) => ({
      field: err.property,
      constraints: err.constraints,
    }));
    return new BadRequestException({
      message: "Validation failed",
      errors: messages,
    });
  },
});
```

It should align error formats with any global error-handling conventions or filters in the project.

---

## Pipes Scope & Application

This skill ensures pipes are applied with the correct scope:

- **Global** (via `useGlobalPipes`) for baseline validation.
- **Controller-level** when certain rules apply only to a specific resource.
- **Parameter-level** for fine-grained transformation/validation.

It should avoid applying heavy or DB-hitting pipes globally.

---

## Integration with Other Skills

- `nestjs-project-scaffold`:
  - This skill assumes global `ValidationPipe` is added in `main.ts` or will add it.
- `nestjs-modules-services-controllers`:
  - Uses DTOs and pipes alongside module/controller structures from that skill.
- `nestjs-authentication`:
  - Uses DTOs (`LoginDto`, `SignupDto`) and validates them.
- `nestjs-typeorm-integration`:
  - Ensures data reaching TypeORM entities has been validated and transformed.

---

## Advanced Topics (Optional)

This skill can also help with:

- Versioned DTOs (v1 vs v2)
- Partial DTOs using `PartialType`, `PickType`, `OmitType` from `@nestjs/mapped-types`
- GraphQL InputType validation when using `@nestjs/graphql`
- Multi-tenant or locale-aware validation if described by the project

Example using `PartialType`:

```ts
import { PartialType } from "@nestjs/mapped-types";
import { CreateUserDto } from "./create-user.dto";

export class UpdateUserDto extends PartialType(CreateUserDto) {}
```

---

## Example Prompts That Should Use This Skill

- “Add validation to these NestJS endpoints using DTOs.”
- “Create DTOs for this payload and reject invalid fields.”
- “Normalize and validate pagination query params.”
- “Implement a custom pipe to validate IDs and throw on invalid ones.”
- “Customize validation error format in our NestJS app.”

For these tasks, rely on this skill to build a **strong validation layer** that protects your NestJS backend,
keeps controllers clean, and ensures consistent request/response contracts.
