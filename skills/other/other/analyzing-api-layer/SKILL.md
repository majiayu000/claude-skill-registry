---
name: analyzing-api-layer
description: Use when analyzing REST/GraphQL API endpoints, contracts, authentication, and client-facing interfaces
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash(mkdir:*, ls:*)
  - Write(docs/unwind/**)
  - Edit(docs/unwind/**)
---

# Analyzing API Layer

**Output:** `docs/unwind/layers/api/` (folder with index.md + section files)

**Principles:** See `analysis-principles.md` - completeness, machine-readable, link to source, no commentary, incremental writes.

## Output Structure

```
docs/unwind/layers/api/
├── index.md           # Endpoint summary table, route count
├── endpoints.md       # All controller/route definitions
├── auth.md            # Authentication & authorization config
├── contracts.md       # OpenAPI/AsyncAPI/TSRest specs [CRITICAL]
└── errors.md          # Error handling patterns
```

For large codebases (20+ route files), split by domain:
```
docs/unwind/layers/api/
├── index.md
├── users-api.md
├── orders-api.md
└── ...
```

## Process (Incremental Writes)

**Step 1: Setup**
```bash
mkdir -p docs/unwind/layers/api/
```
Write initial `index.md`:
```markdown
# API Layer

## Sections
- [Endpoints](endpoints.md) - _pending_
- [Authentication](auth.md) - _pending_
- [API Contracts](contracts.md) - _pending_
- [Error Handling](errors.md) - _pending_

## Endpoint Summary
_Analysis in progress..._
```

**Step 2: Analyze and write contracts.md** [CRITICAL - DO FIRST]
1. Search for OpenAPI, AsyncAPI, TSRest, GraphQL specs
2. Include COMPLETE specs (not summaries)
3. Write `contracts.md` immediately
4. Update `index.md`

**Step 3: Analyze and write endpoints.md**
1. Find all controller/route classes
2. Include actual code with annotations
3. Write `endpoints.md` immediately
4. Update `index.md`

**Step 4: Analyze and write auth.md**
1. Find security configuration
2. Document permission matrix
3. Write `auth.md` immediately
4. Update `index.md`

**Step 5: Analyze and write errors.md**
1. Find error handlers, exception mappers
2. Write `errors.md` immediately
3. Update `index.md`

**Step 6: Finalize index.md**
Add endpoint summary table with final counts

## Output Format

```markdown
# API Layer

## Endpoints

### UserController

[UserController.java](https://github.com/owner/repo/blob/main/src/controller/UserController.java)

```java
@RestController
@RequestMapping("/api/v1/users")
@RequiredArgsConstructor
public class UserController {
    private final UserService userService;
    private final UserMapper userMapper;

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public UserResponse createUser(@Valid @RequestBody CreateUserRequest request) {
        User user = userService.createUser(request);
        return userMapper.toResponse(user);
    }

    @GetMapping("/me")
    @PreAuthorize("isAuthenticated()")
    public UserResponse getCurrentUser(@AuthenticationPrincipal UserDetails user) {
        return userMapper.toResponse(userService.getByEmail(user.getUsername()));
    }

    @GetMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    public UserResponse getUser(@PathVariable Long id) {
        return userMapper.toResponse(userService.getUser(id));
    }
}
```

[Continue for ALL controllers...]

## Endpoint Summary

| Method | Path | Auth | Handler |
|--------|------|------|---------|
| POST | /api/v1/users | None | UserController.createUser |
| GET | /api/v1/users/me | User | UserController.getCurrentUser |
| GET | /api/v1/users/{id} | Admin | UserController.getUser |
| POST | /api/v1/orders | User | OrderController.createOrder |

[List ALL endpoints...]

## OpenAPI Specification

```yaml
openapi: 3.0.0
info:
  title: User API
  version: 1.0.0
paths:
  /api/v1/users:
    post:
      operationId: createUser
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserRequest'
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserResponse'
```

## Security Configuration

[SecurityConfig.java](https://github.com/owner/repo/blob/main/src/config/SecurityConfig.java)

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        return http
            .csrf(csrf -> csrf.disable())
            .sessionManagement(session -> session.sessionCreationPolicy(STATELESS))
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/v1/auth/**").permitAll()
                .requestMatchers("/api/v1/admin/**").hasRole("ADMIN")
                .anyRequest().authenticated()
            )
            .addFilterBefore(jwtFilter, UsernamePasswordAuthenticationFilter.class)
            .build();
    }
}
```

## Error Responses

```java
@RestControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(UserNotFoundException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public ErrorResponse handleNotFound(UserNotFoundException ex) {
        return new ErrorResponse("USER_NOT_FOUND", ex.getMessage());
    }
}
```

## Unknowns

- [List anything unclear]
```

## Additional Requirements

### API Specification Discovery [CRITICAL - MUST PRESERVE]

Search for existing API specifications - these define external contracts and MUST be used AS-IS in any migration to maintain compatibility.

**Search for these file patterns:**

| Spec Type | Common Locations | File Patterns |
|-----------|------------------|---------------|
| OpenAPI/Swagger | `docs/`, `api/`, root | `openapi.yaml`, `openapi.json`, `swagger.yaml`, `swagger.json`, `api.yaml` |
| AsyncAPI | `docs/`, `api/`, root | `asyncapi.yaml`, `asyncapi.json` |
| TSRest | `src/contracts/`, `src/api/` | `contract.ts`, `*Contract.ts`, `*.contract.ts` |
| tRPC | `src/server/`, `src/trpc/` | `router.ts`, `*.router.ts` |
| GraphQL | `src/schema/`, `src/graphql/` | `schema.graphql`, `*.graphql`, `typeDefs.ts` |
| Protobuf | `proto/`, `src/proto/` | `*.proto` |
| JSON Schema | `schemas/`, `src/schemas/` | `*.schema.json` |

**Process:**
1. Search for all spec files using glob patterns
2. Include COMPLETE spec files in documentation (not summaries)
3. Mark as `[CRITICAL - EXTERNAL CONTRACT]`
4. Note any generated client code that depends on specs

**Output Format:**

```markdown
## API Specifications [CRITICAL - EXTERNAL CONTRACT]

### OpenAPI Specification

**Location:** `docs/openapi.yaml`
**Version:** 3.0.0
**Endpoints Defined:** 45

```yaml
# INCLUDE COMPLETE SPEC - DO NOT SUMMARIZE
openapi: 3.0.0
info:
  title: MyService API
  version: 2.1.0
paths:
  /api/v1/users:
    ...
[FULL SPEC HERE]
```

### TSRest Contract

**Location:** `src/contracts/api.contract.ts`

```typescript
// INCLUDE COMPLETE CONTRACT
import { initContract } from '@ts-rest/core';

const c = initContract();

export const apiContract = c.router({
  users: {
    create: {
      method: 'POST',
      path: '/api/users',
      ...
    }
  }
});
```

### AsyncAPI (Event Contracts)

**Location:** `docs/asyncapi.yaml`

```yaml
# INCLUDE COMPLETE SPEC
asyncapi: 2.6.0
info:
  title: MyService Events
channels:
  user.created:
    ...
```
```

**Why This Matters:**
- External clients depend on these contracts
- Breaking changes cause integration failures
- Rebuild MUST maintain exact contract compatibility
- These specs are the source of truth for API shape

### Complete Route Inventory [MUST]

List ALL route files with exact count:

```markdown
## Route Inventory

**Total:** 43 route modules

| # | File | Base Path | Endpoints |
|---|------|-----------|-----------|
| 1 | auth.ts | /api/auth | 8 |
| 2 | users.ts | /api/users | 5 |
| ... | ... | ... | ... |
```

### Missing Documentation Tracking

If a route file exists but is not fully documented, note it:

```markdown
## Documentation Gaps

| Route File | Status | Reason |
|------------|--------|--------|
| onyx.ts | NOT DOCUMENTED | Admin/debug routes |
| playground.ts | NOT DOCUMENTED | Development only |
```

### External API Contracts [MUST]

For any external integrations, document the contract:

```markdown
### GitHub Integration [MUST]

**Endpoints Consumed:**
- GET /user/installations
- GET /orgs/:org/teams
- POST /app/installations/:id/access_tokens

**Webhook Events:**
- installation.created
- installation.deleted
```

### Permission Documentation [MUST]

For each endpoint, document required permissions:

```markdown
| Endpoint | Method | Auth | Permission |
|----------|--------|------|------------|
| /api/budgets | GET | Required | budget:read |
| /api/budgets | POST | Required | budget:create |
| /api/budgets/:id | DELETE | Required | budget:delete (admin) |
```

## Mandatory Tagging

**Every endpoint, route, and contract must have a [MUST], [SHOULD], or [DON'T] tag in its heading.**

Default categorizations for API layer:
- **[MUST]**: All endpoints, authentication flows, external API contracts, permissions
- **[SHOULD]**: Error handling patterns, rate limiting, logging middleware
- **[DON'T]**: Framework-specific middleware config, CORS setup details

Example:
```markdown
### POST /api/users [MUST]
### AuthMiddleware [MUST]
### OpenAPI spec [MUST]
### ErrorHandler [SHOULD]
```

See `analysis-principles.md` section 9 for full tagging rules.

## Refresh Mode

If `docs/unwind/layers/api/` exists, compare current state and add `## Changes Since Last Review` section to `index.md`.
