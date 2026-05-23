---
name: task-plan-writing
description: Write rigorous implementation plans as if presenting to distinguished engineers. Use when entering plan mode, designing architecture, or when the user asks to plan a feature. Raises plan quality through expert audience framing.
---

# Plan Writing

**Plans that would satisfy a technical steering committee of distinguished engineers.**

## Context: Where Plan-Writing Fits

This skill operates within the **Execute** stage of RSID:

```
USER-DRIVEN:    Listen → Execute ← YOU ARE HERE → Reflect
AUTONOMOUS:     Ideate → Execute ← YOU ARE HERE → Reflect
```

After your plan is executed and merged, proceed to Reflect. See the **rsid** skill for the full model.

## The Core Technique

When writing implementation plans, frame your audience as the most distinguished experts in the relevant domain. This isn't pretense—it's a forcing function for rigor.

**The question to ask yourself:**

> Would this plan survive review by [distinguished expert] and their peers?

If you wouldn't present it at a design review with industry legends in the room, the plan isn't ready.

## Domain-Specific Audiences

Match the expert panel to the technology:

| Domain | Distinguished Reviewers | What They'd Scrutinize |
|--------|------------------------|------------------------|
| **TypeScript** | Anders Hejlsberg, Ryan Cavanaugh | Type safety, inference, generics design |
| **React** | Dan Abramov, Sebastian Markbåge | Component model, state management, rendering |
| **Node.js** | Ryan Dahl, Matteo Collina | Event loop, streams, performance |
| **Go** | Rob Pike, Russ Cox | Simplicity, interfaces, concurrency |
| **Rust** | Graydon Hoare, Niko Matsakis | Ownership, lifetimes, safety guarantees |
| **Python** | Guido van Rossum, Raymond Hettinger | Readability, Pythonic patterns |
| **Databases** | Michael Stonebraker, Andy Pavlo | Query patterns, indexing, consistency |
| **Distributed Systems** | Leslie Lamport, Martin Kleppmann | Consensus, ordering, failure modes |
| **Security** | Bruce Schneier, Moxie Marlinspike | Threat models, cryptographic choices |
| **APIs** | Roy Fielding, Kin Lane | REST constraints, evolvability, contracts |

## Architectural Foundation

Every plan must address how the change fits the hexagonal architecture. This isn't optional—it's how we ensure recursive self-improvement.

### The Contract-Port-Adapter Pattern

```
┌─────────────────────────────────────────────────────────────┐
│                     Application Core                        │
│  (Business logic - no platform dependencies)                │
└─────────────────────────────────────────────────────────────┘
            │                              │
            ▼                              ▼
┌───────────────────────┐      ┌───────────────────────┐
│   Contract Package    │      │   Contract Package    │
│  @scope/contract-X    │      │  @scope/contract-Y    │
│  (Pure interfaces)    │      │  (Pure interfaces)    │
└───────────────────────┘      └───────────────────────┘
            │                              │
            ▼                              ▼
┌───────────────────────┐      ┌───────────────────────┐
│     Port Package      │      │     Port Package      │
│    @scope/port-X      │      │    @scope/port-Y      │
│ (Production impl)     │      │ (Production impl)     │
└───────────────────────┘      └───────────────────────┘
            │                              │
            └──────────────┬───────────────┘
                           ▼
              ┌─────────────────────────┐
              │    Composition Root     │
              │  (Wires everything)     │
              │  Only place with        │
              │  platform globals       │
              └─────────────────────────┘
```

### Plan Must Answer These Architecture Questions

| Question | Why It Matters |
|----------|---------------|
| **What contracts are needed?** | Contracts are pure interfaces—if it emits JavaScript, it doesn't belong |
| **What ports implement them?** | Ports never use globals directly; all dependencies injected |
| **Where is the composition root?** | Only place real platform globals are referenced |
| **Are packages hermetically sealed?** | Business logic must be testable without platform |
| **How do tests inject mocks?** | Test doubles created inline, not shipped in ports |

### Capability vs Data Contracts

Plans must distinguish between:

| Type | Contract Contains | Port Contains |
|------|------------------|---------------|
| **Capability** | Interface with methods | Factory returning interface |
| **Data** | Pure types, no methods | Factory + pure functions operating on data |

**Key insight:** If you're tempted to put methods on a data structure, those methods are *operations*—they belong in the port as pure functions.

### Hermetic Primitive Ports

When wrapping platform primitives (Date, console, process, Math.random):

