---
name: audit-permissions
description: >-
  This skill should be used when the user asks to "audit claude permissions",
  "audit permissions", "review local claude settings", "promote permissions to global",
  "clean up claude settings", "find permission patterns", or wants to identify
  project-local Claude Code permissions that should be added to global configuration.
allowed-tools:
  # Scripts
  - Bash(*/audit-permissions/scripts/*)
  - Bash(readlink *)
  # Global settings
  - Read(~/.claude/settings.json)
  - Edit(~/.claude/settings.json)
  - Write(~/.claude/settings.json)
  # Local settings (per-project)
  - Read(**/.claude/settings.local.json)
  - Edit(**/.claude/settings.local.json)
  - Write(**/.claude/settings.local.json)
  # User preferences
  - Read(~/.claude/cc-maintenance.local.md)
  - Edit(~/.claude/cc-maintenance.local.md)
  - Write(~/.claude/cc-maintenance.local.md)
  # Policy detection
  - Read(~/.claude/CLAUDE.md)
---

# Audit Claude Permissions

Scan project-local Claude Code settings files, aggregate permission patterns, and recommend promotions to global configuration.

## Workflow Overview

This audit runs in three phases, each as a separate task. Use TaskCreate at the start to create all three tasks, then work through them sequentially with user input via AskUserQuestion.

- **Phase 1: Promote to Global** — Requires user judgment. Present candidates, get decisions, apply to global config.
- **Phase 2: Automated Redundancy Cleanup** — Script-driven. After Phase 1 promotions, run cleanup script to remove local permissions now covered by global. Present for sanity-checking, then apply.
- **Phase 3: Judgment Calls** — Everything requiring user input: security hygiene, policy conflicts, one-off cruft, empty file deletion, moderate-risk items.

## Initial Setup

1. **Check for symlinked global settings:**

```bash
readlink -f ~/.claude/settings.json
```

If the global settings file is a symlink, note the real path. All writes to `~/.claude/settings.json` must edit the symlink target, not create a new file that replaces the symlink.

2. **Load user preferences** from `~/.claude/cc-maintenance.local.md` (if it exists). See User Preferences section below. Apply any configured defaults (risk tolerance, auto-cleanup preference).

3. **Read global CLAUDE.md** from `~/.claude/CLAUDE.md` to identify tool preference policies for Phase 3 policy conflict detection.

4. **Run the discovery and extraction pipeline:**

```bash
scripts/discover-settings.sh | xargs scripts/extract-permissions.py
```

5. **Read the actual global settings** from `~/.claude/settings.json` — compare against the real allow list, not just the static examples in this skill.

6. **Create tasks** for the three phases:

```
TaskCreate: "Review and promote permissions to global config"
TaskCreate: "Automated redundancy cleanup"
TaskCreate: "Judgment calls: security, policy, and cruft"
```

7. **Analyze the data** and categorize permissions (see Categorization Rules below).

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

1. Add selected permissions to `~/.claude/settings.json` (or symlink target)
2. Respect existing logical groupings (git, nix, gh, etc.)
3. Sort alphabetically within groups
4. Use space-syntax: `Bash(cmd *)` not `Bash(cmd:*)`
5. Mark Phase 1 task as completed

---

## Phase 2: Automated Redundancy Cleanup

**Goal:** Remove local permissions now covered by global config. This is mechanical — the script identifies exact matches; user just sanity-checks the list.

### Preview Cleanup

Run the cleanup script in dry-run mode:

```bash
scripts/discover-settings.sh | scripts/cleanup-redundant.py
```

### Present Findings

Show what would be removed:

```markdown
## Redundant Permissions

| File      | Permissions to Remove | Remaining |
| --------- | --------------------- | --------- |
| project-a | 5 (ls _, grep _, ...) | 12        |
| project-b | 3 (gh api \*, ...)    | 8         |
| ...       | ...                   | ...       |

**Total:** X permissions across Y files
```

The script also normalizes any remaining colon-syntax (`Bash(cmd:*)`) to space-syntax (`Bash(cmd *)`) when applying.

### Get User Decision

