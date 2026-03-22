---
name: release-notes
version: 1.0.0
description: '[Git] Generate professional release notes from git commits between two refs with automated categorization. Use when creating release notes from git history.'

allowed-tools: NONE
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ask user whether to skip.

## Quick Summary

**Goal:** Generate professional release notes from git commits with automated categorization, service detection, and validation.

**Workflow:**

1. **Parse Commits** — `parse-commits.cjs <base> <head>` extracts structured data from git
2. **Categorize** — Pipe through `categorize-commits.cjs` for user-facing vs internal sections
3. **Render** — `render-template.cjs --version vX.Y.Z` generates markdown with Summary, What's New, Improvements, Bug Fixes, Breaking Changes, Technical Details

**Key Rules:**

- **Pipeline**: parse → categorize → render → validate → transform
- **Advanced**: Service detection, breaking change analysis, PR metadata, contributor stats, version bumping
- **Human Review**: Generated notes are Draft status, require review/enhance/approve before publish
- **Validation**: `validate-notes.cjs` scores against quality rules (100 points)

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

# Release Notes Generation Skill

Generate professional release notes from git commits between two refs with automated categorization.

## Invocation

```
/release-notes [base] [head] [--version vX.Y.Z] [--output path]
```

**Examples:**

```bash
# Generate release notes for commits since last tag
/release-notes v1.0.0 HEAD --version v1.1.0

# Compare branches
/release-notes main feature/new-auth --version v2.0.0-beta

# Output to specific file
/release-notes v1.0.0 HEAD --version v1.1.0 --output docs/release-notes/250111-v1.1.0.md
```

## Workflow

### Step 1: Parse Commits

Execute the commit parser to extract structured data from git history:

```bash
node .claude/skills/release-notes/lib/parse-commits.cjs <base> <head> [--with-files]
```

**Output:** JSON with commits array containing:

- `hash`, `shortHash` - Commit identifiers
- `type`, `scope`, `description` - Conventional commit parts
- `breaking` - Boolean for breaking changes
- `author`, `date` - Attribution
- `files` - Changed files (with `--with-files` flag)

### Step 2: Categorize Commits

Pipe parsed commits through the categorizer:

```bash
node .claude/skills/release-notes/lib/parse-commits.cjs <base> <head> | \
node .claude/skills/release-notes/lib/categorize-commits.cjs
```

**Categorization Rules:**
| Type | Category | User-Facing |
| --------------------------------------- | ------------ | --------------------- |
| `feat` | features | Yes |
| `fix` | fixes | Yes |
| `perf` | improvements | Yes |
| `docs` | docs | Yes (unless internal) |
| `refactor` | improvements | Technical only |
| `test`, `ci`, `build`, `chore`, `style` | internal | No |

**Excluded Patterns:**

- `chore(deps):` - Dependency updates
- `chore(config):` - Configuration changes
- `[skip changelog]` - Explicit skip
- `[ci skip]` - CI markers

### Step 3: Render Markdown

Generate the final release notes document:

```bash
node .claude/skills/release-notes/lib/parse-commits.cjs <base> <head> | \
node .claude/skills/release-notes/lib/categorize-commits.cjs | \
node .claude/skills/release-notes/lib/render-template.cjs --version v1.1.0 --output docs/release-notes/250111-v1.1.0.md
```

## Complete Pipeline

For generating release notes in a single command:

```bash
# Full pipeline with output to file
node .claude/skills/release-notes/lib/parse-commits.cjs v1.0.0 HEAD | \
node .claude/skills/release-notes/lib/categorize-commits.cjs | \
node .claude/skills/release-notes/lib/render-template.cjs --version v1.1.0 --output docs/release-notes/250111-v1.1.0.md

# Pipeline to stdout for review
node .claude/skills/release-notes/lib/parse-commits.cjs v1.0.0 HEAD | \
node .claude/skills/release-notes/lib/categorize-commits.cjs | \
node .claude/skills/release-notes/lib/render-template.cjs --version v1.1.0
```

## Advanced Features

