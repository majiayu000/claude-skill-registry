---
name: mssql-mcp
description: Query and manage Microsoft SQL Server databases via MCP natural language interface. Execute queries, inspect schemas, modify data with built-in safety features. Use when working with SQL Server, Azure SQL Database, or building data applications on Microsoft database platforms.
---

# Microsoft SQL Server MCP Skill

Query and manage SQL Server databases through natural language interface with built-in safety features.

## Configuration

### Required Environment Variables

```bash
SERVER_NAME=myserver.database.windows.net
DATABASE_NAME=MyDatabase
```

### Optional Environment Variables

```bash
READONLY=true                  # Enable read-only mode
CONNECTION_TIMEOUT=30          # Connection timeout (seconds)
TRUST_SERVER_CERTIFICATE=true  # Accept self-signed certificates
```

### Authentication Options

**SQL Authentication:**
```bash
USER=dbusername
PASSWORD=dbpassword
```

**Windows/Azure AD:**
Use integrated authentication (no explicit credentials needed)

---

## Core Capabilities

### 1. Query Execution

Execute SQL queries through natural language requests.

**Examples:**
- "Get all users from California"
- "Show top 100 orders by date"
- "Calculate total revenue by month"
- "Find products with price > $50"

**Security:** Requires WHERE clauses for safety.

### 2. Data Modification

Create, update, and delete records.

**Insert:**
- "Add new user: John Doe, john@example.com"
- "Create product: Laptop, $999"

**Update:**
- "Update user ID 123 email to new@example.com"
- "Change order status to 'shipped' for order 456"

**Delete:**
- "Delete orders older than 1 year"
- "Remove user with ID 789"

**Security:** UPDATE and DELETE require WHERE clauses.

### 3. Schema Management

Create and modify database structures.

**Create Tables:**
- "Create users table with id, name, email"
- "Add products table with id, name, price, category"

**Modify Schema:**
- "Add phone column to customers table"
- "Create index on email in users"
- "Add foreign key from orders to customers"

**Drop Objects:**
- "Drop table temp_data"
- "Remove index idx_email from users"

### 4. Database Inspection

Explore database structure and metadata.

**Tables:**
- "List all tables"
- "Show tables in database"

**Schema:**
- "Describe users table"
- "Show structure of orders table"
- "What columns are in products table?"

**Relationships:**
- "List foreign keys"
- "Show table relationships"
- "Display indexes on orders table"

---

## Common Query Patterns

### Filtering

```
"WHERE" conditions for targeting specific records:
- "users from New York"
- "orders created this month"
- "products with price between $10 and $50"
- "customers who signed up in 2024"
```

### Aggregations

```
Calculations across datasets:
- "count of users by state"
- "total revenue by quarter"
- "average order value"
- "maximum price in each category"
```

### Sorting & Limiting

```
Ordering and constraining results:
- "top 10 orders by amount"
- "latest 50 users"
- "highest grossing products"
- "most recent transactions"
```

### Joins & Relationships

```
Combining data from multiple tables:
- "orders with customer names"
- "products with their category names"
- "users with their order counts"
- "customers and their total spend"
```

---

## Safety Features

### Mandatory WHERE Clauses

**SELECT Queries:**
Must include filtering conditions to prevent full table scans.

Good: "Get users where state = 'CA'"
Bad: "Get all users" (blocked)

**UPDATE Statements:**
Must specify which records to update.

Good: "Update email for user ID 123"
Bad: "Update all emails" (blocked)

**DELETE Statements:**
Must specify which records to delete.

Good: "Delete orders older than 2 years"
Bad: "Delete all orders" (blocked)

### Read-Only Mode

Set `READONLY=true` to:
- Disable INSERT, UPDATE, DELETE
- Allow only SELECT and schema inspection
- Safe for production database exploration
- Prevent accidental data changes

---

## SQL Server Data Types

### Numeric

- `INT`, `BIGINT`, `SMALLINT`, `TINYINT`
- `DECIMAL(p,s)`, `NUMERIC(p,s)`
- `FLOAT`, `REAL`
- `MONEY`, `SMALLMONEY`

### String

- `VARCHAR(n)`, `NVARCHAR(n)`
- `CHAR(n)`, `NCHAR(n)`
- `TEXT`, `NTEXT` (deprecated)

### Date/Time

- `DATE`, `TIME`
- `DATETIME`, `DATETIME2`
- `SMALLDATETIME`
- `DATETIMEOFFSET`

