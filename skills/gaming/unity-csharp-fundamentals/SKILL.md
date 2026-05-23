---
name: unity-csharp-fundamentals
description: Unity C# fundamental patterns including TryGetComponent, SerializeField, RequireComponent, and safe coding practices. Essential patterns for robust Unity development. Use PROACTIVELY for any Unity C# code to ensure best practices.
requires:
  - csharp-plugin:csharp-code-style
  - csharp-plugin:csharp-xml-docs
---

# Unity C# Fundamentals - Essential Coding Patterns

## Overview

Core Unity C# patterns for safe, maintainable code. Not optimizations but **fundamental practices**.

**Foundation Required**: C# basics, Unity MonoBehaviour lifecycle

**Core Topics**: TryGetComponent, SerializeField, RequireComponent, Null-safe patterns, Lifecycle management

## Essential Patterns

### TryGetComponent (Required)

**Always use `TryGetComponent` instead of `GetComponent`**:

```csharp
// ❌ WRONG
Rigidbody rb = GetComponent<Rigidbody>();
rb.velocity = Vector3.zero;  // NullReferenceException!

// ✅ CORRECT
Rigidbody rb;
if (TryGetComponent(out rb))
{
    rb.velocity = Vector3.zero;
}

// ✅ Cache in Awake with validation
private Rigidbody mRb;

void Awake()
{
    if (!TryGetComponent(out mRb))
    {
        Debug.LogError($"Missing Rigidbody on {gameObject.name}", this);
    }
}
```

### Global Object Search (Unity 2023.1+)

```csharp
// ❌ OBSOLETE - DON'T USE
GameManager manager = FindObjectOfType<GameManager>();

// ✅ CORRECT - Fastest (unordered)
GameManager manager = FindAnyObjectByType<GameManager>();

// ✅ CORRECT - Ordered
GameManager manager = FindFirstObjectByType<GameManager>();

// ✅ Multiple objects
Enemy[] enemies = FindObjectsByType<Enemy>(FindObjectsSortMode.None);
```

### SerializeField Pattern

```csharp
// ❌ WRONG: Public field
public float speed;

// ✅ CORRECT: SerializeField + private
[SerializeField] private float mSpeed = 5f;

// ✅ With Inspector helpers
[SerializeField, Tooltip("Units/second"), Range(0f, 100f)]
private float mMoveSpeed = 5f;

public float Speed => mSpeed;  // Read-only access
```

### RequireComponent

```csharp
[RequireComponent(typeof(Rigidbody))]
[DisallowMultipleComponent]
public class PhysicsObject : MonoBehaviour
{
    private Rigidbody mRb;

    void Awake()
    {
        TryGetComponent(out mRb);  // Guaranteed to exist
    }
}
```

### Unity Null Safety

```csharp
// ❌ WRONG: C# null operators don't work with Unity Objects
Transform target = mCached ?? FindTarget();  // Broken!
mEnemy?.TakeDamage(10);  // May fail after Destroy

// ✅ CORRECT: Explicit null check
Transform target = mCached != null ? mCached : FindTarget();

if (mEnemy != null)
{
    mEnemy.TakeDamage(10);
}
```

### Lifecycle Order

```csharp
void Awake()     { /* 1. Self-init, cache components */ }
void OnEnable()  { /* 2. Subscribe events */ }
void Start()     { /* 3. Cross-object init */ }
void OnDisable() { /* 4. Unsubscribe events */ }
void OnDestroy() { /* 5. Final cleanup */ }
```

## Unity C# 9.0 Limitations

> **Important**: Unity's Mono/IL2CPP runtime lacks `IsExternalInit`.
> `init` accessor causes compile error CS0518.

```csharp
// ❌ COMPILE ERROR in Unity
public string Name { get; private init; }

// ✅ Use private set
public string Name { get; private set; }

// ✅ Or readonly field + property
private readonly string mName;
public string Name => mName;
```

**Available**: Pattern matching, switch expressions, covariant returns
**NOT Available**: `init`, `required` (C# 11)

## Quick Reference

| Pattern | Rule |
|---------|------|
| Component access | Always `TryGetComponent`, never bare `GetComponent` |
| Serialization | `[SerializeField] private`, not `public` |
| Dependencies | Use `[RequireComponent]` for guaranteed components |
| Null checks | Explicit `!= null`, not `??` or `?.` |
| Caching | Get in `Awake`, reuse everywhere |
| Events | Subscribe in `OnEnable`, unsubscribe in `OnDisable` |
| Global search | `FindAnyObjectByType` (fastest), not `FindObjectOfType` |

## Reference Documentation

### [Component Access Patterns](references/component-access.md)
- TryGetComponent variations and interface-based access
- GetComponentInChildren/Parent patterns
- Allocation-free multiple component access
- Caching strategies and performance comparisons

### [Attributes and Patterns](references/attributes-patterns.md)
- Complete serialization attribute reference
- Inspector customization (Header, Tooltip, Range)
- Execution order control
- Conditional compilation

### [Language Limitations](references/language-limitations.md)
- `init` accessor alternatives with code examples
- Records in Unity (limitations and workarounds)
- `required` modifier alternatives
- Available C# 9.0 features in Unity
