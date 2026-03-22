---
name: N+1 Query Detector
description: Detect and eliminate N+1 query problems in database-backed applications through query counting, execution plan analysis, and ORM configuration auditing
version: 1.0.0
author: Pramod
license: MIT
tags: [n-plus-one, database-performance, query-optimization, orm, eager-loading, sql-profiling, database-testing]
testingTypes: [performance, database]
frameworks: []
languages: [typescript, javascript, python, java]
domains: [api]
agents: [claude-code, cursor, github-copilot, windsurf, codex, aider, continue, cline, zed, bolt, gemini-cli, amp]
---

# N+1 Query Detector Skill

You are an expert QA automation engineer specializing in database performance testing and N+1 query detection. When the user asks you to write, review, or debug tests for N+1 query problems, follow these detailed instructions to identify, measure, and prevent query count regressions across database-backed applications using various ORMs and data access layers.

## Core Principles

1. **Measure, do not guess** -- Always instrument query counting at the database driver level. Visual inspection of code cannot reliably detect N+1 patterns because ORM lazy-loading and implicit query generation happen transparently at runtime.
2. **Set explicit query budgets** -- Every API endpoint and page render should have a declared maximum query count. Treat query budget overruns as test failures, not warnings.
3. **Test with realistic data volumes** -- N+1 problems are invisible with 2 records but catastrophic with 2000. Always seed test data with enough rows to expose linear query scaling.
4. **Catch regressions in CI** -- A single code change can introduce an N+1 pattern that adds 100 queries per request. Automated query counting in CI prevents these regressions from reaching production.
5. **Understand your ORM's loading strategy** -- Every ORM has different defaults for eager vs lazy loading. Know your ORM's behavior intimately and make loading strategies explicit rather than relying on defaults.
6. **Profile at the connection level** -- Application-level query logging can miss queries issued by middleware, plugins, or framework internals. Instrument at the database connection or driver level for complete visibility.
7. **Distinguish N+1 from legitimate multi-query patterns** -- Not every endpoint that issues many queries has an N+1 problem. Some operations legitimately require multiple queries. The key indicator is query count scaling linearly with data size.

## Project Structure

Organize N+1 detection projects with this structure:

```
tests/
  performance/
    n-plus-one/
      api-endpoints.spec.ts
      graphql-resolvers.spec.ts
      page-renders.spec.ts
    query-budgets/
      budget-definitions.ts
      budget-enforcement.spec.ts
  helpers/
    query-counter.ts
    query-logger.ts
    data-seeder.ts
  fixtures/
    database.fixture.ts
    query-monitor.fixture.ts
  reports/
    query-count-reporter.ts
config/
  query-budgets.json
  thresholds.ts
```

## Query Counting Middleware

The foundation of N+1 detection is accurate query counting. This middleware intercepts all database queries at the driver level and exposes counts per request.

### Generic Query Counter for Node.js

```typescript
import { EventEmitter } from 'events';

interface QueryLog {
  sql: string;
  params: unknown[];
  duration: number;
  timestamp: number;
  stack?: string;
}

class QueryCounter extends EventEmitter {
  private queries: QueryLog[] = [];
  private isCapturing = false;

  start(): void {
    this.queries = [];
    this.isCapturing = true;
  }

  stop(): QueryLog[] {
    this.isCapturing = false;
    return [...this.queries];
  }

  record(sql: string, params: unknown[], duration: number): void {
    if (!this.isCapturing) return;

    const entry: QueryLog = {
      sql,
      params,
      duration,
      timestamp: Date.now(),
      stack: new Error().stack,
    };

    this.queries.push(entry);
    this.emit('query', entry);
  }

  get count(): number {
    return this.queries.length;
  }

  get totalDuration(): number {
    return this.queries.reduce((sum, q) => sum + q.duration, 0);
  }

  getGroupedByPattern(): Map<string, number> {
    const groups = new Map<string, number>();

    for (const query of this.queries) {
      // Normalize the SQL by replacing literal values with placeholders
      const normalized = query.sql
        .replace(/= '\w+'/g, "= '?'")
        .replace(/= \d+/g, '= ?')
        .replace(/IN \([^)]+\)/g, 'IN (?)')
        .replace(/LIMIT \d+/g, 'LIMIT ?')
        .replace(/OFFSET \d+/g, 'OFFSET ?');

      groups.set(normalized, (groups.get(normalized) || 0) + 1);
    }

    return groups;
  }

  detectNPlusOne(threshold: number = 5): string[] {
    const groups = this.getGroupedByPattern();
    const violations: string[] = [];

    for (const [pattern, count] of groups) {
      if (count >= threshold) {
        violations.push(
          `N+1 detected: "${pattern}" executed ${count} times`
        );
      }
    }

    return violations;
  }

  reset(): void {
    this.queries = [];
    this.isCapturing = false;
  }
}

export const queryCounter = new QueryCounter();
```

