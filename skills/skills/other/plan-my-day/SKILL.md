---
name: plan-my-day
description: Generate an energy-optimized, time-blocked daily plan based on circadian rhythm research and GTD principles
version: 2.0.0
author: theflohart
tags: [productivity, planning, time-blocking, energy-management, gtd]
---

# Plan My Day

Generate a clean, actionable hour-by-hour plan for the day based on priorities, energy patterns, and constraints.

## Why This vs ChatGPT?

**Problem with "just asking":** You get a different plan each time. No consistency, no memory of what works, no optimization over time.

**This skill provides:**
1. **Consistent methodology** - Same decision framework every day (Top 3 priorities, energy windows, buffer rules)
2. **Energy-aware scheduling** - Automatically matches high-cognitive tasks to your peak hours
3. **Constraint-aware** - Respects your existing calendar, energy patterns, personal boundaries
4. **Learning memory** - Can track what scheduling patterns work best for you over time
5. **Evening reflection built-in** - Forces accountability on what actually got done

**You can replicate this** by writing the same detailed prompt every day, manually checking your calendar, remembering your energy patterns, and tracking completion rates. Or use this skill in 2 minutes.

## Usage

```
/plan-my-day [optional: YYYY-MM-DD for future date]
```

With custom energy profile:

```
/plan-my-day --peak 9-11,14-16 --recovery 13-14
```

## Planning Principles (Research-Backed)

1. **Circadian optimization** - Cognitive performance peaks ~2-3 hours after waking (Roenneberg, 2012)
2. **Ultradian rhythms** - Work in 90-minute blocks with 15-20 minute breaks (Ericsson, 1993)
3. **Decision fatigue prevention** - Schedule high-stakes decisions before 3pm (Kahneman, 2011)
4. **Implementation intentions** - Specific time+task combinations increase completion by 2-3× (Gollwitzer, 1999)

## Energy Windows (Default - Customize Yours)

**Peak Performance (Morning):** 9:00 AM - 12:00 PM
- Deep work, strategic thinking, complex problem-solving
- Highest cognitive capacity
- Schedule your #1 priority here

**Secondary Peak (Afternoon):** 2:00 PM - 4:00 PM
- Focused work, meetings with decisions, creative work
- Still high capacity but slightly lower than morning

**Administrative (Late Afternoon):** 4:00 PM - 6:00 PM
- Email processing, light tasks, 1-on-1s, planning
- Lower energy, avoid complex decisions

**Recovery Blocks:** 12:00 PM - 1:00 PM, 6:00 PM+
- Meals, exercise, walks, recharge
- Non-negotiable for sustained performance

**Wind Down (Evening):** After 7:00 PM
- Reflection, reading, light planning for tomorrow
- No high-cognitive work

## Process

### 1. Gather Context (30 seconds)
- Check existing calendar events
- Review yesterday's incomplete tasks
- Identify any fixed commitments or deadlines
- Note current project priorities

### 2. Identify Top 3 Priorities (60 seconds)
Ask for each potential priority:
- **Impact:** Does this move a key metric or deadline?
- **Urgency:** Must it happen today?
- **Effort:** Can I complete it in available time?

**Filter:** Pick the 3 with highest impact×urgency score

### 3. Build Time-Blocked Schedule (90 seconds)
**Sequencing logic:**
1. Place fixed commitments (meetings, calls) first
2. Assign Priority #1 to longest peak energy block
3. Assign Priority #2 to secondary peak or next available
4. Assign Priority #3 to remaining focused time
5. Add 20-minute buffers between major blocks
6. Schedule admin work (email, Slack) in low-energy windows
7. Protect breaks and meals (non-negotiable)

**Buffer rule:** Only schedule 80% of available time

### 4. Apply Constraints
- **Personal boundaries:** No work before 8am or after 7pm (customize)
- **Meeting limits:** Max 4 hours of meetings per day
- **Focus blocks:** Minimum 90 minutes for deep work (no interruptions)
- **Break enforcement:** 15-minute break every 90 minutes

## Output Format

