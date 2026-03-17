---
name: padz-datastore-persistence
description: Explains the padz hybrid store architecture—files are truth, JSON metadata is a rebuildable cache. Covers self-healing reconciliation (orphans, zombies, staleness), the Backend+Store split for testability, and how to use MemBackend for unit tests. Use when working on storage, persistence, sync, doctor, or writing tests that need store simulation.
---

# Padz Datastore & Persistence

## Design Philosophy

**Files are Truth.** Users trust plain text—future-proof and editable by any tool. If a user deletes a file, the pad is gone. If they create one manually, it's adopted.

**Cache is Rebuildable.** The `data.json` metadata index speeds up listing but can be regenerated from files. Losing it means losing only secondary metadata (pinned state, deletion flags)—never the content.

## Hybrid Store Architecture

```
.padz/
├── data.json           # Metadata cache (rebuildable)
├── config.json         # Scope configuration
└── pad-{uuid}.txt      # Content files (source of truth)
```

### What's Stored Where

| Location | Data | Recoverable? |
|----------|------|--------------|
| `pad-*.txt` | Title + Content | **Source of truth** |
| `data.json` | id, title, created_at, updated_at | Rebuildable from files |
| `data.json` | is_pinned, is_deleted, delete_protected | Lost if cache deleted |

## Self-Healing Reconciliation

The `sync` process runs automatically before `list_pads`. It handles four scenarios:

### 1. Orphan Adoption
**File exists, no DB entry** → Parse file, add to index

```
Cause: User manually created file, or DB corruption
Fix: Extract title from content, create Metadata entry
```

### 2. Zombie Cleanup
**DB entry exists, no file** → Remove from index

```
Cause: User manually deleted file, or interrupted delete operation
Fix: Remove stale Metadata entry
```

### 3. Staleness Check
**File mtime > DB updated_at** → Re-parse content

```
Cause: External edit (vim, another tool)
Fix: Update cached title from file content
```

### 4. Garbage Collection
**Empty/whitespace-only file** → Delete file and DB entry

```
Cause: User emptied file, aborted edit
Fix: Clean up useless files
```

## Write Order: Prefer Orphans over Zombies

When saving:
1. Write content file **first** (atomic)
2. Update index **second**

If crash occurs between steps → Orphan (recoverable content, missing index)
vs. if reversed → Zombie (broken pointer to missing file)

## Backend + Store Split

The architecture separates I/O from business logic:

```
┌──────────────────────────────────────┐
│     PadStore<B: StorageBackend>      │
│  - sync/reconcile logic              │
│  - CRUD operations                   │
│  - implements DataStore trait        │
└─────────────────┬────────────────────┘
                  │ uses
┌─────────────────┴─────────────────┐
│       StorageBackend trait        │
│  (pure I/O, no business logic)    │
└─────────────────┬─────────────────┘
                  │
       ┌──────────┴──────────┐
       │                     │
┌──────▼───────┐    ┌────────▼────────┐
│  FsBackend   │    │   MemBackend    │
│ (filesystem) │    │   (HashMaps)    │
└──────────────┘    └─────────────────┘
```

### StorageBackend Trait

```rust
pub trait StorageBackend {
    // Index operations
    fn load_index(&self, scope: Scope) -> Result<HashMap<Uuid, Metadata>>;
    fn save_index(&self, scope: Scope, index: &HashMap<Uuid, Metadata>) -> Result<()>;

    // Content operations
    fn read_content(&self, id: &Uuid, scope: Scope) -> Result<Option<String>>;
    fn write_content(&self, id: &Uuid, scope: Scope, content: &str) -> Result<()>;
    fn delete_content(&self, id: &Uuid, scope: Scope) -> Result<()>;

    // Discovery (for sync)
    fn list_content_ids(&self, scope: Scope) -> Result<Vec<Uuid>>;
    fn content_mtime(&self, id: &Uuid, scope: Scope) -> Result<Option<DateTime<Utc>>>;

    // Paths & capabilities
    fn content_path(&self, id: &Uuid, scope: Scope) -> Result<PathBuf>;
    fn scope_available(&self, scope: Scope) -> bool;
}
```

### Type Aliases

```rust
type FileStore = PadStore<FsBackend>;     // Production
type InMemoryStore = PadStore<MemBackend>; // Testing
```

## Using MemBackend for Tests

MemBackend fully simulates filesystem behavior without touching disk:

```rust
#[test]
fn test_orphan_recovery() {
    let backend = MemBackend::new();
    let orphan_id = Uuid::new_v4();

    // Simulate orphan: content without index entry
    backend.write_content(&orphan_id, Scope::Project, "Title\n\nBody").unwrap();

    let mut store = PadStore::with_backend(backend);
    let report = store.doctor(Scope::Project).unwrap();

    assert_eq!(report.recovered_files, 1);
}
```

### Test Helpers

```rust
// Simulate write failures
backend.set_simulate_write_error(true);

// Manipulate mtime for staleness tests
backend.set_content_mtime(&id, Scope::Project, future_time);

// Create zombie: index entry without content
let mut index = HashMap::new();
index.insert(zombie_id, metadata);
backend.save_index(Scope::Project, &index).unwrap();
// Don't write content → zombie
```

## Key Locations

| Component | File |
|-----------|------|
| DataStore trait | `crates/padzapp/src/store/mod.rs` |
| StorageBackend trait | `crates/padzapp/src/store/backend.rs` |
| PadStore (business logic) | `crates/padzapp/src/store/pad_store.rs` |
| FsBackend (filesystem) | `crates/padzapp/src/store/fs_backend.rs` |
| MemBackend (testing) | `crates/padzapp/src/store/mem_backend.rs` |

## Developer Guidelines

1. **Never bypass reconciliation** — Always use `list_pads()` or `sync()` before assuming index accuracy
2. **Test with MemBackend** — Full simulation without filesystem overhead
3. **Write content first** — Prefer orphans over zombies on failure
4. **Scopes are isolated** — Project and Global are independent namespaces
5. **Atomic writes in FsBackend** — Uses tmp file + rename pattern
