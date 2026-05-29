---
name: dex-obsidian-setup
description: Enable Obsidian integration and migrate existing vault to wiki links
---

## Purpose

Convert Dex vault to Obsidian wiki link format for graph-based navigation.

## Step 1: Check Current State

Read `System/user-profile.yaml` and check `obsidian_mode` field.

**If already enabled:**
- Say: "Obsidian mode is already enabled. Want to re-run migration? (Safe to run multiple times)"
- If user says no, exit
- If user says yes, continue to Step 3 (skip Step 2)

**If not enabled:**
- Continue to Step 2

## Step 2: Explain Obsidian Integration

Say: "This will enable **Obsidian mode** in your Dex vault:

**What changes:**
- All person/company/project references become clickable wiki links
- Example: `John_Doe` → `[[John_Doe]]`
- Your existing files will be converted automatically

**What stays the same:**
- File structure (PARA folders)
- File contents (just adds `[[ ]]` around references)
- All MCP functionality

**Time estimate:** I'll scan your vault first and show you exactly how long it will take.

**Safety:** I'll create a git backup before any changes. Easy to revert if needed.

Ready to proceed?"

**If NO:** Say "No problem! You can run `/dex-obsidian-setup` anytime." and exit.

**If YES:** Continue to Step 3

## Step 3: Run Migration

Call the migration script using Shell tool (run from the vault root directory):

```bash
python core/obsidian/migrate_to_wikilinks.py
```

The script handles:
- Estimation and user confirmation
- Git backup
- Progress tracking
- macOS notification on completion
- Error handling

Wait for the script to complete and show the output to the user.

## Step 4: Update User Profile

Update `System/user-profile.yaml` to set `obsidian_mode: true`:

1. Read the current file
2. Use StrReplace to update the obsidian_mode field (or add it if missing)
3. If the file uses YAML format, preserve the structure

## Step 5: Optional - Generate Obsidian Config

Ask: "Want me to generate an Obsidian configuration optimized for Dex? This includes:
- Recommended settings (wiki link format, auto-update links)
- Hotkeys for common actions (Cmd+G for graph view)
- Workspace layout (file explorer + backlinks)

These are stored in `.obsidian/` and only affect Obsidian (not Cursor/terminal)."

**If YES:**

Run the config generator (from vault root):

```bash
python core/obsidian/generate_obsidian_config.py
```

Say: "✅ Obsidian config generated! Open your vault in Obsidian to see the optimized setup."

**If NO:**

Say: "No problem! You can always run this later with `python core/obsidian/generate_obsidian_config.py`"

## Step 6: Optional - Start Sync Daemon

Ask: "Want to enable bidirectional sync? This keeps task checkboxes synced between Obsidian and Dex:
- Check a task in Obsidian → syncs to Tasks.md, person pages, meeting notes
- Check a task in Cursor → syncs to Obsidian

Runs in background, zero maintenance."

**If YES:**

Run the daemon installer (from vault root):

```bash
bash core/obsidian/install_sync_daemon.sh
```

**If NO:**

Say: "No problem! You can enable it later by running `bash core/obsidian/install_sync_daemon.sh`"

## Step 7: Completion

Say: "✅ Obsidian mode enabled!

**Next steps:**
1. Open Obsidian: File → Open Folder → select your Dex vault folder
2. Check the graph view: Ctrl/Cmd + G
3. Click any wiki link to navigate

**Tips:**
- Graph filters: Focus on specific areas (People, Projects)
- Search: Cmd/Ctrl + O for quick open
- Backlinks pane: See everywhere a note is referenced

**Resources:**
- See `06-Resources/Dex_System/Obsidian_Guide.md` for detailed tips
- Watch the [beginner's guide](https://www.youtube.com/watch?v=gafuqdKwD_U) if you're new to Obsidian

You can still use Dex in Cursor/terminal exactly as before. Wiki links work everywhere."

## Notes

- This skill is safe to run multiple times (idempotent)
- Migration creates a git backup before making changes
- Revert anytime with `git reset --hard HEAD~1`
- Works with vaults of any size (10K+ files tested)

## Track Usage (Silent)

Update `System/usage_log.md` to mark Obsidian setup as used.

**Analytics (Silent):**

Call `track_event` with event_name `obsidian_enabled` (no properties).

This only fires if the user has opted into analytics. No action needed if it returns "analytics_disabled".
