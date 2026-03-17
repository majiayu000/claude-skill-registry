---
name: sim-scaffold
description: Scaffold simulation-testable modules with sans-IO pattern, proptest state machine tests, and fault injection points — prevents retrofitting costs by making code DST-ready from the start
user-invocable: true
---

# Scaffold Simulation-Testable Module

Generate boilerplate for new modules that are **deterministic simulation testing
(DST) ready from the start**. Prevents the costly retrofitting that FoundationDB
avoided by building simulation infrastructure before writing database code.

## Evidence Base

| Source | Pattern Used |
|--------|--------------|
| **Firezone** (sans-IO blog) | Pure state machine core, effects as return values |
| **sled** (simulation.html) | `receive(msg, at) -> [(msg, destination)]` pattern |
| **Stateright** | `Actor` trait: `on_msg(state, msg) -> Vec<Action>` |
| **FoundationDB** (SIGMOD 2021) | Simulation-first architecture, SimContext |
| **proptest** | State machine testing with `prop_state_machine!` |

## When to Use

- Creating a new module in `gossip-coordination/`
- Adding a new gossip protocol component
- Building a new pipeline stage that touches coordination
- Any new code that manages distributed state, leases, or shard lifecycle

## When NOT to Use

- Adding helper functions to existing modules (use `/sim-review` instead)
- Detection engine rules or regex patterns
- Pure data types with no state transitions

---

## Procedure

### Step 1: Determine Module Type

Ask the user which type of module they are building:

| Type | Description | Template |
|------|-------------|----------|
| **A: Coordination module** | Manages distributed state (shards, leases, epochs) | State machine + InMemory backend |
| **B: Gossip protocol** | Message-passing protocol between nodes | Sans-IO state machine |
| **C: Pipeline component** | Processing stage with checkpointing | Effect-based with trait boundaries |

### Step 2: Gather Invariants

Ask the user:

1. **What are the key state transitions?** (e.g., Open -> Acquired -> Checkpointing -> Done)
2. **What invariants must hold?** (e.g., "only one worker holds a lease at a time")
3. **What are the error conditions?** (e.g., "lease expired", "fence rejected")
4. **What external dependencies exist?** (e.g., persistence, network, timers)

### Step 3: Generate Scaffold

#### Type A: Coordination Module

Generate this file structure under the appropriate crate:

```
src/<module>/
  mod.rs            — Public API, module docs, re-exports
  state.rs          — State machine types
  logic.rs          — Pure state transition functions
  sim.rs            — Simulation harness (behind test-support feature)
  tests/
    proptest_sm.rs  — proptest state machine tests
    invariants.rs   — Invariant assertion functions
```

> **Prerequisite:** `LogicalTime` must be defined in
> `gossip_contracts::coordination` before the scaffold compiles. If the
> coordination contracts module is still a doc stub, define `LogicalTime`
> there first (or use a temporary type alias).

**`state.rs` template:**

```rust
//! State machine types for <module>.
//!
//! All types are plain data — no I/O, no time reads, no randomness.

use gossip_contracts::coordination::LogicalTime;

/// The states this module can be in.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum State {
    // TODO: Fill in states from Step 2
}

/// Inputs that drive state transitions.
#[derive(Debug, Clone)]
pub enum Input {
    // TODO: Fill in inputs from Step 2
}

/// Side effects produced by state transitions.
///
/// Effects are returned as data — the caller is responsible for executing them.
/// This keeps the state machine pure and deterministically testable.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Effect {
    // TODO: Fill in effects from Step 2
}
```

**`logic.rs` template:**

```rust
//! Pure state transition logic for <module>.
//!
//! Every function in this module is a pure function:
//! `fn(current_state, input, now) -> (new_state, Vec<Effect>)`
//!
//! No I/O, no clock reads, no randomness without explicit seed.

use super::state::{Effect, Input, State};
use gossip_contracts::coordination::LogicalTime;

/// Apply an input to the current state, producing a new state and effects.
///
/// # Invariants
///
/// TODO: Document invariants from Step 2
pub fn transition(
    state: &State,
    input: &Input,
    now: LogicalTime,
) -> (State, Vec<Effect>) {
    match (state, input) {
        // TODO: Implement transitions
        _ => (state.clone(), vec![]),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    // TODO: Unit tests for each transition
}
```

