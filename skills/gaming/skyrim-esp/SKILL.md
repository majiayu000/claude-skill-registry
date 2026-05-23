---
name: skyrim-esp
description: Create and modify Skyrim plugin files (.esp/.esl). Use when the user wants to create a mod, add weapons, armor, spells, perks, books, quests, NPCs, factions, globals, leveled lists, encounter zones, locations, outfits, or form lists to a plugin. Includes quest aliases, script property management, type inspection, and detailed analysis. Also use when the user wants to view existing records, create override patches, search for records across plugins, manage perk conditions, compare record versions, or detect load order conflicts. Eliminates need for xEdit for viewing and patching operations.
---

# Skyrim ESP Module

Create, inspect, and modify Skyrim plugin files using the ESP module of Spooky's AutoMod Toolkit.

## Prerequisites

Run all commands from the toolkit directory:
```bash
cd "<TOOLKIT_PATH>"
# Example: cd "C:\Tools\spookys-automod-toolkit"
```

## Command Reference

### Create a Plugin
```bash
dotnet run --project src/SpookysAutomod.Cli -- esp create "<name>.esp" [options]
```
| Option | Description |
|--------|-------------|
| `--light` | Create as ESL-flagged light plugin |
| `--author "Name"` | Set author in header |
| `--output "./path"` | Output directory |

### Inspect a Plugin
```bash
dotnet run --project src/SpookysAutomod.Cli -- esp info "<plugin>"
dotnet run --project src/SpookysAutomod.Cli -- esp list-masters "<plugin>"
```

### Add Records

**Books** (work immediately, no model needed):
```bash
dotnet run --project src/SpookysAutomod.Cli -- esp add-book "<plugin>" "<editorId>" --name "Name" --text "Content..." --value 50
```

**Weapons** (require `--model` to be visible):
```bash
dotnet run --project src/SpookysAutomod.Cli -- esp add-weapon "<plugin>" "<editorId>" --name "Name" --type sword --damage 25 --model iron-sword
```
Model presets: `iron-sword`, `steel-sword`, `iron-dagger`, `hunting-bow`

**Armor** (require `--model` to be visible):
```bash
dotnet run --project src/SpookysAutomod.Cli -- esp add-armor "<plugin>" "<editorId>" --name "Name" --type heavy --slot body --rating 40 --model iron-cuirass
```
Model presets: `iron-cuirass`, `iron-helmet`, `iron-gauntlets`, `iron-boots`, `iron-shield`

**Spells** (require `--effect` to function):
```bash
dotnet run --project src/SpookysAutomod.Cli -- esp add-spell "<plugin>" "<editorId>" --name "Name" --effect damage-health --magnitude 50 --cost 45
```
Effect presets: `damage-health`, `restore-health`, `damage-magicka`, `restore-magicka`, `damage-stamina`, `restore-stamina`, `fortify-health`, `fortify-magicka`, `fortify-stamina`, `fortify-armor`, `fortify-attack`

**Perks** (require `--effect` to function):
```bash
dotnet run --project src/SpookysAutomod.Cli -- esp add-perk "<plugin>" "<editorId>" --name "Name" --description "Effect" --effect weapon-damage --bonus 25 --playable
```
Effect presets: `weapon-damage`, `damage-reduction`, `armor`, `spell-cost`, `spell-power`, `spell-duration`, `sneak-attack`, `pickpocket`, `prices`

**Quests**:
```bash
dotnet run --project src/SpookysAutomod.Cli -- esp add-quest "<plugin>" "<editorId>" --name "Name" --start-enabled
```

**Globals** (configuration variables):
```bash
dotnet run --project src/SpookysAutomod.Cli -- esp add-global "<plugin>" "<editorId>" --type float --value 1.5
```

**NPCs** (record only - need race/face data for visibility):
```bash
dotnet run --project src/SpookysAutomod.Cli -- esp add-npc "<plugin>" "<editorId>" --name "Name" --level 20 --essential
```

