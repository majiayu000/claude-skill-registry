---
name: edd
description: "Eval-Driven Development (EDD) Framework v2.64 - Define-before-implement pattern with structured evals. Provides workflow: Define specifications → Implement features → Verify against evals. Components: TEMPLATE.md for eval definitions, edd.sh CLI script, /edd skill invocation. Check types: CC- (Capability), BC- (Behavior), NFC- (Non-Functional). Integrates with orchestrator workflow for quality-first development. Keywords: evals, define, implement, verify, capability checks, behavior checks, non-functional checks, template, quality assurance, test-driven, specification. Use when: defining new features with structured evals, implementing with verification requirements, creating quality specifications, TDD-style workflow with evals."
---

# EDD (Eval-Driven Development) Framework v2.64

**Eval-Driven Development** is a quality-first development pattern that enforces **define-before-implement** workflow with structured evaluations.

## What is EDD?

EDD provides a systematic approach to software development with three phases:

1. **DEFINE** - Create structured eval specifications using TEMPLATE.md
2. **IMPLEMENT** - Build features according to eval definitions
3. **VERIFY** - Validate implementation against eval criteria

## Check Types

| Prefix | Type | Purpose |
|--------|------|---------|
| `CC-` | Capability Checks | Feature capabilities and functionality |
| `BC-` | Behavior Checks | Expected behaviors and responses |
| `NFC-` | Non-Functional Checks | Performance, security, maintainability |

## Usage

```bash
# Invoke EDD workflow
/edd "Define memory-search feature"

# CLI script (if available)
ralph edd define memory-search
ralph edd check memory-search
```

## Components

- **TEMPLATE.md**: Template for creating eval definitions
- **edd.sh**: CLI script for eval management
- **/edd skill**: Skill invocation from Claude Code
- **~/.claude/evals/**: Directory for eval definitions

## Template Structure

Each eval definition includes:

1. **Capability Checks** (CC-) - What the feature can do
2. **Behavior Checks** (BC-) - How the feature behaves
3. **Non-Functional Checks** (NFC-) - Performance, security, etc.
4. **Implementation Notes** - Technical guidance
5. **Verification Evidence** - Test results

## Example: memory-search.md

```markdown
# Memory Search Eval

**Status**: DRAFT
**Created**: 2026-01-30

## Capability Checks
- [ ] CC-1: Search across semantic memory
- [ ] CC-2: Support filtering by type

## Behavior Checks
- [ ] BC-1: Returns ranked results
- [ ] BC-2: Handles empty queries gracefully

## Non-Functional Checks
- [ ] NFC-1: Search completes in <2s
- [ ] NFC-2: Memory usage <100MB

## Implementation Notes
- Use parallel search for performance
- Cache frequent queries

## Verification Evidence
- Test results attached
```

## Integration with Orchestrator

EDD integrates with the orchestrator workflow to ensure quality-first development:

1. **Clarify** phase - Define evals
2. **Plan** phase - Review eval requirements
3. **Implement** phase - Build to eval specs
4. **Validate** phase - Verify against evals

---

## Swarm Mode Integration (v2.81.1)

EDD framework now supports **swarm mode** for parallel evaluation across multiple check types.

### Auto-Spawn Configuration

When invoked via `/edd`, the framework automatically spawns a specialized evaluation team:

```yaml
Task:
  subagent_type: "general-purpose"
  model: "sonnet"
  team_name: "edd-evaluation-team"
  name: "edd-coordinator"
  mode: "delegate"
  run_in_background: true
  prompt: |
    Execute Eval-Driven Development workflow for: $ARGUMENTS

    EDD Pattern:
    1. DEFINE - Create structured eval specifications
    2. DISTRIBUTE - Assign check types to specialists
    3. VERIFY - Validate against eval criteria
    4. CONSOLIDATE - Merge findings from all evaluators
```

### Team Composition

| Role | Purpose | Specialization |
|------|---------|----------------|
| **Coordinator** | EDD workflow orchestration | Manages eval lifecycle, consolidates findings |
| **Teammate 1** | Capability Checks specialist | CC- prefix: feature capabilities and functionality |
| **Teammate 2** | Behavior Checks specialist | BC- prefix: expected behaviors and responses |
| **Teammate 3** | Non-Functional Checks specialist | NFC- prefix: performance, security, maintainability |

### Swarm Mode Workflow

```
User invokes: /edd "Define memory-search feature"

1. Team "edd-evaluation-team" created
2. Coordinator (edd-coordinator) receives task
3. 3 Teammates spawned with check-type specializations
4. Eval definition distributed:
   - Teammate 1 → Capability Checks (CC-)
   - Teammate 2 → Behavior Checks (BC-)
   - Teammate 3 → Non-Functional Checks (NFC-)
5. Teammates work in parallel (background execution)
6. Coordinator monitors progress and gathers results
7. Findings consolidated into single eval specification
8. Final eval document returned
```

### Parallel Evaluation Pattern

Each teammate focuses on their check type:

```yaml
# Teammate 1: Capability Checks
CC-1: Feature can perform X
CC-2: Feature supports Y configuration
CC-3: Feature integrates with Z system

# Teammate 2: Behavior Checks
BC-1: Feature handles error case A gracefully
BC-2: Feature returns expected response for B
BC-3: Feature maintains state across C

# Teammate 3: Non-Functional Checks
NFC-1: Response time < 100ms
NFC-2: Memory usage < 50MB
NFC-3: Security vulnerability scan passes
```

### Communication Between Teammates

Teammates use the built-in mailbox system:

```yaml
# Teammate sends finding to coordinator
SendMessage:
  type: "message"
  recipient: "edd-coordinator"
  content: "CC-3 defined: Feature integrates with auth system via OAuth2"
```

### Task List Coordination

All teammates share a unified task list:

```bash
# Location: ~/.claude/tasks/edd-evaluation-team/tasks.json

# Example tasks:
[
  {"id": "1", "subject": "Define Capability Checks", "owner": "teammate-1"},
  {"id": "2", "subject": "Define Behavior Checks", "owner": "teammate-2"},
  {"id": "3", "subject": "Define Non-Functional Checks", "owner": "teammate-3"},
  {"id": "4", "subject": "Consolidate eval specification", "owner": "edd-coordinator"}
]
```

### Manual Override

To disable swarm mode:

```bash
/edd "Define feature X" --no-swarm
```

### Output Location

```bash
# Evals saved to ~/.claude/evals/
ls ~/.claude/evals/

# View last eval
cat ~/.claude/evals/latest.md
```

---

## Testing

Test suite: `tests/test_v264_edd_framework.bats` (33 tests)

Run tests:
```bash
bats tests/test_v264_edd_framework.bats
```

### Swarm Mode Tests

Additional tests for swarm mode integration:

```bash
# Test swarm team creation
tests/edd/test-swarm-team-creation.sh

# Test parallel evaluation
tests/edd/test-parallel-evaluation.sh
```

## Status

**Current**: Framework defined with swarm mode integration (v2.81.1)
**Note**: TEMPLATE.md and evals directory structure ready for use

---

**Version**: v2.64 | **Status**: DRAFT | **Tests**: 33 passing
<claude-mem-context>
# Recent Activity

<!-- This section is auto-generated by claude-mem. Edit content outside the tags. -->

*No recent activity*
</claude-mem-context>