**`sim.rs` template:**

```rust
//! Simulation harness for <module>.
//!
//! Connects the pure state machine to a deterministic execution environment
//! with seeded PRNG, simulated clock, and fault injection.

#![cfg(feature = "test-support")]

use std::collections::BinaryHeap;

use rand::rngs::StdRng;
use rand::SeedableRng;

use gossip_contracts::coordination::LogicalTime;

use super::logic;
use super::state::{Effect, Input, State};

/// Deterministic execution context for simulation.
pub struct SimContext {
    /// Seeded PRNG for reproducible randomness.
    pub rng: StdRng,
    /// Simulated logical clock.
    pub clock: LogicalTime,
    /// Seed used to create this context (for reproduction).
    pub seed: u64,
}

impl SimContext {
    /// Create a new simulation context with the given seed.
    pub fn new(seed: u64) -> Self {
        Self {
            rng: StdRng::seed_from_u64(seed),
            clock: LogicalTime::default(),
            seed,
        }
    }

    /// Advance the simulated clock by `ticks`.
    pub fn advance(&mut self, ticks: u64) {
        self.clock = self.clock.advance(ticks);
    }
}

/// Fault injection configuration.
#[derive(Debug, Clone, Default)]
pub struct FaultConfig {
    /// Drop probability for effects (0.0 = none, 1.0 = all).
    pub effect_drop_rate: f64,
    /// Whether to inject lease expiry after N operations.
    pub expire_lease_after: Option<usize>,
    /// Whether to inject process pause (freeze clock).
    pub inject_pause: bool,
}

/// Simulation harness orchestrating multiple state machine instances.
pub struct SimHarness {
    pub ctx: SimContext,
    pub states: Vec<State>,
    pub effects_log: Vec<(usize, Effect)>,
    pub fault_config: FaultConfig,
    op_count: usize,
}

impl SimHarness {
    pub fn new(seed: u64, initial_states: Vec<State>) -> Self {
        Self {
            ctx: SimContext::new(seed),
            states: initial_states,
            effects_log: Vec::new(),
            fault_config: FaultConfig::default(),
            op_count: 0,
        }
    }

    /// Apply an input to a specific state machine instance.
    pub fn apply(&mut self, instance: usize, input: &Input) -> Vec<Effect> {
        let (new_state, effects) =
            logic::transition(&self.states[instance], input, self.ctx.clock);
        self.states[instance] = new_state;
        self.op_count += 1;

        // Log effects for invariant checking.
        for effect in &effects {
            self.effects_log
                .push((instance, effect.clone()));
        }

        effects
    }

    /// Check all invariants against current state.
    ///
    /// Returns a list of violated invariant descriptions.
    pub fn check_invariants(&self) -> Vec<String> {
        let mut violations = Vec::new();

        // TODO: Add invariant checks from Step 2
        // Example:
        // if self.states.iter().filter(|s| matches!(s, State::Active)).count() > 1 {
        //     violations.push("MUTUAL_EXCLUSION: More than one instance active".into());
        // }

        violations
    }
}
```

**`tests/proptest_sm.rs` template:**

```rust
//! proptest state machine tests for <module>.
//!
//! Generates random sequences of valid inputs and verifies that
//! invariants hold after every transition.

#![cfg(all(test, feature = "test-support"))]

use proptest::prelude::*;

use super::sim::{FaultConfig, SimHarness};
use super::state::Input;

/// Strategy for generating valid inputs.
fn arb_input() -> impl Strategy<Value = Input> {
    // TODO: Generate valid inputs based on module types
    prop_oneof![
        // Just(Input::VariantA),
        // Just(Input::VariantB { ... }),
    ]
}

/// Strategy for generating input sequences.
fn arb_input_sequence(max_len: usize) -> impl Strategy<Value = Vec<Input>> {
    prop::collection::vec(arb_input(), 1..=max_len)
}

proptest! {
    /// Invariants hold after every transition under normal conditions.
    #[test]
    fn invariants_hold_sunny_day(
        seed in any::<u64>(),
        inputs in arb_input_sequence(50),
    ) {
        let mut harness = SimHarness::new(seed, vec![/* initial state */]);

        for input in &inputs {
            harness.apply(0, input);

            let violations = harness.check_invariants();
            prop_assert!(
                violations.is_empty(),
                "Invariant violations after {:?}: {:?}",
                input,
                violations,
            );
        }
    }

    /// Invariants hold under fault injection.
    #[test]
    fn invariants_hold_with_faults(
        seed in any::<u64>(),
        inputs in arb_input_sequence(50),
        drop_rate in 0.0..0.5f64,
    ) {
        let mut harness = SimHarness::new(seed, vec![/* initial state */]);
        harness.fault_config = FaultConfig {
            effect_drop_rate: drop_rate,
            ..Default::default()
        };

        for input in &inputs {
            harness.apply(0, input);

            let violations = harness.check_invariants();
            prop_assert!(
                violations.is_empty(),
                "Invariant violations under faults (drop_rate={}) after {:?}: {:?}",
                drop_rate,
                input,
                violations,
            );
        }
    }
}
```

