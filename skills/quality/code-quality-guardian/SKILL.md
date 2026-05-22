---
name: code-quality-guardian
description: Expert code reviewer that enforces best practices, clean code principles, strong typing (TypeScript), architecture guidelines, and security standards. Reviews PRs and code snippets for bugs, code smells, anti-patterns, maintainability risks, performance issues, and security vulnerabilities. Use when reviewing pull requests, analyzing code quality, conducting code audits, or improving TypeScript/JavaScript codebases.
license: Apache-2.0
---

# Code Quality Guardian

## Overview

An expert code reviewer that provides comprehensive, educational feedback on code quality, security, performance, and maintainability. Focuses on TypeScript/JavaScript with strong typing emphasis, but applicable to multiple languages.

## Core Review Process

### Step 1: Initial Analysis
Scan code for immediate issues:
- Syntax errors and compilation failures
- Security vulnerabilities (hardcoded secrets, injection risks)
- Critical bugs that could cause runtime failures
- Type safety violations

### Step 2: Deep Quality Review
Analyze code structure and patterns:
- Code smells and anti-patterns
- Architecture consistency
- Design pattern violations
- Complexity and maintainability
- Test coverage gaps

### Step 3: Educational Feedback
Provide constructive explanations:
- WHY issues matter (not just WHAT is wrong)
- Impact on maintainability, performance, security
- Concrete examples of better approaches
- Learning resources when appropriate

---

## TypeScript & Strong Typing Standards

### Critical Type Safety Rules

**1. ALWAYS Enable Strict Mode**
```typescript
// tsconfig.json - REQUIRED settings
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictPropertyInitialization": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true
  }
}
```

**Why**: Catches 80% of common bugs at compile time. Prevents undefined/null errors, ensures type consistency.

**2. Never Use `any` - Use `unknown` Instead**
```typescript
// ❌ BAD - Disables all type checking
function processData(data: any) {
  return data.value.toUpperCase(); // No safety!
}

// ✅ GOOD - Safe with type guards
function processData(data: unknown) {
  if (typeof data === 'object' && data !== null && 'value' in data) {
    const value = (data as { value: string }).value;
    return typeof value === 'string' ? value.toUpperCase() : '';
  }
  throw new Error('Invalid data structure');
}
```

**Why**: `unknown` forces explicit type checking, preventing runtime type errors.

**3. Explicit Function Signatures**
```typescript
// ❌ BAD - Implicit return type
function calculateTotal(items) {
  return items.reduce((sum, item) => sum + item.price, 0);
}

// ✅ GOOD - Explicit types for clarity and safety
interface Item {
  price: number;
  name: string;
}

function calculateTotal(items: Item[]): number {
  return items.reduce((sum, item) => sum + item.price, 0);
}
```

**Why**: Acts as guardrail for refactoring. Prevents accidental return type changes.

**4. Use Interfaces Over Type Aliases for Objects**
```typescript
// ❌ LESS IDEAL - Type alias
type User = {
  id: string;
  name: string;
  email: string;
};

// ✅ BETTER - Interface (more extensible)
interface User {
  readonly id: string;
  name: string;
  email: string;
}

interface AdminUser extends User {
  permissions: string[];
}
```

**Why**: Interfaces can be extended, provide better error messages, and are cached by compiler.

**5. Immutability with `readonly`**
```typescript
// ✅ Prevent accidental mutations
interface Config {
  readonly apiUrl: string;
  readonly timeout: number;
  settings: {
    readonly maxRetries: number;
  };
}

// Use ReadonlyArray for array immutability
function processItems(items: ReadonlyArray<string>): void {
  // items.push('new'); // ❌ Error: Property 'push' does not exist
  const newItems = [...items, 'new']; // ✅ Create new array
}
```

**Why**: Prevents bugs from unexpected mutations, especially important in React/Redux.

**6. Proper Error Handling - Result Types**
```typescript
// ❌ BAD - Throws are not visible in types
function parseUser(data: string): User {
  if (!data) throw new Error('Empty data');
  return JSON.parse(data);
}

// ✅ GOOD - Errors are part of the type signature
type Result<T, E> = 
  | { success: true; data: T }
  | { success: false; error: E };

function parseUser(data: string): Result<User, string> {
  if (!data) {
    return { success: false, error: 'Empty data' };
  }
  try {
    const parsed = JSON.parse(data);
    return { success: true, data: parsed };
  } catch (e) {
    return { success: false, error: 'Invalid JSON' };
  }
}

// Usage - compiler forces error handling
const result = parseUser(input);
if (result.success) {
  console.log(result.data.name); // Safe access
} else {
  console.error(result.error); // Must handle error
}
```


**Why**: Type-safe error handling prevents unhandled exceptions and makes error paths explicit.

---

## Code Quality Review Template

When reviewing code, provide feedback in this structure:

### ✅ **Strengths**
Highlight what's done well:
- Good patterns and practices used
- Well-structured code
- Effective solutions

### 🚨 **Critical Issues** (Must Fix)
Issues that will cause bugs or security problems:
- Security vulnerabilities
- Type safety violations
- Logic errors
- Data corruption risks

