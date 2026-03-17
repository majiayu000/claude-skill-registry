---
name: backend-simplicity-engineer
description: Backend engineer focused on simplicity, bug elimination, and clean code. Use when user mentions "simplify backend", "fix backend bugs", "clean up code", or "make backend perfect".
version: 1.0.0
agents: [codex-deep-research, gemini-research-analyst]
---

# Backend Simplicity Engineer

**Philosophy: Simple, bug-free, maintainable code. Zero complexity for complexity's sake.**

## When to Use

Invoke this skill when:
- User mentions: "simplify backend", "fix bugs", "clean up code"
- Backend has complex, hard-to-understand code
- Too many abstractions or over-engineering
- Bug reports or error logs
- Performance issues
- Code review before deployment

## Simplicity-First Methodology

### Core Principles

1. **KISS** - Keep It Simple, Stupid
2. **YAGNI** - You Aren't Gonna Need It
3. **DRY** - Don't Repeat Yourself (but don't over-abstract)
4. **Zero Bugs** - Test everything, fix immediately
5. **Readable** - Code is read 10x more than written

### Phase 1: Code Complexity Audit

**1A. Cyclomatic Complexity Check**
```bash
# Find overly complex functions
# Complexity > 10 = needs refactoring

# Simple check: count if/else/while/for/switch
grep -rn "if\|else\|while\|for\|switch" src/ --include="*.ts" | \
  awk -F: '{print $1}' | uniq -c | sort -rn | head -20

# Look for deeply nested code (>3 levels)
grep -rn "    if.*if.*if" src/ --include="*.ts"
```

**1B. Code Duplication Detection**
```bash
# Find duplicate code blocks
# Use: jscpd (install: npm i -g jscpd)
npx jscpd src/ --min-lines 5 --min-tokens 50

# Manual check for similar patterns
grep -rn "export.*function" src/ --include="*.ts" | \
  awk -F: '{print $3}' | sort | uniq -c | sort -rn
```

**1C. Dependency Graph Analysis**
```typescript
// Check for circular dependencies
// Use: madge (install: npm i -g madge)
// npx madge --circular src/

// Check for God Objects (too many dependencies)
// File with >10 imports = probably doing too much
grep -c "^import" src/**/*.ts | awk -F: '$2 > 10 {print $1 " has " $2 " imports"}'
```

### Phase 2: Research Simplification Patterns

**Launch codex-deep-research agent**:
```markdown
Invoke Task tool with subagent_type="codex-deep-research"

Prompt:
"Research the best code simplification patterns and refactoring techniques for a TypeScript + Express.js backend.

Context:
- Project Conductor has 12 APIs, 100+ endpoints
- Uses: Express.js, PostgreSQL, Redis, Socket.io
- Current issues: Too many 'any' types, console.log usage, complex controllers
- Goal: Simple, maintainable, bug-free code

Provide refactoring patterns for:

1. **Controller Simplification**
   - How to keep controllers thin (max 20 lines per method)
   - Single responsibility principle
   - Proper error handling without try-catch hell
   - Input validation patterns

2. **Service Layer Organization**
   - When to create a service vs inline logic
   - Avoiding God Services
   - Dependency injection patterns
   - Testing strategies

3. **Error Handling**
   - Centralized error handling
   - Custom error classes vs generic
   - Error logging best practices
   - User-friendly error messages

4. **Database Queries**
   - Query builders vs raw SQL
   - Connection pool management
   - Transaction patterns
   - Avoiding N+1 queries

5. **Code Organization**
   - File structure conventions
   - Module boundaries
   - When to split vs combine
   - Import/export patterns

6. **TypeScript Best Practices**
   - Eliminating 'any' types
   - Proper type inference
   - Generics vs type assertions
   - Interface vs type

7. **Testing for Simplicity**
   - Unit test patterns
   - Mocking strategies
   - Integration test boundaries
   - Test coverage targets

Provide before/after code examples for each pattern."
```