**`tests/invariants.rs` template:**

```rust
//! Invariant assertion functions for <module>.
//!
//! Each function checks one invariant and returns Ok(()) or
//! Err(description) if violated.

#![cfg(all(test, feature = "test-support"))]

use super::state::State;

/// Check: TODO describe invariant
pub fn check_invariant_name(states: &[State]) -> Result<(), String> {
    // TODO: Implement invariant check
    Ok(())
}
```

---

#### Type B: Gossip Protocol Module

Generate this file structure:

```
src/<module>/
  mod.rs              — Public API, module docs
  protocol.rs         — Sans-IO state machine
  messages.rs         — Protocol message types
  sim.rs              — SimNetwork connecting N protocol instances
  tests/
    proptest_convergence.rs  — Convergence property tests
    proptest_partitions.rs   — Partition tolerance tests
```

**`protocol.rs` template (sans-IO pattern):**

```rust
//! Sans-IO gossip protocol state machine.
//!
//! This module contains NO I/O. The protocol is driven by four methods:
//!
//! - `handle_input(msg, now)` — process an incoming message
//! - `poll_transmit()` — dequeue the next outbound message
//! - `poll_timeout()` — query when the next timer fires
//! - `handle_timeout(now)` — process a timer expiry
//!
//! The caller (runtime or simulation harness) is responsible for actually
//! sending messages and managing real/simulated time.
//!
//! # Evidence
//!
//! This pattern is used by:
//! - sled: `receive(msg, at) -> [(msg, destination)]`
//! - Firezone: sans-IO connlib architecture
//! - Stateright: `Actor::on_msg(state, msg) -> Vec<Action>`

use std::collections::VecDeque;

use gossip_contracts::coordination::LogicalTime;

use super::messages::{GossipMessage, NodeId, Transmit};

/// Configuration for the gossip protocol.
#[derive(Debug, Clone)]
pub struct ProtocolConfig {
    /// This node's identity.
    pub node_id: NodeId,
    /// Gossip interval (in logical time ticks).
    pub gossip_interval: u64,
    /// Failure detection timeout (in logical time ticks).
    pub failure_timeout: u64,
    /// Fan-out: number of peers to gossip to per round.
    pub fanout: usize,
}

/// Sans-IO gossip protocol state machine.
pub struct GossipProtocol {
    config: ProtocolConfig,
    outbox: VecDeque<Transmit>,
    next_gossip: Option<LogicalTime>,
    // TODO: Protocol-specific state (membership table, suspicion map, etc.)
}

impl GossipProtocol {
    /// Create a new protocol instance with the given configuration.
    pub fn new(config: ProtocolConfig, now: LogicalTime) -> Self {
        Self {
            next_gossip: Some(now.advance(config.gossip_interval)),
            outbox: VecDeque::new(),
            config,
        }
    }

    /// Process an incoming message from another node.
    ///
    /// This may enqueue outbound messages (retrievable via `poll_transmit`)
    /// and update internal state, but performs NO I/O.
    pub fn handle_input(&mut self, msg: &GossipMessage, now: LogicalTime) {
        match msg {
            // TODO: Handle each message type
            _ => {}
        }
    }

    /// Dequeue the next outbound message, if any.
    ///
    /// The caller is responsible for actually sending this over the network
    /// (or routing it in-process during simulation).
    pub fn poll_transmit(&mut self) -> Option<Transmit> {
        self.outbox.pop_front()
    }

    /// Query when the next timeout should fire.
    ///
    /// Returns `None` if no timers are pending.
    pub fn poll_timeout(&self) -> Option<LogicalTime> {
        self.next_gossip
    }

    /// Process a timer expiry.
    ///
    /// Call this when the logical clock reaches or exceeds the value
    /// returned by `poll_timeout()`.
    pub fn handle_timeout(&mut self, now: LogicalTime) {
        if self.next_gossip.is_some_and(|t| now >= t) {
            self.do_gossip_round(now);
            self.next_gossip = Some(now.advance(self.config.gossip_interval));
        }
    }

    fn do_gossip_round(&mut self, _now: LogicalTime) {
        // TODO: Select peers, build gossip messages, enqueue via self.outbox
    }
}
```

