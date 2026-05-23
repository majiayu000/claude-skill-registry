---
name: task-planning
description: |

Triggers: dependencies, tasks, speckit, planning, implementation
  Generate phased, dependency-ordered tasks from specs. Identifies parallelization opportunities.

  Triggers: task planning, dependency ordering, phased breakdown, parallel tasks
  Use when: converting specifications to implementation tasks
  DO NOT use when: writing specifications - use spec-writing.
category: planning
tags: [speckit, tasks, planning, implementation, dependencies]
dependencies:
  - spec-kit:shared
  - superpowers:writing-plans
  - superpowers:executing-plans
tools: []
modules:
  - phase-structure.md
  - dependency-patterns.md
progressive_loading: true
usage_patterns:
  - task-generation
  - dependency-ordering
  - implementation-planning
complexity: intermediate
estimated_tokens: 1200
---

# Task Planning

## Overview

Transforms specifications and implementation plans into actionable, dependency-ordered tasks. Creates phased breakdowns that guide systematic implementation.

## When to Use

- Converting specifications to implementation tasks
- Planning feature implementation order
- Identifying parallel execution opportunities
- Breaking down complex features into phases

## Task Phases

Tasks follow a 5-phase structure from setup through polish:

- **Phase 0: Setup** - Project initialization, dependencies, configuration
- **Phase 1: Foundation** - Data models, interfaces, test infrastructure
- **Phase 2: Core Implementation** - Business logic, APIs, services
- **Phase 3: Integration** - External services, middleware, logging
- **Phase 4: Polish** - Optimization, documentation, final testing

For detailed phase definitions, selection guidelines, and anti-patterns, see `modules/phase-structure.md`.

## Task Format

Each task includes:
- **ID**: Unique identifier (TASK-001)
- **Description**: Clear action statement
- **Phase**: Which phase it belongs to
- **Dependencies**: Tasks that must complete first
- **Parallel Marker**: [P] if can run concurrently
- **Files**: Affected file paths
- **Criteria**: How to verify completion

## Dependency Rules

Dependencies define execution order and identify parallelization opportunities:

- **Sequential Tasks**: Execute in strict order when dependencies exist
- **Parallel Tasks [P]**: Can run concurrently when no conflicts exist
- **File Coordination**: Tasks affecting same files must run sequentially

For fan-out/fan-in patterns, task ID conventions, and validation rules, see `modules/dependency-patterns.md`.

## Example Task Entry

```markdown
## Phase 2: Core Implementation

### TASK-007 - Implement user authentication service [P]
**Dependencies**: TASK-003, TASK-004
**Files**: src/services/auth.ts, src/types/user.ts
**Criteria**: All auth tests pass, tokens are valid JWT
```
**Verification:** Run `pytest -v` to verify tests pass.

## Quality Checklist

- [ ] All requirements mapped to tasks
- [ ] Dependencies are explicit
- [ ] Parallel opportunities identified
- [ ] Tasks are right-sized (not too large/small)
- [ ] Each task has clear completion criteria

## Related Skills

- `spec-writing`: Creating source specifications
- `speckit-orchestrator`: Workflow coordination
## Troubleshooting

### Common Issues

**Command not found**
Ensure all dependencies are installed and in PATH

**Permission errors**
Check file permissions and run with appropriate privileges

**Unexpected behavior**
Enable verbose logging with `--verbose` flag
