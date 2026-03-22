---
name: vibe-reflect-and-compound
description: Extracts learnings from completed work, feedback, or failures. Updates a persistent learnings file with capped entries. Use after receiving feedback, fixing bugs, or completing complex tasks.
user-invocable: true
---

# vibe-reflect-and-compound

Every problem solved should produce reusable knowledge. Don't just fix — learn.

## When to Use This Skill

- After receiving feedback on your work (positive or negative)
- After a failed attempt or debugging session
- After completing a complex task
- After a code review with substantive feedback
- Periodically (e.g., end of week) to consolidate learnings

## When NOT to Use This Skill

- After trivial tasks (typo fixes, simple renames)
- When there's nothing new to learn (routine work)
- During active implementation (reflect AFTER, not DURING)

## Steps

1. **Gather input** — What happened?
   - What was the task/feedback/failure?
   - What was expected vs. what actually happened?
   - What was the root cause?

2. **Extract patterns** — Ask:
   - "What would I do differently next time?"
   - "What pattern does this represent?"
   - "Is this a recurring theme?"
   - "What would have caught this earlier?"

3. **Formulate learnings** — Each learning should be:
   - **Actionable** — Not "be careful" but "always run race detection before committing concurrent code"
   - **Specific** — Not "tests are important" but "property-based tests catch edge cases that table-driven tests miss for parser code"
   - **Contextual** — Include when it applies and when it doesn't

4. **Update persistent storage** — Write to:
   - Project learnings file (e.g., `docs/learnings.md` or `LEARNINGS.md`)
   - Claude memory (if available)
   - Team wiki/docs

5. **Cap management** — Keep max 30 active learnings. When exceeding:
   - Archive older learnings to a dated file
   - Keep only the most frequently referenced ones active
   - Merge similar learnings

## Output Format

### Reflection: [Context]

**Trigger**: [What prompted this reflection]

**Learnings Extracted**:
1. **[Pattern name]**: [Actionable learning]
   - *Applies when*: [context]
   - *Evidence*: [what happened]

2. **[Pattern name]**: [Actionable learning]
   - *Applies when*: [context]
   - *Evidence*: [what happened]

**Updated**: [Where learnings were saved]
**Active Count**: X/30
