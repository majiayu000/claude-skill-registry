---
name: roblox-code-reviewer
description: Reviews Roblox Luau code for correctness, modern patterns, security, and performance. Understands event-driven architecture, client/server boundaries, and script organization. Use after writing Roblox code to catch issues before shipping.
allowed-tools: Read, Glob, Grep
model: sonnet
---

# Roblox Code Reviewer

A comprehensive code review skill for Roblox game development. Reviews code for:
- **Testability in Run mode** (CRITICAL for AI agent feedback loops)
- Event-driven architecture correctness
- Client/server boundary violations
- Script organization issues
- Deprecated API usage
- Performance anti-patterns
- Security vulnerabilities

## How to Use

After code is written, review against the checklists in the reference files:
1. **`testability.md` - Run mode testability (CHECK FIRST)**
2. `event-architecture.md` - Connection lifecycle, event ordering, cleanup
3. `client-server.md` - What runs where, security boundaries
4. `script-organization.md` - Where scripts should live
5. `deprecated-patterns.md` - Old APIs and modern replacements
6. `performance.md` - Common performance mistakes
7. `security.md` - Exploit prevention patterns

For each issue found:
1. Quote the problematic code with file:line reference
2. Explain the issue briefly
3. Provide the correct pattern

---

## Quick Reference: Critical Checks

### Testability (HIGHEST PRIORITY)

**AI agents cannot enter Play mode.** Code must be testable in Run mode (server-only, no player).

```lua
-- BAD: Untestable - logic buried in event handlers
Players.PlayerAdded:Connect(function(player)
    player.CharacterAdded:Connect(function(character)
        -- 500 lines of logic that can't be called directly
    end)
end)

-- GOOD: Testable - pure logic in ReplicatedStorage modules
-- ReplicatedStorage/Modules/Combat.lua
local Combat = {}
function Combat.calculateDamage(attackerStats, defenderStats, weapon)
    return math.floor(weapon.damage * (1 + attackerStats.strength / 100))
end
function Combat._reset() end  -- For test isolation
return Combat

-- EVAL TEST (loadstring via plugin):
-- [[
-- local C = require(game.ReplicatedStorage.Modules.Combat)
-- return C.calculateDamage({strength=50}, {}, {damage=100})
-- ]]
-- Returns: 150
```

**Architecture rules:**
- ModuleScripts in ReplicatedStorage unless they need server-only services
- Pure logic separated from network transport
- Use Network Bridge pattern for Remote/Bindable abstraction
- Test modules can simulate client→server via BindableEvents

```lua
-- Network Bridge: same API, swappable transport
-- Test mode: BindableEvent | Production: RemoteEvent
local Bridge = require(ReplicatedStorage.Network.Bridge)
Bridge.setTestMode(true)  -- Enable for testing
local channel = Bridge.createChannel("Combat")
channel:_testFireServer(mockPlayer, data)  -- Simulate client call
```

**See testability.md for full Bridge pattern and test runner.**

### Event-Driven Architecture (Roblox Core Pattern)

Roblox is fundamentally event-driven. Every review must check:

```lua
-- CRITICAL: Store connections for cleanup
local connection = part.Touched:Connect(callback)
-- Later: connection:Disconnect()

-- CRITICAL: Parent LAST (events fire on parenting)
local part = Instance.new("Part")
part.Size = Vector3.new(5, 5, 5)  -- Configure first
part.Parent = workspace           -- Parent last

-- CRITICAL: Use task library, not deprecated globals
task.spawn(fn)   -- not spawn()
task.wait(1)     -- not wait()
task.delay(1, fn) -- not delay()
```

### Client vs Server

| Must be SERVER | Should be CLIENT |
|----------------|------------------|
| DataStore access | UI/Camera |
| Currency/inventory changes | Input handling |
| Damage calculation | Visual effects |
| Game state authority | Client prediction |
| Hit validation | Animation playback |

### Script Placement

| Location | Purpose |
|----------|---------|
| ServerScriptService | Server-only scripts |
| ServerStorage | Server-only modules/data |
| ReplicatedStorage | Shared ModuleScripts |
| StarterPlayerScripts | Persistent client scripts |
| StarterCharacterScripts | Per-spawn client scripts |

### Top 10 Code Smells

1. `Instance.new("Part", workspace)` - Parent as 2nd arg
2. `wait()` / `spawn()` / `delay()` - Use task library
3. `FindFirstChild()` in Heartbeat - Cache references
4. `.Touched:Connect()` without disconnect - Memory leak
5. `RemoteEvent` without type validation - Security hole
6. Client calculating damage - Server authority violation
7. `Velocity` property - Use `AssemblyLinearVelocity`
8. Manual character construction - Use HumanoidDescription
9. Tables created every frame - GC pressure
10. No WaitForChild timeout - Can hang forever

---

## Review Process

### Step 0: Testability Check (FIRST)
- Can core logic be tested via eval (loadstring) in Run mode?
- Do functions return results (not just print)?
- Is state queryable without a player?
- Is logic in callable functions (not buried in event handlers)?
- Is Network Bridge pattern used for Remote/Bindable abstraction?

### Step 1: Architecture Check
- Is code in correct location (server vs client)?
- Are connections properly managed?
- Is parent set last for Instance.new()?

### Step 2: Security Check
- Are RemoteEvent args validated?
- Is critical logic server-side?
- Are there rate limits?

### Step 3: Performance Check
- Any allocations in hot loops?
- Are references cached?
- Any deprecated APIs?

### Step 4: Modern Patterns Check
- Using task library?
- Using constraint physics?
- Using HumanoidDescription for NPCs?

### Step 5: Client Verification (Human-in-the-loop)
After server tests pass:
1. Static analyze client code for errors (server-only services, wrong patterns)
2. Generate Play mode test checklist
3. Prompt user: "Please enter Play mode and verify: [checklist]"
4. Incorporate user feedback, fix issues

See reference files for detailed patterns.
