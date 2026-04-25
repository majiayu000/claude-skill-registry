---
name: distributed-consensus
description: Distributed consensus algorithms and logical time for cloud and multi-node systems. Covers Lamport clocks, vector clocks, FLP impossibility, Paxos (basic, multi, fast), Raft, Viewstamped Replication, Byzantine fault tolerance basics, quorum reads/writes (N/R/W), leader election, and TLA+ specification style. Use when designing replicated state machines, picking a consensus protocol, reasoning about split-brain and quorum loss, or writing formal specs for distributed coordination.
type: skill
category: cloud-systems
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/cloud-systems/distributed-consensus/SKILL.md
superseded_by: null
---
# Distributed Consensus

Consensus is the problem of getting a group of processes that fail independently to agree on a single value, or on a sequence of values, in the presence of network delays, message loss, and process crashes. Consensus is the foundation on which replicated state machines, leader election, distributed locks, configuration management, and strongly consistent databases are built. This skill catalogs the core results, algorithms, and design heuristics a cloud-systems practitioner needs to reason about coordination primitives without reinventing them.

**Agent affinity:** lamport (consensus theory, logical clocks, TLA+), decandia (quorum mechanics in Dynamo-style stores), dean (Paxos/Spanner experience in production systems)

**Concept IDs:** cloud-multi-service-coordination, cloud-procedure-execution, cloud-requirements-tracing

## Why Consensus is Hard

Distributed systems fail in ways that single-node systems do not. Messages arrive late, arrive out of order, arrive twice, or never arrive. Processes crash, restart, and come back with stale state. Networks partition and heal. Clocks drift. Two observers watching the same sequence of events can see them in different orders and both be telling the truth about what they saw. Building reliable systems on this substrate requires algorithms that are correct under the worst combinations of these failures, not just the common cases.

The core insight, due to Lamport, is that "time" in a distributed system is not a physical thing — it is a partial order over events derived from message causality. "Happened-before" (`a -> b` if `a` and `b` are on the same process in program order, or if `a` is a send and `b` is the matching receive) gives a causal structure that distributed algorithms can actually reason about. Wall-clock time is an optimization for the common case, not a correctness foundation.

## The FLP Impossibility Result

Fischer, Lynch, and Paterson (1985) proved that in an asynchronous system with even one faulty process, no deterministic consensus algorithm can guarantee termination. The proof constructs an adversarial scheduler that can always delay messages to keep the system in a bivalent state — a state from which either decision is still reachable.

This result does not say consensus is impossible. It says that any consensus algorithm must give up something: either synchrony assumptions (Paxos, Raft assume partial synchrony and eventually a stable leader), or determinism (randomized consensus terminates with probability 1), or fault tolerance (can tolerate zero failures if synchrony is strong). Every real consensus algorithm sits somewhere on this trade-off curve.

## Lamport Clocks

A Lamport logical clock is a function `L` from events to integers satisfying: if `a -> b` then `L(a) < L(b)`. The simplest implementation is a per-process counter `C`:

1. Before each local event, `C := C + 1`.
2. When sending a message, attach `C`.
3. On receiving a message with timestamp `t`, set `C := max(C, t) + 1`.

Lamport clocks give a total order consistent with causality (ties can be broken by process ID). They do not detect concurrency — if `L(a) < L(b)`, you cannot tell whether `a -> b` or `a || b`.

## Vector Clocks

A vector clock for `n` processes is a length-`n` integer vector `V` at each process. Process `i` increments `V[i]` on local events, attaches `V` to outgoing messages, and on receive sets `V[j] := max(V[j], t[j])` for all `j`, then increments `V[i]`.

Vector clocks give full causality: `a -> b` iff `V(a) < V(b)` (component-wise less-than-or-equal with at least one strict inequality). Concurrency is detectable: `a || b` iff neither `V(a) < V(b)` nor `V(b) < V(a)`.

Vector clocks are the backbone of Dynamo-style eventually consistent stores for detecting conflicting versions, and of causal consistency systems in general.

## The Paxos Family

Paxos (Lamport, 1998 — the "Part-Time Parliament" paper, and later "Paxos Made Simple") is a protocol for agreeing on a single value among a set of processes, at least a majority of which are non-faulty.

**Roles.** Proposers propose values, acceptors vote, learners learn the chosen value. A process may play multiple roles.

**Two phases.**

*Phase 1 (Prepare).* A proposer picks a ballot number `n` larger than any it has used, and sends `Prepare(n)` to a majority of acceptors. Each acceptor promises not to accept any ballot with number less than `n`, and replies with the highest-numbered proposal it has already accepted (if any).

*Phase 2 (Accept).* If the proposer got promises from a majority, it picks a value: if any of the replies contained a prior accepted proposal, it must use the value from the highest-numbered one (this preserves the safety invariant); otherwise it may propose its own value. It sends `Accept(n, v)` to a majority. Each acceptor accepts unless it has since promised a higher ballot.

A value is chosen once a majority of acceptors have accepted it. Once chosen, it cannot change — the phase 1 "must use highest prior" rule ensures any later successful proposer picks the same value.

**Multi-Paxos.** Running basic Paxos for every entry in a log is wasteful. Multi-Paxos elects a stable leader and skips phase 1 for subsequent slots until the leader loses leadership. This is how Paxos is actually used in systems like Chubby and Spanner.

**Fast Paxos.** Allows clients to send directly to acceptors when there is no contention, at the cost of larger quorums when contention is detected.

## Raft

Raft (Ongaro and Ousterhout, 2014) is a consensus protocol designed for understandability. It decomposes consensus into three explicit subproblems: leader election, log replication, and safety. It adds a state machine abstraction and a clean membership change protocol.

