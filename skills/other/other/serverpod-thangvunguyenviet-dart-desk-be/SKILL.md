---
name: serverpod
description: "Expert guidance for the Serverpod backend framework for Flutter/Dart. Use when working with: endpoints, YAML models, ORM/transactions/migrations, auth (Google/Apple/email/custom), caching (Redis/in-memory), real-time streams/WebSockets, deployment, sessions, serialization, code generation, file uploads (S3/GCS/R2), future calls/scheduling, testing (serverpod_test), modules, logging, Insights, Serverpod Mini, web server (Relic routes/middleware), health checks. Triggers: serverpod, endpoint, database model, ORM, session, migration, auth, deploy, generate, file upload, future call, test, mini, health check, web server, middleware, Relic."
---

# Serverpod

Open-source, scalable backend framework for Flutter enabling full-stack Dart development.

- Docs: https://docs.serverpod.dev/
- pub.dev: https://pub.dev/packages/serverpod
- GitHub: https://github.com/serverpod/serverpod

## Project Structure

```
my_project/
├── my_project_server/    # Server (endpoints, models, business logic)
│   ├── lib/src/
│   │   ├── endpoints/    # API endpoints
│   │   └── models/       # YAML model definitions (.spy.yaml)
│   ├── migrations/       # Database migrations
│   └── config/           # Server configuration
├── my_project_client/    # Auto-generated client library
└── my_project_flutter/   # Flutter app
```

## Quick Start

```bash
# Install CLI
dart pub global activate serverpod_cli

# Create project
serverpod create my_project

# Generate code after model/endpoint changes
cd my_project_server && serverpod generate

# Create migration after model changes
serverpod create-migration

# Start server (requires Docker for PostgreSQL + Redis)
docker compose up --build --detach && dart run bin/main.dart
```

For full setup details: see [references/getting-started.md](references/getting-started.md)

## Core Concepts

### Models (YAML)

Define in `lib/src/models/`:

```yaml
# company.spy.yaml
class: Company
table: company
fields:
  name: String
  ceo: Employee?, relation(name=company_ceo)
indexes:
  company_name_idx:
    fields: name
    unique: true
```

After changes: `serverpod generate` then `serverpod create-migration`

**Key features:**
- Types: `int`, `double`, `bool`, `String`, `DateTime`, `Duration`, `UuidValue`, `ByteData`, `Uri`, enums, `List<T>`, `Map<String, T>`
- Field scopes: `database` (default for table models), `api`, `all`, `none`
- Relations: `relation(name=...)`, `relation(parent=table_name)`, `relation(optional)`
- Default values: `default='value'`, `default=true`, `default=now`, `default=persist='value'`

Full model syntax: see [references/models.md](references/models.md)

### Endpoints

Define in `lib/src/endpoints/`:

```dart
class CompanyEndpoint extends Endpoint {
  Future<Company> create(Session session, {required String name}) async {
    return Company.db.insertRow(session, Company(name: name));
  }

  Future<List<Company>> list(Session session) async {
    return Company.db.find(session);
  }
}
```

Call from Flutter:
```dart
final company = await client.company.create(name: 'Acme');
```

- `Session` provides access to database, caching, auth, logging
- All params after `session` must be named
- Throw `SerializableException` subclasses for typed client errors
- Default max request size: 512 kB (override via `get maxRequestSize`)

Advanced patterns: see [references/endpoints.md](references/endpoints.md)

### Database (ORM)

```dart
// Insert
final row = await Company.db.insertRow(session, company);

// Query with filtering
final companies = await Company.db.find(
  session,
  where: (t) => t.name.like('A%') & t.ceo.has(),
  orderBy: (t) => t.name,
  limit: 10,
);

// Find by ID / first match
final c = await Company.db.findById(session, id);
final c = await Company.db.findFirstRow(session, where: (t) => t.name.equals('Acme'));

// Update and delete
company.name = 'New Name';
await Company.db.updateRow(session, company);
await Company.db.deleteWhere(session, where: (t) => t.name.like('Old%'));

// Transactions
await session.db.transaction((tx) async {
  await Company.db.insertRow(session, c1, transaction: tx);
  await Company.db.insertRow(session, c2, transaction: tx);
});

// Eager loading relations
final c = await Company.db.findById(session, id,
  include: Company.include(ceo: Employee.include()));

// Count
final total = await Company.db.count(session);
```

