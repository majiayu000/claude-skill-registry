---
name: team-skill-designer
description: Design and generate unified team skills with role-based routing. All team members invoke ONE skill, SKILL.md routes to role-specific execution via --role arg. Triggers on "design team skill", "create team skill", "team skill designer".
allowed-tools: Task, AskUserQuestion, Read, Write, Bash, Glob, Grep
---

# Team Skill Designer

Meta-skill for creating unified team skills where all team members invoke ONE skill with role-based routing. Generates a complete skill package with SKILL.md as role router and `roles/` folder for per-role execution detail.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│  Team Skill Designer (this meta-skill)                          │
│  → Collect requirements → Analyze patterns → Generate skill pkg │
└───────────────┬─────────────────────────────────────────────────┘
                │
    ┌───────────┼───────────┬───────────┬───────────┐
    ↓           ↓           ↓           ↓           ↓
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│ Phase 1 │ │ Phase 2 │ │ Phase 3 │ │ Phase 4 │ │ Phase 5 │
│ Require │ │ Pattern │ │  Skill  │ │  Integ  │ │  Valid  │
│ Collect │ │ Analyze │ │  Gen    │ │  Verify │ │         │
└─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘
     ↓           ↓           ↓           ↓           ↓
  team-        patterns   SKILL.md +   report    validated
  config.json  .json      roles/*.md   .json     skill pkg
```

## Key Innovation: Unified Skill + Role Router

**Before (command approach)**:
```
.claude/commands/team/
├── coordinate.md     →  /team:coordinate
├── plan.md           →  /team:plan
├── execute.md        →  /team:execute
├── test.md           →  /team:test
└── review.md         →  /team:review
```
→ 5 separate command files, 5 separate skill paths

**After (unified skill approach)**:
```
.claude/skills/team-{name}/
├── SKILL.md          →  Skill(skill="team-{name}", args="--role=xxx")
├── roles/
│   ├── coordinator/
│   │   ├── role.md           # Orchestrator
│   │   └── commands/         # Modular command files
│   ├── planner/
│   │   ├── role.md
│   │   └── commands/
│   ├── executor/
│   │   ├── role.md
│   │   └── commands/
│   ├── tester/
│   │   ├── role.md
│   │   └── commands/
│   └── reviewer/
│       ├── role.md
│       └── commands/
└── specs/
    └── team-config.json
```
→ 1 skill entry point, --role arg routes to per-role execution

**Coordinator spawns teammates with**:
```javascript
Task({
  prompt: `...调用 Skill(skill="team-{name}", args="--role=planner") 执行规划...`
})
```

## Target Output Structure

```
.claude/skills/team-{name}/
├── SKILL.md                    # Role router + shared infrastructure
│   ├─ Frontmatter
│   ├─ Architecture Overview (role routing diagram)
│   ├─ Command Architecture (folder structure explanation)
│   ├─ Role Router (parse --role → Read roles/{role}/role.md → execute)
│   ├─ Shared Infrastructure (message bus, task lifecycle)
│   ├─ Coordinator Spawn Template
│   └─ Error Handling
├── roles/                      # Role-specific execution detail (folder-based)
│   ├── coordinator/
│   │   ├── role.md             # Orchestrator (Phase 1/5 inline, Phase 2-4 delegate)
│   │   └── commands/
│   │       ├── dispatch.md     # Task chain creation
│   │       └── monitor.md      # Progress monitoring
│   ├── {role-1}/
│   │   ├── role.md             # Worker orchestrator
│   │   └── commands/
│   │       └── *.md            # Role-specific command files
│   └── {role-2}/
│       ├── role.md
│       └── commands/
│           └── *.md
└── specs/                      # [Optional] Team-specific config
    └── team-config.json
```

## Core Design Patterns

### Pattern 1: Role Router (Unified Entry Point)

SKILL.md parses `$ARGUMENTS` to extract `--role`:
```
Input: Skill(skill="team-{name}", args="--role=planner")
  ↓ Parse --role=planner
  ↓ Read roles/planner/role.md
  ↓ Execute planner-specific 5-phase logic
```

No --role → error (role is required, set by coordinator spawn).

### Pattern 2: Shared Infrastructure in SKILL.md

SKILL.md defines ONCE, all roles inherit:
- Message bus pattern (team_msg + CLI fallback)
- Task lifecycle (TaskList → TaskGet → TaskUpdate)
- Team name and session directory conventions
- Error handling and escalation rules

### Pattern 3: Role Files = Full Execution Detail

Each `roles/{role}/role.md` contains:
- Toolbox section (available commands, subagent capabilities, CLI capabilities)
- Role-specific 5-phase implementation (Phase 1/5 inline, Phase 2-4 delegate or inline)
- Per-role message types
- Per-role task prefix
- Complete code (no `Ref:` back to SKILL.md)
- Command files in `commands/` for complex phases (subagent delegation, CLI fan-out)

### Pattern 4: Batch Role Generation

Phase 1 collects ALL roles at once (not one at a time):
- Team name + all role definitions in one pass
- Coordinator is always generated
- Worker roles collected as a batch

### Pattern 5: Self-Contained Specs

Design pattern specs are included locally in `specs/`:
```
specs/team-design-patterns.md    # Infrastructure patterns (9) + collaboration index
specs/collaboration-patterns.md  # 10 collaboration patterns with convergence control
specs/quality-standards.md       # Quality criteria (incl. command file standards)
```

---

## Mandatory Prerequisites

> **Do NOT skip**: Read these before any execution.

### Specification Documents (Required Reading)

| Document | Purpose | When |
|----------|---------|------|
| [specs/team-design-patterns.md](specs/team-design-patterns.md) | Infrastructure patterns (8) + collaboration index | **Must read** |
| [specs/collaboration-patterns.md](specs/collaboration-patterns.md) | 10 collaboration patterns with convergence control | **Must read** |
| [specs/quality-standards.md](specs/quality-standards.md) | Quality criteria | Must read before generation |

### Template Files (Must read before generation)

| Document | Purpose |
|----------|---------|
| [templates/skill-router-template.md](templates/skill-router-template.md) | Generated SKILL.md template with role router + command architecture |
| [templates/role-template.md](templates/role-template.md) | Generated role file template with Toolbox + command delegation |
| [templates/role-command-template.md](templates/role-command-template.md) | Command file template with 7 pre-built patterns |

### Existing Reference

| Document | Purpose |
|----------|---------|
| `.claude/commands/team/coordinate.md` | Coordinator spawn patterns |
| `.claude/commands/team/plan.md` | Planner role reference |
| `.claude/commands/team/execute.md` | Executor role reference |
| `.claude/commands/team/test.md` | Tester role reference |
| `.claude/commands/team/review.md` | Reviewer role reference |

---

## Execution Flow

```
Phase 0: Specification Study (MANDATORY)
   -> Read: specs/team-design-patterns.md
   -> Read: specs/collaboration-patterns.md
   -> Read: templates/skill-router-template.md + templates/role-template.md
   -> Read: 1-2 existing team commands for reference
   -> Output: Internalized requirements (in-memory)

Phase 1: Requirements Collection
   -> Ref: phases/01-requirements-collection.md
   - Collect team name and ALL role definitions (batch)
   - For each role: name, responsibility, task prefix, capabilities
   - Pipeline definition (task chain order)
   - Output: team-config.json (team-level + per-role config)

Phase 2: Pattern Analysis
   -> Ref: phases/02-pattern-analysis.md
   - Per-role: find most similar existing command
   - Per-role: select infrastructure + collaboration patterns
   - Per-role: map 5-phase structure
   - Output: pattern-analysis.json

Phase 3: Skill Package Generation
   -> Ref: phases/03-skill-generation.md
   - Generate SKILL.md (role router + command architecture + shared infrastructure)
   - Generate roles/{name}/role.md (per-role orchestrator with Toolbox)
   - Generate roles/{name}/commands/*.md (modular command files)
   - Generate specs/team-config.json
   - Output: .claude/skills/team-{name}/ complete package

Phase 4: Integration Verification
   -> Ref: phases/04-integration-verification.md
   - Verify role router references match role files
   - Verify task prefixes are unique across roles
   - Verify message type compatibility
   - Output: integration-report.json

Phase 5: Validation
   -> Ref: phases/05-validation.md
   - Structural completeness per role file
   - Pattern compliance per role file
   - Quality scoring and delivery
   - Output: validation-report.json + delivered skill package
```

**Phase Reference Documents** (read on-demand):

| Phase | Document | Purpose |
|-------|----------|---------|
| 1 | [phases/01-requirements-collection.md](phases/01-requirements-collection.md) | Batch collect team + all role definitions |
| 2 | [phases/02-pattern-analysis.md](phases/02-pattern-analysis.md) | Per-role pattern matching and phase mapping |
| 3 | [phases/03-skill-generation.md](phases/03-skill-generation.md) | Generate unified skill package |
| 4 | [phases/04-integration-verification.md](phases/04-integration-verification.md) | Verify internal consistency |
| 5 | [phases/05-validation.md](phases/05-validation.md) | Quality gate and delivery |

## Directory Setup

```javascript
const timestamp = new Date().toISOString().slice(0,19).replace(/[-:T]/g, '');
const workDir = `.workflow/.scratchpad/team-skill-${timestamp}`;

Bash(`mkdir -p "${workDir}"`);
```

## Output Structure

```
.workflow/.scratchpad/team-skill-{timestamp}/
├── team-config.json             # Phase 1 output (team + all roles)
├── pattern-analysis.json        # Phase 2 output (per-role patterns)
├── integration-report.json      # Phase 4 output
├── validation-report.json       # Phase 5 output
└── preview/                     # Phase 3 output (preview before delivery)
    ├── SKILL.md
    ├── roles/
    │   ├── coordinator/
    │   │   ├── role.md
    │   │   └── commands/
    │   │       ├── dispatch.md
    │   │       └── monitor.md
    │   └── {role-N}/
    │       ├── role.md
    │       └── commands/
    │           └── *.md
    └── specs/
        └── team-config.json

Final delivery:
.claude/skills/team-{name}/
├── SKILL.md
├── roles/
│   ├── coordinator/
│   │   ├── role.md
│   │   └── commands/
│   └── {role-N}/
│       ├── role.md
│       └── commands/
└── specs/
    └── team-config.json
```

## Comparison: Command Designer vs Skill Designer

| Aspect | team-command-designer | team-skill-designer |
|--------|----------------------|---------------------|
| Output | N separate .md command files | 1 skill package (SKILL.md + roles/) |
| Entry point | N skill paths (/team:xxx) | 1 skill path + --role arg |
| Shared infra | Duplicated in each command | Defined once in SKILL.md |
| Role isolation | Complete (separate files) | Complete (roles/ directory) |
| Coordinator spawn | `Skill(skill="team:plan")` | `Skill(skill="team-{name}", args="--role=planner")` |
| Role generation | One role at a time | All roles in batch |
| Template | command-template.md | skill-router-template.md + role-template.md |

## Error Handling

| Scenario | Resolution |
|----------|------------|
| Specs not found | Fall back to inline pattern knowledge |
| Role name conflicts | AskUserQuestion for rename |
| Task prefix conflicts | Suggest alternative prefix |
| Template variable unresolved | FAIL with specific variable name |
| Quality score < 60% | Re-run Phase 3 with additional context |

## Debugging

| Issue | Solution |
|-------|----------|
| Generated SKILL.md missing router | Check templates/skill-router-template.md |
| Role file missing message bus | Check templates/role-template.md |
| Command file not found | Check templates/role-command-template.md |
| Role folder structure wrong | Verify roles/{name}/role.md + commands/ layout |
| Integration check fails | Review phases/04-integration-verification.md |
| Quality score below threshold | Review specs/quality-standards.md |
