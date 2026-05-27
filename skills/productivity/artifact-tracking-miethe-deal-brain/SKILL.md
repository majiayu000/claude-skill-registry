---
name: artifact-tracking
description: "Use this skill when creating, updating, or querying AI-optimized tracking artifacts (progress files, context notes, bug fixes, observation logs) in YAML+Markdown hybrid format for 95% token reduction. Invoke for: creating phase progress tracking, updating task status and blockers, querying pending work across phases, generating session handoff reports, validating artifact completeness, or migrating existing markdown files to hybrid format. Provides three embedded agents (artifact-tracker, artifact-query, artifact-validator) plus Python migration tools for efficient multi-phase project tracking."
---

# Artifact Tracking Skill

Create, update, query, and validate AI-optimized tracking artifacts with 95% token efficiency.

## Why This Skill

Traditional tracking artifacts (pure markdown) waste tokens:
- **Querying "all pending tasks"**: 92KB file returns everything (98.7% waste)
- **Getting blockers**: 160KB context for 800B answer (99.5% waste)
- **Session handoff**: Must read entire file every time

This skill provides a **hybrid YAML+Markdown format** optimized for AI agent consumption:
- **Field-level queries**: Get exactly what you need (1KB instead of 92KB)
- **Structured metadata**: Programmatically filter tasks by status, agent, priority
- **Efficient updates**: Change one field without rewriting entire file
- **Token savings**: 95-99% reduction in token usage

## When to Use This Skill

### Create Progress Tracking
Starting a new phase of implementation? Create a phase progress file with structured task list, success criteria, and blockers.

**Example**: "Create Phase 2 progress tracking for authentication-overhaul PRD"

### Update Task Status
Need to mark a task complete, move it to in-progress, or block it? Surgical field-level updates without full-file rewrites.

**Example**: "Update TASK-003 status to 'in_progress' and add blocker reference"

### Query Pending Work
Need to find all pending tasks for a specific agent? Or all blockers across phases? Query with filters.

**Example**: "Show all blocked tasks in advanced-editing-v2 phases 1-3"

### Record Implementation Context
Discovered important technical decisions or gotchas? Document them in structured context files for future reference.

**Example**: "Record Phase 1 implementation decisions and integration patterns in context file"

### Generate Session Handoff
Handing off work to another agent or session? Get a concise summary of pending tasks, blockers, and next actions.

**Example**: "Generate session handoff for frontend-developer to continue Phase 3"

### Validate Artifact Quality
Before phase completion, verify tracking files are complete, consistent, and accurate.

**Example**: "Validate Phase 2 progress file for schema compliance and metric accuracy"

### Migrate Existing Artifacts
Have old markdown progress files? Convert them to hybrid format with Python migration tool.

**Example**: "Migrate legacy progress files to hybrid YAML+Markdown format"

## Quick Start

### 1. Create Progress Tracking (Most Common)

```markdown
Task("artifact-tracker", "Create progress tracking for Phase 2 of listings-enhancements-v3 PRD. Include 5 main tasks: implement search API, add filtering UI, optimize database query, write tests, and documentation. Mark all as pending status.")
```

This will create `.claude/progress/listings-enhancements-v3/phase-2-progress.md` with structured YAML metadata and task list.

### 2. Update Task Status

```markdown
Task("artifact-tracker", "Update phase-2-progress.md for advanced-editing-v2: Mark TASK-1.5 (React modal optimization) as 'in_progress' and update overall progress to 40%")
```

YAML metadata is updated surgically without touching task descriptions or other sections.

### 3. Query Pending Tasks

```markdown
Task("artifact-query", "Find all blocked tasks in blocks-v2-implementation phases 1-3. Show task ID, description, blocker reason, and assigned agent")
```

Returns structured results filtered by status across multiple files.

### 4. Generate Session Handoff

```markdown
Task("artifact-query", "Generate session handoff for ui-engineer-enhanced continuing Phase 4 of advanced-editing-v2. Include pending tasks, current blockers, next session agenda, and architecture context")
```

Concise summary with all info needed to continue work.

