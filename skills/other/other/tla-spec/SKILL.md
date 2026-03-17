---
name: tla-spec
description: TLA+ specification correctness guide — evidence-backed methodology for writing correct temporal logic specs, covering canonical form, abstraction selection, safety/liveness decomposition, fairness, TLC soundness, and distributed systems patterns, with every rule grounded in literature
user-invocable: true
---

# TLA+ Specification Correctness Guide

A phased methodology for writing **correct** TLA+ specifications. Every rule,
pattern, and recommendation traces to established literature, Lamport's own
specifications, or battle-tested industrial practice. No guessing.

This skill guides you through specification from foundations to model checking
configuration. Follow the phases in order for new specs; jump to specific phases
for targeted reviews.

## Evidence Base

| ID | Source | Key Principle |
|----|--------|---------------|
| M1 | Lamport, *Specifying Systems* (2002) | Canonical form: `Init /\ [][Next]_vars /\ Fairness` |
| M2 | Lamport, *Specifying Systems* Ch. 6 | Stuttering: `[][Next]_vars` permits stuttering steps; compositional refinement |
| M3 | Lamport, *Specifying Systems* Ch. 8 | Liveness: temporal properties, fairness as specification component |
| M4 | Lamport, *The Temporal Logic of Actions* (1994) | Weak vs strong fairness definitions and selection criteria |
| M5 | Lamport, *Specifying Systems* Ch. 5 | UNCHANGED: every action must specify all unmodified variables |
| M8 | Lamport, *Specifying Systems* Ch. 2-4 | Abstraction: model WHAT not HOW, separate interface from implementation |
| M9 | Lamport, TLA+ community practice | TypeOK as first invariant constraining variable domains |
| M10 | Newcombe et al., CACM 2015 | AWS experience: 3-5 processes sufficient for most design bugs |
| M11 | TLC reference manual | TLC config options and their soundness guarantees |
| M12 | Yu et al., *Model Checking TLA+ Specifications* (1999) | TLC implementation, symmetry reduction, state constraints |
| M14 | Lamport, *Specifying Systems*; Raft TLA+ spec | Distributed systems patterns in TLA+ |
| M16 | Lamport, *A PlusCal User's Manual* (2009) | PlusCal as algorithmic specification language compiling to TLA+ |

## Confidence Tiers

Every rule is tagged with a confidence tier. Higher tiers have stronger evidence
and should be followed more strictly.

| Tier | Meaning | Compliance |
|------|---------|------------|
| **T1** | High confidence, strong evidence from multiple sources | Non-negotiable for correctness |
| **T2** | Good evidence, note caveats | Strong default, deviate with documented reason |
| **T3** | Use with caution, limited evidence | Useful guidance, verify in your context |

## When to Use

- Writing a new TLA+ specification for any protocol or algorithm
- Reviewing an existing TLA+ specification for correctness
- Adding liveness properties to a safety-only specification
- Configuring TLC for model checking
- Modeling distributed systems protocols (consensus, replication, leader election)
- Deciding between PlusCal and TLA+ for a new specification

## When NOT to Use

- Writing implementation code (this is about specifications, not programs)
- Working with other formal methods (Alloy, SPIN, Coq) — different tools, different rules
- Simple sequential algorithms where testing suffices
- When you need a TLA+ syntax tutorial (this assumes basic TLA+ literacy)

---

## Phase 1: Specification Foundations

Establish the structural skeleton of a correct specification. Every TLA+
specification must satisfy these non-negotiable fundamentals before any
properties are checked.

### 1.1 Canonical Form [T1, M1, P4.1.F1]

Use the canonical form as the **default template** for all specifications.

**Safety-only specification** (no liveness requirements):

```tla
---- MODULE MyProtocol ----
EXTENDS Integers, Sequences, FiniteSets, TLC

CONSTANTS
    Node,       \* Set of participating nodes
    MaxValue    \* Domain bound for model checking

VARIABLES
    state,      \* Per-node local state
    msgs        \* Set of in-flight messages (or Bag for realism)

vars == <<state, msgs>>

------------------------------------------------------------
\* Type invariant — ALWAYS define first [T1, M9]
TypeOK ==
    /\ state \in [Node -> {"idle", "active", "done"}]
    /\ msgs \subseteq MessageType

------------------------------------------------------------
\* Initial state
Init ==
    /\ state = [n \in Node |-> "idle"]
    /\ msgs = {}

------------------------------------------------------------
\* Actions — each MUST specify UNCHANGED for all unmodified variables [T1, M5]
ActionA(n) ==
    /\ state[n] = "idle"
    /\ state' = [state EXCEPT ![n] = "active"]
    /\ UNCHANGED <<msgs>>

ActionB(n) ==
    /\ state[n] = "active"
    /\ msgs' = msgs \cup {[type |-> "done", from |-> n]}
    /\ UNCHANGED <<state>>

------------------------------------------------------------
\* Next-state relation
Next ==
    \E n \in Node :
        \/ ActionA(n)
        \/ ActionB(n)

------------------------------------------------------------
\* Specification — canonical form
Spec == Init /\ [][Next]_vars

====
```

**Safety + liveness specification** (add fairness only when needed):

```tla
\* Add ONLY for liveness properties [T1, M1, M3]
Fairness ==
    /\ \A n \in Node : WF_vars(ActionA(n))
    /\ \A n \in Node : WF_vars(ActionB(n))

Spec == Init /\ [][Next]_vars /\ Fairness
```

> **Caveat [P4.1.F1]**: Canonical form is a *default template*, not a law.
> Lamport himself deviates in some specifications (e.g., omitting fairness
> entirely for safety-only specs, using different temporal formulas for
> specific refinement mappings). If you deviate, document WHY with a
> reference to the specific pattern you are following.

### 1.2 Stuttering Invariance Checklist [T1, M2, M5]

