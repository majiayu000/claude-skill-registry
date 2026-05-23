---
version: 1.5.0
name: meta-bootstrap
description: >
  Install the agentic workflow into a project. Sets up context files, adopts skills,
  configures the docs repo connection, and adds the heartbeat to CLAUDE.md. Use when
  the user says "set up the workflow", "bootstrap this project", "install the workflow",
  or "make this project workflow-aware".
disable-model-invocation: true
user-invocable: true
argument-hint: "[target-project-path] [--docs-repo path]"
---

# Bootstrap — Install Workflow into a Project

Sets up the agentic heartbeat workflow in a target project, connecting it to a
shared documentation repository.

## Prerequisites

Before running, confirm with the user:
1. **Target project path** — where to install (default: current working directory)
2. **Docs repo name** — the shared documentation repo name (e.g., `my-docs`)
3. **Workflow repo name** — where agentic-workflow lives (default: `agentic-workflow`)

## Step 1: Validate Paths

1. Confirm the target project exists and is a git repo
2. Confirm the docs repo exists
3. Confirm the workflow repo exists (for copying templates)
4. Check if the target already has a `workflow.json` — if so, this is a re-bootstrap (update, don't overwrite)

## Step 2: Create workflow.json

Create `workflow.json` in the target project root:

```json
{
  "docsRepo": "<docs-repo-name>",
  "workflowRepo": "<workflow-repo-name>",
  "project": {
    "name": "<project-name>",
    "type": "<api|frontend|library|docs>"
  },
  "docs": {
    "templates": "templates",
    "output": {
      "adr": "adr",
      "rfc": "rfc",
      "design": "design",
      "prd": "prd",
      "runbook": "runbooks",
      "postmortem": "postmortems",
      "spike": "spikes",
      "architecture": "architecture"
    }
  }
}
```

Use **repo names** (not paths) for `docsRepo` and `workflowRepo`. The `resolve-repo` script
(`.claude/skills/tool-worktree/scripts/resolve-repo.ps1`) in `tool-worktree`
resolves names to actual paths at runtime, supporting bare+worktree, agentsandbox, and normal clone layouts. Output paths are relative to the resolved docs repo root.

## Step 3: Set Up Context Directory

Create the context structure if it doesn't exist:

```
context/
├── SOUL.md              # Copy from workflow repo, customize for this project
├── USER.md              # Copy template from workflow repo
├── MEMORY.md            # Create empty with section headers
└── memory/
    └── archive/
```

- **SOUL.md**: Copy the base from the workflow repo, then ask the user if they want to customize it for this project's tech stack and patterns
- **USER.md**: Check these locations in order, use the first one found:
  1. Target project's existing `context/USER.md` (keep it, don't overwrite)
  2. The main worktree's `context/USER.md` (for bare+worktree repos: `../{main-branch}/context/USER.md` — USER.md is gitignored so it won't exist in new worktrees, but the main worktree likely has one)
  3. The workflow repo's `context/USER.md` (canonical, most up-to-date)
  4. Create from template as a last resort
- **MEMORY.md**: Create with empty section headers

## Step 4: Copy Templates to Docs Repo

Check if the docs repo already has `templates/`:
- If not: copy all templates from the workflow repo's `templates/` directory
- If yes: compare and report any differences (newer templates in workflow repo)

Templates to copy:
- `prd.md`, `rfc.md`, `design-doc.md`, `adr.md`
- `c4-diagrams.md`, `runbook.md`, `postmortem.md`, `spike.md`

Also create output directories in the docs repo if they don't exist:
- `prd/`, `rfc/`, `design/`, `runbooks/`, `postmortems/`, `spikes/`
- `adr/` and `architecture/` likely already exist

## Step 5: Install Skills

Copy skills from the workflow repo to the target project's `.claude/skills/`:

**Always install (core workflow):**
- `meta-heartbeat/` — session startup
- `meta-wrap-up/` — session end
- `meta-skill-catalog/` — skill registry
- `meta-adopt-skill/` — external skill adoption

