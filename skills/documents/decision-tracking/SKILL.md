---
name: Decision Tracking
description: Architecture Decision Records (ADR) templates, sequential numbering, decision documentation patterns, and decision history management. Use when creating ADRs, documenting architectural decisions, tracking decision rationale, managing decision lifecycle, superseding decisions, searching decision history, or when user mentions ADR, architecture decision, decision record, decision tracking, or decision documentation.
allowed-tools:
---

# Decision Tracking Skill

**CRITICAL: The description field above controls when Claude auto-loads this skill.**

## Overview

Provides comprehensive Architecture Decision Record (ADR) management following Michael Nygard's ADR format. Includes automatic sequential numbering, decision lifecycle tracking, superseding workflows, and decision search capabilities.

## Instructions

### Creating New ADRs

1. Use `scripts/create-adr.sh <title> [docs-path]` to create a new ADR with automatic numbering
2. Script automatically determines next sequential number (0001, 0002, etc.)
3. Creates ADR file with Michael Nygard format: `NNNN-title-in-kebab-case.md`
4. Populates ADR with proper frontmatter (date, status, deciders)
5. Updates the ADR index automatically

### Listing ADRs

1. Use `scripts/list-adrs.sh [docs-path] [--status=accepted|proposed|deprecated|superseded]` to view all ADRs
2. Displays ADR number, title, status, date, and file path
3. Supports filtering by status: accepted, proposed, deprecated, superseded
4. Shows ADRs in chronological order by number
5. Optionally displays quick summary of each ADR

### Searching ADRs

1. Use `scripts/search-adrs.sh <search-term> [docs-path]` to search ADR content
2. Searches titles, context, decisions, and consequences sections
3. Returns matching ADRs with relevant snippets
4. Highlights search terms in results
5. Supports regex patterns for advanced searches

### Updating ADR Index

1. Use `scripts/update-adr-index.sh [docs-path]` to regenerate ADR index
2. Scans all ADR files and extracts metadata
3. Generates comprehensive index with links to all ADRs
4. Groups ADRs by status (accepted, proposed, deprecated, superseded)
5. Updates `docs/adr/index.md` or specified path

### Superseding ADRs

1. Use `scripts/supersede-adr.sh <old-adr-number> <new-title> [docs-path]` to supersede an ADR
2. Marks old ADR status as "superseded" with link to new ADR
3. Creates new ADR with reference to superseded ADR
4. Maintains decision history and rationale chain
5. Updates ADR index automatically

## Available Scripts

- **create-adr.sh**: Create new ADR with auto-numbering and proper format
- **list-adrs.sh**: List all ADRs with filtering and status display
- **search-adrs.sh**: Search ADR content with regex support
- **update-adr-index.sh**: Regenerate comprehensive ADR index
- **supersede-adr.sh**: Mark ADR as superseded and create replacement

## Templates

- **adr-template.md**: Michael Nygard ADR format with all sections
- **adr-frontmatter.yaml**: YAML frontmatter structure for ADR metadata
- **adr-index-template.md**: ADR index format with status groupings
- **decision-matrix.md**: Decision comparison matrix for evaluating options
- **consequences-template.md**: Detailed consequences documentation format

## Examples

See `examples/` directory for detailed usage examples:
- `example-adr-technology.md` - Technology choice ADR (database selection)
- `example-adr-architecture.md` - Architectural decision (microservices vs monolith)
- `example-adr-security.md` - Security decision (authentication strategy)
- `example-adr-superseded.md` - Superseded ADR with replacement links
- `example-adr-index.md` - Complete ADR index with multiple entries

## ADR Format (Michael Nygard)

### Standard Sections

1. **Title**: Short noun phrase describing the decision
2. **Status**: proposed | accepted | deprecated | superseded
3. **Context**: Forces at play, including technological, political, social, and project constraints
4. **Decision**: Response to these forces, stated in full sentences with active voice
5. **Consequences**: Context after applying the decision, including positive, negative, and neutral effects

