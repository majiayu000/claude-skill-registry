---
name: query-builder
description: Interactive database query builder for generating optimized SQL and NoSQL queries.
---

# Query Builder Skill

Interactive database query builder for generating optimized SQL and NoSQL queries.

## Instructions

You are a database query expert. When invoked:

1. **Understand Requirements**:
   - Analyze the requested data operations
   - Identify tables/collections and relationships
   - Determine filters, joins, and aggregations needed
   - Consider performance implications

2. **Detect Database Type**:
   - PostgreSQL, MySQL, SQLite (SQL databases)
   - MongoDB, DynamoDB (NoSQL databases)
   - Check for ORM usage (Prisma, TypeORM, SQLAlchemy, Mongoose)

3. **Generate Queries**:
   - Write optimized, readable queries
   - Use appropriate indexes and query patterns
   - Include parameterized queries to prevent SQL injection
   - Provide both raw SQL and ORM versions when applicable

4. **Explain Query**:
   - Break down query execution flow
   - Highlight performance considerations
   - Suggest indexes if needed
   - Provide alternative approaches when relevant

## Supported Databases

- **SQL**: PostgreSQL, MySQL, MariaDB, SQLite, SQL Server
- **NoSQL**: MongoDB, DynamoDB, Redis, Cassandra
- **ORMs**: Prisma, TypeORM, Sequelize, SQLAlchemy, Django ORM, Mongoose

## Usage Examples

```
@query-builder Get all users with their orders
@query-builder Find top 10 products by revenue
@query-builder --optimize SELECT * FROM users WHERE email LIKE '%@gmail.com'
@query-builder --explain-plan
```

## SQL Query Patterns

### Basic SELECT with Filters
```sql
-- PostgreSQL/MySQL
SELECT
  id,
  username,
  email,
  created_at
FROM users
WHERE
  active = true
  AND created_at >= NOW() - INTERVAL '30 days'
ORDER BY created_at DESC
LIMIT 100;

-- With parameters (prevent SQL injection)
SELECT * FROM users
WHERE email = $1 AND active = $2;
```

### JOIN Operations
```sql
-- INNER JOIN - Get users with their orders
SELECT
  u.id,
  u.username,
  u.email,
  o.id as order_id,
  o.total_amount,
  o.created_at as order_date
FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE o.status = 'completed'
ORDER BY o.created_at DESC;

-- LEFT JOIN - Include users without orders
SELECT
  u.id,
  u.username,
  COUNT(o.id) as order_count,
  COALESCE(SUM(o.total_amount), 0) as total_spent
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.username
HAVING COUNT(o.id) > 0
ORDER BY total_spent DESC;

-- Multiple JOINs
SELECT
  o.id as order_id,
  u.username,
  p.name as product_name,
  oi.quantity,
  oi.price
FROM orders o
INNER JOIN users u ON o.user_id = u.id
INNER JOIN order_items oi ON o.id = oi.order_id
INNER JOIN products p ON oi.product_id = p.id
WHERE o.created_at >= '2024-01-01';
```

### Aggregations
```sql
-- Group by with aggregations
SELECT
  DATE_TRUNC('day', created_at) as date,
  COUNT(*) as order_count,
  SUM(total_amount) as daily_revenue,
  AVG(total_amount) as avg_order_value,
  MAX(total_amount) as largest_order
FROM orders
WHERE created_at >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY DATE_TRUNC('day', created_at)
ORDER BY date DESC;

-- Window functions
SELECT
  id,
  user_id,
  total_amount,
  created_at,
  ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at DESC) as order_rank,
  AVG(total_amount) OVER (PARTITION BY user_id) as user_avg_order
FROM orders;
```

### Subqueries
```sql
-- Subquery in WHERE clause
SELECT * FROM users
WHERE id IN (
  SELECT DISTINCT user_id
  FROM orders
  WHERE total_amount > 1000
);

-- Subquery in SELECT (scalar subquery)
SELECT
  id,
  username,
  (SELECT COUNT(*) FROM orders WHERE user_id = users.id) as order_count,
  (SELECT MAX(total_amount) FROM orders WHERE user_id = users.id) as max_order
FROM users;

-- Common Table Expression (CTE)
WITH recent_orders AS (
  SELECT
    user_id,
    COUNT(*) as order_count,
    SUM(total_amount) as total_spent
  FROM orders
  WHERE created_at >= CURRENT_DATE - INTERVAL '30 days'
  GROUP BY user_id
)
SELECT
  u.id,
  u.username,
  u.email,
  COALESCE(ro.order_count, 0) as recent_orders,
  COALESCE(ro.total_spent, 0) as recent_spending
FROM users u
LEFT JOIN recent_orders ro ON u.id = ro.user_id
WHERE u.active = true;
```

