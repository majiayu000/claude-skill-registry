---
name: Focus Session Manager
description: Automatically manage focus sessions, breaks, and hyperfocus protection. Uses ADHD-optimized Pomodoro technique with flexible timers, health reminders, and gentle interruptions. Protects against hyperfocus burnout while maximizing productive time.
version: 1.0.0
---

# Focus Session Manager

**Protect your health. Maximize focus. Prevent burnout.**

## Core Principle

ADHD brains are prone to hyperfocus (ignoring breaks, health) and time blindness (losing track of time). The solution: Automated session management that tracks time, enforces breaks, and protects health without disrupting flow state.

**Key Insight:** You can't manage time you can't see. Make time visible and automatic.

---

## The Focus Problem

### Problem 1: Hyperfocus Burnout

**Issue:** Code for 4 hours straight without break
**Result:** Exhaustion, health issues, reduced quality

### Problem 2: Time Blindness

**Issue:** "I'll work for 30 min" → Actually 3 hours
**Result:** Missed meetings, forgotten commitments, burnout

### Problem 3: Break Resistance

**Issue:** "Just one more thing" never stops
**Result:** No breaks, deteriorating health, reduced productivity

### Problem 4: Disrupted Flow

**Issue:** Harsh timer interruptions break concentration
**Result:** Frustration, ignoring timers, no break system

---

## Phase 1: Automatic Session Tracking

### Always-On Time Tracking

**Starts automatically when you begin coding:**

```markdown
[Session Started: 14:00]

⏱️ Focus Timer Running
📊 Today's focus time: 0 hours
🎯 Goal: 4 hours
🔥 Current streak: 2 days

Mode: Deep Work
Next break: 14:25 (in 25 min)
```

### Visible Time Display

**Status bar shows:**

```
⏱️ 23:45 | 🧠 Focus Session 1/4 | 💧 Water reminder soon
```

### Session Types (Auto-Detected)

**Deep Work:** Complex coding, architecture

- Duration: 45-90 minutes
- Break: 15 minutes
- Best for: New features, debugging

**Quick Tasks:** Bug fixes, updates

- Duration: 25 minutes
- Break: 5 minutes
- Best for: Small fixes, reviews

**Learning:** Reading docs, tutorials

- Duration: 30 minutes
- Break: 10 minutes
- Best for: New tech, research

---

## Phase 2: ADHD-Optimized Pomodoro

### Traditional Pomodoro (ADHD-Hostile)