### Frontmatter Fields

```yaml
---
number: 0001
title: Use PostgreSQL for Primary Database
date: 2025-10-28
status: accepted
deciders: [Tech Lead, Backend Team]
consulted: [DevOps, Security Team]
informed: [Frontend Team, Product]
---
```

### Numbering Convention

- Use 4-digit zero-padded sequential numbers: 0001, 0002, 0003, etc.
- Filename format: `NNNN-title-in-kebab-case.md`
- Examples: `0001-use-postgresql.md`, `0042-adopt-microservices.md`
- Never reuse numbers even if ADR is deleted

## Decision Lifecycle

### Status Transitions

1. **proposed** → Initial state when ADR is created
2. **accepted** → Decision has been approved and implemented
3. **deprecated** → Decision is no longer recommended but still in use
4. **superseded** → Decision has been replaced by a newer ADR

### Superseding Workflow

1. Identify ADR to supersede (e.g., ADR-0005)
2. Run `supersede-adr.sh 0005 "New Decision Title"`
3. Old ADR updated: status → "superseded", link added to new ADR
4. New ADR created with reference to superseded ADR
5. Index updated automatically

## ADR Storage Structure

Recommended directory structure:
```
docs/
  adr/
    index.md              # Master index of all ADRs
    0001-first-decision.md
    0002-second-decision.md
    0003-third-decision.md
    templates/
      adr-template.md     # Template for new ADRs
```

## Decision Matrix Usage

When evaluating multiple options:
1. Use `templates/decision-matrix.md` to structure comparison
2. Define criteria (performance, cost, maintainability, etc.)
3. Score each option against criteria
4. Weight criteria by importance
5. Calculate weighted scores to guide decision
6. Include completed matrix in ADR context section

## Search Capabilities

The search script supports:
- **Full-text search**: Search all ADR content
- **Regex patterns**: Use patterns like `"auth.*strategy"`
- **Section-specific**: Search only in specific sections
- **Status filtering**: Combine with status filter
- **Date range**: Search ADRs within date range

## Integration

This skill is used by:
- `planning:adr-create` command - Create new ADRs interactively
- `planning:adr-list` command - List and filter ADRs
- `planning:adr-supersede` command - Supersede existing ADRs
- All planning agents requiring decision documentation

## Best Practices

### Writing Effective ADRs

1. **Be specific**: Clearly state what is being decided
2. **Document context**: Explain why the decision is needed
3. **List alternatives**: Show what options were considered
4. **Describe consequences**: Include positive and negative impacts
5. **Use active voice**: "We will use PostgreSQL" not "PostgreSQL will be used"

### When to Create ADRs

- Choosing between architectural patterns (monolith vs microservices)
- Selecting core technologies (databases, frameworks, languages)
- Defining system boundaries and interfaces
- Establishing security or authentication strategies
- Setting coding standards or development practices

### When NOT to Create ADRs

- Routine bug fixes or minor refactoring
- Implementing already-decided features
- Temporary workarounds or experiments
- Decisions that can be easily reversed
- Team process decisions (use meeting notes instead)

## Output Format

All scripts output in consistent formats:
- **list-adrs.sh**: Table format with columns: Number | Title | Status | Date
- **search-adrs.sh**: List format with ADR number, title, and matching snippet
- **create-adr.sh**: Outputs path to created ADR file
- **supersede-adr.sh**: Outputs paths to both old and new ADR files

## Requirements

- ADRs must follow Michael Nygard format exactly
- Sequential numbering must be maintained without gaps
- Frontmatter must include all required fields
- Status must be one of: proposed, accepted, deprecated, superseded
- Superseded ADRs must link to replacement ADRs
- Index must be updated after every ADR creation

---

**Purpose**: Comprehensive Architecture Decision Record management and documentation
**Used by**: All planning agents and commands requiring decision tracking
