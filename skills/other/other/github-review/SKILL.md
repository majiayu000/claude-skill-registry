---
name: github-review
description: "Automated PR code review skill that collects context, performs AI-powered analysis, and publishes structured reviews with inline comments. Use when Claude needs to review pull requests: (1) Analyzing code changes for correctness/security/performance issues, (2) Generating review findings with inline comments, (3) Publishing reviews via GitHub API. Supports one-shot review and CI integration."
---

# GitHub Review Skill

Automated code review skill for pull requests. Collects PR context, performs AI-powered code review, and publishes structured reviews with inline comments.

**Prerequisites:** `gh` CLI authentication is required. `ghx` is an optional accelerator for faster context collection/publishing, but not a hard dependency.

`ghx` here means the `ghx` skill (for example `skills/ghx/scripts/ghx.sh`), not a standalone `ghx` binary on `PATH`.

## Environment and Paths

This skill uses environment variables to stay portable across Holon, local shells, and CI. It defines required inputs/outputs and publish outcomes. Prefer `ghx` when available; otherwise use `gh` commands to satisfy the same contract.

### Key Environment Variables

- **`GITHUB_OUTPUT_DIR`**: Where this skill writes artifacts  
  - Default: system-recommended output directory if provided by caller; otherwise a temp dir `/tmp/holon-ghreview-*`
- **`GITHUB_CONTEXT_DIR`**: Directory for collected PR data  
  - Default: `${GITHUB_OUTPUT_DIR}/github-context`
- **`GITHUB_TOKEN` / `GH_TOKEN`**: Token used for GitHub operations (scopes: `repo` or `public_repo`)
- Publishing options (e.g., inline limits) apply regardless of implementation (`ghx` or direct `gh`).

### Path Examples

```bash
# Runtime-provided output directory (recommended)
export GITHUB_OUTPUT_DIR=/path/to/output

# Local development (keeps workspace clean by defaulting to /tmp if unset)
export GITHUB_OUTPUT_DIR=./output
export GITHUB_TOKEN=ghp_xxx

# CI/CD environment
export GITHUB_OUTPUT_DIR=${PWD}/artifacts
export GITHUB_TOKEN=${{ secrets.GITHUB_TOKEN }}
export MAX_INLINE=10
```

## Workflow

This skill follows a three-step workflow. Agents gather context, generate artifacts, then publish. Use `ghx` if present; otherwise execute equivalent `gh` commands.

### 1. Collect Context
Collect PR information (review-friendly defaults recommended):
- PR metadata (title, description, author, stats)
- Changed files list with full diff
- Existing review threads (to avoid duplicates)
- PR comments and commit history

### 2. Perform Review
Agent analyzes the collected context and generates:
- `review.md` - Human-readable review summary
- `review.json` - Structured findings with path/line/severity/message
- `summary.md` - Brief process summary

Agent follows review guidelines in `prompts/review.md`.

Behavior requirements for this step:
- **Incremental-first**: prioritize newly introduced changes (new commits/diff hunks), and only expand scope when needed for validation.
- **Historical dedup**: consult existing review threads/comments and avoid repeating already-raised findings unless there is new evidence or changed impact.
- **Concise output**: keep review text short, direct, and action-oriented; avoid repetitive background narration.

### 3. Publish Review
Publish the produced artifacts (`review.md`, `review.json`, `summary.md`, `manifest.json`) as one PR review with inline comments.

Implementation guidance:
- Preferred: use `ghx` skill publish flow.
- Fallback: use `gh api graphql`/`gh api repos/.../pulls/.../reviews` to create a single review with inline comments.

### Direct API Example (Inline Comment)

When posting inline comments directly with `gh api`, use typed fields (`-F`) so numeric fields are sent as integers:

```bash
PR=597
REPO=holon-run/holon
HEAD_SHA="$(gh pr view "$PR" --repo "$REPO" --json headRefOid --jq .headRefOid)"

gh api "repos/$REPO/pulls/$PR/comments" \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -F body='[warn] Example inline finding message' \
  -F commit_id="$HEAD_SHA" \
  -F path='skills/github-issue-solve/SKILL.md' \
  -F line=166 \
  -F side='RIGHT'
```

Notes:
- `path` + `line` must map to a line in the PR diff for the selected `commit_id`.
- Use `-F` for `line`/`position`; avoid `-f` for numeric fields to prevent string-type API errors.

## Usage

### Basic Usage

- Collect PR context with `ghx` (agent-triggered if missing).
- Run `github-review` to produce `review.md`, `review.json`, `summary.md`.
- Publish via `ghx` using those artifacts.

### Advanced Options

```bash
# Preview review without posting (dry-run)
export DRY_RUN=true
holon --skill github-review holon-run/holon#123

# Limit inline comments
export MAX_INLINE=10
holon --skill github-review holon-run/holon#123

# Post review even if no findings
export POST_EMPTY=true
holon --skill github-review holon-run/holon#123

# Combine options
export MAX_INLINE=15 POST_EMPTY=true
holon --skill github-review holon-run/holon#123
```