**Factions** (for tracking and organization):
```bash
dotnet run --project src/SpookysAutomod.Cli -- esp add-faction "<plugin>" "<editorId>" --name "Name" --flags "HiddenFromPC,TrackCrime"
```

**LeveledItems** (for random loot distribution):
```bash
# With preset
dotnet run --project src/SpookysAutomod.Cli -- esp add-leveled-item "<plugin>" "<editorId>" --preset low-treasure

# Custom with entries (format: item,level,count)
dotnet run --project src/SpookysAutomod.Cli -- esp add-leveled-item "<plugin>" "<editorId>" --chance-none 15 --add-entry "GoldBase,1,100" --add-entry "LockPick,5,3"

# Guaranteed multi-item drop
dotnet run --project src/SpookysAutomod.Cli -- esp add-leveled-item "<plugin>" "<editorId>" --use-all --add-entry "Sword,10,1" --add-entry "Shield,10,1"
```
Presets: `low-treasure` (25% none), `medium-treasure` (15% none), `high-treasure` (5% none), `guaranteed-loot` (0% none)

**FormLists** (for script property collections):
```bash
# Add vanilla forms by FormKey
dotnet run --project src/SpookysAutomod.Cli -- esp add-form-list "<plugin>" "<editorId>" --add-form "Skyrim.esm:0x000896"

# Add mod forms by EditorID
dotnet run --project src/SpookysAutomod.Cli -- esp add-form-list "<plugin>" "<editorId>" --add-form "MyWeapon01" --add-form "MyWeapon02"

# Use in scripts: FormList Property MyList Auto
# Set property: --property MyList --value "ModName.esp|0x800"
```

**EncounterZones** (for level scaling control):
```bash
# With preset
dotnet run --project src/SpookysAutomod.Cli -- esp add-encounter-zone "<plugin>" "<editorId>" --preset mid-level

# Custom with flags
dotnet run --project src/SpookysAutomod.Cli -- esp add-encounter-zone "<plugin>" "<editorId>" --min-level 30 --max-level 50 --never-resets

# Fully scaling (1-unlimited)
dotnet run --project src/SpookysAutomod.Cli -- esp add-encounter-zone "<plugin>" "<editorId>" --preset scaling
```
Presets: `low-level` (1-10), `mid-level` (10-30), `high-level` (30-50), `scaling` (1-unlimited)
Flags: `--never-resets` (enemies stay dead), `--disable-combat-boundary` (NPCs pursue anywhere)

**Locations** (for quest markers and fast travel):
```bash
# With preset
dotnet run --project src/SpookysAutomod.Cli -- esp add-location "<plugin>" "<editorId>" --name "The Rusty Tankard" --preset inn

# With parent location
dotnet run --project src/SpookysAutomod.Cli -- esp add-location "<plugin>" "<editorId>" --name "My Shop" --preset dwelling --parent-location "WhiterunHoldLocation"

# Custom keywords
dotnet run --project src/SpookysAutomod.Cli -- esp add-location "<plugin>" "<editorId>" --name "Special Place" --add-keyword "LocTypeCity"
```
Presets: `inn` (LocTypeInn), `city` (LocTypeCity), `dungeon` (LocTypeDungeon), `dwelling` (LocTypeDwelling)

**Outfits** (for NPC equipment sets):
```bash
# With preset
dotnet run --project src/SpookysAutomod.Cli -- esp add-outfit "<plugin>" "<editorId>" --preset guard

# Custom items
dotnet run --project src/SpookysAutomod.Cli -- esp add-outfit "<plugin>" "<editorId>" --add-item "ArmorIronCuirass" --add-item "WeaponIronSword"
```
Presets: `guard` (iron armor + sword + shield), `farmer` (clothes), `mage` (robes + hood), `thief` (leather armor)

### Quest Aliases
Quest aliases enable dynamic tracking of NPCs, objects, or locations. Essential for follower frameworks.

