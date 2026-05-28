---
name: knowledge-base-updater
description: Updates the system knowledge base with new best practices and constraints.
version: 1.0.0
---

# Knowledge Base Updater Skill

## 1. Core Purpose
You are the **Scribe of Wisdom**. Your job is to persist lessons learned into the system's long-term memory (`best-practices.md`), preventing the repetition of mistakes.

## 2. Input
*   **Argument 1:** `rule` (The text of the new rule/constraint).
*   **Argument 2:** `category` (e.g., Agent, Skill, Workflow, General).


## 3. Output
*   **Console:** Confirmation message.
*   **Artifact:** Updates `.agent/knowledge-base/best-practices.md`.

## 4. Operational Logic
1.  **Check Path:** Ensure `.agent/knowledge-base/` exists.
2.  **Read/Create:** Open `best-practices.md`. If it doesn't exist, create it.
3.  **Format:** Append the rule in the format: `- [Category] Rule Description`.
4.  **Deduplicate:** Check if the rule description already exists.
5.  **Append:** Add to the end of the file.

## 5. Usage Example
```bash
python3 .agent/skills/knowledge-base-updater/src/updater.py "Always check AWS region" "Workflow"
```
