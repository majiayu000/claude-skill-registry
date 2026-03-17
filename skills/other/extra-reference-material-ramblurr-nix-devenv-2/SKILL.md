---
name: Extra Reference Material
description: Manage offline reference material in the `extra/` directory. Use when needing external documentation, library source code, screenshots, PDFs, or API specs. ALWAYS check `extra/` before web searches. HALT and ask the human when required material is missing - do NOT fall back to WebFetch/WebSearch.
---

# Extra Reference Material

The `extra/` directory (gitignored) contains offline reference material: cloned repos, docs, screenshots, PDFs, API specs. **Always prefer `extra/` over web fetches.**

## Finding extra/ (Critical for Worktrees)

The `extra/` directory lives at the **project root**, NOT in worktrees.

**Detection logic:**
```bash
# If CWD contains .worktrees/, extract project root
# /home/user/project/.worktrees/feature → /home/user/project
pwd | grep -q '\.worktrees/' && echo "${PWD%/.worktrees/*}/extra" || echo "./extra"
```

**Example:**
- Working in: `/home/user/myapp/.worktrees/auth-feature/src/`
- `extra/` is at: `/home/user/myapp/extra/` (NOT `/home/user/myapp/.worktrees/auth-feature/extra/`)

**Verify with:** `git worktree list` shows main worktree path.

## Directory Structure

```
extra/
├── <repo-name>/           # Full git clones (e.g., extra/ratatui/)
├── <name>_docs/           # Documentation folders
├── <name>.md              # Single-file docs
├── screenshots/           # Visual references
└── *.pdf                  # PDF documentation
```

## Using Reference Material

**Priority order:**
1. Search `extra/` with Grep/Glob
2. If not found → HALT (do NOT web search)

**Quick lookup:**
```bash
ls extra/

# Find files by name
find extra/<repo-name> -name "*.md" -o -name "border*" 2>/dev/null

# Search with ripgrep - ALWAYS scope to a subpath
rg "pattern" extra/<repo-name>/src/
```

**ripgrep notes:**
- NEVER run `rg` on `extra/` directly - millions of hits in cloned repos
- Always scope to a specific subpath: `extra/<repo>/src/`, `extra/<name>_docs/`
- Passing the subpath directly respects the repo's own .gitignore (desirable)
- For broad searching, use a Task agent instead

## Exploring Reference Material

**Small files - read directly:**
- Single markdown documents
- Images/screenshots
- Small config files
- Files you already know the path to

**Large codebases - use Task tool agents:**

Directly reading entire reference codebases pollutes your context window. Instead:

1. Review your available Task tool agents (Explore, codebase-analyzer, etc.)
2. Choose an appropriate agent for the task
3. Dispatch it to explore and summarize

**Example:**
```
Use Task tool with subagent_type=Explore:
- Prompt: "In extra/ratatui/, find how borders are implemented.
  Return: file paths, key types/functions, and a brief explanation."
- The subagent explores, you receive a concise summary
```

**When to use agents:**
- Searching for implementation patterns in cloned repos
- Understanding library architecture
- Finding specific APIs or types
- Generating documentation from source

**What to do directly:**
- `ls extra/` to see what's available
- `find` to locate files by name
- Scoped `rg` to verify something exists (always pass subpath, never top-level extra/)
- Read single markdown/text files
- View images and screenshots

## HALT Behavior (Hard Stop)

If required material is not in `extra/`:

1. **HALT immediately** - stop current task
2. **Report what's missing** with specific suggestions
3. **Wait for user** - do NOT fall back to web search

**HALT message format:**
```
HALT: Missing reference material.

Required: <what you need>
Suggestion: <how to add it>

Example commands:
  git clone <url> extra/<name>
  # or
  Add file: extra/<name>.md
```

**Example HALT:**
```
HALT: Missing reference material.

Required: Ratatui widget implementation patterns
Suggestion: Clone ratatui source:
  git clone https://github.com/ratatui/ratatui extra/ratatui

Required: API documentation for external service
Suggestion: Save docs to extra/service_api.md or extra/service_docs/
```

## Adding Material

With user permission, add material directly:

```bash
# Clone reference repos
git clone https://github.com/org/repo extra/repo

# Create doc folders
mkdir -p extra/screenshots

# Download specific files
curl -o extra/spec.pdf https://example.com/spec.pdf
```

**Naming conventions:**
- Repos: `extra/<repo-name>/` (use original repo name)
- Docs: `extra/<name>_docs/` or `extra/<name>.md`
- Screenshots: `extra/screenshots/<descriptive-name>.png`

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Web searching instead of checking extra/ | Always `ls extra/` first |
| Looking for extra/ in worktree path | Use project root path |
| Proceeding without required material | HALT and ask user |
| Creating extra/ in worktree | Create in project root only |