### 5. Validate Completeness

```markdown
Task("artifact-validator", "Validate Phase 1 and Phase 2 progress files for prompt-card-v1. Check schema compliance, metric accuracy, and link validity")
```

Automated quality checks before phase completion.

## Core Workflows

### Workflow: Create Progress Tracking

**When**: Starting implementation of a new phase from PRD

**Steps**:
1. Delegate to `artifact-tracker` agent
2. Provide: PRD name, phase number, phase title, initial task list from implementation plan
3. Agent creates file at `.claude/progress/[prd-name]/phase-[N]-progress.md`
4. File includes YAML frontmatter (metadata) + markdown body (narrative + task tables)
5. Progress defaults to 0%, all tasks pending
6. Ready for task updates as work progresses

**Result**: Structured file that can be queried and updated efficiently across sessions

### Workflow: Update Task Status

**When**: Task completes, enters work, gets blocked, or becomes at-risk

**Steps**:
1. Delegate to `artifact-tracker` agent
2. Provide: file location, task ID, new status, any notes
3. Agent updates YAML frontmatter (task counts, progress percentage, updated timestamp)
4. Agent updates task in markdown table (status, notes)
5. One surgical update, no full-file rewrite
6. File remains queryable and efficient

**Result**: Minimal token usage (~1KB update vs ~25KB full-file approach)

### Workflow: Query Work Status

**When**: Need to find tasks by criteria (agent, status, priority, blocker status)

**Steps**:
1. Delegate to `artifact-query` agent
2. Provide: scope (one phase or all), filter criteria (status, agent, priority, blocking/blocked)
3. Agent loads relevant progress files
4. Agent extracts YAML and applies filters
5. Agent returns formatted results with task locations
6. Results are concise and actionable

**Result**: Seconds to answer queries that would take minutes reading full files

### Workflow: Validate Before Completion

**When**: Phase nearing completion, want to ensure tracking is accurate

**Steps**:
1. Delegate to `artifact-validator` agent
2. Provide: phase number and PRD name
3. Agent validates: YAML schema, field types, required fields, metric calculations, link integrity
4. Agent identifies inconsistencies or missing data
5. Agent suggests fixes or generates automated cleanup
6. You review and approve

**Result**: High-confidence phase completion tracking

### Workflow: Migrate Legacy Files

**When**: Have old markdown progress files to update to new format

**Steps**:
1. Run Python migration script: `python scripts/convert_to_hybrid.py path/to/old/file.md`
2. Script parses existing markdown structure
3. Script generates YAML frontmatter from content
4. Script preserves markdown body and adds task tables if needed
5. Output written to new hybrid format
6. You review and commit

**Result**: Bulk migration without manual rewriting

## Embedded Agents

### artifact-tracker (Haiku 4.5)
Creates and updates progress files with field-level precision. Specializes in:
- Creating new progress tracking files from templates
- Updating task status (pending → in_progress → completed)
- Recording blockers and dependencies
- Documenting implementation decisions in context files
- Surgical field updates without full-file rewrites

Use when: Creating or updating tracking files, recording decisions

### artifact-query (Haiku 4.5)
Queries and synthesizes tracking artifacts efficiently. Specializes in:
- Finding tasks by status, agent, priority, phase, or custom criteria
- Identifying and aggregating blockers across phases
- Generating session handoff reports
- Synthesizing implementation decisions from context files
- Calculating progress metrics across phases

Use when: Finding information, generating reports, creating handoffs

### artifact-validator (Sonnet 4.5)
Validates and maintains artifact quality. Specializes in:
- Schema validation (YAML structure, required fields, data types)
- Completeness checks (all tasks tracked, metrics accurate)
- Quality assurance (token efficiency, link integrity)
- Cleanup and archiving
- Consistency enforcement

Use when: Validating files, checking quality, finding/fixing issues

## Format Reference

Tracking artifacts use **hybrid YAML+Markdown format**:

```yaml
---
# Machine-readable metadata (YAML frontmatter)
type: progress
prd: "listings-enhancements-v3"
phase: 2
title: "Search and Filtering Implementation"
status: in_progress
progress: 45
total_tasks: 8
completed_tasks: 3
in_progress_tasks: 2
blocked_tasks: 1
created: 2025-11-15
updated: 2025-11-17
owners: ["ui-engineer-enhanced"]
contributors: ["backend-engineer"]
blockers:
  - id: "BLOCKER-001"
    title: "Missing API endpoint"
    severity: "critical"
    blocking: ["TASK-2.3", "TASK-2.4"]
    resolution: "Awaiting backend-engineer implementation"
---

# Listings Enhancements V3 - Phase 2: Search and Filtering

**Phase**: 2 of 4
**Status**: In Progress (45% complete)
**Owner**: ui-engineer-enhanced

## Tasks

| ID | Task | Status | Agent | Notes |
|----|------|--------|-------|-------|
| TASK-2.1 | API search endpoint | ✓ | backend-engineer | Complete |
| TASK-2.2 | Search UI component | 🔄 | ui-engineer-enhanced | In review |
| TASK-2.3 | Filter dropdown | 🚫 | ui-engineer-enhanced | Blocked by BLOCKER-001 |
| ... | ... | ... | ... | ... |

## Architecture Context

[Narrative markdown content about implementation decisions, patterns, gotchas]

---

**Key**: YAML frontmatter is machine-readable metadata. Markdown body is human-readable narrative.
```

See `./format-specification.md` for complete format documentation with all YAML fields, value types, and validation rules.

## Directory Structure

Progress and context tracking follows ONE-per-phase rule:

```
.claude/
├── progress/
│   └── [prd-name]/
│       ├── phase-1-progress.md     # ONE per phase
│       ├── phase-2-progress.md
│       └── phase-3-progress.md
│
└── worknotes/
    ├── [prd-name]/
    │   ├── phase-1-context.md      # ONE per phase
    │   ├── phase-2-context.md
    │   └── phase-3-context.md
    │
    ├── fixes/
    │   └── bug-fixes-tracking-11-25.md  # Monthly tracking
    │
    └── observations/
        └── observation-log-11-25.md     # Monthly observations
```

## Using Scripts

Python utilities in `./scripts/` for programmatic operations:

### convert_to_hybrid.py
Migrate old markdown files to hybrid YAML+Markdown format:

```bash
python scripts/convert_to_hybrid.py /path/to/old/progress.md
# Output: progress_hybrid.md (converted format)
```

### validate_artifact.py
Validate tracking files against schema:

```bash
python scripts/validate_artifact.py /path/to/progress.md
# Output: validation report with issues and recommendations
```

### query_artifacts.py
Query tracking files programmatically:

```bash
python scripts/query_artifacts.py \
  --prd "listings-enhancements-v3" \
  --status "blocked" \
  --phase 2
# Output: JSON of matching tasks
```

### migrate_all.py
Bulk migration of all legacy files:

```bash
python scripts/migrate_all.py /path/to/legacy/dir
# Output: Migrated files in hybrid format
```

See `./scripts/README.md` for complete documentation.

## Token Efficiency Metrics

### Example: Query All Pending Tasks

**Traditional Approach**:
- Read full phase-1-progress.md: 160KB
- Read full phase-2-progress.md: 140KB
- Read full phase-3-progress.md: 180KB
- Total: 480KB (~144,000 tokens)
- Return all content, grep for "pending"

**Artifact-Tracking Approach**:
- Query YAML metadata: 3KB (metadata only)
- Load YAML arrays of pending tasks: 2KB
- Format results: 1KB
- Total: 6KB (~1,800 tokens)
- Direct answer to query

**Savings**: 474KB (~142,200 tokens) **98.75% reduction**

### Example: Get Session Handoff

**Traditional Approach**:
- Read 3 progress files: 480KB
- Read 3 context files: 340KB
- Manual synthesis of key info
- Total: 820KB (~246,000 tokens)

**Artifact-Tracking Approach**:
- Query pending tasks: 2KB
- Query blockers: 1KB
- Load context summary fields: 3KB
- Query next session agenda: 1KB
- Total: 7KB (~2,100 tokens)
- Structured handoff ready to use

