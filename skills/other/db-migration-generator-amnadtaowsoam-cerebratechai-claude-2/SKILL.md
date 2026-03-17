---
name: DB Migration Generator
description: Generator สำหรับสร้าง database migration files พร้อม up/down scripts, validation และ rollback safety
---

# DB Migration Generator

## Overview

สร้าง database migration files อัตโนมัติจาก schema changes พร้อม validation, rollback scripts และ safety checks

## Why This Matters

- **Safety**: Auto-generate rollback scripts
- **Consistency**: Standard migration format
- **Validation**: Check before apply
- **Documentation**: Auto-document changes

---

## Quick Start

```bash
# Generate migration
npx generate-migration add_users_table

# Output:
migrations/
└── 20240116120000_add_users_table.ts
    ├── up()    # Apply migration
    └── down()  # Rollback migration
```

---

## Generated Migration

```typescript
// 20240116120000_add_users_table.ts
export async function up(db: Database) {
  await db.schema.createTable('users', (table) => {
    table.uuid('id').primary();
    table.string('email').unique().notNullable();
    table.string('name').notNullable();
    table.timestamps(true, true);
  });
  
  await db.schema.createIndex('users', 'email');
}

export async function down(db: Database) {
  await db.schema.dropTable('users');
}
```

---

## From Schema Diff

```bash
# Generate from Prisma schema changes
npx generate-migration --from-prisma

# Detects:
- New tables
- New columns
- Index changes
- Constraint changes
```

---

## Safety Checks

```typescript
// Auto-generated safety checks
export async function validate(db: Database) {
  // Check table doesn't exist
  const exists = await db.schema.hasTable('users');
  if (exists) {
    throw new Error('Table users already exists');
  }
  
  // Check dependencies
  // Check data integrity
}
```

---

## Summary

**DB Migration Generator:** สร้าง migrations อัตโนมัติ

**Features:**
- Up/down scripts
- Rollback safety
- Validation
- From schema diff

**Usage:**
```bash
npx generate-migration add_users_table
npm run migrate
```
