---
name: technical-planning
description: Use when creating implementation plans for features or tasks. Focuses on tactical execution planning with clear tasks, dependencies, and success criteria.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Technical Planning Skill

Create actionable implementation plans for features and tasks.

## Core Principle

**A good plan turns a vague goal into concrete, executable steps.**

## Planning vs Architecture

**Technical Planning (this skill):**

- Tactical: "How do I build feature X?"
- Specific implementation steps
- Days to weeks of work
- Breaks work into tasks
- Focuses on execution

**Architecture Design (architecture-design skill):**

- Strategic: "How should the system be structured?"
- High-level design decisions
- Weeks to months of impact
- Defines components and patterns
- Focuses on structure

**Use planning for:**

- Implementing specific features
- Breaking down work into tasks
- Sequencing implementation steps
- Estimating complexity

**Use architecture for:**

- Designing new systems
- Major refactors
- Technology choices
- Long-term strategy

## The Planning Process

### 1. Understand Requirements

**Clarify what success looks like:**

- What exactly needs to be built?
- What problem does it solve?
- What are the acceptance criteria?
- What's in scope vs out of scope?

**Ask questions:**

- Who will use this?
- What's the expected behavior?
- What edge cases should be handled?
- Are there performance requirements?
- Security concerns?

### 2. Analyze Current State

**Understand what exists:**

- What code is already there?
- What patterns are in use?
- What can be reused?
- What needs to change?

**Research:**

```bash
# Find similar implementations
grep -r "similar_pattern" .

# Find related files
find . -name "*related*"

# Check existing tests
grep -r "test.*similar" test/
```

### 3. Break Down Into Tasks

**Good tasks are:**

- **Specific**: "Add user authentication" ❌ → "Create login API endpoint" ✅
- **Testable**: Clear success criteria
- **Right-sized**: Hours to days, not weeks
- **Independent** (when possible): Can be done in any order
- **Ordered** (when dependencies exist): Clear sequence

**Task template:**

```markdown
### Task: [Specific deliverable]

**What:** [Concrete description]
**Why:** [Reasoning for this approach]
**Dependencies:** [None, or list of task numbers]
**Complexity:** S | M | L
**Success criteria:**
- [ ] Criterion 1
- [ ] Criterion 2

**Files affected:**
- `path/to/file1.ts`
- `path/to/file2.ts`

**Testing approach:**
[How to verify this works]
```

### 4. Identify Dependencies

**Task dependencies:**

- **Blocks**: Task A must finish before Task B starts
- **Blocked by**: Task B can't start until Task A finishes
- **Related**: Tasks that should coordinate

**Example:**

```
Task 1: Create database schema (no dependencies)
Task 2: Create API endpoint (depends on Task 1)
Task 3: Create UI component (depends on Task 2)
Task 4: Add tests (depends on Tasks 1-3)
```

**Parallel vs Sequential:**

```
Can be parallel:
  Task A: Frontend component
  Task B: Backend API
  (If API contract is defined)

Must be sequential:
  Task 1: Database migration
  Task 2: Update queries to use new schema
  (Task 2 depends on Task 1)
```

### 5. Estimate Complexity

**Use relative sizing, not time:**

- **S (Small)**: 1-4 hours, straightforward
- **M (Medium)**: 4-8 hours, moderate complexity
- **L (Large)**: 1-2 days, complex or uncertain

**If task is > L:** Break it down further

**Complexity factors:**

- How well-understood is the requirement?
- How many unknowns?
- How many files need changes?
- Integration complexity?
- Testing complexity?

**Examples:**

- S: Add validation rule to existing form
- M: Create new API endpoint with tests
- L: Implement new payment provider integration

### 6. Define Testing Strategy

**How will we verify it works?**

- Unit tests for business logic
- Integration tests for API endpoints
- E2E tests for user workflows
- Manual testing steps

**Example:**

```markdown
## Testing Strategy

**Unit tests:**
- Test validation logic
- Test calculation functions
- Test error handling

**Integration tests:**
- Test API endpoint with real database
- Test with various input scenarios
- Test error responses

**E2E tests:**
- User can complete full workflow
- Error messages display correctly
- Success case works end-to-end

**Manual testing:**
- [ ] Test in Chrome
- [ ] Test in Firefox
- [ ] Test on mobile
```

## Plan Document Structure

```markdown
# Implementation Plan: [Feature Name]

**Created:** YYYY-MM-DD
**Estimated complexity:** S | M | L | XL
**Status:** Draft | Approved | In Progress | Complete

## Goal

[One paragraph: What are we building and why?]

## Current State

[What exists today that's relevant to this plan?]
[What needs to change?]
[What can be reused?]

## Proposed Approach

[High-level strategy: How will we build this?]
[Key technical decisions made]
[Alternatives considered and why not chosen]

## Tasks

### Phase 1: Foundation

#### Task 1.1: [Specific deliverable] (Complexity: S)

**What:** [Concrete description of what needs to be built]

**Why:** [Reasoning for this approach]

**Dependencies:** None

**Success criteria:**
- [ ] Criterion 1 (testable)
- [ ] Criterion 2 (testable)
- [ ] All tests pass

**Files affected:**
- `src/components/Feature.tsx` (create)
- `src/types/feature.ts` (update)

**Testing approach:**
- Unit test for component logic
- Integration test for data flow

---

#### Task 1.2: [Next task] (Complexity: M)

**What:** [Description]

**Why:** [Reasoning]

**Dependencies:** Task 1.1

**Success criteria:**
- [ ] Criterion 1
- [ ] Criterion 2

**Files affected:**
- `api/routes/feature.ts` (create)

**Testing approach:**
- Integration test for API endpoint

---

### Phase 2: Integration

[Additional tasks organized by phase]

## Testing Strategy

**Overall approach:**
[How we'll verify the entire feature works]

**Test coverage goals:**
- Critical paths: 100%
- Happy paths: 100%
- Edge cases: 80%

## Risks & Considerations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Database migration fails | High | Test in staging first, have rollback plan |
| API performance slow | Medium | Add caching, monitor metrics |

## Out of Scope

**Explicitly NOT included in this plan:**
- [Feature A - deferred to v2]
- [Integration B - separate work]
- [Optimization C - premature]

## Open Questions

- [ ] Should we use library X or Y?
- [ ] What's the rate limit for the external API?
- [ ] Do we need to support IE11?

## Success Metrics

**How we'll know this is successful:**
- Feature ships to production
- All tests pass
- Performance meets requirements (< 200ms response)
- Zero critical bugs in first week

## References

- [Related documentation]
- [Design mockups]
- [API specifications]
- [Similar implementations]
```

