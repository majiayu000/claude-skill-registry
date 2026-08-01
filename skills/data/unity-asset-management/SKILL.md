---
name: unity-asset-management
description: 'Supports creating, editing, and managing Unity assets (prefabs, materials,
  asset database, Addressables). Includes dependency analysis and import settings.
  Use when: prefab creation, material editing,'
---

---
name: unity-asset-management
description: Supports creating, editing, and managing Unity assets (prefabs, materials, asset database, Addressables). Includes dependency analysis and import settings. Use when: prefab creation, material editing, asset search, dependency analysis, Addressables
allowed-tools: Read, Grep, Glob
---

# Unity Asset Management

A guide for managing prefabs, materials, asset database, and Addressables.

## Quick Start

### 1. Create and Place Prefabs

```javascript
// Create prefab from GameObject
mcp__unity-mcp-server__create_prefab({
  prefabPath: "Assets/Prefabs/Enemy.prefab",
  gameObjectPath: "/Enemy"
})

// Instantiate prefab in scene
mcp__unity-mcp-server__instantiate_prefab({
  prefabPath: "Assets/Prefabs/Enemy.prefab",
  position: { x: 5, y: 0, z: 0 },
  name: "Enemy_01"
})
```

### 2. Create Material

```javascript
// Create basic material
mcp__unity-mcp-server__create_material({
  materialPath: "Assets/Materials/RedMetal.mat",
  shader: "Standard",
  properties: {
    "_Color": [1, 0, 0, 1],
    "_Metallic": 0.8,
    "_Glossiness": 0.6
  }
})
```

### 3. Search Assets

```javascript
// Search for textures
mcp__unity-mcp-server__manage_asset_database({
  action: "find_assets",
  filter: "t:Texture2D"
})
```

## Prefab Management

### Create Prefab

```javascript
// Create prefab from scene GameObject
mcp__unity-mcp-server__create_prefab({
  prefabPath: "Assets/Prefabs/Player.prefab",
  gameObjectPath: "/Player"
})

// Create empty prefab
mcp__unity-mcp-server__create_prefab({
  prefabPath: "Assets/Prefabs/Empty.prefab",
  createFromTemplate: true
})

// Allow overwrite
mcp__unity-mcp-server__create_prefab({
  prefabPath: "Assets/Prefabs/Player.prefab",
  gameObjectPath: "/Player",
  overwrite: true
})
```

### Prefab Mode (Editing)

```javascript
// Open prefab
mcp__unity-mcp-server__open_prefab({
  prefabPath: "Assets/Prefabs/Player.prefab"
})

// Focus on specific object
mcp__unity-mcp-server__open_prefab({
  prefabPath: "Assets/Prefabs/Player.prefab",
  focusObject: "Weapon",  // Relative path from prefab root
  isolateObject: true
})

// Edit in prefab mode (component operations, etc.)
mcp__unity-mcp-server__add_component({
  gameObjectPath: "/Player",  // In prefab mode, prefab root is the root
  componentType: "AudioSource"
})

// Save and exit prefab mode
mcp__unity-mcp-server__save_prefab()
mcp__unity-mcp-server__exit_prefab_mode({ saveChanges: true })

// Exit without saving
mcp__unity-mcp-server__exit_prefab_mode({ saveChanges: false })
```

### Prefab Instantiation

```javascript
// Basic instantiation
mcp__unity-mcp-server__instantiate_prefab({
  prefabPath: "Assets/Prefabs/Enemy.prefab"
})

// With Transform
mcp__unity-mcp-server__instantiate_prefab({
  prefabPath: "Assets/Prefabs/Enemy.prefab",
  position: { x: 10, y: 0, z: 5 },
  rotation: { x: 0, y: 90, z: 0 },
  name: "Enemy_Guard"
})

// With parent object
mcp__unity-mcp-server__instantiate_prefab({
  prefabPath: "Assets/Prefabs/Coin.prefab",
  parent: "/Collectibles",
  position: { x: 0, y: 1, z: 0 }
})
```

