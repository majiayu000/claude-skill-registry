---
name: performance-optimization
description: Use when analyzing and improving performance for database queries, API endpoints, or frontend rendering.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Task
---

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

### N+1 Query Detection
```csharp
// :x: N+1 Problem
var employees = await repo.GetAllAsync();
foreach (var emp in employees)
{
    // Each iteration queries database!
    Console.WriteLine(emp.Department.Name);
}

// :white_check_mark: Eager Loading
var employees = await repo.GetAllAsync(
    e => e.CompanyId == companyId,
    ct,
    e => e.Department,      // Include Department
    e => e.Manager          // Include Manager
);
```

### Query Optimization
```csharp
// :x: Loading all columns
var employees = await repo.GetAllAsync();
var names = employees.Select(e => e.Name);

// :white_check_mark: Projection
var names = await repo.GetAllAsync(
    q => q.Where(e => e.IsActive)
          .Select(e => e.Name));
```

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

### Paging Patterns
```csharp
// :x: Loading all then paging in memory
var all = await repo.GetAllAsync();
var page = all.Skip(skip).Take(take);

// :white_check_mark: Database-level paging
var page = await repo.GetAllAsync(
    (uow, q) => q
        .Where(e => e.IsActive)
        .OrderBy(e => e.Id)
        .Skip(skip)
        .Take(take));
```

## API Optimization

### Parallel Operations
```csharp
// :x: Sequential
var users = await userRepo.GetAllAsync();
var companies = await companyRepo.GetAllAsync();
var settings = await settingsRepo.GetAllAsync();

// :white_check_mark: Parallel (Tuple Await)
var (users, companies, settings) = await (
    userRepo.GetAllAsync(),
    companyRepo.GetAllAsync(),
    settingsRepo.GetAllAsync()
);
```

### Response Size
```csharp
// :x: Returning entire entity
return new Result { Employee = employee };

// :white_check_mark: Return only needed fields
return new Result
{
    Id = employee.Id,
    Name = employee.FullName,
    Status = employee.Status
};
```

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
    loadChildren: () => import('./feature/feature.module')
      .then(m => m.FeatureModule)
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

### Bounded Parallelism
```csharp
// :x: Unbounded
await items.ParallelAsync(ProcessAsync);

// :white_check_mark: Bounded
await items.ParallelAsync(ProcessAsync, maxConcurrent: 5);
```

### Batch Processing
```csharp
// :x: One at a time
foreach (var item in items)
    await repo.UpdateAsync(item);

// :white_check_mark: Batch update
await repo.UpdateManyAsync(items, dismissSendEvent: true);
```

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

:x: **SELECT * in production**
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
