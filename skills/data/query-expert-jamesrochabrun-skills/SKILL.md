---
name: query-expert
description: Master SQL and database queries across multiple systems. Generate optimized queries, analyze performance, design indexes, and troubleshoot slow queries for PostgreSQL, MySQL, MongoDB, and more.
---

# Query Expert

Master database queries across SQL and NoSQL systems. Generate optimized queries, analyze performance with EXPLAIN plans, design effective indexes, and troubleshoot slow queries.

## What This Skill Does

Helps you write efficient, performant database queries:
- **Generate Queries** - SQL, MongoDB, GraphQL queries
- **Optimize Queries** - Performance tuning and refactoring
- **Design Indexes** - Index strategies for faster queries
- **Analyze Performance** - EXPLAIN plans and query analysis
- **Troubleshoot** - Debug slow queries and bottlenecks
- **Best Practices** - Query patterns and anti-patterns

## Supported Databases

### SQL Databases
- **PostgreSQL** - Advanced features, CTEs, window functions
- **MySQL/MariaDB** - InnoDB optimization, replication
- **SQLite** - Embedded database optimization
- **SQL Server** - T-SQL, execution plans, DMVs
- **Oracle** - PL/SQL, partitioning, hints

### NoSQL Databases
- **MongoDB** - Aggregation pipelines, indexes
- **Redis** - Key-value queries, Lua scripts
- **Elasticsearch** - Full-text search queries
- **Cassandra** - CQL, partition keys

### Query Languages
- **SQL** - Standard and vendor-specific
- **MongoDB Query Language** - Find, aggregation
- **GraphQL** - Efficient data fetching
- **Cypher** - Neo4j graph queries

## SQL Query Patterns

### SELECT Queries

#### Basic SELECT

```sql
-- ✅ Select only needed columns
SELECT
    user_id,
    email,
    created_at
FROM users
WHERE status = 'active'
    AND created_at > NOW() - INTERVAL '30 days'
ORDER BY created_at DESC
LIMIT 100;

-- ❌ Avoid SELECT *
SELECT * FROM users;  -- Wastes resources
```

#### JOINs

```sql
-- INNER JOIN (most common)
SELECT
    o.order_id,
    o.total,
    c.name AS customer_name,
    c.email
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
WHERE o.created_at >= '2024-01-01';

-- LEFT JOIN (include all left rows)
SELECT
    c.customer_id,
    c.name,
    COUNT(o.order_id) AS order_count,
    COALESCE(SUM(o.total), 0) AS total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name;

-- Multiple JOINs
SELECT
    o.order_id,
    c.name AS customer_name,
    p.product_name,
    oi.quantity,
    oi.price
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
INNER JOIN products p ON oi.product_id = p.product_id
WHERE o.status = 'completed';
```

#### Subqueries

```sql
-- Subquery in WHERE
SELECT name, email
FROM customers
WHERE customer_id IN (
    SELECT DISTINCT customer_id
    FROM orders
    WHERE total > 1000
);

-- Correlated subquery
SELECT
    c.name,
    (SELECT COUNT(*)
     FROM orders o
     WHERE o.customer_id = c.customer_id) AS order_count
FROM customers c;

-- ✅ Better: Use JOIN instead
SELECT
    c.name,
    COUNT(o.order_id) AS order_count
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name;
```

### Aggregation

```sql
-- GROUP BY with aggregates
SELECT
    category,
    COUNT(*) AS product_count,
    AVG(price) AS avg_price,
    MIN(price) AS min_price,
    MAX(price) AS max_price,
    SUM(stock_quantity) AS total_stock
FROM products
GROUP BY category
HAVING COUNT(*) > 5
ORDER BY avg_price DESC;

-- Multiple GROUP BY columns
SELECT
    DATE_TRUNC('month', created_at) AS month,
    category,
    SUM(total) AS monthly_sales
FROM orders
GROUP BY DATE_TRUNC('month', created_at), category
ORDER BY month DESC, monthly_sales DESC;

-- ROLLUP for subtotals
SELECT
    COALESCE(category, 'TOTAL') AS category,
    COALESCE(brand, 'All Brands') AS brand,
    SUM(sales) AS total_sales
FROM products
GROUP BY ROLLUP(category, brand);
```

### Window Functions (PostgreSQL, SQL Server, MySQL 8+)

