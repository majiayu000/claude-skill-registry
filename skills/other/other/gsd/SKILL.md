---
name: gsd
description: Get Shit Done (GSD) - A comprehensive project management system for solo developers using Claude agents
version: 1.0.0
author: GSD Project
tags: [project-management, agents, workflows, planning, execution]
triggers: [new project, plan phase, execute phase, map codebase, debug, verify]
tools: [Read, Write, Edit, Bash, Glob, Grep, Task, AskUserQuestion]
---

# Get Shit Done (GSD) - Project Management System

A comprehensive project management system designed for solo developers working with Claude AI agents. GSD provides structured workflows for project initialization, planning, execution, verification, and debugging.

## Overview

GSD is a modular agent-based system that transforms project ideas into shipped software through:

1. **Deep questioning** - Extract user vision and requirements
2. **Domain research** - Discover standard stacks and patterns
3. **Roadmap creation** - Break requirements into phases
4. **Phase planning** - Create executable plans with verification
5. **Execution** - Implement plans with atomic commits
6. **Verification** - Ensure goals are achieved, not just tasks done
7. **Debugging** - Systematic investigation of issues

## Core Philosophy

- **Solo Developer + Claude Workflow** - No teams, no stakeholders, no ceremonies
- **Plans are Prompts** - PLAN.md files ARE the execution prompts, not documents
- **Goal-Backward Planning** - Start from what must be TRUE, derive what to build
- **Atomic Commits** - Each task commits independently for clean history
- **Quality Over Speed** - Stop before context degrades (~50% usage)
- **Ship Fast** - Plan → Execute → Ship → Learn → Repeat

## When to Use GSD

Use GSD when you need to:
- Initialize a new software project
- Plan and execute development phases
- Map an existing codebase
- Debug issues systematically
- Verify phase completion
- Track project progress and state

## Quick Start Commands

### New Project
```bash
/gsd:new-project
```
Initializes a new project with questioning → research → requirements → roadmap flow.

### Plan a Phase
```bash
/gsd:plan-phase [phase-number]
```
Creates detailed execution plans with research and verification.

### Execute a Phase
```bash
/gsd:execute-phase [phase-number]
```
Executes all plans in a phase with parallel execution support.

### Map Codebase
```bash
/gsd:map-codebase [optional-focus-area]
```
Analyzes existing codebase with parallel mapper agents.

### Debug Issues
```bash
/gsd:debug [issue-description]
```
Systematic debugging using scientific method and hypothesis testing.

### Verify Phase
```bash
/gsd:verify-work [phase-number]
```
Goal-backward verification of phase completion.

### Check Progress
```bash
/gsd:progress
```
Shows current project position, completed phases, and next steps.

## Agent Skills

GSD includes specialized agents for different tasks:

- **gsd-codebase-mapper** - Explores and documents codebase structure
- **gsd-planner** - Creates executable phase plans
- **gsd-executor** - Executes plans with atomic commits
- **gsd-debugger** - Investigates bugs systematically
- **gsd-verifier** - Verifies goal achievement
- **gsd-research-synthesizer** - Synthesizes research outputs
- **gsd-roadmapper** - Creates project roadmaps
- **gsd-phase-researcher** - Researches phase implementation
- **gsd-project-researcher** - Researches domain ecosystem
- **gsd-integration-checker** - Verifies integrations work
- **gsd-plan-checker** - Validates plan quality

## Command Skills

GSD provides commands for orchestrating the entire project lifecycle:

- **gsd:new-project** - Initialize new project
- **gsd:map-codebase** - Map existing codebase
- **gsd:plan-phase** - Plan a phase
- **gsd:execute-phase** - Execute a phase
- **gsd:verify-work** - Verify phase completion
- **gsd:debug** - Debug issues
- **gsd:discuss-phase** - Gather phase context
- **gsd:research-phase** - Research phase implementation
- **gsd:complete-milestone** - Complete milestone
- **gsd:audit-milestone** - Audit milestone
- **gsd:add-phase** - Add new phase
- **gsd:insert-phase** - Insert phase
- **gsd:remove-phase** - Remove phase
- **gsd:add-todo** - Add todo item
- **gsd:check-todos** - Check todos
- **gsd:plan-milestone-gaps** - Plan milestone gaps
- **gsd:pause-work** - Pause work
- **gsd:resume-work** - Resume work
- **gsd:update** - Update project state
- **gsd:whats-new** - Show what's new

