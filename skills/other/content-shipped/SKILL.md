---
name: content-shipped
description: |
  Log shipped content to the content log. Use when user says "I shipped", "I published", "just posted", or mentions completing content work.
license: MIT
compatibility: marvin
metadata:
  marvin-category: content
  user-invocable: false
  slash-command: null
  model: default
  proactive: true
---

# Content Shipped Skill

Log completed content to track progress against goals.

## When to Use

Trigger phrases:
- "I shipped..."
- "I published..."
- "Just posted..."
- "Finished the..."
- "The {article/video/post} is live"

## Process

### Step 1: Extract Content Details
From the conversation, identify:
- **Type**: Article, video, podcast, social post, etc.
- **Title**: The content title
- **URL**: Link if available
- **Platform**: Where it was published
- **Goal**: Which monthly/annual goal this counts toward

### Step 2: Confirm Details
If any details are unclear, ask:
- "What's the title?"
- "Where was it published?"
- "Which goal does this count toward?"

### Step 3: Log to Content File
Append to `content/log.md`:

```markdown
### {DATE}
- **[{TYPE}]** "{Title}"
  - URL: {link}
  - Platform: {where published}
  - Goal: {which goal this supports}
```

### Step 4: Update Progress
Check `state/goals.md` for relevant monthly targets and note progress.

### Step 5: Celebrate (briefly)
Acknowledge the shipped work:
- "Nice! That's {X}/{Y} for the month."
- "Logged. You're on track for {goal}."

## Output Format

```
Logged: **[{TYPE}]** "{Title}"
Progress: {X}/{Y} {content type} this month
```

## Notes
- Be proactive about detecting shipped content in conversation
- Don't require explicit trigger if context is clear
- Keep celebration brief, not over-the-top

---

*Skill created: 2026-01-22*