```sql
-- ROW_NUMBER
SELECT
    customer_id,
    order_date,
    total,
    ROW_NUMBER() OVER (
        PARTITION BY customer_id
        ORDER BY order_date DESC
    ) AS order_rank
FROM orders;

-- Running totals
SELECT
    order_date,
    total,
    SUM(total) OVER (
        ORDER BY order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total
FROM orders;

-- RANK vs DENSE_RANK
SELECT
    product_name,
    sales,
    RANK() OVER (ORDER BY sales DESC) AS rank,
    DENSE_RANK() OVER (ORDER BY sales DESC) AS dense_rank,
    NTILE(4) OVER (ORDER BY sales DESC) AS quartile
FROM products;

-- LAG and LEAD
SELECT
    order_date,
    total,
    LAG(total, 1) OVER (ORDER BY order_date) AS prev_total,
    LEAD(total, 1) OVER (ORDER BY order_date) AS next_total,
    total - LAG(total, 1) OVER (ORDER BY order_date) AS change
FROM orders;
```

### CTEs (Common Table Expressions)

```sql
-- Simple CTE
WITH active_customers AS (
    SELECT customer_id, name, email
    FROM customers
    WHERE status = 'active'
)
SELECT
    ac.name,
    COUNT(o.order_id) AS order_count
FROM active_customers ac
LEFT JOIN orders o ON ac.customer_id = o.customer_id
GROUP BY ac.customer_id, ac.name;

-- Multiple CTEs
WITH
monthly_sales AS (
    SELECT
        DATE_TRUNC('month', order_date) AS month,
        SUM(total) AS sales
    FROM orders
    GROUP BY DATE_TRUNC('month', order_date)
),
avg_monthly AS (
    SELECT AVG(sales) AS avg_sales
    FROM monthly_sales
)
SELECT
    ms.month,
    ms.sales,
    am.avg_sales,
    ms.sales - am.avg_sales AS variance
FROM monthly_sales ms
CROSS JOIN avg_monthly am
ORDER BY ms.month;

-- Recursive CTE (hierarchies)
WITH RECURSIVE org_tree AS (
    -- Base case
    SELECT
        employee_id,
        name,
        manager_id,
        1 AS level,
        ARRAY[employee_id] AS path
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- Recursive case
    SELECT
        e.employee_id,
        e.name,
        e.manager_id,
        ot.level + 1,
        ot.path || e.employee_id
    FROM employees e
    INNER JOIN org_tree ot ON e.manager_id = ot.employee_id
)
SELECT * FROM org_tree ORDER BY path;
```

## Query Optimization

### 1. Use Indexes Effectively

```sql
-- Create index on frequently queried columns
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);

-- Composite index (order matters!)
CREATE INDEX idx_orders_composite
ON orders(status, customer_id, order_date);

-- ✅ This query uses the index
SELECT * FROM orders
WHERE status = 'pending'
    AND customer_id = 123
    AND order_date > '2024-01-01';

-- ❌ This doesn't use the index (skips first column)
SELECT * FROM orders
WHERE customer_id = 123;

-- Partial/Filtered index (smaller, faster)
CREATE INDEX idx_active_users
ON users(email)
WHERE status = 'active';

-- Covering index (includes all needed columns)
CREATE INDEX idx_users_covering
ON users(email)
INCLUDE (name, created_at);
```

### 2. Avoid SELECT *

```sql
-- ❌ Bad: Retrieves all columns
SELECT * FROM users;

-- ✅ Good: Select only needed columns
SELECT user_id, email, name FROM users;

-- ✅ Good: More efficient for joins
SELECT
    u.user_id,
    u.email,
    o.order_id,
    o.total
FROM users u
INNER JOIN orders o ON u.user_id = o.user_id;
```

### 3. Optimize JOINs

```sql
-- ❌ Bad: Filtering after JOIN
SELECT u.name, o.total
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id
WHERE o.status = 'completed';

-- ✅ Good: Filter before JOIN
SELECT u.name, o.total
FROM users u
INNER JOIN (
    SELECT user_id, total
    FROM orders
    WHERE status = 'completed'
) o ON u.user_id = o.user_id;

-- ✅ Even better: Use WHERE with INNER JOIN
SELECT u.name, o.total
FROM users u
INNER JOIN orders o ON u.user_id = o.user_id
WHERE o.status = 'completed';
```

### 4. Use EXISTS Instead of IN

```sql
-- ❌ Slower: IN with subquery
SELECT name FROM customers
WHERE customer_id IN (
    SELECT customer_id FROM orders WHERE total > 1000
);

-- ✅ Faster: EXISTS
SELECT name FROM customers c
WHERE EXISTS (
    SELECT 1 FROM orders o
    WHERE o.customer_id = c.customer_id
        AND o.total > 1000
);
```

### 5. Avoid Functions on Indexed Columns

```sql
-- ❌ Bad: Function prevents index usage
SELECT * FROM users
WHERE LOWER(email) = 'john@example.com';

-- ✅ Good: Use functional index
CREATE INDEX idx_users_email_lower ON users(LOWER(email));

-- Or use case-insensitive collation
SELECT * FROM users
WHERE email = 'john@example.com' COLLATE utf8_general_ci;
```

### 6. Limit Result Sets

