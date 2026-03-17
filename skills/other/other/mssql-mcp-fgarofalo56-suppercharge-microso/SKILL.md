---
name: mssql-mcp
description: Expert guidance for SQL Server database operations using natural language via the MssqlMcp server. Execute queries, manage schemas, perform CRUD operations, and inspect database structures through conversational interface. Use when working with SQL Server, T-SQL, database queries, data manipulation, or schema management.
---

# SQL Server Database Expert (MssqlMcp)

Expert guidance for SQL Server database operations using the MssqlMcp server. Interact with MSSQL databases through natural language - query data, modify records, manage schemas, and inspect structures without writing SQL directly.

## Core Capabilities

1. **Query Execution** - Run SQL queries via natural language
2. **Data Modification** - Create, update, and delete records
3. **Schema Management** - Create and modify tables, indexes, constraints
4. **Database Inspection** - List tables, view schemas, explore structure
5. **Secure Operations** - Built-in safety constraints (WHERE clause requirements)

## Natural Language Interface

The MssqlMcp server translates conversational requests into SQL operations.

### Query Examples

**Information Retrieval:**
```
"Show me all users from New York"
"Get the top 10 orders by total amount"
"Find all products where price is greater than $100"
"List customers who signed up in the last 30 days"
```

**Aggregations:**
```
"What's the total revenue by month for 2024?"
"Count how many orders are in 'pending' status"
"Calculate average order value by customer segment"
"Show me the distribution of users by state"
```

**Schema Inspection:**
```
"List all tables in the database"
"Show me the structure of the users table"
"What indexes exist on the orders table?"
"Display all foreign key relationships"
```

### Data Modification Examples

**Insert Records:**
```
"Add a new user with name John Doe, email john@example.com"
"Create a product named 'Laptop' with price $999"
"Insert an order for customer ID 123 with items A, B, C"
```

**Update Records:**
```
"Update all pending orders to completed status" (with WHERE clause)
"Change the price of product ID 456 to $1299"
"Set the email for user ID 789 to newemail@example.com"
```

**Delete Records:**
```
"Delete all orders older than 2 years" (with WHERE clause)
"Remove the user with ID 999"
"Clear all temporary records from the staging table"
```

### Schema Management Examples

**Create Tables:**
```
"Create a new table called products with columns for id, name, and price"
"Add a customers table with id, name, email, and created_date fields"
"Create an orders table with foreign keys to customers and products"
```

**Modify Schema:**
```
"Add a 'phone' column to the customers table"
"Create an index on the email column in users"
"Add a foreign key constraint from orders to customers"
"Drop the unused 'temp_data' table"
```

---

## Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| SERVER_NAME | Yes | SQL Server address (e.g., "localhost" or "myserver.database.windows.net") |
| DATABASE_NAME | Yes | Target database name |
| READONLY | No | Set to "true" for read-only access (default: false) |
| CONNECTION_TIMEOUT | No | Connection timeout in seconds |
| TRUST_SERVER_CERTIFICATE | No | Accept self-signed certificates (set to "true" if needed) |

### Authentication

Uses SQL Server authentication or Windows authentication depending on configuration:

**SQL Authentication:**
```
SERVER_NAME=myserver.database.windows.net
DATABASE_NAME=ProductionDB
USER=dbuser
PASSWORD=securepassword
```

**Windows/Azure AD Authentication:**
```
SERVER_NAME=myserver.database.windows.net
DATABASE_NAME=ProductionDB
(Uses integrated authentication)
```

---

## Security Features

### Mandatory WHERE Clauses

**Read Operations:**
- All SELECT queries must include WHERE clauses
- Prevents accidental full table scans
- Protects against unintended data exposure

**Update Operations:**
- UPDATE statements require explicit WHERE clauses
- Prevents accidental bulk updates
- Ensures targeted modifications

**Delete Operations:**
- DELETE statements require WHERE clauses
- Prevents accidental data loss
- Ensures intentional deletions

### Read-Only Mode

Set `READONLY=true` to:
- Disable INSERT, UPDATE, DELETE operations
- Allow only SELECT queries and schema inspection
- Provide safe exploration environment
- Protect production data from modifications

---

## Common Workflows

### Data Analysis Workflow

```
1. "List all tables in the database"
   - Discover available data

2. "Show me the structure of the sales table"
   - Understand schema

3. "Get the top 10 sales by amount for 2024"
   - Query specific data

4. "What's the total revenue by quarter?"
   - Aggregate analysis
```

### Application Development Workflow

```
1. "Create a users table with id, name, email, created_at"
   - Set up schema

2. "Add an index on the email column"
   - Optimize queries

3. "Insert a test user with name Test User"
   - Add test data

4. "Show me all users created today"
   - Verify data
```

