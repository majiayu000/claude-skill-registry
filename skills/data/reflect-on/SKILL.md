---
name: reflect-on
description: Enable automatic reflection on session end. Stop hook will analyze session and extract learnings automatically. Activates for reflect on, enable reflect, auto reflect, automatic learning.
---

# Reflect On Command

**Enable automatic reflection when sessions end.**

## Usage

```bash
/sw:reflect-on
```

## What It Does

Enables automatic session analysis via the stop hook:

```
1. Session starts
      ↓
2. You work with Claude (corrections, approvals, patterns)
      ↓
3. Session ends (all tasks done / user closes)
      ↓
4. Stop hook triggers
      ↓
5. Reflect automatically analyzes transcript
      ↓
6. Learnings extracted and saved to CLAUDE.md Skill Memories
      ↓
7. "Learned from session" notification shown
```

## Output

```
Auto-reflection ENABLED

Stop hook will analyze sessions on exit.
Learnings will be saved to CLAUDE.md Skill Memories section.

Use /sw:reflect-off to disable.
```

## Configuration

Auto-reflection is controlled by `.specweave/config.json`:

```json
{
  "reflect": {
    "enabled": true,
    "model": "haiku",
    "maxLearningsPerSession": 3
  }
}
```

## Related Commands

| Command | Purpose |
|---------|---------|
| `/sw:reflect-off` | Disable automatic reflection |
| `/sw:reflect-status` | Show current configuration |
| `/sw:reflect` | Manual reflection (works anytime) |

## Execution

When this command is invoked:

1. **Read existing config** from `.specweave/config.json`
2. **Update config** to set `reflect.enabled: true`
3. **Display confirmation** message
