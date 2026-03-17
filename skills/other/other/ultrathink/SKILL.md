---
name: ultrathink
description: Deep planning philosophy for craftsman-level architecture. Transforms planning from research-then-design to research-question-simplify-design. Use when --deep flag is set, for epics, complex features (30+ tasks), or when auto_deep_mode preference is enabled. Invokes assumption questioning, codebase soul analysis, and ruthless simplification. (project)
---

<objective>
Elevate planning from competent to insanely great through systematic assumption questioning, deep codebase understanding, and ruthless simplification.

> "The people who are crazy enough to think they can change the world are the ones who do."

**Core philosophy**:

- Think Different - Question every assumption before designing
- Obsess Over Details - Understand the codebase's soul, not just its code
- Plan Like Da Vinci - Architecture so elegant it feels inevitable
- Simplify Ruthlessly - Remove complexity until nothing is left to take away
- Iterate Relentlessly - First solution is never good enough

**When activated**:

- `--deep` flag on any workflow command
- All epic workflows (via `deep_planning_triggers.epic_features`)
- Features with 30+ estimated tasks (via `deep_planning_triggers.complexity_threshold`)
- New architectural patterns (via `deep_planning_triggers.architecture_change`)
- `planning.auto_deep_mode: true` in user preferences

**Outputs**:

- Enhanced plan.md with assumption inventory
- craftsman-decision.md artifact documenting deep thinking
- Simpler architecture than standard planning would produce
</objective>

<quick_start>
Execute craftsman planning workflow:

1. **Think Different** - Create assumption inventory, challenge each one
2. **Obsess Over Details** - Analyze codebase soul (patterns, philosophy)
3. **Plan Like Da Vinci** - Sketch architecture before implementing
4. **Simplify Ruthlessly** - Find minimum viable architecture
5. **Iterate** - Compare alternatives, refine until inevitable

Key principle: One hour of deeper thinking saves ten hours of rework.

Trigger phrases: "ultrathink", "deep planning", "craftsman mode", "--deep"
</quick_start>

<workflow>
<step number="1">
**Think Different: Assumption Inventory**

Before designing anything, catalog and challenge every assumption.

**Create assumption inventory**:

```markdown
## Assumption Inventory

| # | Assumption | Source | Challenge Question | Resolution |
|---|------------|--------|-------------------|------------|
| 1 | Users need X feature | Spec | Is this the real problem or a symptom? | [Validated/Changed/Removed] |
| 2 | We need a database table | Common pattern | Could we use existing data structures? | [Validated/Changed/Removed] |
| 3 | API endpoint required | Architecture | Could this be client-side only? | [Validated/Changed/Removed] |
```

**Challenge questions for each assumption**:

1. Why does it have to work this way?
2. What if we started from zero?
3. What would break if this assumption is false?
4. Is this solving the real problem or a symptom?
5. What's the simplest thing that could possibly work?

**Categories to examine**:

- **Technical assumptions** - Database, API, frontend framework
- **User assumptions** - What users actually need vs what we think they need
- **Architectural assumptions** - Why this pattern? Why these components?
- **Integration assumptions** - Do we need this external service?

**Output**: Document in craftsman-decision.md under "Assumptions Questioned"
</step>

<step number="2">
**Obsess Over Details: Codebase Soul Analysis**

Read the codebase like you're studying a masterpiece. Understand patterns, philosophy, and the *why* behind decisions.

**Analysis process**:

```bash
# Find dominant patterns
grep -r "class.*Service" src/ | wc -l
grep -r "Repository" src/ | wc -l
grep -r "Controller" src/ | wc -l

# Analyze architecture style
ls -la src/
tree src/ -L 2

# Find design decisions in comments
grep -r "// NOTE:" src/
grep -r "// DECISION:" src/
grep -r "// WHY:" src/
```

**Questions to answer**:

1. What patterns dominate this codebase? (Repository, Service, MVC, etc.)
2. What's the philosophy? (Thin controllers? Fat services? Domain-driven?)
3. Where does complexity live? (Services? Components? Database?)
4. What conventions are sacred? (Naming, file structure, error handling)
5. What anti-patterns should we avoid? (Found mistakes to not repeat)

**Soul documentation**:

```markdown
## Codebase Soul

### Dominant Patterns
- Repository pattern for data access (12 instances)
- Service layer for business logic (18 instances)
- React hooks for state management

### Philosophy
- "Thin controllers, fat services" - Controllers are routing only
- "Composition over inheritance" - No deep class hierarchies
- "Explicit over implicit" - No magic, clear data flow

### Conventions
- PascalCase for components, camelCase for hooks
- Services return Result objects, never throw
- Validation at API boundary, trust internal calls

### Anti-Patterns Observed
- src/legacy/UserManager.ts - God object, 2000+ lines (don't repeat)
- Inconsistent error handling in older services
```

