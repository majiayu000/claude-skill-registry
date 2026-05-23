---
name: sparc-refinement
description: SPARC Refinement phase specialist for iterative improvement through TDD, code optimization, refactoring, performance tuning, and quality improvement
version: 1.0.0
category: development
type: hybrid
capabilities:
  - code_optimization
  - test_development
  - refactoring
  - performance_tuning
  - quality_improvement
tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
  - mcp__claude-flow__memory_usage
  - mcp__claude-flow__task_orchestrate
related_skills:
  - sparc-specification
  - sparc-pseudocode
  - sparc-architecture
hooks:
  pre: |
    echo "SPARC Refinement phase initiated"
    memory_store "sparc_phase" "refinement"
    # Run initial tests
    npm test --if-present || echo "No tests yet"
  post: |
    echo "Refinement phase complete"
    # Run final test suite
    npm test || echo "Tests need attention"
    memory_store "refine_complete_$(date +%s)" "Code refined and tested"
---

# SPARC Refinement Agent

> Code refinement specialist focused on iterative improvement through testing, optimization, and refactoring for the SPARC methodology.

## Quick Start

```bash
# Invoke SPARC Refinement/TDD phase
npx claude-flow sparc tdd "Implement authentication service with tests"

# Or directly in Claude Code
# "Use SPARC refinement to implement login with TDD approach"
```

## When to Use

- Implementing features using Test-Driven Development (TDD)
- Refactoring code while maintaining test coverage
- Optimizing performance of existing code
- Improving error handling and resilience
- Enhancing code quality and documentation

## Prerequisites

- Completed architecture phase with clear component design
- Testing framework configured (Jest, pytest, etc.)
- Understanding of TDD red-green-refactor cycle
- Knowledge of code quality metrics

## Core Concepts

### SPARC Refinement Phase

The Refinement phase ensures code quality through:

1. **Test-Driven Development (TDD)** - Write tests first
2. **Code optimization and refactoring** - Improve structure
3. **Performance tuning** - Optimize hot paths
4. **Error handling improvement** - Robust failure recovery
5. **Documentation enhancement** - Keep docs current

### TDD Cycle

| Phase | Action | Goal |
|-------|--------|------|
| Red | Write failing test | Define expected behavior |
| Green | Write minimal code | Make test pass |
| Refactor | Improve code | Clean up while tests pass |

## Implementation Pattern

### Red Phase - Write Failing Tests

```typescript
// Step 1: Write test that defines desired behavior
describe('AuthenticationService', () => {
  let service: AuthenticationService;
  let mockUserRepo: jest.Mocked<UserRepository>;
  let mockCache: jest.Mocked<CacheService>;

  beforeEach(() => {
    mockUserRepo = createMockRepository();
    mockCache = createMockCache();
    service = new AuthenticationService(mockUserRepo, mockCache);
  });

  describe('login', () => {
    it('should return user and token for valid credentials', async () => {
      // Arrange
      const credentials = {
        email: 'user@example.com',
        password: 'SecurePass123!'
      };
      const mockUser = {
        id: 'user-123',
        email: credentials.email,
        passwordHash: await hash(credentials.password)
      };

      mockUserRepo.findByEmail.mockResolvedValue(mockUser);

      // Act
      const result = await service.login(credentials);

      // Assert
      expect(result).toHaveProperty('user');
      expect(result).toHaveProperty('token');
      expect(result.user.id).toBe(mockUser.id);
      expect(mockCache.set).toHaveBeenCalledWith(
        `session:${result.token}`,
        expect.any(Object),
        expect.any(Number)
      );
    });

    it('should lock account after 5 failed attempts', async () => {
      // This test will fail initially - driving implementation
      const credentials = {
        email: 'user@example.com',
        password: 'WrongPassword'
      };

      // Simulate 5 failed attempts
      for (let i = 0; i < 5; i++) {
        await expect(service.login(credentials))
          .rejects.toThrow('Invalid credentials');
      }

      // 6th attempt should indicate locked account
      await expect(service.login(credentials))
        .rejects.toThrow('Account locked due to multiple failed attempts');
    });
  });
});
```

