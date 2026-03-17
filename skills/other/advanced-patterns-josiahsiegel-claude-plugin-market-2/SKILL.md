---
name: advanced-patterns
description: |
  Advanced T-SQL patterns and techniques for SQL Server. Use this skill when: (1) User needs help with CTEs or recursive queries, (2) User asks about APPLY operator, (3) User wants MERGE or OUTPUT clause help, (4) User works with temporal tables, (5) User needs In-Memory OLTP guidance, (6) User asks about advanced grouping (ROLLUP, CUBE, GROUPING SETS).
---

# Advanced T-SQL Patterns

Advanced techniques for complex SQL Server scenarios.

## Quick Reference

### Pattern Selection Guide

| Task | Pattern |
|------|---------|
| Hierarchical data | Recursive CTE |
| Top N per group | ROW_NUMBER + CTE |
| Correlated subquery alternative | CROSS/OUTER APPLY |
| Upsert (insert or update) | MERGE |
| Capture modified rows | OUTPUT clause |
| Historical data tracking | Temporal tables |
| High-throughput OLTP | In-Memory OLTP |
| Multiple aggregation levels | ROLLUP/CUBE/GROUPING SETS |

## Common Table Expressions (CTEs)

### Basic CTE
```sql
WITH RecentOrders AS (
    SELECT CustomerID, OrderDate, Amount
    FROM Orders
    WHERE OrderDate >= DATEADD(month, -3, GETDATE())
)
SELECT c.CustomerName, r.Amount
FROM Customers c
JOIN RecentOrders r ON c.CustomerID = r.CustomerID;
```

### Multiple CTEs
```sql
WITH
Sales AS (
    SELECT ProductID, SUM(Amount) AS TotalSales FROM Orders GROUP BY ProductID
),
Inventory AS (
    SELECT ProductID, SUM(Quantity) AS TotalInventory FROM Stock GROUP BY ProductID
)
SELECT p.ProductName, s.TotalSales, i.TotalInventory
FROM Products p
LEFT JOIN Sales s ON p.ProductID = s.ProductID
LEFT JOIN Inventory i ON p.ProductID = i.ProductID;
```

### Recursive CTE (Hierarchies)
```sql
WITH OrgChart AS (
    -- Anchor: Top-level (no manager)
    SELECT EmployeeID, Name, ManagerID, 0 AS Level,
           CAST(Name AS VARCHAR(1000)) AS Path
    FROM Employees
    WHERE ManagerID IS NULL

    UNION ALL

    -- Recursive: Subordinates
    SELECT e.EmployeeID, e.Name, e.ManagerID, oc.Level + 1,
           CAST(oc.Path + ' > ' + e.Name AS VARCHAR(1000))
    FROM Employees e
    JOIN OrgChart oc ON e.ManagerID = oc.EmployeeID
)
SELECT * FROM OrgChart
OPTION (MAXRECURSION 100);  -- Default is 100, max is 32767
```

### CTE for Deleting Duplicates
```sql
WITH Duplicates AS (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY Email
               ORDER BY CreatedDate DESC
           ) AS RowNum
    FROM Users
)
DELETE FROM Duplicates WHERE RowNum > 1;
```

## APPLY Operator

### CROSS APPLY (Inner Join Behavior)
```sql
-- Top 3 orders per customer
SELECT c.CustomerID, c.Name, o.OrderID, o.Amount
FROM Customers c
CROSS APPLY (
    SELECT TOP 3 OrderID, Amount
    FROM Orders
    WHERE CustomerID = c.CustomerID
    ORDER BY OrderDate DESC
) o;
```

### OUTER APPLY (Left Join Behavior)
```sql
-- Last order per customer (including customers with no orders)
SELECT c.CustomerID, c.Name, o.LastOrderDate, o.LastOrderAmount
FROM Customers c
OUTER APPLY (
    SELECT TOP 1 OrderDate AS LastOrderDate, Amount AS LastOrderAmount
    FROM Orders
    WHERE CustomerID = c.CustomerID
    ORDER BY OrderDate DESC
) o;
```

