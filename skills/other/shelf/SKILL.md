---
name: shelf
description: |
  Shelf framework guardrails, patterns, and best practices for AI-assisted development.
  Use when working with Shelf (Dart HTTP server) projects, or when the user mentions Shelf.
  Provides middleware patterns, request handling, pipeline composition, and server guidelines.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: framework
  language: dart
  extensions: ".dart"
---

# Shelf Framework Guide

> Applies to: Shelf 1.x, Dart 3.x, REST APIs, Microservices, Backend Services
> Complements: `.claude/skills/dart-guide/SKILL.md`

## Core Principles

1. **Middleware Composition**: Everything flows through `Pipeline`; compose handlers with `addMiddleware` and `addHandler`
2. **Handler Simplicity**: A `Handler` is just `FutureOr<Response> Function(Request)` -- keep it functional
3. **Immutable Requests**: Use `request.change()` to pass data downstream via `context`
4. **Cascade Routing**: Use `Cascade` to try multiple handlers in sequence until one succeeds
5. **Separation of Concerns**: Handlers call services, services call repositories -- no business logic in middleware

## Project Structure

```
myapp/
├── bin/
│   └── server.dart               # Entry point (thin: config, serve, shutdown)
├── lib/
│   ├── src/
│   │   ├── app.dart              # Pipeline + Router assembly
│   │   ├── config/
│   │   │   └── config.dart       # Environment-based configuration
│   │   ├── handlers/
│   │   │   ├── health_handler.dart
│   │   │   └── users_handler.dart
│   │   ├── middleware/
│   │   │   ├── auth_middleware.dart
│   │   │   ├── cors_middleware.dart
│   │   │   └── logging_middleware.dart
│   │   ├── models/
│   │   │   └── user.dart
│   │   ├── repositories/
│   │   │   └── user_repository.dart
│   │   └── services/
│   │       └── user_service.dart
│   └── myapp.dart                # Library barrel export
├── test/
│   ├── handlers/
│   │   └── users_handler_test.dart
│   └── middleware/
│       └── auth_middleware_test.dart
├── pubspec.yaml
├── analysis_options.yaml
└── Dockerfile
```

**Architectural rules:**
- `bin/server.dart` is thin: load config, create handler, call `shelf_io.serve`, wire shutdown
- `lib/src/app.dart` owns the Pipeline and Router composition
- Handlers are organized by resource; each handler class exposes a `Router get router`
- Middleware functions return `Middleware` (a typedef for `Handler Function(Handler)`)
- Models use `freezed` for immutability and `json_serializable` for serialization
- Services contain business logic; repositories handle data access

## Dependencies (pubspec.yaml)

```yaml
dependencies:
  shelf: ^1.4.0
  shelf_router: ^1.1.0
  shelf_static: ^1.1.0        # Static file serving
  shelf_web_socket: ^1.0.0    # WebSocket support

  # Data
  freezed_annotation: ^2.4.0
  json_annotation: ^4.8.0

  # Auth
  dart_jsonwebtoken: ^2.12.0
  bcrypt: ^1.1.0

dev_dependencies:
  test: ^1.24.0
  mocktail: ^1.0.0
  build_runner: ^2.4.0
  freezed: ^2.4.0
  json_serializable: ^6.7.0
```

## Application Entry Point

```dart
// bin/server.dart
import 'dart:io';
import 'package:shelf/shelf_io.dart' as shelf_io;
import 'package:myapp/myapp.dart';

Future<void> main() async {
  final config = Config.fromEnvironment();
  final app = Application(config);
  final handler = await app.createHandler();

  final server = await shelf_io.serve(
    handler,
    InternetAddress.anyIPv4,
    config.port,
  );

  print('Server running on http://${server.address.host}:${server.port}');

  // Graceful shutdown
  ProcessSignal.sigint.watch().listen((_) async {
    print('Shutting down...');
    await app.close();
    await server.close();
    exit(0);
  });
}
```

### Entry Point Rules

- Load configuration from environment variables (never hardcode secrets)
- Wire graceful shutdown via `ProcessSignal.sigint`
- Call `app.close()` before `server.close()` to release database connections
- Keep `main()` under 25 lines

## Configuration

- Use a `Config` class with `factory Config.fromEnvironment()` reading from `Platform.environment`
- Provide dev defaults for non-secret values (port, database URL)
- Throw `StateError` in production if critical secrets are missing (JWT_SECRET, API keys)
- Use `const` constructor for Config to enable compile-time checks
- Never log secret values

## Application Setup (Pipeline + Router)

