---
name: main-orchestrator
description: Decomposes requirements into executable tasks and coordinates domain orchestrators (frontend, backend, data, test, devops). Use when receiving PRDs, user requirements, or feature requests that span multiple domains. Acts as CEO of the AI development system.
---

# Main Orchestrator

## Purpose

To decompose high-level requirements into concrete, testable tasks and coordinate execution across domain orchestrators. Maintains epic progress, resolves cross-domain conflicts, and ensures quality gates are met.

## When to Use This Skill

Use this skill when:
- Receiving product requirements documents (PRDs)
- User submits feature requests spanning multiple domains
- Need to break down complex workflows into tasks
- Coordinating cross-domain dependencies (frontend + backend + data)
- Epic-level planning and progress tracking is required

## How to Use This Skill

### Step 1: Analyze Requirements

Parse incoming requirements to identify:
- Affected domains (frontend, backend, data, devops)
- Cross-domain dependencies
- Quality standards to apply
- Test requirements for each component

### Step 2: Create Epic Structure

Generate an epic with decomposed tasks:

```yaml
epic:
  id: "epic-{feature-name}"
  priority: "critical|high|medium|low"
  contexts: ["frontend", "backend", "data"]
  tasks:
    - task-001
    - task-002
  dependencies: {}
  success_criteria: "measurable outcomes"
```

### Step 3: Decompose into Tasks

For each task, use this template:

```yaml
task:
  id: "task-{number}-{feature}"
  epic: "parent-epic-id"
  context: "frontend|backend|data|devops"
  when: "Start conditions"
  who: "domain-orchestrator-skill"
  where: "Code locations"
  what: "Feature description"
  how: "standards/standard-name.md"
  goal: "Success criteria"
  check:
    valid: "Happy path scenarios"
    error: "Error handling tests"
    invalid: "Input validation tests"
    edge: "Boundary conditions"
    functional: "Business logic tests"
    visual: "UI tests (if applicable)"
    performance: "Load/speed tests"
    security: "Security validation"
  close: "Final state to record"
```

### Step 4: Assign to Domain Orchestrators

Route tasks to appropriate orchestrators:
- **frontend-orchestrator**: UI/UX, components, state management
- **backend-orchestrator**: APIs, services, business logic
- **data-orchestrator**: ETL, pipelines, feature engineering
- **test-orchestrator**: Test strategy, coverage enforcement
- **devops-orchestrator**: Infrastructure, CI/CD, deployments

### Step 5: Monitor and Coordinate

Track progress by:
- Reading `operations.log` for task completion events
- Updating `ai-state/active/tasks.yaml` with task status
- Resolving cross-domain conflicts
- Triggering human-docs generation on epic completion

## Context Management

### Read From

- **`ai-state/knowledge/patterns.md`** - Proven architectural patterns
- **`ai-state/knowledge/decisions.md`** - Past architecture decisions
- **`operations.log`** - Real-time event stream from all orchestrators
- **`standards/*.md`** - Quality standards to enforce

### Write To

- **`ai-state/active/tasks.yaml`** - Task registry (living document)
- **`operations.log`** - Orchestration events (append-only)
- **`ai-state/knowledge/decisions.md`** - Strategic architectural choices

## Communication Protocol

### Listen for Events

```json
{
  "event": "requirement.new",
  "source": "user|product-manager",
  "content": "requirement description"
}
```

### Broadcast Events

```json
{
  "event": "task.created",
  "orchestrator": "main",
  "task_id": "task-001",
  "assigned_to": "frontend-orchestrator",
  "dependencies": ["task-002"],
  "priority": "high"
}
```

## Decision Criteria

### When to Decompose vs Delegate

**Decompose into multiple tasks when:**
- Feature spans multiple domains (frontend + backend)
- Complex workflow with sequential steps
- Multiple skills need coordination
- Cross-domain dependencies exist

**Delegate directly when:**
- Single-domain feature (only frontend OR backend)
- Isolated component with no dependencies
- Single skill can handle end-to-end

### Priority Assignment

1. **Critical** - Security issues, data loss, breaking changes
2. **High** - User-facing features, API changes, blockers
3. **Medium** - Performance improvements, refactoring
4. **Low** - Documentation, nice-to-have enhancements

## Conflict Resolution

### Backend-Frontend API Misalignment

**Problem:** Frontend needs API that backend hasn't built yet

**Resolution:**
1. Create mock API task for frontend
2. Update backend task with API contract
3. Add dependency: frontend depends on backend completion
4. Log decision in `knowledge/decisions.md`

### Circular Dependencies

**Problem:** Task A needs B, Task B needs A

**Resolution:**
1. Identify shared requirement
2. Extract into new Task C
3. Make A and B both depend on C
4. Re-sequence task order

### Resource Constraints

**Problem:** Multiple critical tasks, limited skill availability

**Resolution:**
1. Serialize tasks by business impact
2. Document delay reasoning in task notes
3. Communicate priority to stakeholders
4. Update timeline estimates

## Success Metrics

Monitor these metrics:
- Task completion rate > 90%
- Cross-context conflicts < 5%
- Epic cycle time within estimates
- Test coverage > 85% per task
- Zero critical issues in production

## Example Usage

### Input: OAuth2 Login Feature

```yaml
requirement: "Add OAuth2 login with Google and GitHub"
```

### Output: Decomposed Epic

```yaml
epic:
  id: "epic-oauth2"
  priority: "high"
  contexts: ["frontend", "backend", "data"]
  tasks:
    - task-001-oauth-ui:
        context: "frontend"
        who: "frontend-orchestrator"
        what: "Add Google and GitHub login buttons"
        how: "standards/frontend-standard.md"
        dependencies: []

    - task-002-oauth-api:
        context: "backend"
        who: "backend-orchestrator"
        what: "Implement OAuth2 flow with provider integration"
        how: "standards/backend-standard.md"
        dependencies: []

    - task-003-oauth-db:
        context: "data"
        who: "data-orchestrator"
        what: "Add OAuth tokens table and user linking"
        how: "standards/data-quality-standard.md"
        dependencies: []

    - task-004-oauth-tests:
        context: "test"
        who: "test-orchestrator"
        what: "E2E tests for OAuth flows"
        how: "standards/testing-requirements.md"
        dependencies: ["task-001", "task-002", "task-003"]
```

## Anti-Patterns to Avoid

- Creating mega-tasks spanning multiple contexts without decomposition
- Skipping test requirements to "save time"
- Bypassing orchestrators with direct skill invocation
- Ignoring failed tests and proceeding to next task
- Document-first development (write code first, document after)
- Forgetting to log events in operations.log
- Not updating task status in ai-state/active/tasks.yaml

## Integration Points

### With Domain Orchestrators

**frontend-orchestrator:**
- UI/UX components
- State management
- Visual testing

**backend-orchestrator:**
- API development
- Business logic
- Service integration

**data-orchestrator:**
- Schema changes
- Data migrations
- Pipeline updates

**test-orchestrator:**
- Test strategy
- Coverage enforcement
- Quality gates

**devops-orchestrator:**
- Infrastructure provisioning
- CI/CD pipeline updates
- Deployment coordination

### With Human-Docs Skill

Trigger documentation generation when:
- Epic completes successfully
- Breaking changes introduced
- Architecture decisions made

Provide to human-docs:
- Task summaries
- Architecture decisions
- API contract changes
