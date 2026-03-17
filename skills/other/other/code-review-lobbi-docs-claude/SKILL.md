---
name: code-review
description: Comprehensive code review knowledge including security, performance, accessibility, and quality standards across multiple languages and frameworks
trigger_phrases:
  - review code
  - check changes
  - analyze PR
  - code quality
  - security review
  - performance review
  - accessibility review
  - review this code
  - code audit
  - pull request review
categories:
  - review
  - quality
  - security
  - performance
  - accessibility
  - testing
version: 1.0.0
last_updated: 2025-12-17
---

# Code Review Skill

Comprehensive code review knowledge base for systematic evaluation of code changes across security, performance, accessibility, quality, and testing dimensions.

## Overview

This skill provides structured review patterns, checklists, and best practices for conducting thorough code reviews. It covers multiple programming languages, frameworks, and architectural patterns with a focus on actionable feedback.

---

## Review Categories

### 1. Security Review

#### Critical Security Checks

**Authentication & Authorization**
- [ ] Authentication tokens properly validated
- [ ] Authorization checks present on all sensitive operations
- [ ] Session management follows security best practices
- [ ] No hardcoded credentials or API keys
- [ ] Proper role-based access control (RBAC)
- [ ] JWT tokens validated with proper algorithms (not 'none')
- [ ] Password hashing uses bcrypt/argon2 (not MD5/SHA1)

**Input Validation**
- [ ] All user inputs sanitized and validated
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (proper escaping/sanitization)
- [ ] CSRF tokens on state-changing operations
- [ ] File upload validation (type, size, content)
- [ ] JSON/XML parsing with size limits
- [ ] URL validation for redirects

**Data Protection**
- [ ] Sensitive data encrypted at rest
- [ ] TLS/HTTPS for data in transit
- [ ] No sensitive data in logs
- [ ] PII handling compliant with regulations
- [ ] Secure random number generation (crypto.randomBytes)
- [ ] Secrets stored in environment variables or secret managers
- [ ] Database connections use encrypted channels

**Common Vulnerabilities (OWASP Top 10)**
- [ ] No injection flaws (SQL, NoSQL, OS commands)
- [ ] No broken authentication
- [ ] No sensitive data exposure
- [ ] No XML external entities (XXE)
- [ ] No broken access control
- [ ] No security misconfiguration
- [ ] No cross-site scripting (XSS)
- [ ] No insecure deserialization
- [ ] No components with known vulnerabilities
- [ ] Sufficient logging and monitoring

#### Security Code Patterns

**Good:**
```typescript
// Parameterized queries prevent SQL injection
const user = await db.query(
  'SELECT * FROM users WHERE email = $1',
  [userEmail]
);

// Proper password hashing
const hashedPassword = await bcrypt.hash(password, 12);

// Secure session configuration
app.use(session({
  secret: process.env.SESSION_SECRET,
  resave: false,
  saveUninitialized: false,
  cookie: {
    httpOnly: true,
    secure: true, // HTTPS only
    sameSite: 'strict',
    maxAge: 3600000
  }
}));
```

**Bad:**
```typescript
// SQL injection vulnerability
const user = await db.query(
  `SELECT * FROM users WHERE email = '${userEmail}'`
);

// Weak password hashing
const hashedPassword = crypto.createHash('md5').update(password).digest('hex');

// Insecure session
app.use(session({
  secret: 'hardcoded-secret',
  cookie: { secure: false }
}));
```

---

### 2. Performance Review

#### Performance Checklist

**Database & Queries**
- [ ] N+1 query problems identified and fixed
- [ ] Proper database indexing on query fields
- [ ] Query result sets limited (pagination)
- [ ] Connection pooling implemented
- [ ] Expensive queries cached appropriately
- [ ] Batch operations used instead of loops
- [ ] Database transactions properly scoped

**Frontend Performance**
- [ ] Code splitting implemented for large bundles
- [ ] Lazy loading for routes and components
- [ ] Images optimized and lazy loaded
- [ ] CSS/JS minified and compressed
- [ ] Memoization used for expensive computations
- [ ] Virtual scrolling for long lists
- [ ] Web workers for CPU-intensive tasks
- [ ] Service workers for offline capability

**API & Network**
- [ ] API responses paginated
- [ ] GraphQL queries optimized (no over-fetching)
- [ ] Response compression enabled (gzip/brotli)
- [ ] CDN used for static assets
- [ ] HTTP/2 or HTTP/3 enabled
- [ ] Proper caching headers set
- [ ] Rate limiting implemented

