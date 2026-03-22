---
name: memory-tiering
description: Automated multi-tiered memory management (HOT, WARM, COLD). Use this skill to organize, prune, and archive context during memory operations or compactions.
---

# Memory Tiering Skill 🧠⚖️

This skill implements a dynamic, three-tiered memory architecture to optimize context usage and retrieval efficiency.

## The Three Tiers

1.  **🔥 HOT (memory/hot/HOT_MEMORY.md)**:
    *   **Focus**: Current session context, active tasks, temporary credentials, immediate goals.
    *   **Management**: Updated frequently. Pruned aggressively once tasks are completed.
2.  **🌡️ WARM (memory/warm/WARM_MEMORY.md)**:
    *   **Focus**: User preferences (Hui's style, timezone), core system inventory, stable configurations, recurring interests.
    *   **Management**: Updated when preferences change or new stable tools are added.
3.  **❄️ COLD (MEMORY.md)**:
    *   **Focus**: Long-term archive, historical decisions, project milestones, distilled lessons.
    *   **Management**: Updated during archival phases. Detail is replaced by summaries.

## Workflow: `Organize-Memory`

Whenever a memory reorganization is triggered (manual or post-compaction), follow these steps:

### Step 1: Ingest & Audit
- Read all three tiers and recent daily logs (`memory/YYYY-MM-DD.md`).
- Identify "Dead Context" (completed tasks, resolved bugs).

### Step 2: Tier Redistribution
- **Move to HOT**: Anything requiring immediate attention in the next 2-3 turns.
- **Move to WARM**: New facts about the user or system that are permanent.
- **Move to COLD**: Completed high-level project summaries.

### Step 3: Pruning & Summarization
- Remove granular details from COLD.
- Ensure credentials in HOT point to their root files rather than storing raw secrets (if possible).

### Step 4: Verification
- Ensure no critical information was lost during the move.
- Verify that `HOT` is now small enough for efficient context use.

## Usage Trigger
- Trigger manually with: "Run memory tiering" or "整理记忆层级".
- Trigger automatically after any `/compact` command.
