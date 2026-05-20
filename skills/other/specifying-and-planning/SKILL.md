---
name: specifying-and-planning
description: Multi-mode skill for project planning workflows -- extract requirements from specs, break into tasks, create GitHub issues, set up project boards, or generate agent team configurations. Use when planning a project, extracting requirements, breaking down tasks, creating issues from tasks, setting up GitHub projects, or generating team plans.
argument-hint: "<mode> [file-or-args]"
---

# Specifying and Planning

Multi-mode skill for the full project planning pipeline:

```text
spec -> requirements -> tasks -> issues -> team
```

## Modes

### spec-to-requirements

**Trigger**: "extract requirements", "analyze spec", references to `spec.md`

Analyze a spec file and produce structured `requirements.md`:

- **Functional Requirements**: Features, user interactions, data, integrations
- **Non-Functional Requirements**: Performance, security, usability, reliability
- **Requirement Dependencies**: Prerequisites, interdependencies, optional links

Each requirement gets clear acceptance criteria.

### requirements-to-tasks

**Trigger**: "break into tasks", "create task breakdown", references to `requirements.md`

Convert requirements into implementable `tasks.md`:

- **Task description** -- specific functionality to implement
- **Acceptance criteria** -- how to verify completion
- **Implementation approach** -- TDD, refactoring, new feature
- **Required components** -- files, modules, systems needing changes
- **Test requirements** -- what tests to write/update
- **Dependencies** -- prerequisite tasks, interdependent tasks

Focus on functional decomposition. No timeline or phases -- clean technical breakdown.

### tasks-to-issues

**Trigger**: "create issues", "convert tasks to issues", references to `tasks.md`

Create GitHub issues from task breakdown:

```bash
gh issue create --title "Clear title" --body "$(cat <<'EOF'
## Description
Task description

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Implementation Approach
Technical strategy

## Dependencies
- Requires #<issue>
EOF
)"
```

Apply labels: component (frontend, backend), type (feature, refactor), complexity (small, medium, large).

### setup-github-project

**Trigger**: "set up project", "create project board", references to `issues.md`

Create complete GitHub project infrastructure:

1. Parse issues file for labels, milestones, relationships
2. Create labels with smart color coding
3. Set up milestones with due dates
4. Create project board with custom fields
5. Generate all issues with proper labels and milestones
6. Link issue dependencies

### tasks-to-team

**Trigger**: "generate team plan", "create agent team", "parallelize work"

Design agent team configuration from tasks:

1. Read tasks for dependencies and scope
2. Identify parallel work groups (no cross-dependencies)
3. Design teammate roles with distinct file ownership
4. Define coordination strategy and phase gates
5. Write `docs/team.md` with kickoff prompt

Target 3-5 teammates, 5-6 tasks per teammate. Prefer fewer focused teammates over many scattered ones.

## General Principles

- No artificial timelines or phases (except team coordination)
- Focus on deliverables and dependencies
- Each requirement/task/issue should be independently verifiable
- Use TDD approach in task descriptions
- Cache project information in CLAUDE.md
