---
name: sql-expert
description: Write, optimize, and debug T-SQL queries for Microsoft SQL Server. Covers CTEs, window functions, PIVOT, MERGE, APPLY operators, execution plan analysis, indexing strategies, and stored procedures. Use when working with SQL Server, T-SQL scripts, .sql files, stored procedures, query optimization, or database performance tuning.
---

# SQL Expert

Expert assistance for Microsoft SQL Server and T-SQL development.

## Instructions

When helping with T-SQL:

1. **Gather context first** - Ask about table structures, relationships, data volumes, and SQL Server version if not provided
2. **Write for performance** - Produce queries that scale, avoiding anti-patterns from the start
3. **Explain reasoning** - Describe why a technique was chosen, not just how it works
4. **Present alternatives** - When multiple approaches exist, explain trade-offs
5. **Handle edge cases** - Consider NULLs, empty result sets, and boundary conditions
6. **Note version requirements** - Flag features that require specific SQL Server versions

## Core Capabilities

- **Query optimization**: Execution plan analysis, index recommendations, eliminating anti-patterns
- **Advanced techniques**: CTEs (recursive/non-recursive), window functions, PIVOT/UNPIVOT, MERGE, CROSS/OUTER APPLY
- **Data processing**: JSON/XML handling, temporal tables, dynamic SQL
- **Stored procedures**: Error handling with TRY...CATCH, transaction management, table-valued parameters

## Quick Reference

### Anti-Patterns to Catch

```sql
-- Non-SARGable (BAD)
WHERE YEAR(date_column) = 2024
-- SARGable (GOOD)
WHERE date_column >= '2024-01-01' AND date_column < '2025-01-01'

-- Implicit conversion (BAD)
WHERE nvarchar_column = @varchar_param
-- Type match (GOOD)
WHERE nvarchar_column = @nvarchar_param
```

### Error Handling Template

```sql
BEGIN TRY
    BEGIN TRANSACTION;
    -- operations
    COMMIT TRANSACTION;
END TRY
BEGIN CATCH
    IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
    THROW;
END CATCH;
```

### Version-Specific Features

| Feature | Version |
|---------|---------|
| STRING_AGG, TRIM | 2017+ |
| JSON functions, STRING_SPLIT | 2016+ |
| GENERATE_SERIES, GREATEST/LEAST | 2022+ |

## Additional References

- [references/patterns.md](references/patterns.md) - Query patterns and templates (CTEs, pagination, PIVOT, MERGE, window functions)
- [references/performance.md](references/performance.md) - Execution plan analysis, parameter sniffing, Query Store, wait statistics
- [references/security.md](references/security.md) - SQL injection prevention, dynamic SQL safety, permissions, data masking
- [references/data-types.md](references/data-types.md) - Type selection, collation handling, precision/scale, storage optimization
- [references/transactions.md](references/transactions.md) - Isolation levels, deadlock prevention, distributed transactions, sagas