### Prefab Modification

```javascript
// Change properties (also apply to instances)
mcp__unity-mcp-server__modify_prefab({
  prefabPath: "Assets/Prefabs/Enemy.prefab",
  modifications: {
    "health": 150,
    "speed": 3.5
  },
  applyToInstances: true
})

// Do not apply to instances
mcp__unity-mcp-server__modify_prefab({
  prefabPath: "Assets/Prefabs/Enemy.prefab",
  modifications: { "debugMode": true },
  applyToInstances: false
})
```

## Material Management

### Create Material

```javascript
// Standard shader
mcp__unity-mcp-server__create_material({
  materialPath: "Assets/Materials/Metal.mat",
  shader: "Standard",
  properties: {
    "_Color": [0.8, 0.8, 0.8, 1],
    "_Metallic": 1.0,
    "_Glossiness": 0.9
  }
})

// Unlit shader
mcp__unity-mcp-server__create_material({
  materialPath: "Assets/Materials/Unlit.mat",
  shader: "Unlit/Color",
  properties: {
    "_Color": [1, 0, 0, 1]
  }
})

// URP shader
mcp__unity-mcp-server__create_material({
  materialPath: "Assets/Materials/URPLit.mat",
  shader: "Universal Render Pipeline/Lit",
  properties: {
    "_BaseColor": [1, 1, 1, 1],
    "_Smoothness": 0.5
  }
})

// Copy existing material
mcp__unity-mcp-server__create_material({
  materialPath: "Assets/Materials/MetalRed.mat",
  copyFrom: "Assets/Materials/Metal.mat",
  properties: {
    "_Color": [1, 0, 0, 1]
  }
})
```

### Modify Material

```javascript
// Change properties
mcp__unity-mcp-server__modify_material({
  materialPath: "Assets/Materials/Metal.mat",
  properties: {
    "_Color": [0, 0, 1, 1],
    "_Metallic": 0.5
  }
})

// Change shader
mcp__unity-mcp-server__modify_material({
  materialPath: "Assets/Materials/Debug.mat",
  shader: "Unlit/Color",
  properties: {
    "_Color": [1, 0, 1, 1]
  }
})
```

### Common Shader Properties

| Shader | Property | Description |
|--------|----------|-------------|
| Standard | `_Color` | Albedo color [R,G,B,A] |
| Standard | `_Metallic` | Metallic value 0-1 |
| Standard | `_Glossiness` | Smoothness 0-1 |
| Standard | `_MainTex` | Albedo texture |
| Standard | `_BumpMap` | Normal map |
| Standard | `_EmissionColor` | Emission color |
| URP/Lit | `_BaseColor` | Base color |
| URP/Lit | `_Smoothness` | Smoothness |
| URP/Lit | `_BaseMap` | Base texture |

## Asset Database Operations

### Search Assets

```javascript
// Type filter
mcp__unity-mcp-server__manage_asset_database({
  action: "find_assets",
  filter: "t:Texture2D"
})

// Name filter
mcp__unity-mcp-server__manage_asset_database({
  action: "find_assets",
  filter: "Player"
})

// Label filter
mcp__unity-mcp-server__manage_asset_database({
  action: "find_assets",
  filter: "l:UI"
})

// Combined filter
mcp__unity-mcp-server__manage_asset_database({
  action: "find_assets",
  filter: "t:Material Player"
})

// Folder specification
mcp__unity-mcp-server__manage_asset_database({
  action: "find_assets",
  filter: "t:Prefab",
  searchInFolders: ["Assets/Prefabs", "Assets/Characters"]
})
```

### Filter Syntax

