---
name: prisma-rbac
description: Add, repair, and verify Prisma-backed RBAC (User, Group, Role, Permission) in existing NestJS backends with JWT access tokens, refresh-token session rotation, permission guards, and CRUD/assignment APIs. Use when users ask to implement or fix role-based access control, auth session rotation, permission-protected endpoints, or Prisma auth/authorization wiring.
---

# RBAC with Prisma

Use this skill to implement or remediate Role-Based Access Control in a NestJS backend that already uses Prisma. The target model is:

`User -> UserGroup -> Group -> GroupRole -> Role -> RolePermission -> Permission`

This skill assumes a synchronous API workflow and session-backed refresh token rotation.

## Workflow

### Step 1: Preflight checks (required)

- Prisma and PrismaService/PrismaModule are present.
- ConfigModule is available (for `JWT_SECRET`).
- Optional: `@nestjs/jwt`, `@nestjs/config`, bcrypt/bcryptjs (or project password hashing), Swagger, `crypto` (Node built-in) for secure random refresh tokens.

If any optional dependency is missing, add it or adapt (for example, use Nest `LoggerService` instead of a custom logger).

Stop and request the correct backend path if this is not an existing NestJS + Prisma project.

### Step 2: Enforce Prisma schema baseline (required)

Add RBAC models to `prisma/schema.prisma`. Full schema block is in [reference.md](reference.md).

**Models:**

- **User:** `id`, `username` (unique), `password`, `createdAt`, `updatedAt`; relation `userGroups UserGroup[]`.
- **Group:** `id`, `name` (unique), `description?`, timestamps; relations `users UserGroup[]`, `groupRoles GroupRole[]`.
- **UserGroup:** composite `@@id([userId, groupId])`; relations to User and Group with `onDelete: Cascade`; `@@map("user_groups")`.
- **Permission:** `id`, `name` (unique), `description?`, timestamps; relation `rolePermissions RolePermission[]`.
- **Role:** `id`, `name` (unique), `description?`, timestamps; relations `groupRoles GroupRole[]`, `rolePermissions RolePermission[]`.
- **RolePermission:** composite `@@id([roleId, permissionId])`; relations to Role and Permission with `onDelete: Cascade`; `@@map("role_permissions")`.
- **GroupRole:** composite `@@id([groupId, roleId])`; relations to Group and Role with `onDelete: Cascade`; `@@map("group_roles")`.

For refresh tokens, add a session model in Prisma (recommended for production):

- **AuthSession:** `id` (UUID/cuid), `userId`, `refreshTokenHash`, `expiresAt`, `revokedAt?`, `replacedById?`, `userAgent?`, `ip?`, `createdAt`, `updatedAt`.
- Indexes: `@@index([userId])`, `@@index([expiresAt])`, `@@index([revokedAt])`, and unique `refreshTokenHash` when feasible.

Do not store raw refresh tokens in Prisma; store only a one-way hash.

After schema changes, run `npx prisma migrate dev` and `npx prisma generate`.

### Step 3: Enforce token/session model (required)

Use a two-token model:

- **Access token (JWT):** short TTL (5-15 minutes), includes `sub` and optional `username`; used for API authorization.
- **Refresh token:** long TTL (7-30 days), opaque random string (recommended) or JWT with `jti`; used only at refresh endpoint.

Standardized refresh behavior:

1. `POST /auth/login` returns `accessToken` and `refreshToken` and creates a DB session with hashed refresh token.
2. `POST /auth/refresh` validates refresh token, session status (`revokedAt` is null, `expiresAt` is in the future), and user existence.
3. On success, rotate refresh token:
   - Mark old session as revoked and optionally set `replacedById`.
   - Create new session row with new `refreshTokenHash` and new expiry.
   - Return new `accessToken` and new `refreshToken`.
4. If a revoked or unknown refresh token is presented, treat as token reuse and revoke all active sessions for that user or device scope.
5. `POST /auth/logout` revokes current session.
6. Optional `POST /auth/logout-all` revokes all user sessions.

Transport standard:

- Prefer HttpOnly + Secure + SameSite cookie for refresh tokens.
- Accept header/body refresh token only for non-browser clients; do not log tokens.
- Keep access token in `Authorization: Bearer <token>`.

### Step 4: Wire module boundaries and DI (required)

Single **RbacModule** (for example, `src/libs/rbac/rbac.module.ts`):

