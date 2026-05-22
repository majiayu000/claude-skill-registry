---
name: frontend-angular-api-service
description: Use when creating API services for backend communication with proper patterns for caching, error handling, and type safety.
infer: true
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Angular API Service Development Workflow

Use when creating/modifying API services extending PlatformApiService for backend communication.

## Decision Tree

```
What kind of API service?
├── Standard CRUD            → extend PlatformApiService + get/post/put/deleteRequest
├── With caching             → + enableCache option in get() calls
├── File upload/download     → + postFormData() / getBlob()
├── External API             → + override getDefaultHeaders()
├── Search/autocomplete      → + debounce in component, cache short-lived
└── Validation endpoint      → return Observable<boolean>
```

## Workflow

1. **Search** existing services: `grep "{Feature}ApiService" --include="*.ts"`
2. **Read** references (see Read Directives below)
3. **Define** DTOs: request interfaces, response interfaces, command interfaces
4. **Create** service extending `PlatformApiService` with `@Injectable({ providedIn: 'root' })`
5. **Implement** `apiUrl` getter using `environment.apiUrl + '/api/{Controller}'`
6. **Add** query methods (get), command methods (post/put/delete), validation methods
7. **Verify** checklist below

## Key Rules

- Always extend `PlatformApiService` (never use `HttpClient` directly)
- Use `environment.apiUrl` for base URL (never hardcode)
- All methods must have return type annotations: `Observable<T>`
- Define DTOs for all request/response types
- Use `{ enableCache: true, cacheKey, cacheDurationMs }` for cacheable endpoints
- File uploads use `postFormData()`, downloads use `getBlob()`
- Error handling done in component via `tapResponse()`, not in service

## File Location

```
src/Frontend/libs/apps-domains/src/lib/{domain}/services/{feature}-api.service.ts
```

## ⚠️ MUST READ Before Implementation

**IMPORTANT: You MUST read these files before writing any code. Do NOT skip.**

1. **⚠️ MUST READ** `.claude/skills/shared/angular-design-system.md` — platform-core imports
2. **⚠️ MUST READ** `.claude/skills/frontend-angular-api-service/references/api-service-patterns.md` — CRUD, caching, upload, search patterns
3. **⚠️ MUST READ** target app design system: `docs/design-system/07-technical-guide.md`

## Anti-Patterns

- `constructor(private http: HttpClient)` - must extend `PlatformApiService`
- Hardcoded URLs: `this.get('https://api.example.com/...')` - use `environment`
- Missing return type: `getUser(id)` - must be `getUser(id): Observable<UserDto>`
- Untyped response: `this.get('/users')` - must be `this.get<UserDto[]>('/users')`
- Error handling in service - let component handle via `tapResponse()`

## Verification Checklist

- [ ] Extends `PlatformApiService`
- [ ] `apiUrl` getter returns `environment.apiUrl + '/api/{Controller}'`
- [ ] All methods have `Observable<T>` return type
- [ ] DTOs defined for request/response types
- [ ] Caching configured for stable lookup endpoints
- [ ] File operations use `postFormData`/`getBlob`
- [ ] `@Injectable({ providedIn: 'root' })` decorator


## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
