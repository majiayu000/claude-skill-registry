---
name: sync-patterns
description: Compare specs with implementation state, update spec status, and generate sync reports. Use when syncing specs, checking implementation status, marking tasks complete, generating sync reports, or when user mentions spec sync, status updates, or implementation tracking.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# sync-patterns

Reusable patterns and scripts for syncing specification documents with implementation state. This skill provides tools to compare what's documented in specs vs what's implemented in code, update spec status markers, identify completed tasks, and generate comprehensive sync reports.

## When to Use This Skill

Use this skill when:
- Syncing spec documents with actual implementation progress
- Checking if features in specs have been implemented
- Marking specs or tasks as complete/in-progress
- Generating reports of sync status across the project
- Validating implementation coverage vs specifications
- Identifying completed work that hasn't been marked in specs

## Core Capabilities

### 1. Compare Specs vs Code

**Script:** `scripts/compare-specs-vs-code.sh`

Compares specification requirements against actual code implementation.

**Usage:**
```bash
bash ~/.claude/plugins/marketplaces/dev-lifecycle-marketplace/plugins/iterate/skills/sync-patterns/scripts/compare-specs-vs-code.sh <spec-file> [code-directory]
```

**What it does:**
- Extracts requirements/tasks from spec file
- Searches codebase for implementation evidence
- Reports on implemented vs not-yet-implemented features
- Generates comparison summary

**Returns:**
- List of implemented features (with file locations)
- List of pending features
- Implementation coverage percentage

### 2. Update Spec Status

**Script:** `scripts/update-spec-status.sh`

Updates status markers in specification documents.

**Usage:**
```bash
bash ~/.claude/plugins/marketplaces/dev-lifecycle-marketplace/plugins/iterate/skills/sync-patterns/scripts/update-spec-status.sh <spec-file> <status>
```

**Supported statuses:**
- `complete` - Mark entire spec as completed
- `in-progress` - Mark spec as currently being worked on
- `pending` - Mark spec as not yet started
- `blocked` - Mark spec as blocked (requires reason)

**What it does:**
- Updates frontmatter status field
- Adds timestamp of status change
- Maintains status history
- Validates status transitions

### 3. Find Completed Tasks

**Script:** `scripts/find-completed-tasks.sh`

Identifies tasks that are completed in code but not marked complete in specs.

**Usage:**
```bash
bash ~/.claude/plugins/marketplaces/dev-lifecycle-marketplace/plugins/iterate/skills/sync-patterns/scripts/find-completed-tasks.sh [spec-directory] [code-directory]
```

**What it does:**
- Scans spec files for tasks marked as incomplete
- Searches codebase for evidence of completion
- Identifies completion markers (tests, implementations, docs)
- Reports on unmarked completed work

**Completion evidence includes:**
- Passing test files
- Implemented functions/classes
- Configuration files
- Documentation updates

### 4. Generate Sync Report

**Script:** `scripts/generate-sync-report.sh`

Creates comprehensive sync report for entire project or specific spec.

**Usage:**
```bash
bash ~/.claude/plugins/marketplaces/dev-lifecycle-marketplace/plugins/iterate/skills/sync-patterns/scripts/generate-sync-report.sh [spec-file-or-directory] [output-file]
```

**Report includes:**
- Overall sync percentage
- List of completed features
- List of in-progress features
- List of pending features
- Discrepancies (code without spec, spec without code)
- Recommendations for next steps

**Output formats:**
- Markdown report (default)
- JSON data structure (use `--format=json`)
- HTML dashboard (use `--format=html`)

## Templates

### Spec Status Update Template

**Location:** `templates/spec-status-update.template.md`

Template for updating spec status with proper formatting and metadata.

**Variables:**
- `{{SPEC_NAME}}` - Name of specification
- `{{STATUS}}` - New status (complete/in-progress/pending/blocked)
- `{{TIMESTAMP}}` - ISO 8601 timestamp
- `{{REASON}}` - Reason for status change (optional)
- `{{UPDATED_BY}}` - Who updated (agent/user name)

### Sync Report Template

**Location:** `templates/sync-report.template.md`

Template for comprehensive sync reports.