### Green Phase - Make Tests Pass

```typescript
// Step 2: Implement minimum code to pass tests
export class AuthenticationService {
  private failedAttempts = new Map<string, number>();
  private readonly MAX_ATTEMPTS = 5;
  private readonly LOCK_DURATION = 15 * 60 * 1000; // 15 minutes

  constructor(
    private userRepo: UserRepository,
    private cache: CacheService,
    private logger: Logger
  ) {}

  async login(credentials: LoginDto): Promise<LoginResult> {
    const { email, password } = credentials;

    // Check if account is locked
    const attempts = this.failedAttempts.get(email) || 0;
    if (attempts >= this.MAX_ATTEMPTS) {
      throw new AccountLockedException(
        'Account locked due to multiple failed attempts'
      );
    }

    // Find user
    const user = await this.userRepo.findByEmail(email);
    if (!user) {
      this.recordFailedAttempt(email);
      throw new UnauthorizedException('Invalid credentials');
    }

    // Verify password
    const isValidPassword = await this.verifyPassword(
      password,
      user.passwordHash
    );
    if (!isValidPassword) {
      this.recordFailedAttempt(email);
      throw new UnauthorizedException('Invalid credentials');
    }

    // Clear failed attempts on successful login
    this.failedAttempts.delete(email);

    // Generate token and create session
    const token = this.generateToken(user);
    const session = {
      userId: user.id,
      email: user.email,
      createdAt: new Date()
    };

    await this.cache.set(
      `session:${token}`,
      session,
      this.SESSION_DURATION
    );

    return {
      user: this.sanitizeUser(user),
      token
    };
  }

  private recordFailedAttempt(email: string): void {
    const current = this.failedAttempts.get(email) || 0;
    this.failedAttempts.set(email, current + 1);

    this.logger.warn('Failed login attempt', {
      email,
      attempts: current + 1
    });
  }
}
```

### Refactor Phase - Improve Code Quality

```typescript
// Step 3: Refactor while keeping tests green
export class AuthenticationService {
  constructor(
    private userRepo: UserRepository,
    private cache: CacheService,
    private logger: Logger,
    private config: AuthConfig,
    private eventBus: EventBus
  ) {}

  async login(credentials: LoginDto): Promise<LoginResult> {
    // Extract validation to separate method
    await this.validateLoginAttempt(credentials.email);

    try {
      const user = await this.authenticateUser(credentials);
      const session = await this.createSession(user);

      // Emit event for other services
      await this.eventBus.emit('user.logged_in', {
        userId: user.id,
        timestamp: new Date()
      });

      return {
        user: this.sanitizeUser(user),
        token: session.token,
        expiresAt: session.expiresAt
      };
    } catch (error) {
      await this.handleLoginFailure(credentials.email, error);
      throw error;
    }
  }

  private async validateLoginAttempt(email: string): Promise<void> {
    const lockInfo = await this.cache.get(`lock:${email}`);
    if (lockInfo) {
      const remainingTime = this.calculateRemainingLockTime(lockInfo);
      throw new AccountLockedException(
        `Account locked. Try again in ${remainingTime} minutes`
      );
    }
  }

  private async authenticateUser(credentials: LoginDto): Promise<User> {
    const user = await this.userRepo.findByEmail(credentials.email);
    if (!user || !await this.verifyPassword(credentials.password, user.passwordHash)) {
      throw new UnauthorizedException('Invalid credentials');
    }
    return user;
  }

  private async handleLoginFailure(email: string, error: Error): Promise<void> {
    if (error instanceof UnauthorizedException) {
      const attempts = await this.incrementFailedAttempts(email);

      if (attempts >= this.config.maxLoginAttempts) {
        await this.lockAccount(email);
      }
    }
  }
}
```

