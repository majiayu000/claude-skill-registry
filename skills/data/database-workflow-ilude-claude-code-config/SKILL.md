---
name: database-workflow
description: Language-agnostic database best practices covering migrations, schema design, ORM patterns, query optimization, and testing strategies. Activate when working with database files, migrations, schema changes, SQL, ORM code, database tests, or when user mentions migrations, schema design, SQL optimization, NoSQL, database patterns, or connection pooling.
---

# Database Workflow

Language-agnostic guidelines for database design, migrations, schema management, ORM patterns, and query optimization.

## CRITICAL: No Premature Optimization

**Default to simplicity. Optimize only when you have measured evidence of a problem.**

- Don't add indexes "just in case"
- Don't over-normalize without understanding query patterns
- Don't implement complex caching without profiling first
- Measure before optimizing (EXPLAIN, query logs, monitoring)

## Migration Strategies

### Version Control for Schema Changes

**Treat migrations as code:**
- Store in version control alongside application code
- Timestamp or sequential numbering (001, 002, 003...)
- Atomic, single-responsibility changes
- Document WHY in migration files, not just WHAT

**Naming convention:**
```
migrations/
├── 001_create_users_table.sql
├── 002_add_email_index.sql
├── 003_create_orders_table.sql
└── 004_add_user_fk_to_orders.sql
```

### Up/Down Migrations

**Every migration must be reversible:**

```sql
-- UP: Create table
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- DOWN: Drop table
DROP TABLE users;
```

**Complex reversals require care:**
```sql
-- UP: Add constraint
ALTER TABLE orders ADD CONSTRAINT fk_user
    FOREIGN KEY (user_id) REFERENCES users(id);

-- DOWN: Remove constraint (PostgreSQL)
ALTER TABLE orders DROP CONSTRAINT fk_user;
```

### Idempotent Migrations

**Migrations must be safely re-runnable:**

```sql
-- ✅ Good: Idempotent (safe to run multiple times)
CREATE TABLE IF NOT EXISTS users (...);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- ❌ Bad: Fails if run twice
CREATE TABLE users (...);
CREATE INDEX idx_users_email ON users(email);
```

### Rollback Strategies

**Two approaches:**

1. **Down migrations (reversible):**
   - Run DOWN SQL to undo changes
   - Works if migration is reversible
   - Better for critical systems

2. **Snapshot migrations (not reversible):**
   - Never roll back; always migrate forward
   - Create new migration to fix issues
   - Simpler, safer in practice
   - Better for high-availability systems

**Best practice:** Design migrations to be reversible when possible, but plan for forward-only rollbacks in production.

### Migration Naming Conventions

**Use descriptive, action-oriented names:**

```
✅ Good:
- 001_create_users_table
- 002_add_email_unique_constraint
- 003_create_index_users_email
- 004_rename_column_user_id_to_author_id
- 005_add_soft_delete_columns

❌ Bad:
- 001_update
- 002_fix
- 003_schema_change
- 004_v2
```

**Include timestamp + sequence:**
```
2024_11_17_001_create_users_table.sql
2024_11_17_002_add_email_index.sql
```

## Schema Design Principles

### Normalization (1NF, 2NF, 3NF)

**First Normal Form (1NF):**
- Eliminate repeating groups
- All columns contain atomic (non-divisible) values
- Each row is unique

```sql
-- ❌ NOT 1NF: phone_numbers is a repeating group
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255),
    phone_numbers VARCHAR(255) -- "555-1234, 555-5678"
);

-- ✅ 1NF: Separate table for phone numbers
CREATE TABLE user_phones (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    phone_number VARCHAR(20)
);
```

**Second Normal Form (2NF):**
- Meets 1NF
- Remove partial dependencies (non-key columns depend on ALL of primary key)

```sql
-- ❌ NOT 2NF: course_name depends only on course_id, not on (student_id, course_id)
CREATE TABLE enrollments (
    student_id BIGINT,
    course_id BIGINT,
    course_name VARCHAR(255), -- Should be in courses table
    grade CHAR(1),
    PRIMARY KEY (student_id, course_id)
);

-- ✅ 2NF: Move course_name to separate table
CREATE TABLE courses (
    id BIGINT PRIMARY KEY,
    name VARCHAR(255)
);

CREATE TABLE enrollments (
    student_id BIGINT,
    course_id BIGINT REFERENCES courses(id),
    grade CHAR(1),
    PRIMARY KEY (student_id, course_id)
);
```

