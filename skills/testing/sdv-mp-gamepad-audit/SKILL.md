---
name: sdv-mp-gamepad-audit
description: This skill should be used when the user asks to "check multiplayer support", "audit gamepad navigation", "verify split-screen", or before committing changes to menu code. Also use when working on per-player state, mutex locking, PerScreen usage, controller navigation, or any file in the Managers/ or Menus/ directories.
version: 1.0.0
---

# SDV Multiplayer & Gamepad Audit

Static analysis for multiplayer and gamepad support. Since runtime testing of these features is difficult, this skill provides comprehensive code auditing to catch issues before manual testing.

## When to Run This Audit

1. Before committing changes to any file in `Managers/` or `Menus/`
2. After adding new state variables (fields, properties)
3. When implementing features that affect multiple players
4. Before PR creation

## Multiplayer Audit Checklist

### 1. PerScreen Wrapper Audit

All per-player mutable state MUST use `PerScreen<T>`:

```csharp
// WRONG: Static state shared across split-screen players
private static MenuManager menuManager;
private static int currentTab = 0;

// CORRECT: Per-screen state
private static readonly PerScreen<MenuManager> menuManager = new();
private static readonly PerScreen<int> currentTab = new(() => 0);

// Access via .Value
menuManager.Value.DoSomething();
int tab = currentTab.Value;
```

**Audit Points:**
- [ ] All static fields with mutable state use PerScreen<T>
- [ ] PerScreen fields are `readonly` (prevents clearing all screens)
- [ ] PerScreen initialized with proper factory if needed: `new(() => defaultValue)`
- [ ] Manager classes use PerScreen in the entry point

### 2. Context Checks

Verify proper context gating:

```csharp
// Required before accessing world state
if (!Context.IsWorldReady) return;

// Required before player interaction logic
if (!Context.IsPlayerFree) return;

// Required for host-only operations
if (!Context.IsMainPlayer) return;

// Required for save operations
if (Context.IsMainPlayer)
{
    Helper.Data.WriteSaveData("key", data);
}
```

**Audit Points:**
- [ ] Event handlers check `Context.IsWorldReady` before accessing `Game1.player`
- [ ] Save operations check `Context.IsMainPlayer` (farmhands can't use save API)
- [ ] Menu operations check `Context.IsPlayerFree` when appropriate

### 3. Mutex Locking (Shared Furniture)

Dressers and other shared furniture require mutex:

```csharp
// CORRECT: Request lock before opening menu
if (!dresser.mutex.IsLocked())
{
    dresser.mutex.RequestLock(delegate {
        Game1.activeClickableMenu = new WardrobeMenu();
    });
}

// CRITICAL: Release on menu close
public override void emergencyShutDown()
{
    base.emergencyShutDown();
    dresserObject?.mutex?.ReleaseLock();
}

protected override void cleanupBeforeExit()
{
    base.cleanupBeforeExit();
    dresserObject?.mutex?.ReleaseLock();
}
```

**Audit Points:**
- [ ] Shared furniture access uses `mutex.RequestLock()`
- [ ] Menu `emergencyShutDown()` releases mutex
- [ ] Menu `cleanupBeforeExit()` releases mutex
- [ ] Null checks on mutex before release

### 4. Player Data Keying

Per-player save data must be uniquely keyed:

```csharp
// CORRECT: Unique key per player, per save, per multiplayer session
string dataPath = $"data/favoritesData/{Game1.player.Name}_{Constants.SaveFolderName}_{Game1.player.UniqueMultiplayerID}.json";

// Also valid for modData (always prefix with mod ID)
Game1.player.modData[$"{ModId}/PlayerFlag"] = "true";
```

**Audit Points:**
- [ ] Save paths include player identifier AND save folder AND multiplayer ID
- [ ] modData keys prefixed with mod's UniqueID
- [ ] No assumptions that data paths are unique without proper keying

### 5. Location Iteration

Use utilities that work for farmhands:

```csharp
// WRONG: Misses some locations for farmhands
foreach (var loc in Game1.locations) { }

// CORRECT: Works for all players
Utility.ForAllLocations(loc => {
    // process location
});
```

## Gamepad Audit Checklist

### 1. ClickableComponent Navigation

Every clickable element needs navigation IDs:

```csharp
var button = new ClickableComponent(bounds, "name");
button.myID = 1001;                    // REQUIRED: Unique ID
button.leftNeighborID = 1000;          // Left neighbor (or -99999 for none)
button.rightNeighborID = 1002;         // Right neighbor
button.upNeighborID = 900;             // Up neighbor
button.downNeighborID = 1100;          // Down neighbor
```

**Audit Points:**
- [ ] Every ClickableComponent has `myID` set
- [ ] Every ClickableComponent has all four `neighborID`s set
- [ ] IDs are unique within the menu
- [ ] Navigation forms logical grid (no dead ends)
- [ ] Use -99999 for "no neighbor" (not 0 or -1)

### 2. Component List Population

```csharp
public override void populateClickableComponentList()
{
    base.populateClickableComponentList();
    allClickableComponents.AddRange(labels);
    allClickableComponents.AddRange(buttons);
    allClickableComponents.AddRange(equipmentIcons);
    // Add ALL clickable elements
}
```

**Audit Points:**
- [ ] `populateClickableComponentList()` adds all components
- [ ] `snapToDefaultClickableComponent()` called after population
- [ ] Components not added after initial setup (or list repopulated)

### 3. Focus Management

```csharp
public override void snapToDefaultClickableComponent()
{
    base.snapToDefaultClickableComponent();
    currentlySnappedComponent = getComponentWithID(defaultFocusId);
    snapCursorToCurrentSnappedComponent();
}
```

**Audit Points:**
- [ ] Menu has a logical default focus element
- [ ] Focus returns to sensible element after actions
- [ ] Child menus properly handle focus transfer

### 4. Button Hints

For important actions, show controller button hints:

```csharp
// In draw():
if (Game1.options.gamepadControls)
{
    // Draw A button hint next to action button
    b.Draw(Game1.controllerMaps, position, sourceRect, Color.White);
}
```

## Audit Output Format

When running this audit, report findings as:

```
## Multiplayer Audit Results

### Issues Found

1. **PerScreen Missing** - `Managers/MenuManager.cs:45`
   - Field `currentCategory` is static but not wrapped in PerScreen<T>
   - Fix: Change to `private static readonly PerScreen<string> currentCategory = new();`

2. **Mutex Not Released** - `Menus/WardrobeMenu.cs:312`
   - `emergencyShutDown()` doesn't release mutex
   - Fix: Add `dresserObject?.mutex?.ReleaseLock();`

### Gamepad Navigation Issues

1. **Missing neighborID** - `Menus/FavoritesMenu.cs:189`
   - `deleteButton` has no `upNeighborID` set
   - Fix: Add `deleteButton.upNeighborID = renameButton.myID;`

### Passed Checks
- [x] All PerScreen fields are readonly
- [x] Context.IsWorldReady checks present in event handlers
- [x] Save operations check Context.IsMainPlayer
```

## Quick Reference

### Split-Screen Player Access
```csharp
// Current screen's value
var current = perScreenField.Value;

// Specific screen's value
var screen0 = perScreenField.GetValueForScreen(0);

// Current screen ID
int screenId = Context.ScreenId;
```

### Common Navigation ID Ranges
```csharp
// Use ranges to organize IDs
const int LABELS = 10000;
const int BUTTONS = 20000;
const int CATEGORIES = 30000;
const int OUTFIT_CARDS = 40000;

// Then: button.myID = BUTTONS + index;
```
