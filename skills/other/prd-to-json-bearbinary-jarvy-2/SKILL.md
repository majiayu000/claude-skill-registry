---
name: prd-to-json
description: "Convert a PRD markdown file to a structured JSON task file with progress tracking. Use when converting a PRD to JSON, creating trackable tasks from a PRD, or when asked to make a PRD actionable. Triggers on: convert prd to json, prd to json, make prd trackable, create tasks from prd, json from prd."
---

# PRD to JSON Converter

Convert PRD markdown documents into structured JSON task files with progress tracking capabilities.

---

## The Job

1. Read an existing PRD markdown file from `/PRD/` or `/tasks/`
2. Parse the PRD structure (user stories, requirements, etc.)
3. Generate a JSON file with `passed` fields for tracking completion
4. Save to `/tasks/[prd-name].json`

**Important:** This skill converts existing PRDs. Use the `prd` skill first to create the PRD.

---

## Input

The skill accepts:
- A path to a PRD markdown file (e.g., `/PRD/pyroscope-and-load-testing.md`)
- Or a PRD name to search for in `/PRD/` or `/tasks/` directories

---

## JSON Output Schema

```json
{
  "title": "string - Feature/PRD title",
  "priority": "High | Medium | Low",
  "status": "Not Started | In Progress | Partially Compliant | Compliant",
  "source": "string - Path to source PRD file",
  "createdAt": "ISO 8601 timestamp",
  "updatedAt": "ISO 8601 timestamp",
  "overview": {
    "description": "string - Brief description from PRD introduction",
    "goals": ["array of goal strings"]
  },
  "userStories": [
    {
      "id": "US-001",
      "title": "string",
      "description": "string - The 'As a... I want... so that...' statement",
      "passed": false,
      "acceptanceCriteria": [
        {
          "criterion": "string - The specific criterion",
          "passed": false
        }
      ]
    }
  ],
  "functionalRequirements": [
    {
      "id": "FR-1",
      "description": "string",
      "passed": false
    }
  ],
  "nonGoals": ["array of non-goal strings"],
  "technicalConsiderations": [
    {
      "area": "string - Topic area",
      "details": "string - Details or considerations"
    }
  ],
  "acceptanceCriteria": [
    {
      "criterion": "string - Overall acceptance criterion",
      "passed": false
    }
  ],
  "successMetrics": ["array of success metric strings"],
  "openQuestions": ["array of open question strings"]
}
```

---

## Field Definitions

### Status Values
| Status | Meaning |
|--------|---------|
| `Not Started` | No user stories or requirements completed |
| `In Progress` | At least one item completed, work ongoing |
| `Partially Compliant` | Most items complete, some remaining |
| `Compliant` | All user stories and requirements passed |

### The `passed` Field

Every trackable item gets a `passed` field:

```json
{
  "id": "US-001",
  "title": "Create logging package",
  "passed": false,  // <-- Track overall story completion
  "acceptanceCriteria": [
    {
      "criterion": "Logger writes JSON to stdout",
      "passed": false  // <-- Track individual criteria
    }
  ]
}
```

**Rules for `passed`:**
- Default: `false` for all items
- A user story's `passed` becomes `true` when ALL its acceptance criteria are `true`
- Overall `status` updates based on user story completion percentage

---

## Parsing Rules

### User Stories

Look for patterns like:
```markdown
### US-001: Title Here
**Description:** As a [user], I want [feature] so that [benefit].

**Acceptance Criteria:**
- [ ] First criterion
- [ ] Second criterion
```

Extract:
- `id`: From heading (e.g., "US-001")
- `title`: Text after the ID
- `description`: The "As a..." statement
- `acceptanceCriteria`: Each checkbox item

### Functional Requirements

Look for patterns like:
```markdown
- FR-1: Description of the requirement
- FR-2: Another requirement
```

Or:
```markdown
| FR-1 | Description |
```

### Tables

Convert markdown tables to arrays of objects:

```markdown
| Requirement | Description |
|-------------|-------------|
| Config | Environment-based settings |
```

Becomes:
```json
[
  { "requirement": "Config", "description": "Environment-based settings", "passed": false }
]
```

---

## Conversion Process

### Step 1: Identify PRD File

```
User: convert prd to json for pyroscope
```

Search for:
1. `/PRD/pyroscope*.md`
2. `/tasks/prd-pyroscope*.md`
3. Ask user to specify if multiple matches

### Step 2: Parse Sections

