---
name: meeting-sync
description: Sync new Granola meetings to local Knowledge folder. Use during morning planning, when user asks "what should I do today", or asks to review/sync meetings.
---

# Meeting Sync

Check for new Granola meetings and offer to sync them to your local Knowledge/Transcripts folder.

## Instructions

### Step 1: Check for New Meetings

Call the `check_new_meetings` tool via the Granola MCP to see unsynced meetings.

### Step 2: Present Results

If new meetings are found, present them to the user:

```
I found X new meeting(s) since your last sync:

1. **Meeting Title** (Date)
2. **Meeting Title** (Date)
...

Add to Knowledge folder?
```

### Step 3: Ask User for Selection

Use AskUserQuestion with these options:

| Option | Description |
|--------|-------------|
| Sync all | Add all new meetings to Knowledge/Transcripts |
| Select specific | Let user choose which meetings to sync |
| Skip for now | Continue without syncing |

### Step 4: Sync Selected Meetings

For each meeting the user wants to sync:
1. Call `sync_meeting_to_local` with the meeting ID
2. Confirm each sync completed

### Step 5: Continue with Morning Flow

After syncing (or skipping), continue with the normal morning planning workflow:
- Check tasks
- Review priorities
- Suggest focus items for the day

## Example Flow

**User:** "What should I do today?"

**Claude:**
1. Calls `check_new_meetings`
2. "I found 3 new meetings since your last sync..."
3. Presents AskUserQuestion with sync options
4. User selects "Sync all" or specific meetings
5. Syncs selected meetings
6. "Synced 3 meetings. Now for your day..."
7. Continues with task planning

## Notes

- Only Granola meetings with notes/content are worth syncing
- Meetings marked "(no notes)" may be empty placeholders
- Sync state is tracked in `Knowledge/.granola-sync.json`
- Files are saved to `Knowledge/Transcripts/` with sanitized filenames
