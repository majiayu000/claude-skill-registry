---
name: sim-review
description: Simulation-testability code review — enforces DST-compatible patterns in coordination, gossip, and pipeline code based on FoundationDB, TigerBeetle, sled, and Firezone evidence
user-invocable: true
---

# Simulation-Testability Code Review

Enforce that new or modified code maintains **deterministic simulation testing
(DST) compatibility**. Every coordination, gossip, or pipeline operation must be
testable in-process with a seeded PRNG, simulated clock, and no real I/O.

## Evidence Base

This checklist is derived from production-validated DST systems:

| Source | Key Principle |
|--------|---------------|
| **FoundationDB** (SIGMOD 2021) | Abstract IO, replace with simulated impls, control randomness, time as input, single-threaded execution |
| **sled** (simulation.html) | receive/tick pattern, discrete-event sim, priority-queue scheduler |
| **Firezone** (sans-IO blog) | Pure state machine core, effects as return values |
| **Stateright** | Actor trait: `fn on_msg(state, msg) -> Vec<Action>` |
| **TigerBeetle** (VOPR) | Progressive difficulty, time compression |
| **Yuan et al.** (OSDI 2014) | Error handling paths are highest-value test targets |

## When to Use

- After modifying code in `gossip-coordination/`, `gossip-contracts/src/coordination/`,
  or any module touching shard lifecycle, leases, fencing, or gossip protocols
- After adding new trait methods to `CoordinationBackend` or related traits
- After adding new state machine transitions or protocol messages
- Before marking coordination PRs ready for review

## When NOT to Use

- Pure detection engine changes (regex, rule matching) with no coordination aspect
- Connector I/O code that only touches external APIs behind existing trait boundaries
- Documentation-only or CI-only changes
- Identity hashing changes (Boundary 1) unless they affect coordination inputs

---

## Procedure

### Step 1: Identify Changed Code

Determine which files changed and classify each by **boundary**:

| Boundary | Paths | DST Strictness |
|----------|-------|----------------|
| **Coordination core** | `gossip-coordination/src/{traits,in_memory,lease,record,split,cursor,error}.rs` | STRICT — all checklist items apply |
| **Gossip protocol** | `gossip-coordination/src/gossip/` | STRICT — all checklist items apply |
| **Coordination contracts** | `gossip-contracts/src/coordination/` | STRICT — type definitions must support DST |
| **Pipeline** | `gossip-scan-pipeline/src/` | MODERATE — I/O boundaries must be trait-abstracted |
| **Worker** | `gossip-worker/src/` | BOUNDARY — async allowed here, but coordination calls must go through traits |
| **Connectors** | `gossip-connectors/src/` | BOUNDARY — external I/O lives here |

> **Note:** Type A coordination modules (from `/sim-scaffold`) fall under
> the STRICT boundary. Until the coordination crate is implemented, reference
> code lives in `tmp/gossip-project-artifacts/b2_phase2_coordination_final_code/`
> — the paths above are the *target* locations.

If no files fall in STRICT or MODERATE categories, report "No DST-relevant
changes found" and stop.

### Step 2: Run DST Compatibility Checklist

For each changed file in STRICT or MODERATE boundaries, verify **every** item:

```
DST-COMPATIBILITY CHECKLIST
─────────────────────────────
[ ] NO DIRECT CLOCK READS
    std::time::SystemTime, std::time::Instant, tokio::time::*, chrono::*
    are PROHIBITED in coordination/protocol/gossip code.
    → Use LogicalTime passed as explicit parameter (D2.17)

[ ] NO DIRECT I/O
    std::fs::*, std::net::*, tokio::fs::*, tokio::net::*, reqwest::*
    are PROHIBITED outside trait boundaries.
    → All I/O behind trait with in-memory test impl

[ ] LOGICAL TIME AS EXPLICIT INPUT
    Every coordination operation receives LogicalTime as a parameter.
    No function fetches its own notion of "now".
    → fn operation(&mut self, ..., now: LogicalTime) -> Result<...>

[ ] SEEDED RANDOMNESS
    rand::thread_rng(), rand::random(), OsRng are PROHIBITED.
    → Use rand::rngs::StdRng with explicit seed from SimContext
    → Pass &mut impl Rng to functions that need randomness

[ ] SYNCHRONOUS COORDINATION TRAIT METHODS
    New trait methods on CoordinationBackend are synchronous (D2.13).
    → No async fn in coordination traits
    → Async only at the boundary (worker → backend call)

[ ] PURE STATE TRANSITIONS
    State machine transitions are pure functions:
    fn(current_state, input, time) → (new_state, Vec<Effect>)
    → No side effects inside transition logic
    → Effects returned as data, executed by caller
    → Validation ordering: tenant isolation → status check → lease/fence
      check → mutation (security-first, most-actionable-error-first)

[ ] SIDE EFFECTS BEHIND TRAITS
    Every side effect (network send, disk write, timer set) is behind
    a trait boundary with a mock/simulated implementation.
    → #[cfg(feature = "test-support")] impl exists or is planned

[ ] ERROR PATHS TESTED (Yuan et al. OSDI 2014)
    New error enum variants have at least one test exercising them.
    → Check: does every Err(...) path have test coverage?
    → Priority: error paths in lease expiry, fencing, split
    → INFO: Prefer operation-specific error types (AcquireError,
      CheckpointError, etc.) over generic CoordError at public API
      boundaries. Use From<CoordError> with unreachable!() for
      impossible variants (D2.16).

[ ] DETERMINISTIC ITERATION ORDER
    No HashMap/HashSet iteration where order affects correctness.
    → Use BTreeMap/BTreeSet when iteration order matters
    → Or collect into Vec and explicitly .sort() before iterating
      (HashMap + sort is a valid pattern — see reference code split ops)
    → Key question: does any downstream logic depend on iteration order?

[ ] CORRECTNESS PROPERTIES DOCUMENTED
    New coordination operations document their invariants.
    → What must be true before? (preconditions)
    → What must be true after? (postconditions)
    → What must never happen? (safety invariants)

[ ] SANS-IO PROTOCOL PATTERN
    New protocol logic follows the sans-IO pattern:
    → handle_input(&mut self, msg, now) — process incoming message
    → poll_transmit(&mut self) → Option<Transmit> — outbound messages
    → poll_timeout(&self) → Option<LogicalTime> — next timer
    → handle_timeout(&mut self, now) — timer expiry

[ ] INVARIANT ASSERTIONS (Tiger Style, D2.7)
    State types have assert_invariants() called after every mutation.
    → record.assert_invariants() after every state transition
    → Checks: lease consistency, terminal state, fence minimum,
      park_reason consistency, op-log bounded
    → Must be debug_assert! or always-on (Tiger Style preference)
    → Violations must panic, not return errors — they indicate bugs

[ ] IDEMPOTENCY BEFORE VALIDATION
    OpId/payload-hash is checked BEFORE lease/status validation so that
    retries succeed even after the record has transitioned to a terminal
    state (the original result is still in the op-log).
    → check_op_idempotency(record, op_id, payload_hash) is called first
    → If op-log hit: return cached result immediately, skip validation
    → If op-log miss with hash conflict: return OpIdConflict error
    → Only then proceed to validate_lease() and status checks
```

### Step 3: Report Violations

For each violation found, report:

```
VIOLATION: [checklist item name]
  File:    path/to/file.rs:line
  Found:   [what was found — e.g., "std::time::Instant::now()"]
  Fix:     [specific remediation — e.g., "Accept `now: LogicalTime` as parameter"]
  Why:     [one-line explanation of DST impact]
```

Classify severity:

| Severity | Meaning |
|----------|---------|
| **BLOCK** | Breaks simulation determinism — must fix before merge |
| **WARN** | Complicates simulation — should fix, can defer with justification |
| **INFO** | Improvement opportunity — nice to have |

