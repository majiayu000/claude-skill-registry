---
name: plan-generator
description: Creates structured plans from requirements. Generates comprehensive plans with steps, dependencies, risks, and success criteria. Coordinates with specialist agents for planning input and validates plan completeness. Uses template-renderer for formatted output.
version: 1.1
model: opus
invoked_by: both
user_invocable: true
tools: [Read, Write, Edit, Bash, Glob, Grep, Skill]
best_practices:
  - Coordinate with Analyst, PM, Architect for planning input
  - Break down requirements into actionable steps (<=7 per section)
  - Identify dependencies and sequencing
  - Assess risks with mitigation strategies
  - Validate plan completeness and feasibility
  - Use template-renderer for formatted plan output
error_handling: graceful
streaming: supported
related_skills: [template-renderer, writing-plans]
---

# Plan Generator Skill

<identity>
Plan Generator Skill - Creates structured, validated plans from requirements by coordinating with specialist agents and generating comprehensive planning artifacts.
</identity>

<capabilities>
- Creating plans for new features
- Planning refactoring efforts
- Planning system migrations
- Planning architecture changes
- Breaking down complex requirements
- Validating existing plans
</capabilities>

<instructions>
<execution_process>

### Step 1: Analyze Requirements

Parse user requirements:

- Extract explicit requirements
- Identify implicit requirements
- Determine planning scope
- Assess complexity

### Step 2: Coordinate Specialists

Request planning input from relevant agents:

- **Analyst**: Business requirements and market context
- **PM**: Product requirements and user stories
- **Architect**: Technical architecture and design
- **Database Architect**: Data requirements
- **UX Expert**: Interface requirements

### Step 3: Generate Plan Structure

Create plan following this **EXECUTABLE** structure:

````markdown
# Plan: [Title]

## Executive Summary

[2-3 sentence overview]

## Objectives

- [Objective 1]
- [Objective 2]

## Phases

### Phase N: [Phase Title]

**Dependencies**: [Phase numbers or 'None']
**Parallel OK**: [Yes/No - can tasks run concurrently?]

#### Tasks

- [ ] **N.1** [Task description] (~X min)
  - **Command**: `actual shell command here`
  - **Verify**: `command to verify success`
  - **Rollback**: `command to undo if needed`

- [ ] **N.2** [Task description] (~X min) [⚡ parallel OK]
  - **Command**: `...`
  - **Verify**: `...`

#### Phase N Error Handling

If any task fails:

1. Run rollback commands for completed tasks (reverse order)
2. Document error: `echo "Phase N failed: [error]" >> .claude/context/memory/issues.md`
3. Do NOT proceed to Phase N+1

#### Phase N Verification Gate

```bash
# All must pass before proceeding
[verification commands]
```
````

## Risks

| Risk   | Impact  | Mitigation | Rollback  |
| ------ | ------- | ---------- | --------- |
| [Risk] | [H/M/L] | [Strategy] | [Command] |

## Timeline Summary

| Phase | Tasks | Est. Time | Parallel? |
| ----- | ----- | --------- | --------- |
| 1     | 5     | 30 min    | Partial   |
| 2     | 3     | 20 min    | No        |

````

### The Executable Task Format (MANDATORY)

Every task MUST include:
1. **Checkbox** - `- [ ]` for progress tracking
2. **ID** - `N.M` format for reference
3. **Time estimate** - `(~X min)`
4. **Command** - Actual executable command
5. **Verify** - Command to confirm success
6. **Rollback** - Command to undo (if applicable)
7. **Parallel marker** - `[⚡ parallel OK]` if can run concurrently

### Guidelines
- Define clear objectives
- Break down into phases (<=7 phases total)
- Each phase has <=7 tasks
- Every task has executable commands
- Include verification gates between phases

### Step 4: Assess Risks

Identify risks and mitigation:

- Technical risks
- Resource risks
- Timeline risks
- Dependency risks
- Mitigation strategies

### Step 5: Validate Plan

Validate plan completeness:

- All requirements addressed
- Dependencies mapped
- Success criteria defined
- Risks identified
- Plan is feasible

### Step 6: Generate Artifacts

Create plan artifacts using the template-renderer skill:

**Using Template-Renderer**:
After creating plan data structure, invoke template-renderer to generate formatted output:

```javascript
// Map plan data to template tokens
const planTokens = {
  PLAN_TITLE: plan.title,
  DATE: new Date().toISOString().split('T')[0],
  FRAMEWORK_VERSION: 'Agent-Studio v2.2.1',
  STATUS: plan.status || 'Phase 0 - Research',
  EXECUTIVE_SUMMARY: plan.executiveSummary,
  TOTAL_TASKS: `${plan.totalTasks} atomic tasks`,
  FEATURES_COUNT: plan.features.length,
  ESTIMATED_TIME: plan.estimatedTime,
  STRATEGY: plan.strategy,
  KEY_DELIVERABLES_LIST: plan.keyDeliverables.map(d => `- ${d}`).join('\n'),
  // Phase-specific tokens
  PHASE_0_PURPOSE: plan.phases[0].purpose,
  PHASE_0_DURATION: plan.phases[0].duration,
  PHASE_1_NAME: plan.phases[1].name,
  PHASE_1_PURPOSE: plan.phases[1].purpose,
  PHASE_1_DURATION: plan.phases[1].duration,
  DEPENDENCIES: plan.phases[1].dependencies,
  PARALLEL_OK: plan.phases[1].parallelOk ? 'Yes' : 'No',
  VERIFICATION_COMMANDS: plan.phases[1].verificationCommands,
  // Add more phase tokens as needed
};

// Invoke template-renderer skill
Skill({
  skill: 'template-renderer',
  args: {
    templateName: 'plan-template',
    outputPath: `.claude/context/plans/${planId}.md`,
    tokens: planTokens
  }
});
```

