---
name: cc-changelog
description: |
  CONTRIBUTOR TOOL - Track CC changelog, extract new versions since last check,
  analyze impact on plugin (breaking changes, opportunities, deprecations).
  Run periodically or before releases. NOT part of the distributed plugin.
argument-hint: "[--full|--set=VERSION]"
effort: medium
---

# Claude Code Changelog Assistant

Tracks Claude Code releases against the plugin. Fetches the CC changelog,
extracts entries newer than last check, and analyzes impact on plugin
components (agents, skills, hooks, config).

## Usage

```text
/cc-changelog                  # Check for new CC versions, analyze impact
/cc-changelog --full           # Re-analyze all versions (ignore last check)
/cc-changelog --set=2.1.85     # Reset last checked version (then re-run)
```

## Execution Flow

### Step 1: Fetch & Extract New Entries

```bash
bash scripts/fetch-cc-changelog.sh
```

If output starts with `STATUS: UP_TO_DATE` → report "No new CC versions" and stop.

If `STATUS: NEW_VERSIONS` → continue with the changelog content below the header.

For `--full`: run `bash scripts/fetch-cc-changelog.sh --all`
For `--set=X`: run `bash scripts/fetch-cc-changelog.sh --set=X`, then re-run without flag.

### Step 2: Analyze Impact

Read the new changelog entries. For EACH entry, classify into one of:

| Category | Meaning | Action |
|----------|---------|--------|
| **BREAKING** | May break existing plugin functionality | Immediate fix required |
| **OPPORTUNITY** | New CC feature the plugin could use | Add to backlog/plan |
| **RELEVANT FIX** | CC fixed a bug we worked around | Check if workaround can be removed |
| **DEPRECATION** | CC removing something we use | Plan migration |
| **INFO** | Good to know, no action needed | Log in memory update |

Cross-reference against plugin components using rules in
`${CLAUDE_SKILL_DIR}/references/analysis-rules.md`.

### Step 3: Generate Report

Output a structured report:

```markdown
## CC Changelog Analysis: v{last_checked} → v{latest}

### BREAKING (action required)
- [version] description → **Impact**: which plugin file/component
  **Fix**: specific action needed

### OPPORTUNITY (new features)
- [version] description → **Use case**: how plugin could benefit
  **Files**: which plugin files to update

### RELEVANT FIX (workaround removal)
- [version] description → **Current workaround**: what we do now
  **Action**: can we simplify?

### DEPRECATION (migration needed)
- [version] description → **We use this in**: file:line
  **Migration**: what to change

### INFO (no action)
- [version] brief summary (collapsed)
```

### Step 4: Update State

After user reviews the report, ask:

> "Update last checked version to {latest}? This also updates the
> CC internals memory file. [Yes/No]"

If yes:
1. Run `bash scripts/fetch-cc-changelog.sh --set={latest}`
2. Update memory file `reference_cc_source_internals.md` with new findings
3. If BREAKING or DEPRECATION items found, offer to create a plan

## Iron Laws

1. **ALWAYS fetch before analyzing** — never analyze stale cache
2. **NEVER auto-update state** — user must confirm after reviewing report
3. **ALWAYS cross-reference plugin files** — don't just summarize, map to impact
4. **BREAKING changes are BLOCKERS** — surface first, prominently
5. **Track the audit version** — state file is the source of truth
