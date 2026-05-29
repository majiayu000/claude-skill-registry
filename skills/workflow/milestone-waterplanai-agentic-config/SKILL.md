---
name: milestone
description: "Validates backlog section completion, then squashes and tags or identifies gaps. Generates milestone and release notes. Triggers on keywords: milestone, release notes, tag release, validate backlog"
project-agnostic: true
allowed-tools:
  - Read
  - Edit
  - Bash
  - Grep
  - Glob
  - Task
  - Write
  - AskUserQuestion
---


Validate section completion in backlog, then either release or identify gaps.

**All arguments are optional** with smart defaults.

## Argument Parsing

Parse `$ARGUMENTS` into:

| Variable | Source | Required | Default |
|----------|--------|----------|---------|
| `BACKLOG_PATH` | 1st arg | No | Auto-detect: `BACKLOG.md`, `specs/backlog.md`, or skip |
| `SECTION` | 2nd arg | No | Latest incomplete section, or skip if no backlog |
| `BASE_BRANCH` | 3rd arg | No | `origin/main` (fetches first) |
| `VERSION` | 4th arg (if not quoted) | No | Auto-bump from `VERSION` file or latest git tag |
| `VALIDATION_PROMPT` | Last quoted string `"..."` | No | Auto-derive from checklist |
| `SKIP_TAG` | `--skip-tag` flag | No | `false` (tags created by default) |
| `AUTO_MODE` | `--auto` flag | No | `false` (confirmation gates enabled) |
| `WITH_SQUASHED_COMMITS` | `--with-squashed-commits` flag | No | `false` (squashed commits list excluded by default) |

**Parsing Rules:**
- If an argument starts and ends with `"`, treat as `VALIDATION_PROMPT`
- Version is optional; if 4th arg is quoted, there's no version
- If `--skip-tag` flag is present anywhere in arguments, set `SKIP_TAG=true`
- If `--with-squashed-commits` flag is present anywhere in arguments, set `WITH_SQUASHED_COMMITS=true`
- If `--auto` flag is present anywhere in arguments, set `AUTO_MODE=true` (skips confirmation gates)
- Empty `$ARGUMENTS` triggers full auto-detect mode

## Phase 0: Smart Defaults Resolution

**When NO arguments provided:**

### 0.1 Fetch Remote
```bash
git fetch origin main 2>/dev/null || git fetch origin master 2>/dev/null
```

### 0.2 Determine BASE_BRANCH
```bash
# Try origin/main first, fallback to origin/master
git rev-parse origin/main >/dev/null 2>&1 && echo "origin/main" || echo "origin/master"
```

### 0.3 Auto-Detect BACKLOG_PATH
Search in order:
1. `BACKLOG.md` (root)
2. `specs/backlog.md`
3. `docs/backlog.md`
4. `backlog.md`

If none found → **SKIP backlog validation** (proceed without backlog)

### 0.4 Auto-Detect SECTION (if backlog exists)
Find first incomplete section (has `- [ ]` items). If all complete → use most recent section.

### 0.5 Auto-Detect VERSION
**If `SKIP_TAG=false`:**
Priority order:
1. `VERSION` file → parse, increment patch: `X.Y.Z` → `X.Y.(Z+1)`, prefix with `v`
2. Latest git tag matching `v*.*.*` → increment patch
3. Default: `v0.1.0`

**If `SKIP_TAG=true`:**
Set `VERSION=""` (no version/tag will be created)

### 0.6 CHANGELOG Consistency Check (Critical for No-Args Mode)
```bash
# Check if CHANGELOG.md exists and has [Unreleased] content
grep -A 100 "\\[Unreleased\\]" CHANGELOG.md 2>/dev/null | grep -E "^- |^### " | head -20
```

**If CHANGELOG [Unreleased] is EMPTY but commits exist since BASE_BRANCH:**
```
CHANGELOG SYNC REQUIRED

Commits since {BASE_BRANCH}:
  {commit list}

But CHANGELOG.md [Unreleased] section is empty.

Please update CHANGELOG.md with these changes before proceeding.
```
-> **STOP** and wait for user to update changelog.

**If CHANGELOG [Unreleased] has content -> proceed.**

### 0.7 Project-Specific Enforcement

Check if `AGENTS.md` contains project-specific rules:
```bash
test -f AGENTS.md && echo "exists" || echo "none"
```

