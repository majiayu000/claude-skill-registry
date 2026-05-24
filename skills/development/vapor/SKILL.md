---
name: vapor
description: |
  Vapor framework guardrails, patterns, and best practices for AI-assisted development.
  Use when working with Vapor projects, or when the user mentions Vapor.
  Provides Fluent ORM, async Swift, routing, middleware, and server-side Swift guidelines.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: framework
  language: swift
  extensions: ".swift"
---

# Vapor Framework Guide

> Applies to: Vapor 4.x, Swift 5.9+, Fluent ORM, Leaf Templates, Server-Side Swift
> Language Guide: @.claude/skills/swift-guide/SKILL.md

## Overview

Vapor is a server-side Swift framework for building web applications, REST APIs, and backend services. It provides type-safe routing, Fluent ORM, async/await concurrency, JWT authentication, and Leaf templating.

**Use Vapor when:**
- Building Swift-native backend services
- Sharing code between iOS/macOS clients and the server
- You need type-safe, compile-time-checked API development
- You want async/await patterns throughout the stack

**Consider alternatives when:**
- Team lacks Swift experience
- You need a massive middleware ecosystem (consider Express, Rails)
- Maximum raw performance is critical (consider Rust/Actix-web)

## Guardrails

### Vapor-Specific Rules

- Use the `@main` entry point pattern with `Application.make`
- Group routes by resource with `RouteCollection` controllers
- Use Fluent property wrappers (`@ID`, `@Field`, `@Parent`, `@Children`) for models
- Use `Content` protocol for all request/response DTOs
- Use `Validatable` protocol for input validation on every endpoint
- Use `AsyncMiddleware` for cross-cutting concerns (auth, logging, CORS)
- Use `AsyncMigration` with both `prepare` and `revert` methods
- Configure databases from environment variables (never hardcode credentials)
- Use DTOs to separate API contracts from database models
- Implement pagination for all list endpoints
- Use `@Sendable` on all route handler closures
- Mark model classes as `@unchecked Sendable` (Fluent requirement)

### Anti-Patterns

- Do not expose Fluent models directly as API responses (use DTOs)
- Do not put business logic in controllers (use a service layer)
- Do not use `autoMigrate` in production (run migrations explicitly)
- Do not skip `revert` in migrations (always provide rollback)
- Do not use `try!` or `fatalError` in request handlers
- Do not store request-scoped state in global variables

## Project Structure

```
MyVaporApp/
├── Package.swift
├── Sources/
│   └── App/
│       ├── Controllers/        # RouteCollection implementations
│       │   ├── UserController.swift
│       │   └── AuthController.swift
│       ├── Models/             # Fluent models
│       │   ├── User.swift
│       │   └── Post.swift
│       ├── DTOs/               # Request/response types (Content + Validatable)
│       │   ├── UserDTO.swift
│       │   └── CreateUserRequest.swift
│       ├── Migrations/         # AsyncMigration implementations
│       │   ├── CreateUser.swift
│       │   └── CreatePost.swift
│       ├── Middleware/         # AsyncMiddleware implementations
│       │   ├── JWTAuthMiddleware.swift
│       │   └── AppErrorMiddleware.swift
│       ├── Services/          # Business logic (protocol + implementation)
│       │   ├── UserService.swift
│       │   └── EmailService.swift
│       ├── Extensions/
│       │   └── Request+Extensions.swift
│       ├── configure.swift    # Database, middleware, JWT, Leaf setup
│       ├── routes.swift       # Top-level route registration
│       └── entrypoint.swift   # @main entry point
├── Tests/
│   └── AppTests/
│       ├── UserControllerTests.swift
│       └── AuthControllerTests.swift
├── Resources/
│   └── Views/                 # Leaf templates
│       └── index.leaf
├── Public/                    # Static files
│   ├── css/
│   └── js/
└── docker-compose.yml
```

**Layer responsibilities:**
- `Controllers/` -- HTTP routing only: parse request, call service, write response
- `Services/` -- Business logic, orchestration, domain rules
- `Models/` -- Fluent database models with property wrappers
- `DTOs/` -- Request/response types with validation (`Content` + `Validatable`)
- `Migrations/` -- Schema changes with `prepare` and `revert`
- `Middleware/` -- Cross-cutting: auth, error handling, CORS, logging

## Application Setup

### Entry Point and Configuration

