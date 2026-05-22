---
name: dart-expert
version: 1.0.0
description: Expert-level Dart, Flutter, mobile development, and cross-platform apps
category: languages
tags: [dart, flutter, mobile, cross-platform, widgets]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(dart:*, flutter:*)
---

# Dart & Flutter Expert

Expert guidance for Dart programming, Flutter framework, mobile development, and cross-platform applications.

## Core Concepts

### Dart Language
- Strong typing with type inference
- Async/await and Futures
- Streams
- Mixins and extensions
- Null safety
- Collections

### Flutter Framework
- Widgets (Stateless & Stateful)
- State management (Provider, Riverpod, Bloc)
- Navigation and routing
- Material and Cupertino design
- Responsive layouts
- Platform integration

## Dart Fundamentals

```dart
// Variables and types
var name = 'John';  // Type inference
String explicitType = 'Explicit';
final constantValue = 42;  // Runtime constant
const compileConstant = 'Compile-time';

// Null safety
String? nullableString;
String nonNullable = 'Never null';

// Late initialization
late String lateInit;

// Collections
List<String> names = ['Alice', 'Bob', 'Charlie'];
Map<String, int> ages = {'Alice': 25, 'Bob': 30};
Set<int> uniqueNumbers = {1, 2, 3, 3};  // {1, 2, 3}

// Functions
int add(int a, int b) => a + b;

// Named parameters
void createUser({
  required String name,
  int age = 18,
  String? email,
}) {
  print('Creating user: $name, age: $age');
}

// Classes
class User {
  final String id;
  final String name;
  int age;

  User({
    required this.id,
    required this.name,
    this.age = 0,
  });

  // Named constructor
  User.guest() : this(id: 'guest', name: 'Guest');

  // Methods
  void celebrateBirthday() {
    age++;
  }

  @override
  String toString() => 'User($name, $age)';
}

// Mixins
mixin Loggable {
  void log(String message) {
    print('[${DateTime.now()}] $message');
  }
}

class LoggableUser extends User with Loggable {
  LoggableUser({required String id, required String name})
      : super(id: id, name: name);
}

// Extensions
extension StringExtensions on String {
  bool get isValidEmail => contains('@') && contains('.');
  String capitalize() => '${this[0].toUpperCase()}${substring(1)}';
}
```

## Async Programming

```dart
import 'dart:async';

// Future
Future<String> fetchUser(String id) async {
  await Future.delayed(Duration(seconds: 1));
  return 'User $id';
}

// Error handling
Future<User?> fetchUserSafely(String id) async {
  try {
    final user = await fetchUser(id);
    return User(id: id, name: user);
  } catch (e) {
    print('Error: $e');
    return null;
  }
}

// Multiple futures
Future<void> fetchMultiple() async {
  final results = await Future.wait([
    fetchUser('1'),
    fetchUser('2'),
    fetchUser('3'),
  ]);
  print(results);
}

// Streams
Stream<int> countStream() async* {
  for (int i = 1; i <= 5; i++) {
    await Future.delayed(Duration(seconds: 1));
    yield i;
  }
}

// Listen to stream
void listenToStream() {
  countStream().listen(
    (data) => print('Received: $data'),
    onError: (error) => print('Error: $error'),
    onDone: () => print('Done'),
  );
}

// Stream transformations
Stream<String> transformedStream() {
  return countStream()
      .where((n) => n % 2 == 0)
      .map((n) => 'Number: $n')
      .take(3);
}

// StreamController
class Counter {
  final _controller = StreamController<int>();

  Stream<int> get stream => _controller.stream;

  void increment(int value) {
    _controller.add(value);
  }

  void dispose() {
    _controller.close();
  }
}
```

## Flutter Widgets

```dart
import 'package:flutter/material.dart';

// Stateless Widget
class UserCard extends StatelessWidget {
  final User user;

  const UserCard({Key? key, required this.user}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        title: Text(user.name),
        subtitle: Text('Age: ${user.age}'),
        trailing: Icon(Icons.arrow_forward),
      ),
    );
  }
}

// Stateful Widget
class CounterWidget extends StatefulWidget {
  const CounterWidget({Key? key}) : super(key: key);

  @override
  State<CounterWidget> createState() => _CounterWidgetState();
}

class _CounterWidgetState extends State<CounterWidget> {
  int _counter = 0;

  void _incrementCounter() {
    setState(() {
      _counter++;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text('Counter: $_counter'),
        ElevatedButton(
          onPressed: _incrementCounter,
          child: Text('Increment'),
        ),
      ],
    );
  }
}

// Layout
class UserListScreen extends StatelessWidget {
  final List<User> users;

  const UserListScreen({Key? key, required this.users}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Users'),
        actions: [
          IconButton(
            icon: Icon(Icons.add),
            onPressed: () => Navigator.push(
              context,
              MaterialPageRoute(builder: (_) => AddUserScreen()),
            ),
          ),
        ],
      ),
      body: ListView.builder(
        itemCount: users.length,
        itemBuilder: (context, index) {
          return UserCard(user: users[index]);
        },
      ),
    );
  }
}
```

