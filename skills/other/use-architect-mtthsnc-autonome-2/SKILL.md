---
name: use-architect
description: Use after design brainstorm and before creating implementation plans to validate architectural decisions
---

Good architecture makes change easy. This skill validates your design against architectural principles before you build, catching structural issues when they're cheapest to fix.

**Core principle:** Architecture review catches issues at $10 vs $1000 fix later.

# When to Use

- After `use-brainstorm` produces a design
- Before `use-plan-create` creates implementation plan
- When modifying existing architecture significantly
- When architecture questions arise during implementation

**When NOT to use:**
- One-line changes or trivial fixes
- Pure refactoring (architecture already validated)
- When architecture is already documented and unchanged

# The Process

## 1. Understand the Design

- Read design doc from brainstorm phase OR ask for design summary
- Identify domain (frontend/backend/fullstack) from context
- Understand goals, constraints, success criteria

## 2. Detect Domain

**Check for indicators:**
- Frontend: mentions React/Vue/Angular, components, UI, state management
- Backend: mentions database, API, services, persistence
- Fullstack: mentions both

**If unclear:** Ask "Is this frontend, backend, or fullstack architecture?"

## 3. Universal Architectural Review

**Ask questions one at a time (prefer multiple choice):**

- **Entities & Boundaries:** What are the core components/modules? Where do boundaries lie?
- **Dependencies:** What depends on what? Is dependency direction clean?
- **Data Flow:** How does data flow through the system? Is it unidirectional?
- **Error Handling:** Where are errors caught? What's the error propagation strategy?
- **Change Vectors:** What's most likely to change? Will those changes be isolated?
- **Testability:** How will each component be tested? Are dependencies injectable?

## 4. Domain-Specific Review

**If Frontend:**
- State management architecture (local vs global, centralized vs distributed)
- Component hierarchy and composition patterns
- Data fetching strategy (where do we fetch from? how is it cached?)
- Rendering approach (client-side vs server-side vs hybrid)
- User interaction patterns (event handling, side effects)

**If Backend:**
- Service boundaries and responsibilities
- API contract design (REST/GraphQL, versioning)
- Data persistence strategy (ORM vs queries, transaction boundaries)
- Concurrency and scalability considerations
- Authentication/authorization boundaries

**If Fullstack:**
- Where does the backend responsibility end and frontend begin?
- API contract and data contract alignment
- Shared types/models (how are they synchronized?)
- Deployment boundaries (monolith vs microservices)

## 5. Document Architecture Decisions

**For significant decisions, write Architecture Decision Record (ADR):**

```markdown
# ADR: YYYY-MM-DD - [Decision Title]

## Context
[What's the situation? What problem are we solving?]

## Decision
[What did we choose and why?]

## Consequences
- Positive: [benefits]
- Negative: [trade-offs]
- Mitigations: [how we'll address negative consequences]
```

**Save to:** `docs/arch/adr/YYYY-MM-DD-[decision-slug].md`

## 6. Integration

**Output:**
- Architecture validation complete
- Any identified concerns or risks
- ADRs for significant decisions
- Recommendation: proceed to planning OR revise design

**Handoff:**
"Architecture review complete. Ready to create implementation plan with `autonome:use-plan-create`?"

# Core Principles

- **Ask one question at a time** - Don't overwhelm with multiple questions
- **Multiple choice preferred** - Easier to answer when possible
- **Domain detection first** - Tailor questions to context
- **Document decisions** - ADRs capture rationale
- **YAGNI ruthlessly** - Architecture should be simple enough

# Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Time pressure, skip architecture" | Architecture review takes 15-30 min, catches $1000 bugs at $10 cost |
| "It's simple, doesn't need review" | Simple features have architectural choices (state, boundaries, data flow) |
| "I've done this pattern before" | Experience ≠ appropriate for THIS context. Verify assumptions |
| "Can refactor later" | Refactor costs 10x more than getting architecture right first |
| "YAGNI means no architecture" | YAGNI means simple architecture, not NO architecture |
| "PM/lead says just build it" | Authority ≠ correct architecture. Good architecture makes you faster long-term |

# Red Flags - STOP

If you catch yourself thinking:
- "Just implement, we can think about architecture later"
- "This is too simple to need review"
- "I already know the right pattern, don't need to question it"
- "Write ADRs? That's overhead, let's just build"
- "Those 20 features? Just build them as CRUD, YAGNI"
- "PM says skip it, so I'll skip it"

**All of these mean: STOP. Architecture review is cheaper than debugging structural issues later.**

# Related Skills

- **autonome:use-brainstorm** - Create design before architecture review
- **autonome:use-plan-create** - Create implementation plan after architecture review
- **autonome:use-tdd** - TDD for implementation after architecture validated
