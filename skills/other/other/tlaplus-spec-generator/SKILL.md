---
name: tlaplus-spec-generator
description: "Automatically generate TLA+ specifications from source code (C/C++, Python) for formal verification of distributed systems. Use when users need to: (1) Generate TLA+ specs from program implementations, (2) Model distributed systems, consensus protocols, or concurrent algorithms, (3) Extract state variables, actions, and invariants from code, (4) Create formal specifications for model checking with TLC, (5) Verify safety and liveness properties of distributed systems. Particularly effective for message-passing systems, replication protocols, consensus algorithms, and distributed transactions."
---

# TLA+ Spec Generator

Automatically generate TLA+ specifications from program implementations for formal verification of distributed systems.

## Overview

This skill transforms imperative programs (C/C++, Python) into declarative TLA+ specifications. It analyzes program structure to identify state variables, actions, and system behavior, then generates well-structured TLA+ modules suitable for model checking with TLC.

## Workflow

### 1. Analyze Source Code

Generate TLA+ specification from source files:

```bash
# Single file
python3 scripts/generate_spec.py program.py -o Spec.tla

# Multiple files
python3 scripts/generate_spec.py server.py client.py protocol.py -o Protocol.tla

# With module name
python3 scripts/generate_spec.py distributed_system.c -o System.tla --module-name DistributedSystem
```

The generator automatically:
- Detects programming language
- Parses source code
- Identifies state variables and actions
- Extracts system structure
- Generates TLA+ specification

### 2. Specify System Parameters

For distributed systems, specify the number of processes:

```bash
python3 scripts/generate_spec.py consensus.py -o Consensus.tla --processes 3
```

This creates a constant `N` in the TLA+ spec representing the number of processes/nodes.

### 3. Generated Output

The generator produces two files:

**1. Spec.tla** - Complete TLA+ specification:
```tla
---- MODULE Spec ----
EXTENDS Naturals, Sequences, FiniteSets, TLC

CONSTANTS N  \* Number of processes

VARIABLES
  state,
  messages,
  committed

vars == <<state, messages, committed>>

TypeOK ==
  /\ state \in [1..N -> {"Init", "Working", "Done"}]
  /\ messages \in SUBSET Messages
  /\ committed \in SUBSET Operations

Init ==
  /\ state = [p \in 1..N |-> "Init"]
  /\ messages = {}
  /\ committed = {}

SendMessage(p, msg) ==
  /\ state[p] = "Working"
  /\ messages' = messages \cup {msg}
  /\ UNCHANGED <<state, committed>>

Next ==
  \/ \E p \in 1..N, msg \in Messages : SendMessage(p, msg)

Spec == Init /\ [][Next]_vars

====
```

**2. Spec_mapping.txt** - Explanation of program-to-TLA+ mapping:
- State variables and their types
- Actions and what they modify
- Processes identified
- Constants defined

### 4. Refine the Specification

The generated spec is a starting point. Refine it by:

1. **Review state variables** - Ensure all relevant state is captured
2. **Complete action definitions** - Add preconditions and effects
3. **Add invariants** - Define safety properties
4. **Add temporal properties** - Define liveness properties
5. **Adjust abstraction** - Balance detail vs. tractability

### 5. Model Check with TLC

Create a TLC configuration file (Spec.cfg):

```
CONSTANTS
  N = 3

SPECIFICATION Spec

INVARIANT TypeOK
```

Run TLC model checker:

```bash
tlc Spec.tla -config Spec.cfg
```

## Abstraction Levels

Control the level of abstraction:

```bash
# Low abstraction (more detail, larger state space)
python3 scripts/generate_spec.py program.py -o Spec.tla --abstraction low

# Medium abstraction (balanced, recommended)
python3 scripts/generate_spec.py program.py -o Spec.tla --abstraction medium

# High abstraction (minimal states, protocol-level)
python3 scripts/generate_spec.py program.py -o Spec.tla --abstraction high
```

**Medium abstraction (default):**
- Booleans → preserved
- Integers → bounded ranges (0..N)
- Enums → preserved as string sets
- Collections → sequences or sets
- Focus on control flow and key state

## Common Use Cases

### Distributed Consensus Protocol

**Scenario:** Implementing Raft or Paxos consensus algorithm.

**Approach:**
1. Generate spec from implementation
2. Identify processes (nodes), state variables (term, log, votes)
3. Extract actions (RequestVote, AppendEntries, etc.)
4. Add safety properties (leader uniqueness, log consistency)
5. Verify with TLC