### Prisma Integration

```typescript
import { PrismaClient } from '@prisma/client';
import { queryCounter } from './query-counter';

function createInstrumentedPrisma(): PrismaClient {
  const prisma = new PrismaClient({
    log: [
      { level: 'query', emit: 'event' },
    ],
  });

  prisma.$on('query' as never, (e: { query: string; params: string; duration: number }) => {
    queryCounter.record(e.query, JSON.parse(e.params), e.duration);
  });

  return prisma;
}

export const prisma = createInstrumentedPrisma();
```

### Express Middleware for Per-Request Counting

```typescript
import { Request, Response, NextFunction } from 'express';
import { queryCounter } from './query-counter';

interface QueryMetrics {
  queryCount: number;
  totalDuration: number;
  nPlusOneViolations: string[];
}

export function queryCountingMiddleware(
  maxQueries: number = 20
) {
  return (req: Request, res: Response, next: NextFunction) => {
    queryCounter.start();

    const originalJson = res.json.bind(res);
    res.json = function (body: unknown) {
      const logs = queryCounter.stop();
      const violations = queryCounter.detectNPlusOne();

      const metrics: QueryMetrics = {
        queryCount: logs.length,
        totalDuration: logs.reduce((sum, q) => sum + q.duration, 0),
        nPlusOneViolations: violations,
      };

      // Attach metrics to response headers in development
      if (process.env.NODE_ENV !== 'production') {
        res.setHeader('X-Query-Count', metrics.queryCount.toString());
        res.setHeader('X-Query-Duration', `${metrics.totalDuration}ms`);

        if (metrics.queryCount > maxQueries) {
          console.warn(
            `[N+1 WARNING] ${req.method} ${req.path}: ${metrics.queryCount} queries (limit: ${maxQueries})`
          );
          for (const v of violations) {
            console.warn(`  ${v}`);
          }
        }
      }

      return originalJson(body);
    };

    next();
  };
}
```

## Detecting N+1 Patterns in ORMs

### Prisma N+1 Detection

Prisma defaults to lazy-loading relations, which is the primary source of N+1 queries. The fix is explicit `include` or `select` clauses.

```typescript
import { test, expect, beforeAll, afterAll } from 'vitest';
import { prisma } from '../helpers/prisma-instrumented';
import { queryCounter } from '../helpers/query-counter';

beforeAll(async () => {
  // Seed test data with enough volume to expose N+1
  const users = Array.from({ length: 50 }, (_, i) => ({
    name: `User ${i}`,
    email: `user${i}@test.com`,
  }));

  await prisma.user.createMany({ data: users });

  const createdUsers = await prisma.user.findMany();
  for (const user of createdUsers) {
    await prisma.post.createMany({
      data: Array.from({ length: 5 }, (_, i) => ({
        title: `Post ${i} by ${user.name}`,
        content: `Content ${i}`,
        authorId: user.id,
      })),
    });
  }
});

afterAll(async () => {
  await prisma.post.deleteMany();
  await prisma.user.deleteMany();
});

test('GET /api/users should not cause N+1 queries', async () => {
  queryCounter.start();

  // Simulate the endpoint handler
  const users = await prisma.user.findMany({
    include: {
      posts: {
        select: { id: true, title: true },
      },
    },
  });

  const logs = queryCounter.stop();
  const violations = queryCounter.detectNPlusOne();

  // With proper eager loading, this should be 2 queries max:
  // 1. SELECT users
  // 2. SELECT posts WHERE authorId IN (...)
  expect(logs.length).toBeLessThanOrEqual(3);
  expect(violations).toHaveLength(0);

  // Verify the data is complete (not lazy-loaded)
  for (const user of users) {
    expect(user.posts).toBeDefined();
    expect(Array.isArray(user.posts)).toBe(true);
  }
});

test('ANTI-PATTERN: lazy loading causes N+1', async () => {
  queryCounter.start();

  // This is the N+1 anti-pattern -- DO NOT DO THIS in production
  const users = await prisma.user.findMany(); // Query 1
  for (const user of users) {
    // Each iteration issues a new query -- Query 2..N+1
    const posts = await prisma.post.findMany({
      where: { authorId: user.id },
    });
    // Process posts...
  }

  const logs = queryCounter.stop();
  const violations = queryCounter.detectNPlusOne();

  // This will issue 1 + N queries (51 queries for 50 users)
  expect(logs.length).toBeGreaterThan(50);
  expect(violations.length).toBeGreaterThan(0);
});
```

