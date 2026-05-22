---
name: Testing Fundamentals
description: |
  This skill covers testing ZX games for determinism and correctness. Use when the user asks about "sync testing", "replay testing", "determinism", "desync", "checksums", "test my game", or "verify determinism".

  **Load references when:**
  - Determinism patterns → `references/determinism-rules.md`
version: 1.0.0
---

# Testing Fundamentals for Nethercore ZX

## Sync Testing

Runs two identical instances, compares checksums each frame.

```bash
nether run --sync-test
nether run --sync-test --frames 3000  # Specific duration
```

**Pass criteria:** Identical checksums for 1000+ frames.

## Replay Testing

Record and replay for regression testing:

```bash
nether run --record replay.bin  # Record
nether run --replay replay.bin  # Playback
```

**Workflow:**
1. Record on known-good build
2. Replay on new build
3. Compare outcomes

## Determinism Rules

| Do | Don't |
|---|---|
| `zx::random()` | `rand::thread_rng()` |
| `BTreeMap`, `BTreeSet` | `HashMap`, `HashSet` |
| Frame counter | `Instant::now()` |
| Fixed-point math | Floating-point accumulation |

## Test Organization

| Type | Tool | Purpose |
|------|------|---------|
| Unit | `cargo test` | Pure logic |
| Sync | `nether run --sync-test` | Runtime determinism |
| Replay | `--record`/`--replay` | Cross-build validation |

## Common Desync Causes

- Non-deterministic RNG
- HashMap iteration order
- System time reads
- Uninitialized memory
