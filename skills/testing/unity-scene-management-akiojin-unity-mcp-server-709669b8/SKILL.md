---
name: unity-scene-management
description: 'Supports Unity scene and GameObject creation, management, and analysis.
  Efficiently performs hierarchy operations, component configuration, and scene analysis.
  Use when: scene creation, scene loading,'
---

---
name: unity-scene-management
description: Supports Unity scene and GameObject creation, management, and analysis. Efficiently performs hierarchy operations, component configuration, and scene analysis. Use when: scene creation, scene loading, GameObject creation, component addition, hierarchy retrieval, scene analysis
allowed-tools: Read, Grep, Glob
---

# Unity Scene & GameObject Management

A guide for creating, managing, and analyzing Unity scenes, GameObjects, and components.

## Quick Start

### 1. Check Current Scene State

```javascript
// List loaded scenes
mcp__unity-mcp-server__list_scenes({ includeLoadedOnly: true })

// Current scene info
mcp__unity-mcp-server__get_scene_info({ includeGameObjects: true })

// Get hierarchy (lightweight)
mcp__unity-mcp-server__get_hierarchy({
  nameOnly: true,
  maxObjects: 100
})
```

### 2. Create GameObject

```javascript
// Empty GameObject
mcp__unity-mcp-server__create_gameobject({
  name: "GameManager"
})

// Primitive
mcp__unity-mcp-server__create_gameobject({
  name: "Floor",
  primitiveType: "plane",
  position: { x: 0, y: 0, z: 0 },
  scale: { x: 10, y: 1, z: 10 }
})
```

### 3. Add Component

```javascript
// Add Rigidbody
mcp__unity-mcp-server__add_component({
  gameObjectPath: "/Player",
  componentType: "Rigidbody",
  properties: { mass: 1.5, useGravity: true }
})
```

## Scene Operations

### Create Scene

```javascript
// Create and load new scene
mcp__unity-mcp-server__create_scene({
  sceneName: "Level01",
  path: "Assets/Scenes/",
  loadScene: true,
  addToBuildSettings: true
})
```

### Load Scene

```javascript
// Single scene load (replaces current scene)
mcp__unity-mcp-server__load_scene({
  scenePath: "Assets/Scenes/MainMenu.unity",
  loadMode: "Single"
})

// Additive load (adds to current scene)
mcp__unity-mcp-server__load_scene({
  scenePath: "Assets/Scenes/UI.unity",
  loadMode: "Additive"
})
```

### Save Scene

```javascript
// Save current scene
mcp__unity-mcp-server__save_scene()

// Save as new file
mcp__unity-mcp-server__save_scene({
  scenePath: "Assets/Scenes/Level01_backup.unity",
  saveAs: true
})
```

### List & Info

```javascript
// All scenes in project
mcp__unity-mcp-server__list_scenes()

// Only scenes in build settings
mcp__unity-mcp-server__list_scenes({ includeBuildScenesOnly: true })

// Specific scene details
mcp__unity-mcp-server__get_scene_info({
  scenePath: "Assets/Scenes/Main.unity",
  includeGameObjects: true
})
```

## GameObject Management

### Creation Options

```javascript
// Full specification
mcp__unity-mcp-server__create_gameobject({
  name: "Enemy",
  primitiveType: "cube",
  parentPath: "/Enemies",
  position: { x: 5, y: 1, z: 0 },
  rotation: { x: 0, y: 45, z: 0 },
  scale: { x: 1, y: 2, z: 1 },
  tag: "Enemy",
  layer: 8
})
```

### Primitive Types

| Type | Description |
|------|-------------|
| `cube` | Cube |
| `sphere` | Sphere |
| `cylinder` | Cylinder |
| `capsule` | Capsule |
| `plane` | Plane |
| `quad` | Quad (2D plane) |

### Search

