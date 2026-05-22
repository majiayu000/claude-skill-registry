---
name: spacetimedb-reference
description: SpacetimeDB multiplayer development patterns, schema changes, subscriptions, and performance optimization
allowed-tools:
  - WebFetch(domain:spacetimedb.com)
  - Read
  - Grep
  - Glob
---

# SpacetimeDB Reference Guide

Comprehensive guide for developing multiplayer features with SpacetimeDB. This skill provides patterns, best practices, and performance optimization strategies for Sunaba's multiplayer implementation.

## 1. Quick Reference

### Essential Commands

```bash
# Schema development workflow
just spacetime-build      # Build WASM + auto-generate clients
just test                 # Validate all changes (fmt, clippy, tests, clients)

# Server management
just spacetime-check      # Check if server is running
just spacetime-start      # Start server (auto-checks if running)
just spacetime-stop       # Stop local server
just spacetime-publish    # Publish module to local server
just spacetime-logs-tail  # Follow server logs
just spacetime-reset      # Delete database and republish (fixes degraded server)

# Client connection modes (runtime switchable!)
just start                    # Start in singleplayer (default)
just join                     # Connect to localhost:3000 on startup
just join-prod                # Connect to sunaba.app42.blue on startup
cargo run --features multiplayer_native -- --server <url>  # Custom server
```

### Schema Change Quick Commands

| Command                         | Purpose                                              |
|---------------------------------|------------------------------------------------------|
| `just spacetime-build`          | Build WASM server module                             |
| `just spacetime-generate-rust`  | Regenerate Rust client from server                   |
| `just spacetime-generate-ts`    | Regenerate TypeScript client from server             |
| `just spacetime-verify-clients` | Verify Rust client matches server schema             |
| `just spacetime-verify-ts`      | Verify TypeScript client is regenerated              |
| `just test`                     | Full validation (includes both client verifications) |

## 2. Architecture Overview

### Runtime Connection Management

**Default Mode:** Singleplayer - Game starts disconnected, multiplayer is opt-in

**Connection Methods:**
1. **CLI Argument:** `--server <url>` connects on startup
2. **In-Game UI:** Press `M` key → Multiplayer panel → Select server → Connect
3. **Justfile Shortcuts:** `just join` or `just join-prod`

**Connection Flow:**
- **Singleplayer → Multiplayer:** Saves singleplayer world, switches to server-authoritative mode
- **Multiplayer → Singleplayer:** Restores singleplayer world from snapshot
- **Reconnection:** Automatic with exponential backoff (1s, 2s, 4s, 8s, max 30s)
- **Error Handling:** User-friendly messages with retry option

**UI States:** Disconnected (server selection) | Connecting | Connected (stats) | Reconnecting | Error

### Client Architecture (Dual SDK Approach)

| Platform   | SDK            | Implementation                                          | Status               |
|------------|----------------|---------------------------------------------------------|----------------------|
| **Native** | Rust SDK       | `crates/sunaba/src/multiplayer/client.rs`               | ✅ Runtime switchable |
| **WASM**   | TypeScript SDK | `web/js/spacetime_bridge.js` → `window.spacetimeClient` | ✅ Runtime switchable |

**Feature flags:**
- `multiplayer` - Parent feature enabling all multiplayer code
- `multiplayer_native` - Native Rust SDK (depends on `multiplayer`)
- `multiplayer_wasm` - WASM TypeScript SDK (depends on `multiplayer`)
- When `multiplayer` disabled: singleplayer-only build, no server dependencies
- When `multiplayer` enabled: runtime-switchable between singleplayer/multiplayer

### Server Architecture

**Feature Gating:** Server builds **without** `evolution` and `regeneration` features, eliminating most `rand` dependencies. SpacetimeDB provides deterministic RNG via `ctx.rng()`.

**What runs server-side:**
- ✅ CA simulation (falling sand, fire, reactions) using `ctx.rng()`
- ✅ Creature AI (neural network inference only)
- ✅ WorldRng trait abstraction (works with both `thread_rng()` and `ctx.rng()`)
- ❌ Evolution/training (offline only)
- ❌ Regeneration system (offline only)

**Key tables:** `world_config`, `chunk_data`, `player`, `creature_data`, tick timers

## 3. Rand Compatibility

**IMPORTANT:** Always use **rand 0.8** and **stable APIs** to avoid version conflicts:

```rust
use rand::{Rng, thread_rng};  // Always import Rng trait

let mut rng = thread_rng();   // Not rand::rng() (nightly only)
rng.gen_range(0..10);         // Not .random_range() (rand 0.9)
rng.r#gen::<f32>();           // Use r#gen in Rust 2024 ('gen' is keyword)
```

