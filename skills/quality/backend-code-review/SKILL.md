---
name: backend-code-review
description: Conducts comprehensive backend code reviews including API design (REST/GraphQL/gRPC), database patterns, authentication/authorization, caching strategies, message queues, microservices architecture, security vulnerabilities, and performance optimization for Node.js, Python, Java, Go, and C#. Produces detailed review reports with specific issues, severity ratings, and actionable recommendations. Use when reviewing server-side code, analyzing API implementations, checking database queries, validating authentication flows, assessing microservices architecture, or when users mention "review backend code", "check API design", "analyze server code", "validate database patterns", "security audit", "performance review", or "backend code quality".
---

# Backend Code Review

Conduct systematic backend code reviews to identify security vulnerabilities, performance bottlenecks, code quality issues, and architectural concerns. Produces actionable reports with specific locations and fix recommendations.

## Review Process

Follow this structured approach for comprehensive backend code analysis:

## 1. Assess Technology Stack and Scope

Identify technologies and critical areas before starting:

**Technology Inventory:**

```
Backend Language: Node.js/Python/Java/Go/C#
Framework: Express/FastAPI/Spring Boot/Gin/ASP.NET
Database: PostgreSQL/MySQL/MongoDB/Redis
Architecture: Monolith/Microservices/Serverless
Deployment: AWS/GCP/Azure/Docker/Kubernetes
```

**Critical Review Areas (prioritize these):**

- Authentication and authorization logic
- Payment processing and financial transactions
- Data access layers (ORM queries, raw SQL)
- External API integrations and webhooks
- Background jobs and async processing
- File upload and download handlers

**Example Scope Definition:**

```
Review: User authentication service
Files: src/auth/*.ts (15 files, ~2000 lines)
Priority: High (handles user credentials and sessions)
Focus: Security vulnerabilities, JWT implementation, session management
```

### 2. Review Code Quality and Structure

Evaluate code organization, design patterns, and maintainability:

**Code Organization Checklist:**

```
☐ Proper layering (controllers → services → repositories → database)
☐ Consistent file and folder naming (kebab-case, camelCase, etc.)
☐ One class/function per file (or logically grouped)
☐ No circular dependencies between modules
☐ Clear separation of business logic and infrastructure code
```

**SOLID Principles Validation:**

**Single Responsibility:** Each class/module has one reason to change

```javascript
// ❌ Bad: UserService does too much
class UserService {
  createUser() { }
  sendEmail() { }       // Should be EmailService
  processPayment() { }  // Should be PaymentService
}

// ✅ Good: Separated responsibilities
class UserService {
  createUser() { }
}
class EmailService {
  sendEmail() { }
}
class PaymentService {
  processPayment() { }
}
```

**Dependency Injection:** Dependencies injected, not hardcoded

```python
# ❌ Bad: Hardcoded dependency
class UserService:
    def __init__(self):
        self.db = PostgresDB()  # Hardcoded, hard to test

# ✅ Good: Dependency injection
class UserService:
    def __init__(self, db: Database):
        self.db = db  # Injected, easy to mock
```

**Error Handling Pattern:**

```typescript
// ❌ Bad: Silent failures
async function getUser(id: string) {
  try {
    return await db.users.findOne(id);
  } catch (err) {
    return null;  // Swallows error
  }
}

// ✅ Good: Proper error handling
async function getUser(id: string): Promise<User> {
  try {
    const user = await db.users.findOne(id);
    if (!user) {
      throw new NotFoundError(`User ${id} not found`);
    }
    return user;
  } catch (err) {
    logger.error('Failed to fetch user', { id, error: err });
    throw new DatabaseError('User fetch failed', { cause: err });
  }
}
```

**Code Quality Issues to Flag:**

- Functions > 50 lines (should be split)
- Classes > 300 lines (too many responsibilities)
- Cyclomatic complexity > 10 (simplify logic)
- Code duplication > 5 lines (extract to function)
- Missing type definitions (TypeScript, type hints)
- Magic numbers (use named constants)