**Check for AI code analysis tools**:
```markdown
Invoke Task tool with subagent_type="gemini-research-analyst"

Prompt:
"Research if Google's Gemini AI provides any code simplification, refactoring, or quality analysis tools for TypeScript backends.

Investigate:
1. Gemini-powered code review
2. Automated refactoring suggestions
3. Complexity analysis
4. Bug detection
5. Performance profiling
6. Security vulnerability scanning
7. Code generation (to replace boilerplate)

If available:
- How to integrate with TypeScript + Express.js
- Accuracy compared to ESLint/SonarQube
- Cost and performance
- Production readiness"
```

### Phase 3: Bug Hunting & Elimination

**3A. Runtime Error Detection**
```bash
# Check logs for errors
if [ -f logs/error.log ]; then
  echo "Recent errors:"
  tail -100 logs/error.log | grep -i "error\|exception\|failed"
fi

# Check for unhandled promise rejections
grep -rn "Promise\|async" src/ --include="*.ts" | \
  xargs -I {} sh -c 'echo {}; grep -A 5 "{}" | grep -c "catch"'

# Find missing await keywords
grep -rn "async function" src/ --include="*.ts" -A 10 | \
  grep -v "await" | grep -B 1 "Promise"
```

**3B. Type Safety Issues**
```bash
# Find all 'any' types (must be eliminated)
grep -rn ": any" src/ --include="*.ts" | wc -l
# Goal: 0

# Find implicit any
npx tsc --noImplicitAny --noEmit

# Find non-null assertions (! operator - dangerous)
grep -rn "!" src/ --include="*.ts" | grep -v "!=" | grep -v "!==" | wc -l
# Goal: <5
```

**3C. Common Bug Patterns**
```typescript
// Pattern 1: Missing null checks
// Bad
function getUser(id: string) {
  const user = users.find(u => u.id === id);
  return user.name; // Error if user is undefined
}

// Good
function getUser(id: string) {
  const user = users.find(u => u.id === id);
  if (!user) {
    throw new NotFoundError(`User ${id} not found`);
  }
  return user.name;
}

// Pattern 2: Async/await missing
// Bad
function loadData() {
  fetchData().then(data => {
    processData(data).then(result => {
      saveData(result); // Callback hell
    });
  });
}

// Good
async function loadData() {
  const data = await fetchData();
  const result = await processData(data);
  await saveData(result);
}

// Pattern 3: Error swallowing
// Bad
try {
  await riskyOperation();
} catch (error) {
  // Silently fails - very bad!
}

// Good
try {
  await riskyOperation();
} catch (error) {
  logger.error('Risky operation failed', { error });
  throw new OperationError('Failed to complete operation', { cause: error });
}

// Pattern 4: Race conditions
// Bad
let counter = 0;
async function increment() {
  const current = counter;
  await delay(100);
  counter = current + 1; // Lost updates!
}

// Good
let counter = 0;
const lock = new Mutex();
async function increment() {
  await lock.acquire();
  try {
    counter++;
  } finally {
    lock.release();
  }
}
```

### Phase 4: Simplification Refactoring

**4A. Controller Simplification**
```typescript
// BEFORE: Complex controller (60 lines, multiple responsibilities)
export class RequirementsController {
  async getRequirements(req: Request, res: Response) {
    try {
      const page = parseInt(req.query.page as string) || 1;
      const limit = parseInt(req.query.limit as string) || 10;
      const sortBy = (req.query.sortBy as string) || 'createdAt';
      const sortOrder = (req.query.sortOrder as 'asc' | 'desc') || 'desc';

      if (page < 1) {
        return res.status(400).json({ error: 'Invalid page' });
      }
      if (limit < 1 || limit > 100) {
        return res.status(400).json({ error: 'Invalid limit' });
      }

      const offset = (page - 1) * limit;
      const result = await this.db.query(
        'SELECT * FROM requirements ORDER BY $1 $2 LIMIT $3 OFFSET $4',
        [sortBy, sortOrder, limit, offset]
      );

      const total = await this.db.query('SELECT COUNT(*) FROM requirements');

      res.json({
        success: true,
        data: result.rows,
        pagination: {
          page,
          limit,
          total: total.rows[0].count,
          pages: Math.ceil(total.rows[0].count / limit)
        }
      });
    } catch (error: any) {
      console.error(error);
      res.status(500).json({ error: 'Internal server error' });
    }
  }
}

// AFTER: Simple controller (15 lines, single responsibility)
export class RequirementsController {
  constructor(private service: RequirementsService) {}

  async getRequirements(req: Request, res: Response) {
    const params = validatePaginationParams(req.query);
    const result = await this.service.getRequirements(params);

    res.json({
      success: true,
      data: result.requirements,
      pagination: result.pagination
    });
  }
}

// Validation moved to middleware
function validatePaginationParams(query: any): PaginationParams {
  const schema = z.object({
    page: z.coerce.number().int().min(1).default(1),
    limit: z.coerce.number().int().min(1).max(100).default(10),
    sortBy: z.string().default('createdAt'),
    sortOrder: z.enum(['asc', 'desc']).default('desc')
  });

  return schema.parse(query);
}

// Business logic moved to service
class RequirementsService {
  async getRequirements(params: PaginationParams) {
    const requirements = await this.repo.findAll(params);
    const total = await this.repo.count();

    return {
      requirements,
      pagination: {
        page: params.page,
        limit: params.limit,
        total,
        pages: Math.ceil(total / params.limit)
      }
    };
  }
}
```

