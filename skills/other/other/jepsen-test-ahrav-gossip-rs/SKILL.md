---
name: jepsen-test
description: Run Jepsen-style cluster tests using Maelstrom (lightweight) or full Jepsen (heavyweight) — validates correctness of the deployed gossip-rs system with real network behavior, complementing in-process DST
user-invocable: true
---

# Run Jepsen-Style Cluster Tests

Validate correctness of the **deployed gossip-rs system** using real network
behavior. This complements in-process deterministic simulation testing (DST)
by testing the actual binary with real (or simulated-real) networking.

## Evidence Base

| Source | Principle |
|--------|-----------|
| **Jepsen** (jepsen.io) | Found bugs in 30+ production databases; linearizability checking |
| **Maelstrom** (jepsen-io/maelstrom) | Lightweight Jepsen for protocol testing via stdin/stdout JSON |
| **CockroachDB** (Jepsen lessons blog) | Automated Jepsen is inherently flaky — design workloads carefully |
| **Yuan et al.** (OSDI 2014) | 3 nodes suffice for reproducing most distributed failures |
| **Jepsen etcd 3.4.3** | Lease/fence failures directly relevant to gossip-rs coordination |
| **Jepsen Redis-Raft** | Ambiguous failure pattern (succeed but report failure) |

**Key insight:** DST and Jepsen are **complementary**, not competing. DST
explores the state space exhaustively in-process with a simulated network.
Jepsen validates the real deployed system with real networking and OS behavior.

## When to Use

- After implementing a gossip protocol and wanting to verify convergence
- Before releases to validate coordination correctness under real conditions
- When DST passes but you suspect real networking reveals different bugs
- When testing integration between components (not just protocol logic)

## When NOT to Use

- When the gossip protocol doesn't exist yet (use `/sim-scaffold` first)
- For testing pure state machine logic (use `/sim-run` instead — faster, deterministic)
- For testing detection engine correctness (no distributed aspect)

---

## Two Modes

### Mode A: Maelstrom (Lightweight, Development-Time)

Tests the gossip protocol **in isolation** using Maelstrom's simulated network.
Fast iteration, no infrastructure needed.

### Mode B: Full Jepsen (Heavyweight, Pre-Release)

Tests the **full deployed system** with real SSH, real binaries, real network
partitions. Thorough but slow and potentially flaky.

**Default to Mode A** unless the user specifically requests Mode B or the
change involves integration between multiple deployed components.

---

## Mode A: Maelstrom

### Prerequisites

1. Maelstrom binary installed (`brew install maelstrom` or from jepsen-io/maelstrom releases)
2. A Maelstrom-compatible binary wrapper exists at `crates/gossip-worker/src/bin/maelstrom_gossip.rs`
3. The gossip protocol implements the sans-IO pattern (from `/sim-scaffold` Type B)

If the Maelstrom binary wrapper doesn't exist, guide creation:

```rust
// crates/gossip-worker/src/bin/maelstrom_gossip.rs
//
// Thin wrapper that adapts the sans-IO GossipProtocol to Maelstrom's
// JSON stdin/stdout protocol.
//
// Reads Maelstrom JSON messages from stdin, translates to GossipMessage,
// passes to protocol.handle_input(), drains poll_transmit() to stdout.

use std::io::{self, BufRead, Write};
use serde::{Deserialize, Serialize};

// Maelstrom message envelope
#[derive(Deserialize, Serialize)]
struct MaelstromMsg {
    src: String,
    dest: String,
    body: serde_json::Value,
}

fn main() {
    let stdin = io::stdin();
    let stdout = io::stdout();
    let mut out = stdout.lock();

    // Initialize protocol
    // let mut protocol = GossipProtocol::new(...);

    for line in stdin.lock().lines() {
        let line = line.expect("stdin read error");
        let msg: MaelstromMsg = serde_json::from_str(&line)
            .expect("malformed Maelstrom message");

        // Translate Maelstrom message → GossipMessage
        // protocol.handle_input(&gossip_msg, now);

        // Drain outbox → Maelstrom messages
        // while let Some(transmit) = protocol.poll_transmit() {
        //     let response = translate_to_maelstrom(transmit);
        //     serde_json::to_writer(&mut out, &response).unwrap();
        //     out.write_all(b"\n").unwrap();
        //     out.flush().unwrap();
        // }
    }
}
```

### Maelstrom Workloads

| Workload | Maelstrom Challenge | What It Tests |
|----------|-------------------|---------------|
| **Broadcast** | Challenge #3 (broadcast) | Gossip convergence under partitions |
| **Counter** | Challenge #4 (g-counter) | CRDT correctness, eventual consistency |
| **Unique IDs** | Challenge #2 (unique-ids) | ID generation without coordination |
| **Kafka-style log** | Challenge #5 (kafka) | Ordered delivery, offset tracking |