**Load detailed checklist:** [code-quality-checklist.md](references/code-quality-checklist.md)

### 3. Validate API Design

Review API endpoints for REST, GraphQL, or gRPC implementations:

**REST API Review:**

**Endpoint Structure:**

```
✅ Good REST Design:
GET    /api/v1/users           - List users (paginated)
GET    /api/v1/users/:id       - Get single user
POST   /api/v1/users           - Create user
PUT    /api/v1/users/:id       - Replace user
PATCH  /api/v1/users/:id       - Update user
DELETE /api/v1/users/:id       - Delete user

❌ Poor REST Design:
GET    /api/v1/getAllUsers     - Use plural nouns, not verbs
POST   /api/v1/user/create     - POST implies creation
GET    /api/v1/user/get/123    - Use path params, not verbs
```

**HTTP Status Codes:**

```
✅ Correct Usage:
200 OK - Successful GET, PUT, PATCH
201 Created - Successful POST (with Location header)
204 No Content - Successful DELETE
400 Bad Request - Invalid input
401 Unauthorized - Missing/invalid authentication
403 Forbidden - Authenticated but not authorized
404 Not Found - Resource doesn't exist
409 Conflict - Duplicate resource
422 Unprocessable Entity - Validation failed
500 Internal Server Error - Server error

❌ Common Mistakes:
200 for errors - Should use 4xx or 5xx
500 for validation errors - Should use 400 or 422
404 for unauthorized - Should use 403
```

**Pagination Implementation:**

```javascript
// ✅ Good: Cursor-based pagination for large datasets
GET /api/v1/orders?cursor=eyJpZCI6MTIzfQ&limit=20
Response: {
  data: [...],
  pagination: {
    nextCursor: "eyJpZCI6MTQzfQ",
    hasMore: true
  }
}

// ✅ Good: Offset pagination for small/medium datasets
GET /api/v1/users?page=2&pageSize=20
Response: {
  data: [...],
  pagination: {
    page: 2,
    pageSize: 20,
    totalPages: 15,
    totalItems: 300
  }
}
```

**GraphQL Review:**

**N+1 Query Detection:**

```graphql
# ❌ Bad: Causes N+1 queries
query {
  posts {
    id
    title
    author {  # Separate query for each post
      name
    }
  }
}

# ✅ Good: Use DataLoader to batch
const authorLoader = new DataLoader(async (authorIds) => {
  // Batch fetch all authors in one query
  return await db.authors.findByIds(authorIds);
});
```

**gRPC Review:**

Check protocol buffer definitions and error handling:

```protobuf
// ✅ Good proto definition
message GetUserRequest {
  string user_id = 1 [(validate.rules).string.uuid = true];
}

message GetUserResponse {
  User user = 1;
}

service UserService {
  rpc GetUser(GetUserRequest) returns (GetUserResponse);
}
```

**Load detailed checklist:** [api-design-checklist.md](references/api-design-checklist.md)

### 4. Analyze Database Queries and Schema

Review database patterns, query optimization, and data integrity:

**SQL Injection Prevention:**

```python
# ❌ Critical: SQL injection vulnerability
def get_user(username):
    query = f"SELECT * FROM users WHERE username = '{username}'"
    return db.execute(query)

# ✅ Good: Parameterized queries
def get_user(username):
    query = "SELECT * FROM users WHERE username = ?"
    return db.execute(query, (username,))
```

**N+1 Query Problem:**

```javascript
// ❌ Bad: N+1 queries (1 query + N queries for authors)
const posts = await Post.findAll();
for (const post of posts) {
  post.author = await User.findById(post.authorId);  // N queries!
}

// ✅ Good: Join or eager load
const posts = await Post.findAll({
  include: [{ model: User, as: 'author' }]  // 1 query with join
});
```

