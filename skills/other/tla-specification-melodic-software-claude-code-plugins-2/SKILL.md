---
name: tla-specification
description: TLA+ formal specification language for distributed systems and concurrent algorithms
allowed-tools: Read, Glob, Grep, Write, Edit, mcp__perplexity__search
---

# TLA+ Specification Skill

## When to Use This Skill

Use this skill when:

- **Tla Specification tasks** - Working on tla+ formal specification language for distributed systems and concurrent algorithms
- **Planning or design** - Need guidance on Tla Specification approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

TLA+ formal specification language for designing and verifying distributed systems and concurrent algorithms.

## MANDATORY: Documentation-First Approach

Before writing TLA+ specifications:

1. **Invoke `docs-management` skill** for formal methods patterns
2. **Verify TLA+ syntax** via MCP servers (perplexity for latest practices)
3. **Base all guidance on Leslie Lamport's TLA+ documentation**

## Why TLA+?

TLA+ enables:

1. **Precise Design**: Mathematical precision in system design
2. **Early Bug Detection**: Find concurrency bugs before coding
3. **Model Checking**: Exhaustive verification with TLC
4. **Documentation**: Executable specifications that document intent
5. **Industry Adoption**: Used by Amazon (AWS), Microsoft, MongoDB, etc.

## TLA+ Structure

### Basic Module Template

