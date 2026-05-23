---
name: speckit-orchestrator
description: |

Triggers: specification, speckit, planning, orchestrator, orchestration
  Workflow orchestrator for Spec Driven Development. Coordinates skills and tracks progress.

  Triggers: speckit workflow, spec driven development, speckit commands
  Use when: starting any /speckit-* command or coordinating multi-phase development
category: workflow-orchestration
tags: [speckit, workflow, orchestration, planning, specification]
dependencies:
  - spec-kit:shared
  - sanctum:git-workspace-review
  - imbue:evidence-logging
  - superpowers:brainstorming
  - superpowers:writing-plans
  - superpowers:executing-plans
tools: []
modules:
  - command-skill-matrix
  - progress-tracking
progressive_loading: true
usage_patterns:
  - workflow-coordination
  - progress-tracking
  - skill-loading
complexity: intermediate
estimated_tokens: 1500
---
## Table of Contents

- [Overview](#overview)
- [Persistent Presence Lens](#persistent-presence-lens)
- [When to Use](#when-to-use)
- [Core Workflow](#core-workflow)
- [Session Initialization](#session-initialization)
- [Command-Skill Matrix](#command-skill-matrix)
- [Progress Tracking Items](#progress-tracking-items)
- [Exit Criteria](#exit-criteria)
- [Related Skills](#related-skills)


# Speckit Orchestrator

## Overview

Coordinates the Spec Driven Development workflow, skill loading, and progress tracking throughout the command lifecycle.

## Persistent Presence Lens

Treat SDD as a minimal, testable “self-modeling” loop:

- **World model**: repo + speckit artifacts (`spec.md`, `plan.md`, `tasks.md`)
- **Agent model**: loaded skills/plugins + constraints (especially `.specify/memory/constitution.md`) + progress state

This mirrors patterns from open-ended embodied agents (e.g., Voyager/MineDojo) that compound capability via a curriculum (`tasks.md`) and a skill library (reusable plugin skills + superpowers methodology skills).

## When to Use

- Starting any `/speckit-*` command.
- Coordinating multi-phase development workflows.
- Tracking progress across specification, planning, and implementation.
- Ensuring skill dependencies are loaded.

## Core Workflow

### Session Initialization

1. **Verify Repository Context**
   - Confirm working directory is a speckit-enabled project.
   - Check for `.specify/` directory structure.
   - Validate required scripts exist.

2. **Load Persistent State ("presence")**
   - Read `.specify/memory/constitution.md` for constraints/principles.
   - Load current `spec.md` / `plan.md` / `tasks.md` context if present.

3. **Load Command Dependencies**
   - Match current command to required skills.
   - Load complementary superpowers skills.

4. **Initialize Progress Tracking**
   - Create TodoWrite items for workflow phases.
   - Track completion status.

### Command-Skill Matrix

Quick reference for command-to-skill mappings:

| Command | Primary Skill | Complementary Skills |
|---------|--------------|---------------------|
| `/speckit-specify` | spec-writing | brainstorming |
| `/speckit-clarify` | spec-writing | brainstorming |
| `/speckit-plan` | task-planning | writing-plans |
| `/speckit-tasks` | task-planning | executing-plans |
| `/speckit-implement` | - | executing-plans, systematic-debugging |
| `/speckit-analyze` | - | systematic-debugging, verification |
| `/speckit-checklist` | - | verification-before-completion |

**For detailed patterns**: See `modules/command-skill-matrix.md` for complete mappings and loading rules.

### Progress Tracking Items

For each workflow session, track:
- [ ] Repository context verified.
- [ ] Prerequisites validated.
- [ ] Command-specific skills loaded.
- [ ] Artifacts created/updated.
- [ ] Verification completed.

**For detailed patterns**: See `modules/progress-tracking.md` for TodoWrite patterns and metrics.

## Exit Criteria

- Active command completed successfully.
- All required artifacts exist and are valid.
- Progress tracking reflects current state.
- No unresolved blockers.

## Related Skills

- `spec-writing`: Specification creation and refinement.
- `task-planning`: Task generation and planning.
- `superpowers:brainstorming`: Idea refinement.
- `superpowers:writing-plans`: Implementation planning.
- `superpowers:executing-plans`: Task execution.
## Troubleshooting

### Common Issues

**Command not found**
Ensure all dependencies are installed and in PATH

**Permission errors**
Check file permissions and run with appropriate privileges

**Unexpected behavior**
Enable verbose logging with `--verbose` flag