Stuttering steps (where no variable changes) are fundamental to TLA+ and
enable compositional refinement. The `[][Next]_vars` form explicitly permits
them — this is not optional.

```
STUTTERING CHECKLIST
────────────────────
[ ] Specification uses [][Next]_vars (NOT [][Next])
    → [][Next] without _vars FORBIDS stuttering and breaks refinement.
    → The ONLY valid form is [][Next]_vars where vars is the
      tuple of ALL specification variables.

[ ] vars tuple contains ALL declared VARIABLES
    → If you add a variable, update the vars tuple immediately.
    → Missing a variable from vars silently permits arbitrary changes to it.

[ ] Every action specifies UNCHANGED for ALL unmodified variables
    → An action that mentions v1' but not v2' leaves v2 unconstrained.
    → TLC will explore states where v2 takes ANY value in its type domain.
    → This is the #1 source of spurious counterexamples.
```

**Variable grouping pattern** for specs with many variables:

```tla
\* Group related variables for manageable UNCHANGED clauses
nodeVars    == <<state, epoch>>
networkVars == <<msgs, delivered>>
configVars  == <<members, leader>>

vars == <<nodeVars, networkVars, configVars>>

\* Actions use group UNCHANGED
SendMessage(n) ==
    /\ ...
    /\ msgs' = msgs \cup {msg}
    /\ UNCHANGED <<nodeVars, configVars, delivered>>
```

### 1.3 TypeOK as First Invariant [T1, M9]

TypeOK constrains the domains of all variables. It is always the first
invariant you write and the first invariant you check.

**Why TypeOK matters**:
- Catches variable domain errors before expensive property checking
- Acts as a sanity check that Init and Next are well-formed
- Provides a foundation for TLAPS proofs (type correctness is a proof obligation)
- Rapidly detects missing UNCHANGED clauses (unconstrained variables violate TypeOK)

**TypeOK construction rules**:

```
TYPEOK CONSTRUCTION
───────────────────
[ ] Every VARIABLE appears in TypeOK

[ ] TypeOK constrains variables to finite domains for TLC
    → "x \in Nat" is valid TLA+ but NOT model-checkable
    → Use "x \in 0..MaxBound" for model checking

[ ] TypeOK is checked BEFORE other invariants
    → In the TLC config: INVARIANT TypeOK, SafetyProp1, SafetyProp2
    → TypeOK violations are always the first thing to debug

[ ] Function-valued variables use domain constraints
    → state \in [Node -> StatusSet] not just "state is a function"
    → Check both the domain AND the range
```

**TypeOK patterns by variable type**:

| Variable Type | TypeOK Pattern | Example |
|---------------|----------------|---------|
| Simple value | `v \in DomainSet` | `epoch \in Nat` (or `0..MaxEpoch` for TLC) |
| Function | `v \in [Domain -> Range]` | `state \in [Node -> {"idle","active"}]` |
| Set | `v \subseteq BaseSet` | `msgs \subseteq MessageType` |
| Sequence | `v \in Seq(ElemType)` | `log \in Seq(Entry)` (use `BSeq(Entry, MaxLen)` for TLC) |
| Record | `v \in [field1: T1, field2: T2]` | `msg \in [type: MsgTypes, from: Node]` |
| Optional | `v \in T \cup {None}` | `leader \in Node \cup {None}` |
| Bag/Multiset | Custom predicate | `BagToSet(msgs) \subseteq MessageType` |

---

## Phase 2: Abstraction and Modeling

Select the right level of abstraction BEFORE writing specification logic.
Wrong abstraction is the most expensive specification error — it wastes
model-checking time on irrelevant detail or misses real bugs by
over-abstracting.

### 2.1 Seven-Step Abstraction Framework [T2, P3.1, M8]

Follow these steps in order when starting a new specification.

**Step 1: State the property first**

Before modeling any behavior, write down the property you want to verify
in plain English. This determines what MUST be in the specification and
what can be abstracted away.

```
Example:
  Property: "No two nodes hold the lock simultaneously"
  → Need: lock state per node
  → Don't need: network packet format, serialization, retry timers
```

**Step 2: Identify minimal state**

List the minimum set of variables needed to express the property from Step 1.
Every variable must appear in at least one property or be necessary for
computing a variable that does.

```
Minimal state test: For each variable, ask:
  "If I remove this variable, can I still express all my properties?"
  If yes → remove it.
```

**Step 3: Model the environment as nondeterminism**

Do not model external systems (clients, networks, OS) in detail. Replace
them with nondeterministic choices that capture all possible behaviors.

```tla
\* BAD: modeling a specific client
ClientSend == /\ clientState = "ready"
              /\ clientState' = "waiting"
              /\ ...

\* GOOD: nondeterministic environment
ReceiveRequest(n) == \* A request can arrive at any node, any time
    /\ state[n] = "idle"
    /\ state' = [state EXCEPT ![n] = "processing"]
    /\ UNCHANGED <<...>>
```

**Step 4: Choose communication model**

| Model | TLA+ Representation | Use When | Tradeoff |
|-------|-------------------|----------|----------|
| Set of messages | `msgs \subseteq MsgType` | Safety properties only | Simplest; loses ordering and duplicates |
| Bag (multiset) | `msgs \in BagType` | Need duplicate detection | Realistic; moderate complexity |
| Sequence per link | `chan \in [Link -> Seq(MsgType)]` | FIFO ordering required | Most complex; needed for TCP-like channels |

> **[T2, P3.4, M14]**: For most distributed protocol specifications, start
> with a **set** model. Upgrade to bag/sequence only if a property depends
> on message ordering or duplicate counting.

**Step 5: Separate WHAT from HOW**

Specify the intended behavior, not the implementation mechanism.

```tla
\* BAD: specifying HOW (implementation detail)
AcquireLock(n) ==
    /\ Send([type |-> "lock_req", from |-> n])
    /\ WaitForReply(n)
    /\ ProcessReply(n)

\* GOOD: specifying WHAT (observable behavior)
AcquireLock(n) ==
    /\ lock = None
    /\ lock' = n
    /\ UNCHANGED <<...>>
```