```tla
--------------------------- MODULE OrderWorkflow ---------------------------
\* Order Workflow Specification
\* Models the lifecycle of an order from creation to completion

EXTENDS Integers, Sequences, FiniteSets, TLC

CONSTANTS
    MaxOrders,      \* Maximum number of concurrent orders
    MaxItems,       \* Maximum items per order
    Customers,      \* Set of customer IDs
    Products        \* Set of product IDs

VARIABLES
    orders,         \* Function from OrderId -> Order state
    inventory,      \* Function from ProductId -> quantity
    payments,       \* Set of processed payment records
    notifications   \* Sequence of sent notifications

vars == <<orders, inventory, payments, notifications>>

-----------------------------------------------------------------------------
\* Type Definitions
-----------------------------------------------------------------------------

OrderStatus == {"Draft", "Submitted", "Paid", "Shipped", "Delivered", "Cancelled"}

Order == [
    id: Nat,
    customerId: Customers,
    items: SUBSET (Products \X Nat),  \* Set of (product, quantity) pairs
    status: OrderStatus,
    total: Nat
]

TypeInvariant ==
    /\ orders \in [SUBSET Nat -> Order \cup {NULL}]
    /\ inventory \in [Products -> Nat]
    /\ payments \in SUBSET [orderId: Nat, amount: Nat, timestamp: Nat]
    /\ notifications \in Seq([type: STRING, orderId: Nat])

-----------------------------------------------------------------------------
\* Initial State
-----------------------------------------------------------------------------

Init ==
    /\ orders = [o \in {} |-> NULL]
    /\ inventory = [p \in Products |-> 100]  \* Start with 100 of each
    /\ payments = {}
    /\ notifications = <<>>

-----------------------------------------------------------------------------
\* Actions
-----------------------------------------------------------------------------

\* Create a new draft order
CreateOrder(customerId, orderId) ==
    /\ orderId \notin DOMAIN orders
    /\ Cardinality(DOMAIN orders) < MaxOrders
    /\ orders' = orders @@ (orderId :> [
           id |-> orderId,
           customerId |-> customerId,
           items |-> {},
           status |-> "Draft",
           total |-> 0
       ])
    /\ UNCHANGED <<inventory, payments, notifications>>

\* Add item to draft order
AddItem(orderId, productId, quantity) ==
    /\ orderId \in DOMAIN orders
    /\ orders[orderId].status = "Draft"
    /\ quantity > 0
    /\ quantity <= inventory[productId]
    /\ Cardinality(orders[orderId].items) < MaxItems
    /\ orders' = [orders EXCEPT
           ![orderId].items = @ \cup {<<productId, quantity>>},
           ![orderId].total = @ + (quantity * 10)]  \* Simplified pricing
    /\ UNCHANGED <<inventory, payments, notifications>>

\* Submit order for processing
SubmitOrder(orderId) ==
    /\ orderId \in DOMAIN orders
    /\ orders[orderId].status = "Draft"
    /\ orders[orderId].items /= {}
    \* Reserve inventory
    /\ \A <<p, q>> \in orders[orderId].items : inventory[p] >= q
    /\ orders' = [orders EXCEPT ![orderId].status = "Submitted"]
    /\ inventory' = [p \in Products |->
           inventory[p] - Sum({q : <<prod, q>> \in orders[orderId].items, prod = p})]
    /\ notifications' = Append(notifications,
           [type |-> "OrderSubmitted", orderId |-> orderId])
    /\ UNCHANGED <<payments>>

\* Process payment
ProcessPayment(orderId, amount) ==
    /\ orderId \in DOMAIN orders
    /\ orders[orderId].status = "Submitted"
    /\ amount = orders[orderId].total
    /\ payments' = payments \cup {[orderId |-> orderId, amount |-> amount, timestamp |-> 0]}
    /\ orders' = [orders EXCEPT ![orderId].status = "Paid"]
    /\ notifications' = Append(notifications,
           [type |-> "PaymentReceived", orderId |-> orderId])
    /\ UNCHANGED <<inventory>>

\* Ship order
ShipOrder(orderId) ==
    /\ orderId \in DOMAIN orders
    /\ orders[orderId].status = "Paid"
    /\ orders' = [orders EXCEPT ![orderId].status = "Shipped"]
    /\ notifications' = Append(notifications,
           [type |-> "OrderShipped", orderId |-> orderId])
    /\ UNCHANGED <<inventory, payments>>

\* Deliver order
DeliverOrder(orderId) ==
    /\ orderId \in DOMAIN orders
    /\ orders[orderId].status = "Shipped"
    /\ orders' = [orders EXCEPT ![orderId].status = "Delivered"]
    /\ notifications' = Append(notifications,
           [type |-> "OrderDelivered", orderId |-> orderId])
    /\ UNCHANGED <<inventory, payments>>

\* Cancel order (only draft or submitted)
CancelOrder(orderId) ==
    /\ orderId \in DOMAIN orders
    /\ orders[orderId].status \in {"Draft", "Submitted"}
    /\ orders' = [orders EXCEPT ![orderId].status = "Cancelled"]
    \* Return inventory if was submitted
    /\ inventory' = IF orders[orderId].status = "Submitted"
                    THEN [p \in Products |->
                          inventory[p] + Sum({q : <<prod, q>> \in orders[orderId].items, prod = p})]
                    ELSE inventory
    /\ notifications' = Append(notifications,
           [type |-> "OrderCancelled", orderId |-> orderId])
    /\ UNCHANGED <<payments>>

-----------------------------------------------------------------------------
\* Next State Relation
-----------------------------------------------------------------------------

Next ==
    \/ \E c \in Customers, o \in 1..MaxOrders : CreateOrder(c, o)
    \/ \E o \in DOMAIN orders, p \in Products, q \in 1..5 : AddItem(o, p, q)
    \/ \E o \in DOMAIN orders : SubmitOrder(o)
    \/ \E o \in DOMAIN orders : ProcessPayment(o, orders[o].total)
    \/ \E o \in DOMAIN orders : ShipOrder(o)
    \/ \E o \in DOMAIN orders : DeliverOrder(o)
    \/ \E o \in DOMAIN orders : CancelOrder(o)

Spec == Init /\ [][Next]_vars

-----------------------------------------------------------------------------
\* Safety Properties
-----------------------------------------------------------------------------

\* No negative inventory
InventoryNonNegative ==
    \A p \in Products : inventory[p] >= 0

\* Order status transitions are valid
ValidStatusTransitions ==
    \A o \in DOMAIN orders :
        LET status == orders[o].status
        IN status \in OrderStatus

\* Payment only for submitted orders
PaymentOnlyForSubmitted ==
    \A p \in payments :
        p.orderId \in DOMAIN orders

\* No double payments
NoDoublePayment ==
    \A p1, p2 \in payments :
        p1.orderId = p2.orderId => p1 = p2

-----------------------------------------------------------------------------
\* Liveness Properties
-----------------------------------------------------------------------------

\* Every submitted order eventually completes (delivered or cancelled)
EventualCompletion ==
    \A o \in DOMAIN orders :
        orders[o].status = "Submitted" ~>
            orders[o].status \in {"Delivered", "Cancelled"}

\* If payment succeeds, order eventually ships
PaymentLeadsToShipment ==
    \A o \in DOMAIN orders :
        orders[o].status = "Paid" ~> orders[o].status = "Shipped"

-----------------------------------------------------------------------------
\* Helper Functions
-----------------------------------------------------------------------------

Sum(S) ==
    IF S = {} THEN 0
    ELSE LET x == CHOOSE x \in S : TRUE
         IN x + Sum(S \ {x})

NULL == CHOOSE n : n \notin Order

=============================================================================
```

