---
name: fosmvvm-serverrequest-generator
description: Generate ServerRequest types for client-server communication in FOSMVVM. Use when implementing any operation that talks to the server - CRUD operations, data sync, actions, etc. ServerRequest is THE way clients communicate with servers.
---

# FOSMVVM ServerRequest Generator

Generate ServerRequest types for client-server communication.

> **Architecture context:** See [FOSMVVMArchitecture.md](../../docs/FOSMVVMArchitecture.md)

---

## STOP AND READ THIS

**ServerRequest is THE way to communicate with an FOSMVVM server. No exceptions.**

```
┌──────────────────────────────────────────────────────────────────────┐
│                 ALL CLIENTS USE ServerRequest                         │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  iOS App:         Button tap    →  request.processRequest(mvvmEnv:)   │
│  macOS App:       Button tap    →  request.processRequest(mvvmEnv:)   │
│  WebApp:          JS → WebApp   →  request.processRequest(mvvmEnv:)   │
│  CLI Tool:        main()        →  request.processRequest(mvvmEnv:)   │
│  Data Collector:  timer/event   →  request.processRequest(mvvmEnv:)   │
│  Background Job:  cron trigger  →  request.processRequest(mvvmEnv:)   │
│                                                                       │
│  MVVMEnvironment holds: baseURL, headers, version, error handling     │
│  Configure ONCE at startup, use EVERYWHERE via processRequest()       │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
```

### What You Must NEVER Do

```swift
// ❌ WRONG - hardcoded URL
let url = URL(string: "http://server/api/users/123")!
var request = URLRequest(url: url)

// ❌ WRONG - string path
try await client.get("/api/users/\(id)")

// ❌ WRONG - manual JSON encoding
let json = try JSONEncoder().encode(body)
request.httpBody = json
```

```javascript
// ❌ WRONG - hardcoded fetch path
fetch('/api/users/123')

// ❌ WRONG - constructing URLs manually
fetch(`/api/ideas/${ideaId}/move`)
```

### What You Must ALWAYS Do

**Step 1: Configure MVVMEnvironment once at startup**

```swift
// CLI tool, background job, data collector - configure at startup
// Import your shared module to get SystemVersion.currentApplicationVersion
import ViewModels  // ← Your shared module (see FOSMVVMArchitecture.md)

let mvvmEnv = await MVVMEnvironment(
    currentVersion: .currentApplicationVersion,  // From shared module
    appBundle: Bundle.module,
    deploymentURLs: [.debug: URL(string: "http://localhost:8080")!]
)
// NOTE: Version headers (X-FOS-Version) are AUTOMATIC via SystemVersion.current
```

The shared module contains `SystemVersion+App.swift`:
```swift
// In your shared ViewModels module
public extension SystemVersion {
    static var currentApplicationVersion: Self { .v1_0 }
    static var v1_0: Self { .init(major: 1, minor: 0, patch: 0) }
}
```

**Step 2: Use processRequest(mvvmEnv:) everywhere**

```swift
// ✅ RIGHT - ServerRequest with MVVMEnvironment
let request = UserShowRequest(query: .init(userId: id))
try await request.processRequest(mvvmEnv: mvvmEnv)
let user = request.responseBody

// ✅ RIGHT - Create operation
let createRequest = CreateIdeaRequest(requestBody: .init(content: content))
try await createRequest.processRequest(mvvmEnv: mvvmEnv)
let newId = createRequest.responseBody?.id

// ✅ RIGHT - Update operation
let updateRequest = MoveIdeaRequest(requestBody: .init(ideaId: id, newStatus: status))
try await updateRequest.processRequest(mvvmEnv: mvvmEnv)
```

**The path is derived from the type name. The HTTP method comes from the protocol. You NEVER write URL strings. Configuration lives in MVVMEnvironment - you NEVER pass baseURL/headers to individual requests.**

---

## When to Use This Skill

- Implementing any client-server communication
- Adding CRUD operations (Create, Read, Update, Delete)
- Building data collectors or sync tools
- Any Swift code that needs to talk to the server

**If you're about to write `URLRequest` or a hardcoded path string, STOP and use this skill instead.**

---

