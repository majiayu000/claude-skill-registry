---
name: database-migration
description: Execute database migrations across ORMs and platforms with zero-downtime strategies, data transformation, and rollback procedures. Use when migrating databases, changing schemas, performing data transformations, or implementing zero-downtime deployment strategies.
---

# Database Migration

## ORM Migrations

### Sequelize
```javascript
module.exports = {
  up: async (queryInterface, Sequelize) => {
    await queryInterface.createTable('users', {
      id: { type: Sequelize.INTEGER, primaryKey: true, autoIncrement: true },
      email: { type: Sequelize.STRING, unique: true, allowNull: false },
      createdAt: Sequelize.DATE,
      updatedAt: Sequelize.DATE
    });
  },
  down: async (queryInterface) => { await queryInterface.dropTable('users'); }
};
// Run: npx sequelize-cli db:migrate | Rollback: npx sequelize-cli db:migrate:undo
```

### TypeORM
```typescript
import { MigrationInterface, QueryRunner, Table } from 'typeorm';
export class CreateUsers1701234567 implements MigrationInterface {
  public async up(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.createTable(new Table({
      name: 'users',
      columns: [
        { name: 'id', type: 'int', isPrimary: true, isGenerated: true, generationStrategy: 'increment' },
        { name: 'email', type: 'varchar', isUnique: true },
        { name: 'created_at', type: 'timestamp', default: 'CURRENT_TIMESTAMP' }
      ]
    }));
  }
  public async down(queryRunner: QueryRunner): Promise<void> { await queryRunner.dropTable('users'); }
}
// Run: npm run typeorm migration:run | Rollback: npm run typeorm migration:revert
```

### Prisma
```prisma
model User {
  id        Int      @id @default(autoincrement())
  email     String   @unique
  createdAt DateTime @default(now())
}
// Generate: npx prisma migrate dev --name create_users | Apply: npx prisma migrate deploy
```

## Zero-Downtime Column Rename (3-step)

```javascript
// Step 1: Add new column, copy data
module.exports = {
  up: async (queryInterface, Sequelize) => {
    await queryInterface.addColumn('users', 'full_name', { type: Sequelize.STRING });
    await queryInterface.sequelize.query('UPDATE users SET full_name = name');
  },
  down: async (queryInterface) => { await queryInterface.removeColumn('users', 'full_name'); }
};
// Step 2: Deploy code using new column
// Step 3: Remove old column
module.exports = {
  up: async (queryInterface) => { await queryInterface.removeColumn('users', 'name'); },
  down: async (queryInterface, Sequelize) => { await queryInterface.addColumn('users', 'name', { type: Sequelize.STRING }); }
};
```

## Transaction-Based Migrations

```javascript
module.exports = {
  up: async (queryInterface, Sequelize) => {
    const transaction = await queryInterface.sequelize.transaction();
    try {
      await queryInterface.addColumn('users', 'verified', { type: Sequelize.BOOLEAN, defaultValue: false }, { transaction });
      await queryInterface.sequelize.query('UPDATE users SET verified = true WHERE email_verified_at IS NOT NULL', { transaction });
      await transaction.commit();
    } catch (error) {
      await transaction.rollback();
      throw error;
    }
  },
  down: async (queryInterface) => { await queryInterface.removeColumn('users', 'verified'); }
};
```

## Blue-Green Deployment Strategy

```javascript
// Phase 1: Add new column (backward compatible)
await queryInterface.addColumn('users', 'email_new', { type: Sequelize.STRING });

// Phase 2: Deploy code that writes to both columns

// Phase 3: Backfill data
await queryInterface.sequelize.query('UPDATE users SET email_new = email WHERE email_new IS NULL');

// Phase 4: Deploy code that reads from new column

// Phase 5: Remove old column
await queryInterface.removeColumn('users', 'email');
```

## Cross-Database Migrations

```javascript
module.exports = {
  up: async (queryInterface, Sequelize) => {
    const dialect = queryInterface.sequelize.getDialect();
    await queryInterface.createTable('users', {
      id: { type: Sequelize.INTEGER, primaryKey: true, autoIncrement: true },
      data: { type: dialect === 'postgres' ? Sequelize.JSONB : Sequelize.JSON }
    });
  }
};
```