**4B. Eliminate 'any' Types**
```typescript
// BEFORE: any types everywhere
async function createRequirement(data: any): Promise<any> {
  const result = await db.query('INSERT INTO requirements ...', data);
  return result.rows[0];
}

// AFTER: Proper types
interface CreateRequirementRequest {
  title: string;
  description: string;
  priority: 'low' | 'medium' | 'high';
  assigneeId?: string;
}

interface Requirement extends CreateRequirementRequest {
  id: string;
  status: 'draft' | 'approved' | 'rejected';
  createdAt: Date;
  updatedAt: Date;
}

async function createRequirement(
  data: CreateRequirementRequest
): Promise<Requirement> {
  const result = await db.query<Requirement>(
    'INSERT INTO requirements (title, description, priority, assignee_id) VALUES ($1, $2, $3, $4) RETURNING *',
    [data.title, data.description, data.priority, data.assigneeId]
  );
  return result.rows[0];
}
```

**4C. Replace console.log with Logger**
```typescript
// BEFORE: console.log everywhere
console.log('User logged in:', userId);
console.error('Failed to save:', error);

// AFTER: Structured logging
import logger from './logger';

logger.info('User logged in', { userId });
logger.error('Failed to save requirement', {
  error: error.message,
  stack: error.stack,
  requirementId
});

// logger.ts - Simple Pino setup
import pino from 'pino';

export const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  transport: {
    target: 'pino-pretty',
    options: {
      colorize: true,
      translateTime: 'SYS:standard',
      ignore: 'pid,hostname'
    }
  }
});
```

**4D. Centralized Error Handling**
```typescript
// BEFORE: try-catch in every controller
async handler(req: Request, res: Response) {
  try {
    const result = await service.doSomething();
    res.json(result);
  } catch (error) {
    res.status(500).json({ error: 'Something went wrong' });
  }
}

// AFTER: Centralized error middleware
// Custom error classes
export class AppError extends Error {
  constructor(
    message: string,
    public statusCode: number = 500,
    public isOperational: boolean = true
  ) {
    super(message);
    Object.setPrototypeOf(this, AppError.prototype);
  }
}

export class NotFoundError extends AppError {
  constructor(message: string) {
    super(message, 404);
  }
}

export class ValidationError extends AppError {
  constructor(message: string) {
    super(message, 400);
  }
}

// Error middleware
export function errorHandler(
  error: Error,
  req: Request,
  res: Response,
  next: NextFunction
) {
  if (error instanceof AppError) {
    return res.status(error.statusCode).json({
      success: false,
      message: error.message
    });
  }

  // Unexpected errors
  logger.error('Unexpected error', { error: error.stack });
  res.status(500).json({
    success: false,
    message: 'Internal server error'
  });
}

// Controllers become simple
async handler(req: Request, res: Response) {
  const result = await service.doSomething();
  res.json({ success: true, data: result });
}
// Errors propagate to middleware automatically
```

### Phase 5: Code Quality Automation

