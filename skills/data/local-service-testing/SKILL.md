---
name: local-service-testing
description: Use when code changes touch database, cache, queue, or other service-dependent components - enforces testing against real local services instead of mocks
---

# Local Service Testing

## Overview

Test against real services locally before pushing. CI validates—it doesn't discover.

**Core principle:** If you mock what you can run locally, you're hiding bugs.

**Announce at start:** "I'm using local-service-testing to verify changes against real services."

## The Iron Law

```
CI DISCOVERS NOTHING.
IF CI FINDS A BUG, YOUR LOCAL TESTING FAILED.
```

Local services exist for a reason. Use them.

## Critical Clarification

**Unit tests with mocks: REQUIRED** (for TDD cycle)
**Integration tests with real services: ALSO REQUIRED**

This skill does NOT replace mocking in unit tests. It ADDS the requirement for integration tests against real services. Both are mandatory.

## When This Skill Applies

| Code Change | Required Service | Must Test Against |
|-------------|------------------|-------------------|
| Database models/entities | postgres | Real postgres |
| Migrations | postgres | Real postgres |
| Repository/ORM layer | postgres | Real postgres |
| SQL queries | postgres | Real postgres |
| Cache operations | redis | Real redis |
| Session storage | redis | Real redis |
| Pub/sub messages | redis/rabbitmq | Real queue |
| Queue workers | redis/rabbitmq | Real queue |
| API endpoints | all services | All running |

**If your change touches any of these, you MUST test against the real service.**

## Service Detection

At session start, the `session-start.sh` hook reports available services:

```
Checking development services...
  ✓ Found docker-compose.yml

  Available services:
    ✓ postgres (running)
    ○ redis (not running)

  Tip: Start services with: docker-compose up -d
```

### Starting Services

```bash
# Start all services
docker-compose up -d

# Start specific service
docker-compose up -d postgres

# Check status
docker-compose ps
```

### Service Connection Strings

| Service | Default Connection |
|---------|-------------------|
| postgres | `postgresql://localhost:5432/dev` |
| redis | `redis://localhost:6379` |
| rabbitmq | `amqp://localhost:5672` |

Check your project's `.env.example` or docker-compose.yml for actual values.

## Testing Protocol

### Step 1: Identify Service Dependencies

Before testing, identify which services your changes require:

```bash
# Check what files you've changed
git diff --name-only HEAD~1

# Map to services:
# *.sql, *migration*, *model*, *entity*, *repository* → postgres
# *cache*, *redis*, *session*, *queue*, *pub*, *sub* → redis
# *worker*, *job*, *consumer* → queue service
```

### Step 2: Ensure Services Running

```bash
# Start required services
docker-compose up -d postgres redis

# Verify they're ready
docker-compose ps

# Test connectivity
# Postgres
psql postgresql://localhost:5432/dev -c "SELECT 1"

# Redis
redis-cli ping
```

### Step 3: Run Integration Tests

```bash
# Run integration tests (not unit tests with mocks)
pnpm test:integration

# Or run specific integration test suite
pnpm test --grep "integration"

# For Python projects
pytest tests/integration/

# For Go projects
go test -tags=integration ./...
```

### Step 4: Verify Locally Before Pushing

Before `git push`:

```bash
# Full verification
pnpm build
pnpm lint
pnpm typecheck
pnpm test              # Unit tests
pnpm test:integration  # Integration tests against real services
```

## Two-Layer Testing Requirement

### Both Are Required

| Test Layer | Purpose | Uses Mocks? | Uses Real Services? | Required? |
|------------|---------|-------------|---------------------|-----------|
| **Unit tests** | TDD cycle, verify logic | **YES** | No | **YES** |
| **Integration tests** | Verify real behavior | No | **YES** | **YES** |

### Why Both?

- **Unit tests with mocks:** Fast, enable RED-GREEN-REFACTOR, isolate logic
- **Integration tests with services:** Catch real-world failures mocks miss