**See:** [distributed_patterns.md](references/distributed_patterns.md#pattern-2-consensus-protocols)

### Message-Passing System

**Scenario:** Distributed system with processes communicating via messages.

**Approach:**
1. Generate spec from message handlers
2. Model network as set of messages in transit
3. Define Send and Receive actions
4. Add properties (message ordering, delivery guarantees)
5. Check for deadlocks and livelocks

**See:** [distributed_patterns.md](references/distributed_patterns.md#pattern-1-message-passing)

### Replication Protocol

**Scenario:** Primary-backup or multi-master replication.

**Approach:**
1. Generate spec from replication logic
2. Model replicas and their logs
3. Define replication and commit actions
4. Add consistency properties
5. Verify under failures

**See:** [distributed_patterns.md](references/distributed_patterns.md#pattern-4-replication)

### Leader Election

**Scenario:** Implementing leader election algorithm.

**Approach:**
1. Generate spec from election code
2. Model process states (follower, candidate, leader)
3. Extract election actions
4. Add safety (at most one leader) and liveness (eventually a leader)
5. Verify correctness

**See:** [distributed_patterns.md](references/distributed_patterns.md#pattern-3-leader-election)

## Advanced Options

### Focus on Specific Functions

Extract only relevant functions:

```bash
python3 scripts/generate_spec.py system.py -o Spec.tla \
  --focus-functions send_message receive_message commit_transaction
```

### Track Specific Variables

Explicitly specify state variables:

```bash
python3 scripts/generate_spec.py system.py -o Spec.tla \
  --track-vars state messages committed_ops leader_id
```

## Refining Generated Specs

Generated specs need refinement. Common refinements:

**1. Complete action preconditions:**
```tla
\* Generated (incomplete)
SendMessage(p, msg) ==
  /\ messages' = messages \cup {msg}

\* Refined (with precondition)
SendMessage(p, msg) ==
  /\ state[p] = "Active"        \* Precondition
  /\ msg \notin messages         \* No duplicates
  /\ messages' = messages \cup {msg}
  /\ UNCHANGED <<state, committed>>
```

**2. Add invariants:**
```tla
\* Safety properties
SafetyInvariant ==
  /\ \A p \in Procs : state[p] \in ValidStates
  /\ Cardinality({p \in Procs : state[p] = "Leader"}) <= 1

\* Add to spec
INVARIANT TypeOK
INVARIANT SafetyInvariant
```

**3. Add liveness properties:**
```tla
\* Eventually reach consensus
PROPERTY <>[](\A p \in Procs : state[p] = "Committed")

\* Every request is eventually processed
PROPERTY \A req \in Requests : [](Submitted(req) => <>Processed(req))
```

**4. Add fairness:**
```tla
\* Weak fairness: continuously enabled actions eventually happen
Spec == Init /\ [][Next]_vars /\ WF_vars(ReceiveMessage)

\* Strong fairness: infinitely often enabled actions eventually happen
Spec == Init /\ [][Next]_vars /\ SF_vars(ElectLeader)
```

## Tips

- **Start with small models** - Use N=2 or N=3 processes initially
- **Check TypeOK first** - Ensures basic correctness before complex properties
- **Use symmetry** - Add `SYMMETRY Permutations(Procs)` to reduce state space
- **Abstract data values** - Focus on protocol behavior, not data content
- **Iterate abstraction** - If TLC is too slow, increase abstraction
- **Read the mapping file** - Understand how program maps to TLA+
- **Consult patterns** - See reference docs for common distributed system patterns

## Common Issues

**State explosion:** TLC runs out of memory or takes too long.
- Solution: Increase abstraction, reduce N, add state constraints, use symmetry

**Deadlock detected:** TLC finds states with no enabled actions.
- Solution: Check action preconditions, ensure progress is always possible, add fairness

**Invariant violated:** TLC finds counterexample.
- Solution: Review counterexample trace, fix implementation or weaken invariant

**Spec too abstract:** Properties are trivially true.
- Solution: Decrease abstraction, track more variables, preserve more detail

## References

- **[tlaplus_syntax.md](references/tlaplus_syntax.md)**: Complete TLA+ syntax reference with examples
- **[distributed_patterns.md](references/distributed_patterns.md)**: Common patterns for distributed systems (consensus, replication, leader election)

## Scripts

- **generate_spec.py**: Main generation script (orchestrates entire process)
- **program_analyzer.py**: Program analysis module (extracts state, actions, processes)
- **tlaplus_generator.py**: TLA+ generation module (produces TLA+ specifications)

## External Tools

- **TLA+ Toolbox**: IDE for writing and checking TLA+ specs (https://lamport.azurewebsites.net/tla/toolbox.html)
- **TLC Model Checker**: Command-line model checker (included with Toolbox)
- **TLAPS**: TLA+ Proof System for theorem proving (optional)
