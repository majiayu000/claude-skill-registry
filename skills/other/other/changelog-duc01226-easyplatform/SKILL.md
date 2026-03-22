---
name: changelog
version: 1.1.0
description: '[Documentation] Generate or update changelog entries. Use for release changelogs, version history, and change tracking across any project.'
triggers:
    - changelog
    - update changelog
    - add changelog
    - log changes

allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Task, TaskCreate
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ask user whether to skip.

> **External Memory:** For complex or lengthy work (research, analysis, scan, review), write intermediate findings and final results to a report file in `plans/reports/` — prevents context loss and serves as deliverable.

> **Evidence Gate:** MANDATORY IMPORTANT MUST — every claim, finding, and recommendation requires `file:line` proof or traced evidence with confidence percentage (>80% to act, <80% must verify first).

## Quick Summary

**Goal:** Generate business-focused changelog entries by systematically reviewing file changes.

**Workflow:**

1. **Gather Changes** — Get changed files via `git diff` (PR, commit, or range mode)
2. **Create Temp Notes** — Build categorized review notes (Added/Changed/Fixed/etc.)
3. **Review Each File** — Read diffs, identify business impact, categorize changes
4. **Generate Entry** — Write Keep-a-Changelog formatted entry under `[Unreleased]`
5. **Cleanup** — Delete temp notes file

**Key Rules:**

- Use business-focused language, not technical jargon (e.g., "Added pipeline management" not "Added PipelineController.cs")
- Group related changes by module/feature, not by file
- Always insert under the `[Unreleased]` section; create it if missing

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

# Changelog Skill

Generate business-focused changelog entries by systematically reviewing file changes.

## Pre-Execution Checklist

1. **Find existing CHANGELOG.md location**
    - Check root: `./CHANGELOG.md` (preferred)
    - Fallback: `./docs/CHANGELOG.md`
    - If not found: Create at root

2. **Read current changelog** to understand format and last entries

## Workflow

### Step 1: Gather Changes

Determine change scope based on mode:

```bash
# PR/Branch-based (default)
git diff origin/develop...HEAD --name-only

# Commit-based
git show {commit} --name-only

# Range-based
git diff {from}..{to} --name-only
```

### Step 2: Create Temp Notes File

Create `.ai/workspace/changelog-notes-{YYMMDD-HHMM}.md`:

```markdown
# Changelog Review Notes - {date}

## Files Changed

- [ ] file1.ts -
- [ ] file2.cs -

## Categories

### Added (new features)

-

### Changed (modifications to existing)

-

### Fixed (bug fixes)

-

### Deprecated

-

### Removed

-

### Security

-

## Business Summary

<!-- What does this mean for users? -->
```

### Step 3: Systematic File Review

For each changed file:

1. Read file or diff
2. Identify **business impact** (not just technical change)
3. Check box and note in temp file
4. Categorize into appropriate section

**Business Focus Guidelines**:

| Technical (Avoid)               | Business-Focused (Use)                       |
| ------------------------------- | -------------------------------------------- |
| Added `StageCategory` enum      | Added stage categories for pipeline tracking |
| Created `PipelineController.cs` | Added API endpoints for pipeline management  |
| Fixed null reference in GetById | Fixed pipeline loading error                 |
| Added migration file            | Database schema updated for new features     |

### Step 4: Holistic Review

Read temp notes file completely. Ask:

- What's the main feature/fix?
- Who benefits and how?
- What can users now do that they couldn't before?

### Step 5: Generate Changelog Entry

Format (Keep a Changelog):

```markdown
## [Unreleased]

### {Module}: {Feature Title}

**Feature/Fix**: {One-line business description}

#### Added

- {Business-focused item}

#### Changed

- {What behavior changed}

#### Fixed

- {What issue was resolved}
```

### Step 6: Update Changelog

1. Read existing CHANGELOG.md
2. Insert new entry under `[Unreleased]` section
3. If no `[Unreleased]` section, create it after header
4. Preserve existing entries

### Step 7: Cleanup

Delete temp notes file: `.ai/workspace/changelog-notes-*.md`

## Grouping Strategy

Group related changes by module/feature:

```markdown
### Your Service: Hiring Process Management

**Feature**: Customizable hiring process/pipeline management.

#### Added

**Backend**:

- Entities: Pipeline, Stage, PipelineStage
- Controllers: PipelineController, StageController
- Commands: SavePipelineCommand, DeletePipelineCommand

**Frontend**:

- Pages: hiring-process-page
- Components: pipeline-filter, pipeline-stage-display
```

## Anti-Patterns

1. ❌ Creating new changelog in docs/ when root exists
2. ❌ Skipping file review (leads to missed changes)
3. ❌ Technical jargon without business context
4. ❌ Forgetting to delete temp notes file
5. ❌ Not using [Unreleased] section
6. ❌ Listing every file instead of grouping by feature

## Examples

### Good Entry

```markdown
### Your Service: Hiring Process Management

**Feature**: Customizable hiring process/pipeline management for recruitment workflows.

#### Added

- Drag-and-drop pipeline stage builder with default templates
- Stage categories (Sourced, Applied, Interviewing, Offered, Hired, Rejected)
- Pipeline duplication for quick setup
- Multi-language stage names (EN/VI)

#### Changed

- Candidate cards now show current pipeline stage
- Job creation wizard includes pipeline selection
```

### Bad Entry (Too Technical)

```markdown
### Pipeline Changes

#### Added

- Pipeline.cs entity
- StageCategory enum
- PipelineController
- SavePipelineCommand
- 20251216000000_MigrateDefaultStages migration
```

## Reference

See `references/keep-a-changelog-format.md` for format specification.

## Related

- `documentation`
- `release-notes`
- `commit`

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements

---

## Workflow Recommendation

> **IMPORTANT MUST:** If you are NOT already in a workflow, use `AskUserQuestion` to ask the user:
>
> 1. **Activate `feature` workflow** (Recommended) — scout → investigate → plan → cook → review → changelog
> 2. **Execute `/changelog` directly** — run this skill standalone

---

## Next Steps

**MANDATORY IMPORTANT MUST** after completing this skill, use `AskUserQuestion` to recommend:

- **"/test (Recommended)"** — Run tests after changelog update
- **"/docs-update"** — Update docs if needed
- **"Skip, continue manually"** — user decides

## Closing Reminders

**MANDATORY IMPORTANT MUST** break work into small todo tasks using `TaskCreate` BEFORE starting.
**MANDATORY IMPORTANT MUST** validate decisions with user via `AskUserQuestion` — never auto-decide.
**MANDATORY IMPORTANT MUST** add a final review todo task to verify work quality.