We've experienced **80% failure rates** with ORM migrations because unit tests with mocks passed but real databases rejected the changes.

### What Mocks Miss

```typescript
// Mock says this works
const mockDb = {
  query: jest.fn().mockResolvedValue([{ id: 1 }])
};

// But real postgres throws:
// ERROR: relation "users" does not exist
// ERROR: column "email" cannot be null
// ERROR: duplicate key violates unique constraint
```

Real services reveal:
- Schema mismatches
- Constraint violations
- Connection issues
- Transaction behavior
- Performance problems

## Artifact Requirement

Before creating a PR, you must post local testing evidence to the issue.

### Required Artifact Format

```markdown
<!-- LOCAL-TESTING:START -->
## Local Service Testing

| Service | Status | Verification |
|---------|--------|--------------|
| postgres | ✅ Running | Migrations applied, queries executed |
| redis | ✅ Running | Cache operations verified |

**Tests Run:**
- `pnpm test:integration` - PASSED
- Manual verification of [specific feature]

**Tested At:** 2025-01-15T10:30:00Z
<!-- LOCAL-TESTING:END -->
```

### Where to Post

Post as a comment on the GitHub issue you're working on. This is checked by the `validate-local-testing.sh` PreToolUse hook before PR creation.

### When Artifact is Required

The hook checks:
1. Does docker-compose.yml exist?
2. Do changed files match service patterns?
3. If yes to both → artifact required

If no services are relevant to your changes, no artifact is needed.

## Common Patterns

### Database Testing

```typescript
// GOOD: Test against real postgres
describe('UserRepository (integration)', () => {
  beforeAll(async () => {
    await db.migrate.latest();
  });

  afterAll(async () => {
    await db.destroy();
  });

  it('creates user with unique email constraint', async () => {
    await userRepo.create({ email: 'test@example.com' });

    // Real postgres will throw on duplicate
    await expect(
      userRepo.create({ email: 'test@example.com' })
    ).rejects.toThrow(/unique constraint/);
  });
});
```

### Cache Testing

```typescript
// GOOD: Test against real redis
describe('CacheService (integration)', () => {
  beforeEach(async () => {
    await redis.flushdb();
  });

  it('expires keys after TTL', async () => {
    await cache.set('key', 'value', { ttl: 1 });

    expect(await cache.get('key')).toBe('value');

    await sleep(1100);

    expect(await cache.get('key')).toBeNull();
  });
});
```

### API Testing

```typescript
// GOOD: Test against real services
describe('POST /users (integration)', () => {
  it('creates user and caches result', async () => {
    const response = await request(app)
      .post('/users')
      .send({ email: 'new@example.com' });

    expect(response.status).toBe(201);

    // Verify in real database
    const user = await db('users').where({ email: 'new@example.com' }).first();
    expect(user).toBeDefined();

    // Verify in real cache
    const cached = await redis.get(`user:${user.id}`);
    expect(cached).toBeDefined();
  });
});
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Service not starting | Check `docker-compose logs [service]` |
| Connection refused | Ensure service is running and port is correct |
| Database doesn't exist | Run migrations: `pnpm migrate` |
| Tests pass locally, fail in CI | Environment variable mismatch—check `.env` vs CI config |
| Flaky integration tests | Check for proper test isolation and cleanup |

## Checklist

Before creating PR:

- [ ] Identified all service dependencies for changes
- [ ] All required services are running locally
- [ ] Integration tests pass against real services
- [ ] Posted local testing artifact to issue
- [ ] Did not rely on mocks for service-dependent code

## Integration

This skill is called by:
- `tdd-full-coverage` - For integration testing requirements
- `issue-driven-development` - Before PR creation
- `verification-before-merge` - As a merge gate

This skill is enforced by:
- `validate-local-testing.sh` - PreToolUse hook blocks PR without artifact

This skill references:
- `environment-bootstrap` - For service startup patterns
- `session-start` - For service detection at session start
