---
name: flutter-networking
description: Comprehensive Flutter networking guidance including HTTP CRUD operations, WebSocket connections, authentication, error handling, and performance optimization. Use when Claude needs to implement HTTP requests GET POST PUT DELETE, WebSocket real-time communication, authenticated requests with headers and tokens, background parsing with isolates, REST API integration with proper error handling, or any network-related functionality in Flutter applications.
metadata:
  author: Stanislav [MADTeacher] Chernyshev
  version: "1.0"
---

# Flutter Networking

## Quick Start

Add HTTP dependency to `pubspec.yaml`:

```yaml
dependencies:
  http: ^1.6.0
```

Basic GET request:

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

Future<Album> fetchAlbum() async {
  final response = await http.get(
    Uri.parse('https://api.example.com/albums/1'),
  );

  if (response.statusCode == 200) {
    return Album.fromJson(jsonDecode(response.body));
  } else {
    throw Exception('Failed to load album');
  }
}
```

Use in UI with `FutureBuilder`:

```dart
FutureBuilder<Album>(
  future: futureAlbum,
  builder: (context, snapshot) {
    if (snapshot.hasData) {
      return Text(snapshot.data!.title);
    } else if (snapshot.hasError) {
      return Text('${snapshot.error}');
    }
    return const CircularProgressIndicator();
  },
)
```

## HTTP Methods

### GET - Fetch Data

Use for retrieving data. See [http-basics.md](references/http-basics.md) for complete examples.

### POST - Create Data

Use for creating new resources. Requires `Content-Type: application/json` header.

```dart
final response = await http.post(
  Uri.parse('https://api.example.com/albums'),
  headers: <String, String>{
    'Content-Type': 'application/json; charset=UTF-8',
  },
  body: jsonEncode(<String, String>{'title': title}),
);
```

See [http-basics.md](references/http-basics.md) for POST examples.

### PUT - Update Data

Use for updating existing resources.

```dart
final response = await http.put(
  Uri.parse('https://api.example.com/albums/1'),
  headers: <String, String>{
    'Content-Type': 'application/json; charset=UTF-8',
  },
  body: jsonEncode(<String, String>{'title': title}),
);
```

### DELETE - Remove Data

Use for deleting resources.

```dart
final response = await http.delete(
  Uri.parse('https://api.example.com/albums/1'),
  headers: <String, String>{
    'Content-Type': 'application/json; charset=UTF-8',
  },
);
```

## WebSocket

Add WebSocket dependency:

```yaml
dependencies:
  web_socket_channel: ^3.0.3
```

Basic WebSocket connection:

```dart
import 'package:web_socket_channel/web_socket_channel.dart';

final _channel = WebSocketChannel.connect(
  Uri.parse('wss://echo.websocket.events'),
);

// Listen for messages
StreamBuilder(
  stream: _channel.stream,
  builder: (context, snapshot) {
    return Text(snapshot.hasData ? '${snapshot.data}' : '');
  },
)

// Send message
_channel.sink.add('Hello');

// Close connection
_channel.sink.close();
```

See [websockets.md](references/websockets.md) for complete WebSocket implementation.

## Authentication

Add authorization headers to requests:

```dart
import 'dart:io';

final response = await http.get(
  Uri.parse('https://api.example.com/data'),
  headers: {HttpHeaders.authorizationHeader: 'Bearer $token'},
);
```

Common authentication patterns:
- **Bearer Token**: `Authorization: Bearer <token>`
- **Basic Auth**: `Authorization: Basic <base64_credentials>`
- **API Key**: `X-API-Key: <key>`

See [authentication.md](references/authentication.md) for detailed authentication strategies.

## Error Handling

Handle HTTP errors appropriately:

```dart
if (response.statusCode >= 200 && response.statusCode < 300) {
  return Data.fromJson(jsonDecode(response.body));
} else if (response.statusCode == 401) {
  throw UnauthorizedException();
} else if (response.statusCode == 404) {
  throw NotFoundException();
} else {
  throw ServerException();
}
```

See [error-handling.md](references/error-handling.md) for comprehensive error handling strategies.

## Performance

### Background Parsing with Isolates

For large JSON responses, use `compute()` to parse in background isolate:

```dart
import 'package:flutter/foundation.dart';

Future<List<Photo>> fetchPhotos(http.Client client) async {
  final response = await client.get(
    Uri.parse('https://api.example.com/photos'),
  );

  return compute(parsePhotos, response.body);
}

List<Photo> parsePhotos(String responseBody) {
  final parsed = (jsonDecode(responseBody) as List)
      .cast<Map<String, dynamic>>();
  return parsed.map<Photo>((json) => Photo.fromJson(json)).toList();
}
```

See [performance.md](references/performance.md) for optimization techniques.

## Integration with Architecture

When using MVVM architecture (see [flutter-architecture](../flutter-architecture/)):

1. **Service Layer**: Create HTTP service for API endpoints
2. **Repository Layer**: Aggregate data from services, handle caching
3. **ViewModel Layer**: Transform repository data for UI

Example service:

```dart
class AlbumService {
  final http.Client _client;

  AlbumService(this._client);

  Future<Album> fetchAlbum(int id) async {
    final response = await _client.get(
      Uri.parse('https://api.example.com/albums/$id'),
    );

    if (response.statusCode == 200) {
      return Album.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Failed to load album');
    }
  }
}
```

## Common Patterns

### Repository Pattern

Single source of truth for data type:

```dart
class AlbumRepository {
  final AlbumService _service;
  final LocalStorage _cache;

  Future<Album> getAlbum(int id) async {
    try {
      return await _cache.getAlbum(id) ?? 
             await _service.fetchAlbum(id);
    } catch (e) {
      throw AlbumFetchException();
    }
  }
}
```

### Retry Logic

Implement exponential backoff for failed requests:

```dart
Future<T> fetchWithRetry<T>(
  Future<T> Function() fetch, {
  int maxRetries = 3,
}) async {
  for (int i = 0; i < maxRetries; i++) {
    try {
      return await fetch();
    } catch (e) {
      if (i == maxRetries - 1) rethrow;
      await Future.delayed(Duration(seconds: 2 << i));
    }
  }
  throw StateError('Unreachable');
}
```

## Best Practices

### DO

- Use type-safe model classes with `fromJson` factories
- Handle all HTTP status codes appropriately
- Parse JSON in background isolates for large responses
- Implement retry logic for transient failures
- Cache responses when appropriate
- Use proper timeouts
- Secure tokens and credentials

### DON'T

- Parse JSON on main thread for large responses
- Ignore error states in UI
- Store tokens in source code or public repositories
- Make requests without timeout configuration
- Block UI thread with network operations
- Throw generic exceptions without context

## Resources

### references/
- [http-basics.md](references/http-basics.md) - Complete HTTP CRUD operations examples
- [websockets.md](references/websockets.md) - WebSocket implementation patterns
- [authentication.md](references/authentication.md) - Authentication strategies and token management
- [error-handling.md](references/error-handling.md) - Comprehensive error handling patterns
- [performance.md](references/performance.md) - Optimization techniques and best practices

### assets/examples/
- `fetch_example.dart` - Complete GET request with FutureBuilder
- `post_example.dart` - POST request implementation
- `websocket_example.dart` - WebSocket client with stream handling
- `auth_example.dart` - Authenticated request example
- `background_parsing.dart` - compute() for JSON parsing

### assets/code-templates/
- `http_service.dart` - Reusable HTTP service template
- `repository_template.dart` - Repository pattern template