```swift
// entrypoint.swift
import Vapor
import Logging

@main
enum Entrypoint {
    static func main() async throws {
        var env = try Environment.detect()
        try LoggingSystem.bootstrap(from: &env)
        let app = try await Application.make(env)
        do {
            try await configure(app)
            try await app.execute()
        } catch {
            app.logger.report(error: error)
            try? await app.asyncShutdown()
            throw error
        }
    }
}

// configure.swift -- database, middleware, migrations, routes
func configure(_ app: Application) async throws {
    app.middleware.use(FileMiddleware(publicDirectory: app.directory.publicDirectory))
    app.middleware.use(AppErrorMiddleware())
    app.middleware.use(CORSMiddleware())

    // Database (always from environment variables)
    if let databaseURL = Environment.get("DATABASE_URL") {
        try app.databases.use(.postgres(url: databaseURL), as: .psql)
    } else {
        app.databases.use(.postgres(
            hostname: Environment.get("DB_HOST") ?? "localhost",
            port: Environment.get("DB_PORT").flatMap(Int.init) ?? 5432,
            username: Environment.get("DB_USER") ?? "vapor",
            password: Environment.get("DB_PASSWORD") ?? "vapor",
            database: Environment.get("DB_NAME") ?? "vapor_dev"
        ), as: .psql)
    }

    app.migrations.add(CreateUser())
    if app.environment == .development { try await app.autoMigrate() }
    try routes(app)
}

// routes.swift -- group public vs protected
func routes(_ app: Application) throws {
    app.get("health") { _ -> HTTPStatus in .ok }
    let api = app.grouped("api", "v1")
    try api.register(collection: AuthController())

    let protected = api.grouped(JWTAuthMiddleware())
    try protected.register(collection: UserController())
}
```

## Routing with Controllers

```swift
struct UserController: RouteCollection {
    func boot(routes: RoutesBuilder) throws {
        let users = routes.grouped("users")
        users.get(use: index)
        users.get(":userID", use: show)
        users.put(":userID", use: update)
        users.delete(":userID", use: delete)
    }

    @Sendable
    func index(req: Request) async throws -> PaginatedResponse<UserResponse> {
        let page = try req.query.decode(PageRequest.self)
        let result = try await User.query(on: req.db)
            .filter(\.$isActive == true)
            .sort(\.$createdAt, .descending)
            .paginate(PageRequest(page: page.page, per: page.per))
        let items = try result.items.map { try UserResponse(user: $0) }
        return PaginatedResponse(items: items, metadata: PageMetadata(
            page: page.page, perPage: page.per,
            total: result.metadata.total, totalPages: result.metadata.pageCount
        ))
    }

    @Sendable
    func show(req: Request) async throws -> UserResponse {
        guard let user = try await User.find(req.parameters.get("userID"), on: req.db) else {
            throw Abort(.notFound, reason: "User not found")
        }
        return try UserResponse(user: user)
    }
}
```

**Conventions:** Implement `RouteCollection` per resource. Use `@Sendable` on all handlers. Validate before processing. Return DTOs, not Fluent models.

## Fluent Models

### Model with Property Wrappers

```swift
import Fluent
import Vapor

final class User: Model, Content, @unchecked Sendable {
    static let schema = "users"

    @ID(key: .id)
    var id: UUID?

    @Field(key: "email")
    var email: String

    @Field(key: "password_hash")
    var passwordHash: String

    @Enum(key: "role")
    var role: Role

    @Timestamp(key: "created_at", on: .create)
    var createdAt: Date?

    @Timestamp(key: "updated_at", on: .update)
    var updatedAt: Date?

    @Children(for: \.$user)
    var posts: [Post]

    init() {}

    init(id: UUID? = nil, email: String, passwordHash: String, role: Role = .user) {
        self.id = id
        self.email = email
        self.passwordHash = passwordHash
        self.role = role
    }

    enum Role: String, Codable, CaseIterable {
        case admin, user, guest
    }
}
```

**Model conventions:**
- Always mark as `final class` conforming to `Model`, `Content`, `@unchecked Sendable`
- Use `@ID(key: .id)` for UUID primary keys
- Use `@Timestamp` for `created_at` and `updated_at`
- Use `@Parent`/`@Children`/`@Siblings` for relationships
- Provide an empty `init()` (Fluent requirement)

## Migrations

```swift
import Fluent

struct CreateUser: AsyncMigration {
    func prepare(on database: Database) async throws {
        let role = try await database.enum("user_role")
            .case("admin").case("user").case("guest")
            .create()

        try await database.schema("users")
            .id()
            .field("email", .string, .required)
            .field("password_hash", .string, .required)
            .field("role", role, .required)
            .field("created_at", .datetime)
            .field("updated_at", .datetime)
            .unique(on: "email")
            .create()
    }

    func revert(on database: Database) async throws {
        try await database.schema("users").delete()
        try await database.enum("user_role").delete()
    }
}
```

**Migration rules:**
- Always implement both `prepare` and `revert`
- Create enums before referencing them in schema
- Delete enums in `revert` after deleting the table
- Use `.references()` for foreign keys with `onDelete` behavior
- Add indexes for frequently queried columns

## DTOs and Validation

### Request/Response DTOs

```swift
import Vapor

struct CreateUserRequest: Content, Validatable {
    let email: String
    let password: String
    let name: String

    static func validations(_ validations: inout Validations) {
        validations.add("email", as: String.self, is: .email)
        validations.add("password", as: String.self, is: .count(8...))
        validations.add("name", as: String.self, is: !.empty)
    }
}

struct UserResponse: Content {
    let id: UUID
    let email: String
    let name: String
    let role: User.Role
    let createdAt: Date?

    init(user: User) throws {
        self.id = try user.requireID()
        self.email = user.email
        self.name = user.name
        self.role = user.role
        self.createdAt = user.createdAt
    }
}
```