**Step 6: Diagnose over/under-specification**

| Symptom | Diagnosis | Fix |
|---------|-----------|-----|
| TLC explores billions of states for a 3-node model | Over-specified (too much detail) | Remove implementation-level state |
| Safety property passes but system is clearly wrong | Under-specified (missing behaviors) | Add actions for failure cases, concurrent operations |
| Liveness property fails with trivial counterexample | Missing fairness or missing actions | Check that all intended behaviors have actions |
| No errors but the spec "feels wrong" | Wrong abstraction level | Return to Step 1, re-examine the property |

**Step 7: Refine incrementally**

Start with the simplest correct spec and add detail only when needed to
express properties that the simpler spec cannot. Each refinement step
should be verifiable: the refined spec should refine (implement) the
abstract spec.

### 2.2 Ten Distributed Systems Patterns [T2, P3.4, M14]

Common modeling patterns for distributed protocols. Each pattern includes
the TLA+ idiom and notes on when to use it.

#### Pattern 1: Quorum

```tla
\* Abstract: CONSTANT set of quorums
CONSTANT Quorum
ASSUME QuorumAssumption ==
    /\ \A Q \in Quorum : Q \subseteq Node
    /\ \A Q1, Q2 \in Quorum : Q1 \cap Q2 /= {}

\* OR computed majority (simpler for symmetric systems)
Quorum == {S \in SUBSET Node : Cardinality(S) * 2 > Cardinality(Node)}
```

> For model checking, the computed form is often better (no need to
> enumerate quorums in the config). For proof, the abstract CONSTANT
> form is more general.

#### Pattern 2: Epoch / Term (Monotonic Counter)

```tla
\* Per-node monotonic epoch
VARIABLE currentEpoch  \* currentEpoch \in [Node -> Nat]

\* Epoch advances are strictly increasing per node
AdvanceEpoch(n) ==
    /\ currentEpoch' = [currentEpoch EXCEPT ![n] = currentEpoch[n] + 1]
    /\ ...

\* Stale-epoch rejection
ProcessMessage(n, msg) ==
    /\ msg.epoch >= currentEpoch[n]  \* reject stale
    /\ ...
```

#### Pattern 3: Leader Election (Nondeterministic)

```tla
\* Abstract leader election — nondeterministic candidacy
BecomeLeader(n) ==
    /\ \A m \in Node : leader[m] /= n  \* not already leader
    /\ leader' = [leader EXCEPT ![n] = n]
    /\ currentEpoch' = [currentEpoch EXCEPT ![n] = currentEpoch[n] + 1]
    /\ UNCHANGED <<...>>
```

> Do NOT model the election protocol (Raft, ZAB) unless you are
> verifying the election protocol itself. Abstract it as nondeterministic
> leader selection with appropriate constraints.

#### Pattern 4: Timeout (Always-Enabled Action, NO Clock)

```tla
\* BAD: modeling a clock for timeouts
Timeout(n) ==
    /\ clock[n] >= deadline[n]  \* NO — do not model clocks
    /\ ...

\* GOOD: timeout as an always-enabled action
Timeout(n) ==
    /\ state[n] = "waiting"
    /\ state' = [state EXCEPT ![n] = "timed_out"]
    /\ UNCHANGED <<...>>
\* Timeout can fire at ANY time a node is waiting — this captures
\* all possible timeout behaviors without modeling time.
```

> **[T1]**: Never model real-time clocks in a TLA+ specification unless
> you are specifically verifying real-time properties. Timeouts are
> modeled as always-enabled actions that capture the nondeterminism of
> when they fire.

#### Pattern 5: Log Replication (Sequence with Truncate-Overwrite)

```tla
\* Log as sequence with append and truncate-overwrite
VARIABLE log  \* log \in [Node -> Seq(Entry)]

AppendEntry(n, entry) ==
    /\ log' = [log EXCEPT ![n] = Append(log[n], entry)]
    /\ UNCHANGED <<...>>

TruncateAndOverwrite(n, idx, entries) ==
    /\ log' = [log EXCEPT ![n] = SubSeq(log[n], 1, idx) \o entries]
    /\ UNCHANGED <<...>>
```

#### Pattern 6: Membership Change (Config as Log Entry)

```tla
\* Joint consensus: configuration transitions via log
VARIABLE config  \* config \in [Node -> SUBSET Node]

\* Configuration change is a special log entry
ProposeConfigChange(leader, newMembers) ==
    /\ AppendEntry(leader, [type |-> "config", members |-> newMembers])
    /\ config' = [config EXCEPT ![leader] = config[leader] \cup newMembers]
    /\ UNCHANGED <<...>>
```

#### Pattern 7: Idempotency (Accumulating Set)

```tla
\* Track processed operation IDs to ensure idempotency
VARIABLE processed  \* processed \in [Node -> SUBSET OpId]

ProcessOp(n, op) ==
    /\ op.id \notin processed[n]  \* skip if already processed
    /\ \* ... perform operation ...
    /\ processed' = [processed EXCEPT ![n] = processed[n] \cup {op.id}]
    /\ UNCHANGED <<...>>
```

#### Pattern 8: Two-Phase Protocol (Prepare-Collect-Decide)

```tla
\* Two-phase pattern: prepare → collect votes → decide
VARIABLE phase    \* [Node -> {"idle", "prepare", "decide"}]
VARIABLE votes    \* [Node -> SUBSET Node]

Prepare(n) ==
    /\ phase[n] = "idle"
    /\ phase' = [phase EXCEPT ![n] = "prepare"]
    /\ votes' = [votes EXCEPT ![n] = {}]
    /\ \* send prepare messages
    /\ UNCHANGED <<...>>

ReceiveVote(n, voter) ==
    /\ phase[n] = "prepare"
    /\ votes' = [votes EXCEPT ![n] = votes[n] \cup {voter}]
    /\ UNCHANGED <<...>>

Decide(n) ==
    /\ phase[n] = "prepare"
    /\ votes[n] \in Quorum  \* collected a quorum
    /\ phase' = [phase EXCEPT ![n] = "decide"]
    /\ UNCHANGED <<...>>
```

