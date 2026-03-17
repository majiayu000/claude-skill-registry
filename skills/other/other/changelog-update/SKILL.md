---
name: changelog-update
description: Update CHANGELOG.md [Unreleased] section with business-focused entries via systematic file review
triggers:
  - changelog update
  - update changelog
  - changelog-update
activation: user-invoked
---

# Changelog-Update Skill

Update CHANGELOG.md with business-focused entries by systematically reviewing file changes.

**Note**: For automated release notes from conventional commits, use the `release-notes` skill instead.

## When to Use

- **During development**: Document feature/fix for users before PR/merge
- **PR preparation**: Add business-focused entry to CHANGELOG.md
- **Manual documentation**: When commits don't capture full business impact

**Don't use for releases**: Use `release-notes` skill to generate versioned release docs.

## Pre-Execution Checklist

1. [ ] Find existing CHANGELOG.md location
   - Check root: `./CHANGELOG.md` (preferred)
   - Fallback: `./docs/CHANGELOG.md`
   - If not found: Create at root

2. [ ] Read current changelog to understand format and last entries

## Workflow

### Step 1: Gather Changes

Determine change scope:
- **PR-based**: `git diff origin/develop...HEAD --name-only`
- **Branch-based**: `git log origin/develop..HEAD --oneline`
- **Commit-based**: `git show {commit} --name-only`

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
2. Identify business impact (not just technical change)
3. Check box and note in temp file
4. Categorize into appropriate section

**Business Focus Guidelines**:
- ❌ "Added `StageCategory` enum"
- ✅ "Added stage categories (Sourced, Applied, Interviewing, etc.) for pipeline tracking"
- ❌ "Created `PipelineController.cs`"
- ✅ "Added API endpoints for pipeline management"

### Step 4: Holistic Review

Read temp notes file completely. Ask:
- What's the main feature/fix?
- Who benefits and how?
- What can users now do that they couldn't before?

### Step 5: Generate Changelog Entry

Format (Keep a Changelog):

```markdown
## [Unreleased]

### {Feature/Module Name}: {Feature Title}

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
2. Insert new entry under [Unreleased] section
3. If no [Unreleased] section, create it after the header

### Step 7: Cleanup

Delete temp notes file: `.ai/workspace/changelog-notes-*.md`

## Examples

### Good Entry
```markdown
### bravoTALENTS: Hiring Process Management

**Feature**: Customizable hiring process/pipeline management for recruitment workflows.

#### Added
- Drag-and-drop pipeline stage builder with default templates
- Stage categories (Sourced, Applied, Interviewing, Offered, Hired, Rejected)
- Pipeline duplication for quick setup
- Multi-language stage names (EN/VI)
```

### Bad Entry (Too Technical)
```markdown
### Pipeline Changes

#### Added
- Pipeline.cs entity
- StageCategory enum
- PipelineController
- SavePipelineCommand
```

## Anti-Patterns

1. ❌ Creating new changelog in docs/ when root exists
2. ❌ Skipping file review (leads to missed changes)
3. ❌ Technical jargon without business context
4. ❌ Forgetting to delete temp notes file
5. ❌ Not using [Unreleased] section