**Third Normal Form (3NF):**
- Meets 2NF
- Remove transitive dependencies (non-key columns don't depend on other non-key columns)

```sql
-- ❌ NOT 3NF: city and state depend on zip_code, not on user_id
CREATE TABLE users (
    id BIGINT PRIMARY KEY,
    name VARCHAR(255),
    zip_code VARCHAR(5),
    city VARCHAR(100),
    state CHAR(2)
);

-- ✅ 3NF: Move location info to separate table
CREATE TABLE zip_codes (
    code VARCHAR(5) PRIMARY KEY,
    city VARCHAR(100),
    state CHAR(2)
);

CREATE TABLE users (
    id BIGINT PRIMARY KEY,
    name VARCHAR(255),
    zip_code VARCHAR(5) REFERENCES zip_codes(code)
);
```

### Denormalization (When and Why)

**Denormalize when:**
- Query patterns are read-heavy (much more than writes)
- Measurement shows join performance is a bottleneck
- Reporting queries need fast access to aggregated data
- Cache invalidation is simpler than join performance

**Common denormalization patterns:**

1. **Stored aggregates:**
```sql
-- Track order count on user without JOIN
CREATE TABLE users (
    id BIGINT PRIMARY KEY,
    name VARCHAR(255),
    order_count INT DEFAULT 0
);

-- Keep in sync with trigger or application code
```

2. **Purposeful redundancy:**
```sql
-- Store user email on order to avoid JOIN at read time
CREATE TABLE orders (
    id BIGINT PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    user_email VARCHAR(255), -- Denormalized for reporting
    total_amount DECIMAL(10,2)
);
```

3. **Pre-computed views:**
```sql
-- Materialized view for dashboards
CREATE MATERIALIZED VIEW monthly_sales AS
SELECT
    DATE_TRUNC('month', created_at) as month,
    COUNT(*) as order_count,
    SUM(total_amount) as total_revenue
FROM orders
GROUP BY DATE_TRUNC('month', created_at);

-- Refresh periodically, not on every insert
REFRESH MATERIALIZED VIEW monthly_sales;
```

### Indexing Strategies

**Index only when needed. Measure first.**

```sql
-- ✅ Create index for frequently searched columns
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_created_at ON orders(created_at DESC);

-- ❌ Avoid: Index on every column
-- ❌ Avoid: Index on low-cardinality columns (boolean flags)
-- ❌ Avoid: Duplicate indexes
```

**Index types:**

1. **Single-column index (most common):**
```sql
CREATE INDEX idx_users_email ON users(email);
```

2. **Composite index (for multi-column WHERE/JOIN):**
```sql
-- Good for: WHERE user_id = X AND created_at > Y
CREATE INDEX idx_orders_user_created ON orders(user_id, created_at DESC);
```

3. **Partial index (index subset of rows):**
```sql
-- Index only active users (avoid indexing soft-deleted rows)
CREATE INDEX idx_active_users_email ON users(email)
    WHERE deleted_at IS NULL;
```

4. **Unique index (enforce constraint):**
```sql
CREATE UNIQUE INDEX idx_users_email ON users(email);
```

**Index maintenance:**
- Monitor for unused indexes (query database statistics)
- Drop unused indexes after measurement
- ANALYZE/VACUUM regularly to update statistics

### Primary Keys

**Use surrogate keys (auto-incrementing ID) by default:**

```sql
-- ✅ Recommended: Surrogate key
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255)
);

-- ✅ Good for high-volume tables
CREATE TABLE events (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    event_type VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Natural keys only if:**
- Column(s) are guaranteed immutable
- Never reassigned or repurposed
- Are short and stable

```sql
-- ✅ Natural key (country code is stable, never changes)
CREATE TABLE countries (
    code CHAR(2) PRIMARY KEY,
    name VARCHAR(255)
);

-- ❌ Natural key (email changes, should use surrogate)
CREATE TABLE users (
    email VARCHAR(255) PRIMARY KEY
);
```

### Foreign Keys and Constraints

**Always define foreign key relationships:**

```sql
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE orders (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id),
    total_amount DECIMAL(10,2) NOT NULL
);