**If exists:**
1. Read `AGENTS.md` content
2. Parse and store rules for validation in Phase 4.5
3. Common rules to detect:
   - `no emojis` / `DO NOT use emojis` -> flag emoji restrictions
   - `project-agnostic` / `anonymous` -> flag content anonymity requirements
   - `relative symlinks` -> flag symlink requirements

**Store parsed rules as `PROJECT_RULES` for later validation.**

## Phase 1: Pre-Flight Checks

1. **Git state**: Must be clean (no uncommitted changes)
2. **Commits exist**: Must have commits since `BASE_BRANCH`
3. **CHANGELOG exists**: `CHANGELOG.md` must exist with `[Unreleased]` section
4. **Backlog exists** (if path provided): File at `BACKLOG_PATH` must exist
5. **Section exists** (if backlog provided): Section `SECTION` must be found in backlog

If any fail → STOP with specific error message.

## Phase 2: Extract Checklist (if backlog provided)

1. Read backlog file at `BACKLOG_PATH`
2. Find section matching `SECTION` (patterns: `#### 1.2`, `### Phase 1.2`, `## 1.2`)
3. Extract ALL checklist items until next section:
   - `- [ ]` = unchecked
   - `- [x]` = checked
4. Report: `Found X items (Y checked, Z unchecked)`

**If no backlog:** Skip to Phase 4 with auto-approval path.

## Phase 3: Validate Implementation (if backlog provided)

### If `VALIDATION_PROMPT` provided:
Use it as explicit criteria. Spawn validation agent with prompt:
```
VALIDATE: {VALIDATION_PROMPT}

For each criterion, search codebase and report:
- Status: FOUND | MISSING
- Evidence: file:line references
- Notes: any issues
```

### If NO `VALIDATION_PROMPT`:
For each UNCHECKED item (`- [ ]`):

1. Parse item to identify expected:
   - Files/components (look for nouns)
   - Interfaces/functions (look for code terms)
   - Tests (if mentioned)

2. Search codebase:
   - Grep for key terms
   - Glob for expected file patterns
   - Check test directories

3. Classify:
   - **IMPLEMENTED**: Found despite unchecked
   - **MISSING**: No evidence found

## Phase 4: Decision Gate

### Path A: No Backlog (Changelog-Only Validation)

Display:
```
✅ CHANGELOG Validated

Changes since {BASE_BRANCH}:
- {N} commits
- Key changes: {summary}

CHANGELOG [Unreleased] entries:
{entries}

Release Configuration:
- Base: {BASE_BRANCH}
- Version: {VERSION or "(no tag)" if SKIP_TAG=true}
- Commits to squash: N

Proceed with squash + tag? (yes/no)
```

**If `AUTO_MODE=true`:** Skip confirmation, proceed directly to squash/tag.

→ On "yes" (or auto): proceed to squash/tag.

### Path B: Backlog - ALL COMPLETE (all items implemented or checked)

Display:
```
✅ Section {SECTION} COMPLETE

Validated Items:
- [x] Item 1 - evidence: file:line
- [x] Item 2 - evidence: file:line
...

Release Configuration:
- Base: {BASE_BRANCH}
- Version: {VERSION or "(no tag)" if SKIP_TAG=true}
- Commits to squash: N
- CHANGELOG: [Unreleased] → [{VERSION or section name if SKIP_TAG=true}]

Proceed with squash? (yes/no)
```

**If `AUTO_MODE=true`:** Skip confirmation, proceed directly.

**On "yes" (or auto):**
1. Update backlog: mark all items `[x]`, add checkmark to section header
2. **Update CHANGELOG.md:**
   - Move all entries from `[Unreleased]` to new `[{VERSION}] - {YYYY-MM-DD}` section
   - Keep empty `[Unreleased]` section at top
   - If no VERSION provided or `SKIP_TAG=true`, use section name as header
3. Commit: `docs: mark {SECTION} as completed`
4. Create backup: `{branch}-backup/{YYYY}/{MM}/{DD}/001`
5. Soft reset to `BASE_BRANCH`
6. **Generate Conventional Commit message** (see Phase 4B)
7. Create squashed commit with generated message
8. If `VERSION` and `SKIP_TAG=false`: create annotated tag

→ Proceed to **Phase 5: Push Confirmation**

## Phase 4B: Conventional Commit Message Generation

Generate a standardized commit message following Conventional Commits extended format.

### 4B.1 Analyze Changes

```bash
# Get full diff for analysis
git diff {BASE_BRANCH}..HEAD --stat
git diff {BASE_BRANCH}..HEAD --name-status
```