**Output Locations**:
- Plan markdown (from template): `.claude/context/plans/<plan-id>.md`
- Plan JSON (structured data): `.claude/context/plans/<plan-id>.json`
- Plan summary (for quick reference)
</execution_process>

<plan_types>
**Feature Development Plan**:

- Objectives: Feature goals
- Steps: Analysis -> Design -> Implementation -> Testing
- Agents: Analyst -> PM -> Architect -> Developer -> QA

**Refactoring Plan**:

- Objectives: Code quality goals
- Steps: Analysis -> Planning -> Implementation -> Validation
- Agents: Code Reviewer -> Refactoring Specialist -> Developer -> QA

**Migration Plan**:

- Objectives: Migration goals
- Steps: Analysis -> Planning -> Execution -> Validation
- Agents: Architect -> Legacy Modernizer -> Developer -> QA

**Architecture Plan**:

- Objectives: Architecture goals
- Steps: Analysis -> Design -> Validation -> Documentation
- Agents: Architect -> Database Architect -> Security Architect -> Technical Writer
</plan_types>

<integration>
**Integration with Planner Agent**:
Planner agent uses this skill to:
- Generate plans from requirements
- Coordinate specialist input
- Validate plan completeness
- Track plan execution
</integration>

<best_practices>

1. **Coordinate Early**: Get specialist input before finalizing plan
2. **Keep Steps Focused**: <=7 steps per plan section
3. **Map Dependencies**: Clearly identify prerequisites
4. **Assess Risks**: Identify and mitigate risks proactively
5. **Validate Thoroughly**: Ensure plan is complete and feasible
</best_practices>
</instructions>

<examples>
<formatting_example>
**Example Plan Output**

**Command**: "Generate plan for user authentication feature"

**Generated Plan**:

```markdown
# Plan: User Authentication Feature

## Executive Summary
Add JWT-based authentication with login/logout endpoints. Includes password hashing, session management, and security testing.

## Objectives
- Implement JWT-based authentication
- Support login, logout, and session management
- Provide secure password handling

## Phases

### Phase 1: Setup & Design
**Dependencies**: None
**Parallel OK**: Partial

#### Tasks
- [ ] **1.1** Create feature branch (~2 min)
  - **Command**: `git checkout -b feature/auth`
  - **Verify**: `git branch --show-current | grep feature/auth`

- [ ] **1.2** Create auth module directory (~1 min) [⚡ parallel OK]
  - **Command**: `mkdir -p src/auth`
  - **Verify**: `ls -d src/auth`

- [ ] **1.3** Design auth architecture (~15 min)
  - **Command**: `Task({ task_id: 'task-1', agent: "architect", prompt: "Design JWT auth..." })`
  - **Verify**: `ls .claude/context/artifacts/auth-design.md`

#### Phase 1 Verification Gate
```bash
git branch --show-current | grep feature/auth && ls src/auth && ls .claude/context/artifacts/auth-design.md
````

### Phase 2: Implementation

**Dependencies**: Phase 1
**Parallel OK**: No (sequential TDD)

#### Tasks

- [ ] **2.1** Write auth endpoint tests (~10 min)
  - **Command**: `Task({ task_id: 'task-2', agent: "developer", prompt: "TDD: Write failing tests for /login endpoint" })`
  - **Verify**: `npm test -- --grep "login" 2>&1 | grep -E "failing|FAIL"`
  - **Rollback**: `git checkout -- src/auth/__tests__/`

- [ ] **2.2** Implement login endpoint (~15 min)
  - **Command**: `Task({ task_id: 'task-3', agent: "developer", prompt: "Implement login to pass tests" })`
  - **Verify**: `npm test -- --grep "login" 2>&1 | grep -E "passing|PASS"`

- [ ] **2.3** Implement logout endpoint (~10 min)
  - **Command**: `Task({ task_id: 'task-4', agent: "developer", prompt: "TDD: logout endpoint" })`
  - **Verify**: `npm test -- --grep "logout" 2>&1 | grep -E "passing|PASS"`

#### Phase 2 Error Handling

If any task fails:

1. Run: `git stash && git checkout -- src/auth/`
2. Document: `echo "Phase 2 failed: $(date)" >> .claude/context/memory/issues.md`
3. Do NOT proceed to Phase 3

#### Phase 2 Verification Gate

```bash
npm test -- --grep "auth" && echo "All auth tests passing"
```