### Binary

- `BINARY(n)`, `VARBINARY(n)`
- `IMAGE` (deprecated)

### Other

- `BIT` (boolean)
- `UNIQUEIDENTIFIER` (GUID)
- `XML`
- `JSON` (via NVARCHAR)

---

## Common Schema Patterns

### Users Table

```sql
CREATE TABLE users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    username NVARCHAR(50) UNIQUE NOT NULL,
    email NVARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME2 DEFAULT GETUTCDATE(),
    updated_at DATETIME2 DEFAULT GETUTCDATE(),
    is_active BIT DEFAULT 1
);
```

### Orders Table

```sql
CREATE TABLE orders (
    id INT IDENTITY(1,1) PRIMARY KEY,
    customer_id INT NOT NULL FOREIGN KEY REFERENCES customers(id),
    order_date DATETIME2 DEFAULT GETUTCDATE(),
    total_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    created_at DATETIME2 DEFAULT GETUTCDATE()
);
```

### Products Table

```sql
CREATE TABLE products (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(100) NOT NULL,
    description NVARCHAR(MAX),
    price DECIMAL(10,2) NOT NULL,
    category_id INT FOREIGN KEY REFERENCES categories(id),
    stock_quantity INT DEFAULT 0,
    created_at DATETIME2 DEFAULT GETUTCDATE()
);
```

---

## Best Practices

### 1. Query Optimization

- Limit result sets: "top N records"
- Include time ranges: "in the last 30 days"
- Use specific filters: "where status = 'active'"
- Aggregate when possible: "count by category"

### 2. Data Safety

- Query before modifying: verify target records
- Use transactions: for related changes
- Backup before schema changes
- Test in development first

### 3. Performance

- Add indexes on frequently queried columns
- Filter early with WHERE clauses
- Avoid SELECT * patterns
- Use appropriate data types

### 4. Security

- Use read-only mode for analysis
- Minimum privilege accounts
- Never hardcode credentials
- Audit all modifications
- Review generated queries

---

## Troubleshooting

### Connection Failures

- Verify SERVER_NAME format
- Check network/firewall
- Confirm SQL Server is running
- Validate credentials
- Set TRUST_SERVER_CERTIFICATE if needed

### Query Errors

- Add WHERE clauses for filtering
- Reduce result set size
- Check syntax in generated SQL
- Verify column names exist

### Permission Denied

- Check account permissions
- Verify READONLY mode isn't blocking writes
- Confirm database user roles
- Review table-level permissions

### Timeout Issues

- Increase CONNECTION_TIMEOUT
- Optimize queries with indexes
- Reduce data volume with filters
- Check server performance

---

## T-SQL Quick Reference

### Common Functions

```sql
-- String functions
LEN(column), SUBSTRING(col, start, length), CONCAT(a, b)
UPPER(col), LOWER(col), TRIM(col), REPLACE(col, old, new)

-- Date functions
GETDATE(), GETUTCDATE(), DATEADD(day, 7, date)
DATEDIFF(day, start, end), YEAR(date), MONTH(date)
FORMAT(date, 'yyyy-MM-dd')

-- Aggregate functions
COUNT(*), SUM(col), AVG(col), MIN(col), MAX(col)
COUNT(DISTINCT col)

-- NULL handling
ISNULL(col, default), COALESCE(col1, col2, default)
NULLIF(a, b)
```

### Window Functions

```sql
-- Ranking
ROW_NUMBER() OVER (ORDER BY col)
RANK() OVER (PARTITION BY cat ORDER BY col)
DENSE_RANK() OVER (ORDER BY col DESC)

-- Aggregates
SUM(amount) OVER (ORDER BY date)
AVG(price) OVER (PARTITION BY category)
LAG(col, 1) OVER (ORDER BY date)
LEAD(col, 1) OVER (ORDER BY date)
```

### Common Table Expressions

```sql
WITH cte AS (
    SELECT column1, column2
    FROM table
    WHERE condition
)
SELECT * FROM cte;
```

---

## Additional Resources

- [SQL Server Documentation](https://learn.microsoft.com/sql/sql-server/)
- [T-SQL Reference](https://learn.microsoft.com/sql/t-sql/language-reference)
- [Azure SQL Database](https://learn.microsoft.com/azure/azure-sql/)
- [MssqlMcp GitHub](https://github.com/Azure-Samples/SQL-AI-samples/tree/main/MssqlMcp)
