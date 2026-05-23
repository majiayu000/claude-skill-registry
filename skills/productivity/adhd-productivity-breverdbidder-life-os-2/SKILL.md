---
name: adhd-productivity
description: "ADHD-optimized productivity techniques and interventions. Invoke when user shows signs of task abandonment, context switching, or needs focus assistance."
allowed-tools:
  - Read
  - Write
  - Bash
---

# ADHD Productivity Skill

## When to Invoke

- User starts new topic without closing previous task
- User mentions feeling stuck or overwhelmed
- Session duration exceeds 30 minutes without completion
- User asks for help focusing

## Intervention Techniques

### Micro-Commitment
Break tasks into smallest possible step:
- "Just open the file"
- "Just write the first line"
- "Just run one command"

### Body Doubling
Virtual presence accountability:
- "I'm here. You: [action]. Me: ⏱️ Waiting..."
- Set 5-minute timer
- Check in after timer

### Chunking
Divide overwhelming tasks:
- Maximum 3 steps visible at once
- Complete step 1 before revealing step 2
- Celebrate each chunk completion

### Pattern Recognition
Track and call out patterns:
- "This is the 3rd time this week you've switched away from [task]"
- "You typically abandon tasks at the [specific point]"
- "Your completion rate improves when you [specific behavior]"

## Task State Management

```
INITIATED → SOLUTION_PROVIDED → IN_PROGRESS → COMPLETED
                                           ↘ ABANDONED (log pattern)
                                           ↘ BLOCKED (external wait)
                                           ↘ DEFERRED (intentional)
```

## Response Templates

### Level 1 Intervention (0-30 min)
"📌 Quick check: [task] - still on it?"

### Level 2 Intervention (30-60 min)
"🔄 I notice [task] from earlier. Pattern: [observation]. Continue or defer?"

### Level 3 Intervention (>60 min)
"⚠️ ACCOUNTABILITY: [task] started [time] ago. Status? Be honest."

## Success Metrics

Track in `task_completion_streaks` table:
- Daily completion count
- Streak length
- Common blockers
- Peak productivity times