**WorldRng abstraction** (in `sunaba-core/src/world/world.rs`) allows World to work with any RNG source:
```rust
pub trait WorldRng {
    fn gen_bool(&mut self) -> bool;
    fn gen_f32(&mut self) -> f32;
    fn check_probability(&mut self, probability: f32) -> bool;
}
impl<T: ?Sized + rand::Rng> WorldRng for T { ... }  // Blanket impl
```

This supports `thread_rng()` (client), `ctx.rng()` (server), and `DeterministicRng` (genome→brain init).

## 4. Schema Development Workflow

**CRITICAL:** When modifying the SpacetimeDB server schema, follow this checklist to prevent breaking clients.

### Schema Change Checklist

When you modify `crates/sunaba-server/src/` (add/remove/modify tables in tables.rs or reducers in reducers/):

1. **Build server module (auto-generates clients):**
   ```bash
   just spacetime-build
   ```
   - Builds WASM module from `crates/sunaba-server/`
   - Auto-generates Rust client → `crates/sunaba/src/multiplayer/generated/` (gitignored)
   - Auto-generates TypeScript client → `web/src/spacetime/` (gitignored)
   - Clients are type-safe and fully auto-generated from schema

2. **Validate all changes:**
   ```bash
   just test
   ```
   - Runs fmt, clippy, workspace tests
   - Rebuilds release binary with multiplayer features
   - Rebuilds WASM web build
   - Regenerates and verifies both Rust and TypeScript clients
   - Type-checks TypeScript with `tsc --noEmit`

3. **Test locally with server:**
   ```bash
   # Check if server is already running (optional but recommended)
   just spacetime-check

   # Start server if not running (auto-checks, won't conflict)
   just spacetime-start

   # Publish module to local server
   just spacetime-publish

   # Test both native and WASM builds
   cargo run --features multiplayer_native -- --server http://localhost:3000
   just web  # Then test in browser
   ```

   **Troubleshooting:**
   - **If `spacetime-publish` fails:** Server may have stale state or performance degradation. Run `just spacetime-reset` to delete the database and republish fresh.
   - **If server becomes slow:** SpacetimeDB server can degrade over time if automated processes accumulate state. Solution: `just spacetime-stop && just spacetime-start && just spacetime-publish`
   - **If changes not reflected:** Ensure clients were regenerated by checking timestamps on generated files, or manually run `just spacetime-build` again.

### Common Pitfalls

❌ **DON'T:** Edit generated files (they're gitignored and auto-regenerated)
❌ **DON'T:** Commit generated client code (`generated/` and `src/spacetime/` are gitignored)
❌ **DON'T:** Forget to run `just spacetime-build` after modifying server schema
❌ **DON'T:** Manually run `spacetime-generate-rust` or `spacetime-generate-ts` (use `just spacetime-build` instead)
❌ **DON'T:** Keep running a degraded server (run `just spacetime-reset` if publish fails)
✅ **DO:** Run `just test` after schema changes (auto-regenerates clients)
✅ **DO:** Use `just spacetime-check` before starting server to avoid conflicts
✅ **DO:** Run `just spacetime-reset` when server performance degrades
✅ **DO:** Keep reducer signatures simple (avoid complex types)
✅ **DO:** Test both native and WASM builds after schema changes
✅ **DO:** Let generated clients handle all type safety automatically

### Troubleshooting

#### Server Performance Degradation

SpacetimeDB servers can accumulate state from automated processes (ticks, metrics, etc.) causing slowdowns over time.

**Symptoms:**
- `spacetime-publish` fails or times out
- Server becomes unresponsive
- Long delays in reducer execution
- Increasing memory usage over time

**Solution:**
```bash
just spacetime-reset  # Deletes database and republishes fresh
```

This command:
1. Deletes the existing database (including all accumulated state)
2. Republishes the module with a clean slate
3. Resets all timers, metrics, and accumulated data

**For production servers:**
```bash
just spacetime-reset-prod  # USE WITH CAUTION - deletes production data
```

**Prevention:**
- Implement scheduled reducers to clean up old metrics/logs
- Use bounded data structures for accumulating state
- Monitor memory usage and database size
- Set retention policies for time-series data

#### Server Conflicts

If `spacetime-start` hangs or fails:

**Check server status first:**
```bash
just spacetime-check
```

**If running but not responsive, restart:**
```bash
just spacetime-stop
just spacetime-start
```

