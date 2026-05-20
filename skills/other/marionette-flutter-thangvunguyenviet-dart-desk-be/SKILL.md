---
name: marionette-flutter
description: "Expert guidance for Marionette MCP, enabling AI agents to inspect and interact with running Flutter applications. Use when (1) setting up Marionette in a Flutter project, (2) configuring MCP server for Claude Code or Cursor, (3) automating UI testing with tap, enter_text, scroll_to, or take_screenshots, (4) debugging Flutter apps by inspecting widget trees or retrieving logs, (5) performing smoke tests or verifying user flows. Triggers include marionette, MCP server, flutter testing, widget inspection, UI automation, VM service."
---

# Marionette Flutter

Marionette MCP enables AI agents to inspect and interact with running Flutter applications at runtime. It's "Playwright MCP, but for Flutter apps."

## Quick Setup

### 1. Add Package to Flutter App

```yaml
# pubspec.yaml
dev_dependencies:
  marionette_flutter: ^0.3.0
```

### 2. Initialize Binding (Debug Mode Only)

```dart
// main.dart
import 'package:flutter/foundation.dart';
import 'package:marionette_flutter/marionette_flutter.dart';

void main() {
  if (kDebugMode) {
    MarionetteBinding.ensureInitialized();
  }
  runApp(const MyApp());
}
```

### 3. Install MCP Server

```bash
dart pub global activate marionette_mcp
```

Or add to dev_dependencies:
```yaml
dev_dependencies:
  marionette_mcp: ^0.1.0
```

### 4. Configure AI Tool

**Claude Code** (`.claude/mcp.json`):
```json
{
  "mcpServers": {
    "marionette": {
      "command": "dart",
      "args": ["run", "marionette_mcp"]
    }
  }
}
```

**Cursor** (`.cursor/mcp.json`):
```json
{
  "mcpServers": {
    "marionette": {
      "command": "marionette_mcp"
    }
  }
}
```

### 5. Connect to Running App

Run Flutter app in debug mode, find VM Service URI in console:
```
The Dart VM service is listening on http://127.0.0.1:12345/AbCdEfGh=/
```

Ask agent to connect using `ws://127.0.0.1:12345/AbCdEfGh=/ws`

## Available Tools

| Tool | Purpose |
|------|---------|
| `connect` | Connect to Flutter app via VM Service URI |
| `disconnect` | Disconnect from current app |
| `get_interactive_elements` | List visible UI elements (buttons, inputs, etc.) |
| `tap` | Tap element by key or visible text |
| `enter_text` | Enter text in text fields |
| `scroll_to` | Scroll until element is visible |
| `take_screenshots` | Capture base64-encoded screenshots |
| `get_logs` | Retrieve logs from Dart's logging package |
| `hot_reload` | Apply code changes without state loss |

## Custom Widget Configuration

Register custom interactive widgets:

```dart
MarionetteBinding.ensureInitialized(
  configuration: MarionetteConfiguration(
    customInteractiveWidgets: [
      CustomWidget<MyButton>(
        type: InteractiveElementType.button,
        getText: (widget) => widget.label,
      ),
    ],
  ),
);
```

## Common Workflows

### Smoke Test After Refactor
1. Connect to running app
2. `get_interactive_elements` to see current screen
3. `tap` buttons to navigate
4. `take_screenshots` to verify visual state
5. `get_logs` to check for errors

### UI Debugging
1. Connect to app
2. `get_interactive_elements` to inspect widget tree
3. Identify missing or misplaced elements
4. `hot_reload` after fixes

### Form Testing
1. `get_interactive_elements` to find text fields
2. `enter_text` to fill form
3. `tap` submit button
4. `get_logs` to verify submission

## Limitations

- **Debug/profile mode only** - Requires VM Service (not available in release)
- **Manual URI connection** - Must copy URI from console each run
- **Platform-specific gestures** - Some interactions may vary across platforms
- **Custom widgets need configuration** - Register non-standard interactive widgets

## Resources

- Documentation: https://marionette.leancode.co/
- GitHub: https://github.com/leancodepl/marionette_mcp
- pub.dev: https://pub.dev/packages/marionette_flutter
