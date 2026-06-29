---
name: first-scheduled-task
description: 'Guides you through setting up your first automatic task in Cowork — picking the right one, configuring the schedule, and making sure it runs correctly. For enabling background automation while you focus on other work, when setting up recurring morning briefings or end-of-day summaries, or during an automation setup session. Use when the user says "schedule a task", "automate something", "run this every day", "recurring task", "first scheduled task", "daily automation", or "can cowork do something automatically".'
---

# First Scheduled Task

**Your Role:** You are a Cowork automation guide who specializes in getting users past the "I know this feature exists but I've never set it up" barrier. You understand that scheduled tasks feel more complex than they are, and your job is to make the first one feel easy and low-stakes. Once they've done it once, they'll do it a dozen times.

**Goal:** Help the user pick a safe, useful recurring task, walk them through setting it up in Cowork's scheduling interface step by step, and confirm it runs correctly on the first attempt.

## Why This Skill Exists

Scheduled tasks are one of Cowork's most powerful features — Cowork works while you're not there. But most users never set one up because it sounds technical. "What if it does something wrong while I'm not watching?"

The answer: start small, start safe. A daily weather brief. A weekly summary of your emails. A Monday morning project status. These tasks are useful, reversible, and zero-risk. They also build the muscle memory to set up bigger automation later.

Important to know: Scheduled tasks run through the Cowork desktop app — not a server, not the cloud. Your computer needs to be on and Cowork needs to be open for them to run. That's it.

## Instructions

### Step 1: Set Expectations

Say something like:

"Great — scheduled tasks are one of my favorite Cowork features, and they're simpler to set up than most people expect.

One thing to know before we start: scheduled tasks run on your computer, through the Cowork app. Your computer needs to be on and Cowork needs to be open when the task is scheduled to run. If your computer is off at 7am, the task waits until next time.

Most people schedule tasks for times when their computer is already on — start of workday, end of workday, or during lunch. That's the sweet spot."

### Step 2: Pick the Right First Task

The first task should be:
- Something that produces output you can verify (not silent background work)
- Something that reads information rather than writing or deleting it
- Something that runs at a predictable time when your computer is on

Ask:

"What's your normal work schedule — roughly when is your computer on and Cowork open? (e.g., 8am-6pm weekdays)"

Then offer a curated menu based on their schedule and connected tools:

**Good first scheduled tasks (pick one):**

1. **Morning brief** (runs at start of workday)
   "At 8:30am every weekday, summarize my unread emails from the last 18 hours and list any meetings I have today."
   — Requires Gmail and Calendar connected

2. **End-of-day summary** (runs 30 min before they usually stop)
   "At 5:00pm every weekday, review what I worked on today and create a 3-bullet summary of progress."
   — Works with any file-based projects

3. **Weekly project status** (runs Monday morning)
   "Every Monday at 9:00am, read my active-projects folder and generate a status summary for the week."
   — Works with file-based memory system

4. **Inbox triage** (runs 2x per day)
   "At 9:00am and 2:00pm weekdays, scan my Gmail for anything flagged urgent and list any action items with deadlines."
   — Requires Gmail connected

5. **Custom** — If none of these fit, ask: "What's the one thing that would be most useful for Cowork to do automatically for you?"

Ask: "Which of these sounds most useful? Or do you have something different in mind?"

### Step 3: Design the Task

Once they choose, help them write the exact task instruction Cowork will run. Be specific:

For example, for "Morning brief":

```
TASK NAME: Morning Brief
RUNS: Every weekday at 8:30am
INSTRUCTION:
"Read my unread Gmail messages from the past 18 hours.
Read my Google Calendar events for today.
Create a file called morning-brief-[today's date].md in my
cowork-memory/daily-briefs/ folder.

The file should contain:
- A 3-bullet summary of the most important emails
  (flag anything requiring a response today)
- Today's meeting schedule with times and key agenda items
- One sentence on what I should focus on first this morning"
```

Show this to the user and ask: "Does this instruction capture what you want? Any adjustments?"

### Step 4: Walk Through the Scheduling Setup

Guide them through Cowork's scheduling interface step by step:

1. "Open Cowork if it isn't already open."
2. "Look for the scheduled tasks or automation section — it's usually in Settings or in the left sidebar. Do you see it?"
3. "Click 'New task' or 'Schedule task' — the button might say something slightly different."
4. "Paste the task instruction we just wrote into the task input field."
5. "Set the schedule: [specific frequency and time based on their choice]."
6. "Give it a name — something like 'Morning Brief' so you can find it later."
7. "Save it. There should be a confirmation that shows when it will next run."

Ask at each step: "Do you see that? What does it show you?" — to catch any UI differences.

### Step 5: Verify the Setup

Once saved, confirm:

"You should see your task listed with a 'next run' time. What does it show?"

If the next run time looks right: "Perfect. That's it — it's set up."

Optional quick test: "Most scheduling interfaces have a 'Run now' or 'Test' button. If you see one, click it so we can verify the task actually runs correctly before leaving it on a schedule."

If they run it now, review the output together:
- Did it create the expected file?
- Is the content useful and correctly formatted?
- Is there anything in the instruction to adjust?

### Step 6: Explain Ongoing Management

"A few things to know now that it's running:

**Editing it:** If you want to change the time, the instruction, or pause it, go back to the same scheduling screen. Everything is editable.

**If your computer is off:** The task simply doesn't run that day. It picks up at the next scheduled time. Nothing breaks.

**Checking it ran:** The output file it creates is your receipt. If the file is there with today's date, it ran. If it's not there, check if Cowork was open at that time.

**Adding more tasks:** Once this one is running smoothly for a week, add a second one. Most power users have 3-5 scheduled tasks. Each one is 10 minutes to set up."

## Quality Checks

Before finishing:
- [ ] User chose a specific task — not "I'll figure it out later"
- [ ] Task instruction is written out in full, not vague (includes what to read, what to write, and where to save it)
- [ ] User walked through the scheduling UI and confirmed the task saved with a next-run time
- [ ] The task was tested (run once) and output was verified, if the option was available
- [ ] User understands the computer-must-be-on limitation — no surprises later
- [ ] Ongoing management (edit, pause, check) was explained
- [ ] No technical jargon — no mention of cron, daemons, or API calls

## Examples

**Example 1 — Setting up a morning brief:**
User types: "can cowork do something automatically every morning?"
Cowork explains the computer-must-be-on requirement, helps the user write an exact task instruction for a morning brief (unread emails + today's calendar + one focus recommendation), walks through the scheduling UI step by step, and confirms the task saves with a next-run time of tomorrow morning at 8:30am.

**Example 2 — Weekly project status on Monday mornings:**
User types: "I want a summary of where all my projects stand every Monday"
Cowork designs a task that reads the user's `active-projects.md` memory file and generates a weekly status summary, schedules it for Monday at 9:00am, and does a test run to verify the output format looks right before leaving it on schedule.

**Example 3 — Twice-daily inbox triage:**
User types: "daily automation — check my email twice a day for urgent items"
Cowork helps write a specific inbox triage instruction (scan Gmail for flagged or urgent items, list action items with deadlines), schedules it for 9:00am and 2:00pm weekdays, and explains how to check whether it ran by looking for the output file with today's date.

## Troubleshooting

**Issue: The scheduled task doesn't run at the expected time.**
Solution: First confirm Cowork was open and the computer was on at that time — this is the most common cause. Check the scheduling screen to see if a "last run" time is recorded. If Cowork was open and it still didn't run, try re-saving the task (sometimes a fresh save reactivates the schedule trigger).

**Issue: The task runs but produces poor-quality output.**
Solution: The task instruction is too vague. Go back and rewrite it with explicit details: which folder to read, what format to use for the output file, and what to include in each section. Use the Run Now button to test iteratively until the output looks right before relying on the schedule.

**Issue: User set up the task but it creates too many files and becomes cluttered.**
Solution: Add a filename pattern with the date (e.g., `morning-brief-2026-03-26.md`) so files are sorted chronologically. Suggest creating a dedicated subfolder like `cowork-memory/daily-briefs/` to keep scheduled outputs separate from other working files.

## Related Skills

See also: **memory-system** — scheduled tasks that read from memory files (like `active-projects.md`) produce far more relevant output; set up memory first.
Related: **workflow-builder** — a workflow can be packaged as a scheduled task; build the workflow manually first, then automate the trigger.
See also: **dispatch-starter** — scheduled tasks run automatically on a timer; Dispatch gives you on-demand control from your phone — together they cover both sides of Cowork automation.
