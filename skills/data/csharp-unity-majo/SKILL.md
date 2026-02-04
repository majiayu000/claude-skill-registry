---
name: csharp-unity-majo
description: C# and Unity development standards for Mark's projects.
license: Unlicense OR 0BSD
metadata:
  author: Mark Joshwel <mark@joshwel.co>
  version: "2026.2.2"
---

# C# and Unity Standards (Mark)

**Goal**: Write consistent, well-documented C# code for Unity game development following specific naming conventions, XML documentation standards, and British spelling preferences.

## When to Use This Skill

- **Writing C# code for Unity**
- **Creating Unity MonoBehaviour scripts**
- **Writing C# class libraries for games**
- **Implementing Unity event systems**
- **Writing Firebase or external service integrations in Unity**
- **Documenting C# public APIs**
- **Setting up callback registration patterns**

## When NOT to Use This Skill

- **Writing C# for non-Unity projects** (use general C# standards)
- **Writing code for non-gaming contexts**
- **Contributing to external C# projects** with different conventions
- **Writing in other languages** (JavaScript, Python, etc.)

## Process

1. **Check project context** - Verify this is a Unity/C# project
2. **Apply naming conventions by access level**:
   - `public` → camelCase
   - `protected` → PascalCase
   - `private` → _camelCase
3. **Methods always use PascalCase** - Regardless of access level
4. **Add XML documentation** - For all public APIs with `<summary>`, `<param>`, `<returns>`
5. **Use British spellings** - In code identifiers and documentation
6. **Implement callback pattern** - Use List<Action<T>> with Register/Fire methods
7. **Format Debug.Log messages** - Lowercase, consistent with error format
8. **Preserve external naming** - When porting code, keep original naming with source comment
9. **Update AGENTS.md** - Document project-specific Unity/C# patterns

## Constraints

- **ALWAYS use British spellings** in code identifiers and documentation (colour, initialise, behaviour)
- **ALWAYS use PascalCase for methods** regardless of access level
- **ALWAYS use _camelCase for private fields** (prefix with underscore)
- **ALWAYS preserve external code naming** when porting with source attribution
- **NEVER use American spellings** except when interfacing with Unity/.NET APIs (Color, MonoBehaviour)
- **NEVER use lowercase for method names** (even private methods)
- **NEVER rename external ported code** - Preserve original naming for traceability
- **Exception for Unity/.NET APIs**: Use their American spelling when directly referencing (Color, MonoBehaviour, Initialize)

Standards for writing C# code, with Unity-specific patterns.

## Naming Conventions

### Field Naming by Access Level

```csharp
public double lightness;           // public: camelCase
protected Slider LightnessSlider;  // protected: PascalCase
private FirebaseAuth _auth;        // private: _camelCase
```

| Access Level | Convention | Example |
|-------------|------------|---------|
| `public` | camelCase | `lightness`, `userData`, `isReady` |
| `protected` | PascalCase | `LightnessSlider`, `UserData` |
| `private` | _camelCase | `_auth`, `_userData`, `_isInitialised` |

### Method Naming

Methods use **PascalCase** regardless of access level:

```csharp
public void CalculateSimilarity() { }
private void _initialiseAuth() { }  // ❌ WRONG
private void InitialiseAuth() { }   // ✅ CORRECT
```

### Preserved External Code

When porting code from external sources, **preserve the original naming** for traceability:

```csharp
// https://bottosson.github.io/posts/oklab/ (public domain)
public static Lab linear_srgb_to_oklab(RGB c)  // snake_case preserved
{
    // implementation...
}
```

Add a comment linking to the original source.

## XML Documentation

Use XML documentation for public APIs:

```csharp
/// <summary>
///     calculate a similarity percentage from a colour distance
/// </summary>
/// <param name="delta">the delta object returned by CalculateDistance</param>
/// <param name="chromaMax">maximum chroma value, defaults to 1.0f</param>
/// <returns>a similarity percentage (0-100)</returns>
public static float CalculateSimilarity(DeltaLabChE delta, float chromaMax = 1.0f)
{
    // implementation...
}
```

Key points:
- Use lowercase in documentation text (sentence case)
- Indent content within `<summary>` tags
- Include `<param>` for all parameters
- Include `<returns>` for non-void methods
- Use British spellings (colour, initialise, behaviour)

## Callback Registration Pattern

Use List-based callback registration for event systems:

```csharp
private readonly List<Action<FirebaseUser>> _onSignInCallbacks = new();

public void RegisterOnSignInCallback(Action<FirebaseUser> callback)
{
    _onSignInCallbacks.Add(callback);
    Debug.Log($"registering OnSignInCallback ({_onSignInCallbacks.Count})");
}

private void FireOnSignInCallbacks()
{
    foreach (var callback in _onSignInCallbacks)
    {
        try
        {
            callback.Invoke(_user);
        }
        catch (Exception e)
        {
            Debug.LogError($"error invoking callback: {e.Message}");
        }
    }
}
```

Pattern elements:
- Private `List<Action<T>>` for storing callbacks
- Public `Register*Callback` method
- Private `Fire*Callbacks` method with try-catch
- Log registration count for debugging

## Debug.Log Formatting

Use lowercase messages consistent with error message format:

```csharp
Debug.Log($"initialising authentication service");
Debug.Log($"registering OnSignInCallback ({_onSignInCallbacks.Count})");
Debug.LogWarning($"user not authenticated, skipping sync");
Debug.LogError($"error invoking callback: {e.Message}");
```

For errors, follow the standard format:
```csharp
Debug.LogError($"authservice: error: failed to sign in: {e.Message}");
```

## British Spellings

Use British spellings in code identifiers and documentation. See `dev-standards-majo` for the complete list.

Common C# examples:
- `Initialise()` not `Initialize()`
- `colour` not `color`
- `behaviour` not `behavior`
- `Serialise()` not `Serialize()`
- `Normalise()` not `Normalize()`

**Exception**: When interfacing with Unity or .NET APIs that use American spellings (e.g., `MonoBehaviour`, `Color`), use the API's spelling for that specific reference.

## Testing Skills

- **Naming convention check**: Verify field naming by access level (public camelCase, protected PascalCase, private _camelCase)
- **Method naming test**: All methods use PascalCase, never lowercase or _camelCase
- **XML documentation validation**: Public APIs have `<summary>`, `<param>`, `<returns>` tags
- **British spelling verification**: Check colour, initialise, behaviour (not color, initialize, behavior)
- **Callback pattern test**: List<Action<T>> with Register/Fire methods and try-catch
- **Debug.Log format**: Lowercase messages with consistent format
- **External code preservation**: Ported code keeps original naming with source attribution
- **Unity API exception**: Color, MonoBehaviour use American spelling as required by Unity

## Integration

This skill extends `dev-standards-majo`. Always ensure `dev-standards-majo` is loaded for:
- British English spellings
- Error message format
- AGENTS.md maintenance
- Universal code principles

Works alongside:
- `git-majo` — For committing C# changes
- `writing-docs-majo` — For writing C#/Unity documentation
- `task-planning-majo` — For planning Unity projects
