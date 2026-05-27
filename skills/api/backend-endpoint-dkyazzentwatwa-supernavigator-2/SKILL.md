---
name: backend-endpoint
description: Create REST/GraphQL API endpoint with validation, error handling, and tests. Auto-invoke when user says "add endpoint", "create API", "new route", or "add route".
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
version: 1.0.0
---

# Backend API Endpoint Generator

Generate production-ready REST or GraphQL endpoints with request validation, error handling, and comprehensive tests.

## When to Invoke

Auto-invoke when user mentions:
- "Add endpoint"
- "Create API"
- "New route"
- "Add route"
- "Create API endpoint for [resource]"

## What This Does

1. Generates route handler with proper HTTP methods
2. Adds request validation (body, params, query)
3. Implements error handling
4. Creates test file with request/response tests
5. Follows REST/GraphQL conventions
6. Includes authentication middleware (if needed)

## Execution Steps

### Step 1: Gather Endpoint Requirements

**Ask user for endpoint details**:
```
Endpoint path: [e.g., /api/users/:id]
HTTP method: [GET, POST, PUT, PATCH, DELETE]
Resource name: [e.g., User, Post, Product]

Framework:
  - express (default)
  - fastify
  - nestjs
  - graphql

Authentication required: [yes/no]
Request validation needed: [yes/no]
```

**Validate endpoint path**:
- Use predefined function: `functions/route_validator.py`
- Ensure RESTful conventions
- Check path parameters syntax
- No trailing slashes

### Step 1.5: Verify Understanding (ToM Checkpoint) [EXECUTE]

**IMPORTANT**: This step MUST be executed for high-stakes operations.

**Before generating code, confirm interpretation with user**.

**Display verification**:
```
I understood you want:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Endpoint: {METHOD} {PATH}
Resource: {RESOURCE_NAME}
Framework: {FRAMEWORK} (detected from package.json / specified)
Auth required: {yes/no}
Validation needed: {yes/no}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Assumptions I'm making:
- Using {VALIDATION_LIBRARY} for validation (detected from existing validators)
- Error handling follows existing pattern in {ERROR_HANDLER_PATH}
- Route will be registered at {ROUTE_PREFIX} prefix

Proceed with generation? [Y/n]
```

**Skip verification if** (HIGH-STAKES ONLY mode):
- Simple CRUD operation (single resource, single path parameter)
- User explicitly said "quick", "just do it", or "skip confirmation"
- No custom authentication logic specified
- Standard GET/POST/PUT/DELETE without complex business logic

**Always verify if**:
- Multiple path parameters (e.g., `/users/:userId/posts/:postId`)
- Custom authorization logic specified
- Non-standard HTTP methods or patterns
- GraphQL mutations with side effects
- Endpoints involving financial or sensitive data

### Step 1.8: Declare Belief State (Optional - ToM Anchor)

**Before generating code, optionally declare explicit assumptions** (enabled by `tom_features.belief_anchors` in config).

**Display belief state anchor**:
```
📌 BELIEF STATE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

What I know (from context):
✅ Framework: {FRAMEWORK} (from package.json)
✅ TypeScript: {strict/normal} mode (from tsconfig.json)
✅ Validation: {LIBRARY} (from existing validators/)

What I'm assuming (inference):
🔸 Error handler follows pattern in {PATH}
🔸 Routes registered at {PREFIX} prefix
🔸 Using {CONVENTION} commit messages

What I don't know (using defaults):
❓ Request logging preference (will include)
❓ Rate limiting requirements (will skip)
❓ Response envelope format (will use standard)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Adjustments needed before I proceed?
```

**Skip belief anchor if**:
- `tom_features.belief_anchors` is false in config
- User said "skip", "just do it", "quick"
- Simple endpoint with no custom logic

**Show belief anchor if**:
- Complex endpoint with multiple integrations
- User profile indicates preference for detailed explanations
- First endpoint in a new project (establishing patterns)

### Step 2: Generate Route Handler

**Based on HTTP method and framework**:

Use predefined function: `functions/endpoint_generator.py`

```bash
python3 functions/endpoint_generator.py \
  --path "/api/users/:id" \
  --method "GET" \
  --resource "User" \
  --framework "express" \
  --auth true \
  --validation true \
  --template "templates/express-route-template.ts" \
  --output "src/routes/users.ts"
```

**Template includes**:
- Route definition
- Request validation middleware
- Controller/handler function
- Error handling
- Response formatting
- TypeScript types

