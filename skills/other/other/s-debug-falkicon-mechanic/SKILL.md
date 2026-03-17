---
name: s-debug
description: >
  Diagnose and fix bugs using evidence-based investigation. Requires runtime
  evidence before fixes—never guess based on code alone. Covers hypothesis-driven
  debugging, instrumentation logging, Lua errors, taint issues, combat lockdown,
  and API failures. Triggers: error, bug, debug, fix, crash, taint, nil value,
  diagnose, hypothesis, runtime, evidence, instrumentation.
---

# Debugging WoW Addons

Systematic debugging and error recovery for WoW addons.

## Related Commands

- [c-debug](../../commands/c-debug.md) - Reload loop workflow for finding and fixing issues
- [c-review](../../commands/c-review.md) - Full code review (includes debug step)

## MCP Tools (Use These First)

> **MANDATORY**: ALWAYS use MCP tools directly instead of the shell.

| Task | MCP Tool |
|------|----------|
| Get All Output | `addon.output(agent_mode=true)` |
| Lint Addon | `addon.lint(addon="MyAddon")` |
| Scan Deprecations | `addon.deprecations(addon="MyAddon")` |
| Queue Lua Eval | `lua.queue(code=["GetMoney()"])` |
| Get Eval Results | `lua.results()` |

## Capabilities

1. **Evidence-Based Debugging** — Hypothesis-driven investigation with runtime instrumentation and log proof
2. **Error Analysis** — Parse Lua errors, identify root cause in stack traces
3. **Taint Investigation** — Track secure/insecure code interaction and "Action blocked" issues
4. **Combat Issues** — Debug lockdown-related failures and protected frame issues
5. **API Failures** — Handle deprecated or changed APIs (Midnight 12.0 prep)

## Routing Logic

| Request type | Load reference |
|--------------|----------------|
| Evidence-based debugging, hypothesis-driven | [references/evidence-based-debugging.md](references/evidence-based-debugging.md) |
| Lua errors, nil values | [references/error-patterns.md](references/error-patterns.md) |
| Debug workflow, isolation | [references/debugging-strategies.md](references/debugging-strategies.md) |
| Error tracking (BugGrabber) | [../../docs/integration/errors.md](../../docs/integration/errors.md) |
| Troubleshooting guide | [../../docs/integration/troubleshooting.md](../../docs/integration/troubleshooting.md) |
| Structured logging | [../../docs/integration/console.md](../../docs/integration/console.md) |
| Frame inspection | [../../docs/integration/inspect.md](../../docs/integration/inspect.md) |

## Debug Output Best Practice

> **CRITICAL**: Use `MechanicLib:Log()` instead of `print()` for all debug output.

| Feature | `print()` | `MechanicLib:Log()` |
|---------|-----------|---------------------|
| Agent access | ❌ Requires screenshot | ✅ `addon.output` retrieves directly |
| Filtering | ❌ None | ✅ Source + category filters |
| Copyable | ❌ No | ✅ Yes, via Console export |

```lua
-- ✅ Correct: Agent can see this in addon.output
local MechanicLib = LibStub("MechanicLib-1.0", true)
if MechanicLib then
    MechanicLib:Log("MyAddon", "Debug: value=" .. tostring(val), MechanicLib.Categories.CORE)
end

-- ❌ Avoid: Spams chat, requires screenshot
print("[MyAddon] Debug: value=" .. tostring(val))
```

## Quick Reference

### Get Addon Data (Compressed for AI)

**Ask** user to `/reload` and confirm, then:

```bash
addon.output(agent_mode=true)
```

### Common Error Patterns
- `attempt to index nil value`: API returned nil, check if unit exists or data is loaded.
- `Action blocked by Blizzard`: You tried to call a protected function in combat.
- `Interface action failed`: Taint has spread to a secure UI component.

### Systematic Workflow
1. **Gather Evidence**: **Ask** user to `/reload`, wait for confirmation, then `addon.output(agent_mode=true)`
2. **Isolate**: Can you reproduce with minimal code?
3. **Hypothesis**: "If X then Y because Z"
4. **Fix & Validate**: Apply minimal fix, **ask** user to `/reload` and confirm, then verify with `addon.output`.
