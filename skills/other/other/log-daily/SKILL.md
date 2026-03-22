---
name: log-daily
description: Log conversation activity to today's daily note on demand. Use when wrapping up work, capturing decisions, or documenting session outcomes.
---

<daily_note_location>
**Default Path:** "~/Documents/obsidian_vault/vault/publish/7 - Daily Notes/{YYYY}/{MM}/{DD}.md"
If not exists create a note for today
</daily_note_location>


<objective>
Append a structured summary of current session activity to today's daily note. This creates the data layer that vault-analyst reads to discover your work patterns.
</objective>

<when_to_use>
- End of a work session (before closing Claude)
- After completing a significant piece of work
- When important decisions were made that should be recorded
- When the user explicitly requests logging
- Mid-session when switching contexts

**NOT needed when:**
- Just chatting without meaningful work output
- Quick questions with no decisions or outcomes
</when_to_use>

<log_format>
```markdown
---

## Session Log - [TIME]

**Focus:** [1-2 sentence summary of main work]

### Completed
- [Concrete outcome 1]
- [Concrete outcome 2]

### Decisions Made
- [Decision]: [Why]

### Next Steps
- [ ] [Follow-up task if any]

---
```
</log_format>

<quality_guidelines>
**Good entries:**
- "Created YouTube analytics inbox item with 3 integration options"
- "Refactored authentication to use JWT instead of sessions"
- "Decision: Use Postgres over SQLite (need concurrent writes)"

**Bad entries:**
- "Worked on stuff"
- "Had a conversation about the project"
- "Did some research"

**Be specific.** Capture what was DONE, not what was discussed.

**Why this matters:** Vault-analyst reads these logs to find patterns. Vague entries = weak pattern detection. Specific entries = actionable automation recommendations.
</quality_guidelines>

<example_output>
---

# Local LLM integration for cost optimization

### Completed
- Overhauled inbox-processor with local_classify integration
- Created keep-warm launchd agent for Ollama (4-min interval)
- Tested classification accuracy on inbox items (~66%)

### Decisions Made
- Hybrid local/cloud pattern: Local does mechanical work, Claude does judgment
- 4-minute keep-warm interval: Prevents cold start without wasting resources

### Next Steps
- [ ] Monitor token savings over next week
- [ ] Apply pattern to slop-detector skill

---
</example_output>