### Step 3: Generate Validation Schema

**Use predefined function**: `functions/validation_generator.py`

```bash
python3 functions/validation_generator.py \
  --resource "User" \
  --method "POST" \
  --fields "name:string:required,email:email:required,age:number:optional" \
  --library "zod" \
  --output "src/validators/user.validator.ts"
```

**Supported validation libraries**:
- Zod (default, TypeScript-first)
- Joi (JavaScript schema)
- Yup (object schema)
- Express-validator (middleware-based)

**Output example (Zod)**:
```typescript
import { z } from 'zod';

export const createUserSchema = z.object({
  name: z.string().min(1),
  email: z.string().email(),
  age: z.number().optional(),
});

export type CreateUserInput = z.infer<typeof createUserSchema>;
```

### Step 4: Generate Error Handling Middleware

**Use predefined function**: `functions/error_handler_generator.py`

```bash
python3 functions/error_handler_generator.py \
  --framework "express" \
  --template "templates/error-handler-template.ts" \
  --output "src/middleware/errorHandler.ts"
```

**Error handler includes**:
- HTTP status code mapping
- Error response formatting
- Logging integration
- Development vs production modes
- Validation error handling

### Step 5: Generate Test File

**Use predefined function**: `functions/test_generator.py`

```bash
python3 functions/test_generator.py \
  --endpoint "/api/users/:id" \
  --method "GET" \
  --framework "express" \
  --template "templates/endpoint-test-template.spec.ts" \
  --output "tests/routes/users.test.ts"
```

**Test template includes**:
- Success case (200/201)
- Validation errors (400)
- Not found (404)
- Unauthorized (401)
- Server errors (500)
- Edge cases

**Example test**:
```typescript
describe('GET /api/users/:id', () => {
  it('returns user when found', async () => {
    const response = await request(app)
      .get('/api/users/123')
      .expect(200);

    expect(response.body).toMatchObject({
      id: '123',
      name: expect.any(String),
    });
  });

  it('returns 404 when user not found', async () => {
    await request(app)
      .get('/api/users/999')
      .expect(404);
  });
});
```

### Step 6: Generate API Documentation Comment

**JSDoc or OpenAPI annotation**:

```typescript
/**
 * @route GET /api/users/:id
 * @description Get user by ID
 * @access Private
 * @param {string} id - User ID
 * @returns {User} User object
 * @throws {404} User not found
 * @throws {401} Unauthorized
 */
```

### Step 7: Show Endpoint Summary

**Display generated files and usage**:

```
✅ Endpoint Created: GET /api/users/:id

Structure:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📁 src/
   ├── routes/users.ts                (Route handler)
   ├── validators/user.validator.ts   (Request validation)
   └── middleware/errorHandler.ts     (Error handling)

📁 tests/
   └── routes/users.test.ts           (Integration tests)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Route Registration:
import { userRoutes } from './routes/users';
app.use('/api', userRoutes);

Test:
curl http://localhost:3000/api/users/123
# or
npm test -- users.test.ts

Next Steps:
1. Implement business logic in controller
2. Connect to database/service layer
3. Run tests: npm test
4. Test with Postman/Thunder Client
```

---

## Predefined Functions

### 1. route_validator.py

Validates route path follows REST conventions.

**Usage**:
```bash
python3 functions/route_validator.py --path "/api/users/:id" --method "GET"
```

**Checks**:
- RESTful naming (plural resources)
- Path parameter syntax (`:id` or `{id}`)
- No trailing slashes
- HTTP method matches intent

**Returns**: Valid path or error message

---

### 2. endpoint_generator.py

Generates endpoint handler from template.

**Usage**:
```bash
python3 functions/endpoint_generator.py \
  --path "/api/users/:id" \
  --method "GET" \
  --resource "User" \
  --framework "express" \
  --auth true \
  --validation true \
  --template "templates/express-route-template.ts"
```

**Parameters**:
- `--path`: API endpoint path
- `--method`: HTTP method
- `--resource`: Resource name (singular, PascalCase)
- `--framework`: Backend framework
- `--auth`: Include auth middleware
- `--validation`: Include validation middleware
- `--template`: Template file path

**Returns**: Generated endpoint code

---

### 3. validation_generator.py

Generates request validation schema.

**Usage**:
```bash
python3 functions/validation_generator.py \
  --resource "User" \
  --method "POST" \
  --fields "name:string:required,email:email:required" \
  --library "zod"
```