**Add Alias with Script:**
```bash
dotnet run --project src/SpookysAutomod.Cli -- esp add-alias "<plugin>" --quest "<questId>" --name "<aliasName>" --script "<scriptName>" --flags "Optional,AllowReuseInQuest"
```

**Attach Script to Existing Alias:**
```bash
dotnet run --project src/SpookysAutomod.Cli -- esp attach-alias-script "<plugin>" --quest "<questId>" --alias "<aliasName>" --script "<scriptName>"
```

Common flags: `Optional`, `AllowReuseInQuest`, `AllowReserved`, `Essential`, `Protected`

### Script Management

**Attach Script to Quest:**
```bash
dotnet run --project src/SpookysAutomod.Cli -- esp attach-script "<plugin>" --quest "<questId>" --script "<scriptName>"
```

**Set Script Property Manually:**
```bash
dotnet run --project src/SpookysAutomod.Cli -- esp set-property "<plugin>" --quest "<questId>" --script "<scriptName>" --property "<propName>" --value "<formId>" --type object
```

**Auto-Fill Properties (RECOMMENDED):**
```bash
# Single script - parses PSC file and fills vanilla properties
dotnet run --project src/SpookysAutomod.Cli -- esp auto-fill "<plugin>" --quest "<questId>" --script "<scriptName>" --psc-file "<path>" --data-folder "<skyrim-data-path>"

# Bulk auto-fill ALL scripts (5x faster for multiple scripts)
dotnet run --project src/SpookysAutomod.Cli -- esp auto-fill-all "<plugin>" --script-dir "<source-dir>" --data-folder "<skyrim-data-path>"
```

**What Auto-Fill Does:**
- Parses PSC files to extract property names and types
- Searches Skyrim.esm with type-aware filtering
- Automatically fills matching vanilla properties
- Prevents wrong matches (e.g., Location vs Keyword with similar names)
- Supports array properties (creates ScriptObjectListProperty)

### Analysis & Inspection

**Basic Info:**
```bash
dotnet run --project src/SpookysAutomod.Cli -- esp info "<plugin>"
dotnet run --project src/SpookysAutomod.Cli -- esp list-masters "<plugin>"
```

**Type Inspection (Debug Mutagen Types):**
```bash
dotnet run --project src/SpookysAutomod.Cli -- esp debug-types "<pattern>" --json
```
Examples: `QuestAlias`, `Quest*`, `--all`

### Dry-Run Mode
Preview changes without saving:
```bash
dotnet run --project src/SpookysAutomod.Cli -- esp add-weapon "<plugin>" "<id>" --name "Test" --damage 30 --model iron-sword --dry-run --json
```

Available on all `add-*` commands.

### SEQ File Generation

Required for start-enabled quests:
```bash
dotnet run --project src/SpookysAutomod.Cli -- esp generate-seq "<plugin>" --output "./SEQ"
```

### Merge Plugins
```bash
dotnet run --project src/SpookysAutomod.Cli -- esp merge "<source>.esp" "<target>.esp" --output "Merged.esp"
```

## Record Viewing and Override System

View, analyze, and create override patches for existing records without xEdit.

### View Record Details
```bash
# View by EditorID (requires --type)
dotnet run --project src/SpookysAutomod.Cli -- esp view-record "<plugin>" --editor-id "<id>" --type <type>

# View by FormID (type inferred)
dotnet run --project src/SpookysAutomod.Cli -- esp view-record "<plugin>" --form-id "<formid>"
```
**Supported Types:** spell, weapon, armor, quest, npc, perk, faction, book, miscitem, global, leveleditem, formlist, outfit, location, encounterzone

### Create Override Patches
```bash
# Create override patch (copies record to new plugin)
dotnet run --project src/SpookysAutomod.Cli -- esp create-override "<source>.esp" -o "<patch>.esp" --editor-id "<id>" --type <type>
```
The patch automatically:
- Adds source as master reference
- Preserves FormKey from original
- Loads after source in load order (wins conflicts)

