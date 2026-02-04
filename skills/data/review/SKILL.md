---
name: review
description: End of day review with learning capture. Integrates with evening journaling if enabled.
---

Conduct an end-of-day review to capture progress and set up tomorrow.

## Tone Calibration

Before executing this command, read `System/user-profile.yaml` → `communication` section and adapt:

**Career Level Adaptations:**
- **Junior:** Encouraging reflection, celebrate learning moments, normalize struggles
- **Mid:** Focus on impact achieved, challenge to think strategically
- **Senior/Leadership:** Push on organizational impact, team development, strategic thinking
- **C-Suite:** High-level outcomes, strategic decisions, organizational influence

**Directness:**
- **Very direct:** Quick wins/learnings capture, minimal prompting
- **Balanced:** Standard reflection questions (default)
- **Supportive:** More detailed prompts, encourage reflection

**Detail Level:**
- **Concise:** Brief capture, top highlights
- **Balanced:** Standard review format
- **Comprehensive:** Deep reflection, patterns, insights

See CLAUDE.md → "Communication Adaptation" for full guidelines.

---

## Step 0: File Discovery

**Find files modified TODAY:**

```bash
# Get today's date and find files modified today
TODAY=$(date +%Y-%m-%d)
find . -type f -name "*.md" -newermt "$TODAY 00:00:00" ! -newermt "$TODAY 23:59:59" 2>/dev/null | grep -v "node_modules" | xargs ls -lt 2>/dev/null
```

**Critical rules:**
1. **No truncation** — Do NOT use `head` limits on file discovery
2. **Today only** — Use date-based filtering, NOT `-mtime 0` (which captures 24-hour rolling window)
3. **Verify with user** — After listing files, ASK: "These are the files I found modified today. What did you actually work on?"
4. **Don't infer** — File timestamps tell you what changed, not what matters. Wait for user confirmation.

## Step 1: Gather Context

### Completed Tasks Today
Check `03-Tasks/Tasks.md` for tasks completed today using completion timestamps:
- Look for `✅ YYYY-MM-DD` matching today's date
- These show what you actually finished (not just what you worked on)
- Example: `- [x] **Review pricing proposal** ^task-20260127-003 ✅ 2026-01-28 09:15`

### Weekly Priorities
Read `00-Inbox/Weekly_Plans.md` for:
- This week's strategic focus
- Commitments and deadlines
- Key people involved

### Recent Meetings
Check `00-Inbox/Meetings/` for any meeting notes from today.

## Step 2: User Verification

**Present findings to user:**
> "Based on file timestamps, these notes were modified today: [list]
> 
> What did you actually work on today that should be captured in the review?"

Wait for user response before proceeding.

## Step 3: Progress Assessment

With user-verified information:
- What was accomplished?
- What progress was made against weekly priorities?
- What got stuck or blocked?
- What unexpected discoveries emerged?

## Step 4: Auto-Extract Session Learnings

**Scan today's conversation for learnings:**

Before asking the user anything, reflect on today's session and automatically extract:

1. **Mistakes or corrections**
   - Did the user have to correct any assumptions?
   - Did something not work as expected?
   - Were there misunderstandings to document?

2. **Preferences mentioned**
   - Did the user express how they like to work?
   - Were tool preferences or workflow patterns mentioned?
   - Any communication style notes?

3. **Documentation gaps**
   - Did you have to explain something that should be documented?
   - Were there questions about how the system works?
   - Missing templates or unclear processes?

4. **Workflow inefficiencies**
   - Did any task take longer than it should?
   - Were there repetitive manual steps?
   - Opportunities for automation?

**For each learning identified, write to `00-Inbox/Session_Learnings/YYYY-MM-DD.md`:**

```markdown
## HH:MM - [Short title]

**What happened:** [Specific situation from today's session]
**Why it matters:** [Impact on workflows/system]
**Suggested fix:** [Specific action with file paths if applicable]
**Status:** pending

---
```

**Then ask the user:** "I captured [N] learnings from today's session. Anything else you'd like to add?"

**This ensures learnings persist for:**
- Weekly synthesis (`/week`)
- System improvement reviews (`/dex-whats-new`)
- Future reference

## Step 4b: Additional Insights

- Key realizations or connections from user input
- Questions that arose

## Step 5: Tomorrow's Setup

- Top 3 priorities (aligned with weekly focus)
- Open loops to close
- Questions to explore

## Step 6: Track Usage (Silent)

After creating the daily review, silently update usage tracking:

1. Read `System/usage_log.md`
2. Update: `- [ ] Daily review (/review)` → `- [x] Daily review (/review)`
3. No announcement to user

---

## Step 7: Evening Journal (If Enabled)

Check if evening journaling is enabled:

1. Read `System/user-profile.yaml`
2. Check `journaling.evening` value
3. **If `journaling.evening: true`:**
   - Check if today's evening journal exists in `00-Inbox/Journals/YYYY/MM-Month/Evening/YYYY-MM-DD-evening.md`
   - **If missing:**
     - After creating the daily review, prompt: "Want to close the day with an evening reflection? (3 minutes)"
     - If yes: Guide through evening journal (see `/journal` command)
     - Pull in morning journal intention if it exists for reflection
   - **If exists:** Note completion, skip prompt
4. **If `journaling.evening: false`:** Skip journal prompt

## Output Format

Create daily note at `00-Inbox/Daily_Reviews/Daily_Review_[YYYY-MM-DD].md`:

```markdown
---

---

## Demo Mode Check

Before executing, check if demo mode is active:

1. Read `System/user-profile.yaml` and check `demo_mode`
2. **If `demo_mode: true`:**
   - Display: "Demo Mode Active — Using sample data"
   - Use `System/Demo/` paths instead of root paths
   - Write any output to `System/Demo/` subdirectories
3. **If `demo_mode: false`:** Use normal vault paths

date: [YYYY-MM-DD]
type: daily-review
---

# Daily Review — [Day], [Month] [DD], [YYYY]

## Accomplished

- ✓ [Completed item 1]
- ✓ [Completed item 2]

## Progress Made

| Area | Movement |
|------|----------|
| **[Area 1]** | [What moved forward] |
| **[Area 2]** | [What moved forward] |

## Weekly Priorities Progress

> Reference: 00-Inbox/Weekly_Plans.md

- **[Priority 1]:** [Status/progress]
- **[Priority 2]:** [Status/progress]

## Insights

- [Key realization or connection]
- [Important learning]

## Blocked/Stuck

| Item | Blocker | Status |
|------|---------|--------|
| [Item] | [What's blocking] | [Status] |

## Discovered Questions

1. [New question that emerged]
2. [Thing to research]

## Tomorrow's Focus

1. [Priority 1 — tied to weekly focus]
2. [Priority 2]
3. [Priority 3]

## Open Loops

- [ ] [Thing to remember]
- [ ] [Person to follow up with]
- [ ] **Awaiting:** [What you're waiting on from others]
```

## Important Reminders

- **Verify, don't infer** — Always confirm with user what they worked on
- **Weekly alignment** — Connect daily progress to weekly priorities
- **Day of week** — Use system date metadata, verify before writing
