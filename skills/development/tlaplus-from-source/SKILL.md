---
name: tlaplus-from-source
description: Generate a high-level TLA+ model from source code (C, C++, Rust, etc.). Analyzes code to understand its purpose, creates abstractions, writes TLA+ specification, and proposes invariants and properties. Use when the user wants to model source code in TLA+, create a formal specification from implementation, or verify concurrent/distributed algorithms.
---

# Generate High-Level TLA+ Model from Source Code

Create a TLA+ specification from source code by understanding the code's intent, abstracting implementation details, and focusing on the essential concurrent/distributed behavior.

## Philosophy

TLA+ models should capture **what** the system does, not **how** it does it:
- Focus on state transitions and their effects
- Abstract away implementation details (memory management, error handling boilerplate)
- Identify the core concurrent/distributed behavior worth verifying
- Keep the model small enough to be tractable for model checking

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────────┐
│ Phase 1: Understand the Code                                    │
│   → What problem does it solve?                                 │
│   → What are the key functions and their purposes?              │
│   → What state is being managed?                                │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ Phase 2: Identify Abstractions                                  │
│   → What are the essential state variables?                     │
│   → What are the atomic actions?                                │
│   → What concurrency/ordering matters?                          │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ Phase 3: Write TLA+ Specification                               │
│   → Define constants and variables                              │
│   → Write Init and actions                                      │
│   → Define Next as disjunction of actions                       │
│   → Check specification syntax with TLC parser SANY             │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ Phase 4: Propose Properties                                     │
│   → Safety invariants                                           │
│   → Safety properties (what must be true at all times)          │
│   → Liveness properties (what must eventually happen)           │
└─────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Understand the Code

### Step 1.1: Identify the Problem Domain

Read the code and answer in English:

1. **What is the overall purpose?** (e.g., "thread-safe connection management", "distributed consensus", "producer-consumer queue")
2. **What entities exist?** (e.g., threads, processes, clients, servers, connections)
3. **What resources are shared?** (e.g., queues, counters, state machines)

### Step 1.2: Catalog Functions and Their Purpose

For each significant function, document:

| Function | Purpose (in English) | Side Effects | Concurrency Notes |
|----------|---------------------|--------------|-------------------|
| `functionName` | What it does | State changes | Thread-safe? Atomic? |

**Focus on:**
- Public API functions (entry points)
- State-modifying functions (mutators)
- Synchronization points (locks, atomics, barriers)

**Skip:**
- Getters/accessors (unless they have side effects)
- Utility functions (formatting, logging)
- Error handling boilerplate

### Step 1.3: Identify State Variables

List all mutable state that affects the system's behavior:

| State Variable | Type | Purpose | Accessed By |
|----------------|------|---------|-------------|
| `varName` | int/enum/struct | What it tracks | Which functions |

**Look for:**
- Atomic variables (concurrent state)
- Protected fields (mutex-guarded data)
- State enums (state machines)
- Reference counts
- Queues and buffers

### Step 1.4: Identify Concurrency Patterns

Recognize common patterns in the code:

| Pattern | Indicators | TLA+ Abstraction |
|---------|-----------|------------------|
| State machine | Enum state, switch statements | `pc` variable with transitions |
| Reference counting | `refCount`, `addRef/release` | Counter variable |
| Producer-consumer | Queue with enqueue/dequeue | Sequence variable |
| Lock-based | Mutex lock/unlock | Optional: model explicitly or abstract |
| Lock-free | Atomics, CAS operations | Atomic state transitions |
| Connection lifecycle | Connect/disconnect, states | State machine per connection |

---

## Phase 2: Identify Abstractions

### Step 2.1: Choose Abstraction Level

**High-level modeling principles:**

1. **Collapse implementation details**: Multiple C++ statements → one TLA+ action
2. **Abstract data structures**: `std::vector<T>` → finite set or sequence
3. **Simplify types**: `uint32_t refCount` → `Nat` (natural number)
4. **Ignore memory management**: smart pointers, allocation → just the logical state
5. **Model only relevant concurrency**: If code is thread-safe, model the logical operations

### Step 2.2: Map Code Elements to TLA+

| Source Code | TLA+ Abstraction |
|-------------|------------------|
| Class with state machine | Variables + PC states |
| enum State | Set of constants `{State1, State2, ...}` |
| `std::atomic<T>` | Variable (atomicity is implicit in TLA+) |
| `compare_exchange` | Guarded action with atomic state change |
| Thread/process | Element of `Threads` set, may have own `pc[thread]` |
| `shared_ptr<T>` | Logical pointer (present/absent), or reference count |
| Mutex-protected region | Single atomic action (if treating as atomic) |
| Queue | `Seq(Element)` with Append/Head/Tail |
| Counter | `Nat` with increment/decrement |

### Step 2.3: Decide What to Model

**Include:**
- State transitions that affect correctness
- Concurrent access patterns
- Ordering dependencies between operations

**Exclude:**
- Error handling paths (unless modeling failure modes)
- Logging and diagnostics
- Performance optimizations that don't affect correctness
- Memory management details

---

## Phase 3: Write TLA+ Specification

### Step 3.1: Module Header and Constants

```tla
---------------------------- MODULE ModuleName ----------------------------
EXTENDS Naturals, Sequences, FiniteSets

\* Configuration constants
CONSTANTS
    Threads,          \* Set of threads/processes
    MaxValue          \* Bounds for model checking

\* State constants (if using state machine)
CONSTANTS
    State_Init,
    State_Active,
    State_Done
```

### Step 3.2: Variables

```tla
VARIABLES
    state,            \* Current state of the system
    counter,          \* Example counter variable
    pc                \* Program counter for each thread (if multi-threaded)

vars == << state, counter, pc >>
```