## Task Breakdown Strategies

### By Layer

```
Frontend tasks:
- Task 1: Create UI component
- Task 2: Add form validation
- Task 3: Connect to API

Backend tasks:
- Task 4: Create API endpoint
- Task 5: Add business logic
- Task 6: Database queries

Infrastructure:
- Task 7: Update deployment config
```

### By Feature Slice

```
User Authentication (vertical slice):
- Task 1: Login form (frontend)
- Task 2: Login API (backend)
- Task 3: Session management
- Task 4: E2E test for login flow

Password Reset (vertical slice):
- Task 5: Password reset form
- Task 6: Password reset API
- Task 7: Email notification
- Task 8: E2E test for reset flow
```

### By Priority

```
Must Have (P0):
- Task 1: Core functionality
- Task 2: Critical path

Should Have (P1):
- Task 3: Nice to have feature
- Task 4: Enhancement

Could Have (P2):
- Task 5: Polish
- Task 6: Optimization
```

## Planning Best Practices

### Start Simple

**Don't over-plan:**

- Start with high-level tasks
- Add detail as you learn
- Plans evolve during implementation

**Good enough:**

- Plan should be clear enough to start
- Not every detail needs to be known upfront
- Iterate as you go

### Make Tasks Actionable

**Bad task:**

```
- Improve performance
```

**Good task:**

```
### Task 3: Optimize database queries (Complexity: M)

**What:** Add indexes to users table for email and created_at columns

**Success criteria:**
- [ ] Query time reduced from 500ms to < 50ms
- [ ] Migration runs successfully
- [ ] No impact on existing queries
```

### Document Decisions

**Why matters:**

```markdown
## Why this approach?

We chose REST over GraphQL because:
1. Team is more familiar with REST
2. Simple CRUD operations don't need GraphQL flexibility
3. Can add GraphQL later if needed

**Trade-off:** Less flexible, but simpler to implement
```

### Include Examples

**Show, don't just tell:**

```markdown
## API Design

### Endpoint: POST /api/users

**Request:**
```json
{
  "email": "user@example.com",
  "name": "John Doe"
}
```

**Response:**

```json
{
  "id": "123",
  "email": "user@example.com",
  "name": "John Doe",
  "createdAt": "2024-01-01T00:00:00Z"
}
```

```

## Common Planning Mistakes

### ❌ Too Vague

```

BAD:

- Implement user system
- Add features
- Make it work

```

### ❌ Too Detailed

```

BAD:

- Add import statement on line 5
- Declare variable on line 6
- Call function on line 7

```

### ❌ Missing Dependencies

```

BAD:
Task 1: Create UI
Task 2: Create API
(But UI depends on API contract)

```

### ❌ No Success Criteria

```

BAD:
Task: Add validation
(How do we know when it's done?)

GOOD:
Task: Add validation

- [ ] Email format validated
- [ ] Required fields checked
- [ ] Error messages displayed
- [ ] Tests pass

```

## Integration with Other Skills

- Use **simplicity-principles** - Keep plan simple (KISS, YAGNI)
- Use **architecture-design** - For high-level structure decisions
- Use **test-driven-development** - Include testing in tasks
- Reference **solid-principles**, **structural-design-principles** for implementation guidance

## Adaptive Planning

**Plans are living documents:**
- Update as you learn
- Add newly discovered tasks
- Remove tasks that aren't needed
- Adjust estimates based on reality

**When to update plan:**
- Discovered new requirement
- Found existing code to reuse
- Identified additional complexity
- Changed approach

**Document changes:**
```markdown
## Plan Updates

**2024-01-15:** Added Task 3.1 - need to handle legacy data format
**2024-01-20:** Removed Task 2.3 - existing helper function covers this
**2024-01-22:** Increased Task 4 from S to M - more complex than expected
```

## Planning Checklist

- [ ] Goal clearly stated
- [ ] Current state analyzed
- [ ] Approach decided and documented
- [ ] Tasks broken down
- [ ] Tasks are specific and actionable
- [ ] Dependencies identified
- [ ] Complexity estimated
- [ ] Success criteria defined for each task
- [ ] Testing strategy included
- [ ] Risks identified
- [ ] Out of scope explicitly stated
- [ ] Plan reviewed and approved

## Remember

1. **Plans are guides, not contracts** - Adapt as you learn
2. **Start simple, add detail** - Don't over-plan
3. **Make tasks actionable** - Specific and testable
4. **Document decisions** - Explain the "why"
5. **Include testing** - How will we verify it works?

**A good plan makes it easy to start coding.**
