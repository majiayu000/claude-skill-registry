---
name: board-sdk
description: This skill should be used when the user asks about "touch input", "BoardInput", "BoardContact", "piece detection", "glyph", "glyph recognition", "simulator", "Board hardware", "contact phases", "Piece Set", "touch system", "Board SDK", "multi-touch", "noise rejection", or discusses Board hardware integration and input handling.
version: 0.2.0
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

### Contact Types

| Type       | Description                                           |
| ---------- | ----------------------------------------------------- |
| **Finger** | Standard touch point from a finger                    |
| **Glyph**  | Contact from a physical Piece with conductive pattern |

### Contact Phases

| Phase        | Description                     |
| ------------ | ------------------------------- |
| `Began`      | Contact started this frame      |
| `Moved`      | Position or orientation changed |
| `Stationary` | Held in place, no change        |
| `Ended`      | Lifted from surface             |
| `Canceled`   | Tracking interrupted            |

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

| Property      | Type             | Description                                     |
| ------------- | ---------------- | ----------------------------------------------- |
| `Id`          | int              | Unique contact ID (persistent during lifecycle) |
| `Position`    | Vector2          | Screen position in pixels                       |
| `Phase`       | ContactPhase     | Current lifecycle state                         |
| `Type`        | BoardContactType | Finger or Glyph                                 |
| `Orientation` | float            | Rotation angle (glyphs only)                    |
| `IsTouched`   | bool             | Whether piece is being held (glyphs only)       |
| `GlyphId`     | int              | Specific glyph identifier (glyphs only)         |

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
                switch (contact.Phase)
                {
                    case ContactPhase.Began:
                        OnContactBegan?.Invoke(contact);
                        break;
                    case ContactPhase.Moved:
                        OnContactMoved?.Invoke(contact);
                        break;
                    case ContactPhase.Ended:
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
    if (contact.Type == BoardContactType.Glyph)
    {
        // Map glyph to token
        var token = MapGlyphToToken(contact.GlyphId);
        // Convert screen to world position
        Vector3 worldPos = Camera.main.ScreenToWorldPoint(
            new Vector3(contact.Position.x, contact.Position.y, 10));
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

## Coordinate Conversion

### Screen to World

```csharp
// Board SDK provides screen pixels (origin bottom-left)
Vector2 screenPos = contact.Position;

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

When using Unity UI on Board:

```csharp
// Replace standard InputSystemUIInputModule with BoardUIInputModule
// The SDK blocks system touch events
```

This is required because Board SDK intercepts touch input before Unity's standard input system.

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

- Store contacts by ID on `Began`
- Update position on `Moved`
- Clean up on `Ended` or `Canceled`

### Touch State

Use `IsTouched` for gameplay:

- `true` = piece being held/moved by player
- `false` = piece resting on surface

## Additional Resources

### Reference Files

For comprehensive SDK documentation:

- **Documentation/Board-SDK-Documentation/** - Full SDK reference
  - `overview.md` - SDK introduction
  - `learn/concepts.md` - Core terminology
  - `learn/touch-system.md` - Touch handling details
  - `learn/pieces.md` - Piece/glyph recognition
  - `guides/touch-input.md` - Implementation guide
  - `guides/simulator.md` - Simulator usage
  - `reference/` - API documentation

### Key APIs

- `Board.Input.BoardInput` - Touch contact access
- `Board.Input.BoardContact` - Contact data structure
- `Board.Session.BoardSession` - Player management
- `Board.Save.BoardSaveGameManager` - Save data
