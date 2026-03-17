---
name: changelog-manager
description: Reviews git history and updates CHANGELOG.md with entries for [Unreleased] section (converted from agent)
dependencies: []
---

# Changelog Manager

When invoked, perform the following changelog management tasks: analyze git history and update CHANGELOG.md with well-written entries for the `[Unreleased]` section following the Keep a Changelog format.

## Prerequisites

No external skills are required. This skill operates independently.

## Workflow

Execute these steps in order:

### Step 1: Find and Read CHANGELOG.md

1. Look for `CHANGELOG.md` in the repository root:
   ```bash
   ls -la CHANGELOG.md
   ```

2. If not found, check common locations or prompt the user:
   - `docs/CHANGELOG.md`
   - `CHANGES.md`

3. Read the changelog and identify:
   - The last released version (e.g., `## [0.2.0]`)
   - Existing entries under `## [Unreleased]`
   - The changelog format and style used

If no CHANGELOG.md exists, ask the user if they want one created.

### Step 2: Get Git History Since Last Release (Enhanced)

**Path filter note:** If a path filter is provided in the prompt (e.g., `-- agent-alchemy/sdd/`), append it to all `git log` commands in this step to scope results to that sub-project.

1. Find the tag for the last release:
   ```bash
   git tag --list 'v*' --sort=-version:refname | head -5
   ```

2. Get commits with extended format including body (for breaking change notices):
   ```bash
   git log v{version}..HEAD --format="%H|%s|%b" --no-merges [path_filter]
   ```

   If no tags exist, get recent commits with warning:
   ```bash
   git log --format="%H|%s|%b" --no-merges -50 [path_filter]
   ```

3. Extract PR/issue references for later enrichment:
   ```bash
   git log v{version}..HEAD --no-merges --oneline [path_filter] | grep -oE '#[0-9]+' | sort -u
   ```

4. For more context on specific commits, use:
   ```bash
   git show --stat {commit_sha}
   ```

### Step 3: Analyze File Changes

**Purpose:** Understand scope and impact of changes.

1. Get files changed with status (A=Added, M=Modified, D=Deleted, R=Renamed):
   ```bash
   git diff v{version}..HEAD --name-status [path_filter]
   ```

2. Get summary by directory:
   ```bash
   git diff v{version}..HEAD --dirstat [path_filter]
   ```

3. Categorize files by area:

   | Path Pattern | Category | Changelog Relevance |
   |--------------|----------|---------------------|
   | `src/`, `lib/` | Core code | High |
   | `tests/`, `__tests__/` | Tests | Low (skip) |
   | `docs/`, `*.md` | Documentation | Medium |
   | Root configs (`*.json`, `*.toml`) | Configuration | High |
   | `.github/`, CI files | CI/CD | Low (skip) |

4. Flag cross-cutting changes: If 5+ directories affected, note "wide-ranging changes" in summary.

### Step 4: Deep Diff Analysis

**Purpose:** Detect API changes and breaking changes.

1. Detect new public interfaces:
   ```bash
   # Python: new functions/classes (public only, skip underscore-prefixed)
   git diff v{version}..HEAD -- "*.py" | grep -E "^\+\s*(def |class )" | grep -v "_"

   # JS/TS: new exports
   git diff v{version}..HEAD -- "*.ts" "*.js" | grep -E "^\+.*export"
   ```

2. Detect removed interfaces (**BREAKING**):
   ```bash
   # Python
   git diff v{version}..HEAD -- "*.py" | grep -E "^-\s*(def |class )" | grep -v "_"

   # JS/TS
   git diff v{version}..HEAD -- "*.ts" "*.js" | grep -E "^-.*export"
   ```

3. Detect dependency changes:
   ```bash
   git diff v{version}..HEAD -- pyproject.toml package.json requirements*.txt
   ```

4. Track findings internally:
   - `new_apis[]` - new public functions/classes
   - `removed_apis[]` - **BREAKING**
   - `modified_apis[]` - potentially breaking
   - `dependency_changes[]`

### Step 5: PR/Issue Context Enrichment

**Purpose:** Get richer context from PRs and issues.

1. Check gh CLI availability:
   ```bash
   which gh && gh auth status 2>/dev/null
   ```

2. If gh is available, fetch PR context for each PR number found:
   ```bash
   gh pr view {number} --json title,body,labels,files
   ```

3. **Fallback:** If gh unavailable, continue with git data only (log this to user).

4. Extract from PR data:
   - PR title (often better than commit subject)
   - Labels (`breaking-change`, `bug`, `feature`, `security`)
   - PR body for migration notes

### Step 6: Categorize Changes (Enhanced)

**Primary:** Use conventional commit prefixes:

| Prefix | Category | Include in Changelog |
|--------|----------|---------------------|
| `feat:` | Added | Yes |
| `fix:` | Fixed | Yes |
| `refactor:` | Changed | Yes (if user-facing) |
| `change:` | Changed | Yes |
| `perf:` | Changed | Yes |
| `security:` | Security | Yes |
| `deprecate:` | Deprecated | Yes |
| `remove:` | Removed | Yes |
| `docs:` | - | No (internal) |
| `chore:` | - | No (internal) |
| `test:` | - | No (internal) |
| `ci:` | - | No (internal) |
| `style:` | - | No (internal) |
| `build:` | - | No (internal) |

**Secondary signals** (override/augment when detected):

| Signal | Category | Priority |
|--------|----------|----------|
| Removed export detected | Removed + BREAKING | High |
| PR label `breaking-change` | Add BREAKING flag | High |
| PR label `security` | Security | High |
| New export detected | Added | Medium |

For commits without conventional prefixes, use diff analysis results to determine the appropriate category.

### Step 7: Synthesize Entries (Enhanced)

**Entry sources (priority order):**
1. PR title (if more descriptive than commit subject)
2. Commit subject
3. Code analysis (for accuracy)

**Entry Format:**
- Start with imperative verb (Add, Fix, Change, Remove, etc.)
- Focus on user impact, not implementation details
- Keep entries concise (one line preferred)
- Include scope in parentheses if helpful: `Add support for (authentication)`

**Breaking change format:**
```markdown
### Removed
- **BREAKING**: Remove deprecated `oldFunction` (use `newFunction` instead)
```

**Group related changes** when multiple commits touch same feature (>50% file overlap).

### Step 8: Present Draft for Review (Enhanced)

**Show summary stats:**
```
Analyzed N commits since vX.Y.Z:
- Files changed: X (Y core, Z tests)
- New APIs detected: X
- Removed APIs detected: X (BREAKING)
- PR context enriched: X of Y
```

**Prominent breaking changes section** (if any detected):
```
BREAKING CHANGES DETECTED:
- Removed `oldFunction` from module.py
- Changed signature of `processData()`
```

**Show the user:**
1. **Existing [Unreleased] entries** (if any)
2. **Suggested new entries** organized by category
3. **Commits analyzed** with brief summary

**Prompt the user:**

```
Based on {N} commits since v{version}, I suggest these changelog entries:

### Added
- Entry 1
- Entry 2

### Fixed
- Entry 3

### Changed
- Entry 4

Would you like to:
```

Options:
- **"Approve all entries"**
- **"Edit entries (tell me what to change)"**
- **"See detailed analysis"**
- **"See code diffs"**
- **"Skip certain entries"**

### Step 9: Update CHANGELOG.md

Once approved, update CHANGELOG.md:

1. Add new entries under the appropriate categories in `[Unreleased]`
2. Create category headings if they don't exist
3. Preserve existing unreleased entries
4. Maintain consistent formatting

**Category Order** (per Keep a Changelog):
1. Added
2. Changed
3. Deprecated
4. Removed
5. Fixed
6. Security

**Sub-project headings:** When a scope is provided in the prompt, place entries under a sub-project heading within `[Unreleased]`:

```markdown
## [Unreleased]

### sdd

#### Added
- New entry scoped to sdd

### agent-alchemy-tools

#### Fixed
- Fix scoped to agent-alchemy-tools
```

Use `###` for sub-project names and `####` for categories within them. If no scope is provided (default behavior), use `###` for categories directly as usual.

## Edge Case Handling

| Scenario | Handling |
|----------|----------|
| No commits since release | Report "No new commits found since {version}" and exit gracefully |
| No tags exist | Use last 50 commits with warning to user |
| gh CLI unavailable | Skip PR enrichment, proceed with git data only |
| PR not found | Continue without that PR's context |
| Massive refactor (100+ files) | Warn about scope, suggest grouping entries |
| No conventional prefix | Use diff analysis for categorization |
| Merge commits in history | Skip merge commits (use `--no-merges`) |
| Commits already in changelog | Compare and skip duplicates |
| Squash-merged PRs | Treat as single entry, check PR for details |

## Breaking Change Detection

**Auto-flag as BREAKING:**
- Removed public function/class/export
- Removed required parameter
- Changed return type of public function
- PR label contains "breaking"
- Commit body contains "BREAKING CHANGE:"

**Flag for review (ask user):**
- Renamed function/class
- Added required parameter
- Changed default values
- Moved to different module

## Quality Standards

- Never add implementation details (commit SHAs, file paths, technical jargon)
- Write from the user's perspective
- Group related changes when possible
- Flag breaking changes prominently with `**BREAKING**:` prefix
- Maintain the existing changelog's voice and style

## Tool Capability Summary

This skill requires the ability to read files, edit files, search for files and content, and execute shell commands (for git operations and gh CLI). It modifies CHANGELOG.md as its primary output.

---

## Integration Notes

This skill was converted from the changelog-manager agent in the dev-tools plugin package. It is typically delegated to by the release skill during Step 5 (Changelog Update Check). It can also be invoked independently to update the changelog at any time.
