---
name: github-navigator
description: "GitHub operations via gh CLI. CRITICAL: Always use instead of WebFetch for ANY github.com URL. Use when user provides GitHub URL, says 'facebook/react', 'show README', 'list issues', 'check PR', 'clone repo', 'analyze this repo', 'understand the architecture', 'how is X structured', 'explore the codebase'. For deep analysis of external repos, clones locally."
allowed-tools: Bash(gh:*) Bash(git:clone) Read Glob Grep Task
context: fork
hooks:
  PostToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "python3 scripts/validate-gh-output.py"
---

# GitHub Navigator

Uses gh CLI for **all** GitHub operations. Teaches discovery pattern via `gh --help`.

**Requirements:** `gh` CLI installed and authenticated.

## Core Principle

**One pattern for everything:**

0. **Verify** gh CLI is installed and authenticated (first use only)
1. **Identify** command domain (files, issues, PRs, releases, etc.)
2. **Discover** usage via `gh <command> --help` or `gh api --help`
3. **Apply** pattern to user's specific request
4. **Execute** with max 2 attempts, then STOP

## When to Use

**ALWAYS use this skill when:**

- User provides a GitHub URL (any `github.com/` link)
- User asks about GitHub repositories, issues, PRs, releases
- User mentions repo paths like "facebook/react"
- User wants GitHub information or operations

**Common triggers:**

- "Show me the README from facebook/react"
- "List open issues in vercel/next.js"
- "What's in the packages/ directory?"
- "Check latest release for react"
- "View PR #123 in cli/cli"

## Deep Analysis Mode

When user wants to **understand a codebase deeply** (not just fetch a single file), clone the repository locally for comprehensive analysis.

**Trigger phrases:**

- "analyze this repo"
- "understand the architecture"
- "how is X structured"
- "explore the codebase"
- "give me an overview of"
- "what patterns does X use"
- "how does this project work"

**Workflow:**

1. Clone to `/tmp/github-navigator/<owner>-<repo>/`

   ```bash
   git clone --depth 1 https://github.com/OWNER/REPO.git /tmp/github-navigator/OWNER-REPO
   ```

2. Analyze the codebase:
   - **Tech stack detection**: Look for package.json, go.mod, Cargo.toml, pom.xml, requirements.txt, etc.
   - **Directory structure**: Map out the main directories and their purposes
   - **Entry points**: Find main files, index files, app entry points
   - **Patterns**: Identify architectural patterns (MVC, microservices, monorepo, etc.)
   - **Key files**: README, CONTRIBUTING, docs/, examples/

3. Provide comprehensive summary with:
   - Tech stack overview
   - Project structure explanation
   - Key files and their purposes
   - Architectural patterns observed

4. Keep cloned for follow-up questions (user can explore further)

**Cleanup:**

Repos in `/tmp/github-navigator/` are cleaned on system restart. For manual cleanup:

```bash
rm -rf /tmp/github-navigator/
```

**Note:** Use `--depth 1` for faster cloning when full history isn't needed. Use full clone if user needs git history analysis.

## Discovery Pattern

### Step 0: Verify gh CLI (First Use Only)

Before first use, verify gh CLI is installed and authenticated:

```bash
gh --version        # Check if gh is installed
gh auth status      # Check authentication status
```

