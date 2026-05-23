---
name: plan-expert
description: |
  Planning and architecture decision domain expert.

  Knows about:
  - Creating ADRs (Architecture Decision Records)
  - Creating technical specifications
  - Listing and discovering planning artifacts
  - Transforming plans into executable VTM tasks
  - Integrating with research tools (thinking-partner)

  Use when:
  - User wants to document an architectural decision
  - User needs to create a technical specification
  - User wants to explore or list existing ADRs/specs
  - User is ready to convert planning docs into tasks
  - User needs research before making a decision

trigger_phrases:
  - "create an adr"
  - "document a decision"
  - "document this decision"
  - "write an adr"
  - "create a spec"
  - "write a specification"
  - "technical spec"
  - "show my adrs"
  - "list adrs"
  - "show my specs"
  - "list specs"
  - "what adrs do i have"
  - "what specs exist"
  - "turn this into tasks"
  - "convert to vtm"
  - "add to vtm"
  - "make this executable"
  - "let's plan"
  - "help me plan"
  - "plan a feature"
  - "research options"
---

# Plan Expert Skill

## What This Skill Does

Guides you through the complete planning workflow from ideation to executable VTM tasks. Handles ADR and spec creation conversationally, helps you discover existing planning artifacts, and bridges your plans into VTM for execution.

Auto-discovers when you mention planning, documentation, or decision-making activities.

## Available Commands

- `/plan:to-vtm <adr-file> <spec-file>` - Transform ADR+Spec pair into VTM tasks
- `/helpers:thinking-partner` - Research and ideation support (coming soon)

## Planning Workflow

The complete planning-to-execution workflow:

```
1. Ideation & Research
   ↓ (use /helpers:thinking-partner)

2. Document Decision (ADR)
   ↓ (plan-expert creates ADR file)

3. Write Technical Spec
   ↓ (plan-expert creates spec file)

4. Transform to VTM Tasks
   ↓ (plan-expert calls /plan:to-vtm)

5. Execute Tasks
   ↓ (use vtm-expert for execution)
```

## When Claude Uses This

### Creating ADRs

When you say:

- "I want to document our decision about PostgreSQL"
- "Create an ADR for the API authentication approach"
- "We decided to use REST instead of GraphQL, let's document that"

Claude will:

1. Ask clarifying questions about the decision
2. Create ADR file in `docs/adr/ADR-XXX-{topic}.md`
3. Populate template from `.claude/templates/adr-template.md`
4. Guide you through sections (Context, Decision, Consequences)

### Creating Specifications

When you say:

- "Write a spec for the user authentication feature"
- "I need a technical specification for the API layer"
- "Create a spec for implementing the database migration system"

Claude will:

1. Link to the relevant ADR (if exists)
2. Create spec file in `docs/specs/spec-{topic}.md`
3. Populate template from `.claude/templates/spec-template.md`
4. Guide you through sections (Overview, Architecture, Implementation, Tasks)
5. Include acceptance criteria and test requirements

### Listing Planning Artifacts

When you say:

- "Show me my ADRs"
- "What specifications do I have?"
- "List all architectural decisions"

Claude will:

1. Use filesystem MCP to scan directories
2. Display formatted list with:
   - File names
   - Decision/spec titles
   - Status (proposed, accepted, deprecated)
   - Creation dates

### Converting to VTM Tasks

When you say:

- "Turn this ADR and spec into VTM tasks"
- "Add these tasks to my VTM"
- "Make this executable"

Claude will:

1. Verify ADR+Spec pair exists
2. Call `/plan:to-vtm <adr-file> <spec-file>`
3. Show preview of extracted tasks with dependencies
4. Ask for confirmation before ingesting

## ADR Template Structure

When creating an ADR, the plan-expert follows this template:

```markdown
# ADR-XXX: {Decision Title}

## Status

Proposed | Accepted | Deprecated | Superseded

## Context

What is the issue we're trying to solve? What constraints exist?

## Decision

What did we decide to do and why?

## Consequences

### Positive

- What benefits come from this decision?

### Negative

- What drawbacks or costs?
- What mitigations exist?

## Alternatives Considered

What other options did we evaluate and why did we reject them?
```

## Spec Template Structure

When creating a spec, the plan-expert follows this template:

```markdown
# Technical Specification: {Feature Name}

## Related ADR

- ADR-XXX: {Link to decision}

## Overview

Brief description of what we're building and why.

## Architecture

High-level design with components and data flow.

## Implementation Details

Detailed breakdown of what needs to be built.

## Tasks

1. Task 1 description
   - Dependencies: None
   - Test strategy: TDD/Unit/Integration/Direct
   - Estimated hours: X

2. Task 2 description
   - Dependencies: Task 1
   - Test strategy: TDD
   - Estimated hours: Y

## Acceptance Criteria

- AC1: Specific, testable criterion
- AC2: Another testable criterion

## Test Strategy

How to verify this works (unit, integration, e2e).

## Performance Requirements

Any performance constraints or targets.
```

## Integration with /plan:to-vtm

The `/plan:to-vtm` command performs intelligent task extraction:

**Input:**

- ADR file (decision context)
- Spec file (implementation details)

**Process:**

1. Reads both files with line numbers
2. Generates VTM summary (incomplete tasks only)
3. Launches AI agent to extract tasks
4. Agent analyzes dependencies semantically
5. Validates schema, dependencies, circular deps
6. Shows preview with dependency chains

**Output:**

- Validated tasks added to vtm.json
- Dependencies correctly linked
- Rich context preserved (links to source docs)
- Ready to execute with `/vtm:next`