```dart
// lib/src/app.dart
import 'package:shelf/shelf.dart';
import 'package:shelf_router/shelf_router.dart';

class Application {
  final Config config;
  late final UserRepository _userRepository;
  late final UserService _userService;

  Application(this.config);

  Future<Handler> createHandler() async {
    _userRepository = UserRepository();
    _userService = UserService(_userRepository, config);

    final healthHandler = HealthHandler();
    final usersHandler = UsersHandler(_userService);

    final router = Router()
      ..mount('/health', healthHandler.router.call)
      ..mount('/api/v1/users', usersHandler.router.call);

    final pipeline = const Pipeline()
        .addMiddleware(loggingMiddleware())
        .addMiddleware(corsMiddleware())
        .addMiddleware(handleErrors())
        .addHandler(router.call);

    return pipeline;
  }

  Future<void> close() async {
    await _userRepository.close();
  }
}
```

### Pipeline Rules

- Middleware order: logging -> CORS -> error handling -> router
- Logging outermost so it captures all requests including CORS preflight
- Error handling wraps the router so thrown exceptions are caught
- Always call `.call` when mounting a `Router` or passing to `addHandler`
- Use `const Pipeline()` for the initial empty pipeline

## Handlers

Handlers are classes that expose a `Router get router` property. Each route method receives a `Request` and returns a `Response`.

```dart
// lib/src/handlers/users_handler.dart
class UsersHandler {
  final UserService _userService;

  UsersHandler(this._userService);

  Router get router {
    final router = Router();

    // Public routes
    router.post('/register', _register);
    router.post('/login', _login);

    // Protected routes
    router.get('/', _withAuth(_getAll));
    router.get('/<id>', _withAuth(_getById));
    router.put('/<id>', _withAuth(_update));
    router.delete('/<id>', _withAuth(_delete));

    return router;
  }

  Handler _withAuth(Handler handler) {
    return const Pipeline()
        .addMiddleware(authMiddleware())
        .addHandler(handler);
  }

  Future<Response> _register(Request request) async {
    final body = await request.readAsString();
    final json = jsonDecode(body) as Map<String, dynamic>;

    final user = await _userService.register(
      email: json['email'] as String,
      password: json['password'] as String,
      name: json['name'] as String,
    );

    return Response(
      201,
      body: jsonEncode(user.toJson()),
      headers: {'Content-Type': 'application/json'},
    );
  }
}
```

### Handler Rules

- One handler class per resource (UsersHandler, ProductsHandler)
- Keep handler methods under 20 lines; delegate business logic to services
- Use `_withAuth(handler)` helper to wrap individual routes with auth middleware
- Parse request body with `request.readAsString()` then `jsonDecode()`
- Always set `Content-Type: application/json` on JSON responses
- Return appropriate status codes: `201` for creation, `204` for deletion, `200` for reads/updates
- Use `shelf_router` path parameters with angle brackets: `/<id>`

## Middleware

A `Middleware` is a function that takes a `Handler` and returns a new `Handler`.

```dart
// Middleware type signature
typedef Middleware = Handler Function(Handler innerHandler);
```

### Writing Middleware

```dart
Middleware loggingMiddleware() {
  return (Handler innerHandler) {
    return (Request request) async {
      final stopwatch = Stopwatch()..start();
      print('[${DateTime.now()}] ${request.method} ${request.requestedUri}');

      final response = await innerHandler(request);

      stopwatch.stop();
      print(
        '[${DateTime.now()}] ${request.method} ${request.requestedUri} '
        '${response.statusCode} ${stopwatch.elapsedMilliseconds}ms',
      );

      return response;
    };
  };
}
```

### Error Handling Middleware

```dart
Middleware handleErrors() {
  return (Handler innerHandler) {
    return (Request request) async {
      try {
        return await innerHandler(request);
      } on NotFoundException catch (e) {
        return _jsonError(404, e.message);
      } on ValidationException catch (e) {
        return _jsonError(422, e.message, errors: e.errors);
      } on UnauthorizedException {
        return _jsonError(403, 'Unauthorized');
      } catch (e, stack) {
        print('Error: $e\n$stack');
        return _jsonError(500, 'Internal server error');
      }
    };
  };
}

Response _jsonError(int status, String message, {Map<String, dynamic>? errors}) {
  return Response(
    status,
    body: jsonEncode({
      'error': message,
      if (errors != null) 'errors': errors,
    }),
    headers: {'Content-Type': 'application/json'},
  );
}
```

### Middleware Rules

- Return `Middleware` (a function), not `Handler` directly
- Always `await innerHandler(request)` -- never skip calling the inner handler unless short-circuiting (auth failure, rate limit)
- Use `request.change(context: {...request.context, 'key': value})` to pass data downstream
- Error-handling middleware must catch all exceptions and return proper HTTP responses
- Never let unhandled exceptions propagate to `shelf_io.serve`

## Request and Response

### Reading Request Data

| Source | How | Example |
|--------|-----|---------|
| Body | `await request.readAsString()` then `jsonDecode()` | `final json = jsonDecode(await request.readAsString())` |
| Query params | `request.url.queryParameters['key']` | `int.tryParse(request.url.queryParameters['page'] ?? '1') ?? 1` |
| Path params | Extra function arguments (shelf_router) | `Future<Response> _getById(Request request, String id)` |
| Headers | `request.headers['Header-Name']` | `request.headers['Authorization']` |
| Context | `request.context['key']` | `request.context['user'] as User` |

