---
name: thinking-occams-razor
description: Apply parsimony principle to prefer simpler explanations with fewer assumptions. Use for hypothesis selection in debugging, architecture decisions, and choosing between competing approaches.
---

# Occam's Razor (Parsimony Principle)

## Overview

Occam's Razor, attributed to 14th-century philosopher William of Ockham, states: "Entities should not be multiplied beyond necessity" (entia non sunt multiplicanda praeter necessitatem). When multiple explanations fit the evidence equally well, prefer the simplest one—the one with the fewest assumptions.

**Core Principle:** Among competing hypotheses that explain the data equally well, select the one with the fewest assumptions.

**Einstein's Corollary:** "Everything should be made as simple as possible, but no simpler."

## When to Use

- Debugging: Multiple hypotheses could explain a bug
- Architecture: Choosing between design approaches
- Root cause analysis: Several causes seem plausible
- Code review: Evaluating implementation complexity
- Technical decisions: Selecting between tools or patterns
- Incident response: Narrowing down failure causes

Decision flow:

```
Multiple explanations exist? → yes → Do they explain the evidence equally? → yes → APPLY OCCAM'S RAZOR
                                                                          ↘ no → Prefer better explanation
                           ↘ no → Use available explanation
```

## The Process

### Step 1: Enumerate Competing Hypotheses

List all plausible explanations for the observed behavior:

```
Bug: Users intermittently can't log in

Hypotheses:
A. Session token expiration edge case
B. Race condition in auth service
C. Database connection pool exhaustion
D. Cosmic rays flipping bits in memory
E. Complex interaction between CDN cache, load balancer, and session service
```

### Step 2: Count the Assumptions

For each hypothesis, list required assumptions:

| Hypothesis | Assumptions Required |
|------------|---------------------|
| A. Token expiration | 1. Token validation has edge case |
| B. Race condition | 1. Concurrent requests possible, 2. Shared mutable state exists |
| C. DB pool exhaustion | 1. Pool is undersized, 2. Connections are leaking |
| D. Cosmic rays | 1. Hardware failure, 2. No ECC memory, 3. Perfect timing |
| E. Complex interaction | 1. CDN caches auth, 2. LB sticky sessions fail, 3. Session sync delayed |

### Step 3: Verify Explanatory Power

Ensure simpler hypotheses actually explain the evidence:

```
Evidence: Failures correlate with high traffic periods

Hypothesis A (token edge case): 
  - Doesn't explain traffic correlation ❌
  
Hypothesis C (DB pool exhaustion):
  - Explains traffic correlation ✓
  - Fewer assumptions than E
  - PREFERRED by Occam's Razor ✓
```

### Step 4: Test Simplest First

Investigate hypotheses in order of simplicity:

```
1. Check DB connection pool metrics (simplest)
2. Review token validation code (simple)
3. Analyze race condition potential (moderate)
4. Instrument complex service interactions (complex)
5. Check for hardware issues (last resort)
```

### Step 5: Escalate Complexity Only When Needed

If simple explanations are ruled out, move to complex ones with new evidence.

## Complexity Assessment Framework

### Counting Complexity

| Factor | Complexity Cost |
|--------|-----------------|
| Each independent assumption | +1 |
| Each component involved | +1 |
| Each external dependency | +2 |
| Timing-dependent behavior | +2 |
| Requires rare conditions | +3 |
| "Perfect storm" scenarios | +5 |

### Example Comparison

```
Solution A: Add caching layer
- New component (Redis): +1
- Cache invalidation logic: +1  
- New failure mode: +1
Total: 3

Solution B: Optimize existing query
- Query modification: +1
Total: 1

→ Prefer Solution B unless evidence shows it's insufficient
```

## When Simplicity Yields to Complexity

Occam's Razor is a heuristic, not an absolute law. Prefer complexity when:

### 1. Evidence Demands It

```
Simple hypothesis: Single bug in auth service
Evidence: Failures only occur when Feature X AND Feature Y are both enabled

→ Complex interaction hypothesis now has supporting evidence
→ Accept complexity that explains the evidence
```

### 2. Domain Complexity Is Irreducible

```
Problem: Distributed consensus
Simple solution: Single leader (but single point of failure)
Reality: Distributed systems require complex solutions (Raft, Paxos)

→ Some domains have irreducible complexity
→ Don't oversimplify beyond what's correct
```

### 3. Future Requirements Are Known