Raw SQL, migrations, indexing: see [references/database.md](references/database.md)

### Authentication (IDP System)

**Server setup** (`server.dart`):
```dart
import 'package:serverpod_auth_idp_server/core.dart';
import 'package:serverpod_auth_idp_server/providers/google.dart';

final pod = Serverpod(args, Protocol(), Endpoints());

pod.initializeAuthServices(
  tokenManagerBuilders: [JwtConfigFromPasswords()],
  identityProviderBuilders: [
    GoogleIdpConfig(clientSecret: GoogleClientSecret.fromJsonString(
      pod.getPassword('googleClientSecret')!,
    )),
  ],
);
```

**Required endpoints** (create these files):
```dart
// google_idp_endpoint.dart
class GoogleIdpEndpoint extends GoogleIdpBaseEndpoint {}

// refresh_jwt_tokens_endpoint.dart
class RefreshJwtTokensEndpoint extends core.RefreshJwtTokensEndpoint {}
```

**Check auth in methods**:
```dart
final authInfo = session.authenticated; // AuthenticationInfo?
final userIdentifier = authInfo?.userIdentifier; // String (UUID)
```

**Require auth on endpoint**:
```dart
class SecureEndpoint extends Endpoint {
  @override
  bool get requireLogin => true;

  @override
  Set<Scope> get requiredScopes => {Scope('admin')};
}
```

Setup and providers: see [references/authentication.md](references/authentication.md)

### File Uploads

```dart
// Server: create upload description
Future<String?> getUploadDescription(Session session, String path) async {
  return await session.storage.createDirectFileUploadDescription(
    storageId: 'public',
    path: path,
  );
}

// Server: verify upload
Future<bool> verifyUpload(Session session, String path) async {
  return await session.storage.verifyDirectFileUpload(storageId: 'public', path: path);
}

// Server: access files
var url = await session.storage.getPublicUrl(storageId: 'public', path: 'my/path');
var data = await session.storage.retrieveFile(storageId: 'public', path: 'my/path');
```

Cloud storage (GCS, S3, R2): see [references/file-uploads.md](references/file-uploads.md)

### Future Calls (Scheduling)

```dart
class MyFutureCall extends FutureCall {
  Future<void> doWork(Session session) async {
    // Scheduled work here
  }
}

// Schedule with delay
await pod.futureCalls.callWithDelay(const Duration(hours: 1)).myFutureCall.doWork();

// Schedule at specific time
await pod.futureCalls.callAtTime(DateTime(2026, 1, 1)).myFutureCall.doWork();

// Cancel by identifier
await pod.futureCalls.cancel('my-identifier');
```

Full details: see [references/scheduling.md](references/scheduling.md)

### Caching

```dart
// Local (in-memory) and global (Redis) caching
await session.caches.local.put('key', obj);
await session.caches.global.put('key', obj, lifetime: Duration(minutes: 5));
final obj = await session.caches.global.get<MyObject>('key');
await session.caches.localAndGlobal.invalidateKey('key');
```

Cache patterns and groups: see [references/caching.md](references/caching.md)

### Real-time

```dart
// Server: post to channel
session.messages.postMessage('chat_1', ChatMessage(text: 'Hello'));

// Client: listen
client.messages.listen<ChatMessage>('chat_1').listen((msg) => print(msg.text));
```

Streams, WebSockets, patterns: see [references/realtime.md](references/realtime.md)

### Logging

```dart
session.log('Processing request', level: LogLevel.info);
session.log('Error occurred', level: LogLevel.warning, exception: e, stackTrace: stackTrace);
```

