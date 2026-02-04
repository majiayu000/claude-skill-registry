---
name: audit-permissions
description: >-
  This skill should be used when the user asks to "audit claude permissions",
  "audit permissions", "review local claude settings", "promote permissions to global",
  "clean up claude settings", "find permission patterns", or wants to identify
  project-local Claude Code permissions that should be added to global configuration.
allowed-tools: Bash, Read, Write
---

# Audit Claude Permissions

Scan project-local Claude Code settings files, aggregate permission patterns, and recommend promotions to global configuration.

## Workflow Overview

This audit runs in three phases, each as a separate task. Use TaskCreate at the start to create all three tasks, then work through them sequentially with user input via AskUserQuestion.

**Phase 1: Promote to Global** - Review candidates and add selected permissions to global config
**Phase 2: Clean Up Redundant** - Remove local permissions now covered by global
**Phase 3: Security Hygiene** - Review and remove risky or stale permissions

## Pre-flight Check

To avoid permission prompts during the audit, consider adding these to global settings:

- `Read(~/.claude/settings.json)` - read global settings
- `Read(**/.claude/settings.local.json)` - read all local settings files

## Initial Setup

1. Run the discovery and extraction pipeline:

```bash
${CLAUDE_PLUGIN_ROOT}/skills/audit-permissions/scripts/discover-settings.sh | xargs ${CLAUDE_PLUGIN_ROOT}/skills/audit-permissions/scripts/extract-permissions.py
```

2. Read global settings from `~/.claude/settings.json`

3. Create tasks for the three phases:

```
TaskCreate: "Review and promote permissions to global config"
TaskCreate: "Clean up redundant local permissions"
TaskCreate: "Review security hygiene issues"
```

4. Analyze the data and categorize permissions (see Categorization Rules below)

---

## Phase 1: Promote to Global

**Goal:** Identify permissions worth adding to global config and get user approval.

### Present Findings

Show a summary table of promotion candidates:

```markdown
## Promotion Candidates

### Strong Recommendations (safe patterns, multiple projects)

| Permission | Projects | Suggested Global Pattern |
| ---------- | -------- | ------------------------ |
| ...        | ...      | ...                      |

### Moderate Recommendations (review carefully)

| Permission | Projects | Notes |
| ---------- | -------- | ----- |
| ...        | ...      | ...   |

### Cross-Project File Patterns

[If any Read/Write/Edit permissions reference paths outside their project directory
and appear in multiple projects, flag them here. Example: multiple projects have
`Write(~/.config/some-tool/config.json)` - might indicate a shared config worth
adding globally.]
```

### Get User Decision

Use AskUserQuestion to let the user decide:

```
Question: "Which permissions should I add to global settings?"
Options:
- "Add all strong recommendations"
- "Add strong + moderate recommendations"
- "Let me pick specific ones" (then list individually)
- "Skip - don't add any"
```

### Apply Changes

If user approves additions:

1. Add selected permissions to `~/.claude/settings.json`
2. Respect existing logical groupings (git, nix, gh, etc.)
3. Sort alphabetically within groups
4. Mark Phase 1 task as completed

---

## Phase 2: Clean Up Redundant

**Goal:** Remove local permissions that are now covered by global config.

### Preview Cleanup

Run the cleanup script in dry-run mode:

```bash
${CLAUDE_PLUGIN_ROOT}/skills/audit-permissions/scripts/discover-settings.sh | ${CLAUDE_PLUGIN_ROOT}/skills/audit-permissions/scripts/cleanup-redundant.py
```

### Present Findings

Show what would be removed:

```markdown
## Redundant Permissions

| File      | Permissions to Remove | Remaining |
| --------- | --------------------- | --------- |
| project-a | 5 (ls:_, grep:_, ...) | 12        |
| project-b | 3 (gh api:\*, ...)    | 8         |
| ...       | ...                   | ...       |

**Total:** X permissions across Y files
```

### Get User Decision

Use AskUserQuestion:

```
Question: "Should I remove these redundant permissions from local files?"
Options:
- "Yes, clean them up"
- "Show me the full list first"
- "Skip cleanup"
```

### Apply Changes

If user approves:

```bash
${CLAUDE_PLUGIN_ROOT}/skills/audit-permissions/scripts/discover-settings.sh | ${CLAUDE_PLUGIN_ROOT}/skills/audit-permissions/scripts/cleanup-redundant.py --apply
```

Mark Phase 2 task as completed.

---

## Phase 3: Security Hygiene

**Goal:** Identify and remove risky, stale, or overly broad permissions.

### Identify Issues

Flag permissions that match these patterns:

**High Risk (recommend removal):**

- `Bash(curl:*)`, `Bash(wget:*)` - network exfiltration risk
- `Bash(rm:*)` - can delete any file
- `Bash(source:*)` - executes arbitrary scripts
- `Bash(eval:*)` - arbitrary code execution

**Moderate Risk (review):**

