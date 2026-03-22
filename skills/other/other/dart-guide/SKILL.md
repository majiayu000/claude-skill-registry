---
name: dart-guide
description: |
  Dart language guardrails, patterns, and best practices for AI-assisted development.
  Use when working with Dart files (.dart), pubspec.yaml, or when the user mentions Dart/Flutter.
  Provides null safety patterns, async/await guidelines, Flutter integration conventions,
  and testing standards specific to this project's coding standards.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: language
  language: dart
  extensions: ".dart"
---

# Dart Guide

> Applies to: Dart 3.0+, Sound Null Safety, Flutter, Server-side Dart

## Core Principles

1. **Sound Null Safety**: The type system guarantees non-nullable by default; nullable types are explicit
2. **Async by Design**: Use Futures, Streams, and async/await for all I/O and event-driven logic
3. **Immutability First**: Prefer `final` locals, `const` constructors, and immutable data structures
4. **Composition Over Inheritance**: Use mixins, extension methods, and sealed class hierarchies
5. **Effective Dart**: Follow official Effective Dart style for naming, documentation, and API design

## Guardrails

### Version & Dependencies

- Use Dart 3.0+ with sound null safety enabled (no `// @dart=2.x` opt-outs)
- Manage dependencies with `pubspec.yaml`; run `dart pub get` after changes
- Pin dependency versions with caret syntax (`^1.2.0`) for libraries, exact for apps
- Run `dart pub outdated` periodically to check for updates
- Audit transitive dependencies with `dart pub deps`

### Code Style