Logs stored in `serverpod_log`, `serverpod_query_log`, `serverpod_session_log` tables.

Configuration in server config or env vars:
- `SERVERPOD_SESSION_PERSISTENT_LOG_ENABLED` - database storage toggle
- `SERVERPOD_SESSION_CONSOLE_LOG_ENABLED` - console output toggle
- `SERVERPOD_SESSION_LOG_RETENTION_PERIOD` - retention (default: 90 days)
- `SERVERPOD_SESSION_CONSOLE_LOG_FORMAT` - `text` or `json`

### Testing

```dart
import 'package:test/test.dart';
import 'test_tools/serverpod_test_tools.dart';

void main() {
  withServerpod('Given Example endpoint', (sessionBuilder, endpoints) {
    test('when calling hello then should return greeting', () async {
      final greeting = await endpoints.example.hello(sessionBuilder, 'Michael');
      expect(greeting, 'Hello Michael');
    });
  });
}
```

Setup, auth testing, database seeding: see [references/testing.md](references/testing.md)

### Serverpod Mini

Lightweight alternative without PostgreSQL. Create with:

```bash
serverpod create myminipod --mini
```

Supports: endpoints, models, streaming, custom auth, caching, logging. Does NOT support: Postgres ORM, task scheduling, pre-built auth, file uploads, health checks, Insights.

### Web Server (Relic)

```dart
class HelloRoute extends Route {
  @override
  Future<Result> handleCall(Session session, Request request) async {
    return Response.ok(body: Body.fromString('Hello'));
  }
}

// Register in server.dart
pod.webServer.addRoute(HelloRoute(), '/api/hello');
pod.webServer.addMiddleware(myMiddleware, '/path');
```

Routes, middleware, static files: see [references/web-server.md](references/web-server.md)

### Health Checks

Three Kubernetes-style HTTP probes: `/livez` (liveness), `/readyz` (readiness), `/startupz` (startup). Custom indicators via `HealthIndicator<T>`. See [references/health-checks.md](references/health-checks.md)

## Reference Files

| File | Use when |
|------|----------|
| [references/getting-started.md](references/getting-started.md) | Setting up a new project, understanding structure |
| [references/models.md](references/models.md) | Defining YAML models, relations, indexes, enums |
| [references/endpoints.md](references/endpoints.md) | Creating endpoints, inheritance, error handling |
| [references/database.md](references/database.md) | ORM queries, migrations, raw SQL, transactions, indexing |
| [references/authentication.md](references/authentication.md) | Auth setup, sign-in providers, custom auth, scopes |
| [references/caching.md](references/caching.md) | In-memory/Redis caching, cache patterns, TTL |
| [references/realtime.md](references/realtime.md) | Streams, WebSockets, message channels |
| [references/deployment.md](references/deployment.md) | Server config, Docker, cloud deploy, nginx, scaling |
| [references/file-uploads.md](references/file-uploads.md) | File upload API, cloud storage (GCS, S3, R2) |
| [references/scheduling.md](references/scheduling.md) | Future calls, scheduled tasks, cancellation |
| [references/testing.md](references/testing.md) | Integration tests, withServerpod, auth testing, DB seeding |
| [references/serialization.md](references/serialization.md) | Custom serialization, Freezed, ProtocolSerialization |
| [references/modules.md](references/modules.md) | Using and creating Serverpod modules |
| [references/web-server.md](references/web-server.md) | Relic routes, middleware, static files, ContextProperty |
| [references/health-checks.md](references/health-checks.md) | Kubernetes probes (/livez, /readyz, /startupz), custom indicators |
| [references/sessions.md](references/sessions.md) | Session types, properties, manual sessions, lifecycle |
| [references/configuration.md](references/configuration.md) | YAML config, env variables, passwords.yaml, generator.yaml |
| [references/server-events.md](references/server-events.md) | Message channels, local/global messaging, auth revocation |
| [references/exceptions.md](references/exceptions.md) | Serializable exceptions, YAML definition, default values |
