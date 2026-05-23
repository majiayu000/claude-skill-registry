---
name: "HTTP Integration Patterns"
description: "HTTP client configuration, API providers, error handling, and request/response patterns"
version: "1.0.0"
---

# HTTP Integration Patterns

## HTTP Provider Pattern

```dart
import 'dart:convert';
import 'package:http/http.dart' as http;

class UserProvider {
  final http.Client _client;
  final String _baseUrl;
  
  UserProvider(this._client, {String? baseUrl})
      : _baseUrl = baseUrl ?? 'https://api.example.com';
  
  Map<String, String> get _headers => {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  };
  
  Future<UserModel> fetchUser(String id) async {
    final response = await _client.get(
      Uri.parse('$_baseUrl/users/$id'),
      headers: _headers,
    ).timeout(Duration(seconds: 10));
    
    if (response.statusCode == 200) {
      return UserModel.fromJson(json.decode(response.body));
    } else if (response.statusCode == 404) {
      throw ServerException(message: 'User not found');
    } else {
      throw ServerException(
        message: 'Failed to fetch user',
        statusCode: response.statusCode,
      );
    }
  }
  
  Future<List<UserModel>> fetchAllUsers() async {
    final response = await _client.get(
      Uri.parse('$_baseUrl/users'),
      headers: _headers,
    ).timeout(Duration(seconds: 10));
    
    if (response.statusCode == 200) {
      final List<dynamic> data = json.decode(response.body);
      return data.map((json) => UserModel.fromJson(json)).toList();
    } else {
      throw ServerException(message: 'Failed to fetch users');
    }
  }
  
  Future<UserModel> createUser(Map<String, dynamic> data) async {
    final response = await _client.post(
      Uri.parse('$_baseUrl/users'),
      headers: _headers,
      body: json.encode(data),
    ).timeout(Duration(seconds: 10));
    
    if (response.statusCode == 201) {
      return UserModel.fromJson(json.decode(response.body));
    } else {
      throw ServerException(message: 'Failed to create user');
    }
  }
  
  Future<void> deleteUser(String id) async {
    final response = await _client.delete(
      Uri.parse('$_baseUrl/users/$id'),
      headers: _headers,
    ).timeout(Duration(seconds: 10));
    
    if (response.statusCode != 204) {
      throw ServerException(message: 'Failed to delete user');
    }
  }
}
```

## Authenticated HTTP Client

```dart
class AuthenticatedClient extends http.BaseClient {
  final http.Client _inner;
  final String Function() _getToken;
  
  AuthenticatedClient(this._inner, this._getToken);
  
  @override
  Future<http.StreamedResponse> send(http.BaseRequest request) async {
    final token = _getToken();
    if (token.isNotEmpty) {
      request.headers['Authorization'] = 'Bearer $token';
    }
    request.headers['Content-Type'] = 'application/json';
    request.headers['Accept'] = 'application/json';
    
    return _inner.send(request);
  }
}

// Usage in bindings
Get.lazyPut<http.Client>(
  () => AuthenticatedClient(
    http.Client(),
    () => Get.find<StorageService>().token ?? '',
  ),
);
```

## Error Handling

```dart
try {
  final response = await _client.get(url);
  return parseResponse(response);
} on SocketException {
  throw NetworkException();
} on TimeoutException {
  throw ServerException(message: 'Request timeout');
} on FormatException {
  throw ServerException(message: 'Invalid response format');
} catch (e) {
  throw ServerException(message: e.toString());
}
```
