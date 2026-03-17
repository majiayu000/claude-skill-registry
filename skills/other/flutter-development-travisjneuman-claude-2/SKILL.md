---
name: flutter-development
description: Cross-platform development with Flutter and Dart for iOS, Android, Web, Desktop, and embedded. Use when building Flutter apps, implementing Material/Cupertino design, or optimizing Dart code.
---

# Flutter Development

Build beautiful, natively compiled applications for mobile, web, desktop, and embedded from a single codebase.

## Supported Platforms

| Platform | Status | Notes                   |
| -------- | ------ | ----------------------- |
| iOS      | Stable | Full native performance |
| Android  | Stable | Full native performance |
| Web      | Stable | PWA support             |
| macOS    | Stable | Native desktop          |
| Windows  | Stable | Native desktop          |
| Linux    | Stable | Native desktop          |

---

## Project Structure

```
my_app/
├── lib/
│   ├── main.dart
│   ├── app.dart
│   ├── features/
│   │   ├── home/
│   │   │   ├── home_screen.dart
│   │   │   ├── home_controller.dart
│   │   │   └── widgets/
│   │   └── settings/
│   ├── core/
│   │   ├── theme/
│   │   ├── utils/
│   │   └── constants/
│   └── shared/
│       ├── models/
│       ├── services/
│       └── widgets/
├── test/
├── pubspec.yaml
└── analysis_options.yaml
```

---

## Basic Structure

### Main Entry

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'My App',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
        useMaterial3: true,
      ),
      home: const HomeScreen(),
    );
  }
}
```

### Stateless Widget

```dart
class GreetingCard extends StatelessWidget {
  const GreetingCard({
    super.key,
    required this.name,
  });

  final String name;

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Text(
          'Hello, $name!',
          style: Theme.of(context).textTheme.headlineMedium,
        ),
      ),
    );
  }
}
```

### Stateful Widget

```dart
class Counter extends StatefulWidget {
  const Counter({super.key});

  @override
  State<Counter> createState() => _CounterState();
}

class _CounterState extends State<Counter> {
  int _count = 0;

  void _increment() {
    setState(() {
      _count++;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Text(
          'Count: $_count',
          style: Theme.of(context).textTheme.headlineLarge,
        ),
        const SizedBox(height: 16),
        ElevatedButton(
          onPressed: _increment,
          child: const Text('Increment'),
        ),
      ],
    );
  }
}
```

---

## State Management

### Riverpod (Recommended)

```dart
// Provider definition
final counterProvider = StateNotifierProvider<CounterNotifier, int>((ref) {
  return CounterNotifier();
});

class CounterNotifier extends StateNotifier<int> {
  CounterNotifier() : super(0);

  void increment() => state++;
  void decrement() => state--;
}

// Usage in widget
class CounterScreen extends ConsumerWidget {
  const CounterScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final count = ref.watch(counterProvider);

    return Scaffold(
      body: Center(
        child: Text('Count: $count'),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => ref.read(counterProvider.notifier).increment(),
        child: const Icon(Icons.add),
      ),
    );
  }
}

// Async provider
final itemsProvider = FutureProvider<List<Item>>((ref) async {
  final repository = ref.watch(repositoryProvider);
  return repository.fetchItems();
});
```

### BLoC Pattern

```dart
// Events
abstract class CounterEvent {}
class IncrementPressed extends CounterEvent {}
class DecrementPressed extends CounterEvent {}

// State
class CounterState {
  final int count;
  const CounterState(this.count);
}

// BLoC
class CounterBloc extends Bloc<CounterEvent, CounterState> {
  CounterBloc() : super(const CounterState(0)) {
    on<IncrementPressed>((event, emit) {
      emit(CounterState(state.count + 1));
    });
    on<DecrementPressed>((event, emit) {
      emit(CounterState(state.count - 1));
    });
  }
}

// Usage
BlocBuilder<CounterBloc, CounterState>(
  builder: (context, state) {
    return Text('Count: ${state.count}');
  },
)
```

---

## Navigation

### GoRouter (Recommended)

```dart
final router = GoRouter(
  initialLocation: '/',
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => const HomeScreen(),
      routes: [
        GoRoute(
          path: 'details/:id',
          builder: (context, state) {
            final id = state.pathParameters['id']!;
            return DetailsScreen(id: id);
          },
        ),
      ],
    ),
    GoRoute(
      path: '/settings',
      builder: (context, state) => const SettingsScreen(),
    ),
  ],
);

// Usage
MaterialApp.router(
  routerConfig: router,
)

