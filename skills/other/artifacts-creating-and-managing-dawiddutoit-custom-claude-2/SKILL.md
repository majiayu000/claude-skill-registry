---
name: artifacts-creating-and-managing
description: |
  Creates and manages project artifacts (research, spikes, analysis, plans) using templated scripts.
  Use when asked to "create an ADR", "research topic", "spike investigation", "implementation plan", or "create analysis".
  Provides standardized structure, naming conventions, and helper scripts for artifact organization.
  Works with .claude/artifacts/ directory, Python scripts, and markdown templates.
allowed-tools: Read, Write, Bash, Glob, Edit
---

# Artifacts: Creating and Managing

## Table of Contents

1. [Quick Start](#quick-start)
2. [Triggers](#triggers)
3. [Purpose](#purpose)
4. [When to Use Artifacts](#when-to-use-artifacts)
5. [Directory Structure](#directory-structure)
6. [File Naming Conventions](#file-naming-conventions)
7. [Core Rules](#core-rules)
8. [Category Definitions](#category-definitions)
9. [Helper Scripts](#helper-scripts)
10. [Integration Pattern](#integration-pattern)
11. [Supporting Files](#supporting-files)
12. [Best Practices](#best-practices)
13. [Red Flags to Avoid](#red-flags-to-avoid)

## Quick Start

See [scripts/create_adr.py](/Users/dawiddutoit/projects/claude/custom-claude/skills/artifacts-creating-and-managing/scripts/create_adr.py) for creating ADRs.

See [scripts/create_research_topic.py](/Users/dawiddutoit/projects/claude/custom-claude/skills/artifacts-creating-and-managing/scripts/create_research_topic.py) for creating research topics.

See [scripts/create_implementation_plan.py](/Users/dawiddutoit/projects/claude/custom-claude/skills/artifacts-creating-and-managing/scripts/create_implementation_plan.py) for creating implementation plans.

## Triggers

Trigger with phrases like:
- "create an ADR"
- "create ADR for [decision]"
- "research [topic]"
- "create research topic"
- "spike investigation on [topic]"
- "create spike for [investigation]"
- "implementation plan for [feature]"
- "create analysis"
- "analyze [subject]"
- "document decision"
- "plan implementation"

## Purpose

Standardizes how artifacts are created and organized within `.claude/artifacts/` directory. Artifacts are temporary work products that support development but don't belong in version control or permanent documentation.

## When to Use This Skill

Use when asked to:
- Document architectural decisions ("create an ADR for event sourcing")
- Research technical topics ("research GraphQL libraries for React")
- Plan feature implementations ("create implementation plan for 2FA")
- Conduct time-boxed investigations ("spike on OAuth2 integration")
- Analyze existing code or architecture ("analyze performance bottlenecks")

Do NOT use when:
- Creating permanent documentation (use `docs/` directory instead)
- Writing source code (use `src/` directory)
- User needs quick inline answers (respond directly in conversation)

## When to Use Artifacts

**Use artifacts when:**
- Conducting research ("research GraphQL libraries")
- Creating spikes ("spike on authentication approaches")
- Writing analysis ("analyze performance bottlenecks")
- Documenting decisions (ADRs)
- Planning implementations
- Capturing session notes
- Recording investigation results

**Don't use artifacts for:**
- Permanent documentation (use `docs/` instead)
- Source code (use `src/` instead)
- Tests (use `tests/` instead)
- Configuration (use config files)

## Directory Structure

```
.claude/artifacts/
├── YYYY-MM-DD/                    # Date-based organization
│   ├── research/                  # Research topics
│   │   └── topic-name.md
│   ├── spikes/                    # Technical spikes
│   │   └── spike-name.md
│   ├── analysis/                  # Code/architecture analysis
│   │   └── analysis-name.md
│   ├── plans/                     # Implementation plans
│   │   └── plan-name.md
│   ├── sessions/                  # Session notes
│   │   └── session-name.md
│   └── adr/                       # Architecture Decision Records
│       └── NNN-decision-name.md
└── completed/                     # Archived artifacts
    └── adr/
        └── NNN-decision-name.md
```

## File Naming Conventions

**Research topics:**
```
.claude/artifacts/YYYY-MM-DD/research/topic-name.md
Example: .claude/artifacts/2025-12-24/research/graphql-libraries.md
```

**Spikes:**
```
.claude/artifacts/YYYY-MM-DD/spikes/spike-name.md
Example: .claude/artifacts/2025-12-24/spikes/oauth2-integration.md
```

**Analysis:**
```
.claude/artifacts/YYYY-MM-DD/analysis/analysis-name.md
Example: .claude/artifacts/2025-12-24/analysis/performance-bottlenecks.md
```

**Implementation plans:**
```
.claude/artifacts/YYYY-MM-DD/plans/feature-name-plan.md
Example: .claude/artifacts/2025-12-24/plans/user-authentication-plan.md
```

**ADRs:**
```
.claude/artifacts/YYYY-MM-DD/adr/NNN-decision-title.md
Example: .claude/artifacts/2025-12-24/adr/001-use-event-sourcing.md
```

## Core Rules

1. **Date-based organization** - All artifacts under `YYYY-MM-DD/` directory
2. **Kebab-case names** - Use hyphens, lowercase, no spaces
3. **Category folders** - research/, spikes/, analysis/, plans/, adr/
4. **Markdown format** - All artifacts are .md files
5. **Templated creation** - Use helper scripts for consistency
6. **Completion tracking** - Move to `completed/` when done

## Category Definitions

### Research
**Purpose:** Investigate libraries, tools, or approaches

**Template:** See [templates/research_template.md](/Users/dawiddutoit/projects/claude/custom-claude/skills/artifacts-creating-and-managing/templates/research_template.md)

**Example usage:** "Research GraphQL client libraries for React"

### Spikes
**Purpose:** Time-boxed technical investigation

**Template:** Spike template not yet created (use research template as starting point)

**Example usage:** "Spike on OAuth2 integration with existing auth system"

### Analysis
**Purpose:** Investigate existing code/architecture

**Template:** Analysis template not yet created (use research template as starting point)

**Example usage:** "Analyze performance bottlenecks in API handlers"

### Plans
**Purpose:** Document implementation approach

**Template:** See [templates/implementation_plan_template.md](/Users/dawiddutoit/projects/claude/custom-claude/skills/artifacts-creating-and-managing/templates/implementation_plan_template.md)

**Example usage:** "Plan implementation of two-factor authentication"

### ADRs (Architecture Decision Records)
**Purpose:** Document architectural decisions

**Template:** See [templates/adr_template.md](/Users/dawiddutoit/projects/claude/custom-claude/skills/artifacts-creating-and-managing/templates/adr_template.md)

**Example usage:** "ADR 001: Use Event Sourcing for Audit Trail"

## Helper Scripts

All scripts located in `.claude/skills/artifacts-creating-and-managing/scripts/`:

### create_adr.py

See [scripts/create_adr.py](/Users/dawiddutoit/projects/claude/custom-claude/skills/artifacts-creating-and-managing/scripts/create_adr.py) for full script.

**Required:** --title, --status, --context
**Optional:** --decision, --consequences

### create_research_topic.py

See [scripts/create_research_topic.py](/Users/dawiddutoit/projects/claude/custom-claude/skills/artifacts-creating-and-managing/scripts/create_research_topic.py) for full script.

**Required:** --topic, --objective
**Optional:** --questions (multiple)

### create_spike.py

Note: Spike script not yet created. Use create_research_topic.py as alternative.

### create_analysis.py

Note: Analysis script not yet created. Use create_research_topic.py as alternative.

### create_implementation_plan.py

See [scripts/create_implementation_plan.py](/Users/dawiddutoit/projects/claude/custom-claude/skills/artifacts-creating-and-managing/scripts/create_implementation_plan.py) for full script.

**Required:** --feature, --overview
**Optional:** --steps (multiple), --risks

## Integration Pattern

**Typical workflow:**

1. **Create artifact:** Use helper scripts (see Helper Scripts section)
2. **Work on artifact:**
   - Add findings, analysis, or decisions
   - Reference code, documentation, or other artifacts
   - Update as investigation progresses
3. **Complete artifact:**
   - Mark as complete (status: accepted/completed)
   - Move to `completed/` if ADR
   - Reference in code or documentation
   - Archive or delete if temporary
4. **Cross-reference:**
   - Link from code comments: `// See: .claude/artifacts/YYYY-MM-DD/research/topic.md`
   - Link from documentation: `docs/` references artifacts
   - Link between artifacts: Related ADRs reference each other

## Usage Examples

See [examples/](/Users/dawiddutoit/projects/claude/custom-claude/skills/artifacts-creating-and-managing/examples/) directory for detailed usage examples including:
- Research library workflow
- ADR creation workflow
- Implementation plan workflow

## Expected Outcomes

**Successful Artifact Creation:**
- Artifact created in correct location (`.claude/artifacts/YYYY-MM-DD/{category}/`)
- File follows naming conventions (kebab-case)
- Template applied with placeholders filled
- Ready for content addition

**Completed Artifact:**
- Decision documented (for ADRs)
- Research findings captured (for research)
- Implementation steps defined (for plans)
- Cross-referenced in code/docs where appropriate
- Moved to `completed/` if applicable

## Supporting Files

- **[templates/](templates/)** - Markdown templates:
  - adr-template.md
  - research-template.md
  - spike-template.md
  - analysis-template.md
  - plan-template.md

- **[scripts/](scripts/)** - Helper scripts:
  - create_adr.py
  - create_research_topic.py
  - create_spike.py
  - create_analysis.py
  - create_implementation_plan.py
  - list_artifacts.py (find all artifacts)
  - archive_artifact.py (move to completed/)

## Best Practices

1. **Use templates** - Scripts ensure consistency
2. **Date organization** - Easy to find recent artifacts
3. **Descriptive names** - Clear purpose from filename
4. **Complete artifacts** - Don't leave them half-finished
5. **Cross-reference** - Link artifacts to code/docs
6. **Archive when done** - Move completed ADRs to `completed/`
7. **Delete temporary artifacts** - Don't accumulate unnecessary files
8. **Update status** - Keep artifact status current

## Red Flags to Avoid

1. **Creating artifacts in wrong location** - Always use `.claude/artifacts/`
2. **Skipping date folder** - All artifacts under `YYYY-MM-DD/`
3. **Mixed case names** - Use kebab-case consistently
4. **No category folder** - Put in research/, spikes/, etc.
5. **Creating without template** - Use helper scripts
6. **Leaving artifacts incomplete** - Finish or delete
7. **Not archiving ADRs** - Move completed ADRs to `completed/`
8. **Creating permanent docs as artifacts** - Use `docs/` for permanent documentation

---

**Key principle:** Artifacts are temporary work products with standardized structure. They support development but aren't permanent documentation.

**Remember:** Use helper scripts for consistency, organize by date, and archive/delete when complete.