**Key design choices.**

- Strong leader. All client requests go through the leader. Followers are passive. This trades some flexibility for clarity.
- Randomized timeouts. Followers become candidates after a randomized election timeout, reducing split votes.
- Log matching property. If two logs contain an entry with the same index and term, they are identical up to and including that entry.

Raft is used in etcd, Consul, CockroachDB, and many newer systems. The trade-off versus Paxos is: Raft is easier to implement correctly, Paxos is more flexible under pathological network conditions.

## Viewstamped Replication and Virtual Synchrony

VR (Oki and Liskov, 1988) predates Paxos and was rediscovered after Raft. It uses view numbers as ballot numbers and has an explicit primary/backup structure. Virtual synchrony (Birman) extends the ideas with group membership as a first-class concept.

These matter because they remind you that "Paxos vs Raft" is a false dichotomy — consensus has a family of related solutions, and which you pick depends on the application's shape, not on algorithmic superiority.

## Byzantine Fault Tolerance (Sketch)

Byzantine failures are failures where a process may send arbitrary, including malicious, messages. Crash-fault-tolerant algorithms (Paxos, Raft) assume failures are crash-only. BFT algorithms (PBFT, HotStuff, Tendermint) tolerate up to `f` Byzantine processes out of `3f + 1`.

For most cloud-systems work inside a trusted datacenter boundary, CFT is sufficient. BFT becomes relevant when the failure domain includes adversarial actors — cross-organization blockchain systems, supply-chain attestation, or hardened aerospace flight software.

## Quorum Systems: N, R, W

In a replicated read/write store with `N` replicas, a read quorum of `R` and a write quorum of `W` satisfies strong consistency when `R + W > N`. This is the DeCandia/Dynamo formulation and appears in Cassandra, Riak, and many others.

- `W = N, R = 1`. Fast reads, slow writes. Write availability fails if any replica is down.
- `W = 1, R = N`. Fast writes, slow reads. Read availability fails if any replica is down.
- `W = R = (N+1)/2`. Balanced, majority quorums. Survives any `(N-1)/2` failures.
- `R + W <= N`. Eventual consistency — reads may not see recent writes until anti-entropy converges.

The design exercise is: given your latency, availability, and consistency requirements, pick N, R, W that satisfy them. Dynamo's contribution was to make these knobs explicit and per-request.

## Leader Election as a Consensus Primitive

Leader election is consensus where the value being agreed on is "who is the leader for the current term." Raft bakes this in. Paxos-based systems typically run a separate lease-based election (Chubby, ZooKeeper) and use the leader to serialize further writes.

The lease mechanic is essential: a leader holds the lease for a bounded time and must renew it. If the renewal fails, the leader must stop acting (fencing), or a new leader elected before the old one notices will cause split-brain.

## TLA+ as a Specification Language

TLA+ (Lamport) is a formal specification language for concurrent and distributed systems. It is the language in which basic and multi-Paxos were originally expressed precisely enough to prove correct. Its operational mindset is:

1. Specify the system as a state machine: variables, initial predicate, next-state relation.
2. State safety properties as invariants the reachable states must satisfy.
3. State liveness properties as temporal formulas.
4. Model-check small instances with TLC to find bugs early.

Using TLA+ (or its lighter cousin PlusCal) on the design of a consensus-based system is an outsized-ROI activity — bugs that would take months to reproduce in production show up in minutes.

## When to Use This Skill

- Designing a replicated state machine or configuration store that must survive node failures without losing committed state.
- Reviewing a proposed coordination protocol for split-brain, stale-read, or lost-update bugs.
- Choosing between strong and eventual consistency for a given data shape.
- Writing or reading TLA+ or PlusCal specifications for distributed protocols.
- Debugging a production incident where "the cluster saw different values for the same key."
- Explaining to a non-distributed-systems engineer why `sleep 100ms && commit` is not a fix.

## When NOT to Use This Skill

- Single-node systems — consensus primitives are overkill and add latency.
- Pure stateless request/response services — no consensus is needed at the application layer; the database handles it.
- Quick prototypes where correctness is not yet the binding constraint. Reach for a managed consensus service (etcd, ZooKeeper, Consul) and design the application around it, rather than rolling your own.

## Decision Guidance

| Situation | Recommended approach |
|---|---|
| Need a replicated log, small cluster (3-7 nodes), CFT | Raft (etcd, Consul) |
| Need a replicated log, large cluster or cross-region | Multi-Paxos (Spanner) |
| Need eventually consistent KV, tunable consistency | Dynamo-style (Cassandra) |
| Need strong consistency and external time | Spanner / TrueTime |
| Need Byzantine fault tolerance | PBFT/HotStuff only if the trust model demands it |
| Need formal verification of protocol | TLA+ model checking |
| Need distributed locks | ZooKeeper ephemeral nodes, or lease-based via etcd |

## References

- Lamport, L. (1978). "Time, Clocks, and the Ordering of Events in a Distributed System." CACM 21(7).
- Lamport, L. (1998). "The Part-Time Parliament." ACM TOCS 16(2).
- Lamport, L. (2001). "Paxos Made Simple." ACM SIGACT News.
- Fischer, M., Lynch, N., Paterson, M. (1985). "Impossibility of Distributed Consensus with One Faulty Process." JACM 32(2).
- Ongaro, D., Ousterhout, J. (2014). "In Search of an Understandable Consensus Algorithm." USENIX ATC.
- Oki, B., Liskov, B. (1988). "Viewstamped Replication." PODC.
- DeCandia, G., et al. (2007). "Dynamo: Amazon's Highly Available Key-value Store." SOSP.
- Castro, M., Liskov, B. (1999). "Practical Byzantine Fault Tolerance." OSDI.