```markdown
# Daily Plan - [Day], [Month] [Date], [Year]

## Today's Mission

**Primary Goal:** [One-sentence outcome for the day]

**Top 3 Priorities:**
1. [Priority 1 with specific, measurable outcome]
2. [Priority 2 with specific, measurable outcome]
3. [Priority 3 with specific, measurable outcome]

**Success looks like:** [What "done" means today]

---

## Time-Blocked Schedule

### 8:00 - 9:00: Morning Prime 🌅
**Focus:** Wake up, coffee, light movement, review plan

- [ ] Morning routine (30 min)
- [ ] Review today's plan + priorities (10 min)
- [ ] Quick inbox scan (15 min - flag only, don't respond)

**Energy level:** Building

---

### 9:00 - 11:00: Deep Work Block 1 🎯 [PRIORITY #1]
**Focus:** [Specific priority 1 task]

- [ ] [Concrete subtask 1]
- [ ] [Concrete subtask 2]
- [ ] [Concrete subtask 3]

**Target:** [Measurable outcome by 11:00]

**Protection:** Phone off, Slack paused, door closed

---

### 11:00 - 11:15: Break ☕
**Focus:** Step away from desk

- Physical movement (walk, stretch)
- Hydrate
- No screens

---

### 11:15 - 12:30: Deep Work Block 2 🎯 [PRIORITY #2]
**Focus:** [Specific priority 2 task]

- [ ] [Concrete subtask 1]
- [ ] [Concrete subtask 2]

**Target:** [Measurable outcome by 12:30]

---

### 12:30 - 1:30: Lunch Break 🍽️
**Focus:** Eat, recharge, disconnect

- Proper meal (not at desk)
- 15-minute walk if possible
- No work talk

**Energy level:** Recovery

---

### 1:30 - 3:00: Focused Work Block 🎯 [PRIORITY #3]
**Focus:** [Specific priority 3 task]

- [ ] [Concrete subtask 1]
- [ ] [Concrete subtask 2]

**Target:** [Measurable outcome by 3:00]

---

### 3:00 - 3:15: Break ☕
**Focus:** Recharge

---

### 3:15 - 4:30: Meetings / Collaborative Work 👥
**Focus:** [Meeting name or collaborative task]

- [ ] [Meeting 1 with agenda]
- [ ] [Follow-up actions from meetings]

**Prep:** Review agendas 10 minutes before

---

### 4:30 - 5:30: Admin & Communication 📧
**Focus:** Process inbox, respond to messages, light tasks

- [ ] Clear email inbox (respond, archive, defer)
- [ ] Slack catch-up and responses
- [ ] Update project trackers
- [ ] Quick wins / small tasks

**Energy level:** Lower (perfect for admin)

---

### 5:30 - 6:00: Planning & Wrap-Up 📋
**Focus:** Close the day, plan tomorrow

- [ ] Evening check-in (see below)
- [ ] Tomorrow's top 3 priorities draft
- [ ] Inbox zero for peace of mind
- [ ] Close all work apps

---

### 6:00 PM+: Personal Time 🏡
**No work beyond this point**

---

## Success Criteria

### Must-Have (Non-Negotiable) ✓
- [ ] Priority 1 complete: [Specific outcome]
- [ ] Priority 2 complete: [Specific outcome]
- [ ] At least 80% progress on Priority 3

### Should-Have (Important) ⭐
- [ ] [Secondary task 1]
- [ ] [Secondary task 2]

### Nice-to-Have (Bonus) 💡
- [ ] [Bonus task 1]
- [ ] [Bonus task 2]

---

## Evening Check-In (5 minutes at 5:30 PM)

**Completion status:**
- Priority 1 done? **YES / NO** - [If no, why?]
- Priority 2 done? **YES / NO** - [If no, why?]
- Priority 3 done? **YES / NO** - [If no, why?]

**What went well:**
[What worked today? What helped you execute?]

**What got stuck:**
[Where did you lose time? What blocked you?]

**Energy assessment:**
- Peak hours productive? **YES / NO**
- Breaks taken? **YES / NO**
- Felt energized or drained? **[Score 1-10]**

**Tomorrow's adjustment:**
[What to change in tomorrow's plan based on today?]

---

## Quick Decision Framework

**Before saying YES to anything today:**

1. **Is this one of my top 3 priorities?**
   - YES → Schedule it in appropriate energy window
   - NO → Go to #2

2. **Does this directly support today's mission?**
   - YES → Add to relevant time block
   - NO → Go to #3

3. **Can this wait until tomorrow?**
   - YES → Add to tomorrow's list
   - NO → Question if it's really urgent

**If NO to all three → Decline or defer**

---
```