```
Current need: Store user preferences
Simple: JSON file
Future need: Multi-device sync, conflict resolution

→ Database is more complex but necessary
→ Known future needs justify upfront complexity
```

### 4. Simplicity Introduces Technical Debt

```
Simple now: Copy-paste code in 5 places
Simpler long-term: Extract shared function

→ Local simplicity vs. systemic simplicity
→ Prefer systemic simplicity
```

## Application Examples

### Debugging Example

```
Bug: API returns 500 errors sporadically

Hypothesis A: Null pointer in rare code path
  Assumptions: 1
  
Hypothesis B: Memory pressure causes GC pauses that timeout requests
  Assumptions: 3 (memory issues + GC behavior + timeout settings)
  
Hypothesis C: Race condition between cache refresh and request handling
  Assumptions: 4 (concurrent access + shared state + timing + cache implementation)

Occam's Razor: Start with Hypothesis A
Action: Search logs for null pointer exceptions
Result: Found! NPE in user profile edge case
```

### Architecture Example

```
Requirement: Service needs to call another service

Option A: Direct HTTP call
  Components: 1 (HTTP client)
  Assumptions: Target available, network reliable
  
Option B: Message queue with retry
  Components: 3 (queue, producer, consumer)
  Assumptions: Need async, need retry, need decoupling
  
Option C: Service mesh with circuit breaker, retry, timeout
  Components: 5+ (sidecar, control plane, observability)
  Assumptions: At scale, need observability, need traffic management

Occam's Razor: Start with Option A
Escalate to B/C only when evidence shows need for resilience
```

### Code Implementation Example

```python
# Complex (unnecessary assumptions)
def is_even(n):
    binary = bin(n)
    last_bit = binary[-1]
    return last_bit == '0'

# Simple (minimal assumptions)  
def is_even(n):
    return n % 2 == 0

# Occam's Razor: Prefer the modulo approach
# Fewer concepts, fewer operations, same result
```

### Root Cause Analysis Example

```
Symptom: Deployment failed

Complex hypothesis:
"The CI server's Docker daemon ran out of disk space because 
a cron job that cleans old images was disabled when we upgraded 
the server OS last month, and nobody noticed because the monitoring 
alert was routed to a deprecated Slack channel."

Simple hypothesis:
"The build script has a typo in the new environment variable name."

Occam's Razor: Check the build script first
Result: Typo found. DATABSE_URL instead of DATABASE_URL
```

## Common Anti-Patterns

| Anti-Pattern | Description | Correction |
|--------------|-------------|------------|
| Rube Goldberg | Complex solution to simple problem | Ask "what's the minimum needed?" |
| Premature abstraction | Abstracting for hypothetical cases | Wait for evidence of need |
| Resume-driven development | Using complex tech to learn it | Match tool to problem |
| Cargo culting | Copying complex patterns blindly | Understand why patterns exist |
| Conspiracy thinking | Assuming coordinated complex causes | Check simple causes first |

## Verification Checklist

- [ ] Listed all plausible hypotheses/solutions
- [ ] Counted assumptions required for each
- [ ] Verified simpler options have equal explanatory power
- [ ] Investigated in order of simplicity
- [ ] Escalated to complexity only with evidence
- [ ] Confirmed solution is "as simple as possible, but no simpler"
- [ ] Checked for domain-irreducible complexity
- [ ] Considered systemic vs. local simplicity

## Combining with Other Models

- **First Principles**: Reduce to fundamentals, then apply Occam's to solutions
- **Inversion**: "What would make this unnecessarily complex?"
- **Debiasing**: Watch for complexity bias (assuming complex = sophisticated)
- **Pre-Mortem**: Would a simpler approach have fewer failure modes?

## Key Questions

- "What's the simplest explanation that fits all the evidence?"
- "How many things have to be true for this hypothesis to hold?"
- "Am I adding complexity to handle cases I haven't seen?"
- "Would a junior engineer understand this solution?"
- "If I explained this to a non-technical person, how many steps would it take?"
- "What's the minimum change that could fix this?"
- "Am I solving the problem I have, or a problem I might have?"

## Ockham's Warning

"Plurality must never be posited without necessity."

The simplest solution isn't always correct, but it should always be tested first. Complexity should be earned through evidence, not assumed through speculation. When you find yourself building elaborate explanations, step back and ask: "What's the minimum hypothesis that explains what I'm seeing?"
