---
name: thinking-triz
description: Apply TRIZ (Theory of Inventive Problem Solving) methodology to resolve technical contradictions and find innovative solutions. Use for engineering design, breaking through impossible constraints, and systematic innovation.
---

# TRIZ Thinking

## Overview

TRIZ (Teoriya Resheniya Izobretatelskikh Zadatch) is a systematic innovation methodology developed by Genrich Altshuller from analyzing 200,000+ patents. It provides structured approaches to solve "impossible" problems by identifying and resolving contradictions rather than accepting trade-offs.

**Core Principle:** Behind every difficult problem lies a contradiction. Resolve the contradiction, solve the problem. Great innovations don't compromise—they transcend.

## When to Use

- Facing "impossible" trade-offs (fast vs. accurate, secure vs. convenient)
- Stuck choosing between two conflicting requirements
- Need innovation beyond incremental improvement
- Design has hit fundamental constraints
- Competitors all accept the same trade-off you're facing
- Requirements seem mutually exclusive
- Breaking through performance plateaus

Decision flow:

```
Stuck between trade-offs?           → yes → APPLY TRIZ
Requirements seem contradictory?    → yes → APPLY TRIZ
Need breakthrough, not compromise?  → yes → APPLY TRIZ
All solutions have same weakness?   → yes → APPLY TRIZ
```

## The Ideal Final Result (IFR)

Before solving, envision the ideal outcome—the system that solves itself:

```
IFR Formula:
"The [component] [achieves the goal] BY ITSELF,
without [cost/complexity/side effects],
while maintaining [all other functions]"
```

**Software Examples:**

```
Traditional: "We need a caching layer to improve performance"
IFR: "The system is instantly fast without any cache complexity"
→ Leads to: Data structures that are inherently fast, lazy evaluation,
  computation at write-time instead of read-time

Traditional: "We need monitoring to detect failures"
IFR: "The system never fails, or failures instantly self-heal"
→ Leads to: Self-healing architectures, chaos engineering, 
  designing for failure from the start
```

**IFR Questions:**

- What if the problem solved itself?
- What if the harmful element became useful?
- What if we needed zero of the problematic component?
- What's the result we want with zero cost/complexity?

## Contradiction Types

### Technical Contradictions

Improving one parameter worsens another:

| Improving | Worsens | Example |
|-----------|---------|---------|
| Speed | Accuracy | Fast processing loses precision |
| Security | Usability | Strong auth frustrates users |
| Reliability | Cost | Redundancy is expensive |
| Features | Simplicity | More capability, more complexity |
| Throughput | Latency | Batching improves throughput, hurts latency |

### Physical Contradictions

Same element must have opposite properties:

```
"The timeout must be SHORT (for fast failure detection)
 AND LONG (to tolerate network variance)"

"The cache must be LARGE (for high hit rate)
 AND SMALL (for fast invalidation and low memory)"

"The API must be STABLE (for clients)
 AND CHANGING (for evolution)"
```

## The 40 Inventive Principles (Software-Adapted)

### Most Applicable to Software Engineering

| # | Principle | Software Application |
|---|-----------|---------------------|
| 1 | **Segmentation** | Microservices, sharding, pagination, chunked processing |
| 2 | **Taking Out** | Extract the problematic part; separation of concerns |
| 3 | **Local Quality** | Different configs per environment; adaptive algorithms |
| 5 | **Merging** | Combine operations (batch), merge services, reduce round-trips |
| 6 | **Universality** | Multi-purpose components, plugins, generic abstractions |
| 10 | **Preliminary Action** | Pre-computation, caching, lazy loading, warm-up |
| 11 | **Beforehand Cushioning** | Circuit breakers, graceful degradation, fallbacks |
| 13 | **The Other Way Round** | Push vs. pull, invert control, event-driven vs. polling |
| 15 | **Dynamization** | Dynamic scaling, feature flags, runtime configuration |
| 17 | **Another Dimension** | Add metadata layer, versioning, time dimension (event sourcing) |
| 22 | **Blessing in Disguise** | Use errors as signals, leverage constraints, fail-fast |
| 24 | **Intermediary** | Proxy, adapter, facade, message queue, API gateway |
| 25 | **Self-Service** | Automation, self-healing, auto-scaling, self-documenting |
| 26 | **Copying** | Caching, replication, CDN, read replicas, memoization |
| 28 | **Mechanics Substitution** | Replace polling with webhooks, sync with async |
| 32 | **Color Changes** | Status indicators, logging levels, visual feedback |
| 34 | **Discarding/Recovering** | Immutability, event sourcing, garbage collection |
| 35 | **Parameter Changes** | Feature flags, A/B testing, configuration over code |
| 37 | **Thermal Expansion** | Elastic scaling, auto-tuning, adaptive thresholds |
| 40 | **Composite Structures** | Composition over inheritance, layered architecture |

