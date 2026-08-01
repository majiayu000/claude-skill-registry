---
name: sql-db-architecture
description: Understand the toy relational database architecture, crate organization,
  data flow, and implementation patterns. Use when exploring the database codebase,
  understanding query execution, debugging stor
---

---
name: sql-db-architecture
description: Understand the toy relational database architecture, crate organization, data flow, and implementation patterns. Use when exploring the database codebase, understanding query execution, debugging storage/indexing, or planning new features. Keywords: sql-database, database, crate, storage, executor, planner, parser, catalog, WAL, buffer pool, index, architecture
---

# sql-database Architecture Expert

Provides deep understanding of the toy relational database implementation, crate boundaries, and system design.

## When to Activate

Use this skill when:
- Exploring how SQL queries flow through the system
- Understanding storage layer (heap files, slotted pages, WAL)
- Debugging parser → planner → executor pipeline
- Working with indexes (B+Tree, Hash, Bitmap, Trie)
- Navigating crate dependencies and boundaries
- Planning new features that span multiple crates

## System Overview

sql-database is a minimal RDBMS in Rust implementing:
- SQL subset: CREATE/DROP TABLE/INDEX, INSERT, SELECT, UPDATE, DELETE
- Storage: slotted pages + buffer pool + WAL (redo-only)
- Execution: Volcano model with SeqScan/IndexScan operators
- Indexes: B+Tree (sled), Hash, Bitmap (roaring), Trie

## Instructions

### 1. Identify the Query

When user asks about functionality, map to crates:

**"How does SELECT work?"**
→ parser → planner → executor → storage/index → buffer

**"Where are tables created?"**
→ catalog (metadata) → storage (heap allocation) → WAL (logging)

**"How are indexes used?"**
→ planner (index selection) → executor (IndexScan) → index crate

### 2. Crate Responsibility Map

Use this mapping to locate relevant code:

| Crate | Responsibility | Key Types |
|-------|---------------|-----------|
| `common` | Shared types, errors | `Row`, `RecordBatch`, `DbError`, `ColumnId` |
| `types` | SQL types & values | `SqlType`, `Value` |
| `expr` | Expression AST + eval | `Expr`, `BinaryOp`, `UnaryOp` |
| `parser` | SQL → AST | sqlparser-rs adapter |
| `planner` | AST → logical → physical | Plan nodes, optimization rules |
| `executor` | Volcano operators | `Exec` trait, SeqScan, Filter, Project |
| `storage` | Heap table, tuples | `HeapTable`, `RecordId`, slotted pages |
| `buffer` | Page cache (LRU) | `Pager`, `PageId`, `TableId` |
| `wal` | Write-ahead log | `WalRecord`, append/replay |
| `catalog` | Schema metadata | `TableMeta`, `IndexMeta`, `TableSchema` |
| `index` | All index types | `Index` trait, BTree/Hash/Bitmap/Trie |
| `repl` | CLI shell | rustyline, tabled rendering |
| `testsupport` | Test fixtures | `run_sql_script`, snapshots |

### 3. Data Flow Patterns

**Query Execution (SELECT):**
```
SQL string
  → parser (sqlparser-rs → AST)
  → planner (logical plan → physical plan with index selection)
  → executor (Volcano operators: Scan → Filter → Project)
    → storage/index (fetch rows via RecordId)
      → buffer (page cache lookup/fetch)
  → REPL (format RecordBatch with tabled)
```

**Write Path (INSERT/UPDATE/DELETE):**
```
SQL string
  → parser → planner → executor
  → WAL (append WalRecord, fsync)
  → storage (heap table modification)
  → index (maintain all indexes on affected columns)
  → buffer (mark pages dirty)
```

**Recovery:**
```
Startup
  → WAL replay (read WalRecord log)
  → storage (re-apply operations)
  → catalog (restore table/index metadata)
```

### 4. Code Navigation Strategy

**Finding implementations:**
- **Trait definitions**: Search crate root (e.g., `executor/lib.rs` for `Exec`)
- **Concrete operators**: Look in `<crate>/src/<operator>.rs`
- **Tests**: Adjacent `.rs` files or `tests/` directory
- **Integration**: `testsupport/` for end-to-end scripts

**Dependency order** (from CLAUDE.md):
```
common ← types ← expr
         ↓
       parser
         ↓
      catalog
         ↓
  buffer ← storage ← wal
         ↓
      planner
         ↓
       index
         ↓
     executor
         ↓
       repl
```

### 5. Key Design Principles

From the design doc:

1. **Tiny interfaces** - Prefer small traits (`Exec`, `Index`, `HeapTable`, `Pager`)
2. **No implicit coercion** - Same-type comparisons only (v1)
3. **WAL-first writes** - (1) append WAL (2) fsync (3) apply to storage
4. **Rule-based planning** - Predicate pushdown + index selection
5. **Single writer** - No transactions/MVCC in v1
6. **Snapshot tests** - Use `insta` for query output verification

### 6. Response Format

When explaining architecture:

**Component Overview:**
- Purpose in 1 sentence
- Key types/traits
- Dependencies (what it calls)
- Dependents (what calls it)

**Code References:**
- Use `crate/path/file.rs:line` format
- Link related components
- Show trait → impl relationships

**Examples:**
- Provide concrete SQL queries
- Show expected output format
- Reference existing tests when available

## Project Context

- **Language**: Rust (workspace with 13 crates)
- **Build**: `cargo check/test/fmt/clippy`
- **Coverage**: `scripts/coverage.sh` (llvm-cov)
- **Testing**: Unit tests inline, integration in `tests/`, snapshots with `insta`
- **Dependencies**: Pinned in workspace `Cargo.toml` with `workspace = true`

## Common Questions

**"How does index selection work?"**
→ Check `planner/` for rules matching `WHERE` predicates to available indexes

**"Where is Row serialized?"**
→ `storage/` uses `bincode` for tuple layout in slotted pages

**"How does the buffer pool work?"**
→ `buffer/` implements LRU cache over `PageId`, backed by file segments

**"What SQL is supported?"**
→ See SKILL.md header or `parser/` for DDL/DML subset

**"How to add a new operator?"**
→ Implement `Exec` trait in `executor/`, wire into planner physical node generation

## Tool Usage

- **Grep**: Find trait implementations, error types, specific SQL keywords
- **Read**: Examine crate root `lib.rs`, trait definitions, test fixtures
- **Glob**: Locate all operators (`executor/**/*.rs`), test files (`**/tests/*.rs`)

---

For detailed API signatures and implementation notes, see REFERENCE.md.
