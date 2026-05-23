---
name: task-breakdown
description: FIRST STEP - Assess task complexity (0-20 score) and output orchestration level (0-3). Use for ANY non-trivial task BEFORE execution. Scores across scope, time, agents, dependencies, documentation. Level 0 (0-2 direct), Level 1 (3-7 single agent), Level 2 (8-14 multi-agent), Level 3 (15-20 epic). Outputs recommendation then exits. NOT for execution or agent selection (use agent-selector after).
---

# Task Breakdown

## Overview

Systematically decompose complex user requests into atomic, actionable subtasks with clear dependencies and execution order. This skill transforms vague feature requests into structured plans that can be executed independently or delegated to specialized agents.

## When to Use

Trigger this skill when:
- User requests span multiple domains (frontend + backend + infrastructure)
- Task scope is unclear or requires investigation before execution
- Estimated effort exceeds 30 minutes of focused work
- Multiple independent workflows must coordinate
- Clear execution order is critical for success

**DO NOT use** when:
- Task is straightforward and single-domain (use specialized agent directly)
- User provides detailed step-by-step instructions already
- Task is purely investigative (use research/explore agents instead)

## Workflow

### Step 1: Assess Task Complexity & Select Orchestration Level

Analyze the user request to determine complexity score and appropriate orchestration level.

#### Complexity Scoring (0-20 points)

Calculate total score across dimensions:

**1. Scope Breadth (0-5 points)**
- 0: Single file change
- 1: Single domain (backend OR frontend)
- 2: Two domains (backend + frontend)
- 3: Three domains (backend + frontend + infrastructure)
- 4: Four+ domains (full-stack + testing + deployment)
- 5: Epic-level (multiple features, long-term work)

**2. Time Estimate (0-5 points)**
- 0: Under 5 minutes
- 1: 5-30 minutes
- 2: 30 minutes - 2 hours
- 3: 2-8 hours (one day)
- 4: 1-5 days
- 5: 1+ weeks

**3. Agent Requirement (0-4 points)**
- 0: No agents needed (trivial)
- 1: Single agent
- 2: 2-3 agents
- 3: 4-6 agents
- 4: 7+ agents or multi-session coordination

**4. Dependencies (0-3 points)**
- 0: No dependencies
- 1: Simple linear dependencies (A → B → C)
- 2: Moderate dependencies with some parallelization
- 3: Complex dependency graph with sync points

**5. Documentation Need (0-3 points)**
- 0: No documentation needed
- 1: Simple summary sufficient
- 2: Detailed report required
- 3: Comprehensive specs + handoff docs

#### Orchestration Level Selection

Based on total complexity score:

**Level 0: Direct Execution (Score 0-2)**
```
Characteristics:
- Trivial task, obvious solution
- Single file, no agents needed
- Execution time: under 5 minutes

Action:
- Skip breakdown entirely
- Execute directly with Read/Edit/Write
- No artifacts created

Example: "Fix typo in README.md"
```

**Level 1: Agent Delegation (Score 3-7)**
```
Characteristics:
- Single-domain task
- One specialized agent
- Execution time: 5-30 minutes

Action:
- Light task description (no formal breakdown)
- Delegate to one agent via Task tool
- Create micro summary (under 500 words)

Artifacts:
.artifacts/{feature-name}/
└── summary.md (concise, 200-300 lines)

Example: "Add pagination to tasks endpoint"
```

**Level 2: Multi-Agent Orchestration (Score 8-14)**
```
Characteristics:
- Multi-domain task (2-3 domains)
- 2-4 specialized agents
- Execution time: 30min - 1 day

Action:
- Create tasks.md (bullet points, not template)
- Use parallel-coordinator for agent coordination
- Create standard summary (under 1500 words)

Artifacts:
.artifacts/{feature-name}/
├── tasks.md (generated from breakdown)
└── summary.md (standard report)

Example: "Implement user profile editing with avatar upload"
```

**Level 3: Epic Orchestration (Score 15-20)**
```
Characteristics:
- Epic-level work spanning multiple features
- 5+ agents, multi-session workflow
- Execution time: 1+ weeks

Action:
- Create epic.md (high-level roadmap)
- Break into sub-features
- Use epic-orchestrator for session continuity
- Create comprehensive reports per feature

Artifacts:
.artifacts/{epic-name}/
├── epic.md (roadmap)
├── progress.md (overall tracking)
└── features/
    ├── feature-1/
    │   ├── tasks.md
    │   └── sessions/
    │       ├── {timestamp-1}/
    │       └── {timestamp-2}/
    └── feature-2/

Example: "Migrate from REST to GraphQL"
```

#### Output Orchestration Level

After scoring, output recommendation:

```markdown
## Complexity Assessment

**Total Score:** {X} / 20

**Breakdown:**
- Scope: {score}/5 - {reasoning}
- Time: {score}/5 - {reasoning}
- Agents: {score}/4 - {reasoning}
- Dependencies: {score}/3 - {reasoning}
- Documentation: {score}/3 - {reasoning}

**Recommended Level:** Level {0-3} - {Level Name}

**Rationale:** {Why this level is appropriate}

**Next Action:** {What to do - execute directly, delegate, orchestrate, or create epic}
```

### Step 2: Extract Core Requirements

From the user request, identify:
1. **End goal**: What does "done" look like?
2. **Acceptance criteria**: How to verify success?
3. **Constraints**: Technology, timeline, or architectural limitations
4. **Implicit needs**: Tests, docs, migrations often unstated