### SQLAlchemy N+1 Detection (Python)

```python
import pytest
from sqlalchemy import event, text
from sqlalchemy.orm import Session
from app.models import User, Post
from app.database import engine, SessionLocal


class QueryCounter:
    def __init__(self):
        self.queries = []
        self._listening = False

    def start(self, engine):
        self.queries = []
        self._listening = True
        event.listen(engine, "before_cursor_execute", self._record)

    def stop(self, engine):
        self._listening = False
        event.remove(engine, "before_cursor_execute", self._record)
        return self.queries

    def _record(self, conn, cursor, statement, parameters, context, executemany):
        if self._listening:
            self.queries.append({
                "sql": statement,
                "params": parameters,
            })

    @property
    def count(self):
        return len(self.queries)

    def detect_n_plus_one(self, threshold=5):
        from collections import Counter
        import re

        normalized = []
        for q in self.queries:
            sql = re.sub(r"= '[^']*'", "= '?'", q["sql"])
            sql = re.sub(r"= \d+", "= ?", sql)
            normalized.append(sql)

        counts = Counter(normalized)
        return {sql: count for sql, count in counts.items() if count >= threshold}


@pytest.fixture
def query_counter():
    counter = QueryCounter()
    counter.start(engine)
    yield counter
    counter.stop(engine)


def test_get_users_with_posts_no_n_plus_one(query_counter, db_session: Session):
    """Verify eager loading prevents N+1 queries."""
    from sqlalchemy.orm import joinedload

    # Correct: eager load with joinedload
    users = (
        db_session.query(User)
        .options(joinedload(User.posts))
        .all()
    )

    assert query_counter.count <= 2  # 1 JOIN query or 2 separate queries
    violations = query_counter.detect_n_plus_one()
    assert len(violations) == 0

    # Verify data is loaded
    for user in users:
        assert hasattr(user, "posts")


def test_lazy_loading_causes_n_plus_one(query_counter, db_session: Session):
    """Demonstrate the N+1 anti-pattern with lazy loading."""
    # Anti-pattern: no eager loading specified
    users = db_session.query(User).all()  # Query 1

    for user in users:
        _ = user.posts  # Each access triggers a query

    violations = query_counter.detect_n_plus_one()
    assert len(violations) > 0, "Expected N+1 pattern not detected"
```

### Hibernate N+1 Detection (Java)

```java
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import net.ttddyy.dsproxy.QueryCountHolder;
import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest
class NPlusOneDetectionTest {

    @Autowired
    private UserRepository userRepository;

    @Test
    void getUsersWithPosts_shouldNotCauseNPlusOne() {
        QueryCountHolder.clear();

        // Uses @EntityGraph or JOIN FETCH
        var users = userRepository.findAllWithPosts();

        var queryCount = QueryCountHolder.getGrandTotal();

        // Should be at most 1-2 queries with proper fetch strategy
        assertThat(queryCount.getSelect()).isLessThanOrEqualTo(2);

        // Verify posts are loaded
        for (var user : users) {
            assertThat(user.getPosts()).isNotNull();
            assertThat(
                org.hibernate.Hibernate.isInitialized(user.getPosts())
            ).isTrue();
        }
    }
}
```

## Automated Threshold Testing

### Query Budget Definitions

