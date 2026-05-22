---
name: database_migration
router_kit: FullStackKit
description: Execute database migrations across ORMs and platforms with zero-downtime strategies, data transformation, and rollback procedures. Use when migrating databases, changing schemas, performing data transformations, or implementing zero-downtime deployment strategies.
metadata:
  skillport:
    category: auto-healed
    tags: [big data, cleaning, csv, data analysis, data engineering, data science, database, database migration, etl pipelines, export, flyway, import, json, liquibase, machine learning basics, migration, nosql, numpy, pandas, python data stack, query optimization, reporting, schema change, schema design, seed data, sql, statistics, transformation, version control, visualization]
---

# Database Migration

Master database schema and data migrations across ORMs (Sequelize, TypeORM, Prisma), including rollback strategies and zero-downtime deployments.

## When to Use This Skill

- Migrating between different ORMs
- Performing schema transformations
- Moving data between databases
- Implementing rollback procedures
- Zero-downtime deployments
- Database version upgrades
- Data model refactoring

## ORM Migrations

### Sequelize Migrations
```javascript
// migrations/20231201-create-users.js
module.exports = {
  up: async (queryInterface, Sequelize) => {
    await queryInterface.createTable('users', {
      id: {
        type: Sequelize.INTEGER,
        primaryKey: true,
        autoIncrement: true
      },
      email: {
        type: Sequelize.STRING,
        unique: true,
        allowNull: false
      },
      createdAt: Sequelize.DATE,
      updatedAt: Sequelize.DATE
    });
  },

  down: async (queryInterface, Sequelize) => {
    await queryInterface.dropTable('users');
  }
};

// Run: npx sequelize-cli db:migrate
// Rollback: npx sequelize-cli db:migrate:undo
```

### TypeORM Migrations
```typescript
// migrations/1701234567-CreateUsers.ts
import { MigrationInterface, QueryRunner, Table } from 'typeorm';

export class CreateUsers1701234567 implements MigrationInterface {
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
            generationStrategy: 'increment'
          },
          {
            name: 'email',
            type: 'varchar',
            isUnique: true
          },
          {
            name: 'created_at',
            type: 'timestamp',
            default: 'CURRENT_TIMESTAMP'
          }
        ]
      })
    );
  }

  public async down(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.dropTable('users');
  }
}

// Run: npm run typeorm migration:run
// Rollback: npm run typeorm migration:revert
```

### Prisma Migrations
```prisma
// schema.prisma
model User {
  id        Int      @id @default(autoincrement())
  email     String   @unique
  createdAt DateTime @default(now())
}

// Generate migration: npx prisma migrate dev --name create_users
// Apply: npx prisma migrate deploy
```

## Schema Transformations

### Adding Columns with Defaults
```javascript
// Safe migration: add column with default
module.exports = {
  up: async (queryInterface, Sequelize) => {
    await queryInterface.addColumn('users', 'status', {
      type: Sequelize.STRING,
      defaultValue: 'active',
      allowNull: false
    });
  },

  down: async (queryInterface) => {
    await queryInterface.removeColumn('users', 'status');
  }
};
```

### Renaming Columns (Zero Downtime)
```javascript
// Step 1: Add new column
module.exports = {
  up: async (queryInterface, Sequelize) => {
    await queryInterface.addColumn('users', 'full_name', {
      type: Sequelize.STRING
    });

    // Copy data from old column
    await queryInterface.sequelize.query(
      'UPDATE users SET full_name = name'
    );
  },

  down: async (queryInterface) => {
    await queryInterface.removeColumn('users', 'full_name');
  }
};

// Step 2: Update application to use new column

// Step 3: Remove old column
module.exports = {
  up: async (queryInterface) => {
    await queryInterface.removeColumn('users', 'name');
  },

  down: async (queryInterface, Sequelize) => {
    await queryInterface.addColumn('users', 'name', {
      type: Sequelize.STRING
    });
  }
};
```