```sql
-- ✅ Use LIMIT/TOP for pagination
SELECT * FROM orders
ORDER BY created_at DESC
LIMIT 20 OFFSET 0;

-- ✅ Use WHERE to reduce rows early
SELECT * FROM orders
WHERE created_at > NOW() - INTERVAL '7 days'
ORDER BY created_at DESC;
```

### 7. Batch Operations

```sql
-- ❌ Bad: Multiple single inserts
INSERT INTO users (name, email) VALUES ('User1', 'user1@example.com');
INSERT INTO users (name, email) VALUES ('User2', 'user2@example.com');

-- ✅ Good: Batch insert
INSERT INTO users (name, email) VALUES
    ('User1', 'user1@example.com'),
    ('User2', 'user2@example.com'),
    ('User3', 'user3@example.com');

-- ✅ Good: Batch update
UPDATE products
SET price = price * 1.1
WHERE category IN ('Electronics', 'Computers');
```

## EXPLAIN Plans

### PostgreSQL

```sql
-- Simple EXPLAIN
EXPLAIN
SELECT * FROM orders WHERE customer_id = 123;

-- EXPLAIN ANALYZE (actually runs query)
EXPLAIN ANALYZE
SELECT
    c.name,
    COUNT(o.order_id) AS order_count
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name;

-- Look for:
-- - Seq Scan (bad, needs index)
-- - Index Scan (good)
-- - Bitmap Heap Scan (good for multiple rows)
-- - Hash Join vs Nested Loop
-- - High cost numbers
```

### MySQL

```sql
-- EXPLAIN
EXPLAIN
SELECT * FROM orders WHERE customer_id = 123;

-- EXPLAIN ANALYZE (MySQL 8.0.18+)
EXPLAIN ANALYZE
SELECT * FROM orders WHERE customer_id = 123;

-- Look for:
-- - type: ALL (table scan, bad)
-- - type: index (index scan, good)
-- - type: ref (index lookup, great)
-- - Extra: Using filesort (may need index)
-- - Extra: Using temporary (may need optimization)
```

## Indexing Strategies

### When to Index

**✅ Index these columns:**
- Primary keys (automatic)
- Foreign keys
- Columns in WHERE clauses
- Columns in JOIN conditions
- Columns in ORDER BY
- Columns in GROUP BY

**❌ Don't index:**
- Small tables (< 1000 rows)
- Columns with low cardinality (few distinct values)
- Frequently updated columns
- Large text/blob columns

### Index Types

```sql
-- B-Tree (default, most common)
CREATE INDEX idx_users_email ON users(email);

-- Hash index (equality only, PostgreSQL)
CREATE INDEX idx_users_email_hash ON users USING HASH(email);

-- GIN (full-text search, arrays, JSONB)
CREATE INDEX idx_posts_content_gin
ON posts USING GIN(to_tsvector('english', content));

-- GiST (geometric, full-text)
CREATE INDEX idx_locations_gist
ON locations USING GIST(coordinates);

-- Partial index (filtered)
CREATE INDEX idx_orders_pending
ON orders(customer_id)
WHERE status = 'pending';

-- Expression index
CREATE INDEX idx_users_email_domain
ON users((email ~~ '%@gmail.com%'));
```

### Composite Index Order

```sql
-- Index column order matters!
CREATE INDEX idx_orders_search
ON orders(status, customer_id, created_at);

-- ✅ Uses index (left-most column)
WHERE status = 'completed'

-- ✅ Uses index (left-most columns)
WHERE status = 'completed' AND customer_id = 123

-- ✅ Uses full index
WHERE status = 'completed'
    AND customer_id = 123
    AND created_at > '2024-01-01'

-- ❌ Doesn't use index (skips first column)
WHERE customer_id = 123

-- ❌ Doesn't use index (skips first column)
WHERE created_at > '2024-01-01'
```

## MongoDB Queries

### Find Queries

```javascript
// Basic find
db.users.find({ status: 'active' })

// Find with projection
db.users.find(
    { status: 'active' },
    { name: 1, email: 1, _id: 0 }
)

// Find with operators
db.orders.find({
    total: { $gt: 100, $lt: 1000 },
    status: { $in: ['pending', 'processing'] },
    'customer.city': 'New York'
})

// Find with sort and limit
db.products.find({ category: 'Electronics' })
    .sort({ price: -1 })
    .limit(10)

// Count
db.users.countDocuments({ status: 'active' })
```

### Aggregation Pipeline

