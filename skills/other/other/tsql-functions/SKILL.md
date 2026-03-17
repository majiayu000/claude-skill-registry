---
name: tsql-functions
description: |
  Complete T-SQL function reference for SQL Server and Azure SQL Database. Use this skill when: (1) User asks about T-SQL string, date, math, or conversion functions, (2) User needs help with window/ranking functions, (3) User works with JSON or XML in T-SQL, (4) User asks about aggregate functions or GROUP BY, (5) User needs system or metadata functions.
---

# T-SQL Functions Reference

Complete reference for all T-SQL function categories with version-specific availability.

## Quick Reference

### String Functions
| Function | Description | Version |
|----------|-------------|---------|
| `CONCAT(str1, str2, ...)` | NULL-safe concatenation | 2012+ |
| `CONCAT_WS(sep, str1, ...)` | Concatenate with separator | 2017+ |
| `STRING_AGG(expr, sep)` | Aggregate strings | 2017+ |
| `STRING_SPLIT(str, sep)` | Split to rows | 2016+ |
| `STRING_SPLIT(str, sep, 1)` | With ordinal column | 2022+ |
| `TRIM([chars FROM] str)` | Remove leading/trailing | 2017+ |
| `TRANSLATE(str, from, to)` | Character replacement | 2017+ |
| `FORMAT(value, format)` | .NET format strings | 2012+ |

### Date/Time Functions
| Function | Description | Version |
|----------|-------------|---------|
| `DATEADD(part, n, date)` | Add interval | All |
| `DATEDIFF(part, start, end)` | Difference (int) | All |
| `DATEDIFF_BIG(part, s, e)` | Difference (bigint) | 2016+ |
| `EOMONTH(date, [offset])` | Last day of month | 2012+ |
| `DATETRUNC(part, date)` | Truncate to precision | 2022+ |
| `DATE_BUCKET(part, n, date)` | Group into buckets | 2022+ |
| `AT TIME ZONE 'tz'` | Timezone conversion | 2016+ |

### Window Functions
| Function | Description | Version |
|----------|-------------|---------|
| `ROW_NUMBER()` | Sequential unique numbers | 2005+ |
| `RANK()` | Rank with gaps for ties | 2005+ |
| `DENSE_RANK()` | Rank without gaps | 2005+ |
| `NTILE(n)` | Distribute into n groups | 2005+ |
| `LAG(col, n, default)` | Previous row value | 2012+ |
| `LEAD(col, n, default)` | Next row value | 2012+ |
| `FIRST_VALUE(col)` | First in window | 2012+ |
| `LAST_VALUE(col)` | Last in window | 2012+ |
| `IGNORE NULLS` | Skip NULLs in offset funcs | 2022+ |

### SQL Server 2022 New Functions
| Function | Description |
|----------|-------------|
| `GREATEST(v1, v2, ...)` | Maximum of values |
| `LEAST(v1, v2, ...)` | Minimum of values |
| `DATETRUNC(part, date)` | Truncate date |
| `GENERATE_SERIES(start, stop, [step])` | Number sequence |
| `JSON_OBJECT('key': val)` | Create JSON object |
| `JSON_ARRAY(v1, v2, ...)` | Create JSON array |
| `JSON_PATH_EXISTS(json, path)` | Check path exists |
| `IS [NOT] DISTINCT FROM` | NULL-safe comparison |

## Core Patterns

### String Manipulation
```sql
-- Concatenate with separator (NULL-safe)
SELECT CONCAT_WS(', ', FirstName, MiddleName, LastName) AS FullName

-- Split string to rows with ordinal
SELECT value, ordinal
FROM STRING_SPLIT('apple,banana,cherry', ',', 1)

-- Aggregate strings with ordering
SELECT DeptID,
       STRING_AGG(EmployeeName, ', ') WITHIN GROUP (ORDER BY HireDate)
FROM Employees
GROUP BY DeptID
```

### Date Operations
```sql
-- Truncate to first of month
SELECT DATETRUNC(month, OrderDate) AS MonthStart

-- Group by week buckets
SELECT DATE_BUCKET(week, 1, OrderDate) AS WeekBucket,
       COUNT(*) AS OrderCount
FROM Orders
GROUP BY DATE_BUCKET(week, 1, OrderDate)

-- Generate date series
SELECT CAST(value AS date) AS Date
FROM GENERATE_SERIES(
    CAST('2024-01-01' AS date),
    CAST('2024-12-31' AS date),
    1
)
```

### Window Functions
```sql
-- Running total with partitioning
SELECT OrderID, CustomerID, Amount,
       SUM(Amount) OVER (
           PARTITION BY CustomerID
           ORDER BY OrderDate
           ROWS UNBOUNDED PRECEDING
       ) AS RunningTotal
FROM Orders

-- Get previous non-NULL value (SQL 2022+)
SELECT Date, Value,
       LAST_VALUE(Value) IGNORE NULLS OVER (
           ORDER BY Date
           ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING
       ) AS PreviousNonNull
FROM Measurements
```

### JSON Operations
```sql
-- Extract scalar value
SELECT JSON_VALUE(JsonColumn, '$.customer.name') AS CustomerName

-- Parse JSON array to rows
SELECT j.ProductID, j.Quantity
FROM Orders
CROSS APPLY OPENJSON(OrderDetails)
WITH (
    ProductID INT '$.productId',
    Quantity INT '$.qty'
) AS j

-- Build JSON object (SQL 2022+)
SELECT JSON_OBJECT('id': CustomerID, 'name': CustomerName) AS CustomerJson
FROM Customers
```

## Additional References

For deeper coverage of specific function categories, see:

- `references/string-functions.md` - Complete string function reference with examples
- `references/window-functions.md` - Window and ranking functions with frame specifications
