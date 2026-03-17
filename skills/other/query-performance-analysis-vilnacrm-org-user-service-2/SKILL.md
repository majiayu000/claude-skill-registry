---
name: query-performance-analysis
description: Detect N+1 queries, analyze slow queries with EXPLAIN, identify missing indexes, and ensure safe online index migrations for MySQL/MariaDB. Use when optimizing query performance, preventing performance regressions, or debugging slow endpoints. Complements database-migrations skill which covers index creation syntax.
---

# Query Performance Analysis & Index Management

## Context (Input)

Use this skill when:

- New or modified endpoints are slow
- Profiler shows many database queries for single operation
- Need to detect N+1 query problems
- Query execution time is high
- Slow query warnings in MySQL logs
- Performance regression after code changes
- Planning safe index migrations for production
- Need to verify index effectiveness

## Task (Function)

Analyze query performance, detect N+1 issues, identify missing indexes, and create safe online index migrations with verification steps.

**Success Criteria**:

- N+1 queries detected and fixed
- Slow queries identified with EXPLAIN analysis
- Missing indexes detected and added
- Query performance meets acceptable thresholds (<100ms for reads, <500ms for writes)
- Index migrations are safe for production (minimal downtime)
- Performance regression tests added

---

## TL;DR - Quick Performance Checklist

**Before Merging Code:**

- [ ] Run endpoint with profiler - check query count
- [ ] No N+1 queries (queries in loops)
- [ ] Slow queries (<100ms) analyzed with EXPLAIN
- [ ] Missing indexes identified and added
- [ ] Eager loading used where appropriate
- [ ] Query count reasonable for operation (<10 queries ideal)
- [ ] Performance test added to prevent regression

**When Adding Indexes:**

- [ ] Index covers actual query patterns
- [ ] Composite index field order correct
- [ ] Index creation uses ALGORITHM=INPLACE when possible
- [ ] Verification steps included
- [ ] Index usage confirmed with EXPLAIN

---

## Quick Start: 5-Step Performance Analysis

### Step 1: Enable MySQL Slow Query Log

```bash
docker compose exec database mariadb -u root -proot
```

```sql
-- Enable slow query log
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 0.1;  -- Log queries slower than 100ms
SET GLOBAL log_queries_not_using_indexes = 'ON';

-- Verify settings
SHOW VARIABLES LIKE 'slow_query%';
SHOW VARIABLES LIKE 'long_query_time';
```

### Step 2: Run Your Endpoint

```bash
curl https://localhost/api/users
```

### Step 3: Analyze Query Patterns

```sql
-- View recent slow queries (MariaDB)
SELECT * FROM mysql.slow_log ORDER BY start_time DESC LIMIT 10;

-- Or use Symfony Profiler for detailed query analysis
-- Open: https://localhost/_profiler
```

### Step 4: Check for Performance Issues

**N+1 Problem Symptoms**:

- Same query executed many times
- Query count grows with data size
- Queries inside `foreach` loops

**Slow Query Symptoms**:

- Execution time >100ms
- EXPLAIN shows `type: ALL` (full table scan)
- High `rows` vs actual returned rows

### Step 5: Disable Slow Query Log (Production)

```sql
SET GLOBAL slow_query_log = 'OFF';
```

---

## Common Performance Issues

### Issue 1: N+1 Queries

**Detection**: 100+ queries for 100 records

**Fix**: Use eager loading with Doctrine

```php
// ❌ BAD: N+1 problem
$users = $repository->findAll();  // 1 query
foreach ($users as $user) {
    $token = $user->getConfirmationToken();  // N queries if lazy loaded!
}

// ✅ GOOD: Eager loading with QueryBuilder
$qb = $this->createQueryBuilder('u');
$qb->leftJoin('u.confirmationToken', 't')
   ->addSelect('t');  // Eager load tokens
$users = $qb->getQuery()->getResult();
```

**See**: [examples/n-plus-one-detection.md](examples/n-plus-one-detection.md) for complete guide

---

### Issue 2: Slow Queries (No Index)

**Detection**: EXPLAIN shows `type: ALL`, execution time >100ms

