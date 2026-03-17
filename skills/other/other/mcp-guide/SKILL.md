---
name: mcp-guide
description: Guide for selecting and using MCP servers (Git, GitHub, Context7, Knip, Memory, Sequential Thinking). Use when you need help choosing the right tool for version control, GitHub operations, documentation lookup, dead code detection, or knowledge persistence.
allowed-tools: Read, Grep, Glob
---

# MCP Server Usage Guide

This project has MCP servers configured in the workspace `.mcp.json` file. These tools form the **AI Project Management Additions** to assist with automated linting, state tracking, and development.

## Available Servers

| Server                 | Purpose                      | When to Use                                                           |
| ---------------------- | ---------------------------- | --------------------------------------------------------------------- |
| **context7**           | Library documentation lookup | Query up-to-date docs for libraries/frameworks (React, Next.js, etc.) |
| **github**             | GitHub API operations        | PRs, issues, repos, commits, code search via GitHub API               |
| **knip**               | Dead code detection          | Find unused exports, dependencies, and files in the codebase          |
| **spec-lint**          | Enforce spec immutability    | Automatically run to ensure no progress leaks into specs              |
| **next-devtools**      | Next.js inspection           | Debugging React components and Next.js state                          |
| **memory**             | Persistent knowledge graph   | Store/recall architectural decisions, patterns, known issues          |
| **git**                | Git operations               | Commits, diffs, branches, history viewing                             |
| **filesystem**         | File operations              | Read/write project files                                              |
| **sequentialthinking** | Structured reasoning         | Complex debugging, architecture decisions                             |
| **time**               | Timezone utilities           | Timestamps (rarely needed)                                            |

---

## Git & GitHub Tool Selection Guide

Three tools available for version control and GitHub operations. Choose based on the task:

| Task                   | Use This             | Why                       |
| ---------------------- | -------------------- | ------------------------- |
| View status, diff, log | **Git MCP**          | Clean structured output   |
| Create commits         | **Git MCP**          | Proper message formatting |
| List/switch branches   | **Git MCP**          | Simple operations         |
| Push to remote         | **Bash `git push`**  | MCP doesn't support push  |
| Create PRs             | **Bash `gh pr`**     | Reliable, no auth issues  |
| Create/update issues   | **Bash `gh issue`**  | Reliable, no auth issues  |
| Add issue comments     | **Bash `gh issue`**  | Reliable, no auth issues  |
| Search issues          | **Bash `gh issue`**  | Reliable, no auth issues  |
| Search code on GitHub  | **Bash `gh search`** | Reliable, no auth issues  |
| List/manage milestones | **Bash `gh api`**    | No MCP milestone support  |
| Complex git operations | **Bash `git`**       | Rebase, cherry-pick, etc. |

> **⚠️ IMPORTANT:** The GitHub MCP server frequently has authentication failures ("Bad credentials" errors) even when tokens are configured. **Always prefer the `gh` CLI via Bash** for GitHub operations (issues, PRs, searches). The `gh` CLI is pre-authenticated and reliable.

### Decision Flowchart

```
Is it a GitHub.com operation (issues, PRs, remote files)?
├─ Yes → Use Bash `gh` CLI (gh issue, gh pr, gh api)
│        └─ GitHub MCP is unreliable due to auth issues
└─ No → Is it a local git operation?
        ├─ Yes → Use Git MCP
        │        └─ Unless it's push/pull/fetch → Use `git` in Bash
        └─ No → Use Bash
```

### Git MCP Server

Use for local repository operations:

```
mcp__git__git_status      # Working tree status
mcp__git__git_diff        # View changes (staged/unstaged)
mcp__git__git_log         # Commit history
mcp__git__git_commit      # Create commits
mcp__git__git_branch      # List branches
mcp__git__git_checkout    # Switch branches
mcp__git__git_add         # Stage files
```

**Limitations:** Cannot push, pull, fetch, or perform remote operations.

### GitHub MCP Server

> **⚠️ NOT RECOMMENDED:** The GitHub MCP server frequently fails with "Bad credentials" authentication errors. **Use the `gh` CLI via Bash instead** for all GitHub operations.

Available tools (but prefer `gh` CLI):

```
mcp__github__create_issue           # Use: gh issue create
mcp__github__update_issue           # Use: gh issue edit
mcp__github__add_issue_comment      # Use: gh issue comment
mcp__github__list_issues            # Use: gh issue list
mcp__github__create_pull_request    # Use: gh pr create
mcp__github__get_pull_request       # Use: gh pr view
mcp__github__search_code            # Use: gh search code
mcp__github__get_file_contents      # Use: gh api repos/OWNER/REPO/contents/PATH
```

**Limitations:** Unreliable authentication, no milestone CRUD.

### Bash git/gh CLI (Preferred for GitHub)

**The `gh` CLI is the most reliable way to interact with GitHub.** Use it for all GitHub operations.

> For detailed issue management (epics, sub-issues, milestones, GraphQL API), see the `/github-issues` skill.

```bash
# Issues (preferred over GitHub MCP)
gh issue list --search "keyword"           # Search issues
gh issue list --state all --limit 30       # List all issues
gh issue view 123                          # View issue details
gh issue create --title "Title" --body "Body"
gh issue edit 123 --add-label "bug"
gh issue comment 123 --body "Comment text"

# Pull Requests (preferred over GitHub MCP)
gh pr list                                 # List open PRs
gh pr view 123                             # View PR details
gh pr create --title "Title" --body "Body"
gh pr merge 123 --squash

# Search (preferred over GitHub MCP)
gh search issues "keyword repo:owner/repo"
gh search code "function_name repo:owner/repo"

# API access for anything else
gh api repos/OWNER/REPO/milestones
gh api repos/OWNER/REPO/contents/path/to/file

# Remote git operations (not in Git MCP)
git push origin branch-name
git pull origin main
git fetch --all

# Complex git operations
git rebase -i HEAD~3
git cherry-pick abc123
git stash push -m "message"
```

---

## Context7 Usage

Use Context7 to fetch up-to-date documentation for libraries and frameworks:

```
# Get documentation for a library
resolve-library-id: "react"
get-library-docs: { libraryId: "/react/react", topic: "hooks" }
```

Best for:

- Checking current API signatures
- Understanding library-specific patterns
- Verifying framework best practices

---

## Knip Usage

Use Knip to detect dead code and unused dependencies:

```
# Run knip analysis
run_knip: { cwd: "/path/to/project" }

# Get knip documentation
get_knip_docs: { topic: "configuration" }
```

Best for:

- Finding unused exports before refactoring
- Identifying dead code after feature removal
- Cleaning up unused dependencies

---

## Memory Server Usage

The memory server maintains project knowledge across sessions. Use it to:

**Query existing knowledge:**

```
mcp__memory__search_nodes("ruleset")     # Find ruleset architecture info
mcp__memory__search_nodes("technical")   # Find known technical debt
mcp__memory__open_nodes(["KeyFiles"])    # Get key file locations
```

**Store new knowledge:**

```
mcp__memory__create_entities([...])      # Add new architectural concepts
mcp__memory__add_observations([...])     # Add details to existing entities
mcp__memory__create_relations([...])     # Link concepts together
```

**When to update memory:**

- After making significant architectural decisions
- When discovering important patterns or gotchas
- After resolving tricky bugs (document the solution)
- When adding new major features

---

## Sequential Thinking Usage

Use `mcp__sequentialthinking__sequentialthinking` for:

- Debugging complex ruleset merge issues
- Planning multi-step refactors
- Working through character creation edge cases
- Designing new edition support
- Any problem requiring step-by-step reasoning with revision
