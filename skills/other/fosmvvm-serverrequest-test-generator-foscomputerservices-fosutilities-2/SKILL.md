---
name: fosmvvm-serverrequest-test-generator
description: Generate comprehensive ServerRequest tests using VaporTesting infrastructure. Use when testing any ServerRequest type (ShowRequest, ViewModelRequest, CreateRequest, UpdateRequest, DeleteRequest) against a Vapor server.
---

# FOSMVVM ServerRequest Test Generator

Generate test files for ServerRequest types using VaporTesting infrastructure.

## Conceptual Foundation

> For full architecture context, see [FOSMVVMArchitecture.md](../../docs/FOSMVVMArchitecture.md)

ServerRequest testing uses **VaporTesting** infrastructure to send typed requests through the full server stack:

```
┌─────────────────────────────────────────────────────────────────────┐
│                    ServerRequest Test Flow                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Test Code:                                                          │
│    let request = MyRequest(query: .init(...))                        │
│    app.testing().test(request, locale: en) { response in }           │
│                                                                      │
│  Infrastructure handles:                                             │
│    • Path derivation from type name (MyRequest → /my)                │
│    • HTTP method from action (ShowRequest → GET)                     │
│    • Query/body encoding                                             │
│    • Header injection (locale, version)                              │
│    • Response decoding to ResponseBody type                          │
│                                                                      │
│  You verify:                                                         │
│    • response.status (HTTPStatus)                                    │
│    • response.body (R.ResponseBody? - typed!)                        │
│    • response.error (R.ResponseError? - typed!)                      │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## STOP AND READ THIS

**Testing ServerRequests uses VaporTesting infrastructure. No manual URL construction. Ever.**

```
┌──────────────────────────────────────────────────────────────────────┐
│          SERVERREQUEST TESTING USES TestingApplicationTester          │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  1. Configure Vapor Application with routes                           │
│  2. Use app.testing().test(request, locale:) { response in }          │
│  3. Verify response.status, response.body, response.error             │
│                                                                       │
│  TestingServerRequestResponse<R> provides TYPED access to:            │
│    • status: HTTPStatus                                               │
│    • headers: HTTPHeaders                                             │
│    • body: R.ResponseBody?     ← Auto-decoded!                        │
│    • error: R.ResponseError?   ← Auto-decoded!                        │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
```

### What You Must NEVER Do

```swift
// ❌ WRONG - manual URL construction
let url = URL(string: "http://localhost:8080/my_request?query=value")!
let response = try await URLSession.shared.data(from: url)

// ❌ WRONG - string path with method
try await app.test(.GET, "/my_request") { response in }

// ❌ WRONG - manual JSON encoding/decoding
let json = try JSONEncoder().encode(requestBody)
let decoded = try JSONDecoder().decode(ResponseBody.self, from: data)

// ❌ WRONG - constructing TestingHTTPRequest manually
let httpRequest = TestingHTTPRequest(method: .GET, url: "/path", headers: headers)
try await app.testing().performTest(request: httpRequest)
```

### What You Must ALWAYS Do

```swift
// ✅ RIGHT - Use TestingApplicationTester.test() with ServerRequest
let request = MyShowRequest(query: .init(userId: userId))
try await app.testing().test(request, locale: en) { response in
    #expect(response.status == .ok)
    #expect(response.body?.viewModel.name == "Expected Name")
}

// ✅ RIGHT - Test multiple locales
for locale in [en, es] {
    try await app.testing().test(request, locale: locale) { response in
        #expect(response.status == .ok)
        // Localized values are automatically handled
    }
}

