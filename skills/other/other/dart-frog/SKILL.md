---
name: dart-frog
description: |
  Dart Frog framework guardrails, patterns, and best practices for AI-assisted development.
  Use when working with Dart Frog projects, or when the user mentions Dart Frog.
  Provides file-based routing, middleware, dependency injection, and server-side Dart guidelines.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: framework
  language: dart
  extensions: ".dart"
---

# Dart Frog Framework Guide

> Applies to: Dart Frog 1.x, Dart 3.x, REST APIs, Full-Stack Dart, Serverless Functions

## Overview

Dart Frog is a fast, minimalistic backend framework for Dart built on top of Shelf. It provides
file-based routing (similar to Next.js), built-in middleware support, dependency injection via
providers, hot reload during development, and easy deployment with Docker. Dart Frog pairs
naturally with Flutter for full-stack Dart applications.

### Key Features

- File-based routing: route structure mirrors the filesystem
- Middleware cascades: `_middleware.dart` files apply to all routes in their directory subtree
- Dependency injection: `provider<T>()` and `context.read<T>()` for clean service access
- Hot reload: `dart_frog dev` watches for changes automatically
- Production builds: compiles to a self-contained server binary
- Docker-ready: ships with a Dockerfile scaffold

## Guardrails

### Project Organization

- Place all route handlers under `routes/`
- Place business logic, models, repositories, and services under `lib/src/`
- Export a barrel file at `lib/<project_name>.dart`
- Keep route files thin: delegate to services, never embed business logic in handlers
- Mirror test structure under `test/routes/` to match `routes/` layout

### Code Style

- Run `dart format .` before every commit
- Run `dart analyze` and fix all warnings before committing
- Use `very_good_analysis` lint rules (or `lints` package at minimum)
- Exclude generated files (`*.g.dart`, `*.freezed.dart`) from analysis

### Error Handling

- Define custom exception classes extending a base `AppException`
- Use a global error-handler middleware to catch all exceptions and return JSON
- Never expose stack traces in production responses
- Always return structured JSON error bodies: `{"error": "<message>"}`
- Use `dart:io` `HttpStatus` constants instead of magic status code numbers

### Security

- Validate all request body fields before processing
- Use parameterized queries for all database access
- Never hardcode secrets; read from environment variables via a `Config` class
- Set CORS allowed origins to specific domains in production (never `*`)
- Verify JWT signatures with a secret loaded from config, not inline strings

## Project Structure

```
myapp/
routes/
  _middleware.dart          # Global middleware (logging, CORS, error handler, DI)
  index.dart                # GET /
  health.dart               # GET /health
  api/
    _middleware.dart        # JSON content-type header
    v1/
      _middleware.dart      # Auth provider
      users/
        _middleware.dart    # Require authentication
        index.dart          # GET|POST /api/v1/users
        [id].dart           # GET|PUT|DELETE /api/v1/users/:id
      posts/
        index.dart
        [id].dart
    auth/
      login.dart            # POST /api/v1/auth/login
      register.dart         # POST /api/v1/auth/register
  ws.dart                   # WebSocket endpoint
lib/
  myapp.dart                # Barrel export
  src/
    models/
      user.dart
    repositories/
      user_repository.dart
    services/
      user_service.dart
    middleware/
      auth_provider.dart
    exceptions.dart
test/
  routes/
    api/v1/users/
      index_test.dart
pubspec.yaml
Dockerfile
```

## File-Based Routing

### Route-to-File Mapping

| URL Path | File |
|---|---|
| `/` | `routes/index.dart` |
| `/health` | `routes/health.dart` |
| `/api/v1/users` | `routes/api/v1/users/index.dart` |
| `/api/v1/users/:id` | `routes/api/v1/users/[id].dart` |
| `/api/v1/users/:uid/posts/:pid` | `routes/api/v1/users/[uid]/posts/[pid].dart` |

### Handler Signature

Every route file must export a top-level `onRequest` function:

```dart
// Synchronous handler (no async work)
Response onRequest(RequestContext context) { ... }

// Async handler
Future<Response> onRequest(RequestContext context) async { ... }

// Dynamic route — parameters are positional String arguments
Future<Response> onRequest(RequestContext context, String id) async { ... }

// Nested dynamic route — one String per segment
Future<Response> onRequest(
  RequestContext context,
  String userId,
  String postId,
) async { ... }
```

### Method Routing

Use a `switch` on `context.request.method` to dispatch by HTTP verb:

```dart
Future<Response> onRequest(RequestContext context) async {
  return switch (context.request.method) {
    HttpMethod.get => _handleGet(context),
    HttpMethod.post => _handlePost(context),
    _ => Future.value(Response(statusCode: HttpStatus.methodNotAllowed)),
  };
}
```

Always return `405 Method Not Allowed` for unsupported verbs.

## Request Context

### Reading the Request

```dart
// Query parameters
final page = int.tryParse(
  context.request.uri.queryParameters['page'] ?? '1',
) ?? 1;

// JSON body
final body = await context.request.json() as Map<String, dynamic>;

// Headers
final auth = context.request.headers['Authorization'];
```

### Dependency Access

Read any provider-registered dependency:

```dart
final userService = context.read<UserService>();
final config = context.read<Config>();
final currentUser = context.read<User?>(); // nullable for optional auth
```

### Building Responses

```dart
// JSON with default 200
Response.json({'message': 'OK'});

// JSON with explicit status
Response.json(user.toJson(), statusCode: HttpStatus.created);

// No content
Response(statusCode: HttpStatus.noContent);

// Custom headers
response.copyWith(headers: {...response.headers, 'X-Custom': 'value'});
```

## Middleware

Middleware files are named `_middleware.dart` and apply to every route in the same directory
and all subdirectories. They execute from outermost to innermost (root first).

### Anatomy

```dart
Handler middleware(Handler handler) {
  return handler
      .use(someMiddleware())
      .use(provider<SomeType>((context) => SomeType()));
}
```

### Middleware Cascade Order

```
routes/_middleware.dart           -> runs first (global)
routes/api/_middleware.dart       -> runs second
routes/api/v1/_middleware.dart    -> runs third (e.g., auth provider)
routes/api/v1/users/_middleware.dart -> runs last (e.g., require auth)
routes/api/v1/users/index.dart   -> handler
```

### Writing Custom Middleware

A `Middleware` is a function `Handler Function(Handler)`:

```dart
Middleware myMiddleware() {
  return (handler) {
    return (context) async {
      // Before handler
      final response = await handler(context);
      // After handler
      return response;
    };
  };
}
```

### Common Middleware Patterns

- **Request logger**: time the request, log method/path/status/duration
- **CORS**: add `Access-Control-Allow-*` headers, handle OPTIONS preflight
- **Error handler**: wrap handler in try/catch, map exceptions to HTTP status codes
- **JSON content-type**: add `Content-Type: application/json` to responses
- **Auth provider**: parse JWT from `Authorization` header, provide `User?`
- **Require auth**: check `context.read<User?>()`, return 401 if null

## Dependency Injection

Dart Frog uses the `provider<T>()` middleware to register dependencies:

```dart
Handler middleware(Handler handler) {
  return handler
      .use(provider<Config>((_) => Config.fromEnvironment()))
      .use(provider<Database>((ctx) => Database(ctx.read<Config>().dbUrl)))
      .use(provider<UserRepository>((ctx) =>
          UserRepositoryImpl(ctx.read<Database>())))
      .use(provider<UserService>((ctx) => UserService(
          ctx.read<UserRepository>(),
          ctx.read<Config>(),
      )));
}
```

### Rules

- Register providers from least-dependent to most-dependent (Config before Database)
- Providers can read previously registered dependencies via `context.read<T>()`
- Use nullable types (`User?`) for optional dependencies like authenticated user
- Keep the global middleware as the single source of truth for DI wiring
- Prefer constructor injection in services (accept interfaces, not concrete classes)

## Error Handling

### Exception Hierarchy

