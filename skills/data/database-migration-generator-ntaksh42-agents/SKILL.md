---
name: database-migration-generator
description: Generate database migration scripts with rollback support for various databases. Use when creating schema migrations or database changes.
---

# Database Migration Generator Skill

データベースマイグレーションスクリプトを生成するスキルです。

## 主な機能

- **テーブル作成**: CREATE TABLE
- **カラム追加/削除**: ALTER TABLE
- **インデックス**: CREATE INDEX
- **外部キー**: FOREIGN KEY制約
- **ロールバック**: DOWN migration

## 生成例

```sql
-- migrations/001_create_users.up.sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);

-- migrations/001_create_users.down.sql
DROP TABLE IF EXISTS users;
```

## TypeORM (TypeScript)

```typescript
import { MigrationInterface, QueryRunner, Table } from 'typeorm';

export class CreateUsers1234567890 implements MigrationInterface {
    async up(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.createTable(new Table({
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
                }
            ]
        }));
    }

    async down(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.dropTable('users');
    }
}
```

## バージョン情報
- Version: 1.0.0
