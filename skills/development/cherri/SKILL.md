---
name: cherri
description: Use when writing Apple Shortcuts as code using Cherri language. Covers syntax, actions, compilation, and common patterns.
---

# Cherri - Apple Shortcuts Programming Language

Cherri compiles to `.shortcut` files for iOS/macOS. Store `.cherri` files in dotfiles for version-controlled Shortcuts.

## Installation

```bash
brew tap electrikmilk/cherri
brew install electrikmilk/cherri/cherri
```

## Compilation

```bash
cherri file.cherri              # Compile + sign via macOS/AppleID
cherri file.cherri --hubsign    # Sign via RoutineHub (fallback)
cherri file.cherri --skip-sign  # Unsigned (won't import on macOS)
cherri file.cherri --debug      # Debug output
```

Output: `Shortcut Name.shortcut` (name from `#define name` or filename)

**Note:** macOS requires signed shortcuts. Use `--skip-sign` only for syntax checks.

## Syntax Reference

### Defines (Shortcut Metadata)

```cherri
#define name My Shortcut
#define color red
#define glyph heart
#define version 18.4
#define inputs text, image
#define outputs file
```

Colors: `red`, `darkorange`, `orange`, `yellow`, `green`, `teal`, `lightblue`, `blue`, `darkblue`, `violet`, `purple`, `pink`, `taupe`, `gray`, `darkgray`

Glyphs: Use `cherri --glyph=search` to find icons.

### Variables

```cherri
@name = "World"                    // Variable assignment
const greeting = "Hello"           // Constant
@message = "{greeting}, {name}!"   // String interpolation
```

Global variables: `Ask`, `Clipboard`, `CurrentDate`, `ShortcutInput`, `RepeatIndex`, `RepeatItem`

### Essential Actions

```cherri
// Dialogs
alert("Message", "Title")          // Alert with title
alert("Message")                   // Alert without title
show("Text to display")            // Show output

// User input
@text = prompt("Enter text:")      // Text input
@num = askNumber("Enter number:")  // Number input

// Control
nothing()                          // Clear output
stop()                             // Stop shortcut
exit()                             // Same as stop
comment("Note")                    // Add comment
```

### Control Flow

```cherri
// If statement
if condition {
    // code
} else {
    // code
}

// Repeat n times
repeat 5 {
    alert("{RepeatIndex}")
}

// Repeat with named index
repeat i for 5 {
    alert("Index: {i}")
}

// For each in list
for item in list {
    alert(item)
}
```

### Menus

**IMPORTANT:** Use colon `:` after item name, NOT curly braces!

```cherri
menu "Choose an option:" {
    item "Option 1":
        alert("You chose 1")
    item "Option 2":
        alert("You chose 2")
        show("More actions here")
}
```

### Lists

```cherri
#include 'actions/scripting'

@items = list("apple", "banana", "cherry")
@chosen = chooseFromList(items, "Pick one")

repeatEach fruit in items {
    alert(fruit)
}
```

### Custom Actions (Functions)

```cherri
action greet(text name) {
    alert("Hello, {name}!")
}

greet("World")
```

### Includes

```cherri
#include "other_file.cherri"
#include 'actions/scripting'   // Built-in action libraries
```

## Common Patterns

### Hello World

```cherri
#define name Hello World
#define color green
#define glyph star

alert("Hello World!", "Greeting")
```

### User Input Flow

```cherri
#define name Greeter

@name = prompt("What's your name?")
@age = askNumber("What's your age?")
alert("Hello {name}, you are {age} years old!", "Welcome")
```

### Menu-Driven Shortcut

```cherri
#define name Color Picker
#define color blue
#define glyph paintbrush

menu "Pick a color:" {
    item "Red":
        @color = "red"
    item "Green":
        @color = "green"
    item "Blue":
        @color = "blue"
}

alert("You picked: {color}", "Result")
```

## Common Mistakes

| Wrong | Correct | Why |
|-------|---------|-----|
| `alert(title, message)` | `alert(message, title)` | Message first, title second |
| `var = value` | `@var = value` | Variables need `@` prefix |
| `askText("prompt")` | `prompt("prompt")` | Action is `prompt`, not `askText` |
| `menu { item "X" { ... } }` | `menu { item "X": ... }` | Colon after item, not braces |