- Run `dart format .` before every commit (line length: 80 characters)
- Run `dart analyze` with strict mode before committing
- Libraries/packages: `lowercase_with_underscores` (`my_package`)
- Classes/enums/typedefs: `UpperCamelCase` (`UserProfile`)
- Functions/variables/parameters: `lowerCamelCase` (`fetchUser`)
- Constants: `lowerCamelCase` (`defaultTimeout`, not `DEFAULT_TIMEOUT`)
- Private members: prefix with `_` (`_internalState`)
- Follow [Effective Dart](https://dart.dev/effective-dart) guidelines

### Null Safety

- Never use `!` (null assertion) without a preceding null check or guarantee
- Use `?` for nullable types only at API boundaries (JSON, platform channels)
- Prefer `??` (if-null) and `?.` (null-aware access) over explicit null checks
- Use `required` keyword for non-optional named parameters
- Use `late` only when initialization is guaranteed before access (avoid for laziness)

```dart
// BAD: crashes at runtime if null
final name = json['name'] as String;

// GOOD: explicit nullable handling
final name = json['name'] as String? ?? 'Unknown';

// GOOD: required parameter enforces non-null at call site
void createUser({required String name, required String email}) { ... }

// BAD: late used for laziness without guarantees
late final String config;

// GOOD: late with guaranteed initialization in constructor body
late final Database _db;
void init(Database db) => _db = db;
```

### Async/Await

- Always `await` Futures or return them; never fire-and-forget without error handling
- Use `async*` and `yield` for Stream generators
- Set timeouts on all external calls with `.timeout(Duration(...))`
- Catch specific exceptions, not bare `catch (e)`
- Use `Completer` only when bridging callback-based APIs to Futures

```dart
// BAD: fire-and-forget loses errors
void save() {
  repository.save(data); // Future ignored
}

// GOOD: propagate or handle
Future<void> save() async {
  await repository.save(data);
}

// GOOD: timeout on external calls
final response = await http.get(uri).timeout(
  const Duration(seconds: 10),
  onTimeout: () => throw TimeoutException('Request timed out'),
);
```

### Immutability

- Use `final` for all local variables that are not reassigned
- Use `const` constructors for compile-time constant objects (widgets, values)
- Prefer `UnmodifiableListView` or immutable collections from `package:collection`
- Use records for lightweight immutable data groupings
- Mark classes `@immutable` when all fields are final

## Project Structure

```
myproject/
├── lib/
│   ├── src/                   # Private implementation
│   │   ├── models/            # Data classes, records, sealed types
│   │   ├── services/          # Business logic, use cases
│   │   ├── repositories/      # Data access layer
│   │   └── utils/             # Shared utilities, extensions
│   └── my_package.dart        # Public barrel export file
├── bin/                       # CLI entry points (for command-line apps)
│   └── main.dart
├── test/                      # Tests (mirrors lib/src/ structure)
│   ├── models/
│   ├── services/
│   └── repositories/
├── pubspec.yaml               # Dependencies and metadata
├── analysis_options.yaml      # Linter and analyzer configuration
└── README.md
```

- `lib/src/` for private implementation; export public API from `lib/my_package.dart`
- `test/` mirrors `lib/src/` directory structure
- `bin/` only for executable entry points
- No business logic in `main.dart` (delegate to services)

## Key Patterns

### Records and Pattern Matching (Dart 3)

```dart
// Records: lightweight immutable tuples with named fields
typedef UserSummary = ({String name, String email, int age});

UserSummary fetchSummary() => (name: 'Alice', email: 'a@b.com', age: 30);

// Destructuring with pattern matching
final (name: userName, email: _, age: userAge) = fetchSummary();

// Switch expressions with patterns
String classify(Object value) => switch (value) {
  int n when n < 0   => 'negative',
  int n when n == 0  => 'zero',
  int()              => 'positive',
  String s           => 'string: $s',
  (int x, int y)     => 'point ($x, $y)',
  _                  => 'unknown',
};
```

### Sealed Classes and Exhaustive Matching

```dart
sealed class Result<T> {
  const Result();
}

final class Success<T> extends Result<T> {
  final T value;
  const Success(this.value);
}

final class Failure<T> extends Result<T> {
  final String message;
  final Object? error;
  const Failure(this.message, [this.error]);
}

// Exhaustive switch: compiler enforces all subtypes handled
String describe<T>(Result<T> result) => switch (result) {
  Success(:final value) => 'Success: $value',
  Failure(:final message) => 'Failed: $message',
};
```

### Extension Methods and Types

```dart
// Extension methods: add functionality to existing types
extension StringValidation on String {
  bool get isValidEmail => RegExp(r'^[\w-.]+@[\w-]+\.\w+$').hasMatch(this);
  String truncate(int maxLength) =>
      length <= maxLength ? this : '${substring(0, maxLength)}...';
}

// Extension types (Dart 3.3): zero-cost type wrappers
extension type UserId(String value) {
  UserId.generate() : value = Uuid().v4();
  bool get isValid => value.isNotEmpty;
}

// Usage: compile-time type safety, zero runtime overhead
void fetchUser(UserId id) { ... }
fetchUser(UserId('abc-123'));
// fetchUser('raw-string'); // Compile error
```

### Late Keyword (Correct Usage)

```dart
class ApiClient {
  // GOOD: late for dependency injection with guaranteed init
  late final HttpClient _client;

  void configure(HttpClient client) {
    _client = client;
  }

  // GOOD: late final for expensive one-time computation
  late final Map<String, dynamic> _config = _loadConfig();

  Map<String, dynamic> _loadConfig() {
    // expensive operation, runs once on first access
    return jsonDecode(File('config.json').readAsStringSync());
  }
}
```

### Stream Patterns

```dart
// async* generator for producing streams
Stream<int> countDown(int from) async* {
  for (var i = from; i >= 0; i--) {
    await Future.delayed(const Duration(seconds: 1));
    yield i;
  }
}

// Stream transformations
final results = inputStream
    .where((event) => event.isValid)
    .map((event) => event.transform())
    .handleError((error) => logger.warning('Stream error: $error'))
    .distinct();
```

### Isolates for Heavy Computation

```dart
import 'dart:isolate';

// Simple one-shot isolate computation
Future<List<int>> computePrimes(int limit) async {
  return await Isolate.run(() => _sieveOfEratosthenes(limit));
}

List<int> _sieveOfEratosthenes(int limit) {
  final sieve = List.filled(limit + 1, true);
  sieve[0] = sieve[1] = false;
  for (var i = 2; i * i <= limit; i++) {
    if (sieve[i]) {
      for (var j = i * i; j <= limit; j += i) {
        sieve[j] = false;
      }
    }
  }
  return [for (var i = 2; i <= limit; i++) if (sieve[i]) i];
}
```

## Testing

### Standards

- Test files: `*_test.dart` in `test/` (mirror `lib/src/` structure)
- Test functions: `test('description of behavior', () { ... })`
- Group related tests: `group('ClassName', () { ... })`
- Use `package:test` for pure Dart, `package:flutter_test` for widgets
- Use `package:mockito` with `@GenerateMocks` for type-safe mocking
- Coverage target: >80% for business logic, >60% overall
- Test names describe behavior: `'returns empty list when no users exist'`

### Unit Test Pattern

```dart
import 'package:test/test.dart';
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';

@GenerateMocks([UserRepository])
import 'user_service_test.mocks.dart';

void main() {
  late MockUserRepository mockRepo;
  late UserService service;

  setUp(() {
    mockRepo = MockUserRepository();
    service = UserService(mockRepo);
  });

  group('UserService', () {
    group('getUser', () {
      test('returns user when found', () async {
        final expected = User(id: '1', name: 'Alice');
        when(mockRepo.findById('1')).thenAnswer((_) async => expected);

        final result = await service.getUser('1');

        expect(result, isA<Success<User>>());
        expect((result as Success).value, equals(expected));
        verify(mockRepo.findById('1')).called(1);
      });

      test('returns failure when user not found', () async {
        when(mockRepo.findById('99')).thenAnswer((_) async => null);

        final result = await service.getUser('99');

        expect(result, isA<Failure>());
        expect((result as Failure).message, contains('not found'));
      });
    });
  });
}
```

### Async and Stream Testing

```dart
test('stream emits values in order', () {
  expect(
    countDown(3),
    emitsInOrder([3, 2, 1, 0, emitsDone]),
  );
});

test('completes within timeout', () async {
  final result = await fetchData().timeout(const Duration(seconds: 5));
  expect(result, isNotNull);
});
```

## Tooling

### Essential Commands

```bash
dart format .                        # Format all Dart files
dart analyze                         # Static analysis (lint + type checks)
dart test                            # Run all tests
dart test --coverage=coverage        # Run tests with coverage
dart run bin/main.dart               # Run CLI application
dart compile exe bin/main.dart       # AOT compile to native executable
dart pub get                         # Install dependencies
dart pub outdated                    # Check for dependency updates
dart pub deps                        # Show dependency tree
dart fix --apply                     # Auto-apply suggested fixes
```

### Analysis Options Configuration

```yaml
# analysis_options.yaml
include: package:lints/recommended.yaml

analyzer:
  language:
    strict-casts: true
    strict-inference: true
    strict-raw-types: true
  errors:
    missing_return: error
    dead_code: warning

linter:
  rules:
    - prefer_final_locals
    - prefer_const_constructors
    - prefer_const_declarations
    - avoid_dynamic_calls
    - unawaited_futures
    - always_declare_return_types
    - annotate_overrides
    - avoid_print
    - prefer_single_quotes
    - require_trailing_commas
    - unnecessary_lambdas
    - prefer_expression_function_bodies
```

### Pub Configuration

```yaml
# pubspec.yaml
name: my_package
description: A concise description of the package.
version: 1.0.0

environment:
  sdk: ^3.0.0

dependencies:
  http: ^1.2.0
  json_annotation: ^4.8.0

dev_dependencies:
  test: ^1.25.0
  mockito: ^5.4.0
  build_runner: ^2.4.0
  json_serializable: ^6.7.0
  lints: ^4.0.0
  coverage: ^1.7.0
```

## References

For detailed patterns and examples, see:

- [references/patterns.md](references/patterns.md) -- Stream patterns, Isolate communication, sealed class hierarchies

## External References

- [Effective Dart](https://dart.dev/effective-dart)
- [Dart Language Tour](https://dart.dev/language)
- [Dart 3 Records and Patterns](https://dart.dev/language/records)
- [Dart Null Safety](https://dart.dev/null-safety)
- [Dart Concurrency (Isolates)](https://dart.dev/language/concurrency)
- [dart_test package](https://pub.dev/packages/test)
- [mockito for Dart](https://pub.dev/packages/mockito)
- [Dart Lints](https://pub.dev/packages/lints)
