# Evolve: Add Skill - Enable Auto-Discovery

**Command:** `/evolve:add-skill {command} [trigger-phrases]`
**Version:** 1.0.0
**Purpose:** Add auto-discovery skill to an existing command, enabling Claude to automatically suggest it based on conversation context.

---

## What This Command Does

Transforms a manual-only command into an auto-discoverable command by creating a skill with trigger phrases. After this evolution, Claude will automatically suggest the command when users mention related topics.

---

## Usage

```bash
# Auto-generate trigger phrases
/evolve:add-skill pm:next

# Provide custom trigger phrases
/evolve:add-skill pm:next "what should I work on, next task, show next"

# Dry run (preview only)
/evolve:add-skill pm:next --dry-run
```

---

## Arguments

```javascript
const command = ARGUMENTS[0] // Format: namespace:operation (e.g., "pm:next")
const triggerPhrasesArg = ARGUMENTS.slice(1).join(" ") // Optional comma-separated phrases
const dryRun = ARGUMENTS.includes("--dry-run")
```

---

## Implementation

Execute the evolution using the EvolveManager:

```javascript
const { EvolveManager } = require("./.claude/lib/evolve")
const evolve = new EvolveManager()

// Parse trigger phrases if provided
let triggerPhrases = undefined
if (triggerPhrasesArg && triggerPhrasesArg !== "--dry-run") {
  triggerPhrases = triggerPhrasesArg
    .split(",")
    .map((p) => p.trim())
    .filter((p) => p.length > 0)
}

// Execute evolution
try {
  evolve.addSkill(command, triggerPhrases, { dryRun })
} catch (error) {
  console.error("❌ Evolution failed:", error.message)
  process.exit(1)
}
```

---

## Example Output

```
✨ Adding auto-discovery skill to /pm:next

📋 Trigger Phrases (6):
  ✓ "what should I work on"
  ✓ "next task"
  ✓ "show next"
  ✓ "what's next"
  ✓ "get next task"
  ✓ "next pm task"

✅ Skill added to /pm:next

📂 Created: .claude/skills/pm-next-discovery/SKILL.md
📝 Updated: .claude/commands/pm/next.md (added skill_id)

Undo anytime:
  /evolve:remove-skill pm:next
```

---

## What Gets Created

1. **Skill Directory**: `.claude/skills/{namespace}-{operation}-discovery/`
2. **Skill File**: `.claude/skills/{namespace}-{operation}-discovery/SKILL.md`
3. **Evolution Record**: `.claude/history/{command}.evolution.json`
4. **Updated Command**: Command file updated with skill metadata

---

## Validation

The command will validate:

- ✅ Command exists
- ✅ Skill doesn't already exist
- ✅ Trigger phrases don't conflict with existing skills
- ✅ Command format is valid (namespace:operation)

---

## Error Handling

**Command not found:**

```
❌ Command not found: .claude/commands/pm/next.md
Make sure the command exists before adding a skill.
```

**Skill already exists:**

```
❌ Skill already exists for /pm:next
Remove it first: /evolve:remove-skill pm:next
```

**Invalid format:**

```
❌ Invalid command format. Use: namespace:operation
Example: /evolve:add-skill pm:next
```

---

## Before & After

**Before (Manual Only):**

```
User: "What should I work on?"
Claude: "I don't have access to your task list."
User: "/pm:next"
Claude: [executes command]
```

**After (Auto-Discovery):**

```
User: "What should I work on?"
Claude: "Let me check... [automatically suggests /pm:next]"
[executes and shows result]
```

---

## Related Commands

- **Remove Skill:** `/evolve:remove-skill {command}` - Undo this evolution
- **Package Plugin:** `/evolve:to-plugin {domain}` - Package with skill included
- **Test Command:** `/test:command {command}` - Validate evolution worked
- **Rollback:** `/evolve:rollback {command}` - Revert to previous version

---

## Notes

- Non-breaking change: Command still works manually
- Reversible: Use `/evolve:remove-skill` to undo
- History tracked: Evolution recorded in `.claude/history/`
- Quality: Improves user experience through auto-discovery

---

**Status:** Ready for Use
**Library:** Backed by EvolveManager.addSkill() in `.claude/lib/evolve.ts`