## CLI Reference

```bash
cherri --help                     # All options
cherri --action=alert             # Search action definitions
cherri --glyph=star               # Search glyphs
cherri --docs=scripting           # Action documentation by category
```

## Discovering Third-Party Actions

macOS stores all available Shortcuts actions in a ToolKit database. Use the dotfiles script to explore:

```bash
# In dotfiles/shortcuts/
./analyze-shortcuts-actions.fish stats      # Show action counts
./analyze-shortcuts-actions.fish vendors    # List third-party app vendors
./analyze-shortcuts-actions.fish actions raycast  # Find actions for an app
./analyze-shortcuts-actions.fish search clipboard # Search by keyword
./analyze-shortcuts-actions.fish doc        # Generate SHORTCUTS_ACTIONS.md reference
```

The generated `SHORTCUTS_ACTIONS.md` lists all third-party action identifiers you can use in Cherri.

## Workflow: Adding New Extension Apps

When you install a new Shortcuts extension (Toolbox Pro, Actions, etc.):

1. **Regenerate actions doc:**
   ```bash
   ./analyze-shortcuts-actions.fish doc
   ```

2. **Find the app's actions:**
   ```bash
   ./analyze-shortcuts-actions.fish actions toolbox
   ```

3. **Check if Cherri has built-in support:**
   ```bash
   cherri --action=globalVariable
   ```

4. **If no built-in support, document the raw action pattern** (see below)

5. **Update this skill** if you discover useful patterns for the app

## Using Third-Party Actions in Cherri

For actions not built into Cherri, use raw action syntax:

```cherri
// Raw action with identifier from analyze-shortcuts-actions.fish
rawAction("com.alexhay.ToolboxProForShortcuts.IsDarkModeOnIntent", {
    "placeholder": "unused"  // rawAction requires at least one parameter
})
```

**Important:** Cherri's `rawAction` crashes with empty `{}`. Always include at least one placeholder parameter.

**Discovering parameters:** Use the analysis script to query the ToolKit database:

```bash
# Show all parameters for an action
./analyze-shortcuts-actions.fish params GlobalVariablesIntent

# Find actions for an app
./analyze-shortcuts-actions.fish actions sindre
```

The ToolKit database at `~/Library/Shortcuts/ToolKit/` contains all parameter definitions.

## Known Extension App Patterns

### Toolbox Pro

Action prefix: `com.alexhay.ToolboxProForShortcuts`

Key actions:
- `GlobalVariablesIntent` - Get/set/check global variables
- `CheckGVIntent` - Check if global variable exists
- `IsDarkModeOnIntent` - Check dark mode ✅ **verified**
- `DeviceDetailsIntent` - Device info
- `GetTextFromImageIntent` - OCR
- `CreateMenuIntent` / `SmartMenuIntent` - Custom menus

```cherri
// ✅ VERIFIED: Check if dark mode is on
rawAction("com.alexhay.ToolboxProForShortcuts.IsDarkModeOnIntent", {
    "ShowWhenRun": true
})

// ✅ VERIFIED: Global Variables (use `./analyze-shortcuts-actions.fish params GlobalVariablesIntent` for all params)
// Set a variable
rawAction("com.alexhay.ToolboxProForShortcuts.GlobalVariablesIntent", {
    "mode": "set",
    "setVariableKey": "myVariable",
    "setVariableValue": "myValue"
})

// Get a variable
rawAction("com.alexhay.ToolboxProForShortcuts.GlobalVariablesIntent", {
    "mode": "get",
    "getVariableKey": "myVariable"
})

// Delete a variable
rawAction("com.alexhay.ToolboxProForShortcuts.GlobalVariablesIntent", {
    "mode": "delete",
    "deleteVariableKey": "myVariable"
})
```

### Persistent Config (JSON in iCloud) ✅ **THE WAY**

For persistent data across shortcuts, use a JSON file in iCloud Drive:

**Location:** `~/Library/Mobile Documents/com~apple~CloudDocs/dotfiles/shortcuts/config.json`

