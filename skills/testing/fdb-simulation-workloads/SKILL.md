---
name: fdb-simulation-workloads
description: Guide for writing FoundationDB simulation workloads in Rust. Use when
  designing chaos testing, simulation testing, deterministic testing, or workload
  implementations for FDB layers. Covers operation design, invariant checking, and
  determinism requirements.
allowed-tools: Read, Grep, Edit, Write
---

# FDB Simulation Workloads

Patterns for designing Rust workloads that find bugs through autonomous chaos testing.

## Determinism Rules (Critical)

Breaking any rule destroys reproducibility. The simulator requires identical seeds to produce identical execution paths.

| Instead of | Use | Why |
|------------|-----|-----|
| `HashMap` / `HashSet` | `BTreeMap` / `BTreeSet` | Iteration order must be deterministic |
| `rand::random()` | `context.rnd()` | Seeded randomness for reproducibility |
| `SystemTime::now()` | `context.now()` | Simulation controls time |
| Manual retry loops | `db.run()` | Proper retry handling with `maybe_committed` |
| `tokio::spawn()` | Never | Simulation uses custom executor |

## Operation Alphabet

Design operations across three categories:

| Category | Purpose | Examples |
|----------|---------|----------|
| **Normal** | Mirror production traffic distribution | 80% reads, 15% writes, 5% complex updates |
| **Adversarial** | Edge cases customers will send | Empty strings, max-length values, null bytes, boundary integers |
| **Nemesis** | Deliberately break things | Delete random data, crash mid-batch, conflict storms, approach 10MB limit |

## Invariant Patterns

Verify correctness continuously during execution, not just at the end.

| Pattern | Description | Example |
|---------|-------------|---------|
| **Reference Model** | In-memory copy of expected state; compare in check phase | `BTreeMap` tracking all expected key-values |
| **Conservation Laws** | Quantities that must remain constant | Total money across accounts unchanged |
| **Structural Integrity** | Data structure validity checks | Index entries point to existing records |
| **Operation Logging** | Log intent in same transaction | Eliminates `maybe_committed` uncertainty |

## Three-Crate Architecture

Separate production frameworks from simulation-testable code:

```
my-project/
├── my-fdb-service/      # Core FDB operations - NO tokio
├── my-grpc-server/      # Production layer (tokio + tonic)
└── my-fdb-workloads/    # Simulation tests
```

The service crate contains pure `db.run()` transaction logic. The server crate wraps it for production. The workloads crate tests actual service code under chaos.

## Common Pitfalls

1. **Initialization on all clients** - Use `if self.client_id == 0` to run setup once
2. **Ignoring `maybe_committed`** - Check the flag in `db.run()` closure for idempotency
3. **Storing database references** - Each phase receives fresh references; don't cache them
4. **Wrapping `FdbError`** - Keep errors unwrapped so retry mechanism detects retryable errors
5. **Assuming setup is failure-free** - FDB knobs randomize; always use `db.run()` with retry logic

## Full Reference

For detailed examples, patterns, and rationale:
https://pierrezemb.fr/posts/writing-rust-fdb-workloads-that-find-bugs/
