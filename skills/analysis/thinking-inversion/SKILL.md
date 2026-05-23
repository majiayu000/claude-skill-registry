---
name: thinking-inversion
description: Approach problems backward by identifying paths to failure, then systematically avoiding them. Use for risk identification, planning, and avoiding obvious mistakes.
---

# Inversion Thinking

## Overview
Inversion thinking, championed by Charlie Munger and rooted in mathematician Carl Jacobi's principle "Invert, always invert," approaches problems by considering their opposite. Instead of asking "How do I succeed?", ask "How would I guarantee failure?" then avoid those paths.

**Core Principle:** "All I want to know is where I'm going to die, so I'll never go there." — Charlie Munger

## When to Use
- Planning a new project, feature, or initiative
- Evaluating a decision before committing
- Identifying risks that optimistic thinking obscures
- Stuck on how to achieve a positive outcome
- Need to challenge assumptions in a plan
- Writing requirements or acceptance criteria

Decision flow:
```
Have a goal? → yes → Can you list ways to achieve it? → maybe → INVERT FIRST
                                                      ↘ no → Definitely invert
           ↘ no → Define goal, then invert
```

## The Process

### Step 1: Define the Goal Clearly
State what success looks like:
```
Goal: "Ship a reliable authentication system by Q2"
Goal: "Build a high-performing engineering team"
Goal: "Launch product with strong user retention"
```

### Step 2: Invert — Ask "How Would I Fail?"
List all ways to guarantee failure, ruin, or the opposite of your goal:

```
Goal: Ship reliable auth system
Inversions (How to guarantee failure):
- Skip security review and pen testing
- No rate limiting or brute force protection  
- Store passwords in plaintext
- No monitoring or alerting
- Skip edge cases in testing
- No documentation for on-call
- Single point of failure, no redundancy
- Ignore compliance requirements
- No rollback plan
- Deploy on Friday before vacation
```

### Step 3: Categorize the Failure Modes
Group by type and severity:

| Category | Failure Mode | Severity |
|----------|--------------|----------|
| Security | Plaintext passwords | Critical |
| Security | No rate limiting | High |
| Operations | No monitoring | High |
| Operations | No rollback plan | High |
| Process | Skip security review | Critical |
| Process | No documentation | Medium |
| Reliability | Single point of failure | High |

### Step 4: Convert to Avoidance Checklist
Transform each failure mode into a requirement:

```
Anti-goal: Store passwords in plaintext
→ Requirement: Use bcrypt/argon2 with appropriate work factor

Anti-goal: No rate limiting
→ Requirement: Implement rate limiting with exponential backoff

Anti-goal: Deploy Friday before vacation
→ Requirement: No deploys within 48h of team unavailability
```

### Step 5: Prioritize by Impact
Focus on avoiding the failures that would be:
- Most damaging if they occurred
- Most likely to occur without explicit prevention
- Hardest to recover from

## Application Patterns

### For Technical Design
```
Goal: Build scalable API
Invert: How to make it fail under load?
- No caching → Add caching layer
- Synchronous everything → Add async where appropriate  
- No connection pooling → Implement pooling
- N+1 queries → Eager loading, query optimization
- No circuit breakers → Add circuit breakers
```

### For Code Review
```
Goal: Merge high-quality code
Invert: What would make this PR problematic?
- Introduces security vulnerability
- Breaks existing functionality
- No tests for new behavior
- Unclear intent/poor naming
- Performance regression
- Missing error handling
```

### For Career/Team Building
```
Goal: Build successful engineering career
Invert (Munger's list of what to avoid):
- Be unreliable
- Learn only from your own mistakes (ignore others')
- Give up after first failure
- Be resentful and envious
- Stay within comfort zone
- Avoid difficult conversations
- Don't learn continuously
```

### For Project Planning
```
Goal: Successful product launch
Invert: How to guarantee launch failure?
- No user research → Validate with users
- No load testing → Load test before launch
- No rollback capability → Build rollback
- No success metrics defined → Define metrics upfront
- Team burnout → Sustainable pace
- No communication plan → Prepare stakeholder comms
```

## Combining with Pre-Mortem
Inversion + Pre-Mortem creates powerful risk identification:

1. **Inversion**: List ways the project could fail (theoretical)
2. **Pre-Mortem**: Imagine it DID fail, explain why (narrative)
3. **Synthesize**: Combine both lists, prioritize, mitigate

## Common Inversions for Software

| Domain | Goal | Key Inversions to Avoid |
|--------|------|------------------------|
| Security | Secure system | Trusting user input, weak auth, exposed secrets |
| Performance | Fast system | No caching, blocking calls, no indexes |
| Reliability | Stable system | No monitoring, no redundancy, no graceful degradation |
| Maintainability | Clean code | No tests, cryptic names, tight coupling |
| Team | High performance | Poor communication, no psychological safety, unclear goals |

## Verification Checklist
- [ ] Goal clearly defined
- [ ] Listed 10+ ways to fail/achieve opposite
- [ ] Categorized failures by type and severity
- [ ] Converted top failures to explicit requirements
- [ ] Verified plan addresses the most critical inversions
- [ ] Shared inversions with team for blind spot check

## Key Questions
- "What would guarantee failure here?"
- "What mistakes do others commonly make?"
- "What am I most likely to overlook?"
- "If this fails spectacularly, what will the postmortem say?"
- "What would I tell someone else to avoid?"
- "What would the opposite of success look like, specifically?"

## Munger's Warning
"It is remarkable how much long-term advantage people like us have gotten by trying to be consistently not stupid, instead of trying to be very intelligent."

The power of inversion is in avoiding obvious errors that optimism blinds us to. Simple avoidance often beats clever optimization.
