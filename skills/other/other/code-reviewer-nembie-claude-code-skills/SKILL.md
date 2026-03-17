---
name: code-reviewer
description: Automated code review for security, performance, and maintainability. Use when asked for code review, security audit, quality check, PR review, or to find issues in code.
---

# Code Reviewer

Before generating any output, read `config/defaults.md` and adapt all patterns, imports, and code examples to the user's configured stack.

## Review Process

1. Read all files in scope (specified files, PR diff, or project)
2. Analyze each file against the review categories below
3. Output structured findings with severity levels
4. Provide actionable fix suggestions

## Review Categories

### Security

#### Injection Vulnerabilities
```typescript
// BAD: SQL injection
const query = `SELECT * FROM users WHERE id = ${userId}`;

// GOOD: Parameterized query
const user = await prisma.user.findUnique({ where: { id: userId } });
```

#### XSS (Cross-Site Scripting)
```typescript
// BAD: Rendering unsanitized HTML
<div dangerouslySetInnerHTML={{ __html: userContent }} />

// GOOD: Sanitize or use text content
<div>{sanitizeHtml(userContent)}</div>
// Or just render as text
<div>{userContent}</div>
```

#### Authentication Leaks
```typescript
// BAD: Exposing sensitive data
return NextResponse.json({ user: { ...user, password: user.password } });

// GOOD: Exclude sensitive fields
const { password, ...safeUser } = user;
return NextResponse.json({ user: safeUser });
```

#### Hardcoded Secrets
```typescript
// BAD
const API_KEY = 'sk-1234567890abcdef';

// GOOD
const API_KEY = process.env.API_KEY;
```

#### Path Traversal
```typescript
// BAD: User-controlled file path
const filePath = `./uploads/${req.query.filename}`;

// GOOD: Validate and sanitize
const filename = path.basename(req.query.filename);
const filePath = path.join('./uploads', filename);
```

### Performance

#### N+1 Queries
See prisma-query-optimizer skill for detection patterns.

#### Memory Leaks
```typescript
// BAD: Event listener not cleaned up
useEffect(() => {
  window.addEventListener('resize', handleResize);
}, []);

// GOOD: Cleanup on unmount
useEffect(() => {
  window.addEventListener('resize', handleResize);
  return () => window.removeEventListener('resize', handleResize);
}, []);
```

#### Unbounded Operations
```typescript
// BAD: Loading all records
const allUsers = await prisma.user.findMany();

// GOOD: Paginate
const users = await prisma.user.findMany({ take: 50, skip: offset });
```

#### Synchronous File I/O
```typescript
// BAD: Blocks event loop
const data = fs.readFileSync('large-file.json');

// GOOD: Async I/O
const data = await fs.promises.readFile('large-file.json');
```

### Maintainability

#### Magic Numbers
```typescript
// BAD
if (status === 3) { ... }

// GOOD
const STATUS_COMPLETED = 3;
if (status === STATUS_COMPLETED) { ... }

// BETTER: Use enum or const object
const Status = { COMPLETED: 3 } as const;
```

#### Deep Nesting
```typescript
// BAD: Arrow code
if (user) {
  if (user.isActive) {
    if (user.hasPermission('write')) {
      // ...
    }
  }
}

// GOOD: Early returns
if (!user) return;
if (!user.isActive) return;
if (!user.hasPermission('write')) return;
// ...
```

#### God Functions
Functions over 50 lines or with more than 5 parameters should be broken down.

#### Dead Code
Unused imports, unreachable code after return/throw, commented-out code blocks.

### Naming Conventions

#### Inconsistent Naming
```typescript
// BAD: Mixed styles
const user_name = '...';
const userEmail = '...';
const UserAge = 25;

// GOOD: Consistent camelCase for variables
const userName = '...';
const userEmail = '...';
const userAge = 25;
```

#### Unclear Names
```typescript
// BAD
const d = new Date();
const arr = users.filter(u => u.a);

// GOOD
const createdAt = new Date();
const activeUsers = users.filter(user => user.isActive);
```

### Error Handling

#### Swallowed Errors
```typescript
// BAD: Silent failure
try {
  await saveData();
} catch (e) {
  // Nothing
}

// GOOD: Log or handle
try {
  await saveData();
} catch (error) {
  console.error('Failed to save:', error);
  throw error; // Or handle appropriately
}
```

#### Generic Catch
```typescript
// BAD: Catches everything including programming errors
try {
  doSomething();
} catch (e) {
  return defaultValue;
}

// GOOD: Catch specific errors
try {
  doSomething();
} catch (error) {
  if (error instanceof NetworkError) {
    return defaultValue;
  }
  throw error;
}
```

### Test Coverage Gaps

#### Untested Edge Cases
Flag functions that handle:
- Null/undefined inputs without tests
- Empty arrays/objects without tests
- Error conditions without tests
- Boundary values without tests

#### Missing Integration Tests
API routes and database operations should have integration tests.

## Output Format

```
## Code Review Report

### Critical (must fix before merge)
| Severity | File | Line | Issue | Category |
|----------|------|------|-------|----------|
| CRITICAL | src/api/users.ts | 45 | SQL injection vulnerability | Security |

**Details:**
- Issue: User input directly interpolated into query string
- Fix: Use parameterized queries via Prisma
```typescript
// Before
const query = `SELECT * FROM users WHERE email = '${email}'`;

// After
const user = await prisma.user.findUnique({ where: { email } });
```

### Warnings (should fix)
| Severity | File | Line | Issue | Category |
|----------|------|------|-------|----------|
| WARNING | src/hooks/useData.ts | 23 | Missing cleanup in useEffect | Performance |

### Info (suggestions)
| Severity | File | Line | Issue | Category |
|----------|------|------|-------|----------|
| INFO | src/utils/format.ts | 12 | Magic number should be named constant | Maintainability |

### Summary
- Critical: X issues
- Warnings: X issues
- Info: X issues
- Files reviewed: X
```

## Severity-Based Prioritization

After completing the review, sort all findings by severity. If any critical security issue is found, prepend a prominent warning at the top of the output: `⚠ CRITICAL SECURITY ISSUE — address before anything else.` Do not bury critical findings in a long list of minor style suggestions. If there are more than 15 findings, group by severity and show only critical + warning by default, with info-level findings in a collapsed section.

## Reference

See `references/review-checklist.md` for the complete review criteria organized by category.