```typescript
// config/query-budgets.ts

export interface QueryBudget {
  endpoint: string;
  method: string;
  maxQueries: number;
  maxDurationMs: number;
  description: string;
}

export const QUERY_BUDGETS: QueryBudget[] = [
  {
    endpoint: '/api/users',
    method: 'GET',
    maxQueries: 3,
    maxDurationMs: 100,
    description: 'List users with counts',
  },
  {
    endpoint: '/api/users/:id',
    method: 'GET',
    maxQueries: 4,
    maxDurationMs: 50,
    description: 'Single user with relations',
  },
  {
    endpoint: '/api/posts',
    method: 'GET',
    maxQueries: 5,
    maxDurationMs: 150,
    description: 'List posts with author and tags',
  },
  {
    endpoint: '/api/dashboard',
    method: 'GET',
    maxQueries: 8,
    maxDurationMs: 200,
    description: 'Dashboard with aggregations',
  },
  {
    endpoint: '/api/feed',
    method: 'GET',
    maxQueries: 6,
    maxDurationMs: 200,
    description: 'Activity feed with nested data',
  },
];
```

### Budget Enforcement Tests

```typescript
import { test, expect, describe, beforeEach, afterEach } from 'vitest';
import { queryCounter } from '../helpers/query-counter';
import { QUERY_BUDGETS } from '../../config/query-budgets';
import request from 'supertest';
import { app } from '../../src/app';

describe('Query Budget Enforcement', () => {
  for (const budget of QUERY_BUDGETS) {
    test(`${budget.method} ${budget.endpoint} should stay within query budget (max: ${budget.maxQueries})`, async () => {
      queryCounter.start();

      const resolvedEndpoint = budget.endpoint.replace(
        /:id/g,
        '1'
      );

      const response = await request(app)
        [budget.method.toLowerCase() as 'get' | 'post'](resolvedEndpoint)
        .set('Accept', 'application/json');

      const logs = queryCounter.stop();

      expect(response.status).toBeLessThan(500);

      // Enforce query count budget
      expect(
        logs.length,
        `${budget.method} ${budget.endpoint}: ${logs.length} queries exceeds budget of ${budget.maxQueries}. ` +
        `Queries:\n${logs.map((q) => `  - ${q.sql.substring(0, 120)}`).join('\n')}`
      ).toBeLessThanOrEqual(budget.maxQueries);

      // Enforce duration budget
      const totalDuration = logs.reduce((sum, q) => sum + q.duration, 0);
      expect(
        totalDuration,
        `${budget.method} ${budget.endpoint}: ${totalDuration}ms exceeds duration budget of ${budget.maxDurationMs}ms`
      ).toBeLessThanOrEqual(budget.maxDurationMs);

      // Check for N+1 patterns
      const violations = queryCounter.detectNPlusOne(3);
      expect(
        violations,
        `N+1 detected in ${budget.method} ${budget.endpoint}:\n${violations.join('\n')}`
      ).toHaveLength(0);
    });
  }
});
```

## DataLoader Pattern for GraphQL

GraphQL APIs are especially vulnerable to N+1 problems because each resolver fetches data independently. The DataLoader pattern batches and deduplicates these fetches.

```typescript
import DataLoader from 'dataloader';
import { prisma } from './prisma';

// DataLoader batches individual post lookups into a single query
export function createPostLoader() {
  return new DataLoader<string, Post[]>(async (userIds) => {
    // Single query: SELECT * FROM posts WHERE authorId IN (...)
    const posts = await prisma.post.findMany({
      where: {
        authorId: { in: [...userIds] },
      },
    });

    // Map posts back to their respective user IDs
    const postsByUserId = new Map<string, Post[]>();
    for (const post of posts) {
      const existing = postsByUserId.get(post.authorId) || [];
      existing.push(post);
      postsByUserId.set(post.authorId, existing);
    }

    return userIds.map((id) => postsByUserId.get(id) || []);
  });
}

// Test that DataLoader properly batches
import { test, expect } from 'vitest';

test('DataLoader should batch user post lookups', async () => {
  queryCounter.start();

  const postLoader = createPostLoader();

  // These 50 calls should be batched into 1 query
  const userIds = Array.from({ length: 50 }, (_, i) => `user-${i}`);
  const results = await Promise.all(
    userIds.map((id) => postLoader.load(id))
  );

  const logs = queryCounter.stop();

  // DataLoader should batch all 50 lookups into 1 query
  expect(logs.length).toBe(1);
  expect(logs[0].sql).toContain('IN');
  expect(results).toHaveLength(50);
});

test('DataLoader should deduplicate identical requests', async () => {
  queryCounter.start();

  const postLoader = createPostLoader();

  // Same user ID requested 10 times
  const sameId = 'user-1';
  const results = await Promise.all(
    Array.from({ length: 10 }, () => postLoader.load(sameId))
  );

  const logs = queryCounter.stop();

  // Should still be 1 query despite 10 requests
  expect(logs.length).toBe(1);
  // All results should be the same reference
  const firstResult = results[0];
  results.forEach((r) => expect(r).toBe(firstResult));
});
```