**Missing Indexes:**

```sql
-- ❌ Bad: Queries without indexes
SELECT * FROM orders WHERE user_id = 123;  -- No index on user_id
SELECT * FROM products WHERE status = 'active' AND category = 'electronics';

-- ✅ Good: Add indexes for common queries
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_products_status_category ON products(status, category);
```

**Transaction Handling:**

```java
// ❌ Bad: No transaction for multi-step operation
public void transferFunds(Long fromId, Long toId, BigDecimal amount) {
    Account from = accountRepo.findById(fromId);
    Account to = accountRepo.findById(toId);
    from.setBalance(from.getBalance().subtract(amount));
    to.setBalance(to.getBalance().add(amount));
    accountRepo.save(from);  // What if this fails?
    accountRepo.save(to);    // Money lost!
}

// ✅ Good: Atomic transaction
@Transactional
public void transferFunds(Long fromId, Long toId, BigDecimal amount) {
    Account from = accountRepo.findById(fromId);
    Account to = accountRepo.findById(toId);
    from.setBalance(from.getBalance().subtract(amount));
    to.setBalance(to.getBalance().add(amount));
    accountRepo.save(from);
    accountRepo.save(to);
    // Both save or both rollback
}
```

**Connection Pool Configuration:**

```
✅ Recommended Settings:
- Pool size: 10-20 connections (not 100+)
- Connection timeout: 30 seconds
- Idle timeout: 10 minutes
- Max lifetime: 30 minutes
- Connection validation before use
```

**Load detailed checklist:** [database-checklist.md](references/database-checklist.md)

### 5. Audit Security Vulnerabilities

Identify authentication, authorization, and data protection issues:

**Authentication Security:**

**Password Hashing:**

```javascript
// ❌ Critical: Plain text or weak hashing
const hashedPassword = md5(password);  // MD5 is broken

// ✅ Good: Strong hashing with bcrypt or argon2
const hashedPassword = await bcrypt.hash(password, 12);  // Cost factor 12+
```

**JWT Implementation:**

```typescript
// ❌ Bad: Weak JWT configuration
const token = jwt.sign({ userId: user.id }, 'secret123');  // Weak secret, no expiry

// ✅ Good: Secure JWT configuration
const token = jwt.sign(
  { userId: user.id, role: user.role },
  process.env.JWT_SECRET,  // Strong secret from env
  { 
    expiresIn: '15m',       // Short-lived access token
    algorithm: 'HS256',
    issuer: 'api.example.com',
    audience: 'app.example.com'
  }
);
```

**Authorization Validation:**

```python
# ❌ Bad: Missing authorization check
@app.route('/api/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    db.delete_user(user_id)  # Anyone can delete any user!
    return {'success': True}

# ✅ Good: Proper authorization
@app.route('/api/users/<user_id>', methods=['DELETE'])
@requires_auth
def delete_user(user_id):
    current_user = get_current_user()
    if current_user.id != user_id and not current_user.is_admin:
        raise ForbiddenError("Cannot delete other users")
    db.delete_user(user_id)
    return {'success': True}
```

**Input Validation:**

```javascript
// ❌ Bad: No validation
app.post('/api/users', (req, res) => {
  const user = req.body;  // Trust user input
  db.createUser(user);
});

// ✅ Good: Schema validation
const createUserSchema = z.object({
  email: z.string().email().max(255),
  password: z.string().min(12).max(128),
  age: z.number().int().min(18).max(120),
  role: z.enum(['user', 'admin'])
});

app.post('/api/users', (req, res) => {
  const validatedData = createUserSchema.parse(req.body);  // Throws if invalid
  db.createUser(validatedData);
});
```

**Security Checklist:**

```
☐ Passwords hashed with bcrypt/argon2 (cost factor ≥12)
☐ JWT tokens expire within 1 hour (15min recommended)
