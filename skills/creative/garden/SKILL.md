---
name: garden
description: Manage the Idea Garden - plant new ideas, water the garden for fresh ideas, compost rejected ones. Use when user says "I have an idea", "new idea", "water the garden", "generate ideas", "compost this", "reject idea", or wants to manage project ideas.
allowed-tools: Read, Edit, Glob, Grep, Task
---

# Idea Garden Skill

Manages `_AUDIT/GARDEN.md` and `_AUDIT/COMPOST.md` for idea lifecycle tracking.

## Actions

### Plant an Idea
**Triggers:** "I have an idea for...", "new idea", "add idea"

1. Parse idea title from user input
2. Ask for:
   - Short description (1-2 sentences)
   - Key bullet points (2-4 items)
3. Add to `_AUDIT/GARDEN.md` under ## Ideas:
   ```markdown
   ### [Idea Title]
   **Planted:** YYYY-MM-DD
   [Short description]
   - Bullet point 1
   - Bullet point 2
   ```
4. Update "Active Ideas" count in header
5. Update "Last Updated" date

### Water the Garden
**Triggers:** "water the garden", "generate ideas", "brainstorm"

1. Read `_AUDIT/GARDEN.md` to understand existing ideas
2. Read `_AUDIT/COMPOST.md` to understand rejected patterns
3. Generate 10 new ideas that:
   - Extend or complement existing ideas
   - Avoid patterns that led to rejection
   - Align with project goals
4. Present as numbered list:
   ```
   ## Fresh Ideas
   1. **[Title]** - One-line description
   2. **[Title]** - One-line description
   ...

   Which ideas would you like to plant? (e.g., 1, 3, 5)
   ```
5. Plant selected ideas with today's date

### Compost an Idea
**Triggers:** "compost this", "reject idea", "don't want this idea", "remove this"

1. Find idea in GARDEN.md (or accept direct rejection)
2. Ask for rejection reason
3. Add to `_AUDIT/COMPOST.md`:
   ```markdown
   ### [Idea Title]
   **Composted:** YYYY-MM-DD
   **Reason:** [User's reason]
   [Original description if available]
   ```
4. Remove from GARDEN.md if present
5. Update counts in both files

### Graduate an Idea to Plan
**Triggers:** "let's plan this idea", "graduate idea"

1. Find idea in GARDEN.md
2. Enter Plan Mode to create plan in `_PLANS/`
3. Move idea to "Graduated to Plans" table
4. Remove from ## Ideas section

## Idea Lifecycle
- **Fresh** (0-44 days): Ready for development
- **Wilting** (45-60 days): Needs attention, marked ⚠️
- **Composted** (60+ days): Auto-moved during farm audit
