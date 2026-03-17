---
name: SND Saucy Integration
description: Use this skill when working with the Saucy plugin. Covers Gold Saucer mini-game automation (Cuff-a-cur, Triple Triad).
---

# Saucy Integration for SND

This skill covers integration with the Saucy plugin for Gold Saucer mini-game automation.

> **Source:** https://github.com/PunishXIV/Saucy
>
> **Status:** Verified - Saucy has NO IPC API

## CRITICAL INFORMATION

**Saucy does NOT expose any IPC API for external control.**

After reviewing the official Saucy repository source code:
- No IPC providers found
- No CallGate registrations
- No public API surface for inter-plugin communication
- Only user-facing interface is the `/saucy` command

### What Saucy Actually Does

Saucy is a **Gold Saucer mini-game automation plugin**, NOT a fishing plugin.

**Supported Games:**
- **Cuff-a-cur** - Mini-game automation
- **Triple Triad** - Card game automation

**Source Code Analysis:**
- Repository: https://github.com/PunishXIV/Saucy
- Main plugin file: `Saucy/Saucy.cs` - No IPC exports
- Global config: `Saucy/Global.cs` - No CallGate setup
- Framework: Modular architecture via `IModule` interface

## Integration from SND Macros

Since Saucy has no IPC API, you **cannot** control it programmatically from SND Lua scripts.

### Available Control Methods

**1. User Command Only**
```lua
-- The only way to interact with Saucy
yield("/saucy")  -- Opens the Saucy UI
```

**2. Plugin Detection**
```lua
-- Check if Saucy is installed
if not HasPlugin("Saucy") then
    yield("/echo [Script] Saucy plugin not available")
    StopFlag = true
    return
end
```

### What You CANNOT Do

Since there is no IPC API, you cannot:
- Start/stop mini-game automation programmatically
- Check if Saucy is currently running
- Configure Saucy settings from Lua
- Query mini-game state or results
- Trigger specific game automation

### Recommended Alternatives for Automation

If you need **fishing automation** (which Saucy does NOT provide), consider:

**AutoHook Plugin** - Ocean fishing automation
- Repository: https://github.com/InitialDet/AutoHook
- Used in ocean fishing scripts (see `Reference/FishingRaid_original.lua`)
- Provides actual fishing automation

**For Gold Saucer automation**, Saucy must be:
- Configured manually via `/saucy` command
- Started by the user through the plugin UI
- Cannot be controlled from SND macros

## Common Misconceptions

### ❌ INCORRECT Documentation (Previously in this skill)
```lua
-- THESE DO NOT EXIST - Saucy has no IPC API
IPC.Saucy.IsRunning()      -- DOES NOT EXIST
IPC.Saucy.StartFishing()   -- DOES NOT EXIST
IPC.Saucy.StopFishing()    -- DOES NOT EXIST
```

### ✅ CORRECT Usage
```lua
-- Only valid interaction with Saucy from SND
if HasPlugin("Saucy") then
    yield("/echo [Script] Saucy is available")
    yield("/echo [Script] Use /saucy command to configure")
end
```

## Workflow Integration

Since Saucy cannot be controlled from macros, workflows requiring Gold Saucer mini-games must:

1. **Manual Setup**: User configures Saucy via `/saucy` UI
2. **Manual Start**: User starts mini-game automation manually
3. **Script Waits**: SND macro can wait for user confirmation
4. **No Automation**: Cannot automate mini-game start/stop

### Example: Waiting for Manual Saucy Completion
```lua
-- Script acknowledges Saucy exists but cannot control it
if HasPlugin("Saucy") then
    yield("/echo [Script] Please start Saucy manually with /saucy")
    yield("/echo [Script] Type 'continue' in chat when done")

    -- Wait for user confirmation (manual pattern)
    -- Note: This requires custom chat monitoring implementation
end
```

## Summary

- **Saucy**: Gold Saucer mini-game plugin (Cuff-a-cur, Triple Triad)
- **No IPC API**: Cannot be controlled from SND Lua scripts
- **Manual Only**: Configuration and start via `/saucy` command
- **Not for Fishing**: Use AutoHook for fishing automation
- **Source Verified**: Confirmed by reviewing official repository

## See Also

For actual fishing automation, see:
- **AutoHook plugin** - Ocean fishing automation
- `Reference/FishingRaid_original.lua` - Example ocean fishing script

For other Gold Saucer features:
- Check for future Saucy updates that may add IPC
- Consider alternative plugins with IPC support