**If start fails with "address already in use":**
- Another SpacetimeDB instance is already running
- Use `just spacetime-check` to verify
- Either use the existing instance or stop it first with `just spacetime-stop`

**If changes not reflected after publish:**
1. Verify clients were regenerated: `just spacetime-build`
2. Check server logs: `just spacetime-logs-tail`
3. Try a clean restart: `just spacetime-stop && just spacetime-start && just spacetime-publish`
4. If still not working: `just spacetime-reset`

## 5. Subscription Best Practices

**CRITICAL:** SpacetimeDB subscriptions have specific SQL limitations and performance characteristics that require careful query design.

### SQL Limitations

SpacetimeDB's SQL WHERE clauses have limited functionality:

- ❌ **No subqueries**: Cannot use `WHERE x = (SELECT chunk_x FROM player ...)`
- ❌ **No arithmetic in WHERE**: Cannot use `ABS(x - player.x) <= 10`
- ❌ **No functions in WHERE**: Cannot use `ABS()`, `SQRT()`, `POW()`, etc.
- ✅ **Use BETWEEN for ranges**: `WHERE x BETWEEN -10 AND 10 AND y BETWEEN -10 AND 10`
- ✅ **Basic comparisons only**: `=`, `<`, `>`, `<=`, `>=`, `!=`, `<>`

**Example:**
```rust
// ❌ WRONG - Uses ABS() function
subscribe("SELECT * FROM chunk_data WHERE ABS(x) <= 10 AND ABS(y) <= 10");

// ✅ CORRECT - Uses BETWEEN
subscribe("SELECT * FROM chunk_data WHERE x BETWEEN -10 AND 10 AND y BETWEEN -10 AND 10");

// ❌ WRONG - No subqueries or arithmetic
subscribe("SELECT * FROM chunk_data WHERE x = (SELECT chunk_x FROM player WHERE id = me)");

// ✅ CORRECT - Client-side filtering or re-subscription
let center = get_player_chunk_pos();
subscribe(&format!(
    "SELECT * FROM chunk_data WHERE x BETWEEN {} AND {} AND y BETWEEN {} AND {}",
    center.x - 10, center.x + 10, center.y - 10, center.y + 10
));
```

### Subscription Management

**Zero-copy subscriptions:** Same query subscribed multiple times has no overhead (SpacetimeDB deduplicates internally). This is a critical optimization for multiplayer games where multiple systems might query the same data.

**Overlapping queries have overhead:** Different queries with overlapping data cause server to process/serialize rows multiple times.

**Update pattern:** Always unsubscribe → subscribe to minimize overlap

```rust
// ✅ CORRECT - Minimize overlap by unsubscribing first
if let Some(old_sub) = self.chunk_subscription.take() {
    old_sub.unsubscribe();  // Unsubscribe first
}
let new_sub = conn.subscribe("SELECT * FROM ..."); // Then subscribe
self.chunk_subscription = Some(new_sub);

// ❌ WRONG - Subscribe before unsubscribe causes overlap
let new_sub = conn.subscribe("SELECT * FROM ...");
if let Some(old_sub) = self.chunk_subscription.take() {
    old_sub.unsubscribe();  // Too late - overlap already happened
}
```

**Brief gaps are OK:** Chunks remain in client world during re-subscription, only subscription cache updates.

**Group by lifetime:** Organize subscriptions by how long they'll remain active. Keep permanent data subscriptions separate from dynamic ones to avoid unnecessary resubscription overhead.

**Bundle updates:** Updates across overlapping subscriptions consolidate into a single TransactionUpdate message rather than generating separate messages per subscription, improving network efficiency.

### Dynamic Filtering Workarounds

Since SpacetimeDB doesn't support dynamic WHERE clauses based on other table values:

1. **Client-side filtering**: Subscribe to large area, filter progressively on client
2. **Re-subscription**: Periodically re-subscribe with new center when player moves
3. **Rate limiting**: Control sync rate to avoid frame drops (2-3 items per frame)

**Example progressive loading pattern:**
```rust
// 1. Initial subscription: small radius for fast spawn
subscribe("SELECT * FROM chunk_data WHERE x BETWEEN -3 AND 3 AND y BETWEEN -3 AND 3");

// 2. After spawn loads: expand to larger radius
unsubscribe_old();
subscribe("SELECT * FROM chunk_data WHERE x BETWEEN -10 AND 10 AND y BETWEEN -10 AND 10");

// 3. When player moves >8 chunks: re-subscribe with new center
let new_center = player_chunk_pos;
subscribe(&format!(
    "SELECT * FROM chunk_data WHERE x BETWEEN {} AND {} AND y BETWEEN {} AND {}",
    new_center.x - 10, new_center.x + 10,
    new_center.y - 10, new_center.y + 10
));
```

