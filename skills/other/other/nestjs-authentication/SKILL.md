---
name: "nestjs-authentication"
description: "Use this skill whenever the user wants to design, implement, or refactor authentication and authorization in a NestJS TypeScript backend, including JWT, sessions, refresh tokens, guards, roles/permissions, and integration with modules/services/controllers."
---

# NestJS Authentication Skill

## Purpose

You are a specialized assistant for **authentication and authorization in NestJS**.

Use this skill to:

- Set up or refactor **auth modules** in a NestJS project
- Implement **local/email-password login**, **signup**, **logout**
- Implement **JWT** access tokens (and optionally refresh tokens)
- Implement **guards**, **decorators**, and **strategies** for:
  - Authenticated routes
  - Role-based access control (RBAC)
  - Permissions/claims-based access
- Integrate auth into **controllers**, **services**, and other modules
- Secure API endpoints and keep secrets & tokens handled correctly
- Integrate with external identity providers (OAuth / OpenID) at a high level (patterns, not provider-specific SDKs)

Do **not** use this skill for:

- Project creation/scaffolding → use `nestjs-project-scaffold`
- Non-NestJS frameworks (e.g. Hono, Express-only backends)
- Low-level database/ORM work (entities & migrations) → use TypeORM-specific skills

If `CLAUDE.md` exists, follow its preferences about auth style (JWT vs sessions, OAuth providers, password storage rules, etc.).

---

## When To Apply This Skill

Trigger this skill when the user asks for things like:

- “Add auth to this NestJS API.”
- “Create login/signup/logout endpoints in Nest.”
- “Protect these routes with JWT auth.”
- “Implement role-based access (admin/user) using guards.”
- “Add refresh tokens to our NestJS auth.”
- “Refactor this messy Nest auth module into something clean.”

Avoid when:

- Only implementing domain logic unrelated to auth.
- Only exposing a public, unauthenticated endpoint.

---

## Default Auth Approach (Configurable)

By default, this skill prefers:

- **Stateless JWT** access tokens for API auth
- Optional **refresh tokens** to renew access
- `@nestjs/passport` + `passport-jwt` (or equivalent) strategies
- Password hashing with **bcrypt** (or argon2 if project prefers)
- Role-based access via custom decorators and guards

Adjust based on project constraints (e.g. session cookies, API gateway, external IdP).

---

## Suggested Module Structure

By convention, an auth module is structured like:

```text
src/modules/auth/
  auth.module.ts
  auth.service.ts
  auth.controller.ts
  strategies/
    jwt.strategy.ts
    local.strategy.ts       # optional
  guards/
    jwt-auth.guard.ts
    roles.guard.ts
  dto/
    login.dto.ts
    signup.dto.ts
  decorators/
    current-user.decorator.ts
    roles.decorator.ts
```

User-facing data (e.g. `User` entity, user repository) typically lives in a `users` module
and is injected into `AuthService` when needed.

---

## High-Level Workflow

When this skill is active, follow these steps:

### 1. Confirm or create an `AuthModule`

- If an `AuthModule` already exists:
  - Inspect its structure and see if it aligns with the conventions above.
  - Plan refactor steps if it is tangled or non-idiomatic.
- If no `AuthModule` exists:
  - Create `src/modules/auth/auth.module.ts`, `auth.service.ts`, `auth.controller.ts`, `dto/`, `guards/`, `strategies/`, `decorators/`.

Example minimal `AuthModule` outline:

```ts
import { Module } from "@nestjs/common";
import { JwtModule } from "@nestjs/jwt";
import { PassportModule } from "@nestjs/passport";
import { AuthService } from "./auth.service";
import { AuthController } from "./auth.controller";
import { JwtStrategy } from "./strategies/jwt.strategy";
import { UsersModule } from "../user/user.module";

@Module({
  imports: [
    UsersModule,
    PassportModule,
    JwtModule.register({}), // config via ConfigModule or env
  ],
  controllers: [AuthController],
  providers: [AuthService, JwtStrategy],
  exports: [AuthService],
})
export class AuthModule {}
```