## PlusCal

PlusCal is an algorithm language that compiles to TLA+:

### PlusCal Example

```tla
--------------------------- MODULE DistributedLock ---------------------------
EXTENDS Integers, Sequences, TLC

CONSTANTS Nodes, NULL

(*--algorithm distributed_lock

variables
    lock = NULL,                    \* Current lock holder
    requests = [n \in Nodes |-> 0], \* Request timestamps
    grants = [n \in Nodes |-> FALSE];

define
    \* Safety: At most one node holds lock
    MutualExclusion ==
        \A n1, n2 \in Nodes :
            grants[n1] /\ grants[n2] => n1 = n2

    \* Liveness: Every request eventually granted
    EventuallyGranted ==
        \A n \in Nodes :
            requests[n] > 0 ~> grants[n]
end define;

fair process Node \in Nodes
variables
    myTimestamp = 0;
begin
    Request:
        myTimestamp := myTimestamp + 1;
        requests[self] := myTimestamp;

    WaitForLock:
        await lock = NULL \/ lock = self;
        lock := self;

    EnterCriticalSection:
        grants[self] := TRUE;
        \* Critical section work here

    ExitCriticalSection:
        grants[self] := FALSE;
        lock := NULL;
        goto Request;
end process;

end algorithm; *)

\* BEGIN TRANSLATION - Auto-generated by TLA+
\* ... TLA+ translation appears here ...
\* END TRANSLATION

=============================================================================
```

### PlusCal Constructs

```text
variables         - Global variable declarations
define            - Define operators/invariants
process           - Process definition (fair = fair scheduling)
procedure         - Reusable procedure
begin/end         - Process body
await             - Wait for condition
either/or         - Non-deterministic choice
while             - Loop
if/then/else      - Conditional
goto              - Jump to label
call              - Procedure call
return            - Return from procedure
with              - Atomic with non-deterministic selection
```

## Common Patterns

### Consensus Algorithm

```tla
--------------------------- MODULE SimpleConsensus ---------------------------
EXTENDS Integers, FiniteSets

CONSTANTS
    Nodes,      \* Set of participant nodes
    Values,     \* Possible values to agree on
    Quorum      \* Minimum nodes for quorum

VARIABLES
    proposed,   \* proposed[n] = value proposed by node n
    accepted,   \* accepted[n] = value accepted by node n
    decided     \* decided[n] = final decided value (or NULL)

vars == <<proposed, accepted, decided>>

TypeOK ==
    /\ proposed \in [Nodes -> Values \cup {NULL}]
    /\ accepted \in [Nodes -> Values \cup {NULL}]
    /\ decided \in [Nodes -> Values \cup {NULL}]

Init ==
    /\ proposed = [n \in Nodes |-> NULL]
    /\ accepted = [n \in Nodes |-> NULL]
    /\ decided = [n \in Nodes |-> NULL]

\* Node proposes a value
Propose(n, v) ==
    /\ proposed[n] = NULL
    /\ proposed' = [proposed EXCEPT ![n] = v]
    /\ UNCHANGED <<accepted, decided>>

\* Node accepts a proposed value
Accept(n, v) ==
    /\ \E m \in Nodes : proposed[m] = v
    /\ accepted[n] = NULL
    /\ accepted' = [accepted EXCEPT ![n] = v]
    /\ UNCHANGED <<proposed, decided>>

\* Node decides if quorum reached
Decide(n) ==
    /\ decided[n] = NULL
    /\ \E v \in Values :
        /\ Cardinality({m \in Nodes : accepted[m] = v}) >= Quorum
        /\ decided' = [decided EXCEPT ![n] = v]
    /\ UNCHANGED <<proposed, accepted>>

Next ==
    \/ \E n \in Nodes, v \in Values : Propose(n, v)
    \/ \E n \in Nodes, v \in Values : Accept(n, v)
    \/ \E n \in Nodes : Decide(n)

Spec == Init /\ [][Next]_vars

\* Safety: Agreement - all decided values are the same
Agreement ==
    \A n1, n2 \in Nodes :
        decided[n1] /= NULL /\ decided[n2] /= NULL =>
            decided[n1] = decided[n2]

\* Safety: Validity - decided value was proposed
Validity ==
    \A n \in Nodes :
        decided[n] /= NULL =>
            \E m \in Nodes : proposed[m] = decided[n]

=============================================================================
```