**Example:**
```
User: "Add JWT authentication to the API"

Extracted:
- End goal: Users can authenticate via JWT tokens
- Acceptance: Login endpoint returns valid JWT, protected routes verify tokens
- Constraints: Must work with existing user model, FastAPI backend
- Implicit: Need tests, migration for new fields, frontend integration
```

### Step 3: Decompose into Atomic Tasks

Break down into **independently verifiable** subtasks. Each subtask should:
- Be completable in under 30 minutes
- Have clear input/output
- Be testable in isolation
- Map to a single domain/agent

**Task granularity:**
- ✅ GOOD: "Create Pydantic model for JWT payload with user_id and expiry"
- ❌ TOO BROAD: "Implement backend authentication"
- ❌ TOO GRANULAR: "Import jwt library"

**Decomposition strategies:**
- **Vertical slicing**: Full stack for one feature (model → API → UI)
- **Horizontal layers**: All backend, then all frontend
- **Dependency chains**: Prerequisites first (DB schema → API → UI)

### Step 4: Map Dependencies

Create a dependency graph:
```
Task A → Task B (B depends on A completing)
Task C ⊥ Task D (C and D are independent, can parallelize)
```

**Dependency types:**
- **Hard**: Must complete before (API contract before frontend types)
- **Soft**: Benefits from order but not required (tests after implementation)
- **Blocked**: External dependency (waiting for design approval)

### Step 5: Generate Execution Plan

Output a structured plan with:

```markdown
## Execution Plan: [Feature Name]

### Phase 1: [Foundation/Setup]
- [ ] Task 1 (Domain: backend, Estimate: 15min)
- [ ] Task 2 (Domain: database, Estimate: 10min)

### Phase 2: [Core Implementation]
- [ ] Task 3 (Domain: backend, Estimate: 30min, Depends: 1,2)
- [ ] Task 4 (Domain: frontend, Estimate: 25min, Depends: 3)

### Phase 3: [Validation]
- [ ] Task 5 (Domain: testing, Estimate: 20min, Depends: 3,4)

**Total Estimate:** 100 minutes
**Parallelization Potential:** Phase 2 tasks 3,4 can overlap partially
**Recommended Agents:** fastapi-backend-expert, React Frontend Expert (F1), Pytest Master (T1)
```

### Step 6: Gate Checks

Before finalizing plan, validate:
- ✅ Every task has clear acceptance criteria
- ✅ No task exceeds 30 minutes estimated effort
- ✅ All dependencies are explicit and resolvable
- ✅ Plan covers implicit needs (tests, docs, migrations)
- ✅ Phases are ordered by dependency, not arbitrary preference

If validation fails, refine decomposition and repeat.

## Output Format

Return a structured breakdown as markdown:

```markdown
# Task Breakdown: [Feature Name]

**Complexity Assessment:** [Low/Medium/High]
**Total Estimated Effort:** [X minutes/hours]
**Recommended Approach:** [Execute directly / Delegate to agents / Hybrid]

## Atomic Tasks

### 1. [Task Name]
- **Domain:** [backend/frontend/infrastructure/testing/docs]
- **Estimate:** [X min]
- **Dependencies:** [None / Task IDs]
- **Agent:** [Suggested specialized agent or "main"]
- **Acceptance:** [How to verify completion]

### 2. [Task Name]
...

## Execution Order

**Phase 1 (Sequential):** Tasks 1,2
**Phase 2 (Parallel):** Tasks 3,4
**Phase 3 (Final):** Task 5

## Notes
- [Any assumptions, risks, or clarifications needed]
```

## Best Practices

1. **Bias toward smaller tasks**: Easier to track, test, and delegate
2. **Make dependencies explicit**: Never assume "obvious" order
3. **Include validation tasks**: Tests and verification are tasks too
4. **Consider rollback**: Complex changes need migration reversal plans
5. **Document assumptions**: State what you're inferring vs what user said

## Anti-Patterns

- **Analysis paralysis**: Don't over-decompose simple tasks
- **Hidden dependencies**: Every "then" implies a dependency - make it explicit
- **Ignoring implicit needs**: Tests, docs, migrations are ALWAYS needed
- **Domain mixing**: One task shouldn't span backend + frontend
- **Vague acceptance**: "Make it work" is not acceptance criteria

## Examples

### Example 1: Medium Complexity
**User:** "Add real-time notifications to dashboard"

**Breakdown:**
1. Add WebSocket endpoint to FastAPI (backend, 20min)
2. Create Notification model and table (database, 15min)
3. Implement notification sending service (backend, 25min, depends: 1,2)
4. Add WebSocket client to React (frontend, 20min, depends: 1)
5. Create NotificationBadge component (frontend, 15min, depends: 4)
6. Write integration tests (testing, 25min, depends: 3,5)

**Execution:** Phase 1 (1,2 parallel) → Phase 2 (3,4 parallel) → Phase 3 (5,6 sequential)

### Example 2: Low Complexity (No Breakdown Needed)
**User:** "Fix typo in README"

**Assessment:** Low complexity, single file, under 5 minutes
**Action:** Execute directly, skip breakdown skill

### Example 3: High Complexity
**User:** "Migrate from REST to GraphQL"

**Breakdown:** 20+ tasks across schema design, resolver implementation, client updates, testing strategy, gradual rollout plan
**Note:** High complexity triggers full breakdown with multiple phases and gate checks between phases