**Memory Management**
- [ ] Event listeners properly removed
- [ ] No memory leaks (closures, timers)
- [ ] Large objects properly disposed
- [ ] File streams closed after use
- [ ] WeakMap/WeakSet used for caching

#### Performance Anti-Patterns

**Bad - N+1 Query:**
```typescript
// Loads users, then queries each user's posts separately
const users = await User.findAll();
for (const user of users) {
  user.posts = await Post.findAll({ where: { userId: user.id } });
}
```

**Good - Eager Loading:**
```typescript
// Single query with JOIN
const users = await User.findAll({
  include: [{ model: Post }]
});
```

**Bad - No Memoization:**
```typescript
function ExpensiveComponent({ data }) {
  // Recalculates on every render
  const processed = expensiveOperation(data);
  return <div>{processed}</div>;
}
```

**Good - With Memoization:**
```typescript
function ExpensiveComponent({ data }) {
  const processed = useMemo(
    () => expensiveOperation(data),
    [data]
  );
  return <div>{processed}</div>;
}
```

---

### 3. Accessibility Review (WCAG 2.1 AA)

#### Accessibility Checklist

**Semantic HTML**
- [ ] Proper heading hierarchy (h1, h2, h3)
- [ ] Semantic elements used (nav, main, article, aside)
- [ ] Form labels properly associated
- [ ] Button vs link used appropriately
- [ ] Tables have proper headers

**Keyboard Navigation**
- [ ] All interactive elements keyboard accessible
- [ ] Logical tab order maintained
- [ ] Focus indicators visible
- [ ] No keyboard traps
- [ ] Skip links provided for navigation

**Screen Reader Support**
- [ ] All images have alt text
- [ ] ARIA labels where needed
- [ ] ARIA roles appropriate
- [ ] Live regions for dynamic content
- [ ] Hidden content properly marked

**Color & Contrast**
- [ ] Text contrast ratio >= 4.5:1 (normal text)
- [ ] Text contrast ratio >= 3:1 (large text)
- [ ] Information not conveyed by color alone
- [ ] Focus indicators meet contrast requirements

**Forms & Inputs**
- [ ] Error messages associated with fields
- [ ] Required fields clearly marked
- [ ] Form validation accessible
- [ ] Placeholder text not used as labels
- [ ] Autocomplete attributes set

#### Accessibility Code Examples

**Good:**
```tsx
// Proper form accessibility
<form>
  <label htmlFor="email">
    Email Address <span aria-label="required">*</span>
  </label>
  <input
    id="email"
    type="email"
    required
    aria-required="true"
    aria-describedby="email-error"
    autoComplete="email"
  />
  <span id="email-error" role="alert">
    {errors.email}
  </span>
</form>

// Accessible modal
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="dialog-title"
  aria-describedby="dialog-description"
>
  <h2 id="dialog-title">Confirm Action</h2>
  <p id="dialog-description">Are you sure?</p>
  <button onClick={handleConfirm}>Confirm</button>
  <button onClick={handleCancel}>Cancel</button>
</div>
```

**Bad:**
```tsx
// Poor accessibility
<div onClick={handleClick}>Click me</div> // Should be button
<img src="photo.jpg" /> // Missing alt text
<input placeholder="Email" /> // Placeholder not a label
<div class="error">{error}</div> // Not associated with input
```

---

### 4. Code Quality Standards

#### Code Quality Checklist

**Readability**
- [ ] Descriptive variable and function names
- [ ] Functions under 50 lines (single responsibility)
- [ ] Consistent naming conventions (camelCase, PascalCase)
- [ ] No magic numbers (use named constants)
- [ ] Logical code organization
- [ ] Proper indentation and formatting

**Maintainability**
- [ ] DRY principle followed (no duplication)
- [ ] SOLID principles applied
- [ ] Low coupling, high cohesion
- [ ] Proper separation of concerns
- [ ] Configuration externalized
- [ ] Feature flags for gradual rollout

**Error Handling**
- [ ] All errors properly caught and handled
- [ ] User-friendly error messages
- [ ] Errors logged with context
- [ ] Graceful degradation implemented
- [ ] Retry logic for transient failures
- [ ] Circuit breakers for external services

**Code Comments**
- [ ] Complex logic explained
- [ ] Why, not what (code is self-explanatory)
- [ ] TODO/FIXME with issue tracking links
- [ ] JSDoc/TSDoc for public APIs
- [ ] No commented-out code

#### Code Quality Examples