**Output**: Document in craftsman-decision.md under "Codebase Soul"
</step>

<step number="3">
**Plan Like Da Vinci: Architecture Sketch**

Before writing a single line, sketch the architecture so clearly that anyone could understand it.

**Architecture sketch process**:

1. **Component diagram** - What pieces exist and how they connect
2. **Data flow** - How data moves through the system
3. **Integration points** - Where does this touch existing code?
4. **Boundaries** - What's in scope vs out of scope?

**Sketch template**:

```markdown
## Architecture Sketch

### Component Overview
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   UI Layer  │────▶│  Service    │────▶│  Repository │
│ (React/Vue) │     │   Layer     │     │   Layer     │
└─────────────┘     └─────────────┘     └─────────────┘
                           │
                    ┌──────┴──────┐
                    │  Existing   │
                    │  Services   │
                    └─────────────┘

### Data Flow
1. User action → Component → Service call
2. Service validates, orchestrates
3. Repository handles persistence
4. Response flows back through layers

### Integration Points
- Reuses: AuthService, ValidationService
- Extends: BaseRepository pattern
- New: FeatureService (single new service)

### Boundaries
IN SCOPE: User-facing feature, API endpoint, database table
OUT OF SCOPE: Admin interface (future), analytics (separate feature)
```

**Quality check**:

> "If I had to explain this design to Steve Jobs, would he say 'this is exactly right' or 'why is this so complicated'?"

**Output**: Include architecture sketch in plan.md
</step>

<step number="4">
**Simplify Ruthlessly: Minimum Viable Architecture**

The goal is elegance achieved when there's nothing left to take away.

**Simplification questions**:

1. Can we achieve this with fewer components?
2. Can we reuse more existing code?
3. Can we eliminate this abstraction?
4. Is this future-proofing or over-engineering?
5. Would a junior developer understand this in 5 minutes?

**Complexity budget**:

```markdown
## Complexity Budget

| Component | Complexity | Justification |
|-----------|------------|---------------|
| FeatureService | Medium | Core business logic requires it |
| FeatureRepository | Low | Standard pattern, simple CRUD |
| FeatureComponent | Low | UI composition of existing components |
| NewAbstraction | REJECTED | Premature - can refactor later if needed |
```

**Red flags to eliminate**:

- Abstractions with only one implementation
- Interfaces defined "for the future"
- Configuration that's never changed
- Generic utilities for specific problems
- Inheritance hierarchies deeper than 2 levels

**The simplification test**:

```
BEFORE: 5 new components, 3 new services, 2 new abstractions
AFTER:  2 new components, 1 new service, 0 new abstractions
```

**Output**: Document in craftsman-decision.md under "The Simplest Thing That Works"
</step>

<step number="5">
**Iterate: Design Alternatives**

The first solution is never good enough. Generate alternatives and compare.

**Generate 3 approaches**:

```markdown
## Design Alternatives

### Approach A: Service-Heavy (Initial Thought)
- New FeatureService, FeatureRepository, FeatureValidator
- Pros: Follows existing patterns exactly
- Cons: 3 new files, validation duplicates UserValidator

### Approach B: Composition (Simplified)
- Extend UserService with feature method
- Reuse existing ValidationService
- Pros: 1 file change, maximum reuse
- Cons: Makes UserService slightly larger

### Approach C: Functional (Alternative)
- Pure functions, no new classes
- Composable validation pipeline
- Pros: Simplest, most testable
- Cons: Deviates from OOP codebase style

### Selected: Approach B
Reasoning: Maximum reuse, minimum new code, consistent with codebase soul.
The slight growth in UserService is acceptable - it remains focused.
```

**Selection criteria**:

1. Simplicity (fewer moving parts)
2. Consistency (matches codebase soul)
3. Reuse (leverages existing code)
4. Testability (easy to verify)
5. Maintainability (junior dev can modify)

**Output**: Document in craftsman-decision.md under "Trade-offs Made"
</step>
</workflow>

<artifacts>
**craftsman-decision.md** - Required output for deep planning mode:

```markdown
# Craftsman Design Decisions

Feature: [Feature Name]
Planning Mode: Deep/Ultrathink
Date: [Date]

## Assumptions Questioned

| Assumption | Why We Questioned | Resolution |
|------------|-------------------|------------|
| [assumption] | [question] | [validated/changed/removed] |

## Codebase Soul

### Dominant Patterns
- [pattern]: [count] instances

### Philosophy
- "[principle]" - [explanation]

### Anti-Patterns to Avoid
- [file/pattern] - [why to avoid]

## The Simplest Thing That Works

We chose [approach] because:
- [reason 1]
- [reason 2]

We rejected [alternative] because:
- [reason 1]

Complexity budget spent on:
- [only necessary complexity]

## Trade-offs Made

- [Simplicity] over [feature] because [reasoning]
- [Consistency] over [optimization] because [reasoning]

## Architecture Sketch

[ASCII diagram or description]
```
</artifacts>