// Navigate
context.go('/details/123');
context.push('/settings');
context.pop();
```

---

## Common Widgets

### Lists

```dart
ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, index) {
    final item = items[index];
    return ListTile(
      leading: CircleAvatar(
        backgroundImage: NetworkImage(item.imageUrl),
      ),
      title: Text(item.title),
      subtitle: Text(item.subtitle),
      trailing: const Icon(Icons.chevron_right),
      onTap: () => context.push('/details/${item.id}'),
    );
  },
)
```

### Forms

```dart
class LoginForm extends StatefulWidget {
  const LoginForm({super.key});

  @override
  State<LoginForm> createState() => _LoginFormState();
}

class _LoginFormState extends State<LoginForm> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  void _submit() {
    if (_formKey.currentState!.validate()) {
      // Process login
    }
  }

  @override
  Widget build(BuildContext context) {
    return Form(
      key: _formKey,
      child: Column(
        children: [
          TextFormField(
            controller: _emailController,
            decoration: const InputDecoration(
              labelText: 'Email',
              prefixIcon: Icon(Icons.email),
            ),
            keyboardType: TextInputType.emailAddress,
            validator: (value) {
              if (value == null || !value.contains('@')) {
                return 'Enter a valid email';
              }
              return null;
            },
          ),
          const SizedBox(height: 16),
          TextFormField(
            controller: _passwordController,
            decoration: const InputDecoration(
              labelText: 'Password',
              prefixIcon: Icon(Icons.lock),
            ),
            obscureText: true,
            validator: (value) {
              if (value == null || value.length < 6) {
                return 'Password must be at least 6 characters';
              }
              return null;
            },
          ),
          const SizedBox(height: 24),
          ElevatedButton(
            onPressed: _submit,
            child: const Text('Login'),
          ),
        ],
      ),
    );
  }
}
```

---

## Networking

### Dio HTTP Client

```dart
class ApiService {
  final Dio _dio;

  ApiService() : _dio = Dio(BaseOptions(
    baseUrl: 'https://api.example.com',
    connectTimeout: const Duration(seconds: 10),
    receiveTimeout: const Duration(seconds: 10),
  )) {
    _dio.interceptors.add(LogInterceptor());
  }

  Future<List<Item>> getItems() async {
    try {
      final response = await _dio.get('/items');
      return (response.data as List)
          .map((json) => Item.fromJson(json))
          .toList();
    } on DioException catch (e) {
      throw ApiException(e.message ?? 'Unknown error');
    }
  }
}
```

---

## Local Storage

### Hive (Recommended)

```dart
// Model
@HiveType(typeId: 0)
class Item extends HiveObject {
  @HiveField(0)
  late String id;

  @HiveField(1)
  late String name;
}

// Setup
await Hive.initFlutter();
Hive.registerAdapter(ItemAdapter());
await Hive.openBox<Item>('items');

// Usage
final box = Hive.box<Item>('items');
await box.put('key', item);
final item = box.get('key');
```

### SharedPreferences

```dart
final prefs = await SharedPreferences.getInstance();
await prefs.setString('token', 'abc123');
final token = prefs.getString('token');
```

---

## Platform-Specific Code

```dart
import 'dart:io' show Platform;
import 'package:flutter/foundation.dart' show kIsWeb;

Widget build(BuildContext context) {
  if (kIsWeb) {
    return WebLayout();
  } else if (Platform.isIOS) {
    return CupertinoLayout();
  } else if (Platform.isAndroid) {
    return MaterialLayout();
  } else if (Platform.isMacOS || Platform.isWindows || Platform.isLinux) {
    return DesktopLayout();
  }
  return DefaultLayout();
}
```

---

## Testing

### Widget Tests

```dart
testWidgets('Counter increments', (tester) async {
  await tester.pumpWidget(const MaterialApp(home: Counter()));

  expect(find.text('Count: 0'), findsOneWidget);

  await tester.tap(find.byIcon(Icons.add));
  await tester.pump();

  expect(find.text('Count: 1'), findsOneWidget);
});
```

### Unit Tests

```dart
test('Item fromJson parses correctly', () {
  final json = {'id': '1', 'name': 'Test'};
  final item = Item.fromJson(json);

  expect(item.id, '1');
  expect(item.name, 'Test');
});
```

---

## Performance

### Best Practices

```dart
// Use const constructors
const SizedBox(height: 16)

// Avoid rebuilds with const
const MyStaticWidget()

// Use ListView.builder for long lists
ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, index) => ItemWidget(items[index]),
)

