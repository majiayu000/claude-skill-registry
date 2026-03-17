---
name: Jira Orchestration Workflow
description: This skill should be used when the user asks to "orchestrate jira", "work on issue", "complete jira ticket", "development workflow", "jira automation", "issue lifecycle", "work on story", "fix bug ticket", or needs guidance on coordinating development work through Jira with multi-agent orchestration patterns.
version: 1.0.0
---

# Jira Orchestration Workflow

Execute 6-phase protocol for coordinating Jira-based development work with multi-agent orchestration.

## When to Use

- Starting work on Jira issues (Bug, Story, Task, Epic)
- Automating development workflows
- Tracking progress and linking commits/PRs
- Coordinating multi-agent work

## The 6-Phase Protocol

**EXPLORE → PLAN → CODE → TEST → FIX → COMMIT**

Each phase must complete validation gates before proceeding.

### Phase 1: EXPLORE
- Fetch issue details, acceptance criteria, linked issues
- Analyze affected codebase areas and dependencies
- Agents: code-analyst, requirements-analyzer, dependency-mapper
- Outputs: Issue analysis, affected files, dependency map, risk assessment
- Jira: Transition to "In Progress", add analysis comment, log effort

### Phase 2: PLAN
- Design solution, break into subtasks, create task DAG
- Plan file changes, define success criteria
- Agents (by type): Bug→critical-bug-analyzer; Story→feature-architect; Task→technical-planner; Epic→epic-decomposer
- Outputs: Implementation plan, test plan, rollback strategy
- Jira: Create sub-tasks, add plan comment, update estimate

### Phase 3: CODE
- Execute DAG tasks in parallel
- Implement changes, add docs and error handling
- Agents (by tech): Frontend→frontend-developer; Backend→backend-developer; DevOps→infra-engineer
- Outputs: Code changes, configs, migration scripts
- Jira: Add progress comments, log time spent, flag blockers

### Phase 4: TEST
- Run unit/integration/E2E tests, verify acceptance criteria
- Agents: test-engineer, qa-specialist, integration-tester
- Outputs: Test results, coverage, performance metrics
- Jira: Add test results, attach reports
- Failure: Return to FIX, do NOT complete issue

### Phase 5: FIX
- Debug failures, address code review feedback
- Re-run tests until passing (max 3 iterations before escalation)
- Agents: debugger, code-reviewer, refactoring-specialist
- Loop: Return to TEST after fixes

### Phase 6: COMMIT
- Create PR with issue key, link to Jira, request review
- Format: `[ISSUE-KEY] description\n\nResolves: ISSUE-KEY`
- Agents: git-specialist, pr-creator, documentation-writer
- Jira: Add PR link, transition to "In Review"

## Agent Selection

| Issue Type | Primary | Secondary |
|-----------|---------|-----------|
| Bug | critical-bug-analyzer, debugger | root-cause-investigator, test-engineer |
| Story | feature-architect, code-architect | frontend/backend-developer |
| Task | technical-planner | technology-specific |
| Epic | epic-decomposer | split into stories first |
| Spike | research-specialist, poc-developer | domain experts |

By Technology: Frontend→react-specialist; Backend→api-specialist; DevOps→infra-engineer; Mobile→mobile-developer

By Priority: Blocker→critical-bug-analyzer + escalate; Critical→senior agents + extended thinking; High→standard selection; Medium/Low→optimize for efficiency

## Blocker Handling

**Mark blocker when:** Missing requirements, dependencies, technical limits, security concerns, breaking changes.

**Immediate:** Add "Blocked" label, create detailed comment, link blocking issue, notify stakeholders.

**Escalate when:** Persists >4 hours, beyond agent authority, security vulnerability, breaking changes, customer impact, legal/compliance questions.

**Process:** Pause, document context, create Jira comment, tag humans, transition to "Waiting for Support".

## Human Involvement

**Always required:** Security changes, breaking API/DB changes, infrastructure, customer-facing features, compliance.

**Optional (post-review):** Bug fixes, docs, tests, refactoring.

## Progress Tracking

**Update Jira at:** Phase transitions, blockers, test failures, PR creation, hourly.

**Status format:**
```
## Progress - Phase: [NAME]
- Completed: [items]
- In Progress: [items] (X%)
- Blocked: [items] ([reason])
- Next: [steps]
- Time Spent: Xh Ym
```

**Metrics:** Velocity (story points/sprint), Cycle Time (In Progress→Done), Lead Time (creation→completion), Work Log (time/phase).

## Best Practices

- Never skip phases (critical validations at each)
- Checkpoint between phases for recovery
- Run independent tasks in parallel
- Use 3-5 agents minimum, 13 maximum
- Frequent Jira updates: comments, work logs, links, labels, components
- Quality gates: All tests passing, >80% coverage, no vulnerabilities, docs updated, human review

## Workflows by Issue Type

**Bug:** EXPLORE (reproduce)→PLAN (fix design)→CODE→TEST (add regression)→FIX→COMMIT
**Story:** EXPLORE→PLAN (subtasks)→CODE (parallel)→TEST (E2E)→FIX→COMMIT
**Epic:** Decompose into Stories, execute each Story workflow, integrate results

## PR/Commit Format

**PR Title:** `[ISSUE-KEY] Brief description`

**Commit:**
```
[ISSUE-KEY] description

Changes:
- item1
- item2

Resolves: ISSUE-KEY
```

**Branch:** `[type]/[issue-key]-[description]` (e.g., feature/PROJ-123-auth)

**Smart commits:** `[ISSUE-KEY] #comment text` | `#time 2h 30m` | `#transition In Review`

## Quality Gates

- [ ] All tests passing (unit, integration, E2E)
- [ ] Coverage >80%
- [ ] No security vulnerabilities
- [ ] No breaking changes (or documented)
- [ ] Documentation updated
- [ ] PR created and linked
- [ ] Human review requested
- [ ] Acceptance criteria met

## Example: Bug Fix

**Issue:** PROJ-123 "Login timeout after 5 minutes"

| Phase | Activity | Agents |
|-------|----------|--------|
| EXPLORE | Analyze auth code, identify JWT expiry | code-analyst, security-specialist |
| PLAN | Design fix: extend expiry, fix cleanup | critical-bug-analyzer |
| CODE | Update JWT config, implement refresh | backend-developer, security-specialist |
| TEST | Unit/integration/manual tests | test-engineer, qa-specialist |
| FIX | No fixes needed | - |
| COMMIT | Create PR, link to PROJ-123 | git-specialist |

## Integration

Works with: jira (API), git-workflows (branches/PRs), orchestration-patterns (agent coordination), testing (test execution), debugging (root cause analysis).