### Data Maintenance Workflow

```
1. "Count records in the temp_logs table older than 30 days"
   - Check data volume

2. "Delete records from temp_logs older than 30 days"
   - Clean up data

3. "Update all NULL email addresses to 'unknown@example.com' in users"
   - Data quality improvements
```

### Reporting Workflow

```
1. "Calculate total orders by month for the last year"
   - Time-series analysis

2. "Show customer segments by total spend"
   - Customer analysis

3. "List top 20 products by revenue"
   - Product performance
```

---

## Best Practices

### Querying Data

1. **Be Specific** - Include clear filtering criteria
2. **Limit Results** - Request "top N" for large datasets
3. **Use Aggregations** - Count, sum, average rather than full scans
4. **Include Time Ranges** - Filter by date when working with time-series data

**Good Examples:**
```
"Show me the last 50 orders"
"Get users who signed up this month"
"Count products by category"
```

**Avoid:**
```
"Show me all records" (too broad)
"Get everything" (unspecific)
```

### Modifying Data

1. **Always Include Conditions** - Specify exactly which records to modify
2. **Verify First** - Query before updating/deleting
3. **Use Transactions** - For related changes
4. **Test in Dev** - Never test destructive operations in production first

**Safe Pattern:**
```
1. "Show me orders with status 'pending' older than 7 days"
   (Review what will be affected)

2. "Update orders to 'expired' status where status is 'pending' and created more than 7 days ago"
   (Execute with confidence)
```

### Schema Management

1. **Plan Changes** - Think through impacts before creating/modifying
2. **Backup First** - Always backup before schema changes
3. **Check Dependencies** - Understand relationships before dropping tables
4. **Add Indexes Strategically** - Index frequently queried columns

### Security

1. **Use Read-Only Mode** - For exploratory analysis
2. **Limit Permissions** - Use accounts with minimal required permissions
3. **Never Share Credentials** - Use environment variables
4. **Audit Changes** - Log all data modifications
5. **Review Queries** - Understand what's being executed

---

## Troubleshooting

### Connection Issues

**Problem:** Cannot connect to server

**Solutions:**
- Verify SERVER_NAME is correct
- Check network connectivity
- Ensure SQL Server is running
- Verify firewall rules allow connection
- Check authentication credentials
- Set TRUST_SERVER_CERTIFICATE=true for self-signed certs

### Query Errors

**Problem:** "WHERE clause required" error

**Solution:** All read/update/delete operations need filtering conditions. Be specific about which records to target.

**Problem:** Timeout errors

**Solutions:**
- Reduce result set size (use TOP N)
- Add WHERE clauses to filter data
- Increase CONNECTION_TIMEOUT value
- Optimize query performance with indexes

### Permission Errors

**Problem:** "Permission denied" on operations

**Solutions:**
- Verify account has required permissions
- Check if READONLY mode is enabled (disables modifications)
- Ensure database user has appropriate roles
- Review database-level and table-level permissions

---

## Examples by Scenario

### E-Commerce Database

**Customer Analysis:**
```
"Show me customers who haven't ordered in 90 days"
"Calculate average order value by customer segment"
"Find customers with more than 5 orders"
```

**Inventory Management:**
```
"List products with stock below 10 units"
"Show me products that haven't sold in 6 months"
"Calculate inventory turnover rate by category"
```

**Sales Reporting:**
```
"Total revenue by day for the last 30 days"
"Top 10 products by revenue this quarter"
"Customer lifetime value calculation"
```

### User Management System

**User Queries:**
```
"Count active users by subscription tier"
"Find users who haven't logged in for 30 days"
"List recently registered users"
```

**User Updates:**
```
"Deactivate users who haven't verified email after 7 days"
"Update subscription expiry dates for annual users"
"Reset failed login attempts for user ID 123"
```

### Analytics Database

**Aggregations:**
```
"Calculate daily active users for the last week"
"Show page view trends by hour of day"
"Conversion rate by traffic source"
```

**Performance Queries:**
```
"Average response time by API endpoint"
"Error rate by service over time"
"Database query performance metrics"
```

---

## When to Use This Skill

- Querying SQL Server databases conversationally
- Exploring database schemas and structures
- Performing data analysis without writing SQL
- Managing database records (CRUD operations)
- Creating and modifying table structures
- Generating reports from SQL Server data
- Database maintenance and cleanup tasks
- Learning SQL Server concepts through natural language

## Keywords

sql server, mssql, t-sql, database, queries, crud operations, schema management, natural language sql, database interaction, data analysis, sql queries, table management, database inspection, data modification, sql automation
