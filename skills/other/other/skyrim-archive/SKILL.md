---
name: skyrim-archive
description: Read, extract, create, and edit BSA/BA2 archives. Use when the user wants to package mod assets, extract files from existing mods, inspect archive contents, or modify archives (add/remove/replace files).
---

# Skyrim Archive Module

Read, extract, and create BSA/BA2 archives using Spooky's AutoMod Toolkit.

## Prerequisites

Run all commands from the toolkit directory:
```bash
cd "<TOOLKIT_PATH>"
# Example: cd "C:\Tools\spookys-automod-toolkit"
```

## External Tools

| Tool | Purpose | Auto-Download |
|------|---------|---------------|
| BSArch | Create/extract archives | No - manual install |

### Installing BSArch
1. Download xEdit from [GitHub releases](https://github.com/TES5Edit/TES5Edit/releases)
2. Extract the archive
3. Copy `BSArch.exe` to `tools/bsarch/` in the toolkit directory

Check tool status:
```bash
dotnet run --project src/SpookysAutomod.Cli -- archive status
```

## Command Reference

### Check Tool Status
```bash
dotnet run --project src/SpookysAutomod.Cli -- archive status
```

### Get Archive Info
```bash
dotnet run --project src/SpookysAutomod.Cli -- archive info "<archive>"
```
Output includes: Archive type, version, file count, total size.

### List Archive Contents
```bash
dotnet run --project src/SpookysAutomod.Cli -- archive list "<archive>" [options]
```
| Option | Default | Description |
|--------|---------|-------------|
| `--filter`, `-f` | - | Filter pattern (e.g., `*.nif`, `textures/*`) |
| `--limit` | 100 | Max files to list (0 = all) |

### Extract Archive
```bash
dotnet run --project src/SpookysAutomod.Cli -- archive extract "<archive>" --output "<dir>" [options]
```
| Option | Description |
|--------|-------------|
| `--output`, `-o` | Output directory |
| `--filter`, `-f` | Filter pattern for files to extract |

**Requires:** BSArch tool installed

### Create Archive
```bash
dotnet run --project src/SpookysAutomod.Cli -- archive create "<directory>" --output "<file>" [options]
```
| Option | Default | Description |
|--------|---------|-------------|
| `--output`, `-o` | Required | Output archive path |
| `--compress` | true | Compress archive contents |
| `--game` | `sse` | Game type: `sse`, `le`, `fo4`, `fo76` |

**Requires:** BSArch tool installed

### Add Files to Archive
```bash
dotnet run --project src/SpookysAutomod.Cli -- archive add-files "<archive>" --files <file1> <file2> ... [options]
```
| Option | Default | Description |
|--------|---------|-------------|
| `--files` | Required | Files to add to the archive |
| `--base-dir` | Auto-detect | Base directory for calculating relative paths |
| `--preserve-compression` | true | Keep original compression settings |

**Requires:** BSArch tool installed
**Note:** Automatically detects common parent directory to preserve folder structure

### Remove Files from Archive
```bash
dotnet run --project src/SpookysAutomod.Cli -- archive remove-files "<archive>" --filter "<pattern>" [options]
```
| Option | Default | Description |
|--------|---------|-------------|
| `--filter` | Required | Filter pattern (e.g., `*.esp`, `scripts/*`) |
| `--preserve-compression` | true | Keep original compression settings |

**Requires:** BSArch tool installed

### Replace Files in Archive
```bash
dotnet run --project src/SpookysAutomod.Cli -- archive replace-files "<archive>" --source "<directory>" [options]
```
| Option | Default | Description |
|--------|---------|-------------|
| `--source` | Required | Directory with replacement files |
| `--filter` | - | Filter pattern for files to replace |
| `--preserve-compression` | true | Keep original compression settings |

**Requires:** BSArch tool installed

### Update Single File
```bash
dotnet run --project src/SpookysAutomod.Cli -- archive update-file "<archive>" --file "<target>" --source "<file>" [options]
```
| Option | Default | Description |
|--------|---------|-------------|
| `--file` | Required | Target file path in archive (e.g., `scripts/MyScript.pex`) |
| `--source` | Required | Source file to update with |
| `--preserve-compression` | true | Keep original compression settings |

**Requires:** BSArch tool installed
**Note:** Convenience wrapper for single file updates

### Extract Single File
```bash
dotnet run --project src/SpookysAutomod.Cli -- archive extract-file "<archive>" --file "<target>" --output "<path>"
```
| Option | Default | Description |
|--------|---------|-------------|
| `--file` | Required | File path in archive to extract |
| `--output` | Required | Output file path |

**Requires:** BSArch tool installed
**Note:** Faster than full extraction for single file access

### Merge Archives
```bash
dotnet run --project src/SpookysAutomod.Cli -- archive merge <archive1> <archive2> ... --output "<file>" [options]
```
| Option | Default | Description |
|--------|---------|-------------|
| `--output` | Required | Output merged archive path |
| `--compress` | true | Compress merged archive |

**Requires:** BSArch tool installed
**Note:** Later archives overwrite earlier ones on conflict

### Validate Archive
```bash
dotnet run --project src/SpookysAutomod.Cli -- archive validate "<archive>"
```

**Requires:** BSArch tool installed (for info/list commands only)
**Note:** Checks if archive is readable and reports issues/warnings

### Optimize Archive
```bash
dotnet run --project src/SpookysAutomod.Cli -- archive optimize "<archive>" [options]
```
| Option | Default | Description |
|--------|---------|-------------|
| `--output` | Original | Output path (defaults to overwriting original) |
| `--compress` | true | Enable compression |

**Requires:** BSArch tool installed
**Note:** Repacks archive with compression, reports size savings

### Compare Archives
```bash
dotnet run --project src/SpookysAutomod.Cli -- archive diff "<archive1>" "<archive2>"
```

**Requires:** BSArch tool installed (for list commands only)
**Note:** Shows added, removed, and modified files between versions

## Common Workflows

### Inspect Existing Mod Archive
```bash
# Get archive info
dotnet run --project src/SpookysAutomod.Cli -- archive info "SomeMod.bsa"

# List first 100 files
dotnet run --project src/SpookysAutomod.Cli -- archive list "SomeMod.bsa"

# List all NIF meshes
dotnet run --project src/SpookysAutomod.Cli -- archive list "SomeMod.bsa" --filter "*.nif"

# List all textures
dotnet run --project src/SpookysAutomod.Cli -- archive list "SomeMod.bsa" --filter "textures/*"

# List all scripts
dotnet run --project src/SpookysAutomod.Cli -- archive list "SomeMod.bsa" --filter "*.pex"
```

### Extract Mod for Analysis/Editing
```bash
# Extract entire archive
dotnet run --project src/SpookysAutomod.Cli -- archive extract "SomeMod.bsa" --output "./Extracted"

# Extract only textures
dotnet run --project src/SpookysAutomod.Cli -- archive extract "SomeMod.bsa" --output "./Extracted" --filter "textures/*"

# Extract only meshes
dotnet run --project src/SpookysAutomod.Cli -- archive extract "SomeMod.bsa" --output "./Extracted" --filter "*.nif"

# Extract only scripts for decompilation
dotnet run --project src/SpookysAutomod.Cli -- archive extract "SomeMod.bsa" --output "./Extracted" --filter "scripts/*"
```

### Package Mod as BSA
```bash
# 1. Organize files in Data structure
# MyModData/
#   meshes/mymod/weapon.nif
#   textures/mymod/weapon.dds
#   scripts/MyMod_Script.pex

# 2. Create compressed SSE archive
dotnet run --project src/SpookysAutomod.Cli -- archive create "./MyModData" --output "MyMod.bsa"

# 3. Create uncompressed archive (faster loading)
dotnet run --project src/SpookysAutomod.Cli -- archive create "./MyModData" --output "MyMod.bsa" --compress false

# 4. Create LE-compatible archive
dotnet run --project src/SpookysAutomod.Cli -- archive create "./MyModData" --output "MyMod.bsa" --game le
```

### Archive Editing Workflows

#### Add New Files to Existing Archive
```bash
# Add new mesh and texture to existing mod archive
dotnet run --project src/SpookysAutomod.Cli -- archive add-files "MyMod.bsa" \
  --files "meshes/mymod/newweapon.nif" "textures/mymod/newweapon.dds"

# Archive is updated with new files while preserving existing content
```

#### Remove Deprecated Files from Archive
```bash
# Remove all ESP files (if mod was converted to ESL)
dotnet run --project src/SpookysAutomod.Cli -- archive remove-files "MyMod.bsa" --filter "*.esp"

# Remove old scripts folder
dotnet run --project src/SpookysAutomod.Cli -- archive remove-files "MyMod.bsa" --filter "scripts/old/*"

# Remove specific file
dotnet run --project src/SpookysAutomod.Cli -- archive remove-files "MyMod.bsa" --filter "deprecated.txt"
```

#### Update Scripts in Archive
```bash
# Recompiled scripts and need to update them in archive
# 1. Compile updated scripts
dotnet run --project src/SpookysAutomod.Cli -- papyrus compile "./Source" --output "./CompiledScripts"

# 2. Replace scripts in archive
dotnet run --project src/SpookysAutomod.Cli -- archive replace-files "MyMod.bsa" \
  --source "./CompiledScripts" \
  --filter "*.pex"

# Only files that exist in archive are replaced
```

#### Patch Mod Archive
```bash
# Create patch with updated assets
# 1. Extract files you want to update
dotnet run --project src/SpookysAutomod.Cli -- archive extract "OriginalMod.bsa" \
  --output "./Patch" \
  --filter "textures/armor/*"

# 2. Modify the extracted textures (use external tools)

# 3. Replace textures in archive
dotnet run --project src/SpookysAutomod.Cli -- archive replace-files "OriginalMod.bsa" \
  --source "./Patch" \
  --filter "textures/armor/*"
```

#### Quick Single File Operations
```bash
# Update just one script after recompiling
dotnet run --project src/SpookysAutomod.Cli -- archive update-file "MyMod.bsa" \
  --file "scripts/MainScript.pex" \
  --source "./MainScript.pex"

# Extract just one file for inspection
dotnet run --project src/SpookysAutomod.Cli -- archive extract-file "MyMod.bsa" \
  --file "scripts/MainScript.pex" \
  --output "./MainScript.pex"
```

#### Merge Multiple Mod Archives
```bash
# Combine base mod + patches into single archive
dotnet run --project src/SpookysAutomod.Cli -- archive merge \
  "MyMod-Base.bsa" \
  "MyMod-Patch1.bsa" \
  "MyMod-Patch2.bsa" \
  --output "MyMod-Complete.bsa"

# Later archives overwrite earlier ones on conflict
```

#### Archive Maintenance
```bash
# Check archive integrity before distribution
dotnet run --project src/SpookysAutomod.Cli -- archive validate "MyMod.bsa"

# Optimize old archive with compression
dotnet run --project src/SpookysAutomod.Cli -- archive optimize "OldMod.bsa" \
  --output "OldMod-Optimized.bsa"

# Compare two versions to see what changed
dotnet run --project src/SpookysAutomod.Cli -- archive diff \
  "MyMod-v1.bsa" \
  "MyMod-v2.bsa"
```

### Troubleshooting Workflow
```bash
# 1. Check what's in a broken mod's BSA
dotnet run --project src/SpookysAutomod.Cli -- archive list "BrokenMod.bsa" --limit 0

# 2. Extract everything for analysis
dotnet run --project src/SpookysAutomod.Cli -- archive extract "BrokenMod.bsa" --output "./Debug"

# 3. Analyze plugin structuredotnet run --project src/SpookysAutomod.Cli -- esp analyze "./Debug/BrokenMod.esp" --json

# 4. Check mesh textures
dotnet run --project src/SpookysAutomod.Cli -- nif textures "./Debug/meshes/SomeMesh.nif"

# 5. Decompile scripts
dotnet run --project src/SpookysAutomod.Cli -- papyrus decompile "./Debug/scripts" --output "./Debug/Source"
```

### Complete Mod Modification Workflow
```bash
# 1. Extract existing mod
dotnet run --project src/SpookysAutomod.Cli -- archive extract "OriginalMod.bsa" --output "./ModWork"

# 2. Analyze plugin to understand structure
dotnet run --project src/SpookysAutomod.Cli -- esp analyze "./ModWork/OriginalMod.esp"

# 3. Decompile scripts for modification
dotnet run --project src/SpookysAutomod.Cli -- papyrus decompile "./ModWork/scripts" --output "./ModWork/Source"

# 4. Make changes (edit PSC files, modify plugin records, etc.)

# 5. Recompile modified scripts
dotnet run --project src/SpookysAutomod.Cli -- papyrus compile "./ModWork/Source" --output "./ModWork/scripts" --headers "./skyrim-script-headers"

# 6. Repackage as BSA
dotnet run --project src/SpookysAutomod.Cli -- archive create "./ModWork" --output "ModifiedMod.bsa"
```

## Directory Structure for Packaging

The source directory should mirror Skyrim's Data folder:
```
MyModData/
  meshes/
    mymod/
      weapon.nif
      armor.nif
  textures/
    mymod/
      weapon.dds
      weapon_n.dds
      armor.dds
  scripts/
    MyMod_MainScript.pex
    MyMod_EffectScript.pex
  sound/
    fx/
      mymod/
        sound.wav
```

## Archive Types

### BSA (Bethesda Softworks Archive)
- Used by: Skyrim LE, Skyrim SE
- Magic: `BSA\0`
- Supports compression
- Best for general mod assets

### BA2 (Bethesda Archive 2)
- Used by: Fallout 4, Fallout 76
- Magic: `BTDX`
- Two storage types: General, Textures
- Better compression for textures

### Game Type Selection

| Game | Flag | Notes |
|------|------|-------|
| `sse` | Skyrim SE/AE | Default, most common |
| `le` | Skyrim LE | Older format |
| `fo4` | Fallout 4 | BA2 format |
| `fo76` | Fallout 76 | BA2 format |

## Common Issues

### BSArch Not Found
```bash
# Check status
dotnet run --project src/SpookysAutomod.Cli -- archive status

# Follow installation instructions if missing
```

### Wrong Archive Format
- SSE mods need SSE archives (`--game sse`)
- LE mods need LE archives (`--game le`)
- Using wrong format causes purple textures or crashes

### Missing Files After Packaging
- Ensure correct directory structure
- Files must be in proper subfolders (meshes/, textures/, etc.)
- Case sensitivity may matter

## Important Notes

1. **BSArch required** for create/extract/edit - info/list work without it
2. **Match archive to game** - SSE and LE use different formats
3. **Directory structure matters** - Must mirror Data folder
4. **Compression trade-off** - Smaller files but slower loading
5. **Archive editing** - add-files, remove-files, and replace-files use extract-modify-repack workflow (may take time for large archives)
6. **Preserve compression** - By default, editing operations preserve the original archive compression settings
7. **Use `--json` flag** for machine-readable output when scripting

## JSON Output

All commands support `--json` for structured output:
```bash
dotnet run --project src/SpookysAutomod.Cli -- archive info "MyMod.bsa" --json
```

Example response:
```json
{
  "success": true,
  "result": {
    "fileName": "MyMod.bsa",
    "type": "BSA",
    "version": "105",
    "fileCount": 150,
    "fileSize": 52428800
  }
}
```
