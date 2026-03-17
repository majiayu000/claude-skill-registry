---
name: hook-template
description: Generate hook script from template
user-invocable: true
---

# Hook Template Generator

Generate a hook script and configuration based on requirements.

**Usage**: `/hook-template [hook-type] [purpose]`

---

## Hook Types

| Type | When it Runs | Use Case |
|------|--------------|----------|
| `PreToolUse` | Before tool | Block, validate |
| `PostToolUse` | After tool | Log, notify |
| `Stop` | When stopping | Continue loops |
| `Notification` | On alerts | External notify |

---

## Process

1. **Gather Requirements**
   - Hook type
   - Purpose
   - Matcher (for Pre/PostToolUse)

2. **Generate Script** at `.claude/hooks/[name].sh`

3. **Update settings.json** with hook config

4. **Make Executable**: `chmod +x`

5. **Validate** with `/hooks-check`

---

## Templates

### PreToolUse (Blocker)
```bash
#!/bin/bash
INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name')
# Your logic
echo '{"decision": "allow"}'
```

### Stop (Auto-Loop)
```bash
#!/bin/bash
CHECKPOINT=".auto-loop/checkpoint.json"
if [[ ! -f "$CHECKPOINT" ]]; then
  echo '{"decision": "allow"}'
  exit 0
fi
# Continue logic
```

---

## Example

```
/hook-template PreToolUse "block edits to package-lock.json"

Creates:
- .claude/hooks/protect-lockfile.sh
- Updates .claude/settings.json
```