### Running Maelstrom Tests

```bash
# Build the Maelstrom wrapper
cargo build --release --bin maelstrom_gossip

# Run broadcast challenge (gossip convergence)
maelstrom test \
  -w broadcast \
  --bin target/release/maelstrom_gossip \
  --node-count 5 \
  --time-limit 20 \
  --rate 10 \
  --nemesis partition

# Run with stricter timing
maelstrom test \
  -w broadcast \
  --bin target/release/maelstrom_gossip \
  --node-count 25 \
  --time-limit 20 \
  --rate 100 \
  --nemesis partition \
  --latency 100
```

### Maelstrom Output Analysis

After a Maelstrom run, analyze the results:

```bash
# Open results in browser
maelstrom serve

# Or parse JSON results directly
cat store/latest/results.edn
```

**Key metrics to check:**
- `:valid?` — Did all operations satisfy the consistency model?
- `:lost-count` — Messages that were sent but never delivered
- `:stable-count` — Messages that converged to all nodes
- `:latency` — Message propagation time distribution

**Report format:**

```
MAELSTROM REPORT — {workload}
═════════════════════════════
Nodes:            {count}
Duration:         {seconds}s
Operations:       {count}
Nemesis:          {partition|none|...}

Result:           {PASS|FAIL}

Consistency:
  Valid:          {yes|no}
  Lost messages:  {count} ({percentage}%)
  Stable:         {count} ({percentage}%)

Latency (ms):
  p50:  {value}
  p95:  {value}
  p99:  {value}

Convergence:
  Rounds to full convergence: {count}
  Expected (O(log n)):        {ceil(log2(nodes))}
  Status: {WITHIN BOUND | EXCEEDS BOUND}

{if FAIL}
Anomalies found:
  - {description of consistency violation}
  - {messages lost during partition}
{/if}
```

---

## Mode B: Full Jepsen

### Prerequisites

