---
name: project-widget
description: Guide for creating reusable widgets in app_widget packages with platform adaptive support (project)
---

# Flutter Widget Development Skill

This skill guides the creation of reusable widgets following this project's modular package conventions.

## When to Use

Trigger this skill when:
- Creating a reusable UI component
- Building platform-adaptive widgets (Material/Cupertino)
- User asks to "create a widget", "add a component", or "build reusable UI"

## Mason Template

**Always use Mason template first:**

```bash
# Create widget package
mason make widget --name WidgetName --type stateless --folder subfolder

# Options:
# --type: stateless or stateful
# --folder: subfolder in app_widget/ (e.g., "buttons", "cards")
# --has_platform_adaptive: Include Material/Cupertino variants (default: true)
```

## Project Structure

Widgets are organized in `app_widget/` as separate packages:

```
app_widget/
├── adaptive/              # Responsive/adaptive components
│   ├── lib/
│   │   ├── app_adaptive_widgets.dart  # Barrel export
│   │   └── src/
│   │       ├── scaffold.dart           # AppAdaptiveScaffold
│   │       └── action.dart             # Adaptive action widgets
│   └── pubspec.yaml
├── artwork/               # Assets (icons, lottie, images)
├── feedback/              # Snackbars, dialogs, toasts
└── web_view/              # WebView wrapper
```

## Widget Package Structure

```
app_widget/widget_name/
├── lib/
│   ├── widget_name.dart           # Barrel export (package entry point)
│   └── src/
│       ├── widget_name.dart       # Main widget implementation
│       └── widget_name_theme.dart # Optional theming
├── test/
│   └── widget_name_test.dart
└── pubspec.yaml
```

## Barrel Export Pattern

Every widget package needs a barrel export file:

```dart
// lib/app_widget_name.dart
library app_widget_name;

export 'src/main_widget.dart';
export 'src/secondary_widget.dart';
// Export all public widgets
```

## Widget Implementation Patterns

### Stateless Widget
```dart
import 'package:flutter/material.dart';

class CustomButton extends StatelessWidget {
  final String label;
  final VoidCallback? onPressed;

  const CustomButton({
    super.key,
    required this.label,
    this.onPressed,
  });

  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      onPressed: onPressed,
      child: Text(label),
    );
  }
}
```

### Platform Adaptive Widget
```dart
import 'dart:io' show Platform;
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

class AdaptiveButton extends StatelessWidget {
  final String label;
  final VoidCallback? onPressed;

  const AdaptiveButton({
    super.key,
    required this.label,
    this.onPressed,
  });

  @override
  Widget build(BuildContext context) {
    if (Platform.isIOS || Platform.isMacOS) {
      return CupertinoButton(
        onPressed: onPressed,
        child: Text(label),
      );
    }
    return ElevatedButton(
      onPressed: onPressed,
      child: Text(label),
    );
  }
}
```

## Dependencies

In widget package `pubspec.yaml`:

```yaml
name: app_widget_name
description: Widget description

environment:
  sdk: ">=3.8.0 <4.0.0"

dependencies:
  flutter:
    sdk: flutter

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^6.0.0
```

## Workspace Registration

Add new widget packages to root `pubspec.yaml`:

```yaml
workspace:
  # existing packages...
  - app_widget/widget_name
```

## Using Widgets in Main App

Import the package:

```dart
import 'package:app_widget_name/app_widget_name.dart';

// Use in widget tree
CustomButton(
  label: 'Click me',
  onPressed: () => print('Clicked'),
)
```

## Testing

Create widget tests in package `test/` directory:

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:app_widget_name/app_widget_name.dart';

void main() {
  testWidgets('CustomButton renders label', (tester) async {
    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: CustomButton(label: 'Test'),
        ),
      ),
    );
    expect(find.text('Test'), findsOneWidget);
  });
}
```

Run tests: `cd app_widget/widget_name && flutter test`

## Existing Widget Packages Reference

- **app_adaptive_widgets**: `AppAdaptiveScaffold`, responsive layouts
- **app_artwork**: `LaddingPageLottie`, SVG icons, images
- **app_feedback**: Snackbar helpers, dialog utilities
- **app_web_view**: WebView wrapper with platform support