> Pair with a refinement mapping to show this implements a simpler
> atomic specification. [T2]

#### Pattern 9: Failure and Restart (Durable vs Volatile State)

```tla
\* Failure: volatile state lost, durable state preserved
VARIABLE volatileState  \* lost on restart
VARIABLE durableState   \* preserved on restart

Crash(n) ==
    /\ volatileState' = [volatileState EXCEPT ![n] = InitVolatile]
    /\ UNCHANGED <<durableState, ...>>
    \* Durable state is UNCHANGED — this is the key invariant

Restart(n) ==
    /\ \* recover from durableState[n]
    /\ volatileState' = [volatileState EXCEPT
                           ![n] = RecoverFrom(durableState[n])]
    /\ UNCHANGED <<durableState, ...>>
```

#### Pattern 10: Ghost Variables (Append-Only History)

```tla
\* Ghost variable: records history for property checking
\* Does NOT affect system behavior — only used in invariants/properties
VARIABLE history  \* history \in Seq(Event)

\* Append to history in every action that is relevant
ActionWithHistory(n) ==
    /\ \* ... normal action logic ...
    /\ history' = Append(history, [type |-> "action", node |-> n, ...])
    /\ UNCHANGED <<...>>

\* Use ghost variable in properties
NoDoubleCommit ==
    \A i, j \in 1..Len(history) :
        /\ history[i].type = "commit"
        /\ history[j].type = "commit"
        /\ history[i].key = history[j].key
        => history[i].value = history[j].value
```

> Ghost variables are specification-only artifacts. They are
> append-only (history never shrinks) and used solely to express
> properties that reference past states. Mark them clearly in comments.

---

## Phase 3: Safety Verification

After establishing the specification structure (Phase 1) and modeling
decisions (Phase 2), verify safety properties.

### 3.1 Safety Specification Checklist [T1, M9, M5]

```
SAFETY CHECKLIST
────────────────
[ ] TypeOK is defined and checked first
    → Every variable constrained to its domain [T1, M9]

[ ] All safety invariants expressed as state predicates
    → "P is always true" written as INVARIANT P in TLC config
    → For action properties, use [][ActionProp]_vars form

[ ] Deadlock-freedom checked between safety and liveness phases
    → TLC checks deadlock by default (all states have a Next step)
    → Intentional termination: add a Done action or use
      PROPERTY [][Next]_vars => <>[]done to distinguish
    → [P4.4.F6]: ALWAYS check deadlock-freedom after safety passes
      but BEFORE adding liveness. A deadlocked spec trivially
      satisfies some liveness properties (vacuous truth).

[ ] No CONSTRAINT in the TLC config for the final check
    → CONSTRAINT is acceptable during development to speed iteration
    → CONSTRAINT MUST be removed for the final safety verification
    → [T1, M11]: CONSTRAINT can hide states reachable via longer paths

[ ] Invariants are inductive (for TLAPS proofs)
    → An invariant I is inductive if: I /\ Next => I'
    → TypeOK is typically inductive; complex safety properties
      may need strengthening (adding auxiliary conjuncts)
```

### 3.2 Deadlock-Freedom Gate [T1, P4.4.F6]

**This check is mandatory between the safety and liveness phases.**

A specification deadlocks if some reachable state has no Next step enabled.
TLC checks this by default. However:

1. If your protocol has intentional termination, you must distinguish it
   from unintentional deadlock:

```tla
\* Termination action — prevents false deadlock reports
Done ==
    /\ AllNodesFinished
    /\ UNCHANGED vars

Next == ActionA \/ ActionB \/ ... \/ Done
```

2. A deadlocked spec can **vacuously satisfy liveness properties**.
   If the system deadlocks in a state where the liveness property is
   already satisfied, TLC will report no error. This is not a real
   liveness guarantee.

```
DEADLOCK GATE
─────────────
[ ] TLC reports zero deadlock states
    OR
[ ] All "deadlock" states are intentional termination states
    AND they are documented in the spec
    AND a Done action is present
```

### 3.3 TLC Safety Configuration [T1, M11, M12]

Recommended TLC configuration for safety checking:

```
\* MyProtocol.cfg — safety checking configuration
SPECIFICATION Spec

\* Type invariant first, then safety properties
INVARIANT TypeOK
INVARIANT SafetyProperty1
INVARIANT SafetyProperty2

\* State constraint for development ONLY — remove for final check
\* CONSTRAINT StateConstraint

\* Symmetry sets — safe for safety properties [T1, M11]
SYMMETRY NodeSymmetry

\* Constants
CONSTANT Node = {n1, n2, n3}
CONSTANT MaxValue = 3
```

| TLC Option | Safety Checking | Notes |
|------------|----------------|-------|
| `INVARIANT` | Sound | Always use for state predicates |
| `CONSTRAINT` | Sound but incomplete | May miss states reachable via longer paths; remove for final check |
| `SYMMETRY` | Sound if symmetry set is correct | Incorrect symmetry sets produce unsound results silently |
| `VIEW` | Sound | Reduces state space via abstraction |
| `ACTION_CONSTRAINT` | Sound | Restricts which actions TLC explores |

---

## Phase 4: Liveness Verification

Liveness properties ("something good eventually happens") require fairness
assumptions and careful TLC configuration. This is where most soundness
errors occur.

### 4.1 Six-Phase Liveness Methodology [T1, M3, P3.2, P3.3]

Follow these phases strictly in order.

**Phase L1: Write safety first (complete Phase 3)**

Never add liveness to a specification that has not passed safety checking.
Liveness debugging on an incorrect safety spec is wasted effort.