**`sim.rs` template (SimNetwork):**

```rust
//! Simulation network connecting N gossip protocol instances.
//!
//! Messages are delivered via an in-process priority queue ordered by
//! logical time, following sled's discrete-event simulation pattern.

#![cfg(feature = "test-support")]

use std::cmp::Reverse;
use std::collections::BinaryHeap;

use rand::rngs::StdRng;
use rand::SeedableRng;

use gossip_contracts::coordination::LogicalTime;

use super::messages::{NodeId, Transmit};
use super::protocol::{GossipProtocol, ProtocolConfig};

/// A scheduled event in the simulation.
#[derive(Debug)]
struct ScheduledEvent {
    time: LogicalTime,
    kind: EventKind,
}

#[derive(Debug)]
enum EventKind {
    Deliver(Transmit),
    Timeout(NodeId),
}

impl PartialEq for ScheduledEvent {
    fn eq(&self, other: &Self) -> bool {
        self.time == other.time
    }
}

impl Eq for ScheduledEvent {}

impl PartialOrd for ScheduledEvent {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for ScheduledEvent {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        // Min-heap: earliest time first.
        Reverse(self.time).cmp(&Reverse(other.time))
    }
}

/// Network fault injection configuration.
#[derive(Debug, Clone, Default)]
pub struct NetworkFaults {
    /// Message drop probability (0.0 = reliable, 1.0 = total partition).
    pub drop_rate: f64,
    /// Maximum message delay in ticks (0 = instant delivery).
    pub max_delay: u64,
    /// Set of (from, to) pairs that are partitioned.
    pub partitions: Vec<(NodeId, NodeId)>,
}

/// Simulated network of gossip protocol instances.
pub struct SimNetwork {
    pub nodes: Vec<GossipProtocol>,
    pub rng: StdRng,
    pub clock: LogicalTime,
    event_queue: BinaryHeap<ScheduledEvent>,
    pub faults: NetworkFaults,
    pub seed: u64,
}

impl SimNetwork {
    /// Create a network of `n` nodes with the given seed.
    pub fn new(seed: u64, n: usize, config_fn: impl Fn(usize) -> ProtocolConfig) -> Self {
        let clock = LogicalTime::default();
        let nodes = (0..n)
            .map(|i| GossipProtocol::new(config_fn(i), clock))
            .collect::<Vec<_>>();

        let mut net = Self {
            nodes,
            rng: StdRng::seed_from_u64(seed),
            clock,
            event_queue: BinaryHeap::new(),
            faults: NetworkFaults::default(),
            seed,
        };

        // Schedule initial timeouts.
        for (i, node) in net.nodes.iter().enumerate() {
            if let Some(t) = node.poll_timeout() {
                net.event_queue.push(ScheduledEvent {
                    time: t,
                    kind: EventKind::Timeout(NodeId(i as u64)),
                });
            }
        }

        net
    }

    /// Run the simulation for up to `max_ticks` logical time ticks.
    ///
    /// Returns the number of events processed.
    pub fn run(&mut self, max_ticks: u64) -> usize {
        let deadline = self.clock.advance(max_ticks);
        let mut events_processed = 0;

        while let Some(event) = self.event_queue.pop() {
            if event.time > deadline {
                self.event_queue.push(event);
                break;
            }

            self.clock = event.time;
            events_processed += 1;

            match event.kind {
                EventKind::Deliver(transmit) => {
                    let dst = transmit.destination.0 as usize;
                    if dst < self.nodes.len() {
                        self.nodes[dst].handle_input(&transmit.message, self.clock);
                        self.drain_outbox(dst);
                    }
                }
                EventKind::Timeout(node_id) => {
                    let idx = node_id.0 as usize;
                    if idx < self.nodes.len() {
                        self.nodes[idx].handle_timeout(self.clock);
                        self.drain_outbox(idx);

                        // Re-schedule next timeout.
                        if let Some(t) = self.nodes[idx].poll_timeout() {
                            self.event_queue.push(ScheduledEvent {
                                time: t,
                                kind: EventKind::Timeout(node_id),
                            });
                        }
                    }
                }
            }
        }

        events_processed
    }

    fn drain_outbox(&mut self, node_idx: usize) {
        while let Some(transmit) = self.nodes[node_idx].poll_transmit() {
            // TODO: Apply fault injection (drops, delays, partitions)
            // using self.faults and self.rng
            self.event_queue.push(ScheduledEvent {
                time: self.clock.advance(1), // Minimum 1-tick delivery delay
                kind: EventKind::Deliver(transmit),
            });
        }
    }

    /// Check convergence: do all nodes agree on the same state?
    pub fn check_convergence(&self) -> bool {
        // TODO: Define convergence check based on protocol semantics
        true
    }
}
```