**DTO conventions:**
- Request types conform to `Content` + `Validatable`
- Response types conform to `Content` only
- Always validate in the controller before processing: `try CreateUserRequest.validate(content: req)`
- Use `Validatable` rules: `.email`, `.count(range)`, `!.empty`, `.url`, `.alphanumeric`

## Middleware

### Custom AsyncMiddleware

```swift
import Vapor
import JWT

struct JWTAuthMiddleware: AsyncMiddleware {
    func respond(
        to request: Request,
        chainingTo next: any AsyncResponder
    ) async throws -> Response {
        guard let token = request.headers.bearerAuthorization?.token else {
            throw Abort(.unauthorized, reason: "Missing authorization token")
        }

        let payload = try await request.jwt.verify(token, as: UserPayload.self)

        guard let userID = UUID(payload.subject.value),
              let user = try await User.find(userID, on: request.db),
              user.isActive else {
            throw Abort(.unauthorized, reason: "User not found or inactive")
        }

        request.auth.login(user)
        return try await next.respond(to: request)
    }
}
```

### Error Middleware

```swift
import Vapor

struct AppErrorMiddleware: AsyncMiddleware {
    func respond(
        to request: Request,
        chainingTo next: any AsyncResponder
    ) async throws -> Response {
        do {
            return try await next.respond(to: request)
        } catch let abort as AbortError {
            let body = ErrorResponse(error: true, reason: abort.reason, code: abort.status.code)
            return try await body.encodeResponse(status: abort.status, for: request)
        } catch {
            request.logger.error("Unexpected error: \(error)")
            let reason = request.application.environment.isRelease
                ? "An internal error occurred" : error.localizedDescription
            let body = ErrorResponse(error: true, reason: reason, code: 500)
            return try await body.encodeResponse(status: .internalServerError, for: request)
        }
    }
}

struct ErrorResponse: Content {
    let error: Bool
    let reason: String
    let code: UInt
}
```

## Content Negotiation

Vapor's `Content` protocol handles JSON automatically. Configure custom encoding in `configure.swift`:

```swift
let encoder = JSONEncoder()
encoder.keyEncodingStrategy = .convertToSnakeCase
encoder.dateEncodingStrategy = .iso8601
ContentConfiguration.global.use(encoder: encoder, for: .json)
```

## Authentication (JWT)

```swift
// configure.swift -- register signing key
guard let jwtSecret = Environment.get("JWT_SECRET") else {
    fatalError("JWT_SECRET environment variable not set")
}
await app.jwt.keys.add(hmac: HMACKey(from: jwtSecret), digestAlgorithm: .sha256)

// Payload definition
struct UserPayload: JWTPayload {
    var subject: SubjectClaim
    var expiration: ExpirationClaim
    var isAdmin: Bool?

    func verify(using algorithm: some JWTAlgorithm) throws {
        try expiration.verifyNotExpired()
    }
}

// Token generation (in login handler)
let payload = UserPayload(
    subject: .init(value: try user.requireID().uuidString),
    expiration: .init(value: Date().addingTimeInterval(3600))
)
let token = try await req.jwt.sign(payload)
```

## Commands Reference

```bash
# Initialize project
swift package init --type executable --name MyVaporApp

# Resolve dependencies
swift package resolve

# Build and run
swift build
swift run App serve --hostname 0.0.0.0 --port 8080

# Run tests
swift test
swift test --filter AppTests

# Run database migrations manually
swift run App migrate
swift run App migrate --revert

# Docker build
docker build -t my-vapor-app .
docker compose up -d
```

## Dependencies

| Package | Purpose |
|---------|---------|
| `vapor/vapor` | Core web framework |
| `vapor/fluent` | ORM abstraction |
| `vapor/fluent-postgres-driver` | PostgreSQL support |
| `vapor/fluent-sqlite-driver` | SQLite (development/testing) |
| `vapor/redis` | Redis caching and sessions |
| `vapor/jwt` | JWT authentication |
| `vapor/leaf` | Template engine |
| `XCTVapor` | Testing utilities (included with Vapor) |

## Advanced Topics

For detailed patterns, WebSocket integration, Leaf templates, queues, testing, and deployment, see:

- [references/patterns.md](references/patterns.md) -- Fluent query patterns, relationships, eager loading, WebSocket, Leaf templates, background queues, comprehensive testing, Docker deployment

## External References

- [Vapor Documentation](https://docs.vapor.codes/)
- [Fluent Documentation](https://docs.vapor.codes/fluent/overview/)
- [Vapor Discord](https://discord.gg/vapor)
- [Swift Server Workgroup](https://www.swift.org/sswg/)