## Implementation Note

This skill specifies behavior and artifacts, not a mandatory script path. Prefer `ghx` skill/script when available in the skill runtime; otherwise direct `gh` commands are valid if outputs and publish semantics match this contract.

## Agent Prompts

**`prompts/review.md`**: Review guidelines and output format for agents

Agents should read this file to understand review priorities, what to skip, and how to structure findings.

## Output Contract

### Required Inputs (from collection script)

1. **`${GITHUB_CONTEXT_DIR}/github/pr.json`**: PR metadata
2. **`${GITHUB_CONTEXT_DIR}/github/files.json`**: Changed files list
3. **`${GITHUB_CONTEXT_DIR}/github/pr.diff`**: Full diff of changes

### Optional Inputs (from collection script)

4. **`${GITHUB_CONTEXT_DIR}/github/review_threads.json`**: Existing review comments
5. **`${GITHUB_CONTEXT_DIR}/github/comments.json`**: PR discussion comments
6. **`${GITHUB_CONTEXT_DIR}/github/commits.json`**: Commit history
7. **`${GITHUB_CONTEXT_DIR}/github/check_runs.json`**: Check runs (when `INCLUDE_CHECKS=true`)

### Required Outputs (from agent)

1. **`${GITHUB_OUTPUT_DIR}/review.md`**: Human-readable review summary
   - Overall summary of the PR
   - Key findings by severity
   - Detailed feedback organized by category
   - Positive notes and recommendations

2. **`${GITHUB_OUTPUT_DIR}/review.json`**: Structured review findings
   ```json
   [
     {
       "path": "path/to/file.go",
       "line": 42,
       "severity": "error|warn|nit",
       "message": "Clear description of the issue",
       "suggestion": "Specific suggestion for fixing (optional)"
     }
   ]
   ```

3. **`${GITHUB_OUTPUT_DIR}/summary.md`**: Brief summary of the review process
   - PR reference and metadata
   - Number of findings
   - Review outcomes

### Optional Outputs (from agent)

4. **`${GITHUB_OUTPUT_DIR}/manifest.json`**: Execution metadata
   ```json
   {
     "provider": "github-review",
     "pr_ref": "holon-run/holon#123",
     "findings_count": 5,
     "inline_comments_count": 3,
     "status": "completed|completed_with_empty|failed"
   }
   ```

## Context Files

When context is collected, the following files are available under `${GITHUB_CONTEXT_DIR}/github/`:

- `pr.json`: Pull request metadata
- `files.json`: List of changed files
- `pr.diff`: Full diff of changes
- `review_threads.json`: Existing review comments (if any)
- `comments.json`: PR discussion comments (if any)
- `commits.json`: Commit history (if any)

## Integration Examples

### Holon Skill Mode

```yaml
# .github/workflows/pr-review.yml
name: PR Review
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Holon review
        uses: holon-run/holon@main
        with:
          skill: github-review
          args: ${{ github.repository }}#${{ github.event.pull_request.number }}
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          MAX_INLINE: 20
```

### Manual Review

```bash
# Review a PR manually
export GITHUB_TOKEN=ghp_xxx
export GITHUB_OUTPUT_DIR=./my-review
mkdir -p $GITHUB_OUTPUT_DIR

# Collect context (implementation-defined)
# Prefer ghx; fallback to gh commands that produce equivalent artifacts.

# Perform review (agent reads context, generates findings)
# ... agent processes ...

# Publish review with inline comments
# Prefer ghx; fallback to gh api review endpoints.
```

## Important Notes

- **Idempotency**: The skill fetches existing review threads to avoid duplicating comments
- **Incremental review default**: repeated PR updates should be reviewed with incremental priority, not full re-review by default
- **Dedup by history**: previously explicit feedback should not be repeated unless context materially changes
- **No workflow trigger changes**: this skill update does not alter `.github/workflows/` trigger behavior
- **Rate limits**: GitHub API has rate limits; the skill uses pagination and batching appropriately
- **Large PRs**: Use `MAX_FILES` to limit context collection for PRs with many changed files
- **Inline limits**: Use `MAX_INLINE` to avoid overwhelming reviewers with too many comments
- **Silent success**: By default, the skill doesn't post reviews when no findings are found (use `POST_EMPTY=true` to change this)
- **Headless operation**: The skill runs without user interaction; all configuration is via environment variables

## Capabilities

You MAY use these commands directly via `gh` CLI:
- `gh pr view` - View PR details
- `gh pr diff` - Get PR diff
- `gh api` - Make API calls

If `ghx` is available, prefer it for lower implementation cost. If not, direct `gh` usage is acceptable.

## Reference Documentation

See [prompts/review.md](prompts/review.md) for detailed review guidelines and instructions.
Implementation guidance:
- Preferred: use `ghx` context collection.
- Fallback: use `gh pr view`, `gh pr diff`, `gh api` to collect equivalent artifacts under `${GITHUB_CONTEXT_DIR}/github/`.