// ✅ RIGHT - Test error responses
let badRequest = MyShowRequest(query: .init(userId: invalidId))
try await app.testing().test(badRequest, locale: en) { response in
    #expect(response.status == .notFound)
    #expect(response.error != nil)
}
```

**The path is derived from the ServerRequest type. HTTP method comes from the action. Headers are automatic. You NEVER write URL strings or decode JSON manually.**

---

## When to Use This Skill

- Testing any ServerRequest implementation
- Verifying server responses for CRUD operations
- Testing error handling and edge cases
- Multi-locale response verification
- Integration testing between client request types and server controllers

**If you're about to write `URLSession`, `app.test(.GET, "/path")`, or manual JSON decoding, STOP and use this skill instead.**

## What This Skill Generates

| File | Location | Purpose |
|------|----------|---------|
| `{Feature}RequestTests.swift` | `Tests/{Target}Tests/Requests/` | Test suite for ServerRequest |
| Test YAML (if needed) | `Tests/{Target}Tests/TestYAML/` | Localization for test ViewModels |

## Project Structure Configuration

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `{Feature}` | Feature or entity name (PascalCase) | `Idea`, `User`, `Dashboard` |
| `{Target}` | Server test target | `WebServerTests`, `AppTests` |
| `{ViewModelsTarget}` | Shared ViewModels SPM target | `ViewModels` |
| `{WebServerTarget}` | Server-side target | `WebServer`, `AppServer` |
| `{ResourceDir}` | YAML resource directory | `TestYAML`, `Resources` |

---

## Key Types

### TestingServerRequestResponse<R>

Wraps HTTP response with typed access:

| Property | Type | Description |
|----------|------|-------------|
| `status` | `HTTPStatus` | HTTP status code (.ok, .notFound, etc.) |
| `headers` | `HTTPHeaders` | Response headers |
| `body` | `R.ResponseBody?` | **Typed** response body (auto-decoded) |
| `error` | `R.ResponseError?` | **Typed** error (auto-decoded) |

### TestingApplicationTester Extension

```swift
func test<R: ServerRequest>(
    _ request: R,
    locale: Locale = en,
    headers: HTTPHeaders = [:],
    afterResponse: (TestingServerRequestResponse<R>) async throws -> Void
) async throws -> any TestingApplicationTester
```

### Convenience Locales

Available on `TestingApplicationTester`:
- `en` - English
- `enUS` - English (US)
- `enGB` - English (UK)
- `es` - Spanish

---

## Test Structure

### Basic Test Suite

```swift
import FOSFoundation
@testable import FOSMVVM
import FOSTesting
import FOSTestingVapor
import Foundation
import Testing
import Vapor
import VaporTesting

@Suite("MyFeature Request Tests")
struct MyFeatureRequestTests {
    @Test func showRequest_success() async throws {
        try await withTestApp { app in
            let request = MyShowRequest(query: .init(id: validId))

            try await app.testing().test(request, locale: en) { response in
                #expect(response.status == .ok)
                #expect(response.body?.viewModel != nil)
            }
        }
    }

    @Test func showRequest_notFound() async throws {
        try await withTestApp { app in
            let request = MyShowRequest(query: .init(id: invalidId))

            try await app.testing().test(request, locale: en) { response in
                #expect(response.status == .notFound)
            }
        }
    }
}

private func withTestApp(_ test: (Application) async throws -> Void) async throws {
    try await withApp { app in
        // Configure routes
        try app.routes.register(collection: MyController())
        try await test(app)
    }
}
```

### Testing Different Request Types

| Request Type | HTTP Method | What to Test |
|--------------|-------------|--------------|
| `ShowRequest` | GET | Query params, response body, localization |
| `ViewModelRequest` | GET | ViewModel population, all localized fields |
| `CreateRequest` | POST | RequestBody validation, created entity, ID response |
| `UpdateRequest` | PATCH | RequestBody validation, updated entity, response |
| `DeleteRequest` | DELETE | Entity removal, status code |

---

## How to Use This Skill

**Invocation:**
/fosmvvm-serverrequest-test-generator

**Prerequisites:**
- ServerRequest type understood from conversation context
- Test scenarios identified (success paths, error paths, validation)
- Controller implementation exists or is being created
- VaporTesting infrastructure understood

**Workflow integration:**
This skill is used when testing ServerRequest implementations. The skill references conversation context automatically—no file paths or Q&A needed. Typically follows fosmvvm-serverrequest-generator.

## Pattern Implementation

This skill references conversation context to determine test structure:

### Request Analysis

From conversation context, the skill identifies:
- **ServerRequest type** (from prior discussion or server implementation)
- **Request protocol** (ShowRequest, CreateRequest, UpdateRequest, etc.)
- **ResponseBody type** (ViewModel or simple structure)
- **ResponseError type** (custom errors or EmptyError)

### Test Scenario Planning

Based on operation semantics:
- **Success paths** (valid input, expected output)
- **Error paths** (not found, validation failure, business logic errors)
- **Localization** (if ResponseBody has localized fields)
- **Multi-locale** (testing across supported locales)

### Infrastructure Detection

From project state:
- **Existing test patterns** (similar test files in codebase)
- **Localization setup** (YAML fixtures needed)
- **Database requirements** (seed data for tests)

### Test File Generation

1. Test suite conforming to VaporTesting patterns
2. One @Test function per scenario
3. withTestApp helper for application setup
4. Route registration
5. Request invocations using app.testing().test()

### Context Sources

Skill references information from:
- **Prior conversation**: Test requirements, scenarios discussed
- **ServerRequest**: If Claude has read ServerRequest code into context
- **Controller**: From server implementation
- **Existing tests**: From codebase analysis of similar test files

---

## Common Scenarios

### Testing ViewModelRequest with Localization

```swift
@Test func viewModelRequest_multiLocale() async throws {
    try await withTestApp { app in
        let request = DashboardViewModelRequest()

        // Test English
        try await app.testing().test(request, locale: en) { response in
            #expect(response.status == .ok)
            let vm = try #require(response.body)
            #expect(try vm.pageTitle.localizedString == "Dashboard")
        }

        // Test Spanish
        try await app.testing().test(request, locale: es) { response in
            #expect(response.status == .ok)
            let vm = try #require(response.body)
            #expect(try vm.pageTitle.localizedString == "Tablero")
        }
    }
}
```

### Testing CreateRequest with Validation

```swift
@Test func createRequest_validInput() async throws {
    try await withTestApp { app in
        let request = CreateIdeaRequest(requestBody: .init(
            content: "Valid idea content"
        ))

        try await app.testing().test(request, locale: en) { response in
            #expect(response.status == .ok)
            #expect(response.body?.id != nil)
        }
    }
}

