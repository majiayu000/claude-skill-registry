---
name: index-strategies
description: |
  SQL Server index design and optimization strategies. Use this skill when: (1) User needs help designing indexes, (2) User asks about clustered vs nonclustered indexes, (3) User wants to optimize columnstore indexes, (4) User needs filtered or covering indexes, (5) User asks about index maintenance and fragmentation.
---

# Index Strategies

Comprehensive guide to SQL Server index design and optimization.

## Quick Reference

### Index Types

| Type | Description | Best For |
|------|-------------|----------|
| Clustered | Table data order | Primary access path, range scans |
| Nonclustered | Separate structure | Specific query patterns |
| Columnstore | Column-based storage | Analytics, aggregations |
| Filtered | Partial index | Well-known subsets |
| Covering | All columns needed | Avoiding key lookups |

### Clustered Index Guidelines

**Ideal Clustered Key:**
- Narrow (small data type)
- Unique or mostly unique
- Ever-increasing (identity, sequential GUID)
- Static (rarely updated)

```sql
-- Good: Identity column
CREATE CLUSTERED INDEX CIX_Orders ON Orders(OrderID);

-- Good: Sequential GUID
CREATE TABLE Orders (
    OrderID UNIQUEIDENTIFIER DEFAULT NEWSEQUENTIALID() PRIMARY KEY CLUSTERED
);

-- Avoid: Wide composite keys, frequently updated columns, GUIDs (NEWID)
```

### Nonclustered Index Design

```sql
-- Basic index
CREATE NONCLUSTERED INDEX IX_Orders_CustomerID
ON Orders(CustomerID);

-- Covering index (avoids key lookup)
CREATE NONCLUSTERED INDEX IX_Orders_CustomerID_Cover
ON Orders(CustomerID)
INCLUDE (OrderDate, TotalAmount, Status);

-- Filtered index (partial)
CREATE NONCLUSTERED INDEX IX_Orders_Active
ON Orders(CustomerID, OrderDate)
WHERE Status = 'Active';

-- Descending order
CREATE NONCLUSTERED INDEX IX_Orders_DateDesc
ON Orders(OrderDate DESC, OrderID DESC);
```

## Index Selection Guide

### By Query Pattern

| Pattern | Recommended Index |
|---------|-------------------|
| `WHERE Col = value` | Nonclustered on Col |
| `WHERE Col = v1 AND Col2 = v2` | Nonclustered on (Col, Col2) |
| `WHERE Col = v ORDER BY Col2` | Nonclustered on (Col, Col2) |
| `WHERE Col BETWEEN x AND y` | Col as leftmost key |
| `SELECT * WHERE Col = v` | Clustered or covering NC |
| Large aggregations | Columnstore |
| Specific subset queries | Filtered index |

### Column Order in Composite Keys

```sql
-- Order matters! Left-to-right matching
CREATE INDEX IX_Example ON Table(A, B, C);

-- These queries CAN use the index:
WHERE A = 1
WHERE A = 1 AND B = 2
WHERE A = 1 AND B = 2 AND C = 3
WHERE A = 1 AND B > 5 ORDER BY B

-- These queries CANNOT use index seek:
WHERE B = 2                    -- A not specified
WHERE B = 2 AND C = 3          -- A not specified
WHERE A = 1 AND C = 3          -- B skipped (partial match only)
```

## Columnstore Indexes

### Clustered Columnstore
```sql
-- Best for data warehousing
CREATE CLUSTERED COLUMNSTORE INDEX CCI_FactSales
ON FactSales;

-- Ordered columnstore (SQL 2022+)
CREATE CLUSTERED COLUMNSTORE INDEX CCI_FactSales
ON FactSales
ORDER (DateKey, ProductKey);
```

### Nonclustered Columnstore
```sql
-- Hybrid OLTP/OLAP
CREATE NONCLUSTERED COLUMNSTORE INDEX NCCI_Orders_Analysis
ON Orders(OrderDate, ProductID, Quantity, Amount)
WHERE Status = 'Completed';
```

