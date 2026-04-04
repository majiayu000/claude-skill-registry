# Flutter Skill - Mobile App Development

## Description

Flutter expert for cross-platform mobile app development with Dart, Riverpod state management, GoRouter navigation, Dio HTTP client, and widget-based architecture.

## When to Use

Use this skill when:

- Creating Flutter widgets or screens
- Setting up state management with Riverpod
- Implementing navigation with GoRouter
- Integrating with backend APIs
- Writing widget tests
- Fixing Flutter-specific bugs
- Optimizing mobile app performance

## MCP Server Setup

### Official Dart & Flutter MCP Server

Add to your Claude Code MCP configuration:

```json
{
  "mcpServers": {
    "dart": {
      "command": "dart",
      "args": ["mcp-server"]
    }
  }
}
```

**Requirements:** Dart 3.9+

### Flutter MCP (Real-time Documentation)

```bash
npx flutter-mcp
```

Or add to MCP config:

```json
{
  "mcpServers": {
    "flutter-mcp": {
      "command": "npx",
      "args": ["flutter-mcp"]
    }
  }
}
```

**Features:**

- Real-time Flutter/Dart documentation
- All 50,000+ pub.dev packages
- Version-specific docs
- Local caching

## Key Commands

```bash
# Create new Flutter project
flutter create --org com.example --project-name diddit apps/flutter

# Run app
cd apps/flutter && flutter run

# Run tests
flutter test

# Analyze code
flutter analyze

# Format code
dart format .

# Generate code (Riverpod, Freezed, JSON)
dart run build_runner build --delete-conflicting-outputs

# Build APK
flutter build apk --release

# Build iOS
flutter build ios --release
```

## Project Structure

```
apps/flutter/
├── lib/
│   ├── main.dart
│   ├── app.dart
│   ├── router/
│   ├── core/
│   │   ├── constants/
│   │   ├── theme/
│   │   └── utils/
│   ├── features/
│   │   ├── auth/
│   │   ├── tasks/
│   │   ├── rewards/
│   │   └── family/
│   └── shared/
│       ├── widgets/
│       ├── services/
│       └── providers/
├── test/
├── pubspec.yaml
└── analysis_options.yaml
```

## Code Patterns

### Widget Pattern

```dart
class TaskCard extends ConsumerWidget {
  const TaskCard({
    super.key,
    required this.task,
    required this.onTap,
  });

  final Task task;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Card(
      child: ListTile(
        title: Text(task.title),
        onTap: onTap,
      ),
    );
  }
}
```

### Provider Pattern

```dart
@riverpod
class TasksNotifier extends _$TasksNotifier {
  @override
  Future<List<Task>> build() async {
    return ref.read(taskRepositoryProvider).getTasks();
  }

  Future<void> addTask(Task task) async {
    state = const AsyncLoading();
    state = await AsyncValue.guard(() async {
      await ref.read(taskRepositoryProvider).addTask(task);
      return ref.read(taskRepositoryProvider).getTasks();
    });
  }
}
```

### Repository Pattern

```dart
class TaskRepositoryImpl implements TaskRepository {
  TaskRepositoryImpl(this._dio);
  final Dio _dio;

  @override
  Future<List<Task>> getTasks() async {
    final response = await _dio.get('/api/tasks');
    return (response.data as List)
        .map((json) => Task.fromJson(json))
        .toList();
  }
}
```

## Dependencies

```yaml
dependencies:
  flutter_riverpod: ^2.5.0
  riverpod_annotation: ^2.3.0
  go_router: ^14.0.0
  dio: ^5.4.0
  shared_preferences: ^2.2.0
  flutter_secure_storage: ^9.0.0
  freezed_annotation: ^2.4.0
  json_annotation: ^4.8.1

dev_dependencies:
  build_runner: ^2.4.0
  riverpod_generator: ^2.4.0
  freezed: ^2.4.0
  json_serializable: ^6.7.0
  mockito: ^5.4.4
```

## Quality Checklist

- [ ] `const` constructors used
- [ ] State management with Riverpod
- [ ] Error handling implemented
- [ ] Loading states shown
- [ ] Accessibility (Semantics)
- [ ] Tests passing
- [ ] `flutter analyze` clean
- [ ] Code formatted

## Resources

- [Flutter Docs](https://docs.flutter.dev)
- [Riverpod Docs](https://riverpod.dev)
- [GoRouter Docs](https://pub.dev/packages/go_router)
- [Dart MCP Server](https://docs.flutter.dev/ai/mcp-server)
- [Flutter MCP](https://github.com/adamsmaka/flutter-mcp)

## Agent Reference

See `.github/agents/flutter-agent.md` for complete agent specification.
