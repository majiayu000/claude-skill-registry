---
name: session-start
description: Runs the session startup procedure - verifies setup, loads config and state, checks skill models, and reports project status. Use at the beginning of a fresh session.
model: claude-sonnet-4-6
allowed-tools:
  - Read
  - Bash
  - Glob
  - Grep
  - WebSearch
  - WebFetch
---

## Your Task

Run the full session start procedure and report project status to the user.

---

# Session Start Skill

You perform the 8-step session startup procedure that initializes a working session.

---

## Step 1: Verify Setup

Quick dependency check:

```bash
~/.bitwize-music/venv/bin/python3 -c "import mcp" 2>&1 >/dev/null && echo "MCP ready" || echo "MCP missing"
```

- If MCP missing: **Stop immediately** and suggest: `/bitwize-music:setup mcp`
- If config missing (`~/.bitwize-music/config.yaml` doesn't exist): suggest `/bitwize-music:configure`
- Don't proceed until setup is complete

## Step 2: Load Config

Read `~/.bitwize-music/config.yaml`.

If missing, tell user to run `/bitwize-music:configure`.

## Step 3: Load Overrides

Read `paths.overrides` from config (default: `{content_root}/overrides`):

- Check for `{overrides}/CLAUDE.md` — incorporate instructions if found
- Check for `{overrides}/pronunciation-guide.md` — note if found
- Skip silently if missing (overrides are optional)

## Step 4: Load State Cache

Read `~/.bitwize-music/cache/state.json`:

- If missing, corrupted, schema mismatch, or config changed: rebuild via MCP
  ```
  rebuild_state()
  ```

## Step 4.5: Check for Plugin Upgrades

Compare `plugin_version` in state.json against current version in `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json`:

1. **If `plugin_version` is null** (first run or pre-upgrade-system): Set to current version, skip migrations
2. **If versions match**: No action needed
3. **If stored < current** (upgrade detected):
   - Read migration files from `${CLAUDE_PLUGIN_ROOT}/migrations/` for versions between stored and current
   - Process actions in order:
     - `auto`: Execute silently (run `check` first — skip if returns 0)
     - `action`: Show description, ask user to confirm before executing
     - `info`: Display to user
     - `manual`: Show instruction to user
   - Rebuild state to update `plugin_version`
4. Report: "Upgraded from X to Y" with summary of actions taken

## Step 5: (Removed)

Skill model checking is no longer part of session start. Run `/bitwize-music:skill-model-updater check` manually when new Claude models are released.

## Step 6: Report From State Cache

Using data from `state.json`, report:

### Album Ideas
From `state.ideas.counts` — show count by status (Pending, In Progress, etc.)

### In-Progress Albums
Filter `state.albums` for status: "In Progress", "Research Complete", "Complete"

For each, show:
- Album name, genre, status
- Track progress (completed/total)

### Pending Source Verifications
From `state.albums` — find tracks where `sources_verified` is "Pending"

If any found, warn: "These tracks have unverified sources — generation is blocked until verified."

### Last Session Context
From `state.session`:
- Last album worked on
- Last phase
- Pending actions

## Step 7: Show Contextual Tips

Based on state, show ONE relevant tip:

| Condition | Tip |
|-----------|-----|
| No albums exist | "Try `/bitwize-music:tutorial` to create your first album" |
| Ideas exist but no albums | "You have album ideas! Use `/bitwize-music:album-ideas list` to review them" |
| In-progress albums exist | "Resume where you left off: `/bitwize-music:resume <album-name>`" |
| Overrides loaded | "Custom overrides loaded from {overrides}/" |
| Overrides missing | "Customize your workflow with override files — see `/reference/overrides/`" |
| Pending verifications | "Source verification needed before generation can proceed" |

Also show one random general tip (rotate through these):
- "Ask 'what should I do next?' for workflow guidance"
- "Use `/bitwize-music:resume` to quickly jump back into an album"
- "The researcher skill coordinates 10 specialized sub-skills for deep research"
- "Check pronunciation before generating — Suno can't infer from context"
- "Use `/bitwize-music:clipboard` to copy lyrics/prompts for Suno"
- "Master your audio with `/bitwize-music:mastering-engineer` for professional results"

## Step 8: Ask

End with: "What would you like to work on?"

---

## Report Format

```
SESSION START
=============

Setup: MCP ready, config loaded
Overrides: [loaded from {path} | not found (optional)]
State: [loaded | rebuilt | error]

ALBUM IDEAS
  Pending: X | In Progress: Y

IN-PROGRESS ALBUMS
  [album-name] (genre) - Status [X/Y tracks]
  [album-name] (genre) - Status [X/Y tracks]

PENDING VERIFICATIONS
  [album-name]: track-01, track-05

LAST SESSION
  Album: [name] | Phase: [phase]
  Pending: [actions]

TIP: [contextual tip]

What would you like to work on?
```

---

## Remember

1. **Don't skip steps** — Each step matters for session integrity
2. **Rebuild state if needed** — Stale state leads to wrong recommendations
3. **Be concise** — This is a status report, not a conversation
4. **Warn about verifications** — Unverified sources block generation
5. **One tip, not five** — Pick the most relevant tip for the current state
