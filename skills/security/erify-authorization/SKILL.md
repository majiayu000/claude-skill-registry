---
name: erify-authorization
description: Patterns for implementing role-based authorization in erify_api with JSONB roles/permissions, AdminGuard, and multi-scope access control
---

# erify_api Authorization Patterns

This skill provides **erify_api-specific** authorization implementation patterns, including role-based access control with JSONB storage, AdminGuard implementation, and multi-scope permissions.

**For general authentication/authorization principles, see**:
- `authentication-authorization-nestjs` - Comprehensive auth patterns
- `backend-controller-pattern-nestjs` - Controller patterns with auth decorators

## When to Use This Skill

- Implementing new admin endpoints with permission requirements
- Adding role-based access control to controllers
- Designing multi-scope access patterns (studio, client, system-wide)
- Troubleshooting permission denied errors
- Extending the permission system with new roles or permissions

## Core Principles

### 1. Separation of Concerns

**Authentication** (`eridu_auth`): Handles user identity and JWT issuance  
**Authorization** (`erify_api`): Handles permissions and access control

> **IMPORTANT**: Never add authorization claims to JWT payload. Keep JWTs minimal with identity claims only.

### 2. Multi-Scope Access

Different user types have different access scopes:

| User Type | Access Scope | Implementation |
|-----------|-------------|----------------|
| MC | Own shows only | Via `ShowMC` relationship |
| Studio Operator | Studio's rooms | Via `StudioMembership` |
| Content Manager | Specific clients | Via `roles` + client filtering |
| System Manager | All data | Via `roles: ["system_manager"]` |
| Read-only Admin | View-only | Via `roles: ["analyst"]` |

### 3. Role-Based Permissions

Use roles for permission bundles, custom permissions for edge cases.

## Permission Model

### Database Schema

```prisma
model User {
  isSystemAdmin  Boolean  @default(false)  // Full access bypass
  roles          Json     @default("[]")   // ["content_manager", "analyst"]
  permissions    Json     @default("[]")   // ["users:read", "custom:feature"]
}
```

**Storage**: JSONB in PostgreSQL (Prisma `Json` type)

**Why JSONB**:
- Indexable with GIN for fast queries
- Type-safe (Prisma parses to `string[]`)
- Supports JSONB containment operators

### Permission Format

Use `module:action` format:
- `users:read`, `users:write`
- `shows:read`, `shows:write`
- `reports:read`, `reports:export`

### Role Definitions

Define roles in `AdminGuard` or shared constants:

```typescript
const ROLE_PERMISSIONS: Record<string, string[]> = {
  content_manager: ['shows:read', 'shows:write', 'schedules:read', 'schedules:write'],
  analyst: ['users:read', 'shows:read', 'reports:read'],
  support: ['users:read', 'tickets:read', 'tickets:write'],
  system_manager: ['*:*'], // All permissions
};
```

### Effective Permissions

Effective permissions = Role permissions + Custom permissions

**Example**:
```json
{
  "roles": ["content_manager"],
  "permissions": ["reports:export"]
}
```

**Effective**: `shows:read`, `shows:write`, `schedules:read`, `schedules:write`, `reports:export`

## Implementation Patterns

### AdminGuard Pattern

```typescript
@Injectable()
export class AdminGuard implements CanActivate {
  private readonly ROLE_PERMISSIONS: Record<string, string[]> = {
    // Define role mappings here
  };

  async canActivate(context: ExecutionContext): Promise<boolean> {
    const requiredPermissions = this.reflector.getAllAndOverride<string[]>(
      ADMIN_PERMISSIONS_KEY,
      [context.getHandler(), context.getClass()],
    ) || [];

    const request = context.switchToHttp().getRequest<AuthenticatedRequest>();
    const user = await this.userService.getUserByExtId(request.user.ext_id);

    // 1. System admin bypasses all checks
    if (user.isSystemAdmin) return true;

    // 2. Expand roles to permissions
    const userRoles = (user.roles as string[]) || [];
    const rolePermissions = userRoles.flatMap(role => this.ROLE_PERMISSIONS[role] || []);
    
    // 3. Combine with custom permissions
    const customPermissions = (user.permissions as string[]) || [];
    const effectivePermissions = [...new Set([...rolePermissions, ...customPermissions])];

    // 4. Check if user has ALL required permissions
    return requiredPermissions.every(req => effectivePermissions.includes(req));
  }
}
```

### Controller Pattern

```typescript
@Controller('admin/users')
export class AdminUserController {
  // Read-only access
  @AdminProtected('users:read')
  @Get()
  getUsers() { ... }

  // Write access
  @AdminProtected('users:write')
  @Post()
  createUser() { ... }

  // Multiple permissions required
  @AdminProtected(['users:read', 'users:write'])
  @Patch(':id')
  updateUser() { ... }

  // System admin only (no specific permission)
  @AdminProtected()
  @Delete(':id')
  dangerousOperation() { ... }
}
```

