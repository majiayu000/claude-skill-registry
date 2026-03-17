---
name: migration-generator
description: Create database migrations from model changes, schema diffs, and migration best practices.
---

# Migration Generator Skill

Create database migrations from model changes, schema diffs, and migration best practices.

## Instructions

You are a database migration expert. When invoked:

1. **Detect Schema Changes**:
   - Compare current schema with desired state
   - Identify added/removed tables and columns
   - Detect modified column types and constraints
   - Find changed indexes and foreign keys

2. **Generate Migration Files**:
   - Create forward (up) and backward (down) migrations
   - Use ORM-specific migration format when applicable
   - Include data migrations when needed
   - Handle edge cases and potential data loss

3. **Ensure Safety**:
   - Prevent accidental data deletion
   - Add rollback capability
   - Include validation steps
   - Warn about breaking changes

4. **Best Practices**:
   - Make migrations atomic and reversible
   - Avoid destructive operations in production
   - Test migrations on staging first
   - Keep migrations small and focused

## Supported Frameworks

- **SQL**: Raw SQL migrations (PostgreSQL, MySQL, SQLite)
- **Node.js**: Prisma, TypeORM, Sequelize, Knex.js
- **Python**: Alembic, Django migrations, SQLAlchemy
- **Ruby**: Rails Active Record Migrations
- **Go**: golang-migrate, goose
- **PHP**: Laravel migrations, Doctrine

## Usage Examples

```
@migration-generator Add user email verification
@migration-generator --from-diff
@migration-generator --rollback
@migration-generator --data-migration
@migration-generator --zero-downtime
```

## Raw SQL Migrations

### PostgreSQL - Add Table
```sql
-- migrations/001_create_users_table.up.sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(50) UNIQUE NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  active BOOLEAN DEFAULT true NOT NULL,
  created_at TIMESTAMP DEFAULT NOW() NOT NULL,
  updated_at TIMESTAMP DEFAULT NOW() NOT NULL
);

-- Create indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_active ON users(active) WHERE active = true;

-- Add comments
COMMENT ON TABLE users IS 'Application users';
COMMENT ON COLUMN users.email IS 'User email address (unique)';

-- migrations/001_create_users_table.down.sql
DROP TABLE IF EXISTS users CASCADE;
```

### Add Column with Default Value
```sql
-- migrations/002_add_email_verified.up.sql
-- Step 1: Add column as nullable
ALTER TABLE users ADD COLUMN email_verified BOOLEAN;

-- Step 2: Set default value for existing rows
UPDATE users SET email_verified = false WHERE email_verified IS NULL;

-- Step 3: Make column NOT NULL
ALTER TABLE users ALTER COLUMN email_verified SET NOT NULL;

-- Step 4: Set default for future rows
ALTER TABLE users ALTER COLUMN email_verified SET DEFAULT false;

-- migrations/002_add_email_verified.down.sql
ALTER TABLE users DROP COLUMN email_verified;
```

### Modify Column Type (Safe)
```sql
-- migrations/003_increase_email_length.up.sql
-- Safe: increasing varchar length
ALTER TABLE users ALTER COLUMN email TYPE VARCHAR(320);

-- migrations/003_increase_email_length.down.sql
-- Warning: May fail if data exceeds old limit
ALTER TABLE users ALTER COLUMN email TYPE VARCHAR(255);
```

### Add Foreign Key
```sql
-- migrations/004_create_orders.up.sql
CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL,
  total_amount DECIMAL(10,2) NOT NULL CHECK (total_amount >= 0),
  status VARCHAR(20) DEFAULT 'pending' NOT NULL,
  created_at TIMESTAMP DEFAULT NOW() NOT NULL,
  updated_at TIMESTAMP DEFAULT NOW() NOT NULL,

  CONSTRAINT fk_orders_user_id
    FOREIGN KEY (user_id)
    REFERENCES users(id)
    ON DELETE CASCADE
);

-- Indexes for foreign keys and common queries
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_created_at ON orders(created_at);

-- Composite index for common query pattern
CREATE INDEX idx_orders_user_status ON orders(user_id, status);

-- migrations/004_create_orders.down.sql
DROP TABLE IF EXISTS orders CASCADE;
```