1. Docker or Vagrant for provisioning test nodes
2. Compiled gossip-rs binaries for the target platform
3. SSH access configured for test nodes
4. Jepsen Clojure framework (or the project's custom test harness)

### Cluster Configuration

Based on Yuan et al. (OSDI 2014): **3 nodes suffice for reproducing most
distributed failures**. Use 5 nodes for partition tolerance testing.

```
Cluster topology:
  Node 1 (n1): gossip-rs worker + coordination backend
  Node 2 (n2): gossip-rs worker + coordination backend
  Node 3 (n3): gossip-rs worker + coordination backend
  [Node 4 (n4): optional, for partition quorum testing]
  [Node 5 (n5): optional, for partition quorum testing]
```

### Jepsen Workloads

| Workload | What It Tests | Evidence |
|----------|---------------|----------|
| **Shard acquisition** | Linearizability of acquire/release | Core correctness |
| **Lease exclusivity** | Only one worker holds lease at a time | etcd Jepsen 3.4.3 |
| **Checkpoint fence** | Stale-epoch checkpoints are rejected | D2.14, Gray & Cheriton |
| **Split correctness** | Children cover parent range exactly | Shard coverage invariant |
| **Concurrent acquisition** | Two workers race for same shard | Fence monotonicity |
| **Crash recovery** | Worker crashes mid-checkpoint, restarts | Done-ledger durability |
| **Full partition** | Network split isolates subsets | Consensus safety |
| **Asymmetric partition** | A→B works, B→A drops | Lifeguard false positives |
| **Process pause** | GC-style pause during lease hold | etcd Jepsen pattern |

### Nemesis Configurations

| Nemesis | Description | Level |
|---------|-------------|-------|
| **partition-random-halves** | Split cluster into two random halves | Standard |
| **partition-random-node** | Isolate a single random node | Standard |
| **kill-random-node** | SIGKILL a random node process | Standard |
| **pause-random-node** | SIGSTOP/SIGCONT a node (simulates GC pause) | Standard |
| **clock-skew** | Adjust system clock on random nodes | Advanced |
| **combined** | Multiple nemeses active simultaneously | Chaos |

### Running Full Jepsen Tests

```bash
# Provision test cluster (Docker)
cd jepsen/gossip-rs
docker compose up -d

# Run shard acquisition linearizability test
lein run test \
  --nodes n1,n2,n3 \
  --workload shard-acquisition \
  --nemesis partition-random-halves \
  --time-limit 60 \
  --concurrency 10

# Run lease exclusivity test (etcd failure pattern)
lein run test \
  --nodes n1,n2,n3 \
  --workload lease-exclusivity \
  --nemesis pause-random-node \
  --time-limit 120 \
  --concurrency 5

# Run combined chaos test
lein run test \
  --nodes n1,n2,n3,n4,n5 \
  --workload full-lifecycle \
  --nemesis combined \
  --time-limit 300 \
  --concurrency 20
```

### Full Jepsen Output Analysis

```
JEPSEN REPORT — {workload}
══════════════════════════
Nodes:            {count}
Duration:         {seconds}s
Operations:       {count} ({ok}/{fail}/{info})
Nemesis:          {type}
Concurrency:      {threads}

Result:           {PASS|FAIL}

Linearizability:
  Valid history:  {yes|no}
  Checker:        {porcupine|elle|custom}
  Anomalies:      {count}

Invariant checks:
  ┌─────────────────────────────┬────────┬────────┐
  │ Invariant                   │ Status │ Checks │
  ├─────────────────────────────┼────────┼────────┤
  │ Lease exclusivity (S1)      │ PASS   │ 1234   │
  │ Fence monotonicity (S2)     │ PASS   │ 567    │
  │ Terminal irreversibility (S3)│ PASS   │ 89     │
  │ Shard coverage (S4)         │ FAIL   │ 12     │
  └─────────────────────────────┴────────┴────────┘

{if FAIL}
Failing operations:
  t=12.3s  :invoke  acquire-shard  shard-7  worker-2
  t=12.3s  :ok      acquire-shard  shard-7  worker-2  epoch=5
  t=12.5s  NEMESIS: partition [n1,n3] | [n2]
  t=13.1s  :invoke  checkpoint     shard-7  worker-1  epoch=4
  t=13.2s  :ok      checkpoint     shard-7  worker-1  ← VIOLATION: stale epoch accepted

Reproduction:
  lein run test --nodes n1,n2,n3 --workload {workload} --nemesis {nemesis} \
    --time-limit 60 --test-seed {seed}
{/if}
```

---

## Correctness Properties

These properties must be verified by every Jepsen run. They correspond to the
project's invariant catalog and are checked by specific verifiers.

| Layer | Property | Checker | Reference |
|-------|----------|---------|-----------|
| **Coordination** | Linearizability of shard operations | Porcupine / custom | Herlihy & Wing 1990 |
| **Coordination** | Fence monotonicity, lease exclusivity | Custom invariant checker | D2.14, Gray & Cheriton 1989 |
| **Gossip** | Eventual convergence (all nodes informed) | Custom convergence checker | Demers et al. PODC 1987 |
| **Gossip** | O(log n) round convergence speed | Timing analysis | SWIM protocol, DSN 2002 |
| **Shard lifecycle** | Terminal irreversibility | State machine invariant | D2 locked decisions |
| **Shard lifecycle** | Split coverage (no gaps, no overlaps) | Algebraic verification | Shard boundary spec |
| **Persistence** | Exactly-once commit protocol | Typestate + fault injection | Stripe idempotency pattern |
| **End-to-end** | No missed secrets, no duplicate reports | Diff against ground truth | Application-specific |

---

## Decision: Maelstrom vs Full Jepsen

| Factor | Maelstrom | Full Jepsen |
|--------|-----------|-------------|
| **Setup time** | Minutes | Hours |
| **Run time** | Seconds | Minutes-hours |
| **Network realism** | Simulated JSON | Real TCP/SSH |
| **Fault injection** | Network partitions | Network + process + clock + disk |
| **Tests protocol logic** | Excellent | Good |
| **Tests integration** | Poor | Excellent |
| **Tests deployment** | No | Yes |
| **Flakiness** | Low | Medium-high (CockroachDB lesson) |
| **When to use** | Development, per-feature | Pre-release, nightly |

**Rule of thumb:**
- Start with Maelstrom during development
- Graduate to full Jepsen when the system is deployed and integrated
- Run both in CI (Maelstrom per-PR, Jepsen nightly)

---

## Relationship to DST (`/sim-run`)

```
                    Speed           Realism          Bugs Found
                    ─────           ───────          ──────────
/sim-run Level 1    ████████████    ██               Logic bugs, state machine errors
/sim-run Level 2    ██████████      ████             Concurrency, timing, lease expiry
/sim-run Level 3    ████████        ██████           Cascading failures, Byzantine
/jepsen Maelstrom   ██████          ████████         Protocol convergence, message loss
/jepsen Full        ██              ██████████████   Integration, deployment, real OS
```

They test **different things** at **different layers**. Both are needed:
- DST finds logic bugs fast (thousands of seeds per second)
- Jepsen finds integration bugs that DST can't (real networking, real OS)

---

## Related Skills

- `/sim-run` — In-process deterministic simulation (complementary)
- `/sim-review` — Verify code is DST-compatible
- `/sim-scaffold` — Generate simulation harnesses and Maelstrom wrappers
- `/dist-sys-auditor` — Validate distributed systems design decisions
