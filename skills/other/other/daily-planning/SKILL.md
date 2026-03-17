---
name: daily-planning
description: Plan a day's priorities, meetings, and intentions. Accepts an optional target date (default: today). Use with date arguments like "tomorrow", "Monday", "2026-02-12", or "next Tuesday". Reads current Today.md as context for prior work.
argument-hint: "[target-date: today|tomorrow|monday|YYYY-MM-DD]"
metadata:
  orchestrated: true
  phases_file: phases.yaml
---

# Daily Planning Ritual

This skill guides you through a planning ritual that helps set intentions, prioritize outcomes, and prepare for a target day. By default it plans for today, but accepts a target date argument to plan ahead (e.g., planning Friday for Monday).

**Orchestration**: This skill uses subagent orchestration. See `phases.yaml` for phase definitions.

---

<!-- phase:setup -->
## Setup Complete

The orchestrator has loaded configuration and context:

- **Vault**: `{{VAULT}}`
- **Target Date**: {{DATES.target_date}} ({{DATES.day_name}})
- **Week**: {{DATES.week}}, **Month**: {{DATES.month}}, **Quarter**: {{DATES.quarter}}
- **Relative**: {{#if DATES.is_today}}Today{{else if DATES.is_future}}{{DATES.days_from_today}} day(s) from now{{else}}In the past{{/if}}

{{#if DIRECTIVES.success}}
**Directives loaded** for {{DIRECTIVES.user.preferred_name}}.
Apply throughout this ritual:
- Use `{{DIRECTIVES.user.preferred_name}}` in greetings and prompts
- Reference `{{DIRECTIVES.user.leadership_identity}}` when suggesting leadership intentions
- Use growth edge and patterns_to_watch when generating coaching prompts
- Adapt communication style based on formality={{DIRECTIVES.ai.formality}}, directness={{DIRECTIVES.ai.directness}}
{{else}}
**No directives found.** Using default communication style.
Suggest running `/init` at the end.
{{/if}}
<!-- /phase:setup -->

---

<!-- phase:gather -->
## Context Gathered

### Calendar for {{DATES.target_date}} ({{DATES.day_name}})

{{#if CALENDAR.events}}
Found {{CALENDAR.events.length}} meetings:

{{#each CALENDAR.events}}
- **{{this.start_time}}-{{this.end_time}}**: {{this.title}} {{#if this.is_one_on_one}}→ [[{{this.other_person}}]] template{{else}}→ [Meeting] template{{/if}}
{{/each}}

**Focus hours available**: ~{{CALENDAR.summary.focus_hours}}h
{{else}}
No calendar data available. Meetings can be added manually.
{{/if}}

### Prior Work Context

Read from `{{VAULT}}/00_Brain/Captive/Today.md` for:
- Completed items and recent wins
- Unfinished priorities that may carry forward
- Actions that need follow-up

### Additional Context Sources

Scan these locations for context:
- Recent `{{VAULT}}/00_Brain/Periodic/Daily/` files
- `{{VAULT}}/00_Brain/Captive/Week.md` for weekly context
- `{{VAULT}}/01_Projects/` for active projects
- `{{VAULT}}/02_Areas/Insights/` and `People/` for themes
- `{{VAULT}}/00_Brain/Captive/Year.md` and `Quarter.md` for coaching context
<!-- /phase:gather -->

---

<!-- phase:preflight:inline -->
## Pre-flight Check

Before planning, handle the current Today.md appropriately:

1. Get **today's actual date** using `date +"%Y-%m-%d"` (current calendar date)
2. Compare to **target date**: {{DATES.target_date}}
3. Read `{{VAULT}}/00_Brain/Captive/Today.md` and extract the `date` from frontmatter (if it exists)

**If target date is TODAY:**
   a. If Today.md date matches today → note was already created, ask user if they want to regenerate
   b. If Today.md date is older:
      - Check if archive exists at `{{VAULT}}/00_Brain/Periodic/Daily/{Today.md date}.md`
      - If archive exists and content matches → already digested, proceed
      - If archive exists but content differs → **STOP**: "The note from {date} has changes that aren't archived yet. Please run daily-review first, or confirm you want to discard those changes."
      - If no archive exists → **STOP**: "The note from {date} hasn't been digested yet. Please run daily-review first, or confirm you want to skip archiving."
      - Only proceed if user explicitly confirms to skip/discard

**If target date is FUTURE (tomorrow, Monday, specific future date):**
   a. Read Today.md content as **context source** (work completed before target date)
   b. Check if target date already has an archive at `{{VAULT}}/00_Brain/Periodic/Daily/{target-date}.md`:
      - If archive exists → Ask: "A plan for {target-date} already exists in the archive. Do you want to regenerate it?"
   c. Warn user: "Planning for {target-date} will overwrite Today.md. The current Today.md ({Today.md date}) content will be used as context. Make sure yesterday's work is archived if needed."
   d. Proceed only if user confirms
<!-- /phase:preflight -->

---

<!-- phase:interact:inline -->
## Interactive Planning Session

Engage the user to plan for **{{DATES.target_date}} ({{DATES.day_name}})**:

### 1. Present Calendar Overview

- Show: "I found X meetings on your calendar for **{{DATES.target_date}} ({{DATES.day_name}})**:"
- List by time with detected template:
  - "09:30-10:00: 1:1 Simone/Michi → [[Simone]] template"
  - "13:00-13:55: CE Leadership Weekly → [Meeting] template"
- For uncertain matches, note: "(needs confirmation)"
- Note filtered events: "Filtered out X events (OOO notices, blockers, lunch)"
- Ask: "Does this look right? Any template assignments to change?"

### 2. Contextual Questions

- "What's your expected energy level **on {{DATES.day_name}}**?" (High/Medium/Low)
- "Where will you be working **on {{DATES.target_date}}**?" (Office/Home/Travel/Other)
- "Are there any deadlines, events, or constraints **on {{DATES.target_date}}**?"
- For [[PersonName]] meetings: "What do you want to focus on with [PersonName]?"

### 3. Priority Discussion

- Review prior work and progress from Today.md context
- Discuss active projects and areas that need attention
- Help user identify the **top 3 outcomes** for the target date:
  - Priority 1: Most critical outcome that must happen
  - Priority 2: Team/strategic work
  - Priority 3: Personal/operational task
- Frame priorities as **outcomes**, not just tasks (what will be different by end of the target day?)

### 4. Leadership Intention (Context-Aware)

Based on gathered context for the target date, suggest 2-3 relevant intentions with reasoning:

- Heavy meeting day (4+ meetings) → "Present", "Listening", "Patient"
- Many [[PersonName]] meetings scheduled → "Supportive", "Coaching", "Curious"
- Big deadline or presentation → "Decisive", "Confident", "Clear"
- Low energy reported → "Sustainable", "Boundaries", "Selective"
- High energy + light calendar → "Creative", "Ambitious", "Momentum"
- Yesterday had unfinished priorities → "Focused", "Finishing", "Discipline"
- Conflict or difficult conversations pending → "Calm", "Direct", "Empathetic"

Present suggestions with brief reasoning, then let user choose or provide their own.

### 5. Generate Coaching Prompts (Context-Aware)

Based on gathered context (goals, day type, priorities), generate personalized prompts for the Wins and Insights sections. Act as an experienced executive coach developing the user according to their stated leadership and unit goals.

**Determine day type for target date:**
- Heavy meeting day (4+ meetings): Focus on presence, listening, energy protection
- 1:1 heavy day (2+ 1:1s): Focus on coaching vs. solving, feedback, development
- Deadline/delivery day: Focus on delivery, recognition, sustainable effort
- Low energy day: Focus on boundaries, sustainability, delegation
- Strategic/light calendar day: Focus on clarity, long-term thinking, creative work

**Generate Wins prompts** (2-3 total across Personal, Team, Project Progress):

Connect to:
- Target date priorities → "If you complete [Priority 1], what will that prove about your capability?"
- Leadership intention → "How will you know if you successfully embodied '[intention]' on {{DATES.target_date}}?"
- 1:1 meetings → "What opportunity does your 1:1 with [Person] give you to practice [leadership focus]?"
- Growth edge → "Where might '[growth edge]' show up today? What's your plan?"
- Unit goals → "What progress today connects to [Key Outcome]?"

**Generate Insights prompts** (2-3 total across What Went Well, What Could Be Better, Key Insight):

Connect to:
- Patterns to watch → "Did you notice '[pattern]' on {{DATES.target_date}}? What triggered it?"
- Leadership development → "Where did you practice '[leadership focus]' on {{DATES.target_date}}? What worked?"
- Questions that serve me → Select 1 relevant question for Key Insight of the Day
- Day type context:
  - Heavy meeting day: "Which meeting energized vs. drained you? Why?"
  - 1:1 day: "What question unlocked something for someone today?"
  - Deadline day: "What was the hidden cost of today's push? Worth it?"

**Prompt generation rules:**
- Maximum 2-3 prompts per section
- Each prompt should be specific to the target date's context, not generic
- Connect prompts to stated goals when available
- Frame Wins as celebration/recognition; Insights as learning/pattern-recognition
- If goals are empty, use thoughtful generic prompts and suggest filling in Year.md/Quarter.md
<!-- /phase:interact -->

---

<!-- phase:generate:inline -->
## Generate Daily Plan

Read `{{VAULT}}/00_Brain/Systemic/Templates/Captive/today.md` as the single source of truth for structure.

### 1. Fill Frontmatter

Using the template's frontmatter keys:
- Copy the exact keys from the template (date, day, week, month, quarter, energy, location, focus_hours, meetings)
- Fill values using the **target date** ({{DATES.target_date}}), not today's date

### 2. Fill Focus Section

- Replace priority prompts with user's actual priorities
- Replace Leadership Intention placeholder with user's chosen intention

### 3. Fill Meetings Section

From calendar events:
- Parse all meeting templates from the template's `## Meetings` section
- Each `### ...` heading defines a template type
- Sort events by start time
- For each meeting, use the template assigned during calendar overview
- Replace placeholder values with actual event data

**Template discovery:**
Read `{{VAULT}}/00_Brain/Systemic/Templates/Captive/today.md` and parse the `## Meetings` section.
For each `### ...` heading found, extract:
- The heading pattern (e.g., `[Meeting Name/Topic]`, `[[PersonName]]`)
- The template content (everything until next `###` or `---`)

**Match each calendar event to best template:**
- `### [[PersonName]]` pattern: Events that appear to be 1:1 conversations
- `### [Meeting Name/Topic]` pattern: Group meetings, syncs, reviews, etc.
- For `[[PersonName]]` templates, extract the other person's name using `user_name` from calendars.json

### 4. Fill Wins Section

With generated coaching prompts:
- Keep the section structure from template (Personal, Team, Project Progress)
- Replace generic prompts with the context-aware prompts generated in Phase 3
- Personal: 1-2 prompts connecting to leadership intention and growth edge
- Team: 1 prompt connecting to 1:1s or team development
- Project Progress: Keep the [[project-name]] placeholder format for user to fill

### 5. Fill Insights Section

With generated coaching prompts:
- Keep the section structure from template (What Went Well, What Could Be Better, Key Insight)
- What Went Well: 1-2 prompts about patterns, energy, or leadership practice
- What Could Be Better: 1-2 prompts connecting to patterns to watch or growth edge
- Key Insight of the Day: Use one question from "Questions That Serve Me" or a powerful coaching question

### 6. Keep Remaining Sections

- **Capture section**: Keep as-is from template (user fills during day)

Store the complete generated content as `{{PLAN}}` for the write phase.
<!-- /phase:generate -->

---

<!-- phase:write -->
## Write and Confirm

The orchestrator writes the plan via subagent:
- Path: `{{VAULT}}/00_Brain/Captive/Today.md`
- Content: `{{PLAN}}`

### Confirm with User

After successful write:
- Show the target date: "Plan created for **{{DATES.target_date}} ({{DATES.day_name}})**"
- Summarize the 3 priorities
- Highlight the leadership intention
- Note any meetings prepared

### Optional Suggestions

- Time blocking specific focus hours
- When to tackle highest-priority items
- Breaks or energy management strategies

{{#unless DIRECTIVES.success}}
**Tip**: Run `/init` to personalize your planning experience with leadership context and coaching prompts.
{{/unless}}
<!-- /phase:write -->

---

## Tips for Effective Planning

- **Outcomes over tasks**: Frame priorities as what will be accomplished, not just activities
- **Realistic priorities**: Three well-chosen priorities are better than an overwhelming list
- **Plan ahead**: Use target dates to plan Friday for Monday, skip holidays, or prepare for important days
- **Review prior work**: Learn from what worked and what didn't from recent work
- **Intentionality**: The leadership intention helps maintain focus on how you work, not just what you work on

## Integration with Other Skills

- **daily-review**: Evening counterpart that reflects on the day, fills Completed/Wins/Insights, and archives to Periodic/Daily/
- **weekly-planning**: Higher-level planning that daily-planning aligns with
- **weekly-review**: Review that synthesizes the week and archives to Periodic/Weekly/
- **create-project**: Action to create new project files that show up in context gathering