@Test func createRequest_invalidInput() async throws {
    try await withTestApp { app in
        let request = CreateIdeaRequest(requestBody: .init(
            content: ""  // Empty content should fail validation
        ))

        try await app.testing().test(request, locale: en) { response in
            #expect(response.status == .badRequest)
            #expect(response.error != nil)
        }
    }
}
```

### Testing UpdateRequest

```swift
@Test func updateRequest_success() async throws {
    try await withTestApp { app in
        // First create an entity
        let createRequest = CreateIdeaRequest(requestBody: .init(content: "Original"))
        var createdId: ModelIdType?
        try await app.testing().test(createRequest, locale: en) { response in
            createdId = response.body?.id
        }

        // Then update it
        let updateRequest = UpdateIdeaRequest(requestBody: .init(
            ideaId: try #require(createdId),
            content: "Updated content"
        ))

        try await app.testing().test(updateRequest, locale: en) { response in
            #expect(response.status == .ok)
            #expect(response.body?.viewModel.content == "Updated content")
        }
    }
}
```

### Testing DeleteRequest

```swift
@Test func deleteRequest_success() async throws {
    try await withTestApp { app in
        // Create, then delete
        let deleteRequest = DeleteIdeaRequest(requestBody: .init(ideaId: existingId))

        try await app.testing().test(deleteRequest, locale: en) { response in
            #expect(response.status == .ok)
        }

        // Verify deleted (should return not found)
        let showRequest = ShowIdeaRequest(query: .init(ideaId: existingId))
        try await app.testing().test(showRequest, locale: en) { response in
            #expect(response.status == .notFound)
        }
    }
}
```

### Testing ShowRequest with Query Parameters

```swift
@Test func showRequest_withQuery() async throws {
    try await withTestApp { app in
        let request = UserShowRequest(query: .init(
            userId: userId,
            includeDetails: true
        ))

        try await app.testing().test(request, locale: en) { response in
            #expect(response.status == .ok)
            #expect(response.body?.user.details != nil)
        }
    }
}
```

---

## Testing ServerRequestError Localizations

### Why Error Localization Testing is Different

Unlike ViewModels, `ServerRequestError` types:
- Are often **enums**, not structs
- Do **not** conform to `Stubbable` or `RetrievablePropertyNames`
- Cannot use `expectTranslations(ErrorType.self)` like ViewModels

This means you must **manually test each error case** individually.

### The Pattern

Use `LocalizableTestCase.expectTranslations(_ localizable:)` on each error's `Localizable` property:

```swift
@Suite("MyError Localization Tests")
struct MyErrorLocalizationTests: LocalizableTestCase {
    let locStore: LocalizationStore

