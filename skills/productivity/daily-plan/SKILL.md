---
name: daily-plan
description: Generate context-aware daily plan with calendar, tasks, and priorities. Integrates with morning journaling if enabled.
---

## Purpose

Generate your daily plan with full context awareness. Automatically gathers information from your calendar, tasks, meetings, and relationships to create a focused plan.

## Usage

- `/daily-plan` — Create today's daily plan
- `/daily-plan tomorrow` — Plan for tomorrow (evening planning)
- `/daily-plan --setup` — Re-run integration setup

---

## Tone Calibration

Before executing this command, read `System/user-profile.yaml` → `communication` section and adapt:

**Career Level Adaptations:**
- **Junior:** More encouraging, explain "why" behind prioritization, suggest asking for help
- **Mid:** Collaborative, focus on impact and ownership
- **Senior/Leadership:** Strategic questions, challenge priorities, focus on delegation
- **C-Suite:** High-level, strategic focus, organizational outcomes

**Directness:**
- **Very direct:** Brief bullets, action-focused, minimal context
- **Balanced:** Context + action (default)
- **Supportive:** More encouragement, explain reasoning

**Detail Level:**
- **Concise:** Brief summary, top 3 priorities
- **Balanced:** Standard daily plan format
- **Comprehensive:** Extended context, dependencies, risks

See CLAUDE.md → "Communication Adaptation" for full guidelines.

---

## Step 0: Demo Mode Check

Before anything else, check if demo mode is active:

1. Read `System/user-profile.yaml`
2. Check `demo_mode` value
3. **If `demo_mode: true`:**
   - Display banner: "Demo Mode Active — Using sample data from System/Demo/"
   - Use these paths instead of normal paths:
     - `System/Demo/03-Tasks/Tasks.md` instead of `03-Tasks/Tasks.md`
     - `System/Demo/00-Inbox/` instead of `00-Inbox/`
     - `System/Demo/05-Areas/People/` instead of `05-Areas/People/`
     - `System/Demo/04-Projects/` instead of `04-Projects/`
   - Skip calendar/Granola integrations (use demo meeting data)
   - Write output to `System/Demo/07-Archives/Plans/`
4. **If `demo_mode: false`:** Proceed normally

---

## Step 1: Check for Updates (Background)

Silently check if Dex has updates available:

1. Call update checker MCP: `check_for_updates(force=False)`
   - This respects the 7-day interval
   - Won't check if checked recently
   - Won't block if network issues

