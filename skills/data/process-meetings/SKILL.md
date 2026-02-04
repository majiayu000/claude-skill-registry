---
name: process-meetings
description: Process synced Granola meetings to update person pages, extract tasks, and organize meeting notes
---

# Process Meetings

Process meetings that have been synced from Granola by the background automation. Updates person pages, extracts tasks, and organizes meeting notes.

## How It Works

Meetings are synced automatically every 30 minutes by a background process. This command reads those synced files and:
- Creates/updates person and company pages
- Extracts action items to 03-Tasks/Tasks.md
- Links everything together

**No terminal commands are shown** - the heavy lifting happens in the background.

## Arguments

- No arguments: Process all unprocessed meetings from the last 7 days
- `today`: Only process today's meetings
- `"search term"`: Find meetings by title/attendee
- `--people-only`: Only update person/company pages (skip tasks)
- `--no-todos`: Create notes but don't extract tasks
- `--setup`: Install/check background automation

## Process

### Step 1: Check Background Sync Status

First, check if background sync is set up:

```bash
# Check for state file (indicates sync has run)
ls .scripts/meeting-intel/processed-meetings.json
```

**If state file exists:** Background sync is working. Continue to Step 2.

**If state file doesn't exist:**
> "Background meeting sync isn't set up yet. This runs automatically every 30 minutes so `/process-meetings` doesn't need terminal commands.
>
> **To set up (one-time, takes 30 seconds):**
> ```bash
> cd .scripts/meeting-intel && ./install-automation.sh
> ```
>
> Or run `/process-meetings --setup` and I'll do it for you.
>
> **Requirements:**
> - Granola app installed ([granola.ai](https://granola.ai))
> - An LLM API key in `.env` (GEMINI_API_KEY, ANTHROPIC_API_KEY, or OPENAI_API_KEY)"

If user runs `--setup`:
```bash
cd .scripts/meeting-intel && ./install-automation.sh
```

### Step 2: Find Synced Meetings

Read the processed meetings state:
```javascript
const state = JSON.parse(fs.readFileSync('.scripts/meeting-intel/processed-meetings.json'));
```

List meeting files in `00-Inbox/Meetings/`:
```bash
find 00-Inbox/Meetings -name "*.md" -mtime -7 | head -50
```

For each meeting file:
1. Read frontmatter to get `granola_id`, `participants`, `company`, `date`
2. Check if person/company pages need updating
3. Check if tasks need extracting (look for unchecked items in "For Me" section)

Report findings:
> "Found X synced meetings from the last 7 days. Y need person page updates, Z have unextracted tasks."

### Step 3: Update Person Pages

For each participant in synced meetings:

1. **Load user profile** for email domain:
   ```
   Read System/user-profile.yaml → get email_domain
   ```

2. **Classify as Internal/External:**
   - If participant email domain matches user's domain → Internal
   - Otherwise → External

3. **Check if person page exists:**
   - Internal: `05-Areas/People/Internal/{Name}.md`
   - External: `05-Areas/People/External/{Name}.md`

4. **If page doesn't exist, create it:**
   ```markdown
   # {Name}

   ## Overview

   | Field | Value |
   |-------|-------|
   | **Company** | {company from meeting} |
   | **Email** | {if available} |
   | **First Met** | {meeting date} |

   ## Recent Interactions

   - [{Meeting Title}](00-Inbox/Meetings/{date}/{slug}.md) — {date}

   ## Notes

   *Auto-created from meeting on {date}*
   ```

5. **If page exists, add meeting to Recent Interactions:**
   - Read existing page
   - Add new meeting link under "## Recent Interactions"
   - Keep max 20 entries (remove oldest if needed)
   - Update "Last Interaction" in frontmatter

### Step 4: Update Company Pages

For each unique external company domain:

1. **Check if company page exists:** `05-Areas/Companies/{Company}.md`

2. **If doesn't exist, create it:**
   ```markdown
   # {Company Name}

   ## Overview

   | Field | Value |
   |-------|-------|
   | **Website** | {domain} |
   | **Stage** | Unknown |
   | **First Contact** | {date} |

   ## Key Contacts

   - [[05-Areas/People/External/{Person}|{Person}]]

   ## Meeting History

   - [{Meeting Title}](00-Inbox/Meetings/{date}/{slug}.md) — {date}

   ## Notes

   *Auto-created from meeting on {date}*
   ```

3. **If exists, update:**
   - Add any new contacts to "Key Contacts"
   - Add meeting to "Meeting History"

### Step 5: Extract Tasks (unless --no-todos or --people-only)

For each meeting with unextracted tasks:

1. **Find action items** in the "## Action Items > ### For Me" section
2. **For each unchecked item** (`- [ ]`):
   - Extract task description
   - Get task ID (format: `^task-YYYYMMDD-XXX`)
   - Read pillar from meeting frontmatter

3. **Create task** using Work MCP:
   ```
   create_task(
     title: "Task description",
     priority: "P2",  // default, P1 if "urgent" mentioned
     pillar: "{from meeting}",
     people: ["{participants}"],
     source: "meeting:{meeting-path}"
   )
   ```

4. **Mark as extracted** by adding comment to meeting note:
   ```markdown
   <!-- tasks-extracted: 2026-02-03T10:30:00Z -->
   ```

### Step 6: Summary Report

```
## Meeting Processing Complete ✅

**Synced meetings found:** X (last 7 days)
**Background sync status:** Running (last sync: 10 min ago)

### Updates Made

**Person pages:**
- Created: 3 new (Alice Chen, Bob Smith, Carol Wang)
- Updated: 5 existing

**Company pages:**
- Created: 1 new (Acme Corp)
- Updated: 2 existing

**Tasks extracted:** 7 items added to 03-Tasks/Tasks.md

### Recent Meetings

| Date | Meeting | Company | Participants |
|------|---------|---------|--------------|
| Feb 3 | Product Review | Acme | Alice, Bob |
| Feb 2 | Strategy Call | BigCo | Carol |

---
*Background sync runs every 30 min. Check status: `.scripts/meeting-intel/install-automation.sh --status`*
```

## Error Handling

**If no meetings found:**
> "No meetings synced in the last 7 days. Make sure:
> 1. Granola is running during your meetings
> 2. Background sync is set up (run `/process-meetings --setup`)
> 3. Check logs: `.scripts/logs/meeting-intel.stdout.log`"

**If background sync isn't running:**
> "Background sync appears to be stopped. To restart:
> ```bash
> cd .scripts/meeting-intel && ./install-automation.sh
> ```"

## Examples

```
/process-meetings
```
> "Found 8 synced meetings. Updating 12 person pages, extracting 5 tasks..."

```
/process-meetings today
```
> "Found 2 meetings from today. Processing..."

```
/process-meetings --setup
```
> "Installing background automation..." [runs install script]

```
/process-meetings --people-only
```
> "Updating person and company pages only (skipping task extraction)..."