**Good:**
```typescript
// Clear naming and single responsibility
const MAX_LOGIN_ATTEMPTS = 3;
const LOCKOUT_DURATION_MS = 15 * 60 * 1000; // 15 minutes

async function validateUserCredentials(
  email: string,
  password: string
): Promise<User | null> {
  const user = await findUserByEmail(email);

  if (!user) {
    return null;
  }

  if (isAccountLocked(user)) {
    throw new AccountLockedError(user.lockoutUntil);
  }

  const isValid = await verifyPassword(password, user.passwordHash);

  if (!isValid) {
    await incrementFailedAttempts(user);
    return null;
  }

  await resetFailedAttempts(user);
  return user;
}
```

**Bad:**
```typescript
// Poor naming, multiple responsibilities, magic numbers
async function check(e: string, p: string) {
  const u = await db.query('SELECT * FROM users WHERE email = ?', [e]);
  if (!u) return null;
  if (u.fa > 3 && Date.now() - u.lat < 900000) throw new Error('locked');
  const ok = await bcrypt.compare(p, u.ph);
  if (!ok) {
    await db.query('UPDATE users SET fa = fa + 1, lat = ? WHERE id = ?', [Date.now(), u.id]);
    return null;
  }
  await db.query('UPDATE users SET fa = 0 WHERE id = ?', [u.id]);
  return u;
}
```

---

### 5. Test Coverage Requirements

#### Testing Checklist

**Unit Tests**
- [ ] All business logic unit tested
- [ ] Edge cases covered
- [ ] Error conditions tested
- [ ] Mocks used for external dependencies
- [ ] Test coverage >= 80%
- [ ] Tests are deterministic (no flaky tests)

**Integration Tests**
- [ ] API endpoints tested
- [ ] Database operations tested
- [ ] External service integrations tested
- [ ] Authentication flows tested
- [ ] Error handling tested

**E2E Tests**
- [ ] Critical user flows covered
- [ ] Happy paths tested
- [ ] Error scenarios tested
- [ ] Cross-browser compatibility
- [ ] Mobile responsiveness

**Test Quality**
- [ ] Tests are readable and maintainable
- [ ] AAA pattern (Arrange, Act, Assert)
- [ ] Meaningful test descriptions
- [ ] No test interdependencies
- [ ] Fast execution (< 10s for unit tests)

#### Test Examples

**Good Unit Test:**
```typescript
describe('UserService.validateCredentials', () => {
  it('should return user when credentials are valid', async () => {
    // Arrange
    const email = 'user@example.com';
    const password = 'SecurePass123!';
    const mockUser = { id: 1, email, passwordHash: 'hash' };

    jest.spyOn(userRepo, 'findByEmail').mockResolvedValue(mockUser);
    jest.spyOn(bcrypt, 'compare').mockResolvedValue(true);

    // Act
    const result = await userService.validateCredentials(email, password);

    // Assert
    expect(result).toEqual(mockUser);
    expect(userRepo.findByEmail).toHaveBeenCalledWith(email);
  });

  it('should throw AccountLockedError when account is locked', async () => {
    // Arrange
    const email = 'locked@example.com';
    const password = 'password';
    const lockoutUntil = new Date(Date.now() + 900000);
    const mockUser = {
      id: 2,
      email,
      failedAttempts: 3,
      lockoutUntil
    };

    jest.spyOn(userRepo, 'findByEmail').mockResolvedValue(mockUser);

    // Act & Assert
    await expect(
      userService.validateCredentials(email, password)
    ).rejects.toThrow(AccountLockedError);
  });
});
```

---

### 6. Documentation Standards

#### Documentation Checklist

**Code Documentation**
- [ ] Public APIs have JSDoc/TSDoc
- [ ] Complex algorithms explained
- [ ] Type definitions documented
- [ ] Examples provided for usage
- [ ] Deprecation notices added

**README Documentation**
- [ ] Setup instructions clear
- [ ] Dependencies listed
- [ ] Environment variables documented
- [ ] Usage examples provided
- [ ] Troubleshooting section

**API Documentation**
- [ ] Endpoint descriptions
- [ ] Request/response schemas
- [ ] Authentication requirements
- [ ] Error codes documented
- [ ] Rate limiting explained

**Architecture Documentation**
- [ ] ADRs for major decisions
- [ ] System diagrams updated
- [ ] Data flow documented
- [ ] Integration points documented

---

## Language-Specific Review Patterns

### TypeScript/JavaScript

#### TypeScript Best Practices

**Type Safety**
- [ ] No `any` types (use `unknown` if needed)
- [ ] Strict mode enabled
- [ ] Union types over enums for constants
- [ ] Proper generic constraints
- [ ] Type guards for narrowing