### Search for Records
```bash
# Search by pattern
dotnet run --project src/SpookysAutomod.Cli -- esp find-record --search "<pattern>" --type <type> --plugin "<plugin>"

# Search across all plugins in Data folder
dotnet run --project src/SpookysAutomod.Cli -- esp find-record --search "<pattern>" --type <type> --data-folder "C:/Skyrim/Data" --all-plugins
```

### Batch Override Multiple Records
```bash
# Create overrides for all matching records
dotnet run --project src/SpookysAutomod.Cli -- esp batch-override "<source>.esp" -o "<patch>.esp" --search "<pattern>*" --type <type>

# Override specific records by EditorID list
dotnet run --project src/SpookysAutomod.Cli -- esp batch-override "<source>.esp" -o "<patch>.esp" --type <type> --editor-ids "ID1,ID2,ID3"
```

### Compare Records
```bash
# Compare same record in two plugins
dotnet run --project src/SpookysAutomod.Cli -- esp compare-record "<plugin1>.esp" "<plugin2>.esp" --editor-id "<id>" --type <type>
```

### Detect Conflicts
```bash
# Find which plugins modify a specific record
dotnet run --project src/SpookysAutomod.Cli -- esp conflicts "<data-folder>" --editor-id "<id>" --type <type>

# Check all conflicts for a plugin
dotnet run --project src/SpookysAutomod.Cli -- esp conflicts "<data-folder>" --plugin "<plugin>.esp"
```

### Condition Management (Perks Only)

**Note:** Conditions only work on Perk, Package, IdleAnimation, and MagicEffect records.

**List Conditions:**
```bash
dotnet run --project src/SpookysAutomod.Cli -- esp list-conditions "<plugin>" --editor-id "<perkId>" --type perk
```

**Add Condition:**
```bash
# Add level requirement
dotnet run --project src/SpookysAutomod.Cli -- esp add-condition "<source>.esp" -o "<patch>.esp" --editor-id "<perkId>" --type perk --function GetLevel

# Common functions: GetLevel, IsSneaking, IsRunning, IsSwimming, IsInCombat
```

**Remove Conditions:**
```bash
# Remove conditions by index (get indices from list-conditions)
dotnet run --project src/SpookysAutomod.Cli -- esp remove-condition "<source>.esp" -o "<patch>.esp" --editor-id "<perkId>" --type perk --indices "0,2"
```

## Common Workflows

### Create a Complete Weapon Mod
```bash
# 1. Create plugin
dotnet run --project src/SpookysAutomod.Cli -- esp create "MyWeaponMod.esp" --light --author "YourName"

# 2. Add weapon with model
dotnet run --project src/SpookysAutomod.Cli -- esp add-weapon "MyWeaponMod.esp" "MyWeapon_Sword" --name "Blade of Power" --type sword --damage 35 --value 500 --model iron-sword

# 3. Verify
dotnet run --project src/SpookysAutomod.Cli -- esp info "MyWeaponMod.esp"
```

### Create a Spell Pack
```bash
# Create plugin
dotnet run --project src/SpookysAutomod.Cli -- esp create "SpellPack.esp" --light

# Add damage spell
dotnet run --project src/SpookysAutomod.Cli -- esp add-spell "SpellPack.esp" "SP_Fireball" --name "Greater Fireball" --effect damage-health --magnitude 75 --cost 60

# Add healing spell
dotnet run --project src/SpookysAutomod.Cli -- esp add-spell "SpellPack.esp" "SP_Heal" --name "Major Healing" --effect restore-health --magnitude 100 --cost 50

# Add buff spell
dotnet run --project src/SpookysAutomod.Cli -- esp add-spell "SpellPack.esp" "SP_Fortify" --name "Warrior's Blessing" --effect fortify-health --magnitude 50 --duration 120 --cost 80
```