```dart
class AppException implements Exception {
  final String message;
  const AppException(this.message);
}

class ValidationException extends AppException {
  final Map<String, List<String>> errors;
  const ValidationException(super.message, [this.errors = const {}]);
}

class NotFoundException extends AppException {
  const NotFoundException(super.message);
}

class UnauthorizedException extends AppException {
  const UnauthorizedException([super.message = 'Unauthorized']);
}

class ForbiddenException extends AppException {
  const ForbiddenException([super.message = 'Forbidden']);
}
```

### Global Error Handler Middleware

```dart
Middleware errorHandler() {
  return (handler) {
    return (context) async {
      try {
        return await handler(context);
      } on ValidationException catch (e) {
        return Response.json(
          {'error': e.message, 'errors': e.errors},
          statusCode: HttpStatus.unprocessableEntity,
        );
      } on NotFoundException catch (e) {
        return Response.json(
          {'error': e.message}, statusCode: HttpStatus.notFound);
      } on UnauthorizedException catch (e) {
        return Response.json(
          {'error': e.message}, statusCode: HttpStatus.unauthorized);
      } on ForbiddenException catch (e) {
        return Response.json(
          {'error': e.message}, statusCode: HttpStatus.forbidden);
      } catch (e, stack) {
        print('Unhandled: $e\n$stack');
        return Response.json(
          {'error': 'Internal server error'},
          statusCode: HttpStatus.internalServerError,
        );
      }
    };
  };
}
```

## Models

Use `freezed` + `json_serializable` for immutable, serializable models:

```dart
@freezed
class User with _$User {
  const User._();

  const factory User({
    required String id,
    required String email,
    required String name,
    @Default(false) bool isAdmin,
    @JsonKey(includeToJson: false) String? passwordHash,
    required DateTime createdAt,
    DateTime? updatedAt,
  }) = _User;

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
}
```

Run code generation after model changes:

```bash
dart run build_runner build --delete-conflicting-outputs
```

## Commands

```bash
# Scaffold a new project
dart_frog create myapp

# Development server with hot reload
dart_frog dev

# Production build
dart_frog build

# Run the compiled server
./build/bin/server

# Generate a new route file
dart_frog new route /api/v1/users

# Generate a new middleware file
dart_frog new middleware auth

# Run tests
dart test

# Code generation (freezed, json_serializable)
dart run build_runner build --delete-conflicting-outputs

# Format and analyze
dart format .
dart analyze
```

## Testing

### Route Handler Tests

Use `mocktail` to mock `RequestContext` and injected services:

```dart
class MockRequestContext extends Mock implements RequestContext {}
class MockUserService extends Mock implements UserService {}

void main() {
  late MockRequestContext context;
  late MockUserService userService;

  setUp(() {
    context = MockRequestContext();
    userService = MockUserService();
    when(() => context.read<UserService>()).thenReturn(userService);
  });

  test('GET returns users list', () async {
    when(() => userService.getAll(page: any(named: 'page'),
        limit: any(named: 'limit')))
        .thenAnswer((_) async => [mockUser]);

    when(() => context.request).thenReturn(
      Request.get(Uri.parse('http://localhost/api/v1/users')),
    );

    final response = await route.onRequest(context);
    expect(response.statusCode, equals(HttpStatus.ok));
  });
}
```

### Testing Rules

- Mirror route paths in test file paths: `routes/api/v1/users/index.dart` -> `test/routes/api/v1/users/index_test.dart`
- Mock all injected dependencies via `context.read<T>()`
- Test each HTTP method separately
- Test error cases (validation, not found, unauthorized)
- Coverage target: >80% for route handlers and services

## Advanced Topics

For detailed patterns and examples, see:

- [references/patterns.md](references/patterns.md) -- Route patterns, WebSocket, database integration, authentication, deployment

## External References

- [Dart Frog Documentation](https://dartfrog.vgv.dev/)
- [Dart Frog GitHub](https://github.com/VeryGoodOpenSource/dart_frog)
- [Very Good Ventures Blog](https://verygood.ventures/blog)
- [Dart Server Tutorial](https://dart.dev/tutorials/server/httpserver)
- [Shelf Package](https://pub.dev/packages/shelf)