-- With explicit constraint name for cleaner error messages
CREATE TABLE order_items (
    id BIGSERIAL PRIMARY KEY,
    order_id BIGINT NOT NULL,
    product_id BIGINT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    CONSTRAINT fk_order FOREIGN KEY (order_id) REFERENCES orders(id),
    CONSTRAINT fk_product FOREIGN KEY (product_id) REFERENCES products(id)
);
```

**Cascade behaviors:**

```sql
-- DELETE CASCADE: Delete orders when user is deleted (use with caution)
CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE

-- RESTRICT: Prevent user deletion if orders exist (safer default)
CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE RESTRICT

-- SET NULL: Set user_id to NULL if user deleted (for optional relationships)
CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
```

### Constraints

**Use constraints to enforce data integrity at database level:**

```sql
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    age INT CHECK (age >= 18),
    role VARCHAR(50) DEFAULT 'user' CHECK (role IN ('user', 'admin', 'moderator')),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id),
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    total_amount DECIMAL(10,2) NOT NULL CHECK (total_amount > 0),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    -- Composite constraint
    CONSTRAINT valid_status CHECK (status IN ('pending', 'confirmed', 'shipped', 'delivered', 'cancelled')),
    -- Unique constraint on composite columns
    CONSTRAINT unique_user_order_date UNIQUE (user_id, DATE(created_at))
);
```

## ORM Patterns

### Active Record vs Data Mapper

**Active Record:**
- Model contains both data and database logic
- Simple for small projects
- Model directly calls database
- Example: Rails, Django ORM

```python
# Active Record pattern
class User(Model):
    name = CharField()
    email = CharField()

    def save(self):
        # Object knows how to save itself
        db.insert('users', {...})

    @staticmethod
    def find_by_email(email):
        return db.query('SELECT * FROM users WHERE email = ?', email)

# Usage
user = User(name='John', email='john@example.com')
user.save()
found_user = User.find_by_email('john@example.com')
```

**Data Mapper:**
- Model contains only data; repository handles database logic
- Better separation of concerns
- Model is a plain object
- Example: SQLAlchemy, TypeORM

```python
# Data Mapper pattern
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

class UserRepository:
    def save(self, user):
        # Repository handles persistence
        db.insert('users', {'name': user.name, 'email': user.email})

    def find_by_email(self, email):
        row = db.query('SELECT * FROM users WHERE email = ?', email)
        return User(row['name'], row['email']) if row else None

# Usage
user = User('John', 'john@example.com')
repo = UserRepository()
repo.save(user)
found_user = repo.find_by_email('john@example.com')
```

**Choose based on project scale:**
- Small apps: Active Record (simpler)
- Medium to large: Data Mapper (more flexible)

### Query Builders

**Use query builders to avoid string concatenation and SQL injection:**

```python
# ❌ Vulnerable to SQL injection
query = f"SELECT * FROM users WHERE email = '{email}'"
result = db.execute(query)

# ✅ Safe: Parameterized query
result = db.query('SELECT * FROM users WHERE email = ?', [email])

# ✅ Better: Query builder
result = (
    db.select(User)
    .where(User.email == email)
    .where(User.active == True)
    .order_by(User.created_at.desc())
    .limit(10)
    .execute()
)
```

**Benefits of query builders:**
- Prevent SQL injection
- Cleaner, more maintainable code
- Database-agnostic (can switch databases)
- Compose queries dynamically

### Eager Loading vs Lazy Loading

**Lazy Loading (default, but can cause N+1):**
```python
# Each user fetch triggers a separate query for posts
users = db.query(User).limit(10).all()
for user in users:
    print(user.posts)  # Additional query per user = 10+ queries!
```

**Eager Loading (prevent N+1):**
```python
# Single query with JOIN
users = db.query(User).join(Post).limit(10).all()
for user in users:
    print(user.posts)  # No additional queries

# Or use explicit eager loading
users = db.query(User).options(joinedload(User.posts)).limit(10).all()
```

### N+1 Query Problem

**Recognize and fix N+1 problems:**

```python
# ❌ N+1 Problem: 1 query for users + N queries for posts
users = db.query(User).all()  # 1 query
for user in users:
    posts = db.query(Post).filter(Post.user_id == user.id).all()  # N more queries

# ✅ Fix 1: Eager loading with JOIN
users = db.query(User).join(Post).distinct().all()

