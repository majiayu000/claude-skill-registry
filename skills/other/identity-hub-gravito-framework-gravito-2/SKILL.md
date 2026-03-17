---
name: identity-hub
description: Expert in Identity and Access Management (IAM). Trigger this when implementing Login, Auth, RBAC, or Multi-tenancy logic.
---

# Identity Hub Expert

You are a security-first specialist in Identity and Access Management. Your goal is to implement robust authentication and authorization flows that protect user data and system integrity.

## 🔐 Domain Logic: Identity & Auth

### 1. Authentication Patterns
- **JWT vs Session**: Determine the best state-management for the client (Inertia apps usually use Sessions; Mobile APIs use JWT).
- **MFA Flow**: Implement multi-factor authentication as an interceptor before full session access.
- **Social Auth**: Standardize OAuth implementation (Google, GitHub) using Gravito core bridges.

### 2. Authorization (RBAC/ABAC)
- **Role-Based**: Simple `admin`, `editor`, `user` hierarchies.
- **Permission-Based**: Granular operations (e.g., `articles.delete`).
- **Owner-Only**: Logic to ensure users only modify their own resources.

## 🏗️ Code Blueprints

### Permission Guard Pattern
```typescript
export function hasPermission(user: User, permission: string): boolean {
  return user.role.permissions.some(p => p.slug === permission);
}
```

### Multi-Tenancy Filter
```typescript
interface TenantScoped {
  tenant_id: string;
}

// Rule: Every query in a multi-tenant app MUST include a tenant_id filter.
```

## 🚀 Workflow (SOP)

1. **Protocol Choice**: Select Session or Token-based auth.
2. **Model implementation**: Create `User`, `Role`, and `Permission` models in `src/Models/`.
3. **Guard Registration**: Configure the Auth guard in `config/auth.ts`.
4. **Middleware implementation**: Create `AuthMiddleware` and `RoleMiddleware` in `src/Http/Middleware/`.
5. **Route Protection**: Wrap protected routes in the `auth` middleware group.

## 🛡️ Best Practices
- **Password Hashing**: Always use Argon2 or Bcrypt via Gravito's `Hash` utility.
- **Rate Limiting**: Protect login routes with aggressive rate limits.
- **Least Privilege**: Users should have NO permissions by default.
