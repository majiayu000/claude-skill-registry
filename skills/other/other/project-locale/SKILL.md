---
name: project-locale
description: Guide for adding localized text using l10n in app_lib/locale package (project)
---

# Flutter Localization Skill

This skill guides adding localized text following this project's l10n conventions.

## When to Use

Trigger this skill when:
- Adding new user-facing text to the app
- Creating new screens or widgets with text content
- User asks to "add text", "localize", "translate", or "add string"

## Package Location

All localization files are in `app_lib/locale/`:

```
app_lib/locale/
├── l10n.yaml              # Flutter gen-l10n configuration
├── lib/
│   ├── app_locale.dart    # Main export with delegates
│   ├── arb/
│   │   └── app_en.arb     # Template ARB file (English)
│   ├── extensions/
│   │   └── build_context.dart  # context.l10n extension
│   └── gen_l10n/          # Generated files (do not edit)
└── pubspec.yaml
```

## Adding New Text

### Step 1: Add to ARB File

Edit `app_lib/locale/lib/arb/app_en.arb`:

```json
{
  "@@locale": "en",
  "existingKey": "Existing text",
  "newKey": "Your new text here",
  "newKeyWithParam": "Hello {name}!",
  "@newKeyWithParam": {
    "placeholders": {
      "name": {
        "type": "String",
        "example": "John"
      }
    }
  }
}
```

### Step 2: Regenerate Localizations

```bash
melos run gen-l10n
```

Or from the locale package:

```bash
cd app_lib/locale && flutter gen-l10n
```

### Step 3: Use in Widgets

```dart
import 'package:app_locale/app_locale.dart';

// In a widget's build method:
Text(context.l10n.newKey)
Text(context.l10n.newKeyWithParam(userName))
```

## ARB Key Naming Conventions

| Pattern | Example | Use Case |
|---------|---------|----------|
| `camelCase` | `welcomeMessage` | Simple text |
| `screenAction` | `homeTitle`, `settingsBack` | Screen-specific text |
| `navItem` | `navHome`, `navSettings` | Navigation items |
| `btnAction` | `btnSubmit`, `btnCancel` | Button labels |
| `errorType` | `errorNetwork`, `errorAuth` | Error messages |
| `msgType` | `msgSuccess`, `msgLoading` | Status messages |

## Parameterized Strings

### Basic Parameter

```json
{
  "greeting": "Hello {name}!",
  "@greeting": {
    "placeholders": {
      "name": {"type": "String"}
    }
  }
}
```

Usage: `context.l10n.greeting('Alice')`

### Multiple Parameters

```json
{
  "itemCount": "{count} items in {category}",
  "@itemCount": {
    "placeholders": {
      "count": {"type": "int"},
      "category": {"type": "String"}
    }
  }
}
```

Usage: `context.l10n.itemCount(5, 'Books')`

### Pluralization

```json
{
  "itemsSelected": "{count, plural, =0{No items} =1{1 item} other{{count} items}} selected",
  "@itemsSelected": {
    "placeholders": {
      "count": {"type": "int"}
    }
  }
}
```

## Adding New Locales

### Step 1: Create New ARB File

Copy `app_en.arb` to `app_<locale>.arb` (e.g., `app_zh.arb`):

```bash
cp app_lib/locale/lib/arb/app_en.arb app_lib/locale/lib/arb/app_zh.arb
```

### Step 2: Update Locale Tag

Change `"@@locale": "en"` to `"@@locale": "zh"` and translate all values.

### Step 3: Register Locale

Edit `app_lib/locale/lib/app_locale.dart`:

```dart
static List<Locale> supportedLocales = [
  const Locale('en'), // English
  const Locale('zh'), // Chinese
];
```

### Step 4: Regenerate

```bash
melos run gen-l10n
```

## Best Practices

1. **Always use l10n** - Never hardcode user-facing strings
2. **Descriptive keys** - Use meaningful camelCase key names
3. **Group related strings** - Use prefixes (nav*, btn*, error*, etc.)
4. **Document placeholders** - Always include `@key` metadata for parameterized strings
5. **Run gen-l10n** - Always regenerate after ARB changes
6. **Test with context** - Ensure widgets have BuildContext access for l10n

## Quick Reference

```dart
// Import
import 'package:app_locale/app_locale.dart';

// Simple text
context.l10n.appName

// With parameter
context.l10n.greeting(userName)

// In non-widget context (pass context)
AppLocalizations.of(context).appName
```

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `l10n not found` | Missing import | Add `import 'package:app_locale/app_locale.dart';` |
| `key undefined` | Not regenerated | Run `melos run gen-l10n` |
| `null check` | No localization delegate | Ensure `AppLocale.localizationsDelegates` in MaterialApp |