# ✅ Fix 2: Use IN clause for batch loading
user_ids = [u.id for u in users]
posts = db.query(Post).filter(Post.user_id.in_(user_ids)).all()
# Now merge posts back to users in memory

# ✅ Fix 3: Use ORM eager loading
users = db.query(User).options(selectinload(User.posts)).all()
```

## Query Optimization

### Index Usage

**Write queries that use indexes:**

```sql
-- ✅ Uses index on email
SELECT * FROM users WHERE email = 'john@example.com';

-- ✅ Uses index on user_id, created_at
SELECT * FROM orders
WHERE user_id = 123 AND created_at > '2024-01-01'
ORDER BY created_at DESC;

-- ❌ Can't use index (function on column)
SELECT * FROM users WHERE LOWER(email) = 'john@example.com';
-- Fix: CREATE INDEX idx_users_email_lower ON users(LOWER(email));

-- ❌ Can't use index (leading wildcard)
SELECT * FROM users WHERE email LIKE '%@example.com';
-- Fix: Use full-text search or store domain separately

-- ✅ Can use index (trailing wildcard)
SELECT * FROM users WHERE email LIKE 'john%';
```

### Query Analysis (EXPLAIN)

**Always analyze slow queries before optimizing:**

```sql
-- PostgreSQL
EXPLAIN ANALYZE
SELECT * FROM orders o
JOIN users u ON o.user_id = u.id
WHERE u.email = 'john@example.com'
ORDER BY o.created_at DESC
LIMIT 10;

-- MySQL
EXPLAIN
SELECT * FROM orders o
JOIN users u ON o.user_id = u.id
WHERE u.email = 'john@example.com'
ORDER BY o.created_at DESC
LIMIT 10;
```

**Look for:**
- Seq Scan (full table scan) - add index?
- Hash Join (expensive) - add index on join column
- Sort (expensive) - add index with correct sort order
- High execution time - which step is slow?

### Avoiding SELECT *

**Fetch only columns you need:**

```sql
-- ❌ Fetches all columns (slower, more bandwidth)
SELECT * FROM orders WHERE user_id = 123;

-- ✅ Fetch only needed columns
SELECT id, user_id, total_amount, created_at
FROM orders
WHERE user_id = 123;

-- ✅ Reduces memory/bandwidth especially for large text columns
SELECT id, user_id, total_amount
FROM orders
WHERE user_id = 123;
```

### Connection Pooling

**Use connection pooling in production:**

```python
# ❌ Anti-pattern: New connection per query
def get_user(user_id):
    conn = connect()  # New connection!
    user = conn.query('SELECT * FROM users WHERE id = ?', user_id)
    conn.close()
    return user

# ✅ Use connection pool
pool = ConnectionPool(
    host='localhost',
    database='myapp',
    min_size=5,
    max_size=20,
    timeout=30
)

def get_user(user_id):
    with pool.get_connection() as conn:  # Reuses from pool
        return conn.query('SELECT * FROM users WHERE id = ?', user_id)
```

**Pool configuration (tune for your workload):**
- `min_size`: Minimum idle connections (default 5-10)
- `max_size`: Maximum concurrent connections (default 20-50)
- `timeout`: Connection acquisition timeout
- `idle_timeout`: Close idle connections after N seconds

## SQL vs NoSQL Considerations

### When to Use SQL (ACID, Relations)

**Use SQL when:**
- Data has strong relationships (orders → users → addresses)
- Consistency is critical (financial transactions, inventory)
- Need complex queries with JOINs
- Data is structured and schema is stable
- Multi-record transactions (ACID guarantees)

**Example scenarios:**
- E-commerce: Products, Orders, Users with complex relationships
- Banking: Transactions must be atomic and consistent
- CRM: Complex queries across related entities
- Content management: Structured articles with authors, tags, categories

### When to Use NoSQL (Scale, Flexibility)

**Use NoSQL when:**
- Data is unstructured or semi-structured
- Schema evolves rapidly (different object shapes)
- Horizontal scaling is priority (sharding)
- High write throughput needed
- Document-oriented data (JSON-like)

**Example scenarios:**
- Real-time analytics: Time-series data
- Content platforms: Variable document structures
- Caching layer: Key-value store
- Event streaming: Logs, events, activity feeds
- Catalog systems: Products with variable attributes

**Document database (MongoDB, Firebase):**
```
✅ Good: User profiles with flexible attributes
✅ Good: Product catalog with variable specs
❌ Bad: Complex multi-entity queries and JOINs

