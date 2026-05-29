---
name: inverse-conway
description: Align architecture and team structure using inverse Conway maneuver
allowed-tools: Read, Glob, Grep, Write, Edit
---

# Inverse Conway Maneuver Skill

## When to Use This Skill

Use this skill when:

- **Inverse Conway tasks** - Working on align architecture and team structure using inverse conway maneuver
- **Planning or design** - Need guidance on Inverse Conway approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Apply inverse Conway maneuver to deliberately design team structure for desired architecture.

## MANDATORY: Documentation-First Approach

Before applying inverse Conway:

1. **Invoke `docs-management` skill** for architecture-team alignment
2. **Verify Conway patterns** via MCP servers (perplexity)
3. **Base guidance on Team Topologies and DDD literature**

## Conway's Law

```text
Conway's Law:

"Organizations which design systems are constrained to
produce designs which are copies of the communication
structures of these organizations."
                                    — Melvin Conway, 1968

IMPLICATION:
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Team A    │    │   Team B    │    │   Team C    │
└──────┬──────┘    └──────┬──────┘    └──────┬──────┘
       │                  │                  │
       ▼                  ▼                  ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Component A │◄──►│ Component B │◄──►│ Component C │
└─────────────┘    └─────────────┘    └─────────────┘

If teams communicate, their components will integrate.
If teams don't communicate, their components won't integrate well.
```

## Inverse Conway Maneuver

```text
Inverse Conway Maneuver:

Instead of: Team structure → Architecture (emergent)
Do this:    Desired architecture → Team structure (deliberate)

PROCESS:
1. Design the target architecture
2. Identify communication patterns needed
3. Restructure teams to match
4. Architecture follows teams

┌─────────────────────────────────────────────────────────┐
│              TARGET ARCHITECTURE                        │
│                                                         │
│  ┌───────────┐   ┌───────────┐   ┌───────────┐         │
│  │ Service A │   │ Service B │   │ Service C │         │
│  └─────┬─────┘   └─────┬─────┘   └─────┬─────┘         │
│        │               │               │                │
│        └───────────────┼───────────────┘                │
│                        │                                │
│                 ┌──────┴──────┐                         │
│                 │  Platform   │                         │
│                 └─────────────┘                         │
└─────────────────────────────────────────────────────────┘
                        │
                        ▼ DESIGN TEAMS TO MATCH
┌─────────────────────────────────────────────────────────┐
│                  TEAM STRUCTURE                         │
│                                                         │
│  ┌───────────┐   ┌───────────┐   ┌───────────┐         │
│  │  Team A   │   │  Team B   │   │  Team C   │         │
│  │(Service A)│   │(Service B)│   │(Service C)│         │
│  └─────┬─────┘   └─────┬─────┘   └─────┬─────┘         │
│        │               │               │                │
│        └───────────────┼───────────────┘                │
│                        │                                │
│                 ┌──────┴──────┐                         │
│                 │  Platform   │                         │
│                 │    Team     │                         │
│                 └─────────────┘                         │
└─────────────────────────────────────────────────────────┘
```

## Architecture-Team Alignment

### Bounded Contexts to Teams

```text
DDD Bounded Context → Team Mapping:

BOUNDED CONTEXTS               TEAMS
┌─────────────────┐           ┌─────────────────┐
│  Order Context  │ ───────►  │    Order Team   │
│                 │           │                 │
│ • Order         │           │ • Full-stack    │
│ • OrderItem     │           │ • Own deployment│
│ • OrderStatus   │           │ • Own data      │
└─────────────────┘           └─────────────────┘

┌─────────────────┐           ┌─────────────────┐
│ Payment Context │ ───────►  │   Payment Team  │
│                 │           │                 │
│ • Payment       │           │ • Full-stack    │
│ • Transaction   │           │ • Own deployment│
│ • Refund        │           │ • Own data      │
└─────────────────┘           └─────────────────┘

BENEFITS:
✓ Clear ownership
✓ Reduced coordination
✓ Autonomous deployment
✓ Domain expertise
```

### Integration Seams

```text
Where Contexts Meet → Team Interfaces:

┌─────────────────┐     API Contract     ┌─────────────────┐
│  Order Context  │◄───────────────────►│ Payment Context │
│                 │                      │                 │
│     Team A      │    Clear interface   │     Team B      │
└─────────────────┘                      └─────────────────┘

INTEGRATION PATTERNS:
• Shared Kernel: Small shared code (use sparingly)
• Customer-Supplier: One serves the other
• Anti-Corruption Layer: Translate between contexts
• Open Host Service: Published API for many consumers
```

## Applying Inverse Conway

### Step 1: Define Target Architecture

```text
Architecture Vision:

1. Identify key components/services
2. Define boundaries (bounded contexts)
3. Specify integration patterns
4. Note scaling requirements
5. Consider operational aspects

Questions:
□ What services will exist?
□ What are the boundaries?
□ How will services communicate?
□ What data does each own?
□ What are deployment units?
```

### Step 2: Map Communication Needs

