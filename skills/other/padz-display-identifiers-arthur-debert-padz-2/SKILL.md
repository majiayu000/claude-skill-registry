---
name: padz-display-identifiers
description: Explains the Display Identifier system in padz—a dual-identifier approach that provides stable, user-friendly IDs (1, 2, p1, d1) while internally using UUIDs. Use when working on pad listing, selection, or any CLI command that references pads by ID. Critical for understanding why filtered views preserve canonical indexes.
---

# Padz Display Identifiers

## The Problem

UUIDs are unwieldy for CLI users. Naive sequential indexing (`1, 2, 3...` based on current view) causes "index drift"—the same ID can refer to different pads depending on filters.

```bash
$ padz list
1. Hi Mom
2. Hi Dad

$ padz search Dad
1. Hi Dad     # DANGER: Is "1" global or search-local?
```

## The Solution: Dual Identifiers

1. **UUID (Internal)**: Immutable, used in storage and business logic
2. **Display Index (External)**: Stable integer from canonical ordering

### Canonical Ordering

Indexes are assigned from the **full, unfiltered list**, not the current view:

```bash
$ padz search Dad
2. Hi Dad     # Still ID 2—safe to delete
```

### Index Types

| Type | Format | Assignment |
|------|--------|------------|
| Regular | `1`, `2`, `3` | All non-deleted pads, newest first |
| Pinned | `p1`, `p2` | Pinned non-deleted pads only |
| Deleted | `d1`, `d2` | Soft-deleted pads |

### Pinned Pads Have Two Indexes

A pinned pad appears **twice**: as `pN` and as its regular index. This ensures stability when unpinning—the regular index remains unchanged.

```bash
$ padz list
p1. Important Note    # Also accessible as "2"
1.  Newest Note
2.  Important Note    # Same pad as p1
3.  Oldest Note
```

## Tree Support

Child pads use dot notation. Each level maintains its own index namespace:

```
1          # Root pad
1.1        # First child of pad 1
1.1.1      # First grandchild
1.p1       # Pinned child of pad 1
```

### Ranges

Select multiple pads with range syntax:

```bash
padz delete 1-3        # Delete pads 1, 2, 3
padz delete p1-p3      # Delete pinned 1, 2, 3
padz delete 1.1-1.3    # Delete children 1-3 of pad 1
```

## Implementation

### Generating Indexes (Output)

Location: `crates/padzapp/src/index.rs` — function `index_pads`

Three-pass algorithm:
1. Sort all pads by `created_at` descending
2. First pass: Assign `pN` to pinned non-deleted pads
3. Second pass: Assign `N` to ALL non-deleted pads (including pinned)
4. Third pass: Assign `dN` to deleted pads

**Always use `index_pads`** for listing. Never manually enumerate.

### Resolving Indexes (Input)

Location: `crates/padzapp/src/api.rs` — function `parse_selectors`

Flow: `User Input` → `DisplayIndex` → `UUID`

Business logic (`commands/*`) only receives UUIDs. The fragility of human-friendly IDs is contained at the API boundary.

### Key Types

```rust
enum DisplayIndex {
    Pinned(usize),   // p1, p2...
    Regular(usize),  // 1, 2...
    Deleted(usize),  // d1, d2...
}

enum PadSelector {
    Path(Vec<DisplayIndex>),           // "1.2.3"
    Range(Vec<DisplayIndex>, Vec<DisplayIndex>), // "1-3"
    Title(String),                     // "My Note"
}

struct DisplayPad {
    pad: Pad,
    index: DisplayIndex,
    matches: Option<Vec<SearchMatch>>,
    children: Vec<DisplayPad>,
}
```

## Developer Guidelines

1. **Never bypass `index_pads`** — All pad listings must use canonical indexing
2. **Commands receive UUIDs only** — Keep index resolution at API boundary
3. **Pinned pads are dual-indexed** — Expect two entries per pinned pad in indexed lists
4. **Tree indexes are per-parent** — Each nesting level starts at 1
