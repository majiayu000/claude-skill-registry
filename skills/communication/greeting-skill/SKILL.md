---
name: greeting-skill
description: Activates automatically when user greets warmly. Demonstrates the auto-trigger pattern—Claude detects friendly intent and engages accordingly.
keywords:
  - hello
  - hi
  - greetings
  - welcome
  - hey
  - good morning
  - good afternoon
  - good evening
---

# Greeting Skill

## What This Skill Does

This skill demonstrates the **auto-trigger pattern**. When you greet Claude warmly, it automatically detects your friendly intent and responds with matching warmth and positivity.

**Key concept:** You don't ask Claude to "engage greeting mode"—the skill activates implicitly based on your tone and words.

## Auto-Trigger Keywords

This skill engages when you use:
- "hello", "hi", "hey"
- "welcome", "greetings"
- "good morning", "good afternoon", "good evening"
- Other warm, friendly opening remarks

## Response Approach

When triggered:
1. **Acknowledge the greeting warmly**
2. **Set a positive tone for the conversation**
3. **Offer to help** with whatever the user needs next
4. **Be genuine and personable**

## Example Scenarios

### Scenario 1: Simple Hello
**User:** "Hello!"
**Response:** (Skill auto-triggers)
- Warm acknowledgment
- Brief, genuine response
- Ready to help with next task

### Scenario 2: Greeting with Context
**User:** "Hi! I'm ready to work on the project"
**Response:** (Skill auto-triggers)
- Match their energy
- Acknowledge their readiness
- Transition into work mode

### Scenario 3: First Message of Session
**User:** "Good morning!"
**Response:** (Skill auto-triggers)
- Return the greeting
- Energetic, positive start
- Invite them into the work ahead

## What Makes This Different from `/greet` Command

| Aspect | greeting-skill | /greet command |
|--------|---|---|
| **Trigger** | Automatic (implicit) | Manual (explicit: `/greet`) |
| **Purpose** | Set session tone | Personalized greeting with arguments |
| **Use Case** | Conversational opener | Explicit greeting of specific person |

Both coexist—they serve different purposes.

## Key Insight: Auto-Triggers in Action

This skill is a simple but powerful demonstration of why auto-triggers matter:
- **No friction** - Just be yourself; the skill responds appropriately
- **Implicit intent** - Claude understands your tone without explicit instructions
- **Natural interaction** - Feels conversational, not formulaic

This same pattern powers more complex skills (like code-review-skill, which auto-triggers when you mention debugging or refactoring).