**Supported field types**:
- `string`, `number`, `boolean`
- `email`, `url`, `uuid`
- `array`, `object`
- `date`, `datetime`

**Returns**: Validation schema code

---

### 4. error_handler_generator.py

Generates error handling middleware.

**Usage**:
```bash
python3 functions/error_handler_generator.py \
  --framework "express" \
  --template "templates/error-handler-template.ts"
```

**Returns**: Error handler middleware code

---

### 5. test_generator.py

Generates endpoint integration tests.

**Usage**:
```bash
python3 functions/test_generator.py \
  --endpoint "/api/users/:id" \
  --method "GET" \
  --framework "express" \
  --template "templates/endpoint-test-template.spec.ts"
```

**Generates tests for**:
- Success responses
- Validation errors
- Authentication errors
- Not found errors
- Server errors

**Returns**: Generated test code

---

## Templates

### express-route-template.ts

Express.js route handler template.

**Placeholders**:
- `${ROUTE_PATH}` - API endpoint path
- `${HTTP_METHOD}` - HTTP method (lowercase)
- `${RESOURCE_NAME}` - Resource name (PascalCase)
- `${VALIDATION_MIDDLEWARE}` - Validation middleware
- `${AUTH_MIDDLEWARE}` - Authentication middleware

### fastify-route-template.ts

Fastify route handler template (alternative).

### graphql-resolver-template.ts

GraphQL resolver template (alternative).

### validation-zod-template.ts

Zod validation schema template.

### endpoint-test-template.spec.ts

Integration test template with supertest.

**Placeholders**:
- `${ENDPOINT_PATH}` - Endpoint to test
- `${HTTP_METHOD}` - HTTP method
- `${TEST_CASES}` - Generated test cases

---

## Examples

See `examples/` directory for reference implementations:

1. **users-get.ts** - GET endpoint with auth
2. **users-post.ts** - POST endpoint with validation
3. **graphql-resolver.ts** - GraphQL mutation example

Each example includes:
- Route/resolver implementation
- Validation schema
- Error handling
- Test file
- Usage documentation

---

## Best Practices

### REST API Design
- **Use plural nouns** for resources (`/users`, not `/user`)
- **Use HTTP methods correctly** (GET=read, POST=create, PUT/PATCH=update, DELETE=remove)
- **Nest resources properly** (`/users/:userId/posts/:postId`)
- **Return proper status codes** (200, 201, 400, 401, 404, 500)

### Request Validation
- **Validate all inputs** (body, params, query)
- **Fail fast** (validate before business logic)
- **Clear error messages** (tell user what's wrong)
- **Sanitize inputs** (prevent injection attacks)

### Error Handling
- **Centralized error handler** (DRY principle)
- **Consistent error format** (always same structure)
- **Don't expose internals** (sanitize stack traces in production)
- **Log errors** (for debugging)

### Security
- **Authentication** (verify identity)
- **Authorization** (check permissions)
- **Rate limiting** (prevent abuse)
- **Input sanitization** (prevent XSS, SQL injection)

### Testing
- **Test happy path** (success cases)
- **Test error cases** (validation, auth, not found)
- **Test edge cases** (empty data, large data)
- **Mock external dependencies** (database, APIs)

---

## Troubleshooting

### Route Not Found (404)

**Problem**: Endpoint returns 404 even though route is defined

**Solutions**:
1. Check route registration order (specific before generic)
2. Verify path matches exactly (case-sensitive)
3. Check middleware isn't blocking request
4. Validate HTTP method matches

### Validation Always Fails

**Problem**: Valid requests fail validation

**Solutions**:
1. Check field names match exactly
2. Verify data types are correct
3. Check required vs optional fields
4. Inspect validation error message

### Tests Failing

**Problem**: Integration tests don't pass

**Solutions**:
1. Ensure test database is seeded
2. Check test fixtures are correct
3. Verify mocks are set up properly
4. Run tests with `--verbose` flag

---

## Success Criteria

**This skill succeeds when**:
- [ ] Endpoint responds with correct status codes
- [ ] Request validation catches invalid inputs
- [ ] Error handling works consistently
- [ ] Tests cover success and error cases
- [ ] Code follows REST/GraphQL conventions
- [ ] Documentation is clear and complete

---

**Auto-invoke this skill when creating API endpoints to ensure consistency and security** 🔒
