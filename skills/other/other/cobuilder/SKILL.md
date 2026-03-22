---
name: cobuilder
description: This skill should be used when the user asks to "brainstorm a feature", "create a PRD", "write a solution design", "plan a new initiative", "start a new project", "ideate on a feature", "brainstorm and build", "go from idea to implementation", "generate a TDD pipeline", or when System 3/Guardian needs to drive the complete ideation → PRD → SD → worktree → autonomous TDD pipeline. Parent skill for CoBuilder orchestration-level workflows. For worker-level powers (TDD, debugging, verification), see the separate worker-superpowers skill.
version: 1.0.0
title: "CoBuilder Orchestration Workflows"
status: active
type: skill
last_verified: 2026-03-21
grade: authoritative
---

# CoBuilder Orchestration Workflows

High-level workflows for the CoBuilder multi-agent pipeline, inspired by [superpowers](https://github.com/obra/superpowers). These sub-skills are used by System 3, Guardian, and Orchestrators — not by workers directly.

**For worker-level powers** (TDD, debugging, verification, brainstorming), see `Skill("worker-superpowers")`.

---

## Sub-Skills

| Sub-Skill | Invoke As | Purpose |
|-----------|-----------|---------|
| **ideation-to-execution** | `Skill("cobuilder:ideation-to-execution")` | Brainstorm → PRD → SD → Worktree → TDD Pilot |
| **tdd-pipeline** | `Skill("cobuilder:tdd-pipeline")` | Generate and configure TDD pipeline DOT files |

---

## Quick Start

### Full Initiative (System 3 / Guardian)

```
Skill("cobuilder:ideation-to-execution")  # 5-phase workflow: brainstorm → PRD → SD → worktree → pilot
```

### Generate Pipeline Only

```
Skill("cobuilder:tdd-pipeline")           # Instantiate tdd-validated template from SD
```

### Brief Workers on Powers

When creating worker task assignments, include:
```
"Load Skill('worker-superpowers') for TDD workflow, systematic debugging, and verification."
```

---

## Core Principles

1. **Never jump to code** — Discover → Design → Plan → Execute
2. **Test first** — Every feature starts with a failing test (via worker-superpowers)
3. **Blind acceptance tests** — Write tests from PRD before any implementation
4. **Isolated execution** — Workers run in worktrees with scoped file access
5. **Pipeline-driven** — DOT graph defines execution order, not ad-hoc delegation
