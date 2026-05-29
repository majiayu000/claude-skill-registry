---
name: setperms
description: "Set tool permissions for Claude Code. Configures allowed commands, rules, and preferences in .claude/ directory. Triggers on: setperms, init tools, configure permissions, setup project, set permissions, init claude."
allowed-tools: "Read Write Bash"
compatibility: "Creates project-local .claude/ configuration."
depends-on: []
related-skills: []
---

# /setperms

Initialize Claude Code with modern dev-shell-tools for a comfortable development experience.

## What This Does

**Installs complete dev environment setup:**

1. **Permissions** (`.claude/settings.local.json`) - Pre-approved CLI tools
2. **Rules** (`.claude/rules/cli-tools.md`) - Instructions to prefer modern tools

Tools from [dev-shell-tools](https://github.com/0xDarkMatter/dev-shell-tools):

**Core Tools:**
- **Git**: Full git access, lazygit, gh (GitHub CLI), delta, difft
- **File ops**: ls, mkdir, cat, wc, tree, eza, bat, chmod
- **Search**: rg (ripgrep), fd, fzf, ast-grep/sg
- **Navigation**: zoxide/z, broot/br
- **Data processing**: jq, yq, sd, xargs
- **Analysis**: tokei, procs, hyperfine, dust

**Dev Tools:**
- **Package managers**: npm, node, python, uv, pip, brew
- **Task runners**: just, bash
- **Network**: curl, http (httpie), firecrawl
- **Documentation**: tldr
- **Windows**: powershell

**AI CLI Tools:**
- **gemini**: Google Gemini CLI (2M context)
- **claude**: Anthropic Claude CLI
- **codex**: OpenAI Codex CLI
- **perplexity**: Perplexity CLI (web search)

## Execution Flow

```
/setperms
    |
    +-- Check for existing .claude/ files
    |     +-- If exists: Ask to overwrite or skip
    |     +-- If not: Proceed
    |
    +-- Create .claude directory
    +-- Create .claude/rules directory
    |
    +-- Write settings.local.json (permissions)
    +-- Write rules/cli-tools.md (tool preferences)
```

## Instructions

### Step 1: Check for existing settings

```bash
ls -la .claude/settings.local.json 2>/dev/null
ls -la .claude/rules/cli-tools.md 2>/dev/null
```

If files exist, ask user:
- **Overwrite**: Replace entirely
- **Skip**: Keep existing, do nothing

### Step 2: Create directories

```bash
mkdir -p .claude/rules
```

### Step 3: Write permissions file

Write to `.claude/settings.local.json`:

```json
{
  "permissions": {
    "allow": [
      "Bash(git:*)",
      "Bash(ls:*)",
      "Bash(mkdir:*)",
      "Bash(cat:*)",
      "Bash(wc:*)",
      "Bash(tree:*)",
      "Bash(curl:*)",
      "Bash(rg:*)",
      "Bash(fd:*)",
      "Bash(fzf:*)",
      "Bash(z:*)",
      "Bash(zoxide:*)",
      "Bash(br:*)",
      "Bash(broot:*)",
      "Bash(ast-grep:*)",
      "Bash(sg:*)",
      "Bash(bat:*)",
      "Bash(eza:*)",
      "Bash(delta:*)",
      "Bash(difft:*)",
      "Bash(jq:*)",
      "Bash(yq:*)",
      "Bash(sd:*)",
      "Bash(lazygit:*)",
      "Bash(gh:*)",
      "Bash(tokei:*)",
      "Bash(uv:*)",
      "Bash(just:*)",
      "Bash(http:*)",
      "Bash(procs:*)",
      "Bash(hyperfine:*)",
      "Bash(npm:*)",
      "Bash(node:*)",
      "Bash(python:*)",
      "Bash(pip:*)",
      "Bash(powershell -Command:*)",
      "Bash(powershell.exe:*)",
      "Bash(bash:*)",
      "Bash(chmod:*)",
      "Bash(xargs:*)",
      "Bash(command -v:*)",
      "Bash(brew:*)",
      "Bash(tldr:*)",
      "Bash(dust:*)",
      "Bash(btm:*)",
      "Bash(bottom:*)",
      "Bash(firecrawl:*)",
      "Bash(gemini:*)",
      "Bash(claude:*)",
      "Bash(codex:*)",
      "Bash(perplexity:*)"
    ],
    "deny": [],
    "ask": [
      "Bash(git reset --hard:*)",
      "Bash(git checkout -- :*)",
      "Bash(git clean -f:*)",
      "Bash(git stash drop:*)",
      "Bash(git stash clear:*)",
      "Bash(git restore --worktree:*)",
      "Bash(git push --force:*)",
      "Bash(git push -f:*)",
      "Bash(git push origin --force:*)",
      "Bash(git push origin -f:*)",
      "Bash(git branch -D:*)"
    ]
  },
  "hooks": {}
}
```

### Step 4: Write rules file

Write to `.claude/rules/cli-tools.md`:

```markdown
# CLI Tool Preferences (dev-shell-tools)

ALWAYS prefer modern CLI tools over traditional alternatives.

## File Search & Navigation

| Instead of | Use | Why |
|------------|-----|-----|
| `find` | `fd` | 5x faster, respects .gitignore |
| `grep` | `rg` (ripgrep) | 10x faster, respects .gitignore |
| `ls` | `eza` | Git status, tree view |
| `cat` | `bat` | Syntax highlighting |
| `cd` + manual | `z`/`zoxide` | Frecent directories |
| `tree` | `eza --tree` | Interactive |

## Data Processing

| Instead of | Use |
|------------|-----|
| `sed` | `sd` |
| Manual JSON | `jq` |
| Manual YAML | `yq` |

## Git Operations

| Instead of | Use |
|------------|-----|
| `git diff` | `delta` or `difft` |
| Manual git | `lazygit` |
| GitHub web | `gh` |

## Code Analysis

- Line counts: `tokei`
- AST search: `ast-grep` / `sg`
- Benchmarks: `hyperfine`
- Disk usage: `dust`

## System Monitoring

| Instead of | Use |
|------------|-----|
| `du -h` | `dust` |
| `top`/`htop` | `btm` (bottom) |

## Documentation

| Instead of | Use |
|------------|-----|
| `man <cmd>` | `tldr <cmd>` |

## Python

| Instead of | Use |
|------------|-----|
| `pip` | `uv` |
| `python -m venv` | `uv venv` |

## Task Running

Prefer `just` over Makefiles.

## Web Fetching

| Priority | Tool | When to Use |
|----------|------|-------------|
| 1 | `WebFetch` | First attempt - fast, built-in |
| 2 | `r.jina.ai/URL` | JS-rendered pages, cleaner extraction |
| 3 | `firecrawl <url>` | Anti-bot bypass, blocked sites |

## AI CLI Tools

For multi-model analysis:

| Tool | Model | Best For |
|------|-------|----------|
| `gemini` | Gemini 2.5 | 2M context, large codebases |
| `claude` | Claude | Coding, analysis |
| `codex` | OpenAI | Deep reasoning |
| `perplexity` | Perplexity | Web search, current info |

## Git Safety

Destructive commands require confirmation (in "ask" list):

| Command | Risk | Safe Alternative |
|---------|------|------------------|
| `git reset --hard` | Loses uncommitted changes | `git stash` first |
| `git checkout -- <file>` | Discards file changes | `git stash` or `git diff` first |
| `git clean -fd` | Deletes untracked files | `git clean -n` (dry run) first |
| `git stash drop` | Permanently deletes stash | Check `git stash list` first |
| `git push --force` | Overwrites remote history | `git push --force-with-lease` |
| `git branch -D` | Deletes unmerged branch | `git branch -d` (safe delete) |

**Before destructive operations:**
1. Check status: `git status`
2. Check for uncommitted changes: `git diff`
3. Consider stashing: `git stash`
4. Use dry-run flags when available

Reference: https://github.com/0xDarkMatter/dev-shell-tools
```

### Step 5: Confirm

Report to user:
```
Initialized Claude Code with dev-shell-tools:

Created:
  .claude/settings.local.json  (51 tool permissions, 11 guardrails)
  .claude/rules/cli-tools.md   (modern tool preferences)

Claude will now:
  - Auto-approve dev-shell-tools commands
  - Prefer fd over find, rg over grep, bat over cat, etc.
  - Use AI CLIs for multi-model analysis
  - Ask before destructive git commands (reset --hard, push --force, etc.)

To customize: edit files in .claude/
To add to git: git add .claude/
```

## Options

| Flag | Effect |
|------|--------|
| `--force` | Overwrite existing without asking |
| `--perms-only` | Only install permissions, skip rules |
| `--rules-only` | Only install rules, skip permissions |
| `--minimal` | Minimal permissions (git, ls, cat, mkdir only) |
| `--full` | Add cloud/container tools (docker, kubectl, terraform, etc.) |
| `--no-guardrails` | Skip git safety guardrails (empty "ask" list) |

### Full Template (--full)

Adds to permissions:
```json
"Bash(docker:*)",
"Bash(docker-compose:*)",
"Bash(podman:*)",
"Bash(kubectl:*)",
"Bash(helm:*)",
"Bash(terraform:*)",
"Bash(pulumi:*)",
"Bash(aws:*)",
"Bash(gcloud:*)",
"Bash(az:*)",
"Bash(wrangler:*)",
"Bash(flyctl:*)",
"Bash(railway:*)"
```

## Notes

- Permissions are project-local (don't affect other projects)
- Rules instruct Claude to prefer modern tools
- Global settings in `~/.claude/` still apply
- Changes take effect on next tool use (no restart needed)
- Tools from: https://github.com/0xDarkMatter/dev-shell-tools