Document structure:
{
  _id: 1,
  name: "John",
  email: "john@example.com",
  preferences: {
    language: "en",
    theme: "dark",
    notifications: true
  }
}
```

**Key-value store (Redis, Memcached):**
```
✅ Good: Caching, sessions, rate limiting
✅ Good: Real-time leaderboards
❌ Bad: Complex queries, relationships

Structure:
user:123 → { name, email, created_at }
session:abc123 → { user_id, expires_at }
```

**Graph database (Neo4j):**
```
✅ Good: Social networks, recommendations
✅ Good: Complex relationship queries
❌ Bad: Simple CRUD operations

Relationships:
User -[:FOLLOWS]-> User
User -[:COMMENTED_ON]-> Post
```

## Testing Database Code

### Test Databases

**Use separate test database:**

```python
# config.py
if os.getenv('ENV') == 'test':
    DATABASE_URL = 'postgresql://test_user:test_pass@localhost/test_db'
else:
    DATABASE_URL = os.getenv('DATABASE_URL')

# conftest.py (pytest)
@pytest.fixture(autouse=True)
def setup_test_db():
    """Create test database and tables before each test."""
    # Create tables
    db.create_all()
    yield
    # Cleanup
    db.drop_all()
```

### Fixtures and Seeds

**Use fixtures for test data:**

```python
# conftest.py
import pytest
from app.models import User, Order

@pytest.fixture
def sample_user(db):
    """Create a test user."""
    user = User(name='John Doe', email='john@example.com')
    db.add(user)
    db.commit()
    return user

@pytest.fixture
def sample_orders(db, sample_user):
    """Create orders for test user."""
    orders = [
        Order(user_id=sample_user.id, total_amount=100.00),
        Order(user_id=sample_user.id, total_amount=200.00),
    ]
    db.add_all(orders)
    db.commit()
    return orders

# test_orders.py
def test_get_user_orders(sample_user, sample_orders):
    """Test fetching user orders."""
    orders = Order.query.filter_by(user_id=sample_user.id).all()
    assert len(orders) == 2
    assert sum(o.total_amount for o in orders) == 300.00
```

### Transaction Rollback

**Rollback transactions to isolate tests:**

```python
# conftest.py - Automatic rollback after each test
@pytest.fixture(autouse=True)
def db_transaction(db):
    """Wrap each test in a transaction that rolls back."""
    transaction = db.begin_nested()
    yield
    transaction.rollback()  # Undo all changes from this test

# Or use explicit rollback
def test_create_user():
    db.begin()
    user = User(name='John', email='john@example.com')
    db.add(user)
    db.commit()
    assert user.id is not None

    db.rollback()
    # Changes are undone, database is clean for next test
```

## Common Patterns (SQL and NoSQL)

### Soft Deletes

**Mark records as deleted instead of removing:**

```sql
-- Add deleted_at column
ALTER TABLE users ADD COLUMN deleted_at TIMESTAMP NULL;

-- Soft delete (update)
UPDATE users SET deleted_at = CURRENT_TIMESTAMP WHERE id = 123;

-- Query only active records
SELECT * FROM users WHERE deleted_at IS NULL;

-- Create index on deleted_at for efficient queries
CREATE INDEX idx_users_active ON users(deleted_at) WHERE deleted_at IS NULL;
```

**Pros:** Recoverable, audit trail, can restore data
**Cons:** Need to remember to filter deleted records everywhere

### Audit Logs

**Track all data changes:**

```sql
CREATE TABLE audit_log (
    id BIGSERIAL PRIMARY KEY,
    entity_type VARCHAR(100),
    entity_id BIGINT,
    action VARCHAR(20), -- CREATE, UPDATE, DELETE
    old_values JSONB,
    new_values JSONB,
    changed_by BIGINT REFERENCES users(id),
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- PostgreSQL trigger to auto-log changes
CREATE FUNCTION audit_trigger() RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO audit_log (entity_type, entity_id, action, new_values, changed_at)
    VALUES ('user', NEW.id, TG_OP, row_to_json(NEW), NOW());
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER users_audit AFTER UPDATE ON users
FOR EACH ROW EXECUTE FUNCTION audit_trigger();
```

### Timestamps (Created/Updated)

**Track record creation and modification:**

```sql
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Auto-update updated_at on changes (PostgreSQL)
CREATE FUNCTION update_timestamp() RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER users_update_timestamp BEFORE UPDATE ON users
FOR EACH ROW EXECUTE FUNCTION update_timestamp();
```

### Hierarchical Data (Trees)

**Store tree structures in relational database:**

```sql
-- Option 1: Adjacency List (simple, slow to query)
CREATE TABLE categories (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255),
    parent_id BIGINT REFERENCES categories(id)
);