## What ServerRequest Provides

| Concern | How ServerRequest Handles It |
|---------|------------------------------|
| URL Path | Derived from type name via `Self.path` (e.g., `MoveIdeaRequest` → `/move_idea`) |
| HTTP Method | Determined by `action.httpMethod` (ShowRequest=GET, CreateRequest=POST, etc.) |
| Request Body | `RequestBody` type, automatically JSON encoded via `requestBody?.toJSONData()` |
| Response Body | `ResponseBody` type, automatically JSON decoded into `responseBody` |
| Error Response | `ResponseError` type, automatically decoded when response can't decode as `ResponseBody` |
| Validation | `RequestBody: ValidatableModel` for write operations |
| Body Size Limits | `RequestBody.maxBodySize` for large uploads (files, images) |
| Type Safety | Compiler enforces correct types throughout |

---

## Request Protocol Selection

Choose based on the operation:

| Operation | Protocol | HTTP Method | RequestBody Required? |
|-----------|----------|-------------|----------------------|
| Read data | `ShowRequest` | GET | No |
| Read ViewModel | `ViewModelRequest` | GET | No |
| Create entity | `CreateRequest` | POST | Yes (ValidatableModel) |
| Update entity | `UpdateRequest` | PATCH | Yes (ValidatableModel) |
| Replace entity | (use `.replace` action) | PUT | Yes |
| Soft delete | `DeleteRequest` | DELETE | No |
| Hard delete | `DestroyRequest` | DELETE | No |

---

## What This Skill Generates

### Core Files (Always)

| File | Location | Purpose |
|------|----------|---------|
| `{Action}Request.swift` | `{ViewModelsTarget}/Requests/` | The ServerRequest type |
| `{Action}Controller.swift` | `{WebServerTarget}/Controllers/` | Server-side handler |

### Optional: WebApp Bridge (for web clients)

| File | Purpose |
|------|---------|
| WebApp route | Bridges JS fetch to ServerRequest.fetch() |
| JS handler guidance | How to invoke from browser |

---

## How to Use This Skill

**Invocation:**
/fosmvvm-serverrequest-generator

**Prerequisites:**
- Operation requirements understood from conversation context
- RequestBody and ResponseBody structures discussed or documented
- Client type identified (iOS app, WebApp, CLI tool, background job, etc.)

**Workflow integration:**
This skill is typically used when implementing client-server communication. The skill references conversation context automatically—no file paths or Q&A needed. Often follows fosmvvm-viewmodel-generator (for ResponseBody ViewModels) and fosmvvm-fields-generator (for RequestBody validation).

## Pattern Implementation

This skill references conversation context to determine ServerRequest structure:

### Operation Type Detection

From conversation context, the skill identifies:
- **CRUD operation** (create, read, update, delete)
- **HTTP semantics** (GET for read, POST for create, PATCH/PUT for update, DELETE for delete)
- **Protocol choice** (ShowRequest, ViewModelRequest, CreateRequest, UpdateRequest, DeleteRequest)

### Request Structure Design

From requirements already in context:
- **RequestBody fields** (what data the client sends)
- **Query parameters** (URL query string data)
- **Fragment parameters** (URL fragment/anchor data)
- **Validation requirements** (ValidatableModel for write operations)

### Response Structure Design

From requirements already in context:
- **ResponseBody type** (often a ViewModel, sometimes just an ID)
- **ResponseError type** (custom error structure or EmptyError)
- **Success scenarios** (what indicates successful operation)
- **Error scenarios** (known failure modes requiring structured errors)

### Client Detection

From conversation context:
- **Target platform** (iOS/macOS app, WebApp browser, CLI tool, background job)
- **Bridge requirements** (whether WebApp route needed for browser clients)
- **MVVMEnvironment setup** (how client configures baseURL and headers)

### File Generation

**Core files:**
1. ServerRequest type with RequestBody, ResponseBody, ResponseError
2. Controller with action handler
3. Route registration

**Optional (for WebApp clients):**
4. WebApp route bridging JS to ServerRequest
5. JavaScript handler guidance

### Context Sources