// Cache images
CachedNetworkImage(
  imageUrl: url,
  placeholder: (context, url) => const CircularProgressIndicator(),
)
```

---

## Best Practices

### DO:

- Use const constructors everywhere possible
- Split widgets into smaller components
- Use Riverpod or BLoC for state
- Follow Flutter naming conventions
- Write widget tests

### DON'T:

- Put logic in build methods
- Create god widgets
- Use setState for complex state
- Ignore null safety
- Skip code generation setup

---

## Dart 3 Features

### Sealed Classes and Pattern Matching

```dart
// Sealed classes for exhaustive pattern matching
sealed class Result<T> {}
class Success<T> extends Result<T> { final T value; Success(this.value); }
class Failure<T> extends Result<T> { final String error; Failure(this.error); }

// Exhaustive switch
String display(Result<User> result) => switch (result) {
  Success(value: final user) => 'Hello, ${user.name}',
  Failure(error: final msg) => 'Error: $msg',
};
```

### Records

```dart
// Lightweight data tuples
(String, int) getUserInfo() => ('John', 30);

// Named fields
({String name, int age}) getUserDetails() => (name: 'John', age: 30);

// Destructuring
final (name, age) = getUserInfo();
final (:name, :age) = getUserDetails();
```

### Extension Types

```dart
// Zero-cost type wrappers (compile-time only)
extension type UserId(String value) {
  bool get isValid => value.isNotEmpty;
}

extension type Email(String value) {
  factory Email.validated(String raw) {
    if (!raw.contains('@')) throw FormatException('Invalid email');
    return Email(raw);
  }
}

// Usage - type-safe, zero runtime cost
void sendEmail(Email to, UserId from) { ... }
sendEmail(Email.validated('a@b.com'), UserId('user123'));
```

### If-Case and Switch Expressions

```dart
// If-case for pattern matching
if (json case {'name': String name, 'age': int age}) {
  print('$name is $age years old');
}

// Switch expressions (concise)
final icon = switch (status) {
  'active' => Icons.check_circle,
  'pending' => Icons.hourglass_empty,
  'error' => Icons.error,
  _ => Icons.help,
};
```

---

## Riverpod 3.0 Patterns

```dart
// Modern Riverpod with code generation
@riverpod
class Counter extends _$Counter {
  @override
  int build() => 0;

  void increment() => state++;
  void decrement() => state--;
}

// Async provider with Riverpod 3.0
@riverpod
Future<List<Item>> items(Ref ref) async {
  final repository = ref.watch(repositoryProvider);
  return repository.fetchItems();
}

// Family provider (parameterized)
@riverpod
Future<User> user(Ref ref, String userId) async {
  return ref.watch(apiClientProvider).getUser(userId);
}

// Usage in widget
class ItemScreen extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final items = ref.watch(itemsProvider);

    return items.when(
      data: (data) => ListView.builder(
        itemCount: data.length,
        itemBuilder: (context, i) => ItemTile(data[i]),
      ),
      loading: () => const CircularProgressIndicator(),
      error: (err, stack) => Text('Error: $err'),
    );
  }
}
```

---

## Material 3 / Material You

```dart
MaterialApp(
  theme: ThemeData(
    colorScheme: ColorScheme.fromSeed(
      seedColor: Colors.deepPurple,
      brightness: Brightness.light,
    ),
    useMaterial3: true,
  ),
  darkTheme: ThemeData(
    colorScheme: ColorScheme.fromSeed(
      seedColor: Colors.deepPurple,
      brightness: Brightness.dark,
    ),
    useMaterial3: true,
  ),
  themeMode: ThemeMode.system,
);

// Dynamic color (Android 12+)
import 'package:dynamic_color/dynamic_color.dart';

DynamicColorBuilder(
  builder: (lightDynamic, darkDynamic) {
    return MaterialApp(
      theme: ThemeData(
        colorScheme: lightDynamic ?? defaultLightScheme,
        useMaterial3: true,
      ),
    );
  },
);
```

---

## Build and Deployment

### Fastlane

```ruby
# fastlane/Fastfile
platform :ios do
  lane :beta do
    build_flutter_app
    upload_to_testflight
  end
end

platform :android do
  lane :beta do
    build_flutter_app
    upload_to_play_store(track: 'internal')
  end
end
```

### Codemagic CI/CD

```yaml
# codemagic.yaml
workflows:
  flutter-release:
    name: Flutter Release
    environment:
      flutter: stable
    scripts:
      - name: Build
        script: flutter build appbundle --release
    artifacts:
      - build/**/outputs/**/*.aab
    publishing:
      google_play:
        credentials: $GCLOUD_SERVICE_ACCOUNT
        track: internal
```

### EAS Build (for Expo/RN comparison reference)

Flutter apps typically use Fastlane, Codemagic, or GitHub Actions for CI/CD rather than EAS.