**Phase L2: Identify liveness requirements**

Write down what MUST eventually happen in plain English:

```
Examples:
  - "Every request eventually receives a response"
  - "Every node eventually learns of every update"
  - "The leader eventually commits every proposed entry"
  - "The system eventually reaches a stable configuration"
```

Express each as a temporal formula:

```tla
\* "Every request eventually receives a response"
Liveness1 == \A r \in requests : <>(responded[r])

\* "The leader eventually commits" (conditional on leadership)
Liveness2 == []<>(committed = proposed)

\* Response: "always eventually" (repeated liveness)
Liveness3 == []<>(\E n \in Node : state[n] = "active")
```

**Phase L3: Select fairness — WF first, SF only when needed [T2, M4, P3.3]**

Use the fairness selection decision table:

| Condition | Fairness | Rationale |
|-----------|----------|-----------|
| Action is continuously enabled once enabled | `WF_vars(Action)` | WF suffices: if enabled forever, it eventually happens |
| Action is repeatedly enabled then disabled (intermittent) | `SF_vars(Action)` | SF needed: must happen if repeatedly enabled, even if intermittently disabled |
| Action represents environment/external input | **No fairness** | Never make the environment fair — it models adversarial behavior |
| Action is the composite `Next` | **No fairness on `Next` alone** | `WF_vars(Next)` says "some action happens" but does not guarantee WHICH action happens; useless for most properties |
| Timeout action | Usually no fairness | Timeouts model nondeterminism; fairness on timeouts constrains which timeouts fire |

**WF vs SF decision procedure**:
1. Start with `WF_vars(A)` for every system action A
2. Check if TLC finds a liveness counterexample
3. If the counterexample shows Action A repeatedly enabled then disabled
   without executing, upgrade to `SF_vars(A)` for that specific action
4. **Never** start with SF — it is a stronger assumption and may hide
   real liveness bugs

> **[T2, M4]**: Lamport's convention: "Weak fairness is almost always
> what you want." Strong fairness is needed only for actions that are
> intermittently disabled by other actions (e.g., a receive action that
> is enabled only when a message is in transit, and messages can be
> repeatedly consumed and re-sent).

**Phase L4: Verify machine closure (automatic in canonical form)**

A specification `Spec == Init /\ [][Next]_vars /\ Fairness` is
machine-closed if the safety part (`Init /\ [][Next]_vars`) does not
constrain which infinite behaviors are possible (only fairness does that).

In the canonical form, machine closure is **guaranteed** [T1, M1].
You only need to worry about machine closure if you deviate from canonical
form (e.g., adding raw temporal formulas to the spec).

**Phase L5: Model-check liveness [T1, P3.2, M11, M12]**

**THIS IS THE CRITICAL STEP.** TLC's liveness checking has soundness
traps that do not exist in safety checking.

```
LIVENESS MODEL-CHECKING RULES
──────────────────────────────
[ ] REMOVE all CONSTRAINT directives from the TLC config
    → CONSTRAINT + liveness = UNSOUND [T1, M11]
    → CONSTRAINT can hide infinite behaviors that violate liveness
    → This is NON-NEGOTIABLE for liveness checking

[ ] REMOVE all SYMMETRY directives from the TLC config
    → SYMMETRY + liveness = DANGEROUS [T1, M11]
    → Symmetry reduction may cause TLC to miss liveness violations
    → It is sometimes safe but the conditions are subtle;
      removing it is always safe

[ ] Use -lncheck final for production liveness verification
    → -lncheck final performs the complete liveness check
    → Without -lncheck, TLC may use an incomplete algorithm

[ ] Liveness properties go in PROPERTY (not INVARIANT)
    → INVARIANT is for state predicates (safety)
    → PROPERTY is for temporal formulas (liveness)
```

**Phase L6: Debug liveness failures [T1, P3.2]**

TLC liveness counterexamples have a **lasso structure**: a finite prefix
followed by a back-loop to a previously visited state. The back-loop
represents an infinite behavior where the liveness property is never
satisfied.

```
Lasso structure:
  s0 → s1 → s2 → ... → sk → ... → sj
                               ↑        |
                               └────────┘
                             (back-loop: infinite repetition)

Debugging procedure:
1. Read the finite prefix: how does the system reach state sk?
2. Read the back-loop: what actions repeat forever?
3. Check: is there an action that SHOULD fire but doesn't?
   → If yes: add or strengthen fairness for that action
4. Check: is the counterexample realistic?
   → Unrealistic: the environment acts adversarially in a way your
     system need not tolerate. Consider if your liveness requirement
     is too strong.
   → Realistic: the protocol has a liveness bug. Fix the protocol.
5. Check: does the back-loop involve only stutter steps?
   → If yes: your specification may be missing an action.
```

### 4.2 Complete TLC Soundness Matrix [T1, M11, M12]

This is the complete map of TLC configuration options versus soundness
for safety and liveness checking. **Reference this table before every
TLC run.**

| Config Option | Safety | Liveness | Risk | Recommendation |
|---------------|--------|----------|------|----------------|
| **INVARIANT** | Sound | N/A (wrong directive) | None for safety | Use for state predicates |
| **PROPERTY** | N/A (wrong directive) | Sound (with caveats below) | None | Use for temporal formulas |
| **CONSTRAINT** | Sound (but incomplete) | **UNSOUND** | High: hides reachable states from liveness check | Remove for final liveness check; acceptable during development for safety only |
| **SYMMETRY** | Sound (if correct) | **Dangerous** | Medium: may miss counterexamples | Remove for liveness; use only for safety with verified symmetry set |
| **VIEW** | Sound | **Unverified** | Medium: hash collisions possible | Use with caution; verify key results without VIEW |
| **ACTION_CONSTRAINT** | Sound | **Context-dependent** | Medium: may prevent actions needed for liveness counterexample | Review carefully for liveness |
| **-lncheck final** | N/A | Required for soundness | High if omitted: may use incomplete algorithm | Always use for production liveness checks |
| **-workers N** (N>1) | Sound | Sound (TLC 2.18+) | Low: older TLC versions had bugs with multi-worker liveness | Use current TLC version |

