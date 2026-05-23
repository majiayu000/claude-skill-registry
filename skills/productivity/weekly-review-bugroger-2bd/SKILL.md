---
name: weekly-review
description: Review and archive a week's work. Synthesizes daily archives into weekly patterns, guides reflection on leadership and themes, extracts insights to semantic notes (People, Projects, Insights), and archives to Periodic/Weekly/. Accepts an optional target week (default: current week).
argument-hint: "[target-week: (empty)|last week|YYYY-Www]"
metadata:
  orchestrated: true
  phases_file: phases.yaml
---

# Weekly Review Ritual

This skill guides you through a weekly review ritual that synthesizes the week's work, reflects on leadership intentions and patterns, extracts learnings to semantic notes, and archives to Periodic/Weekly/.

**Orchestration**: This skill uses subagent orchestration. See `phases.yaml` for phase definitions.

---

<!-- phase:setup -->
## Setup Complete

The orchestrator has loaded configuration and context:

- **Vault**: `{{VAULT}}`
- **Target Week**: {{DATES.week}} ({{DATES.week_start}} to {{DATES.week_end}})
- **Month**: {{DATES.month}}, **Quarter**: {{DATES.quarter}}, **Year**: {{DATES.year}}

{{#if DIRECTIVES.success}}
**Directives loaded** for {{DIRECTIVES.user.preferred_name}}.
Apply throughout this ritual:
- Use `{{DIRECTIVES.user.preferred_name}}` in prompts
- Reference `{{DIRECTIVES.user.leadership_identity}}` when reflecting on leadership
- Use `{{DIRECTIVES.user.growth_edge}}` when exploring development
- Apply `{{DIRECTIVES.user.patterns_to_watch}}` when identifying weekly patterns
- Connect to `{{DIRECTIVES.user.key_goals}}` when recognizing progress
- Adapt style based on formality={{DIRECTIVES.ai.formality}}, directness={{DIRECTIVES.ai.directness}}
{{else}}
**No directives found.** Using default communication style.
Suggest running `/init` at the end.
{{/if}}
<!-- /phase:setup -->

---

<!-- phase:load -->
## Week Content Loaded

**Week.md content for {{DATES.week}}:**

**Frontmatter:**
- Week: {{WEEK_CONTENT.frontmatter.week}}
- Dates: {{WEEK_CONTENT.frontmatter.dates}}
- Month: {{WEEK_CONTENT.frontmatter.month}}
- Quarter: {{WEEK_CONTENT.frontmatter.quarter}}

**Focus Theme:** {{WEEK_CONTENT.sections.focus_theme}}

**Key Outcomes:**
{{#each WEEK_CONTENT.sections.key_outcomes}}
- {{this}}
{{/each}}

**Completeness:**
- Wins filled: {{WEEK_CONTENT.completeness.wins_filled}}
- Reflections filled: {{WEEK_CONTENT.completeness.reflections_filled}}
- Coaching check-in filled: {{WEEK_CONTENT.completeness.coaching_filled}}
- Daily notes: {{WEEK_CONTENT.completeness.daily_notes_count}}/5 days
<!-- /phase:load -->

---

<!-- phase:gather -->
## Daily Archives Gathered

**Daily archives for {{DATES.week}}:**

{{#if WEEK_CONTEXT.daily_archives}}
{{#each WEEK_CONTEXT.daily_archives}}
### {{this.day_name}} ({{this.date}})
- Energy: {{this.energy}}
- Meetings: {{this.meeting_count}}
- Focus Hours: {{this.focus_hours}}
- Priority completion: {{this.priority_completion}}
- Wins: {{this.wins_count}}
- Key insight: "{{this.key_insight}}"
{{/each}}

**Week Aggregates:**
- Total meetings: {{WEEK_CONTEXT.aggregates.total_meetings}}
- Total focus hours: {{WEEK_CONTEXT.aggregates.total_focus_hours}}h
- Average energy: {{WEEK_CONTEXT.aggregates.avg_energy}}
- Energy trend: {{WEEK_CONTEXT.aggregates.energy_trend}}
- Priority completion rate: {{WEEK_CONTEXT.aggregates.priority_completion_rate}}%
- People interacted with: {{WEEK_CONTEXT.aggregates.unique_people}}
- Projects touched: {{WEEK_CONTEXT.aggregates.unique_projects}}
{{else}}
**No daily archives found for this week.**
{{/if}}

{{#if WEEK_CONTEXT.missing_days}}
**Missing days:** {{WEEK_CONTEXT.missing_days}}
{{/if}}
<!-- /phase:gather -->

---

<!-- phase:preflight:inline -->
## Pre-flight Check

Before reviewing, verify the week state:

### 1. Week Verification

- Week.md frontmatter week: `{{WEEK_CONTENT.frontmatter.week}}`
- Target review week: `{{DATES.week}}`

If weeks don't match:
- "The Week.md file is for **{{WEEK_CONTENT.frontmatter.week}}**, but you're reviewing **{{DATES.week}}**."
- Ask: "Should I review the existing Week.md week instead?"

### 2. Archive Check

Check if archive exists at `{{VAULT}}/00_Brain/Periodic/Weekly/{{DATES.week}}.md`:
- If exists: "This week has already been archived. Would you like to view the archive, or re-review and update it?"

### 3. Daily Archive Completeness

Check which workdays (Mon-Fri) have daily archives:

{{#if WEEK_CONTEXT.missing_days}}
**Missing daily archives:** {{WEEK_CONTEXT.missing_days}}

"Some daily reviews are missing. The weekly review will proceed with partial data."

Ask: "Would you like to:
1. Proceed with available data ({{WEEK_CONTEXT.daily_archives.length}} of 5 days)
2. Run `/daily-review` for missing days first
3. Cancel and complete daily reviews"
{{else}}
**All workdays archived.** Ready to proceed.
{{/if}}

### 4. Archived Marker Check

If Week.md contains `archived:` in frontmatter:
- "This week appears to already be archived. Check `Periodic/Weekly/{{WEEK_CONTENT.frontmatter.archived}}.md`"
- Ask: "Would you like to view the existing archive?"

Proceed only when state is validated.
<!-- /phase:preflight -->

---

<!-- phase:interact:inline -->
## Interactive Review Session (7 Parts)

Guide the user through comprehensive weekly reflection for **{{DATES.week}}**:

### Part 1: Week Summary

Present the synthesized week overview:

"Here's your week at a glance for **{{DATES.week}}** ({{DATES.week_start}} to {{DATES.week_end}}):"

- **Days reviewed:** {{WEEK_CONTEXT.daily_archives.length}}/5
- **Total meetings:** {{WEEK_CONTEXT.aggregates.total_meetings}}
- **Total focus hours:** {{WEEK_CONTEXT.aggregates.total_focus_hours}}h
- **Energy trend:** {{WEEK_CONTEXT.aggregates.energy_trend}} ({{WEEK_CONTEXT.aggregates.avg_energy}} avg)
- **Priority completion rate:** {{WEEK_CONTEXT.aggregates.priority_completion_rate}}%

Ask: "Does this feel accurate to how your week went?"

### Part 2: Leadership Intention Reflection

"Let's reflect on how you showed up as a leader this week."

For each day with a leadership intention from {{WEEK_CONTEXT.aggregates.leadership_intentions}}:
- "On {{day}}, you set out to be '{{intention}}'"
- "Looking back, how well did you embody that intention? (1-10)"

Then synthesize:
- "Across the week, which intention served you best?"
- "Where did you struggle to maintain your intended stance?"
- "What pattern do you notice about when you're at your best?"

### Part 3: Synthesize Wins

"Let's identify the wins that defined this week."

Review wins across all daily archives, grouped by category:

**Personal Wins:**
{{#each WEEK_CONTEXT.wins.personal}}
- {{this.date}}: {{this.content}}
{{/each}}

Ask: "Which personal win are you most proud of? Why does it matter?"

**Organisational Wins:**
{{#each WEEK_CONTEXT.wins.organisational}}
- {{this.date}}: {{this.content}}
{{/each}}

Ask: "What team success stands out? Who deserves recognition?"

**Strategic Wins:**
{{#each WEEK_CONTEXT.wins.strategic}}
- {{this.date}}: {{this.content}}
{{/each}}

Ask: "What project progress moved the needle most?"

**Theme Identification:**
"Looking at all these wins together, what's the THEME of this week?"
- Suggest 2-3 potential themes based on pattern analysis
- Let user confirm or provide their own

### Part 4: Synthesize Insights

"Let's crystallize the learnings from this week."

Review all Key Insights from daily archives:
{{#each WEEK_CONTEXT.insights}}
- {{this.date}}: "{{this.key_insight}}"
{{/each}}

Ask: "Which insight feels most important to carry forward?"

Review What Went Well patterns from {{WEEK_CONTEXT.what_went_well}}:
- "I noticed these recurring patterns in what energized you..."
- "How can you do more of this next week?"

Review What Could Be Better patterns from {{WEEK_CONTEXT.what_could_be_better}}:
- "These friction points appeared multiple times..."
- "What's one change that would address the biggest friction?"

### Part 5: People Synthesis

"Let's review your key relationships this week."

List all 1:1 meetings and significant interactions from {{WEEK_CONTEXT.people_interactions}}:

{{#each WEEK_CONTEXT.people_interactions}}
**{{this.person}}**: {{this.interaction_count}} interactions
- Dates: {{this.dates}}
- Topics: {{this.topics}}
- Notable: {{this.notable_moment}}
{{/each}}

Ask for each significant person:
- "What's your key takeaway from your interactions with {{person}}?"
- "Is there follow-up needed?"

Prepare People file updates for confirmation phase.

### Part 6: Coaching Moment

Connect to growth edge and patterns:

"Let's check in on your development:"

**Growth Edge Check:**
{{#if DIRECTIVES.user.growth_edge}}
- "Your growth edge is: '{{DIRECTIVES.user.growth_edge}}'"
- "Where did this show up this week?"
- "What progress did you make?"
{{/if}}

**Patterns to Watch:**
{{#if DIRECTIVES.user.patterns_to_watch}}
- "You're watching for: {{DIRECTIVES.user.patterns_to_watch}}"
- "Did any of these patterns emerge this week?"
- "What triggered them?"
{{/if}}

**Self-Care Check:**
- "How's your energy as the week closes?"
- "What boundaries served you well?"
- "What do you need to protect next week?"

### Part 7: Forward Synthesis

"Let's prepare for next week:"

**Carry Forward:**
Review all Carry Forward items from daily archives and Week.md:
- Items from {{WEEK_CONTEXT.carry_forward}}
- Items from {{WEEK_CONTENT.sections.carry_forward}}

Ask: "Which are still relevant? Which can be dropped?"

**Incomplete Decisions:**
- "Were there decisions discussed but not finalized this week?"
- Ask: "Any that need to be resolved?"

**Next Week Setup:**
- "Based on this week, what's your focus theme for next week?"
- "What one thing would make next week successful?"

Store synthesis in WEEK_SYNTHESIS for later phases.
<!-- /phase:interact -->

---

<!-- phase:synthesize -->
## Semantic Synthesis

Launch subagent to prepare semantic note updates based on the week's content and interactions:

Using extract-to-areas sub-skill with:
- Scope: week
- People: {{WEEK_CONTEXT.aggregates.unique_people}}
- Projects: {{WEEK_CONTEXT.aggregates.unique_projects}}
- Insights: Key learnings from WEEK_SYNTHESIS

Each entity type returns structured updates for user approval.
<!-- /phase:synthesize -->

---

<!-- phase:confirm:inline -->
## Confirm Updates

Present all proposed changes for user approval:

### Archive Summary

"Ready to archive **{{DATES.week}}** to `Periodic/Weekly/{{DATES.week}}.md`"

**Week Summary:**
- Days archived: {{WEEK_CONTEXT.daily_archives.length}}/5
- Week Theme: "{{WEEK_SYNTHESIS.theme}}"
- Leadership Reflection: Reviewed {{WEEK_CONTEXT.aggregates.leadership_intentions.length}} daily intentions
- Top Win: "{{WEEK_SYNTHESIS.top_win}}"
- Key Insight: "{{WEEK_SYNTHESIS.key_insight}}"

### Semantic Updates

"The following semantic notes will be updated:"

{{#if SEMANTIC_UPDATES.updates}}
{{#each SEMANTIC_UPDATES.updates}}
- **{{this.type}}**: [[{{this.path}}]] → "{{this.content}}" (section: {{this.section}})
{{/each}}
{{else}}
No semantic updates to apply.
{{/if}}

{{#if SEMANTIC_UPDATES.new_insights}}
**New Insight Suggestions:**
{{#each SEMANTIC_UPDATES.new_insights}}
- Create: {{this.suggested_name}} — "{{this.content}}"
{{/each}}
{{/if}}

Ask: "Proceed with archive and semantic updates?"
- Options: Yes, all / Archive only, skip semantic / Review each update / Cancel

### Handle Confirmations

- If "Yes, all" → proceed to write phase
- If "Archive only" → set flag to skip semantic updates
- If "Review each" → present each update individually for approval
- If "Cancel" → exit with summary of captured synthesis (not lost)
<!-- /phase:confirm -->

---

<!-- phase:write -->
## Archive and Update

The orchestrator executes writes via subagents:

### 1. Archive Weekly
- Read template from `{{VAULT}}/00_Brain/Systemic/Templates/Periodic/weekly.md`
- Transform Week.md content to archive format
- Include daily archive links from {{WEEK_CONTEXT.daily_links}}
- Include synthesis from interactive session
- Write to `{{VAULT}}/00_Brain/Periodic/Weekly/{{DATES.week}}.md`
- Update Week.md with archived placeholder

### 2. Update Semantic Notes
- Apply confirmed updates via `update-semantic` subagent
- Log each update: "[type] [[path]] updated with [section] entry"

### Completion Message

After successful write:
- "Week archived to `Periodic/Weekly/{{DATES.week}}.md`"
- Show semantic notes updated: "[count] notes updated"
- Link to archive: `[[00_Brain/Periodic/Weekly/{{DATES.week}}]]`

### Suggest Next Steps

- "Ready for next week? Run `/weekly-planning` when you're ready."
- If end of month approaching: "Consider running `/monthly-review` soon."
- If patterns emerged: "Consider updating `Month.md` or `Quarter.md` with this week's themes."

{{#unless DIRECTIVES.success}}
**Tip**: Run `/init` to personalize your review experience with coaching context.
{{/unless}}
<!-- /phase:write -->

---

## Tips for Effective Weekly Review

- **Patterns over incidents**: Look for recurring themes across days
- **Theme clarity**: One clear theme is better than five vague ones
- **People matter**: Take time to reflect on key relationships
- **Synthesis compounds**: Weekly insights build on daily learnings
- **Forward focus**: Use the review to set up next week's success

## Metabolic Flow

This ritual moves content through the knowledge metabolism:

```
Captive (volatile)     →    Periodic (archive)      →    Semantic (crystallized)
Week.md + Daily/*.md        Weekly/YYYY-Www.md          People/, Projects/,
                                                        Insights/
```

## Integration with Other Skills

- **daily-review**: Creates the daily archives that weekly-review synthesizes
- **weekly-planning**: Morning counterpart that creates Week.md
- **monthly-review**: Higher-level synthesis that uses weekly archives
- **get-week-content**: Sub-skill that parses Week.md structure
- **gather-week-context**: Sub-skill that collects daily archives
- **extract-to-areas**: Sub-skill that prepares semantic updates
- **archive-weekly**: Sub-skill that handles Captive → Periodic transition
