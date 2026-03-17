---
name: team-command-designer
description: Design and generate team command .md files following established patterns (8 infrastructure patterns + 10 collaboration patterns with convergence control). Triggers on "design team command", "create team role", "new teammate".
allowed-tools: Task, AskUserQuestion, Read, Write, Bash, Glob, Grep
---

# Team Command Designer

Design and generate team command .md files following established patterns extracted from existing team commands (coordinate, plan, execute, test, review). Supports 10 collaboration patterns for diverse team interaction models.

## Architecture Overview

```
Phase 0: Specification Study (Mandatory - read design patterns + collaboration patterns)
         |
Phase 1: Requirements Collection    -> role-config.json
         |
Phase 2: Pattern Analysis           -> applicable-patterns.json (infra + collaboration)
         |
Phase 3: Command Generation         -> {team-name}/{role-name}.md
         |
Phase 4: Integration Verification   -> integration-report.json
         |
Phase 5: Validation                 -> validation-report.json
```

## Key Design Principles

1. **Pattern Compliance**: All generated commands must follow infrastructure + collaboration patterns
2. **Message Bus Integration**: Every command must include team_msg logging
3. **Task Lifecycle**: Standard TaskList -> TaskGet -> TaskUpdate flow
4. **Complexity-Adaptive**: Support direct execution and sub-agent delegation
5. **Five-Phase Execution**: Each command follows the 5-phase structure
6. **Convergence Control**: Every collaboration pattern has explicit convergence criteria
7. **Feedback Loops**: Every pattern has structured feedback mechanisms
8. **Composable Patterns**: Collaboration patterns can be combined for complex workflows

---

## Mandatory Prerequisites

> **Do NOT skip**: Before performing any operations, you **must** completely read the following documents.

### Specification Documents (Required Reading)

| Document | Purpose | When |
|----------|---------|------|
| [specs/team-design-patterns.md](specs/team-design-patterns.md) | Infrastructure patterns (8) + collaboration pattern index | **Must read before execution** |
| [specs/collaboration-patterns.md](specs/collaboration-patterns.md) | 10 collaboration patterns with convergence/feedback control | **Must read before execution** |
| [specs/quality-standards.md](specs/quality-standards.md) | Quality standards for generated team commands | Must read before generation |

### Template Files (Must read before generation)

| Document | Purpose |
|----------|---------|
| [templates/command-template.md](templates/command-template.md) | Team command .md file template with all required sections |

### Existing Team Commands (Reference)

| Document | Purpose |
|----------|---------|
| `.claude/commands/team/coordinate.md` | Coordinator pattern - orchestration, team lifecycle |
| `.claude/commands/team/plan.md` | Planner pattern - exploration, plan generation |
| `.claude/commands/team/execute.md` | Executor pattern - implementation, self-validation |
| `.claude/commands/team/test.md` | Tester pattern - adaptive test-fix cycle |
| `.claude/commands/team/review.md` | Reviewer pattern - multi-dimensional review |
| `.claude/commands/team/spec/` | Spec team folder - folder-based team example |

---

## Execution Flow

```
Input Parsing:
   Parse $ARGUMENTS for role name and capabilities description

Phase 0: Specification Study (MANDATORY)
   -> Refer to: specs/team-design-patterns.md, specs/collaboration-patterns.md, templates/command-template.md
   - Read infrastructure patterns (Section A of team-design-patterns.md)
   - Read collaboration patterns specification (collaboration-patterns.md)
   - Read command template
   - Read 1-2 existing team commands most similar to the new role
   - Output: Internalized requirements (in-memory)

Phase 1: Requirements Collection
   -> Refer to: phases/01-requirements-collection.md
   - Collect team name (folder name) and role name
   - Collect responsibilities, communication patterns
   - Determine task prefix (e.g., PLAN-*, IMPL-*, ANALYZE-*)
   - Select applicable tools and capabilities
   - Output: role-config.json (includes team_name, skill_path, output_folder)

Phase 2: Pattern Analysis
   -> Refer to: phases/02-pattern-analysis.md, specs/team-design-patterns.md
   - Identify which existing command is most similar
   - Select applicable design patterns
   - Determine message types needed
   - Map phase structure to role responsibilities
   - Output: applicable-patterns.json

Phase 3: Command Generation
   -> Refer to: phases/03-command-generation.md, templates/command-template.md
   - Apply template with role-specific content
   - Generate YAML front matter
   - Generate message bus section
   - Generate 5-phase execution process
   - Generate implementation code
   - Generate error handling table
   - Output: {team-name}/{role-name}.md

Phase 4: Integration Verification
   -> Refer to: phases/04-integration-verification.md
   - Verify consistency with coordinate.md spawn patterns
   - Check message type compatibility
   - Verify task prefix uniqueness
   - Ensure allowed-tools are sufficient
   - Output: integration-report.json

Phase 5: Validation
   -> Refer to: phases/05-validation.md, specs/quality-standards.md
   - Check all required sections exist
   - Verify message bus compliance
   - Validate task lifecycle pattern
   - Score against quality standards
   - Output: validation-report.json + final {team-name}/{role-name}.md
```