### Create a Perk Overhaul
```bash
# Create plugin
dotnet run --project src/SpookysAutomod.Cli -- esp create "PerkMod.esp" --light

# Combat perks
dotnet run --project src/SpookysAutomod.Cli -- esp add-perk "PerkMod.esp" "PM_WeaponMaster" --name "Weapon Master" --description "+20% weapon damage" --effect weapon-damage --bonus 20 --playable

# Magic perks
dotnet run --project src/SpookysAutomod.Cli -- esp add-perk "PerkMod.esp" "PM_Efficiency" --name "Magical Efficiency" --description "Spells cost 25% less" --effect spell-cost --bonus 25 --playable

# Stealth perks
dotnet run --project src/SpookysAutomod.Cli -- esp add-perk "PerkMod.esp" "PM_Assassin" --name "Assassin's Strike" --description "3x sneak attack damage" --effect sneak-attack --bonus 200 --playable
```

### Add Content to Existing Mod
```bash
# Check what's in the mod
dotnet run --project src/SpookysAutomod.Cli -- esp info "ExistingMod.esp"

# Add new content
dotnet run --project src/SpookysAutomod.Cli -- esp add-weapon "ExistingMod.esp" "NewWeapon" --name "Added Sword" --damage 30 --model steel-sword

# Verify addition
dotnet run --project src/SpookysAutomod.Cli -- esp info "ExistingMod.esp"
```

### Create a Dungeon with Level Scaling
```bash
# Create plugin
dotnet run --project src/SpookysAutomod.Cli -- esp create "DungeonMod.esp" --light

# Create location
dotnet run --project src/SpookysAutomod.Cli -- esp add-location "DungeonMod.esp" "DM_Crypt" --name "Forgotten Crypt" --preset dungeon

# Create encounter zone
dotnet run --project src/SpookysAutomod.Cli -- esp add-encounter-zone "DungeonMod.esp" "DM_CryptZone" --preset mid-level --never-resets

# Create boss loot
dotnet run --project src/SpookysAutomod.Cli -- esp add-leveled-item "DungeonMod.esp" "DM_BossChest" --preset high-treasure

# Verify
dotnet run --project src/SpookysAutomod.Cli -- esp info "DungeonMod.esp"
```

### Create NPCs with Custom Outfits
```bash
# Create plugin
dotnet run --project src/SpookysAutomod.Cli -- esp create "NPCMod.esp" --light

# Create custom outfit
dotnet run --project src/SpookysAutomod.Cli -- esp add-outfit "NPCMod.esp" "NM_GuardOutfit" --preset guard

# Create faction
dotnet run --project src/SpookysAutomod.Cli -- esp add-faction "NPCMod.esp" "NM_TownGuards" --name "Town Guards"

# Create NPC (outfit assigned in Creation Kit)
dotnet run --project src/SpookysAutomod.Cli -- esp add-npc "NPCMod.esp" "NM_GuardCaptain" --name "Captain Smith" --level 20 --essential
```

### Create Form List for Script Property
```bash
# Create plugin
dotnet run --project src/SpookysAutomod.Cli -- esp create "ScriptHelpers.esp" --light

# Create form list with weapons
dotnet run --project src/SpookysAutomod.Cli -- esp add-form-list "ScriptHelpers.esp" "SH_AllWeapons" --add-form "MyWeapon01" --add-form "MyWeapon02"

# In your script, declare: FormList Property AllWeapons Auto
# Then auto-fill or manually set: --property AllWeapons --value "ScriptHelpers.esp|0x800"
```

## Important Notes

1. **Always use `--model`** for weapons and armor - without it they'll be invisible
2. **Always use `--effect`** for spells and perks - without it they won't function
3. **EditorIDs must be unique** - use a prefix like `MyMod_` to avoid conflicts
4. **Light plugins (.esl)** have a 2048 record limit but don't use a load order slot
5. **Start-enabled quests require SEQ files** - generate with `generate-seq` command
6. **Use `--json` flag** for machine-readable output when scripting

## JSON Output

All commands support `--json` for structured output:
```bash
dotnet run --project src/SpookysAutomod.Cli -- esp info "MyMod.esp" --json
```