> **[T1, P3.2]**: The safe liveness workflow: (1) pass all safety checks
> with CONSTRAINT/SYMMETRY, (2) remove CONSTRAINT and SYMMETRY,
> (3) add PROPERTY directives, (4) run with `-lncheck final`,
> (5) accept the longer runtime.

---

## Phase 5: Model Checking Configuration

### 5.1 Small Model Heuristics [T2, M10, P4.4.F3]

AWS's experience (Newcombe et al., CACM 2015): **3-5 processes are
sufficient for finding most design bugs**. Start small, increase only
when needed.

| Model Size | When Sufficient | When Insufficient |
|------------|----------------|-------------------|
| 2 nodes | Mutual exclusion, simple leader-follower | Quorum-based protocols (need 3+) |
| 3 nodes | Most consensus protocols, quorum systems | Protocols with f+1 requirements where f>1 |
| 4-5 nodes | Complex fault-tolerance (f=1 with 2f+1) | Threshold-dependent bugs (e.g., f=2 requires 5+ nodes) |
| >5 nodes | Byzantine fault tolerance (3f+1) | Rarely needed for design verification |

> **Caveat [P4.4.F3]**: Small models miss:
> - **Threshold-dependent bugs**: Properties that only fail at specific
>   quorum sizes (e.g., a bug that manifests only with exactly 2 of 5
>   nodes failing)
> - **Symmetry-breaking bugs**: Bugs that require specific asymmetric
>   configurations
> - **Scaling-related issues**: Performance properties that degrade
>   non-linearly
>
> If your protocol has threshold-dependent behavior, test at least one
> configuration AT the threshold and one ABOVE it.

### 5.2 TLC Configuration Guide

**Development configuration** (fast iteration):

```
SPECIFICATION Spec
INVARIANT TypeOK
INVARIANT SafetyProperty
CONSTRAINT SmallStateConstraint   \* OK for safety development
SYMMETRY NodeSymmetry             \* OK for safety development
CONSTANT Node = {n1, n2, n3}     \* Start small
```

**Final safety configuration** (production):

```
SPECIFICATION Spec
INVARIANT TypeOK
INVARIANT SafetyProperty
\* NO CONSTRAINT — full state space
SYMMETRY NodeSymmetry             \* OK for safety (if correct)
CONSTANT Node = {n1, n2, n3}
```

**Final liveness configuration** (production):

```
SPECIFICATION Spec
INVARIANT TypeOK                  \* Keep safety checks active
PROPERTY LivenessProperty
\* NO CONSTRAINT — UNSOUND with liveness
\* NO SYMMETRY — DANGEROUS with liveness
CONSTANT Node = {n1, n2, n3}
```

**TLC command-line flags**:

| Flag | Purpose | When to Use |
|------|---------|-------------|
| `-workers auto` | Use all CPU cores | Always (production runs) |
| `-lncheck final` | Complete liveness check | Always for liveness verification |
| `-deadlock` | Disable deadlock checking | Only if spec has intentional terminal states AND Done action is present |
| `-depth N` | Limit search depth | Development only; never for final verification |
| `-coverage N` | Print coverage stats every N minutes | Development; helps find unreachable actions |
| `-dump format file` | Dump state graph | Debugging counterexamples |
| `-simulate num=N` | Random simulation instead of full BFS | Very large state spaces where exhaustive check is infeasible |

### 5.3 Multi-Tool Awareness [T3, P4.3.F6, P4.4.F2]

TLC is not the only TLA+ verification tool. Be aware of alternatives
and their strengths.

| Tool | Technique | Strengths | Limitations |
|------|-----------|-----------|-------------|
| **TLC** | Explicit-state model checking | Complete for finite models; well-understood soundness; fast for small models | Exponential state explosion; finite models only |
| **Apalache** | Symbolic model checking (SMT) | Handles larger state spaces; bounded model checking for unbounded domains; type checking | Slower per-state; less mature than TLC; limited liveness support |
| **TLAPS** | Interactive theorem proving | Full mathematical proofs; unbounded verification; strongest guarantee | High manual effort; steep learning curve |
| **Quint** | Emerging: TLA+-like language with better tooling | Modern syntax; integrated testing; simulation | Not yet production-proven; subset of TLA+ expressiveness |

> **TLC-specific advice is marked throughout this skill.** Where behavior
> differs in Apalache, notes are included. However, this skill primarily
> targets TLC workflows. For Apalache-specific guidance, consult the
> Apalache documentation.
>
> **Apalache type annotations**: Apalache requires type annotations
> that TLC ignores. If you plan to use both tools, add Apalache type
> annotations as comments:
> ```tla
> \* @type: Set(NODE) => Bool;
> IsQuorum(S) == Cardinality(S) * 2 > Cardinality(Node)
> ```

---

## Phase 6: PlusCal Considerations [T3, M16, P4.4.F1]

PlusCal is a higher-level algorithmic language that compiles to TLA+.
It is a valid choice for certain specifications.

### 6.1 PlusCal Decision Table

| Factor | PlusCal | Raw TLA+ |
|--------|---------|----------|
| **Author familiarity** | Imperative/sequential programming | Set theory, temporal logic |
| **Specification type** | Sequential or simple concurrent algorithms | Complex concurrent/distributed protocols |
| **Expressiveness ceiling** | Limited: sequential composition, limited nondeterminism | Full: arbitrary temporal logic, flexible composition |
| **Compilation** | Compiles to TLA+ (can inspect/modify output) | Direct |
| **Fairness** | Automatic per-process fairness | Manual fairness specification |
| **Best for** | Teaching, prototyping, algorithm verification | Protocol verification, refinement, industrial use |

