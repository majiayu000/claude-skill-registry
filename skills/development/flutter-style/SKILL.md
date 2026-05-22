---
name: innozverse-flutter-style
description: Follow Flutter and Dart development best practices including project structure, API service patterns, StatefulWidget usage, and environment configuration. Use when working on mobile app features or modifying Flutter code.
---

# innozverse Flutter Development Style

Follow these patterns when building mobile features in apps/mobile.

## Project Structure

```
lib/
├── main.dart           # App entry
├── services/           # API clients
│   └── api_service.dart
├── models/             # Data models
├── screens/            # Full screens
└── widgets/            # Reusable widgets
```

## API Service Pattern

```dart
// lib/services/api_service.dart
import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  final String baseUrl;

  ApiService({required this.baseUrl});

  Future<UserResponse> getUser(String id) async {
    final uri = Uri.parse('$baseUrl/users/$id');
    final response = await http.get(uri);

    if (response.statusCode == 200) {
      final json = jsonDecode(response.body);
      return UserResponse.fromJson(json);
    } else {
      throw Exception('Failed to get user: ${response.statusCode}');
    }
  }
}
```

## Model Pattern

```dart
// lib/models/user.dart
class User {
  final String id;
  final String name;
  final String email;

  User({
    required this.id,
    required this.name,
    required this.email,
  });

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'] as String,
      name: json['name'] as String,
      email: json['email'] as String,
    );
  }
}
```

## StatefulWidget Pattern

```dart
class UsersScreen extends StatefulWidget {
  const UsersScreen({super.key});

  @override
  State<UsersScreen> createState() => _UsersScreenState();
}

class _UsersScreenState extends State<UsersScreen> {
  final ApiService _apiService = ApiService(baseUrl: apiBaseUrl);
  List<User>? _users;
  bool _loading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _loadUsers();
  }

  Future<void> _loadUsers() async {
    try {
      final users = await _apiService.getUsers();
      setState(() {
        _users = users;
        _loading = false;
      });
    } catch (e) {
      setState(() {
        _error = e.toString();
        _loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_loading) return const CircularProgressIndicator();
    if (_error != null) return Text('Error: $_error');

    return ListView.builder(
      itemCount: _users?.length ?? 0,
      itemBuilder: (context, index) {
        return Text(_users![index].name);
      },
    );
  }
}
```

## Environment Configuration

```dart
const String apiBaseUrl = String.fromEnvironment(
  'API_BASE_URL',
  defaultValue: 'http://localhost:8080',
);
```

Run with:
```bash
flutter run --dart-define=API_BASE_URL=https://api.example.com
```

## Best Practices

- Use `const` constructors where possible
- Prefer `final` over `var`
- Handle errors with try/catch
- Show loading states
- Use Material Design 3
- Follow flutter_lints rules