## Request-Level Query Budgets

### Middleware That Fails Requests Exceeding Budget

```typescript
import { Request, Response, NextFunction } from 'express';
import { queryCounter } from './query-counter';

interface BudgetConfig {
  [route: string]: {
    maxQueries: number;
    action: 'warn' | 'block' | 'log';
  };
}

const budgetConfig: BudgetConfig = {
  'GET /api/users': { maxQueries: 3, action: 'block' },
  'GET /api/posts': { maxQueries: 5, action: 'block' },
  'GET /api/dashboard': { maxQueries: 10, action: 'warn' },
  '*': { maxQueries: 20, action: 'log' },
};

export function queryBudgetMiddleware() {
  return (req: Request, res: Response, next: NextFunction) => {
    queryCounter.start();

    const originalEnd = res.end.bind(res);
    res.end = function (...args: Parameters<Response['end']>) {
      const logs = queryCounter.stop();
      const routeKey = `${req.method} ${req.route?.path || req.path}`;
      const config =
        budgetConfig[routeKey] || budgetConfig['*'];

      if (logs.length > config.maxQueries) {
        const message = `Query budget exceeded: ${routeKey} used ${logs.length}/${config.maxQueries} queries`;

        switch (config.action) {
          case 'block':
            if (!res.headersSent) {
              res.status(503).json({
                error: 'Service temporarily unavailable',
                reason: process.env.NODE_ENV === 'development' ? message : undefined,
              });
              return res;
            }
            break;
          case 'warn':
            console.warn(`[QUERY BUDGET WARNING] ${message}`);
            break;
          case 'log':
            console.log(`[QUERY BUDGET] ${message}`);
            break;
        }
      }

      return originalEnd(...args);
    } as Response['end'];

    next();
  };
}
```

## CI Integration for Query Count Regression

### GitHub Actions Workflow Integration

```typescript
// tests/performance/query-regression.spec.ts
import { test, expect, describe } from 'vitest';
import { queryCounter } from '../helpers/query-counter';
import { readFileSync, writeFileSync, existsSync } from 'fs';
import { join } from 'path';

const BASELINE_PATH = join(__dirname, '../../.query-baseline.json');

interface QueryBaseline {
  [endpoint: string]: {
    queryCount: number;
    measuredAt: string;
  };
}

function loadBaseline(): QueryBaseline {
  if (existsSync(BASELINE_PATH)) {
    return JSON.parse(readFileSync(BASELINE_PATH, 'utf-8'));
  }
  return {};
}

function saveBaseline(baseline: QueryBaseline): void {
  writeFileSync(BASELINE_PATH, JSON.stringify(baseline, null, 2));
}

describe('Query Count Regression Detection', () => {
  const endpoints = [
    { method: 'GET', path: '/api/users', handler: getUsersHandler },
    { method: 'GET', path: '/api/posts', handler: getPostsHandler },
    { method: 'GET', path: '/api/dashboard', handler: getDashboardHandler },
  ];

  for (const endpoint of endpoints) {
    test(`${endpoint.method} ${endpoint.path} should not regress in query count`, async () => {
      const baseline = loadBaseline();
      const key = `${endpoint.method} ${endpoint.path}`;

      queryCounter.start();
      await endpoint.handler();
      const logs = queryCounter.stop();

      const currentCount = logs.length;

      if (baseline[key]) {
        const previousCount = baseline[key].queryCount;
        const regressionThreshold = Math.ceil(previousCount * 1.1); // 10% tolerance

        expect(
          currentCount,
          `Query regression detected for ${key}: was ${previousCount}, now ${currentCount}`
        ).toBeLessThanOrEqual(regressionThreshold);
      }

      // Update baseline if running in update mode
      if (process.env.UPDATE_QUERY_BASELINE === 'true') {
        baseline[key] = {
          queryCount: currentCount,
          measuredAt: new Date().toISOString(),
        };
        saveBaseline(baseline);
      }
    });
  }
});
```

