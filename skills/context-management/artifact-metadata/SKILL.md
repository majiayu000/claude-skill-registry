---
name: artifact-metadata
description: Manage artifact metadata, versioning, ownership, and history tracking. Use when relevant to the task.
---

# artifact-metadata

Manage artifact metadata, versioning, ownership, and history tracking.

## Triggers

- "update artifact metadata"
- "track artifact version"
- "artifact history"
- "who owns [artifact]"
- "artifact status"
- "version [artifact]"

## Purpose

This skill provides consistent metadata management for all SDLC and marketing artifacts. It tracks ownership, versioning, review history, and status across the artifact lifecycle.

## Behavior

When triggered, this skill:

1. **Locates or creates metadata**:
   - Check for existing `metadata.json` alongside artifact
   - Create new metadata if none exists
   - Validate against metadata schema

2. **Updates metadata fields**:
   - Version (semantic versioning)
   - Status (draft, review, baselined, deprecated)
   - Owner (agent or user)
   - Reviewers (list of reviewing agents)
   - Timestamps (created, modified, baselined)

3. **Tracks history**:
   - Version history with change summaries
   - Review records with reviewer and outcome
   - Approval records

4. **Validates relationships**:
   - Parent/child artifact links
   - Requirement traceability links
   - Cross-references to related artifacts

## Metadata Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["artifact_id", "name", "type", "version", "status", "owner"],
  "properties": {
    "artifact_id": {
      "type": "string",
      "description": "Unique identifier (e.g., SAD-001, UC-003)"
    },
    "name": {
      "type": "string",
      "description": "Human-readable artifact name"
    },
    "type": {
      "type": "string",
      "enum": ["requirements", "architecture", "test", "security", "deployment", "marketing", "report"]
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$",
      "description": "Semantic version"
    },
    "status": {
      "type": "string",
      "enum": ["draft", "review", "approved", "baselined", "deprecated"]
    },
    "owner": {
      "type": "string",
      "description": "Primary owner (agent name or user)"
    },
    "created": {
      "type": "string",
      "format": "date-time"
    },
    "modified": {
      "type": "string",
      "format": "date-time"
    },
    "baselined": {
      "type": "string",
      "format": "date-time"
    },
    "reviewers": {
      "type": "array",
      "items": {"type": "string"}
    },
    "history": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "version": {"type": "string"},
          "date": {"type": "string", "format": "date-time"},
          "author": {"type": "string"},
          "summary": {"type": "string"}
        }
      }
    },
    "reviews": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "reviewer": {"type": "string"},
          "date": {"type": "string", "format": "date-time"},
          "outcome": {"type": "string", "enum": ["approved", "conditional", "rejected"]},
          "comments": {"type": "string"}
        }
      }
    },
    "traceability": {
      "type": "object",
      "properties": {
        "requirements": {"type": "array", "items": {"type": "string"}},
        "parent": {"type": "string"},
        "children": {"type": "array", "items": {"type": "string"}}
      }
    },
    "tags": {
      "type": "array",
      "items": {"type": "string"}
    }
  }
}
```

## Usage Examples

### Create New Metadata

```
User: "Create metadata for the SAD"

Skill creates:
.aiwg/architecture/sad/metadata.json
{
  "artifact_id": "SAD-001",
  "name": "Software Architecture Document",
  "type": "architecture",
  "version": "0.1.0",
  "status": "draft",
  "owner": "architecture-designer",
  "created": "2025-12-08T14:30:00Z",
  "modified": "2025-12-08T14:30:00Z",
  "reviewers": [],
  "history": [],
  "reviews": []
}
```

### Update Version After Changes

```
User: "Version the SAD to 1.0.0 with summary 'Initial baseline'"

Skill updates:
- version: "1.0.0"
- status: "baselined"
- baselined: "2025-12-08T16:45:00Z"
- history: [adds entry with version, date, summary]
```

### Record Review

```
User: "Record security-architect review as approved"

Skill updates:
- reviews: [adds review record]
- reviewers: [adds "security-architect" if not present]
- modified: [updates timestamp]
```

### Query Ownership

```
User: "Who owns the test plan?"

Skill responds:
"Test Plan (TP-001) is owned by test-architect.
Status: review
Version: 0.3.0
Last modified: 2025-12-07
Reviewers: security-auditor, requirements-analyst"
```

## Status Lifecycle

```
draft → review → approved → baselined
  ↑        ↓
  └── rejected (returns to draft)

baselined → deprecated (end of life)
```

### Status Transitions

| From | To | Triggered By |
|------|-----|-------------|
| draft | review | Submit for review |
| review | approved | All reviewers approve |
| review | draft | Any reviewer rejects |
| approved | baselined | Formal baseline action |
| baselined | deprecated | Superseded or retired |

## Version Conventions

- **0.x.x**: Draft versions (not baselined)
- **1.0.0**: First baseline
- **x.y.0**: Minor changes (compatible)
- **x.0.0**: Major changes (may break traceability)

### Auto-Version Rules

| Change Type | Version Bump |
|-------------|-------------|
| Typo fix | patch (0.0.x) |
| Section update | minor (0.x.0) |
| Structure change | major (x.0.0) |
| Initial baseline | 1.0.0 |

## Artifact Type Conventions

| Type | ID Prefix | Location |
|------|-----------|----------|
| requirements | UC-, REQ-, NFR- | .aiwg/requirements/ |
| architecture | SAD-, ADR-, API- | .aiwg/architecture/ |
| test | TP-, TC-, TS- | .aiwg/testing/ |
| security | TM-, SEC- | .aiwg/security/ |
| deployment | DP-, RN- | .aiwg/deployment/ |
| marketing | CB-, CA- | .aiwg/marketing/ |
| report | RPT- | .aiwg/reports/ |

## CLI Usage

```bash
# Create metadata for artifact
python artifact_metadata.py --create --artifact ".aiwg/architecture/sad.md" --type architecture

# Update version
python artifact_metadata.py --version "1.0.0" --artifact ".aiwg/architecture/sad.md" --summary "Initial baseline"

# Record review
python artifact_metadata.py --review --artifact ".aiwg/architecture/sad.md" \
  --reviewer "security-architect" --outcome "approved" --comments "LGTM"

# Query metadata
python artifact_metadata.py --query --artifact ".aiwg/architecture/sad.md"

# List all artifacts by status
python artifact_metadata.py --list --status "review"

# Validate all metadata
python artifact_metadata.py --validate-all
```

## Integration

This skill integrates with:
- `artifact-orchestration`: Sets initial metadata when creating artifacts
- `gate-evaluation`: Checks artifact status for gate criteria
- `traceability-check`: Uses traceability links in metadata
- `template-engine`: Copies metadata template on instantiation

## Output Locations

- Metadata file: `{artifact-dir}/metadata.json`
- Alternatively: `{artifact-dir}/{artifact-name}.metadata.json`
- Index file: `.aiwg/reports/artifact-index.json`

## References

- Schema: `schemas/artifact-metadata.schema.json`
- Conventions: AIWG Artifact Naming Guide
