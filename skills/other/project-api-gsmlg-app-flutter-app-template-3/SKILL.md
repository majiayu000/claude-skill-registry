---
name: project-api
description: Guide for creating API client packages from OpenAPI specs using the api_client brick in app_api (project)
---

# Flutter API Client Development Skill

This skill guides the creation of API client packages using OpenAPI specifications, Dio, Retrofit, and code generation following this project's conventions.

## When to Use

Trigger this skill when:
- Integrating with a third-party API (GitHub, Stripe, etc.)
- Creating a client for a REST API
- User asks to "create an API client", "integrate API", "add API package"
- Need type-safe HTTP client with generated models

## Technology Stack

- **OpenAPI 3.0** - API specification format
- **swagger_parser** - Code generation from OpenAPI specs
- **Dio** - HTTP client for Dart
- **Retrofit** - Type-safe HTTP client generator
- **json_serializable** - JSON serialization

## Project Structure

API client packages MUST be created in `app_api/`:

```
app_api/
└── {api_name}/
    ├── lib/
    │   ├── {api_name}.dart              # Barrel export file
    │   ├── openapi.yaml                 # OpenAPI specification
    │   └── src/
    │       ├── {api_name}.dart          # Generated root client
    │       ├── clients/                 # Generated API clients
    │       └── models/                  # Generated DTOs/models
    ├── swagger_parser.yaml              # Code generation config
    ├── test/
    │   └── {api_name}_test.dart
    └── pubspec.yaml
```

## Creating a New API Client

### Step 1: Generate Package with Mason Brick

```bash
mason make api_client -o app_api/{api_name} --package_name {api_name}
```

**Example for GitHub API:**
```bash
mason make api_client -o app_api/github_api --package_name github_api
```

### Step 2: Add to Root Workspace

Add to root `pubspec.yaml` workspace section:

```yaml
workspace:
  - app_api/{api_name}
```

### Step 3: Write OpenAPI Specification

Edit `app_api/{api_name}/openapi.yaml` with your API definition.

### Step 4: Generate Code

```bash
cd app_api/{api_name}
flutter pub get
dart run swagger_parser
dart run build_runner build --delete-conflicting-outputs
```

## OpenAPI Specification Writing

### Basic Structure

```yaml
openapi: 3.1.0
info:
  title: GitHub API
  version: "1.0.0"
  description: GitHub REST API client

servers:
  - url: https://api.github.com
    description: GitHub API

tags:
  - name: Users
    description: User management endpoints
  - name: Repos
    description: Repository endpoints

paths:
  /users/{username}:
    get:
      tags: [Users]
      summary: Get a user
      operationId: getUser
      parameters:
        - name: username
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: User found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          description: User not found

  /users/{username}/repos:
    get:
      tags: [Repos]
      summary: List user repositories
      operationId: getUserRepos
      parameters:
        - name: username
          in: path
          required: true
          schema:
            type: string
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: per_page
          in: query
          schema:
            type: integer
            default: 30
      responses:
        '200':
          description: List of repositories
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Repository'

components:
  schemas:
    User:
      type: object
      required: [id, login, avatar_url]
      properties:
        id:
          type: integer
          format: int64
        login:
          type: string
        avatar_url:
          type: string
          format: uri
        name:
          type: string
          nullable: true
        email:
          type: string
          format: email
          nullable: true
        bio:
          type: string
          nullable: true
        public_repos:
          type: integer
        followers:
          type: integer
        following:
          type: integer

    Repository:
      type: object
      required: [id, name, full_name]
      properties:
        id:
          type: integer
          format: int64
        name:
          type: string
        full_name:
          type: string
        description:
          type: string
          nullable: true
        private:
          type: boolean
        html_url:
          type: string
          format: uri
        stargazers_count:
          type: integer
        forks_count:
          type: integer
        language:
          type: string
          nullable: true

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer

security:
  - bearerAuth: []
```

### Common OpenAPI Patterns

#### Path Parameters

```yaml
/users/{userId}/posts/{postId}:
  get:
    parameters:
      - name: userId
        in: path
        required: true
        schema:
          type: integer
      - name: postId
        in: path
        required: true
        schema:
          type: integer
```

#### Query Parameters

```yaml
/search:
  get:
    parameters:
      - name: q
        in: query
        required: true
        schema:
          type: string
      - name: sort
        in: query
        schema:
          type: string
          enum: [asc, desc]
          default: asc
      - name: limit
        in: query
        schema:
          type: integer
          minimum: 1
          maximum: 100
          default: 20
```

