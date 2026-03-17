---
name: database-migration-helper
description: Creates database migrations with proper schema changes, data migrations, and rollback support for various ORMs (Prisma, TypeORM, Alembic, etc.). Use when managing database schema changes.
---

# Database Migration Helper Skill

Expert at creating safe, reversible database migrations across different frameworks and tools.

## When to Activate

- "create database migration for [change]"
- "generate migration to add [table/column]"
- "write data migration for [transformation]"

## Prisma Migrations

```prisma
// prisma/schema.prisma
model User {
  id        Int      @id @default(autoincrement())
  email     String   @unique
  name      String
  role      Role     @default(USER)
  posts     Post[]
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([email])
  @@map("users")
}

model Post {
  id          Int       @id @default(autoincrement())
  title       String
  slug        String    @unique
  content     String    @db.Text
  published   Boolean   @default(false)
  authorId    Int
  author      User      @relation(fields: [authorId], references: [id], onDelete: Cascade)
  publishedAt DateTime?
  createdAt   DateTime  @default(now())
  updatedAt   DateTime  @updatedAt

  @@index([slug])
  @@index([authorId, publishedAt])
  @@map("posts")
}

enum Role {
  USER
  ADMIN
  MODERATOR
}
```

```bash
# Create migration
npx prisma migrate dev --name add_user_role

# Apply migrations
npx prisma migrate deploy

# Reset database (development only)
npx prisma migrate reset

# Create migration without applying
npx prisma migrate dev --create-only
```

## TypeORM Migrations

```typescript
// migrations/1234567890-AddUserRole.ts
import { MigrationInterface, QueryRunner, TableColumn } from 'typeorm';

export class AddUserRole1234567890 implements MigrationInterface {
  name = 'AddUserRole1234567890';

  public async up(queryRunner: QueryRunner): Promise<void> {
    // Add role column
    await queryRunner.addColumn(
      'users',
      new TableColumn({
        name: 'role',
        type: 'enum',
        enum: ['user', 'admin', 'moderator'],
        default: "'user'",
      })
    );

    // Create index
    await queryRunner.createIndex(
      'users',
      new Index({
        name: 'IDX_USERS_ROLE',
        columnNames: ['role'],
      })
    );

    // Data migration - set existing users to 'user' role
    await queryRunner.query(
      `UPDATE users SET role = 'user' WHERE role IS NULL`
    );
  }

  public async down(queryRunner: QueryRunner): Promise<void> {
    // Remove index
    await queryRunner.dropIndex('users', 'IDX_USERS_ROLE');

    // Remove column
    await queryRunner.dropColumn('users', 'role');
  }
}
```

```bash
# Generate migration from entity changes
npm run typeorm migration:generate -- -n AddUserRole

# Create empty migration
npm run typeorm migration:create -- -n DataMigration

# Run migrations
npm run typeorm migration:run

# Revert last migration
npm run typeorm migration:revert
```

## Alembic (Python) Migrations

```python
# alembic/versions/001_add_user_role.py
"""add user role

Revision ID: 001
Revises:
Create Date: 2024-01-01 12:00:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create enum type
    role_enum = postgresql.ENUM('user', 'admin', 'moderator', name='role')
    role_enum.create(op.get_bind())

    # Add column
    op.add_column(
        'users',
        sa.Column('role', role_enum, nullable=False, server_default='user')
    )

    # Create index
    op.create_index('ix_users_role', 'users', ['role'])

    # Data migration
    op.execute("""
        UPDATE users
        SET role = 'admin'
        WHERE email IN (SELECT email FROM admin_emails)
    """)


def downgrade():
    # Remove index
    op.drop_index('ix_users_role', table_name='users')

    # Remove column
    op.drop_column('users', 'role')

    # Drop enum
    op.execute('DROP TYPE role')
```

```bash
# Create migration
alembic revision -m "add user role"

# Auto-generate migration from models
alembic revision --autogenerate -m "add user role"

# Run migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Show current version
alembic current
```

## Sequelize Migrations (Node.js)

