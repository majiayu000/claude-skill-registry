---
name: "flutter-localizing-apps"
description: "Configures a Flutter app to support multiple languages and regions. Use when preparing an application for international markets and diverse user locales."
metadata:
  model: "models/gemini-3.1-pro-preview"
  last_modified: "Thu, 12 Mar 2026 22:17:07 GMT"

---
# Localizing Flutter Applications

## Contents
- [Core Configuration](#core-configuration)
- [Defining ARB Resources](#defining-arb-resources)
- [App Integration](#app-integration)
- [Advanced Formatting](#advanced-formatting)
- [Workflows](#workflows)
- [Troubleshooting & Gotchas](#troubleshooting--gotchas)

## Core Configuration

Configure the project to support code generation for localizations.

1. Add required dependencies to `pubspec.yaml`:
```yaml
dependencies:
  flutter:
    sdk: flutter
  flutter_localizations:
    sdk: flutter
  intl: any

flutter:
  generate: true # Required for l10n code generation
```

2. Create an `l10n.yaml` file in the project root to configure the `gen-l10n` tool:
```yaml
arb-dir: lib/l10n
template-arb-file: app_en.arb
output-localization-file: app_localizations.dart
# Optional: Set to false to generate files into lib/ instead of the synthetic package
# synthetic-package: false 
```

## Defining ARB Resources

Store localized strings in Application Resource Bundle (`.arb`) files within the configured `arb-dir`.

Create the template file (e.g., `lib/l10n/app_en.arb`):
```json
{
  "helloWorld": "Hello World!",
  "@helloWorld": {
    "description": "The conventional newborn programmer greeting"
  }
}
```

Create translation files (e.g., `lib/l10n/app_es.arb`):
```json
{
  "helloWorld": "¡Hola Mundo!"
}
```

## App Integration

Initialize the `Localizations` widget by configuring the root `MaterialApp` or `CupertinoApp`.

```dart
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart'; // Adjust import if synthetic-package is false

return MaterialApp(
  title: 'Localized App',
  localizationsDelegates: const [
    AppLocalizations.delegate,
    GlobalMaterialLocalizations.delegate,
    GlobalWidgetsLocalizations.delegate,
    GlobalCupertinoLocalizations.delegate,
  ],
  supportedLocales: const [
    Locale('en'), // English
    Locale('es'), // Spanish
  ],
  home: const MyHomePage(),
);
```

Access localized values in the widget tree using the generated `AppLocalizations` class:
```dart
Text(AppLocalizations.of(context)!.helloWorld)
```

*Note: If using `WidgetsApp` instead of `MaterialApp`, omit `GlobalMaterialLocalizations.delegate`.*

## Advanced Formatting

Use placeholders, plurals, and selects for dynamic content. Define parameters in the `@key` metadata.

### Placeholders
```json
"hello": "Hello {userName}",
"@hello": {
  "description": "A message with a single parameter",
  "placeholders": {
    "userName": {
      "type": "String",
      "example": "Bob"
    }
  }
}
```

### Plurals
```json
"nWombats": "{count, plural, =0{no wombats} =1{1 wombat} other{{count} wombats}}",
"@nWombats": {
  "placeholders": {
    "count": {
      "type": "num",
      "format": "compact"
    }
  }
}
```

### Selects (Gender/Enums)
```json
"pronoun": "{gender, select, male{he} female{she} other{they}}",
"@pronoun": {
  "placeholders": {
    "gender": {
      "type": "String"
    }
  }
}
```

### Dates and Numbers
Use `format` and `optionalParameters` to leverage `intl` formatting.
```json
"dateMessage": "Date: {date}",
"@dateMessage": {
  "placeholders": {
    "date": {
      "type": "DateTime",
      "format": "yMd"
    }
  }
}
```

## Workflows

### Task Progress: Adding a New Language
Copy this checklist to track progress when introducing a new locale.

- [ ] Create a new `.arb` file in the `arb-dir` (e.g., `app_fr.arb`).
- [ ] Translate all keys present in the template `.arb` file.
- [ ] Add the new `Locale` to the `supportedLocales` list in `MaterialApp`.
- [ ] Run validator -> Execute `flutter gen-l10n` to verify ARB syntax and regenerate `AppLocalizations`.
- [ ] Review errors -> Fix any missing placeholders or malformed plural/select statements.
- [ ] If targeting iOS, complete the "Configuring iOS App Bundle" workflow.

### Task Progress: Configuring iOS App Bundle
Flutter handles runtime localization, but iOS requires bundle-level configuration for the App Store and system settings.

- [ ] Open `ios/Runner.xcodeproj` in Xcode.
- [ ] Select the `Runner` project in the Project Navigator.
- [ ] Navigate to the `Info` tab.
- [ ] Under the **Localizations** section, click the `+` button.
- [ ] Add the newly supported languages/regions.
- [ ] Run validator -> Build the iOS app to ensure `project.pbxproj` is correctly updated.

## Troubleshooting & Gotchas

### Missing Localizations Ancestor
Widgets like `TextField` and `CupertinoTabBar` require a `Localizations` ancestor with specific delegates (`MaterialLocalizations` or `CupertinoLocalizations`). 

**Error:** `No MaterialLocalizations found.` or `CupertinoTabBar requires a Localizations parent...`
**Fix:** Ensure the widget is a descendant of `MaterialApp`/`CupertinoApp`. If building a standalone widget tree (e.g., in tests or a custom `WidgetsApp`), wrap the widget in a `Localizations` widget:

```dart
Localizations(
  locale: const Locale('en', 'US'),
  delegates: const [
    DefaultWidgetsLocalizations.delegate,
    DefaultMaterialLocalizations.delegate, // Required for TextField
    DefaultCupertinoLocalizations.delegate, // Required for CupertinoTabBar
  ],
  child: child,
)
```

### Advanced Locale Definition
If supporting languages with multiple scripts (e.g., Chinese), use `Locale.fromSubtags` to explicitly define the `scriptCode` and `countryCode` to prevent Flutter from resolving to an unexpected variant.

```dart
supportedLocales: const [
  Locale.fromSubtags(languageCode: 'zh', scriptCode: 'Hans', countryCode: 'CN'),
  Locale.fromSubtags(languageCode: 'zh', scriptCode: 'Hant', countryCode: 'TW'),
]
```