Use ConfigModule for secrets/expiry settings rather than hardcoding values.

### 2. Environment & Config

- Ensure environment variables for JWT:

  ```env
  JWT_ACCESS_SECRET=super-secret-key
  JWT_ACCESS_EXPIRES_IN=15m
  JWT_REFRESH_SECRET=another-super-secret-key
  JWT_REFRESH_EXPIRES_IN=7d
  ```

- Create a config file (e.g. `src/config/auth.config.ts`) if project uses modular config:

  ```ts
  export default () => ({
    auth: {
      jwtAccessSecret: process.env.JWT_ACCESS_SECRET,
      jwtAccessExpiresIn: process.env.JWT_ACCESS_EXPIRES_IN ?? "15m",
      jwtRefreshSecret: process.env.JWT_REFRESH_SECRET,
      jwtRefreshExpiresIn: process.env.JWT_REFRESH_EXPIRES_IN ?? "7d",
    },
  });
  ```

- Use `ConfigService` inside `AuthModule`/JwtModule registration.

### 3. AuthService Responsibilities

Design `AuthService` to handle:

- Validating credentials (delegating to `UsersService` and password hashing)
- Issuing tokens (access & refresh)
- Refreshing tokens (if implemented)
- High-level auth flows (`login`, `signup`, `logout`, etc.)

Example outline:

```ts
// src/modules/auth/auth.service.ts
import { Injectable, UnauthorizedException } from "@nestjs/common";
import { JwtService } from "@nestjs/jwt";
import * as bcrypt from "bcrypt";
import { UsersService } from "../user/user.service";
import { User } from "../user/entities/user.entity";

@Injectable()
export class AuthService {
  constructor(
    private readonly usersService: UsersService,
    private readonly jwtService: JwtService,
  ) {}

  async validateUser(email: string, password: string): Promise<User | null> {
    const user = await this.usersService.findByEmail(email);
    if (!user) return null;

    const passwordValid = await bcrypt.compare(password, user.passwordHash);
    if (!passwordValid) return null;

    return user;
  }

  async createAccessToken(user: User) {
    const payload = { sub: user.id, email: user.email, roles: user.roles };
    return this.jwtService.signAsync(payload);
  }

  async createAuthTokens(user: User) {
    // Optionally create refresh tokens here too
    const accessToken = await this.createAccessToken(user);
    return { accessToken };
  }
}
```

### 4. Strategies & Guards

Implement JWT strategy:

```ts
// src/modules/auth/strategies/jwt.strategy.ts
import { Injectable } from "@nestjs/common";
import { PassportStrategy } from "@nestjs/passport";
import { ExtractJwt, Strategy } from "passport-jwt";
import { ConfigService } from "@nestjs/config";

@Injectable()
export class JwtStrategy extends PassportStrategy(Strategy) {
  constructor(configService: ConfigService) {
    super({
      jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
      ignoreExpiration: false,
      secretOrKey: configService.get<string>("auth.jwtAccessSecret"),
    });
  }

  async validate(payload: any) {
    // Attach to request.user
    return {
      userId: payload.sub,
      email: payload.email,
      roles: payload.roles,
    };
  }
}
```

JWT auth guard:

```ts
// src/modules/auth/guards/jwt-auth.guard.ts
import { Injectable } from "@nestjs/common";
import { AuthGuard } from "@nestjs/passport";

@Injectable()
export class JwtAuthGuard extends AuthGuard("jwt") {}
```

Roles decorator & guard (for RBAC):

```ts
// src/modules/auth/decorators/roles.decorator.ts
import { SetMetadata } from "@nestjs/common";

export const ROLES_KEY = "roles";
export const Roles = (...roles: string[]) => SetMetadata(ROLES_KEY, roles);
```