### Columnstore Best Practices
1. **Load batches >= 102,400 rows** - Creates compressed segments
2. **Order data by filtered columns** - Better segment elimination
3. **Use REORGANIZE, not REBUILD** - More efficient maintenance
4. **Avoid frequent small updates** - Causes deltastore fragmentation
5. **Partition by date** - Enables partition elimination

```sql
-- Maintenance
ALTER INDEX CCI_FactSales ON FactSales REORGANIZE;

-- Check fragmentation
SELECT
    object_name(object_id) AS TableName,
    index_id,
    avg_fragmentation_in_percent,
    fragment_count
FROM sys.dm_db_index_physical_stats(DB_ID(), NULL, NULL, NULL, 'LIMITED');
```

## Filtered Indexes

```sql
-- Index active orders only
CREATE NONCLUSTERED INDEX IX_Orders_Active
ON Orders(CustomerID, OrderDate)
WHERE Status = 'Active';

-- Index non-NULL values
CREATE UNIQUE INDEX IX_Users_Email
ON Users(Email)
WHERE Email IS NOT NULL;

-- Constraints:
-- - Cannot use variable in filter
-- - Query WHERE must match or be subset of filter WHERE
-- - May cause parameter sniffing issues
```

## Covering Indexes

```sql
-- Eliminate key lookups
-- Original: Index on CustomerID, query selects OrderDate, Amount
-- Execution plan shows Key Lookup

-- Solution: Covering index
CREATE INDEX IX_Orders_CustomerID_Cover
ON Orders(CustomerID)
INCLUDE (OrderDate, Amount, Status);

-- INCLUDE columns:
-- - Not in key (not sorted)
-- - Stored at leaf level only
-- - Don't contribute to 900-byte key limit
-- - Perfect for frequently selected columns
```

## Index Maintenance

### Fragmentation Guidelines

| Fragmentation % | Action |
|-----------------|--------|
| < 5% | None needed |
| 5-30% | REORGANIZE |
| > 30% | REBUILD |

```sql
-- Reorganize (online, minimal locking)
ALTER INDEX IX_Orders_CustomerID ON Orders REORGANIZE;

-- Rebuild (offline by default, more thorough)
ALTER INDEX IX_Orders_CustomerID ON Orders REBUILD;

-- Online rebuild (Enterprise Edition)
ALTER INDEX IX_Orders_CustomerID ON Orders
REBUILD WITH (ONLINE = ON);

-- Resumable rebuild (SQL 2017+)
ALTER INDEX IX_Orders_CustomerID ON Orders
REBUILD WITH (ONLINE = ON, RESUMABLE = ON, MAX_DURATION = 60);

-- Resume interrupted rebuild
ALTER INDEX IX_Orders_CustomerID ON Orders RESUME;
```

### Statistics Update
```sql
-- Update after index changes
UPDATE STATISTICS Orders;

-- Full scan for accurate stats
UPDATE STATISTICS Orders WITH FULLSCAN;

-- Check last update
SELECT
    OBJECT_NAME(object_id) AS TableName,
    name AS StatsName,
    STATS_DATE(object_id, stats_id) AS LastUpdated
FROM sys.stats
WHERE object_id = OBJECT_ID('Orders');
```

## Performance Monitoring

### Index Usage Stats
```sql
SELECT
    OBJECT_NAME(i.object_id) AS TableName,
    i.name AS IndexName,
    ius.user_seeks,
    ius.user_scans,
    ius.user_lookups,
    ius.user_updates
FROM sys.indexes i
LEFT JOIN sys.dm_db_index_usage_stats ius
    ON i.object_id = ius.object_id
    AND i.index_id = ius.index_id
WHERE OBJECTPROPERTY(i.object_id, 'IsUserTable') = 1
ORDER BY ius.user_seeks + ius.user_scans DESC;
```

### Missing Index Recommendations
```sql
SELECT
    migs.avg_user_impact AS ImpactPercent,
    mid.statement AS TableName,
    mid.equality_columns,
    mid.inequality_columns,
    mid.included_columns
FROM sys.dm_db_missing_index_groups mig
JOIN sys.dm_db_missing_index_group_stats migs
    ON mig.index_group_handle = migs.group_handle
JOIN sys.dm_db_missing_index_details mid
    ON mig.index_handle = mid.index_handle
ORDER BY migs.avg_user_impact DESC;
```

