---
name: sql-to-osc
description: |
  SQL to OSC (Online Schema Change) conversion expert for Flyway migration scripts.
  Use when: (1) Converting SQL migration files to OSC format, (2) User mentions "OSC", "轉換 OSC", "osc.txt", or "Online Schema Change", (3) Working with Flyway ALTER TABLE/CREATE INDEX statements that need OSC conversion.
---

# SQL to OSC Conversion Expert

Convert Flyway SQL migration scripts to OSC format following project conventions.

## Quick Reference

**OSC Format:** `{database}<TAB>{table}<TAB>{operations};`

| SQL | OSC |
|-----|-----|
| `USE db;` | Remove (db in column 1) |
| `ALTER TABLE tbl` | Remove (tbl in column 2) |
| `NULL` | `DEFAULT NULL` |
| `CREATE INDEX idx ON tbl (col)` | `ADD INDEX idx (col)` |
| `varchar` | `VARCHAR` |
| Multiple operations | Comma-joined, no space |

## Conversion Workflow

1. **Read source SQL** from `src/main/resources/db/migration/`
2. **Parse statements**: Extract database, table, operations
3. **Transform**:
   - Remove `USE` and `ALTER TABLE` wrappers
   - Convert `NULL` → `DEFAULT NULL`
   - Convert `CREATE INDEX...ON table` → `ADD INDEX...`
   - Uppercase data types
4. **Format output**: `{db}\t{table}\t{op1},{op2},...;`
5. **Write to** `src/main/resources/db/osc/osc-{YYYYMMDD}.txt` (e.g., `osc-20251212.txt`)

## Output Requirements

- **Encoding**: UTF-8 (no BOM)
- **Line ending**: LF (`\n`)
- **Separator**: TAB (`\t`) between columns
- **Operations**: Comma (`,`) joined, NO space after comma
- **Line ending**: Semicolon (`;`)

## Example

**Input** (`V1.0__alter_my_table.sql`):
```sql
USE mydb;

ALTER TABLE MY_TABLE
    ADD COLUMN NEW_COL bigint(20) NULL AFTER EXISTING_COL;

CREATE INDEX MY_TABLE_NEW_COL_IDX ON MY_TABLE (NEW_COL);
```

**Output** (`osc-{YYYYMMDD}.txt`):
```
mydb	MY_TABLE	ADD COLUMN NEW_COL BIGINT(20) DEFAULT NULL AFTER EXISTING_COL,ADD INDEX MY_TABLE_NEW_COL_IDX (NEW_COL);
```

## Conversion Summary Template

```
✓ 轉換完成

來源: {source_file}
輸出: src/main/resources/db/osc/osc-{YYYYMMDD}.txt

影響資料表: {tables}
操作統計:
  - ADD COLUMN: {count}
  - ADD INDEX: {count}
  - MODIFY COLUMN: {count}
```
