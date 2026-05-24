---
name: ralph-github-create-issues
description: Converts a PRD markdown file into GitHub Issues (parent + sub-issues) for ralph-github-start-loop to execute. Use when user wants to push PRD stories to GitHub Issues.
---

# Create PRD Issues

Convert a local PRD or plan file into GitHub Issues.

## Usage

```
/ralph-create-github-issues              # Looks in .claude/plans/ then prds/
/ralph-create-github-issues auth-flow    # Convert specific PRD by name
```

For story sizing and acceptance criteria guidance, see `references/best-practices.md`.

## Preflight

Run these checks. Stop if critical ones fail.

```bash
# 1. Auth check
gh auth status

# 2. Find plan/PRD files — check all locations
ls .claude/plans/*.md 2>/dev/null
ls plans/*.md 2>/dev/null
ls prds/*.md 2>/dev/null

# 3. PRD not already an issue (stop if found open)
gh issue list --label prd --state all --json number,title,state

# 4. Ensure prd label exists
gh label create prd --description "Product Requirements Document" --color "0052CC" 2>/dev/null || true

# 5. Get existing PRDs for dependency matching
gh issue list --label prd --state open --json number,title
```

### Where to find plans

Check these locations in order:

1. **`.claude/plans/`** — Where plan mode saves approved plans. This is the primary source.
2. **`plans/`** — Project-level plans directory.
3. **`prds/`** — Standalone PRDs not generated from plan mode.

If files exist in multiple locations, list all and ask which to convert. If only one file is found, use it directly. **If no files are found in any location, ask the user for the path to their PRD/plan file.**

Scan PRD markdown for dependency references ("depends on X", "see `feature.md`"). Note matches for later.

**Note:** Assume `gh sub-issue` and `gh issue-dependency` are already installed. Do NOT try to install them. Just run the commands — if they fail, skip that step and continue.

## Create Issues

### Parent Issue

```bash
gh issue create \
  --title "Feature Name" \
  --label "prd" \
  --label "enhancement" \
  --body "$(cat <<'EOF'
## Overview
<From PRD intro>

## Branch
`feature/<name>`

## Quality Gates
```bash
npm run typecheck
npm run lint
npm test
```

## Implementation Order
1. Story one
2. Story two
EOF
)"
```

### Sub-Issues

For each story:

```bash
# Create issue
gh issue create \
  --title "Story Title" \
  --body "$(cat <<'EOF'
**Files:** `path/to/file.tsx`

**Acceptance Criteria:**
- [ ] Specific change
- [ ] Typecheck passes
- [ ] Lint passes

**Notes:**
Context if needed.
EOF
)"

# Link to parent
gh sub-issue add <parent> <child>
```

### Dependencies

If dependencies detected in preflight, use GraphQL API (no extension needed):

```bash
# Get repo info
OWNER=$(gh repo view --json owner -q '.owner.login')
REPO=$(gh repo view --json name -q '.name')

# Get node IDs (replace 50 and 42 with actual issue numbers)
BLOCKED_ID=$(gh api graphql -f query="{ repository(owner: \"$OWNER\", name: \"$REPO\") { issue(number: 50) { id } } }" --jq '.data.repository.issue.id')
BLOCKING_ID=$(gh api graphql -f query="{ repository(owner: \"$OWNER\", name: \"$REPO\") { issue(number: 42) { id } } }" --jq '.data.repository.issue.id')

# Add blocked-by relationship
gh api graphql -f query="mutation { addBlockedBy(input: {issueId: \"$BLOCKED_ID\", blockingIssueId: \"$BLOCKING_ID\"}) { clientMutationId } }"
```

## Output

```
Created: #50 - Feature Name
  → #51 Story One
  → #52 Story Two

Dependencies: Blocked by #42 (Auth Flow)
Branch: feature/<name>

Run: /ralph-github-start-loop
```

Then ask:

```
Remove local plan/PRD file? <path> (y/n)
```

If yes, delete the source file. GitHub Issue is now source of truth.
