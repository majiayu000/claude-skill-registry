---
name: reflect-off
description: Disable automatic reflection on session end. Manual reflection still works. Activates for reflect off, disable reflect, stop auto reflect.
---

# Reflect Off Command

**Disable automatic reflection when sessions end.**

## Usage

```bash
/sw:reflect-off
```

## What It Does

Disables automatic session analysis:

- Stop hook no longer triggers reflection
- Manual `/sw:reflect` still works
- Existing learnings preserved

## Output

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧠 REFLECT: Automatic Mode Disabled
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌ Auto-reflection is now DISABLED

Changes:
  • Stop hook will NOT analyze sessions
  • Manual /sw:reflect still available
  • Existing learnings preserved

To re-enable: /sw:reflect-on
To check status: /sw:reflect-status
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Related Commands

| Command | Purpose |
|---------|---------|
| `/sw:reflect-on` | Enable automatic reflection |
| `/sw:reflect-status` | Show current configuration |
| `/sw:reflect` | Manual reflection (always works) |

## Execution

**CRITICAL: This is a SIMPLE command. NO Glob, NO parallel tool calls needed.**

When this command is invoked:

1. **Read existing config** (ONE tool call):
   ```
   Read .specweave/state/reflect-config.json
   ```
   (If file doesn't exist, create with autoReflect: false)

2. **Write updated config** (ONE tool call - WAIT for step 1):
   Update `autoReflect` to `false`, preserve other fields.
   Write to `.specweave/state/reflect-config.json`

3. **Display confirmation** (NO tool call - just output text):
   ```
   ❌ Auto-reflection DISABLED

   Manual /sw:reflect still works.
   Use /sw:reflect-on to re-enable.
   ```

**WARNING**: Do NOT use Glob to scan directories - this command only writes ONE file.