### Complex Queries
```sql
-- Recursive CTE for hierarchical data
WITH RECURSIVE category_tree AS (
  -- Base case: root categories
  SELECT id, name, parent_id, 0 as level
  FROM categories
  WHERE parent_id IS NULL

  UNION ALL

  -- Recursive case: child categories
  SELECT c.id, c.name, c.parent_id, ct.level + 1
  FROM categories c
  INNER JOIN category_tree ct ON c.parent_id = ct.id
)
SELECT * FROM category_tree
ORDER BY level, name;

-- Find top N per group
WITH ranked_products AS (
  SELECT
    p.*,
    c.name as category_name,
    ROW_NUMBER() OVER (PARTITION BY p.category_id ORDER BY p.sales DESC) as rank
  FROM products p
  INNER JOIN categories c ON p.category_id = c.id
)
SELECT * FROM ranked_products
WHERE rank <= 3;
```

### UPSERT (INSERT or UPDATE)
```sql
-- PostgreSQL - ON CONFLICT
INSERT INTO users (id, username, email, updated_at)
VALUES ($1, $2, $3, NOW())
ON CONFLICT (id)
DO UPDATE SET
  username = EXCLUDED.username,
  email = EXCLUDED.email,
  updated_at = NOW();

-- MySQL - ON DUPLICATE KEY UPDATE
INSERT INTO users (id, username, email, updated_at)
VALUES (?, ?, ?, NOW())
ON DUPLICATE KEY UPDATE
  username = VALUES(username),
  email = VALUES(email),
  updated_at = NOW();
```

## ORM Query Examples

### Prisma (TypeScript)
```typescript
// Basic query
const users = await prisma.user.findMany({
  where: {
    active: true,
    createdAt: {
      gte: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000)
    }
  },
  orderBy: { createdAt: 'desc' },
  take: 100
});

// Relations
const userWithOrders = await prisma.user.findUnique({
  where: { id: userId },
  include: {
    orders: {
      where: { status: 'completed' },
      include: {
        items: {
          include: { product: true }
        }
      }
    }
  }
});

// Aggregations
const stats = await prisma.order.groupBy({
  by: ['userId'],
  where: {
    createdAt: {
      gte: new Date('2024-01-01')
    }
  },
  _count: { id: true },
  _sum: { totalAmount: true },
  _avg: { totalAmount: true }
});

// Raw SQL when needed
const result = await prisma.$queryRaw`
  SELECT * FROM users
  WHERE email = ${email}
  AND active = true
`;
```

### TypeORM (TypeScript)
```typescript
// Query builder
const users = await dataSource
  .getRepository(User)
  .createQueryBuilder('user')
  .where('user.active = :active', { active: true })
  .andWhere('user.createdAt >= :date', {
    date: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000)
  })
  .orderBy('user.createdAt', 'DESC')
  .take(100)
  .getMany();

// Relations
const userWithOrders = await dataSource
  .getRepository(User)
  .createQueryBuilder('user')
  .leftJoinAndSelect('user.orders', 'order')
  .leftJoinAndSelect('order.items', 'item')
  .leftJoinAndSelect('item.product', 'product')
  .where('user.id = :id', { id: userId })
  .andWhere('order.status = :status', { status: 'completed' })
  .getOne();

// Aggregations
const stats = await dataSource
  .getRepository(Order)
  .createQueryBuilder('order')
  .select('order.userId', 'userId')
  .addSelect('COUNT(order.id)', 'orderCount')
  .addSelect('SUM(order.totalAmount)', 'totalSpent')
  .addSelect('AVG(order.totalAmount)', 'avgOrder')
  .where('order.createdAt >= :date', { date: new Date('2024-01-01') })
  .groupBy('order.userId')
  .getRawMany();
```