- `@Global()` so services are available app-wide.
- **Imports:** `ConfigModule`, `JwtModule.registerAsync({ useFactory: (config: ConfigService) => ({ secret: config.get('JWT_SECRET') }), inject: [ConfigService] })`. Throw if `JWT_SECRET` is missing.
- **Providers:** AuthService, SessionService (or TokenService backed by Prisma), UserService, GroupService, RoleService, PermissionService, UserGroupsService (and optionally GroupRolesService, RolePermissionsService if mirroring full reference).
- **Exports:** same services.
- **Controllers:** AuthController, UserController, GroupController, RoleController, PermissionController.

Register RbacModule in `AppModule` imports.

### Step 5: Implement guard behavior (required)

File: `src/libs/rbac/guards/auth.guard.ts`.

1. Extract token: `AuthContextUtils.getTokenFromHeader(request)` from `Authorization: Bearer <token>`. If missing, throw `UnauthorizedException`.
2. Validate: `authService.isValidToken(token)`. If false, throw Unauthorized.
3. Session check is optional for access tokens if stateless-only, recommended if session-aware access revocation is required:
   - If session-aware: include a `sid` claim in access token and verify active session exists in DB/cache.
   - If missing or revoked, throw Unauthorized (for example, "Session not found or revoked").
4. Attach token to request (for example, `(request as AuthenticatedRequest).authToken = token`).
5. **Permission check:** Read `permissions` metadata from handler and class: `reflector.get<string[]>('permissions', context.getHandler())` then class. If `requiredPermissions.length > 0`:
   - Decode JWT to get `sub` (userId).
   - Run Prisma: count permissions where `name` is in `requiredPermissions` and the permission is reachable via: User (userId) -> UserGroup -> Group -> GroupRole -> Role -> RolePermission -> Permission. Use a single `prisma.permission.count({ where: { name: { in: requiredPermissions }, rolePermissions: { some: { role: { groupRoles: { some: { group: { users: { some: { userId } } } } } } } } } })`.
   - If count < requiredPermissions.length, throw Unauthorized ("Insufficient permissions").
6. Return true.

Inject: AuthService, SessionService (or TokenService), Reflector, JwtService, PrismaService. Use Nest LoggerService or project logger for warnings.

### Step 6: Implement auth/session services (required)

- **login(username, password):** Validate with UserService (for example, `userService.isValidUser`), fetch user, generate short-lived access JWT (payload: `{ sub: user.id, username, sid }`), generate refresh token, hash refresh token, persist session, return `{ accessToken, refreshToken }`. Throw Unauthorized on invalid credentials.
- **refresh(refreshToken):** Hash and lookup session; verify not revoked and not expired; rotate session and refresh token; return new token pair.
- **logout(refreshToken | sid):** Revoke current session.
- **logoutAll(userId):** Revoke all active sessions for user (optional but recommended).
- **generateToken(payload):** Use JwtService with secret from ConfigService.
- **isValidToken(token):** JwtService.verifyAsync with secret; ensure payload has `sub` and (if used) `username`. Return boolean.

## SessionService (or TokenService)

Prefer Prisma-backed session store over in-memory for production.

- **createSession(input):** Persist hashed refresh token, expiry, metadata.
- **findActiveByRefreshTokenHash(hash):** Return matching active session.
- **rotateSession(sessionId, newHash, newExpiry):** Revoke old + create successor session atomically.
- **revokeSession(sessionId):** Mark revoked.
- **revokeAllForUser(userId):** Revoke all active sessions for user.
- **cleanupExpired():** Optional scheduled cleanup.

If using Redis instead of Prisma, keep the same service contract and rotation semantics.

### Step 7: Add auth context helpers and interfaces (required)

- **AuthContextUtils** (for example, `src/libs/rbac/utils/auth-context.utils.ts`): Parse `Authorization` header; static `getTokenFromHeader(request)` returns token when scheme is `Bearer`, else undefined.
- **SessionInterface** (for example, `src/libs/rbac/interfaces/session.interface.ts`): include `id`, `userId`, `refreshTokenHash`, `expiresAt`, `revokedAt?`, `replacedById?`.

### Step 8: Protect routes with permissions metadata (required)

- **Guard + permissions:** `@UseGuards(AuthGuard)` and `@SetMetadata('permissions', ['resource.action'])` (for example, `['users.read']`, `['users.create']`). Guard requires user to have **all** listed permissions.
- **Composite (optional):** When Swagger is used, define `Authentication()` = `applyDecorators(UseGuards(AuthGuard), ApiBearerAuth('JWT-auth'), HttpCode(HttpStatus.OK))` and use `@Authentication()` on protected routes.

