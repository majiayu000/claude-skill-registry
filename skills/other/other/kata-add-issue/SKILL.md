---
name: kata-add-issue
description: Capture an idea, task, or issue that surfaces during a Kata session as a structured issue for later work. This skill creates markdown issue files in the .planning/issues/open directory with relevant metadata and content extracted from the conversation. Triggers include "add issue", "capture issue", "new issue", "create issue", "log issue", "file issue", "add todo" (deprecated), "capture todo" (deprecated), "new todo" (deprecated).
metadata:
  version: "0.3.0"
allowed-tools: Read Write Bash Glob
---
<objective>
Capture an idea, task, or issue that surfaces during a Kata session as a structured issue for later work.

Enables "thought -> capture -> continue" flow without losing context or derailing current work.
</objective>

<context>
@.planning/STATE.md
</context>

<process>

<step name="deprecation_notice">
**If the user invoked with "todo" vocabulary** (e.g., "add todo", "capture todo", "new todo"):

Display:

> **Note:** "todos" are now "issues". Using `/kata-add-issue`.

Then proceed with the action (non-blocking).
</step>

<step name="check_and_migrate">
Check if legacy `.planning/todos/` exists and needs migration:

```bash
if [ -d ".planning/todos/pending" ] && [ ! -d ".planning/todos/_archived" ]; then
  # Create new structure
  mkdir -p .planning/issues/open .planning/issues/closed

  # Copy pending todos to open issues
  cp .planning/todos/pending/*.md .planning/issues/open/ 2>/dev/null || true

  # Copy done todos to closed issues
  cp .planning/todos/done/*.md .planning/issues/closed/ 2>/dev/null || true

  # Archive originals
  mkdir -p .planning/todos/_archived
  mv .planning/todos/pending .planning/todos/_archived/ 2>/dev/null || true
  mv .planning/todos/done .planning/todos/_archived/ 2>/dev/null || true

  echo "Migrated todos to issues format"
fi
```

Migration is idempotent: presence of `_archived/` indicates already migrated.
</step>

<step name="ensure_directory">
```bash
mkdir -p .planning/issues/open .planning/issues/closed
```
</step>

<step name="check_existing_areas">
```bash
find .planning/issues/open -maxdepth 1 -name "*.md" 2>/dev/null | xargs -I {} grep "^area:" {} 2>/dev/null | cut -d' ' -f2 | sort -u
```

Note existing areas for consistency in infer_area step.
</step>

<step name="extract_content">
**With arguments:** Use as the title/focus.
- `/kata-add-issue Add auth token refresh` -> title = "Add auth token refresh"

**Without arguments:** Analyze recent conversation to extract:
- The specific problem, idea, or task discussed
- Relevant file paths mentioned
- Technical details (error messages, line numbers, constraints)

Formulate:
- `title`: 3-10 word descriptive title (action verb preferred)
- `problem`: What's wrong or why this is needed
- `solution`: Approach hints or "TBD" if just an idea
- `files`: Relevant paths with line numbers from conversation
- `provenance`: (optional) Origin of the issue - "local" (default), "github:owner/repo#N", or other external reference
</step>

<step name="infer_area">
Infer area from file paths:

| Path pattern                   | Area       |
| ------------------------------ | ---------- |
| `src/api/*`, `api/*`           | `api`      |
| `src/components/*`, `src/ui/*` | `ui`       |
| `src/auth/*`, `auth/*`         | `auth`     |
| `src/db/*`, `database/*`       | `database` |
| `tests/*`, `__tests__/*`       | `testing`  |
| `docs/*`                       | `docs`     |
| `.planning/*`                  | `planning` |
| `scripts/*`, `bin/*`           | `tooling`  |
| No files or unclear            | `general`  |

Use existing area from step 2 if similar match exists.
</step>

<step name="check_duplicates">
```bash
find .planning/issues/open -maxdepth 1 -name "*.md" -exec grep -l -i "[key words from title]" {} + 2>/dev/null
```

If potential duplicate found:
1. Read the existing issue
2. Compare scope

If overlapping, use AskUserQuestion:
- header: "Duplicate?"
- question: "Similar issue exists: [title]. What would you like to do?"
- options:
  - "Skip" - keep existing issue
  - "Replace" - update existing with new context
  - "Add anyway" - create as separate issue
</step>

<step name="create_file">
```bash
timestamp=$(date "+%Y-%m-%dT%H:%M")
date_prefix=$(date "+%Y-%m-%d")
```

Generate slug from title (lowercase, hyphens, no special chars).

Write to `.planning/issues/open/${date_prefix}-${slug}.md`:

```markdown
---
created: [timestamp]
title: [title]
area: [area]
provenance: [provenance or "local"]
files:
  - [file:lines]
---

## Problem

[problem description - enough context for future Claude to understand weeks later]

## Solution

[approach hints or "TBD"]
```
</step>

<step name="sync_to_github">
**Check GitHub integration:**

```bash
GITHUB_ENABLED=$(cat .planning/config.json 2>/dev/null | grep -o '"enabled"[[:space:]]*:[[:space:]]*[^,}]*' | head -1 | grep -o 'true\|false' || echo "false")
```

**If `GITHUB_ENABLED=false`:** Log "Local-only issue (GitHub integration disabled)" and skip to next step.

**If `GITHUB_ENABLED=true`:**

1. **Check if already synced:**
   - Read the just-created local file's frontmatter
   - If `provenance` already contains `github:`, skip (already synced)

2. **Create backlog label (idempotent):**
   ```bash
   gh label create "backlog" --description "Kata backlog issues" --force 2>/dev/null || true
   ```

3. **Build issue body file:**
   Write to `/tmp/issue-body.md`:
   ```markdown
   ## Problem

   [problem section from local file]

   ## Solution

   [solution section from local file]

   ---
   *Created via Kata `/kata-add-issue`*
   ```

4. **Create GitHub Issue:**
   ```bash
   ISSUE_URL=$(gh issue create \
     --title "$TITLE" \
     --body-file /tmp/issue-body.md \
     --label "backlog" 2>/dev/null)
   ```

5. **Extract issue number and update provenance:**
   ```bash
   if [ -n "$ISSUE_URL" ]; then
     ISSUE_NUMBER=$(echo "$ISSUE_URL" | grep -oE '[0-9]+$')
     REPO_NAME=$(gh repo view --json nameWithOwner --jq '.nameWithOwner' 2>/dev/null)
     # Update local file's frontmatter with provenance
     # provenance: github:owner/repo#N
   fi
   ```

6. **Update local file frontmatter:**
   - Read the local issue file
   - Replace `provenance: local` with `provenance: github:${REPO_NAME}#${ISSUE_NUMBER}`
   - Write updated file

**Non-blocking error handling:** All GitHub operations are wrapped to warn but continue on failure. Local file creation is never blocked by GitHub failures.

```bash
if ! gh auth status &>/dev/null; then
  echo "Warning: gh CLI not authenticated. GitHub sync skipped."
fi
```
</step>

<step name="update_state">
If `.planning/STATE.md` exists:

1. Count issues: `find .planning/issues/open -maxdepth 1 -name "*.md" 2>/dev/null | wc -l`
2. Update "### Pending Issues" under "## Accumulated Context"
</step>

<step name="git_commit">
Commit the issue and any updated state:

**Check planning config:**

```bash
COMMIT_PLANNING_DOCS=$(cat .planning/config.json 2>/dev/null | grep -o '"commit_docs"[[:space:]]*:[[:space:]]*[^,}]*' | grep -o 'true\|false' || echo "true")
git check-ignore -q .planning 2>/dev/null && COMMIT_PLANNING_DOCS=false
```

**If `COMMIT_PLANNING_DOCS=false`:** Skip git operations, log "Issue saved (not committed - commit_docs: false)"

**If `COMMIT_PLANNING_DOCS=true` (default):**

```bash
git add .planning/issues/open/[filename]
[ -f .planning/STATE.md ] && git add .planning/STATE.md
git commit -m "$(cat <<'EOF'
docs(issue): capture issue - [title]

Area: [area]
EOF
)"
```

Confirm: "Committed: docs(issue): capture issue - [title]"
</step>

<step name="confirm">
```
Issue saved: .planning/issues/open/[filename]

  [title]
  Area: [area]
  Files: [count] referenced
  GitHub: #[number] (if synced, otherwise "local only")

---

Would you like to:

1. Continue with current work
2. Add another issue
3. View all issues (/kata-check-issues)
```
</step>

</process>

<output>
- `.planning/issues/open/[date]-[slug].md`
- Updated `.planning/STATE.md` (if exists)
- GitHub Issue #N with `backlog` label (if github.enabled=true)
</output>

<anti_patterns>
- Don't create issues for work in current plan (that's deviation rule territory)
- Don't create elaborate solution sections - captures ideas, not plans
- Don't block on missing information - "TBD" is fine
</anti_patterns>

<success_criteria>
- [ ] Directory structure exists
- [ ] Issue file created with valid frontmatter
- [ ] Problem section has enough context for future Claude
- [ ] No duplicates (checked and resolved)
- [ ] Area consistent with existing issues
- [ ] STATE.md updated if exists
- [ ] Issue and state committed to git
- [ ] GitHub Issue created with backlog label (if github.enabled=true)
- [ ] Provenance field set in local file (if GitHub synced)
</success_criteria>