---

#### Type C: Pipeline Component

Generate this file structure:

```
src/<component>/
  mod.rs          — Public API
  state.rs        — Processing state types
  logic.rs        — Pure processing logic
  traits.rs       — I/O trait boundaries
  sim.rs          — Simulation with mock I/O
  tests/
    proptest_processing.rs
```

Use the same SimContext pattern as Type A, but the trait boundaries focus on
I/O operations (read source data, write checkpoints, emit findings) rather
than distributed coordination.

---

### Step 4: Verify Scaffold Compiles

After generating the scaffold:

```bash
cargo check --all-features
```

If compilation fails, fix the generated code. Common issues:
- Missing imports (add `use` statements)
- Type mismatches with existing crate types
- Feature gate misalignment

### Step 5: Generate Initial Tests

Run the generated proptest to verify the scaffold works:

```bash
cargo test --features test-support -- <module>::tests
```

The initial tests should pass (they test the empty/default state machine).

### Step 6: Report

```
SIM-SCAFFOLD REPORT
════════════════════
Module:          <name>
Type:            {Coordination | Gossip Protocol | Pipeline Component}
Files created:   {count}
Pattern:         {sans-IO | state machine + effects | trait boundary}

Invariants to implement:
  1. {invariant from Step 2}
  2. {invariant from Step 2}

Next steps:
  1. Implement state transitions in logic.rs
  2. Add proptest strategies for Input variants
  3. Implement invariant checks in sim.rs
  4. Run /sim-review on completed implementation
```

---

## Quick Reference: Module Types

| | Type A: Coordination | Type B: Gossip Protocol | Type C: Pipeline |
|---|---|---|---|
| **Manages** | Distributed state (shards, leases, epochs) | Message-passing between nodes | Processing stages with checkpoints |
| **Core pattern** | State machine + InMemory backend | Sans-IO (handle_input/poll_transmit/poll_timeout/handle_timeout) | Effect-based with trait boundaries |
| **sim-review boundary** | STRICT | STRICT | MODERATE |
| **Time model** | `LogicalTime` parameter on every op | `LogicalTime` parameter on every method | `LogicalTime` at checkpoint boundaries |
| **Key test** | Proptest state machine (invariants after every transition) | Proptest convergence + partition tolerance | Proptest processing correctness |
| **Sim harness** | `SimHarness` (single-node state machine) | `SimNetwork` (N-node discrete-event sim) | `SimContext` + mock I/O traits |
| **Fault injection** | Lease expiry, concurrent access, clock advance | Message loss/reorder, partitions, delays | I/O failure, corrupt input |

---

## Related Skills

- `/sim-review` — Review existing code for DST compatibility
- `/sim-run` — Execute simulation tests
- `/test-strategy` — Choose between unit/property/fuzz/simulation testing
- `/dist-sys-auditor` — Validate distributed systems design decisions