**Savings**: 813KB (~243,900 tokens) **97.1% reduction**

## Examples

### Example 1: Create Phase Progress

```markdown
Task("artifact-tracker", "Create Phase 1 progress tracking for blocks-v2-implementation PRD. Phase title: 'Core Blocks Model Implementation'. Include these tasks: implement Block model schema, add database migrations, create block repository layer, add CRUD endpoints, write integration tests. All tasks start as pending with medium priority. Assign to backend-engineer.")
```

Result: `.claude/progress/blocks-v2-implementation/phase-1-progress.md` created with structured YAML metadata and task list.

### Example 2: Update Progress

```markdown
Task("artifact-tracker", "Update phase-1-progress.md for advanced-editing-v2: Mark TASK-1.1 (Modal component skeleton) as complete. Mark TASK-1.2 (Form inputs integration) as in_progress. Update overall progress from 20% to 35%. Add note: 'UI skeleton complete, working on form integration'")
```

Result: YAML metadata updated surgically, progress metrics recalculated.

### Example 3: Query Blockers

```markdown
Task("artifact-query", "Find all critical and high-severity blockers across all phases of prompt-card-v1 PRD. Show blocker ID, title, what tasks it's blocking, and resolution path.")
```

Result: Structured list of blockers with impact analysis.

### Example 4: Session Handoff

```markdown
Task("artifact-query", "Generate session handoff for ai-artifacts-engineer continuing work on listings-enhancements-v3. Show: current phase, pending tasks in priority order, active blockers, implementation decisions from context files, and immediate next actions for new session.")
```

Result: Concise handoff with all context needed to continue.

## Best Practices

### 1. ONE Progress File Per Phase

Never create multiple progress files for the same phase. Use a single `.claude/progress/[prd]/phase-[N]-progress.md` and update it across sessions.

### 2. Update Metadata Regularly

Keep YAML frontmatter current:
- `progress`: Update as tasks complete
- `updated`: Set when making changes
- `blockers`: Add/remove as situation changes
- `completed_tasks`, `in_progress_tasks`: Keep in sync with markdown tasks

### 3. Use Consistent Task IDs

Task IDs should follow pattern: `TASK-[PHASE].[SEQUENCE]` (e.g., `TASK-2.1`, `TASK-2.2`, `TASK-2.3`)

### 4. Link Tasks to Blockers

When a task is blocked, reference the blocker ID:
- In markdown: `Blocked by BLOCKER-001`
- In YAML `blockers.blocking` array: `["TASK-2.3", "TASK-2.4"]`

### 5. Query Before Reading Full Files

Never read entire progress files manually when querying. Use `artifact-query` agent:
- "Show all blocked tasks" → Query returns 1KB
- Reading full files → 480KB waste

### 6. Archive Completed Phases

Use `artifact-validator` to clean up after phase completion:
- Mark phase as `status: complete`
- Archive to history/ if keeping reference
- Remove from active tracking

## Reference Guides

**Complete Format Specification**: See `./format-specification.md` for all YAML fields, value types, constraints, and validation rules.

**Migration Guide**: See `./migration-guide.md` for step-by-step instructions to convert existing markdown artifacts to hybrid format.

**Query Patterns**: See `./query-patterns.md` for common query examples and efficient filter combinations.

**Template Reference**: See `./TEMPLATES-INDEX.md` for all available templates (progress, context, bug fixes, observations).

**Schema Reference**: See `./schemas/` directory for validation schemas and examples.

## Integration with Other Skills

This skill works with:

- **Documentation writer** - For permanent docs about tracking system
- **Lead PM** - For orchestrating multi-phase projects
- **Code reviewer** - For validating tracking before merge
- **Implementation planner** - For creating initial task lists

When starting a new PRD:
1. **Planner** creates implementation plan with phases and tasks
2. **artifact-tracker** creates phase progress files from plan
3. **Teams** update files as work progresses
4. **artifact-query** generates reports on progress
5. **artifact-validator** audits quality before phase completion
