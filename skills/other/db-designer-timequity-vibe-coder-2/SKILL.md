---
name: db-designer
description: |
  Generate database schema from feature descriptions. User doesn't see SQL.
  Use when: features require data persistence.
  Triggers: internal use only.
---

# Database Designer

Infer schema from requirements. User never writes SQL.

## Process

1. **Analyze requirements**
   - "Users can save expenses" → users, expenses tables
   - "Track categories" → categories table
   - "Monthly reports" → consider aggregation

2. **Design schema**
   - Tables and columns
   - Relationships (1:1, 1:N, N:M)
   - Indexes for performance

3. **Generate migration**
   - Create migration file
   - Apply to database
   - Update ORM models

## Schema Patterns

| Feature | Tables |
|---------|--------|
| Auth | users, sessions |
| Blog | posts, comments, tags |
| E-commerce | products, orders, order_items |
| Tasks | tasks, projects, labels |
| Social | users, posts, follows, likes |

## Template-Specific

### Supabase (nextjs-supabase)
```sql
-- Auto-generated, user doesn't see
create table expenses (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references users(id),
  amount decimal not null,
  category text,
  created_at timestamptz default now()
);
```

### PostgreSQL (fastapi-postgres)
```python
# Alembic migration auto-generated
class Expense(Base):
    id = Column(UUID, primary_key=True)
    user_id = Column(UUID, ForeignKey('users.id'))
    amount = Column(Numeric, nullable=False)
```

### Drizzle (hono-drizzle)
```typescript
// Schema auto-generated
export const expenses = pgTable('expenses', {
  id: uuid('id').primaryKey().defaultRandom(),
  userId: uuid('user_id').references(() => users.id),
  amount: numeric('amount').notNull(),
});
```

## User Experience

User: "I want to track expenses by category"

Internally:
1. Create expenses table
2. Create categories table
3. Add foreign key
4. Generate models
5. Create migration
6. Apply to database

User sees: "✅ Ready to save expenses"