```javascript
// Search by name
mcp__unity-mcp-server__find_gameobject({
  name: "Player",
  exactMatch: true
})

// Search by tag
mcp__unity-mcp-server__find_gameobject({
  tag: "Enemy"
})

// Search by layer
mcp__unity-mcp-server__find_gameobject({
  layer: 8  // 0-31
})

// Partial match search
mcp__unity-mcp-server__find_gameobject({
  name: "Spawn",
  exactMatch: false
})
```

### Modify

```javascript
// Transform change
mcp__unity-mcp-server__modify_gameobject({
  path: "/Player",
  position: { x: 0, y: 1, z: 0 },
  rotation: { x: 0, y: 90, z: 0 }
})

// Name, tag, layer change
mcp__unity-mcp-server__modify_gameobject({
  path: "/OldName",
  name: "NewName",
  tag: "Player",
  layer: 3
})

// Change parent object
mcp__unity-mcp-server__modify_gameobject({
  path: "/Player",
  parentPath: "/Characters"
})

// Unparent
mcp__unity-mcp-server__modify_gameobject({
  path: "/Characters/Player",
  parentPath: null
})

// Change active state
mcp__unity-mcp-server__modify_gameobject({
  path: "/Player",
  active: false
})
```

### Delete

```javascript
// Single delete
mcp__unity-mcp-server__delete_gameobject({
  path: "/OldObject"
})

// Multiple delete
mcp__unity-mcp-server__delete_gameobject({
  paths: ["/Object1", "/Object2", "/Object3"]
})

// Keep children
mcp__unity-mcp-server__delete_gameobject({
  path: "/Parent",
  includeChildren: false
})
```

### Get Hierarchy

```javascript
// Lightweight (names and paths only) - for large scenes
mcp__unity-mcp-server__get_hierarchy({
  nameOnly: true,
  maxObjects: 500
})

// Detailed (with components and transform) - for small scenes
mcp__unity-mcp-server__get_hierarchy({
  includeComponents: true,
  includeTransform: true,
  maxObjects: 50
})

// Specific subtree only
mcp__unity-mcp-server__get_hierarchy({
  rootPath: "/Enemies",
  maxDepth: 2
})

// Exclude inactive objects
mcp__unity-mcp-server__get_hierarchy({
  includeInactive: false
})
```

## Component System

### Add Component

```javascript
// Basic addition
mcp__unity-mcp-server__add_component({
  gameObjectPath: "/Player",
  componentType: "Rigidbody"
})

// With properties
mcp__unity-mcp-server__add_component({
  gameObjectPath: "/Player",
  componentType: "BoxCollider",
  properties: {
    size: { x: 1, y: 2, z: 1 },
    center: { x: 0, y: 1, z: 0 },
    isTrigger: false
  }
})

// Custom script
mcp__unity-mcp-server__add_component({
  gameObjectPath: "/Player",
  componentType: "PlayerController"
})
```

### Modify Component

#### `modify_component` - Batch change multiple properties

```javascript
mcp__unity-mcp-server__modify_component({
  gameObjectPath: "/Player",
  componentType: "Rigidbody",
  properties: {
    mass: 2.0,
    drag: 0.5,
    useGravity: true
  }
})
```

#### `set_component_field` - Precise single field change

```javascript
// Serialized field (including private)
mcp__unity-mcp-server__set_component_field({
  gameObjectPath: "/Player",
  componentType: "PlayerController",
  fieldPath: "_moveSpeed",
  value: 5.0
})

// Nested field
mcp__unity-mcp-server__set_component_field({
  gameObjectPath: "/Player",
  componentType: "PlayerController",
  fieldPath: "settings.jumpHeight",
  value: 3.0
})

// Array element
mcp__unity-mcp-server__set_component_field({
  gameObjectPath: "/Player",
  componentType: "Inventory",
  fieldPath: "items[0].count",
  value: 10
})

// Object reference
mcp__unity-mcp-server__set_component_field({
  gameObjectPath: "/Player",
  componentType: "PlayerController",
  fieldPath: "targetTransform",
  objectReference: { assetPath: "Assets/Prefabs/Target.prefab" }
})

// Enum value
mcp__unity-mcp-server__set_component_field({
  gameObjectPath: "/Player",
  componentType: "PlayerController",
  fieldPath: "state",
  enumValue: "Running"
})
```

