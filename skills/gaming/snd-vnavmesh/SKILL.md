---
name: SND vnavmesh Integration
description: Use this skill when implementing navigation or movement in SND macros using the vnavmesh plugin. Covers pathfinding, movement control, navmesh utilities, and movement patterns.
---

# vnavmesh Integration for SND

This skill covers integration with the vnavmesh plugin for navigation and movement in SND macros.

> **Source:** Verified from https://github.com/awgil/ffxiv_navmesh/blob/master/vnavmesh/IPCProvider.cs (Last verified: 2025-12-11)

## Prerequisites

```lua
-- Always check plugin availability first
if not HasPlugin("vnavmesh") then
    yield("/echo [Script] vnavmesh plugin not available")
    StopFlag = true
    return
end

-- Check if vnavmesh is ready
if not IPC.vnavmesh.Nav.IsReady() then
    yield("/echo [Script] vnavmesh is not ready")
    StopFlag = true
    return
end
```

## Complete API Reference (Official)

All IPC calls use the prefix `vnavmesh.` internally. In SND Lua, access via `IPC.vnavmesh.*`.

### Nav Functions (Navmesh Management)
```lua
-- Check if navmesh is loaded and ready
IPC.vnavmesh.Nav.IsReady() → boolean

-- Get navmesh build progress (0.0 to 1.0)
IPC.vnavmesh.Nav.BuildProgress() → number

-- Reload navmesh (uses cached data if available)
IPC.vnavmesh.Nav.Reload() → nil

-- Rebuild navmesh (forces full rebuild, ignores cache)
IPC.vnavmesh.Nav.Rebuild() → nil

-- Pathfind from one point to another (returns path waypoints)
IPC.vnavmesh.Nav.Pathfind(Vector3 from, Vector3 to, boolean fly) → List<Vector3>

-- Pathfind with tolerance/range
IPC.vnavmesh.Nav.PathfindWithTolerance(Vector3 from, Vector3 to, boolean fly, number range) → List<Vector3>

-- Pathfind with cancellation token (advanced)
IPC.vnavmesh.Nav.PathfindCancelable(Vector3 from, Vector3 to, boolean fly, CancellationToken cancel) → List<Vector3>

-- Cancel all pathfinding operations (calls Reload internally)
IPC.vnavmesh.Nav.PathfindCancelAll() → nil

-- Check if any pathfinding is in progress
IPC.vnavmesh.Nav.PathfindInProgress() → boolean

-- Get number of queued pathfind requests
IPC.vnavmesh.Nav.PathfindNumQueued() → number

-- Get/Set auto-load navmesh setting
IPC.vnavmesh.Nav.IsAutoLoad() → boolean
IPC.vnavmesh.Nav.SetAutoLoad(boolean enabled) → nil

-- Build bitmap of navmesh (for debugging/visualization)
IPC.vnavmesh.Nav.BuildBitmap(Vector3 startingPos, string filename, number pixelSize) → boolean
IPC.vnavmesh.Nav.BuildBitmapBounded(Vector3 startingPos, string filename, number pixelSize, Vector3 minBounds, Vector3 maxBounds) → boolean
```

### Query Functions (Mesh Queries)
```lua
-- Get nearest point on navmesh
IPC.vnavmesh.Query.Mesh.NearestPoint(Vector3 p, number halfExtentXZ, number halfExtentY) → Vector3?

-- Get point on floor
-- NOTE: allowUnlandable parameter is present but currently unused in the implementation
IPC.vnavmesh.Query.Mesh.PointOnFloor(Vector3 p, boolean allowUnlandable, number halfExtentXZ) → Vector3?
```