```javascript
// migrations/20240101120000-add-user-role.js
'use strict';

module.exports = {
  up: async (queryInterface, Sequelize) => {
    // Add column
    await queryInterface.addColumn('users', 'role', {
      type: Sequelize.ENUM('user', 'admin', 'moderator'),
      allowNull: false,
      defaultValue: 'user',
    });

    // Add index
    await queryInterface.addIndex('users', ['role'], {
      name: 'users_role_idx',
    });

    // Data migration using raw SQL
    await queryInterface.sequelize.query(`
      UPDATE users
      SET role = 'admin'
      WHERE is_admin = true
    `);

    // Remove old column
    await queryInterface.removeColumn('users', 'is_admin');
  },

  down: async (queryInterface, Sequelize) => {
    // Re-add old column
    await queryInterface.addColumn('users', 'is_admin', {
      type: Sequelize.BOOLEAN,
      defaultValue: false,
    });

    // Reverse data migration
    await queryInterface.sequelize.query(`
      UPDATE users
      SET is_admin = true
      WHERE role = 'admin'
    `);

    // Remove index
    await queryInterface.removeIndex('users', 'users_role_idx');

    // Remove column and enum
    await queryInterface.removeColumn('users', 'role');
    await queryInterface.sequelize.query('DROP TYPE IF EXISTS "enum_users_role"');
  },
};
```

## Raw SQL Migration Template

```sql
-- Up Migration
-- migrations/001_add_user_role_up.sql

-- Add enum type (PostgreSQL)
CREATE TYPE user_role AS ENUM ('user', 'admin', 'moderator');

-- Add column
ALTER TABLE users ADD COLUMN role user_role NOT NULL DEFAULT 'user';

-- Create index
CREATE INDEX idx_users_role ON users(role);

-- Data migration
UPDATE users SET role = 'admin' WHERE id IN (1, 2, 3);

-- Down Migration
-- migrations/001_add_user_role_down.sql

-- Remove index
DROP INDEX IF EXISTS idx_users_role;

-- Remove column
ALTER TABLE users DROP COLUMN IF EXISTS role;

-- Drop type
DROP TYPE IF EXISTS user_role;
```

## Complex Data Migration Example

```typescript
// Data transformation migration
export class MigrateUserData1234567890 implements MigrationInterface {
  public async up(queryRunner: QueryRunner): Promise<void> {
    // 1. Create new table structure
    await queryRunner.query(`
      CREATE TABLE users_new (
        id SERIAL PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        profile JSONB NOT NULL,
        created_at TIMESTAMP DEFAULT NOW()
      )
    `);

    // 2. Migrate data with transformation
    await queryRunner.query(`
      INSERT INTO users_new (id, email, profile, created_at)
      SELECT
        id,
        email,
        jsonb_build_object(
          'firstName', first_name,
          'lastName', last_name,
          'phone', phone,
          'address', jsonb_build_object(
            'street', address_street,
            'city', address_city,
            'zip', address_zip
          )
        ) as profile,
        created_at
      FROM users_old
    `);

    // 3. Drop old table
    await queryRunner.query(`DROP TABLE users_old`);

    // 4. Rename new table
    await queryRunner.query(`ALTER TABLE users_new RENAME TO users`);
  }

  public async down(queryRunner: QueryRunner): Promise<void> {
    // Reverse migration
    // ... implementation
  }
}
```

## Best Practices

- Always include both `up` and `down` migrations
- Test migrations on copy of production data
- Use transactions for data migrations
- Add indexes after data insertion for large tables
- Version control all migrations
- Never modify existing migrations after deployment
- Use descriptive migration names
- Add comments explaining complex migrations
- Test rollback procedures
- Back up database before major migrations
- Use batching for large data migrations
- Monitor migration execution time
- Handle NULL values properly
- Validate data after migration

## Output Checklist

- ✅ Migration file created
- ✅ Up migration implemented
- ✅ Down migration implemented
- ✅ Indexes added
- ✅ Data migration (if needed)
- ✅ Constraints added
- ✅ Tested on sample data
- 📝 Migration notes documented