### Rename Column (Safe)
```sql
-- migrations/005_rename_password_column.up.sql
-- Step 1: Add new column
ALTER TABLE users ADD COLUMN password_hash_new VARCHAR(255);

-- Step 2: Copy data
UPDATE users SET password_hash_new = password_hash;

-- Step 3: Make NOT NULL
ALTER TABLE users ALTER COLUMN password_hash_new SET NOT NULL;

-- Step 4: Drop old column
ALTER TABLE users DROP COLUMN password_hash;

-- Step 5: Rename new column
ALTER TABLE users RENAME COLUMN password_hash_new TO password_hash;

-- migrations/005_rename_password_column.down.sql
-- Reversible using same pattern
ALTER TABLE users ADD COLUMN password_hash_old VARCHAR(255);
UPDATE users SET password_hash_old = password_hash;
ALTER TABLE users ALTER COLUMN password_hash_old SET NOT NULL;
ALTER TABLE users DROP COLUMN password_hash;
ALTER TABLE users RENAME COLUMN password_hash_old TO password_hash;
```

## ORM Migration Examples

### Prisma Migrations
```prisma
// schema.prisma - Add new model
model User {
  id            Int       @id @default(autoincrement())
  email         String    @unique
  username      String    @unique
  passwordHash  String    @map("password_hash")
  active        Boolean   @default(true)
  emailVerified Boolean   @default(false) @map("email_verified")
  createdAt     DateTime  @default(now()) @map("created_at")
  updatedAt     DateTime  @updatedAt @map("updated_at")

  orders  Order[]
  profile UserProfile?

  @@index([email])
  @@index([username])
  @@map("users")
}

model UserProfile {
  id        Int      @id @default(autoincrement())
  userId    Int      @unique @map("user_id")
  bio       String?  @db.Text
  avatarUrl String?  @map("avatar_url")

  user User @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@map("user_profiles")
}
```

```bash
# Generate migration
npx prisma migrate dev --name add_user_profile

# Apply migration in production
npx prisma migrate deploy

# Reset database (development only!)
npx prisma migrate reset
```

**Generated Migration:**
```sql
-- CreateTable
CREATE TABLE "user_profiles" (
    "id" SERIAL NOT NULL,
    "user_id" INTEGER NOT NULL,
    "bio" TEXT,
    "avatar_url" TEXT,

    CONSTRAINT "user_profiles_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "user_profiles_user_id_key" ON "user_profiles"("user_id");

-- AddForeignKey
ALTER TABLE "user_profiles" ADD CONSTRAINT "user_profiles_user_id_fkey"
  FOREIGN KEY ("user_id") REFERENCES "users"("id") ON DELETE CASCADE ON UPDATE CASCADE;
```

### TypeORM Migrations
```typescript
// migration/1234567890123-CreateUser.ts
import { MigrationInterface, QueryRunner, Table, TableIndex } from 'typeorm';

export class CreateUser1234567890123 implements MigrationInterface {
  public async up(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.createTable(
      new Table({
        name: 'users',
        columns: [
          {
            name: 'id',
            type: 'int',
            isPrimary: true,
            isGenerated: true,
            generationStrategy: 'increment',
          },
          {
            name: 'email',
            type: 'varchar',
            length: '255',
            isUnique: true,
            isNullable: false,
          },
          {
            name: 'username',
            type: 'varchar',
            length: '50',
            isUnique: true,
            isNullable: false,
          },
          {
            name: 'password_hash',
            type: 'varchar',
            length: '255',
            isNullable: false,
          },
          {
            name: 'active',
            type: 'boolean',
            default: true,
            isNullable: false,
          },
          {
            name: 'created_at',
            type: 'timestamp',
            default: 'now()',
            isNullable: false,
          },
          {
            name: 'updated_at',
            type: 'timestamp',
            default: 'now()',
            isNullable: false,
          },
        ],
      }),
      true,
    );

    // Create indexes
    await queryRunner.createIndex(
      'users',
      new TableIndex({
        name: 'idx_users_email',
        columnNames: ['email'],
      }),
    );

    await queryRunner.createIndex(
      'users',
      new TableIndex({
        name: 'idx_users_username',
        columnNames: ['username'],
      }),
    );
  }

  public async down(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.dropTable('users');
  }
}
```