### Step 3.3: Type Invariant

```tla
TypeOk ==
    /\ state \in {State_Init, State_Active, State_Done}
    /\ counter \in Nat
    /\ counter <= MaxValue
    /\ pc \in [Threads -> PCStates]
```

### Step 3.4: Initial State

```tla
Init ==
    /\ state = State_Init
    /\ counter = 0
    /\ pc = [t \in Threads |-> PC_Start]
```

### Step 3.5: Actions

For each significant operation identified in Phase 1:

```tla
\* Action: Description of what this action models. This description should describe the effect of the action on the state of the system and role of this code in the overall system behavior.
\* Source: functionName() in source.cpp
ActionName(thread) ==
    /\ pc[thread] = PC_Ready           \* Guard: when can this happen?
    /\ state = State_Active            \* Additional guards
    /\ counter' = counter + 1          \* State changes
    /\ pc' = [pc EXCEPT ![thread] = PC_Next]
    /\ UNCHANGED << state >>           \* Explicitly unchanged variables
```

**Action naming conventions:**
- Use descriptive names matching the source function
- Include thread/process parameter if per-entity
- Add comments referencing source code location

### Step 3.6: Next State Relation

```tla
Next ==
    \/ \E t \in Threads : ActionName(t)
    \/ \E t \in Threads : AnotherAction(t)
    \/ SystemWideAction

\* Stuttering step (optional, for liveness)
Spec == Init /\ [][Next]_vars
```

### Step 3.7: Check Specification Syntax with TLC Parser SANY

If available, check specification syntax with TLA+ MCP tool `tlaplus_mcp_sany_parse`.

---

## Phase 4: Propose Properties

### Step 4.1: Safety Invariants

Safety invariants are state exspressions that must be true in every state:

```tla
\* No negative counter
CounterNonNegative == counter >= 0

\* Mutual exclusion
MutualExclusion ==
    Cardinality({t \in Threads : pc[t] = PC_Critical}) <= 1

\* State consistency
StateConsistency ==
    state = State_Done => counter > 0
```

Check safety invariants with TLA+ MCP tool `tlaplus_mcp_tlc_check`.

**Common safety patterns:**
| Pattern | Invariant |
|---------|-----------|
| No overflow | `counter <= MaxValue` |
| Mutual exclusion | At most one thread in critical section |
| No resource leak | Resources acquired = resources released |
| State validity | State machine only in valid states |

### Step 4.2: Safety Properties

Safety properties are temporal properties that state what must be true at all times:

```tla

\* Actions happen in order
OrderedActions ==
    [][pc = PC_Step1 => (pc' = PC_Step2)]_pc

```

Check safety properties with TLA+ MCP tool `tlaplus_mcp_tlc_check`.

### Step 4.2: Liveness Properties

Liveness properties state what must **eventually** happen:

```tla
\* Every thread eventually completes
EventualCompletion ==
    \A t \in Threads : <>(pc[t] = PC_Done)

\* Counter eventually increases
EventualProgress ==
    counter < MaxValue ~> counter >= MaxValue

\* If disconnect is requested, it eventually completes
DisconnectCompletes ==
    [](disconnectRequested => <>(state = State_Disconnected))
```

Check liveness properties with TLA+ MCP tool `tlaplus_mcp_tlc_check`.

---

## Output Format

After completing the phases, present:

### 1. English Summary

```markdown
## Code Analysis Summary

### Purpose
[One paragraph describing what the code does]

### Key Functions
- `function1`: [purpose]
- `function2`: [purpose]

### State Variables
- `var1`: [what it tracks]
- `var2`: [what it tracks]

### Concurrency Model
[How threads/processes interact]
```

### 2. TLA+ Specification

Complete, runnable TLA+ module.

### 3. Properties Summary

```markdown
## Proposed Properties

### Safety Invariants
1. **InvariantName**: [what it ensures]
2. **InvariantName**: [what it ensures]

### Liveness Properties
1. **PropertyName**: [what must eventually happen]

### Recommended Checks
- [ ] Run TLC with small bounds first
- [ ] Verify TypeOk holds
- [ ] Check for deadlock
```

---

## Example: Modeling a Reference Counter

**Source code pattern:**
```cpp
std::atomic<int32_t> counter {0};

bool reserve() {
    if (counter.fetch_add(1) >= 0) {
        return true;
    } else {
        release();
        return false;
    }
}

void release() {
    if (counter.fetch_sub(1) == threshold) {
        finish();
    }
}
```

**TLA+ abstraction:**
```tla
VARIABLES counter, finished

Reserve(thread) ==
    /\ counter >= 0
    /\ counter' = counter + 1
    /\ UNCHANGED finished

Release(thread) ==
    /\ counter > 0
    /\ counter' = counter - 1
    /\ finished' = IF counter' = 0 THEN TRUE ELSE finished

\* Safety: counter never goes negative while active
CounterSafety == finished = FALSE => counter >= 0
```

---

## Tips for Effective Modeling

1. **Start simple**: Model the happy path first, add error handling later
2. **Use small bounds**: `Threads = {T1, T2}`, `MaxValue = 3` for initial checks
3. **Name constants descriptively**: `State_Connecting` not `S1`
4. **Comment actions**: Reference source code locations
5. **Verify incrementally**: Check TypeOk and basic invariants before complex properties
6. **Abstract atomicity**: If source uses locks, model locked region as single action

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Model too detailed | Focus on state changes, not implementation steps |
| Missing UNCHANGED | Every variable must be primed or in UNCHANGED |
| Unbounded state | Add finite bounds for model checking |
| Implicit assumptions | Make all preconditions explicit guards |
| Modeling syntax, not semantics | Understand what code does, not how it's written |