**5A. ESLint Configuration**
```json
// .eslintrc.json - Enforce simplicity
{
  "extends": [
    "eslint:recommended",
    "@typescript-eslint/recommended"
  ],
  "rules": {
    "@typescript-eslint/no-explicit-any": "error",
    "@typescript-eslint/explicit-function-return-type": "warn",
    "complexity": ["error", 10],
    "max-depth": ["error", 3],
    "max-lines-per-function": ["warn", 50],
    "max-params": ["error", 4],
    "no-console": "error",
    "no-duplicate-imports": "error",
    "prefer-const": "error",
    "no-var": "error"
  }
}
```

**5B. Pre-commit Hooks**
```bash
# Install husky
npm install --save-dev husky

# Add pre-commit hook
cat > .husky/pre-commit << 'EOF'
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

# Run linting
npm run lint

# Run type checking
npm run typecheck

# Run tests
npm test

# Block commit if any fail
EOF

chmod +x .husky/pre-commit
```

**5C. Automated Testing**
```typescript
// Simple, readable tests
describe('RequirementsService', () => {
  describe('createRequirement', () => {
    it('should create requirement with valid data', async () => {
      const data = {
        title: 'New Feature',
        description: 'Add user authentication',
        priority: 'high' as const
      };

      const result = await service.createRequirement(data);

      expect(result).toMatchObject(data);
      expect(result.id).toBeDefined();
      expect(result.status).toBe('draft');
    });

    it('should throw ValidationError for invalid priority', async () => {
      const data = {
        title: 'Feature',
        description: 'Description',
        priority: 'invalid' as any
      };

      await expect(service.createRequirement(data))
        .rejects
        .toThrow(ValidationError);
    });

    it('should throw ValidationError for empty title', async () => {
      const data = {
        title: '',
        description: 'Description',
        priority: 'medium' as const
      };

      await expect(service.createRequirement(data))
        .rejects
        .toThrow(ValidationError);
    });
  });
});
```

### Phase 6: Performance Simplification

**6A. Database Query Optimization**
```typescript
// BEFORE: N+1 query problem
async function getProjectsWithRequirements() {
  const projects = await db.query('SELECT * FROM projects');

  for (const project of projects.rows) {
    project.requirements = await db.query(
      'SELECT * FROM requirements WHERE project_id = $1',
      [project.id]
    ); // N queries!
  }

  return projects.rows;
}

// AFTER: Single JOIN query
async function getProjectsWithRequirements() {
  const result = await db.query(`
    SELECT
      p.*,
      json_agg(r.*) as requirements
    FROM projects p
    LEFT JOIN requirements r ON r.project_id = p.id
    GROUP BY p.id
  `);

  return result.rows;
}
```

**6B. Caching Strategy**
```typescript
// Simple Redis caching wrapper
class CachedService {
  constructor(
    private redis: Redis,
    private ttl: number = 300 // 5 minutes
  ) {}

  async get<T>(key: string, fetcher: () => Promise<T>): Promise<T> {
    // Try cache first
    const cached = await this.redis.get(key);
    if (cached) {
      return JSON.parse(cached);
    }

    // Cache miss - fetch and cache
    const data = await fetcher();
    await this.redis.setex(key, this.ttl, JSON.stringify(data));
    return data;
  }

  async invalidate(key: string) {
    await this.redis.del(key);
  }
}

// Usage
async getRequirements(params: PaginationParams) {
  const cacheKey = `requirements:${JSON.stringify(params)}`;

  return this.cache.get(cacheKey, async () => {
    return this.repo.findAll(params);
  });
}
```

### Phase 7: Documentation & Maintainability

**7A. Self-Documenting Code**
```typescript
// BEFORE: Needs comments
async function processReqs(data: any) {
  // Validate input
  if (!data.title || data.title.length < 3) {
    throw new Error('Invalid');
  }

  // Save to DB
  const result = await this.db.query('INSERT INTO...');

  // Send notification
  await this.sendEmail(data.assignee, 'New req');

  return result;
}

// AFTER: Self-explanatory names, no comments needed
async function createRequirement(request: CreateRequirementRequest) {
  validateRequirementRequest(request);

  const requirement = await this.repository.save(request);

  await this.notifier.notifyAssignee(requirement);

  return requirement;
}
```

