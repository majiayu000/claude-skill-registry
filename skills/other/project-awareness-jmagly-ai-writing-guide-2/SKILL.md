# project-awareness

Comprehensive project context detection and state awareness.

## Triggers

- "what project is this"
- "project context"
- "what phase are we in"
- "where are we?"
- "what's next?"
- "project status"
- "current phase"
- "who is on the team"
- "what framework is active"
- "ready to transition?"
- "what's blocking us?"
- (Auto-triggered at session start for context building)

## Purpose

This skill provides rich project context awareness including:
- Project type and technology stack detection
- AIWG framework state (installed frameworks, current phase)
- Team configuration and agent assignments
- Recent activity and artifact status
- Active work detection (branches, PRs, iterations)
- Recommendations for next actions

## Behavior

When triggered, this skill:

1. **Detects project type**:
   - Monorepo vs single project
   - Library vs application vs service
   - Web, API, CLI, mobile, etc.
   - Programming languages and frameworks

2. **Identifies AIWG state**:
   - Installed frameworks (SDLC, MMK, addons)
   - Current lifecycle phase
   - Active iteration (if applicable)
   - Deployed agents and commands

3. **Parses team configuration**:
   - Team roster from `.aiwg/team/`
   - Agent assignments
   - Role responsibilities

4. **Loads recent activity**:
   - Git log (recent commits, active branches)
   - Recent artifact changes
   - Open PRs and issues

5. **Builds context object**:
   - Structured data for other skills
   - Summary for user display
   - Recommendations for next actions

## Trigger Phrase Mappings

| Natural Language | Action |
|------------------|--------|
| "Where are we?" | Check phase status, recent activity |
| "What's next?" | Identify pending tasks, next milestone |
| "Project status" | Full status report |
| "Current phase" | Phase name + completion percentage |
| "Ready to transition?" | Gate criteria check |
| "What's blocking us?" | Risk register + blockers |
| "How long until..." | Milestone progress estimate |
| "Who owns..." | Team and agent assignments |

## Information Sources

### Primary Sources (Check First)
- `.aiwg/planning/phase-status.md` - Current phase and progress
- `.aiwg/planning/iteration-plan.md` - Current iteration tasks
- `.aiwg/gates/` - Gate criteria and validation status

### Secondary Sources
- `.aiwg/risks/risk-register.md` - Active risks and blockers
- `.aiwg/team/agent-assignments.md` - Who's working on what
- `.aiwg/requirements/` - Requirements completion status
- `.aiwg/architecture/` - Architecture baseline status

### Context Sources
- `CLAUDE.md` - Project configuration
- `.aiwg/intake/project-intake.md` - Original project scope
- Git log - Recent activity

## Context Object Structure

```json
{
  "project": {
    "name": "my-project",
    "type": "application",
    "subtype": "web-api",
    "root": "/path/to/project",
    "description": "From package.json or README"
  },

  "tech_stack": {
    "languages": ["typescript", "python"],
    "runtime": "node",
    "framework": "express",
    "package_manager": "npm",
    "database": "postgresql",
    "testing": "vitest",
    "ci_cd": "github-actions"
  },

  "aiwg": {
    "installed": true,
    "frameworks": ["sdlc-complete"],
    "addons": ["aiwg-utils", "voice-framework"],
    "phase": "elaboration",
    "iteration": 3,
    "agents_deployed": 45,
    "commands_deployed": 38
  },

  "team": {
    "members": [
      {"name": "John", "role": "tech-lead", "agent": "architecture-designer"}
    ],
    "agent_assignments": {
      "architecture-designer": "John",
      "test-architect": "Jane"
    }
  },

  "activity": {
    "current_branch": "feature/user-auth",
    "recent_commits": [...],
    "open_prs": [...],
    "modified_artifacts": [...],
    "last_gate_check": "2025-12-05"
  },

  "artifacts": {
    "total": 24,
    "by_status": {
      "draft": 5,
      "review": 3,
      "baselined": 16
    },
    "recent": [...]
  },

  "recommendations": [
    "Complete SAD review (2 reviewers pending)",
    "Run gate-check for Elaboration exit",
    "Update risk register (7 days stale)"
  ]
}
```

## Response Formats

### Quick Status (Default)

```
Phase: [Current Phase] ([X]% complete)
Iteration: [N] of [Total]
Next Milestone: [Milestone Name] - [Date/Status]
Blockers: [Count] ([List if < 3])
```

### Full Status (On Request)

