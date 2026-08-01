---
name: exact-folder-name
description: 'Use when: you need to be sure a new skill will work as intended, confused
  about skill creation, unsure about naming conventions, need help with activation
  descriptions, want to avoid common mistakes'
---

---
name: _skillwriting
description: Use when: you need to be sure a new skill will work as intended, confused about skill creation, unsure about naming conventions, need help with activation descriptions, want to avoid common mistakes
---

# Skill Writing Guide

## Instructions

### 1. CRITICAL: Name First!
**Folder name MUST match skill name exactly**. The Skills system requires this for recognition.
- Choose skill name for precise activation (avoid accidental loading)
- Keep descriptions under 1024 characters
- Use keyword redundancy for reliable activation

### 2. Directory Structure
```
~/claude-autonomy-platform/.claude/skills/<skill-name>/
├── SKILL.md (required)
├── scripts/ (optional - for utility tools)
└── reference/ (optional - for documentation/data)
```

**Important**: Use project-level skills directory, not user-level `~/.claude/skills/`

**Naming Convention**:
- **Core/system skills**: Prefix with underscore (e.g., `_skillwriting`, `_video-watching`, `_svg-drawing`)
- **Personal skills**: No underscore (e.g., `remembering-amy`, `spending-autonomous-time`)
- Core skills are utilities useful to all Claudes; personal skills are individual-specific

### 3. SKILL.md Format
```yaml
---
name: exact-folder-name
description: Specific activation criteria with keywords
---

# Skill Name

## Instructions
[How to use the skill]

## Examples
[Practical examples]
```

### 4. Advanced Features
- **Symlinks work**: Link to central tools for maintenance
- **Scripts accessible**: `python3 scripts/tool.py` works from skill context
- **Session-persistent**: Skills stay active until session swap
- **Multiple skills**: Can have several active simultaneously

### 5. CRITICAL: Writing 'Use When' Descriptions

**Skills are problem detectors, not success validators!**

The description should trigger when someone NEEDS the skill, not when they're already succeeding:

✅ **CORRECT**: "Use when: confused about session swaps, lost todos, wondering when to trigger"
❌ **WRONG**: "Use when: managing session swaps, handling context transitions"

✅ **CORRECT**: "Use when: timer mysteriously stopped, service won't start, getting weird prompts"
❌ **WRONG**: "Use when: monitoring timer health, checking service status"

✅ **CORRECT**: "Use when: baffled by ClAP, errors make no sense, don't know where to start"
❌ **WRONG**: "Use when: debugging ClAP problems, fixing configuration issues"

**The skill should appear at the moment of struggle, not the moment of competence!**

### 6. Best Practices
- Plan name and description before creating folder
- **Write descriptions from the struggling user's perspective**
- Test activation criteria carefully
- Use symlinks for central tool maintenance
- Reference docs with `[file.csv](reference/file.csv)`
- **Avoid duplication**: Cross-reference existing context instead of repeating
- **Unique value only**: Include only what this skill uniquely provides
- **Name triggers**: Put actual names/keywords you want to activate on in description

## Examples

**Good activation**: `"Use when: confused about hedgehog dosing, unsure about medication calculations"`
**Poor activation**: `"Calculate and record medication doses for hedgehogs"` (sounds like you're already doing it)

**Memory skills**: `"Remember Amy, Erin, Ed, Orange, Delta and household members"`
**Name triggers**: Include actual names in description for activation

**Directory naming**:
✅ `hedgehog-dosing/` with `name: hedgehog-dosing`
❌ `hedgehog-meds/` with `name: hedgehog-dosing` (mismatch!)

**Cross-referencing**:
✅ `[See ed-care skill for protocols]` (avoids duplication)
✅ `[See identity doc for details]` (references existing context)
❌ Repeating information available elsewhere