## Configuration

```yaml
# sparc-refinement-config.yaml
tdd_settings:
  cycle: "red-green-refactor"
  coverage_threshold: 80
  test_framework: "jest"

refactoring:
  max_complexity: 10
  max_file_lines: 500
  max_function_lines: 30

performance:
  benchmark_enabled: true
  profiling_enabled: true

quality_metrics:
  code_coverage: 80
  cyclomatic_complexity: 10
  maintainability_index: 20
```

## Usage Examples

### Example 1: Performance Optimization

```typescript
// Before: N database queries
async function getUserPermissions(userId: string): Promise<string[]> {
  const user = await db.query('SELECT * FROM users WHERE id = ?', [userId]);
  const roles = await db.query('SELECT * FROM user_roles WHERE user_id = ?', [userId]);
  const permissions = [];

  for (const role of roles) {
    const perms = await db.query('SELECT * FROM role_permissions WHERE role_id = ?', [role.id]);
    permissions.push(...perms);
  }

  return permissions;
}

// After: Single optimized query with caching
async function getUserPermissions(userId: string): Promise<string[]> {
  // Check cache first
  const cached = await cache.get(`permissions:${userId}`);
  if (cached) return cached;

  // Single query with joins
  const permissions = await db.query(`
    SELECT DISTINCT p.name
    FROM users u
    JOIN user_roles ur ON u.id = ur.user_id
    JOIN role_permissions rp ON ur.role_id = rp.role_id
    JOIN permissions p ON rp.permission_id = p.id
    WHERE u.id = ?
  `, [userId]);

  // Cache for 5 minutes
  await cache.set(`permissions:${userId}`, permissions, 300);

  return permissions;
}
```

### Example 2: Error Handling

```typescript
// Define custom error hierarchy
export class AppError extends Error {
  constructor(
    message: string,
    public code: string,
    public statusCode: number,
    public isOperational = true
  ) {
    super(message);
    Object.setPrototypeOf(this, new.target.prototype);
    Error.captureStackTrace(this);
  }
}

export class ValidationError extends AppError {
  constructor(message: string, public fields?: Record<string, string>) {
    super(message, 'VALIDATION_ERROR', 400);
  }
}

export class AuthenticationError extends AppError {
  constructor(message: string = 'Authentication required') {
    super(message, 'AUTHENTICATION_ERROR', 401);
  }
}

// Global error handler
export function errorHandler(
  error: Error,
  req: Request,
  res: Response,
  next: NextFunction
): void {
  if (error instanceof AppError && error.isOperational) {
    res.status(error.statusCode).json({
      error: {
        code: error.code,
        message: error.message,
        ...(error instanceof ValidationError && { fields: error.fields })
      }
    });
  } else {
    // Unexpected errors
    logger.error('Unhandled error', { error, request: req });
    res.status(500).json({
      error: {
        code: 'INTERNAL_ERROR',
        message: 'An unexpected error occurred'
      }
    });
  }
}
```

### Example 3: Circuit Breaker Pattern

```typescript
// Circuit breaker for external services
export class CircuitBreaker {
  private failures = 0;
  private lastFailureTime?: Date;
  private state: 'CLOSED' | 'OPEN' | 'HALF_OPEN' = 'CLOSED';

  constructor(
    private threshold = 5,
    private timeout = 60000 // 1 minute
  ) {}

  async execute<T>(operation: () => Promise<T>): Promise<T> {
    if (this.state === 'OPEN') {
      if (this.shouldAttemptReset()) {
        this.state = 'HALF_OPEN';
      } else {
        throw new Error('Circuit breaker is OPEN');
      }
    }

    try {
      const result = await operation();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  private onSuccess(): void {
    this.failures = 0;
    this.state = 'CLOSED';
  }

  private onFailure(): void {
    this.failures++;
    this.lastFailureTime = new Date();

    if (this.failures >= this.threshold) {
      this.state = 'OPEN';
    }
  }

  private shouldAttemptReset(): boolean {
    return this.lastFailureTime
      && (Date.now() - this.lastFailureTime.getTime()) > this.timeout;
  }
}
```

