---
name: thinking-first-principles
description: Break complex problems into fundamental truths by questioning assumptions and rebuilding from irreducible components. Use for innovation, challenging status quo, or when conventional solutions fail.
---

# First Principles Reasoning

## Overview
First principles thinking strips away assumptions and conventions to reveal fundamental truths, then reconstructs solutions from those basics. This approach, championed by Elon Musk and rooted in Aristotle's philosophy, enables breakthrough solutions by escaping the trap of reasoning by analogy.

**Core Principle:** Don't accept "that's how it's always done." Reduce to fundamentals, then rebuild.

## When to Use
- Conventional approaches have failed or seem inadequate
- You're told something is "impossible" or "too expensive"
- Designing new systems/products from scratch
- Challenging industry assumptions or pricing
- Problem seems intractable using existing mental models
- You need innovation rather than incremental improvement

Decision flow:
```
Problem intractable? → yes → Are you reasoning from analogy? → yes → APPLY FIRST PRINCIPLES
                                                            ↘ no → Already at fundamentals
                  ↘ no → Standard problem-solving may suffice
```

## The Process

### Step 1: Identify Current Assumptions
List everything you "know" or assume about the problem:
- What are the constraints everyone accepts?
- What costs/limitations are considered fixed?
- What's the conventional wisdom?
- Why do people say it can't be done?

```
Example: "Rocket launches cost $65M because that's what aerospace companies charge"
Assumptions: Must buy from existing suppliers, existing designs are optimal, 
             materials must be aerospace-grade, vertical integration is too hard
```

### Step 2: Break Down to Fundamentals
Ask repeatedly: "What are we absolutely certain is true?"

Decomposition questions:
- What are the physical/mathematical constraints?
- What are the raw inputs required?
- What laws of physics/economics apply?
- What would this cost if built from raw materials?
- What is the minimum viable version?

```
Example: Rocket raw materials (aluminum, titanium, copper, carbon fiber)
         = ~2% of typical rocket price
Fundamental truth: Materials aren't the cost driver; 
                   manufacturing/overhead/margins are
```

### Step 3: Challenge Each Assumption
For each assumption, ask:
- Is this actually true, or just convention?
- What evidence supports this?
- Under what conditions would this be false?
- Who benefits from this assumption persisting?

Use the "5 Whys" to drill deeper:
```
Why is it expensive? → Suppliers charge high margins
Why? → Limited competition
Why? → High barriers to entry
Why? → Assumption that you must use existing supply chain
Why? → Nobody questioned it
```

### Step 4: Rebuild from Fundamentals
Starting ONLY from verified truths:
- What's the simplest solution that satisfies fundamental requirements?
- What new approaches become possible without false constraints?
- How would you solve this if starting from scratch today?
- What would a solution look like with 10x less resources?

```
Example: Build rockets in-house using commodity materials
         = SpaceX reduced launch costs by 10x
```

### Step 5: Validate Against Reality
- Does your reconstructed solution violate any physics/laws?
- What practical constraints remain?
- What's the minimum viable test?
- How can you prove/disprove this quickly?

## Mental Traps to Avoid

| Trap | Description | Antidote |
|------|-------------|----------|
| Reasoning by Analogy | "Others do it this way" | Ask "but is it optimal?" |
| Appeal to Authority | "Experts say it's impossible" | "What specifically makes it impossible?" |
| Sunk Cost | "We've always done it this way" | "What if we started fresh today?" |
| Complexity Bias | Assuming complex = better | "What's the simplest version?" |
| False Constraints | Accepting artificial limits | "Is this a law of physics or convention?" |

## Application Examples

### Software Architecture
```
Assumption: "We need a microservices architecture"
First Principles:
- What problem are we solving? (scalability, team independence, deployment)
- What's the minimum that achieves this?
- A modular monolith might suffice for current scale
```

### Cost Reduction
```
Assumption: "This service costs $50k/month, that's just cloud pricing"
First Principles:
- What compute/storage do we actually need?
- What are we paying for that we don't use?
- Could we reduce by 80% with right-sizing?
```

### Feature Development
```
Assumption: "Users need feature X (because competitor has it)"
First Principles:
- What job is the user trying to accomplish?
- What's the simplest way to enable that job?
- Maybe a different approach solves it better
```

## Verification Checklist
- [ ] Listed all assumptions about the problem
- [ ] Identified which assumptions are physics/math vs convention
- [ ] Challenged at least 3 "obvious" constraints
- [ ] Rebuilt solution using only verified fundamentals
- [ ] Validated that solution doesn't violate actual constraints
- [ ] Identified minimum viable test to prove/disprove approach

## Combining with Other Models
- **Inversion**: After first principles, ask "what would make this fail?"
- **Second-Order Thinking**: Consider downstream effects of your new approach
- **Pre-Mortem**: Imagine your first-principles solution failed—why?

## Key Questions
- "What do we know to be absolutely true?"
- "Why does everyone assume this constraint exists?"
- "What would we do if we had to solve this with 10% of the budget?"
- "If we were starting from scratch today, would we build it this way?"
- "What would a complete outsider try?"
