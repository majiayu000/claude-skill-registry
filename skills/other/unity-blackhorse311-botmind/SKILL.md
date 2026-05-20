---
name: unity
description: |
  Integrates Unity APIs, MonoBehaviours, and game engine components for SPT/EFT modding.
  Use when: Working with Unity GameObjects, transforms, physics, NavMesh, coroutines, or any UnityEngine namespace.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# Unity Skill

Unity integration for SPT (Single Player Tarkov) modding via BepInEx plugins. This project uses Unity 2021.x APIs through decompiled EFT assemblies, with heavy reliance on `Physics.OverlapSphere`, `NavMesh`, `Vector3` math, and coroutine-based async patterns. All Unity calls happen on the main thread; use `UnityMainThreadDispatcher` patterns when needed.

## Quick Start

### NavMesh Position Validation

```csharp
using UnityEngine;
using UnityEngine.AI;

// ALWAYS validate positions before navigation
public bool TryGetValidNavMeshPosition(Vector3 target, out Vector3 validPosition, float maxDistance = 2f)
{
    if (NavMesh.SamplePosition(target, out NavMeshHit hit, maxDistance, NavMesh.AllAreas))
    {
        validPosition = hit.position;
        return true;
    }
    validPosition = Vector3.zero;
    return false;
}
```

### Physics Overlap for Detection

```csharp
// Find lootable objects within radius
private readonly Collider[] _scanBuffer = new Collider[64];

public void ScanForLoot(Vector3 position, float radius, int layerMask)
{
    int count = Physics.OverlapSphereNonAlloc(position, radius, _scanBuffer, layerMask);
    for (int i = 0; i < count; i++)
    {
        var collider = _scanBuffer[i];
        // Process collider.gameObject
    }
}
```

### Distance and Direction Calculations

```csharp
// Prefer sqrMagnitude for distance comparisons (avoids sqrt)
float distanceSq = (targetPos - botPos).sqrMagnitude;
if (distanceSq < maxDistanceSq) // Compare squared values
{
    Vector3 direction = (targetPos - botPos).normalized;
    // Use direction for facing/movement
}
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| NavMesh sampling | Validate movement targets | `NavMesh.SamplePosition(pos, out hit, 2f, NavMesh.AllAreas)` |
| Physics overlap | Area detection | `Physics.OverlapSphereNonAlloc(pos, radius, buffer, mask)` |
| Layer masks | Filter physics queries | `LayerMask.GetMask("Loot", "Interactive")` |
| Transform caching | Performance | `private Transform _cachedTransform;` |
| Vector3 math | Distance/direction | `(a - b).sqrMagnitude`, `(a - b).normalized` |

## Common Patterns

### Spawn Position Calculation

**When:** Spawning MedicBuddy team behind player

```csharp
public Vector3 CalculateSpawnPosition(Transform playerTransform, float distance = 15f)
{
    // Spawn behind and slightly offset
    Vector3 behindPlayer = playerTransform.position - playerTransform.forward * distance;
    
    if (TryGetValidNavMeshPosition(behindPlayer, out Vector3 validPos))
        return validPos;
    
    // Fallback: try sides
    Vector3 leftPos = playerTransform.position - playerTransform.right * distance;
    if (TryGetValidNavMeshPosition(leftPos, out validPos))
        return validPos;
        
    return playerTransform.position; // Last resort
}
```

### Coroutine for Timed Operations

**When:** Healing ticks, delayed actions

```csharp
private IEnumerator HealOverTime(float totalAmount, float duration)
{
    float elapsed = 0f;
    float healPerSecond = totalAmount / duration;
    
    while (elapsed < duration)
    {
        ApplyHealing(healPerSecond * Time.deltaTime);
        elapsed += Time.deltaTime;
        yield return null; // Wait one frame
    }
}
```

## See Also

- [patterns](references/patterns.md) - GameObject handling, physics queries, NavMesh
- [workflows](references/workflows.md) - Common Unity workflows in SPT modding

## Related Skills

- See the **csharp** skill for C# patterns and error handling
- See the **bepinex** skill for plugin lifecycle and Unity integration
- See the **harmony** skill for patching Unity methods