```javascript
// Group and count
db.orders.aggregate([
    { $match: { status: 'completed' } },
    { $group: {
        _id: '$customer_id',
        total_orders: { $sum: 1 },
        total_spent: { $sum: '$total' },
        avg_order: { $avg: '$total' }
    }},
    { $sort: { total_spent: -1 } },
    { $limit: 10 }
])

// Lookup (JOIN)
db.orders.aggregate([
    { $lookup: {
        from: 'customers',
        localField: 'customer_id',
        foreignField: '_id',
        as: 'customer'
    }},
    { $unwind: '$customer' },
    { $project: {
        order_id: 1,
        total: 1,
        'customer.name': 1,
        'customer.email': 1
    }}
])

// Complex aggregation
db.sales.aggregate([
    // Filter
    { $match: {
        date: { $gte: ISODate('2024-01-01') }
    }},

    // Add computed fields
    { $addFields: {
        month: { $month: '$date' },
        year: { $year: '$date' }
    }},

    // Group by month
    { $group: {
        _id: { year: '$year', month: '$month' },
        total_sales: { $sum: '$amount' },
        order_count: { $sum: 1 },
        avg_sale: { $avg: '$amount' }
    }},

    // Sort
    { $sort: { '_id.year': 1, '_id.month': 1 } },

    // Reshape
    { $project: {
        _id: 0,
        date: {
            $concat: [
                { $toString: '$_id.year' },
                '-',
                { $toString: '$_id.month' }
            ]
        },
        total_sales: 1,
        order_count: 1,
        avg_sale: { $round: ['$avg_sale', 2] }
    }}
])
```

### MongoDB Indexes

```javascript
// Single field index
db.users.createIndex({ email: 1 })

// Compound index
db.orders.createIndex({ customer_id: 1, created_at: -1 })

// Unique index
db.users.createIndex({ email: 1 }, { unique: true })

// Partial index
db.orders.createIndex(
    { customer_id: 1 },
    { partialFilterExpression: { status: 'active' } }
)

// Text index
db.products.createIndex({ name: 'text', description: 'text' })

// TTL index (auto-delete after time)
db.sessions.createIndex(
    { created_at: 1 },
    { expireAfterSeconds: 3600 }
)

// List indexes
db.users.getIndexes()

// Analyze query performance
db.orders.find({ customer_id: 123 }).explain('executionStats')
```

## GraphQL Queries

```graphql
# Basic query
query {
  users {
    id
    name
    email
  }
}

# Query with arguments
query {
  user(id: "123") {
    name
    email
    orders {
      id
      total
      status
    }
  }
}

# Query with variables
query GetUser($userId: ID!) {
  user(id: $userId) {
    name
    email
    orders(limit: 10, status: COMPLETED) {
      id
      total
      createdAt
    }
  }
}

# Fragments (reusable fields)
fragment UserFields on User {
  id
  name
  email
  createdAt
}

query {
  user(id: "123") {
    ...UserFields
    orders {
      id
      total
    }
  }
}

# Avoid N+1 queries with DataLoader
query {
  orders {
    id
    total
    customer {  # Batched by DataLoader
      name
      email
    }
  }
}
```

## Common Anti-Patterns

### ❌ N+1 Query Problem

```sql
-- Bad: N+1 queries
SELECT * FROM customers;  -- 1 query
-- Then for each customer:
SELECT * FROM orders WHERE customer_id = ?;  -- N queries

-- Good: Single JOIN query
SELECT
    c.customer_id,
    c.name,
    o.order_id,
    o.total
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id;
```

### ❌ Using OR on Different Columns

```sql
-- Bad: Can't use indexes effectively
SELECT * FROM products
WHERE name = 'iPhone' OR category = 'Electronics';

-- Good: Use UNION
SELECT * FROM products WHERE name = 'iPhone'
UNION
SELECT * FROM products WHERE category = 'Electronics';
```

### ❌ Implicit Type Conversion

```sql
-- Bad: '123' is string, user_id is integer
SELECT * FROM users WHERE user_id = '123';

-- Good: Use correct type
SELECT * FROM users WHERE user_id = 123;
```

## Query Performance Checklist

- [ ] Select only needed columns (no SELECT *)
- [ ] Add indexes to WHERE/JOIN/ORDER BY columns
- [ ] Use EXPLAIN to analyze query plan
- [ ] Avoid functions on indexed columns
- [ ] Use EXISTS instead of IN for subqueries
- [ ] Batch INSERT/UPDATE operations
- [ ] Use appropriate JOIN types
- [ ] Filter early (WHERE before JOIN)
- [ ] Use LIMIT for large result sets
- [ ] Monitor slow query logs
- [ ] Update statistics regularly
- [ ] Avoid SELECT DISTINCT when possible
- [ ] Use covering indexes when appropriate

## Resources

- **PostgreSQL**: https://www.postgresql.org/docs/current/performance-tips.html
- **MySQL**: https://dev.mysql.com/doc/refman/8.0/en/optimization.html
- **MongoDB**: https://docs.mongodb.com/manual/core/query-optimization/
- **Use The Index, Luke**: https://use-the-index-luke.com/

---

**"Premature optimization is the root of all evil, but slow queries are the root of all frustration."**
