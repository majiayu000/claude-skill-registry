---
name: Spec Management
description: Templates, scripts, and examples for managing feature specifications in specs/ directory. Use when creating feature specs, listing specifications, validating spec completeness, updating spec status, searching spec content, organizing project requirements, tracking feature development, managing technical documentation, or when user mentions spec management, feature specifications, requirements docs, spec validation, or specification organization.
allowed-tools: 
---

# Spec Management Skill

**CRITICAL: The description field above controls when Claude auto-loads this skill.**

## Overview

Provides comprehensive specification management capabilities including spec creation, status tracking, validation, searching, and template-based documentation. Manages feature specifications in the `specs/` directory with consistent numbering, metadata, and status tracking.

## Instructions

### Creating New Specifications

1. Use `scripts/create-spec.sh <spec-name> [description]` to create new numbered specs
2. Automatically assigns next available spec number (e.g., 001-feature-name.md)
3. Generates spec with complete frontmatter and all sections
4. Initializes status as "draft" with creation timestamp
5. Creates organized directory structure if needed

### Listing Specifications

1. Use `scripts/list-specs.sh [--status STATUS] [--format FORMAT]` to list all specs
2. Displays specs with number, title, status, priority, and last modified date
3. Filter by status: draft, in-progress, review, approved, implemented, rejected
4. Output formats: table (default), json, markdown, csv
5. Sorted by spec number with color-coded status indicators

### Validating Specifications

1. Use `scripts/validate-spec.sh <spec-file>` to check spec completeness
2. Validates frontmatter: title, status, priority, owner, tags
3. Checks required sections: Problem, Solution, Requirements, Tasks, Success Criteria
4. Verifies task breakdown format and numbering
5. Generates validation report with warnings and errors

### Updating Spec Status

1. Use `scripts/update-status.sh <spec-file> <new-status>` to change spec status
2. Valid statuses: draft, in-progress, review, approved, implemented, rejected
3. Updates status timestamp and maintains status history
4. Optionally adds status change comment
5. Validates status transition rules

### Searching Specifications

1. Use `scripts/search-specs.sh <query> [--section SECTION]` to search spec content
2. Searches across all specs or within specific sections
3. Supports regex patterns and multi-word queries
4. Displays matches with context and spec location
5. Filter by tags, status, or priority

## Available Scripts

- **create-spec.sh**: Create new numbered specification with template
- **list-specs.sh**: List all specifications with filtering and formatting
- **validate-spec.sh**: Validate spec completeness and format
- **update-status.sh**: Update specification status with history tracking
- **search-specs.sh**: Search specification content with context

## Templates

- **spec-template.md**: Complete specification template with all standard sections
- **spec-metadata.yaml**: Frontmatter template with all metadata fields
- **task-breakdown-template.md**: Task list format with subtasks and estimates
- **requirements-template.md**: Requirements documentation format (functional, non-functional, constraints)
- **success-criteria-template.md**: Success metrics and acceptance criteria format

## Examples

See `examples/` directory for detailed usage examples:
- `example-spec-simple.md` - Simple feature specification with basic sections
- `example-spec-complex.md` - Complex feature with detailed technical design
- `example-spec-ai-feature.md` - AI/ML feature specification with model details
- `example-validation-report.md` - Example validation output with errors and warnings
- `example-spec-list.md` - Example list command output in different formats

## Specification Structure

### Required Frontmatter
```yaml
---
spec-id: 001
title: Feature Name
status: draft
priority: medium
owner: team-name
created: 2025-01-15
updated: 2025-01-15
tags: [category, feature-type]
---
```

### Required Sections
1. **Problem Statement** - What problem are we solving?
2. **Proposed Solution** - How will we solve it?
3. **Requirements** - Functional, non-functional, constraints
4. **Technical Design** - Architecture, components, data models
5. **Task Breakdown** - Numbered tasks with estimates
6. **Success Criteria** - Measurable outcomes and acceptance criteria
7. **Dependencies** - External dependencies and blockers
8. **Timeline** - Estimated schedule and milestones
9. **Risks** - Potential risks and mitigation strategies

### Status Workflow
```
draft → in-progress → review → approved → implemented
                               ↓
                            rejected
```

## Validation Rules

### Frontmatter Validation
- Spec ID must be numeric and unique
- Status must be valid enum value
- Priority must be: low, medium, high, critical
- Owner must be specified
- Created and updated dates must be valid ISO dates
- Tags must be non-empty array

### Content Validation
- All required sections must be present
- Each section must have content (not empty)
- Task breakdown must have numbered tasks
- Requirements must be categorized
- Success criteria must be measurable

### Warnings
- Long spec (>1000 lines) may need splitting
- Missing optional sections (e.g., Alternatives Considered)
- Outdated spec (not updated in >30 days)
- Tasks without estimates
- Vague success criteria

## Directory Structure

### Phase-Nested Structure (Recommended)

Specs are organized in phase directories based on dependencies:

```
specs/
├── phase-0/                    # Features with no dependencies
│   ├── F001-core-data/
│   │   ├── spec.md
│   │   └── tasks.md
│   └── F002-base-api/
├── phase-1/                    # Features depending on Phase 0
│   ├── F003-user-auth/
│   └── F004-chat-system/
├── phase-2/                    # Features depending on Phase 1
│   └── F005-analytics/
└── infrastructure/             # Infrastructure specs (not phased)
    └── 001-database/
```

### Phase Calculation

Phase is calculated automatically based on dependencies:
- **Phase 0**: No dependencies (foundation features)
- **Phase N**: max(dependency phases) + 1

Example: F003 depends on F001 (phase 0) and F002 (phase 0) → F003 is Phase 1

### Naming Convention

- **Format**: `F{XXX}-{feature-slug}/`
- **Numbering**: Zero-padded 3-digit IDs (F001, F002, ..., F050, F100)
- **Slug**: kebab-case, 2-4 words max
- Numbers are never reused. Deleted specs leave gaps in numbering.

### Legacy Flat Structure

For backward compatibility, the system also supports:
```
specs/
├── features/
│   ├── 001-feature-name/
│   └── 002-another-feature/
└── infrastructure/
    └── 001-component/
```

The system checks phase-nested first, then falls back to legacy structure.

## Integration

This skill is used by:
- `planning:create-spec` command - Create new feature specifications
- `planning:review-specs` command - Review and validate all specs
- `planning:track-progress` command - Track feature implementation progress
- All development agents - Reference specs for implementation guidance
- Project management tools - Export spec data for tracking

## Best Practices

1. **Keep specs focused** - One feature per spec
2. **Update status regularly** - Reflect current development state
3. **Link related specs** - Reference dependencies between specs
4. **Include examples** - Add code samples and mockups
5. **Review before approval** - Validate with team before implementation
6. **Archive old specs** - Move implemented specs to archive/
7. **Use consistent tags** - Maintain tag taxonomy for filtering
8. **Write measurable criteria** - Success criteria must be testable

---

**Purpose**: Comprehensive specification management for feature documentation
**Used by**: Planning agents, development teams, project managers