### Step 9: Align DTOs and controllers (required)

**DTOs:** Create/patch/get/delete per entity. Examples:

- CreateUserDto: username, password (and validation).
- GetUserDto: id, username, createdAt (no password).
- PatchUserDto: optional username, password.
- Replace-user-groups: body as array of group IDs; same idea for group-roles and role-permissions.

Use class-validator where applicable (`IsString`, `IsOptional`, `MinLength`, etc.). If Swagger is present, add `@ApiProperty` to DTOs.

**Controllers:**

- **Auth:** `POST login` (body: username, password; return token pair), `POST refresh` (read refresh token from cookie/header/body, rotate session), `POST logout` (revoke current refresh session), optional `POST logout-all`.
- **Users:** CRUD (list, create, get by id, patch, delete), change-password, list/replace/assign/remove user groups. Protect with AuthGuard and `@SetMetadata('permissions', ['users.read'])` etc.
- **Groups, Roles, Permissions:** CRUD plus assignment endpoints (for example, replace group roles, replace role permissions). Same guard + permissions pattern.

Use a consistent permission naming convention (for example, `users.read`, `users.create`, `users.update`, `users.delete`, `groups.assign`).

### Step 10: Enforce hashing and secret-safe logging (required)

Do not store plain passwords. Use bcrypt/bcryptjs (for example, per setup-bcryptjs-nestjs skill) or the project's existing hashing. UserService (or a dedicated service) should hash on create/patch and verify on login.

## Adaptations

- **Logger:** Reference project may use a custom logger; use Nest `LoggerService` or the project's logger in AuthGuard and AuthService.
- **Swagger:** If present, add `@ApiBearerAuth('JWT-auth')`, `@ApiOperation`, `@ApiResponse` on auth and protected endpoints; optional `Responses(kind)` decorator for common status codes. Document refresh cookie/header contract explicitly. If Swagger is not used, omit these.
- **Encryption package:** If the reference uses a specific encryption package, prefer bcrypt/bcryptjs for new backends unless the project already has a standard.
- **Refresh token hashing:** Prefer SHA-256/SHA-512 with per-token random value, or HMAC keyed by server secret; never store plaintext refresh tokens.

### Step 11: Verification gates (required)

- Build/test passes for the backend after RBAC changes.
- Prisma migration and client generation succeed.
- Login returns access+refresh token pair.
- Refresh rotates sessions and invalidates/revokes replaced refresh sessions.
- Protected routes enforce required permissions and deny insufficient scopes.
- No plaintext passwords or refresh tokens are persisted or logged.

## Checklist

- [ ] Prisma schema has User, Group, Role, Permission, UserGroup, GroupRole, RolePermission; migrations run.
- [ ] AuthSession (or equivalent session store) exists for hashed refresh tokens and rotation.
- [ ] JWT_SECRET in env; JwtModule registered in RbacModule.
- [ ] Access token TTL and refresh token TTL configured (env-driven).
- [ ] AuthService, SessionService (or TokenService), UserService, GroupService, RoleService, PermissionService, UserGroupsService (and optional GroupRolesService, RolePermissionsService) implemented.
- [ ] AuthGuard: token extraction, validation, permission count via Prisma, and optional session-aware access-token revocation.
- [ ] Refresh endpoint rotates refresh token on every use and handles reuse detection.
- [ ] AuthContextUtils.getTokenFromHeader and SessionInterface in place.
- [ ] AuthController (login, refresh, logout, optional logout-all); User, Group, Role, Permission controllers with CRUD and assignments; routes protected with AuthGuard and SetMetadata('permissions', [...]).
- [ ] Passwords hashed; no plain-text storage.
- [ ] Refresh tokens are hashed, never logged, and delivered via secure transport.

For full schema details, see [reference.md](reference.md).

## Official References

1. NestJS Authentication: https://docs.nestjs.com/security/authentication
2. NestJS Authorization: https://docs.nestjs.com/security/authorization
3. NestJS Guards: https://docs.nestjs.com/guards
4. Prisma Data Model: https://www.prisma.io/docs/orm/prisma-schema/data-model/models
5. Prisma Migrate: https://www.prisma.io/docs/orm/prisma-migrate