### Changing Column Types
```javascript
module.exports = {
  up: async (queryInterface, Sequelize) => {
    // For large tables, use multi-step approach

    // 1. Add new column
    await queryInterface.addColumn('users', 'age_new', {
      type: Sequelize.INTEGER
    });

    // 2. Copy and transform data
    await queryInterface.sequelize.query(`
      UPDATE users
      SET age_new = CAST(age AS INTEGER)
      WHERE age IS NOT NULL
    `);

    // 3. Drop old column
    await queryInterface.removeColumn('users', 'age');

    // 4. Rename new column
    await queryInterface.renameColumn('users', 'age_new', 'age');
  },

  down: async (queryInterface, Sequelize) => {
    await queryInterface.changeColumn('users', 'age', {
      type: Sequelize.STRING
    });
  }
};
```

## Data Transformations

### Complex Data Migration
```javascript
module.exports = {
  up: async (queryInterface, Sequelize) => {
    // Get all records
    const [users] = await queryInterface.sequelize.query(
      'SELECT id, address_string FROM users'
    );

    // Transform each record
    for (const user of users) {
      const addressParts = user.address_string.split(',');

      await queryInterface.sequelize.query(
        `UPDATE users
         SET street = :street,
             city = :city,
             state = :state
         WHERE id = :id`,
        {
          replacements: {
            id: user.id,
            street: addressParts[0]?.trim(),
            city: addressParts[1]?.trim(),
            state: addressParts[2]?.trim()
          }
        }
      );
    }

    // Drop old column
    await queryInterface.removeColumn('users', 'address_string');
  },

  down: async (queryInterface, Sequelize) => {
    // Reconstruct original column
    await queryInterface.addColumn('users', 'address_string', {
      type: Sequelize.STRING
    });

    await queryInterface.sequelize.query(`
      UPDATE users
      SET address_string = CONCAT(street, ', ', city, ', ', state)
    `);

    await queryInterface.removeColumn('users', 'street');
    await queryInterface.removeColumn('users', 'city');
    await queryInterface.removeColumn('users', 'state');
  }
};
```

## Rollback Strategies

### Transaction-Based Migrations
```javascript
module.exports = {
  up: async (queryInterface, Sequelize) => {
    const transaction = await queryInterface.sequelize.transaction();

    try {
      await queryInterface.addColumn(
        'users',
        'verified',
        { type: Sequelize.BOOLEAN, defaultValue: false },
        { transaction }
      );

      await queryInterface.sequelize.query(
        'UPDATE users SET verified = true WHERE email_verified_at IS NOT NULL',
        { transaction }
      );

      await transaction.commit();
    } catch (error) {
      await transaction.rollback();
      throw error;
    }
  },

  down: async (queryInterface) => {
    await queryInterface.removeColumn('users', 'verified');
  }
};
```

### Checkpoint-Based Rollback
```javascript
module.exports = {
  up: async (queryInterface, Sequelize) => {
    // Create backup table
    await queryInterface.sequelize.query(
      'CREATE TABLE users_backup AS SELECT * FROM users'
    );

    try {
      // Perform migration
      await queryInterface.addColumn('users', 'new_field', {
        type: Sequelize.STRING
      });

      // Verify migration
      const [result] = await queryInterface.sequelize.query(
        "SELECT COUNT(*) as count FROM users WHERE new_field IS NULL"
      );

      if (result[0].count > 0) {
        throw new Error('Migration verification failed');
      }

      // Drop backup
      await queryInterface.dropTable('users_backup');
    } catch (error) {
      // Restore from backup
      await queryInterface.sequelize.query('DROP TABLE users');
      await queryInterface.sequelize.query(
        'CREATE TABLE users AS SELECT * FROM users_backup'
      );
      await queryInterface.dropTable('users_backup');
      throw error;
    }
  }
};
```

## Zero-Downtime Migrations

