---
name: complexity-assessment
description: 'AI-based complexity assessment for task analysis. Use when determining the appropriate workflow, phases, and validation depth for a task.'
version: 1.0.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Glob, Grep]
best_practices:
  - Be conservative - when in doubt, go higher complexity
  - Flag research needs for unfamiliar technologies
  - Consider hidden complexity in optional features
error_handling: graceful
streaming: supported
source: auto-claude
---

# Complexity Assessment Skill

## Overview

Analyze a task description and determine its true complexity to ensure the right workflow and validation depth are selected. Accuracy over speed - wrong complexity means wrong workflow means failed implementation.

**Core principle:** Accuracy over speed. Wrong complexity = wrong workflow = failed implementation.

## When to Use

**Always:**

- Before planning any new task
- When requirements are gathered but approach unclear
- When determining validation depth for QA

**Exceptions:**

- Obvious simple fixes (typos, color changes)
- Tasks where complexity is explicitly specified

## The Iron Law

```
NO PLANNING WITHOUT COMPLEXITY ASSESSMENT FOR NEW TASKS
```

New tasks must be assessed before selecting a workflow approach.

## Workflow Types

Determine the type of work being requested:

### FEATURE

- Adding new functionality to the codebase
- Enhancing existing features with new capabilities
- Building new UI components, API endpoints, or services
- Examples: "Add screenshot paste", "Build user dashboard", "Create new API endpoint"

### REFACTOR

- Replacing existing functionality with a new implementation
- Migrating from one system/pattern to another
- Reorganizing code structure while preserving behavior
- Examples: "Migrate auth from sessions to JWT", "Refactor cache layer"

### INVESTIGATION

- Debugging unknown issues
- Root cause analysis for bugs
- Performance investigations
- Examples: "Find why page loads slowly", "Debug intermittent crash"

### MIGRATION

- Data migrations between systems
- Database schema changes with data transformation
- Import/export operations
- Examples: "Migrate user data to new schema", "Import legacy records"

### SIMPLE

- Very small, well-defined changes
- Single file modifications
- No architectural decisions needed
- Examples: "Fix typo", "Update button color", "Change error message"

## Complexity Tiers

### SIMPLE

- 1-2 files modified
- Single service/area
- No external integrations
- No infrastructure changes
- No new dependencies
- Examples: typo fixes, color changes, text updates, simple bug fixes

### STANDARD

- 3-10 files modified
- 1-2 services/areas
- 0-1 external integrations (well-documented, simple to use)
- Minimal infrastructure changes (e.g., adding an env var)
- May need some research but core patterns exist
- Examples: adding a new API endpoint, creating a new component

### COMPLEX

- 10+ files OR cross-cutting changes
- Multiple services/areas
- 2+ external integrations
- Infrastructure changes (Docker, databases, queues)
- New architectural patterns
- Greenfield features requiring research
- Examples: new integrations (Stripe, Auth0), database migrations, new services

## Workflow

### Phase 1: Load Requirements

Read the requirements document:

```bash
# Read the requirements file
cat .claude/context/requirements/[task-name].md
```

Extract:

- **task_description**: What needs to be built
- **workflow_type**: Type of work (feature, refactor, etc.)
- **scope**: Which areas are affected
- **requirements**: Specific requirements
- **acceptance_criteria**: How success is measured
- **constraints**: Any limitations

### Phase 2: Analyze the Task

Read the task description carefully. Look for:

**Complexity Indicators (suggest higher complexity):**

- "integrate", "integration" - external dependency
- "optional", "configurable", "toggle" - feature flags, conditional logic
- "docker", "compose", "container" - infrastructure
- Database names (postgres, redis, mongo) - infrastructure + config
- API/SDK names (stripe, auth0, openai) - external research needed
- "migrate", "migration" - data/schema changes
- "across", "all services", "everywhere" - cross-cutting
- "new service" - significant scope
- ".env", "environment", "config" - configuration complexity

**Simplicity Indicators (suggest lower complexity):**

- "fix", "typo", "update", "change" - modification
- "single file", "one component" - limited scope
- "style", "color", "text", "label" - UI tweaks
- Specific file paths mentioned - known scope

### Phase 3: Assess Dimensions

#### Scope Analysis

- How many files will likely be touched?
- How many areas are involved?
- Is this a localized change or cross-cutting?

#### Integration Analysis

- Does this involve external services/APIs?
- Are there new dependencies to add?
- Do these dependencies require research?

#### Infrastructure Analysis

- Does this require Docker/container changes?
- Does this require database schema changes?
- Does this require new environment configuration?

#### Knowledge Analysis

- Does the codebase already have patterns for this?
- Will research be needed for external docs?
- Are there unfamiliar technologies involved?

#### Risk Analysis

- What could go wrong?
- Are there security considerations?
- Could this break existing functionality?

### Phase 4: Determine Phases Needed

Based on your analysis, determine which phases are needed:

**For SIMPLE tasks:**

```
discovery → quick_spec → validation
```

(3 phases, no research, minimal planning)

**For STANDARD tasks:**

```
discovery → requirements → context → spec_writing → planning → validation
```

(6 phases, context-based spec writing)

