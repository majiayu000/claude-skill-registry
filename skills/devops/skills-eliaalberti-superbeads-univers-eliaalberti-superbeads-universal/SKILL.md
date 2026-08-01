---
name: skills-eliaalberti-superbeads-univers
description: Updates the project's CLAUDE.md with key learnings from this session,
  optimized for context efficiency.
---

# /preserve - Preserve Session Knowledge to CLAUDE.md

## Description

Updates the project's CLAUDE.md with key learnings from this session, optimized for context efficiency.

You MUST use this skill at the end of significant sessions. This ensures knowledge persists across sessions and prevents re-learning.

---

## Purpose

Preserve session knowledge efficiently:
- Update CLAUDE.md with decisions, progress, insights
- Maintain context efficiency (target: <280 lines)
- Archive old content when needed
- Protect core sections from archiving

## Usage

- `/preserve` - Interactive preservation with options
- Run at end of sessions with significant learnings

---

## Process

### Step 1: Check for CLAUDE.md

Look for CLAUDE.md in the current working directory (or common variations):
- `CLAUDE.md`
- `Claude.md`
- `.claude/CLAUDE.md`

If not found, ask:
"No CLAUDE.md found. Would you like me to create one, or output preservation notes to conversation instead?"

### Step 2: Ask What to Preserve

Use AskUserQuestion with multi-select:

**Question:** "What should be preserved from this session?"

**Options:**
1. **Phase/Status Changes** - What moved forward, what's now complete
2. **Key Decisions** - Choices made and why (for future reference)
3. **New Files/Structure** - What was created or changed
4. **Patterns/Insights** - Reusable learnings, "aha" moments
5. **Blockers/Warnings** - Issues for future sessions
6. **Next Steps** - Clear action items

### Step 3: Review Current CLAUDE.md

If CLAUDE.md exists, read it to understand:
- Current structure and format
- What sections exist
- What needs updating vs adding

### Step 4: Generate Updates

Based on selections, prepare updates following these rules:

**HIGH SIGNAL (include):**
- Status changes (1 line each)
- Decisions + rationale (table row format)
- New directories/files (brief tree or list)
- Clear next steps

**LOW SIGNAL (exclude):**
- Verbose explanations (point to docs)
- Implementation details (they're in files)
- Full file contents
- Timestamps or session logs

**FORMAT RULES:**
- Tables for structured data
- Single-line entries, not paragraphs
- Point to files: "See `path/to/file.md`"
- Target: CLAUDE.md under 280 lines

### Step 5: Apply Updates

Edit CLAUDE.md directly, then summarize:

```
CLAUDE.md Updated

Preserved:
* [What was added/changed]
* [What was added/changed]

CLAUDE.md is now [X] lines (target: <280)
```

### Step 6: Check Line Count and Archive Logic

After updating, count CLAUDE.md lines:
```bash
wc -l CLAUDE.md
```

**IF lines > 280:**

1. **Identify auto-archivable content:**
   - `## Session Notes (DATE)` sections older than 7 days
   - `## Completed Projects` section

2. **Calculate impact:**
   - Current lines
   - Lines after auto-archive

3. **Report to user:**
   ```
   CLAUDE.md is [X] lines (target: <280).

   Auto-archivable content found:
   * Session Notes (2026-01-10) - 25 lines
   * Completed Projects - 15 lines

   Archiving would reduce to [Y] lines.

   Archive now? [Yes / No, all content is essential]
   ```

4. **IF still > 280 after auto-archivable content:**

   Identify other sections that are NOT in the CORE list (see below) and NOT marked PROTECTED:

   ```
   Still over 280 lines. These sections could also be archived:
   * ## [Non-core Section] - 12 lines
   * ## [Another Section] - 8 lines

   Archive these too? [Yes / No / Select which]
   ```

5. **IF user approves archiving:**
   - Find project root (where CLAUDE.md is)
   - Append archived content to {project_root}/CLAUDE-Archive.md
   - Remove archived sections from CLAUDE.md
   - Report result

### Step 7: Archive File Handling

**Archive file location:**
```
{project_root}/CLAUDE-Archive.md
```

**Archive file format:**
```markdown
# CLAUDE.md Archive

Archived content from CLAUDE.md to maintain context efficiency.

---

## Archived: [DATE]

[Archived section content]

---
```

**If archive exists:** Append new content with date header.

### Step 8: If No CLAUDE.md

Output a structured summary to conversation:

```markdown
# Session Preservation: [Brief Title]
**Project:** [Directory name]
**Date:** [Today]

## [Selected sections with content]

---

## Quick Resume Context
[2-3 sentences for future sessions]
```

Then suggest: "Consider creating a CLAUDE.md to persist this across sessions."

---

## CORE Sections (Never Suggest Archiving)

These section names are essential and should NEVER be suggested for archiving:

- `## Context`
- `## Approach`
- `## Paths`
- `## Key References`
- `## Skills`
- `## MCP Tools`
- `## Key Patterns`
- `## Current Status`
- `## Next Steps`
- Any section with `(PROTECTED)` in the heading

---

## Auto-Archivable Patterns

These patterns are automatically identified as archivable:

| Pattern | Rule |
|---------|------|
| `## Session Notes (DATE)` | Archive if DATE is > 7 days old |
| `## Completed Projects` | Always archivable |
| `## Completed Tasks` | Always archivable |
| Sections with `(ARCHIVABLE)` | User-marked as archivable |

---

## Best Practices

### Do's

- Run /preserve after significant sessions
- Choose only what's truly worth preserving
- Keep entries concise - point to files, don't duplicate
- Respect existing CLAUDE.md format

### Don'ts

- Don't preserve implementation details (they're in the code)
- Don't let CLAUDE.md grow unbounded
- Don't archive PROTECTED or CORE sections
- Don't preserve every session - only meaningful ones

---

## Guidelines

- **Context efficiency is paramount** - Future sessions pay for every token
- **Signal over noise** - The "why" matters more than the "what"
- **Point, don't duplicate** - Reference files instead of copying content
- **Respect existing format** - Match the CLAUDE.md style already in use
- **Never archive PROTECTED or CORE** - These are essential for context
- **Ask before archiving non-auto content** - User decides what's truly essential

---

## Related Skills

- [resume-SKILL](./resume-SKILL.md) - Start sessions by loading CLAUDE.md
- [compress-SKILL](./compress-SKILL.md) - Save full session logs before /compact
- [wrapup-SKILL](./wrapup-SKILL.md) - Quick session end with summary

---

*This skill preserves session knowledge to CLAUDE.md for future sessions.*
