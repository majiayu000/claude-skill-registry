---
name: project-kickoff
description: "Bootstrap new projects with curated settings.local.json permissions, CLAUDE.md, and .gitignore. Detects project type and generates comprehensive permission presets so you never get prompted. Auto-discovers connected MCP servers. Also tidies existing messy settings files. Trigger with 'kickoff', 'new project', 'bootstrap', 'setup claude', 'tidy permissions', 'clean settings', or 'init project'."
compatibility: claude-code-only
---

# Project Kickoff

Bootstrap a new project so Claude Code has the right permissions from the start. The goal is **zero permission prompts** after setup — every command you'd reasonably use should be pre-approved.

**Problem**: Every new project accumulates permission approvals one click at a time. Project `settings.local.json` shadows global settings (does not merge), so each project needs its own complete list. This skill generates that list upfront.

**Output**: `settings.local.json`, `CLAUDE.md`, `.gitignore` (and optionally git init + GitHub repo).

## Operating Modes

### Mode 1: New Project Setup

**When**: Starting a new project, or working in a directory without `.claude/settings.local.json`.

**Steps**:

1. **Detect project type** from files present in the directory:

   | Indicator | Type |
   |-----------|------|
   | `wrangler.jsonc` or `wrangler.toml` | cloudflare-worker |
   | `vercel.json` or `next.config.*` | vercel-app |
   | `package.json` (no deploy target) | javascript-typescript |
   | `pyproject.toml` or `setup.py` or `requirements.txt` | python |
   | `Cargo.toml` | rust |
   | `go.mod` | go |
   | `Gemfile` or `Rakefile` | ruby |
   | `composer.json` or `wp-config.php` | php |
   | `Dockerfile` or `docker-compose.yml` | docker |
   | `.claude/agents/` or operational scripts | ops-admin |
   | Empty directory | Ask the user |

   If ambiguous, ask. Types can stack (e.g. cloudflare-worker + javascript-typescript).

2. **Generate `.claude/settings.local.json`**:

   Read [references/permission-presets.md](references/permission-presets.md) for preset definitions, then:

   a. **Always include Universal Base** — file ops, text processing, network, system, git. These are needed by every project.

   b. **Add detected language presets** — JS/TS, Python, PHP, Go, Rust, Ruby, etc. When in doubt, include more rather than less. Adding `Bash(cargo *)` to a JS project costs nothing if Rust isn't installed.

   c. **Add deployment presets** if detected — Cloudflare Worker, Vercel, Docker, Cloud CLIs.

   d. **Auto-discover MCP servers** — Use `ToolSearch` to find available MCP tools, extract the unique server names from tool names (e.g. `mcp__vault__secret_list` → server is `vault`), and generate `mcp__servername__*` for each. This is necessary because:
      - `mcp__*` (single wildcard) does NOT work — wildcard doesn't cross `__` boundary
      - `mcp__*__*` (double wildcard) also does NOT work
      - Each server must be listed individually: `mcp__vault__*`, `mcp__brain__*`, etc.

   e. **Always include**: `WebSearch`, `WebFetch`

   f. **Always include explicit `gh` subcommands** alongside `Bash(gh *)` — there's a known bug where `Bash(gh *)` doesn't match some subcommands:
      ```
      "Bash(gh *)",
      "Bash(gh repo *)",
      "Bash(gh issue *)",
      "Bash(gh pr *)",
      "Bash(gh api *)",
      "Bash(gh search *)",
      "Bash(gh run *)",
      "Bash(gh release *)",
      ```

   g. Write with `//` comment groups for organisation.

   h. Warn the user: **"Project settings.local.json SHADOWS your global settings — it does not merge. A session restart is needed for changes to take effect."**

3. **Generate `CLAUDE.md`**:
   - Read [references/claude-md-templates.md](references/claude-md-templates.md) for templates
   - Fill in: project name (from directory name or ask), today's date, detected stack
   - Pre-fill Jez's defaults (Cloudflare account ID, pnpm, EN-AU)

4. **Generate `.gitignore`**:
   - Use the type-appropriate template from [references/claude-md-templates.md](references/claude-md-templates.md)
   - Always include `.claude/settings.local.json` and `.dev.vars`