```typescript
// Ports must accept optional environment overrides
export type ClockEnvironmentOverrides = {
  readonly performance?: PerformanceLike | null  // undefined = host default, null = disable
  readonly dateNow?: () => number
}

export function createSystemClock(options: ClockOptions = {}): Clock {
  const env = resolveEnvironment(options.environment)
  // ...
}
```

This ensures every package is testable in isolation.

## What Distinguished Engineers Expect

### 1. Precise Problem Statement

**They'd ask:** "What exactly are we solving, and why does it matter?"

- State the problem in one paragraph
- Explain why existing solutions don't suffice
- Define success criteria upfront

**Anti-pattern:** Jumping to solution before establishing the problem.

### 2. Considered Alternatives

**They'd ask:** "What else did you consider, and why did you reject it?"

- List 2-3 alternative approaches
- Explain trade-offs of each
- Justify your chosen approach

**Anti-pattern:** Presenting one solution as if it's obviously correct.

### 3. Precise Technical Details

**They'd ask:** "Show me the types. Show me the interfaces."

- Define key data structures
- Specify function signatures
- Document contracts between components

**Anti-pattern:** Hand-waving with "we'll figure out the details during implementation."

### 4. Edge Cases and Failure Modes

**They'd ask:** "What happens when things go wrong?"

- List known edge cases
- Define error handling strategy
- Consider partial failure scenarios

**Anti-pattern:** Only describing the happy path.

### 5. Testability

**They'd ask:** "How will you know this works?"

- Describe testing strategy
- Identify what's mockable vs integration
- Define acceptance criteria

**Anti-pattern:** "We'll add tests after."

### 6. Migration and Rollout

**They'd ask:** "How do we get from here to there safely?"

- Describe incremental steps
- Identify breaking changes
- Plan for rollback if needed

**Anti-pattern:** Big-bang deployments with no incremental path.

## Plan Structure Template

```markdown
## Problem

[One paragraph describing the problem and why it matters]

## Success Criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Alternatives Considered

### Option A: [Name]
[Description, pros, cons]

### Option B: [Name]
[Description, pros, cons]

### Chosen Approach: [Name]
[Why this option wins]

## Design

### Contracts (Pure Interfaces)

```typescript
// @scope/contract-{name}
// Only interfaces and types—no runtime code

export interface [CapabilityName] {
  [method](args): ReturnType
}

// OR for data contracts:
export interface [DataName] {
  readonly [field]: Type
}
```

### Ports (Implementations)

```typescript
// @scope/port-{name}
// Factory with deps first, options second

export interface [Name]Dependencies {
  readonly [dep]: ContractType  // Other contracts needed
}

export interface [Name]Options {
  readonly [option]?: ConfigType  // Optional configuration
}

export function create[Name](
  deps: [Name]Dependencies,
  options: [Name]Options = {}
): [Name] {
  // Implementation using deps, never globals
}
```

### Composition Root

Where ports are wired together with real implementations:

```typescript
// src/main.ts
const clock = createSystemClock()
const logger = createLogger({ clock, channel: createStderrChannel() })
const app = createApp({ logger })
```

### Component Breakdown

1. [Component 1]: [responsibility]
2. [Component 2]: [responsibility]

### Data Flow

[How data moves through the system—contracts at boundaries]

## Edge Cases

| Case | Handling |
|------|----------|
| [Edge case 1] | [How handled] |
| [Edge case 2] | [How handled] |

## Testing Strategy

- Unit: [what's unit tested]
- Integration: [what's integration tested]
- E2E: [acceptance scenarios]

## Implementation Steps

1. [ ] Step 1
2. [ ] Step 2
3. [ ] Step 3

## Open Questions

- [Question 1]
- [Question 2]
```

## Rigor Calibration

Match detail level to scope:

| Scope | Plan Depth | Expert Scrutiny Level |
|-------|------------|----------------------|
| **Small fix** (< 50 lines) | Minimal—just describe the change | Quick sanity check |
| **Feature** (50-500 lines) | Standard—full template | Design review |
| **Architecture** (500+ lines, multi-file) | Deep—extended alternatives, migration plan | Architecture review board |
| **Breaking change** | Maximum—versioning strategy, migration guide | Full committee |

## Self-Check Questions

Before presenting a plan, verify:

### Expert Review Readiness
- [ ] Could I defend this to Anders Hejlsberg (or domain equivalent)?
- [ ] Have I shown my work on alternatives?
- [ ] Are the types/interfaces concrete, not hand-wavy?
- [ ] Have I addressed "what could go wrong"?
- [ ] Is there a clear path from current state to done?
- [ ] Would a senior engineer be able to implement from this plan alone?

### Architectural Compliance
- [ ] Are contracts pure (no runtime code, no JS emitted)?
- [ ] Do ports inject all dependencies (no direct globals)?
- [ ] Is there a clear composition root?
- [ ] Are packages hermetically sealed (testable without platform)?
- [ ] Can tests create inline mocks without shipping test code in ports?
- [ ] Do primitive ports accept environment overrides?
- [ ] Are capability vs data contracts clearly distinguished?

## Anti-Patterns

### The "Trust Me" Plan

**Wrong:**
> "We'll refactor the auth system to be more modular."

**Right:**
> "We'll extract `AuthService` into three components: `TokenValidator`, `SessionManager`, and `PermissionChecker`. Here are the interfaces..."

### The "Happy Path Only" Plan

**Wrong:**
> "User clicks button, API returns data, we display it."

**Right:**
> "User clicks button. If network fails, show cached data with stale indicator. If API returns 429, back off exponentially. If response is malformed, log error and show fallback UI."

### The "Implementation as Plan" Plan

**Wrong:**
> "1. Create file. 2. Add function. 3. Call function."

**Right:**
> "1. Define the `CachePolicy` interface. 2. Implement `LRUCachePolicy` with configurable max size. 3. Integrate into `DataFetcher` via dependency injection."

### The "Kitchen Sink" Plan

**Wrong:**
> 47-step plan covering every micro-decision

**Right:**
> Focused plan covering decisions that matter, leaving obvious details to implementation

### The "Leaky Abstraction" Plan

**Wrong:**
```typescript
// Port that uses globals directly
export function createLogger(): Logger {
  return {
    info(msg) {
      console.log(new Date().toISOString(), msg)  // NO! Direct globals
    }
  }
}
```

**Right:**
```typescript
// Port with injected dependencies
export interface LoggerDeps {
  channel: OutChannel
  clock: Clock
}

export function createLogger(deps: LoggerDeps): Logger {
  return {
    info(msg) {
      deps.channel.write(`${deps.clock.timestamp()} ${msg}`)
    }
  }
}
```

### The "Methods on Data" Plan

**Wrong:**
```typescript
// Contract with operations baked in
export interface Dag<T> {
  nodes: Map<string, DagNode<T>>
  getTopologicalOrder(): string[]  // NO! This is an operation
  validate(): ValidationResult     // NO! This is an operation
}
```

**Right:**
```typescript
// Contract: just the data
export type Dag<T> = readonly DagNode<T>[]

// Port: operations as pure functions
export function getTopologicalOrder<T>(dag: Dag<T>): string[]
export function validateDag<T>(dag: Dag<T>): ValidationResult
```

## Integration with Claude Code

When entering plan mode (`/plan` or `EnterPlanMode`):

1. Identify the domain and select appropriate expert panel
2. Use the plan structure template
3. Apply rigor calibration based on scope
4. Verify architectural compliance (contract-port separation)
5. Run through self-check questions before presenting
6. Use `ExitPlanMode` only when plan meets distinguished engineer standards

### Related Skills

| Skill | When to Use |
|-------|-------------|
| **rsid** | Outer context—after merge, reflect and record learnings |
| **coding-patterns** | Reference for contract-port architecture, hermetic primitives, TypeScript patterns |
| **tsc-reviewer** (agent) | After implementation, verify plan was followed correctly |
| **effective-git** | Atomic commits that match plan steps |
| **verification-pipeline** | Ensure plan includes verification gates |

### Architectural Pattern Reference

The `coding-patterns` skill contains the authoritative reference for:

- Contract package structure (`@scope/contract-{name}`)
- Port package structure (`@scope/port-{name}`)
- Factory function argument order (deps first, options second)
- Hermetic primitive port patterns
- Composition root wiring
- Testing with inline mocks

**When writing a plan, invoke `coding-patterns` if you need detailed guidance on any of these patterns.**

## The Standard

**A good plan is one you'd be proud to present to the creators of the tools you're using.**

If Anders Hejlsberg would raise an eyebrow at your TypeScript plan, it's not ready. If Dan Abramov would question your React component boundaries, rethink them. If Leslie Lamport would find holes in your distributed system design, fill them first.

The experts aren't actually reviewing your plan—but writing as if they were produces plans worth implementing.