### Performance Tips

- **Start small**: Begin with small subscription for fast initial load (e.g., 3-chunk radius = 49 chunks)
- **Expand progressively**: Expand to larger subscription after critical data loaded (e.g., 10-chunk radius = 441 chunks)
- **Re-subscribe on movement**: Re-subscribe when player moves far from subscription center (>8 chunks for 10-radius subscription)
- **Use eviction**: Keep memory usage bounded by unloading distant chunks
- **Rate-limit client sync**: Process 2-3 chunks per frame to avoid frame drops

**Example implementation:**
```rust
// Fast initial load: 49 chunks (7x7 grid) loads in <1 second
subscribe("WHERE x BETWEEN -3 AND 3 AND y BETWEEN -3 AND 3");

// Progressive expansion: Stream remaining 392 chunks in background
// Use spiral iterator + ChunkLoadQueue for rate-limited loading

// Dynamic re-subscription: Update center as player explores
if player_moved_far {
    resubscribe_chunks(new_center, radius);  // Unsubscribe → subscribe pattern
}

// Memory management: Evict chunks >10 from player
world.evict_distant_chunks(player_pos);
```

## 6. Performance Optimization

### Indexing Strategies

SpacetimeDB supports B-Tree indexes on single or multiple columns for efficient querying.

**When to define indexes:**
- Columns used frequently in WHERE clauses
- Foreign key columns for joins
- Fields used for sorting or range queries

**How to define indexes:**
```rust
// Rust: Single-column index
#[index(btree)]
pub chunk_x: i32,

// Multi-column index (supports prefix matching)
#[index(btree, name = "position_idx")]
pub chunk_x: i32,
#[index(btree, name = "position_idx")]
pub chunk_y: i32,
```

**Multi-column index optimization:**
- Index on `(chunk_x, chunk_y)` supports efficient queries on:
  - Both fields: `WHERE chunk_x = 5 AND chunk_y = 10`
  - First field only: `WHERE chunk_x = 5`
  - Range queries: `WHERE chunk_x BETWEEN 0 AND 10 AND chunk_y = 5`

**Best practices:**
- Index only frequently-queried columns (indexes have storage/write overhead)
- Use multi-column indexes for common query patterns
- Avoid over-indexing (slows inserts/updates)

### Query Optimization

**Prefer indexed lookups over full table scans:**
```rust
// ❌ WRONG - Full table scan
let chunk = ChunkData::iter().find(|c| c.chunk_x == x && c.chunk_y == y);

// ✅ CORRECT - Use indexed filter
let chunk = ChunkData::filter_by_chunk_x(&x)
    .find(|c| c.chunk_y == y);

// ✅ BEST - Use multi-column index if available
let chunk = ChunkData::filter_by_position_idx(&x, &y).next();
```

**Batch operations within reducers:**
```rust
// ❌ WRONG - Multiple client calls
for chunk in chunks {
    client.call_reducer("update_chunk", chunk);  // N network round trips
}

// ✅ CORRECT - Single reducer with batch operation
#[spacetimedb::reducer]
pub fn update_chunks(ctx: &ReducerContext, chunks: Vec<ChunkUpdate>) {
    for chunk in chunks {
        ChunkData::update_by_position(&ctx, chunk.x, chunk.y, chunk.data);
    }
}
client.call_reducer("update_chunks", chunks);  // 1 network round trip
```

### Table Design

**Right-size data types:**
```rust
// ❌ WRONG - Oversized types waste memory/bandwidth
pub chunk_x: i64,  // -9 quintillion to +9 quintillion (overkill for chunks)
pub material_id: u32,  // 4 billion materials (we have ~50)

// ✅ CORRECT - Use smallest type that fits data range
pub chunk_x: i32,  // -2 billion to +2 billion (plenty for world coords)
pub material_id: u8,  // 0-255 (enough for 255 materials)
```

**Split monolithic tables:**
```rust
// ❌ WRONG - One large player table with rarely-accessed data
#[table(name = player)]
pub struct Player {
    pub id: u64,
    pub x: f32, pub y: f32,  // Updated every frame
    pub inventory: Vec<Item>,  // Updated occasionally
    pub stats: PlayerStats,  // Updated rarely
    pub achievements: Vec<Achievement>,  // Updated very rarely
}

// ✅ CORRECT - Split by access frequency
#[table(name = player_position)]
pub struct PlayerPosition { pub id: u64, pub x: f32, pub y: f32 }

#[table(name = player_inventory)]
pub struct PlayerInventory { pub player_id: u64, pub items: Vec<Item> }

#[table(name = player_stats)]
pub struct PlayerStats { pub player_id: u64, pub stats: Stats }
```