5. **Optionally** (ask first):
   - `git init` + first commit
   - `gh repo create jezweb/[name] --private` + push

### Mode 2: Tidy Existing Permissions

**When**: User says "tidy permissions", "clean settings", or the existing `settings.local.json` has more than ~50 entries.

**Steps**:

1. Run the tidy script to analyse the current file:
   ```bash
   python3 ${SKILL_DIR}/scripts/tidy_permissions.py .claude/settings.local.json
   ```

2. Review the report. It flags:
   - **Leaked secrets**: API keys, tokens, hex strings embedded in approval patterns
   - **Shell fragments**: `Bash(do)`, `Bash(fi)`, `Bash(then)`, `Bash(else)`, `Bash(done)`
   - **Legacy colon syntax**: `Bash(git:*)` → should be `Bash(git *)`
   - **Duplicates**: Entries covered by a broader pattern already present (e.g. `Bash(git add *)` is redundant if `Bash(git *)` exists)
   - **One-time entries**: Entire commit messages, hardcoded paths that will never match again
   - **Consolidation opportunities**: e.g. 5 separate `Bash(git add:*)`, `Bash(git commit:*)` could become `Bash(git *)`
   - **Missing MCP servers**: Compare connected servers vs. what's in the allow list

3. Present the cleaned version with a diff showing what changed.

4. Apply after user confirmation. Recommend the user rotate any leaked secrets.

### Mode 3: Add Preset

**When**: User says "add python permissions", "add MCP permissions", or "add docker permissions" to an existing project.

**Steps**:

1. Read the relevant preset section from [references/permission-presets.md](references/permission-presets.md)
2. Read the existing `.claude/settings.local.json`
3. Merge without duplicating — add new entries, keep existing groups
4. Write the updated file
5. Remind user: **session restart required** for changes to take effect

## MCP Server Auto-Discovery

To discover connected MCP servers, run these ToolSearch queries:

```
ToolSearch("+brain")
ToolSearch("+vault")
ToolSearch("+playwright")
ToolSearch("+gmail")
ToolSearch("+xero")
```

Or search broadly: `ToolSearch("mcp")` and extract unique server prefixes from returned tool names.

Each discovered server gets a wildcard entry: `mcp__servername__*`

## Permission Syntax Quick Reference

| Pattern | Meaning |
|---------|---------|
| `Bash(git *)` | Preferred — space before `*` = word boundary |
| `Bash(nvidia-smi)` | Exact match, no arguments |
| `WebFetch` | Blanket web fetch (all domains) |
| `WebFetch(domain:x.com)` | Domain-scoped web fetch |
| `WebSearch` | Blanket web search |
| `mcp__brain__*` | All tools on one server |
| `mcp__brain__brain_sites` | One specific MCP tool |

### What Does NOT Work

| Pattern | Why |
|---------|-----|
| `mcp__*` | Wildcard doesn't cross `__` boundary |
| `mcp__*__*` | Still doesn't work — segments aren't glob-expanded |
| `Bash(git:*)` | Deprecated colon syntax (still works but prefer space) |

### Important Behaviours

- **Not hot-reloaded**: Edits to `settings.local.json` require a **session restart**
- **"Don't ask again"** injects at runtime (no restart needed) using legacy colon format — this is normal
- **Shadows, not merges**: Project `settings.local.json` completely replaces global allow list
- **Shell safety**: `Bash(git *)` won't match `git add && rm -rf /` — operators are handled safely
- **`gh` bug**: `Bash(gh *)` sometimes doesn't match subcommands — include explicit `Bash(gh issue *)` etc. as workaround

## Autonomy

- **Just do it**: Detect project type, read existing files, auto-discover MCP servers
- **Brief confirmation**: Write settings.local.json, CLAUDE.md, .gitignore (show what will be written)
- **Ask first**: git init, GitHub repo creation, overwriting existing files, applying tidy fixes

## Reference Files

| When | Read |
|------|------|
| Building permission presets | [references/permission-presets.md](references/permission-presets.md) |
| Generating CLAUDE.md and .gitignore | [references/claude-md-templates.md](references/claude-md-templates.md) |