```
## Project: [Name]
Phase: [Phase] | Iteration: [N]
Started: [Date] | Target: [Date]

### Completion
- Requirements: [X]%
- Architecture: [X]%
- Implementation: [X]%
- Testing: [X]%

### Active Work
- [Task 1] - [Owner] - [Status]
- [Task 2] - [Owner] - [Status]

### Blockers/Risks
- [Risk 1] - [Severity] - [Mitigation]

### Next Steps
1. [Action 1]
2. [Action 2]
```

## Detection Methods

### Project Type Detection

| Indicator | Project Type |
|-----------|-------------|
| package.json + src/index.ts | Node.js application |
| package.json + lib/ | Node.js library |
| setup.py or pyproject.toml | Python package |
| Cargo.toml | Rust project |
| go.mod | Go module |
| pom.xml | Java Maven project |
| turbo.json or lerna.json | Monorepo |

### Framework Stack Detection

| Files | Framework |
|-------|-----------|
| next.config.js | Next.js |
| angular.json | Angular |
| vite.config.ts | Vite |
| django, manage.py | Django |
| express in package.json | Express |
| fastapi in requirements | FastAPI |

### AIWG State Detection

| Location | Information |
|----------|-------------|
| .aiwg/ | AIWG artifacts directory exists |
| .aiwg/config/registry.json | Installed frameworks |
| .aiwg/planning/phase-plan-*.md | Current phase |
| .aiwg/planning/iteration-*.md | Current iteration |
| .claude/agents/ | Deployed agents |
| .claude/commands/ | Deployed commands |

### Phase Detection Heuristics

| Artifacts Present | Likely Phase |
|-------------------|--------------|
| intake/ only | Concept/Inception |
| requirements/ + architecture/ draft | Inception |
| architecture/ baselined | Elaboration |
| testing/ + deployment/ draft | Construction |
| deployment/ baselined | Transition |
| All baselined + production logs | Production |

## Phase Reference

| Phase | Description | Key Artifacts |
|-------|-------------|---------------|
| Inception | Vision, risks, feasibility | intake forms, business case |
| Elaboration | Architecture baseline | SAD, ADRs, test strategy |
| Construction | Feature implementation | code, tests, reviews |
| Transition | Deployment, handover | runbooks, training |
| Production | Operations, iteration | monitoring, incidents |

## Command Bindings

This skill may trigger these commands based on context:

| Context | Command |
|---------|---------|
| User wants full report | `/project-status` |
| User asks about health | `/project-health-check` |
| User asks about gate readiness | `/flow-gate-check [phase]` |
| User seems lost on next steps | Suggest relevant flow command |

## Usage Examples

### Session Start Context

```
Model auto-invokes project-awareness

Returns:
"Project: MyAPI (Node.js/Express API)
Phase: Elaboration (Iteration 3)
Team: 4 members assigned
Recent: SAD approved, Test Plan in review

Recommendations:
- Complete Test Plan review
- Begin Construction planning"
```

### Explicit Query

```
User: "What phase are we in?"

Skill returns:
"Current Phase: Elaboration
Milestone: Architecture Baseline (ABM)
Progress: 75% complete

Completed:
✓ Requirements baseline
✓ SAD approved
✓ 3/5 ADRs written

Remaining:
- Test Plan approval
- Risk register update
- Gate check"
```

### Team Query

```
User: "Who owns the architecture?"

Skill returns:
"Architecture ownership:
- Lead: John (architecture-designer)
- Reviewers: Jane (security-architect), Bob (test-architect)

Recent activity:
- SAD v1.2 updated 2 days ago
- ADR-005 created yesterday"
```

## CLI Usage

```bash
# Full context dump
python project_awareness.py --full

# Specific aspects
python project_awareness.py --tech-stack
python project_awareness.py --aiwg-state
python project_awareness.py --team
python project_awareness.py --activity

# JSON output
python project_awareness.py --full --json

# Recommendations only
python project_awareness.py --recommendations
```

## Integration

This skill provides context for:
- `artifact-orchestration`: Knows current phase for artifact selection
- `gate-evaluation`: Knows what gate to check
- `parallel-dispatch`: Knows which agents are relevant
- `template-engine`: Knows project name, type for templates
- All SDLC flows: Phase and iteration context
- All other skills that need project context

## Caching

Context is cached for performance:
- Tech stack: Cached until package files change
- AIWG state: Cached for 5 minutes
- Activity: Refreshed on each call
- Team: Cached until team files change

Cache location: `.aiwg/working/context-cache.json`

## References

- Team configuration: `.aiwg/team/`
- Phase plans: `.aiwg/planning/`
- Registry: `.aiwg/config/registry.json`
- Artifact index: `.aiwg/reports/artifact-index.json`