**Control table visibility:**
```rust
// Internal-only tables (not synced to clients)
#[table(name = server_metrics, public = false)]
pub struct ServerMetrics { ... }

// Client-visible tables (synced via subscriptions)
#[table(name = chunk_data, public = true)]
pub struct ChunkData { ... }
```

**Manage table growth:**
```rust
// Cleanup old data periodically
#[scheduled_reducer(10m)]  // Every 10 minutes
pub fn cleanup_old_metrics(ctx: &ReducerContext) {
    let cutoff = ctx.timestamp - Duration::from_secs(3600);  // Keep 1 hour
    ServerMetrics::delete_by_timestamp_before(&ctx, cutoff);
}
```

## 7. Advanced Topics

### Subscription Semantics

**Two-channel WebSocket architecture:**
- Client-to-server: Requests (subscribe, call reducer, etc.)
- Server-to-client: Responses and updates
- **Guarantee:** Responses are always sent in the same order requests were received

**Four-step subscription workflow:**
1. Client sends Subscribe message with SQL query
2. Host captures committed database snapshot
3. Host evaluates query against snapshot, finds matching rows
4. Host sends SubscribeApplied response with all initial matches
5. Client SDK atomically locks cache, inserts rows, invokes callbacks

**Atomic cache updates:**
- Client cache is locked during TransactionUpdate processing
- All insertions/deletions complete before callbacks execute
- Callbacks never observe inconsistent intermediate states
- Cache reads are "effectively free" (local access)

### State Synchronization Guarantees

**Transaction atomicity:**
- Each database transaction generates exactly zero or one update message
- Updates reflect committed operations in order
- Clients receive exactly one response with all initially matching rows from a consistent snapshot

**Cache consistency:**
- Client cache always maintains a consistent and correct subset of committed database state
- Callbacks receive visibility into fully updated cache content
- No torn reads or partial updates visible to application code

**Callback execution:**
- SDK queues callbacks during TransactionUpdate processing
- Callbacks deferred until all insertions/deletions complete
- Prioritizes consistency over raw latency

### Transaction Handling

**Update ordering:**
- Responses to client requests sent in request order
- Transaction updates delivered in commit order
- No message reordering within a single WebSocket connection

**Update batching:**
- Multiple overlapping subscriptions bundle updates into single TransactionUpdate
- Reduces message overhead and network bandwidth
- Client processes all updates atomically before callbacks

## 8. Common Pitfalls

### Schema & Code Generation
- ❌ Editing generated client files (they're gitignored and auto-regenerated)
- ❌ Committing generated code to git
- ❌ Forgetting `just spacetime-build` after schema changes
- ❌ Skipping `just test` validation after schema changes

### Subscriptions
- ❌ Using SQL functions in WHERE clauses (`ABS()`, `SQRT()`, etc.)
- ❌ Overlapping subscriptions with different queries (causes duplicate serialization)
- ❌ Subscribing before unsubscribing (creates temporary overlap)
- ❌ Large initial subscription causing slow spawn times

### Queries & Performance
- ❌ Full table scans with `.iter().find()` instead of indexed filters
- ❌ Multiple client calls instead of batched reducer operations
- ❌ Oversized data types (u64 when u8 suffices)
- ❌ Monolithic tables mixing high-frequency and low-frequency data

### Table Design
- ❌ Making internal tables public unnecessarily (wastes client sync overhead)
- ❌ No cleanup for unbounded tables (metrics, logs, etc.)
- ❌ Missing indexes on frequently-queried columns
- ❌ Over-indexing (slows writes without query benefit)

## References

- [SpacetimeDB Official Docs](https://spacetimedb.com/docs)
- [Subscriptions Guide](https://spacetimedb.com/docs/subscriptions)
- [Subscription Semantics](https://spacetimedb.com/docs/subscriptions/semantics)
- [Index Documentation](https://spacetimedb.com/docs/tables/indexes)
- [Performance Best Practices](https://spacetimedb.com/docs/tables/performance)
- Sunaba server implementation: `crates/sunaba-server/src/`
- Sunaba Rust client: `crates/sunaba/src/multiplayer/client.rs`
- Sunaba TypeScript client: `web/js/spacetime_bridge.js`