**7B. API Documentation**
```typescript
/**
 * Create a new requirement
 *
 * @param request - Requirement data
 * @returns Created requirement with ID and timestamps
 * @throws ValidationError if request is invalid
 * @throws DatabaseError if save fails
 *
 * @example
 * ```typescript
 * const requirement = await service.createRequirement({
 *   title: 'Add authentication',
 *   description: 'Implement JWT-based auth',
 *   priority: 'high'
 * });
 * ```
 */
async createRequirement(
  request: CreateRequirementRequest
): Promise<Requirement> {
  // Implementation
}
```

## Validation Checklist

Before marking backend as "simple and bug-free":

### Code Quality
- [ ] Zero 'any' types (all properly typed)
- [ ] Zero console.log (use logger)
- [ ] Zero try-catch blocks in controllers (use error middleware)
- [ ] No functions >50 lines
- [ ] No files >300 lines
- [ ] No circular dependencies
- [ ] Cyclomatic complexity <10 per function

### Bug Prevention
- [ ] All async functions have await or return Promise
- [ ] All Promises have .catch() or try-catch
- [ ] All user input is validated
- [ ] All database queries use parameterized queries (SQL injection safe)
- [ ] All null/undefined cases handled
- [ ] No race conditions
- [ ] No memory leaks (event listeners cleaned up)

### Testing
- [ ] >75% code coverage
- [ ] All critical paths have tests
- [ ] All error cases have tests
- [ ] Integration tests for all APIs
- [ ] No flaky tests

### Performance
- [ ] No N+1 queries
- [ ] Caching implemented where appropriate
- [ ] Database indexes on query columns
- [ ] Connection pooling configured
- [ ] API response time <200ms (p95)

### Maintainability
- [ ] Clear file structure
- [ ] Consistent naming conventions
- [ ] Self-documenting code
- [ ] API documentation complete
- [ ] README up to date
- [ ] No dead code

## Output Format

After backend audit, provide:

```markdown
## Backend Simplicity Audit Report

**Status**: [SIMPLE ✅ / NEEDS REFACTORING ⚠️ / COMPLEX ❌]

### Complexity Metrics

- Total 'any' types: [count] (target: 0)
- console.log usage: [count] (target: 0)
- Functions >50 lines: [count] (target: 0)
- Files >300 lines: [count] (target: <3)
- Cyclomatic complexity: [avg] (target: <10)
- Test coverage: [%] (target: >75%)

### Bugs Found

#### Critical Bugs 🔴
1. [Bug description]
   - Location: [file:line]
   - Impact: [What breaks]
   - Fix: [Code change needed]

#### Potential Bugs 🟡
1. [Issue description]
   - Location: [file:line]
   - Risk: [What could break]
   - Prevention: [Code change]

### Simplification Opportunities

#### High Priority
1. [Complex code section]
   - Current complexity: [metric]
   - Suggested refactoring: [pattern]
   - Estimated effort: [hours]

#### Medium Priority
1. [Optimization opportunity]
   - Current approach: [description]
   - Simpler approach: [alternative]
   - Benefit: [why simpler is better]

### Code Quality Score

- Simplicity: [X/10]
- Bug-Free: [X/10]
- Maintainability: [X/10]
- Performance: [X/10]
- Test Coverage: [X/10]

**Overall**: [X/50] - [Grade: A+ to F]

### Refactoring Plan

#### Phase 1: Bug Fixes (Week 1)
- [ ] Fix critical bugs
- [ ] Add missing error handling
- [ ] Fix type safety issues

#### Phase 2: Simplification (Week 2)
- [ ] Eliminate 'any' types
- [ ] Replace console.log with logger
- [ ] Refactor complex functions
- [ ] Add missing tests

#### Phase 3: Optimization (Week 3)
- [ ] Fix N+1 queries
- [ ] Add caching
- [ ] Optimize database indexes
- [ ] Performance profiling

### Code Examples

[Provide specific before/after refactoring examples]
```

## Example Usage

User: "Simplify the backend and eliminate bugs"

This skill will:
1. Audit all TypeScript files for complexity
2. Find all bugs (null checks, async/await, race conditions)
3. Research simplification patterns
4. Detect code duplication
5. Check type safety (eliminate 'any')
6. Validate error handling
7. Test coverage analysis
8. Generate refactoring plan with specific code changes
9. Implement fixes if requested
10. Verify with automated tests