```typescript
// migration/1234567890124-AddForeignKey.ts
import { MigrationInterface, QueryRunner, Table, TableForeignKey } from 'typeorm';

export class AddOrdersForeignKey1234567890124 implements MigrationInterface {
  public async up(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.createTable(
      new Table({
        name: 'orders',
        columns: [
          {
            name: 'id',
            type: 'int',
            isPrimary: true,
            isGenerated: true,
            generationStrategy: 'increment',
          },
          {
            name: 'user_id',
            type: 'int',
            isNullable: false,
          },
          {
            name: 'total_amount',
            type: 'decimal',
            precision: 10,
            scale: 2,
            isNullable: false,
          },
          {
            name: 'status',
            type: 'varchar',
            length: '20',
            default: "'pending'",
            isNullable: false,
          },
          {
            name: 'created_at',
            type: 'timestamp',
            default: 'now()',
          },
        ],
      }),
      true,
    );

    // Add foreign key
    await queryRunner.createForeignKey(
      'orders',
      new TableForeignKey({
        columnNames: ['user_id'],
        referencedColumnNames: ['id'],
        referencedTableName: 'users',
        onDelete: 'CASCADE',
      }),
    );
  }

  public async down(queryRunner: QueryRunner): Promise<void> {
    const table = await queryRunner.getTable('orders');
    const foreignKey = table.foreignKeys.find(
      fk => fk.columnNames.indexOf('user_id') !== -1,
    );
    await queryRunner.dropForeignKey('orders', foreignKey);
    await queryRunner.dropTable('orders');
  }
}
```

```bash
# Generate migration
npx typeorm migration:generate -n AddUserProfile

# Run migrations
npx typeorm migration:run

# Revert last migration
npx typeorm migration:revert
```

### Alembic (Python/SQLAlchemy)
```python
# alembic/versions/001_create_users_table.py
"""create users table

Revision ID: 001
Revises:
Create Date: 2024-01-01 12:00:00.000000

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
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('active', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )

    # Create indexes
    op.create_index('idx_users_email', 'users', ['email'])
    op.create_index('idx_users_username', 'users', ['username'])
    op.create_index(
        'idx_users_active',
        'users',
        ['active'],
        postgresql_where=sa.text('active = true')
    )

def downgrade():
    op.drop_table('users')
```

```python
# alembic/versions/002_add_email_verified.py
"""add email_verified column

Revision ID: 002
Revises: 001
Create Date: 2024-01-02 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None

def upgrade():
    # Add column as nullable first
    op.add_column('users', sa.Column('email_verified', sa.Boolean(), nullable=True))

    # Set default value for existing rows
    op.execute('UPDATE users SET email_verified = false WHERE email_verified IS NULL')

    # Make column NOT NULL
    op.alter_column('users', 'email_verified', nullable=False, server_default='false')

def downgrade():
    op.drop_column('users', 'email_verified')
```

```bash
# Generate migration
alembic revision --autogenerate -m "add user profile"

# Run migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Rollback to specific version
alembic downgrade 001
```

### Django Migrations
```python
# app/migrations/0001_initial.py
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('username', models.CharField(max_length=50, unique=True)),
                ('password_hash', models.CharField(max_length=255)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['email'], name='idx_users_email'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['username'], name='idx_users_username'),
        ),
    ]
```

```python
# app/migrations/0002_add_user_profile.py
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('avatar_url', models.URLField(blank=True, null=True)),
                ('user', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='app.user',
                    related_name='profile'
                )),
            ],
            options={
                'db_table': 'user_profiles',
            },
        ),
    ]
```

```bash
# Generate migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Rollback to specific migration
python manage.py migrate app 0001

# Show migration status
python manage.py showmigrations
```

## Data Migrations

### Backfill Data (PostgreSQL)
```sql
-- migrations/006_backfill_user_roles.up.sql
-- Add role column
ALTER TABLE users ADD COLUMN role VARCHAR(20);

-- Backfill existing users with default role
UPDATE users SET role = 'member' WHERE role IS NULL;

-- Make NOT NULL after backfill
ALTER TABLE users ALTER COLUMN role SET NOT NULL;
ALTER TABLE users ALTER COLUMN role SET DEFAULT 'member';

-- Add check constraint
ALTER TABLE users ADD CONSTRAINT chk_users_role
  CHECK (role IN ('admin', 'member', 'guest'));

-- migrations/006_backfill_user_roles.down.sql
ALTER TABLE users DROP COLUMN role;
```