| Filter | Description | Example |
|--------|-------------|---------|
| `t:Type` | Search by type | `t:Texture2D`, `t:Material`, `t:Prefab` |
| `l:Label` | Search by label | `l:UI`, `l:Environment` |
| `name` | Search by name | `Player`, `Enemy*` |
| Combined | AND with space | `t:Material Red` |

### Get Asset Info

```javascript
mcp__unity-mcp-server__manage_asset_database({
  action: "get_asset_info",
  assetPath: "Assets/Textures/Player.png"
})
// Returns: type, size, dependencies, labels, etc.
```

### Folder Operations

```javascript
// Create folder
mcp__unity-mcp-server__manage_asset_database({
  action: "create_folder",
  folderPath: "Assets/NewFeature/Prefabs"
})
```

### Move, Copy, Delete Assets

```javascript
// Move
mcp__unity-mcp-server__manage_asset_database({
  action: "move_asset",
  fromPath: "Assets/Old/Player.prefab",
  toPath: "Assets/New/Player.prefab"
})

// Copy
mcp__unity-mcp-server__manage_asset_database({
  action: "copy_asset",
  fromPath: "Assets/Templates/Enemy.prefab",
  toPath: "Assets/Enemies/Enemy_01.prefab"
})

// Delete
mcp__unity-mcp-server__manage_asset_database({
  action: "delete_asset",
  assetPath: "Assets/Unused/OldPrefab.prefab"
})
```

### Refresh and Save

```javascript
// Refresh asset database
mcp__unity-mcp-server__manage_asset_database({
  action: "refresh"
})

// Save all assets
mcp__unity-mcp-server__manage_asset_database({
  action: "save"
})
```

## Dependency Analysis

### Get Dependencies

```javascript
// Get asset dependencies
mcp__unity-mcp-server__analyze_asset_dependencies({
  action: "get_dependencies",
  assetPath: "Assets/Prefabs/Player.prefab",
  recursive: true  // Include indirect dependencies
})
```

### Get Dependents

```javascript
// Find assets that reference this asset
mcp__unity-mcp-server__analyze_asset_dependencies({
  action: "get_dependents",
  assetPath: "Assets/Materials/PlayerMat.mat"
})
```

### Detect Circular Dependencies

```javascript
mcp__unity-mcp-server__analyze_asset_dependencies({
  action: "analyze_circular"
})
```

### Detect Unused Assets

```javascript
mcp__unity-mcp-server__analyze_asset_dependencies({
  action: "find_unused",
  includeBuiltIn: false
})
```

### Analyze Size Impact

```javascript
// Total size of asset and its dependencies
mcp__unity-mcp-server__analyze_asset_dependencies({
  action: "analyze_size_impact",
  assetPath: "Assets/Prefabs/Boss.prefab"
})
```

### Validate References

```javascript
// Detect broken references
mcp__unity-mcp-server__analyze_asset_dependencies({
  action: "validate_references"
})
```

## Addressables System

### Entry Management

```javascript
// Add entry
mcp__unity-mcp-server__addressables_manage({
  action: "add_entry",
  assetPath: "Assets/Prefabs/Enemy.prefab",
  groupName: "Enemies",
  address: "enemy_basic",
  labels: ["combat", "spawn"]
})

// Remove entry
mcp__unity-mcp-server__addressables_manage({
  action: "remove_entry",
  assetPath: "Assets/Prefabs/OldEnemy.prefab"
})

// Change address
mcp__unity-mcp-server__addressables_manage({
  action: "set_address",
  assetPath: "Assets/Prefabs/Enemy.prefab",
  newAddress: "enemy_soldier"
})

// Add label
mcp__unity-mcp-server__addressables_manage({
  action: "add_label",
  assetPath: "Assets/Prefabs/Enemy.prefab",
  label: "boss"
})

// Remove label
mcp__unity-mcp-server__addressables_manage({
  action: "remove_label",
  assetPath: "Assets/Prefabs/Enemy.prefab",
  label: "combat"
})

// Move entry to different group
mcp__unity-mcp-server__addressables_manage({
  action: "move_entry",
  assetPath: "Assets/Prefabs/Enemy.prefab",
  targetGroupName: "BossEnemies"
})
```