Skill references information from:
- **Prior conversation**: Operation requirements, data structures discussed
- **Specification files**: If Claude has read API specs or feature docs into context
- **Existing patterns**: From codebase analysis of similar requests

---

### ServerRequest Type Template

```swift
// {Action}Request.swift
import FOSMVVM

public final class {Action}Request: {Protocol}, @unchecked Sendable {
    public typealias Query = EmptyQuery       // or custom Query type
    public typealias Fragment = EmptyFragment
    // ResponseError: use EmptyError OR define nested ResponseError struct (see below)

    public let requestBody: RequestBody?
    public var responseBody: ResponseBody?

    // What the client sends
    public struct RequestBody: ServerRequestBody, ValidatableModel {
        // Fields...
    }

    // What the server returns
    public struct ResponseBody: {Protocol}ResponseBody {
        // Fields (often contains a ViewModel)
    }

    // Optional: Custom error type (nested, not top-level!)
    // public struct ResponseError: ServerRequestError { ... }

    public init(
        query: Query? = nil,
        fragment: Fragment? = nil,
        requestBody: RequestBody? = nil,
        responseBody: ResponseBody? = nil
    ) {
        self.requestBody = requestBody
        self.responseBody = responseBody
    }
}
```

**Note:** All subtypes (RequestBody, ResponseBody, ResponseError) are nested inside the request class. This avoids namespace pollution and provides unique YAML localization keys automatically.

### Controller Template

**Controller action = Protocol name (minus "Request")**

| Protocol | Action | HTTP Method |
|----------|--------|-------------|
| `ShowRequest` | `.show` | GET |
| `ViewModelRequest` | `.show` | GET |
| `CreateRequest` | `.create` | POST |
| `UpdateRequest` | `.update` | PATCH |
| `DeleteRequest` | `.delete` | DELETE |
| `DestroyRequest` | `.destroy` | DELETE |
| Custom request | Whatever fits your semantics | Depends on action |

The pattern is mechanical: `UpdateRequest` → `.update`. `CreateRequest` → `.create`. Just match the names.

```swift
// {Action}Controller.swift
import Vapor
import FOSMVVM
import FOSMVVMVapor

final class {Action}Controller: ServerRequestController {
    typealias TRequest = {Action}Request

    let actions: [ServerRequestAction: ActionProcessor] = [
        .{action}: {Action}Request.performAction
    ]
}

private extension {Action}Request {
    static func performAction(
        _ request: Vapor.Request,
        _ serverRequest: {Action}Request,
        _ requestBody: RequestBody
    ) async throws -> ResponseBody {
        let db = request.db

        // 1. Fetch/validate
        // 2. Perform operation
        // 3. Build response (often a ViewModel)

        return .init(...)
    }
}
```

### Controller Registration

```swift
// In WebServer routes.swift
try versionedGroup.register(collection: {Action}Controller())
```

### Client Invocation

**All Swift clients (iOS, macOS, CLI, background jobs, etc.):**

```swift
// MVVMEnvironment configured once at app/tool startup (see "What You Must ALWAYS Do")
let request = {Action}Request(requestBody: .init(...))
try await request.processRequest(mvvmEnv: mvvmEnv)
let result = request.responseBody
```

