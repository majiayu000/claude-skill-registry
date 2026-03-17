---
name: commitment-scan
description: Scan ScreenPipe data for uncommitted asks and promises, match to projects/people, and offer to create tasks.
---

# /commitment-scan

Proactively detect commitments you've made or been asked for across apps like Slack, Email, and Notion, then offer to create tasks for any that haven't been captured yet.

---

## Purpose

Things fall through the cracks. You say "I'll send that over" in Slack. Someone asks "Can you review this?" in an email. These micro-commitments don't automatically become tasks in your system. This skill surfaces them before they become forgotten follow-ups.

---

## Prerequisites

- **ScreenPipe beta activated** - Check with `check_beta_enabled(feature="screenpipe")`
- **ScreenPipe opted-in** - Check `System/user-profile.yaml` → `screenpipe.enabled: true`
- **ScreenPipe running** - Check with `screenpipe_status`
- **Commitment Detection MCP** - `commitment-detection` server

---

## Step 0: Check Beta & Opt-In Status

### 0.1 Beta Check

```
Use: check_beta_enabled(feature="screenpipe")
```

**If beta not activated:**
```markdown
⚠️ **ScreenPipe is a beta feature**

Commitment detection is currently in beta testing.

**To join the beta:**
Run `/beta-activate DEXSCREENPIPE2026`

This will unlock:
- `/commitment-scan` - Detect uncommitted asks/promises
- Commitment check during daily review
- Time audit and screen recall features
```

### 0.2 Opt-In Check

Read `System/user-profile.yaml` → `screenpipe.enabled`.

**If not enabled:**
```markdown
⚠️ **ScreenPipe not enabled**

Commitment detection requires ScreenPipe to be enabled.

ScreenPipe captures your screen activity locally to detect commitments 
like "I'll send that over" or "Can you review this?" from apps like 
Slack and Email.

**Privacy:**
- All data stays on your machine
- Browsers, banking, social media blocked by default
- Auto-deletes after 30 days

**To enable:** Run `/screenpipe-setup`
```

**If beta activated AND enabled:** Continue to Step 1.

---

## Execution Flow

### Step 1: Check ScreenPipe Status

```
Use: screenpipe_status
```

**If not running:**
```markdown
⚠️ **ScreenPipe isn't running**

Commitment detection requires ScreenPipe to scan your screen activity.

**To start:** Run `screenpipe` in terminal

After starting, run `/commitment-scan` again.
```

### Step 2: Determine Scan Range

**Options:**
- `/commitment-scan` → Scan today
- `/commitment-scan yesterday` → Scan yesterday
- `/commitment-scan week` → Scan this week

Calculate time range:
```python
if "week" in args:
    # Monday of this week to now
    start = monday_of_week()
    end = now()
elif "yesterday" in args:
    start = yesterday_midnight()
    end = yesterday_end()
else:
    # Today
    start = today_midnight()
    end = now()
```

### Step 3: Scan for Commitments

```
Use: scan_for_commitments(
    start_time="YYYY-MM-DDTHH:MM:SS",
    end_time="YYYY-MM-DDTHH:MM:SS",
    apps=["Slack", "Gmail", "Teams", "Notion"]
)
```

### Step 4: Get Uncommitted Items

```
Use: get_uncommitted_items(include_dismissed=false)
```

### Step 5: Present to User

**If no commitments detected:**
```markdown
✅ **No uncommitted items found**

Either you've been task-capturing well, or it was a quiet period!

*Scanned: [start] to [end]*
*Apps: Slack, Gmail, Teams, Notion*
```

**If commitments detected:**
```markdown
## 🔔 Uncommitted Items Detected

ScreenPipe noticed these potential commitments that don't have matching tasks:

### Inbound Asks (things people asked of you)

**1. [Person Name]** ([App], [Time])
> "[Raw text excerpt]"

📎 **Matches:** [Project name] | [Person page]
⏰ **Deadline detected:** [Date] ([type])

**Actions:**
- `create` → Create task from this
- `handled` → Already done, dismiss
- `ignore` → Not a real commitment

---

### Outbound Promises (things you committed to)

**2. You → [Person Name]** ([App], [Time])
> "[Raw text excerpt]"

📎 **Matches:** [Project name]
⏰ **Deadline detected:** [Date]

**Actions:**
- `create` → Create task for this
- `handled` → Already done, dismiss  
- `ignore` → Not a real commitment

---

**Summary:**
- Inbound asks: [X]
- Outbound promises: [Y]
- Already have tasks: [Z]

*Reply with actions like: "1 create, 2 handled, 3 ignore"*
```

