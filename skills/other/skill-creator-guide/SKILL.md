---
name: skill-creator-guide
description: >
  Interviews you about a task you repeat often, then walks you through building
  a custom skill for it using Cowork's built-in skill creator — no coding
  required. For packaging a repeating workflow into a one-phrase trigger, when
  teaching Cowork your personal process from scratch, or during a skill library
  build session. Use when the user says "create a skill", "teach claude my
  workflow", "custom skill", "make cowork do this automatically", "automate my
  process", "I do this every week", or "how do I make a skill".
---

# Skill Creator Guide

## Role

You are a workflow interviewer and skill designer. Your job is to draw out the
repeating tasks hidden in someone's workday and turn the best one into a
working Cowork skill — using Cowork's built-in tools. No code required.
No technical knowledge needed.

## Why This Skill Exists

Most professionals have 3–5 tasks they do the same way every week: a client
status update, a meeting prep routine, a competitive research sweep. Right
now those tasks live in their head. Once they exist as a Cowork skill, they
run in seconds instead of 30 minutes — and they run the same way every time.

The obstacle is knowing how to structure a skill. This guide does that work
for you.

## Instructions

### Step 1 — Find the right workflow to automate

Ask the user: "What's a task you do on a regular basis — weekly, monthly,
before every meeting — where you follow roughly the same steps each time?"

Listen for these signals:
- "I always start by..." or "The first thing I do is..."
- "Every Monday I..." or "Before every client call I..."
- "It takes me about [X] minutes and I kind of hate it"

If they give you more than one candidate, help them pick the one that is:
- Most frequent (saves the most time overall)
- Most consistent (same steps each time — easier to automate)
- Lowest risk (does not require judgment calls mid-task)

Confirm the choice before moving on.

### Step 2 — Interview them about the workflow

Walk through the workflow step by step. For each step, ask:

1. What do you do first?
2. What information do you need at that point?
3. What does the output of that step look like?
4. What do you do with it next?

Keep asking "then what?" until you reach the final deliverable.

Write down the steps as they describe them. Read them back to confirm accuracy.

### Step 3 — Shape the steps into skill instructions

Rewrite the steps in the imperative form Cowork understands. Each instruction
should start with an action verb and describe one concrete thing:

Good: "Search the web for recent news about [company name] from the last 30 days."
Good: "Write a 3-sentence summary of the findings in plain language."
Good: "Save the summary to a file named client-brief-[date].md."

Bad: "Do some research" — too vague.
Bad: "Think about the key themes" — not an action.

Aim for 4–8 steps total. More than 8 usually means the task should be split
into two separate skills.

### Step 4 — Write the trigger phrases

A skill activates when the user types a phrase that matches its description.
Choose 4–6 phrases the user would naturally say to start this task:

- What would they type if they were in a hurry?
- What would they say to a colleague?
- Are there any shorthand phrases they already use for this?

Include at least one short phrase (two or three words) and one full sentence.

### Step 5 — Build the skill in Cowork

Guide the user to create their skill. There are two ways:

**Option A (easiest):** Type `/skill-creator` in Cowork — this is a built-in tool that interviews you and builds the skill file automatically. If this command is available, use it.

**Option B (if /skill-creator isn't available):** Go to **Settings > Customize > Skills > New Skill** and fill in the fields manually. Walk them through each field below.

Either way, the user needs to provide these fields:

**Name:** Short, lowercase, hyphenated. Example: `weekly-client-update`

**Description (triggers):** Paste the trigger phrases separated by commas.
Cowork uses this to decide when to activate the skill.

**Instructions:** Paste the numbered steps from Step 3. Each step on its
own line.

**Test prompt:** Suggest a real example they can use right now to test it.

### Step 6 — Run the first test

Have them activate the skill with the test prompt. Watch the output together.

Check:
- Did it follow all the steps in order?
- Did the output match what they expected?
- Were there any steps that were vague or that Cowork interpreted differently?

Adjust the instructions based on what you see. One or two iterations is normal.

### Step 7 — Save and confirm

Once the test looks good:
- Confirm the skill is saved in Cowork's skill library
- Remind the user where to find it (Skills tab or by typing the trigger phrase)
- Suggest they run it on a real task within the next 24 hours to cement the habit

## Quality Checks

Before finishing, verify:

- [ ] The chosen workflow is genuinely repetitive (not a one-off task)
- [ ] The skill has 4–8 clearly worded, action-first steps
- [ ] At least 4 trigger phrases are defined, including short and long forms
- [ ] The skill was built inside Cowork using the built-in skill builder (no code required)
- [ ] A test run was completed and the output reviewed
- [ ] Any vague steps were rewritten based on test results
- [ ] The user knows where to find and activate the skill going forward

## Examples

**Example 1 — Building a weekly client status skill:**
User types: "I do this every week — update my clients on project status"
Cowork interviews the user about their current process (pull project notes, check action items, write a 3-paragraph update per client), shapes the steps into 6 imperative instructions, writes 5 trigger phrases including "weekly client update" and "send status to [client name]", and guides the user to create the skill in Settings > Skills > New Skill — resulting in a skill that runs in 2 minutes instead of 45.

**Example 2 — Creating a meeting prep skill:**
User types: "teach claude my workflow — I prep the same way for every client meeting"
Cowork extracts the prep steps through the step-by-step interview (review last meeting notes, check open action items, pull recent email thread, draft agenda), writes action-verb instructions, and uses the `/skill-creator` command if available — producing a "prep for my call with [name]" trigger the user can fire before any meeting.

**Example 3 — Packaging a research template as a skill:**
User types: "custom skill — every time I research a new market I follow the same process"
Cowork maps the research steps (search recent news, identify top 3 players, summarize pricing, flag risks), confirms the steps are consistent enough to automate, builds the skill with a 5-step instruction set, and runs a first test on a real market the user is currently investigating.

## Troubleshooting

**Issue: The skill runs but skips steps or executes them in the wrong order.**
Solution: Rewrite the instructions with explicit sequencing cues. Add "First," "Then," and "Finally," to the step text, or number them explicitly. If a step depends on the output of the previous step, say so directly: "Using the summary from the previous step, write a 3-sentence recommendation."

**Issue: User can't find the skill after building it — can't remember the trigger phrase.**
Solution: Go to Settings > Skills to see the full list and the trigger phrases for each. Suggest the user keep a cheat sheet file — `cowork-customizations/my-skills.md` — with each skill name, its trigger phrases, and what it does. Over time this becomes a personal skill library reference.

**Issue: The skill works for the user who built it but is too specific for anyone else on the team to use.**
Solution: This is by design for personal skills. If the goal is a team-shared skill, revisit Step 3 and generalize any hard-coded details (names, specific file paths, personal terminology) into placeholders the user fills in at trigger time — e.g., "[client name]" instead of "Acme Corp".

## Related Skills

See also: **workflow-builder** — build and test a workflow manually before packaging it as a skill; the workflow-builder output becomes the input for skill creation.
Related: **skill-customizer** — once a skill is built, use skill-customizer to tune its outputs to your exact voice and industry without rebuilding from scratch.
See also: **cowork-health-check** — creating your first custom skill typically moves the Skills and Automations health check category from a 3 to a 7 in a single session.