### Path Functions (Movement Control)
```lua
-- Move along waypoints
-- IMPORTANT: The 'fly' parameter is INVERTED internally (!fly)
-- Pass true to walk/run, false to fly
IPC.vnavmesh.Path.MoveTo(List<Vector3> waypoints, boolean fly) → nil

-- Stop current movement
IPC.vnavmesh.Path.Stop() → nil

-- Check if path following is active
IPC.vnavmesh.Path.IsRunning() → boolean

-- Get number of remaining waypoints
IPC.vnavmesh.Path.NumWaypoints() → number

-- Get list of remaining waypoints
IPC.vnavmesh.Path.ListWaypoints() → List<Vector3>

-- Get/Set whether movement is allowed
IPC.vnavmesh.Path.GetMovementAllowed() → boolean
IPC.vnavmesh.Path.SetMovementAllowed(boolean allowed) → nil

-- Get/Set camera alignment to movement
IPC.vnavmesh.Path.GetAlignCamera() → boolean
IPC.vnavmesh.Path.SetAlignCamera(boolean align) → nil

-- Get/Set tolerance for reaching waypoints
IPC.vnavmesh.Path.GetTolerance() → number
IPC.vnavmesh.Path.SetTolerance(number tolerance) → nil
```

### SimpleMove Functions (High-Level Movement)
```lua
-- Pathfind and move to destination (most commonly used)
IPC.vnavmesh.SimpleMove.PathfindAndMoveTo(Vector3 dest, boolean fly) → boolean

-- Pathfind and move close to destination (within range)
IPC.vnavmesh.SimpleMove.PathfindAndMoveCloseTo(Vector3 dest, boolean fly, number range) → boolean

-- Check if SimpleMove pathfinding is in progress
IPC.vnavmesh.SimpleMove.PathfindInProgress() → boolean
```

### Window Functions
```lua
-- Get/Set vnavmesh window visibility
IPC.vnavmesh.Window.IsOpen() → boolean
IPC.vnavmesh.Window.SetOpen(boolean open) → nil
```

### DTR Functions (Server Info Bar)
```lua
-- Get/Set DTR entry visibility
IPC.vnavmesh.DTR.IsShown() → boolean
IPC.vnavmesh.DTR.SetShown(boolean shown) → nil
```

## Legacy API Mapping

Some older scripts may use simplified function names. Here's the mapping:

```lua
-- Legacy                           → Official
IPC.vnavmesh.IsReady()             → IPC.vnavmesh.Nav.IsReady()
IPC.vnavmesh.BuildProgress()       → IPC.vnavmesh.Nav.BuildProgress()
IPC.vnavmesh.Reload()              → IPC.vnavmesh.Nav.Reload()
IPC.vnavmesh.Rebuild()             → IPC.vnavmesh.Nav.Rebuild()
IPC.vnavmesh.PathfindAndMoveTo()   → IPC.vnavmesh.SimpleMove.PathfindAndMoveTo()
IPC.vnavmesh.PathfindInProgress()  → IPC.vnavmesh.SimpleMove.PathfindInProgress()
IPC.vnavmesh.Stop()                → IPC.vnavmesh.Path.Stop()
IPC.vnavmesh.IsRunning()           → IPC.vnavmesh.Path.IsRunning()
```

## Helper Functions

### vnavmesh Status Checking
```lua
function IsVnavmeshReady()
    return HasPlugin("vnavmesh") and IPC.vnavmesh.Nav.IsReady()
end

function IsVnavmeshRunning()
    return IPC.vnavmesh.Path.IsRunning() or IPC.vnavmesh.SimpleMove.PathfindInProgress()
end

function GetVnavmeshBuildProgress()
    if not IsVnavmeshReady() then
        return 0.0
    end
    return IPC.vnavmesh.Nav.BuildProgress()
end
```

### Reload and Rebuild
```lua
function ReloadVnavmesh()
    if not HasPlugin("vnavmesh") then
        yield("/echo [Script] vnavmesh plugin not available")
        return false
    end

    IPC.vnavmesh.Nav.Reload()
    yield("/echo [Script] vnavmesh reloaded")
    return true
end

function RebuildVnavmesh()
    if not HasPlugin("vnavmesh") then
        yield("/echo [Script] vnavmesh plugin not available")
        return false
    end

    IPC.vnavmesh.Nav.Rebuild()
    yield("/echo [Script] vnavmesh rebuild started")
    return true
end
```

