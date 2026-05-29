---
name: sdv-data-validation
description: This skill should be used when the user asks to "validate data structures", "check save format", "update config options", or discusses data persistence. Also use when modifying FavoritesModel.cs, ModConfig.cs, modData conventions, JSON save files, or when preparing migrations for breaking changes.
version: 1.0.0
---

# SDV Data Validation

Validate data structures and prevent regressions in save formats, config, and modData conventions.

## When to Use This Skill

1. Modifying `Models/FavoritesModel.cs` (FavoritesData, FavoriteOutfit)
2. Modifying `ModConfig.cs`
3. Changing modData key conventions
4. Adding new save data fields
5. Before commits affecting data persistence

## Data Structure Validation

### FavoritesData Schema

```csharp
public class FavoritesData
{
    public List<FavoriteOutfit> Favorites { get; set; }
}

public class FavoriteOutfit
{
    // Metadata
    public bool isFavorite { get; set; } = false;
    public string Name { get; set; } = "";
    public string Category { get; set; } = "";  // Spring/Summer/Fall/Winter/Special
    public int LastWorn { get; set; } = 0;

    // Item references (modData tags)
    public Dictionary<string, string> Items { get; set; }
    // Keys: "Hat", "Shirt", "Pants", "Shoes", "LeftRing", "RightRing"
    // Values: modData tag like "Hat_abc123"

    // Item IDs (for recreation)
    public Dictionary<string, string> ItemIds { get; set; }
    // Keys: "Hat", "Shirt", "Pants", "Shoes", "LeftRing", "RightRing"
    // Values: QualifiedItemId like "(H)6", "(S)1001"

    // Dye colors
    public Dictionary<string, string> ItemColors { get; set; }
    // Keys: "Shirt", "Pants" (only dyeable items)
    // Values: "R,G,B,A" format

    // Appearance
    public string HairIndex { get; set; } = "";
    public int Hair { get; set; } = 0;
    public string AccessoryIndex { get; set; } = "";
    public int Accessory { get; set; } = 0;
}
```

### Validation Checks

**Required Fields:**
- [ ] `Name` is non-null (can be empty)
- [ ] `Category` is valid: "Spring", "Summer", "Fall", "Winter", or "Special"
- [ ] `Items` dictionary is non-null
- [ ] `ItemIds` dictionary is non-null
- [ ] `ItemColors` dictionary is non-null

**Item References:**
- [ ] Item keys are valid slot names: "Hat", "Shirt", "Pants", "Shoes", "LeftRing", "RightRing"
- [ ] ItemIds values are valid QualifiedItemIds (start with type prefix)
- [ ] ItemColors values match "R,G,B,A" format

**Data Integrity:**
- [ ] If Items has a slot, ItemIds should have the same slot
- [ ] ItemColors only contains keys for dyeable items ("Shirt", "Pants")

## ModConfig Validation

### Current Schema

```csharp
public sealed class ModConfig
{
    public bool StartingDresser { get; set; } = true;
    public bool RobinSellsDressers { get; set; } = true;
    public bool TravelingMerchantSellsDressers { get; set; } = true;
    public bool IncludeRingsInOutfits { get; set; } = true;
    public bool IncludeFacialHair { get; set; } = false;
    public bool IncludeModdedHairstyles { get; set; } = true;
    public bool IncludeModdedAccessories { get; set; } = true;
    public DresserSharingMode DresserInventorySharing { get; set; } = DresserSharingMode.Touching;
}

public enum DresserSharingMode { Individual, Touching, SameBuilding }
```

### Validation Checks

**When adding new config options:**
- [ ] Added to `ModConfig.cs` with proper default value
- [ ] Added to GMCM registration in `StardewOutfitManager.cs`
- [ ] Default value matches intended behavior
- [ ] XML documentation added

**GMCM Registration Pattern:**
```csharp
api.AddBoolOption(
    mod: ModManifest,
    name: () => "Option Name",
    tooltip: () => "Description of what this does",
    getValue: () => Config.OptionName,
    setValue: v => Config.OptionName = v
);
```

## ModData Key Conventions

### Correct Format

