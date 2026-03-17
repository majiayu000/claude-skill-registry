---
context: fork
---

# /weekly-summary

Generate comprehensive weekly summary from daily notes, meetings, tasks, and project updates using parallel sub-agents.

## Usage

```
/weekly-summary
/weekly-summary --last-week
/weekly-summary --from 2026-01-01 --to 2026-01-07
/weekly-summary --output page    # Create Page note instead of just outputting
```

## Instructions

This skill uses **5 parallel sub-agents** to gather data concurrently from different vault areas, then synthesizes a comprehensive weekly report.

### Phase 1: Launch Parallel Data Collectors

Create **5 Task agents** running in parallel (use `model: "haiku"` for speed):

**Agent 1: Daily Notes Collector** (Haiku)
```
Task: Extract key activities from daily notes
- Determine date range (default: last 7 days, or from user's --from/--to flags)
- Use Glob to find +Daily/YYYY/YYYY-MM-DD.md files in range
- For each daily note:
  - Read content
  - Extract "Wins" or achievements section
  - Extract "Challenges" or blockers section
  - Extract "Notes" or key decisions
  - Extract task completions (lines with [x])
  - Note significant activities or meetings mentioned
- Return: Structured data with date, wins, challenges, decisions, completed tasks
```

**Agent 2: Tasks Analyzer** (Haiku)
```
Task: Analyze task completions and changes
- Use Glob to find all "Task - *.md" files
- Filter to tasks modified in date range (check frontmatter.modified)
- Categorize:
  - Completed this week (completed: true, modified in range)
  - New tasks created (created in range)
  - Still in progress (high priority, not completed)
  - Blocked tasks (status issues mentioned)
- For each category, extract: title, priority, project, due date
- Return: Task statistics and key task movements
```

**Agent 3: Meetings Collector** (Haiku)
```
Task: Gather meeting summaries from this week
- Use Glob to find all "+Meetings/Meeting - *.md" files
- Filter to meetings with date in range (frontmatter.date)
- For each meeting:
  - Extract title, date, attendees, project
  - Extract summary or key decisions from frontmatter or first section
  - Note action items (lines starting with "- [ ]" or "TODO")
  - Extract important discussion points
- Group by project if possible
- Return: Chronological list of meetings with key points
```

**Agent 4: ADR Tracker** (Haiku)
```
Task: Track architecture decisions this week
- Use Glob to find all "ADR - *.md" files
- Filter to ADRs modified or created in date range
- For each ADR:
  - Extract title, status (proposed/accepted/deprecated)
  - Note status changes (proposed → accepted)
  - Extract decision and rationale summary
  - Note impacted projects or systems
- Return: New ADRs, status changes, key decisions
```

**Agent 5: Project Progress Tracker** (Haiku)
```
Task: Analyze project progress this week
- Use Glob to find all "Project - *.md" files
- Filter to projects with status: active
- For each active project:
  - Check if modified in date range
  - Extract status, priority, recent updates
  - Count related tasks completed this week
  - Note any status changes (paused, completed)
  - Extract milestones mentioned
- Return: Project progress summary with task completions
```

### Phase 2: Wait for All Agents

Use TaskOutput with blocking to wait for all 5 agents to complete. Collect their outputs.

### Phase 3: Synthesize Weekly Summary

Combine all agent data into cohesive weekly summary:

```markdown
# Weekly Summary: {{Start Date}} - {{End Date}}

Generated: {{TIMESTAMP}}

## 📊 Week at a Glance

**Highlights:**
- {{Top 3 achievements from daily notes}}
- {{Major decisions or milestones}}
- {{Significant meetings or collaborations}}

**Statistics:**
- **Tasks Completed:** {{count}} ({{high priority count}} high priority)
- **New Tasks Created:** {{count}}
- **Meetings:** {{count}} ({{total hours if available}})
- **ADRs:** {{new count}} new, {{status change count}} updated
- **Active Projects:** {{count}} ({{tasks completed across projects}})

---

## ✅ Completed Tasks ({{count}})

### High Priority ({{count}})
- [x] [[Task - {{title}}]] ({{project}}) - {{due date}}
- [x] [[Task - {{title}}]] ({{project}})

### Medium Priority ({{count}})
{{list}}

### Low Priority ({{count}})
{{list if > 5, else "All completed"}}

---

## 🚀 Project Progress

### [[Project Name]] ({{status}})
**Tasks Completed:** {{count}}/{{total}}
**Key Updates:**
- {{update from project note or meetings}}
- {{completed task summaries}}

**Next Steps:**
- {{open high priority tasks}}
- {{upcoming milestones}}

---

### [[Another Project]] ({{status}})
{{same format}}

---

## 🏛️ Architecture Decisions

### New ADRs ({{count}})
- **[[ADR - {{title}}]]** ({{status}})
  - **Decision:** {{one-line summary}}
  - **Rationale:** {{brief reason}}
  - **Impact:** {{projects or systems affected}}

### Status Changes ({{count}})
- **[[ADR - {{title}}]]**: Proposed → Accepted
  - {{context for change}}

---

## 📅 Meetings This Week ({{count}})

### Monday, {{DATE}}
- **[[Meeting - {{title}}]]** ({{project}})
  - Attendees: {{list}}
  - **Key Points:** {{summary}}
  - **Action Items:** {{count}} ({{assigned tasks}})

### Wednesday, {{DATE}}
{{same format}}

---

## 💡 Daily Highlights

### {{Monday DATE}}
**Wins:**
- {{from daily note}}

**Challenges:**
- {{from daily note}}

### {{Tuesday DATE}}
{{same format}}

---

## 🎯 Focus for Next Week

**Priorities:**
1. {{High priority open tasks}}
2. {{Upcoming project milestones}}
3. {{Pending ADR decisions}}
4. {{Follow-ups from meetings}}

**Blocked Items:**
- {{Tasks or projects marked blocked}}
- {{Challenges noted in daily notes}}

**Upcoming:**
- {{Due dates next week}}
- {{Scheduled meetings}}
- {{Project deadlines}}

---

## 📈 Trends & Insights

**Productivity:**
- Task completion rate: {{completed}}/{{total new + existing}} ({{%}})
- Average daily task completions: {{avg}}
- Most active project: [[{{project}}]] ({{task count}} tasks)

**Collaboration:**
- People most frequently mentioned: {{top 3}}
- Cross-project connections: {{count meetings involving 2+ projects}}

**Quality:**
- ADRs with quality indicators: {{count}}/{{total}} ({{%}})
- Stale projects updated: {{count}}
- Documentation created: {{new Page notes}}

---

## 🏷️ Tags This Week

Most frequently used tags:
- #{{tag1}} ({{count}} notes)
- #{{tag2}} ({{count}} notes)
- #{{tag3}} ({{count}} notes)

---

## Related Notes

- [[Weekly Summary {{previous week}}]] (last week)
- Active projects: {{list wiki-links}}
- Team members involved: {{list Person wiki-links}}
```

### Phase 4: Output Options

Based on user's `--output` flag:

1. **Console Output (default)**
   - Print the summary to console
   - Offer to save as Page note

2. **Create Page Note**
   - Save as `Page - Weekly Summary YYYY-MM-DD.md`
   - Frontmatter:
     ```yaml
     type: Page
     title: Weekly Summary {{START_DATE}} - {{END_DATE}}
     created: {{TODAY}}
     tags:
       - weekly-summary
       - productivity
       - meta/reporting
     date-range:
       start: {{START_DATE}}
       end: {{END_DATE}}
     ```

3. **Append to Weekly Log**
   - Check if `Page - 2026 Weekly Summaries.md` exists
   - Append this week's summary
   - Add to table of contents

### Phase 5: Follow-up Prompts

After generating summary, offer:

```
✅ Weekly summary generated!

Would you like to:
1. Export to Page note for archiving
2. Review blocked tasks and challenges
3. Generate next week's priorities as Task notes
4. Create meeting follow-up tasks
5. Update project notes with progress
```

## Use Cases

**Weekly Reviews:**
- Personal productivity tracking
- Team status reports
- Manager updates
- Sprint retrospectives

**Time Tracking:**
- Where did time go this week?
- Which projects got attention?
- Meeting time vs. execution time

**Accountability:**
- Track commitment completions
- Identify recurring blockers
- Measure velocity trends

**Historical Record:**
- Archive weekly progress
- Year-end reviews
- Performance self-assessments

## Configuration

### Date Range Detection

```javascript
// Default: Last 7 days
if (args.includes('--last-week')) {
  // Previous Monday - Sunday
  start = previousMonday;
  end = previousSunday;
} else if (args.includes('--from') && args.includes('--to')) {
  // Custom range
  start = parseDate(args['--from']);
  end = parseDate(args['--to']);
} else {
  // Last 7 days from today
  start = today - 7;
  end = today;
}
```

### Customization

Users can customize by editing `.claude/skills/weekly-summary/SKILL.md`:
- Adjust date range defaults
- Add/remove sections
- Change prioritization logic
- Modify output format
- Add custom metrics

## Performance

- **5 parallel agents** = 5x faster than sequential
- **~100 notes/week**: 20-40 seconds
- **~500 notes/week**: 1-2 minutes
- Uses Haiku for speed (Sonnet alternative for deeper analysis)

## Notes

- Excludes templates and system notes
- Handles missing data gracefully (some weeks may have no ADRs, etc.)
- Chronological ordering within sections
- Links preserved for easy navigation
- Can run for any historical week
- Output is ready to share with teams or managers
