---
name: github-issue-solve
description: "Solve GitHub issues by implementing features or fixes and creating pull requests. Use when: (1) Implementing features described in issues, (2) Fixing bugs reported in issues, (3) Creating PRs from issue requirements."
---

# GitHub Issue Solve Skill

Automation skill for solving GitHub issues by implementing solutions and creating pull requests.

## Purpose

This skill helps you:
1. Analyze GitHub issues and understand requirements
2. Implement features or fixes in the codebase
3. Create feature branches and commit changes
4. Create pull requests with proper descriptions

## Prerequisites

This skill can use:
- **`ghx`** (default): Must be attempted first for context collection
- **`gh` CLI** (fallback): Use only when `ghx` is unavailable or fails

`ghx` here means the `ghx` skill (for example `skills/ghx/scripts/ghx.sh`), not a standalone `ghx` binary on `PATH`.

## Environment & Paths

- **`GITHUB_OUTPUT_DIR`**: Where this skill writes artifacts  
  - Default: system-recommended output directory if provided by caller; otherwise a temp dir `/tmp/holon-ghissue-*`
- **`GITHUB_CONTEXT_DIR`**: Where `ghx` writes collected data  
  - Default: `${GITHUB_OUTPUT_DIR}/github-context`
- **`GITHUB_TOKEN` / `GH_TOKEN`**: Token used for GitHub operations (scopes: `repo` or `public_repo`)

## Inputs & Outputs

- **Inputs**: `${GITHUB_CONTEXT_DIR}/github/issue.json`, `${GITHUB_CONTEXT_DIR}/github/comments.json` (produced via `ghx` by default; fallback via `gh` commands only if `ghx` fails)
- **Outputs** (agent writes under `${GITHUB_OUTPUT_DIR}`):
  - `summary.md`
  - `manifest.json`

## Definition of Done (Strict)

The run is successful only if all of the following are true:
1. Code changes are implemented for the target issue.
2. Changes are pushed to a branch.
3. A GitHub PR is actually created or updated using `gh`.
4. PR existence is verified via `gh pr view`.
5. `${GITHUB_OUTPUT_DIR}/summary.md` and `${GITHUB_OUTPUT_DIR}/manifest.json` include publish result details (`pr_number` and `pr_url`).

## Workflow

### 1. Context Collection

If context is not pre-populated, always follow this decision order:
1. Attempt `ghx` collection first.
2. If `ghx` is unavailable or fails, fall back to `gh issue view` / `gh api` and write equivalent context files under `${GITHUB_CONTEXT_DIR}/github/`.
3. Record the collector and fallback reason (if any) in outputs:
   - `context_collector`: `ghx` or `gh`
   - `fallback_reason`: non-empty only when `context_collector=gh`
     - Example: `ghx command not found in PATH`
     - Example: `ghx context collect failed with exit code 1`

### 2. Analyze Issue

Read the collected context:
- `${GITHUB_CONTEXT_DIR}/github/issue.json`: Issue metadata (title, body, labels, assignees)
- `${GITHUB_CONTEXT_DIR}/github/comments.json`: Discussion comments

Understand:
- What feature or fix is requested
- Any specific requirements or constraints
- Related issues or PRs mentioned

### 3. Implement Solution

Create a feature branch and implement the solution:

```bash
# Create feature branch
git checkout -b feature/issue-<number>

# Make your changes to the codebase
# ... implement the feature or fix ...

# Commit changes
git add .
git commit -m "Feature: <description>"

# Push to remote
git push -u origin feature/issue-<number>
```

### 4. Generate Artifacts

Create the required output files:

#### `${GITHUB_OUTPUT_DIR}/summary.md`

Human-readable summary of your work:
- Issue reference and description
- What was implemented
- Key changes made
- Testing performed

#### `${GITHUB_OUTPUT_DIR}/manifest.json`

Execution metadata:
```json
{
  "provider": "github-issue-solve",
  "issue_ref": "holon-run/holon#502",
  "context_collector": "ghx|gh",
  "fallback_reason": "",
  "branch": "feature/issue-502",
  "status": "completed|failed",
  "commits": ["abc123", "def456"]
}
```