```text
Communication Matrix:

           │ Svc A │ Svc B │ Svc C │ Platform
───────────┼───────┼───────┼───────┼──────────
Service A  │   -   │  Low  │ None  │   High
Service B  │  Low  │   -   │ High  │   High
Service C  │ None  │ High  │   -   │   High
Platform   │ High  │ High  │ High  │    -

High = Frequent, detailed coordination
Low = Occasional, well-defined interfaces
None = No direct communication needed
```

### Step 3: Design Team Structure

```text
Team Structure Rules:

1. ONE TEAM PER BOUNDED CONTEXT
   - Full ownership
   - Reduced dependencies
   - Clear accountability

2. MINIMIZE TEAM DEPENDENCIES
   - If A and B need heavy coordination → same team
   - If A and B are independent → separate teams
   - If dependency is API-only → separate teams OK

3. SIZE APPROPRIATELY
   - 5-9 people per team
   - Can understand entire domain
   - Manageable cognitive load

4. PLATFORM TEAMS FOR SHARED NEEDS
   - Common infrastructure
   - Shared services
   - Self-service focus
```

### Step 4: Plan Transition

```text
Transition Approaches:

GRADUAL EVOLUTION:
Week 1-4: Pilot new team structure with one boundary
Week 5-8: Expand to adjacent boundaries
Week 9+: Full rollout

BIG BANG (Risky):
Day 1: New structure in place
Requires: Clear communication, quick stabilization

HYBRID:
• Announce new target structure
• Allow organic movement
• Timebox the transition
```

## Common Patterns

### Monolith to Microservices

```text
FROM:
┌─────────────────────────────────┐
│         Monolith Team           │
│    (Everyone on everything)     │
└─────────────────────────────────┘

TO:
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│   Orders    │ │  Payments   │ │  Shipping   │
│    Team     │ │    Team     │ │    Team     │
└─────────────┘ └─────────────┘ └─────────────┘
        │             │               │
        └─────────────┼───────────────┘
                      │
              ┌───────┴───────┐
              │   Platform    │
              │     Team      │
              └───────────────┘

APPROACH:
1. Identify bounded contexts in monolith
2. Assign teams to contexts
3. Extract services gradually
4. Move code ownership with teams
```

### Feature Teams to Stream-Aligned

```text
FROM:
┌──────────────────────────────────────────────┐
│              Feature Teams                    │
│  ┌────────┐  ┌────────┐  ┌────────┐          │
│  │Feature │  │Feature │  │Feature │          │
│  │ Team 1 │  │ Team 2 │  │ Team 3 │          │
│  └────────┘  └────────┘  └────────┘          │
│  (Work on any part of codebase)              │
└──────────────────────────────────────────────┘

TO:
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│   Stream    │ │   Stream    │ │   Stream    │
│  Aligned 1  │ │  Aligned 2  │ │  Aligned 3  │
│             │ │             │ │             │
│ OWN: Search │ │ OWN: Cart   │ │OWN: Checkout│
└─────────────┘ └─────────────┘ └─────────────┘

APPROACH:
1. Identify value streams
2. Map current contributions by stream
3. Assign teams to streams
4. Transfer ownership gradually
```

## Anti-Patterns

```text
Inverse Conway Anti-Patterns:

1. IGNORING CURRENT STATE
   - Don't try to change everything overnight
   - Acknowledge existing structure
   - Plan gradual transition

2. FORCING ARCHITECTURE ON UNWILLING TEAMS
   - Need buy-in, not mandate
   - Explain the why
   - Support the transition

3. CREATING UNREALISTIC BOUNDARIES
   - Boundaries should be natural
   - Too many teams = too much coordination
   - Too few teams = cognitive overload

4. NEGLECTING PLATFORM NEEDS
   - Stream-aligned teams need platform support
   - Platform teams reduce duplication
   - Self-service is the goal

5. IGNORING PEOPLE
   - Skills need to match teams
   - Career paths matter
   - Cultural fit important
```

## Assessment Template

```markdown
# Inverse Conway Analysis: [Organization]

## Current State

### Current Architecture
```text
[Diagram of current architecture]
```

### Current Teams

| Team | Responsibilities | Size |
|------|-----------------|------|
| [Name] | [What they own] | [N] |

### Misalignments

| Issue | Impact |
|-------|--------|
| [Misalignment] | [Effect] |

## Target State

### Target Architecture

```text
[Diagram of target architecture]
```

### Target Teams

| Team | Type | Responsibilities |
|------|------|-----------------|
| [Name] | [Type] | [What they'll own] |

## Communication Analysis

### Required Interactions

| From | To | Frequency | Type |
|------|-----|-----------|------|
| [Team] | [Team] | [H/M/L] | [API/Collab] |

## Transition Plan

### Phase 1: [Timeframe]

- [Action]
- [Action]

### Phase 2: [Timeframe]

- [Action]
- [Action]

## Risks

| Risk | Mitigation |
|------|------------|
| [Risk] | [Strategy] |

## Workflow

When applying inverse Conway:

1. **Document Current State**: Architecture and teams today
2. **Design Target Architecture**: What structure do we want?
3. **Map Boundaries**: Identify bounded contexts
4. **Design Team Structure**: Teams to match architecture
5. **Identify Transitions**: How to get from current to target
6. **Plan Execution**: Phased approach
7. **Execute and Adapt**: Iterate based on feedback

## References

For detailed guidance:

---

**Last Updated:** 2025-12-26
