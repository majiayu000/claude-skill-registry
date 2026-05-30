---
name: reflect
description: >
  Analyzes conversation transcripts to extract user corrections, patterns, and preferences,
  then proposes skill improvements. Use this skill when users provide corrections, express
  preferences about code style, or when patterns emerge from successful approaches. Can be
  triggered manually with /reflect or automatically at session end when enabled.
---

# Reflect - Self-Improving Skills

## Overview

This skill enables Claude Code to learn from conversations by analyzing corrections,
approvals, and patterns, then proposing updates to relevant skills. It implements
a "correct once, never again" learning system.

## Usage Modes

### 1. Manual Reflection (/reflect)
Trigger analysis of the current conversation:
```
/reflect [skill-name]
```
- Without skill-name: Analyzes all skills used in conversation
- With skill-name: Focuses on specific skill

### 2. Automatic Reflection
When enabled via `/reflect-on`, runs automatically at session end via Stop hook.

### 3. Toggle Commands
- `/reflect-on` - Enable automatic reflection
- `/reflect-off` - Disable automatic reflection
- `/reflect-status` - Show current configuration

## Confidence Levels

**HIGH** - Explicit corrections:
- User contradicts Claude's approach with specific alternative
- Pattern: "Don't do X, do Y instead"
- Action: Direct updates with deprecation warnings

**MEDIUM** - Approvals and patterns:
- User approves specific approach
- Pattern succeeds multiple times
- Action: Add to "Best Practices" section

**LOW** - Observations:
- User questions or suggests alternatives
- Pattern: "Have you considered..." or "Why not try..."
- Action: Add to "Considerations" section

## Workflow

1. **Signal Detection** - Scan transcript for corrections/patterns
2. **Context Analysis** - Extract 5-message context around signals
3. **Skill Mapping** - Match signals to relevant skills
4. **Change Proposal** - Generate diff of proposed updates
5. **User Review** - Interactive approval with natural language editing
6. **Application** - Safe YAML/markdown updates with backups
7. **Git Commit** - Automatic commit with descriptive message

## Scripts

### Core Engine
- `scripts/reflect.py` - Main orchestration logic
- `scripts/extract_signals.py` - Pattern detection engine
- `scripts/update_skill.py` - Safe skill file updates
- `scripts/present_review.py` - Interactive review interface

### Automation
- `scripts/hook-stop.sh` - Stop hook integration
- `scripts/toggle-on.sh` - Enable auto-reflection
- `scripts/toggle-off.sh` - Disable auto-reflection
- `scripts/toggle-status.sh` - Show status

## Safety Features

- Timestamped backups before all edits
- YAML validation before writing
- Lock files prevent concurrent runs
- Graceful error handling with rollback
- Git status checks before commits

## References

See `references/signal-patterns.md` for detailed pattern library.