> **[T3, P4.4.F1]**: A finished PlusCal specification is better than an
> unfinished TLA+ specification. If PlusCal gets you to a checkable spec
> faster, use it. But know the ceiling: PlusCal cannot express all TLA+
> patterns (e.g., arbitrary interleaving of non-process actions, complex
> fairness, stuttering-sensitive refinement).
>
> **When to switch from PlusCal to TLA+**:
> - You need fairness on individual actions (not just processes)
> - You need to compose specifications via refinement
> - You need ghost variables that participate in the temporal formula
> - PlusCal's process model does not match your system's concurrency model

---

## Common Mistakes Catalog

Mistakes ordered by frequency and severity. Each cites the research finding
that identifies it.

| # | Mistake | Consequence | Fix | Finding |
|---|---------|------------|-----|---------|
| 1 | Missing UNCHANGED for a variable | Variable is unconstrained; TLC explores all possible values | Add explicit UNCHANGED for every unmodified variable in every action | [T1, M5] |
| 2 | Using `[][Next]` instead of `[][Next]_vars` | Stuttering forbidden; breaks compositional refinement | Always use `_vars` subscript | [T1, M2] |
| 3 | CONSTRAINT in liveness config | **Unsound**: may hide liveness violations | Remove CONSTRAINT for all liveness checking | [T1, M11] |
| 4 | SYMMETRY in liveness config | **Dangerous**: may miss liveness counterexamples | Remove SYMMETRY for liveness checking | [T1, M11] |
| 5 | Fairness on environment actions | Over-constrains the model; hides real liveness bugs | Never apply fairness to actions representing external/adversarial behavior | [T2, M4] |
| 6 | Starting with SF instead of WF | Stronger assumption than needed; masks bugs | Start with WF, upgrade to SF only for intermittently disabled actions | [T2, M4, P3.3] |
| 7 | Fairness on composite Next only | Does not guarantee which sub-action executes | Apply fairness to individual actions, not Next | [T2, M4] |
| 8 | No TypeOK invariant | Domain errors caught late or not at all | Always define and check TypeOK first | [T1, M9] |
| 9 | Skipping deadlock check before liveness | Deadlocked spec can vacuously satisfy liveness | Check deadlock-freedom after safety, before liveness | [T1, P4.4.F6] |
| 10 | Modeling clocks for timeouts | Unnecessary complexity; wrong abstraction | Model timeouts as always-enabled nondeterministic actions | [T2, M14] |
| 11 | vars tuple missing a variable | That variable can change arbitrarily in stutter steps | Always verify vars contains ALL declared VARIABLES | [T1, M2, M5] |
| 12 | Using Nat instead of bounded range | TLC cannot enumerate infinite sets | Use `0..MaxBound` for model checking | [T1, M9, M12] |

---

## Quick Reference: Specification Template

Copy-paste starting point for a new distributed protocol specification:

```tla
---- MODULE ProtocolName ----
EXTENDS Integers, Sequences, FiniteSets, TLC

\*-------------------------------------------------------------
\* Constants
\*-------------------------------------------------------------
CONSTANTS
    Node,           \* Set of nodes (symmetry set for TLC)
    None            \* Sentinel: model value in TLC config

ASSUME NoneAssumption == None \notin Node

\*-------------------------------------------------------------
\* Variables
\*-------------------------------------------------------------
VARIABLES
    \* @type: NODE -> Str;
    state,          \* Per-node state
    \* @type: Set(MSG);
    msgs            \* Messages in flight (set model)

vars == <<state, msgs>>

\*-------------------------------------------------------------
\* Message constructors
\*-------------------------------------------------------------
Message == [type: {"request", "response"}, from: Node, to: Node]

\*-------------------------------------------------------------
\* Type invariant [T1, M9]
\*-------------------------------------------------------------
TypeOK ==
    /\ state \in [Node -> {"idle", "active", "done"}]
    /\ msgs \subseteq Message

\*-------------------------------------------------------------
\* Initial state
\*-------------------------------------------------------------
Init ==
    /\ state = [n \in Node |-> "idle"]
    /\ msgs = {}

\*-------------------------------------------------------------
\* Actions [T1, M5 — every action has explicit UNCHANGED]
\*-------------------------------------------------------------
SendRequest(sender, receiver) ==
    /\ state[sender] = "idle"
    /\ state' = [state EXCEPT ![sender] = "active"]
    /\ msgs' = msgs \cup {[type |-> "request",
                            from |-> sender,
                            to   |-> receiver]}

HandleRequest(n) ==
    /\ \E msg \in msgs :
        /\ msg.type = "request"
        /\ msg.to = n
        /\ state' = [state EXCEPT ![n] = "done"]
        /\ msgs' = (msgs \ {msg}) \cup
                    {[type |-> "response",
                      from |-> n,
                      to   |-> msg.from]}

HandleResponse(n) ==
    /\ \E msg \in msgs :
        /\ msg.type = "response"
        /\ msg.to = n
        /\ state' = [state EXCEPT ![n] = "done"]
        /\ msgs' = msgs \ {msg}

\*-------------------------------------------------------------
\* Next-state relation
\*-------------------------------------------------------------
Next ==
    \E n1, n2 \in Node :
        \/ SendRequest(n1, n2)
        \/ HandleRequest(n1)
        \/ HandleResponse(n1)

\*-------------------------------------------------------------
\* Fairness [T2, M4 — WF first, SF only if needed]
\*-------------------------------------------------------------
Fairness ==
    \A n \in Node :
        /\ WF_vars(HandleRequest(n))
        /\ WF_vars(HandleResponse(n))
    \* NO fairness on SendRequest — it is an environment/client action

\*-------------------------------------------------------------
\* Specification
\*-------------------------------------------------------------
\* Safety-only (check safety first):
SafetySpec == Init /\ [][Next]_vars

\* Full specification (add fairness for liveness):
Spec == Init /\ [][Next]_vars /\ Fairness

\*-------------------------------------------------------------
\* Safety properties
\*-------------------------------------------------------------
Safety1 == \A n \in Node :
    state[n] = "done" => \E msg \in msgs \cup {} : TRUE  \* placeholder

\*-------------------------------------------------------------
\* Liveness properties [T1, M3]
\*-------------------------------------------------------------
\* Every active node eventually completes
Liveness1 == \A n \in Node :
    state[n] = "active" ~> state[n] = "done"

====
```

