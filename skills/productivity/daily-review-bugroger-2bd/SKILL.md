---
name: daily-review
description: Review and archive a day's work. Guides reflection on wins and insights, synthesizes learnings to semantic notes (People, Projects, Insights, Resources), and archives to Periodic. Accepts an optional target date (default: today).
argument-hint: "[target-date: today|yesterday|YYYY-MM-DD]"
metadata:
  orchestrated: true
  phases_file: phases.yaml
---

# Daily Review Ritual

This skill guides you through an evening review ritual that helps reflect on the day, complete wins and insights sections with personalized coaching, synthesize learnings to semantic notes, and archive the day to Periodic.

**Orchestration**: This skill uses subagent orchestration. See `phases.yaml` for phase definitions.

---

<!-- phase:setup -->
## Setup Complete

The orchestrator has loaded configuration and context:

- **Vault**: `{{VAULT}}`
- **Target Date**: {{DATES.target_date}} ({{DATES.day_name}})
- **Week**: {{DATES.week}}, **Month**: {{DATES.month}}, **Quarter**: {{DATES.quarter}}

{{#if DIRECTIVES.success}}
**Directives loaded** for {{DIRECTIVES.user.preferred_name}}.
Apply throughout this ritual:
- Use `{{DIRECTIVES.user.preferred_name}}` in prompts
- Reference `{{DIRECTIVES.user.leadership_identity}}` when reflecting on leadership
- Use `{{DIRECTIVES.user.growth_edge}}` when exploring development
- Apply `{{DIRECTIVES.user.patterns_to_watch}}` when probing for patterns
- Connect to `{{DIRECTIVES.user.key_goals}}` when recognizing progress
- Adapt style based on formality={{DIRECTIVES.ai.formality}}, directness={{DIRECTIVES.ai.directness}}
{{else}}
**No directives found.** Using default communication style.
Suggest running `/init` at the end.
{{/if}}
<!-- /phase:setup -->

---

<!-- phase:load -->
## Day Loaded

Today.md content for **{{DATES.target_date}} ({{DATES.day_name}})**:

**Frontmatter:**
- Energy: {{TODAY_CONTENT.frontmatter.energy}}
- Location: {{TODAY_CONTENT.frontmatter.location}}
- Focus Hours: {{TODAY_CONTENT.frontmatter.focus_hours}}
- Meetings: {{TODAY_CONTENT.frontmatter.meetings}}

**Priorities:**
{{#each TODAY_CONTENT.sections.priorities}}
- {{this.status}}: {{this.text}}
{{/each}}

**Leadership Intention:** {{TODAY_CONTENT.sections.leadership_intention}}

**Entities Found:**
- People: {{TODAY_CONTENT.entities.people}}
- Projects: {{TODAY_CONTENT.entities.projects}}

**Completeness:**
- Wins filled: {{TODAY_CONTENT.completeness.wins_filled}}
- Insights filled: {{TODAY_CONTENT.completeness.insights_filled}}
<!-- /phase:load -->

---

<!-- phase:preflight:inline -->
## Pre-flight Check

Before reviewing, verify the note state:

### 1. Date Verification

- Today.md frontmatter date: `{{TODAY_CONTENT.frontmatter.date}}`
- Target review date: `{{DATES.target_date}}`

If dates don't match:
- "The Today.md file is dated **{{TODAY_CONTENT.frontmatter.date}}**, but you're reviewing **{{DATES.target_date}}**."
- Ask: "Should I review the existing note ({{TODAY_CONTENT.frontmatter.date}}) instead?"

### 2. Archive Check

Check if archive exists at `{{VAULT}}/00_Brain/Periodic/Daily/{{DATES.target_date}}.md`:
- If exists: "This day has already been archived. Would you like to view the archive, or re-review and update it?"

### 3. Archived Marker Check

If Today.md contains `archived:` in frontmatter:
- "This day appears to already be archived. Check `Periodic/Daily/{{TODAY_CONTENT.frontmatter.archived}}.md`"
- Ask: "Would you like to view the existing archive?"

Proceed only when state is validated.
<!-- /phase:preflight -->

---

<!-- phase:interact:inline -->
## Interactive Review Session

Guide the user through reflection for **{{DATES.target_date}} ({{DATES.day_name}})**:

### 1. Quick Check-in

"How are you feeling as the day wraps up?"
- Note the response for coaching context (compare to morning energy if available)

### 2. Priority Status

Review each priority from the day:

{{#each TODAY_CONTENT.sections.priorities}}
**Priority {{@index}}: {{this.text}}**
- Current status: {{this.status}}
- Ask: "How did this go? Completed / Partial / Deferred?"
- If partial or deferred, capture brief context
{{/each}}

### 3. Dynamic Coached Wins Completion

**Generate contextual coaching questions dynamically based on the actual day.**

No pre-phrased templates. Synthesize:
1. **What actually happened today** — meetings held, priorities addressed, captures made, energy reported
2. **User's development context** — leadership_identity, growth_edge, key_goals from directives
3. **Day type** — heavy meeting day vs. focused work vs. mixed

**Examples of dynamic question generation:**

*If day had 3 1:1s and growth_edge mentions "delegation":*
> "You had three 1:1s today—[names from meetings]. Given you're working on delegation, did any of these conversations create space for you to hand something off?"

*If a priority was marked completed and it connects to key_goals:*
> "You finished [priority]. How does that move you toward [relevant key_goal]?"

*If leadership_intention was "Focused" and calendar was heavy:*
> "You set out to be 'Focused' but had [N] meetings. How did you protect that intention?"

**Guide through each wins category:**
- **Personal**: Connect to energy protection, boundaries, growth_edge progress
- **Organisational**: Connect to team interactions, 1:1 themes, recognition opportunities
- **Strategic**: Connect to project progress, key_goals advancement

### 4. Dynamic Coached Insights Completion

**Generate reflection questions from day content + patterns.**

**Pattern detection:**
- What themes emerge from meetings, priorities, captures?
- Any recurring names, topics, or blockers?

**Cross-reference with patterns_to_watch:**
*If day content shows evidence of a watched pattern:*
> "I noticed you had back-to-back meetings all afternoon—you mentioned watching for overcommitment. How did that land?"

**Energy trajectory:**
*If morning energy was "High" but evening mood is different:*
> "You started the day at high energy but mentioned feeling drained. What shifted?"

**Guide through:**
- **What Went Well**: Pattern or habit that paid off, source of energy
- **What Could Be Better**: Friction points, reactive moments, patterns that emerged
- **Key Insight**: One crystallized learning to carry forward

Connect insights to longer-term development:
> "How does this fit with where you're trying to grow as a {{leadership_identity}}?"
<!-- /phase:interact -->

---

<!-- phase:synthesize:parallel -->
## Parallel Synthesis

Launch parallel subagents to prepare semantic note updates:

### People Updates
For each person in `{{TODAY_CONTENT.entities.people}}`:
- Read their People file at `{{VAULT}}/02_Areas/People/[Name].md`
- Prepare update for Interactions section based on meeting content

### Project Updates
For each project in `{{TODAY_CONTENT.entities.projects}}`:
- Read project file at `{{VAULT}}/01_Projects/[project].md`
- Prepare update for Progress section based on wins and priority completion

### Insight Updates
Based on Key Insight captured:
- Determine if it connects to an existing Insight note
- Prepare update for Evidence section, or flag for new note creation

### Resource Updates
For each capture in `{{TODAY_CONTENT.sections.captures}}`:
- Categorize: link, article, idea, note
- For links/articles: Prepare Resource note creation/update in `03_Resources/`
- For ideas: Route to relevant Project, Area, or Insight

Each subagent returns structured updates for user approval.
<!-- /phase:synthesize -->

---

<!-- phase:confirm:inline -->
## Confirm Updates

Present all proposed changes for user approval:

### Archive Summary

"Ready to archive **{{DATES.target_date}} ({{DATES.day_name}})** to `Periodic/Daily/{{DATES.target_date}}.md`"

**Day Summary:**
- Priorities: X completed, Y partial, Z deferred
- Leadership Intention: {{leadership_intention}} — [reflection summary]
- Wins captured: [count]
- Key Insight: "[insight preview]"

### Semantic Updates

"The following semantic notes will be updated:"

{{#each SEMANTIC_UPDATES.updates}}
- **{{this.type}}**: [[{{this.path}}]] → "{{this.content}}" (section: {{this.section}})
{{/each}}

Ask: "Proceed with archive and semantic updates?"
- Options: Yes, all / Archive only, skip semantic / Review each update / Cancel

### Handle Confirmations

- If "Yes, all" → proceed to write phase
- If "Archive only" → set flag to skip semantic updates
- If "Review each" → present each update individually for approval
- If "Cancel" → exit with summary of captured wins/insights (not lost)
<!-- /phase:confirm -->

---

<!-- phase:write -->
## Archive and Update

The orchestrator executes writes via subagents:

### 1. Archive Daily
- Read template from `{{VAULT}}/00_Brain/Systemic/Templates/Periodic/daily.md`
- Transform Today.md content to archive format
- Write to `{{VAULT}}/00_Brain/Periodic/Daily/{{DATES.target_date}}.md`
- Update Today.md with archived placeholder

### 2. Update Semantic Notes
- Apply confirmed updates via `update-semantic` subagent
- Log each update: "[type] [[path]] updated with [section] entry"

### Completion Message

After successful write:
- "Day archived to `Periodic/Daily/{{DATES.target_date}}.md`"
- Show semantic notes updated: "[count] notes updated"
- Link to archive: `[[00_Brain/Periodic/Daily/{{DATES.target_date}}]]`

### Suggest Next Steps

- "Ready for tomorrow? Run `/daily-planning` when you're ready."
- If patterns emerged: "Consider updating `Quarter.md` with this week's themes."
- If new insight captured: "This insight might deserve its own note in Insights/"

{{#unless DIRECTIVES.success}}
**Tip**: Run `/init` to personalize your review experience with coaching context.
{{/unless}}
<!-- /phase:write -->

---

## Tips for Effective Review

- **Honesty over perfection**: Capture what actually happened, not what you wanted to happen
- **Patterns over incidents**: Look for recurring themes across days
- **Specificity wins**: "Great 1:1 with Sarah about career goals" beats "Good meetings"
- **Synthesis compounds**: Updates to semantic notes build knowledge over time

## Metabolic Flow

This ritual moves content through the knowledge metabolism:

```
Captive (volatile)       →    Periodic (archive)    →    Semantic (crystallized)
Today.md                      Daily/YYYY-MM-DD.md        People/, Projects/,
                                                         Insights/, Resources/
```

## Integration with Other Skills

- **daily-planning**: Morning counterpart that creates Today.md
- **weekly-review**: Synthesizes daily archives into weekly patterns
- **get-today-content**: Sub-skill that parses Today.md structure
- **archive-daily**: Sub-skill that handles Captive → Periodic transition
- **update-semantic**: Sub-skill that appends to semantic notes