<integration>
**How ultrathink integrates with workflow commands**:

```bash
# Check if deep planning should be enabled
DEEP_MODE=$(bash .spec-flow/scripts/utils/load-preferences.sh --should-deep-plan --is-epic)

# Or with explicit flag
/feature "auth system" --deep   # Forces ultrathink
/epic "payment platform"        # Auto-triggers via epic_features
/plan --deep                    # Forces ultrathink for current feature
/plan --quick                   # Skips ultrathink even if pref enabled
```

**Preference hierarchy**:

1. `--deep` flag → always ultrathink
2. `--quick` flag → never ultrathink
3. `planning.auto_deep_mode: true` → ultrathink by default
4. `deep_planning_triggers` → ultrathink for matching conditions
5. Default → standard planning
</integration>

<philosophy>
> "Design is not just what it looks like and feels like. Design is how it works."

The ultrathink methodology is not about spending more time. It's about spending time on the right questions:

- Standard planning asks: "How do we build this?"
- Ultrathink asks: "Should we build this? What's the simplest way?"

Standard planning produces working solutions.
Ultrathink produces elegant solutions that feel inevitable.

The difference is not in the output format, but in the thinking process:

```
STANDARD: Research → Design → Estimate → Document
ULTRATHINK: Research → QUESTION → Design → SIMPLIFY → Estimate → Document
                        ↑                    ↑
                   assumptions           ruthlessly
```

**When to skip ultrathink**:

- Trivial changes (typo fixes, config updates)
- Well-understood patterns (CRUD endpoints, standard components)
- Time-critical hotfixes (ship now, refactor later)
- Explicit `--quick` flag

**When ultrathink is essential**:

- Epics (multi-sprint, multiple subsystems)
- Complex features (30+ tasks estimated)
- New architectural patterns
- Performance-critical code
- Security-sensitive features
</philosophy>

<workflow_integration>
## Embedded Checkpoints Across Workflow (v11.1)

Ultrathink philosophy is embedded as lightweight checkpoints throughout the workflow, not just during explicit `/ultrathink` invocations.

**Configuration**: `.spec-flow/config/ultrathink-integration.yaml`

### Phase Checkpoints

| Phase | Principle | Checkpoint |
|-------|-----------|------------|
| `/spec` | Think Different | Assumption inventory before requirements |
| `/plan` | Obsess + Simplify | Codebase soul analysis, 3 alternatives, complexity budget |
| `/tasks` | Simplify Ruthlessly | Task count validation, simplification review |
| `/implement` | Craft, Don't Code | Anti-duplication ritual, abstraction justification |
| `/optimize` | Iterate Relentlessly | Pride check, real problem validation |

### Progressive Depth

Complexity determines thinking depth automatically:

```
Trivial (<5 tasks)    → Skip checkpoints, fast path
Standard (5-30 tasks) → Lightweight inline checkpoints
Complex (30+ tasks)   → Full checkpoints + separate artifacts
Epic (multi-sprint)   → Mandatory deep planning + craftsman-decision.md
```

### Checkpoint Display

Each checkpoint displays a thinking prompt:

```
┌─────────────────────────────────────────────────────────────┐
│ 💭 ULTRATHINK CHECKPOINT: [Principle]                       │
├─────────────────────────────────────────────────────────────┤
│ Before proceeding, consider:                                │
│ • [Question 1]                                              │
│ • [Question 2]                                              │
│ • [Question 3]                                              │
└─────────────────────────────────────────────────────────────┘
```

### Spec Phase: Think Different

```markdown
## Assumption Inventory (inline in spec.md)

| # | Assumption | Source | Challenge | Status |
|---|------------|--------|-----------|--------|
| 1 | [from user input] | User request | Is this the real problem? | [validated] |
```

### Plan Phase: Obsess + Simplify

Required sections in plan.md:
- **Codebase Soul Summary** - Dominant patterns, philosophy, conventions
- **Architecture Alternatives** - At least 3 approaches for complex features
- **Complexity Budget** - Justify each new component

### Tasks Phase: Simplify Ruthlessly

Validation after task generation:
- Task count check (warn if >25)
- Simplification review (combine, remove, defer options)
- Complexity rationale (required for 20+ tasks)

### Implement Phase: Craft, Don't Code

Pre-coding ritual before each task batch:
1. **Anti-duplication search** - mgrep/Grep before creating new files
2. **Extend vs create decision** - Prefer extending existing code
3. **Abstraction check** - Must earn its complexity

### Benefits

- **Consistent quality** - Same thinking applied regardless of who runs the workflow
- **Velocity preservation** - Lightweight for simple work, deep for complex
- **Self-documenting** - Thinking artifacts capture design rationale
- **Reduced rework** - "One hour of deeper thinking saves ten hours of rework"
</workflow_integration>
