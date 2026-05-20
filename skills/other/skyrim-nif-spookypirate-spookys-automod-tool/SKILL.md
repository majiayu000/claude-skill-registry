---
name: skyrim-nif
description: Read and manipulate NIF 3D mesh files. Use when the user wants to inspect meshes, find texture paths, scale models, or troubleshoot invisible items.
---

# Skyrim NIF Module

Read and manipulate NIF (NetImmerse Format) 3D mesh files using Spooky's AutoMod Toolkit.

## Prerequisites

Run all commands from the toolkit directory:
```bash
cd "<TOOLKIT_PATH>"
# Example: cd "C:\Tools\spookys-automod-toolkit"
```

## Overview

NIF files are the 3D model format used by Skyrim for meshes (weapons, armor, architecture, etc.). This module provides read capabilities and basic transformations.

**Note:** This module cannot create new meshes from scratch. For that, use Blender with the NifTools addon.

## Command Reference

### Get NIF Info
```bash
dotnet run --project src/SpookysAutomod.Cli -- nif info "<nif>"
```
Output includes: Filename, file size, header string, NIF version.

### List Textures
```bash
dotnet run --project src/SpookysAutomod.Cli -- nif textures "<nif>"
```
Lists all texture paths referenced in the mesh.

### Scale Mesh
```bash
dotnet run --project src/SpookysAutomod.Cli -- nif scale "<nif>" <factor> [options]
```
| Option | Default | Description |
|--------|---------|-------------|
| `<factor>` | Required | Scale factor (1.5 = 150%, 0.5 = 50%) |
| `--output`, `-o` | input file | Output file path |

### Copy NIF
```bash
dotnet run --project src/SpookysAutomod.Cli -- nif copy "<nif>" --output "<file>"
```
Copies and validates the NIF file.

## Common Workflows

### Inspect Mesh for Troubleshooting
```bash
# Get basic info about a mesh
dotnet run --project src/SpookysAutomod.Cli -- nif info "./Meshes/Weapons/Iron/IronSword.nif"

# Find what textures it uses
dotnet run --project src/SpookysAutomod.Cli -- nif textures "./Meshes/Weapons/Iron/IronSword.nif"
```

Example texture output:
```
Textures (3):
  textures\weapons\iron\ironsword.dds
  textures\weapons\iron\ironsword_n.dds
  textures\weapons\iron\ironsword_s.dds
```

### Scale Weapon/Armor
```bash
# Make weapon 50% larger
dotnet run --project src/SpookysAutomod.Cli -- nif scale "./Meshes/weapon.nif" 1.5 --output "./Meshes/weapon_large.nif"

# Make weapon 50% smaller
dotnet run --project src/SpookysAutomod.Cli -- nif scale "./Meshes/weapon.nif" 0.5 --output "./Meshes/weapon_small.nif"

# Double the size
dotnet run --project src/SpookysAutomod.Cli -- nif scale "./Meshes/weapon.nif" 2.0 --output "./Meshes/weapon_huge.nif"
```

### Find Missing Textures
```bash
# 1. Extract BSA to get meshes
dotnet run --project src/SpookysAutomod.Cli -- archive extract "SomeMod.bsa" --output "./Extracted"

# 2. Check what textures a mesh needs
dotnet run --project src/SpookysAutomod.Cli -- nif textures "./Extracted/meshes/myarmor.nif"

# 3. Verify those textures exist in the extracted files
# If missing, that explains purple/missing textures in-game
```

### Troubleshoot Invisible Items
```bash
# 1. Check if mesh file exists and is valid
dotnet run --project src/SpookysAutomod.Cli -- nif info "./Meshes/MyWeapon.nif"

# 2. If info fails, mesh is corrupted or wrong format

# 3. If info succeeds, check texture paths
dotnet run --project src/SpookysAutomod.Cli -- nif textures "./Meshes/MyWeapon.nif"

# 4. Common causes of invisible items:
#    - Mesh file not found (wrong path in ESP)
#    - Mesh is wrong format (LE vs SE)
#    - Textures missing
```

## NIF Format Information

### Skyrim NIF Versions
| Game | NIF Version | Notes |
|------|-------------|-------|
| Skyrim LE | 20.2.0.7 | Older format |
| Skyrim SE/AE | 20.2.0.7 | BSTriShape optimized |
| Fallout 4 | 20.2.0.7 | Different shaders |

### Common Node Types
| Node | Purpose |
|------|---------|
| BSFadeNode | Root node for meshes |
| NiTriShape | Triangle geometry (LE) |
| BSTriShape | Optimized geometry (SE) |
| BSLightingShaderProperty | Material/shader info |
| NiSkinInstance | Skinning for animated meshes |

### Texture Slots
| Slot | Suffix | Purpose |
|------|--------|---------|
| Diffuse | none / _d | Base color |
| Normal | _n | Normal map (bumpiness) |
| Specular | _s | Specular/gloss |
| Glow | _g | Emissive/glow |
| Cube Map | _e | Environment reflections |

## Vanilla Mesh Paths

Useful vanilla mesh paths for `--model` option in ESP module:

### Weapons
```
Weapons\Iron\IronSword.nif
Weapons\Iron\IronDagger.nif
Weapons\Iron\IronWarAxe.nif
Weapons\Iron\IronMace.nif
Weapons\Iron\IronBattleaxe.nif
Weapons\Iron\IronGreatsword.nif
Weapons\Iron\IronWarhammer.nif
Weapons\Bow\HuntingBow.nif
Weapons\Staff\Staff.nif
```

### Armor
```
Armor\Iron\Male\IronCuirass_1.nif
Armor\Iron\Male\IronHelmet.nif
Armor\Iron\Male\IronGauntlets.nif
Armor\Iron\Male\IronBoots.nif
Armor\Iron\IronShield.nif
```

## Limitations

This module **CAN**:
- Read NIF file information
- List referenced textures
- Scale meshes uniformly
- Copy/validate NIF files

This module **CANNOT**:
- Create new meshes from scratch
- Edit mesh geometry (vertices, faces)
- Retexture meshes (change texture paths)
- Create or edit rigging/skinning
- Convert between NIF versions (LE to SE)

For advanced mesh editing, use:
- **Blender** + **NifTools** addon - Full mesh creation/editing
- **NifSkope** - Direct NIF editing
- **Cathedral Assets Optimizer** - LE to SE conversion

## Important Notes

1. **LE vs SE meshes** - SE uses optimized BSTriShape, not compatible with LE
2. **Texture paths are relative** - Start from Data folder (e.g., `textures\weapons\...`)
3. **Case sensitivity** - Windows ignores case, but be consistent
4. **Scale affects all nodes** - Uniform scaling only
5. **Use `--json` flag** for machine-readable output when scripting

## JSON Output

All commands support `--json` for structured output:
```bash
dotnet run --project src/SpookysAutomod.Cli -- nif info "./Meshes/weapon.nif" --json
```

Example responses:
```json
{
  "success": true,
  "result": {
    "fileName": "weapon.nif",
    "fileSize": 45678,
    "version": "20.2.0.7",
    "headerString": "Gamebryo File Format, Version 20.2.0.7"
  }
}
```

Textures response:
```json
{
  "success": true,
  "result": {
    "textures": [
      "textures\\weapons\\iron\\ironsword.dds",
      "textures\\weapons\\iron\\ironsword_n.dds"
    ]
  }
}
```
