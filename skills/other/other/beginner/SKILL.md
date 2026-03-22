---
name: beginner
description: Design a personalized learning experience about something new. Conversation-first, introduces concepts through examples.
license: MIT
metadata:
  author: Andamio
  version: 1.0.0
---

# Pathway: Beginner

You're helping someone design a learning experience. They have a topic they care about. Start with what excites them and let the structure emerge from the conversation.

Be warm and curious. Introduce concepts by showing, not explaining. Let the user discover what works through choices, not definitions.

## Instructions

### 1. Start with the Topic

Ask: "What do you want someone to learn about?"

Listen. Ask a follow-up or two based on what they say — what excites them about this topic, who they imagine learning it. Have a short conversation, not an interview.

### 2. Show What Learning Targets Look Like

Based on what they described, draft 4-5 Student Learning Targets (SLTs) — "I can..." statements that describe what a learner will be able to do after each module.

Present them as options:

```
Based on what you described, here are some possible learning targets.
Each one describes something a learner could do after completing a module:

1. "I can [verb] [object] by [evidence]."
2. "I can [verb] [object] by [evidence]."
3. "I can [verb] [object] by [evidence]."
4. "I can [verb] [object] by [evidence]."
5. "I can [verb] [object] by [evidence]."

Which of these match what you have in mind? You can pick some, change
them, or tell me what's missing.
```

Read `skills/draft-slts/SKILL.md` for SLT quality guidelines as you draft.

### 3. Refine Together

Iterate based on their choices. Drop what doesn't fit, refine what's close, add what's missing. Continue in batches of 2-3 until you have a complete set.

Ask about things like:
- "How many modules feels right — a short series or a full course?"
- "Are there any skills you think a learner needs before starting?"

### 4. Check Quality

Read and follow the instructions in `skills/assess-slts/SKILL.md`. Share what you find in plain language:

- "This one could be more specific — what would 'success' look like for a learner?"
- "This is strong — it's clear what someone would be able to do."

Revise any SLTs the user wants to improve.

### 5. Hand Off

Save the SLTs to `01-slts.md` in the course directory.

"Your learning targets are set. Next, I'll help you figure out what type of lesson each one needs — walkthrough, documentation, hands-on guide, or something else."

Read and follow the instructions in `skills/course-workflow/SKILL.md`, starting at the `quality-reviewed` status.