### ⚠️ **Major Issues** (Should Fix)
Significant quality or maintainability problems:
- Code smells and anti-patterns
- Poor error handling
- Tight coupling
- Missing tests for critical logic

### 💡 **Minor Issues** (Nice to Have)
Improvements for better code quality:
- Naming improvements
- Simplification opportunities
- Documentation gaps
- Style inconsistencies

### 📚 **Recommendations**
Concrete, actionable improvements with examples.

---

## Common Code Smells to Flag

### 1. Long Methods (>30 lines)
**Smell**: Method doing too much
**Fix**: Extract smaller, focused functions
**Impact**: Hard to test, understand, maintain

### 2. God Objects (>10 responsibilities)
**Smell**: Class knows/does too much
**Fix**: Single Responsibility Principle - split into focused classes
**Impact**: Hard to test, high coupling

### 3. Deep Nesting (>3 levels)
**Smell**: Complex conditional logic
**Fix**: Early returns, extract conditions, guard clauses
**Impact**: Hard to read, error-prone

### 4. Duplicate Code
**Smell**: Same logic in multiple places
**Fix**: Extract to shared function/utility
**Impact**: Maintenance burden, inconsistent behavior

### 5. Magic Numbers/Strings
**Smell**: Hardcoded values without context
**Fix**: Named constants with clear meaning
**Impact**: Unclear intent, hard to change

### 6. Mutable Shared State
**Smell**: Global variables or mutable shared objects
**Fix**: Immutable data, dependency injection
**Impact**: Unpredictable behavior, hard to test

---

## Security Checklist

Always check for these vulnerabilities:

### Input Validation
- [ ] User input is validated before processing
- [ ] SQL injection protection (parameterized queries)
- [ ] XSS prevention (proper escaping)
- [ ] Path traversal protection
- [ ] File upload validation (type, size)

### Authentication & Authorization
- [ ] Passwords are hashed (bcrypt, argon2)
- [ ] No hardcoded credentials
- [ ] Proper session management
- [ ] Authorization checks on sensitive operations
- [ ] Rate limiting on auth endpoints

### Data Protection
- [ ] Sensitive data encrypted at rest
- [ ] TLS/HTTPS for data in transit
- [ ] No sensitive data in logs
- [ ] Secure environment variable usage
- [ ] No secrets in version control

### Dependencies
- [ ] Dependencies regularly updated
- [ ] Known vulnerabilities checked
- [ ] Minimal dependency footprint
- [ ] License compatibility verified

---

## Performance Optimization Patterns

### Database Access
```typescript
// ❌ BAD - N+1 query problem
async function getUsersWithPosts() {
  const users = await db.users.findAll();
  for (const user of users) {
    user.posts = await db.posts.findByUser(user.id); // N queries!
  }
  return users;
}

// ✅ GOOD - Single query with join
async function getUsersWithPosts() {
  return db.users.findAll({
    include: [{ model: db.posts }]
  });
}
```

### Caching
```typescript
// ✅ Memoization for expensive computations
const memoize = <T extends (...args: any[]) => any>(fn: T): T => {
  const cache = new Map();
  return ((...args: any[]) => {
    const key = JSON.stringify(args);
    if (cache.has(key)) return cache.get(key);
    const result = fn(...args);
    cache.set(key, result);
    return result;
  }) as T;
};

const expensiveCalculation = memoize((n: number) => {
  // Complex calculation
  return result;
});
```

### Lazy Loading
```typescript
// ✅ Load heavy resources only when needed
class DataProcessor {
  private _heavyLibrary?: HeavyLibrary;
  
  private get heavyLibrary(): HeavyLibrary {
    if (!this._heavyLibrary) {
      this._heavyLibrary = new HeavyLibrary();
    }
    return this._heavyLibrary;
  }
  
  process(data: Data) {
    if (data.requiresHeavyProcessing) {
      return this.heavyLibrary.process(data);
    }
    return this.lightweightProcess(data);
  }
}
```

---

## Testing Best Practices

### Test Structure (AAA Pattern)
```typescript
describe('UserService', () => {
  it('should create user with valid data', async () => {
    // Arrange - Set up test data
    const userData = {
      name: 'John Doe',
      email: 'john@example.com'
    };
    
    // Act - Execute the operation
    const user = await userService.createUser(userData);
    
    // Assert - Verify the results
    expect(user.id).toBeDefined();
    expect(user.name).toBe(userData.name);
    expect(user.email).toBe(userData.email);
  });
});
```

### Test Coverage Priorities
1. **Critical business logic** (payment, auth, data integrity)
2. **Edge cases** (empty input, null, boundary values)
3. **Error paths** (invalid input, exceptions)
4. **Integration points** (API calls, database operations)

### Test Quality Indicators
- ✅ Tests are independent and isolated
- ✅ Tests are fast (<1s for unit tests)
- ✅ Tests have clear, descriptive names
- ✅ Tests verify behavior, not implementation
- ✅ Tests are maintainable and readable

---

## Architecture Patterns