**Install if not already present (documentation):**
- `doc-prd/`, `doc-rfc/`, `doc-design/`, `doc-adr/`
- `doc-runbook/`, `doc-postmortem/`, `doc-spike/`
- `viz-c4-diagram/`
- `tool-vitepress/`

For each skill:
1. Create the directory under `.claude/skills/`
2. Copy the SKILL.md (the version from workflow repo is the source of truth)
3. If the target project already has a skill with the same name, warn and ask

**DO NOT overwrite** existing project-specific skills (like `playwright-cli`, `perf-debugging`).

**Install based on project type (development):**

Read `project.type` from `workflow.json` and install dev skills accordingly:

| Skill | api | frontend | library | docs |
|-------|-----|----------|---------|------|
| `dev-dependency-backend` | yes | no | yes | no |
| `dev-dependency-frontend` | no | yes | no | no |
| `dev-security-backend` | yes | no | yes | no |
| `dev-security-frontend` | no | yes | no | no |
| `dev-tdd-backend` | yes | no | yes | no |
| `dev-tdd-frontend` | no | yes | no | no |
| `dev-verification-backend` | yes | no | yes | no |
| `dev-verification-frontend` | no | yes | no | no |
| `dev-dependency` (router) | yes | yes | yes | no |
| `dev-security` (router) | yes | yes | yes | no |
| `dev-tdd` (router) | yes | yes | yes | no |
| `dev-verify` (router) | yes | yes | yes | no |
| `dev-blueprint` | yes | yes | yes | no |
| `dev-iterative-retrieval` | yes | yes | yes | no |
| `dev-search-first` | yes | yes | yes | no |
| `dev-perf` | yes | yes | yes | no |
| `dev-commit` | yes | yes | yes | yes |

Routers: only install if at least one sub-skill for that router is installed.
For `docs` project type: skip all dev-* skills except `dev-commit` (every project makes commits).

**Conditional .NET skills (install based on project detection):**

For .NET projects (detected by presence of `*.csproj` or `*.sln` files):

```bash
# Always install for .NET projects
# dev-dotnet-migrate — version migration assistant
```

```bash
# Detect EF Core usage
grep -rl "Microsoft.EntityFrameworkCore" --include="*.csproj" . 2>/dev/null
# If found → install dev-dotnet-efcore
# If not → skip
```

```bash
# Detect MSBuild complexity (3+ csproj files OR Directory.Build.props exists)
CSPROJ_COUNT=$(find . -name "*.csproj" -not -path "*/bin/*" -not -path "*/obj/*" | wc -l)
test -f Directory.Build.props && HAS_DIR_BUILD=true || HAS_DIR_BUILD=false
# If CSPROJ_COUNT >= 3 OR HAS_DIR_BUILD == true → install dev-dotnet-build
# If not → skip
```

**Conditional agent installation:**

```bash
# If dev-dotnet-build is installed → copy dotnet-build-resolver agent
# If dev-perf exists → copy dotnet-perf-analyst agent
# Create .claude/agents/ directory if installing any agents
```

## Step 5b: Install Hooks

Copy hook scripts from the workflow repo to the target project:

1. Create `.claude/hooks/` directory in the target project
2. Copy all hook scripts:
   - `on-prompt-submit.ps1` — detects wrap-up intent ("bye", "exit", "/exit", "done", etc.) and injects wrap-up instructions
   - `on-pre-compact.ps1` — flushes session context to daily memory before context compaction
   - `on-session-end.ps1` — appends session end marker to daily memory, updates session count
3. Make scripts executable (`chmod +x`)
4. Merge hook configuration into the project's `.claude/settings.local.json`:
   - Read `.claude/hooks/settings-hooks.json` from the workflow repo
   - Merge the `hooks` section into the target's `.claude/settings.local.json`
   - If the target already has hooks configured, merge without overwriting existing hooks
   - Use `settings.local.json` (not `settings.json`) because it is gitignored — hooks
     reference pwsh scripts installed by bootstrap, which are environment-specific
5. Copy the opencode plugin for cross-tool compatibility:
   - Create `.opencode/plugins/` directory in the target project
   - Copy `.opencode/plugins/hooks.ts` from the workflow repo
   - Copy `.opencode/package.json` from the workflow repo
   - This lets opencode call the same `.ps1` hooks via its plugin system

