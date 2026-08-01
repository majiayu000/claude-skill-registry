---
name: serialization-review
description: 'Review JSON serialization for scenes, prefabs, and components. Use when:
  (1) implementing serializable components, (2) debugging save/load failures, (3)
  adding asset types, (4) reviewing serialization'
---

---
name: serialization-review
description: Review JSON serialization for scenes, prefabs, and components. Use when: (1) implementing serializable components, (2) debugging save/load failures, (3) adding asset types, (4) reviewing serialization code, (5) investigating data corruption, (6) implementing JsonConverters.
---

# Serialization Review

## Overview
This skill audits JSON serialization implementation to ensure scenes, prefabs, and components serialize/deserialize correctly, maintain version compatibility, handle resource references properly, and follow established serialization patterns.

## Table of Contents
- [Overview](#overview)
- [When to Use](#when-to-use)
- [Serialization Architecture](#serialization-architecture)
- [Serialization Patterns](#serialization-patterns)
- [Review Checklist](#review-checklist)
- [Review Output Format](#review-output-format)
- [Examples](#examples)

## When to Use
Invoke this skill when:
- Adding new serializable components
- Debugging scene save/load issues
- Implementing new asset types (prefabs, animations, tilemaps)
- Refactoring component data structures
- Versioning serialization format
- Questions about custom JsonConverter implementation
- Investigating data corruption or missing data after load

## Serialization Architecture

### SceneSerializer
**Location**: `Engine/Scene/Serializer/SceneSerializer.cs`

**Responsibilities**:
- Serialize/deserialize entire scene to/from JSON
- Handle entity hierarchy and component serialization
- Manage custom converters and serialization options

**Key Methods**: `Serialize(Scene, path)`, `Deserialize(path)`

### Custom Converters
**Location**: `Engine/Scene/Serializer/`

**Existing Converters**:
- `Vector2Converter`, `Vector3Converter`, `Vector4Converter`
- `TileMapComponentConverter`
- Component-specific converters for complex types

## Serialization Patterns

### 1. JsonIgnore for Runtime Data

**Pattern**: Use `[JsonIgnore]` for runtime-only data

```csharp
public class RigidBody2DComponent
{
    // Serialized properties
    public BodyType Type { get; set; } = BodyType.Dynamic;
    public float Mass { get; set; } = 1.0f;
    public bool FixedRotation { get; set; } = false;

    // Runtime-only (not serialized)
    [JsonIgnore]
    public Body? RuntimeBody { get; set; }

    // Runtime-only (not serialized)
    [JsonIgnore]
    public World? RuntimeWorld { get; set; }
}
```

**Why?**: Runtime objects (physics bodies, loaded meshes, textures) should not be serialized - they're recreated at runtime.

### 2. Resource Path Serialization

**Pattern**: Store paths, not loaded resources

```csharp
public class SpriteRendererComponent
{
    // Serialize path, not loaded texture
    public string TexturePath { get; set; } = string.Empty;

    // Color is serialized
    public Vector4 Color { get; set; } = Vector4.One;

    // Runtime-only loaded texture (not serialized)
    [JsonIgnore]
    public Texture? LoadedTexture { get; set; }
}

// At runtime, load texture from path with error handling
if (!string.IsNullOrEmpty(sprite.TexturePath))
{
    try
    {
        sprite.LoadedTexture = textureFactory.LoadTexture(sprite.TexturePath);
    }
    catch (FileNotFoundException)
    {
        logger.Warn($"Missing texture: {sprite.TexturePath}");
        sprite.LoadedTexture = textureFactory.GetDefaultTexture();
    }
}
```

### 3. Custom Converter for Complex Types

**When Needed**:
- Custom serialization format or optimized JSON structure
- Backward compatibility with breaking changes
- Complex type handling (vectors, GUIDs, nested structures)

## Review Checklist

When reviewing serialization implementation, verify:

**1. Runtime Data Exclusion**
- [ ] All runtime objects marked with `[JsonIgnore]`
- [ ] Physics bodies, loaded textures/meshes not serialized
- [ ] Cached/computed values excluded

**2. Resource References**
- [ ] Paths stored instead of loaded resources
- [ ] Valid path format (relative to project root)
- [ ] Missing path handling at load time

**3. Circular References**
- [ ] Entity parent/child relationships handled correctly
- [ ] Component cross-references resolved properly
- [ ] No infinite loops in serialization

**4. Version Compatibility**
- [ ] New fields have default values
- [ ] Removed fields handled gracefully
- [ ] Custom converters for breaking changes

**5. Custom Converters**
- [ ] Necessary (complex types, optimization, compatibility)
- [ ] Read/Write methods symmetric
- [ ] Registered in serialization options

## Review Output Format

Report findings as:

**Issue**: [Serialization problem description]
**Component**: [Component class name]
**Location**: [File path and line number]
**Problem**: [What will break or serialize incorrectly]
**Fix**: [Code change with before/after]
**Priority**: [Critical/High/Medium/Low]

### Example Report

**Issue**: Runtime physics body being serialized
**Component**: RigidBody2DComponent
**Location**: Engine/Scene/Components/RigidBody2DComponent.cs:45
**Problem**: `RuntimeBody` property will serialize the entire Box2D body object, causing massive JSON files and deserialization failures (Box2D objects aren't JSON-serializable)
**Fix**:
```csharp
// Before
public Body? RuntimeBody { get; set; }

// After
[JsonIgnore]
public Body? RuntimeBody { get; set; }
```
**Priority**: Critical

## Examples

For detailed guidance and comprehensive examples:

### [Custom Converters](examples/custom-converters.md)
Complete JsonConverter implementations with:
- Full AnimationComponent converter with error handling
- Vector3, GUID, and common type converters
- Registration and testing patterns
- Best practices for symmetric Read/Write methods

### [Common Issues](examples/common-issues.md)
Anti-pattern catalog with before/after fixes:
- Runtime objects not marked [JsonIgnore]
- Loaded resources instead of paths
- Missing default values for new fields
- Circular references in entity hierarchy
- Platform-specific path separators
- Asymmetric converter implementations