- `Bash(git reset:*)`, `Bash(git checkout:*)` - can discard work
- `Bash(pkill:*)`, `Bash(kill:*)` - process termination
- `Bash(python:*)`, `Bash(python3:*)`, `Bash(node:*)` - arbitrary code (flag if user hasn't consciously chosen this)

**One-Off Cruft (safe to remove):**

- Hardcoded file paths (e.g., `Bash(, prettier --write /full/path/to/file.md)`)
- Incomplete shell constructs (`Bash(done)`, `Bash(for file in *.rs)`)
- Very specific commands with no wildcards that look like debugging artifacts
- Duplicate entries

**Cross-Project File Access:**

- `Read`, `Write`, or `Edit` permissions for paths outside the project
- Flag if the same external path appears in multiple projects (potential global candidate)
- Flag broad patterns like `Write(~/.config/*)` as security concerns

### Present Findings

```markdown
## Security Hygiene Review

### High Risk - Recommend Removal

| Permission     | Project   | Risk              |
| -------------- | --------- | ----------------- |
| `Bash(curl:*)` | project-x | Data exfiltration |
| ...            | ...       | ...               |

### Moderate Risk - Review

| Permission | Project | Risk |
| ---------- | ------- | ---- |
| ...        | ...     | ...  |

### One-Off Cruft

| Permission                                           | Project   |
| ---------------------------------------------------- | --------- |
| `Bash(, prettier --write /path/to/specific/file.md)` | project-y |
| ...                                                  | ...       |

### External File Access

| Permission                     | Projects   | Path                            |
| ------------------------------ | ---------- | ------------------------------- |
| `Write(~/.config/tool/config)` | 3 projects | Shared config - consider global |
| `Edit(/etc/hosts)`             | 1 project  | System file - review necessity  |
```

### Get User Decision

Use AskUserQuestion:

```
Question: "How should I handle the security hygiene items?"
Options:
- "Remove all flagged items"
- "Remove high risk + cruft only"
- "Let me review each category"
- "Skip - keep everything"
```

If user wants to review categories, ask about each:

- High risk items
- Moderate risk items
- One-off cruft
- External file access

### Apply Changes

Edit each affected `settings.local.json` to remove approved items.

Mark Phase 3 task as completed.

---

## Scripts

All scripts are in `${CLAUDE_PLUGIN_ROOT}/skills/audit-permissions/scripts/`.

- **`scripts/discover-settings.sh`** - Finds all `.claude/settings.local.json` files across `~` using `fd` with sensible exclusions (Library, node_modules, .git, etc.). Max depth of 5 for performance.
- **`scripts/extract-permissions.py`** - Aggregates permissions from multiple settings files. Outputs JSON with each permission, occurrence count, and list of projects using it. Sorted by count descending.
- **`scripts/cleanup-redundant.py`** - Removes permissions from local files that are covered by global config. Dry-run by default; use `--apply` to modify files.

**Usage examples:**

```bash
# Extract and aggregate all permissions
${CLAUDE_PLUGIN_ROOT}/skills/audit-permissions/scripts/discover-settings.sh | xargs ${CLAUDE_PLUGIN_ROOT}/skills/audit-permissions/scripts/extract-permissions.py

# Preview redundant permission cleanup (dry-run, default)
${CLAUDE_PLUGIN_ROOT}/skills/audit-permissions/scripts/discover-settings.sh | ${CLAUDE_PLUGIN_ROOT}/skills/audit-permissions/scripts/cleanup-redundant.py

# Actually remove redundant permissions
${CLAUDE_PLUGIN_ROOT}/skills/audit-permissions/scripts/discover-settings.sh | ${CLAUDE_PLUGIN_ROOT}/skills/audit-permissions/scripts/cleanup-redundant.py --apply
```

---

## Categorization Rules

### Reasonable Global Candidates

Patterns worth promoting. These operate on local project code or perform read-only operations.

**Git Commands (read-only):**
`git branch:*`, `git diff:*`, `git log:*`, `git show:*`, `git status:*`

**File Inspection (read-only):**
`cat:*`, `head:*`, `tail:*`, `ls:*`, `find:*`, `grep:*`, `du:*`

**Build and Check Commands:**
`cargo build:*`, `cargo test:*`, `cargo check:*`, `go build:*`, `go test:*`,
`npm run build:*`, `npm run test:*`, `deno check:*`, `deno lint:*`, `xcodebuild:*`

**System Utilities:**
`open:*`, `pbcopy`, `pbpaste`, `lsof:*`, `ps:*`

**Nix Commands:**
`nix build:*`, `nix-build:*`, `nix develop:*`, `nix eval:*`, `nix flake:*`,
`nix path-info:*`, `nix-prefetch-url:*`, `nh darwin build:*`

**Homebrew (read-only):**
`brew info:*`, `brew search:*`

**GitHub CLI:**
`gh api:*`, `gh issue list:*`, `gh issue view:*`, `gh pr list:*`, `gh pr view:*`,
`gh pr diff:*`, `gh pr checks:*`, `gh search:*`, `gh run list:*`, `gh run view:*`

**Wildcards:**
`* --help *`, `* --version`

### Pattern Generalization

When promoting, generalize cautiously - only for safe patterns:

| Local Pattern                 | Global Pattern          | Notes                        |
| ----------------------------- | ----------------------- | ---------------------------- |
| `Bash(npm run build)`         | `Bash(npm run build:*)` | Safe - runs project scripts  |
| `Bash(cargo test --release)`  | `Bash(cargo test:*)`    | Safe - tests local code      |
| `Bash(nix build .#package)`   | `Bash(nix build:*)`     | Safe - sandboxed builds      |
| `Bash(python3 script.py)`     | Keep specific or skip   | Risky - arbitrary code       |
| `WebFetch(domain:github.com)` | Keep as-is              | Domain patterns don't change |

### Formatting Rules for Global Settings

When adding to `~/.claude/settings.json`:

- Respect existing logical groupings (git, file inspection, nix, brew, gh, system utilities, build tools, wildcards, Skills, MCP tools)
- Within each group, sort alphabetically
- Place new permissions in the appropriate group based on command prefix
