---
name: dist-sys-auditor
description: Distributed systems design and implementation auditor — enforces evidence-backed coordination decisions, citation requirements, invariant tracking, and correctness verification against academic literature, battle-tested systems, and the project's locked architectural decisions
---

# Distributed Systems Auditor

Enforce evidence-backed distributed systems design and implementation for the
gossip-rs project. Every coordination decision **must** trace to established
academic literature, a battle-tested production system, or a formally verified
specification. **No novel protocols. No uncited coordination logic.**

## When to Use

- Proposing or evaluating any distributed systems pattern (leases, fencing,
  sharding, consensus, failure detection, idempotency)
- Writing or modifying code in `gossip-coordination`, or any code touching
  Boundary 2 (Coordination) contracts
- Designing or modifying types/traits in `gossip-contracts` that relate to
  coordination, cursors, shards, epochs, or OpIds
- Discussing failure modes, consistency guarantees, ordering, or CAP trade-offs
- Adding or modifying any state machine that coordinates distributed workers
- Implementing checkpointing, lease renewal, cursor advancement, or shard
  assignment logic

## When NOT to Use

- Pure detection engine work (regex, rule matching) with no coordination aspect
- Connector I/O code that doesn't touch coordination primitives
- Build tooling, CI, or documentation-only changes

---

## Step 0: Load Evidence Base

**On every invocation**, read these files before doing anything else:

1. `tmp/gossip-project-artifacts/distributed-secret-scanner-instructions.md`
   — master instructions with evidence hierarchy, anti-patterns, citation table
2. `tmp/gossip-project-artifacts/gossip-contracts-references.md`
   — curated references organized by boundary

These are the primary evidence sources. Patterns found here are pre-approved.

If the current work touches specific boundary contracts, also read the relevant
boundary draft files in `tmp/gossip-project-artifacts/boundary_*.rs` to check
locked decisions and specified APIs.

---

## Step 1: Detect Mode

**Design Mode** — you are in a brainstorming session, plan mode, writing a
design doc, or discussing architecture without modifying a specific code file.

**Implementation Mode** — you are writing, reviewing, or modifying Rust code
that embodies coordination patterns.

If both apply (designing while coding), use both workflows.

---

## Design Mode Workflow

### 1. Check Locked Decisions

Verify the proposal does not contradict any locked architectural decision:

- **D2.1**: Cursor is two-layer (last_key + token)
- **D2.2**: ShardSpec uses half-open [start, end) ranges
- **D2.3**: Cursor monotonicity is a hard safety invariant
- **D2.4**: Cursor bounds checking is a hard safety invariant
- **D2.5**: Checkpoints require a `last_key` (no regression to None)
- **D3.3**: Lex-ordered byte strings for all key ranges
- **Decision A**: No custom leader election — use consensus backends
- **Decision B**: No gossip protocols — use leases + fencing

If a conflict is found, **BLOCK** and explain the contradiction.

### 2. Check Anti-Patterns

Verify against the 7 explicit prohibitions from Section 9 of the instructions:

1. Do not design novel consensus protocols
2. Do not assume clocks are synchronized
3. Do not conflate "no response" with "failure"
4. Do not use unbounded queues
5. Do not rely on wall-clock timeouts for correctness
6. Do not silently drop scan work
7. Do not assume network reliability

If any anti-pattern is detected, **BLOCK** with the specific prohibition
number and reference.

### 3. Produce Decision Record

Every design decision **must** be presented in this format:

```markdown
## Distributed Systems Decision: [topic]

### Locked Decisions Check
- [x] No conflict with D2.1–D2.5, D3.3, Decision A/B
  (or [ ] Conflicts with [decision] — resolution required)

### Anti-Pattern Check
- [x] No novel consensus protocols
- [x] No clock synchronization assumptions
- [x] No conflating "no response" with "failure"
- [x] No unbounded queues
- [x] No wall-clock timeouts for correctness
- [x] No silent work drops
- [x] No network reliability assumptions

### Decision Record

| Field | Detail |
|-------|--------|
| **Problem** | [what we're deciding] |
| **Approach** | [pattern/technique name] |
| **Provenance** | [Level N] — [citation with URL/paper] |
| **Fit** | [why this matches our constraints] |
| **Trade-offs** | [what we give up] |
| **Safety invariant** | [what must never happen] |
| **Liveness invariant** | [what must eventually happen] |
| **Verification** | [how we test invariants hold] |

### Alternatives Considered

| Alternative | Why Rejected | Reference |
|-------------|-------------|-----------|
| [option] | [reason] | [citation] |

### Open Questions
[anything unresolved, flagged for follow-up]
```