### Example 4: Complexity Reduction

```typescript
// Bad: Cyclomatic complexity = 7
function processUser(user: User): void {
  if (user.age > 18) {
    if (user.country === 'US') {
      if (user.hasSubscription) {
        // Process premium US adult
      } else {
        // Process free US adult
      }
    } else {
      if (user.hasSubscription) {
        // Process premium international adult
      } else {
        // Process free international adult
      }
    }
  } else {
    // Process minor
  }
}

// Good: Cyclomatic complexity = 2
function processUser(user: User): void {
  const processor = getUserProcessor(user);
  processor.process(user);
}

function getUserProcessor(user: User): UserProcessor {
  const type = getUserType(user);
  return ProcessorFactory.create(type);
}
```

## Execution Checklist

- [ ] Write failing tests for new functionality (Red)
- [ ] Implement minimum code to pass tests (Green)
- [ ] Refactor while keeping tests green (Refactor)
- [ ] Optimize performance of hot paths
- [ ] Add comprehensive error handling
- [ ] Implement retry logic and circuit breakers
- [ ] Verify code coverage >= 80%
- [ ] Check cyclomatic complexity < 10
- [ ] Run full test suite
- [ ] Update documentation

## Best Practices

1. **Test First**: Always write tests before implementation
2. **Small Steps**: Make incremental improvements
3. **Continuous Refactoring**: Improve code structure continuously
4. **Performance Budgets**: Set and monitor performance targets
5. **Error Recovery**: Plan for failure scenarios
6. **Documentation**: Keep docs in sync with code

## Error Handling

| Issue | Resolution |
|-------|------------|
| Tests failing after refactor | Revert and make smaller changes |
| Low code coverage | Add tests for uncovered paths |
| High complexity | Extract methods, use patterns |
| Performance regression | Profile and optimize hot paths |

## Metrics & Success Criteria

```javascript
// Jest configuration for coverage
module.exports = {
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    }
  },
  coveragePathIgnorePatterns: [
    '/node_modules/',
    '/test/',
    '/dist/'
  ]
};
```

- Code coverage: >= 80%
- Cyclomatic complexity: < 10
- All tests passing
- No performance regressions
- Error handling for all failure paths

## Integration Points

### MCP Tools

```javascript
// Store refinement phase progress
mcp__claude-flow__memory_usage {
  action: "store",
  key: "sparc/refinement/metrics",
  namespace: "coordination",
  value: JSON.stringify({
    coverage: 85,
    testsPass: true,
    complexity: 8,
    timestamp: Date.now()
  })
}
```

### Hooks

```bash
# Pre-refinement hook (run tests)
npx claude-flow@alpha hooks pre-task --description "SPARC Refinement phase"
npm test --if-present

# Post-refinement hook (verify coverage)
npx claude-flow@alpha hooks post-task --task-id "refine-complete"
npm run test:coverage
```

### Related Skills

- [sparc-specification](../sparc-specification/SKILL.md) - Requirements phase
- [sparc-pseudocode](../sparc-pseudocode/SKILL.md) - Algorithm design phase
- [sparc-architecture](../sparc-architecture/SKILL.md) - System design phase

## References

- [SPARC Methodology](https://github.com/ruvnet/claude-flow)
- [Test-Driven Development](https://martinfowler.com/bliki/TestDrivenDevelopment.html)
- [Refactoring Guru](https://refactoring.guru/)
- [Jest Documentation](https://jestjs.io/docs/getting-started)

## Version History

- **1.0.0** (2026-01-02): Initial release - converted from agent to skill format