**CLI access (fish):**
```bash
shortcuts-config get                    # View all
shortcuts-config get currentProject     # Get key
shortcuts-config set currentProject foo # Set key
shortcuts-config del currentProject     # Delete key
```

**Shortcuts access:** Use "Get File" and "Save File" actions pointing to:
`/dotfiles/shortcuts/config.json` in iCloud Drive

**Why this (not Data Jar or other apps):**
- Direct CLI access with `jq` and `shortcuts-config`
- Version controllable (can symlink to dotfiles repo)
- No app dependency
- Works on iOS via Files app + Shortcuts "Get File"/"Save File"
- Claude Code can read/write directly

### Menu Box ✅ **installed**

Action prefix: `dev.alexhay.MenuBox`

Beautiful custom menus with SF Symbols, colors, and hidden data fields. Fully CLI-driven - no GUI needed.

**Quick Menu (inline, no pre-config):**
```cherri
// Create menu from marked-up text
// Format: "Title | symbol" per line
rawAction("dev.alexhay.MenuBox.QuickMenuIntent", {
    "text": "Settings | gear\nProfile | person.circle\nHelp | questionmark.circle"
})
```

**Custom Menu Items (full control):**
```cherri
// Create styled menu item with SF Symbol
rawAction("dev.alexhay.MenuBox.CreateSymbolItemIntent", {
    "title": "Settings",
    "subtitle": "Configure options",
    "symbol": "gear",
    "symbolColourHex": "#FFFFFF",
    "bgColourHex": "#007AFF",
    "mask": "circle"
})

// Create menu item from emoji
rawAction("dev.alexhay.MenuBox.CreateEmojiItemIntent", {
    "title": "Coffee Break",
    "emoji": "☕️"
})

// Create menu item from image
rawAction("dev.alexhay.MenuBox.CreateImageItemIntent", {
    "title": "Photo",
    "image": imageVariable
})
```

**Hidden Data Fields:** Each menu item supports `field1` through `field4` for storing data that isn't visible but accessible when item is selected.

**Menu Sets:** Save menus to reuse across shortcuts:
```cherri
rawAction("dev.alexhay.MenuBox.CreateMenuSetIntent", {
    "menuItems": menuItemsVariable,
    "setType": "new",
    "setName": "My Project Menu"
})

// Later, choose from saved set
rawAction("dev.alexhay.MenuBox.ChooseMenuSetIntent", {
    "menuSet": "My Project Menu"
})
```

Run `./analyze-shortcuts-actions.fish params CreateSymbolItemIntent` for all styling options (weights, scales, masks).

### FocusCuts ✅ **installed** (macOS only)

Action prefix: `dev.snailedit.FocusCuts`

FocusCuts provides Focus Mode awareness with 3 custom actions + a status bar menu.

**Get current Focus Mode:**
```cherri
// Returns the currently active Focus Mode name (or empty if none)
rawAction("dev.snailedit.FocusCuts.GetCurrentFocusModeIntent", {
    "ShowWhenRun": false
})
```

**Check if specific Focus is active:**
```cherri
rawAction("dev.snailedit.FocusCuts.IsFocusModeActiveIntent", {
    "focusMode": "Work"  // returns true/false
})
```

**List all Focus Modes:**
```cherri
rawAction("dev.snailedit.FocusCuts.ListFocusModesIntent", {
    "ShowWhenRun": false
})
```

**Focus-aware conditional logic pattern:**
```cherri
// Get current focus, then branch
rawAction("dev.snailedit.FocusCuts.GetCurrentFocusModeIntent", {
    "ShowWhenRun": false
})
@focusMode = ShortcutInput

if focusMode == "Work" {
    alert("Loading work projects...", "Work Mode")
} else if focusMode == "Personal" {
    alert("Loading personal projects...", "Personal Mode")
} else {
    alert("No Focus Mode active", "Default")
}
```

**FocusCuts menu bar:** Also provides a status bar menu showing shortcuts relevant to your current Focus Mode (configure in app).

### Logger ✅ **installed**

Action prefix: `com.alexhay.Console`

Real-time debugging console with log levels, tags, and iCloud sync. Much better than `alert()` spam.

