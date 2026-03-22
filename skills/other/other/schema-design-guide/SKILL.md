---
name: schema-design-guide
description: >
  Guide for relational database schema design with normalization, indexing strategy, constraints,
  naming conventions, and denormalization tradeoffs. Use when the user designs database tables,
  asks about normalization, needs indexing advice, or defines foreign key relationships. Trigger
  whenever database schema, table design, or data modeling is discussed.
---

# Schema Design Guide

Design well-structured relational database schemas with proper normalization, strategic indexing,
referential integrity, and clear naming conventions.

## When to Use
- User designs new database tables
- User asks about normalization or denormalization
- User needs help with indexing strategy
- User defines relationships between tables
- User asks about naming conventions for database objects

## Core Patterns

### Normalization (1NF through 3NF)

Apply normalization to eliminate redundancy, then selectively denormalize for performance.

```sql
-- BAD: Unnormalized (repeating groups, redundant data)
CREATE TABLE orders_bad (
  id SERIAL PRIMARY KEY,
  customer_name VARCHAR(255),
  customer_email VARCHAR(255),
  product1_name VARCHAR(255),
  product1_price DECIMAL(10,2),
  product2_name VARCHAR(255),
  product2_price DECIMAL(10,2)
);

-- GOOD: Normalized to 3NF
CREATE TABLE customers (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE products (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE orders (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  customer_id BIGINT NOT NULL REFERENCES customers(id),
  status VARCHAR(50) NOT NULL DEFAULT 'pending'
    CHECK (status IN ('pending', 'confirmed', 'shipped', 'delivered', 'cancelled')),
  ordered_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE order_items (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  order_id BIGINT NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
  product_id BIGINT NOT NULL REFERENCES products(id),
  quantity INT NOT NULL CHECK (quantity > 0),
  unit_price DECIMAL(10,2) NOT NULL CHECK (unit_price >= 0),
  UNIQUE (order_id, product_id)
);
```

### Indexing Strategy

Index columns used in WHERE, JOIN, and ORDER BY clauses. Prefer composite indexes
that match query patterns.

```sql
-- Index for frequent queries
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_status_ordered_at ON orders(status, ordered_at DESC);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);

-- Partial index for active records only
CREATE INDEX idx_orders_pending ON orders(ordered_at DESC)
  WHERE status = 'pending';

-- Covering index to avoid table lookups
CREATE INDEX idx_products_name_price ON products(name, price);

-- Expression index for case-insensitive search
CREATE INDEX idx_customers_email_lower ON customers(LOWER(email));

-- GIN index for full-text search
CREATE INDEX idx_products_name_search ON products USING gin(to_tsvector('english', name));
```

### Constraints and Data Integrity

Use database-level constraints as the last line of defense. Application validation
can have bugs; constraints cannot be bypassed.

```sql
CREATE TABLE accounts (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  email VARCHAR(255) NOT NULL,
  balance DECIMAL(12,2) NOT NULL DEFAULT 0 CHECK (balance >= 0),
  account_type VARCHAR(20) NOT NULL CHECK (account_type IN ('checking', 'savings')),
  opened_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  closed_at TIMESTAMPTZ,

  -- Ensure closed_at is after opened_at
  CONSTRAINT valid_dates CHECK (closed_at IS NULL OR closed_at > opened_at),

  -- Unique email per account type
  CONSTRAINT unique_email_per_type UNIQUE (email, account_type)
);

-- Foreign key with appropriate action
CREATE TABLE transactions (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  account_id BIGINT NOT NULL REFERENCES accounts(id) ON DELETE RESTRICT,
  amount DECIMAL(12,2) NOT NULL,
  description TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

### Naming Conventions

Consistent naming makes schemas self-documenting.

```sql
-- Tables: plural, snake_case
CREATE TABLE user_profiles (...);
CREATE TABLE order_items (...);

-- Columns: singular, snake_case
-- Primary key: id
-- Foreign key: referenced_table_singular_id
CREATE TABLE comments (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  user_id BIGINT NOT NULL REFERENCES users(id),
  post_id BIGINT NOT NULL REFERENCES posts(id),
  body TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Indexes: idx_table_columns
CREATE INDEX idx_comments_user_id ON comments(user_id);
CREATE INDEX idx_comments_post_id_created_at ON comments(post_id, created_at DESC);

-- Constraints: chk_table_description, uq_table_columns
ALTER TABLE comments ADD CONSTRAINT chk_comments_body_length CHECK (length(body) > 0);
```

### Strategic Denormalization

Denormalize only when you have measured performance problems and normalization is the
bottleneck.

```sql
-- Denormalized: Store computed totals for read-heavy dashboards
CREATE TABLE order_summaries (
  order_id BIGINT PRIMARY KEY REFERENCES orders(id),
  item_count INT NOT NULL DEFAULT 0,
  total_amount DECIMAL(12,2) NOT NULL DEFAULT 0,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Keep denormalized data in sync with a trigger
CREATE OR REPLACE FUNCTION update_order_summary()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO order_summaries (order_id, item_count, total_amount, updated_at)
  SELECT
    COALESCE(NEW.order_id, OLD.order_id),
    COUNT(*),
    COALESCE(SUM(quantity * unit_price), 0),
    now()
  FROM order_items
  WHERE order_id = COALESCE(NEW.order_id, OLD.order_id)
  ON CONFLICT (order_id)
  DO UPDATE SET
    item_count = EXCLUDED.item_count,
    total_amount = EXCLUDED.total_amount,
    updated_at = EXCLUDED.updated_at;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_order_items_summary
AFTER INSERT OR UPDATE OR DELETE ON order_items
FOR EACH ROW EXECUTE FUNCTION update_order_summary();
```

## Anti-Patterns

- **No primary key**: Every table must have a primary key. Without one, you cannot reliably update or delete specific rows.
- **Using VARCHAR for everything**: Use appropriate types -- INT for counts, DECIMAL for money, TIMESTAMPTZ for timestamps, BOOLEAN for flags.
- **Missing foreign keys**: Skipping foreign keys "for performance" leads to orphaned records and data corruption. The database should enforce referential integrity.
- **Over-indexing**: Every index slows writes and uses storage. Only index columns that appear in frequent query WHERE, JOIN, or ORDER BY clauses.
- **Premature denormalization**: Start normalized. Denormalize only when query performance is measurably insufficient and indexing cannot help.
- **Using soft deletes everywhere**: `deleted_at` columns add complexity to every query. Use them only when audit history is a real requirement.

## Quick Reference

| Normal Form | Rule | Fix |
|---|---|---|
| 1NF | No repeating groups | One value per cell, separate table for lists |
| 2NF | No partial dependencies | Every non-key column depends on the full PK |
| 3NF | No transitive dependencies | Non-key columns depend only on the PK |

| Index Type | Use Case |
|---|---|
| B-tree (default) | Equality, range, ORDER BY |
| Hash | Equality only (rare) |
| GIN | Full-text, JSONB, arrays |
| GiST | Geometric, range types |
| Partial | Queries filtering on a specific value |