**For STANDARD tasks WITH external dependencies:**

```
discovery → requirements → research → context → spec_writing → planning → validation
```

(7 phases, includes research for unfamiliar dependencies)

**For COMPLEX tasks:**

```
discovery → requirements → research → context → spec_writing → self_critique → planning → validation
```

(8 phases, full pipeline with research and self-critique)

### Phase 5: Determine Validation Depth

Based on complexity and risk analysis, recommend validation depth:

| Risk Level   | When to Use                                    | Validation Depth                    |
| ------------ | ---------------------------------------------- | ----------------------------------- |
| **TRIVIAL**  | Docs-only, comments, whitespace                | Skip validation entirely            |
| **LOW**      | Single area, < 5 files, no DB/API changes      | Unit tests only                     |
| **MEDIUM**   | Multiple files, 1-2 areas, API changes         | Unit + Integration tests            |
| **HIGH**     | Database changes, auth/security, cross-service | Unit + Integration + E2E + Security |
| **CRITICAL** | Payments, data deletion, security-critical     | All above + Manual review + Staging |

**Skip Validation Criteria (TRIVIAL):**
Set only when ALL are true:

- Documentation-only changes (\*.md, comments, docstrings)
- OR purely cosmetic (whitespace, formatting, linting fixes)
- No functional code modified
- Confidence >= 0.9

**Security Scan Required when ANY apply:**

- Authentication/authorization code touched
- User data handling modified
- Payment/financial code involved
- API keys, secrets, or credentials handled
- New dependencies with network access
- File upload/download functionality

### Phase 6: Output Assessment

Create the structured assessment:

```markdown
# Complexity Assessment: [Task Name]

## Summary

| Dimension     | Assessment                                        |
| ------------- | ------------------------------------------------- |
| Complexity    | [simple/standard/complex]                         |
| Workflow Type | [feature/refactor/investigation/migration/simple] |
| Confidence    | [0.0-1.0]                                         |

## Reasoning

[2-3 sentence explanation]

## Analysis

### Scope

- Estimated files: [number]
- Estimated areas: [number]
- Cross-cutting: [yes/no]
- Notes: [brief explanation]

### Integrations

- External services: [list]
- New dependencies: [list]
- Research needed: [yes/no]
- Notes: [brief explanation]

### Infrastructure

- Docker changes: [yes/no]
- Database changes: [yes/no]
- Config changes: [yes/no]
- Notes: [brief explanation]

### Knowledge

- Patterns exist: [yes/no]
- Research required: [yes/no]
- Unfamiliar tech: [list]
- Notes: [brief explanation]

### Risk

- Level: [low/medium/high]
- Concerns: [list]
- Notes: [brief explanation]

## Recommended Phases

1. [phase1]
2. [phase2]
3. ...

## Validation Recommendations

| Setting          | Value                              |
| ---------------- | ---------------------------------- |
| Risk Level       | [trivial/low/medium/high/critical] |
| Skip Validation  | [yes/no]                           |
| Minimal Mode     | [yes/no]                           |
| Test Types       | [unit, integration, e2e]           |
| Security Scan    | [yes/no]                           |
| Staging Required | [yes/no]                           |

**Reasoning**: [1-2 sentences explaining validation depth]

## Flags

- Needs research: [yes/no]
- Needs self-critique: [yes/no]
- Needs infrastructure setup: [yes/no]
```

## Decision Flowchart

```
START
  |
  +--> Are there 2+ external integrations OR unfamiliar technologies?
  |     YES -> COMPLEX (needs research + critique)
  |     NO
  |      |
  +--> Are there infrastructure changes (Docker, DB, new services)?
  |     YES -> COMPLEX (needs research + critique)
  |     NO
  |      |
  +--> Is there 1 external integration that needs research?
  |     YES -> STANDARD + research phase
  |     NO
  |      |
  +--> Will this touch 3+ files across 1-2 areas?
  |     YES -> STANDARD
  |     NO
  |      |
  +--> SIMPLE (1-2 files, single area, no integrations)
```

## Verification Checklist

Before completing assessment:

- [ ] Requirements document read completely
- [ ] All complexity indicators identified
- [ ] All simplicity indicators identified
- [ ] Scope analyzed (files, areas, cross-cutting)
- [ ] Integrations analyzed (external, dependencies)
- [ ] Infrastructure needs assessed
- [ ] Knowledge gaps identified
- [ ] Risk level determined
- [ ] Phases determined
- [ ] Validation depth recommended

## Common Mistakes

### Underestimating Integrations

**Why it's wrong:** One integration can touch many files.

**Do this instead:** Flag research needs for any unfamiliar technology.

### Ignoring Infrastructure

**Why it's wrong:** Docker/DB changes add significant complexity.

**Do this instead:** Check for infrastructure needs early.

### Over-Confident

**Why it's wrong:** Rarely should confidence be above 0.9.

**Do this instead:** Be conservative. When in doubt, go higher complexity.

## Integration with Other Skills

This skill works well with:

- **spec-gathering**: Provides requirements for assessment
- **spec-writing**: Uses assessment to determine spec depth
- **qa-workflow**: Uses validation recommendations

## Memory Protocol

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.
