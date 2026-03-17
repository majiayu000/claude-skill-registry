---
name: project-database
description: Guide for using app_database package with Drift for user settings, app config, and persistent data (project)
---

# Flutter Database Skill

This skill guides the implementation of persistent local storage using the `app_database` package, which uses Drift (SQLite) for structured data storage.

## When to Use

Trigger this skill when:
- Storing user settings or preferences
- Saving app configuration data
- Persisting structured data (lists, objects, relationships)
- Caching data for offline access
- User asks to "save to database", "persist data", "store settings", "create table"

**Note:** For sensitive data like tokens or passwords, use `app_secure_storage` instead.

## Package Location

```
app_lib/database/
├── lib/
│   ├── app_database.dart              # Barrel export
│   └── src/
│       ├── database.dart              # Main database class
│       ├── database.g.dart            # Generated code
│       └── type_converter.dart        # Custom type converters
├── pubspec.yaml
└── test/
```

## Package Import

```dart
import 'package:app_database/app_database.dart';
```

## Accessing the Database

The `AppDatabase` is injected via `MainProvider` and available throughout the app:

```dart
import 'package:app_database/app_database.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

// In any widget with access to BuildContext
final db = context.read<AppDatabase>();
```

## Adding a New Table

### Step 1: Define the Table

Add table definition in `app_lib/database/lib/src/database.dart`:

```dart
import 'package:drift/drift.dart';
import 'package:drift/native.dart';
import 'package:drift_flutter/drift_flutter.dart';
import 'package:path_provider/path_provider.dart';

part 'database.g.dart';

// Define the table
class UserSettings extends Table {
  IntColumn get id => integer().autoIncrement()();
  TextColumn get key => text().unique()();
  TextColumn get value => text()();
  DateTimeColumn get updatedAt => dateTime().withDefault(currentDateAndTime)();
}

// Register the table in the database
@DriftDatabase(tables: [UserSettings])
class AppDatabase extends _$AppDatabase {
  AppDatabase([QueryExecutor? executor]) : super(executor ?? _openConnection());

  factory AppDatabase.forTesting() {
    return AppDatabase(NativeDatabase.memory());
  }

  @override
  int get schemaVersion => 2;  // Increment when changing schema

  // ... rest of the class
}
```

### Step 2: Generate Code

Run build_runner to generate the database code:

```bash
cd app_lib/database
dart run build_runner build --delete-conflicting-outputs
```

Or from the project root:

```bash
melos run build-runner
```

### Step 3: Handle Migration (if updating existing table)

Add migration logic in the database class:

```dart
@override
MigrationStrategy get migration {
  return MigrationStrategy(
    onCreate: (Migrator m) async {
      await m.createAll();
    },
    onUpgrade: (Migrator m, int from, int to) async {
      if (from < 2) {
        await m.createTable(userSettings);
      }
    },
  );
}
```

## Common Table Patterns

### Key-Value Settings Table

```dart
class AppSettings extends Table {
  IntColumn get id => integer().autoIncrement()();
  TextColumn get key => text().unique()();
  TextColumn get value => text()();
  DateTimeColumn get updatedAt => dateTime().withDefault(currentDateAndTime)();
}
```

### User Preferences Table

```dart
class UserPreferences extends Table {
  IntColumn get id => integer().autoIncrement()();
  TextColumn get theme => text().withDefault(const Constant('system'))();
  TextColumn get language => text().withDefault(const Constant('en'))();
  BoolColumn get notificationsEnabled => boolean().withDefault(const Constant(true))();
  IntColumn get fontSize => integer().withDefault(const Constant(14))();
  DateTimeColumn get createdAt => dateTime().withDefault(currentDateAndTime)();
  DateTimeColumn get updatedAt => dateTime().withDefault(currentDateAndTime)();
}
```

### Cached Items Table

```dart
class CachedItems extends Table {
  IntColumn get id => integer().autoIncrement()();
  TextColumn get itemId => text().unique()();
  TextColumn get jsonData => text()();
  DateTimeColumn get cachedAt => dateTime().withDefault(currentDateAndTime)();
  DateTimeColumn get expiresAt => dateTime().nullable()();
}
```

### Favorites/Bookmarks Table

```dart
class Favorites extends Table {
  IntColumn get id => integer().autoIncrement()();
  TextColumn get itemId => text()();
  TextColumn get itemType => text()();  // 'article', 'product', etc.
  TextColumn get title => text()();
  TextColumn get metadata => text().nullable()();  // JSON string
  DateTimeColumn get createdAt => dateTime().withDefault(currentDateAndTime)();

  @override
  List<Set<Column>> get uniqueKeys => [
    {itemId, itemType},  // Composite unique key
  ];
}
```