---

## Quick Reference: Decision Tables

### Fairness Selection [T2, M4, P3.3]

```
Is the action an environment/external action?
  YES → No fairness. Stop.
  NO  ↓
Is the action continuously enabled once enabled?
  YES → WF_vars(Action). Stop.
  NO  ↓
Is the action repeatedly enabled then disabled (intermittently)?
  YES → SF_vars(Action). Document why WF is insufficient.
  NO  ↓
Is the action enabled only once?
  → WF_vars(Action) suffices (same as continuously enabled case).
```

### Communication Model [T2, P3.4]

```
Does your property depend on message ordering?
  YES → Sequence model (per-link Seq). Stop.
  NO  ↓
Does your property depend on detecting duplicates?
  YES → Bag model. Stop.
  NO  ↓
Use Set model (simplest).
```

### TLC Config for Checking Phase [T1, M11, M12]

```
Phase: Safety development?
  → CONSTRAINT ok, SYMMETRY ok, INVARIANT

Phase: Final safety?
  → NO CONSTRAINT, SYMMETRY ok, INVARIANT

Phase: Liveness development?
  → NO CONSTRAINT, NO SYMMETRY, PROPERTY, -lncheck

Phase: Final liveness?
  → NO CONSTRAINT, NO SYMMETRY, PROPERTY, -lncheck final, -workers auto
```

---

## Evidence Traceability Matrix

Maps each section of this skill to the research findings that support it.

| Section | Research Findings | Tier | Confidence |
|---------|-------------------|------|------------|
| 1.1 Canonical Form | M1, P4.1.F1 | T1 | HIGH (with caveat: default, not law) |
| 1.2 Stuttering & UNCHANGED | M2, M5 | T1 | HIGH |
| 1.3 TypeOK | M9 | T1 | HIGH |
| 2.1 Abstraction Framework | P3.1, M8 | T2 | HIGH |
| 2.2 Distributed Patterns | P3.4, M14 | T2 | HIGH |
| 3.1 Safety Checklist | M9, M5, M11, M12 | T1 | HIGH |
| 3.2 Deadlock-Freedom Gate | P4.4.F6 | T1 | HIGH (adversarial correction) |
| 3.3 TLC Safety Config | M11, M12 | T1 | HIGH |
| 4.1 Liveness Methodology | M3, P3.2, P3.3 | T1 | HIGH |
| 4.2 TLC Soundness Matrix | M11, M12, P3.2 | T1 | HIGH |
| 5.1 Small Model Heuristics | M10, P4.4.F3 | T2 | MEDIUM (caveats on thresholds) |
| 5.2 TLC Config Guide | M11, M12 | T1 | HIGH |
| 5.3 Multi-Tool Awareness | P4.3.F6, P4.4.F2 | T3 | MEDIUM |
| 6.1 PlusCal | M16, P4.4.F1 | T3 | MEDIUM |

---

## Why Every Rule Exists [P4.4.F5]

> **[Adversarial correction P4.4.F5]**: A template-based approach risks
> users following rules by rote without understanding WHY. Every rule in
> this skill includes its rationale. If you find yourself following a rule
> without understanding it, stop and read the "Why" or "Rationale" column.
> Rote rule-following produces specifications that look correct but miss
> the point.

---

## References

1. Lamport, L. *Specifying Systems: The TLA+ Language and Tools for Hardware and Software Engineers*. Addison-Wesley, 2002. [Primary source for M1-M5, M8, M14]
2. Lamport, L. "The Temporal Logic of Actions." *ACM Transactions on Programming Languages and Systems*, 16(3):872-923, 1994. [M4: fairness definitions]
3. Yu, Y., Manolios, P., Lamport, L. "Model Checking TLA+ Specifications." *Correct Hardware Design and Verification Methods*, LNCS 1703, 1999. [M12: TLC implementation]
4. Newcombe, C., Rath, T., Zhang, F., Muehlfield, B., Ring, A., Kirkwood, B. "How Amazon Web Services Uses Formal Methods." *Communications of the ACM*, 58(4):66-73, 2015. [M10: small model sufficiency, industrial practice]
5. Lamport, L. "A PlusCal User's Manual." 2009. [M16: PlusCal]
6. TLC Model Checker Reference. https://lamport.azurewebsites.net/tla/current-tools.html [M11: TLC config options]
7. Ongaro, D., Ousterhout, J. "In Search of an Understandable Consensus Algorithm (Extended Version)." Stanford University, 2014. [Raft TLA+ specification as exemplar]
8. Lamport, L. "Paxos Made Simple." *ACM SIGACT News*, 32(4):18-25, 2001. [Protocol specification methodology]
9. Kuppe, M., Lamport, L., Ricketts, D. "The TLA+ Toolbox." *arXiv:1912.10633*, 2019. [TLC tooling and configuration]
10. Konnov, I., Kukovec, J., Tran, T.-H. "TLA+ Model Checking Made Symbolic." *Proceedings of the ACM on Programming Languages*, 3(OOPSLA), 2019. [Apalache: symbolic model checking for TLA+]

## Related Skills

- `/deep-research` — use before this skill when entering unfamiliar
  protocol territory; gather evidence before specifying
- `/dist-sys-auditor` — complementary: audits distributed systems
  implementation code; this skill audits the specification
- `/sim-review` — after specification passes, sim-review ensures
  the implementation maintains specification-level properties
- `/sim-scaffold` — generate simulation-testable code from spec decisions