### Safe VNAV Calls (with pcall)

```lua
--- Safely call vnavmesh methods with error handling
-- @param method function - The vnavmesh method to call
-- @param ... any - Arguments to pass
-- @return boolean, any - Success status and result/nil
local function _safe_vnav(method, ...)
    local ok, res = pcall(method, ...)
    if not ok then
        Log("VNAV error: %s", tostring(res))
        return false, nil
    end
    return true, res
end

--- Wait for vnavmesh to be ready with timeout
-- @param timeout number - Maximum wait time (default: TIME.TIMEOUT)
-- @return boolean - True if ready
function WaitVnavReady(timeout)
    return WaitUntil(function()
        local ok, res = _safe_vnav(IPC.vnavmesh.Nav.IsReady)
        return ok and res
    end, timeout or TIME.TIMEOUT, TIME.POLL, 0.0)
end

--- Start pathfinding with safety checks
-- @param dest Vector3 - Destination position
-- @param fly boolean - Whether to fly (default: false)
-- @return boolean - True if pathfinding started
function PathandMoveVnav(dest, fly)
    fly = (fly == true)

    if not WaitVnavReady(TIME.TIMEOUT) then
        Log("VNAV not ready (timeout)")
        return false
    end

    local okMove, moveRes = _safe_vnav(IPC.vnavmesh.SimpleMove.PathfindAndMoveTo, dest, fly)
    if not okMove or not moveRes then
        Log("VNAV pathfind failed")
        return false
    end
    return true
end

--- Stop when close to destination
-- @param dest Vector3 - Destination position
-- @param stopDistance number - Distance to stop at (default: 3.0)
-- @return boolean - True if stopped successfully
function StopCloseVnav(dest, stopDistance)
    if not (dest and dest.X and dest.Y and dest.Z) then
        Log("StopCloseVnav: invalid destination")
        return false
    end
    stopDistance = toNumberSafe(stopDistance, 3.0, 0.01)

    -- Wait for movement to start
    local okRun = WaitUntil(function()
        local ok, res = _safe_vnav(IPC.vnavmesh.Path.IsRunning)
        return ok and res
    end, TIME.TIMEOUT, TIME.POLL, 0.0)

    if not okRun then
        Log("VNAV not running (timeout)")
        return false
    end

    -- Monitor until close enough or stopped
    while true do
        local okRunLoop, running = _safe_vnav(IPC.vnavmesh.Path.IsRunning)
        if not okRunLoop then return false end
        if not running then return true end

        local pos = Entity and Entity.Player and Entity.Player.Position
        if pos and IsWithinDistance(pos, dest, stopDistance) then
            _safe_vnav(IPC.vnavmesh.Path.Stop)
            return true
        end
        Sleep(TIME.POLL)
    end
end

--- Move near a destination and stop at specified distance
-- @param dest Vector3 - Destination position
-- @param stopDistance number - Distance to stop at (default: 3.0)
-- @param fly boolean - Whether to fly (default: false)
-- @return boolean - True if successfully reached near destination
function MoveNearVnav(dest, stopDistance, fly)
    stopDistance = toNumberSafe(stopDistance, 3.0, 0.01)
    if not PathandMoveVnav(dest, fly) then return false end
    return StopCloseVnav(dest, stopDistance) == true
end
```

## Movement Patterns

### Basic Movement
```lua
-- Move to position
if not IPC.vnavmesh.SimpleMove.PathfindInProgress() and not IPC.vnavmesh.Path.IsRunning() then
    IPC.vnavmesh.SimpleMove.PathfindAndMoveTo(Vector3(x, y, z), false)
end

-- Wait for movement completion
while IPC.vnavmesh.Path.IsRunning() or IPC.vnavmesh.SimpleMove.PathfindInProgress() do
    yield("/wait 1")
end

-- Stop movement if needed
IPC.vnavmesh.Path.Stop()
```

