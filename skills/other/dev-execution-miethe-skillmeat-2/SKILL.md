---
name: dev-execution
description: "Unified execution engine for all development workflows. Progressive disclosure for phase execution, quick features, story completion, and scaffolding. Integrates with artifact-tracking and meatycapture-capture. Use when running /dev:execute-phase, /dev:quick-feature, /dev:implement-story, /dev:complete-user-story, or /dev:create-feature commands."
---

# Dev Execution Skill

Unified guidance for executing development workflows with token-efficient progressive disclosure.

## Quick Start

| Mode | When to Use | Command |
|------|-------------|---------|
| Phase | Multi-phase plans with YAML tracking | `/dev:execute-phase` |
| Quick | Simple features, single-session | `/dev:quick-feature` |
| Story | User story with existing plan | `/dev:implement-story` |
| Full Story | Complete story end-to-end | `/dev:complete-user-story` |
| Scaffold | New feature structure | `/dev:create-feature` |

## Execution Modes

Load only the mode-specific content you need:

| Mode | Guide | When to Load |
|------|-------|--------------|
| [Phase Execution](./modes/phase-execution.md) | Multi-phase YAML-driven work with batch delegation |
| [Quick Execution](./modes/quick-execution.md) | Simple single-session features (~1-3 files) |
| [Story Execution](./modes/story-execution.md) | User story implementation with plan |
| [Scaffold Execution](./modes/scaffold-execution.md) | New feature structure creation |

## Core Principles

### 1. Delegate Everything

- **Opus orchestrates; subagents execute**
- Never write implementation code directly
- Use batch delegation for parallel work
- Reference @CLAUDE.md for agent assignments

### 2. Token Efficiency

- Load only mode-specific content when needed
- Use YAML head extraction for large files
- Request-log operations via `/mc` (token-efficient)
- Read progress YAML only (~2KB), not full files (~25KB)

### 3. Quality Gates

All modes share these gates - run after each significant change:

```bash
pnpm test && pnpm typecheck && pnpm lint
```

Detailed gate requirements: [./validation/quality-gates.md]

## Agent Assignment Quick Reference

| Task Type | Agent |
|-----------|-------|
| Find files/patterns | codebase-explorer |
| Deep analysis | explore |
| React/UI components | ui-engineer-enhanced |
| TypeScript backend | backend-typescript-architect |
| Deep debugging | ultrathink-debugger |
| Validation/review | task-completion-validator |
| Most docs (90%) | documentation-writer |

For detailed assignments: [./orchestration/agent-assignments.md]

## Orchestration References

| Reference | Purpose |
|-----------|---------|
| [Batch Delegation](./orchestration/batch-delegation.md) | Parallel Task() patterns and execution |
| [Parallel Patterns](./orchestration/parallel-patterns.md) | Dependency-aware batching strategy |
| [Agent Assignments](./orchestration/agent-assignments.md) | Complete agent selection guide |

## Validation References

| Reference | Purpose |
|-----------|---------|
| [Quality Gates](./validation/quality-gates.md) | Test, lint, typecheck requirements |
| [Milestone Checks](./validation/milestone-checks.md) | Phase completion criteria |
| [Completion Criteria](./validation/completion-criteria.md) | Story/feature done definition |

## Skill Integrations

### artifact-tracking

For phase execution, use artifact-tracking skill for:

- CREATE progress files for new phases
- UPDATE task status after completion
- QUERY pending/blocked tasks
- ORCHESTRATE batch delegation
- **Plan status**: Use `manage-plan-status.py` to update implementation plan status (draft → in-progress → completed)

Integration patterns: [./integrations/artifact-tracking.md]

### meatycapture-capture

For request-log operations during any execution mode:

- **Capture new issues**: Use `mc-quick.sh` (~50 tokens vs ~200+ for JSON)
- **Update status**: `meatycapture log item update DOC ITEM --status done`
- **Add notes**: `meatycapture log note add DOC ITEM -c "text"`
- **Search logs**: `meatycapture log search "query" PROJECT`

**Quick capture script**:
```bash
mc-quick.sh bug api validation "Issue title" "What's wrong" "Expected behavior"
```

**Script location**: `.claude/skills/meatycapture-capture/scripts/mc-quick.sh`

Integration patterns: [./integrations/request-log-workflow.md]

## Common Patterns

### Start Work on Logged Item

