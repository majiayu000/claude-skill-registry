---
name: generate-repository
description: Generate repository class for SQLite data access with CRUD methods, row mapping, and TypeScript types. Use when creating new database tables or data access layers.
allowed-tools: Read, Write, Glob, Grep
---

# Generate Repository

Generate a repository class for SQLite data access following the repository pattern.

## Usage

When user requests to create a repository, ask for:

1. **Entity name** (e.g., "WaterLog", "SleepLog", "WeightTracking")
2. **Table name** (snake_case, e.g., "water_logs", "sleep_logs")
3. **Fields** and their types (with database column names)
4. **Which fields are JSON** (arrays, objects, etc.)
5. **Whether to include getByDate() method**

## Implementation Pattern

Based on `src/lib/database/repositories/mealLogRepository.ts` pattern.

### File Structure

Create file: `src/lib/database/repositories/{entityName}Repository.ts`

```typescript
import { getDatabase } from '../connection';
import type { EntityType } from '@/lib/types/health';
import { v4 as uuidv4 } from 'uuid';

export class EntityRepository {
  private db = getDatabase();

  addEntity(data: Omit<EntityType, 'id' | 'createdAt'>): EntityType {
    const id = uuidv4();
    const createdAt = new Date().toISOString();
    const newEntity = { ...data, id, createdAt };

    const stmt = this.db.prepare(`
      INSERT INTO table_name (id, field1, field2, created_at)
      VALUES (?, ?, ?, ?)
    `);

    stmt.run(
      newEntity.id,
      newEntity.field1,
      JSON.stringify(newEntity.field2), // for JSON fields
      newEntity.createdAt
    );

    return newEntity;
  }

  getEntitiesByDate(date: string): EntityType[] {
    const stmt = this.db.prepare('SELECT * FROM table_name WHERE date = ?');
    const rows = stmt.all(date) as any[];

    return rows.map((row) => ({
      id: row.id,
      date: row.date,
      field1: row.field_1, // snake_case → camelCase
      field2: JSON.parse(row.field_2), // JSON fields
      createdAt: row.created_at,
    }));
  }

  getEntityById(id: string): EntityType | null {
    const stmt = this.db.prepare('SELECT * FROM table_name WHERE id = ?');
    const row = stmt.get(id) as any;

    if (!row) return null;

    return {
      id: row.id,
      date: row.date,
      field1: row.field_1,
      field2: JSON.parse(row.field_2),
      createdAt: row.created_at,
    };
  }

  getAllEntities(): EntityType[] {
    const stmt = this.db.prepare('SELECT * FROM table_name');
    const rows = stmt.all() as any[];

    return rows.map((row) => ({
      id: row.id,
      date: row.date,
      field1: row.field_1,
      field2: JSON.parse(row.field_2),
      createdAt: row.created_at,
    }));
  }

  updateEntity(id: string, updates: Partial<EntityType>): void {
    const stmt = this.db.prepare('SELECT * FROM table_name WHERE id = ?');
    const current = stmt.get(id) as any;
    if (!current) throw new Error('Entity not found');

    const updated = {
      ...current,
      ...updates,
      field_2: JSON.stringify(updates.field2 || JSON.parse(current.field_2)),
    };

    const updateStmt = this.db.prepare(`
      UPDATE table_name SET
        field_1 = ?,
        field_2 = ?
      WHERE id = ?
    `);

    updateStmt.run(updated.field_1, updated.field_2, id);
  }

  deleteEntity(id: string): void {
    const stmt = this.db.prepare('DELETE FROM table_name WHERE id = ?');
    stmt.run(id);
  }
}
```

## Key Conventions

- Class name: `{Entity}Repository` (PascalCase)
- Private `db` property via `getDatabase()`
- Use `uuid()` for IDs, ISO strings for timestamps
- Throw errors with descriptive messages (e.g., 'Entity not found')
- Map DB columns (snake_case) to TS props (camelCase)
- JSON fields use `JSON.stringify()` on write, `JSON.parse()` on read
- Date-based queries use `WHERE date = ?` pattern
- Include both getByDate and getById methods when applicable

## Steps

1. Ask user for entity name, table name, fields, and JSON fields
2. Create file: `src/lib/database/repositories/{entityName}Repository.ts`
3. Generate class with private db connection
4. Generate CRUD methods (add, get, update, delete)
5. Add row mapping for snake_case → camelCase conversion
6. Handle JSON fields with JSON.stringify/parse
7. Export class for use in API routes

## Implementation Checklist

- [ ] Repository class properly exported
- [ ] CRUD methods implemented
- [ ] Row mapping handles snake_case to camelCase
- [ ] JSON fields properly serialized
- [ ] Error handling for not found cases
- [ ] Timestamps use ISO format
- [ ] UUIDs generated for new records