### Movement with Timeout
```lua
function MoveToPositionWithTimeout(x, y, z, timeout)
    timeout = timeout or 30

    if not HasPlugin("vnavmesh") then
        yield("/echo [Script] vnavmesh not available")
        return false
    end

    if not IPC.vnavmesh.SimpleMove.PathfindInProgress() and not IPC.vnavmesh.Path.IsRunning() then
        IPC.vnavmesh.SimpleMove.PathfindAndMoveTo(Vector3(x, y, z), false)
    end

    local startTime = os.clock()
    while (IPC.vnavmesh.Path.IsRunning() or IPC.vnavmesh.SimpleMove.PathfindInProgress()) and
          (os.clock() - startTime) < timeout do
        yield("/wait 1")
    end

    if IPC.vnavmesh.Path.IsRunning() then
        yield("/echo [Script] Movement timeout, stopping")
        IPC.vnavmesh.Path.Stop()
        return false
    end

    return true
end
```

### Movement Near Position (With Tolerance)
```lua
function MoveNearPosition(x, y, z, tolerance, timeout)
    tolerance = tolerance or 3.0
    timeout = timeout or 30

    if IsAtPosition(x, y, z, tolerance) then
        return true
    end

    return MoveToPositionWithTimeout(x, y, z, timeout)
end

function IsAtPosition(targetX, targetY, targetZ, tolerance)
    tolerance = tolerance or 2.0
    local playerPos = Player.Position
    local dx = targetX - playerPos.X
    local dy = targetY - playerPos.Y
    local dz = targetZ - playerPos.Z
    local distance = math.sqrt(dx * dx + dy * dy + dz * dz)
    return distance <= tolerance
end
```

### Movement with Retry
```lua
function MoveWithRetry(x, y, z, maxRetries)
    maxRetries = maxRetries or 3

    for attempt = 1, maxRetries do
        if MoveToPositionWithTimeout(x, y, z, 30) then
            return true
        end

        if attempt < maxRetries then
            yield("/echo [Script] Movement attempt " .. attempt .. " failed, retrying")
            yield("/wait 2")
        end
    end

    yield("/echo [Script] Movement failed after " .. maxRetries .. " attempts")
    return false
end
```

### Wait for vnavmesh Stop
```lua
function WaitForVnavmeshStop(timeout)
    timeout = timeout or 30
    local startTime = os.clock()

    while IsVnavmeshRunning() and (os.clock() - startTime) < timeout do
        yield("/wait 1")
    end

    if IsVnavmeshRunning() then
        yield("/echo [Script] vnavmesh timeout, forcing stop")
        IPC.vnavmesh.Stop()
        return false
    end

    return true
end
```

## Advanced Patterns

### Safe Movement Function
```lua
function SafeMoveToPosition(x, y, z, timeout)
    timeout = timeout or 30

    -- Check prerequisites
    if not HasPlugin("vnavmesh") then
        yield("/echo [Script] ERROR: vnavmesh plugin not available")
        return false
    end

    if not Player.Available then
        yield("/echo [Script] ERROR: Player not available")
        return false
    end

    -- Check if already at destination
    if IsAtPosition(x, y, z, 2.0) then
        yield("/echo [Script] Already at destination")
        return true
    end

    -- Start movement
    if not IPC.vnavmesh.SimpleMove.PathfindInProgress() and not IPC.vnavmesh.Path.IsRunning() then
        IPC.vnavmesh.SimpleMove.PathfindAndMoveTo(Vector3(x, y, z), false)
    end

    -- Wait for completion with timeout
    local startTime = os.clock()
    while (IPC.vnavmesh.Path.IsRunning() or IPC.vnavmesh.SimpleMove.PathfindInProgress()) and
          (os.clock() - startTime) < timeout do
        yield("/wait 1")
    end

    -- Handle timeout
    if IPC.vnavmesh.Path.IsRunning() then
        yield("/echo [Script] WARNING: Movement timeout, stopping")
        IPC.vnavmesh.Path.Stop()
        return false
    end

    -- Verify arrival
    if IsAtPosition(x, y, z, 3.0) then
        yield("/echo [Script] Movement completed successfully")
        return true
    else
        yield("/echo [Script] WARNING: Movement completed but not at exact destination")
        return true -- Still consider success if close enough
    end
end
```

