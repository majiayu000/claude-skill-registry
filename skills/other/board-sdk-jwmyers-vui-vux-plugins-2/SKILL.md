---
name: board-sdk
description: This skill should be used when the user asks about "touch input", "BoardInput", "BoardContact", "piece detection", "glyph", "glyph recognition", "simulator", "Board hardware", "contact phases", "Piece Set", "touch system", "Board SDK", "multi-touch", "noise rejection", or discusses Board hardware integration and input handling.
version: 0.3.0
---

# Board SDK Integration

Expert knowledge of the Board SDK for Unity, enabling touch input, piece detection, and hardware integration for the Board multi-touch display.

## Board Hardware Overview

Board is a specialized multi-touch display with:

- **Unlimited touch tracking** - No 10-touch limit
- **ML-powered piece recognition** - Physical game pieces with conductive glyphs
- **Noise rejection** - Filters palms, wrists, elbows automatically
- **1920×1080 resolution** - 16:9 landscape display

## Core Concepts

### Contact Types (BoardContactType)

| Type       | Value | Description                                           |
| ---------- | ----- | ----------------------------------------------------- |
| **Finger** | 0     | Standard touch point from a finger                    |
| **Glyph**  | 1     | Contact from a physical Piece with conductive pattern |
| **Blob**   | 2     | Reserved for future use                               |

### Contact Phases (BoardContactPhase)

| Phase        | Value | Description                     |
| ------------ | ----- | ------------------------------- |
| `None`       | 0     | Default state, no activity      |
| `Began`      | 1     | Contact started this frame      |
| `Moved`      | 2     | Position or orientation changed |
| `Ended`      | 3     | Lifted from surface             |
| `Canceled`   | 4     | Tracking interrupted            |
| `Stationary` | 5     | Held in place, no change        |

**IMPORTANT:** Handle `Stationary` in addition to `Began`/`Moved`/`Ended`. A glyph placed directly without movement triggers `Began` then `Stationary` (not `Moved`). This is critical for piece placement detection.

### Pieces and Glyphs

- **Piece**: Physical object with conductive glyph on base (no electronics)
- **Glyph**: Unique pattern identifying the Piece
- **Piece Set**: Collection of Pieces trained together (one active at a time)
- **Model**: `.tflite` ML file for recognizing a Piece Set

## SDK Components

### BoardInput (Touch Input)

Primary input API for contacts and glyphs:

```csharp
using Board.Input;

// Get all active contacts of a type
BoardContact[] fingers = BoardInput.GetActiveContacts(BoardContactType.Finger);
BoardContact[] pieces = BoardInput.GetActiveContacts(BoardContactType.Glyph);

// Get all contacts regardless of type
BoardContact[] all = BoardInput.GetActiveContacts();
```

### BoardContact Properties

| Property                 | Type              | Description                                              |
| ------------------------ | ----------------- | -------------------------------------------------------- |
| `contactId`              | int               | Unique contact ID (persistent during lifecycle)          |
| `screenPosition`         | Vector2           | Current position in screen pixels (1920×1080)            |
| `previousScreenPosition` | Vector2           | Position in previous frame                               |
| `bounds`                 | Rect              | Screen-space bounding rect                               |
| `phase`                  | BoardContactPhase | Current lifecycle state                                  |
| `type`                   | BoardContactType  | Finger, Glyph, or Blob                                   |
| `timestamp`              | double            | When contact began/mutated (Time.realtimeSinceStartup)   |
| `orientation`            | float             | Rotation in radians clockwise from vertical (Glyph only) |
| `previousOrientation`    | float             | Orientation in previous frame (Glyph only)               |
| `isTouched`              | bool              | Finger touching the Piece (Glyph only)                   |
| `glyphId`                | int               | Piece index 0 to N-1 (Glyph only)                        |
| `isInProgress`           | bool              | True for Began, Moved, Stationary                        |
| `isNoneEndedOrCanceled`  | bool              | True for None, Ended, Canceled                           |

**Note:** Screen origin (0,0) is bottom-left. Convert orientation to degrees: `float degrees = orientation * Mathf.Rad2Deg;`

### BoardSession (Players)

Manage player profiles and sessions:

```csharp
using Board.Session;

// Get current players
var players = BoardSession.GetPlayers();
foreach (var player in players)
{
    string name = player.Name;
    Texture2D avatar = player.Avatar;
}
```