Extract these sections from the markdown:
- Title (first H1)
- Introduction/Overview
- Goals
- User Stories (with acceptance criteria)
- Functional Requirements
- Non-Goals
- Technical Considerations
- Success Metrics
- Open Questions

### Step 3: Generate JSON

1. Create the JSON structure
2. Set all `passed` fields to `false`
3. Set `status` to "Not Started"
4. Add metadata (`createdAt`, `source`)

### Step 4: Save File

- **Location:** `/tasks/`
- **Filename:** `[prd-name].json` (match PRD name, kebab-case)
- Report the output path to user

---

## Example Conversion

### Input PRD (excerpt):

```markdown
# PRD: Pyroscope End-to-End Implementation

## Overview
Complete Pyroscope integration with proper configuration...

## Goals
- Production-ready configuration
- Grafana integration

## User Stories

### US-001: Configuration Improvements
**Description:** As a developer, I want environment-based Pyroscope configuration so that settings can change per environment.

**Acceptance Criteria:**
- [ ] Server address configurable via PYROSCOPE_SERVER_ADDRESS
- [ ] Application name configurable via PYROSCOPE_APPLICATION_NAME
- [ ] go test ./... passes

## Functional Requirements

- FR-1: Create configuration struct with environment variable support
- FR-2: Update SetupProfiling() to use configuration
```

### Output JSON:

```json
{
  "title": "Pyroscope End-to-End Implementation",
  "priority": "Medium",
  "status": "Not Started",
  "source": "/PRD/pyroscope-and-load-testing.md",
  "createdAt": "2024-01-15T10:00:00Z",
  "updatedAt": "2024-01-15T10:00:00Z",
  "overview": {
    "description": "Complete Pyroscope integration with proper configuration...",
    "goals": [
      "Production-ready configuration",
      "Grafana integration"
    ]
  },
  "userStories": [
    {
      "id": "US-001",
      "title": "Configuration Improvements",
      "description": "As a developer, I want environment-based Pyroscope configuration so that settings can change per environment.",
      "passed": false,
      "acceptanceCriteria": [
        {
          "criterion": "Server address configurable via PYROSCOPE_SERVER_ADDRESS",
          "passed": false
        },
        {
          "criterion": "Application name configurable via PYROSCOPE_APPLICATION_NAME",
          "passed": false
        },
        {
          "criterion": "go test ./... passes",
          "passed": false
        }
      ]
    }
  ],
  "functionalRequirements": [
    {
      "id": "FR-1",
      "description": "Create configuration struct with environment variable support",
      "passed": false
    },
    {
      "id": "FR-2",
      "description": "Update SetupProfiling() to use configuration",
      "passed": false
    }
  ],
  "nonGoals": [],
  "technicalConsiderations": [],
  "acceptanceCriteria": [],
  "successMetrics": [],
  "openQuestions": []
}
```

---

## Updating Progress

When working through tasks, update the JSON file:

### Mark Acceptance Criterion Complete:
```json
{
  "criterion": "Server address configurable via PYROSCOPE_SERVER_ADDRESS",
  "passed": true  // Changed from false
}
```

### Mark User Story Complete:
When all acceptance criteria are `passed: true`:
```json
{
  "id": "US-001",
  "passed": true,  // Auto-set when all criteria pass
  "acceptanceCriteria": [
    { "criterion": "...", "passed": true },
    { "criterion": "...", "passed": true }
  ]
}
```

### Update Overall Status:
- 0% stories passed → "Not Started"
- 1-49% stories passed → "In Progress"
- 50-99% stories passed → "Partially Compliant"
- 100% stories passed → "Compliant"

---

## Commands

After conversion, suggest these follow-up actions:

```
Task file created: /tasks/pyroscope-and-load-testing.json

Next steps:
1. Review the generated tasks
2. Start implementing US-001
3. Update passed fields as you complete criteria
4. Run: cat /tasks/pyroscope-and-load-testing.json | jq '.userStories[] | select(.passed == false)'
   to see remaining work
```

---

## Checklist

Before saving the JSON:

- [ ] All user stories extracted with IDs
- [ ] All acceptance criteria captured per story
- [ ] All functional requirements extracted
- [ ] `passed: false` set on all trackable items
- [ ] `status` set to "Not Started"
- [ ] `source` points to original PRD
- [ ] Timestamps included
- [ ] Valid JSON (parseable by `jq`)
- [ ] Saved to `/tasks/[name].json`
