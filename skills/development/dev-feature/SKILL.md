---
name: dev-feature
description: >-
  Execute the feature development workflow for complex, multi-session features.
  Use when starting new features, architecture changes, refactoring projects,
  or any work requiring research, design, and implementation phases.
  Invoked by: "new feature", "implement feature", "start feature development",
  "complex feature", "multi-session work".
---

# Feature Development Workflow SOP

**Version**: 1.0.0
**Last Updated**: 2026-01-11
**Status**: Active

---

## Overview

### Purpose
This workflow enables complex, multi-session feature development using AI agents with persistent documentation. It ensures continuity across sessions, tracks progress systematically, and allows any agent (or human) to pick up work exactly where the previous session left off.

### When to Use
**ALWAYS**: Multi-day features, architecture changes, projects requiring research + design + implementation phases, work spanning multiple sessions
**SKIP**: Tasks completable in a single session, simple bug fixes, minor updates

---

## Process Workflow

### Flow Diagram
```
[New Feature Request]
        |
[Phase 1: Setup] --> Create feature folder + INDEX.md
        |
[Phase 2: Research] --> Spawn Explore agent --> research/*.md
        |
[Phase 3: Design] --> design/DESIGN_##_*.md
        |
[Phase 4: Planning] --> development/EXECUTION_##_*.md
        |
[Phase 5: Execute] --> Spawn sub-agents --> Implement
        |
[Phase 6: Validate] --> TypeScript + Review + Tests
        |
[Phase 7: Handoff] --> Update SESSION_HANDOFF.md
```

### Phase Summary
| Phase | Objective | Deliverable | Duration |
|-------|-----------|-------------|----------|
| 1. Setup | Create folder structure | Feature folder with INDEX.md | 15-30 min |
| 2. Research | Understand current state | Gap analysis, research notes | 1-4 hours |
| 3. Design | Create solution designs | Design documents per component | 2-6 hours |
| 4. Planning | Break into executable tasks | Execution documents with checkboxes | 1-2 hours |
| 5. Execution | Implement via sub-agents | Working code (pending validation) | Variable |
| 6. Validation | Verify correctness | Validated code, updated docs | 15-30 min |
| 7. Handoff | Document session state | Updated SESSION_HANDOFF.md | 10-15 min |

---

## Quick Start

### Starting a New Feature

1. **Create Feature Folder**
   ```
   /docs/ignored/{feature-name}/
   ├── INDEX.md                    # Central navigation + status
   ├── SESSION_HANDOFF.md          # Session continuity
   ├── research/                   # Research and analysis
   ├── design/                     # Design documents
   └── development/                # Execution plans
   ```

2. **Create INDEX.md** using [INDEX_TEMPLATE.md](templates/INDEX_TEMPLATE.md)

3. **Create SESSION_HANDOFF.md** using [SESSION_HANDOFF_TEMPLATE.md](templates/SESSION_HANDOFF_TEMPLATE.md)

4. **Begin Research Phase** - Invoke `/design-research` skill

### Resuming a Feature

1. Read `INDEX.md` for overall project status
2. Read `SESSION_HANDOFF.md` for last session context
3. Check dependency graph for next available task
4. Read relevant DESIGN + EXECUTION docs
5. Continue execution

---

## Key Principles

1. **Index as Single Source of Truth** - INDEX.md is the authoritative reference for project status
2. **Session Handoff Continuity** - Every session ends with updated SESSION_HANDOFF.md
3. **Atomic Execution Documents** - Each execution is self-contained with clear inputs/outputs
4. **Agent Specialization** - Use Explore for research, general-purpose for implementation
5. **Documentation-Driven Progress** - Work isn't "done" until docs reflect completion

---

## Detailed Workflow

See [WORKFLOW.md](WORKFLOW.md) for complete phase-by-phase instructions including:
- Step-by-step procedures for each phase
- Agent spawning patterns
- Validation checklists
- Troubleshooting guidance

---

## Templates

| Template | Purpose | Location |
|----------|---------|----------|
| INDEX_TEMPLATE | Central navigation and status tracking | [templates/INDEX_TEMPLATE.md](templates/INDEX_TEMPLATE.md) |
| SESSION_HANDOFF_TEMPLATE | Session continuity | [templates/SESSION_HANDOFF_TEMPLATE.md](templates/SESSION_HANDOFF_TEMPLATE.md) |
| EXECUTION_TEMPLATE | Step-by-step implementation plan | [templates/EXECUTION_TEMPLATE.md](templates/EXECUTION_TEMPLATE.md) |

---

## Agent Spawn Patterns

### Research Phase (Explore Agent)
```
Use Task tool with subagent_type: "Explore"
- Codebase questions
- Finding files/patterns
- Understanding architecture
```

### Implementation Phase (General-Purpose Agent)
```
Use Task tool with subagent_type: "general-purpose"
- Creating files
- Modifying code
- Running validations
```

---

## Quick Reference

### Folder Structure
| Type | Location |
|------|----------|
| Feature Docs | `/docs/ignored/{feature}/` |
| Index | `/docs/ignored/{feature}/INDEX.md` |
| Handoff | `/docs/ignored/{feature}/SESSION_HANDOFF.md` |
| Research | `/docs/ignored/{feature}/research/` |
| Design | `/docs/ignored/{feature}/design/` |
| Execution | `/docs/ignored/{feature}/development/` |

### Validation Commands
```bash
# TypeScript check
npx tsc --noEmit

# Format and lint
task format-all

# Run tests
task test
```

### Status Indicators
| Symbol | Meaning |
|--------|---------|
| ░░░░░░░░░░ | Not started (0%) |
| █████░░░░░ | In progress (50%) |
| ██████████ | Complete (100%) |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Agent lacks context | Provide full design doc content in prompt |
| Dependency not met | Check INDEX.md dependency graph before starting |
| Lost session state | Read SESSION_HANDOFF.md to restore context |
| Stale documentation | Run documentation update agent after code changes |

---

## Related Skills

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| `/design-research` | Research and design | Phase 2-3: Research and Design |
| `/review-code` | Code review | Phase 6: Validation |
| `/test` | Testing | Phase 6: Validation |
| `/git-pr` | Create pull requests | After feature complete |

> **Note**: Skill paths (`/skill-name`) work after deployment. In the template repo, skills are in domain folders.

---

**End of SOP**