#### Request Body

```yaml
/users:
  post:
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/CreateUserRequest'
    responses:
      '201':
        description: User created
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/User'
```

#### File Upload

```yaml
/upload:
  post:
    requestBody:
      content:
        multipart/form-data:
          schema:
            type: object
            properties:
              file:
                type: string
                format: binary
              description:
                type: string
```

#### Headers

```yaml
/protected:
  get:
    parameters:
      - name: X-API-Key
        in: header
        required: true
        schema:
          type: string
```

#### Enums

```yaml
components:
  schemas:
    Status:
      type: string
      enum:
        - pending
        - active
        - completed
        - cancelled
```

#### Nullable Fields

```yaml
components:
  schemas:
    User:
      properties:
        bio:
          type: string
          nullable: true  # Can be null
```

#### Arrays

```yaml
components:
  schemas:
    TagList:
      type: array
      items:
        type: string
      minItems: 1
      maxItems: 10
```

#### Nested Objects

```yaml
components:
  schemas:
    Order:
      type: object
      properties:
        id:
          type: integer
        items:
          type: array
          items:
            $ref: '#/components/schemas/OrderItem'
        shipping:
          $ref: '#/components/schemas/Address'
```

## swagger_parser Configuration

The `swagger_parser.yaml` file controls code generation:

```yaml
swagger_parser:
  # OpenAPI spec location
  schema_path: ./openapi.yaml

  # Output directory for generated files
  output_directory: lib/src

  # API name (affects class names)
  name: "github_api"

  # Programming language
  language: dart

  # JSON serialization method
  json_serializer: json_serializable  # or: freezed, dart_mappable

  # Generate root client with all API instances
  root_client: true
  root_client_name: "GithubApi"

  # Generate export file
  export_file: true

  # Class naming
  client_postfix: Client  # UsersClient, ReposClient

  # Enum handling
  enums_to_json: false
  enums_parent_prefix: true
  unknown_enum_value: false

  # Organize generated code
  put_in_folder: false
  put_clients_in_folder: true

  # Skip certain parameters
  skipped_parameters:
    - "X-Request-Id"

  # Rename patterns
  replacement_rules:
    - pattern: "V1"
      replacement: ""
```

## Using Generated API Client

### Basic Usage (with createDioClient helper)

```dart
import 'package:github_api/github_api.dart';

// Create pre-configured Dio instance with automatic logging
// - Debug mode: LogInterceptor enabled by default
// - Release mode: LogInterceptor disabled by default
final dio = createDioClient(
  baseUrl: 'https://api.github.com',
  headers: {
    'Accept': 'application/vnd.github.v3+json',
  },
);

// Create API client
final api = GithubApi(dio);

// Make API calls
final user = await api.usersClient.getUser(username: 'octocat');
print('User: ${user.login}');

final repos = await api.reposClient.getUserRepos(
  username: 'octocat',
  page: 1,
  perPage: 10,
);
print('Repos: ${repos.length}');
```

### Logging Configuration

The `createDioClient` helper provides environment-aware logging:

```dart
// Default behavior:
// - Debug mode: logging ON
// - Release mode: logging OFF

// Explicitly enable/disable logging
final dio = createDioClient(
  baseUrl: 'https://api.example.com',
  enableLogging: true,  // Force enable
  // enableLogging: false, // Force disable
);

// Disable logging in debug via environment variable:
// flutter run --dart-define=DISABLE_API_LOG=true
```

### With Authentication

```dart
class AuthInterceptor extends Interceptor {
  final String token;

  AuthInterceptor(this.token);

  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) {
    options.headers['Authorization'] = 'Bearer $token';
    handler.next(options);
  }
}

// Setup with custom interceptors
final dio = createDioClient(
  baseUrl: 'https://api.github.com',
  interceptors: [AuthInterceptor('your-token')],
);

final api = GithubApi(dio);
```

### Error Handling

```dart
try {
  final user = await api.usersClient.getUser(username: 'nonexistent');
} on DioException catch (e) {
  switch (e.response?.statusCode) {
    case 404:
      print('User not found');
      break;
    case 401:
      print('Unauthorized - check your token');
      break;
    case 403:
      print('Forbidden - rate limit exceeded?');
      break;
    default:
      print('Error: ${e.message}');
  }
}
```

