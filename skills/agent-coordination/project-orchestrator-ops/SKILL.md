---
name: project-orchestrator-ops
description: Project management and multi-agent orchestration for autonomous software development. Use when coordinating development teams, breaking down requirements into tasks, tracking progress across agents, managing scope and timelines, or running end-to-end project builds. Triggers on queries like "build me a website", "create an app", "manage this project", "coordinate the team", "what's the project status", or any request requiring multi-agent coordination.
---

# Project Orchestrator Operations

Coordinate autonomous software development across specialized agents without human intervention.

## Core Workflow

### 1. Intake & Scoping

On new project request:
1. Parse requirements into: features, tech stack, integrations, constraints
2. Identify ambiguities → resolve from context or flag for user (batch questions)
3. Create project brief with: objectives, success criteria, deliverables, timeline estimate

### 2. Task Decomposition

Break project into agent-assignable tasks:

```
PROJECT
├── Phase 1: Foundation
│   ├── [backend-dev] Database schema design
│   ├── [backend-dev] API scaffolding
│   ├── [frontend-dev] Project setup & routing
│   └── [supabase-admin] Database provisioning
├── Phase 2: Core Features
│   ├── [backend-dev] Auth implementation
│   ├── [frontend-dev] Auth UI
│   ├── [frontend-dev] Core screens
│   └── [backend-dev] Business logic APIs
├── Phase 3: Integration
│   ├── [frontend-dev] API integration
│   ├── [api-admin] External service setup
│   └── [testing-ops] Integration tests
├── Phase 4: Polish
│   ├── [frontend-dev] UI refinement
│   ├── [docs-admin] Documentation
│   └── [codebase-admin] Cleanup audit
└── Phase 5: Deploy
    ├── [github-admin] CI/CD setup
    ├── [deployment-ops] Production deployment
    └── [monitoring-ops] Health monitoring
```

### 3. Agent Assignment Matrix

| Task Type | Primary Agent | Backup |
|-----------|--------------|--------|
| Database/Schema | supabase-admin | backend-dev |
| API Routes | backend-dev | - |
| Business Logic | backend-dev | - |
| UI Components | frontend-dev | - |
| Styling | frontend-dev | - |
| Auth | backend-dev + frontend-dev | - |
| External APIs | api-admin | backend-dev |
| CI/CD | github-admin | deployment-ops |
| Deployment | deployment-ops | github-admin |
| Testing | testing-ops | - |
| Documentation | docs-admin | - |
| Cleanup | codebase-admin | - |

### 4. Execution Protocol

For each phase:
1. Dispatch tasks to agents with: context, inputs, expected outputs, dependencies
2. Monitor completion (check file system for deliverables)
3. Validate outputs meet acceptance criteria
4. Resolve blockers or escalate
5. Proceed to next phase when all tasks complete

### 5. Handoff Format

When dispatching to agent:
```markdown
## Task Assignment

**Agent:** [agent-name]
**Project:** [project-name]
**Phase:** [N] of [total]

### Objective
[Clear statement of what to build]

### Inputs
- [Files, schemas, specs available]

### Expected Outputs
- [Specific deliverables with paths]

### Acceptance Criteria
- [ ] [Testable criterion 1]
- [ ] [Testable criterion 2]

### Dependencies
- Requires: [prior task outputs]
- Blocks: [subsequent tasks]

### Context
[Relevant project decisions, constraints, patterns to follow]
```

### 6. Progress Tracking

Maintain status in project directory:
```
project/
├── .orchestrator/
│   ├── PROJECT_BRIEF.md
│   ├── TASK_BREAKDOWN.md
│   ├── STATUS.md          # Current state
│   ├── DECISIONS.md       # Key decisions made
│   └── BLOCKERS.md        # Issues requiring resolution
```

Status format:
```markdown
## Project Status

**Phase:** 2 of 5 (Core Features)
**Progress:** 60%
**Blockers:** None

### Completed
- [x] Database schema (supabase-admin)
- [x] API scaffolding (backend-dev)
- [x] Project setup (frontend-dev)

### In Progress
- [ ] Auth implementation (backend-dev) - 80%
- [ ] Core screens (frontend-dev) - 50%

### Pending
- [ ] API integration
- [ ] External services
```

## Decision Authority

### Autonomous Decisions (No escalation)
- Tech stack choices within project constraints
- File/folder organization
- Code patterns and conventions
- Library selection for common needs
- Error handling approaches

### Escalate to User
- Scope changes beyond original requirements
- External service costs or commitments
- Ambiguous business logic
- Security-sensitive decisions
- Timeline extensions >20%

## Quality Gates

Before phase transition:
- [ ] All tasks marked complete
- [ ] Deliverables exist at expected paths
- [ ] Build passes without errors
- [ ] Tests pass (if applicable)
- [ ] No critical TODOs remaining

Before final delivery:
- [ ] All phases complete
- [ ] Documentation complete (docs-admin)
- [ ] Codebase audit passed (codebase-admin)
- [ ] Deployment successful (deployment-ops)
- [ ] Health check passing (monitoring-ops)

## Blocker Resolution

1. **Missing dependency** → Check if prior task complete, re-run if needed
2. **Ambiguous requirement** → Infer from context, document decision
3. **Technical constraint** → Adjust approach, document trade-off
4. **Agent failure** → Retry with more context, escalate if repeated
5. **External service issue** → Use mock/stub, flag for later resolution

## Project Templates

### Web Application
Phases: Setup → Auth → Core → Polish → Deploy
Agents: frontend-dev, backend-dev, supabase-admin, github-admin, deployment-ops

### Mobile Application  
Phases: Setup → Auth → Screens → API → Deploy
Agents: frontend-dev (React Native), backend-dev, supabase-admin, deployment-ops

### API/Backend Service
Phases: Schema → Routes → Logic → Tests → Deploy
Agents: backend-dev, supabase-admin, testing-ops, deployment-ops

### Marketing Site
Phases: Design → Build → Content → Deploy
Agents: frontend-dev, docs-admin, deployment-ops