### Complex Data Migration (Node.js/TypeORM)
```typescript
// migration/1234567890125-MigrateUserData.ts
import { MigrationInterface, QueryRunner } from 'typeorm';

export class MigrateUserData1234567890125 implements MigrationInterface {
  public async up(queryRunner: QueryRunner): Promise<void> {
    // Get all users
    const users = await queryRunner.query('SELECT id, full_name FROM users');

    // Split full_name into first_name and last_name
    for (const user of users) {
      const parts = user.full_name?.split(' ') || ['', ''];
      const firstName = parts[0] || '';
      const lastName = parts.slice(1).join(' ') || '';

      await queryRunner.query(
        'UPDATE users SET first_name = $1, last_name = $2 WHERE id = $3',
        [firstName, lastName, user.id],
      );
    }

    // Drop old column
    await queryRunner.query('ALTER TABLE users DROP COLUMN full_name');
  }

  public async down(queryRunner: QueryRunner): Promise<void> {
    // Add back full_name column
    await queryRunner.query('ALTER TABLE users ADD COLUMN full_name VARCHAR(255)');

    // Reconstruct full_name
    await queryRunner.query(
      `UPDATE users SET full_name = first_name || ' ' || last_name`,
    );

    // Drop first_name and last_name
    await queryRunner.query('ALTER TABLE users DROP COLUMN first_name');
    await queryRunner.query('ALTER TABLE users DROP COLUMN last_name');
  }
}
```

### Data Migration with Python/Alembic
```python
# alembic/versions/003_migrate_prices.py
"""migrate prices to cents

Revision ID: 003
Revises: 002
Create Date: 2024-01-03 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = '003'
down_revision = '002'

def upgrade():
    # Add new column
    op.add_column('products', sa.Column('price_cents', sa.Integer(), nullable=True))

    # Migrate data: convert decimal to cents
    op.execute('''
        UPDATE products
        SET price_cents = CAST(price * 100 AS INTEGER)
    ''')

    # Make NOT NULL after migration
    op.alter_column('products', 'price_cents', nullable=False)

    # Drop old column
    op.drop_column('products', 'price')

    # Rename new column
    op.alter_column('products', 'price_cents', new_column_name='price')

def downgrade():
    # Add back decimal column
    op.add_column('products', sa.Column('price_decimal', sa.Numeric(10, 2), nullable=True))

    # Convert back to decimal
    op.execute('''
        UPDATE products
        SET price_decimal = price / 100.0
    ''')

    op.alter_column('products', 'price_decimal', nullable=False)
    op.drop_column('products', 'price')
    op.alter_column('products', 'price_decimal', new_column_name='price')
```

## Zero-Downtime Migrations

### Adding NOT NULL Column
```sql
-- Migration 1: Add column as nullable
ALTER TABLE users ADD COLUMN phone VARCHAR(20);

-- Deploy application code that writes to phone column

-- Migration 2: Backfill existing data
UPDATE users SET phone = 'UNKNOWN' WHERE phone IS NULL;

-- Migration 3: Make column NOT NULL
ALTER TABLE users ALTER COLUMN phone SET NOT NULL;
ALTER TABLE users ALTER COLUMN phone SET DEFAULT 'UNKNOWN';
```

### Renaming Column (Zero Downtime)
```sql
-- Phase 1: Add new column
ALTER TABLE users ADD COLUMN email_address VARCHAR(255);

-- Phase 2: Deploy app code that writes to both columns

-- Phase 3: Backfill data
UPDATE users SET email_address = email WHERE email_address IS NULL;

-- Phase 4: Deploy app code that reads from new column

-- Phase 5: Drop old column
ALTER TABLE users DROP COLUMN email;

-- Phase 6: Rename new column (optional)
ALTER TABLE users RENAME COLUMN email_address TO email;
```

### Removing Column (Safe)
```sql
-- Phase 1: Deploy code that doesn't use the column

-- Phase 2: Remove NOT NULL constraint (make safe to rollback)
ALTER TABLE users ALTER COLUMN deprecated_field DROP NOT NULL;

-- Phase 3: Wait and verify no issues

-- Phase 4: Drop the column
ALTER TABLE users DROP COLUMN deprecated_field;
```

## Common Patterns