**WebApp (browser clients):**
See [WebApp Bridge Pattern](#webapp-bridge-pattern) below.

---

## WebApp Bridge Pattern

When the client is a web browser, you need a bridge between JavaScript and ServerRequest:

```
Browser                    WebApp (Swift)                      WebServer
   │                            │                                  │
   │  POST /action-name         │                                  │
   │  (JSON body)               │                                  │
   │ ─────────────────────────► │                                  │
   │                            │  request.processRequest(mvvmEnv:)│
   │                            │ ────────────────────────────────►│
   │                            │ ◄────────────────────────────────│
   │  ◄──────────────────────── │  (ResponseBody)                  │
   │  (HTML fragment or JSON)   │                                  │
```

**The WebApp route is internal wiring** - it's how browsers invoke ServerRequest, just like a button tap invokes it in iOS.

### WebApp Route

```swift
// WebApp routes.swift
app.post("{action-name}") { req async throws -> Response in
    // 1. Decode what JS sent
    let body = try req.content.decode({Action}Request.RequestBody.self)

    // 2. Call server via ServerRequest (NOT hardcoded URL!)
    // mvvmEnv is configured at WebApp startup
    let serverRequest = {Action}Request(requestBody: body)
    try await serverRequest.processRequest(mvvmEnv: req.application.mvvmEnv)

    // 3. Return response (HTML fragment or JSON)
    guard let response = serverRequest.responseBody else {
        throw Abort(.internalServerError, reason: "No response from server")
    }
    // ...
}
```

### JavaScript Handler

```javascript
async function handle{Action}(data) {
    const response = await fetch('/{action-name}', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    // Handle response...
}
```

**Note:** The JS fetches to the WebApp (same origin), which then uses ServerRequest to talk to the WebServer. The browser NEVER talks directly to the WebServer.

---

## Common Patterns

### ViewModel Response

Most operations return a ViewModel for UI update:

```swift
public struct ResponseBody: UpdateResponseBody {
    public let viewModel: IdeaCardViewModel
}
```

### ID-Only Response

Some operations just need confirmation:

```swift
public struct ResponseBody: CreateResponseBody {
    public let id: ModelIdType
}
```

### Empty Response

Delete operations often return nothing:

```swift
// Use EmptyBody as ResponseBody
public typealias ResponseBody = EmptyBody
```

---

## ResponseError - Typed Error Handling

Each `ServerRequest` can define a custom `ResponseError` type for structured error responses from the server.

### How It Works

When processing a response:
1. Framework tries to decode as `ResponseBody`
2. If that fails, tries to decode as `ResponseError`
3. If `ResponseError` decode succeeds, that error is thrown
4. Client catches with try/catch at the call site

### When to Use Custom ResponseError

**Use custom `ResponseError` when:**
- Operation has known failure modes (validation, quota, permissions)
- Server returns structured error details (field names, error codes)
- Client needs to take specific action based on error type
- You want field-level validation error display

**Use `EmptyError` (default) when:**
- Operation rarely fails
- Failures are exceptional (network down, server crash)
- No structured error response expected
- You only need success/failure, not why

### Nesting Pattern

**ResponseError MUST be nested inside the request class**, just like RequestBody and ResponseBody:

```swift
public final class CreateIdeaRequest: CreateRequest, @unchecked Sendable {
    public typealias Query = EmptyQuery
    public typealias Fragment = EmptyFragment
    // No typealias needed - ResponseError is nested

    public let requestBody: RequestBody?
    public var responseBody: ResponseBody?

    // ✅ All subtypes nested inside the request
    public struct RequestBody: ServerRequestBody, ValidatableModel { ... }
    public struct ResponseBody: CreateResponseBody { ... }
    public struct ResponseError: ServerRequestError { ... }  // ← Nested, not top-level

    public init(...) { ... }
}
```

**Why nesting matters:**
- Consistent with RequestBody/ResponseBody pattern
- Avoids namespace pollution (no `CreateIdeaError`, `MoveIdeaError`, etc. at top level)
- YAML localization keys are scoped: `CreateIdeaRequest.ResponseError.ErrorCode.quotaExceeded`
- No need for unique type names like `GovernanceLessonCreateError` - nesting provides uniqueness

### Pattern 1: Errors with Associated Values

For errors that need dynamic data in their messages, use `LocalizableSubstitutions`:

```swift
public final class CreateIdeaRequest: CreateRequest, @unchecked Sendable {
    // ... other typealiases and properties ...

    public struct ResponseError: ServerRequestError {
        public let code: ErrorCode
        public let message: LocalizableSubstitutions

        public enum ErrorCode: Codable, Sendable {
            case duplicateContent
            case quotaExceeded(requestedSize: Int, maximumSize: Int)
            case invalidCategory(category: String)

            var message: LocalizableSubstitutions {
                switch self {
                case .duplicateContent:
                    .init(
                        baseString: .localized(for: Self.self, parentType: ResponseError.self, propertyName: "duplicateContent"),
                        substitutions: [:]
                    )
                case .quotaExceeded(let requestedSize, let maximumSize):
                    .init(
                        baseString: .localized(for: Self.self, parentType: ResponseError.self, propertyName: "quotaExceeded"),
                        substitutions: [
                            "requestedSize": LocalizableInt(value: requestedSize),
                            "maximumSize": LocalizableInt(value: maximumSize)
                        ]
                    )
                case .invalidCategory(let category):
                    .init(
                        baseString: .localized(for: Self.self, parentType: ResponseError.self, propertyName: "invalidCategory"),
                        substitutions: [
                            "category": LocalizableString.constant(category)
                        ]
                    )
                }
            }
        }

        public init(code: ErrorCode) {
            self.code = code
            self.message = code.message  // Required to localize properly via Codable
        }
    }
}
```

```yaml
en:
  CreateIdeaRequest:
    ResponseError:
      ErrorCode:
        duplicateContent: "The requested content is a duplicate of an existing idea."
        quotaExceeded: "The requested content size %{requestedSize} exceeds the maximum allowed size %{maximumSize}."
        invalidCategory: "The category %{category} is not valid."
```

### Pattern 2: Simple Errors (String-Based Codes)

For simpler errors without associated values, use a `String` raw value enum:

```swift
public final class MoveIdeaRequest: UpdateRequest, @unchecked Sendable {
    // ... other typealiases and properties ...

    public struct ResponseError: ServerRequestError {
        public let code: ErrorCode
        public let message: LocalizableString

        public enum ErrorCode: String, Codable, Sendable {
            case ideaNotFound
            case invalidTransition

            var message: LocalizableString {
                .localized(for: Self.self, parentType: ResponseError.self, propertyName: rawValue)
            }
        }

        public init(code: ErrorCode) {
            self.code = code
            self.message = code.message  // Required to localize properly via Codable
        }
    }
}
```

```yaml
en:
  MoveIdeaRequest:
    ResponseError:
      ErrorCode:
        ideaNotFound: "The idea was not found"
        invalidTransition: "Cannot move to the requested status"
```

### Type Safety Means You Already Know

**STOP. Before you panic about "how do I know what error type I have?"**

This isn't JavaScript. The type system tells you everything at compile time:

```swift
// When you write this request...
let request = MoveIdeaRequest(requestBody: body)

// ...you KNOW:
// - MoveIdeaRequest.ResponseError exists (it's declared in the type)
// - It has exactly the cases you defined (ideaNotFound, invalidTransition)
// - Each case has whatever properties you gave it

// So when you catch, you catch THE SPECIFIC TYPE:
do {
    try await request.processRequest(mvvmEnv: mvvmEnv)
} catch let error as MoveIdeaRequest.ResponseError {
    // I KNOW this is MoveIdeaRequest.ResponseError
    // I KNOW it has .code
    // I KNOW .code is ErrorCode enum with ideaNotFound, invalidTransition
    // No mystery. No runtime discovery. No "what if?"
}
```

**The anti-pattern (JavaScript brain):**
```swift
// ❌ WRONG - treating typed errors as unknown
catch let error as ServerRequestError {
    // "How do I get the message? What properties does it have?"
    // This thinking is WRONG. You're not in a typeless world.
}
```

**The pattern (Swift brain):**
```swift
// ✅ RIGHT - you know the exact type
catch let error as MoveIdeaRequest.ResponseError {
    switch error.code {
    case .ideaNotFound: // I know this exists
    case .invalidTransition: // I know this exists
    }
}
```

The `ServerRequestError` protocol is a marker (`Error, Codable, Sendable`). It doesn't guarantee properties because **it doesn't need to** - you catch the concrete type, not the protocol.

### Client Error Handling

The primary pattern is try/catch at the call site:

```swift
do {
    try await request.processRequest(mvvmEnv: mvvmEnv)
} catch let error as CreateIdeaError {
    switch error.code {
    case .duplicateContent:
        showDuplicateWarning(message: error.message)
    case .quotaExceeded(let requestedSize, let maximumSize):
        showQuotaError(requested: requestedSize, maximum: maximumSize, message: error.message)
    case .invalidCategory(let category):
        highlightInvalidCategory(category, message: error.message)
    }
} catch {
    showGenericError(error)
}
```

### Built-in ValidationError

FOSMVVM provides `ValidationError` for field-level validation failures:

```swift
// In controller - use Validations to collect errors
let validations = Validations()

if requestBody.email.isEmpty {
    validations.validations.append(.init(
        status: .error,
        fieldId: "email",
        message: .localized(for: CreateUserRequest.self, propertyName: "emailRequired")
    ))
}

// Throw if any errors
if let error = validations.validationError {
    throw error
}
```

```swift
// Client catches ValidationError
catch let error as ValidationError {
    for validation in error.validations {
        for message in validation.messages {
            for fieldId in message.fieldIds {
                formFields[fieldId]?.showError(message.message)
            }
        }
    }
}
```

> **Architecture context:** See [ServerRequestError - Typed Error Responses](../../docs/FOSMVVMArchitecture.md#serverrequesterror---typed-error-responses) for full details.

---

## Testing ServerRequests

**Always test via `ServerRequest.processRequest(mvvmEnv:)` - never via manual HTTP.**

See [fosmvvm-serverrequest-test-generator](../fosmvvm-serverrequest-test-generator/SKILL.md) for complete testing guidance.

```swift
// ✅ RIGHT - tests the actual client code path
let request = Update{Entity}Request(
    query: .init(entityId: id),
    requestBody: .init(name: "New Name")
)
try await request.processRequest(mvvmEnv: testMvvmEnv)
#expect(request.responseBody?.viewModel.name == "New Name")

// ❌ WRONG - manual HTTP bypasses version negotiation
try await app.sendRequest(.PATCH, "/entity/\(id)", body: json)
```

---

## See Also

- [Architecture Patterns](../shared/architecture-patterns.md) - Mental models (errors are data, type safety, etc.)
- [FOSMVVMArchitecture.md](../../docs/FOSMVVMArchitecture.md) - Full architecture, especially "Core Principle: ServerRequest Is THE Way"
- [fosmvvm-serverrequest-test-generator](../fosmvvm-serverrequest-test-generator/SKILL.md) - For testing ServerRequest types
- [fosmvvm-viewmodel-generator](../fosmvvm-viewmodel-generator/SKILL.md) - For ViewModels returned by requests
- [fosmvvm-fields-generator](../fosmvvm-fields-generator/SKILL.md) - For ValidatableModel in RequestBody
- [fosmvvm-leaf-view-generator](../fosmvvm-leaf-view-generator/SKILL.md) - For Leaf templates that render ViewModels
- [reference.md](reference.md) - Complete file templates

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-12-24 | Initial Kairos-specific skill |
| 2.0 | 2025-12-26 | Complete rewrite: top-down architecture focus, "ServerRequest Is THE Way" principle, generalized from Kairos, WebApp bridge as platform pattern |
| 2.1 | 2025-12-27 | MVVMEnvironment is THE configuration holder for all clients (CLI, iOS, macOS, etc.) - not raw baseURL/headers. DRY principle enforcement. |
| 2.2 | 2025-12-27 | Added shared module pattern - SystemVersion.currentApplicationVersion from shared module, reference to FOSMVVMArchitecture.md |
| 2.3 | 2025-12-27 | Added `ServerRequestBodySize` for large upload body size limits (`maxBodySize` on RequestBody) |
| 2.4 | 2026-01-08 | Added controller action mapping table, testing section with reference to test generator skill |
| 2.5 | 2026-01-08 | Simplified action mapping: "action = protocol name minus Request". Removed drama, just state the pattern. |
| 2.6 | 2026-01-09 | Added ResponseError section with two patterns: associated values (LocalizableSubstitutions) and simple string codes (LocalizableString). Added YAML examples and built-in ValidationError usage. |
| 2.7 | 2026-01-20 | ResponseError MUST be nested inside request class (like RequestBody/ResponseBody). Updated patterns to show nesting with correct YAML key paths. |
| 2.8 | 2026-01-20 | Added "Type Safety Means You Already Know" section - explicit mental model that Swift's type system means you catch concrete error types, not protocols. Prevents JavaScript-brain panic about runtime type discovery. |
| 2.9 | 2026-01-24 | Update to context-aware approach (remove file-parsing/Q&A). Skill references conversation context instead of asking questions or accepting file paths. |