**Basic logging:**
```cherri
// Log a message with category (info/success/warning/error)
rawAction("com.alexhay.Console.LogMessageIntent", {
    "title": "API Response",
    "messages": "Got 200 OK",
    "category": "success",
    "tag": "api"
})

// Log with error fallback if empty
rawAction("com.alexhay.Console.LogMessageIntent", {
    "title": "User Input",
    "messages": userInput,
    "errorIfEmpty": true,
    "errorMessage": "No input provided!"
})
```

**Session control:**
```cherri
// Start a logging session
rawAction("com.alexhay.Console.StartLoggingIntent", {
    "mode": "start"
})

// ... your shortcut logic ...

// Stop logging
rawAction("com.alexhay.Console.StartLoggingIntent", {
    "mode": "stop"
})
```

**Log files/items:**
```cherri
rawAction("com.alexhay.Console.LogItemsIntent", {
    "items": fileVariable,
    "title": "Downloaded File",
    "message": "Processing complete"
})
```

**Conditional logging:**
```cherri
// Log different messages based on condition
rawAction("com.alexhay.Console.LogConditionalMessageIntent", {
    "condition": "equals",
    "sourceValue": statusCode,
    "query": "200",
    "trueTitle": "Success",
    "trueMessage": "Request completed",
    "trueCategory": "success",
    "falseTitle": "Failed",
    "falseMessage": "Request failed with status",
    "falseCategory": "error",
    "tag": "api"
})
```

**Export logs:**
```cherri
// Output all logs as markdown
rawAction("com.alexhay.Console.OutputMessagesIntent", {
    "outputMode": "markdown"
})

// Clear console after export
rawAction("com.alexhay.Console.ClearMessagesIntent", {
    "ShowWhenRun": false
})
```

**System diagnostics:**
```cherri
// Log device details (model, OS, battery, etc.)
rawAction("com.alexhay.Console.LogDeviceDetailsIntent", {
    "tag": "system"
})

// Log internet connection info
rawAction("com.alexhay.Console.LogInternetConnectionIntent", {
    "tag": "network"
})
```

**Debugging workflow:**
1. Add `StartLoggingIntent` at shortcut start
2. Sprinkle `LogMessageIntent` calls at key points
3. Use tags to filter (e.g., "api", "ui", "data")
4. Use categories for severity (info/success/warning/error)
5. Export with `OutputMessagesIntent` when done
6. Logs sync via iCloud - debug iOS shortcuts from Mac

### Actions by Sindre Sorhus ✅ **installed**

Action prefix: `com.sindresorhus.Actions`

199 utility actions. Key ones:

```cherri
// Generate UUID
rawAction("com.sindresorhus.Actions.GenerateUUIDIntent", {
    "placeholder": "unused"
})

// Format duration
rawAction("com.sindresorhus.Actions.FormatDurationIntent", {
    "placeholder": "unused"
})

// Debug (shows variables in console)
rawAction("com.sindresorhus.Actions.DebugIntent", {
    "placeholder": "unused"
})
```

Run `./analyze-shortcuts-actions.fish actions sindre` for full list (199 actions).

### Charty ✅ **installed**

Action prefix: `com.brogrammers.charty`

Generate charts and graphs from Shortcuts. 24 actions for 7 chart types: bar, line, pie, donut, scatter, area, rings.

**Create a chart:**
```cherri
// Create new chart (returns chart ID)
rawAction("com.brogrammers.charty.NewChartIntent", {
    "title": "Monthly Stats",
    "automaticId": true
})
@chartId = ShortcutInput
```

**Add data series:**
```cherri
// Add bar series
rawAction("com.brogrammers.charty.AddSeriesToChartIntent", {
    "chartId": "{chartId}",
    "label": "Revenue",
    "type": "bar",
    "barXValues": ["Jan", "Feb", "Mar"],
    "barYValues": [100, 150, 200]
})

// Add line series
rawAction("com.brogrammers.charty.AddSeriesToChartIntent", {
    "chartId": "{chartId}",
    "label": "Trend",
    "type": "line",
    "lineXValues": [1, 2, 3],
    "lineYValues": [100, 150, 200]
})

// Add pie/donut series
rawAction("com.brogrammers.charty.AddSeriesToChartIntent", {
    "chartId": "{chartId}",
    "label": "Distribution",
    "type": "pie",
    "pieLabels": ["A", "B", "C"],
    "pieValues": [30, 50, 20]
})
```