### Blue-Green Deployment Strategy
```javascript
// Phase 1: Make changes backward compatible
module.exports = {
  up: async (queryInterface, Sequelize) => {
    // Add new column (both old and new code can work)
    await queryInterface.addColumn('users', 'email_new', {
      type: Sequelize.STRING
    });
  }
};

// Phase 2: Deploy code that writes to both columns

// Phase 3: Backfill data
module.exports = {
  up: async (queryInterface) => {
    await queryInterface.sequelize.query(`
      UPDATE users
      SET email_new = email
      WHERE email_new IS NULL
    `);
  }
};

// Phase 4: Deploy code that reads from new column

// Phase 5: Remove old column
module.exports = {
  up: async (queryInterface) => {
    await queryInterface.removeColumn('users', 'email');
  }
};
```

## Cross-Database Migrations

### PostgreSQL to MySQL
```javascript
// Handle differences
module.exports = {
  up: async (queryInterface, Sequelize) => {
    const dialectName = queryInterface.sequelize.getDialect();

    if (dialectName === 'mysql') {
      await queryInterface.createTable('users', {
        id: {
          type: Sequelize.INTEGER,
          primaryKey: true,
          autoIncrement: true
        },
        data: {
          type: Sequelize.JSON  // MySQL JSON type
        }
      });
    } else if (dialectName === 'postgres') {
      await queryInterface.createTable('users', {
        id: {
          type: Sequelize.INTEGER,
          primaryKey: true,
          autoIncrement: true
        },
        data: {
          type: Sequelize.JSONB  // PostgreSQL JSONB type
        }
      });
    }
  }
};
```

## Resources

- **references/orm-switching.md**: ORM migration guides
- **references/schema-migration.md**: Schema transformation patterns
- **references/data-transformation.md**: Data migration scripts
- **references/rollback-strategies.md**: Rollback procedures
- **assets/schema-migration-template.sql**: SQL migration templates
- **assets/data-migration-script.py**: Data migration utilities
- **scripts/test-migration.sh**: Migration testing script

## 🔄 Workflow

> **Kaynak:** [Prisma Migration Guide - Zero Downtime](https://www.prisma.io/dataguide/postgresql/database-migrations) & [Liquibase Best Practices](https://docs.liquibase.com/concepts/best-practices.html)

### Aşama 1: Planning & Backup (Safety First)
- [ ] **Backup**: Migrasyon öncesi tam veritabanı yedeği al veya Point-in-Time Recovery (PITR) ayarlarını kontrol et.
- [ ] **Impact Analysis**: Tablo büyüklüğüne göre migrasyonun ne kadar süreceğini ve kilitlenme (Lock) riskini hesapla.
- [ ] **Rollback Script**: Her `up` betiği için mutlaka çalışan bir `down` betiği hazırla.

### Aşama 2: Expand-Contract Strategy (Zero Downtime)
- [ ] **Expand**: Yeni alanları ekle (Backward compatible). Eski kod hala çalışabilir olmalı.
- [ ] **Backfill**: Verileri eski alandan yeni alana (varsa) arka planda küçük paketler halinde kopyala.
- [ ] **Contract**: Tüm kod yeni alanı kullanmaya başladığında eski alanı veya tabloyu kaldır.

### Aşama 3: Validation & Drift Detection
- [ ] **Verification**: Migrasyon sonrası şema bütünlüğünü doğrula.
- [ ] **Schema Drift**: Dosya bazlı şema ile veritabanındaki gerçek şema arasındaki farkları (Drift) kontrol et.
- [ ] **Automation**: Migrasyonu CI/CD sürecine (Github Actions/Gitlab CI) entegre et.

### Kontrol Noktaları
| Aşama | Doğrulama |
|-------|-----------|
| 1 | Migrasyon sırasında veritabanı kilitlendi mi? (Lock Analysis) |
| 2 | Rollback testi yapıldı mı ve başarılı oldu mu? |
| 3 | Migrasyon logları merkezi sistemde saklanıyor mu? |

---
*Database Migration v1.5 - With Workflow*