### Frontend Integration Pattern

Expose effective permissions via `/me` endpoint:

```typescript
@Get()
async getMe(@CurrentUser() user: AuthenticatedUser) {
  const dbUser = await this.userService.getUserByExtId(user.ext_id);
  
  // Expand roles to effective permissions
  const userRoles = (dbUser?.roles as string[]) || [];
  const rolePermissions = userRoles.flatMap(role => ROLE_PERMISSIONS[role] || []);
  const customPermissions = (dbUser?.permissions as string[]) || [];
  const effectivePermissions = [...new Set([...rolePermissions, ...customPermissions])];
  
  return {
    ...user,
    isSystemAdmin: dbUser?.isSystemAdmin ?? false,
    roles: userRoles,
    permissions: effectivePermissions, // For UI permission checks
  };
}
```

## Best Practices

### ✅ DO

1. **Use roles for onboarding**: Assign `roles: ["content_manager"]` instead of 50 individual permissions
2. **Use custom permissions for edge cases**: Add specific permissions on top of roles
3. **Use granular permission strings**: `users:read`, `users:write` (not `admin:read`)
4. **Use isSystemAdmin for full access**: Bypass all permission checks
5. **Keep permission logic in backend**: Frontend uses same permission strings
6. **Document role definitions**: Keep `ROLE_PERMISSIONS` mapping well-documented
7. **Use JSONB for storage**: Enables fast queries with GIN indexes

### ❌ DON'T

1. **Don't add permissions to JWT**: Keep JWTs minimal (identity only)
2. **Don't create roles for every edge case**: Use custom permissions instead
3. **Don't use coarse permissions**: `admin:read` is too broad
4. **Don't duplicate permission logic**: Backend and frontend should use same strings
5. **Don't forget to expand roles**: Always combine role + custom permissions
6. **Don't use TEXT/CSV for storage**: JSONB is superior for queries

## Common Patterns

### Pattern 1: Read/Write Separation

```typescript
// Read endpoints
@AdminProtected('module:read')
@Get()
list() { ... }

@AdminProtected('module:read')
@Get(':id')
get() { ... }

// Write endpoints
@AdminProtected('module:write')
@Post()
create() { ... }

@AdminProtected('module:write')
@Patch(':id')
update() { ... }

@AdminProtected('module:write')
@Delete(':id')
delete() { ... }
```

### Pattern 2: Scoped Access

```typescript
// Studio-scoped access
@Get('shows')
@AdminProtected('shows:read')
async getShows(@AuthUser() user) {
  // Filter by user's studio memberships
  const studioIds = user.studioMemberships.map(m => m.studioId);
  return this.showService.findByStudioRooms(studioIds);
}

// Client-scoped access
@Get('shows')
@AdminProtected('shows:read')
async getShows(@AuthUser() user, @Query('clientId') clientId?: string) {
  // Filter by user's client memberships or roles
  const clientIds = this.getAccessibleClients(user);
  return this.showService.findByClients(clientIds);
}

// System-wide access
@Get('shows')
@AdminProtected('shows:read:all')
async getAllShows() {
  // No filtering - system manager only
  return this.showService.findAll();
}
```

### Pattern 3: Role Assignment

```typescript
// Assign role to user
await prisma.user.update({
  where: { id: userId },
  data: { roles: ['content_manager'] },
});

// Add custom permission
await prisma.user.update({
  where: { id: userId },
  data: { 
    roles: ['analyst'],
    permissions: ['reports:export'],
  },
});
```

## Troubleshooting

### Permission Denied (403)

1. Check user's `isSystemAdmin` flag
2. Check user's `roles` array
3. Check user's `permissions` array
4. Verify endpoint's `@AdminProtected()` requirements
5. Check `AdminGuard` logs for missing permissions

### Role Not Expanding

1. Verify role name matches `ROLE_PERMISSIONS` mapping
2. Check for typos in role name
3. Ensure `ROLE_PERMISSIONS` is defined consistently
4. Consider extracting to shared constants file

### Permissions Not Updating

1. Verify database update succeeded
2. Check if caching is enabled (invalidate cache)
3. Force token refresh (logout + login)
4. Check `/me` endpoint response

## Related Skills

- `authentication-authorization-nestjs` - Comprehensive auth patterns
- `backend-controller-pattern-nestjs` - Controller patterns with auth decorators
- `backend-controller-pattern-admin` - Admin controller patterns
- `data-validation` - Input validation and serialization

## Related Documentation

- [Authorization Guide](../../apps/erify_api/docs/AUTHORIZATION_GUIDE.md)
- [Authentication Guide](../../apps/erify_api/docs/AUTHENTICATION_GUIDE.md)
- [Architecture Overview](../../apps/erify_api/docs/ARCHITECTURE.md)
