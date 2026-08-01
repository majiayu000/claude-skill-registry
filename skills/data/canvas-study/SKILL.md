---
name: canvas-study
description: Use Canvas LMS data to create personalized, prioritized study plans.
---

---
name: canvas-study-plan
description: Create personalized study plans from Canvas data. Use for: (1) "Help me plan my week" or similar study requests, (2) Prioritizing assignments by deadline and grade impact, (3) Analyzing course grades and identifying attention areas, (4) Generating weekly schedules. Requires canvas_get_upcoming, canvas_get_grades, and canvas_list_announcements tools.
---

# Canvas Study Strategy

Use Canvas LMS data to create personalized, prioritized study plans.

## Workflow

1. **Gather Data**
   - `canvas_get_upcoming` - All assignments across courses
   - `canvas_get_grades` - Current standing in each course
   - `canvas_list_announcements` - Important course updates

2. **Analyze & Prioritize**
   - Rank by: deadline proximity AND grade weight
   - Flag courses below target grade (typically B+ or 87%)
   - Balance short deadlines with long-term prep

3. **Generate Plan**
   - Break assignments into 2-3 hour study blocks
   - Include buffer time (20% minimum)
   - Mix focused study with practice problems

## Output Template

```
📅 WEEKLY STUDY PLAN

🎯 PRIORITY RANKING

1. [Course]: [Assignment]
   Due: [Date/Time] | Weight: [X%] | Est: [X hrs]
   Tips: [2-3 specific tips]

2. [Next priority...]

📊 GRADE STATUS
✅ On track: [Courses with B+ or better]
⚠️ Needs attention: [Courses below target]
   → [One actionable recommendation each]

📋 SUGGESTED SCHEDULE
[Day]: [2-3 hr block for top priority]
[Day]: [Balance remaining work]

💡 QUICK TIPS
- [1-2 high-impact strategies]
```

## Key Principles

- **Verify deadlines**: Check exact times, don't assume midnight
- **Be realistic**: Students have multiple courses; don't overbook
- **Prioritize impact**: Weight + deadline, not just urgency
- **Encourage**: Reduce stress, build confidence

## Fallback

If Canvas data unavailable: provide general study advice and prompt user to connect Canvas in Settings.