**Fix**: Add index

```sql
-- Check query performance
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';

-- If type: ALL → add index
```

**Add index in Doctrine migration**:

```php
// migrations/VersionXXX.php
public function up(Schema $schema): void
{
    $this->addSql('CREATE INDEX idx_users_email ON users (email)');
}
```

**Or in XML mapping**:

```xml
<!-- config/doctrine/User.orm.xml -->
<indexes>
    <index name="idx_email" columns="email"/>
</indexes>
```

**See**: [examples/slow-query-analysis.md](examples/slow-query-analysis.md) for EXPLAIN interpretation

---

### Issue 3: Missing Indexes on Filtered Fields

**Detection**: Queries filter/sort on fields without indexes

**Common patterns needing indexes**:

- WHERE clause fields: `email = ?`, `status = ?`
- ORDER BY fields: `created_at DESC`
- Composite filters: `status = ? AND type = ?`
- Foreign keys: `user_id`, `token_id`

**Cursor pagination + UUID index strategy (this repo)**:

This service uses **cursor pagination** on `id` (UUID). For pagination with filters, use a **composite index**:

```xml
<indexes>
    <index name="idx_status_id" columns="status,id"/>
</indexes>
```

**See**: [reference/index-strategies.md](reference/index-strategies.md) for index selection guide

---

## Performance Thresholds

| Operation                  | Target | Max Acceptable |
| -------------------------- | ------ | -------------- |
| GET single                 | <50ms  | 100ms          |
| GET collection (100 items) | <200ms | 500ms          |
| POST/PATCH/PUT             | <100ms | 300ms          |
| Query count per endpoint   | <5     | 10             |

**See**: [reference/performance-thresholds.md](reference/performance-thresholds.md) for complete thresholds

---

## Safe Index Migrations

**MariaDB 11.4+** supports online DDL:

- Most index operations are **non-blocking** with `ALGORITHM=INPLACE`
- InnoDB allows concurrent reads and writes during index builds
- **Note**: Large tables may still cause brief locks at start/end

**Recommendation**: For production index builds, schedule during low-traffic periods for very large tables.

### Production Migration Strategy

1. **Create Doctrine migration with index**
2. **Use ALGORITHM=INPLACE** for non-blocking creation
3. **Schedule during low traffic** for large tables
4. **Run migration**: `make doctrine-migrations-migrate`
5. **Verify index created**: `SHOW INDEX FROM table_name`
6. **Verify index is used**: Run EXPLAIN on queries
7. **Measure performance improvement**

```php
// Migration example with online DDL
public function up(Schema $schema): void
{
    $this->addSql('CREATE INDEX idx_users_email ON users (email) ALGORITHM=INPLACE LOCK=NONE');
}
```

---

## Performance Testing

```php
final class UserEndpointPerformanceTest extends ApiTestCase
{
    public function testNoN1Queries(): void
    {
        // Arrange: Create test data
        for ($i = 0; $i < 50; $i++) {
            $this->createUser();
        }

        // Act: Enable query counter
        $this->enableQueryCounter();
        $this->client->request('GET', '/api/users');

        // Assert: Should have minimal queries
        $queryCount = $this->getQueryCount();
        $this->assertLessThan(10, $queryCount, 'N+1 query detected!');
    }

    public function testEndpointPerformance(): void
    {
        // Measure response time
        $start = microtime(true);
        $response = $this->client->request('GET', '/api/users');
        $duration = (microtime(true) - $start) * 1000;

        // Assert: Should be fast
        $this->assertLessThan(200, $duration, "Too slow: {$duration}ms");
    }
}
```

---

## Quick Commands Reference

```bash
# Connect to MySQL
docker compose exec database mariadb -u root -proot db
```

```sql
-- Enable slow query log
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 0.1;

-- View slow queries
SELECT * FROM mysql.slow_log ORDER BY start_time DESC LIMIT 10;

-- Check indexes
SHOW INDEX FROM users;

-- EXPLAIN query
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';

-- EXPLAIN with extended info
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';

-- IMPORTANT: Disable slow query log in production
SET GLOBAL slow_query_log = 'OFF';
```