### APPLY with Table-Valued Function
```sql
-- Call function for each row
SELECT c.CustomerID, f.MonthlyTotal, f.OrderCount
FROM Customers c
CROSS APPLY dbo.GetCustomerMonthlyStats(c.CustomerID) f;
```

### APPLY to Unpivot Columns
```sql
-- Transform columns to rows
SELECT ID, AttributeName, AttributeValue
FROM Products
CROSS APPLY (
    VALUES
        ('Color', Color),
        ('Size', Size),
        ('Weight', CAST(Weight AS VARCHAR))
) AS Unpivoted(AttributeName, AttributeValue)
WHERE AttributeValue IS NOT NULL;
```

## MERGE Statement

### Basic Upsert
```sql
MERGE INTO TargetTable AS t
USING SourceTable AS s
ON t.ID = s.ID
WHEN MATCHED THEN
    UPDATE SET t.Name = s.Name, t.Value = s.Value, t.UpdatedAt = GETDATE()
WHEN NOT MATCHED BY TARGET THEN
    INSERT (ID, Name, Value, CreatedAt)
    VALUES (s.ID, s.Name, s.Value, GETDATE())
WHEN NOT MATCHED BY SOURCE THEN
    DELETE
OUTPUT $action, inserted.*, deleted.*;
```

### MERGE with Conditions
```sql
MERGE INTO Products AS t
USING StagingProducts AS s
ON t.ProductID = s.ProductID
WHEN MATCHED AND s.Price <> t.Price THEN
    UPDATE SET t.Price = s.Price, t.LastModified = GETDATE()
WHEN MATCHED AND s.Discontinued = 1 THEN
    DELETE
WHEN NOT MATCHED THEN
    INSERT (ProductID, Name, Price) VALUES (s.ProductID, s.Name, s.Price);
```

## OUTPUT Clause

### Capture Inserted Rows
```sql
DECLARE @InsertedRows TABLE (ID INT, Name VARCHAR(100));

INSERT INTO Customers (Name, Email)
OUTPUT inserted.CustomerID, inserted.Name INTO @InsertedRows
VALUES ('John', 'john@email.com'), ('Jane', 'jane@email.com');

SELECT * FROM @InsertedRows;
```

### Capture Updated Rows (Before and After)
```sql
UPDATE Products
SET Price = Price * 1.1
OUTPUT deleted.ProductID, deleted.Price AS OldPrice, inserted.Price AS NewPrice
WHERE Category = 'Electronics';
```

### Capture Deleted Rows
```sql
DELETE FROM ExpiredOrders
OUTPUT deleted.*
INTO OrderArchive
WHERE ExpiryDate < DATEADD(year, -1, GETDATE());
```

## Advanced Grouping

### ROLLUP (Hierarchical Subtotals)
```sql
SELECT
    COALESCE(Region, 'Total') AS Region,
    COALESCE(Product, 'All Products') AS Product,
    SUM(Sales) AS TotalSales
FROM SalesData
GROUP BY ROLLUP (Region, Product);
-- Groups: (Region, Product), (Region), ()
```

### CUBE (All Combinations)
```sql
SELECT Region, Product, SUM(Sales) AS TotalSales
FROM SalesData
GROUP BY CUBE (Region, Product);
-- Groups: (Region, Product), (Region), (Product), ()
```

### GROUPING SETS (Custom Combinations)
```sql
SELECT Region, Product, Year, SUM(Sales)
FROM SalesData
GROUP BY GROUPING SETS (
    (Region, Product),
    (Region, Year),
    (Product),
    ()
);
```

### Identify Grouping Level
```sql
SELECT
    CASE WHEN GROUPING(Region) = 1 THEN 'All' ELSE Region END AS Region,
    CASE WHEN GROUPING(Product) = 1 THEN 'All' ELSE Product END AS Product,
    SUM(Sales) AS TotalSales,
    GROUPING_ID(Region, Product) AS GroupLevel
    -- GroupLevel: 0 = both, 1 = Product rolled up, 2 = Region rolled up, 3 = both
FROM SalesData
GROUP BY ROLLUP (Region, Product);
```