```ts
// src/modules/auth/guards/roles.guard.ts
import {
  CanActivate,
  ExecutionContext,
  Injectable,
} from "@nestjs/common";
import { Reflector } from "@nestjs/core";
import { ROLES_KEY } from "../decorators/roles.decorator";

@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const requiredRoles = this.reflector.getAllAndOverride<string[]>(ROLES_KEY, [
      context.getHandler(),
      context.getClass(),
    ]);
    if (!requiredRoles || requiredRoles.length === 0) return true;

    const { user } = context.switchToHttp().getRequest();
    if (!user || !user.roles) return false;

    return requiredRoles.some((role) => user.roles.includes(role));
  }
}
```

### 5. AuthController

Expose login/signup endpoints via a controller:

```ts
// src/modules/auth/auth.controller.ts
import { Body, Controller, Post, UseGuards } from "@nestjs/common";
import { AuthService } from "./auth.service";
import { LoginDto } from "./dto/login.dto";

@Controller("auth")
export class AuthController {
  constructor(private readonly authService: AuthService) {}

  @Post("login")
  async login(@Body() dto: LoginDto) {
    const user = await this.authService.validateUser(dto.email, dto.password);
    if (!user) {
      // throw UnauthorizedException here or inside AuthService
      throw new UnauthorizedException("Invalid credentials");
    }
    return this.authService.createAuthTokens(user);
  }

  // signup, refresh, logout endpoints can be added similarly
}
```

For more advanced setups:

- Use local strategy (`passport-local`) for form login flows.
- Use refresh token endpoints that validate refresh tokens and issue new access tokens.

### 6. Securing Routes in Other Modules

Use guards and decorators in other modules’ controllers:

```ts
// src/modules/user/user.controller.ts
import { Controller, Get, UseGuards } from "@nestjs/common";
import { JwtAuthGuard } from "../auth/guards/jwt-auth.guard";
import { Roles } from "../auth/decorators/roles.decorator";
import { RolesGuard } from "../auth/guards/roles.guard";

@Controller("users")
@UseGuards(JwtAuthGuard, RolesGuard)
export class UserController {
  @Get("me")
  @Roles("user", "admin")
  getMe() {
    // controller logic
  }
}
```

This skill should:

- Help apply guards correctly at class or method level.
- Avoid overcomplicated configs when simple solutions suffice.

### 7. Password Handling

Best practices enforced by this skill:

- Always hash passwords using bcrypt or argon2 before storage.
- Never log or return password hashes in responses.
- Use environment-based salt rounds or parameters when needed.

### 8. Integrating with Other Skills

- **nestjs-modules-services-controllers**:
  - This skill uses module/service/controller structure created by that skill.
- **nestjs-typeorm-integration**:
  - User entities, user repositories, and DB schema belong there; this skill coordinates with it for auth needs.
- **nestjs-testing-skill**:
  - Tests for auth flows (login, token validation, guards) can be added via that skill.

---

## Advanced Topics (Optional)

This skill can also support:

- **Session-based auth** using cookies and server-side sessions (instead of or alongside JWT).
- **OAuth/OIDC** integrations (Google, GitHub, etc.):
  - Using Passport strategies and OAuth callbacks.
  - Storing user identities from external providers.
- **API gateway / microservices integration**:
  - Using JWTs to authenticate requests across services.
  - Extracting auth logic into a dedicated auth service in a microservice architecture.

These should be applied when the project explicitly requires them.

---

## Example Prompts That Should Use This Skill

- “Implement JWT login and protect `/admin` routes in this NestJS app.”
- “Add signup, login, and me endpoints to this NestJS project.”
- “Refactor our existing auth module to use guards and decorators cleanly.”
- “Add role-based access control (user/admin) to our controllers.”
- “Implement refresh tokens and secure them properly.”

For such prompts, rely on this skill to provide **secure, idiomatic NestJS auth structures**,
keeping concerns separated between tokens, guards, controllers, and user data access.