### Phase 3: Security Review

**Dependencies**: Phase 2
**Parallel OK**: Yes

#### Tasks

- [ ] **3.1** Security audit (~20 min) [⚡ parallel OK]
  - **Command**: `Task({ task_id: 'task-5', agent: "security-architect", prompt: "Audit auth implementation" })`
  - **Verify**: `ls .claude/context/reports/security-audit.md`

- [ ] **3.2** Run security tests (~5 min) [⚡ parallel OK]
  - **Command**: `npm run test:security`
  - **Verify**: `echo $?` (exit code 0)

## Risks

| Risk                | Impact | Mitigation            | Rollback                  |
| ------------------- | ------ | --------------------- | ------------------------- |
| JWT secret exposure | High   | Use env vars          | Rotate secret immediately |
| SQL injection       | High   | Parameterized queries | `git revert HEAD`         |

## Timeline Summary

| Phase     | Tasks | Est. Time   | Parallel? |
| --------- | ----- | ----------- | --------- |
| 1         | 3     | 18 min      | Partial   |
| 2         | 3     | 35 min      | No        |
| 3         | 2     | 25 min      | Yes       |
| **Total** | **8** | **~78 min** |           |

````

**After plan generation**, invoke template-renderer:

```javascript
// Map plan data to tokens
const tokens = {
  PLAN_TITLE: 'User Authentication Feature',
  DATE: '2026-01-28',
  FRAMEWORK_VERSION: 'Agent-Studio v2.2.1',
  STATUS: 'Phase 0 - Research',
  EXECUTIVE_SUMMARY: 'Add JWT-based authentication with login/logout endpoints...',
  TOTAL_TASKS: '8 atomic tasks',
  FEATURES_COUNT: '1',
  ESTIMATED_TIME: '~78 minutes',
  STRATEGY: 'Foundation-first → Core features → Security review',
  KEY_DELIVERABLES_LIST: '- Authentication module\n- Login/logout endpoints\n- Security audit',
  PHASE_1_NAME: 'Setup & Design',
  PHASE_1_PURPOSE: 'Create feature branch and design architecture',
  PHASE_1_DURATION: '18 minutes',
  DEPENDENCIES: 'None',
  PARALLEL_OK: 'Partial',
  VERIFICATION_COMMANDS: 'git branch --show-current | grep feature/auth && ls src/auth',
};

// Render plan using template
Skill({
  skill: 'template-renderer',
  args: {
    templateName: 'plan-template',
    outputPath: '.claude/context/plans/user-auth-plan.md',
    tokens: tokens
  }
});
````

</formatting_example>
</examples>

## Rules

### The Iron Law of Planning

```

EVERY TASK MUST HAVE AN EXECUTABLE COMMAND

```

A task without a command is not a task - it's a wish.

### Mandatory Elements

- **Every task** must have: checkbox, ID, time estimate, command, verify
- **Every phase** must have: verification gate, error handling
- **Every risk** must have: rollback command

### Anti-Patterns (DO NOT)

| Anti-Pattern                | Problem                    | Fix                               |
| --------------------------- | -------------------------- | --------------------------------- |
| "Install X" without command | Not executable             | Add: `cp -r source dest`          |
| "Verify Y works"            | Vague                      | Add: `npm test \| grep PASS`      |
| "Update Z"                  | What file? What change?    | Add exact `Edit` or `sed` command |
| No time estimates           | Can't track progress       | Add `(~X min)` to every task      |
| No rollback                 | Can't recover from failure | Add rollback command              |

### Quality Checklist

Before finalizing any plan, verify:

- [ ] Can I copy-paste every command and run it?
- [ ] Does every verify command have a clear pass/fail output?
- [ ] Is there a rollback for every destructive operation?
- [ ] Are time estimates realistic and granular?
- [ ] Are parallel tasks marked with ⚡?

## Template Integration

This skill uses the `template-renderer` skill to generate formatted plans:

**Integration Flow**:

1. plan-generator creates structured plan data (JSON)
2. Maps plan data to template tokens (see Step 6)
3. Invokes template-renderer with plan-template
4. Outputs rendered plan to `.claude/context/plans/`

**Required Tokens** (for plan-template):

- Core: `PLAN_TITLE`, `DATE`, `FRAMEWORK_VERSION`, `STATUS`
- Summary: `EXECUTIVE_SUMMARY`, `TOTAL_TASKS`, `ESTIMATED_TIME`, `STRATEGY`
- Phases: `PHASE_N_NAME`, `PHASE_N_PURPOSE`, `DEPENDENCIES`, `PARALLEL_OK`
- Verification: `VERIFICATION_COMMANDS`

See `.claude/templates/plan-template.md` for complete token list.

## Related Skills

- [`template-renderer`](../template-renderer/SKILL.md) - Renders plan-template with token replacement
- [`writing-plans`](../writing-plans/SKILL.md) - Bite-sized task plans with complete code for implementation

## Memory Protocol (MANDATORY)

**Before starting:**

```bash
cat .claude/context/memory/learnings.md
```

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: Your context may reset. If it's not in memory, it didn't happen.
