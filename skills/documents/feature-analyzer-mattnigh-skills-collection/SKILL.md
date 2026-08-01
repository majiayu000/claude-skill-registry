---
name: feature-analyzer-mattnigh-skills-collection
description: 'Comprehensive feature artifact analysis for loading and understanding
  complete feature context. Use when needing to: (1) Load all feature documentation
  before implementation, (2) Build mental model of'
---

---
name: feature-analyzer
description: Comprehensive feature artifact analysis for loading and understanding complete feature context. Use when needing to: (1) Load all feature documentation before implementation, (2) Build mental model of feature requirements and architecture, (3) Prepare context for downstream operations like checklist generation or task execution, (4) Analyze feature completeness and artifact availability. Triggers on: analyze feature, load feature context, prepare feature, check feature prerequisites, understand feature scope.
allowed-tools: Read, Write, Bash (*)
---

# Feature Analyzer

Load and analyze all feature artifacts to build comprehensive understanding for downstream operations.

## Workflow Overview

1. **Scan** - Check artifact availability
2. **Load** - Read all feature documents
3. **Build** - Construct complete mental model
4. **Confirm** - Ready for operations

## Step 1: Scan Feature Directory

Run prerequisites scanner to identify available artifacts:

```bash
.claude/skills/feature-analyzer/scripts/check-prerequisites.sh <feature-directory>
```

Scanner checks for:
- Core artifacts: spec.md, ux.md, plan.md, tasks.md
- Data artifacts: data-model.md, contracts/
- Support artifacts: research.md, setup.md

Outputs JSON with AVAILABLE and MISSING arrays. Exits with error if core files missing.

## Step 2: Load Feature Artifacts

Read all available artifacts in priority order:

### Core Documents (Required)
- `spec.md` - Requirements (FR-XXX), user stories, acceptance criteria
- `ux.md` - User flows, interactions, states, errors
- `plan.md` - Architecture, components, technology stack
- `tasks.md` - Implementation phases, TDD cycles, execution order

### Data & Contracts
- `data-model.md` - Entities, validation, state machines
- `contracts/` - APIs, messages, schemas
  - openapi.yaml
  - contracts.md

### Supporting Documents
- `research.md` - Technical decisions, rationale
- `setup.md` - Environment, dependencies, commands

## Step 3: Build Mental Model

Extract and internalize from each artifact:

**From spec.md:**
- Main journey and goal
- All requirements with IDs
- Test scenarios
- Edge cases and constraints

**From ux.md:**
- Complete flow with triggers
- States and transitions
- Error handling patterns

**From plan.md:**
- Code structure (A/B/C/D patterns)
- Requirement→Component mapping
- Technical constraints

**From tasks.md:**
- Implementation sequence
- TDD coverage targets
- File creation paths
- Dependencies

**From data-model.md:**
- Field definitions and rules
- Constants and limits
- Entity relationships

**From contracts:**
- Endpoint specifications
- Message formats
- Protocol definitions

## Step 4: Confirm Readiness

Output minimal confirmation:
```
✅ Feature context loaded: [feature-name]
   Available: [list of loaded artifacts]
   Ready for: implementation | checklist | queries
```

## Error Handling

- **Missing core files**: Stop and report specific missing file
- **Malformed content**: Report file and parsing error
- **Access denied**: Report permission issue

## Usage Notes

This skill prepares context for:
- Task execution (implementation from tasks.md)
- Checklist generation (requirements validation)
- Architecture queries
- Technical guidance

Context remains in memory for entire conversation.