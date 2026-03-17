---
name: skyrim-mcm
description: Create and edit MCM Helper configuration files for mod settings menus. Use when the user wants to add in-game settings, configuration options, toggles, sliders, or dropdowns to their mod.
---

# Skyrim MCM Module

Create and edit MCM Helper configuration files for in-game mod settings menus using Spooky's AutoMod Toolkit.

## Prerequisites

Run all commands from the toolkit directory:
```bash
cd "<TOOLKIT_PATH>"
# Example: cd "C:\Tools\spookys-automod-toolkit"
```

## Overview

MCM (Mod Configuration Menu) allows mods to have in-game settings menus. This module generates JSON configuration files compatible with [MCM Helper](https://www.nexusmods.com/skyrimspecialedition/mods/53000).

## Command Reference

### Create MCM Configuration
```bash
dotnet run --project src/SpookysAutomod.Cli -- mcm create "<modName>" "<displayName>" --output "<file>"
```
| Option | Description |
|--------|-------------|
| `<modName>` | Internal mod name (no spaces, used for file paths) |
| `<displayName>` | Display name shown in MCM menu |
| `--output`, `-o` | Output file path |

### Get MCM Info
```bash
dotnet run --project src/SpookysAutomod.Cli -- mcm info "<config>"
```

### Validate MCM Configuration
```bash
dotnet run --project src/SpookysAutomod.Cli -- mcm validate "<config>"
```

### Add Toggle (Checkbox)
```bash
dotnet run --project src/SpookysAutomod.Cli -- mcm add-toggle "<config>" "<id>" "<text>" [options]
```
| Option | Description |
|--------|-------------|
| `<config>` | Path to config.json |
| `<id>` | Control identifier (e.g., `bEnabled`) |
| `<text>` | Display text |
| `--help-text` | Help text shown on hover |
| `--page` | Target page name |

### Add Slider
```bash
dotnet run --project src/SpookysAutomod.Cli -- mcm add-slider "<config>" "<id>" "<text>" --min <n> --max <n> [options]
```
| Option | Default | Description |
|--------|---------|-------------|
| `<config>` | Required | Path to config.json |
| `<id>` | Required | Control identifier (e.g., `fDamage`) |
| `<text>` | Required | Display text |
| `--min` | 0 | Minimum value |
| `--max` | 100 | Maximum value |
| `--step` | 1 | Step increment |

## Common Workflows

### Create Basic Mod Settings
```bash
# 1. Create the MCM config
dotnet run --project src/SpookysAutomod.Cli -- mcm create "MyMod" "My Awesome Mod" --output "./MCM/config/MyMod/config.json"

# 2. Add an enable toggle
dotnet run --project src/SpookysAutomod.Cli -- mcm add-toggle "./MCM/config/MyMod/config.json" "bEnabled" "Enable Mod" --help-text "Turn the mod on or off"

# 3. Add a debug toggle
dotnet run --project src/SpookysAutomod.Cli -- mcm add-toggle "./MCM/config/MyMod/config.json" "bDebugMode" "Debug Mode" --help-text "Show debug messages"

# 4. Add a damage multiplier slider
dotnet run --project src/SpookysAutomod.Cli -- mcm add-slider "./MCM/config/MyMod/config.json" "fDamageMultiplier" "Damage Multiplier" --min 0.5 --max 3.0 --step 0.1

# 5. Validate the configuration
dotnet run --project src/SpookysAutomod.Cli -- mcm validate "./MCM/config/MyMod/config.json"
```

### Create Multi-Page Settings
```bash
# Create config
dotnet run --project src/SpookysAutomod.Cli -- mcm create "MyMod" "My Mod" --output "./MCM/config.json"

# Add controls to "General" page (default)
dotnet run --project src/SpookysAutomod.Cli -- mcm add-toggle "./MCM/config.json" "bEnabled" "Enable Mod"

# Add controls to "Combat" page
dotnet run --project src/SpookysAutomod.Cli -- mcm add-slider "./MCM/config.json" "fDamage" "Damage Bonus" --min 0 --max 100 --page "Combat"
dotnet run --project src/SpookysAutomod.Cli -- mcm add-toggle "./MCM/config.json" "bCritical" "Enable Criticals" --page "Combat"

# Add controls to "Magic" page
dotnet run --project src/SpookysAutomod.Cli -- mcm add-slider "./MCM/config.json" "fSpellCost" "Spell Cost Reduction" --min 0 --max 50 --page "Magic"
```

### Validate and Check Existing MCM
```bash
# Check MCM structure
dotnet run --project src/SpookysAutomod.Cli -- mcm info "./MCM/config/SomeMod/config.json"

# Validate for errors
dotnet run --project src/SpookysAutomod.Cli -- mcm validate "./MCM/config/SomeMod/config.json"
```

## MCM Helper Integration

### Required File Structure
MCM Helper expects files in specific locations:
```
Data/
  MCM/
    config/
      MyMod/
        config.json     # Main config (required)
        settings.ini    # Default values (optional)
    translations/
      MyMod_english.txt # Translations (optional)
```

### Config JSON Format
Generated config.json structure:
```json
{
  "modName": "MyMod",
  "displayName": "My Awesome Mod",
  "minMcmVersion": 7,
  "pages": [
    {
      "pageDisplayName": "Main",
      "content": [
        {
          "type": "toggle",
          "id": "bEnabled",
          "text": "Enable Mod"
        },
        {
          "type": "slider",
          "id": "fDamage",
          "text": "Damage Multiplier",
          "min": 0.5,
          "max": 2.0,
          "step": 0.1
        }
      ]
    }
  ]
}
```

### Control Types

| Type | Description | Properties |
|------|-------------|------------|
| toggle | Checkbox | id, text, help |
| slider | Value slider | id, text, min, max, step |
| dropdown | Dropdown list | id, text, options |
| keymap | Key binding | id, text |
| text | Text input | id, text |

### Linking MCM to Scripts

MCM values are stored as GlobalVariables in your plugin:
```papyrus
ScriptName MyMod_ConfigScript extends Quest

; These must match the MCM control IDs
GlobalVariable Property bEnabled Auto
GlobalVariable Property fDamageMultiplier Auto

Function ApplySettings()
    If bEnabled.GetValue() == 1
        float damage = fDamageMultiplier.GetValue()
        ; Apply settings...
    EndIf
EndFunction
```

## Naming Conventions

### Control IDs
Follow Hungarian notation for clarity:
- `bSomething` - Boolean toggles
- `fSomething` - Float sliders
- `iSomething` - Integer values
- `sSomething` - String values

### Examples
- `bEnabled` - Main enable toggle
- `bDebugMode` - Debug mode toggle
- `fDamageMultiplier` - Damage multiplier (float)
- `iItemCount` - Item count (integer)
- `fSpellCostReduction` - Spell cost reduction percentage

## Important Notes

1. **MCM Helper required** - Users must have MCM Helper installed
2. **GlobalVariables must exist** - Create matching globals in your plugin
3. **File location matters** - Place config in `Data/MCM/config/ModName/`
4. **Validate before release** - Always run validate command
5. **Use `--json` flag** for machine-readable output when scripting

## Complete MCM + Plugin Workflow (Basic)

```bash
# 1. Create the plugin
dotnet run --project src/SpookysAutomod.Cli -- esp create "MyConfigMod.esp" --light

# 2. Add globals that match MCM controls
dotnet run --project src/SpookysAutomod.Cli -- esp add-global "MyConfigMod.esp" "bEnabled" --type long --value 1
dotnet run --project src/SpookysAutomod.Cli -- esp add-global "MyConfigMod.esp" "fDamageMultiplier" --type float --value 1.0

# 3. Create MCM config
dotnet run --project src/SpookysAutomod.Cli -- mcm create "MyConfigMod" "My Config Mod" --output "./MCM/config/MyConfigMod/config.json"

# 4. Add matching controls
dotnet run --project src/SpookysAutomod.Cli -- mcm add-toggle "./MCM/config/MyConfigMod/config.json" "bEnabled" "Enable Mod"
dotnet run --project src/SpookysAutomod.Cli -- mcm add-slider "./MCM/config/MyConfigMod/config.json" "fDamageMultiplier" "Damage Multiplier" --min 0.5 --max 2.0 --step 0.1

# 5. Validate
dotnet run --project src/SpookysAutomod.Cli -- mcm validate "./MCM/config/MyConfigMod/config.json"
```

## Complete MCM + Script Workflow with Auto-Fill
```bash
# 1. Create the plugin and quest
dotnet run --project src/SpookysAutomod.Cli -- esp create "MyConfigMod.esp" --light
dotnet run --project src/SpookysAutomod.Cli -- esp add-quest "MyConfigMod.esp" "MyConfigQuest" --start-enabled

# 2. Add globals that match MCM controls
dotnet run --project src/SpookysAutomod.Cli -- esp add-global "MyConfigMod.esp" "bEnabled" --type long --value 1
dotnet run --project src/SpookysAutomod.Cli -- esp add-global "MyConfigMod.esp" "fDamageMultiplier" --type float --value 1.0
dotnet run --project src/SpookysAutomod.Cli -- esp add-global "MyConfigMod.esp" "bDebugMode" --type long --value 0

# 3. Create script that references these globals
cat > "./Scripts/Source/MyConfigScript.psc" << 'EOF'
ScriptName MyConfigScript extends Quest

GlobalVariable Property bEnabled Auto
GlobalVariable Property fDamageMultiplier Auto
GlobalVariable Property bDebugMode Auto

Event OnInit()
    RegisterForSingleUpdate(1.0)
EndEvent

Event OnUpdate()
    If bEnabled.GetValue() == 1
        float mult = fDamageMultiplier.GetValue()
        If bDebugMode.GetValue() == 1
            Debug.Notification("Damage multiplier: " + mult)
        EndIf
    EndIf
    RegisterForSingleUpdate(5.0)
EndEvent
EOF

# 4. Compile script
dotnet run --project src/SpookysAutomod.Cli -- papyrus compile "./Scripts/Source/MyConfigScript.psc" --output "./Scripts" --headers "./skyrim-script-headers"

# 5. Attach script to quest
dotnet run --project src/SpookysAutomod.Cli -- esp attach-script "MyConfigMod.esp" --quest "MyConfigQuest" --script "MyConfigScript"

# 6. Auto-fill script properties from PSC (links globals automatically!)
dotnet run --project src/SpookysAutomod.Cli -- esp auto-fill "MyConfigMod.esp" --quest "MyConfigQuest" --script "MyConfigScript" --psc-file "./Scripts/Source/MyConfigScript.psc" --data-folder "C:/Skyrim/Data"

# Output:
# Filled property 'bEnabled' with MyConfigMod.esp:0x000800
# Filled property 'fDamageMultiplier' with MyConfigMod.esp:0x000801
# Filled property 'bDebugMode' with MyConfigMod.esp:0x000802

# 7. Create MCM config
dotnet run --project src/SpookysAutomod.Cli -- mcm create "MyConfigMod" "My Config Mod" --output "./MCM/config/MyConfigMod/config.json"

# 8. Add matching MCM controls
dotnet run --project src/SpookysAutomod.Cli -- mcm add-toggle "./MCM/config/MyConfigMod/config.json" "bEnabled" "Enable Mod"
dotnet run --project src/SpookysAutomod.Cli -- mcm add-slider "./MCM/config/MyConfigMod/config.json" "fDamageMultiplier" "Damage Multiplier" --min 0.5 --max 2.0 --step 0.1
dotnet run --project src/SpookysAutomod.Cli -- mcm add-toggle "./MCM/config/MyConfigMod/config.json" "bDebugMode" "Debug Mode"

# 9. Validate MCM
dotnet run --project src/SpookysAutomod.Cli -- mcm validate "./MCM/config/MyConfigMod/config.json"

# 10. Generate SEQ file (required for start-enabled quest)
dotnet run --project src/SpookysAutomod.Cli -- esp generate-seq "MyConfigMod.esp" --output "./SEQ"
```

**Why This Workflow Matters:**
- Auto-fill automatically links the GlobalVariable properties in your script to the actual globals in your plugin
- No manual property filling in Creation Kit required
- Type-safe matching ensures correct globals are linked
- Works with your own plugin's globals, not just vanilla Skyrim records

## JSON Output

All commands support `--json` for structured output:
```bash
dotnet run --project src/SpookysAutomod.Cli -- mcm info "./config.json" --json
```