### SQLAlchemy (Python)
```python
from sqlalchemy import select, func, and_, or_
from datetime import datetime, timedelta

# Basic query
stmt = (
    select(User)
    .where(
        and_(
            User.active == True,
            User.created_at >= datetime.now() - timedelta(days=30)
        )
    )
    .order_by(User.created_at.desc())
    .limit(100)
)
users = session.execute(stmt).scalars().all()

# Joins
stmt = (
    select(User, Order)
    .join(Order, User.id == Order.user_id)
    .where(Order.status == 'completed')
    .order_by(Order.created_at.desc())
)
results = session.execute(stmt).all()

# Aggregations
stmt = (
    select(
        func.date_trunc('day', Order.created_at).label('date'),
        func.count(Order.id).label('order_count'),
        func.sum(Order.total_amount).label('revenue'),
        func.avg(Order.total_amount).label('avg_order')
    )
    .where(Order.created_at >= datetime.now() - timedelta(days=7))
    .group_by(func.date_trunc('day', Order.created_at))
    .order_by('date desc')
)
stats = session.execute(stmt).all()

# Raw SQL when needed
result = session.execute(
    text("SELECT * FROM users WHERE email = :email"),
    {"email": email}
).fetchall()
```

## NoSQL Query Examples

### MongoDB
```javascript
// Basic query
db.users.find({
  active: true,
  createdAt: { $gte: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000) }
})
.sort({ createdAt: -1 })
.limit(100);

// Aggregation pipeline
db.orders.aggregate([
  {
    $match: {
      status: 'completed',
      createdAt: { $gte: new Date('2024-01-01') }
    }
  },
  {
    $group: {
      _id: '$userId',
      orderCount: { $sum: 1 },
      totalSpent: { $sum: '$totalAmount' },
      avgOrder: { $avg: '$totalAmount' }
    }
  },
  {
    $sort: { totalSpent: -1 }
  },
  {
    $limit: 10
  }
]);

// Lookup (join)
db.users.aggregate([
  {
    $lookup: {
      from: 'orders',
      localField: '_id',
      foreignField: 'userId',
      as: 'orders'
    }
  },
  {
    $match: { 'orders.0': { $exists: true } }
  },
  {
    $project: {
      username: 1,
      email: 1,
      orderCount: { $size: '$orders' }
    }
  }
]);
```

### Mongoose (Node.js)
```javascript
// Basic query
const users = await User.find({
  active: true,
  createdAt: { $gte: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000) }
})
.sort({ createdAt: -1 })
.limit(100);

// Population (join)
const user = await User.findById(userId)
  .populate({
    path: 'orders',
    match: { status: 'completed' },
    populate: {
      path: 'items.product'
    }
  });

// Aggregation
const stats = await Order.aggregate([
  {
    $match: {
      createdAt: { $gte: new Date('2024-01-01') }
    }
  },
  {
    $group: {
      _id: {
        $dateToString: { format: '%Y-%m-%d', date: '$createdAt' }
      },
      orderCount: { $sum: 1 },
      revenue: { $sum: '$totalAmount' },
      avgOrder: { $avg: '$totalAmount' }
    }
  },
  { $sort: { _id: -1 } }
]);
```

## Performance Optimization

### Use Indexes
```sql
-- Create indexes for frequently queried columns
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_created_at ON orders(created_at);

-- Composite index for multiple columns
CREATE INDEX idx_orders_user_status ON orders(user_id, status);

-- Partial index (PostgreSQL)
CREATE INDEX idx_active_users ON users(email) WHERE active = true;

-- Index for full-text search (PostgreSQL)
CREATE INDEX idx_products_search ON products
USING GIN(to_tsvector('english', name || ' ' || description));
```

### Query Optimization Tips
```sql
-- ❌ Bad - SELECT *
SELECT * FROM users WHERE id = 1;

-- ✓ Good - Select only needed columns
SELECT id, username, email FROM users WHERE id = 1;

-- ❌ Bad - Function on indexed column
SELECT * FROM users WHERE LOWER(email) = 'user@example.com';

-- ✓ Good - Store lowercase email or use functional index
SELECT * FROM users WHERE email = 'user@example.com';

-- ❌ Bad - OR conditions can't use index efficiently
SELECT * FROM orders WHERE user_id = 1 OR customer_email = 'user@example.com';

-- ✓ Good - Use UNION when appropriate
SELECT * FROM orders WHERE user_id = 1
UNION
SELECT * FROM orders WHERE customer_email = 'user@example.com';

-- ❌ Bad - NOT IN with subquery
SELECT * FROM users WHERE id NOT IN (SELECT user_id FROM banned_users);

-- ✓ Good - LEFT JOIN with NULL check
SELECT u.* FROM users u
LEFT JOIN banned_users bu ON u.id = bu.user_id
WHERE bu.user_id IS NULL;
```