**BLOCK examples:** Direct clock read in coordination code, unsynchronized
HashMap iteration in shard assignment, async fn in CoordinationBackend trait.

**WARN examples:** Missing error path test, undocumented invariant, randomness
without seed propagation.

**INFO examples:** Could extract pure function for better testability, could add
proptest strategy for new type.

### Step 4: Check Invariant Assertions

For files in STRICT boundary:

1. Identify new state transitions or operations
2. Check that each has at least one `debug_assert!` or invariant check
3. Check that the invariant catalog is referenced or extended. Known IDs:
   - **S1** Mutual exclusion (lease), **S2** Fence monotonicity,
     **S3** Terminal irreversibility, **S4** Shard coverage (split),
     **S5** Idempotency (OpId), **S6** Progress (liveness)
   - **L1** Lease exclusivity (stale-epoch rejection),
     **L2** Zombie rejection (restarted worker)
4. Verify that new operations have corresponding proptest strategies (or TODO markers)

### Step 5: Verify Error Coverage

For each new error variant added to `CoordError` or similar enums:

1. Search for test functions that trigger this variant
2. If none exist, flag as WARN with suggested test skeleton
3. Priority: lease expiry, fence rejection, split validation, concurrent access errors

### Step 6: Summary Report

```
SIM-REVIEW REPORT
═════════════════
Files reviewed:    {count}
DST boundary:      {STRICT|MODERATE|BOUNDARY}

Findings:
  BLOCK: {count}
  WARN:  {count}
  INFO:  {count}

{detail for each finding}

Checklist passage rate: {passed}/{total} items
```

---

## Quick Reference: Allowed vs Prohibited Patterns

### Prohibited in STRICT boundary

```rust
// PROHIBITED: Direct clock
let now = std::time::Instant::now();
let now = std::time::SystemTime::now();
let now = tokio::time::Instant::now();

// PROHIBITED: Direct I/O
let data = std::fs::read("file.txt")?;
let stream = tokio::net::TcpStream::connect(addr).await?;

// PROHIBITED: Unseeded randomness
let val = rand::random::<u64>();
let mut rng = rand::thread_rng();

// PROHIBITED: Non-deterministic iteration
let map: HashMap<K, V> = ...;
for (k, v) in &map { /* order is random */ }

// PROHIBITED: Async coordination trait
#[async_trait]
trait CoordinationBackend {
    async fn acquire_shard(&self, ...) -> Result<...>; // NO
}
```

### Allowed

```rust
// OK: Explicit time parameter
fn acquire_shard(&mut self, spec: &ShardSpec, now: LogicalTime) -> Result<ShardRecord> { ... }

// OK: Seeded RNG
fn select_peer(&self, rng: &mut impl Rng) -> NodeId { ... }

// OK: Deterministic iteration (BTreeMap)
let map: BTreeMap<K, V> = ...;
for (k, v) in &map { /* sorted order */ }

// OK: Deterministic iteration (HashMap + explicit sort)
let map: HashMap<K, V> = ...;
let mut entries: Vec<_> = map.iter().collect();
entries.sort_by_key(|(k, _)| k.clone());

// OK: I/O behind trait boundary
trait PersistenceBackend {
    fn write_checkpoint(&self, data: &[u8]) -> Result<()>;
}
// with:
#[cfg(feature = "test-support")]
struct InMemoryPersistence { ... }

// OK: Pure state transition
fn transition(state: ShardStatus, event: ShardEvent, now: LogicalTime)
    -> (ShardStatus, Vec<Effect>) { ... }
```

---

## Related Skills

- `/dist-sys-auditor` — Evidence-backed distributed systems design review
- `/test-strategy` — Assess and recommend testing strategy
- `/sim-scaffold` — Generate DST-ready module scaffolding
- `/sim-run` — Execute simulation tests