If not installed, see [Installation](#installation).
If not authenticated, run `gh auth login` for private repos and write operations.

### Step 1: Identify Command Domain

| User Request | Command Domain | Primary Command |
|--------------|----------------|-----------------|
| Fetch file content | Files | `gh api repos/OWNER/REPO/contents/PATH` |
| List directory | Files | `gh api repos/OWNER/REPO/contents/PATH` |
| Issues (list, view, create, close) | Issues | `gh issue` |
| Pull Requests (list, view, diff, merge) | PRs | `gh pr` |
| Releases (list, view, create) | Releases | `gh release` |
| Actions/Workflows (runs, logs) | Actions | `gh run` or `gh workflow` |
| Repository info (clone, view, fork) | Repo | `gh repo` |

### Step 2: Discover Usage

**For files/directories (use gh api):**

```bash
gh api --help
```

**For everything else (use gh subcommands):**

```bash
gh issue --help           # Shows all issue subcommands
gh issue list --help      # Shows specific flags
gh pr --help              # Shows all PR subcommands
gh release --help         # Shows release operations
```

### Step 3: Apply Pattern

Extract usage from help, substitute user's values, execute.

### Step 4: Execute with Guardrails

- **Max 2 attempts** per command pattern
- If fails twice: **STOP** and report error to user
- **Never loop endlessly** trying variations

## File & Directory Operations

Use `gh api` for all file operations.

### Fetch File Content

```bash
# Raw content (preferred for text files)
gh api repos/OWNER/REPO/contents/PATH -H "Accept: application/vnd.github.raw"

# Examples
gh api repos/facebook/react/contents/README.md -H "Accept: application/vnd.github.raw"
gh api repos/vercel/next.js/contents/package.json -H "Accept: application/vnd.github.raw"

# Specific branch/ref
gh api repos/OWNER/REPO/contents/PATH?ref=BRANCH -H "Accept: application/vnd.github.raw"

# Example
gh api repos/facebook/react/contents/package.json?ref=main -H "Accept: application/vnd.github.raw"
```

**Note:** If your shell interprets special characters in the URL path (like `?`), quote the path appropriately for your environment.

### List Directory Contents

```bash
# Get directory listing (returns JSON array)
gh api repos/OWNER/REPO/contents/PATH

# Format nicely with jq
gh api repos/OWNER/REPO/contents/PATH | jq -r '.[] | "\(.type): \(.name)"'

# Show directories and files separately
gh api repos/vercel/next.js/contents/packages | \
  jq -r 'group_by(.type) | map({type: .[0].type, items: map(.name)}) | .[]'

# Simple list of names
gh api repos/OWNER/REPO/contents/PATH | jq -r '.[].name'

# Repository root
gh api repos/OWNER/REPO/contents
```

### Get Default Branch

```bash
gh api repos/OWNER/REPO --jq .default_branch
```

## Issue Operations

Use `gh issue` subcommands.

### List Issues

```bash
# Basic list
gh issue list --repo OWNER/REPO

# Filter by state
gh issue list --repo OWNER/REPO --state open
gh issue list --repo OWNER/REPO --state closed
gh issue list --repo OWNER/REPO --state all

# Filter by label
gh issue list --repo OWNER/REPO --label bug
gh issue list --repo OWNER/REPO --label "good first issue"

# Limit results
gh issue list --repo OWNER/REPO --limit 10

# JSON output
gh issue list --repo OWNER/REPO --json number,title,state,author
```

### View Issue

```bash
# View issue details
gh issue view NUMBER --repo OWNER/REPO

# View with comments
gh issue view NUMBER --repo OWNER/REPO --comments

# JSON output
gh issue view NUMBER --repo OWNER/REPO --json title,body,state,comments
```

### Create Issue (Requires Confirmation)

```bash
# ⚠️ MUST confirm with user first
gh issue create --repo OWNER/REPO --title "Title" --body "Description"
```

### Close Issue (Requires Confirmation)

```bash
# ⚠️ MUST confirm with user first
gh issue close NUMBER --repo OWNER/REPO
```

## Pull Request Operations

Use `gh pr` subcommands.

### List PRs

```bash
# Basic list
gh pr list --repo OWNER/REPO

# Filter by state
gh pr list --repo OWNER/REPO --state open
gh pr list --repo OWNER/REPO --state closed
gh pr list --repo OWNER/REPO --state merged

# Filter by author
gh pr list --repo OWNER/REPO --author USERNAME

# JSON output
gh pr list --repo OWNER/REPO --json number,title,state,author
```

### View PR

```bash
# View PR details
gh pr view NUMBER --repo OWNER/REPO

# View with comments
gh pr view NUMBER --repo OWNER/REPO --comments

# JSON output
gh pr view NUMBER --repo OWNER/REPO --json title,body,state,mergeable
```

### View PR Diff

```bash
gh pr diff NUMBER --repo OWNER/REPO

# Specific files only
gh pr diff NUMBER --repo OWNER/REPO --patch
```

### Check PR Status

```bash
# View CI/CD checks
gh pr checks NUMBER --repo OWNER/REPO
```

### Merge PR (Requires Confirmation)

```bash
# ⚠️ MUST confirm with user first
gh pr merge NUMBER --repo OWNER/REPO
```

## Release Operations

Use `gh release` subcommands.

### List Releases

```bash
# List all releases
gh release list --repo OWNER/REPO

# Limit results
gh release list --repo OWNER/REPO --limit 5
```

### View Release

```bash
# View specific release
gh release view TAG --repo OWNER/REPO

# Latest release
gh release view --repo OWNER/REPO
```

### Download Release Assets

```bash
# Download all assets from a release
gh release download TAG --repo OWNER/REPO

# Download specific pattern
gh release download TAG --repo OWNER/REPO --pattern "*.tar.gz"
```

## Actions/Workflow Operations

Use `gh run` and `gh workflow` subcommands.

### List Workflow Runs

```bash
# List recent runs
gh run list --repo OWNER/REPO

# Filter by workflow
gh run list --repo OWNER/REPO --workflow build.yml

# Limit results
gh run list --repo OWNER/REPO --limit 10
```

### View Run Details

```bash
# View run info
gh run view RUN_ID --repo OWNER/REPO

# View logs
gh run view RUN_ID --repo OWNER/REPO --log
```

## Repository Operations

Use `gh repo` subcommands.

### View Repository Info

```bash
# View repo details
gh repo view OWNER/REPO

# JSON output
gh repo view OWNER/REPO --json name,description,stargazersCount,forksCount
```

### Clone Repository

```bash
# Clone repo
gh repo clone OWNER/REPO

# Clone to specific directory
gh repo clone OWNER/REPO target-directory
```

### Fork Repository

```bash
# Fork repo to your account
gh repo fork OWNER/REPO

# Fork and clone
gh repo fork OWNER/REPO --clone
```

## Safety Rules

### Failure Limits

**Maximum 2 attempts per command pattern, then STOP.**

1. **Attempt 1**: Run the command as discovered from help
2. **If fails**: Check error message, adjust ONCE
3. **Attempt 2**: Run corrected command
4. **If fails again**: **STOP** - Report error to user

### Destructive Operations

**Always confirm before executing:**

- Delete or archive operations (`gh repo delete`, `gh repo archive`)
- State changes (`gh pr merge`, `gh issue close`)
- Creating resources (`gh issue create`, `gh pr create`)
- Security operations (`gh secret set`, `gh workflow run`)
- Force flags (`--force`, `--yes`, `-y`)

**Confirmation pattern:**

```
⚠️  This will [ACTION] in [REPO].
Command: [command]

Confirm you want to proceed?
```

## Authentication

Most operations work unauthenticated for public repos. Private repos and write operations require auth.

### Check Auth Status

```bash
gh auth status
```

### Authenticate

```bash
gh auth login
```

### Refresh with Additional Scopes

```bash
# If you get "Resource not accessible" errors
gh auth refresh -s repo -s workflow -s read:org
```

## Error Handling

### Common Errors and Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `gh: command not found` | gh CLI not installed | Install: `brew install gh` (macOS) |
| `HTTP 401: Unauthorized` | Not authenticated | Run: `gh auth login` |
| `HTTP 404: Not Found` | Repo doesn't exist or private | Check name, or authenticate |
| `unknown flag: --xyz` | Wrong flag syntax | Check: `gh <cmd> --help` |
| `Resource not accessible` | Insufficient permissions | Run: `gh auth refresh -s repo` |
| `API rate limit exceeded` | Too many requests | Authenticate for 5000/hr limit |

### Debugging Strategy

When command fails: Read error → check `gh <cmd> --help` → try once more → report to user if still fails.

**DO NOT try multiple blind variations.**

## Advanced: gh api

For operations not covered by gh subcommands, use `gh api` directly:

```bash
gh api repos/OWNER/REPO                    # Get repo info
gh api repos/OWNER/REPO/commits            # List commits
gh api repos/OWNER/REPO/issues/NUMBER --jq '.title,.state'
```

**Prefer standard commands when available** - simpler and more reliable.

See [REFERENCES.md](REFERENCES.md) for GraphQL examples.

## Installation

Install: `brew install gh` (macOS) or see [REFERENCES.md](REFERENCES.md). Then: `gh auth login`

---

> **License:** MIT | **See also:** [REFERENCES.md](REFERENCES.md)