### Eager vs Lazy Loading Audit

```typescript
import { test, expect, describe } from 'vitest';
import { PrismaClient } from '@prisma/client';

describe('ORM Loading Strategy Audit', () => {
  test('all list endpoints should use explicit includes', async () => {
    // Parse the route handlers and check for include clauses
    const routeFiles = [
      'src/routes/users.ts',
      'src/routes/posts.ts',
      'src/routes/comments.ts',
    ];

    for (const file of routeFiles) {
      const content = require('fs').readFileSync(file, 'utf-8');

      // Check for findMany without include (potential N+1)
      const findManyWithoutInclude = /\.findMany\(\s*\)/g;
      const matches = content.match(findManyWithoutInclude);

      if (matches) {
        console.warn(
          `${file}: Found ${matches.length} findMany() calls without includes`
        );
      }

      expect(
        matches,
        `${file} has findMany() without explicit include — potential N+1`
      ).toBeNull();
    }
  });

  test('related data access should use include, not separate queries', async () => {
    // Verify that getting a user with posts uses a single include
    queryCounter.start();

    const user = await prisma.user.findUnique({
      where: { id: 'test-user-1' },
      include: {
        posts: true,
        comments: true,
        profile: true,
      },
    });

    const logs = queryCounter.stop();

    // findUnique with include should generate at most 4 queries
    // (1 per relation + 1 for the main entity, or fewer with JOINs)
    expect(logs.length).toBeLessThanOrEqual(4);
  });
});
```

## Configuration

### Query Counter Configuration

```typescript
// config/thresholds.ts

export const QUERY_THRESHOLDS = {
  // Maximum queries per request before triggering N+1 detection
  nPlusOneDetectionThreshold: 5,

  // Maximum total queries per request
  maxQueriesPerRequest: 20,

  // Maximum total query duration per request (ms)
  maxQueryDurationMs: 500,

  // Percentage increase allowed before flagging as regression
  regressionTolerancePercent: 10,

  // Minimum data volume for meaningful N+1 testing
  minimumTestDataRows: 50,

  // Enable detailed query logging in CI
  verboseLogging: process.env.CI === 'true',

  // File path for query count baselines
  baselinePath: '.query-baseline.json',
};
```

## Best Practices

1. **Always use `include` or `select` with list queries** -- When fetching a list of records that will need related data, declare the relations upfront in the query. Never iterate over results and issue individual relation lookups.

2. **Seed tests with at least 50 parent records** -- N+1 problems are proportional to data size. With 2 records, 3 queries vs 2 queries is invisible. With 50 records, 51 queries vs 2 queries is obvious.

3. **Make query budgets part of the API contract** -- Document the expected query count for each endpoint. When a PR changes an endpoint, reviewers should verify that the query budget is still reasonable.

4. **Use DataLoader for GraphQL resolvers** -- Every resolver that accesses related data must use a DataLoader instance. Create a new DataLoader per request to avoid cross-request caching issues.

5. **Profile production queries periodically** -- N+1 problems can hide behind caches in development. Use production query profiling tools (pg_stat_statements, slow query logs) to identify patterns that only emerge at production data volumes.

6. **Prefer batch operations over loops** -- Replace `for` loops that issue individual `INSERT`, `UPDATE`, or `DELETE` statements with batch operations (`createMany`, `updateMany`, bulk operations).

7. **Test with pagination** -- N+1 detection must work correctly with paginated queries. Ensure that eager loading applies to the paginated subset, not to all records.

8. **Instrument integration tests, not just unit tests** -- Unit tests with mocked databases cannot detect N+1 patterns. Use integration tests with a real database (or in-memory database like SQLite) for query counting.