## Token Efficiency

The plan-to-vtm bridge achieves 80% token reduction:

- VTM summary filters to incomplete tasks only
- Completed tasks reduced to capability summaries
- Agent receives only relevant context
- Prevents token budget exhaustion

## Best Practices

1. **ADR First, Spec Second**
   - Always document the decision before implementation details
   - Specs should reference their ADR

2. **One ADR per Decision**
   - Keep ADRs focused on single decisions
   - Link related ADRs if needed

3. **Detailed Acceptance Criteria**
   - Specs should have testable ACs
   - Each AC becomes validation for tasks

4. **Explicit Dependencies**
   - Spec tasks should list dependencies clearly
   - Agent uses this for VTM dependency analysis

5. **Test Strategy per Task**
   - Specify TDD/Unit/Integration/Direct
   - Aligns with VTM test_strategy field

## MCP Integration

The plan-expert skill uses these MCP servers:

**Filesystem MCP:**

- Read/write ADR files (`docs/adr/*.md`)
- Read/write spec files (`docs/specs/*.md`)
- List and discover planning artifacts
- Template population from `.claude/templates/adr-template.md` and `.claude/templates/spec-template.md`

**Firecrawl MCP** (via /helpers:thinking-partner):

- Deep research on GitHub, technical forums, documentation
- Scrape architecture examples

**Tavily MCP** (via /helpers:thinking-partner):

- General web search for research
- Find best practices and patterns

**Context7 MCP** (via /helpers:thinking-partner):

- Official library documentation
- Code examples from package docs

## Example Session

```
User: "I need to plan a new authentication system"

Claude (plan-expert): Let me help you plan that. First, have you
researched authentication approaches yet? I can help with that using
the thinking-partner.

User: "Yes, I've decided on JWT with refresh tokens"

Claude: Great! Let's document that decision. I'll create an ADR.

[Creates docs/adr/ADR-047-jwt-authentication.md from adr-template.md]

Claude: I've created ADR-047. Let me populate it with your decision...

[Populates Context, Decision, Consequences sections]

Claude: Now let's create the technical specification. What components
need to be built?

User: "Auth middleware, token service, refresh endpoint, logout"

Claude: Perfect. I'll create the spec with those tasks.

[Creates docs/specs/spec-jwt-authentication.md from spec-template.md]

Claude: I've created the spec with 8 tasks. Ready to add these to VTM?

User: "Yes, do it"

Claude: [Calls /plan:to-vtm docs/adr/ADR-047-jwt-authentication.md docs/specs/spec-jwt-authentication.md]

[Shows preview of 8 tasks with dependencies]

Claude: I see 8 new tasks. Task dependencies look good:
- TASK-020: JWT token service (no dependencies)
- TASK-021: Auth middleware (depends on TASK-020)
- TASK-022: Refresh endpoint (depends on TASK-020, TASK-021)
- ...

Shall I add these to your VTM?

User: "Yes"

Claude: ✅ Added 8 tasks to VTM. Run /vtm:next to see what's ready!
```

## Directory Structure

Expected project structure for plan domain:

```
project-root/
├── docs/
│   ├── adr/
│   │   ├── ADR-001-initial-architecture.md
│   │   ├── ADR-042-database-choice.md
│   │   └── ADR-047-jwt-authentication.md
│   └── specs/
│       ├── spec-initial-setup.md
│       ├── spec-database-layer.md
│       └── spec-jwt-authentication.md
├── .claude/
│   └── templates/
│       ├── adr-template.md
│       └── spec-template.md
└── vtm.json
```

## Customization

### Add Your Own Trigger Phrases

Edit the frontmatter above to include project-specific terms:

```yaml
trigger_phrases:
  - "create an adr"
  - "new architecture decision" # Add this
  - "rfp" # Your team uses "RFP" for specs
  - "implementation plan" # Alternative to "spec"
```

### Templates

The plan-expert uses these templates:

- `.claude/templates/adr-template.md` - ADR format
- `.claude/templates/spec-template.md` - Spec format

You can customize these templates to match your team's preferences.

## Technical Details

**Architecture:**

- Skill uses filesystem MCP for all file operations
- Commands wrap VTM CLI for transformation
- Agent-based extraction (not parsers) for flexibility
- Multi-layer validation before ingestion

**Data Flow:**

```
User intent → plan-expert detects →
Filesystem MCP (create/list files) →
User edits docs →
/plan:to-vtm (transform) →
vtm CLI (validate + ingest) →
VTM updated
```

## Error Handling

**ADR Creation Errors:**

- Directory missing: plan-expert creates `docs/adr/` directory
- Duplicate ADR number: Suggests next available number
- Template missing: Falls back to inline template

**Spec Creation Errors:**

- No ADR reference: Warns but allows creation
- Directory missing: Creates `docs/specs/` directory
- Template missing: Falls back to inline template

**Transformation Errors:**

- ADR not found: Clear error with path
- Spec not found: Clear error with path
- Validation errors: Shows all errors, suggests fixes
- Circular dependencies: Shows cycle path

## See Also

- ADR-046: Plan-VTM Bridge Architecture
- Technical spec: `specs/spec-plan-to-vtm.md`
- Command: `.claude/commands/plan/to-vtm.md`
- Design: `.claude/designs/plan.json`

## Status

**Implemented:**

- ✅ /plan:to-vtm command (transformation)

**In Progress:**

- 🔄 plan-expert skill (this file)

**Planned:**

- ⏳ /helpers:thinking-partner command
- ⏳ Validation hooks (pre-commit, pre-to-vtm)
- ⏳ MCP server registrations
