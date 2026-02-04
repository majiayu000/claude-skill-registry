---
name: laravel-permission
description: Spatie Laravel Permission - roles, permissions, middleware, Blade directives, teams, wildcards, super-admin, API, testing. Use when implementing RBAC, role-based access control, or user authorization.
versions:
  laravel: "12.46"
  spatie-permission: "6.24"
  php: "8.5"
user-invocable: false
references: references/spatie-permission.md, references/middleware.md, references/blade-directives.md, references/teams.md, references/wildcard-permissions.md, references/super-admin.md, references/cache.md, references/direct-permissions.md, references/artisan-commands.md, references/custom-models.md, references/events.md, references/query-scopes.md, references/policies.md, references/api-usage.md, references/testing.md, references/performance.md
related-skills: laravel-auth, laravel-api, laravel-testing
---

# Laravel Permission (Spatie)

## Agent Workflow (MANDATORY)

Before ANY implementation, launch in parallel:

1. **fuse-ai-pilot:explore-codebase** - Check existing auth patterns
2. **fuse-ai-pilot:research-expert** - Verify Spatie Permission docs via Context7
3. **mcp__context7__query-docs** - Check Laravel authorization patterns

After implementation, run **fuse-ai-pilot:sniper** for validation.

---

## Overview

Spatie Laravel Permission provides complete role-based access control (RBAC) for Laravel applications.

| Component | Purpose |
|-----------|---------|
| **Role** | Group of permissions (admin, writer) |
| **Permission** | Single ability (edit articles) |
| **Middleware** | Route protection |
| **Blade Directives** | UI authorization |
| **Teams** | Multi-tenant scoping |
| **Wildcards** | Hierarchical permissions |
| **Super Admin** | Bypass all checks |
| **Events** | Audit logging (v6.15.0+) |
| **Query Scopes** | Filter users by role/permission |
| **API Support** | Sanctum/Passport integration |
| **Policies** | Resource-based authorization |

---

## Critical Rules

1. **Seed roles/permissions** in `DatabaseSeeder`
2. **Cache reset** after changes: `php artisan permission:cache-reset`
3. **Use kebab-case** for naming: `edit-articles`
4. **Never hardcode** role checks in controllers - use middleware
5. **Set team context** early in request for multi-tenant apps
6. **Specify guard for API** - `permission:edit,api`
7. **Clear cache in tests** - Reset in setUp()/beforeEach()

---

## Reference Guide

### Core Concepts

| Topic | Reference | When to consult |
|-------|-----------|-----------------|
| **Setup** | [spatie-permission.md](references/spatie-permission.md) | Installation, model setup, core methods |
| **Middleware** | [middleware.md](references/middleware.md) | Route protection patterns |
| **Blade** | [blade-directives.md](references/blade-directives.md) | UI authorization directives |
| **Direct vs Role** | [direct-permissions.md](references/direct-permissions.md) | Permission inheritance |

### Advanced Features

| Topic | Reference | When to consult |
|-------|-----------|-----------------|
| **Teams** | [teams.md](references/teams.md) | Multi-tenant permissions |
| **Wildcards** | [wildcard-permissions.md](references/wildcard-permissions.md) | Hierarchical patterns |
| **Super Admin** | [super-admin.md](references/super-admin.md) | Bypass all permissions |
| **Custom Models** | [custom-models.md](references/custom-models.md) | UUID, extending models |

### Integration

| Topic | Reference | When to consult |
|-------|-----------|-----------------|
| **API Usage** | [api-usage.md](references/api-usage.md) | Sanctum, guards, JSON responses |
| **Policies** | [policies.md](references/policies.md) | Laravel Policy integration |
| **Query Scopes** | [query-scopes.md](references/query-scopes.md) | `User::role()`, `User::permission()` |
| **Events** | [events.md](references/events.md) | Audit logging, notifications |

### Operations & Quality

| Topic | Reference | When to consult |
|-------|-----------|-----------------|
| **Cache** | [cache.md](references/cache.md) | Performance, debugging |
| **CLI** | [artisan-commands.md](references/artisan-commands.md) | Artisan commands |
| **Testing** | [testing.md](references/testing.md) | Tests, factories, setup |
| **Performance** | [performance.md](references/performance.md) | Optimization, N+1, caching |

---

### Templates (Code Examples)

#### Setup & Seeding
| Template | Purpose |
|----------|---------|
| [UserModel.php.md](references/templates/UserModel.php.md) | User model with HasRoles trait |
| [RoleSeeder.php.md](references/templates/RoleSeeder.php.md) | Basic role seeding |
| [PermissionSeeder.php.md](references/templates/PermissionSeeder.php.md) | Permission creation seeder |
| [WildcardSeeder.php.md](references/templates/WildcardSeeder.php.md) | Hierarchical permissions |

