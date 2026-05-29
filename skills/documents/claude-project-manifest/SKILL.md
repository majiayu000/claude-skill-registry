---
name: claude-project-manifest
description: Creates annotated bibliography-style manifests for Claude projects, tracking files, conversation threads, and relationships with unique IDs and annotations. Use when documenting project contents, creating file inventories, tracking conversation history, or building navigable knowledge maps.
license: MIT
complexity: intermediate
time_to_learn: 30min
tags: [documentation, inventory, annotation, bibliography, knowledge-management]
---

# Claude Project Manifest

Create structured, annotated documentation of Claude projects that tracks files, conversation threads, and their relationships.

## When to Use

- Documenting project contents and structure
- Creating file inventories with annotations
- Tracking conversation history across sessions
- Building navigable knowledge maps
- Onboarding new collaborators to existing projects

## Core Concepts

### Manifest Structure

A manifest has four primary sections:

1. **Metadata**: Project-level information (ID, version, status)
2. **Files**: Annotated file inventory with provenance
3. **Threads**: Conversation summaries and accomplishments
4. **Relations**: Dependencies and connections between entities

### ID System

| Entity | Format | Example |
|--------|--------|---------|
| Project | `PROJ-{YEAR}-{SEQ}` | `PROJ-2024-001` |
| File | `FILE-{SEQ}` | `FILE-042` |
| Thread | `THR-{SEQ}` | `THR-017` |
| Relation | `REL-{SEQ}` | `REL-123` |

## Quick Start

### Minimal Manifest

```yaml
manifest:
  id: "PROJ-2024-001"
  version: "1.0.0"
  created: "2024-01-15T10:30:00Z"

  project:
    name: "My Project"
    description: "Brief description of the project"
    status: active

files:
  - id: "FILE-001"
    path: "src/main.py"
    title: "Main Entry Point"
    summary: "Application entry and initialization"
```

### Full File Entry

```yaml
files:
  - id: "FILE-001"
    path: "src/main.py"
    type: source  # source | config | doc | asset | generated
    thread_id: "THR-001"
    title: "Main Entry Point"
    summary: "One-line description of purpose"
    notes: |
      Extended annotation explaining:
      - Design decisions made
      - Why this approach was chosen
      - Key implementation details
      - Known limitations or TODOs
    tags: [core, initialization]
    depends_on: ["FILE-002", "FILE-003"]
    created: "2024-01-15T10:30:00Z"
    modified: "2024-01-16T14:20:00Z"
```

### Thread Entry

```yaml
threads:
  - id: "THR-001"
    started: "2024-01-15T10:30:00Z"
    ended: "2024-01-15T12:45:00Z"
    title: "Initial Project Setup"
    summary: "Created core infrastructure and configuration"
    accomplishments:
      - "Created directory structure"
      - "Implemented Config class with validation"
      - "Added logging infrastructure"
    files_created: ["FILE-001", "FILE-002"]
    files_modified: []
    decisions:
      - "Chose YAML over JSON for config readability"
      - "Used dataclasses instead of Pydantic for simplicity"
    tags: [setup, infrastructure]
```

### Relations

```yaml
relations:
  - id: "REL-001"
    type: depends_on
    source: "FILE-001"
    target: "FILE-002"
    annotation: "Main imports and uses Config class"

  - id: "REL-002"
    type: implements
    source: "FILE-003"
    target: "FILE-004"
    annotation: "Repository implements StorageInterface"
```

Relation types:
- `depends_on`: Source requires target to function
- `extends`: Source builds upon target
- `implements`: Source implements interface defined in target
- `references`: Source refers to target without hard dependency
- `supersedes`: Source replaces target (for versioning)

## Writing Annotations

### File Annotations

Good annotations answer:
- **What**: What does this file do?
- **Why**: Why was this approach chosen?
- **How**: Key implementation details
- **Context**: What prompted its creation?

Example:
```yaml
notes: |
  Implements rate limiting using token bucket algorithm.
  Chose token bucket over sliding window for better burst handling.
  Created during THR-003 when API overload issues emerged.
  TODO: Add Redis backend for distributed rate limiting.
```

### Thread Annotations

Capture:
- **Goal**: What we set out to accomplish
- **Outcome**: What we actually achieved
- **Decisions**: Key choices made and rationale
- **Artifacts**: Files created or modified

## Workflow

### Starting a New Project

1. Create manifest file (`manifest.yaml`)
2. Add project metadata
3. Set initial status to `active`

### During Development

1. Log new threads as conversations happen
2. Add files with annotations when created
3. Record relations as dependencies form
4. Update thread accomplishments

### Project Handoff

1. Review all thread summaries
2. Verify file annotations are current
3. Validate all relations are documented
4. Export to markdown report if needed

## Output Formats

### YAML (Primary)

Best for editing and version control. See `assets/templates/manifest.yaml`.

### JSON (Machine-Readable)

For programmatic access. See `assets/templates/manifest.json`.

### Markdown Report

Human-readable export for documentation. See `assets/templates/manifest-report.md`.

## References

- `references/manifest-schema.md` — Full schema specification
- `references/annotation-guidelines.md` — Writing effective annotations
- `references/id-systems.md` — ID generation strategies
- `references/workflow-integration.md` — Integration patterns

## Related Skills

- **knowledge-graph-builder**: For more complex relationship modeling
- **documentation-generator**: For generating docs from manifests