```bash
# Mark item in-progress
meatycapture log item update DOC.md ITEM-01 --status in-progress

# Execute work via appropriate agents...

# Mark complete with note
meatycapture log item update DOC.md ITEM-01 --status done
meatycapture log note add DOC.md ITEM-01 -c "Completed in PR #123"
```

### Phase Execution with Artifact Tracking

```bash
# 1. Read progress YAML (token-efficient)
head -100 ${progress_file} | sed -n '/^---$/,/^---$/p'

# 2. Identify batch from parallelization field

# 3. Delegate batch (parallel Task() calls in single message)
Task("ui-engineer-enhanced", "TASK-1.1: ...")
Task("backend-typescript-architect", "TASK-1.2: ...")

# 4. Update artifact tracking
Task("artifact-tracker", "Update phase N: Mark TASK-1.1, TASK-1.2 complete")

# 5. Update request-log if applicable
meatycapture log item update REQ-*.md REQ-ITEM --status done
```

### Update Plan Status

```bash
# Mark implementation plan in progress
python .claude/skills/artifact-tracking/scripts/manage-plan-status.py \
  --file docs/project_plans/implementation_plans/features/feature-name-v1.md \
  --status in-progress

# Mark complete after all phases done
python .claude/skills/artifact-tracking/scripts/manage-plan-status.py \
  --file docs/project_plans/implementation_plans/features/feature-name-v1.md \
  --status completed
```

### Quick Feature Flow

```bash
# 1. Resolve input (REQ-ID, file path, or text)
# 2. codebase-explorer for pattern discovery
# 3. Create lightweight plan
# 4. Delegate to agents
# 5. Quality gates: pnpm test && pnpm typecheck && pnpm lint
# 6. Update request-log if from REQ-ID
```

## Error Recovery

When blocked on any task:

1. **Document** the blocker in progress tracker
2. **Attempt** standard recovery (see mode-specific guidance)
3. **If unrecoverable**: Stop, report to user with clear next steps
4. **Track** issue in request-log if it warrants separate tracking:
   ```bash
   MC_STATUS=blocked mc-quick.sh bug [DOMAIN] [COMPONENT] "Blocked: [title]" "[What's blocking]" "[What's needed]"
   ```

## Architecture Compliance

All implementations must follow the project's established patterns. Check `CLAUDE.md` for project-specific conventions.

### General Principles

- **Follow existing patterns**: Match conventions already in the codebase
- **Separation of concerns**: Keep layers distinct (API, business logic, data access)
- **Type safety**: Use TypeScript/Python types; avoid `any` or untyped code
- **Error handling**: Consistent error responses and proper exception handling
- **Observability**: Logging, metrics, and tracing where appropriate

### Backend Standards

- **Layered architecture**: Controllers/routers → services → repositories → data store
- **DTOs/schemas**: Separate API contracts from internal models
- **Validation**: Input validation at API boundaries
- **Pagination**: Use cursor or offset pagination for list endpoints
- **Documentation**: OpenAPI/Swagger specs for APIs

### Frontend Standards

- **Component library**: Use project's designated UI library consistently
- **State management**: Follow project's chosen pattern (React Query, Redux, etc.)
- **Error boundaries**: Graceful error handling in UI
- **Loading states**: Proper feedback during async operations
- **Accessibility**: WCAG compliance, keyboard navigation, ARIA labels
- **Responsive design**: Support required viewport sizes

### Testing Standards

- **Unit tests**: Business logic and utility functions
- **Integration tests**: API endpoints and service interactions
- **E2E tests**: Critical user flows
- **Accessibility tests**: Automated a11y checks for UI
- **Coverage**: Meet project's minimum coverage requirements

## Phase Completion Definition

A phase is **ONLY** complete when:

1. All tasks in plan completed
2. All success criteria met (verified)
3. All tests passing
4. Quality gates passed (types, lint, build)
5. Progress tracker updated to `status: completed`
6. All commits pushed

**Never mark phase complete if any criterion is unmet.**

## Output Format

Provide structured status updates:

```
Phase N Execution Update

Orchestration Status:
- Batch 1: ✅ Complete (3/3)
- Batch 2: 🔄 In Progress (1/2)
- Batch 3: ⏳ Pending

Current Work:
- ✅ TASK-2.1 → ui-engineer-enhanced
- 🔄 TASK-2.2 → backend-typescript-architect

Recent Commits:
- abc1234 feat(web): implement X component

Progress: 60% (6/10 tasks)
```

---

**Remember**: Follow @CLAUDE.md delegation rules. Orchestrate; don't implement directly. Load only the guidance you need.
