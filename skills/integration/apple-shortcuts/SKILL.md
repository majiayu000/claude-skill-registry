---
name: apple-shortcuts
description: Use when working with Apple Shortcuts on macOS/iOS - discovering actions, extension apps, running shortcuts from CLI, or integrating with automation workflows.
---

# Apple Shortcuts

Automation platform for macOS and iOS. Shortcuts can be created via GUI, Cherri (code), or imported.

## Running Shortcuts from CLI

```bash
# List all shortcuts
shortcuts list

# Run a shortcut by name
shortcuts run "My Shortcut"

# Run with text input
shortcuts run "My Shortcut" <<< "input text"

# Via URL scheme (works from any app)
open "shortcuts://run-shortcut?name=My%20Shortcut&input=text&text=Hello"
```

URL scheme parameters:
- `name`: Shortcut name (URL encoded)
- `input`: `text` or `clipboard`
- `text`: Actual input string

## Discovering Available Actions

macOS stores all Shortcuts actions in a ToolKit database:

```
~/Library/Shortcuts/ToolKit/Tools-prod.*.sqlite
```

Use the dotfiles script to explore:

```bash
cd ~/projects/jasonkuhrt/dotfiles/shortcuts

./analyze-shortcuts-actions.fish stats      # Action counts
./analyze-shortcuts-actions.fish vendors    # Third-party apps
./analyze-shortcuts-actions.fish actions raycast  # Actions for an app
./analyze-shortcuts-actions.fish search clipboard # Search by keyword
./analyze-shortcuts-actions.fish doc        # Generate reference doc
```

## Shortcuts Storage

```
~/Library/Shortcuts/Shortcuts.sqlite     # Shortcut definitions
~/Library/Shortcuts/ToolKit/             # Action database
```

Shortcuts are stored in SQLite with actions as binary plist blobs. Not meant for direct editing—use Cherri for code-based shortcuts.

## Persistent Config

Use JSON in iCloud Drive instead of extension apps for config storage:

**Location:** `~/Library/Mobile Documents/com~apple~CloudDocs/dotfiles/shortcuts/config.json`

```bash
# CLI (fish)
shortcuts-config get                    # View all
shortcuts-config set currentProject foo # Set key
shortcuts-config get currentProject     # Get key
```

**In Shortcuts:** Use "Get File" / "Save File" pointing to `/dotfiles/shortcuts/config.json`

**Do not use Data Jar or similar apps.** JSON gives:
- Direct CLI access (`jq`, `shortcuts-config`)
- Version controllable (symlink to git repo)
- No app dependency
- Cross-platform (iOS Files app can read it too)
- Claude Code can read/write directly

## Extension Apps

Apps that add actions to Shortcuts:

| App | Platform | Purpose |
|-----|----------|---------|
| **Toolbox Pro** | iOS + Mac (M1+)* | Global variables, OCR, device info |
| **Actions** | iOS + macOS | 180+ extra actions (Sindre Sorhus) |
| **Menu Box** | iOS + macOS | Beautiful menus with SF Symbols, colors, hidden data |
| **Logger** | iOS + macOS | Debug console with log levels, tags, iCloud sync |
| **FocusCuts** | macOS only | Status bar menu for Focus Mode-aware shortcuts |
| **Charty** | iOS + macOS | Generate charts (bar, line, pie, scatter, etc.) |

*Wrapped iOS app—runs on Apple Silicon via "Designed for iPhone/iPad"

### Installing Extension Apps

```bash
# Native macOS apps (via mas)
mas install 1586435171  # Actions
```

Wrapped iOS apps (Toolbox Pro) require manual App Store install—`mas` can't install them.

### After Installing New Apps

1. Open Shortcuts app (triggers ToolKit database refresh)
2. Discover actions: `./analyze-shortcuts-actions.fish actions <appname>`
3. Get parameters: `./analyze-shortcuts-actions.fish params <action>`
4. Use in Cherri with `rawAction()` syntax

## macOS Signing Requirement

**macOS will not import unsigned shortcuts.**

```bash
# Unsigned - syntax check only, won't import on macOS
cherri myshortcut.cherri --skip-sign

# Signed via macOS/AppleID (default)
cherri myshortcut.cherri

# Signed via RoutineHub service (if macOS signing fails)
cherri myshortcut.cherri --hubsign
```

Signed shortcuts contain `AppleIDValidationRecord` and `SigningPublicKey` in an AEA1 archive format (different from code signing - `codesign -dv` won't recognize them).

## Wrapped iOS Apps on Mac

Some iOS apps run on Apple Silicon Macs via compatibility mode:

```
/Applications/App Name.app/
├── WrappedBundle -> Wrapper/ActualApp.app
└── Wrapper/
    └── ActualApp.app  (iOS app)
```

These apps:
- Can't be installed via `mas` CLI
- Require manual App Store install
- Work identically to iOS versions
- Sync via iCloud

## Shortcuts Database Schema

For advanced exploration:

```sql
-- List all third-party actions
SELECT id FROM Tools
WHERE id NOT LIKE 'com.apple.%'
ORDER BY id;

-- Count by vendor
SELECT
    substr(id, 1, instr(substr(id, instr(id, '.') + 1), '.') + instr(id, '.')) as vendor,
    COUNT(*) as count
FROM Tools
WHERE id NOT LIKE 'com.apple.%'
GROUP BY vendor
ORDER BY count DESC;
```

## Integration with Cherri

See the `cherri` skill for:
- Writing shortcuts as code
- Raw action syntax for third-party apps
- Known extension app patterns

## Key Learnings

1. **Shortcuts are signed** - macOS requires signed `.shortcut` files for import
2. **Actions come from apps** - Install extension apps to get more actions
3. **ToolKit database is truth** - Query it to discover available actions and parameters
4. **URL schemes work everywhere** - Trigger shortcuts from CLI, scripts, other apps
5. **Wrapped iOS apps exist** - Some "Mac" apps are actually iOS apps in disguise
6. **Use JSON for config** - Store persistent data in `iCloud Drive/dotfiles/shortcuts/config.json`, not extension apps like Data Jar. This gives CLI access via `shortcuts-config` and works cross-platform.

## Resources

- [Cherri](https://cherrilang.org) - Shortcuts programming language
- [Toolbox Pro](https://toolboxpro.app) - Global variables, menus, device info
- [Actions](https://sindresorhus.com/actions) - 180+ extra actions (free)
