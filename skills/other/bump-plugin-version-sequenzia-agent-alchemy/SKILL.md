---
name: bump-plugin-version
description: Bumps plugin versions across the Agent Alchemy ecosystem
user-invocable: true
disable-model-invocation: true
argument-hint: "[--plugin <group,...>] [--level patch|minor|major] [--dry-run]"
allowed-tools:
  - Read
  - Edit
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
---

# Bump Plugin Version

Automate version bumps across the Agent Alchemy ecosystem. Scans 5 version locations per plugin, detects drift, applies consistent updates, adds a CHANGELOG entry, and creates a conventional commit.

**CRITICAL: Complete ALL 6 phases.** The workflow is not complete until Phase 6: Commit is finished. After completing each phase, immediately proceed to the next phase without waiting for user prompts.

## Critical Rules

### AskUserQuestion is MANDATORY

**IMPORTANT**: You MUST use the `AskUserQuestion` tool for ALL questions to the user. Never ask questions through regular text output.

- Plugin selection -> AskUserQuestion
- Bump level selection -> AskUserQuestion
- Drift resolution -> AskUserQuestion
- Confirmation prompts -> AskUserQuestion

Text output should only be used for:
- Displaying progress updates between phases
- Presenting inventory tables and drift reports
- Phase transition markers

If you need the user to make a choice or provide input, use AskUserQuestion.

**NEVER do this** (asking via text output):
```
Which plugins would you like to bump?
1. core-tools
2. dev-tools
```

**ALWAYS do this** (using AskUserQuestion tool):
```yaml
AskUserQuestion:
  questions:
    - header: "Plugins"
      question: "Which plugins would you like to bump?"
      options:
        - label: "core-tools (0.1.1)"
          description: "Current version: 0.1.1"
        - label: "dev-tools (0.1.1)"
          description: "Current version: 0.1.1"
      multiSelect: true
```

### Plan Mode Behavior

**CRITICAL**: This skill performs an interactive version bump workflow, NOT an implementation plan. When invoked during Claude Code's plan mode:

- **DO NOT** create an implementation plan for how to build the bumper
- **DO NOT** defer the version bump to an "execution phase"
- **DO** proceed with the full workflow immediately
- **DO** make file edits as normal

## Phase Overview

Execute these phases in order, completing ALL of them:

1. **Discovery** — Read marketplace.json, build plugin inventory with current versions
2. **Drift Check** — Scan all 5 version locations for inconsistencies
3. **Selection** — Choose plugins and bump level, compute new versions
4. **Bump** — Edit all 5 version locations per plugin
5. **Changelog** — Add entries under `## [Unreleased]` in CHANGELOG.md
6. **Commit** — Stage modified files and create a conventional commit

---

## Phase 1: Discovery

**Goal:** Read the marketplace registry and build a complete plugin inventory.

### Step 1: Parse Arguments

Parse `$ARGUMENTS` for:
- `--plugin <group,...>` — Comma-separated list of plugin groups to bump (e.g., `--plugin core-tools,dev-tools`). Default: prompt for selection in Phase 3.
- `--level patch|minor|major` — Bump level. Default: prompt for selection in Phase 3.
- `--dry-run` — Show what would change without modifying files. Default: `false`.

Set variables:
- `PLUGIN_FILTER` from `--plugin` value (default: `null` = prompt in Phase 3)
- `BUMP_LEVEL` from `--level` value (default: `null` = prompt in Phase 3)
- `DRY_RUN` from `--dry-run` flag (default: `false`)

### Step 2: Load Marketplace Registry

Read the marketplace registry:
```
Read: ${CLAUDE_PLUGIN_ROOT}/../../.claude-plugin/marketplace.json
```

Build a plugin map from the `plugins` array:

```
{
  group_name -> {
    marketplace_name: "agent-alchemy-{group}",
    version: "x.y.z",
    source_dir: "{group}"
  }
}
```

The `group_name` is derived from the `source` field by stripping the leading `./`.

### Step 3: Display Inventory

Display the current plugin inventory:

```
[Phase 1/6] Plugin Inventory

| Plugin | Marketplace Name | Current Version |
|--------|-----------------|-----------------|
| core-tools | agent-alchemy-core-tools | 0.1.1 |
| dev-tools | agent-alchemy-dev-tools | 0.1.1 |
| sdd-tools | agent-alchemy-sdd-tools | 0.1.2 |
| tdd-tools | agent-alchemy-tdd-tools | 0.1.0 |
| git-tools | agent-alchemy-git-tools | 0.1.0 |
| plugin-tools | agent-alchemy-plugin-tools | 0.1.0 |
```