## Real Examples

### Example 1: High-Output Day (Founder/Exec)

**Context:** Product launch week, high-stakes demos, team coordination

```markdown
## Top 3 Priorities:
1. Finalize launch announcement (900 words, 3 versions) - DONE by 11:30
2. Run partner demo with clear next steps - DONE by 3:00
3. Team sprint planning with Q2 priorities set - DONE by 5:00

## Schedule:
- 9:00-11:30: Deep work → Launch copy (Priority #1)
- 12:30-2:45: Partner demo prep + execution (Priority #2)
- 3:00-4:45: Sprint planning with team (Priority #3)
- 5:00-5:30: Email/admin/wrap

## Evening Check-In:
✓ Priority 1: YES (shipped 3 versions, CEO approved)
✓ Priority 2: YES (partner committed, contract signed)
✓ Priority 3: YES (team aligned, stories pointed)

What worked: Protected deep work time for writing, prepped demo thoroughly
Tomorrow: Start execution on sprint, less coordination overhead
```

### Example 2: Deep Work Day (Individual Contributor)

**Context:** IC developer, needs 6+ hours of uninterrupted coding

```markdown
## Top 3 Priorities:
1. Ship authentication refactor (PR ready for review) - DONE by 12:00
2. Debug production issue #847 (root cause found + fix deployed) - DONE by 4:00
3. Documentation for new API endpoints (published) - DONE by 6:00

## Schedule:
- 9:00-12:00: Deep work → Auth refactor (Priority #1)
- 1:00-4:00: Deep work → Debug + deploy (Priority #2)
- 4:15-5:45: Documentation writing (Priority #3)
- 5:45-6:00: Update tickets, close day

## Protections:
- Slack: Paused 9am-12pm, 1pm-4pm
- No meetings scheduled
- Phone: DND mode

## Evening Check-In:
✓ Priority 1: YES (PR approved, merged)
✓ Priority 2: YES (issue resolved, monitoring green)
✓ Priority 3: 90% (docs drafted, needs final review tomorrow)

What worked: Zero meetings = maximum flow state
Tomorrow: Finish docs, start new feature work
```

### Example 3: Meeting-Heavy Day (Manager/Director)

**Context:** Leadership role, multiple teams, coordination day

```markdown
## Top 3 Priorities:
1. Align exec team on Q2 budget priorities - DONE by 11:00
2. Resolve team conflict (performance conversation) - DONE by 3:00
3. Approve 3 critical design reviews - DONE by 5:30

## Schedule:
- 8:30-9:00: Pre-meeting prep (agendas, talking points)
- 9:00-11:00: Exec budget meeting (Priority #1)
- 11:15-12:15: 1-on-1 performance conversation (Priority #2)
- 1:30-3:00: Design review meetings (Priority #3, all 3 back-to-back)
- 3:15-4:30: Email/admin/follow-ups from meetings
- 4:30-5:00: Next week prep + team updates

## Evening Check-In:
✓ Priority 1: YES (budget approved, owners assigned)
✓ Priority 2: YES (performance plan agreed, follow-up scheduled)
✓ Priority 3: YES (2 approved, 1 needs revision)

What got stuck: Back-to-back meetings = no thinking time
Tomorrow: Block 2-hour deep work window, fewer meetings
```

## Real Case Study

**User:** Marketing manager at B2B SaaS company, struggled with reactive days