### Principle Application Examples

**Segmentation (#1):**

```
Problem: Monolith is slow to deploy and scale
Contradiction: Need unified system (consistency) AND independent scaling
Apply: Segment by bounded context → Microservices with clear boundaries
```

**Preliminary Action (#10):**

```
Problem: Complex queries are slow
Contradiction: Need real-time results AND complex aggregations
Apply: Pre-compute during write → Materialized views, denormalization
```

**The Other Way Round (#13):**

```
Problem: Polling for updates wastes resources
Contradiction: Need immediate updates AND low server load
Apply: Invert the flow → Webhooks, Server-Sent Events, WebSockets
```

**Intermediary (#24):**

```
Problem: Direct client-service coupling is fragile
Contradiction: Need loose coupling AND reliable communication
Apply: Add intermediary → Message queue, API gateway, service mesh
```

## Resolving Physical Contradictions

When the same element needs opposite properties, use separation:

### Separation in Time

```
"Cache must be fresh AND cached"
→ Time-based invalidation: cached now, fresh later
→ TTL strategies, cache warming schedules

"System must accept AND reject requests"  
→ Rate limiting: accept up to threshold, reject after
→ Token bucket, sliding window
```

### Separation in Space

```
"Data must be local (fast) AND distributed (resilient)"
→ Multi-region with local reads, distributed writes
→ Read replicas, write-through caching

"Logs must be detailed (debugging) AND minimal (performance)"
→ Detailed in dev, minimal in prod
→ Different log levels per environment
```

### Separation by Condition

```
"Authentication must be strict AND frictionless"
→ Strict for sensitive operations, frictionless for low-risk
→ Step-up authentication, risk-based auth

"Validation must be thorough AND fast"
→ Thorough for untrusted input, fast for internal
→ Trust boundaries, schema validation at edges only
```

### Separation in Scale/Level

```
"API must be stable AND evolving"
→ Stable interface, evolving implementation
→ Versioning, backward compatibility, API contracts
```

## Contradiction Analysis Framework

### Step 1: State the Contradiction Clearly

```
Template:
"We need [PARAMETER A] to be [STATE 1] for [BENEFIT 1]
 BUT also [STATE 2] for [BENEFIT 2]"

Example:
"We need response time to be FAST for user experience
 BUT also processing to be THOROUGH for accuracy"
```

### Step 2: Identify the Conflicting Requirements

List what each state provides:

```
FAST processing:              THOROUGH processing:
- Better UX                   - Higher accuracy  
- Lower timeout risk          - Complete validation
- Reduced server load         - Fewer edge case bugs
```

### Step 3: Apply Separation Principles

Try each separation type:

```
Time: Can we be fast first, thorough later? (async processing)
Space: Can we be fast here, thorough there? (edge vs. origin)
Condition: Can we be fast sometimes, thorough others? (adaptive)
Scale: Can fast and thorough exist at different levels? (layered validation)
```

### Step 4: Apply Inventive Principles

Scan relevant principles:

```
#1 Segmentation: Break into fast-path and slow-path
#10 Preliminary Action: Pre-compute thorough checks
#13 Other Way Round: Push complexity to write-time
#24 Intermediary: Queue for async thorough processing
#26 Copying: Cache thorough results for fast retrieval
```

### Step 5: Synthesize Solutions

Combine insights into concrete approaches:

```
Solution: Layered validation with async completion
- Edge: Fast syntactic validation (immediate)
- Queue: Thorough semantic validation (async)
- Response: Immediate acknowledgment, webhook for final result
```

## Software Engineering Contradiction Patterns

### Speed vs. Accuracy

```
Contradiction: Need fast results AND accurate results
TRIZ Solutions:
- #1 Segmentation: Fast approximate first, accurate refinement
- #10 Preliminary Action: Pre-compute accurate, serve cached
- #26 Copying: Cache accurate results, serve instantly
Example: Typeahead with fast fuzzy match, async precise ranking
```

### Security vs. Usability

```
Contradiction: Need strong security AND frictionless UX
TRIZ Solutions:
- Separation by Condition: Risk-based authentication
- #3 Local Quality: Stricter for sensitive operations
- #15 Dynamization: Adaptive security based on context
Example: Passwordless for trusted device, MFA for new device
```

### Consistency vs. Availability

```
Contradiction: Need strong consistency AND high availability (CAP)
TRIZ Solutions:
- Separation in Space: Consistent within region, eventually across
- #1 Segmentation: Some data strongly consistent, some eventual
- #17 Another Dimension: Version vectors, conflict resolution
Example: CRDT for collaborative editing, strong consistency for transactions
```

### Simplicity vs. Capability

```
Contradiction: Need powerful features AND simple interface
TRIZ Solutions:
- #1 Segmentation: Progressive disclosure, advanced mode
- #6 Universality: Composable primitives vs. monolithic features
- #24 Intermediary: Abstraction layers hiding complexity
Example: Simple API with sensible defaults, advanced options available
```

## Resource Analysis

TRIZ teaches using existing resources before adding new ones:

### Resource Types

| Type | Examples | Software Analog |
|------|----------|-----------------|
| Substance | Materials at hand | Existing data, unused fields |
| Field | Energy sources | Compute, network, existing events |
| Space | Unused volume | Memory, disk, idle cores |
| Time | Idle periods | Off-peak processing, startup time |
| Information | Available signals | Logs, metrics, existing state |
| Function | Existing capabilities | Libraries, services already running |

### Finding Hidden Resources

```
Before: "We need a new service to track user sessions"
Resource Analysis:
- What data already exists? → Auth tokens have user identity
- What's already running? → Load balancer sees all requests
- What's unused? → Request headers have room for session ID
Solution: Encode session in existing auth flow, no new service
```

## Evolution Patterns

TRIZ identifies how systems evolve—use to anticipate future state:

| Pattern | Description | Software Example |
|---------|-------------|------------------|
| Increasing Ideality | Systems evolve toward IFR | Serverless (no server management) |
| Uneven Development | Parts evolve at different rates | Legacy + modern microservices |
| Transition to Micro | Components get smaller | Monolith → microservices → functions |
| Dynamization | Static becomes dynamic | Config files → feature flags → ML |
| Increased Controllability | More fine-grained control | Manual → automated → autonomous |

## Verification Checklist

- [ ] Stated the contradiction explicitly (technical or physical)
- [ ] Defined the Ideal Final Result
- [ ] Attempted separation (time, space, condition, scale)
- [ ] Reviewed applicable inventive principles
- [ ] Analyzed available resources before adding new ones
- [ ] Solution resolves contradiction, not just compromises
- [ ] Considered evolution trajectory of the system

## Integration with Other Thinking Models

- **First Principles**: Break down assumptions before applying TRIZ
- **Inversion**: What would make the contradiction worse? Avoid that.
- **Systems Thinking**: Trace contradiction through feedback loops
- **Second-Order**: Consider downstream effects of resolving the contradiction

## Key Questions

- "What is the exact contradiction I'm facing?"
- "What would the Ideal Final Result look like?"
- "Can I separate the conflicting requirements in time, space, or condition?"
- "What resources already exist that I'm not using?"
- "Which inventive principle fits this contradiction pattern?"
- "Am I truly resolving the contradiction, or just compromising?"

## Altshuller's Insight

"You can wait a hundred years for enlightenment, or you can solve the problem in 15 minutes with these principles."

The power of TRIZ is that inventive solutions follow patterns. What seems like creative genius is often systematic application of principles that have worked across domains for decades.