### 4B.2 Determine Commit Type

Parse changed files and categorize by **primary change type**:

| Type | When to Use |
|------|-------------|
| `feat` | New feature or capability added |
| `fix` | Bug fix |
| `docs` | Documentation only changes |
| `chore` | Maintenance, deps, configs (no production code) |
| `refactor` | Code restructuring without behavior change |
| `test` | Adding or modifying tests |
| `style` | Formatting, whitespace, linting |
| `perf` | Performance improvements |
| `build` | Build system or external dependencies |
| `ci` | CI/CD configuration changes |

**Selection Priority:**
1. If ANY `feat` changes exist -> type = `feat`
2. Else if ANY `fix` changes exist -> type = `fix`
3. Else use dominant change type

### 4B.3 Determine Scope

Analyze changed file paths to identify scope:

```bash
# Get unique top-level directories/components
git diff --name-only {BASE_BRANCH}..HEAD | cut -d'/' -f1-2 | sort -u
```

**Scope Rules:**
- Single component modified -> use component name (e.g., `commands`, `skills`)
- Multiple related components -> use parent (e.g., `core`)
- Unrelated changes -> omit scope or use `release`
- Version/release changes -> scope = `release` or version number

### 4B.4 Generate Commit Title

Format: `<type>(<scope>): <description>`

**Description Rules:**
- Imperative mood ("add" not "added")
- Lowercase first letter
- No period at end
- Max 72 characters total
- Summarize the main purpose

**Examples:**
- `feat(commands): add milestone validation workflow`
- `fix(parser): handle empty input gracefully`
- `docs(readme): update installation instructions`
- `chore(deps): bump typescript to v5.3`

### 4B.5 Generate Commit Body

Structure the body with these sections (include only non-empty):

```
## Added
- New feature 1
- New feature 2

## Changed
- Modified behavior 1
- Updated component 2

## Fixed
- Bug fix 1
- Issue resolution 2

## Removed
- Deprecated item 1
```

**Content Generation:**
1. Parse `git diff {BASE_BRANCH}..HEAD` file by file
2. Categorize each file's changes:
   - New files -> Added
   - Modified files -> Changed (or Fixed if bug-related)
   - Deleted files -> Removed
3. Summarize meaningful changes (not every line)
4. Reference file paths where helpful

### 4B.6 Include Original Commits (Optional)

**Only if `WITH_SQUASHED_COMMITS=true`**, append squashed commit references:

```bash
# Get original commit messages
git log --oneline {BASE_BRANCH}..HEAD
```

Format as:
```
Squashed commits:
- {sha7} {message}
- {sha7} {message}
- {sha7} {message}
```

**If `WITH_SQUASHED_COMMITS=false` (default)**: Omit this section entirely from the commit message.

### 4B.7 Complete Message Template

```
<type>(<scope>): <description>

## Added
- {additions}

## Changed
- {changes}

## Fixed
- {fixes}

## Removed
- {removals}

<!-- Only if WITH_SQUASHED_COMMITS=true -->
Squashed commits:
- {sha} {message}
- {sha} {message}
<!-- End conditional -->
```

### 4B.8 Commit Message Example

```
feat(milestone): add validation workflow with smart defaults

## Added
- Smart defaults resolution for all arguments
- CHANGELOG consistency check
- AGENTS.md validation
- Push confirmation gate

## Changed
- Refactored argument parsing to support quoted strings
- Updated backup branch naming format

## Fixed
- Backlog detection now searches multiple locations
```

### Path C: Backlog - INCOMPLETE (missing items)

Display:
```
❌ Section {SECTION} INCOMPLETE

Missing:
1. {item} - {what's missing}
2. {item} - {what's missing}

Implemented but unchecked:
1. {item} - {evidence}

Options:
(A) Create /spec for missing items
(B) Abort - review manually
```

**On "A":** Output spec creation commands:
```
Missing items require specs:

/spec CREATE {item-1-title}
/spec CREATE {item-2-title}
```

**On "B":** STOP cleanly.

## Phase 4.5: AGENTS.md Validation (Pre-Push Gate)

**If `PROJECT_RULES` were parsed in Phase 0.7, validate all changes against AGENTS.md rules:**

### 4.5.1 Get Changed Files
```bash
git diff --name-only {BASE_BRANCH}..HEAD
```

### 4.5.2 Validate Against PROJECT_RULES

For each rule detected, run validation:

**Emoji Check (if emoji restriction detected):**
```bash
# Check all changed .md files for emoji characters
git diff {BASE_BRANCH}..HEAD -- '*.md' | grep -P '[\x{1F300}-\x{1F9FF}]' || echo "clean"
```

**Project-Agnostic/Anonymous Check (if anonymity rule detected):**
```bash
# Check for personal identifiers, hardcoded usernames, local paths
git diff {BASE_BRANCH}..HEAD | grep -iE '(/Users/[a-z]+|/home/[a-z]+|@[a-z]+\.com)' || echo "clean"
```

**Symlink Check (if symlink rule detected):**
```bash
# Check for absolute symlinks in changed files
for f in $(git diff --name-only {BASE_BRANCH}..HEAD); do
  if [ -L "$f" ]; then
    target=$(readlink "$f")
    [[ "$target" = /* ]] && echo "ABSOLUTE: $f -> $target"
  fi
done
```

### 4.5.3 Violation Handling

**If ANY violations found:**
```
AGENTS.md VIOLATIONS DETECTED

The following changes violate project-specific rules:

Rule: {rule description}
Violations:
  - {file}: {violation details}
  - {file}: {violation details}

Rule: {rule description}
Violations:
  - {file}: {violation details}

Fix these violations before proceeding with release.
```
-> **STOP** - Do not proceed to Phase 5.

**If NO violations -> proceed to Phase 5.**

## Phase 5: Push Confirmation

After successful squash/tag, display:

```
## Release Prepared Locally

Commit: {sha} {message}
Branch: {branch}
Tag: {VERSION} (if created, otherwise "(none)")
Backup: {backup-branch}

Push to origin?

Commands to execute:
  git push --force-with-lease origin {branch}
  git push origin {VERSION}  # if tag created (SKIP_TAG=false)

Proceed with push? (yes/no)
```

**If `AUTO_MODE=true`:** Skip confirmation, proceed directly with push.

**On "yes" (or auto):**
1. Execute: `git push --force-with-lease origin {branch}`
2. If `VERSION` and `SKIP_TAG=false`: Execute: `git push origin {VERSION}`
3. Report success with remote URLs

**On "no" (only when `AUTO_MODE=false`):**
Display manual commands and exit:
```
Skipped push. Run manually when ready:
  git push --force-with-lease origin {branch}
  git push origin {VERSION}  # if tag was created
```

## Abort Conditions

| Condition | Action |
|-----------|--------|
| Backlog not found (when path specified) | STOP: "File not found: {path}" |
| Section not found (when specified) | STOP: "Section {SECTION} not found. Available: [list]" |
| No commits to squash | STOP: "No commits between {BASE_BRANCH} and HEAD" |
| Git dirty | STOP: "Uncommitted changes. Commit or stash first." |
| CHANGELOG missing | STOP: "CHANGELOG.md not found or missing [Unreleased] section" |
| CHANGELOG empty + commits exist | STOP: "Update CHANGELOG [Unreleased] before proceeding" |
| AGENTS.md violations | STOP: List violations, require fixes before release |
| User declines | STOP cleanly, no changes |
| Push fails | STOP: show error, suggest manual resolution |

## Usage Examples

```bash
# NO ARGUMENTS - full auto mode
# Auto-detects: backlog, section, base branch, version, validates changelog
/milestone

# With backlog and section (base branch auto-detected)
/milestone specs/backlog.md 1.2

# Full release with all args
/milestone specs/backlog.md 1.2 main v0.1.1-alpha

# With validation prompt
/milestone specs/backlog.md 1.2 main v0.1.1-alpha "NoteMeta extended, parser exists, 20 tests pass"

# Without custom prompt (auto-detect from checklist)
/milestone docs/roadmap.md 2.1 main v2.1.0

# Validate only, no version tag
/milestone CHANGELOG.md phase-3 develop

# Quoted prompt without version
/milestone specs/features.md 4.0 main "API endpoints implemented, auth working"

# Skip tag creation with --skip-tag flag
/milestone specs/backlog.md 1.2 main --skip-tag

# Skip tag with validation prompt
/milestone specs/backlog.md 1.2 main --skip-tag "All tests passing"

# Auto-detect mode without tags
/milestone --skip-tag

# Autonomous mode (skip all confirmation gates)
/milestone --auto

# Autonomous mode with skip-tag (used by orchestrators)
/milestone --skip-tag --auto

# Include squashed commits in message (opt-in)
/milestone --with-squashed-commits
```
