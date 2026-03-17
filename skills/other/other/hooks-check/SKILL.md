---
name: hooks-check
description: Validate hooks configuration and scripts
user-invocable: true
---

# Hooks Validator

Validate hooks configuration in `.claude/settings.json` and hook scripts.

---

## Validation Steps

### 1. Check settings.json
Verify `hooks` section exists and is valid.

### 2. Validate Hook Structure
```json
{
  "hooks": {
    "PreToolUse": [...],
    "PostToolUse": [...],
    "Stop": [...],
    "Notification": [...]
  }
}
```

### 3. Validate Each Hook Entry
- [ ] `type` is "command"
- [ ] `command` path exists
- [ ] Script is executable

### 4. Validate Hook Scripts
- [ ] File exists and is executable
- [ ] Outputs valid JSON
- [ ] Has appropriate shebang

---

## Output Format

```markdown
## Hooks Validation Report

### Configuration Status: VALID / INVALID

### Configured Hooks
| Type | Matcher | Script | Status |
|------|---------|--------|--------|
| Stop | * | auto-loop-stop.sh | OK |

### Script Validation
| Script | Exists | Executable | Valid Output |
|--------|--------|------------|--------------|
| auto-loop-stop.sh | OK | OK | OK |

### Issues Found
1. [Issue and fix]
```

---

## Auto-Fix

- Make scripts executable
- Add missing shebang
- Create missing hook scripts