### Building Responses

| Status | Method |
|--------|--------|
| 200 OK | `Response.ok(jsonEncode(data), headers: {'Content-Type': 'application/json'})` |
| 201 Created | `Response(201, body: jsonEncode(data), headers: {'Content-Type': 'application/json'})` |
| 204 No Content | `Response(204)` |
| 404 Not Found | `Response.notFound(jsonEncode({'error': 'Not found'}), headers: {'Content-Type': 'application/json'})` |
| Modify response | `response.change(headers: {...response.headers, 'X-Custom': 'value'})` |

### Request/Response Rules

- Parse query parameters defensively with `int.tryParse` and defaults
- Read the body only once (it is a stream); do not call `readAsString()` twice
- Use `request.change(context:)` for downstream data, never mutable globals
- Set `Content-Type` on every response that has a body

## Routing with shelf_router

```dart
final router = Router()
  ..get('/health', _health)
  ..get('/users', _listUsers)
  ..get('/users/<id>', _getUser)
  ..post('/users', _createUser)
  ..put('/users/<id>', _updateUser)
  ..delete('/users/<id>', _deleteUser);

// Mount sub-routers with path prefix
final root = Router()
  ..mount('/api/v1', apiRouter.call)
  ..mount('/ws', webSocketHandler);
```

### Routing Rules

- Use `..method('/path', handler)` cascade syntax for readability
- Mount sub-routers with `..mount('/prefix', router.call)`
- Path parameters use angle brackets: `/<id>`, `/<slug>`
- Always version API routes: `/api/v1/...`
- Group related routes in a single handler class

## Cascade (Fallback Routing)

`Cascade` tries handlers in order until one returns a non-404 response.

```dart
import 'package:shelf/shelf.dart';
import 'package:shelf_static/shelf_static.dart';

final cascade = Cascade()
    .add(apiRouter)
    .add(createStaticHandler('public', defaultDocument: 'index.html'));

final handler = const Pipeline()
    .addMiddleware(loggingMiddleware())
    .addHandler(cascade.handler);
```

### Cascade Rules

- Place specific handlers (API) before generic handlers (static files)
- `Cascade` treats 404 and 405 as "not handled" by default
- Use `statusCodes` parameter to customize which codes trigger fallthrough
- Useful for SPAs: API routes first, then static file handler as fallback

## Custom Exception Types

```dart
class UnauthorizedException implements Exception {
  final String message;
  UnauthorizedException([this.message = 'Unauthorized']);
}

class NotFoundException implements Exception {
  final String message;
  NotFoundException(this.message);
}

class ValidationException implements Exception {
  final String message;
  final Map<String, List<String>> errors;
  ValidationException(this.message, [this.errors = const {}]);
}
```

### Exception Rules

- Define domain exceptions that implement `Exception` (not `Error`)
- Map exceptions to HTTP status codes in error-handling middleware only
- Never throw generic `Exception('message')` -- use typed exceptions
- Include structured error details (field-level validation errors)

## Commands

```bash
# Development
dart run bin/server.dart            # Start server
dart run --enable-vm-service bin/server.dart  # With debugger

# Code generation (freezed, json_serializable)
dart run build_runner build --delete-conflicting-outputs
dart run build_runner watch         # Watch mode for codegen

# Testing
dart test                           # Run all tests
dart test test/handlers/            # Run specific directory
dart test --coverage                # With coverage

# Quality
dart format .                       # Format all files
dart analyze                        # Static analysis
dart fix --apply                    # Auto-fix lint issues

# Build
dart compile exe bin/server.dart -o server  # AOT compile to native binary
```

## Best Practices Summary

- **Pipeline**: Compose middleware with `Pipeline`; order matters (outermost runs first)
- **Handlers**: Keep thin; delegate to services; one class per resource
- **Error Handling**: Centralize in middleware; catch all exceptions; return structured JSON errors
- **Context**: Pass data between middleware and handlers via `request.change(context:)`
- **Testing**: Use `shelf` directly in tests (no HTTP server needed); mock services with `mocktail`
- **Security**: Validate all inputs; use parameterized database queries; never log secrets
- **Performance**: Compile to native executable for production; use streaming for large responses

## Advanced Topics

For detailed middleware examples, WebSocket support, static files, authentication flows, rate limiting, and testing patterns, see:

- [references/patterns.md](references/patterns.md) -- Full middleware patterns, WebSocket handler, static file serving, JWT auth, rate limiting, repository pattern, integration testing, Dockerfile

## External References

- [Shelf Documentation](https://pub.dev/packages/shelf)
- [shelf_router](https://pub.dev/packages/shelf_router)
- [shelf_static](https://pub.dev/packages/shelf_static)
- [shelf_web_socket](https://pub.dev/packages/shelf_web_socket)
- [Dart Server Tutorial](https://dart.dev/tutorials/server/httpserver)
