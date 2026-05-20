---
name: GitHub CLI Workflows
description: This skill should be used when the user asks to "use GitHub CLI", "use gh command", work with "pull requests", "create a PR", "merge pull request", "approve PR", "review PR comments", "check PR status", work with "issues", "triage issues", "list issues", "label issues", work with "GitHub Actions", "check CI status", "fix failing CI", "view workflow runs", "download workflow logs", "rerun workflow", or mentions "gh tool", "gh command", or GitHub automation tasks. Provides comprehensive guidance for autonomously creating and executing GitHub workflows using the official GitHub CLI.
version: 0.1.0
---

# GitHub CLI Workflows

## Purpose

Enable autonomous creation and execution of GitHub workflows using the official GitHub CLI (`gh`). This skill provides the knowledge and patterns needed to work with pull requests, issues, GitHub Actions, and the GitHub API through command-line operations.

## Core Philosophy

Work autonomously within user-specified boundaries, respecting the current Claude Code mode (accept edits vs plan mode). Design multi-step workflows tailored to specific needs, handle errors intelligently, and always verify context before executing repository operations.

## Prerequisites

### Required Tools

**GitHub CLI must be installed.** Check with:
```bash
gh --version
```

If not installed, guide the user to https://cli.github.com/ for installation instructions (brew, apt, etc.).

### Authentication Status

**Do not proactively check authentication**, but be prepared to recognize and diagnose authentication errors. When auth issues occur, guide the user to resolve them (see `references/troubleshooting.md`).

## The Golden Rule: Use `--help` First

**CRITICAL:** Every `gh` command and subcommand supports `--help` to display comprehensive usage information, including:
- Available flags and options
- Argument formats
- Detailed examples
- Exit codes
- Related commands

**When to use `--help`:**
- Before constructing any complex command
- When uncertain about flag syntax
- When encountering errors (verify command structure)
- To discover available subcommands
- To check for new features or options

**Examples:**
```bash
gh --help                    # List all commands
gh repo --help               # Repository commands
gh repo create --help        # Specific command details
gh pr create --help          # PR creation options
gh api --help                # API usage with examples
```

**Pattern:** `gh <command> <subcommand> --help` works at every level. Always check help before guessing command syntax.

## Repository Context

Before executing repo-specific commands, verify repository context:

```bash
gh repo view
```

This confirms:
- Current repository (owner/repo)
- Authentication works
- Proper permissions exist

**When context is unclear**, infer from the current directory unless explicitly specified otherwise. Use `-R owner/repo` flag to override when working across multiple repositories.

## Core Capabilities

### Pull Requests

Create, review, comment, merge, and manage pull requests programmatically.

**Common operations:**
- Create PR from current branch
- List open PRs with filters
- View PR details and checks
- Review and comment on PRs
- Merge PRs with various strategies
- Checkout PR branches locally

See `references/pr-workflows.md` for detailed patterns.

### Issues

Triage, label, comment, and manage issues systematically.

**Common operations:**
- List new/open issues
- Create issues with templates
- Add/remove labels
- Comment and discuss
- Close with resolution notes
- Link to PRs

See `references/issue-workflows.md` for detailed patterns.

### GitHub Actions

Monitor workflow runs, analyze failures, view logs, and trigger reruns.

**Common operations:**
- List workflow runs
- Check run status and conclusion
- Download and analyze logs
- Rerun failed workflows
- Cancel running workflows
- View workflow definitions

See `references/actions-workflows.md` for detailed patterns.

### GitHub API

Execute custom operations not covered by core commands using `gh api`.

**Common operations:**
- GraphQL queries for complex data
- REST API operations
- Pagination handling with `--paginate`
- JSON output parsing with `--jq`
- Custom integrations

See `references/api-usage.md` for detailed patterns and examples.

## Working with JSON Output

Many `gh` commands support `--json` for structured output and `--jq` for filtering.

**When to use JSON:**
- Parse results programmatically
- Extract specific fields
- Process multiple items
- Make decisions based on output

**When to use human-readable:**
- Show output directly to user
- Initial exploration
- Debugging

**Pattern:** Fetch with JSON, format for humans in responses:

```bash
# Get structured data
gh pr list --json number,title,author,state

# Extract specific fields
gh pr view 123 --json title,body --jq '.title'

# Process and format for user display
```

Always show users formatted, readable output in responses, even when working with JSON internally.

## Destructive Operations

**Always ask user confirmation** before executing operations that:
- Close issues or PRs
- Delete branches
- Merge pull requests
- Archive repositories
- Modify labels or milestones permanently

**Offer dry-run option when available:**
```
I can perform a dry-run first to show what would happen. Would you like me to:
1. Execute the operation now
2. Perform a dry-run and report the outcome
3. Show you the exact command to review first
```