### 5. Create Pull Request

Use a direct `gh` publish flow (single mandatory path):

```bash
ISSUE_NUMBER=<issue number>
HEAD_BRANCH="$(git branch --show-current)"
BASE_BRANCH="${BASE_BRANCH:-main}"
PR_TITLE="Fix #${ISSUE_NUMBER}: <short title>"
PR_BODY_FILE="${GITHUB_OUTPUT_DIR}/summary.md"

EXISTING_PR_NUMBER="$(gh pr list --head "$HEAD_BRANCH" --json number --jq '.[0].number // empty')"

if [ -n "$EXISTING_PR_NUMBER" ]; then
  gh pr edit "$EXISTING_PR_NUMBER" --title "$PR_TITLE" --body-file "$PR_BODY_FILE" --base "$BASE_BRANCH"
  PR_NUMBER="$EXISTING_PR_NUMBER"
else
  gh pr create --base "$BASE_BRANCH" --head "$HEAD_BRANCH" --title "$PR_TITLE" --body-file "$PR_BODY_FILE"
  PR_NUMBER="$(gh pr list --head "$HEAD_BRANCH" --json number --jq '.[0].number // empty')"
fi

if [ -z "$PR_NUMBER" ]; then
  echo "ERROR: failed to resolve PR number after publish" >&2
  exit 1
fi

PR_URL="$(gh pr view "$PR_NUMBER" --json url --jq .url)"
if [ -z "$PR_URL" ]; then
  echo "ERROR: failed to resolve PR url after publish" >&2
  exit 1
fi
```

Treat publish execution as mandatory completion work, not optional cleanup.
Update `${GITHUB_OUTPUT_DIR}/summary.md` and `${GITHUB_OUTPUT_DIR}/manifest.json` with `pr_number` and `pr_url`.

## Output Contract

### Required Outputs

1. **`${GITHUB_OUTPUT_DIR}/summary.md`**: Human-readable summary
   - Issue reference and description
   - Implementation details
   - Changes made
   - Testing performed

2. **`${GITHUB_OUTPUT_DIR}/manifest.json`**: Execution metadata
   ```json
   {
     "provider": "github-issue-solve",
     "issue_ref": "holon-run/holon#502",
     "context_collector": "ghx|gh",
     "fallback_reason": "",
     "branch": "feature/issue-502",
     "status": "completed|failed",
     "commits": ["abc123"],
     "pr_number": 123,
     "pr_url": "https://github.com/holon-run/holon/pull/123"
   }
   ```

### Failure Rules

- If PR create/edit or PR verification fails, mark the run as failed.
- Do not report success when only artifacts were generated without a PR side effect.
- On failure, write actionable publish error details and next steps in `${GITHUB_OUTPUT_DIR}/summary.md`.
- If `ghx` is available but not attempted first for context collection, treat as process failure and correct before reporting success.

## Git Operations

You are responsible for all git operations:

```bash
# Create feature branch
git checkout -b feature/issue-<number>

# Stage changes
git add .

# Commit with descriptive message
git commit -m "Feature: <description>"

# Push to remote
git push -u origin feature/issue-<number>
```

## GitHub CLI Operations

You MAY use these commands:
- `gh issue view <number>` - View issue details
- `gh issue comment <number>` - Comment on issues
- `gh pr create` / `gh pr edit` - Create or update PR
- `gh pr view <number>` - Verify PR details after publish

## Important Notes

- You are running **HEADLESSLY** - do not wait for user input or confirmation
- Attempt `ghx` first for context collection; use `gh` only as explicit fallback with documented reason
- Create feature branches following the pattern `feature/issue-<number>` or `fix/issue-<number>`
- Write clear commit messages describing what was changed
- Include "Closes #<number>" in PR body to auto-link the issue
- Run tests if available before creating the PR
- Do not mark success until `gh pr view` returns a valid PR URL

## Reference Documentation

See [references/issue-solve-workflow.md](references/issue-solve-workflow.md) for detailed workflow guide.
