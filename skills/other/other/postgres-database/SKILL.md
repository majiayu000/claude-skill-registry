---
name: postgres-database
description: PostgreSQL schema design, indexing, and query patterns. Use when designing database schemas, writing migrations, optimizing queries, or working with any PostgreSQL database.
---

# PostgreSQL Database Patterns

## Schema Design Principles
- Always add `created_at`, `updated_at` timestamps to every table
- Use `UUID` or `BIGSERIAL` for primary keys (UUID for distributed systems)
- Use foreign key constraints (never orphaned rows)
- Normalize to 3NF, then denormalize only for proven performance needs
- Soft delete with `deleted_at TIMESTAMP NULL` instead of hard delete

## Essential Indexes
```sql
-- Always index foreign keys
CREATE INDEX idx_posts_user_id ON posts(user_id);

-- Composite index for common filter+sort patterns
CREATE INDEX idx_posts_user_created ON posts(user_id, created_at DESC);

-- Partial index for active records only
CREATE INDEX idx_users_active_email ON users(email) WHERE deleted_at IS NULL;

-- Full text search
CREATE INDEX idx_posts_fts ON posts USING GIN(to_tsvector('english', title || ' ' || body));
```

## Migration Pattern (Alembic)
```python
def upgrade():
    op.create_table('posts',
        sa.Column('id', sa.BigInteger(), primary_key=True),
        sa.Column('user_id', sa.BigInteger(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('body', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
    )
    op.create_index('idx_posts_user_id', 'posts', ['user_id'])

def downgrade():
    op.drop_table('posts')
```

## Query Patterns
```sql
-- Pagination (use keyset, not OFFSET for large tables)
SELECT * FROM posts
WHERE created_at < $1  -- cursor
ORDER BY created_at DESC
LIMIT 20;

-- Avoid N+1: use JOIN or subquery
SELECT u.*, COUNT(p.id) as post_count
FROM users u
LEFT JOIN posts p ON p.user_id = u.id
GROUP BY u.id;

-- Upsert
INSERT INTO settings(user_id, key, value)
VALUES ($1, $2, $3)
ON CONFLICT (user_id, key) DO UPDATE SET value = EXCLUDED.value;
```

## Rules
- NEVER use SELECT * in production queries — list columns explicitly
- Always use parameterized queries — never f-string SQL (SQL injection risk)
- Use connection pooling (PgBouncer or SQLAlchemy pool_size)
- Run EXPLAIN ANALYZE on slow queries before adding indexes
- Use transactions for multi-table writes
- Vacuum and analyze after bulk operations
- Set statement_timeout to prevent runaway queries