### Two-Phase Commit

```tla
--------------------------- MODULE TwoPhaseCommit ---------------------------
EXTENDS Integers, FiniteSets

CONSTANTS
    Coordinators,
    Participants

VARIABLES
    coordState,     \* Coordinator state
    partState,      \* Participant states
    prepared,       \* Set of prepared participants
    decision        \* Final decision

vars == <<coordState, partState, prepared, decision>>

CoordStates == {"init", "waiting", "committed", "aborted"}
PartStates == {"working", "prepared", "committed", "aborted"}

TypeOK ==
    /\ coordState \in CoordStates
    /\ partState \in [Participants -> PartStates]
    /\ prepared \in SUBSET Participants
    /\ decision \in {"pending", "commit", "abort"}

Init ==
    /\ coordState = "init"
    /\ partState = [p \in Participants |-> "working"]
    /\ prepared = {}
    /\ decision = "pending"

\* Coordinator sends prepare request
SendPrepare ==
    /\ coordState = "init"
    /\ coordState' = "waiting"
    /\ UNCHANGED <<partState, prepared, decision>>

\* Participant prepares (votes yes)
Prepare(p) ==
    /\ partState[p] = "working"
    /\ partState' = [partState EXCEPT ![p] = "prepared"]
    /\ prepared' = prepared \cup {p}
    /\ UNCHANGED <<coordState, decision>>

\* Participant aborts (votes no)
Abort(p) ==
    /\ partState[p] = "working"
    /\ partState' = [partState EXCEPT ![p] = "aborted"]
    /\ UNCHANGED <<coordState, prepared, decision>>

\* Coordinator decides commit (all prepared)
DecideCommit ==
    /\ coordState = "waiting"
    /\ prepared = Participants
    /\ coordState' = "committed"
    /\ decision' = "commit"
    /\ partState' = [p \in Participants |-> "committed"]
    /\ UNCHANGED <<prepared>>

\* Coordinator decides abort (any aborted)
DecideAbort ==
    /\ coordState = "waiting"
    /\ \E p \in Participants : partState[p] = "aborted"
    /\ coordState' = "aborted"
    /\ decision' = "abort"
    /\ partState' = [p \in Participants |->
           IF partState[p] = "prepared" THEN "aborted" ELSE partState[p]]
    /\ UNCHANGED <<prepared>>

Next ==
    \/ SendPrepare
    \/ \E p \in Participants : Prepare(p)
    \/ \E p \in Participants : Abort(p)
    \/ DecideCommit
    \/ DecideAbort

Spec == Init /\ [][Next]_vars

\* Safety: Atomicity - all participants reach same decision
Atomicity ==
    decision /= "pending" =>
        \A p \in Participants :
            (decision = "commit" => partState[p] = "committed") /\
            (decision = "abort" => partState[p] \in {"aborted", "working"})

=============================================================================
```

## TLC Model Checking

### Configuration File (.cfg)

