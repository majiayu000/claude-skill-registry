---
name: debrief
description: End-of-session reflection. Extracts memories, suggests updates to about-taylor.md and CLAUDE.md. Run before ending a long session or when context is getting full. Triggers on "debrief", "extract memories", "session summary".
allowed-tools: Read, Write, Edit, Glob, Bash(date:*)
---

End-of-session debrief to capture learnings and keep documentation current.

## When to Run

- Before ending a productive session
- When context window is getting full
- After significant conversations about preferences, workflows, or decisions
- Periodically as maintenance

## Workflow

### Phase 1: Gather Context

1. **Read current state:**
   - `.claude/memories/about-taylor.md` - Current profile
   - `.claude/memories/index.json` - Existing memories
   - `CLAUDE.md` - Current instructions (skim for relevant sections)

2. **Get today's date:**
   ```bash
   date +%Y-%m-%d
   ```

### Phase 2: Analyze Conversation

Review the conversation for memory-worthy moments:

**Preferences** (category: `preference`)
- "I like X better than Y"
- "I prefer...", "I don't want..."
- Choices made when given options

**Corrections** (category: `workflow` or `context`)
- "Actually...", "No, that's not right"
- Clarifications about how something works
- Misunderstandings corrected

**Personal Context** (category: `personal` or `context`)
- Life events (moves, job changes, milestones)
- Schedule or routine changes
- Health, relationships, living situation

**Workflow Insights** (category: `workflow`)
- How Taylor actually uses tools vs. assumptions
- Shortcuts or patterns observed
- Friction points identified

**Decisions** (category: `project` or `workflow`)
- Architecture or design choices
- Tool/technology selections
- Process changes

### Phase 3: Present Findings

Present findings one category at a time:

```markdown
## Proposed Memories

### Memory 1: [Brief title]
**Category:** preference
**Content:** Taylor prefers X over Y because Z.
**Source:** [Quote or paraphrase from conversation]

Action? [Save / Skip / Edit]
```

### Phase 4: Updates to about-taylor.md

Check if any new information should be added to the profile:
- Job status changes
- New skills or interests
- Updated preferences that are significant enough for the profile
- Life changes (location, situation)

```markdown
## Suggested Profile Updates

### Update 1: [Section]
**Current:** [What it says now, if anything]
**Proposed:** [New or updated text]
**Reason:** [Why this matters]

Action? [Apply / Skip / Edit]
```

**Remember:** about-taylor.md has a 300-line limit. Only add significant, lasting information.

### Phase 5: Updates to CLAUDE.md

Check if any workflow or instruction changes should be documented:
- New conventions established
- Process improvements agreed upon
- Corrections to existing instructions
- New skills or capabilities added

```markdown
## Suggested CLAUDE.md Updates

### Update 1: [Section]
**Location:** [Which section]
**Change:** [What to add/modify]
**Reason:** [Why this should be documented]

Action? [Apply / Skip / Edit]
```

### Phase 6: Execute Approved Changes

For approved memories:
1. Create JSON file: `.claude/memories/YYYY-MM-DD-NNN.json`
   ```json
   {
     "date": "YYYY-MM-DD",
     "category": "preference|workflow|context|project|personal",
     "content": "Concise description (1-2 sentences)",
     "source": "conversation|observation|correction"
   }
   ```
2. Update `.claude/memories/index.json`

For approved profile/CLAUDE.md updates:
1. Apply edits to the relevant files
2. Confirm changes

### Phase 7: Summary

```markdown
## Debrief Complete

**Memories saved:** N
**Profile updates:** N
**CLAUDE.md updates:** N
**Skipped:** N

Next debrief recommended: [if context is still full, suggest continuing]
```

## Memory JSON Format

```json
{
  "date": "2026-01-20",
  "category": "preference",
  "content": "Taylor prefers not to over-engineer tooling for rare edge cases.",
  "source": "conversation"
}
```

## Tips

- Be selective - not every detail needs a memory
- Memories should be durable (still relevant in weeks/months)
- Profile updates should be significant life/work changes
- CLAUDE.md updates should be reusable conventions, not one-off fixes
- When in doubt, ask rather than skip
