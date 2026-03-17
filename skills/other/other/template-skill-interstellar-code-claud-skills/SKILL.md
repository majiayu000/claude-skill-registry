---
name: template-skill
description: Replace with description of the skill and when Claude should use it.
---

# Insert instructions below

## 🎨 **VISUAL OUTPUT FORMATTING**

**CRITICAL: All template-skill output MUST use the colored-output formatter skill!**

### Use Colored-Output Skill

**IMPORTANT: Use MINIMAL colored output (2-3 calls max) to prevent screen flickering!**

**Example formatted output (MINIMAL PATTERN):**
```bash
# START: Header only
bash .claude/skills/colored-output/color.sh skill-header "YOUR-SKILL-NAME" "Starting task..."

# MIDDLE: Regular text (no colored calls)
Processing data...
Performing operations...

# END: Result only
bash .claude/skills/colored-output/color.sh success "" "Task completed"
```

**WHY:** Each bash call creates a task in Claude CLI, causing screen flickering. Keep it minimal!

---
