---
name: reflect-check
description: Diagnostic tool for validating SpecWeave reflection system health and troubleshooting issues. Use when reflection seems stuck, learnings aren't being captured, or CLAUDE.md Skill Memories aren't updating. Checks configuration, permissions, and system state.
allowed-tools: Read, Bash
---

# Reflect Health Check

**Version**: 2.0.0
**Category**: Diagnostics
**Status**: Active

## Purpose

Diagnostic command to validate reflection system health and troubleshoot issues.

## Activation Triggers

**Primary keywords**:
- `reflect-check`
- `reflect check`
- `check reflect`
- `reflection health`
- `reflect diagnostics`

**Natural language**:
- "Check if reflection is working"
- "Why isn't reflection learning?"
- "Is auto-reflect enabled?"
- "Diagnose reflection issues"
- "Reflection not working"

## What This Skill Does

Runs comprehensive health checks on the reflection system:

1. **Config validation**: Checks `.specweave/config.json` reflect settings
2. **CLAUDE.md check**: Verifies Skill Memories section exists
3. **Recent activity**: Shows learnings in CLAUDE.md
4. **Hook status**: Verifies reflection hooks are working

## Execution

When activated, check these items in order:

1. Read `.specweave/config.json` for reflect configuration
2. Read `CLAUDE.md` for Skill Memories section
3. Count learnings per skill category
4. Report any issues found

## Output Format

```
REFLECT HEALTH CHECK

Configuration
   Reflection:      Enabled
   Model:           haiku
   Max/session:     3

CLAUDE.md Status
   Skill Memories:  Found
   Total learnings: 5 across 3 skills

   - devops: 1 learning
   - frontend: 2 learnings
   - general: 2 learnings

Last modified: 2026-01-29

RECOMMENDATIONS
   - None - system healthy
```

## When to Use

- Reflection seems stuck or not learning
- After marketplace updates
- User reports "reflection not working"
- Debugging silent failures
- Verifying system health

## Success Criteria

- Config exists with reflect enabled
- CLAUDE.md has Skill Memories section
- Learnings are being added
- Clear actionable recommendations if issues found

## Related

- `/sw:reflect` - Manual reflection
- `/sw:reflect-status` - Show config and stats

## Project-Specific Learnings

**Before starting work, check for project-specific learnings:**

```bash
# Check if skill memory exists for this skill
cat .specweave/skill-memories/reflect-check.md 2>/dev/null || echo "No project learnings yet"
```

Project learnings are automatically captured by the reflection system when corrections or patterns are identified during development. These learnings help you understand project-specific conventions and past decisions.