---

## Phase 2: Drift Check

**Goal:** Scan all 5 version locations and detect inconsistencies against marketplace.json (the source of truth).

### Version Locations

For each plugin, versions appear in up to 5 locations:

| # | File | Description |
|---|------|-------------|
| 1 | `claude/.claude-plugin/marketplace.json` | Source of truth — JSON `"version"` field |
| 2 | `CLAUDE.md` (root) | Plugin Inventory table — `\| {group} \| ... \| {version} \|` |
| 3 | `docs/index.md` | Project Status table — `\| {Display Name} \| {version} \| {status} \|` |
| 4 | `docs/plugins/index.md` | At a Glance table — `\| [{Name}](...) \| ... \| {version} \|` |
| 5 | `docs/plugins/{group}.md` | Per-plugin doc file — format varies (see Per-Plugin Formats below) |

### Per-Plugin Doc Formats (Location 5)

Each plugin doc uses a different version format. When scanning, look within the first 15 lines:

| Plugin | Format | Example |
|--------|--------|---------|
| core-tools | Parenthetical in prose + vertical table | `Core Tools (v0.1.1) provides...` and `\| **Version** \| 0.1.1 \|` |
| dev-tools | Bold metadata line | `**Version:** 0.1.1 \| **Skills:** ...` |
| sdd-tools | Bold metadata with plugin name | `**Plugin:** ... \| **Version:** 0.1.2 \| ...` |
| tdd-tools | Backtick-wrapped parenthetical | `` (`v0.1.0`) `` in prose |
| git-tools | Bold metadata line | `**Version:** 0.1.0 \| **Skills:** ...` |
| plugin-tools | Bold metadata with plugin name | `**Plugin:** ... \| **Version:** 0.1.0 \| ...` |

### Step 1: Scan All Locations

For each plugin in the inventory:

1. **Location 2 (CLAUDE.md):** Read the Plugin Inventory table. Find the row matching the plugin group name. Extract the version from the last column.

2. **Location 3 (docs/index.md):** Read the Project Status table. Find the row matching the plugin's display name. Extract the version. Note: not all plugins may be listed here — skip silently if absent.

3. **Location 4 (docs/plugins/index.md):** Read the At a Glance table. Find the row matching the plugin name. Extract the version from the Version column.

4. **Location 5 (docs/plugins/{group}.md):** Read the first 15 lines. Search for the version string using the format described in Per-Plugin Formats above.

Compare each found version against the marketplace.json version (Location 1). Record any mismatches.

### Step 2: Present Drift Report

```
[Phase 2/6] Version Drift Check

✓ No drift detected — all locations consistent.
```

Or if drift is found:

```
[Phase 2/6] Version Drift Check

| Plugin | Location | Expected | Found |
|--------|----------|----------|-------|
| core-tools | docs/plugins/core-tools.md | 0.1.1 | 0.1.0 |
| dev-tools | CLAUDE.md | 0.1.1 | 0.1.0 |
```

### Step 3: Resolve Drift (if any)

If drift was detected, present resolution options via AskUserQuestion:

```yaml
AskUserQuestion:
  questions:
    - header: "Drift"
      question: "Version drift detected in N locations. How should we proceed?"
      options:
        - label: "Fix drift first"
          description: "Update drifted locations to match marketplace.json before bumping"
        - label: "Ignore and bump"
          description: "Proceed with version bump — drifted locations will be overwritten with new version"
        - label: "Abort"
          description: "Stop the workflow to investigate manually"
      multiSelect: false
```

If **Fix drift first**: Use Edit to update each drifted location to match marketplace.json, then continue to Phase 3.

If **Ignore and bump**: Continue to Phase 3. The bump will overwrite with the new version anyway.

If **Abort**: Display the drift details and exit.

---

## Phase 3: Selection

**Goal:** Determine which plugins to bump and the bump level. Compute new versions.

### Step 1: Select Plugins

If `PLUGIN_FILTER` was provided via `--plugin`, use those plugins. Validate each against the inventory — warn and skip any that don't exist.

Otherwise, present a multi-select via AskUserQuestion listing all plugins with their current versions. The options should include each plugin as a selectable item.

