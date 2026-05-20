---
name: Generating New Skills
description: Meta-skill that creates other skills from detected patterns. Use when user repeatedly explains workflow (2+ times), says 'remember this', or you notice repetitive pattern.
---

# Skill Generator

## When to Use
- User explains same process 2+ times
- User says "remember this", "save workflow"
- You notice reusable pattern
- Detailed step-by-step methodology provided

## Detection Signals
1. Repetition (2+ similar requests)
2. Detailed instructions
3. Explicit: "make this a skill"
4. API/docs pattern

## Auto-Learning Process

### Track Pattern
```bash
npm run learn:track
# or
npm run learn:record "what asked" "how to do it"
```

### Threshold → Auto-Generate
After 2 occurrences: `.claude/skills/auto-[intent]-[id]/SKILL.md`

### Generated Format
Official Anthropic format:
- YAML: name + description only
- Gerund-form naming
- Under 500 lines
- Progressive disclosure