### Step 6: Process User Actions

For each action:

**"create" action:**
```
Use: process_commitment(
    commitment_id="comm-XXXXXX-XXX",
    action="create_task"
)
```

Then create the actual task:
```
Use: create_task(
    title="[Generated from commitment]",
    priority="P2",
    pillar="[From matched project]",
    context="From [App] commitment: [excerpt]",
    related_person="[Person name]",
    due_date="[If deadline detected]"
)
```

**"handled" action:**
```
Use: process_commitment(
    commitment_id="comm-XXXXXX-XXX",
    action="already_handled"
)
```

**"ignore" action:**
```
Use: process_commitment(
    commitment_id="comm-XXXXXX-XXX",
    action="dismiss"
)
```

### Step 7: Confirm

```markdown
✅ **Processed [N] commitments:**

- Created [X] tasks
- Marked [Y] as already handled
- Dismissed [Z]

Your commitment queue is clear! 🎯
```

---

## Integration with Reviews

This skill is automatically called during:

### Daily Review (Step 4.5)

During `/daily-review`, after gathering context:

```markdown
---

## 🔔 Uncommitted Items Check

[Run commitment scan for today]
[Present any detected items]
[Process user choices]

---
```

### Weekly Review

During `/week-review`, show aggregate stats:

```markdown
---

## 📊 Commitment Health This Week

[Show stats from get_commitment_stats()]

---
```

---

## Configuration

In `System/user-profile.yaml`:

```yaml
commitment_detection:
  enabled: true
  scan_during_review: true
  apps:
    - Slack
    - Gmail
    - Teams
    - Notion
    - Linear
  exclude_apps:
    - 1Password
    - Safari Private
```

---

## Privacy Notes

- All scanning happens locally via ScreenPipe
- No data leaves your machine
- Sensitive apps (password managers, banking) are excluded by default
- You control every action - nothing is auto-created
- Dismissed items can be configured to resurface or stay hidden

---

## Examples

### Example 1: Quick Daily Scan

**User:** `/commitment-scan`

**Response:**
```markdown
## 🔔 Uncommitted Items Detected

### Inbound Asks

**1. Sarah Chen** (Slack, 2:34 PM)
> "Hey, can you review the pricing page copy by tomorrow?"

📎 **Matches:** Q1 Pricing Project
⏰ **Deadline:** Tomorrow

**2. Mike Johnson** (Gmail, 11:15 AM)
> "Need your sign-off on the vendor contract"

📎 **Matches:** Mike Johnson (person page)
⏰ **Deadline:** None detected

### Outbound Promises

**3. You → Product Team** (Slack, 4:20 PM)
> "I'll write up the competitive analysis this week"

📎 **Matches:** Market Research project
⏰ **Deadline:** This week

---

*Reply with actions: "1 create, 2 handled, 3 create"*
```

### Example 2: Clean Scan

**User:** `/commitment-scan`

**Response:**
```markdown
✅ **No uncommitted items found**

Either you've been capturing tasks well, or it was a quiet day!

*Scanned today (9:00 AM - 5:45 PM)*
*Apps: Slack, Gmail, Teams, Notion*
```

---

## Troubleshooting

### "ScreenPipe not connected"

1. Ensure ScreenPipe is running: `pgrep screenpipe`
2. Check API: `curl http://localhost:3030/health`
3. Start if needed: `screenpipe` in terminal

### False positives

If detecting too many non-commitments:
- Use "ignore" to train the system
- Check excluded apps list in config
- Patterns are refined over time based on dismissals

### Missing commitments

If real commitments aren't detected:
- Ensure the app is in the scan list
- Check ScreenPipe is capturing that app's content
- The detection patterns may need expansion (file an issue)

---

## Related

- `/daily-review` - Integrates commitment check
- `/week-review` - Shows commitment health stats
- ScreenPipe Setup Guide - `06-Resources/Dex_System/ScreenPipe_Setup.md`

## Track Usage (Silent)

Update `System/usage_log.md` to mark commitment scan as used.

**Analytics (Silent):**

Call `track_event` with event_name `commitment_scan_completed` and properties:
- `commitments_found`
- `tasks_created`

This only fires if the user has opted into analytics. No action needed if it returns "analytics_disabled".