If `auto_cleanup_redundant: true` in user preferences, skip the question and apply directly (still show the summary). Otherwise:

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
scripts/discover-settings.sh | scripts/cleanup-redundant.py --apply
```

Mark Phase 2 task as completed.

---

## Phase 3: Judgment Calls

**Goal:** Everything that requires real user judgment — security risks, policy conflicts, stale cruft, and cleanup opportunities. Present all categories together.

### Category A: Security Hygiene

Flag permissions that match these patterns:

**High Risk (recommend removal):**

- `Bash(curl *)`, `Bash(wget *)` — network exfiltration risk
- `Bash(rm *)` — can delete any file
- `Bash(source *)` — executes arbitrary scripts
- `Bash(eval *)` — arbitrary code execution

**Moderate Risk (review):**

- `Bash(git reset *)`, `Bash(git checkout *)` — can discard work
- `Bash(pkill *)`, `Bash(kill *)` — process termination
- `Bash(python *)`, `Bash(python3 *)`, `Bash(node *)` — arbitrary code (flag if user hasn't consciously chosen this)

Adjust what counts as "moderate" vs "high" based on the user's `risk_tolerance` preference if set.

### Category B: Policy Conflicts

Read the user's global `~/.claude/CLAUDE.md` for stated tool preferences. Flag local permissions that conflict with those policies.

**How to detect:** Look for patterns like "prefer X over Y", "use X instead of Y", "avoid Y". Then scan all local permissions for uses of the deprecated tool. For example:

> If CLAUDE.md says "prefer tool X over built-in Y", flag all `Y` permissions across local settings as policy conflicts.

Present these as informational — the user may have valid reasons for specific overrides.

### Category C: One-Off Cruft

- Hardcoded file paths (e.g., `Bash(prettier --write /full/path/to/file.md)`)
- Incomplete shell constructs (`Bash(done)`, `Bash(for file in *.rs)`)
- Very specific commands with no wildcards that look like debugging artifacts
- Duplicate entries
- Legacy colon-syntax permissions (`Bash(cmd:*)`) that weren't caught by the cleanup script (e.g., ones without a global equivalent)

### Category D: Cross-Project File Access

- `Read`, `Write`, or `Edit` permissions for paths outside the project
- Flag if the same external path appears in multiple projects (potential global candidate)
- Flag broad patterns like `Write(~/.config/*)` as security concerns

### Category F: MCP Tool Permissions

- Flag MCP tools with write/send/delete capabilities (message sending, data deletion, post creation) — these have side effects beyond the local environment
- Flag server-wide wildcards (`mcp__server__*`) — convenient but auto-permits any future tools added to that server without review
- Suggest consolidation: if all or most tools from a server are individually listed, suggest replacing with the server wildcard (with a note about the trade-off)

### Category E: Empty File Deletion

After cleanup, identify settings files where:

- All permissions have been removed (empty allow list or no allow list)
- No other settings exist (no hooks, enabledPlugins, etc.)

Offer to delete these empty files entirely — they serve no purpose.

### Present Findings

```markdown
## Judgment Calls

### Security Hygiene

#### High Risk — Recommend Removal

| Permission     | Project   | Risk              |
| -------------- | --------- | ----------------- |
| `Bash(curl *)` | project-x | Data exfiltration |

#### Moderate Risk — Review

| Permission | Project | Risk |
| ---------- | ------- | ---- |
| ...        | ...     | ...  |

### Policy Conflicts

| Permission      | Projects | Policy                      |
| --------------- | -------- | --------------------------- |
| `WebFetch(url)` | 3        | CLAUDE.md: prefer Firecrawl |

### One-Off Cruft

| Permission                                         | Project   |
| -------------------------------------------------- | --------- |
| `Bash(prettier --write /path/to/specific/file.md)` | project-y |

### External File Access

| Permission                     | Projects   | Notes                           |
| ------------------------------ | ---------- | ------------------------------- |
| `Write(~/.config/tool/config)` | 3 projects | Shared config — consider global |
| `Edit(/etc/hosts)`             | 1 project  | System file — review necessity  |

### MCP Tool Permissions

| Permission                 | Projects | Notes                                       |
| -------------------------- | -------- | ------------------------------------------- |
| `mcp__slack__post_message` | 2        | Side effect: sends messages externally      |
| `mcp__puppeteer__*`        | 1        | Server wildcard — auto-permits future tools |

### Empty Settings Files

| File                                      | Reason                                     |
| ----------------------------------------- | ------------------------------------------ |
| `~/project-z/.claude/settings.local.json` | All permissions removed, no other settings |
```

### Get User Decision

Use AskUserQuestion:

```
Question: "How should I handle the judgment call items?"
Options:
- "Remove all flagged items"
- "Remove high risk + cruft only"
- "Let me review each category"
- "Skip — keep everything"
```

If user wants to review categories, ask about each separately.

### Apply Changes

Edit each affected `settings.local.json` to remove approved items. Delete empty settings files if approved.

Mark Phase 3 task as completed.

---

## Session Wrap-Up

After all phases complete, offer to create or update `~/.claude/cc-maintenance.local.md` with session learnings. Include:

- Any risk tolerance preferences expressed during the session
- Tool preference notes mentioned during review
- Freeform notes from user decisions (overrides, exceptions, per-project rules — anything the user said that should carry forward to future audits)
- Session history entry (date, summary of changes)

---

## User Preferences

**Location:** `~/.claude/cc-maintenance.local.md`

Read at audit start. If missing, proceed with defaults. At session end, offer to create/update.

**Format:** YAML frontmatter for structured preferences + markdown body for freeform notes.

```yaml
---
# All preferences are optional
risk_tolerance: moderate # conservative | moderate | aggressive
auto_cleanup_redundant: true
---
## Tool Preferences
- Prefer Exa/Firecrawl over built-in WebSearch/WebFetch

## Risk Notes
- sqlite3 and op item get considered moderate risk
- uv run python treated as arbitrary code execution

## Notes
- Always keep python3 permissions in the data-science project
- Don't consolidate Firecrawl tools into a server wildcard

## Session History
### 2026-02-09
- Promoted 13 permissions to global
- Removed ~220 cruft permissions from Assistant project
```

**Behavior:**

- `risk_tolerance` adjusts what gets flagged as moderate vs high in Phase 3
- `auto_cleanup_redundant` skips the confirmation prompt in Phase 2 (still shows summary)
- Tool Preferences section supplements CLAUDE.md policy detection
- Notes section is a freeform catch-all for any user preferences that don't fit the structured sections — overrides, exceptions, per-project rules, anything the agent should remember across audits
- Session History provides context for future audits

---

## Scripts

All scripts are in `scripts/` relative to this skill directory.

- **`scripts/discover-settings.sh`** — Finds all `.claude/settings.local.json` files across `~` using `fd` with sensible exclusions (Library, node_modules, .git, etc.). Max depth of 5 for performance.
- **`scripts/extract-permissions.py`** — Aggregates permissions from multiple settings files. Outputs JSON with each permission, occurrence count, and list of projects using it. Sorted by count descending.
- **`scripts/cleanup-redundant.py`** — Removes permissions from local files that are covered by global config. Handles cross-syntax matching (colon-syntax vs space-syntax). Normalizes remaining permissions to space-syntax on write. Dry-run by default; use `--apply` to modify files.

**Usage examples:**

```bash
# Extract and aggregate all permissions
scripts/discover-settings.sh | xargs scripts/extract-permissions.py

# Preview redundant permission cleanup (dry-run, default)
scripts/discover-settings.sh | scripts/cleanup-redundant.py

# Actually remove redundant permissions
scripts/discover-settings.sh | scripts/cleanup-redundant.py --apply
```

---

## Categorization Rules

### Formatting Rules

Use space-syntax for all permissions: `Bash(cmd *)` not `Bash(cmd:*)`.

### Reasonable Global Candidates

Patterns worth promoting. These operate on local project code or perform read-only operations. Compare against the **actual** global config, not just this static list — these are examples of the kinds of patterns to look for.

**Git Commands (read-only):**
`git branch *`, `git diff *`, `git log *`, `git show *`, `git status *`

**File Inspection (read-only):**
`cat *`, `head *`, `tail *`, `ls *`, `find *`, `grep *`, `du *`

**Build and Check Commands:**
`cargo build *`, `cargo test *`, `cargo check *`, `go build *`, `go test *`,
`npm run build *`, `npm run test *`, `deno check *`, `deno lint *`, `xcodebuild *`

**System Utilities:**
`open *`, `pbcopy`, `pbpaste`, `lsof *`, `ps *`

**Nix Commands:**
`nix build *`, `nix-build *`, `nix develop *`, `nix eval *`, `nix flake *`,
`nix path-info *`, `nix-prefetch-url *`, `nh darwin build *`

**Homebrew (read-only):**
`brew info *`, `brew search *`

**GitHub CLI:**
`gh api *`, `gh issue list *`, `gh issue view *`, `gh pr list *`, `gh pr view *`,
`gh pr diff *`, `gh pr checks *`, `gh search *`, `gh run list *`, `gh run view *`

**Wildcards:**
`* --help *`, `* --version`

### Pattern Generalization

When promoting, generalize cautiously — only for safe patterns:

| Local Pattern                 | Global Pattern          | Notes                        |
| ----------------------------- | ----------------------- | ---------------------------- |
| `Bash(npm run build)`         | `Bash(npm run build *)` | Safe — runs project scripts  |
| `Bash(cargo test --release)`  | `Bash(cargo test *)`    | Safe — tests local code      |
| `Bash(nix build .#package)`   | `Bash(nix build *)`     | Safe — sandboxed builds      |
| `Bash(python3 script.py)`     | Keep specific or skip   | Risky — arbitrary code       |
| `WebFetch(domain:github.com)` | Keep as-is              | Domain patterns don't change |

### Formatting Rules for Global Settings

When adding to `~/.claude/settings.json`:

- Respect existing logical groupings (git, file inspection, nix, brew, gh, system utilities, build tools, wildcards, Skills, MCP tools)
- Within each group, sort alphabetically
- Place new permissions in the appropriate group based on command prefix
- Use space-syntax: `Bash(cmd *)` not `Bash(cmd:*)`