**Good:**
```typescript
// Proper typing with generics
interface ApiResponse<T> {
  data: T;
  status: number;
  error?: string;
}

async function fetchData<T>(url: string): Promise<ApiResponse<T>> {
  try {
    const response = await fetch(url);
    const data = await response.json() as T;
    return { data, status: response.status };
  } catch (error) {
    return {
      data: {} as T,
      status: 500,
      error: error instanceof Error ? error.message : 'Unknown error'
    };
  }
}

// Type guards
function isUser(obj: unknown): obj is User {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    'id' in obj &&
    'email' in obj
  );
}
```

#### Modern JavaScript Patterns

**Good:**
```typescript
// Destructuring and default values
function createUser({
  email,
  name,
  role = 'user',
  active = true
}: CreateUserInput) {
  return { email, name, role, active };
}

// Optional chaining and nullish coalescing
const userName = user?.profile?.name ?? 'Anonymous';

// Async/await over promise chains
async function processData() {
  try {
    const data = await fetchData();
    const processed = await transform(data);
    await save(processed);
  } catch (error) {
    logger.error('Processing failed', error);
    throw error;
  }
}
```

---

### React Component Patterns

#### React Best Practices

**Component Structure**
- [ ] Functional components with hooks
- [ ] Props properly typed
- [ ] State minimal and localized
- [ ] Effects have proper dependencies
- [ ] No inline function definitions in JSX
- [ ] Keys used correctly in lists

**Good:**
```typescript
interface UserListProps {
  users: User[];
  onUserSelect: (userId: string) => void;
}

const UserList: React.FC<UserListProps> = ({ users, onUserSelect }) => {
  const [searchTerm, setSearchTerm] = useState('');

  const filteredUsers = useMemo(
    () => users.filter(u => u.name.includes(searchTerm)),
    [users, searchTerm]
  );

  const handleSelect = useCallback(
    (userId: string) => {
      onUserSelect(userId);
    },
    [onUserSelect]
  );

  return (
    <div>
      <input
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        placeholder="Search users..."
      />
      <ul>
        {filteredUsers.map(user => (
          <li key={user.id}>
            <button onClick={() => handleSelect(user.id)}>
              {user.name}
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};
```

**Bad:**
```typescript
// Multiple issues
function UserList({ users, onUserSelect }) { // No types
  const [searchTerm, setSearchTerm] = useState('');

  // No memoization - filters on every render
  const filteredUsers = users.filter(u => u.name.includes(searchTerm));

  return (
    <div>
      <ul>
        {filteredUsers.map(user => ( // No key
          <li>
            {/* Inline function creates new reference every render */}
            <button onClick={() => onUserSelect(user.id)}>
              {user.name}
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

---

### Node.js Best Practices

**Server Setup**
- [ ] Proper error handling middleware
- [ ] Request validation middleware
- [ ] Rate limiting implemented
- [ ] Helmet for security headers
- [ ] CORS properly configured
- [ ] Graceful shutdown handling

**Good:**
```typescript
import express from 'express';
import helmet from 'helmet';
import rateLimit from 'express-rate-limit';

const app = express();

// Security middleware
app.use(helmet());
app.use(express.json({ limit: '10mb' }));

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100
});
app.use('/api/', limiter);

// Error handling
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  logger.error('Unhandled error', { error: err, path: req.path });
  res.status(500).json({ error: 'Internal server error' });
});

// Graceful shutdown
process.on('SIGTERM', async () => {
  logger.info('SIGTERM received, closing server...');
  await server.close();
  await db.disconnect();
  process.exit(0);
});
```

---

### Python Patterns

**Python Best Practices**
- [ ] Type hints on functions
- [ ] PEP 8 compliance
- [ ] Context managers for resources
- [ ] List comprehensions over loops
- [ ] Dataclasses for data structures

**Good:**
```python
from dataclasses import dataclass
from typing import List, Optional
from contextlib import contextmanager

@dataclass
class User:
    id: int
    email: str
    name: str
    role: str = 'user'