### Service Boundary Detection

Analyze which services are affected by the release:

```bash
# Parse with file changes, then detect services
node .claude/skills/release-notes/lib/parse-commits.cjs v1.0.0 HEAD --with-files | \
node .claude/skills/release-notes/lib/detect-services.cjs
```

**Output:** Service impact analysis with severity levels (critical, high, medium, low)

### Breaking Change Analysis

Enhanced breaking change detection with migration info extraction:

```bash
node .claude/skills/release-notes/lib/parse-commits.cjs v1.0.0 HEAD | \
node .claude/skills/release-notes/lib/categorize-commits.cjs | \
node .claude/skills/release-notes/lib/detect-breaking.cjs
```

**Detects:**

- `BREAKING CHANGE:` in commit body
- `!` suffix on commit type (e.g., `feat!:`)
- Migration instructions

### PR Metadata Extraction

Extract and link pull request information:

```bash
# Extract PR numbers from commit messages
node .claude/skills/release-notes/lib/parse-commits.cjs v1.0.0 HEAD | \
node .claude/skills/release-notes/lib/extract-pr-metadata.cjs

# With GitHub API enrichment (requires gh CLI)
node .claude/skills/release-notes/lib/parse-commits.cjs v1.0.0 HEAD | \
node .claude/skills/release-notes/lib/extract-pr-metadata.cjs --fetch-gh
```

**Extracts:** PR numbers, titles, labels, authors from commits

### Contributor Statistics

Generate detailed contributor stats:

```bash
node .claude/skills/release-notes/lib/parse-commits.cjs v1.0.0 HEAD | \
node .claude/skills/release-notes/lib/contributor-stats.cjs
```

**Output:** Contributor list with commit counts, feature/fix breakdown

### Version Bumping

Automatically determine and bump semantic version based on commit types:

```bash
# Auto-bump based on commits (feat→minor, fix→patch, BREAKING→major)
node .claude/skills/release-notes/lib/parse-commits.cjs v1.0.0 HEAD | \
node .claude/skills/release-notes/lib/bump-version.cjs

# Bump with prerelease tag
node .claude/skills/release-notes/lib/bump-version.cjs --prerelease beta

# Per-service versioning
node .claude/skills/release-notes/lib/bump-version.cjs --service {service-name}

# Dry run (don't write version file)
node .claude/skills/release-notes/lib/bump-version.cjs --dry-run
```

**Version Files:**

- Root: `.version`
- Per-service: `.versions/<service-name>.version`

### Quality Validation

Validate release notes against quality rules:

```bash
# Validate with default threshold (70)
node .claude/skills/release-notes/lib/validate-notes.cjs docs/release-notes/v1.1.0.md

# Custom threshold
node .claude/skills/release-notes/lib/validate-notes.cjs docs/release-notes/v1.1.0.md --threshold 80

# JSON output for CI
node .claude/skills/release-notes/lib/validate-notes.cjs docs/release-notes/v1.1.0.md --json
```

**Validation Rules (100 points total):**
| Rule | Weight | Description |
| --------------------------- | ------ | ---------------------------- |
| summary_exists | 15 | Has Summary section |
| summary_not_empty | 10 | Summary has content |
| has_version | 10 | Version number present |
| features_documented | 10 | Features properly formatted |
| fixes_documented | 10 | Bug fixes properly formatted |
| no_broken_links | 10 | No empty link references |
| contributors_listed | 10 | Contributors section present |
| has_date | 5 | Date present |
| no_todo_markers | 5 | No TODO/FIXME markers |
| proper_heading_hierarchy | 5 | Proper H1→H2 structure |
| no_placeholder_text | 5 | No placeholder text |
| technical_details_collapsed | 5 | Tech details in <details> |

### LLM-Powered Transforms

Transform release notes for different audiences using Claude API:

```bash
# Requires ANTHROPIC_API_KEY environment variable
export ANTHROPIC_API_KEY="your-api-key"

# Create executive summary
node .claude/skills/release-notes/lib/transform-llm.cjs docs/release-notes/v1.1.0.md --transform executive

# Transform for business stakeholders
node .claude/skills/release-notes/lib/transform-llm.cjs docs/release-notes/v1.1.0.md --transform business --output docs/release-notes/v1.1.0-business.md

# Transform for end users
node .claude/skills/release-notes/lib/transform-llm.cjs docs/release-notes/v1.1.0.md --transform enduser
```

**Transform Types:**
| Type | Description |
| ----------- | ------------------------------ |
| `summarize` | Brief 3-5 bullet point summary |
| `business` | ROI-focused, business language |
| `enduser` | User-friendly, non-technical |
| `executive` | Strategic impact summary |
| `technical` | Enhanced technical details |

### Full Enhanced Pipeline

Combine all features for comprehensive release notes:

```bash
# Enhanced pipeline with service detection
node .claude/skills/release-notes/lib/parse-commits.cjs v1.0.0 HEAD --with-files | \
node .claude/skills/release-notes/lib/detect-services.cjs | \
node .claude/skills/release-notes/lib/categorize-commits.cjs | \
node .claude/skills/release-notes/lib/detect-breaking.cjs | \
node .claude/skills/release-notes/lib/contributor-stats.cjs | \
node .claude/skills/release-notes/lib/render-template.cjs --version v1.1.0

# With version bumping and validation
node .claude/skills/release-notes/lib/parse-commits.cjs v1.0.0 HEAD --with-files | \
node .claude/skills/release-notes/lib/bump-version.cjs | \
node .claude/skills/release-notes/lib/categorize-commits.cjs | \
node .claude/skills/release-notes/lib/render-template.cjs --output docs/release-notes/v1.1.0.md && \
node .claude/skills/release-notes/lib/validate-notes.cjs docs/release-notes/v1.1.0.md
```

## Configuration

See `config.yaml` for:

- **categories** - Commit type to section mapping
- **services** - Service boundary detection by file patterns
- **exclude** - Patterns to exclude from user-facing notes
- **output** - Directory and filename format settings

## Output Structure

```markdown
# Release Notes: v1.1.0

**Date:** 2025-01-11
**Version:** v1.1.0
**Status:** Draft

---

## Summary

This release includes 3 new features, 2 improvements, 5 bug fixes.

## What's New

- **Add employee export endpoint** (API)
- **Implement dark mode toggle** (UI)

## Improvements

- **Optimize database queries** (Persistence)

## Bug Fixes

- **Fix date picker timezone issue** (Frontend)
- **Resolve null pointer in auth flow**

## Documentation

- **Update API documentation** (API)

## Breaking Changes

> **Warning**: The following changes may require migration

### Migrate to OAuth 2.1 (Auth)

Legacy JWT tokens no longer accepted.
Migration guide: docs/migrations/oauth-2.1.md

---

## Technical Details

<details>
<summary>For Developers</summary>

### Commits Included

| Hash    | Type | Description                    |
| ------- | ---- | ------------------------------ |
| abc1234 | feat | Add employee export endpoint   |
| def5678 | fix  | Fix date picker timezone issue |

...

</details>

## Contributors

- @john.doe
- @jane.smith

---

_Generated with [Claude Code](https://claude.com/claude-code)_
```

## Human Review Gate

Generated release notes are **Draft** status by default:

1. **Review** - Check accuracy, add context where needed
2. **Enhance** - Add migration steps, links, screenshots
3. **Approve** - Change status to "Released"
4. **Publish** - Commit and push

## Integration with Other Skills

- **`/commit`** - After generating notes, commit them
- **`/git-manager`** - Create PR for release notes review
- **`/docs-update`** - Update CHANGELOG.md with new release

## Troubleshooting

### No commits found

Verify the refs exist and have commits between them:

```bash
git log --oneline <base>..<head>
```

### Non-conventional commits

Commits not following `type(scope): description` format go to "other" category. Consider running commitlint enforcement.

### Missing scope context

Add scope mappings to `config.yaml` → `services` section for better context labels.

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