```csharp
// Prefix with mod's UniqueID
item.modData[$"{ModId}/FavoriteItem"] = "value";

// This mod's convention (from manifest.json: LiminalWarmth.StardewOutfitManager)
item.modData["LiminalWarmth.StardewOutfitManager/FavoriteItem"] = $"{item.Name}_{Guid.NewGuid()}";
```

### Validation Checks

- [ ] All modData keys start with `LiminalWarmth.StardewOutfitManager/`
- [ ] No legacy keys without prefix (migration needed if found)
- [ ] Keys are consistent across codebase

### Migration for Legacy Keys

If old keys exist without prefix:

```csharp
// Check for legacy key and migrate
if (item.modData.TryGetValue("StardewOutfitManagerFavoriteItem", out string legacyValue))
{
    // Migrate to new key
    item.modData[$"{ModId}/FavoriteItem"] = legacyValue;
    item.modData.Remove("StardewOutfitManagerFavoriteItem");
}
```

## Save File Paths

### Correct Pattern

```csharp
// Unique per player, per save, per multiplayer session
string path = $"data/favoritesData/{Game1.player.Name}_{Constants.SaveFolderName}_{Game1.player.UniqueMultiplayerID}.json";

// Use Helper.Data API
Helper.Data.WriteJsonFile<FavoritesData>(path, data);
var loaded = Helper.Data.ReadJsonFile<FavoritesData>(path);
```

### Validation Checks

- [ ] Path includes player name
- [ ] Path includes save folder
- [ ] Path includes multiplayer ID
- [ ] Using `Helper.Data` API (not raw file I/O)

## Breaking Change Migration

When making breaking changes to data structures:

### 1. Identify Breaking Changes

Examples of breaking changes:
- Renaming a property
- Changing a property type
- Removing a required field
- Changing dictionary key format

### 2. Create Migration Code

```csharp
private FavoritesData MigrateData(FavoritesData data, int fromVersion)
{
    // Version 1 -> 2: Renamed "Outfit" to "Items"
    if (fromVersion < 2)
    {
        foreach (var outfit in data.Favorites)
        {
            // Migration logic
        }
    }

    // Version 2 -> 3: Added ItemColors
    if (fromVersion < 3)
    {
        foreach (var outfit in data.Favorites)
        {
            outfit.ItemColors ??= new Dictionary<string, string>();
        }
    }

    return data;
}
```

### 3. Handle Null/Missing Fields

Always use null-safe access:

```csharp
// WRONG: Assumes Items exists
var hatTag = outfit.Items["Hat"];

// CORRECT: Null-safe
if (outfit.Items?.TryGetValue("Hat", out string hatTag) == true)
{
    // Use hatTag
}

// Also initialize missing dictionaries on load
outfit.Items ??= new Dictionary<string, string>();
outfit.ItemIds ??= new Dictionary<string, string>();
outfit.ItemColors ??= new Dictionary<string, string>();
```

## Audit Output Format

```
## Data Validation Results

### Schema Issues
- [ ] FavoriteOutfit.Category allows invalid values (no validation)
- [ ] Missing null check for Items dictionary in LoadFavorites

### Config Issues
- [ ] New option `DebugMode` not registered in GMCM

### ModData Key Issues
- [ ] Legacy key "StardewOutfitManagerFavoriteItem" found in FavoritesMethods.cs:45
  - Fix: Migrate to "LiminalWarmth.StardewOutfitManager/FavoriteItem"

### Breaking Changes
- [ ] Property renamed from `Outfit` to `Items` - migration required

### Passed Checks
- [x] All config options have defaults
- [x] Save paths include all required components
- [x] ItemIds use valid QualifiedItemId format
```

## Quick Reference

### Valid QualifiedItemId Prefixes
```
(O)   Object
(BC)  BigCraftable
(F)   Furniture
(W)   Weapon
(B)   Boots
(H)   Hat
(P)   Pants
(S)   Shirt
(T)   Tool
(TR)  Trinket
(R)   Ring
```

### Valid Category Values
```
"Spring"
"Summer"
"Fall"
"Winter"
"Special"
```

### Valid Item Slot Keys
```
"Hat"
"Shirt"
"Pants"
"Shoes"
"LeftRing"
"RightRing"
```