❌ Rigid 25-min timer (might be mid-thought)
❌ Harsh interruption (breaks flow)
❌ Forced break (when you're in flow)
❌ No hyperfocus protection (ignores long sessions)

### ADHD-Friendly Pomodoro

✅ Flexible timers (25/45/90 min options)
✅ Gentle reminders (dismissable but persistent)
✅ Flow-aware breaks (suggests good stopping points)
✅ Hyperfocus detection (escalating alerts)

### Smart Break Timing

```markdown
[25 minutes elapsed]

🟡 Break suggestion available

Good stopping point detected:

- ✅ Just committed code
- ✅ Tests passing
- ✅ Natural pause point

Take 5-minute break?
[Take Break Now] [Extend 15 min] [Remind in 5 min]
```

---

## Phase 3: Break Management

### Break Types

**Micro-Break (2 minutes):**

- Look away from screen (20-20-20 rule)
- Stretch in chair
- No leaving desk

**Short Break (5 minutes):**

- Stand up
- Walk around
- Get water
- Bathroom

**Medium Break (15 minutes):**

- Walk outside
- Snack
- Different room
- Social interaction

**Long Break (30-60 minutes):**

- Meal
- Exercise
- Complete context switch

### Automatic Break Reminders

```markdown
[After 25 min coding]

⏸️ Break Suggestion (5 minutes)

Your brain has been focused for 25 min.
Short break will improve next session.

Break activities:

- [ ] Stand and stretch
- [ ] Get water
- [ ] Look out window (eyes)
- [ ] Bathroom if needed

Timer: 5 minutes
Resume automatically after break.

[Start Break] [Extend Session] [Dismiss]
```

### Break Enforcement Levels

**Level 1: Gentle Reminder (25-45 min)**

```
💭 Reminder: Break time soon
[Dismissable, comes back in 10 min]
```

**Level 2: Strong Suggestion (45-90 min)**

```
⚠️ You've been coding for 60 minutes
Break highly recommended
[Dismissable twice, then escalates]
```

**Level 3: Health Alert (90+ min)**

```
🚨 HEALTH ALERT: 90 min no break

This is affecting:
- Eye strain
- Back pain
- Mental fatigue
- Code quality

Required actions:
- [ ] Stand up NOW
- [ ] 2-minute walk
- [ ] Water

[Cannot dismiss until you move]
```

**Level 4: Forced Break (3+ hours)**

```
🛑 MANDATORY BREAK

You've been coding for 3 hours straight.
Context saved automatically.
Dev server paused.

Required 15-minute break.
I'll help you resume after.

[Break Started - Timer: 15:00]
```

---

## Phase 4: Hyperfocus Protection

### Hyperfocus Detection

**Triggers at 90 minutes continuous work:**

```markdown
[90 minutes elapsed]

🔍 HYPERFOCUS DETECTED

You've been deeply focused for 90 minutes.
This is good for productivity BUT...

Health check required:

- [ ] When did you last drink water? \_\_\_\_
- [ ] When did you last move? \_\_\_\_
- [ ] Are your eyes strained? Y/N
- [ ] Do you need bathroom? Y/N

If 2+ concerns: TAKE BREAK NOW
If 0-1 concerns: Can extend 30 min

[Take Break] [Extend 30min] [Health Check]
```

### The Hyperfocus Paradox

**Good Hyperfocus:** Deep work on right thing
**Bad Hyperfocus:** Stuck optimizing CSS for 4 hours

### Detecting Bad Hyperfocus

```markdown
[2 hours on same file, many reverts]

💭 Gentle check-in:

I notice you've been working on button.css
for 2 hours with 12 commits and 5 reverts.

Questions:

- Is this P0 for shipping? YES/NO
- Could this be "good enough" now? YES/NO
- Are you stuck in perfectionism? YES/NO

Maybe time to:

- Commit current state
- Move to next task
- Come back later with fresh eyes

[Keep Going] [Take Break] [Switch Tasks]
```

---

## Phase 5: Session Planning

### Daily Session Plan (Auto-Generated)

```markdown
# Today's Focus Sessions

Total available: 6 hours
Sessions planned: 4

Morning (9am - 12pm):

- Session 1: Build dashboard UI (45 min) 🔨
  Break: 10 min
- Session 2: Connect to API (45 min) 🔨
  Break: 10 min
- Session 3: Handle errors (30 min) ⚡
  Break: Lunch (60 min)

Afternoon (1pm - 5pm):

- Session 4: Write tests (45 min) 🧪
  Break: 10 min
- Session 5: Code review (30 min) 👀
  Break: 10 min
- Session 6: Deploy (20 min) 🚀
  Break: End of day

Total focus time: 4.5 hours
Buffer time: 1.5 hours (interruptions)

Realistic and achievable! 💪
```

### Energy-Aware Scheduling

```markdown
Morning Energy: High ⚡⚡⚡

- Schedule: Complex tasks (new features)
- Session length: 45-90 min
- Break length: 10 min

Afternoon Energy: Medium ⚡⚡

- Schedule: Medium tasks (bug fixes)
- Session length: 30-45 min
- Break length: 15 min

Evening Energy: Low ⚡

- Schedule: Easy tasks (docs, reviews)
- Session length: 25 min
- Break length: 5-10 min
```

---

## Phase 6: Context-Aware Breaks

### Before-Break Ritual (Automatic)

```markdown
[Break starting in 1 minute]

Quick save (30 seconds):
✅ Auto-committing code
✅ Saving mental state
✅ Noting next step

You were: Adding email validation
Next: Test validation logic (10 min)

Break ready! Take 5 minutes.
Resume will be easy.
```

### After-Break Ritual (Automatic)

```markdown
[Break ended]

Welcome back! (Rested: 5 minutes)

Quick recap:
📍 File: src/components/form.tsx:42
💭 You were: Adding email validation
🎯 Next: Test validation logic (10 min)
⏱️ Session: 25 minutes

[Resume button opens file at exact line]

Estimated resume time: 30 seconds
```

---

## Phase 7: Health Monitoring

### The 20-20-20 Rule (Auto-Enforced)

**Every 20 minutes: Look at something 20 feet away for 20 seconds**

```markdown
[20 minutes screen time]

👁️ Eye Break (20 seconds)

Look at something 20 feet away.
Clock will count down.

20... 19... 18... 17...

[Countdown with calming animation]

✅ Done! Eyes protected.
```

### Hydration Reminders

```markdown
[60 minutes since last water reminder]

💧 Hydration Check

When did you last drink water?

- Just now: Reset timer
- 30 min ago: Doing okay
- 1+ hour ago: Go drink NOW

ADHD brains often forget water.
Dehydration affects focus.

[I drank water] [Remind in 30min]
```

### Movement Tracking

```markdown
[90 minutes sitting]

🚶 Movement Required

You've been sitting for 90 minutes.
This affects:

- Blood flow
- Energy levels
- Back health
- Focus quality

Minimum: Stand for 2 minutes
Better: Walk for 5 minutes
Best: Go outside

[I moved] [Remind in 15min]
```

---

## Phase 8: Transition Rituals

### Starting Work Ritual

```markdown
[Morning start]

☀️ Good morning! Let's start work.

Quick setup (2 minutes):

1. Review today's plan ✅
2. Set focus goal: 4 hours
3. Pick first task ✅
4. Start focus timer ✅

First session: Dashboard UI (45 min)
Next break: 9:45am

Let's do this! 💪

[Start Session]
```

### Ending Work Ritual

```markdown
[5pm - End of day]

🌙 Wrapping up for the day?

Today's stats:

- Focus time: 4.5 hours ✅
- Sessions completed: 6
- Breaks taken: 5
- Tasks completed: 7

Tomorrow setup:

- First task: Test password reset (30 min)
- Should be quick! Easy start.

Wins today:
✅ Built entire dashboard UI
✅ Connected to API
✅ Fixed 2 bugs

You crushed it today! 🎉

[End Day] [Keep Working]
```

### Task Switch Ritual

```markdown
[Switching from Task A to Task B]

🔄 Task Switch

Saving Task A context...
✅ Committed work
✅ Saved mental state

Loading Task B...
✅ Opened files
✅ Loaded context
✅ Showing next step

Switch time: 2 minutes

Ready for Task B!
```

---

## Phase 9: Distraction Management

### Focus Mode Levels

**Level 1: Normal (Default)**

- Notifications: On
- Chat: Available
- Interruptions: Allowed

**Level 2: Focus Mode**

- Notifications: Snoozed
- Chat: Away status
- Interruptions: Emergency only

**Level 3: Deep Work Mode**

- Notifications: Off
- Chat: Do not disturb
- Interruptions: None
- Music: Focus playlist auto-starts

### Auto-Enable Focus Mode

```markdown
[Deep work session starting]

Enabling Focus Mode:
✅ Notifications snoozed
✅ Chat status: Away
✅ Email closed
✅ Focus music started

Distractions minimized.
You have 45 minutes of protected time.

[Session starting...]
```

### Distraction Recovery

```markdown
[You opened Twitter mid-session]

💭 Distraction detected!

You were focused on: Building dashboard
Time lost: 5 minutes
Session time remaining: 15 minutes

Quick reset:

- [ ] Close Twitter
- [ ] Take 2-minute break
- [ ] Resume with fresh focus

Or:

- [ ] Take full break now (5 min)
- [ ] Resume with new session

No judgment! ADHD brains wander.
Let's just get back on track. 💪
```

---

## Phase 10: Session Analytics

### Daily Stats (Auto-Generated)

```markdown
# Today's Focus Summary

⏱️ Total Focus Time: 4.5 hours
🎯 Goal: 4 hours (exceeded! 🎉)
📊 Sessions: 6 completed
⏸️ Breaks: 5 taken
🔥 Longest session: 90 min
💧 Water reminders: 6 (all completed)
👁️ Eye breaks: 12 (all completed)

Top productive hours:
9am-11am: 2 hours deep work ⚡
2pm-4pm: 1.5 hours ⚡

Distraction time: 30 min (acceptable)

Health score: 9/10 (excellent!)

- Took all breaks ✅
- Drank water ✅
- Eye breaks ✅
- Moved regularly ✅

Tomorrow's recommendation:
Same pattern works well for you!
```

### Weekly Trends

```markdown
# This Week's Focus Patterns

Mon: 4.5 hours (great!)
Tue: 3 hours (interrupted day)
Wed: 5 hours (best day! 🔥)
Thu: 4 hours (solid)
Fri: 2 hours (expected lower)

Weekly average: 3.7 hours/day
Trend: +15% vs last week 📈

Best times for deep work:

- 9-11am (morning energy)
- 2-4pm (post-lunch focus)

Avoid scheduling deep work:

- 11am-1pm (pre-lunch slump)
- 4-5pm (end of day fatigue)

Keep the momentum! 💪
```

---

## Automation

### Auto-Start (Session Detection)

```markdown
[You opened VS Code at 9:00am]

Good morning! Starting focus session...

✅ Timer started
✅ First task loaded
✅ Break scheduled (9:45am)
✅ Focus mode enabled

Session: Build dashboard UI
Duration: 45 minutes

Let's code! 🚀
```

### Auto-Pause (Inactivity Detection)

```markdown
[No code changes for 10 min]

Session paused automatically.

Are you:

- Taking a break? (Timer paused)
- In a meeting? (Session saved)
- Distracted? (Gentle reminder)
- Done for now? (End session)

[Resume] [Take Break] [End Session]
```

### Auto-End (5pm Default)

```markdown
[5:00pm]

End of work day!

Auto-wrapping up:
✅ Session saved
✅ Context preserved
✅ Stats logged
✅ Tomorrow prepared

See you tomorrow! 🌙
```

---

## Success Metrics

You're using this well when:

- ✅ Taking regular breaks (not skipping)
- ✅ Hyperfocus sessions < 90 min
- ✅ Health checks completed (water, eyes, movement)
- ✅ Focus time increasing (sustainable pace)
- ✅ End-of-day energy higher (not exhausted)

---

## Related Skills

- **context-preserver** - Auto-saves state before/after breaks
- **task-breakdown-specialist** - Plans work for sessions
- **completion-coach** - Helps finish sessions strong

---

**Focus hard. Break often. Protect your health.** ⏱️
