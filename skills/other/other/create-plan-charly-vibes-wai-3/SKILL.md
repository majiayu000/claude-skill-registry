---
name: create-plan
description: Design phased implementation plans with TDD approach
disable-model-invocation: true
---

# Create Implementation Plan

Create a detailed implementation plan for the requested feature.

## When Invoked

1. **If a spec file is provided**: Read it fully and begin planning
2. **If no parameters**: Ask for the feature/task description

## Process

### Step 1: Understand the Requirement

1. Read any mentioned spec files completely
2. Check existing research/documentation for related work
3. Review any previous discussions or decisions on the topic
4. Understand the scope and constraints
5. Ask clarifying questions if anything is unclear

### Step 2: Research the Codebase

**Create a todo list to track research tasks.**

1. Find relevant existing patterns and code
2. Identify integration points
3. Note conventions to follow
4. Understand the current architecture
5. Identify files that will need changes

**Use parallel research when possible:**
- Search for similar features
- Read key files that will be affected
- Check for existing tests to understand test patterns

### Step 3: Design Options (if applicable)

If multiple approaches are viable:

1. Present 2-3 design options
2. Include pros/cons for each
3. Recommend an approach (explain why)
4. Get user alignment before detailed planning

### Step 4: Write the Plan

Save to `plans/YYYY-MM-DD-description.md`:

```markdown
# [Feature Name] Implementation Plan

**Date**: YYYY-MM-DD

## Overview

[Brief description of what we're implementing]

## Related

- Spec: `specs/XX_feature.feature` (if applicable)
- Research: `research/YYYY-MM-DD-topic.md` (if applicable)
- Related issues/tickets: [references]

## Current State

[What exists now, what's missing, what needs to change]

## Desired End State

[What will exist after implementation]

**How to verify:**
- [Specific verification steps]
- [Expected behaviors]

## Out of Scope

[What we're explicitly NOT doing to prevent scope creep]

## Risks & Mitigations

[Identified risks and how we'll handle them]

## Phase 1: [Name]

### Changes Required

**File: `path/to/file.ext`**
- Changes: [Specific modifications needed]
- Tests: [What tests to write first (TDD)]

**File: `another/file.ext`**
- Changes: [Specific modifications needed]
- Tests: [What tests to write first (TDD)]

### Implementation Approach

[How we'll implement this phase - key decisions, patterns to use]

### Success Criteria

#### Automated:
- [ ] Tests pass: `npm test` (or relevant command)
- [ ] Type checking passes (if applicable)
- [ ] Linting passes (if applicable)
- [ ] Build succeeds (if applicable)

#### Manual:
- [ ] [Specific manual verification step 1]
- [ ] [Specific manual verification step 2]

### Dependencies

[Any dependencies on other work or external factors]

---

## Phase 2: [Name]

[Continue with same structure for each phase]

---

## Testing Strategy

**Following TDD:**
1. Write tests first for each behavior
2. Watch tests fail (Red)
3. Implement minimal code to pass (Green)
4. Refactor while keeping tests green

**Test types needed:**
- Unit tests: [What to unit test]
- Integration tests: [What integration scenarios]
- E2E tests: [If applicable]

## Rollback Strategy

[How to safely rollback if something goes wrong]

## Related Links

- [Related documentation]
- [Similar implementations in the codebase]
- [External resources]
```

### Step 5: Review and Iterate

1. Present the plan to the user
2. Highlight key decisions made
3. Note any areas where feedback is particularly valuable
4. Iterate based on feedback until approved

## Guidelines

1. **Be specific**: Include actual file paths and concrete changes, not vague descriptions
2. **Follow TDD**: Plan tests before implementation for each phase
3. **Break into phases**: Each phase should be independently verifiable and take <2 hours ideally
4. **Track progress**: Use todo list throughout planning process
5. **No open questions**: Resolve all questions before finalizing (use AskUserQuestion tool)
6. **Consider the user**: Plans should be readable by both humans and AI agents
7. **Be realistic**: Account for complexity, don't oversimplify

## Usage Scenarios

**Scenario 1: Feature with spec**
```
User: Create a plan for implementing user authentication based on specs/auth.feature

Agent: I'll create an implementation plan for user authentication. Let me first read the spec and research the codebase.

[Reads spec file, searches for existing auth patterns, creates todo list]

Agent: Based on the spec and codebase research, I see we need JWT-based authentication. I found existing patterns in the API middleware that we should follow. I'll create a 3-phase plan:

Phase 1: JWT token validation
Phase 2: Authentication middleware
Phase 3: Protected route integration

[Creates plan file at plans/2026-01-12-user-authentication.md]

Here's the plan I've created: [summarizes key points]

The plan follows our existing API patterns and includes TDD approach. Any feedback before we proceed?
```

**Scenario 2: No spec, just description**
```
User: I need to add pagination to the user list endpoint

Agent: I'll create a plan for adding pagination. What would you like me to document?

Let me research the codebase first to understand:
1. How other endpoints handle pagination
2. Current user list implementation
3. Database query patterns

[Creates todo list, researches in parallel]

Agent: I found that other endpoints use cursor-based pagination with the pattern from utils/pagination.ts.

I have two design options:

**Option 1: Cursor-based (Recommended)**
- Pros: Consistent with existing endpoints, handles large datasets well
- Cons: Slightly more complex client implementation

**Option 2: Offset-based**
- Pros: Simpler client implementation
- Cons: Performance issues with large offsets, inconsistent with our patterns

I recommend Option 1 for consistency. Shall I proceed with that approach?

[After confirmation, creates detailed plan]
```

**Scenario 3: Complex feature requiring exploration**
```
User: Create a plan for real-time notifications

Agent: Real-time notifications is a complex feature. Before I can create a detailed plan, I need to research several technical decisions:

1. Transport mechanism (WebSockets, SSE, polling?)
2. Current infrastructure capabilities
3. Scalability requirements
4. Client-side integration points

Let me research these first, then I'll present options and create the detailed plan. [Uses research command or explores]

[After research, presents 2-3 options with tradeoffs, gets alignment, then creates detailed plan]
```