**Variables:**
- `{{PROJECT_NAME}}` - Project name
- `{{REPORT_DATE}}` - Report generation date
- `{{SYNC_PERCENTAGE}}` - Overall sync percentage
- `{{COMPLETED_COUNT}}` - Number of completed items
- `{{IN_PROGRESS_COUNT}}` - Number of in-progress items
- `{{PENDING_COUNT}}` - Number of pending items
- `{{COMPLETED_ITEMS}}` - List of completed items
- `{{IN_PROGRESS_ITEMS}}` - List of in-progress items
- `{{PENDING_ITEMS}}` - List of pending items
- `{{DISCREPANCIES}}` - List of discrepancies
- `{{RECOMMENDATIONS}}` - Next steps

## Examples

### Example 1: Complete Sync Workflow

See `examples/sync-workflow.md` for step-by-step guide on performing a complete sync.

**High-level steps:**
1. Compare specs with code to identify status
2. Update spec files with current status
3. Find completed tasks not yet marked
4. Generate comprehensive sync report
5. Review report and take action

### Example 2: Status Markers

See `examples/status-markers.md` for examples of completion markers in code.

**Common markers:**
- Test files: `describe('feature')`, `it('should work')`
- Implementation: Function definitions, class exports
- Configuration: Config files, environment variables
- Documentation: README updates, inline comments

## Integration with Agents

The sync-analyzer agent uses these scripts to:
1. Analyze current sync state
2. Identify discrepancies
3. Generate recommendations
4. Update documentation

**Example agent usage:**
```markdown
Phase 1: Analyze Sync State

Run comparison script:
Bash: bash ~/.claude/plugins/marketplaces/dev-lifecycle-marketplace/plugins/iterate/skills/sync-patterns/scripts/compare-specs-vs-code.sh specs/feature.md src/

Phase 2: Update Status

Mark completed items:
Bash: bash ~/.claude/plugins/marketplaces/dev-lifecycle-marketplace/plugins/iterate/skills/sync-patterns/scripts/update-spec-status.sh specs/feature.md complete

Phase 3: Generate Report

Create sync report:
Bash: bash ~/.claude/plugins/marketplaces/dev-lifecycle-marketplace/plugins/iterate/skills/sync-patterns/scripts/generate-sync-report.sh specs/ sync-report.md
```

## Best Practices

### Status Management

1. **Always timestamp status changes**
   - Include ISO 8601 timestamps
   - Maintain status history in spec frontmatter

2. **Validate status transitions**
   - pending → in-progress → complete (normal flow)
   - blocked → in-progress (after unblocking)
   - complete → in-progress (if rework needed)

3. **Document blocking reasons**
   - If status is "blocked", always include reason
   - Reference blocking issue/ticket if applicable

### Sync Frequency

1. **Regular syncs**
   - Sync at end of each feature implementation
   - Weekly sync for long-running projects
   - Before milestone releases

2. **Automated triggers**
   - After significant code changes
   - Before pull request creation
   - During CI/CD pipeline

### Report Distribution

1. **Share with team**
   - Include in project documentation
   - Add to PR descriptions
   - Share in status meetings

2. **Track over time**
   - Keep historical sync reports
   - Monitor sync percentage trends
   - Identify chronic discrepancies

## Script Error Handling

All scripts implement consistent error handling:

```bash
# Exit codes
0 - Success
1 - Invalid arguments
2 - File not found
3 - Invalid status
4 - Parsing error
5 - Write permission error
```

**Error output:**
- Errors written to stderr
- Descriptive error messages
- Suggestions for resolution

## Dependencies

**Required:**
- bash 4.0+
- grep (with -P flag for PCRE)
- find
- sed

**Optional (enhanced features):**
- jq (for JSON output)
- pandoc (for HTML output)
- git (for commit history integration)

## Progressive Disclosure

**Basic usage:** Use scripts directly for simple tasks

**Advanced usage:** Chain scripts together for complex workflows

**Full integration:** Integrate with agents and commands for automated syncing

---

**Location:** `plugins/iterate/skills/sync-patterns/`
**Used by:** sync-analyzer agent, /iterate:sync command
**Dependencies:** Bash, standard UNIX tools
