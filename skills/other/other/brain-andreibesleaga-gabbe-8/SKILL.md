---
name: episodic-consolidation
description: Consolidate short-term events into long-term 'Semantic' memory.
context_cost: high
tools: [write_to_file, grep_search]
---

# Episodic Consolidation Skill

This skill mimics the brain's "Sleep" process (Hippocampus to Neocortex transfer). Use it at the end of a long task (Task Boundary).

## 1. The Consolidation Process
1.  **Replay:** Review the `AUDIT_LOG.md` or Session History.
2.  **Extract:** Identify "Generalized Rules" from specific events.
    *   *Event:* "I fixed a bug in `auth.go` caused by nil pointer."
    *   *Rule:* "Always check for nil in `auth.go` User structs."
3.  **Store:** Write this Rule to `memory/semantic/rules.md`.

## 2. Identifying Episodic Drifts
Check if the "Story" of the project has changed.
*   **Drift:** "We used to use SQL, now we use NoSQL."
*   **Action:** Update the `PROJECT_CONTEXT.md` (The World Model) to reflect this new reality.

## 3. Pruning (Forgetting)
Active forgetting is crucial.
*   **Action:** Delete temporary scratchpads, logs, or `tmp/` files that are no longer predicting the future.
