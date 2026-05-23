---
name: roblox-explorer
description: Efficient patterns for exploring Roblox instance trees using Lua eval. Use when you need to understand Roblox project structure, find instances, or trace data flow.
allowed-tools: Read, Glob, Grep
model: sonnet
---

# Roblox Instance Exploration

When using `roblox_eval` to explore instance trees, use these token-efficient patterns.

## Principles

1. **Return tables, not prints** - `return x` not `print(x)`
2. **Use short variable names** - `local r={}` not `local results={}`
3. **One-liners when possible** - Avoid verbose loops
4. **GetDescendants > recursive** - Built-in is faster
5. **GetFullName for paths** - Easy to trace back

---

## Quick Patterns

### List Children
```lua
-- Short: list names
return {game.Workspace:GetChildren()}

-- With class info
local r={}for _,v in game.Workspace:GetChildren()do r[v.Name]=v.ClassName end return r
```

### Find by Class
```lua
-- All scripts in game
local r={}for _,v in game:GetDescendants()do if v:IsA("Script")then r[#r+1]=v:GetFullName()end end return r

-- All RemoteEvents
local r={}for _,v in game:GetDescendants()do if v:IsA("RemoteEvent")then r[#r+1]=v:GetFullName()end end return r

-- Generic pattern
local r={}for _,v in game:GetDescendants()do if v:IsA("CLASS")then r[#r+1]=v:GetFullName()end end return r
```

### Find by Name Pattern
```lua
-- Contains "Spawn"
local r={}for _,v in game:GetDescendants()do if v.Name:find("Spawn")then r[#r+1]=v:GetFullName()end end return r

-- Starts with "NPC"
local r={}for _,v in game:GetDescendants()do if v.Name:sub(1,3)=="NPC"then r[#r+1]=v:GetFullName()end end return r
```

### Get Script Source
```lua
return game.ServerScriptService.GameManager.Source

-- First 500 chars (preview)
return game.ServerScriptService.GameManager.Source:sub(1,500)
```

### Get Properties
```lua
-- Specific properties
local p=workspace.SpawnPoint return{Pos=p.Position,Size=p.Size,Anchored=p.Anchored}

-- All attributes
return workspace.SpawnPoint:GetAttributes()

-- All tags
local CS=game:GetService("CollectionService")return CS:GetTags(workspace.SpawnPoint)
```

### Tree Structure (Depth Limited)
```lua
-- 2-level tree
local function t(i,d)if d<1 then return"..."end local r={}for _,c in i:GetChildren()do r[c.Name.."("..c.ClassName..")"]=t(c,d-1)end return r end return t(game.ReplicatedStorage,2)
```

---

## Search Patterns

### Grep in Scripts
```lua
-- Find "FireServer" in all scripts
local r={}for _,v in game:GetDescendants()do
if v:IsA("LuaSourceContainer")and v.Source:find("FireServer")then
r[#r+1]=v:GetFullName()end end return r
```

### Find References to Module
```lua
-- Who requires "Utilities"?
local r={}for _,v in game:GetDescendants()do
if v:IsA("LuaSourceContainer")and v.Source:find('require.-Utilities')then
r[#r+1]=v:GetFullName()end end return r
```

### Find RemoteEvent Handlers
```lua
-- Find OnServerEvent connections
local r={}for _,v in game:GetDescendants()do
if v:IsA("Script")and v.Source:find("OnServerEvent")then
r[#r+1]=v:GetFullName()end end return r
```

---

## Service Shortcuts

```lua
local WS=game.Workspace
local SSS=game:GetService("ServerScriptService")
local SS=game:GetService("ServerStorage")
local RS=game:GetService("ReplicatedStorage")
local SP=game:GetService("StarterPlayer")
local SG=game:GetService("StarterGui")
local PS=game:GetService("Players")
```

---

## Output Formats

### Compact List
```lua
return table.concat(results, "\n")
```

### Name → Class Map
```lua
local r={}for _,v in parent:GetChildren()do r[v.Name]=v.ClassName end return r
```

### Path List
```lua
-- GetFullName() gives "Workspace.Map.Building.Part"
r[#r+1]=v:GetFullName()
```

### Count Only
```lua
local n=0 for _,v in game:GetDescendants()do if v:IsA("Part")then n=n+1 end end return n
```

---

## Exploration Strategy

1. **Start broad** - List services, count descendants
   ```lua
   local r={}for _,s in{"Workspace","ServerScriptService","ReplicatedStorage","ServerStorage"}do
   r[s]=#game:GetService(s):GetDescendants()end return r
   ```

2. **Narrow down** - Find entry points
   ```lua
   -- Server scripts (entry points)
   local r={}for _,v in game.ServerScriptService:GetDescendants()do
   if v:IsA("Script")then r[#r+1]=v:GetFullName()end end return r
   ```

3. **Trace connections** - Find RemoteEvents, requires
   ```lua
   -- What remotes exist?
   local r={}for _,v in game.ReplicatedStorage:GetDescendants()do
   if v:IsA("RemoteEvent")or v:IsA("RemoteFunction")then r[#r+1]=v.Name end end return r
   ```

4. **Read specific scripts** - Once you know what to look at
   ```lua
   return game.ServerScriptService.GameManager.Source
   ```

---

## Common Mistakes

### Too Verbose
```lua
-- BAD: 50+ tokens
local results = {}
for _, instance in ipairs(game:GetDescendants()) do
    if instance:IsA("Script") then
        table.insert(results, instance:GetFullName())
    end
end
return results

-- GOOD: 25 tokens
local r={}for _,v in game:GetDescendants()do if v:IsA("Script")then r[#r+1]=v:GetFullName()end end return r
```

### Forgetting Return
```lua
-- BAD: prints to Studio console, returns nil
for _,v in game:GetChildren()do print(v.Name)end

-- GOOD: returns data
return {game:GetChildren()}
```

### Too Deep Recursion
```lua
-- BAD: manual recursion (slow, can stackoverflow)
local function recurse(i)...recurse(c)...end

-- GOOD: use built-in
game:GetDescendants()  -- already recursive
```