### Pagination
```sql
-- ❌ Bad - OFFSET gets slower with large offsets
SELECT * FROM users
ORDER BY created_at DESC
LIMIT 20 OFFSET 10000;

-- ✓ Good - Cursor-based pagination
SELECT * FROM users
WHERE created_at < '2024-01-01 12:00:00'
ORDER BY created_at DESC
LIMIT 20;

-- ✓ Better - Keyset pagination
SELECT * FROM users
WHERE (created_at, id) < ('2024-01-01 12:00:00', 12345)
ORDER BY created_at DESC, id DESC
LIMIT 20;
```

## Common Patterns

### Soft Deletes
```sql
-- Add deleted_at column
ALTER TABLE users ADD COLUMN deleted_at TIMESTAMP NULL;

-- "Delete" by setting timestamp
UPDATE users SET deleted_at = NOW() WHERE id = 1;

-- Query active records
SELECT * FROM users WHERE deleted_at IS NULL;

-- Create index for better performance
CREATE INDEX idx_users_deleted_at ON users(deleted_at)
WHERE deleted_at IS NULL;
```

### Audit Trail
```sql
-- Audit table
CREATE TABLE audit_log (
  id SERIAL PRIMARY KEY,
  table_name VARCHAR(50),
  record_id INTEGER,
  action VARCHAR(10),
  old_values JSONB,
  new_values JSONB,
  changed_by INTEGER,
  changed_at TIMESTAMP DEFAULT NOW()
);

-- Trigger for automatic audit
CREATE OR REPLACE FUNCTION audit_trigger()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO audit_log (table_name, record_id, action, old_values, new_values, changed_by)
  VALUES (
    TG_TABLE_NAME,
    NEW.id,
    TG_OP,
    row_to_json(OLD),
    row_to_json(NEW),
    current_user_id()
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

### Running Totals
```sql
-- Window function approach
SELECT
  date,
  daily_revenue,
  SUM(daily_revenue) OVER (ORDER BY date) as running_total
FROM daily_stats
ORDER BY date;
```

## Anti-Patterns to Avoid

### N+1 Query Problem
```javascript
// ❌ Bad - N+1 queries
const users = await User.findAll();
for (const user of users) {
  const orders = await Order.findAll({ where: { userId: user.id } });
  // Process orders...
}

// ✓ Good - Single query with join
const users = await User.findAll({
  include: [{ model: Order }]
});
```

### Missing Indexes
```sql
-- ❌ Bad - No index on foreign key
SELECT * FROM orders WHERE user_id = 123; -- Slow!

-- ✓ Good - Index on foreign key
CREATE INDEX idx_orders_user_id ON orders(user_id);
```

### Retrieving Too Much Data
```sql
-- ❌ Bad - Fetching all rows
SELECT * FROM orders; -- Could be millions of rows!

-- ✓ Good - Use pagination
SELECT * FROM orders
ORDER BY created_at DESC
LIMIT 100;
```

## Best Practices

1. **Always use parameterized queries** to prevent SQL injection
2. **Index foreign keys** and frequently queried columns
3. **Use EXPLAIN ANALYZE** to understand query performance
4. **Avoid SELECT *** - only fetch needed columns
5. **Use transactions** for data consistency
6. **Implement pagination** for large datasets
7. **Cache frequently accessed data** (Redis, Memcached)
8. **Monitor slow queries** and optimize them
9. **Use connection pooling** to manage database connections
10. **Regular VACUUM and ANALYZE** on PostgreSQL

## Notes

- Test queries with realistic data volumes
- Monitor query execution time in production
- Use read replicas for read-heavy workloads
- Consider database-specific features (PostgreSQL extensions, MySQL storage engines)
- Document complex queries with comments
- Keep ORMs updated but know raw SQL for complex operations
