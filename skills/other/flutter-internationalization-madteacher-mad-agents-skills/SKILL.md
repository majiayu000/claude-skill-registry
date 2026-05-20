---
name: flutter-internationalization
description: Complete guide for internationalizing Flutter apps using gen-l10n and intl packages. Use when Claude needs to add localization support to Flutter applications, translate UI text, format numbers/dates for different locales, or configure multi-language support for Material/Cupertino apps.
metadata:
  author: Stanislav [MADTeacher] Chernyshev
  version: "1.0"
---

# Flutter Internationalization

## Overview

Comprehensive guide for adding internationalization (i18n) to Flutter applications. Covers setup, configuration, message management, number/date formatting, and advanced topics like locale override and custom language support.

## Quick Start

Choose approach based on app needs:

**gen-l10n (Recommended)** - Modern, automated, code generation
- Best for: Most new projects, teams, complex apps
- Uses: ARB files, automated code generation
- See: [Setup gen-l10n](#setup-gen-l10n)

**intl package** - Manual control, code-based
- Best for: Simple apps, legacy projects, full control
- Uses: `Intl.message()` code, manual translation files
- See: [Setup intl package](#setup-intl-package)

**Manual/Custom** - Maximum flexibility
- Best for: Very simple apps, custom workflows
- Uses: Direct Map-based lookups
- See: [Custom localizations](#custom-localizations)

## Setup gen-l10n

### 1. Add Dependencies

Update `pubspec.yaml`:

```yaml
dependencies:
  flutter:
    sdk: flutter
  flutter_localizations:
    sdk: flutter
  intl: any
```

Run:

```bash
flutter pub add flutter_localizations --sdk=flutter
flutter pub add intl:any
```

### 2. Enable Code Generation

Add to `pubspec.yaml`:

```yaml
flutter:
  generate: true
```

### 3. Configure l10n.yaml

Create `l10n.yaml` in project root:

```yaml
arb-dir: lib/l10n
template-arb-file: app_en.arb
output-localization-file: app_localizations.dart
```

For advanced options, see [l10n-config.md](references/l10n-config.md).

### 4. Create ARB Files

Create directory `lib/l10n/`.

**Template file** `lib/l10n/app_en.arb`:

```json
{
  "helloWorld": "Hello World!",
  "@helloWorld": {
    "description": "Greeting message"
  }
}
```

**Translation file** `lib/l10n/app_es.arb`:

```json
{
  "helloWorld": "¡Hola Mundo!"
}
```

For complete ARB format, see [arb-format.md](references/arb-format.md).

### 5. Generate Code

Run:

```bash
flutter gen-l10n
```

Or run app to trigger auto-generation:

```bash
flutter run
```

### 6. Configure MaterialApp

Import and setup:

```dart
import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'l10n/app_localizations.dart';

MaterialApp(
  localizationsDelegates: [
    AppLocalizations.delegate,
    GlobalMaterialLocalizations.delegate,
    GlobalWidgetsLocalizations.delegate,
    GlobalCupertinoLocalizations.delegate,
  ],
  supportedLocales: [
    Locale('en'),
    Locale('es'),
  ],
  home: MyHomePage(),
)
```

### 7. Use Localizations

Access in widgets:

```dart
Text(AppLocalizations.of(context)!.helloWorld)
```

## Message Types

### Simple Messages

No parameters:

```json
{
  "welcome": "Welcome to our app",
  "@welcome": {
    "description": "Welcome message"
  }
}
```

### Placeholder Messages

With parameters:

```json
{
  "greeting": "Hello {userName}!",
  "@greeting": {
    "description": "Personalized greeting",
    "placeholders": {
      "userName": {
        "type": "String",
        "example": "Alice"
      }
    }
  }
}
```

Use in code:

```dart
Text(AppLocalizations.of(context)!.greeting('Alice'))
```

### Plural Messages

Based on count:

```json
{
  "itemCount": "{count, plural, =0{No items} =1{1 item} other{{count} items}}",
  "@itemCount": {
    "placeholders": {
      "count": {
        "type": "int"
      }
    }
  }
}
```

Use in code:

```dart
Text(AppLocalizations.of(context)!.itemCount(5))
```

### Select Messages

Based on string value:

```json
{
  "pronoun": "{gender, select, male{he} female{she} other{they}}",
  "@pronoun": {
    "placeholders": {
      "gender": {
        "type": "String"
      }
    }
  }
}
```

Use in code:

```dart
Text(AppLocalizations.of(context)!.pronoun('male'))
```

## Number and Date Formatting

### Numbers

Format numbers automatically:

```json
{
  "price": "Price: {value}",
  "@price": {
    "placeholders": {
      "value": {
        "type": "int",
        "format": "simpleCurrency"
      }
    }
  }
}
```

Format options: `compact`, `currency`, `simpleCurrency`, `decimalPattern`, etc.

### Dates

Format dates automatically:

```json
{
  "eventDate": "Event on {date}",
  "@eventDate": {
    "placeholders": {
      "date": {
        "type": "DateTime",
        "format": "yMMMd"
      }
    }
  }
}
```

Format options: `yMd`, `yMMMd`, `yMMMMd`, `Hm`, etc.

For complete formatting options, see [number-date-formats.md](references/number-date-formats.md).

## Advanced Topics

### Locale Override

Override locale for specific widgets:

```dart
Localizations.override(
  context: context,
  locale: const Locale('es'),
  child: CalendarDatePicker(...),
)
```

### Custom Locale Definitions

For complex locales (Chinese, French regions):

```dart
supportedLocales: [
  Locale.fromSubtags(languageCode: 'zh'),
  Locale.fromSubtags(languageCode: 'zh', scriptCode: 'Hans'),
  Locale.fromSubtags(languageCode: 'zh', scriptCode: 'Hant', countryCode: 'TW'),
]
```

### Locale Resolution Callback

Control locale fallback:

```dart
MaterialApp(
  localeResolutionCallback: (locale, supportedLocales) {
    // Always accept user's locale
    return locale;
  },
)
```

### Access Current Locale

Get current app locale:

```dart
Locale myLocale = Localizations.localeOf(context);
```

## Setup intl Package

### Manual Setup

1. Add dependencies (same as gen-l10n)
2. Create localization class:

```dart
class DemoLocalizations {
  DemoLocalizations(this.localeName);

  static Future<DemoLocalizations> load(Locale locale) {
    final String name = Intl.canonicalizedLocale(locale.toString());
    return initializeMessages(name).then((_) => DemoLocalizations(name));
  }

  static DemoLocalizations of(BuildContext context) {
    return Localizations.of<DemoLocalizations>(context, DemoLocalizations)!;
  }

  String get title {
    return Intl.message(
      'Hello World',
      name: 'title',
      desc: 'Title',
      locale: localeName,
    );
  }
}
```

3. Create delegate:

```dart
class DemoLocalizationsDelegate extends LocalizationsDelegate<DemoLocalizations> {
  const DemoLocalizationsDelegate();

  @override
  bool isSupported(Locale locale) => ['en', 'es'].contains(locale.languageCode);

  @override
  Future<DemoLocalizations> load(Locale locale) => DemoLocalizations.load(locale);

  @override
  bool shouldReload(DemoLocalizationsDelegate old) => false;
}
```

4. Generate ARB files:

```bash
dart run intl_translation:extract_to_arb --output-dir=lib/l10n lib/main.dart
dart run intl_translation:generate_from_arb --output-dir=lib/l10n lib/main.dart lib/l10n/intl_*.arb
```

## Custom Localizations

For maximum simplicity:

```dart
class DemoLocalizations {
  DemoLocalizations(this.locale);

  final Locale locale;

  static DemoLocalizations of(BuildContext context) {
    return Localizations.of<DemoLocalizations>(context, DemoLocalizations)!;
  }

  static const _localizedValues = <String, Map<String, String>>{
    'en': {'title': 'Hello World'},
    'es': {'title': 'Hola Mundo'},
  };

  String get title {
    return _localizedValues[locale.languageCode]!['title']!;
  }
}
```

## Best Practices

1. **Use gen-l10n** for new projects - simpler, safer, better tooling
2. **Add descriptions** to ARB entries - provides context for translators
3. **Format numbers/dates** with format types - automatic locale handling
4. **Test all locales** - verify formatting, RTL, and translations
5. **Use pluralization** - handle count variations correctly
6. **Keep messages short** - easier to translate, more consistent
7. **Don't concatenate strings** - use placeholders instead
8. **Enable nullable-getter** to reduce null checks in user code

## Resources

### references/

**l10n-config.md** - Complete reference for `l10n.yaml` configuration options, including output directories, code generation settings, and locale handling.

**arb-format.md** - Comprehensive guide to ARB file format, covering simple messages, placeholders, plurals, selects, and metadata.

**number-date-formats.md** - Number and date formatting reference with format types, patterns, and locale-specific examples.

### assets/

Example templates and boilerplate code can be added here for common internationalization patterns.

## When to Use This Skill

Use this skill when:
- Adding localization support to a new Flutter app
- Translating existing Flutter app to multiple languages
- Configuring number/date formatting for different locales
- Setting up RTL (right-to-left) language support
- Implementing locale-specific layouts or widgets
- Managing ARB files and translations
- Troubleshooting localization issues
- Adding custom language support beyond built-in locales
- Optimizing app bundle size with deferred loading
