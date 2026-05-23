---
name: 73-close-lessons-learn-150
description: "[73] CLOSE. Record and maintain Lessons in MEMORY.md after a problem is solved or the user confirms success. Use when capturing a new lesson, moving lessons through the pipeline, updating Session State, or enhancing Project Architecture Quick Reference with new insights."
---

# Close-Lessons-Learn 150 Protocol

## Goal

Capture durable learning from a solved problem and keep the Memory pipeline consistent.

## When to use

Use this skill when:
- The user confirms a fix worked (e.g., "works", "fixed", "отлично").
- A non‑obvious bug or root cause was discovered.
- A recurring pattern should be turned into a protocol.
- New architectural insights emerge that should be documented in Project Architecture Quick Reference.

## Workflow

1. **Open `MEMORY.md`** (repo root).
2. **Append a new Lesson** to `## 🆕 Lessons (Inbox)` using this template:

```
### <YYYY-MM-DD> <Short title>
**Problem:** <what was broken>
**Attempts:** <what was tried, if any>
**Solution:** <what fixed it>
**Why it worked:** <causal explanation>
**Principle:** <one-sentence rule for the future>
```

3. **If 3+ related lessons exist**, create a Short‑Term entry:
   - Move the related lessons (or summarize them) into `## 🔄 Short-Term Memory`.
   - Write a common pattern and an emerging principle.

4. **If a principle is stable**, promote it to `## 💎 Long-Term Memory` as a protocol:
   - Format: Context → Protocol → Reasoning.

5. **Update Session State** only if it affects the current task.

6. **Review Project Architecture Quick Reference** and enhance if needed:
   - Check if the lesson reveals new architectural insights (new directories, patterns, workflows)
   - Add missing directories, workspaces, or key patterns discovered during work
   - Update existing entries with new information or clarifications
   - Keep the reference current and comprehensive

## Output expectations

- Report exactly what you recorded or moved.
- If you did **not** write a lesson, say why.
- If you updated the Project Architecture Quick Reference, specify what was added or modified.