## Directory Setup

```javascript
const timestamp = new Date().toISOString().slice(0,19).replace(/[-:T]/g, '');
const workDir = `.workflow/.scratchpad/team-cmd-${timestamp}`;

Bash(`mkdir -p "${workDir}"`);
```

## Output Structure

```
.workflow/.scratchpad/team-cmd-{timestamp}/
├── role-config.json              # Phase 1 output (includes team_name)
├── applicable-patterns.json      # Phase 2 output
├── integration-report.json       # Phase 4 output
├── validation-report.json        # Phase 5 output
└── {role-name}.md                # Final generated command

Final delivery (folder-based):
.claude/commands/team/{team-name}/
├── {role-name}.md                # e.g., coordinator.md, analyst.md
├── ...                           # Other roles in same team
└── (each team = one folder)

Skill path mapping:
  .claude/commands/team/{team-name}/{role-name}.md  →  /team:{team-name}:{role-name}
  Example: .claude/commands/team/spec/analyst.md    →  /team:spec:analyst
```

---

## Reference Documents by Phase

### Phase 0: Specification Study

| Document | Purpose | When to Use |
|----------|---------|-------------|
| [specs/team-design-patterns.md](specs/team-design-patterns.md) | Team command design patterns | Understand all required patterns **Required Reading** |
| [templates/command-template.md](templates/command-template.md) | Command file template | Understand output structure **Required Reading** |

### Phase 1: Requirements Collection

| Document | Purpose | When to Use |
|----------|---------|-------------|
| [phases/01-requirements-collection.md](phases/01-requirements-collection.md) | Collection process guide | Execute requirements gathering |
| [specs/team-design-patterns.md](specs/team-design-patterns.md) | Pattern reference | Validate role fits team architecture |

### Phase 2: Pattern Analysis

| Document | Purpose | When to Use |
|----------|---------|-------------|
| [phases/02-pattern-analysis.md](phases/02-pattern-analysis.md) | Analysis process guide | Execute pattern matching |
| [specs/team-design-patterns.md](specs/team-design-patterns.md) | Full pattern catalog | Select applicable patterns |

### Phase 3: Command Generation

| Document | Purpose | When to Use |
|----------|---------|-------------|
| [phases/03-command-generation.md](phases/03-command-generation.md) | Generation process guide | Execute command file generation |
| [templates/command-template.md](templates/command-template.md) | Command template | Apply template with role content |

### Phase 4: Integration Verification

| Document | Purpose | When to Use |
|----------|---------|-------------|
| [phases/04-integration-verification.md](phases/04-integration-verification.md) | Verification process guide | Execute integration checks |

### Phase 5: Validation

| Document | Purpose | When to Use |
|----------|---------|-------------|
| [phases/05-validation.md](phases/05-validation.md) | Validation process guide | Execute quality checks |
| [specs/quality-standards.md](specs/quality-standards.md) | Quality criteria | Score generated command |

### Debugging & Troubleshooting

| Issue | Solution Document |
|-------|------------------|
| Generated command missing message bus | [specs/team-design-patterns.md](specs/team-design-patterns.md) - Pattern 1 |
| Task lifecycle not standard | [specs/team-design-patterns.md](specs/team-design-patterns.md) - Pattern 3 |
| Integration check fails | [phases/04-integration-verification.md](phases/04-integration-verification.md) |
| Quality score below threshold | [specs/quality-standards.md](specs/quality-standards.md) |

### Reference & Background

| Document | Purpose | Notes |
|----------|---------|-------|
| `.claude/commands/team/coordinate.md` | Coordinator reference | Spawn patterns, task chain creation |
| `.claude/commands/team/plan.md` | Planner reference | Exploration, plan generation patterns |
| `.claude/commands/team/execute.md` | Executor reference | Implementation, delegation patterns |
| `.claude/commands/team/test.md` | Tester reference | Adaptive fix cycle pattern |
| `.claude/commands/team/review.md` | Reviewer reference | Multi-dimensional review pattern |
