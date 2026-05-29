---
name: governance
description: Toggle PAI governance enforcement on/off. Control chain-of-command routing and session-end requirements.
model_tier: haiku
parallel_hints:
  can_parallel_with: []
  must_serialize_with: [startup, startupO, session-end]
  preferred_batch_size: 1
context_hints:
  max_file_context: 20
  compression_level: 2
  requires_git_context: false
  requires_db_context: false
escalation_triggers:
  - pattern: "production|compliance"
    reason: "Governance changes for production/compliance require human approval"
---

# Governance Control Skill

> **Purpose:** Toggle governance enforcement without editing config files
> **Trigger:** `/governance [on|off|status]`
> **Config:** `.claude/Governance/config.json`

---

## Required Actions

When this skill is invoked, Claude MUST immediately execute the following based on arguments:

### Parse Arguments

Check the skill invocation arguments:
- No args or `status` → Show status (default)
- `on` → Enable all governance
- `off` → Disable all governance
- `chain on/off` → Toggle chain_of_command_enforcement
- `session on/off` → Toggle session_end_enforcement
- `bypass on/off` → Toggle bypass_allowed_for_single_file

---

### Action: Status Check (default)

**If no arguments or `status`**, read the config and display:

```bash
cat .claude/Governance/config.json
```

Then output this table with actual values:

```markdown
## Governance Status

| Setting | Status |
|---------|--------|
| governance_enabled | [✅ ON or ❌ OFF] |
| chain_of_command_enforcement | [✅ ON or ❌ OFF] |
| session_end_enforcement | [✅ ON or ❌ OFF] |
| bypass_allowed_for_single_file | [✅ ON or ❌ OFF] |
```

---

### Action: Toggle All (`on` or `off`)

**If argument is `on`**, update config:

```json
{
  "governance_enabled": true,
  "chain_of_command_enforcement": true,
  "session_end_enforcement": true,
  "bypass_allowed_for_single_file": true,
  "notes": "Set governance_enabled to false to disable all governance checks"
}
```

**If argument is `off`**, update config:

```json
{
  "governance_enabled": false,
  "chain_of_command_enforcement": false,
  "session_end_enforcement": false,
  "bypass_allowed_for_single_file": true,
  "notes": "Set governance_enabled to false to disable all governance checks"
}
```

After updating, confirm: "Governance [enabled/disabled]. All settings updated."

---

### Action: Toggle Specific Setting

**If argument is `chain on/off`**, update only `chain_of_command_enforcement`.
**If argument is `session on/off`**, update only `session_end_enforcement`.
**If argument is `bypass on/off`**, update only `bypass_allowed_for_single_file`.

After updating, show the full status table.

---

## Quick Reference

| Command | Effect |
|---------|--------|
| `/governance` | Show status |
| `/governance on` | Enable all |
| `/governance off` | Disable all |
| `/governance chain off` | Allow direct specialist spawning |
| `/governance session off` | Skip session-end checks |
| `/governance bypass off` | Require coordinator for ALL tasks |

---

## When to Disable

**Disable governance for:**
- Emergency P0 fixes (speed over process)
- Solo exploration sessions
- Quick prototyping

**Keep enabled for:**
- Production changes
- Multi-agent coordination
- Anything touching compliance/security

---

## Related

- `.claude/Governance/config.json` - Raw config file
- `.claude/Governance/HIERARCHY.md` - Chain of command
- `/session-end` - Session close-out (respects governance toggle)
- `/startupO` - Shows governance status at session start
