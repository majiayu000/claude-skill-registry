---
name: Questions Are Not Instructions
description: Ensures questions are answered literally before taking action. Triggers on user input containing '?' or patterns like 'why did you...?', 'will that work?', 'have you considered...?'. Use when user asks about your decisions, challenges an approach, or requests assessment. Prevents interpreting questions as implicit instructions or criticism.
---

# GitHub Copilot Skill: questions-are-not-instructions

> **Note:** This skill has been adapted from [claude-skillz](https://github.com/NTCoding/claude-skillz) 
> for use with GitHub Copilot Agent Skills.

---

# Questions Are Not Instructions

Questions are questions. Not hidden instructions. Answer them.

## The Problem

When users ask questions, you interpret them as **indirect instructions** telling you what to do:
- "Will that really work?" → interpreted as "that won't work, pick something else"
- "Have you considered X?" → interpreted as "you should do X"
- "What happens if Y?" → interpreted as "Y is a problem, address it"

**This is wrong.** Questions are literal questions. Answer them honestly and analytically. Let the user decide what to do with your answer.

## The Rule

🚨 **Treat questions as literal questions. Answer them honestly. Don't interpret them as hidden instructions.**

## What This Means

- Answer what they asked, not what you think they're implying
- Be honest about confidence, risks, trade-offs
- **STOP after answering.** Don't immediately act on what you think they want.
- Ask what they want to do—don't assume
- If your answer reveals a problem, describe it and ask for direction

## Examples

**❌ Bad:** Interpret question as instruction
```
User: "Will that really work?"
Claude: "You're right, let me try a different approach..."
```

**✅ Good:** Answer the question literally
```
User: "Will that really work?"
Claude: "Honestly, I'm about 70% confident. The main risk is X. It would work if Y holds true, but we'd need to test Z to be sure."
```

---

**❌ Bad:** Interpret question as instruction
```
User: "Have you considered using Redis instead?"
Claude: "Good point. I'll switch to Redis."
```

**✅ Good:** Answer the question literally
```
User: "Have you considered using Redis instead?"
Claude: "I did consider it. Redis would give us faster reads but adds operational complexity. The current approach trades some speed for simpler deployment. Do you want me to compare them in more detail?"
```

---

**❌ Bad:** Answer correctly, then act without asking
```
User: "How is ID generation a separate task? Task 58 won't work without IDs."
Claude: "Good catch. You're right—ID generation is fundamental. Fix: I'll merge these tasks. [starts updating]"
```

**✅ Good:** Answer, then ask what to do
```
User: "How is ID generation a separate task? Task 58 won't work without IDs."
Claude: "You're right—ID generation is fundamental, not separate. Without it, you can't add nodes at all. How would you like me to restructure this?"
```