#### Routes & Middleware
| Template | Purpose |
|----------|---------|
| [routes-example.md](references/templates/routes-example.md) | Protected routes examples |
| [ControllerMiddleware.php.md](references/templates/ControllerMiddleware.php.md) | Middleware in controllers |
| [BladeExamples.blade.md](references/templates/BladeExamples.blade.md) | Blade directive examples |

#### Teams & Multi-Tenant
| Template | Purpose |
|----------|---------|
| [TeamMiddleware.php.md](references/templates/TeamMiddleware.php.md) | Multi-tenant middleware |
| [TeamSeeder.php.md](references/templates/TeamSeeder.php.md) | Team-scoped roles seeder |
| [TeamModel.php.md](references/templates/TeamModel.php.md) | Team model with boot |

#### Super Admin & Cache
| Template | Purpose |
|----------|---------|
| [SuperAdminSetup.php.md](references/templates/SuperAdminSetup.php.md) | Gate::before bypass |
| [CacheConfig.php.md](references/templates/CacheConfig.php.md) | Cache configuration |
| [DeployScript.sh.md](references/templates/DeployScript.sh.md) | CI/CD cache management |

#### API Integration
| Template | Purpose |
|----------|---------|
| [ApiPermissionSetup.php.md](references/templates/ApiPermissionSetup.php.md) | API guard + Sanctum |
| [ApiExceptionHandler.php.md](references/templates/ApiExceptionHandler.php.md) | JSON error responses |
| [ApiUserResource.php.md](references/templates/ApiUserResource.php.md) | User resource with permissions |

#### Policies & Events
| Template | Purpose |
|----------|---------|
| [PostPolicy.php.md](references/templates/PostPolicy.php.md) | Policy with Spatie integration |
| [PermissionEventListener.php.md](references/templates/PermissionEventListener.php.md) | Audit event listeners |
| [UserQueryExamples.php.md](references/templates/UserQueryExamples.php.md) | Query scope examples |
| [PermissionAudit.php.md](references/templates/PermissionAudit.php.md) | Audit service |

#### Testing
| Template | Purpose |
|----------|---------|
| [PermissionTest.php.md](references/templates/PermissionTest.php.md) | Pest & PHPUnit tests |
| [UserFactory.php.md](references/templates/UserFactory.php.md) | Factory with permission states |

#### Custom Models
| Template | Purpose |
|----------|---------|
| [CustomRole.php.md](references/templates/CustomRole.php.md) | Extended Role model |
| [CustomPermission.php.md](references/templates/CustomPermission.php.md) | Extended Permission model |
| [UUIDMigration.php.md](references/templates/UUIDMigration.php.md) | UUID tables migration |
| [SetupPermissions.php.md](references/templates/SetupPermissions.php.md) | Custom artisan command |

---

## Quick Reference

### Assign Role
```php
$user->assignRole('admin');
```

### Check Permission
```php
$user->can('edit articles');
```

### Middleware (Web)
```php
Route::middleware(['role:admin'])->group(fn () => ...);
```

### Middleware (API)
```php
Route::middleware(['auth:sanctum', 'permission:edit,api'])->group(fn () => ...);
```

### Blade
```blade
@role('admin') ... @endrole
@can('edit articles') ... @endcan
```

### Query Scopes
```php
User::role('admin')->get();
User::permission('edit articles')->get();
```

### Teams
```php
setPermissionsTeamId($team->id);
```

### Wildcards
```php
$role->givePermissionTo('articles.*');
```

### Super Admin
```php
Gate::before(fn ($user, $ability) =>
    $user->hasRole('Super-Admin') ? true : null
);
```

### Testing
```php
beforeEach(fn () => app(PermissionRegistrar::class)->forgetCachedPermissions());
```

---

## Feature Matrix

| Feature | Status | Reference |
|---------|--------|-----------|
| Basic RBAC | ✅ | spatie-permission.md |
| Middleware | ✅ | middleware.md |
| Blade Directives | ✅ | blade-directives.md |
| Multi-Guard (web/api) | ✅ | middleware.md, api-usage.md |
| Teams (Multi-Tenant) | ✅ | teams.md |
| Wildcard Permissions | ✅ | wildcard-permissions.md |
| Super Admin | ✅ | super-admin.md |
| Cache Management | ✅ | cache.md |
| Direct vs Role Perms | ✅ | direct-permissions.md |
| Artisan Commands | ✅ | artisan-commands.md |
| UUID Support | ✅ | custom-models.md |
| Custom Models | ✅ | custom-models.md |
| Events (v6.15.0+) | ✅ | events.md |
| Query Scopes | ✅ | query-scopes.md |
| Policy Integration | ✅ | policies.md |
| API / Sanctum | ✅ | api-usage.md |
| Testing | ✅ | testing.md |
| Performance | ✅ | performance.md |