### With Retry Logic

```dart
import 'package:dio_smart_retry/dio_smart_retry.dart';

final dio = Dio();
dio.interceptors.add(RetryInterceptor(
  dio: dio,
  logPrint: print,
  retries: 3,
  retryDelays: const [
    Duration(seconds: 1),
    Duration(seconds: 2),
    Duration(seconds: 3),
  ],
));
```

### Environment Configuration

```dart
enum Environment { development, staging, production }

class ApiConfig {
  static String baseUrl(Environment env) {
    switch (env) {
      case Environment.development:
        return 'http://localhost:3000';
      case Environment.staging:
        return 'https://staging-api.example.com';
      case Environment.production:
        return 'https://api.example.com';
    }
  }
}

final dio = Dio(BaseOptions(
  baseUrl: ApiConfig.baseUrl(Environment.production),
  connectTimeout: const Duration(seconds: 10),
  receiveTimeout: const Duration(seconds: 30),
));
```

## Complete Example: GitHub API Client

### 1. Generate Package

```bash
mason make api_client -o app_api/github_api --package_name github_api
```

### 2. Write OpenAPI Spec

```yaml
# app_api/github_api/openapi.yaml
openapi: 3.1.0
info:
  title: GitHub API
  version: "1.0.0"
servers:
  - url: https://api.github.com

paths:
  /users/{username}:
    get:
      operationId: getUser
      parameters:
        - name: username
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'

  /users/{username}/repos:
    get:
      operationId: listUserRepos
      parameters:
        - name: username
          in: path
          required: true
          schema:
            type: string
        - name: per_page
          in: query
          schema:
            type: integer
            default: 30
      responses:
        '200':
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Repository'

components:
  schemas:
    User:
      type: object
      required: [id, login]
      properties:
        id:
          type: integer
        login:
          type: string
        name:
          type: string
          nullable: true
        avatar_url:
          type: string

    Repository:
      type: object
      required: [id, name]
      properties:
        id:
          type: integer
        name:
          type: string
        description:
          type: string
          nullable: true
        stargazers_count:
          type: integer
```

### 3. Generate Code

```bash
cd app_api/github_api
flutter pub get
dart run swagger_parser
dart run build_runner build --delete-conflicting-outputs
```

### 4. Use in App

```dart
// lib/services/github_service.dart
import 'package:dio/dio.dart';
import 'package:github_api/github_api.dart';

class GithubService {
  late final GithubApi _api;

  GithubService({String? token}) {
    final dio = Dio(BaseOptions(
      baseUrl: 'https://api.github.com',
      headers: {
        'Accept': 'application/vnd.github.v3+json',
        if (token != null) 'Authorization': 'Bearer $token',
      },
    ));
    _api = GithubApi(dio);
  }

  Future<User> getUser(String username) {
    return _api.usersClient.getUser(username: username);
  }

  Future<List<Repository>> getUserRepos(String username, {int perPage = 30}) {
    return _api.reposClient.listUserRepos(
      username: username,
      perPage: perPage,
    );
  }
}
```

## Dependencies (Auto-generated)

```yaml
dependencies:
  dio: ^5.7.0
  json_annotation: ^4.9.0
  freezed_annotation: ^3.0.0
  retrofit: ^4.4.2

dev_dependencies:
  build_runner: any
  json_serializable: ^6.9.3
  freezed: ^3.0.6
  swagger_parser: ^1.26.1
  retrofit_generator: ^9.1.9
```

## Workflow Summary

1. **Create package:** `mason make api_client -o app_api/{name} --package_name {name}`
2. **Add to workspace:** Update root `pubspec.yaml`
3. **Write OpenAPI spec:** Edit `openapi.yaml`
4. **Generate code:** `dart run swagger_parser && dart run build_runner build`
5. **Use client:** Import and create instance with Dio

## Best Practices

1. **Version your OpenAPI specs** - Keep specs in version control
2. **Use operationId** - Provides meaningful method names
3. **Define all schemas** - Enables type-safe models
4. **Handle nullable fields** - Mark optional fields as nullable
5. **Document endpoints** - Add descriptions and examples
6. **Use security schemes** - Define authentication requirements
7. **Add interceptors** - For auth, logging, retry logic
8. **Configure timeouts** - Prevent hanging requests
9. **Test generated clients** - Mock Dio for unit tests