### Smart Movement with Navmesh Validation
```lua
function SmartMoveToPosition(x, y, z, fly)
    fly = fly or false

    if not IsVnavmeshReady() then
        yield("/echo [Script] vnavmesh not ready")
        return false
    end

    -- Get nearest point on navmesh
    local nearestPoint = IPC.vnavmesh.Query.Mesh.NearestPoint(Vector3(x, y, z), 2.0, 2.0)
    if nearestPoint then
        yield("/echo [Script] Moving to nearest navmesh point")
        IPC.vnavmesh.SimpleMove.PathfindAndMoveTo(nearestPoint, fly)
    else
        yield("/echo [Script] No navmesh point found, trying direct movement")
        IPC.vnavmesh.SimpleMove.PathfindAndMoveTo(Vector3(x, y, z), fly)
    end

    return true
end
```

### Floor-based Movement
```lua
function MoveToFloorPosition(x, y, z, fly)
    fly = fly or false

    if not IsVnavmeshReady() then
        yield("/echo [Script] vnavmesh not ready")
        return false
    end

    local floorPoint = IPC.vnavmesh.Query.Mesh.PointOnFloor(Vector3(x, y, z), false, 1.0)
    if floorPoint then
        yield("/echo [Script] Moving to floor position")
        IPC.vnavmesh.SimpleMove.PathfindAndMoveTo(floorPoint, fly)
        return true
    else
        yield("/echo [Script] No floor point found")
        return false
    end
end
```

### Build Progress Monitoring
```lua
function MonitorVnavmeshBuild()
    if not HasPlugin("vnavmesh") then
        yield("/echo [Script] vnavmesh plugin not available")
        return false
    end

    if not IPC.vnavmesh.Nav.IsReady() then
        local progress = GetVnavmeshBuildProgress()
        yield("/echo [Script] vnavmesh building... " .. math.floor(progress * 100) .. "%")

        while not IPC.vnavmesh.Nav.IsReady() do
            progress = GetVnavmeshBuildProgress()
            yield("/echo [Script] Build progress: " .. math.floor(progress * 100) .. "%")
            yield("/wait 2")
        end

        yield("/echo [Script] vnavmesh build completed")
    end

    return true
end
```

## State Machine Integration

```lua
CharacterState = {
    ready = Ready,
    moving = Moving,
    -- ... other states
}

function Moving()
    if MoveToPositionWithTimeout(targetX, targetY, targetZ, 30) then
        yield("/echo [Script] Movement completed")
        State = CharacterState.ready
    else
        yield("/echo [Script] Movement failed")
        State = CharacterState.ready
    end
end
```

## Character Condition Integration

```lua
-- Check if character is busy (including vnavmesh)
function IsCharacterBusy()
    return Svc.Condition[CharacterCondition.casting] or
           Svc.Condition[CharacterCondition.betweenAreas] or
           Svc.Condition[CharacterCondition.beingMoved] or
           IPC.vnavmesh.Path.IsRunning() or
           Player.IsBusy
end
```

## Configuration Variables

```lua
configs:
  EnableVnavmesh:
    default: true
    description: Enable vnavmesh navigation
  MovementTimeout:
    default: 30
    description: Movement timeout in seconds
  MovementTolerance:
    default: 3.0
    description: Movement tolerance distance
```

## Best Practices

1. **Always check plugin availability** before using vnavmesh
2. **Use timeouts** for all movement operations (default: 30s)
3. **Check movement state** before starting new movement
4. **Verify arrival** at destination after movement completes
5. **Use appropriate wait times**: 1s for movement checking
6. **Handle vnavmesh not ready** state gracefully
7. **Stop movement** on timeout to prevent stuck states