### Step 2: Select Bump Level

If `BUMP_LEVEL` was provided via `--level`, use it.

Otherwise, ask via AskUserQuestion:

```yaml
AskUserQuestion:
  questions:
    - header: "Bump Level"
      question: "What type of version bump?"
      options:
        - label: "Patch (x.y.Z)"
          description: "Bug fixes, minor updates — most common for skill changes"
        - label: "Minor (x.Y.0)"
          description: "New features, new skills or agents"
        - label: "Major (X.0.0)"
          description: "Breaking changes to skill interfaces or agent contracts"
      multiSelect: false
```

### Step 3: Compute New Versions

For each selected plugin, compute the new version by applying the bump level:
- **patch**: Increment the third segment (0.1.1 → 0.1.2)
- **minor**: Increment the second segment, reset third to 0 (0.1.1 → 0.2.0)
- **major**: Increment the first segment, reset second and third to 0 (0.1.1 → 1.0.0)

### Step 4: Display Bump Plan

```
[Phase 3/6] Bump Plan

| Plugin | Current | New | Level |
|--------|---------|-----|-------|
| core-tools | 0.1.1 | 0.1.2 | patch |
| dev-tools | 0.1.1 | 0.1.2 | patch |
```

If `DRY_RUN` is `true`:
```
[Dry Run] No files will be modified. Showing what would change:

Files that would be edited:
- claude/.claude-plugin/marketplace.json (2 entries)
- CLAUDE.md (2 rows in Plugin Inventory)
- docs/index.md (2 rows in Project Status — if present)
- docs/plugins/index.md (2 rows in At a Glance)
- docs/plugins/core-tools.md (2 version occurrences)
- docs/plugins/dev-tools.md (1 version occurrence)
- CHANGELOG.md (1 new entry)

Dry run complete.
```
Then stop — do NOT proceed to Phase 4.

---

## Phase 4: Bump

**Goal:** Edit all 5 version locations for each selected plugin.

**CRITICAL:** Track every file modified in a `MODIFIED_FILES` list for Phase 6 staging.

### Location 1: marketplace.json

Read `claude/.claude-plugin/marketplace.json`. For each selected plugin, use Edit to replace the old version string with the new one. Target the specific `"version": "old_version"` line within that plugin's entry block.

### Location 2: CLAUDE.md (Plugin Inventory Table)

Read the Plugin Inventory table in the root `CLAUDE.md`. For each selected plugin, find the row matching the group name and use Edit to replace the old version with the new version in that row. Use enough surrounding context to ensure a unique match.

### Location 3: docs/index.md (Project Status Table)

Read the Project Status table in `docs/index.md`. For each selected plugin, find the row matching the plugin's display name. Use Edit to replace the old version with the new one.

**Note:** Not all plugins appear in this table. If a plugin is not found, skip silently — do not abort or warn.

### Location 4: docs/plugins/index.md (At a Glance Table)

Read the At a Glance table in `docs/plugins/index.md`. For each selected plugin, find the row and use Edit to replace the old version with the new one.

### Location 5: Per-Plugin Doc Files

For each selected plugin, read the first 15 lines of `docs/plugins/{group}.md` and update version occurrences using the format-specific patterns:

**core-tools** — Two occurrences:
1. Parenthetical: `(v{old})` → `(v{new})` in the prose paragraph
2. Vertical table: `| **Version** | {old} |` → `| **Version** | {new} |`

**dev-tools** — One occurrence:
1. Bold metadata: `**Version:** {old}` → `**Version:** {new}`

**sdd-tools** — One occurrence:
1. Bold metadata: `**Version:** {old}` → `**Version:** {new}`

**tdd-tools** — One occurrence:
1. Backtick parenthetical: `` (`v{old}`) `` → `` (`v{new}`) ``

**git-tools** — One occurrence:
1. Bold metadata: `**Version:** {old}` → `**Version:** {new}`

**plugin-tools** — One occurrence:
1. Bold metadata: `**Version:** {old}` → `**Version:** {new}`

### Strategy for Each Edit

1. Read the file (or use already-read content)
2. Search for the old version string in the expected location/format
3. Use Edit with enough surrounding context for a unique match
4. If the pattern is not found, warn and skip — do not abort the entire workflow
5. Add the file path to `MODIFIED_FILES`

### Display Progress

After completing all edits:

```
[Phase 4/6] Version Bump Complete

Updated N files across N plugins:
- claude/.claude-plugin/marketplace.json ✓
- CLAUDE.md ✓
- docs/index.md ✓ (N of N plugins found)
- docs/plugins/index.md ✓
- docs/plugins/core-tools.md ✓ (2 occurrences)
- docs/plugins/dev-tools.md ✓ (1 occurrence)
```

If any locations were skipped:

```
Skipped:
- docs/index.md: plugin-tools not found in table (OK — not listed)
```

---

## Phase 5: Changelog

**Goal:** Add version bump entries under `## [Unreleased]` in CHANGELOG.md.

### Step 1: Read CHANGELOG.md

Read `CHANGELOG.md` from the repository root. Find the `## [Unreleased]` section.

### Step 2: Build Entry

Group bumped plugins by version transition for concise entries. For example, if core-tools and dev-tools both went from 0.1.1 to 0.1.2:

```markdown
### Changed

- Bump core-tools and dev-tools from 0.1.1 to 0.1.2
```

If plugins had different starting versions:

```markdown
### Changed

- Bump core-tools and dev-tools from 0.1.1 to 0.1.2
- Bump sdd-tools from 0.1.2 to 0.1.3
```

### Step 3: Insert Entry

Use Edit to insert the changelog entry immediately after the `## [Unreleased]` line. If there is already content under `[Unreleased]`, add the new entry after any existing entries (before the next `## [x.y.z]` heading or end of section). If a `### Changed` section already exists under `[Unreleased]`, append to it rather than creating a duplicate.

Add `CHANGELOG.md` to `MODIFIED_FILES`.

### Display Progress

```
[Phase 5/6] Changelog Updated

Added entry under [Unreleased]:
  - Bump core-tools and dev-tools from 0.1.1 to 0.1.2
```

---

## Phase 6: Commit

**Goal:** Stage all modified files and create a conventional commit.

### Step 1: Stage Files

Stage each file in `MODIFIED_FILES` individually using `git add`:

```bash
git add claude/.claude-plugin/marketplace.json
git add CLAUDE.md
git add docs/index.md
git add docs/plugins/index.md
git add docs/plugins/core-tools.md
git add docs/plugins/dev-tools.md
git add CHANGELOG.md
```

**CRITICAL:** Do NOT use `git add -A` or `git add .`. Only stage files that were actually modified by this skill.

### Step 2: Create Commit

Build the commit message:

**Single plugin:**
```
chore(marketplace): bump {group} to {new_version}
```

**Multiple plugins, same new version:**
```
chore(marketplace): bump {group1}, {group2} to {new_version}
```

**Multiple plugins, different new versions:**
```
chore(marketplace): bump {group1} to {v1}, {group2} to {v2}
```

Create the commit:
```bash
git commit -m "$(cat <<'EOF'
chore(marketplace): bump core-tools, dev-tools to 0.1.2
EOF
)"
```

### Step 3: Verify and Report

Run `git status` to verify the commit succeeded.

```
[Phase 6/6] Committed

chore(marketplace): bump core-tools, dev-tools to 0.1.2

Staged files: N
Commit: {short_hash}
```

If the commit fails (e.g., pre-commit hook):
1. Display the error output
2. Do NOT use `--amend` or `--no-verify`
3. Suggest the user fix the issue and run `/git-commit` manually

---

## Error Handling

### Missing Doc Files

If a `docs/plugins/{group}.md` file doesn't exist for a selected plugin, warn and skip:
```
Warning: docs/plugins/{group}.md not found — skipping Location 5 for {group}
```

### Unmatched Version Patterns

If a version string can't be found at an expected location:
```
Warning: Could not find version {old} in {file} at expected location — skipping
```
Continue with other locations. Do not abort.

### Plugin Not in Docs Table

If a plugin doesn't appear in `docs/index.md` or `docs/plugins/index.md` tables, skip silently. These tables may not list all plugins.

### Git Commit Failure

If `git commit` fails:
1. Report the full error output
2. Do NOT use `--amend` (would modify the previous commit)
3. Do NOT use `--no-verify` (would skip hooks)
4. Suggest manual resolution

### No Plugins Selected

If the user selects no plugins in Phase 3, display a message and exit:
```
No plugins selected. Exiting.
```

### Invalid Bump Level

If `--level` has an unrecognized value, warn and prompt via AskUserQuestion.
