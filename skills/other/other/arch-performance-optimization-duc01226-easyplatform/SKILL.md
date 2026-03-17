---
name: arch-performance-optimization
version: 1.1.0
description: '[Architecture] Use when analyzing and improving performance for database queries, API endpoints, or frontend rendering.'
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Task
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

**Prerequisites:** **MUST READ** `.claude/skills/shared/evidence-based-reasoning-protocol.md` before executing.

## Quick Summary

**Goal:** Analyze and resolve performance bottlenecks across database, API, network, and frontend layers.

**Workflow:**

1. **Identify Bottleneck** — Classify as database, API, network, or frontend issue
2. **Measure Baseline** — Gather metrics before changes (response time, query time, bundle size)
3. **Optimize** — Apply layer-specific fixes (indexes, caching, lazy loading, OnPush)
4. **Verify** — Measure again and confirm improvement without regressions

**Key Rules:**

- Never use `SELECT *` or unbounded result sets in production
- Always use async I/O; never block threads with `.Result`
- Avoid N+1 queries — use eager loading or batch fetching
- Use bounded parallelism (`ParallelAsync` with `maxConcurrent`) for background jobs

# Performance Optimization Workflow

## When to Use This Skill

- Slow API response times
- Database query optimization
- Frontend rendering issues
- Memory usage concerns
- Scalability planning

## Pre-Flight Checklist

- [ ] Identify performance bottleneck
- [ ] Gather baseline metrics
- [ ] Determine acceptable thresholds
- [ ] Plan measurement approach

## Performance Analysis Framework

### Step 1: Identify Bottleneck Type

```
Performance Issue
├── Database (slow queries, N+1)
├── API (serialization, processing)
├── Network (payload size, latency)
└── Frontend (rendering, bundle size)
```

### Step 2: Measure Baseline

```bash
# API response time
curl -w "@curl-format.txt" -o /dev/null -s "http://api/endpoint"

# Database query time (SQL Server)
SET STATISTICS TIME ON;
SELECT * FROM Table WHERE ...;

# Frontend bundle analysis
npm run build -- --stats-json
npx webpack-bundle-analyzer stats.json
```

## Database Optimization

**⚠️ MUST READ:** CLAUDE.md for N+1 detection, eager loading, projection, paging, and parallel query patterns. See `database-optimization` skill for advanced index and query optimization.

### Index Recommendations

```sql
-- Frequently filtered columns
CREATE INDEX IX_Employee_CompanyId ON Employees(CompanyId);
CREATE INDEX IX_Employee_Status ON Employees(Status);

-- Composite index for common queries
CREATE INDEX IX_Employee_Company_Status
ON Employees(CompanyId, Status)
INCLUDE (FullName, Email);

-- Full-text search index
CREATE FULLTEXT INDEX ON Employees(FullName, Email);
```

## API Optimization

**⚠️ MUST READ:** CLAUDE.md for parallel tuple queries and response DTO patterns.

### Caching

```csharp
// Static data caching
private static readonly ConcurrentDictionary<string, LookupData> _cache = new();

public async Task<LookupData> GetLookupAsync(string key)
{
    if (_cache.TryGetValue(key, out var cached))
        return cached;

    var data = await LoadFromDbAsync(key);
    _cache.TryAdd(key, data);
    return data;
}
```

## Frontend Optimization

### Bundle Size

```typescript
// :x: Import entire library
import _ from 'lodash';

// :white_check_mark: Import specific functions
import { debounce } from 'lodash-es/debounce';
```

### Lazy Loading

```typescript
// :white_check_mark: Lazy load routes
const routes: Routes = [
    {
        path: 'feature',
        loadChildren: () => import('./feature/feature.module').then(m => m.FeatureModule)
    }
];
```

### Change Detection

```typescript
// :white_check_mark: OnPush for performance
@Component({
  changeDetection: ChangeDetectionStrategy.OnPush
})

// :white_check_mark: Track-by for lists
trackByItem = this.ngForTrackByItemProp<Item>('id');

// Template
@for (item of items; track trackByItem)
```

### Virtual Scrolling

```typescript
// For large lists
import { CdkVirtualScrollViewport } from '@angular/cdk/scrolling';

<cdk-virtual-scroll-viewport itemSize="50">
  @for (item of items; track item.id) {
    <div class="item">{{ item.name }}</div>
  }
</cdk-virtual-scroll-viewport>
```

## Background Job Optimization

**⚠️ MUST READ:** CLAUDE.md for bounded parallelism (`ParallelAsync` with `maxConcurrent`) and batch processing (`UpdateManyAsync`) patterns.

## Performance Monitoring

### Logging Slow Operations

```csharp
var sw = Stopwatch.StartNew();
var result = await ExecuteOperation();
sw.Stop();

if (sw.ElapsedMilliseconds > 1000)
    Logger.LogWarning("Slow operation: {Ms}ms", sw.ElapsedMilliseconds);
```

### Database Query Logging

```csharp
// In DbContext configuration
optionsBuilder.LogTo(
    Console.WriteLine,
    new[] { DbLoggerCategory.Database.Command.Name },
    LogLevel.Information);
```

## Performance Checklist

### Database

- [ ] Indexes on filtered columns
- [ ] Eager loading for relations
- [ ] Projection for partial data
- [ ] Paging at database level
- [ ] No N+1 queries

### API

- [ ] Parallel operations where possible
- [ ] Response DTOs (not entities)
- [ ] Caching for static data
- [ ] Pagination for lists

### Frontend

- [ ] Lazy loading for routes
- [ ] OnPush change detection
- [ ] Track-by for lists
- [ ] Virtual scrolling for large lists
- [ ] Tree-shaking imports

### Background Jobs

- [ ] Bounded parallelism
- [ ] Batch operations
- [ ] Paged processing
- [ ] Appropriate scheduling

## Anti-Patterns to AVOID

:x: **SELECT \* in production**

```csharp
var all = await context.Table.ToListAsync();
```

:x: **Synchronous I/O**

```csharp
var result = asyncOperation.Result;  // Blocks thread
```

:x: **Unbounded result sets**

```csharp
await repo.GetAllAsync();  // Could be millions
```

:x: **Repeated database calls in loops**

```csharp
foreach (var id in ids)
    await repo.GetByIdAsync(id);  // N queries
```

## Verification Checklist

- [ ] Baseline metrics recorded
- [ ] Bottleneck identified and addressed
- [ ] Changes measured against baseline
- [ ] No new performance issues introduced
- [ ] Monitoring in place

## Related

- `arch-security-review`
- `database-optimization`

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
