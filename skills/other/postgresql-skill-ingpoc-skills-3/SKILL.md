---
name: postgresql-skill
description: This skill provides PostgreSQL-specific patterns for database design, optimization, and transaction management
---

# PostgreSQL Development

## Purpose

PostgreSQL is a powerful relational database. This skill documents patterns for safe transactions, optimization, and concurrent access.

## When to Use

Use this skill when:
- Designing database schema
- Creating migrations
- Implementing transactions
- Optimizing queries
- Managing connections

## Key Patterns

### 1. Transaction Management

Wrap operations in transactions:

```python
async def transfer_funds(self, from_account, to_account, amount):
    async with self.db.transaction():
        await self.db.execute(
            "UPDATE accounts SET balance = balance - ? WHERE id = ?",
            (amount, from_account)
        )
        await self.db.execute(
            "UPDATE accounts SET balance = balance + ? WHERE id = ?",
            (amount, to_account)
        )
```

### 2. Connection Pooling

Use connection pools for efficiency:

```python
pool = await asyncpg.create_pool(
    'postgresql://user:password@localhost/db',
    min_size=10,
    max_size=20
)
```

### 3. Query Optimization

Use proper indexing:

```sql
CREATE INDEX idx_user_email ON users(email);
CREATE INDEX idx_transaction_date ON transactions(created_at);
```

## See Also

- PostgreSQL Documentation: https://www.postgresql.org/docs/