### Add Enum Column
```sql
-- Create enum type (PostgreSQL)
CREATE TYPE user_status AS ENUM ('active', 'inactive', 'suspended');

-- Add column with enum type
ALTER TABLE users ADD COLUMN status user_status DEFAULT 'active' NOT NULL;

-- Rollback
ALTER TABLE users DROP COLUMN status;
DROP TYPE user_status;
```

### Add JSON Column
```sql
-- PostgreSQL
ALTER TABLE users ADD COLUMN metadata JSONB DEFAULT '{}' NOT NULL;
CREATE INDEX idx_users_metadata ON users USING GIN(metadata);

-- MySQL
ALTER TABLE users ADD COLUMN metadata JSON;
```

### Add Full-Text Search
```sql
-- PostgreSQL
ALTER TABLE products ADD COLUMN search_vector tsvector;

-- Create generated column
UPDATE products SET search_vector =
  to_tsvector('english', name || ' ' || description);

-- Create GIN index for fast searching
CREATE INDEX idx_products_search ON products USING GIN(search_vector);

-- Trigger to keep search_vector updated
CREATE TRIGGER products_search_update
BEFORE INSERT OR UPDATE ON products
FOR EACH ROW EXECUTE FUNCTION
  tsvector_update_trigger(search_vector, 'pg_catalog.english', name, description);
```

## Best Practices

### DO ✓
- **Make migrations reversible** - Always implement `down` migration
- **Test on staging first** - Never run untested migrations in production
- **Keep migrations small** - One logical change per migration
- **Use transactions** - Ensure atomicity (when DB supports it)
- **Backup before migration** - Always have a rollback plan
- **Add indexes concurrently** - Use `CONCURRENTLY` in PostgreSQL to avoid locks
- **Version control migrations** - Commit migrations with code changes
- **Document breaking changes** - Add comments for complex migrations
- **Use batch updates** - For large data migrations, process in chunks

### DON'T ✗
- **Never modify committed migrations** - Create new migration instead
- **Don't use SELECT *** - Specify columns in data migrations
- **Avoid long-running migrations** - Break into smaller steps
- **Don't assume data state** - Validate before transforming
- **Never skip migrations** - Run in order
- **Don't ignore warnings** - Address deprecation notices
- **Avoid circular dependencies** - Keep migration order clean
- **Don't forget indexes** - Especially on foreign keys

## Migration Checklist

```markdown
## Pre-Migration Checklist

- [ ] Migration tested on local database
- [ ] Migration tested on staging environment
- [ ] Database backup created
- [ ] Migration is reversible (down migration works)
- [ ] Reviewed for potential data loss
- [ ] Checked for long-running operations
- [ ] Foreign key constraints validated
- [ ] Indexes added for new columns
- [ ] Performance impact assessed
- [ ] Team notified of migration schedule

## Post-Migration Checklist

- [ ] Migration completed successfully
- [ ] Application logs checked for errors
- [ ] Database performance monitored
- [ ] Rollback plan tested (if needed)
- [ ] Documentation updated
- [ ] Migration marked as applied in version control
```

## Troubleshooting

### Migration Failed Mid-Way
```sql
-- Check migration status
SELECT * FROM schema_migrations;

-- Manual rollback if transaction failed
BEGIN;
-- Run down migration manually
ROLLBACK;

-- Or mark as not applied
DELETE FROM schema_migrations WHERE version = '20240101120000';
```

### Large Table Migration
```sql
-- Use batch processing for large updates
DO $$
DECLARE
  batch_size INTEGER := 1000;
  offset_val INTEGER := 0;
  rows_updated INTEGER;
BEGIN
  LOOP
    UPDATE users
    SET email_verified = false
    WHERE id IN (
      SELECT id FROM users
      WHERE email_verified IS NULL
      ORDER BY id
      LIMIT batch_size
      OFFSET offset_val
    );

    GET DIAGNOSTICS rows_updated = ROW_COUNT;
    EXIT WHEN rows_updated = 0;

    offset_val := offset_val + batch_size;
    COMMIT;
    RAISE NOTICE 'Updated % rows', offset_val;
  END LOOP;
END $$;
```

## Notes

- Always test migrations in non-production environment first
- Use database transactions when possible
- Keep migrations in version control
- Document complex migrations
- Consider zero-downtime strategies for production
- Monitor database performance during migrations
- Have rollback plan ready
- Use ORM migration tools when available for type safety
