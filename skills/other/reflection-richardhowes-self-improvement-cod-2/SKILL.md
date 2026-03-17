---
name: reflection
description: Self-improving meta-skill that learns from user corrections and updates the TARGET PROJECT's skill files. Only runs when user explicitly says "reflect". Commits all skill updates to Git.
---

# Reflection Skill

## Purpose

Improve future Claude Code sessions by learning from mistakes and user corrections.
Updates skill files in the **target project's** `.claude/skills/` directory.

This is a **meta-skill** - it modifies other skills based on session learnings.

## When to Run (Explicit Triggers Only)

Only activate when the user explicitly requests reflection:

- "reflect"
- "don't do this again"
- "remember this for next time"
- "update your skills"
- "learn from this"

**Never run automatically** - always wait for explicit user trigger.

## Where Rules Go

Rules are written to the **target project's** skill files (NOT the plugin repository):

| Rule Type | Target File |
|-----------|-------------|
| General conventions | `.claude/skills/conventions.md` |
| VILT patterns | `.claude/skills/vilt-patterns.md` |
| Project-specific | `.claude/skills/project-rules.md` |
| Unclear/mixed | `.claude/skills/lessons-learned.md` |

If the target project doesn't have `.claude/skills/`, create it with a starter structure.

## Process

1. **Analyse** the completed session
   - Review conversation for corrections
   - Identify repeated mistakes
   - Note stated preferences

2. **Extract** atomic, durable rules
   - One rule per concept
   - "Do X" or "Never Y" format
   - Date-stamped for tracking

3. **Check** for contradictions
   - Read existing skill files
   - Flag conflicting rules
   - Ask user to resolve

4. **Update** appropriate skill file(s)
   - Append to `## Learned Rules` section
   - Preserve existing formatting
   - Keep changes minimal

5. **Commit** changes separately from code
   - Use semantic commit message
   - Include rule summary in body

## Rule Quality Bar

A rule must be:

- **Durable**: Will apply to future work in this project
- **Actionable**: Clear imperative ("Always X", "Never Y")
- **Specific**: Not too broad or vague
- **Non-contradicting**: Doesn't conflict with existing rules

## Rule Format

```markdown
- [YYYY-MM-DD] RULE_TEXT (source: BRIEF_CORRECTION_CONTEXT)
```

Examples:
```markdown
- [2025-01-09] Always eager load relationships in service methods that return collections (source: booking service review)
- [2025-01-09] Never use axios - use Inertia router instead (source: corrected 3x in dashboard component)
- [2025-01-10] Use FloatingLabelInput for all form fields (source: user preference stated)
```

## Starter Skill Structure

When creating `.claude/skills/` in a new project:

```markdown
# Lessons Learned

## Purpose
Project-specific rules learned from Claude Code sessions.

## Learned Rules
<!-- Reflection appends here -->
```

## Git Commit Format

```
chore(skills): reflect session learnings

- Added: [rule summary]
- Source: [correction context]
- File: .claude/skills/[filename].md
```

## What NOT to Learn

Do not create rules for:
- One-time exceptions
- User's momentary preferences
- Context-specific decisions
- Temporary workarounds

Only learn patterns that should **always** apply.
