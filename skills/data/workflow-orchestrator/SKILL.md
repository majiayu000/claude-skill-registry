---
name: workflow-orchestrator
description: |
  Always-on workflow orchestration for Claude Code projects. Detects context
  and activates appropriate skills automatically. Chains with tdd, no-workarounds,
  dogfood-skills, doc-maintenance, and repo-hygiene based on task context.
category: development
---

# Workflow Orchestrator

Always-on context detection and skill chaining for Claude Code projects.

## How It Works

This skill runs in the background, detecting context and activating appropriate skills:

| Context Detected | Skill Activated | Action |
|-----------------|-----------------|--------|
| New project creation | project-init | Scaffold standard structure |
| Task completion | doc-maintenance | Update PLAN.md, README.md |
| Bug fix in tool | tdd + no-workarounds | TDD workflow, no manual workarounds |
| Feature completion | dogfood-skills | Run `skills scan`, install recommendations |
| Non-obvious discovery | claudeception | Extract as new skill |
| Parallel tasks needed | agent-orchestration | Coordinate agents via AGENTS.md |
| Research needed | research-to-plan | Web search, write RESEARCH.md |
| Session end | repo-hygiene | Clean test-skill-* artifacts |

## Conditional Chaining

Skills chain based on context:

### New Project Flow
```
project-init → dogfood-skills → tdd (ready)
```

### Task Completion Flow
```
task complete → doc-maintenance → repo-hygiene
```

### Bug Fix Flow
```
bug detected → tdd (RED) → tdd (GREEN) → tdd (REFACTOR) → doc-maintenance
```

### Feature Completion Flow
```
feature done → dogfood-skills → repo-hygiene → doc-maintenance
```

### Feature Development Flow
```
research-to-plan → tdd → doc-maintenance → dogfood-skills → repo-hygiene
```

### Testing Pipeline
```
tdd → suggest-tests → unit-test-workflow → property-based-testing → repo-hygiene
```

## Context Detection

The orchestrator detects context from:

1. **User commands**: "create project", "fix bug", "add feature"
2. **File changes**: New files, modified tests, config changes
3. **Git state**: Branch names, commit messages
4. **Error messages**: Test failures, build errors
5. **Conversation history**: Previous actions and outcomes

## Skill Relationships

| Skill | Triggers | Chains To |
|-------|----------|-----------|
| project-init | "create", "scaffold", "initialize" | dogfood-skills |
| doc-maintenance | Task completion | repo-hygiene |
| agent-orchestration | Parallel tasks | doc-maintenance |
| gitignore-hygiene | After commits | repo-hygiene |
| research-to-plan | Research needed | tdd |
| tdd | Bug fix, new feature | suggest-tests, doc-maintenance |
| suggest-tests | After tdd | unit-test-workflow |
| unit-test-workflow | Test generation | property-based-testing |
| property-based-testing | Serialization patterns | repo-hygiene |
| repo-hygiene | Session end, cleanup | doc-maintenance (feature flows) |

## Standard Project Structure

```
project/
├── CLAUDE.md           # Project guidance for Claude
├── README.md           # User-facing documentation
├── PLAN.md             # Remaining work tracker
├── RESEARCH.md         # Investigation notes
├── AGENTS.md           # Agent coordination
├── .gitignore          # Comprehensive patterns
└── .claude/
    └── skills/         # Project-specific skills
```

## When Skills Run

### Automatically (Context Detection)

- **project-init**: User mentions creating a project
- **doc-maintenance**: After any task marked complete
- **repo-hygiene**: End of session or before commit

### On Explicit Invocation

- `/project-init [name]`: Create new project
- `/doc-maintenance`: Update documentation
- `/agent-orchestration [task]`: Coordinate agents
- `/gitignore-hygiene`: Clean gitignore
- `/research-to-plan [topic]`: Research to plan

### Chained (Triggered by Other Skills)

- **tdd** triggers after bug fixes
- **dogfood-skills** triggers after feature completion
- **repo-hygiene** triggers as terminal skill

## Rationalizations (Do Not Skip)

| Rationalization | Why It's Wrong | Required Action |
|-----------------|----------------|-----------------|
| "I'll update docs later" | Later never comes | doc-maintenance now |
| "Small change, no docs" | Small changes accumulate | Update PLAN.md |
| "Agents are overkill" | Parallel work saves time | Consider orchestration |
| "Gitignore is fine" | Hidden files get committed | Run hygiene check |
| "I know the research" | Knowledge cutoff may be stale | Web search for 2026 |
| "Skip the tests" | Bugs escape | TDD required |
| "Skip cleanup" | Slop accumulates | repo-hygiene at end |

## Integration

This orchestrator connects all workflow skills:

- **project-init**: Scaffolds new projects
- **doc-maintenance**: Updates documentation
- **agent-orchestration**: Coordinates parallel work
- **gitignore-hygiene**: Maintains gitignore
- **research-to-plan**: Converts research to plans
- **tdd**: Test-driven development
- **no-workarounds**: Prevents manual workarounds
- **dogfood-skills**: Enforces dogfooding
- **repo-hygiene**: Final cleanup

## References

For detailed guidance, see:
- [file-structure.md](references/file-structure.md) - Standard project layouts