## Temporal Tables (SQL 2016+)

### Create System-Versioned Table
```sql
CREATE TABLE Products (
    ProductID INT PRIMARY KEY,
    Name NVARCHAR(100),
    Price DECIMAL(18,2),
    ValidFrom DATETIME2 GENERATED ALWAYS AS ROW START,
    ValidTo DATETIME2 GENERATED ALWAYS AS ROW END,
    PERIOD FOR SYSTEM_TIME (ValidFrom, ValidTo)
)
WITH (SYSTEM_VERSIONING = ON (HISTORY_TABLE = dbo.ProductsHistory));
```

### Query Historical Data
```sql
-- Point in time
SELECT * FROM Products
FOR SYSTEM_TIME AS OF '2024-01-01 12:00:00';

-- Time range
SELECT * FROM Products
FOR SYSTEM_TIME BETWEEN '2024-01-01' AND '2024-06-30';

-- All history
SELECT * FROM Products
FOR SYSTEM_TIME ALL;
```

## In-Memory OLTP

### Create Memory-Optimized Table
```sql
-- First add filegroup
ALTER DATABASE YourDB
ADD FILEGROUP MemOptFG CONTAINS MEMORY_OPTIMIZED_DATA;

ALTER DATABASE YourDB
ADD FILE (NAME = 'MemOptFile', FILENAME = 'C:\Data\MemOpt') TO FILEGROUP MemOptFG;

-- Create table
CREATE TABLE OrdersMemOpt (
    OrderID INT NOT NULL PRIMARY KEY NONCLUSTERED HASH WITH (BUCKET_COUNT = 1000000),
    CustomerID INT NOT NULL INDEX IX_Customer NONCLUSTERED HASH WITH (BUCKET_COUNT = 100000),
    OrderDate DATETIME2 NOT NULL,
    Amount DECIMAL(18,2) NOT NULL,
    INDEX IX_Date NONCLUSTERED (OrderDate)
) WITH (MEMORY_OPTIMIZED = ON, DURABILITY = SCHEMA_AND_DATA);
```

### Natively Compiled Procedure
```sql
CREATE PROCEDURE InsertOrderFast
    @CustomerID INT,
    @Amount DECIMAL(18,2)
WITH NATIVE_COMPILATION, SCHEMABINDING
AS
BEGIN ATOMIC WITH (TRANSACTION ISOLATION LEVEL = SNAPSHOT, LANGUAGE = N'English')
    INSERT INTO dbo.OrdersMemOpt (OrderID, CustomerID, OrderDate, Amount)
    VALUES (NEXT VALUE FOR dbo.OrderSeq, @CustomerID, SYSDATETIME(), @Amount);
END;
```

## Table-Valued Constructor

### VALUES as Table
```sql
SELECT * FROM (
    VALUES
        (1, 'Apple', 1.50),
        (2, 'Banana', 0.75),
        (3, 'Orange', 2.00)
) AS Products(ID, Name, Price);
```

### Use in MERGE
```sql
MERGE INTO Products AS t
USING (VALUES
    (1, 'Apple', 1.60),
    (2, 'Banana', 0.80)
) AS s(ID, Name, Price)
ON t.ID = s.ID
WHEN MATCHED THEN UPDATE SET Price = s.Price
WHEN NOT MATCHED THEN INSERT VALUES (s.ID, s.Name, s.Price);
```

## Sequences

### Create and Use Sequence
```sql
CREATE SEQUENCE OrderSeq
    AS INT START WITH 1 INCREMENT BY 1;

-- Get next value
SELECT NEXT VALUE FOR OrderSeq;

-- Use in INSERT
INSERT INTO Orders (OrderID, CustomerID)
VALUES (NEXT VALUE FOR OrderSeq, @CustomerID);

-- Use as default
ALTER TABLE Orders
ADD CONSTRAINT DF_OrderID DEFAULT NEXT VALUE FOR OrderSeq FOR OrderID;
```