## Writing Queries

### Basic CRUD in Database Class

Add methods to `AppDatabase` class:

```dart
@DriftDatabase(tables: [UserSettings])
class AppDatabase extends _$AppDatabase {
  // ... constructor and config

  // Create or Update a setting
  Future<void> setSetting(String key, String value) async {
    await into(userSettings).insertOnConflictUpdate(
      UserSettingsCompanion(
        key: Value(key),
        value: Value(value),
        updatedAt: Value(DateTime.now()),
      ),
    );
  }

  // Read a setting
  Future<String?> getSetting(String key) async {
    final result = await (select(userSettings)
      ..where((t) => t.key.equals(key)))
      .getSingleOrNull();
    return result?.value;
  }

  // Delete a setting
  Future<void> deleteSetting(String key) async {
    await (delete(userSettings)..where((t) => t.key.equals(key))).go();
  }

  // Get all settings
  Future<Map<String, String>> getAllSettings() async {
    final results = await select(userSettings).get();
    return Map.fromEntries(
      results.map((r) => MapEntry(r.key, r.value)),
    );
  }

  // Watch a setting (reactive stream)
  Stream<String?> watchSetting(String key) {
    return (select(userSettings)..where((t) => t.key.equals(key)))
        .watchSingleOrNull()
        .map((result) => result?.value);
  }
}
```

### Using DAOs for Organization

For complex tables, create separate DAO classes:

```dart
// In database.dart
part 'settings_dao.dart';

@DriftDatabase(tables: [UserSettings], daos: [SettingsDao])
class AppDatabase extends _$AppDatabase {
  // ...
}
```

```dart
// In settings_dao.dart
part of 'database.dart';

@DriftAccessor(tables: [UserSettings])
class SettingsDao extends DatabaseAccessor<AppDatabase> with _$SettingsDaoMixin {
  SettingsDao(super.db);

  Future<void> setSetting(String key, String value) async {
    await into(userSettings).insertOnConflictUpdate(
      UserSettingsCompanion(
        key: Value(key),
        value: Value(value),
        updatedAt: Value(DateTime.now()),
      ),
    );
  }

  Future<String?> getSetting(String key) async {
    final result = await (select(userSettings)
      ..where((t) => t.key.equals(key)))
      .getSingleOrNull();
    return result?.value;
  }

  Stream<String?> watchSetting(String key) {
    return (select(userSettings)..where((t) => t.key.equals(key)))
        .watchSingleOrNull()
        .map((result) => result?.value);
  }
}
```

## Complete Example: Settings Repository

### Define the Table and Queries

```dart
// database.dart
class AppSettings extends Table {
  IntColumn get id => integer().autoIncrement()();
  TextColumn get key => text().unique()();
  TextColumn get value => text()();
  DateTimeColumn get updatedAt => dateTime().withDefault(currentDateAndTime)();
}

@DriftDatabase(tables: [AppSettings])
class AppDatabase extends _$AppDatabase {
  // ... constructor

  @override
  int get schemaVersion => 2;

  // Settings methods
  Future<void> setSetting(String key, String value) async {
    await into(appSettings).insertOnConflictUpdate(
      AppSettingsCompanion(
        key: Value(key),
        value: Value(value),
        updatedAt: Value(DateTime.now()),
      ),
    );
  }

  Future<String?> getSetting(String key) async {
    final result = await (select(appSettings)
      ..where((t) => t.key.equals(key)))
      .getSingleOrNull();
    return result?.value;
  }

  Stream<String?> watchSetting(String key) {
    return (select(appSettings)..where((t) => t.key.equals(key)))
        .watchSingleOrNull()
        .map((result) => result?.value);
  }
}
```

### Create a Settings Repository

```dart
// lib/repositories/settings_repository.dart
import 'package:app_database/app_database.dart';

class SettingsRepository {
  final AppDatabase _db;

  SettingsRepository(this._db);

  // Theme settings
  static const _themeKey = 'app_theme';

  Future<String> getTheme() async {
    return await _db.getSetting(_themeKey) ?? 'system';
  }

  Future<void> setTheme(String theme) async {
    await _db.setSetting(_themeKey, theme);
  }

  Stream<String> watchTheme() {
    return _db.watchSetting(_themeKey).map((v) => v ?? 'system');
  }

  // Language settings
  static const _languageKey = 'app_language';

  Future<String> getLanguage() async {
    return await _db.getSetting(_languageKey) ?? 'en';
  }

  Future<void> setLanguage(String language) async {
    await _db.setSetting(_languageKey, language);
  }

  // Onboarding completed
  static const _onboardingKey = 'onboarding_completed';

  Future<bool> isOnboardingCompleted() async {
    final value = await _db.getSetting(_onboardingKey);
    return value == 'true';
  }

  Future<void> setOnboardingCompleted(bool completed) async {
    await _db.setSetting(_onboardingKey, completed.toString());
  }
}
```