```bash
# Create migration
make doctrine-migrations-generate

# Run migration
make doctrine-migrations-migrate

# Validate schema
docker compose exec php bin/console doctrine:schema:validate
```

---

## Workflow Integration

### When to Use This Skill

**Use after**:

- [api-platform-crud](../api-platform-crud/SKILL.md) - After creating endpoints
- [database-migrations](../database-migrations/SKILL.md) - After adding entities

**Use before**:

- [load-testing](../load-testing/SKILL.md) - Optimize before load testing
- [ci-workflow](../ci-workflow/SKILL.md) - Validate performance in CI

**Related skills**:

- [testing-workflow](../testing-workflow/SKILL.md) - Add performance tests
- [documentation-sync](../documentation-sync/SKILL.md) - Document performance changes

---

## Reference Documentation

### Examples (Detailed Scenarios)

- **[examples/README.md](examples/README.md)** - Examples index
- **[examples/n-plus-one-detection.md](examples/n-plus-one-detection.md)** - Complete N+1 detection and fix guide
- **[examples/slow-query-analysis.md](examples/slow-query-analysis.md)** - EXPLAIN analysis walkthrough

### Reference Guides

- **[reference/performance-thresholds.md](reference/performance-thresholds.md)** - Acceptable performance limits
- **[reference/mysql-slow-query-guide.md](reference/mysql-slow-query-guide.md)** - Complete slow query log documentation
- **[reference/index-strategies.md](reference/index-strategies.md)** - When to use which index type

---

## Comparison: This Skill vs database-migrations

| Aspect      | query-performance-analysis | database-migrations          |
| ----------- | -------------------------- | ---------------------------- |
| **Purpose** | **WHAT** indexes to add    | **HOW** to create indexes    |
| **Focus**   | Performance analysis       | Schema definition            |
| **Tools**   | EXPLAIN, slow query log    | Doctrine migrations, XML     |
| **When**    | Debugging slow queries     | Creating entities/migrations |
| **Output**  | Performance insights       | Migration files, XML config  |

**Workflow**: Use this skill to **identify** needed indexes, then use database-migrations for **migration syntax**.

---

## Troubleshooting

**Issue**: Can't enable slow query log

**Solution**: Verify MySQL permissions, ensure connected to correct database

---

**Issue**: EXPLAIN shows ALL but index exists

**Solution**:

1. Verify index covers your query pattern
2. Check composite index field order
3. Ensure query uses indexed fields exactly
4. Check if optimizer chooses full scan for small tables

---

**Issue**: Container name error

**Solution**: Use `database` as the service name:

```bash
docker compose exec database mariadb -u root -proot  # ✅ Correct
docker compose exec mysql mariadb -u root -proot     # ❌ Wrong
```

---

**Issue**: Symfony Profiler not showing queries

**Solution**: Enable profiler in dev mode:

```yaml
# config/packages/dev/web_profiler.yaml
web_profiler:
  toolbar: true
  intercept_redirects: false
```

---

## External Resources

- **[MySQL EXPLAIN Documentation](https://dev.mysql.com/doc/refman/8.0/en/explain.html)**
- **[MariaDB Query Optimization](https://mariadb.com/kb/en/query-optimization/)**
- **[Doctrine Performance Tips](https://www.doctrine-project.org/projects/doctrine-orm/en/current/reference/improving-performance.html)**
- **[Symfony Profiler](https://symfony.com/doc/current/profiler.html)**

---

## Best Practices

### DO ✅

- Use Symfony Profiler in development for every new feature
- Analyze queries before deploying to production
- Add performance tests to prevent regressions
- Use eager loading to prevent N+1 queries
- Create indexes for frequently filtered/sorted fields
- Use EXPLAIN ANALYZE for detailed query plans

### DON'T ❌

- Leave slow query log enabled in production at low threshold
- Add indexes without analyzing query patterns
- Ignore N+1 warnings (they compound quickly)
- Skip EXPLAIN analysis before adding indexes
- Forget to verify index is actually used after creation
- Add indexes on every column (write overhead)