**Export chart:**
```cherri
rawAction("com.brogrammers.charty.ExportChartAsImageIntent", {
    "chartId": "{chartId}"
})
```

**Other actions:** `StyleChartIntent`, `StyleAxisIntent`, `AddAverageIntent`, `FilterDataIntent`, `GroupDataIntent`, `AddSeriesFromCSVIntent`

Run `./analyze-shortcuts-actions.fish actions charty` for full list (24 actions).

---

*Update this skill with verified patterns when you discover them. Use `./analyze-shortcuts-actions.fish actions <name>` to find action identifiers for installed apps.*

## Community Reference (Not Installed)

Other Shortcuts extensions worth exploring later:

| App | Purpose | Link |
|-----|---------|------|
| **Pushcut** | Webhook triggers, location/schedule automation, home server | https://pushcut.io |
| **a-Shell** | Run shell commands (Python, Unix tools) on iOS | https://holzschu.github.io/a-Shell_iOS/ |
| **Jayson** | JSON viewer/editor with Shortcuts actions | https://jayson.app |
| **GizmoPack** | CSV parsing, Wallet pass generation | App Store |
| **Jellycuts** | Write Shortcuts in code (alternative to Cherri) | App Store |
| **Shortcutify** | Control Mac from iPhone, Google/Todoist integration | App Store |
| **Text Case** | Advanced text formatting | App Store |
| **AI Actions** | AI-powered Shortcuts actions (Sindre Sorhus) | App Store |

## Development Workflow

Use the `shortcuts-dev` fish function for quick iteration:

```bash
shortcuts-dev compile myshortcut.cherri  # Compile and sign
shortcuts-dev run myshortcut.cherri      # Compile, sign, and open
shortcuts-dev check myshortcut.cherri    # Syntax check only (fast)

shortcuts-dev params GlobalVariablesIntent  # Discover action params
shortcuts-dev actions toolbox               # List app's actions
shortcuts-dev vendors                       # List all apps

shortcuts-dev examples                      # List example templates
```

**Example templates** in `shortcuts/examples/`:
- `menu-driven.cherri` - Menu Box with SF Symbols
- `focus-aware.cherri` - FocusCuts conditional logic
- `with-logging.cherri` - Logger debugging workflow

## SF Symbols

Apple's icon library (5,000+ icons). Used by Menu Box `symbol` parameter.

**Naming convention:** base name + modifiers (dot-separated)

```
person                    # Outline
person.fill               # Solid fill
person.circle             # With circle background
person.circle.fill        # Solid with circle background
person.badge.plus         # With badge
person.2                  # Multiple (2 people)
person.2.fill             # Multiple, solid
```

**Common modifiers:**
- `.fill` - Solid version
- `.circle` / `.square` / `.rectangle` - Shape background
- `.badge.plus` / `.badge.minus` - With badge
- `.slash` - Crossed out / disabled
- `2` / `3` - Multiple items

**Common symbols:**
| Category | Symbols |
|----------|---------|
| Actions | `plus`, `minus`, `xmark`, `checkmark`, `arrow.right`, `arrow.left` |
| Objects | `gear`, `folder`, `doc`, `photo`, `video`, `music.note` |
| People | `person`, `person.2`, `person.circle` |
| Status | `bell`, `star`, `heart`, `flag`, `bookmark` |
| System | `magnifyingglass`, `house`, `trash`, `pencil`, `link` |
| Alerts | `exclamationmark.triangle`, `info.circle`, `questionmark.circle` |

**Browse icons:**
- **SF Symbols app** (free): https://developer.apple.com/sf-symbols/
- **Online browser:** https://sfsymbols.com

## Resources

- **Docs:** https://cherrilang.org/language/
- **Playground:** https://playground.cherrilang.org/
- **GitHub:** https://github.com/electrikmilk/cherri
- **Glyph Search:** https://glyphs.cherrilang.org/
- **Zed Extension:** https://github.com/videah/zed-cherri