### Use in Widget with Stream

```dart
class SettingsScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final db = context.read<AppDatabase>();

    return StreamBuilder<String?>(
      stream: db.watchSetting('app_theme'),
      builder: (context, snapshot) {
        final theme = snapshot.data ?? 'system';

        return ListTile(
          title: const Text('Theme'),
          subtitle: Text(theme),
          onTap: () => _showThemePicker(context, db),
        );
      },
    );
  }

  void _showThemePicker(BuildContext context, AppDatabase db) {
    showDialog(
      context: context,
      builder: (context) => SimpleDialog(
        title: const Text('Select Theme'),
        children: ['system', 'light', 'dark'].map((theme) {
          return SimpleDialogOption(
            onPressed: () {
              db.setSetting('app_theme', theme);
              Navigator.pop(context);
            },
            child: Text(theme),
          );
        }).toList(),
      ),
    );
  }
}
```

## Type Converters

### Built-in StringListConverter

The package includes a converter for `List<String>`:

```dart
class Tags extends Table {
  IntColumn get id => integer().autoIncrement()();
  TextColumn get tags => text().map(const StringListConverter())();
}
```

### Custom JSON Converter

For complex objects:

```dart
class JsonMapConverter extends TypeConverter<Map<String, dynamic>, String> {
  const JsonMapConverter();

  @override
  Map<String, dynamic> fromSql(String fromDb) {
    return json.decode(fromDb) as Map<String, dynamic>;
  }

  @override
  String toSql(Map<String, dynamic> value) {
    return json.encode(value);
  }
}

// Usage
class CachedData extends Table {
  IntColumn get id => integer().autoIncrement()();
  TextColumn get data => text().map(const JsonMapConverter())();
}
```

### Enum Converter

```dart
enum SyncStatus { pending, synced, failed }

class SyncStatusConverter extends TypeConverter<SyncStatus, String> {
  const SyncStatusConverter();

  @override
  SyncStatus fromSql(String fromDb) {
    return SyncStatus.values.firstWhere((e) => e.name == fromDb);
  }

  @override
  String toSql(SyncStatus value) {
    return value.name;
  }
}
```

## Testing

### In-Memory Database for Tests

```dart
void main() {
  late AppDatabase db;

  setUp(() {
    db = AppDatabase.forTesting();
  });

  tearDown(() async {
    await db.close();
  });

  test('saves and retrieves setting', () async {
    await db.setSetting('test_key', 'test_value');

    final result = await db.getSetting('test_key');
    expect(result, equals('test_value'));
  });

  test('watches setting changes', () async {
    final stream = db.watchSetting('watched_key');

    // Set up expectation
    expectLater(
      stream,
      emitsInOrder([null, 'first', 'second']),
    );

    // Trigger changes
    await db.setSetting('watched_key', 'first');
    await db.setSetting('watched_key', 'second');
  });
}
```

## Best Practices

1. **Use for structured data** - Database is ideal for relational data, lists, complex queries
2. **Use secure storage for secrets** - Don't store tokens/passwords in SQLite
3. **Increment schemaVersion** when changing table structure
4. **Write migrations** for production apps to preserve user data
5. **Use streams** for reactive UI updates with `watch*` methods
6. **Create repositories** to encapsulate database logic
7. **Use DAOs** for complex tables with many queries
8. **Use type converters** for custom types (enums, JSON, lists)
9. **Test with in-memory database** using `AppDatabase.forTesting()`
10. **Run build_runner** after changing table definitions

## When to Use Database vs Secure Storage vs SharedPreferences

| Use Case | Solution |
|----------|----------|
| API tokens, passwords | `app_secure_storage` |
| Simple key-value (theme, flags) | `SharedPreferences` or Database |
| Structured data, lists | `app_database` |
| Relational data | `app_database` |
| Offline cache | `app_database` |
| Complex queries needed | `app_database` |

## Drift Documentation

For advanced features (joins, transactions, custom queries), see:
- [Drift Documentation](https://drift.simonbinder.eu/)
- [Drift Getting Started](https://drift.simonbinder.eu/docs/getting-started/)

## Regenerate Database Code

After modifying tables:

```bash
# From app_lib/database directory
dart run build_runner build --delete-conflicting-outputs

# Or from project root
melos run build-runner
```