### `modify_component` vs `set_component_field`

| Feature | modify_component | set_component_field |
|---------|------------------|---------------------|
| Use case | Batch multiple properties | Precise single field |
| Nested support | ❌ Top-level only | ✅ Dot notation |
| Array elements | ❌ | ✅ `[index]` supported |
| Private fields | △ Serialized only | ✅ All serialized |
| Object references | △ | ✅ assetPath/guid |

### List & Remove Component

```javascript
// List components
mcp__unity-mcp-server__list_components({
  gameObjectPath: "/Player"
})

// Remove component
mcp__unity-mcp-server__remove_component({
  gameObjectPath: "/Player",
  componentType: "OldScript"
})

// When multiple of same type exist
mcp__unity-mcp-server__remove_component({
  gameObjectPath: "/Player",
  componentType: "AudioSource",
  componentIndex: 1  // Second AudioSource
})
```

### Available Component Types

```javascript
// Search by category
mcp__unity-mcp-server__get_component_types({
  category: "Physics"  // Physics, Rendering, UI, etc.
})

// Search by name
mcp__unity-mcp-server__get_component_types({
  search: "Collider"
})

// Only those addable via AddComponent
mcp__unity-mcp-server__get_component_types({
  onlyAddable: true
})
```

## Scene Analysis

### Analyze Entire Scene

```javascript
// Object statistics
mcp__unity-mcp-server__analyze_scene_contents({
  groupByType: true,
  includePrefabInfo: true
})

// With memory info
mcp__unity-mcp-server__analyze_scene_contents({
  includeMemoryInfo: true
})
```

### Component Search

```javascript
// Find objects with specific component
mcp__unity-mcp-server__find_by_component({
  componentType: "Light",
  searchScope: "scene"
})

// Include prefabs in search
mcp__unity-mcp-server__find_by_component({
  componentType: "AudioSource",
  searchScope: "all",
  includeInactive: true
})
```

### Detailed Inspection

```javascript
// GameObject details
mcp__unity-mcp-server__get_gameobject_details({
  gameObjectName: "Player",
  includeComponents: true,
  includeMaterials: true,
  includeChildren: true,
  maxDepth: 3
})

// All component property values
mcp__unity-mcp-server__get_component_values({
  gameObjectName: "Player",
  componentType: "Rigidbody",
  includePrivateFields: true
})

// Object reference relationships
mcp__unity-mcp-server__get_object_references({
  gameObjectName: "Player",
  includeAssetReferences: true,
  includeHierarchyReferences: true
})
```

## Common Workflows

### Scene Setup

```javascript
// 1. Create new scene
mcp__unity-mcp-server__create_scene({
  sceneName: "GameLevel",
  loadScene: true
})

// 2. Create environment objects
mcp__unity-mcp-server__create_gameobject({
  name: "Environment"
})

mcp__unity-mcp-server__create_gameobject({
  name: "Ground",
  primitiveType: "plane",
  parentPath: "/Environment",
  scale: { x: 50, y: 1, z: 50 }
})

// 3. Set up lighting
mcp__unity-mcp-server__create_gameobject({
  name: "Sun"
})

mcp__unity-mcp-server__add_component({
  gameObjectPath: "/Sun",
  componentType: "Light",
  properties: {
    type: "Directional",
    intensity: 1.0,
    color: { r: 1, g: 0.95, b: 0.8, a: 1 }
  }
})

// 4. Save
mcp__unity-mcp-server__save_scene()
```