-- Query children
SELECT * FROM categories WHERE parent_id = 5;

-- Query ancestors (recursive, expensive)
WITH RECURSIVE ancestors AS (
    SELECT id, name, parent_id FROM categories WHERE id = 5
    UNION ALL
    SELECT c.id, c.name, c.parent_id
    FROM categories c
    JOIN ancestors a ON c.id = a.parent_id
)
SELECT * FROM ancestors;
```

```sql
-- Option 2: Closure Table (trade space for query speed)
CREATE TABLE categories (id BIGSERIAL PRIMARY KEY, name VARCHAR(255));

CREATE TABLE category_closure (
    ancestor_id BIGINT REFERENCES categories(id),
    descendant_id BIGINT REFERENCES categories(id),
    depth INT,
    PRIMARY KEY (ancestor_id, descendant_id)
);

-- Query all descendants
SELECT c.* FROM categories c
JOIN category_closure cc ON c.id = cc.descendant_id
WHERE cc.ancestor_id = 5 AND cc.depth > 0;
```

### Pagination

**Implement efficient pagination:**

```sql
-- ❌ OFFSET is slow for large offsets
SELECT * FROM orders LIMIT 10 OFFSET 100000;

-- ✅ Better: Keyset pagination (cursor-based)
SELECT * FROM orders
WHERE id > 12345  -- Last ID from previous page
ORDER BY id
LIMIT 10;

-- ✅ With composite key
SELECT * FROM orders
WHERE (user_id, created_at) > (123, '2024-11-17')
ORDER BY user_id, created_at
LIMIT 10;
```

### Transactions

**Use transactions for data consistency:**

```python
# ❌ No transaction - inconsistent state if error occurs
user = db.query(User).get(123)
user.balance -= 50
db.commit()

account = db.query(Account).get(456)
account.balance += 50
db.commit()  # If this fails, money disappears!

# ✅ Transaction - all-or-nothing
try:
    with db.transaction():
        user = db.query(User).get(123)
        user.balance -= 50

        account = db.query(Account).get(456)
        account.balance += 50

        db.flush()
except Exception:
    # Everything rolls back automatically
    raise
```

## Common Pitfalls

### N+1 Queries

**Problem:** One query per item instead of batching
**Fix:** Use eager loading or batch queries

### Missing Indexes

**Problem:** Slow queries on large tables
**Fix:** Analyze slow queries with EXPLAIN, add indexes on WHERE/JOIN columns

### No Transaction Boundaries

**Problem:** Inconsistent data if error occurs mid-operation
**Fix:** Wrap multi-step operations in transactions

### Over-Normalization

**Problem:** Too many JOINs make queries slow and complex
**Fix:** Denormalize strategically where proven necessary

### Unbounded Queries

**Problem:** SELECT * without LIMIT causes memory exhaustion
**Fix:** Always LIMIT and paginate large result sets

### Wrong Cascade Rules

**Problem:** Accidental data loss or orphaned records
**Fix:** Choose CASCADE, RESTRICT, or SET NULL deliberately

### Storing Passwords in Plain Text

**Problem:** Security breach if database compromised
**Fix:** Store bcrypt hashes, never plain passwords

### Accidental Type Mismatches

**Problem:** VARCHAR(255) used for numbers, can't query properly
**Fix:** Use correct data types (INTEGER, BIGINT, DECIMAL, not VARCHAR)

### Not Testing Migrations

**Problem:** Migration fails in production, downtime
**Fix:** Test migrations on production-like data before deploying

### Schema Changes Without Backward Compatibility

**Problem:** Old application code breaks with new schema
**Fix:** Support both old and new columns temporarily, add deprecation period

### No Query Timeouts

**Problem:** Slow query locks database, cascading failures
**Fix:** Set statement timeouts and query timeouts in production

---

**See project-specific database configuration in `.claude/CLAUDE.md` if present.**
