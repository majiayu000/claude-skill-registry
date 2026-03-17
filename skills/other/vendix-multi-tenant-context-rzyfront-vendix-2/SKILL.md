---
name: vendix-multi-tenant-context
description: >
  Explains the 'Context Bridge' pattern where Middleware resolves the tenant (domain/store), stores it in the Request object, and an Interceptor unifies it with user authentication into AsyncLocalStorage.
license: Apache-2.0
metadata:
  author: Vendix
  version: "1.0"
  scope: [root, backend]
  auto_invoke:
    - "Implementing multi-tenant logic"
    - "Handling store context"
    - "Fixing Forbidden/403 errors in scoped services"
allowed-tools: [Read, Edit, Write, Glob, Grep, Bash]
---

## Multi-Tenant Context Bridge

Vendix uses a **Context Bridge** pattern to manage multi-tenancy. This pattern ensures that every request has a verified `store_id` and `organization_id` available throughout the execution flow, without relying on passing parameters through every function call.

### 1. Middleware Resolution

The `DomainResolverMiddleware` is the first line of defense. It identifies the tenant based on the hostname or a specific header.

```typescript
// apps/backend/src/common/middleware/domain-resolver.middleware.ts
async use(req: Request, res: Response, next: NextFunction) {
  const hostname = this.extractHostname(req);
  const x_store_id = req.headers['x-store-id'];

  // Priority 1: x-store-id header (development/manual override)
  if (x_store_id) {
    req['domain_context'] = { store_id: Number(x_store_id) };
    return next();
  }

  // Priority 2: Hostname resolution (production)
  const domain = await this.publicDomains.resolveDomain(hostname);
  req['domain_context'] = {
    store_id: domain.store_id,
    organization_id: domain.organization_id,
  };
  next();
}
```

### 2. Request Bridging

Middleware cannot use `AsyncLocalStorage` directly if it needs to coexist with NestJS Interceptors that also manage context. Instead, it "bridges" the information by attaching it to the `Request` object.

```typescript
req["domain_context"] = { store_id, organization_id };
```

### 3. Interceptor Unification

The `RequestContextInterceptor` merges user authentication (from `req.user`) with the domain context (from `req['domain_context']`) and initializes the `AsyncLocalStorage`.

```typescript
// apps/backend/src/common/interceptors/request-context.interceptor.ts
intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
  const req = context.switchToHttp().getRequest();
  const user = req.user;
  const domain_context = req['domain_context'];

  const contextObj: RequestContext = {
    user_id: user?.id,
    organization_id: user?.organization_id || domain_context?.organization_id,
    store_id: user?.store_id || domain_context?.store_id,
    is_super_admin: roles.includes('super_admin'),
    // ...
  };

  return RequestContextService.asyncLocalStorage.run(contextObj, () => {
    return next.handle();
  });
}
```

### 4. Safe Context Service

The `RequestContextService` provides a static API to access the context. It must **never** provide static fallbacks or "mock" data if the context is missing, as this could lead to data leakage between tenants.

```typescript
// apps/backend/src/common/context/request-context.service.ts
export class RequestContextService {
  public static asyncLocalStorage = new AsyncLocalStorage<RequestContext>();

  static getContext(): RequestContext | undefined {
    return this.asyncLocalStorage.getStore();
  }

  static getStoreId(): number | undefined {
    return this.getContext()?.store_id;
  }
}
```

### 5. Scoped Prisma Usage

Prisma services use the `RequestContextService` to automatically filter queries by the current tenant.

```typescript
// apps/backend/src/prisma/services/ecommerce-prisma.service.ts
async findMany(args: any) {
  const store_id = RequestContextService.getStoreId();
  if (!store_id) throw new ForbiddenException('No store context found');

  return this.prisma.product.findMany({
    ...args,
    where: { ...args.where, store_id }
  });
}
```

## Troubleshooting 403 Forbidden

If you encounter a `403 Forbidden` error in a scoped service:

1. **Check Middleware:** Ensure `DomainResolverMiddleware` is applied to the route.
2. **Check Interceptor:** Ensure `RequestContextInterceptor` is active (usually global).
3. **Verify Header:** If testing via API, ensure `x-store-id` is sent or the `Host` header matches a registered domain.
4. **Context Presence:** Use `RequestContextService.getContext()` to debug if the store is being resolved correctly.