## Step 6: Initialize Catalog

Create or update `.claude/skills/meta-skill-catalog/catalog.json`:
- If no catalog exists: create one with all installed skills
- If catalog exists: merge new skills into it, preserving existing entries
- For each installed skill, populate version tracking fields:
  - `version`: read from the skill's SKILL.md frontmatter
  - `installed_from`: `"agentic-workflow"`
  - `installed_version`: same as `version` (freshly installed)
  - `installed_date`: today's date (YYYY-MM-DD)

## Step 7: Update CLAUDE.md

Append the heartbeat section to the project's existing CLAUDE.md. If CLAUDE.md doesn't exist, create it.

**Do NOT replace** existing CLAUDE.md content. Append at the end:

```markdown

## Heartbeat

Before doing anything else in any session:

1. Read `context/SOUL.md` — who you are, how you behave
2. Read `context/USER.md` — who you're helping and their preferences
3. Read `context/MEMORY.md` — long-term curated knowledge
4. Read `context/memory/{today}.md` + `context/memory/{yesterday}.md` — recent session context
5. **Create or open today's memory file** — if `context/memory/{YYYY-MM-DD}.md` doesn't exist, create it with a session start timestamp. If it already exists (second session today), append a new session header.
6. Read `workflow.json` — know where docs repo and templates live
7. Scan `context/` — flag anything older than 30 days
8. Greet the user briefly. Mention what you remember from recent sessions if relevant.

Don't ask permission for steps 1-6. Just do it.

## Workflow Config

This project uses a shared documentation repository. See `workflow.json` for paths.

- **Templates**: Document templates live in the docs repo
- **Output**: Generated docs (ADRs, RFCs, etc.) go to the docs repo
- **Skills**: Document generation skills read `workflow.json` for paths

## Memory

You wake up fresh each session. These files are your continuity:

- **Daily notes:** `context/memory/YYYY-MM-DD.md` — raw logs of what happened
- **Long-term:** `context/MEMORY.md` — curated wisdom, distilled from daily notes

### Memory Security
- **MEMORY.md only loads in main sessions** (direct chat with your human)
- **DO NOT load in shared contexts** (group chats, sub-agent sessions, CI)

### Write It Down — No "Mental Notes"
- When someone says "remember this" → update the daily file or MEMORY.md
- When you learn a lesson → update SOUL.md or MEMORY.md
- When you make a mistake → document it so future-you doesn't repeat it

## Commits

- Keep commit messages clean — no AI tool mentions or commercial branding
- No "Co-Authored-By" lines
- Verify before declaring done
```

## Step 7b: Create AGENTS.md Symlink

Create a symlink for opencode compatibility:

```bash
ln -s CLAUDE.md AGENTS.md
```

This lets opencode (which prefers `AGENTS.md`) read the same instructions as Claude Code.
Skip if `AGENTS.md` already exists.

## Step 8: Update .gitignore

Add these entries to the project's `.gitignore` if not already present:

```
# Workflow context (personal, don't share)
context/USER.md
context/MEMORY.md
context/memory/
CLAUDE.local.md
```

## Step 9: Present Summary

Show the user what was done:

```
### Workflow Bootstrap Complete

**Project:** {project-name}
**Docs repo:** {docs-repo-path}

#### Installed
- [x] workflow.json configured
- [x] context/ directory created (SOUL.md, USER.md template, MEMORY.md)
- [x] {N} templates copied to docs repo
- [x] {N} skills installed
- [x] Catalog initialized with {N} skills
- [x] Heartbeat added to CLAUDE.md
- [x] AGENTS.md symlink created (opencode compatibility)
- [x] .gitignore updated

#### Next Steps
1. Fill in `context/USER.md` with your details
2. Review and customize `context/SOUL.md` for this project
3. Start a new session — the heartbeat will run automatically
```

## Re-Bootstrap (Update)

If `workflow.json` already exists, this is an update:
- Compare installed skills vs workflow repo skills — report new/updated
- Compare templates — report changes
- Offer to update individual components
- Never overwrite context files (SOUL.md, USER.md, MEMORY.md) without asking