### UI Canvas Setup

```javascript
// Create Canvas
mcp__unity-mcp-server__create_gameobject({ name: "Canvas" })
mcp__unity-mcp-server__add_component({
  gameObjectPath: "/Canvas",
  componentType: "Canvas",
  properties: { renderMode: "ScreenSpaceOverlay" }
})
mcp__unity-mcp-server__add_component({
  gameObjectPath: "/Canvas",
  componentType: "CanvasScaler"
})
mcp__unity-mcp-server__add_component({
  gameObjectPath: "/Canvas",
  componentType: "GraphicRaycaster"
})

// Add button
mcp__unity-mcp-server__create_gameobject({
  name: "StartButton",
  parentPath: "/Canvas"
})
mcp__unity-mcp-server__add_component({
  gameObjectPath: "/Canvas/StartButton",
  componentType: "Button"
})
```

### Physics Object Placement

```javascript
// Create physics object
mcp__unity-mcp-server__create_gameobject({
  name: "PhysicsCube",
  primitiveType: "cube",
  position: { x: 0, y: 5, z: 0 }
})

// Add Rigidbody
mcp__unity-mcp-server__add_component({
  gameObjectPath: "/PhysicsCube",
  componentType: "Rigidbody",
  properties: { mass: 1.0 }
})

// Collider is auto-added (for primitives)
```

## Common Mistakes

### 1. Wrong Path Format

```javascript
// ❌ Without slash
gameObjectPath: "Player"

// ✅ Leading slash required
gameObjectPath: "/Player"

// ✅ Hierarchy path
gameObjectPath: "/Parent/Child/GrandChild"
```

### 2. Undefined Tag/Layer

```javascript
// ❌ Using non-existent tag
tag: "CustomEnemy"  // Error

// ✅ Add tag first
mcp__unity-mcp-server__manage_tags({
  action: "add",
  tagName: "CustomEnemy"
})
```

### 3. Missing Inactive Objects

```javascript
// ❌ Cannot find inactive object
mcp__unity-mcp-server__find_gameobject({ name: "HiddenObject" })

// ✅ Explicitly include inactive
mcp__unity-mcp-server__get_hierarchy({
  includeInactive: true
})
```

### 4. Performance Issues with Large Hierarchy

```javascript
// ❌ Getting all info (high token usage)
mcp__unity-mcp-server__get_hierarchy({
  includeComponents: true,
  includeTransform: true,
  maxObjects: -1  // Unlimited
})

// ✅ Lightweight for overview
mcp__unity-mcp-server__get_hierarchy({
  nameOnly: true,
  maxObjects: 100
})

// ✅ Get details only for specific object
mcp__unity-mcp-server__get_gameobject_details({
  gameObjectName: "SpecificObject",
  includeComponents: true
})
```

### 5. Losing Changes Without Save

```javascript
// ✅ Save after important changes
mcp__unity-mcp-server__save_scene()
```

## Tool Reference

| Tool | Purpose |
|------|---------|
| `create_scene` | Create scene |
| `load_scene` | Load scene |
| `save_scene` | Save scene |
| `list_scenes` | List scenes |
| `get_scene_info` | Get scene info |
| `create_gameobject` | Create GameObject |
| `find_gameobject` | Find GameObject |
| `modify_gameobject` | Modify GameObject |
| `delete_gameobject` | Delete GameObject |
| `get_hierarchy` | Get hierarchy |
| `add_component` | Add component |
| `modify_component` | Modify component (batch) |
| `set_component_field` | Modify field (precise) |
| `remove_component` | Remove component |
| `list_components` | List components |
| `get_component_types` | List available types |
| `analyze_scene_contents` | Analyze scene |
| `find_by_component` | Find by component |
| `get_gameobject_details` | Get detailed info |
| `get_component_values` | Get property values |
| `manage_tags` | Manage tags |
| `manage_layers` | Manage layers |
