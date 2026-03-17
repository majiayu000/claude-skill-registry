---
name: database-implementer
description: Creates database schemas, migrations, queries, and data access layers. Use when implementing database-related tasks. Handles schema design, migrations, CRUD operations, and database optimization.
---

# Database Implementer Skill

## Instructions

1. Analyze database requirements from task
2. Review data models and relationships
3. Create database schema/migrations
4. Implement data access layer (models, repositories)
5. Write database queries
6. Add indexes and constraints
7. Return implementation with:
   - Migration files
   - Model definitions
   - Query implementations
   - Index and constraint definitions

## Examples

**Input:** "Create User and Task tables"
**Output:**
```sql
-- migrations/001_create_users_tasks.sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(60) NOT NULL,
    name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);

CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'todo',
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_status ON tasks(status);
```

## Database Implementation Areas

- **Schema Design**: Tables, columns, data types
- **Migrations**: Versioned schema changes
- **Relationships**: Foreign keys, joins, associations
- **Indexes**: Performance optimization indexes
- **Constraints**: Unique, check, not null constraints
- **Queries**: CRUD operations, complex queries
- **Data Access Layer**: Models, repositories, ORM usage
- **Optimization**: Query optimization, indexing strategy

## Best Practices

- **Normalization**: Proper database normalization
- **Indexes**: Index foreign keys and frequently queried columns
- **Migrations**: Versioned, reversible migrations
- **Constraints**: Use database constraints for data integrity
- **Performance**: Optimize queries, avoid N+1 problems
- **Backup Strategy**: Consider backup and recovery
