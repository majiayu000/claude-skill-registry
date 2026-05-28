---
disable-model-invocation: true
name: repoprompt-tool-guidance-refresh
description: Update RepoPrompt tool guidance based on MCP/CLI changes across versions. Two-phase workflow - invoke BEFORE upgrading (--pre), then AFTER upgrading (--post). Uses `~/.pi/agent/skills/repoprompt-tool-guidance-refresh/scripts/track-rp-version.sh` to detect and diff changes (outputs to `~/.pi/agent/skills/repoprompt-tool-guidance-refresh/rp-tool-defs/`).
---

# Workflow

This skill has two invocation modes depending on where you are in the upgrade cycle.

**Canonical locations** (use these even if your working directory differs):
- Skill directory: `~/.pi/agent/skills/repoprompt-tool-guidance-refresh/` (may be a symlink target)
- Script: `~/.pi/agent/skills/repoprompt-tool-guidance-refresh/scripts/track-rp-version.sh`
- Output directory: `~/.pi/agent/skills/repoprompt-tool-guidance-refresh/rp-tool-defs/`

## Phase A — Pre-Upgrade (invoke BEFORE updating RepoPrompt)

1. Run the version tracking script:
   ```bash
   ~/.pi/agent/skills/repoprompt-tool-guidance-refresh/scripts/track-rp-version.sh --pre
   ```
   (Equivalent if you `cd ~/.pi/agent/skills/repoprompt-tool-guidance-refresh`: `./scripts/track-rp-version.sh --pre`)

2. The script writes a baseline snapshot under:
   - `~/.pi/agent/skills/repoprompt-tool-guidance-refresh/rp-tool-defs/`

   Files created/updated:
   - `.baseline_version` — the baseline `rp-cli` version
   - `rpcli-help__{VERSION}.txt` — output of `rp-cli --help`
   - `rpcli-l__{VERSION}.txt` — output of `rp-cli -l`

3. **Stop here.** Tell the user:
   > ✓ Baseline captured at v{VERSION}. Go update RepoPrompt, then re-invoke this skill.

## Phase B — Post-Upgrade (invoke AFTER updating RepoPrompt)

1. Run the version tracking script:
   ```bash
   ~/.pi/agent/skills/repoprompt-tool-guidance-refresh/scripts/track-rp-version.sh --post
   ```
   (Equivalent if you `cd ~/.pi/agent/skills/repoprompt-tool-guidance-refresh`: `./scripts/track-rp-version.sh --post`)

2. On version change, the script captures a *new* snapshot and generates diffs under:
   - `~/.pi/agent/skills/repoprompt-tool-guidance-refresh/rp-tool-defs/`

   Files created/updated:
   - `rpcli-help__{NEW_VERSION}.txt` / `rpcli-l__{NEW_VERSION}.txt` — new snapshots
   - `rpcli-help__{NEW_VERSION}.diff` — changes in `rp-cli --help`
   - `rpcli-l__{NEW_VERSION}.diff` — changes in `rp-cli -l` (MCP tool definitions)

3. If no changes detected in the diffs, tell the user and stop:
   > ✓ No MCP/CLI tool changes detected. Documentation is current.

4. **(Optional) Changelog context**: Ask the user:
   > Paste release notes for v{NEW_VERSION} (or press Enter to skip):

   If provided, write to `~/.pi/agent/skills/repoprompt-tool-guidance-refresh/changelog-latest.md`. If skipped, proceed using diffs as ground truth.

5. **Review diffs** and identify what changed:
   - New tools
   - Removed tools
   - Changed parameters or descriptions
   - New modes/options

## Phase C — Update MCP Documentation

1. The MCP files live in two locations outside this skill folder:
   - **AGENTS prefaces**: `agent/AGENTS-prefaces/rp-mcp-*.md`
   - **Prompts**: `agent/prompts/rp-*.md` (excluding `*-cli.md`)

2. Using the diffs as reference, make surgical updates to bring these files into alignment with the new tool definitions.

## Phase D — Update CLI Documentation

1. The CLI-related files:
   - **AGENTS prefaces**: `agent/AGENTS-prefaces/rp-cli-preface.md`
   - **Prompts**: `~/.pi/agent/skills/repoprompt-tool-guidance-refresh/rp-cli-prompts/rp-*-cli.md`
   - **Extension**: `agent/extensions/repoprompt-cli.ts`

2. Using the diffs as reference, make surgical updates to the preface and prompts.

3. Check whether `repoprompt-cli.ts` encodes assumptions invalidated by the changes. If so, patch minimally.

## Phase E — Git

Stage the changed files.

---

# Scope of Relevant Changes

Only update documentation for changes that affect levers you directly use:
- New/changed/removed MCP tools
- New/changed/removed CLI commands or flags
- Changed parameters, modes, or behaviors

Ignore changes that only affect:
- RepoPrompt desktop app UI (without MCP/CLI changes)
- Integrations with other apps/harnesses (without MCP/CLI changes)
- Internal implementation details not exposed via tools

The diffs are the source of truth. If a changelog item has no corresponding signature in the diffs, it's not relevant to this refresh.