### Dependency Injection
```typescript
// ✅ GOOD - Dependencies injected, testable
interface UserRepository {
  findById(id: string): Promise<User | null>;
  save(user: User): Promise<void>;
}

class UserService {
  constructor(
    private readonly userRepo: UserRepository,
    private readonly emailService: EmailService
  ) {}
  
  async registerUser(data: UserData): Promise<User> {
    const user = await this.userRepo.save(data);
    await this.emailService.sendWelcome(user.email);
    return user;
  }
}
```

### Repository Pattern
```typescript
// Separate data access from business logic
interface Repository<T> {
  findById(id: string): Promise<T | null>;
  findAll(): Promise<T[]>;
  save(entity: T): Promise<T>;
  delete(id: string): Promise<void>;
}

class UserRepository implements Repository<User> {
  // Implementation specific to User data access
}
```

### SOLID Principles
- **Single Responsibility**: One reason to change
- **Open/Closed**: Open for extension, closed for modification
- **Liskov Substitution**: Subtypes must be substitutable for base types
- **Interface Segregation**: Many specific interfaces > one general
- **Dependency Inversion**: Depend on abstractions, not concretions

---

## Clean Code Principles

### Naming Conventions
```typescript
// ✅ GOOD - Clear, intention-revealing names
const activeUserCount = users.filter(u => u.isActive).length;
const isEligibleForDiscount = (user: User) => user.orderCount > 10;

// ❌ BAD - Unclear abbreviations
const cnt = users.filter(u => u.a).length;
const check = (u: User) => u.oc > 10;
```

### Function Size
- **Target**: 5-15 lines per function
- **Maximum**: 30 lines (if exceeded, refactor)
- **Single Level of Abstraction**: Don't mix high and low level operations

### Comment Guidelines
```typescript
// ❌ BAD - Redundant comment
// Set user name
user.name = newName;

// ✅ GOOD - Explains WHY, not WHAT
// We normalize to lowercase because our database 
// has case-sensitive collation
user.email = email.toLowerCase();

// ✅ GOOD - Documents complex business logic
/**
 * Calculates discount based on order history.
 * Premium users (>10 orders) get 15% off.
 * Regular users (3-10 orders) get 5% off.
 * New users get free shipping on first order.
 */
function calculateDiscount(user: User, order: Order): number {
  // Implementation
}
```

---

## References

For detailed information, see reference files:
- `references/SECURITY_PATTERNS.md` - Comprehensive security guidelines
- `references/TYPESCRIPT_ADVANCED.md` - Advanced TypeScript patterns
- `references/REFACTORING_CATALOG.md` - Common refactoring techniques

---

## Review Workflow

1. **Understand Context**: What is the code trying to achieve?
2. **Quick Scan**: Look for critical issues first
3. **Deep Analysis**: Review structure, patterns, quality
4. **Prioritize Feedback**: Critical → Major → Minor
5. **Be Educational**: Explain WHY, provide examples
6. **Stay Constructive**: Suggest solutions, not just problems

---

## Example Review Output

```markdown
## Code Review: UserService.ts

### ✅ Strengths
- Good use of dependency injection for testability
- Clear function names and structure
- Proper error handling with Result type

### 🚨 Critical Issues

**Security: SQL Injection Risk** (Line 45)
Current code:
```typescript
db.query(`SELECT * FROM users WHERE email = '${email}'`)
```

Problem: Direct string concatenation allows SQL injection attacks.

Fix:
```typescript
db.query('SELECT * FROM users WHERE email = ?', [email])
```

**Type Safety: Implicit `any`** (Line 67)
The `processData` function parameter has implicit `any` type, disabling type checking.

Fix: Add explicit type annotation:
```typescript
function processData(data: UserData): Result<ProcessedData, Error>
```

### ⚠️ Major Issues

**Code Smell: God Object** (UserService class)
The UserService handles authentication, email, database operations, and business logic. 
This violates Single Responsibility Principle.

Recommendation: Split into focused services:
- AuthenticationService
- UserRepository
- EmailService
- UserBusinessLogic

### 💡 Minor Issues

**Naming: Unclear variable** (Line 23)
`const temp` doesn't reveal intent.

Suggestion: `const normalizedEmail` or `const sanitizedInput`

**Performance: Unnecessary array iteration** (Line 89)
Using `.map().filter()` creates intermediate array.

Optimization:
```typescript
// Instead of:
users.map(u => u.email).filter(e => e.includes('@'));

// Use:
users.filter(u => u.email.includes('@')).map(u => u.email);
```

### 📚 Recommendations

1. **Add Unit Tests**: Critical authentication logic lacks test coverage
2. **Error Logging**: Add structured logging for debugging
3. **Input Validation**: Use Zod or similar for runtime validation
4. **Documentation**: Add JSDoc for public API methods

Overall: Good foundation with some critical security issues to address.
Priority: Fix SQL injection and type safety issues before merge.
```

---

## Usage Tips

- **For PR Reviews**: Focus on changes, not entire codebase
- **For Refactoring**: Identify code smells systematically
- **For New Code**: Check patterns and architecture early
- **For Learning**: Use reviews as teaching moments

---

**Remember**: The goal is to help developers write better code through clear, 
constructive, educational feedback. Focus on impact and provide actionable solutions.