### Group Management

```javascript
// List groups
mcp__unity-mcp-server__addressables_manage({
  action: "list_groups"
})

// List entries in group
mcp__unity-mcp-server__addressables_manage({
  action: "list_entries",
  groupName: "Enemies",
  pageSize: 50,
  offset: 0
})

// Create group
mcp__unity-mcp-server__addressables_manage({
  action: "create_group",
  groupName: "DLC_01"
})

// Remove group
mcp__unity-mcp-server__addressables_manage({
  action: "remove_group",
  groupName: "OldGroup"
})
```

### Addressables Build

```javascript
// Build
mcp__unity-mcp-server__addressables_build({
  action: "build",
  buildTarget: "StandaloneWindows64"
})

// Clean build (delete cache then build)
mcp__unity-mcp-server__addressables_build({
  action: "clean_build"
})
```

### Addressables Analysis

```javascript
// Detect duplicate assets
mcp__unity-mcp-server__addressables_analyze({
  action: "analyze_duplicates",
  pageSize: 20
})

// Analyze dependencies
mcp__unity-mcp-server__addressables_analyze({
  action: "analyze_dependencies",
  assetPath: "Assets/Prefabs/Player.prefab"
})

// Detect unused assets
mcp__unity-mcp-server__addressables_analyze({
  action: "analyze_unused",
  pageSize: 50
})
```

## Import Settings

### Get Import Settings

```javascript
mcp__unity-mcp-server__manage_asset_import_settings({
  action: "get",
  assetPath: "Assets/Textures/Player.png"
})
```

### Texture Settings

```javascript
mcp__unity-mcp-server__manage_asset_import_settings({
  action: "modify",
  assetPath: "Assets/Textures/Player.png",
  settings: {
    maxTextureSize: 1024,
    textureCompression: "Compressed",
    filterMode: "Bilinear",
    generateMipMaps: true,
    sRGBTexture: true
  }
})
```

### Audio Settings

```javascript
mcp__unity-mcp-server__manage_asset_import_settings({
  action: "modify",
  assetPath: "Assets/Audio/BGM.mp3",
  settings: {
    loadType: "Streaming",
    compressionFormat: "Vorbis",
    quality: 0.7,
    sampleRateSetting: "PreserveSampleRate"
  }
})
```

### Apply Preset

```javascript
// Apply saved preset
mcp__unity-mcp-server__manage_asset_import_settings({
  action: "apply_preset",
  assetPath: "Assets/Textures/UI_Icon.png",
  preset: "UISprite"
})
```

### Reimport

```javascript
mcp__unity-mcp-server__manage_asset_import_settings({
  action: "reimport",
  assetPath: "Assets/Textures/Player.png"
})
```

## Common Workflows

### Prefab Workflow

```javascript
// 1. Build GameObject in scene
mcp__unity-mcp-server__create_gameobject({
  name: "NewEnemy",
  primitiveType: "capsule"
})

mcp__unity-mcp-server__add_component({
  gameObjectPath: "/NewEnemy",
  componentType: "Rigidbody"
})

// 2. Convert to prefab
mcp__unity-mcp-server__create_prefab({
  prefabPath: "Assets/Prefabs/Enemies/NewEnemy.prefab",
  gameObjectPath: "/NewEnemy"
})

// 3. Delete original in scene
mcp__unity-mcp-server__delete_gameobject({
  path: "/NewEnemy"
})

// 4. Instantiate from prefab
mcp__unity-mcp-server__instantiate_prefab({
  prefabPath: "Assets/Prefabs/Enemies/NewEnemy.prefab",
  position: { x: 0, y: 0, z: 0 }
})
```

### Material Variations