def validate_email(email: str) -> bool:
    """Validate email format using regex."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def filter_active_users(users: List[User]) -> List[User]:
    """Return only active users using list comprehension."""
    return [user for user in users if user.active]

@contextmanager
def database_connection(conn_string: str):
    """Context manager for database connections."""
    conn = create_connection(conn_string)
    try:
        yield conn
    finally:
        conn.close()
```

---

### SQL Review Patterns

**SQL Best Practices**
- [ ] Parameterized queries only
- [ ] Proper indexes on WHERE/JOIN columns
- [ ] LIMIT clauses on large queries
- [ ] Transactions for multi-step operations
- [ ] No SELECT * (specify columns)

**Good:**
```sql
-- Proper indexing and pagination
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_posts_user_created ON posts(user_id, created_at);

-- Efficient query with proper joins
SELECT
  u.id,
  u.name,
  u.email,
  COUNT(p.id) as post_count
FROM users u
LEFT JOIN posts p ON u.id = p.user_id
WHERE u.active = true
GROUP BY u.id, u.name, u.email
ORDER BY u.created_at DESC
LIMIT 20 OFFSET 0;

-- Transaction for consistency
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
```

---

## Review Process

### 1. File Change Analysis

```markdown
## Files Changed Analysis

### High Risk Files (require thorough review)
- Authentication/authorization code
- Database migrations
- Security configurations
- Payment processing
- Data encryption

### Medium Risk Files
- Business logic
- API endpoints
- Database queries
- External integrations

### Low Risk Files
- UI components
- Tests
- Documentation
- Configuration files
```

### 2. Impact Assessment

**Questions to Ask:**
- What is the blast radius of this change?
- Are there backward compatibility concerns?
- Does this require database migrations?
- Will this affect existing users?
- Are there performance implications?
- Does this change security posture?

### 3. Comment Generation Template

```markdown
## 🔴 Critical Issues (Must Fix)
- [ ] **Security**: [Description]
  ```suggestion
  [Suggested fix]
  ```

## 🟡 Important Issues (Should Fix)
- [ ] **Performance**: [Description]
  ```suggestion
  [Suggested fix]
  ```

## 🔵 Suggestions (Nice to Have)
- [ ] **Code Quality**: [Description]
  ```suggestion
  [Suggested fix]
  ```

## ✅ Positive Feedback
- Well-structured error handling
- Good test coverage
- Clear variable naming
```

### 4. Approval Criteria

**Approve when:**
- [ ] No critical security issues
- [ ] All tests passing
- [ ] Code coverage maintained/improved
- [ ] Documentation updated
- [ ] No performance regressions
- [ ] Accessibility requirements met
- [ ] Code follows style guide
- [ ] Changes are backward compatible (or migration plan exists)

**Request changes when:**
- Critical security vulnerabilities
- Failing tests
- Missing test coverage
- Breaking changes without migration
- Performance regressions
- Accessibility violations

---

## Common Issues Reference

### Security Issues
- Hardcoded secrets
- SQL injection vulnerabilities
- Missing authentication checks
- Insecure random number generation
- Sensitive data in logs
- Missing CSRF protection

### Performance Issues
- N+1 queries
- Missing database indexes
- Unnecessary re-renders (React)
- Large bundle sizes
- Synchronous operations blocking event loop
- Memory leaks

### Code Smells
- Functions > 50 lines
- Deeply nested conditionals (> 3 levels)
- Duplicate code
- Magic numbers
- Poor naming
- God objects

### Missing Error Handling
- Unhandled promise rejections
- Missing try/catch blocks
- No input validation
- Silent failures
- Generic error messages

### Incomplete Tests
- Missing edge cases
- No error scenario tests
- Flaky tests
- No integration tests
- Missing accessibility tests

---

## Review Workflow

1. **Initial Scan** (2 minutes)
   - Review PR description
   - Check file changes count
   - Identify high-risk files

2. **Deep Dive** (15-30 minutes)
   - Review each file systematically
   - Apply category checklists
   - Note issues with severity

3. **Testing Verification** (5 minutes)
   - Check test coverage
   - Verify tests are passing
   - Review test quality

4. **Documentation Check** (3 minutes)
   - Verify docs are updated
   - Check for breaking changes
   - Ensure examples are current

5. **Feedback Generation** (5 minutes)
   - Organize comments by severity
   - Provide code suggestions
   - Add positive feedback

6. **Decision** (1 minute)
   - Approve, request changes, or comment
   - Set follow-up items

---

## Tools Integration

### Automated Checks
- **ESLint/Prettier**: Code style
- **SonarQube**: Code quality metrics
- **Snyk/Dependabot**: Security vulnerabilities
- **Jest/Vitest**: Test coverage
- **Lighthouse**: Performance/accessibility
- **TypeScript**: Type safety

### Manual Review Focus
- Business logic correctness
- Architecture decisions
- Security implications
- User experience impact
- Code maintainability

---

## Conclusion

Effective code reviews balance thoroughness with efficiency. Use this skill as a checklist to ensure consistent, high-quality reviews that catch critical issues while fostering team learning and code improvement.

**Key Principles:**
- Security first
- Performance matters
- Accessibility is non-negotiable
- Quality over speed
- Constructive feedback
- Continuous improvement