### 4. Citation Requirement (HARD GATE)

The **Provenance** field is mandatory. Use this evidence hierarchy — prefer
higher levels:

| Level | Label | Example |
|-------|-------|---------|
| 5 | Formally verified | TLA+ specs, Coq/Isabelle proofs (IronFleet, Verdi) |
| 4 | Peer-reviewed | SOSP, OSDI, NSDI, EuroSys, VLDB, SIGMOD papers |
| 3 | Battle-tested | FoundationDB, CockroachDB, Kafka, etcd, TigerBeetle |
| 2 | Industry whitepapers | AWS, Google, Meta engineering blogs with depth |
| 1 | Textbooks | DDIA (Kleppmann), Attiya & Welch, Tanenbaum |

If no citation from levels 1–5 exists, the recommendation is **NOVEL** and
must be explicitly flagged:

```
**Provenance**: Level 0 — NOVEL/UNJUSTIFIED
**WARNING**: No established reference found. This pattern requires:
  - Extra review from a second opinion
  - Property-based tests covering all invariants
  - Consider whether an existing proven pattern could substitute
```

### 5. Gap Analysis

If the pattern is not covered by the curated references, do targeted web
research. Search for:
- `"{pattern name}" paper SOSP OSDI VLDB`
- `"{pattern name}" production implementation`
- `"{pattern name}" formal verification TLA+`
- `"{pattern name}" failure mode post-mortem`

When a valuable reference is found, recommend adding it to
`gossip-contracts-references.md`:

```markdown
### Suggested Reference Addition

Add to section: [boundary section name]

| Title | Authors / Source | Year | Why It Matters |
|-------|-----------------|------|----------------|
| [title](URL) | [authors] | [year] | [relevance to our project] |
```

---

## Implementation Mode Workflow

### 1. Identify Coordination Patterns

Scan the code being written or modified for these patterns:

- **Lease logic** — acquire, renew, expire, revoke
- **Epoch/fence checks** — monotonic token validation, stale-write rejection
- **Cursor advancement** — progress tracking, checkpoint writes
- **Shard boundary operations** — range checks, split/merge, key encoding
- **Idempotency** — OpId generation, duplicate detection, payload hash
- **State machine transitions** — coordinator states, worker lifecycle
- **Failure detection** — heartbeat, lease expiry, accrual detection
- **Retry/backpressure** — exponential backoff, circuit breaking, queue bounds

### 2. Emit Inline Audit

For **each** coordination pattern identified, produce:

```markdown
**Pattern: [name]** (file:line_start–line_end)
- **Invariant**: [the safety or liveness property this code upholds]
- **Reference**: [paper/system/post] — [URL or citation from references doc]
- **Violation scenario**: [concrete description of what breaks — e.g.,
  "zombie worker with expired lease commits stale results, overwriting
  valid progress from the new lease holder"]
- **Verification**: [specific test — e.g., "property test: for any sequence
  of checkpoint operations, cursor.last_key is monotonically non-decreasing"]
```

### 3. Monotonicity & Ordering Check

These are **hard safety invariants** (D2.3, D2.4). Explicitly verify:

```markdown
### Monotonicity & Ordering Check
- [ ] Cursor advancement: `new_key >= old_key` enforced
- [ ] Epoch/fence tokens: monotonically increasing, no reuse
- [ ] Shard bounds: half-open [start, end), start < end
- [ ] Checkpoint regression: no regression of last_key to None (D2.5)
```

If any of these cannot be verified from the code, emit a **BLOCK**.

### 4. Flag Unproven Code

Any coordination logic that doesn't map to a known pattern with a citation
gets flagged:

```markdown
### Flags

| Severity | Location | Issue |
|----------|----------|-------|
| BLOCK | file:NN | No citation for [pattern] — NOVEL/UNJUSTIFIED |
| BLOCK | file:NN | Contradicts locked decision [D2.X] |
| BLOCK | file:NN | Anti-pattern violation: [prohibition #N] |
| WARN | file:NN | Evidence level 1-2 only — consider stronger reference |
| WARN | file:NN | Missing verification strategy for [invariant] |
| INFO | file:NN | Stronger test available: [suggestion] |
```

### 5. Missing Coverage Report

Identify coordination patterns in the code that lack corresponding tests or
property-based verification:

```markdown
### Missing Coverage
| Pattern | Invariant | Suggested Verification |
|---------|-----------|----------------------|
| [pattern] | [invariant] | [test type + description] |
```

---

## Severity Levels

- **BLOCK**: Must be resolved before proceeding. No citation for a
  coordination pattern, contradiction with a locked decision, or anti-pattern
  violation.
- **WARN**: Should be addressed. Weak evidence level, missing verification
  strategy, or subtle failure mode risk.
- **INFO**: Improvement opportunity. Stronger test available, additional
  reference found, or pattern could be tightened.

---

## Quick Reference: Locked Decisions

These are non-negotiable. Code must conform:

| ID | Decision | Source |
|----|----------|--------|
| D2.1 | Cursor is two-layer: `last_key` (coordinator-visible) + `token` (connector-opaque) | Spanner query restart (2017) |
| D2.2 | ShardSpec uses half-open `[start, end)` byte ranges | Spanner, Bigtable, FoundationDB |
| D2.3 | Cursor monotonicity: coordinator rejects `new_key < old_key` | Hard safety invariant |
| D2.4 | Cursor bounds: cursor must fall within shard's `[start, end)` | Hard safety invariant |
| D2.5 | Checkpoints require `last_key` — no regression to None | Hard safety invariant |
| D3.3 | Lex-ordered byte strings for all key ranges | Bigtable, FoundationDB, CockroachDB |
| A | No custom leader election — use consensus backends (etcd/Raft, ZK/ZAB) | Ongaro & Ousterhout 2014 |
| B | No gossip protocols — use leases + fencing | Gray & Cheriton 1989 |

## Quick Reference: Anti-Patterns

| # | Prohibition | Reference |
|---|-------------|-----------|
| 1 | No novel consensus protocols | Use Raft via etcd or existing impl |
| 2 | No clock synchronization assumptions | Use logical clocks or HLCs |
| 3 | No conflating "no response" with "failure" | FLP result (Fischer, Lynch, Paterson 1985) |
| 4 | No unbounded queues | Explicit backpressure required |
| 5 | No wall-clock timeouts for correctness | Clocks for liveness only |
| 6 | No silent work drops | Every scan unit reaches terminal state |
| 7 | No network reliability assumptions | Bailis & Kingsbury 2014 |

## Quick Reference: Key Citations

| Concept | Primary Reference |
|---------|-------------------|
| Leases | Gray & Cheriton, SOSP 1989 |
| Fencing tokens | Kleppmann, "How to do distributed locking" (2016) |
| Consensus (Raft) | Ongaro & Ousterhout, USENIX ATC 2014 |
| Range sharding | Corbett et al. (Spanner), OSDI 2012 |
| Cursor restart | Bacon et al. (Spanner), 2017 |
| Idempotency keys | Stripe (Brandur Leach), 2017 |
| Exactly-once | Akidau et al. (Dataflow Model), VLDB 2015 |
| Linearizability | Herlihy & Wing, TOPLAS 1990 |
| Distributed snapshots | Chandy & Lamport, TOCS 1985 |
| Failure detection | Hayashibara et al. (Phi accrual), SRDS 2004 |
| Work stealing | Blumofe & Leiserson, JACM 1999 |
| FLP impossibility | Fischer, Lynch, Paterson, JACM 1985 |
| Sagas | Garcia-Molina & Salem, SIGMOD 1987 |
| WAL / ARIES | Mohan et al., TODS 1992 |
| DST | FoundationDB (Apple, 2021) |
| TLA+ in industry | Newcombe et al., CACM 2015 |
| Causal ordering | Lamport, CACM 1978 |
| HLC | Kulkarni et al., OPODIS 2014 |

## Related Skills

- `/deep-research` — use before this skill when entering entirely new
  territory. Deep-research gathers evidence; dist-sys-auditor enforces it.
- `/interface-design-review` — complementary: checks API ergonomics;
  dist-sys-auditor checks distributed correctness. Run both on coordination APIs.
- `/design-tournament` — use when multiple viable approaches surface.
  Feed tournament results into dist-sys-auditor for citation validation.
- `/test-strategy` — dist-sys-auditor recommends verification strategies;
  test-strategy helps implement them.
- `/security-reviewer` — covers memory safety; dist-sys-auditor covers
  coordination safety (zombie writes, split-brain, lost progress).
- `/doc-rigor` — after dist-sys-auditor approves a pattern, doc-rigor
  ensures documentation captures why the pattern was chosen with its citation.