```javascript
// Create base material
mcp__unity-mcp-server__create_material({
  materialPath: "Assets/Materials/Enemy_Base.mat",
  shader: "Standard",
  properties: {
    "_Metallic": 0.2,
    "_Glossiness": 0.5
  }
})

// Create variations
const colors = [
  { name: "Red", color: [1, 0, 0, 1] },
  { name: "Blue", color: [0, 0, 1, 1] },
  { name: "Green", color: [0, 1, 0, 1] }
]

for (const variant of colors) {
  mcp__unity-mcp-server__create_material({
    materialPath: `Assets/Materials/Enemy_${variant.name}.mat`,
    copyFrom: "Assets/Materials/Enemy_Base.mat",
    properties: { "_Color": variant.color }
  })
}
```

### Addressables Setup

```javascript
// 1. Create group
mcp__unity-mcp-server__addressables_manage({
  action: "create_group",
  groupName: "Characters"
})

// 2. Add assets
mcp__unity-mcp-server__addressables_manage({
  action: "add_entry",
  assetPath: "Assets/Prefabs/Player.prefab",
  groupName: "Characters",
  address: "player",
  labels: ["player", "controllable"]
})

mcp__unity-mcp-server__addressables_manage({
  action: "add_entry",
  assetPath: "Assets/Prefabs/NPC.prefab",
  groupName: "Characters",
  address: "npc_villager",
  labels: ["npc", "friendly"]
})

// 3. Build
mcp__unity-mcp-server__addressables_build({
  action: "build"
})

// 4. Analyze
mcp__unity-mcp-server__addressables_analyze({
  action: "analyze_duplicates"
})
```

## Common Mistakes

### 1. Prefab Path Format

```javascript
// ❌ No extension
prefabPath: "Assets/Prefabs/Player"

// ✅ .prefab extension required
prefabPath: "Assets/Prefabs/Player.prefab"

// ❌ Not starting with Assets
prefabPath: "Prefabs/Player.prefab"

// ✅ Start with Assets/
prefabPath: "Assets/Prefabs/Player.prefab"
```

### 2. Material Path Format

```javascript
// ❌ No extension
materialPath: "Assets/Materials/Red"

// ✅ .mat extension required
materialPath: "Assets/Materials/Red.mat"
```

### 3. Forgetting to Exit Prefab Mode

```javascript
// ✅ Always exit prefab mode
mcp__unity-mcp-server__open_prefab({ prefabPath: "..." })
// ... edit ...
mcp__unity-mcp-server__exit_prefab_mode({ saveChanges: true })
```

### 4. Forgetting to Refresh

```javascript
// After modifying files externally
// ✅ Refresh to reflect changes
mcp__unity-mcp-server__manage_asset_database({
  action: "refresh"
})
```

### 5. Addressables Group Not Created

```javascript
// ❌ Adding entry to non-existent group
mcp__unity-mcp-server__addressables_manage({
  action: "add_entry",
  groupName: "NonExistent",  // Error
  ...
})

// ✅ Create group first
mcp__unity-mcp-server__addressables_manage({
  action: "create_group",
  groupName: "NewGroup"
})

mcp__unity-mcp-server__addressables_manage({
  action: "add_entry",
  groupName: "NewGroup",
  ...
})
```

## Tool Reference

| Tool | Purpose |
|------|---------|
| `create_prefab` | Create prefab |
| `open_prefab` | Start prefab mode |
| `exit_prefab_mode` | End prefab mode |
| `save_prefab` | Save prefab |
| `instantiate_prefab` | Instantiate prefab |
| `modify_prefab` | Modify prefab |
| `create_material` | Create material |
| `modify_material` | Modify material |
| `manage_asset_database` | Asset DB operations |
| `analyze_asset_dependencies` | Dependency analysis |
| `manage_asset_import_settings` | Import settings |
| `addressables_manage` | Addressables management |
| `addressables_build` | Addressables build |
| `addressables_analyze` | Addressables analysis |