## Workflow Skills

Detailed workflow definitions for complex operations:

- **discovery-phase** - Phase discovery workflow
- **execute-phase** - Phase execution workflow
- **diagnose-issues** - Parallel UAT diagnosis
- **map-codebase** - Codebase mapping workflow
- **discuss-phase** - Phase discussion workflow
- **verify-phase** - Phase verification workflow
- **verify-work** - Work verification workflow
- **transition** - Phase transition workflow
- **resume-project** - Project resumption workflow

## Reference Skills

Reference documents for best practices and guidelines:

- **questioning** - Deep questioning techniques
- **tdd** - Test-driven development patterns
- **ui-brand** - UI/UX guidelines
- **verification-patterns** - Verification methodologies
- **git-integration** - Git workflow patterns
- **checkpoints** - Checkpoint handling
- **continuation-format** - Continuation format specification

## Project Structure

GSD creates a `.planning/` directory with:

```
.planning/
├── PROJECT.md           # Project context and vision
├── config.json          # Workflow preferences
├── REQUIREMENTS.md      # Scoped requirements
├── ROADMAP.md          # Phase structure
├── STATE.md            # Project memory and state
├── research/            # Domain research outputs
├── phases/              # Phase-specific artifacts
│   ├── XX-name/
│   │   ├── XX-PLAN.md
│   │   ├── XX-SUMMARY.md
│   │   ├── XX-CONTEXT.md
│   │   ├── XX-RESEARCH.md
│   │   ├── XX-VERIFICATION.md
│   │   └── XX-UAT.md
└── codebase/            # Codebase analysis
    ├── STACK.md
    ├── ARCHITECTURE.md
    ├── STRUCTURE.md
    ├── CONVENTIONS.md
    ├── TESTING.md
    ├── INTEGRATIONS.md
    └── CONCERNS.md
```

## Key Concepts

### Goal-Backward Planning

Instead of asking "what should we build?", ask "what must be TRUE for the goal to be achieved?"

**Forward:** "Build authentication system" → task list
**Goal-Backward:** "Users can securely access accounts" → derive what must exist

### Atomic Commits

Each task commits independently with descriptive messages:

```bash
feat(01-01): implement user login
fix(01-02): fix password validation
test(01-03): add login tests
```

### Context Budgeting

Plans complete within ~50% context usage to maintain quality:
- 0-30%: PEAK quality
- 30-50%: GOOD quality
- 50-70%: DEGRADING quality
- 70%+: POOR quality (avoid)

### Wave-Based Execution

Plans are grouped into waves for parallel execution:
- **Wave 1:** Independent plans (no dependencies)
- **Wave 2:** Plans depending only on Wave 1
- **Wave 3:** Plans depending on Wave 2, etc.

## Anti-Patterns to Avoid

- **Enterprise PM Theater** - No RACI matrices, sprint ceremonies, stakeholder management
- **Horizontal Layers** - Don't group by "all models, then all APIs" - group by features
- **Vague Success Criteria** - "Authentication works" → "User can log in with email/password"
- **Time Estimates** - Never estimate in hours/days/weeks
- **Task Completion ≠ Goal Achievement** - Verify outcomes, not just task completion

## Getting Help

Each agent, command, and workflow has its own SKILL.md with detailed instructions. Use:

- `@skills/gsd/agents/` for agent-specific help
- `@skills/gsd/commands/` for command-specific help
- `@skills/gsd/workflows/` for workflow-specific help
- `@skills/gsd/references/` for reference documentation

## Version

GSD Version: 1.0.0
Last Updated: 2026-01-19