    init() throws {
        self.locStore = try Self.loadLocalizationStore(
            bundle: Bundle.module,
            resourceDirectoryName: "TestYAML"
        )
    }

    @Test func errorMessages_simpleErrors() throws {
        // Test each error case individually
        let serverFailed = MyError(code: .serverFailed)
        try expectTranslations(serverFailed.message)

        let appFailed = MyError(code: .applicationFailed)
        try expectTranslations(appFailed.message)
    }

    @Test func errorMessages_withSubstitutions() throws {
        // For errors with associated values, test with representative values
        let quotaError = QuotaError(code: .quotaExceeded(requested: 100, maximum: 50))
        try expectTranslations(quotaError.message)
    }
}
```

### Testing Error Messages in Integration Tests

When testing the full request/response cycle, verify error messages resolve:

```swift
@Test func createRequest_validationError_hasLocalizedMessage() async throws {
    try await withTestApp { app in
        let request = CreateIdeaRequest(requestBody: .init(content: ""))

        try await app.testing().test(request, locale: en) { response in
            #expect(response.status == .badRequest)
            let error = try #require(response.error)

            // Verify the message resolved (not empty or pending)
            #expect(!error.message.isEmpty)

            // Optionally verify specific text for English locale
            #expect(try error.message.localizedString.contains("required"))
        }
    }
}
```

### Why Not Stubbable?

`Stubbable` works well for ViewModels because:
- ViewModels are structs with many properties
- A single `stub()` provides a complete test instance

`ServerRequestError` types are often enums where:
- Each case may have different associated values
- Each case may have a different localized message
- A single `stub()` can't cover all cases

**You must enumerate and test each error case explicitly.**

### Checklist for Error Localization Tests

- [ ] Test each enum case for simple errors
- [ ] Test representative associated values for parameterized errors
- [ ] Verify messages resolve (not empty) for all configured locales
- [ ] Verify substitution placeholders are replaced in `LocalizableSubstitutions`

---

## Troubleshooting

### "Route not found" Error

**Cause:** Controller not registered in test app.

**Fix:** Register the controller before testing:
```swift
try app.routes.register(collection: MyController())
```

### Response body is nil but status is .ok

**Cause:** JSON decoding failed silently.

**Fix:** Check that `ResponseBody` type matches server response exactly. Use `response.headers` to verify Content-Type.

### Localization not applied

**Cause:** Locale not passed to encoder.

**Fix:** The `test(_:locale:)` method handles this automatically. Ensure you're passing the locale parameter.

### "Missing Translation" in Response

**Cause:** YAML localization not loaded.

**Fix:** Initialize localization store in test app setup:
```swift
try app.initYamlLocalization(
    bundle: Bundle.module,
    resourceDirectoryName: "TestYAML"
)
```

---

## Naming Conventions

| Concept | Convention | Example |
|---------|------------|---------|
| Test suite | `{Feature}RequestTests` | `IdeaRequestTests` |
| Test file | `{Feature}RequestTests.swift` | `IdeaRequestTests.swift` |
| Test method (success) | `{action}Request_success` | `showRequest_success` |
| Test method (error) | `{action}Request_{errorCase}` | `showRequest_notFound` |
| Test method (validation) | `{action}Request_{validationCase}` | `createRequest_emptyContent` |
| Test helper | `withTestApp` | `withTestApp { app in }` |
| Locale constant | `en`, `es`, `enUS`, `enGB` | `locale: en` |

---

---

## File Templates

See [reference.md](reference.md) for complete file templates.

---

## See Also

- [FOSMVVMArchitecture.md](../../docs/FOSMVVMArchitecture.md) - Full architecture
- [fosmvvm-serverrequest-generator](../fosmvvm-serverrequest-generator/SKILL.md) - Creating ServerRequest types
- [fosmvvm-viewmodel-test-generator](../fosmvvm-viewmodel-test-generator/SKILL.md) - Testing ViewModels (localization only)
- [reference.md](reference.md) - Complete file templates

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.1 | 2025-01-20 | Add ServerRequestError localization testing guidance |
| 1.2 | 2026-01-24 | Update to context-aware approach (remove file-parsing/Q&A). Skill references conversation context instead of asking questions or accepting file paths. |
| 1.0 | 2025-01-05 | Initial skill |