### BoardApplication (System)

System integration features:

```csharp
using Board.Core;

// Show pause screen
BoardApplication.ShowPauseScreen();

// Check if paused
bool isPaused = BoardApplication.IsPaused;
```

### BoardSaveGameManager (Save Data)

Persistent storage per player:

```csharp
using Board.Save;

// Save game data
BoardSaveGameManager.Save("slot1", saveData);

// Load game data
var loaded = BoardSaveGameManager.Load("slot1");
```

## Input Handling Pattern

### In This Project

`InputManager.cs` is the ONLY file that imports `Board.Input`:

```csharp
namespace ZeroDayAttack.Input
{
    using Board.Input;

    public class InputManager : MonoBehaviour
    {
        public static InputManager Instance { get; private set; }

        // Events for other systems
        public event Action<BoardContact> OnContactBegan;
        public event Action<BoardContact> OnContactMoved;
        public event Action<BoardContact> OnContactEnded;

        void Update()
        {
            var contacts = BoardInput.GetActiveContacts();
            foreach (var contact in contacts)
            {
                switch (contact.phase)
                {
                    case BoardContactPhase.Began:
                        OnContactBegan?.Invoke(contact);
                        break;
                    case BoardContactPhase.Moved:
                        OnContactMoved?.Invoke(contact);
                        break;
                    case BoardContactPhase.Stationary:
                        // IMPORTANT: Handle Stationary for pieces placed without movement
                        OnContactStationary?.Invoke(contact);
                        break;
                    case BoardContactPhase.Ended:
                        OnContactEnded?.Invoke(contact);
                        break;
                }
            }
        }
    }
}
```

### Token Detection

`TokenManager.cs` subscribes to InputManager events:

```csharp
void Start()
{
    InputManager.Instance.OnContactBegan += HandleContactBegan;
}

void HandleContactBegan(BoardContact contact)
{
    if (contact.type == BoardContactType.Glyph)
    {
        // Map glyph to token
        var token = MapGlyphToToken(contact.glyphId);
        // Convert screen to world position
        Vector3 worldPos = Camera.main.ScreenToWorldPoint(
            new Vector3(contact.screenPosition.x, contact.screenPosition.y, 10));
        // Snap to nearest edge node
        SnapTokenToNode(token, worldPos);
    }
}
```

## Simulator

Test without hardware using Board's Simulator:

1. Open **Board > Input > Simulator**
2. Enable Simulation
3. Use mouse to simulate touches
4. Place virtual pieces

### Simulator Features

- Mouse clicks = finger touches
- Keyboard shortcuts for piece placement
- Virtual glyph positioning

### Simulator Icon Setup (Required for Glyph Testing)

To test glyph/piece detection in the simulator:

1. **Create Simulation Icons**: For each piece type, create a `BoardContactSimulationIcon` ScriptableObject

   - Right-click in Project > Create > Board > Contact Simulation Icon
   - Set the GlyphId to match the token's GlyphId in TokenDatabase

2. **Configure Palette**: Add icons to the simulator palette

   - Open Board > Input > Simulator
   - Add each simulation icon to the available palette

3. **GlyphId Mapping**: Ensure TokenDatabase GlyphIds match simulation icon GlyphIds

```text
Token in TokenDatabase    Simulation Icon GlyphId
─────────────────────     ─────────────────────────
Red Attack (GlyphId: 1)   → SimIcon_RedAttack (1)
Red Exploit (GlyphId: 2)  → SimIcon_RedExploit (2)
...
```

**Troubleshooting**: If glyphs are not detected, verify GlyphId values match between TokenDatabase entries and simulation icons.

## Coordinate Conversion

### Screen to World

```csharp
// Board SDK provides screen pixels (origin bottom-left)
Vector2 screenPos = contact.screenPosition;

// Convert to world coordinates
Vector3 worldPos = Camera.main.ScreenToWorldPoint(
    new Vector3(screenPos.x, screenPos.y, 10));
```

### World to Grid

```csharp
// World position to grid coordinates
int gridX = Mathf.FloorToInt((worldPos.x - LayoutConfig.GridLeft) / LayoutConfig.TileSize);
int gridY = Mathf.FloorToInt((worldPos.y - LayoutConfig.GridBottom) / LayoutConfig.TileSize);
```

## Glyph ID Mapping

Map Board SDK glyph IDs to game tokens:

```csharp
// In TokenDatabase or TokenManager
Dictionary<int, TokenData> glyphToToken = new()
{
    { 1, redAttack },
    { 2, redExploit },
    { 3, redGhost },
    { 4, blueAttack },
    { 5, blueExploit },
    { 6, blueGhost }
};
```

## UI Input Considerations

### BoardUIInputModule

When using Unity UI on Board, you must use `BoardUIInputModule` instead of `InputSystemUIInputModule`:

**Why Required:** Board SDK intercepts touch input before Unity's standard input system. Without this, UI elements won't respond to touch.

**Setup:**

1. Select your EventSystem GameObject in the scene
2. Remove or disable `InputSystemUIInputModule` component
3. Add `BoardUIInputModule` component

```csharp
// In scene hierarchy:
// EventSystem
//   └─ BoardUIInputModule (instead of InputSystemUIInputModule)
```

See `vendor-docs/reference/Board.Input.md` for full API details.

## Best Practices

### Isolation

Keep Board SDK imports isolated to `InputManager`:

- Other scripts subscribe to InputManager events
- Enables testing without hardware
- Prevents SDK coupling

### Coordinate Handling

Always convert coordinates:

- SDK provides screen pixels
- Game logic uses world units
- Grid positions use integer coordinates

### Contact Lifecycle

Track contacts properly:

- Store contacts by `contactId` on `Began`
- Update position on `Moved` or `Stationary`
- Clean up on `Ended` or `Canceled`
- Use `isInProgress` helper to check if contact is active

### Touch State

Use `isTouched` for gameplay:

- `true` = piece being held/moved by player
- `false` = piece resting on surface

## Reference Files

This skill's `references/` folder contains complete SDK documentation organized for efficient navigation.

### Custom Guides (8 files)

| File                      | Contains                                                      | Read When                            |
| ------------------------- | ------------------------------------------------------------- | ------------------------------------ |
| `contact-handling.md`     | BoardContact struct properties, phase enum values, lifecycle  | Need exact property names or values  |
| `glyph-detection.md`      | GlyphId mapping, TokenDatabase setup, .tflite model config    | Setting up piece detection           |
| `integration-patterns.md` | Zero-Day Attack specific patterns, InputManager isolation     | Implementing input handling          |
| `sample-code-guide.md`    | SDK sample BoardInputManager walkthrough, Dictionary tracking | Learning contact lifecycle patterns  |
| `save-system.md`          | BoardSaveGameManager usage, metadata, storage quotas          | Implementing save/load functionality |
| `session-management.md`   | BoardSession player handling, profile vs guest modes          | Working with player profiles         |
| `simulator-setup.md`      | BoardContactSimulationIcon configuration, palette setup       | Testing without hardware             |
| `vendor-docs-index.md`    | Complete index of all 26 vendor docs with descriptions        | Need to dive deeper into SDK API     |

### Vendor Documentation (26 files in `vendor-docs/`)

For complete SDK API details, see `vendor-docs-index.md`. Organized by category:

| Category         | Files | Key Content                                                                                  |
| ---------------- | ----- | -------------------------------------------------------------------------------------------- |
| **get-started/** | 4     | Installation, project-setup, build-deploy, sample-scene                                      |
| **learn/**       | 5     | architecture, concepts, hardware, pieces, touch-system                                       |
| **guides/**      | 6     | touch-input, simulator, pause-menu, player-management, profile-switcher, save-game-system    |
| **reference/**   | 10    | Board.Input.md (575 lines), Board.Core.md, Board.Session.md, Board.Save.md, enums, delegates |

### API Reference by Namespace

| Namespace                | Reference File              | Key Classes                                        |
| ------------------------ | --------------------------- | -------------------------------------------------- |
| `Board.Input`            | `Board.Input.md`            | BoardInput, BoardContact, BoardInputSettings       |
| `Board.Input.Debug`      | `Board.Input.Debug.md`      | BoardInputDebugView, BoardContactDebugView         |
| `Board.Input.Simulation` | `Board.Input.Simulation.md` | BoardContactSimulation, BoardContactSimulationIcon |
| `Board.Core`             | `Board.Core.md`             | BoardApplication, BoardLogger, BoardPlayer         |
| `Board.Session`          | `Board.Session.md`          | BoardSession, BoardSessionPlayer                   |
| `Board.Save`             | `Board.Save.md`             | BoardSaveGameManager, BoardSaveGameMetadata        |