Use `--dry-run` flags where supported (check `--help` for availability).

## Error Handling Workflow

When a `gh` command fails, follow this sequence:

### 1. Review Command Output
Most errors have clear, actionable messages. Read the error carefully:
- Authentication required
- Permission denied
- Resource not found
- Invalid arguments
- Rate limit exceeded

### 2. Search Troubleshooting Documentation
Use grep/search tools to find relevant information in `references/troubleshooting.md`:
```bash
# Search for specific error patterns
grep -i "authentication" references/troubleshooting.md
```

Avoid reading the entire troubleshooting file unless necessary.

### 3. Verify Command with `--help`
Check that command syntax matches the help documentation:
```bash
gh <command> <subcommand> --help
```

Common issues:
- Wrong flag names
- Missing required arguments
- Incorrect argument order
- Flag used with wrong command

### 4. Report to User
If the error persists after these steps, report detailed diagnostics:
- Exact command executed
- Complete error output
- Steps already attempted
- Relevant troubleshooting findings
- Suggested next actions

Ask for user guidance on how to proceed.

## Autonomy and User Boundaries

### Respect Current Mode

**In accept-edits mode:**
- Make changes directly
- Execute commands autonomously
- Commit and push as needed

**In plan mode:**
- Create detailed implementation plans
- Get user approval before execution
- Document each planned step

### User-Specified Boundaries

Honor any constraints the user provides:
- Repository limits
- Branch protections
- Label conventions
- Review requirements
- Approval workflows

### Workflow-Specific Autonomy

**Fix Failing CI/CD:**
View run → Download logs → Analyze errors → Suggest fixes → Implement → Push → (Rerun only if workflow won't auto-trigger)

**Triage Issues:**
Execute based on user-specified parameters (which labels to apply, what comments to add, etc.)

**Implement PR Feedback:**
Read comments → Make changes → Commit → Push (respecting current mode)

**Create Pull Requests:**
Verify branch → Push if needed → Create PR with description → Link issues (respecting current mode)

Be as autonomous as possible within established boundaries.

## Common Patterns

For frequently-used patterns and workflows, see `references/common-patterns.md`:
- Authentication checks and recovery
- Multi-repository operations
- Batch processing issues/PRs
- CI/CD integration patterns
- Error recovery strategies
- Working with draft PRs
- Managing labels and milestones
- Using PR templates

## Command Discovery

Discover available commands at any level:

```bash
gh --help                    # All core commands
gh pr --help                 # PR subcommands
gh issue --help              # Issue subcommands
gh run --help                # Actions run commands
gh workflow --help           # Workflow commands
gh api --help                # API usage (extensive examples)
```

Each help page includes:
- Command descriptions
- Available subcommands
- Flags and options
- Usage examples
- Related commands

## Output Visibility

**Always show commands before execution** so users understand what's running:

```
Checking repository context with:
$ gh repo view

Creating pull request with:
$ gh pr create --title "feat: Add user authentication" --body "..." --base main
```

This transparency helps users:
- Understand the workflow
- Learn `gh` commands
- Verify correctness
- Reproduce manually if needed

## Additional Resources

### Reference Files

Detailed workflows and patterns are documented in `references/`:

- **`references/pr-workflows.md`** - Pull request operations: create, review, merge, comment
- **`references/issue-workflows.md`** - Issue management: triage, label, comment, close
- **`references/actions-workflows.md`** - GitHub Actions: check runs, view logs, rerun
- **`references/api-usage.md`** - Direct API calls with `gh api` for custom operations
- **`references/common-patterns.md`** - Reusable patterns: auth checks, error recovery, batch operations
- **`references/troubleshooting.md`** - Common problems and solutions

### Example Files

Real-world scenarios with expected outputs in `examples/`:

- **`examples/fix-failing-ci.md`** - Complete workflow for diagnosing and fixing CI failures
- **`examples/triage-issues.md`** - Systematic issue triage with labeling and commenting
- **`examples/pr-review-cycle.md`** - End-to-end PR creation, review, and merge process

## Key Reminders

1. **Check `--help` before guessing** command syntax
2. **Verify repository context** before repo-specific operations
3. **Ask confirmation** for destructive operations
4. **Follow error handling workflow**: output → troubleshooting → --help → report
5. **Respect user mode** (accept-edits vs plan mode)
6. **Show commands** before execution for transparency
7. **Format output** for human readability in responses
8. **Be autonomous** within user-specified boundaries
9. **Use JSON/jq** for programmatic processing
10. **Reference detailed docs** in references/ as needed

---

For comprehensive workflow details, consult the reference files. For working examples, see the examples directory. Always prioritize using `--help` to discover current command capabilities.