```text
SPECIFICATION Spec

\* Constants
CONSTANTS
    Nodes = {n1, n2, n3}
    Values = {v1, v2}
    Quorum = 2
    NULL = NULL

\* Invariants to check
INVARIANT TypeOK
INVARIANT Agreement
INVARIANT Validity

\* Liveness properties
PROPERTY EventuallyDecided

\* Constraints for bounded model checking
CONSTRAINT StateConstraint

\* Symmetry for optimization
SYMMETRY Symmetry
```

### Running TLC

```bash
# Command-line TLC
java -jar tla2tools.jar -config Spec.cfg Spec.tla

# With workers for parallelism
java -jar tla2tools.jar -workers 4 -config Spec.cfg Spec.tla

# Generate trace on error
java -jar tla2tools.jar -dump dot,colorize states.dot Spec.tla
```

## Temporal Operators

```text
[]P          - Always P (invariant)
<>P          - Eventually P
P ~> Q       - P leads to Q (if P then eventually Q)
[]<>P        - Infinitely often P
<>[]P        - Eventually always P
P /\ Q       - P and Q
P \/ Q       - P or Q
~P           - Not P
P => Q       - P implies Q
ENABLED A    - Action A is enabled
[A]_v        - A or v unchanged
<<A>>_v      - A and v changes
WF_v(A)      - Weak fairness
SF_v(A)      - Strong fairness
```

## Integration with C\#

```csharp
// Specification-driven design: implement to match TLA+ spec

public enum OrderStatus
{
    Draft,
    Submitted,
    Paid,
    Shipped,
    Delivered,
    Cancelled
}

// State machine matching TLA+ transitions
public sealed class Order
{
    private static readonly Dictionary<(OrderStatus From, string Action), OrderStatus> _transitions = new()
    {
        // Matches TLA+ SubmitOrder action
        { (OrderStatus.Draft, "Submit"), OrderStatus.Submitted },
        // Matches TLA+ ProcessPayment action
        { (OrderStatus.Submitted, "Pay"), OrderStatus.Paid },
        // Matches TLA+ ShipOrder action
        { (OrderStatus.Paid, "Ship"), OrderStatus.Shipped },
        // Matches TLA+ DeliverOrder action
        { (OrderStatus.Shipped, "Deliver"), OrderStatus.Delivered },
        // Matches TLA+ CancelOrder action
        { (OrderStatus.Draft, "Cancel"), OrderStatus.Cancelled },
        { (OrderStatus.Submitted, "Cancel"), OrderStatus.Cancelled },
    };

    public OrderStatus Status { get; private set; } = OrderStatus.Draft;

    public Result Transition(string action)
    {
        if (!_transitions.TryGetValue((Status, action), out var newStatus))
            return Result.Failure($"Invalid transition: {Status} -> {action}");

        Status = newStatus;
        return Result.Success();
    }
}

// Invariant checking in tests (matches TLA+ safety properties)
public class OrderInvariantTests
{
    [Fact]
    public void InventoryNonNegative_IsAlwaysTrue()
    {
        // Simulates TLA+ model checking for InventoryNonNegative
        var inventory = new Dictionary<string, int>();
        // ... run through state space
        Assert.All(inventory.Values, qty => Assert.True(qty >= 0));
    }
}
```

## Workflow

When creating TLA+ specifications:

1. **Identify State**: What variables define system state?
2. **Define Types**: What are valid values for each variable?
3. **Specify Init**: What is the initial state?
4. **Define Actions**: What state transitions are possible?
5. **Write Invariants**: What must always be true (safety)?
6. **Write Liveness**: What must eventually happen?
7. **Model Check**: Run TLC to verify properties
8. **Refine**: Add detail or fix discovered bugs

## Best Practices

1. **Start Simple**: Begin with minimal spec, add complexity gradually
2. **Check Types First**: TypeOK should pass before complex properties
3. **Use Constants**: Parameterize for easy model size adjustment
4. **Add Constraints**: Bound state space for tractable checking
5. **Symmetry**: Exploit symmetry to reduce state space
6. **Trace Errors**: Use TLC traces to understand failures
7. **Document Intent**: Comments explain why, not what

## References

For detailed guidance:

---

**Last Updated:** 2025-12-26
