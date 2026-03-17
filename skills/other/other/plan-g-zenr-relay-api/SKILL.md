---
name: plan
description: Break a scope or feature set into stories and tasks for sprint planning (Sofia Nakamura's workflow)
disable-model-invocation: true
---

Plan the following scope: $ARGUMENTS

## Step 1 — Understand the Scope
- Read the request and identify all deliverables
- Read the existing codebase to understand what exists and what's new
- Identify which layers are affected (see Layers in project config)

## Step 2 — Break Into Stories
Each story is a vertical slice of functionality that can be independently delivered and demonstrated.

Format each story as:
```markdown
### Story: <title>
**As a** <user/developer/operator>
**I want** <capability>
**So that** <business value>

**Acceptance Criteria:**
- [ ] <specific, testable criterion>

**Files Affected:**
- <layer/file> — <what changes>
- <test file> — <what tests needed>

**Estimated Complexity:** Small / Medium / Large
```

## Step 3 — Order by Dependency
- Identify dependencies between stories (Story B requires Story A)
- Order stories so dependencies are satisfied
- Mark stories that can be parallelized

## Step 4 — Break Stories Into Tasks
Each story should have 2-6 concrete tasks:
```markdown
**Tasks:**
1. [ ] Add Pydantic models to the models file
2. [ ] Add service method to the service layer
3. [ ] Add API endpoint to the appropriate router
4. [ ] Write tests (success, validation, error paths)
5. [ ] Update project documentation and env example file
6. [ ] Run /verify and /review
```

## Step 5 — Risk Assessment
For each story, identify:
- **Technical risks** — unknown APIs, complex logic, concurrency concerns
- **Dependencies** — external libraries, config changes, breaking changes
- **Testing complexity** — needs mock implementations, special fixtures

## Step 6 — Output Sprint Plan
```markdown
# Sprint Plan: <scope title>

## Summary
- Stories: X
- Total tasks: X
- Estimated effort: Small/Medium/Large

## Story Order (dependency-aware)
1. Story A (no dependencies)
2. Story B (depends on A)

## Stories
<full story details from Step 2>

## Risks
<from Step 5>
```

## Rules
- Stories must be independently demonstrable (Sofia's requirement)
- Every story must include tests (Priya's requirement)
- Every story must maintain backwards compatibility (Sofia's requirement)
- Architecture decisions documented with rationale (Alex's requirement)