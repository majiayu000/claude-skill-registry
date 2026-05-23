---
name: week-review
description: Review week's progress, meetings, and learnings
---

Create a synthesis of the week reviewing activity, progress, and what was accomplished.

## Data Sources

### 1. Task Progress

```
03-Tasks/Tasks.md                              # Task completion status
00-Inbox/Weekly_Plans.md              # Weekly priorities
```

**Extract:**
- Tasks completed vs planned
- Tasks carried over
- New tasks added during the week
- Blocked items

### 2. Project Activity

```
04-Projects/**/*.md               # Modified this week (check mtime)
```

**Extract:**
- Projects with activity
- Milestones reached
- Blockers identified
- Status changes

### 3. Meetings & People

```
00-Inbox/Meetings/*.md                   # Meeting notes from this week
People/**/*.md                        # Person pages updated
```

**Extract:**
- Meetings held
- Key discussions and decisions
- New contacts made
- Follow-up actions

### 4. Learnings Captured

```
06-Resources/Learnings/**/*.md           # Explicit learnings from completed work
System/Session_Learnings/*.md          # Silent learnings captured during sessions
```

**Extract:**
- Session learnings from this week (mistakes, patterns, improvements)
- Patterns identified and documented
- Preferences documented
- Insights worth remembering
- System improvement opportunities

### 5. Journals (If Enabled)

```
00-Inbox/Journals/YYYY/MM-Month/Morning/*.md    # Morning journals this week
00-Inbox/Journals/YYYY/MM-Month/Evening/*.md    # Evening journals this week
```

**Extract (if journaling is enabled):**
- Energy patterns throughout the week
- Recurring themes or concerns
- Wins and frustrations mentioned
- Intention vs reality (morning plans vs evening reflections)

---

## Analysis Process

1. **Task Review**
   - Scan `03-Tasks/Tasks.md` for completion timestamps from this week (look for `✅ YYYY-MM-DD` dates in the past 7 days)
   - Count completed vs planned from Week Priorities
   - Identify what carried over and why
   - Note any scope creep (tasks added mid-week)
   - Observe patterns: Which days were most productive? Morning or afternoon completions?

2. **Project Scan**
   - Check modification dates on project files
   - Note status changes and progress
   - Identify blocked projects

3. **Meeting Analysis**
   - Review meeting notes from the week
   - Extract action items and commitments
   - Note key decisions made

4. **Learning Compilation & Pattern Detection**
   - Review any new entries in `06-Resources/Learnings/`
   - Scan `System/Session_Learnings/` files from this week
   - Extract themes or patterns
   
   **Pattern Detection:**
   - **Recurring issues**: Same mistake mentioned 2+ times across daily learnings
     - Count occurrences and identify root cause
     - Suggest adding to `06-Resources/Learnings/Mistake_Patterns.md`
   
   - **Consistent preferences**: User repeatedly mentioned a workflow preference
     - Identify the preference pattern
     - Suggest adding to `06-Resources/Learnings/Working_Preferences.md`
   
   **After identifying patterns, prompt user:**
   
   > "This week's session learnings revealed:
   > 
   > **Recurring Issues:**
   > - [Issue X] (appeared 3 times) - [brief description]
   > 
   > **Workflow Preferences:**
   > - [Preference Y] (mentioned 2 times) - [brief description]
   > 
   > Should I add these to your pattern files? This helps prevent future mistakes and aligns my assistance with your preferences."
   
   Only prompt if clear patterns exist (2+ occurrences). Get user confirmation before adding.

5. **Quarterly Progress Check (if quarterly planning enabled)**
   - Use `get_quarterly_goals()` to fetch current quarter goals
   - For each goal, use `get_goal_status(goal_id)` to get:
     - Progress at start of week (from last review or goal file history)
     - Progress at end of week (current)
     - Calculate delta (progress made this week)
   - Identify:
     - Goals that advanced (had linked priority completion)
     - Goals with no movement (stalled)
     - Overall quarter velocity

6. **Career Evidence Check (if Career system enabled)**
   - Check if `05-Areas/Career/` folder exists
   - If yes:
     - Review completed tasks and priorities from this week
     - Identify high-impact accomplishments (major milestones, significant wins, big launches)
     - Check for evidence of skills from `05-Areas/Career/Growth_Goals.md`
     - After presenting weekly synthesis, prompt for evidence capture

---

## Output Format

Create `00-Inbox/Weekly_Synthesis_YYYY-MM-DD.md`:

```markdown
# Weekly Synthesis - Week of [Date]

## TL;DR

- **Tasks:** [X completed] / [Y planned] — [Z%] completion
- **Meetings:** [N total]
- **Projects touched:** [count]
- **Key wins:** [1-2 bullets]
- **Carried over:** [1-2 items that didn't get done]

---

## Task Completion

### Done This Week
- [x] [Task from Week Priorities]
- [x] [Task from Week Priorities]

### Carried Over
- [ ] [Task] - [reason not completed]

### Added Mid-Week
- [Task that wasn't planned but got done]

### Blocked
- [ ] [Task] - blocked by [reason]

---

## Project Progress

### Active Projects

| Project | Status | This Week | Next Steps |
|---------|--------|-----------|------------|
| [Name]  | [On track/At risk] | [What happened] | [Next action] |

### Milestones Reached
- [Project]: [Milestone achieved]

### Blockers
- [Project]: [What's blocking progress]

---

## Meetings & People

### Meetings Held

| Date | Topic | Attendees | Key Outcome |
|------|-------|-----------|-------------|
| [Day] | [Topic] | [Names] | [Decision/insight] |

### New Contacts
- [Name] at [Company] - [context]

### Action Items from Meetings
- [ ] [Action] - for [who] - due [when]

---

## Learnings

### Session Learnings (Auto-Captured)
> From `System/Session_Learnings/` this week

- [Learning from daily sessions]
- [System improvements identified]
- [Mistakes caught and corrected]

### Explicit Learnings (Saved)
> From `06-Resources/Learnings/` entries

- [Insights from `/save-insight`]
- [Patterns documented]

### Working Preferences Updated
- [Any new preferences documented in Working_Preferences.md]

### Actionable Improvements
> Based on learnings above, what should we change?

- [ ] [Specific system improvement]
- [ ] [Documentation update needed]
- [ ] [Process refinement]

---

## Quarterly Progress (if quarterly planning enabled)

> This week's contribution to Q1 2026 goals

|| Goal | Start of Week | End of Week | This Week | Status |
|------|---------------|-------------|-----------|--------|
|| Launch Product v2.0 | 40% | 55% | +15% ✅ | On track |
|| Build Team Capacity | 20% | 30% | +10% ✅ | Progressing |
|| Improve Customer NPS | 10% | 10% | No change ⚠️ | Stalled |

**Analysis:**
- Goals 1 and 2 advanced through completed weekly priorities
- Goal 3 had no linked priorities this week
- Overall quarter velocity: [X%] per week

**Recommendation:** Goal 3 needs attention next week

---

## Next Week

### Top 3 Priorities
1. [Most important thing]
2. [Second priority]
3. [Third priority]

### Upcoming Meetings
- [Day]: [Meeting]
- [Day]: [Meeting]

### Blocked Items Needing Resolution
| Item | Blocked Since | What Would Unblock It |
|------|---------------|-----------------------|
| [Item] | [Date] | [Action needed] |

---

## Energy & Patterns (Optional)

<details>
<summary>Click to expand</summary>

### Energy Patterns
> Based on journal entries (if enabled) and observations

- [Energy level patterns noticed]
- [Time of day/week patterns]

### What Gave Energy
- [Activity that was energizing]

### What Drained Energy  
- [Activity that was draining]

### Recurring Themes
- [Themes from journals/work this week]

### Adjustment for Next Week
- [What to do differently based on patterns]

</details>
```

---

## Follow-up Actions

After synthesis:
1. Update 03-Tasks/Tasks.md with new priorities
2. Archive completed items from Week Priorities
3. Update project pages with status changes
4. Schedule meetings for blocked items if needed

---

## Career Evidence Capture (If Career System Enabled)

After creating the weekly synthesis, check if `05-Areas/Career/` exists:

**If exists:**

1. **Use Career MCP to scan for evidence:**
   - Call `scan_work_for_evidence` tool with:
     - `date_range: "this-week"` or `date_range: "last-7-days"`
     - `impact_level: "high"` (default)
     - `include_goals: true`
     - `include_priorities: true`
   - Tool returns completed high-impact work with career metadata (skills, impact level, career goal alignment)

2. **Manually scan for additional wins:**
   - Major milestones from projects (check `04-Projects/**/*.md` modified this week)
   - Tasks marked with `# Career:` tag in completed tasks

3. Prompt user with MCP-discovered + manual wins:

> "Nice work this week! I noticed some accomplishments that might be worth capturing for career growth:
> 
> **Significant wins:**
> - [Completed goal/milestone 1] — demonstrates [skill/competency]
> - [Completed goal/milestone 2] — shows [leadership/impact]
> 
> Worth saving any of these as career evidence? This helps when:
> - Writing self-reviews
> - Preparing for promotion discussions
> - Building your resume
> 
> **Quick capture options:**
> 1. "Yes, let's capture [specific item]" → I'll create an Achievement file
> 2. "Not this week" → Skip for now
> 3. "Remind me at end of quarter" → I'll prompt during `/quarter-review`"

3. If user wants to capture:
   - Ask clarifying questions (impact, metrics, skills demonstrated)
   - Create file in `05-Areas/Career/Evidence/Achievements/YYYY-MM-DD-[title].md`
   - Use template from `System/Templates/Career_Evidence_Achievement.md`
   - Pre-fill what you know from the work context

**If Career folder doesn't exist:**
- Skip this section entirely

---

## Weekly Journal (If Enabled)

Check if weekly journaling is enabled:

1. Read `System/user-profile.yaml`
2. Check `journaling.weekly` value
3. **If `journaling.weekly: true`:**
   - Check if this week's journal exists in `00-Inbox/Journals/YYYY/MM-Month/Weekly/YYYY-WXX.md`
   - **If missing:**
     - After creating the weekly synthesis, prompt: "Want to reflect on the week in your journal? (5-10 minutes)"
     - If yes: Guide through weekly journal (see `/journal` command)
     - Pull in daily journals from this week for context
     - Synthesize patterns from the week
   - **If exists:** Note completion, skip prompt
4. **If `journaling.weekly: false`:** Skip journal prompt

---

## Track Usage (Silent)

After generating the weekly synthesis, silently update usage tracking:

1. Read `System/usage_log.md`
2. Update: `- [ ] Weekly review (/week-review)` → `- [x] Weekly review (/week-review)`
3. No announcement to user

---

## Next Week Planning Prompt

After generating the synthesis (and optional journal), prompt the user:

> "Week synthesized and saved. Want to plan next week now? (Recommended - takes 5-10 min)
> 
> This will help you start Monday with clear priorities."

**Options:**
1. **"Yes, let's plan next week"** → Run `/week-plan` for next week
2. **"No, I'll do it Monday"** → End command

If user chooses Yes, flow directly into `/week-plan` command with `target_week: next` parameter.
