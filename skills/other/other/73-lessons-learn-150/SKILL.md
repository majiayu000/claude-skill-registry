---
name: 73-lessons-learn-150
description: "[73] LESSONS. Record and maintain Lessons in MEMORY.md after a problem is solved or the user confirms success. Use when capturing a new lesson, moving lessons through the pipeline, or enhancing Project Architecture Quick Reference with new insights."
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

## What are "Principles" (from AGENTS.md and MEMORY.md)

- **Principle Scan (AGENTS.md):** After every message, the agent analyzes whether the task/solution revealed a **fundamental truth, protocol, or anti-pattern** that is a **general rule** (not a one-off). If yes, it records a "Principles Detected" block (e.g. `## 🧠 Principles Detected` with `**[Name]**: [definition]`).
- **Principles in MEMORY.md:** The section `## 🧠 Principles (Context Engineering)` holds the curated map (Architecture Map, Coding Conventions, Domain Axioms, Anti-Patterns). Each Lesson has a **Principle:** field = one-sentence rule. When closing lessons, any **Principles Detected** during the session must also be persisted there.

## Workflow

1. **Read the active session log** in `.sessions/SESSION_[date]-[name].md` for evidence, context, and any **Principles Detected** blocks (or "Followed Principles") from agent responses.
2. **Open `MEMORY.md`** (repo root).
3. **Record Principles Detected:** For each principle that was detected during the session (from session log or from the work just done):
   - If it is already captured as the **Principle:** of a new lesson below, do not duplicate.
   - If it is a standalone general rule (convention, axiom, or anti-pattern), add it to `## 🧠 Principles` in the appropriate subsection (e.g. **Coding Conventions**, **Domain Axioms**, **Anti-Patterns**) as a new bullet: `*   **[Name]:** [Concise definition].`
4. **Append a new Lesson** to `## 🆕 Lessons (Inbox)` using this template:

```
### <YYYY-MM-DD> <Short title>
**Problem:** <what was broken>
**Attempts:** <what was tried, if any>
**Solution:** <what fixed it>
**Why it worked:** <causal explanation>
**Principle:** <one-sentence rule for the future>
```

5. **If 3+ related lessons exist**, create a Short‑Term entry:
   - Move the related lessons (or summarize them) into `## 🔄 Short-Term Memory`.
   - Write a common pattern and an emerging principle.

6. **If a principle is stable**, promote it to `## 💎 Long-Term Memory` as a protocol:
   - Format: Context → Protocol → Reasoning.

7. **Review Project Architecture Quick Reference** and enhance if needed:
   - Check if the lesson reveals new architectural insights (new directories, patterns, workflows)
   - Add missing directories, workspaces, or key patterns discovered during work
   - Update existing entries with new information or clarifications
   - Keep the reference current and comprehensive

## Output expectations

- Report exactly what you recorded or moved.
- Report how many **Principles Detected** were recorded and where (Inbox lesson **Principle:** field vs. `## 🧠 Principles` section).
- If you did **not** write a lesson, say why.
- If you updated the Project Architecture Quick Reference, specify what was added or modified.