9. **Log the full query with parameters** -- When a query budget violation is detected, log the complete SQL with bound parameters. This makes it immediately clear which query is being repeated.

10. **Use connection pooling metrics** -- Monitor connection pool checkout counts per request. An N+1 pattern will show high pool checkout rates even if individual queries are fast.

11. **Fail CI on query count regressions** -- Make query budget tests non-optional in CI. A query count regression that is merged today becomes a production performance incident tomorrow.

12. **Audit ORM lazy-loading configuration** -- Review your ORM's default loading strategy. In Prisma, relations are not loaded by default. In Hibernate, `@OneToMany` defaults to `FetchType.LAZY`. Know the defaults and override them explicitly.

## Anti-Patterns to Avoid

1. **Iterating and querying in a loop** -- The classic N+1 anti-pattern: `users.forEach(async (user) => { const posts = await getPosts(user.id); })`. Always use `include`, `JOIN`, or `IN` clauses instead.

2. **Relying on ORM lazy loading in production** -- Lazy loading is convenient in development but catastrophic in production. Disable lazy loading or configure your ORM to warn when it triggers implicit queries.

3. **Caching to hide N+1 problems** -- Adding a Redis cache on top of an N+1 endpoint masks the problem but does not fix it. Cache misses will still trigger the full N+1 pattern, and cold starts become extremely slow.

4. **Testing with empty or minimal data** -- Testing with 1-2 records will never reveal N+1 issues. The query count will look reasonable even with the most pathological access patterns. Always test with realistic data volumes.

5. **Using `SELECT *` when only IDs are needed** -- Fetching full records when you only need identifiers wastes bandwidth and memory. Use `select` clauses to fetch only the columns you need, and use `IN` queries for batch lookups.

6. **Ignoring GraphQL query depth** -- Deeply nested GraphQL queries can create cascading N+1 problems at each resolver level. Implement query depth limiting and require DataLoader at every level.

7. **Manual SQL string construction in loops** -- Building `WHERE id = ?` queries in a loop instead of `WHERE id IN (?, ?, ?)` is an N+1 pattern that ORMs would normally prevent. If writing raw SQL, always use batch operations.

## Debugging Tips

1. **Enable query logging at the driver level** -- Set `log: ['query']` in Prisma, `echo=True` in SQLAlchemy, or `hibernate.show_sql=true` in Hibernate. Count the queries manually for a single request to establish a baseline.

2. **Use `EXPLAIN ANALYZE` on repeated queries** -- If you see the same query pattern repeated many times, run `EXPLAIN ANALYZE` to understand its execution plan. A query that does a full table scan 50 times per request is doubly problematic.

3. **Check for missing indexes on foreign keys** -- N+1 queries often hit foreign key columns. Ensure that all foreign key columns have indexes. Without indexes, each individual query in the N+1 pattern does a sequential scan.

4. **Watch for N+1 in serialization** -- Some frameworks trigger lazy loading during JSON serialization when accessing relation properties. The N+1 happens not in the controller but in the serializer.

5. **Profile with a database proxy** -- Tools like pgBouncer, datasource-proxy (Java), or prisma-query-log can intercept all queries without modifying application code. This gives complete visibility into query patterns.

6. **Count queries per request in development** -- Add a simple middleware that logs the total query count for every request during development. Make this visible in the terminal output so developers notice regressions immediately.

7. **Examine the SQL pattern, not just the count** -- A high query count is not always N+1. Look for the signature pattern: one query followed by N identical queries with different parameter values. This distinguishes N+1 from legitimate multi-query operations.

8. **Test GraphQL resolvers in isolation** -- When debugging GraphQL N+1 issues, test each resolver independently with the DataLoader context to verify that batching is working. A misconfigured DataLoader that creates a new instance per resolve call will not batch.

9. **Check for N+1 in database triggers** -- If your database has triggers that run additional queries on INSERT or UPDATE, these can create N+1-like behavior that is invisible at the application level. Review trigger definitions when query counts exceed expectations.

10. **Use flamegraph-style query visualization** -- Tools that show queries on a timeline (like Prisma Studio or Django Debug Toolbar) make it visually obvious when 50 identical queries fire in sequence. The waterfall pattern of N+1 is unmistakable in a timeline view.