2. **If update available:**
   - Store notification message for prepending to final output
   - Format: "🎁 Dex v{version} is available. Run /dex-update to see what's new and update."
   - Continue immediately (don't wait for user)

3. **If no update or too recent:**
   - Continue silently (don't mention)
   - No user-facing output

4. **If error (network, API limit):**
   - Continue silently (don't mention)
   - Will retry tomorrow

**Note:** This runs in background. Don't announce "Checking for updates..." or wait for user input. Just proceed with daily planning.

---

## Step 2: Morning Journal Check (If Enabled)

Check if morning journaling is enabled:

1. Read `System/user-profile.yaml`
2. Check `journaling.morning` value
3. **If `journaling.morning: true`:**
   - Check if today's morning journal exists in `00-Inbox/Journals/YYYY/MM-Month/Morning/YYYY-MM-DD-morning.md`
   - **If missing:**
     - Prompt: "Let's start with a quick morning reflection first. It'll take 5 minutes and helps you plan with more intention."
     - Guide through morning journal (see `/journal` command)
     - After completion, continue to Step 2
   - **If exists:** Continue to Step 2
4. **If `journaling.morning: false`:** Skip to Step 2

---

## Step 3: Monday Weekly Planning Gate

If today is Monday, check if the week is planned:

1. Check current day of week
2. **If Monday:**
   - Read `00-Inbox/Weekly_Plans.md`
   - Check the `Week of:` date in frontmatter/header
   - **If week is not current week:**
     
     Prompt user:
     > "It's Monday and this week isn't planned yet.
     > 
     > Planning your week first helps ensure today's work aligns with what matters most. (Takes 5-10 min)
     > 
     > **[Plan the week first]** — Run `/week-plan` then come back to daily plan
     > **[Skip to today]** — I'll plan the week later"
     
     - If user chooses "Plan the week first" → Run `/week-plan` → Then return to daily planning
     - If user chooses "Skip to today" → Continue to Step 3, but note in output that week isn't planned
     
   - **If week is current week:** Continue to Step 3
   
3. **If not Monday:** Continue to Step 3

---

## Step 4: Yesterday's Review Check (Soft Gate)

Unlike a hard block, this is a gentle check:

1. Calculate yesterday's date (skip weekends if not a work day)
2. Look for `00-Inbox/Daily_Reviews/Daily_Review_YYYY-MM-DD.md`
3. **If exists:** Extract context:
   - Open Loops → Items that need attention today
   - Tomorrow's Focus → Today's starting point
   - Blocked items → Check if resolved
4. **If missing:** Warn but continue:
   > "I notice yesterday's review is missing. I can still plan today, but you might want to run `/review` later to capture what you accomplished."

## Step 3.5: Level-Up Check (Smart Trigger)

Check if it's time to surface `/dex-level-up`:

1. Read `System/usage_log.md` to check `last_dex_level_up_prompt` date (stored at bottom of file)
2. **If 7+ days since last prompt OR field doesn't exist:**
   - Count unchecked features in usage log
   - **If 3+ unchecked features exist:**
     - Add this to the daily plan output (in a "Tips" or "System" section):
       ```markdown
       ---
       
       💡 **Tip:** You're using {{X}} of {{Y}} Dex features. Run `/dex-level-up` to see what you might be missing.
       ```
     - Update `last_dex_level_up_prompt: YYYY-MM-DD` in usage_log.md
3. **Otherwise:** Skip this check

---

## Step 3.6: Self-Learning Checks (Background)

Run automated self-learning checks before gathering context. These are fast, throttled checks that keep Dex up-to-date.

**Execute silently in background:**

1. **Changelog Check** (if 6+ hours since last check)
   ```bash
   node .scripts/check-anthropic-changelog.cjs 2>/dev/null &
   ```
   - Respects 6-hour minimum interval
   - Writes alert file if updates found
   - Non-blocking (runs in background)

2. **Learning Review Check** (if not checked today)
   ```bash
   bash .scripts/learning-review-prompt.sh 2>/dev/null &
   ```
   - Counts pending learnings from past 7 days
   - Creates alert if 5+ pending
   - Updates `.last-learning-check` file with today's date

**Note:** These checks also run at session start via hooks, but running here ensures they happen during daily planning even if hooks aren't configured. The interval throttling prevents duplicate work.

**If alert files exist, they will be surfaced in Step 4 context.**

---

## Step 5: Context Gathering

Gather context from all available sources in parallel:

### From Calendar (if enabled)

```
Use: calendar_get_events_with_attendees for today
```

Extract:
- Today's meetings with times
- Attendees (for People/ lookup)
- Back-to-back meeting detection
- Free time blocks

### From Granola (if enabled)

Check for recent meeting notes that might have action items.

### From 03-Tasks/Tasks.md

```
Use: list_tasks with status filter
```

Extract:
- P0 items (must do)
- P1 items (important)
- Started but not completed
- Overdue items

### From Week Priorities

Read `00-Inbox/Weekly_Plans.md`:
- This week's Top 3
- Key meetings
- Pillar balance check

### From Work Summary (Work MCP)

```
Use: get_work_summary()
```

Extract:
- Quarterly goals with progress (if quarterly planning enabled)
- Weekly priorities with completion status
- Tasks grouped by priority link
- Warnings about stalled goals or orphaned work

This provides strategic context for the day: "Your tasks today contribute to Priority 2, which advances Goal 1"

### From People/

For each meeting attendee:
- Look up `People/External/` or `People/Internal/`
- Surface recent context, open items with them

### From Self-Learning Alerts

Check for pending alerts created by background automation:

1. **Changelog Updates**: Read `System/changelog-updates-pending.md` if exists
   - Extract: Latest version, update date
   - Surface: "🆕 New Claude Code features available - run `/dex-whats-new`"

2. **Learning Reviews**: Read `System/learning-review-pending.md` if exists
   - Extract: Count of pending learnings
   - Surface: "📚 {count} pending learnings from this week - run `/dex-whats-new --learnings`"

**Include in daily plan output if present** - these are actionable items for improving your system.

---

## Step 6: Synthesis

Combine all gathered context into recommendations:

### Focus Recommendation

Based on:
- P0 tasks (highest weight)
- Yesterday's "Tomorrow Focus"
- Meeting prep needs
- Week Priorities alignment

Generate 3 recommended focus items.

### Meeting Prep

For each meeting:
- Who's attending (with People/ context)
- Related tasks or projects
- Suggested prep if none exists

### Heads Up

Flag potential issues:
- Back-to-back meetings
- P0 items with no time blocked
- People you owe follow-ups to

---

## Step 7: Generate Daily Plan

**Before displaying the plan:**

If update notification was captured in Step 1, prepend it to the output:

```
🎁 Dex v{version} is available. Run /dex-whats-new for details.

---

[Daily plan follows below]
```

**Then create the plan:**

Create `07-Archives/Plans/YYYY-MM-DD.md`:

```markdown
---
date: YYYY-MM-DD
type: daily-plan
integrations_used: [calendar, tasks, people]
---

# Daily Plan — {{Day}}, {{Month}} {{DD}}

## TL;DR
- {{1-2 sentence summary}}
- {{X}} meetings today
- {{Key focus area}}

---

## Strategic Context (if quarterly planning enabled)

**This Week's Priority:** {{Priority 2}} — Ship beta version  
**Advances Goal:** Q1-2026-goal-1 (Launch Product v2.0) — Currently at 55%

**Today's Contribution:**
- Your P0 tasks contribute to this week's priority
- Completing them moves Goal 1 toward 60%

---

## Career Development (if Career system enabled)

**If `05-Areas/Career/` exists and today's work has career metadata:**

> 💡 **Career Growth Today:**
> 
> Today's work develops these skills:
> - **[Skill 1]** — From [Goal/Priority Title]
> - **[Skill 2]** — From [Goal/Priority Title]
> 
> These map to your target role: [Target Role from Growth_Goals.md]

**Optional: Show stale skills:**

> ⚠️ **Skill to practice:** You haven't worked on "[Stale Skill]" in [X] days — required for [target level]

**Tag reminder:**

> **Tip:** Add `# Career: [skill]` to tasks that develop specific skills for evidence tracking.

---

## Carried From Yesterday

> From yesterday's review (if exists)

### Open Loops
- [ ] {{Items from yesterday's review}}

### Yesterday's Focus → Today's Starting Point
1. {{Priority 1}}
2. {{Priority 2}}

---

## Today's Focus

**If I only do three things today:**

1. [ ] {{Focus item 1}} — {{Pillar}} *(supports Week Priority #X)*
2. [ ] {{Focus item 2}} — {{Pillar}} *(supports Week Priority #Y)*
3. [ ] {{Focus item 3}} — {{Pillar}}

> 📍 **This week's priorities:** [Link to Week Priorities.md or brief reference]

---

## Schedule

| Time | Meeting/Block | Who | Prep |
|------|---------------|-----|------|
| {{Time}} | {{Meeting}} | {{Attendees}} | {{Prep link or "None needed"}} |
| ... | ... | ... | ... |

### Free Blocks
- {{Time range}}: {{Suggested use}}

---

## Tasks by Priority

### P0 - Must Do Today
- [ ] {{Task}}

### P1 - Important
- [ ] {{Task}}

### P2 - If Time Allows
- [ ] {{Task}}

---

## People Context

### Meeting with {{Name}}
- Role: {{From People/ page}}
- Last interaction: {{Date}}
- Open items: {{Any pending tasks involving them}}

---

## Heads Up

{{Flags and warnings}}

- ⚠️ Back-to-back meetings from X to Y
- ⏰ P0 item "{{task}}" has no time blocked
- 📞 You owe {{Name}} a follow-up from {{Date}}

---

*Generated: {{timestamp}}*
*Integrations: {{list}}*
```

---

## Step 8: Track Usage (Silent)

After generating the daily plan, silently update usage tracking:

1. Read `System/usage_log.md`
2. Update these items:
   - `- [ ] Daily planning (/daily-plan)` → `- [x] Daily planning (/daily-plan)`
   - Update `First daily plan: YYYY-MM-DD` if not set
3. No announcement to user

---

## Graceful Degradation

The plan works at multiple levels:

### Full Context (Calendar + Granola + Tasks + People)
- Complete schedule with attendee lookup
- Meeting prep suggestions
- Relationship context

### Partial Context (Tasks + People only)
- Focus recommendations from tasks
- No schedule section
- Still useful for prioritization

### Minimal Context (Tasks only)
- Basic focus list
- Task priorities
- Prompt for manual schedule input

### No Context (Nothing configured)
- Interactive flow asking about priorities
- Creates basic daily note
- Encourages setting up integrations

---

## Evening Planning Variant

`/daily-plan tomorrow`:

1. Check for evening journal (if journaling enabled)
2. Gather tomorrow's calendar
3. Review unfinished tasks from today
4. Generate tomorrow's draft plan
5. Save as `07-Archives/Plans/YYYY-MM-DD-draft.md`

---

## MCP Dependencies

| Integration | MCP Server | Tools Used |
|-------------|------------|------------|
| Calendar | dex-calendar-mcp | `calendar_get_today`, `calendar_get_events_with_attendees` |
| Granola | dex-granola-mcp | `get_recent_meetings` |
| Work | dex-work-mcp | `list_tasks`, `list_week_priorities`, `suggest_focus` |

---

## Setup Instructions

### Calendar MCP Setup

1. Ensure `core/mcp/calendar_server.py` exists
2. Add to Claude Desktop config at `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "dex-calendar": {
      "command": "python",
      "args": ["/path/to/dex/core/mcp/calendar_server.py"],
      "env": {
        "VAULT_PATH": "/path/to/dex"
      }
    }
  }
}
```

3. Restart Claude Desktop
4. Run `/daily-plan --setup` to configure

### Granola MCP Setup

1. Install Granola app (macOS only)
2. Ensure `core/mcp/granola_server.py` exists
3. Add to Claude Desktop config (same file, similar pattern)
4. Granola will auto-detect from local cache at `~/Library/Application Support/Granola/cache-v3.json`