## State Management (Provider)

```dart
import 'package:provider/provider.dart';

// State class
class UserProvider extends ChangeNotifier {
  List<User> _users = [];

  List<User> get users => _users;

  Future<void> fetchUsers() async {
    _users = await api.getUsers();
    notifyListeners();
  }

  void addUser(User user) {
    _users.add(user);
    notifyListeners();
  }

  void removeUser(String id) {
    _users.removeWhere((user) => user.id == id);
    notifyListeners();
  }
}

// Setup provider
void main() {
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => UserProvider()),
        ChangeNotifierProvider(create: (_) => AuthProvider()),
      ],
      child: MyApp(),
    ),
  );
}

// Consume provider
class UserList extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final userProvider = Provider.of<UserProvider>(context);

    return ListView.builder(
      itemCount: userProvider.users.length,
      itemBuilder: (context, index) {
        final user = userProvider.users[index];
        return ListTile(
          title: Text(user.name),
          trailing: IconButton(
            icon: Icon(Icons.delete),
            onPressed: () => userProvider.removeUser(user.id),
          ),
        );
      },
    );
  }
}

// Consumer widget
class UserCounter extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Consumer<UserProvider>(
      builder: (context, userProvider, child) {
        return Text('Total users: ${userProvider.users.length}');
      },
    );
  }
}
```

## Navigation

```dart
// Basic navigation
Navigator.push(
  context,
  MaterialPageRoute(builder: (context) => DetailScreen()),
);

// Named routes
MaterialApp(
  routes: {
    '/': (context) => HomeScreen(),
    '/details': (context) => DetailScreen(),
    '/settings': (context) => SettingsScreen(),
  },
);

Navigator.pushNamed(context, '/details');

// Pass arguments
Navigator.pushNamed(
  context,
  '/details',
  arguments: {'userId': '123'},
);

// Get arguments
final args = ModalRoute.of(context)!.settings.arguments as Map;

// Return data
final result = await Navigator.push(
  context,
  MaterialPageRoute(builder: (_) => SelectionScreen()),
);

// Pop with result
Navigator.pop(context, selectedValue);
```

## HTTP and API

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

class ApiService {
  final String baseUrl = 'https://api.example.com';

  Future<List<User>> fetchUsers() async {
    final response = await http.get(Uri.parse('$baseUrl/users'));

    if (response.statusCode == 200) {
      final List<dynamic> data = json.decode(response.body);
      return data.map((json) => User.fromJson(json)).toList();
    } else {
      throw Exception('Failed to load users');
    }
  }

  Future<User> createUser(User user) async {
    final response = await http.post(
      Uri.parse('$baseUrl/users'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode(user.toJson()),
    );

    if (response.statusCode == 201) {
      return User.fromJson(json.decode(response.body));
    } else {
      throw Exception('Failed to create user');
    }
  }
}

// Model with JSON serialization
class User {
  final String id;
  final String name;
  final String email;

  User({required this.id, required this.name, required this.email});

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'],
      name: json['name'],
      email: json['email'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'email': email,
    };
  }
}
```

## Best Practices

### Dart
- Use const constructors when possible
- Leverage null safety
- Use final for immutable values
- Prefer async/await over .then()
- Use extensions for utility methods
- Follow Effective Dart guidelines

### Flutter
- Keep widgets small and focused
- Use const widgets for optimization
- Avoid rebuilding entire trees
- Implement proper state management
- Handle errors gracefully
- Test widgets thoroughly
- Use keys when needed

### Performance
- Use ListView.builder for long lists
- Implement pagination
- Cache network images
- Minimize widget rebuilds
- Use const constructors
- Profile app performance
- Lazy load resources

## Anti-Patterns

❌ Large widget trees
❌ State in StatelessWidget
❌ Not disposing controllers
❌ Ignoring null safety
❌ Synchronous I/O in UI
❌ No error handling
❌ Hard-coded strings

## Resources

- Dart: https://dart.dev/
- Flutter: https://flutter.dev/
- Pub.dev: https://pub.dev/
- Flutter Widget Catalog: https://flutter.dev/docs/development/ui/widgets
- Effective Dart: https://dart.dev/guides/language/effective-dart