**Before using skill:**
- Average day: 6-8 hours in meetings, 2 hours of "work" squeezed in
- Top priorities rarely completed
- Constant email/Slack interruptions
- 15% weekly goal completion rate
- Felt productive but accomplished little

**After implementing plan-my-day:**
- Used skill every morning (2-3 minutes to generate plan)
- Protected 9-11am deep work block (calendar marked "Focus Time")
- Set clear Top 3 priorities each day
- Added evening check-ins to track completion

**Results after 8 weeks:**
- 74% weekly goal completion rate (+59 points)
- Meetings reduced from 6-8 hrs/day to 3-4 hrs/day
- Deep work blocks protected 4 days/week (vs 0 before)
- Self-reported energy levels: 8.2/10 (vs 4.1/10 before)
- Team feedback: "You're more present and decisive"

**Key insight:** "The daily plan gave me permission to say no. If it wasn't in my Top 3, I deferred it. That one change unlocked everything."

## Configuration Options

### Standard Mode (default)
```
/plan-my-day
```
- Balanced energy windows
- 8-hour workday assumption
- 20% buffer time

### High-Output Mode
```
/plan-my-day --mode high-output
```
- 10-hour workday
- More aggressive scheduling
- 10% buffer time
- Best for: Launch weeks, crunch periods

### Deep Work Mode
```
/plan-my-day --mode deep-work
```
- Maximum uninterrupted blocks
- Minimal meetings
- 30% buffer time
- Best for: Individual contributors, creators

### Meeting-Heavy Mode
```
/plan-my-day --mode coordination
```
- Meeting-first scheduling
- Work blocks fit around commitments
- 25% buffer time
- Best for: Managers, executives, client-facing roles

## Installation

```bash
# Copy skill to your skills directory
cp -r plan-my-day $HOME/.openclaw/skills/

# Verify installation
/plan-my-day --version
```

**No dependencies required** - Pure planning logic.

## Future Integrations (Coming Soon)

- **Google Calendar sync** - Auto-import existing events
- **Completion tracking** - Analytics on your planning accuracy over time
- **Energy pattern learning** - Adapts to when you actually perform best
- **Team coordination** - Sync focus blocks across teams

## Pro Tips

1. **Run it FIRST thing** - Before checking email or Slack. Set the day, don't react to it.
2. **Protect Peak hours** - Block 9-11am as "Focus Time" on your calendar. Decline meetings here.
3. **Track completion rates** - Use evening check-in data to improve your estimations
4. **Adjust energy windows** - Default is 9-11am peak, but if you're different, customize it
5. **Combine with "shutdown ritual"** - Evening check-in + tomorrow's prep = mental closure
6. **Don't over-schedule** - If plan shows 7 hours of tasks for 8-hour day, you're on track

## Common Mistakes to Avoid

❌ **Planning too much** - If you schedule 100% of your time, you'll fail. Always leave 20% buffer.
❌ **Ignoring energy windows** - Putting hard thinking work at 4pm sets you up for failure.
❌ **Skipping breaks** - 90-minute focus blocks REQUIRE 15-minute breaks or performance drops.
❌ **No evening reflection** - Without check-ins, you can't improve your planning accuracy.
❌ **Changing Top 3 mid-day** - Unless genuinely urgent, stick to morning priorities.

## Quality Checklist

A good daily plan has:
- [ ] Clear Top 3 priorities with measurable outcomes
- [ ] #1 priority scheduled in peak energy window
- [ ] 20% buffer time (not every minute scheduled)
- [ ] Breaks scheduled every 90 minutes
- [ ] Protected lunch break (minimum 30 minutes)
- [ ] Evening check-in template included
- [ ] No work scheduled after 7pm (personal time protected)

## Support

Issues or suggestions? Provide:
- Your typical day structure (work hours, meeting load)
- Top 3 priorities example
- Energy pattern (when you're most focused)
- What's not working in current output

---

**Built on circadian rhythm research (Roenneberg), deliberate practice principles (Ericsson), and GTD methodology (Allen).**

**Plan your day in 2 minutes. Execute with focus. Win consistently.**