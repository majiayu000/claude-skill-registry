---
name: fosmvvm-fluent-datamodel-generator
description: Generate Fluent DataModels for FOSMVVM server-side persistence. Use when creating new database-backed entities, adding tables, or when the user mentions adding Models like Users, Ideas, Documents, etc. Uses fosmvvm-fields-generator for the Fields layer, then generates Fluent DataModel, migrations, and tests.
---

# FOSMVVM Fluent DataModel Generator

Generate Fluent DataModels for server-side persistence following FOSMVVM architecture.

> **Dependency:** This skill uses [fosmvvm-fields-generator](../fosmvvm-fields-generator/SKILL.md) for the Fields layer (protocol, messages, YAML). Run that skill first for form-backed models.

## Scope Guard

This skill is specifically for **Fluent** persistence layer (typically in Vapor server apps).

**STOP and ask the user if:**
- The project doesn't use Fluent
- The target is iOS-only with CoreData, SwiftData, or Realm
- The user mentions a non-Fluent ORM or persistence layer
- You're unsure whether Fluent is the persistence layer

**Check for Fluent indicators:**
- `Package.swift` imports `fluent`, `fluent-postgres-driver`, `fluent-sqlite-driver`, etc.
- Existing models use `@ID`, `@Field`, `@Parent`, `@Children`, `@Siblings` property wrappers
- A `Migrations/` directory exists with Fluent migration patterns
- Imports include `FluentKit` or `Fluent`

If Fluent isn't present, inform the user: *"This skill generates Fluent DataModels for server-side persistence. Your project doesn't appear to use Fluent. How would you like to proceed?"*

---

## When to Use This Skill

- User asks to create a new model/entity/table
- User wants to add a database-backed type (Users, Ideas, Documents, etc.)
- User mentions needing CRUD operations for a new concept
- Creating the persistence layer for a new entity

## Architecture Context

In FOSMVVM, the **Model** is the center - the source of truth that reads and writes flow through.

See [FOSMVVMArchitecture.md](../../docs/FOSMVVMArchitecture.md) for full context.

### DataModel in the Architecture

```
                    ┌─────────────────────────────────────┐
                    │         Fluent DataModel            │
                    │    (implements Model + Fields)      │
                    │                                     │
                    │  • All fields (system + user)       │
                    │  • Relationships (@Parent, etc.)    │
                    │  • Timestamps, audit fields         │
                    │  • Persistence logic                │
                    └──────────────┬──────────────────────┘
                                   │
              ┌────────────────────┼────────────────────────┐
              │                    │                        │
              ▼                    ▼                        ▼
    ┌─────────────────┐  ┌─────────────────┐    ┌─────────────────┐
    │ ViewModelFactory│  │  CreateRequest  │    │  UpdateRequest  │
    │   (projector)   │  │   RequestBody   │    │   RequestBody   │
    │                 │  │                 │    │                 │
    │ → ViewModel     │  │ → persists to   │    │ → updates       │
    │   (projection)  │  │   DataModel     │    │   DataModel     │
    └─────────────────┘  └─────────────────┘    └─────────────────┘
```

### Fields vs DataModels

**Fields protocol** = Form input (user-editable subset)
- What users type into forms
- Validation, labels, placeholders
- NO relationships, NO system-assigned fields

**DataModel** = Complete entity (Fluent implementation)
- All fields including system-assigned (createdBy, timestamps)
- All relationships (@Parent, @Siblings, @Children)
- Fluent property wrappers, migrations, seeds

**Not all entities need Fields:**
- Session: system auth, no user form → DataModel-only
- Audit records: system-generated → DataModel-only
- Junction tables: pure storage → DataModel-only

---

## File Structure

Each form-backed model requires files across multiple targets:

```
── fosmvvm-fields-generator ──────────────────────────────────
{ViewModelsTarget}/                  (shared protocol layer)
  FieldModels/
    {Model}Fields.swift              ← Protocol + Enum + Validation
    {Model}FieldsMessages.swift      ← Localization message struct

{ResourcesPath}/                     (localization resources)
  FieldModels/
    {Model}FieldsMessages.yml        ← YAML localization strings

── fosmvvm-fluent-datamodel-generator (this skill) ───────────
{WebServerTarget}/                   (server implementation)
  DataModels/
    {Model}.swift                    ← Fluent model (implements protocol)
  Migrations/
    {Model}+Schema.swift             ← Table creation migration
    {Model}+Seed.swift               ← Seed data migration

Tests/
  {ViewModelsTarget}Tests/
    FieldModels/
      {Model}FieldsTests.swift       ← Unit tests

database.swift                       ← Register migrations
```

---

## Generation Process

### Step 1: Gather Requirements

Before generating, ask/confirm:
1. **Model name** (singular, PascalCase): e.g., `User`, `Idea`, `Document`
2. **Fields** with types and constraints
3. **Enums** for constrained string fields
4. **Relationships** to other models (foreign keys)
5. **Seed data** requirements (debug vs test environments)

### Step 2: Design Checkpoint

Before generating files, explicitly confirm:

1. **Is this a form?** If no user input, skip Fields entirely.
   - System-generated entities (Session, audit records) → DataModel-only
   - Junction tables → DataModel-only, no Fields

2. **Relationships?**
   - One-to-many: `@Parent` in DataModel only, not in Fields
   - Many-to-many: Junction table + `@Siblings`, NEVER UUID arrays

3. **System-assigned fields?** (createdBy, timestamps, status history)
   - These go in DataModel only, not Fields

4. **Clear naming?** Relationship names must be self-documenting.
   - Bad: `sourceNodes` (what sources? what nodes?)
   - Good: `originatingConversations` (clear relationship meaning)

Get explicit approval before generating.

### Step 3: Generate Files in Order

Generate files in this order (dependencies flow down):

**If form-backed model, run fosmvvm-fields-generator first:**
1. `{Model}Fields.swift` - Protocol defines the contract *(via fosmvvm-fields-generator)*
2. `{Model}FieldsMessages.swift` - Validation message struct *(via fosmvvm-fields-generator)*
3. `{Model}FieldsMessages.yml` - Localization strings *(via fosmvvm-fields-generator)*

**Then generate DataModel layer (this skill):**
4. `{Model}.swift` - Fluent model implementation
5. `{Model}+Schema.swift` - Database migration
6. `{Model}+Seed.swift` - Seed data
7. `{Model}FieldsTests.swift` - Tests
8. Update `database.swift` - Register migrations

### Step 4: Verify

After generation:
1. Run `swiftformat .` to add file headers and format code
2. Run `swiftlint` to verify lint rules are upheld
3. Run `swift build` to verify compilation
4. Run `swift test` to verify tests pass
5. Run migrations: server will auto-migrate on startup

---

## File Templates

See [reference.md](reference.md) for complete file templates with all patterns.

---

## Key Patterns

### Fluent DataModel

```swift
import FluentKit
import FOSFoundation
import FOSMVVM
import FOSMVVMVapor
import Foundation

final class {Model}: DataModel, {Model}Fields, Hashable, @unchecked Sendable {
    static let schema = "{models}"  // snake_case plural

    @ID(key: .id) var id: ModelIdType?

    // Fields from protocol
    @Field(key: "field_name") var fieldName: FieldType

    // Validation messages
    let {model}ValidationMessages: {Model}FieldsMessages

    // Timestamps
    @Timestamp(key: "created_at", on: .create) var createdAt: Date?
    @Timestamp(key: "updated_at", on: .update) var updatedAt: Date?

    // CRITICAL: Initialize validationMessages FIRST
    init() {
        self.{model}ValidationMessages = .init()
    }

    init(id: ModelIdType? = nil, fieldName: FieldType) {
        self.{model}ValidationMessages = .init()  // FIRST!
        self.id = id
        self.fieldName = fieldName
    }
}
```

### Relationships (Associated Types Pattern)

**PRINCIPLE: Existential types (`any Protocol`) are a code smell.** Always ask "Is there any other way?" before using them.

For required relationships, use **associated types** in the protocol:

```swift
public protocol IdeaFields: ValidatableModel, Codable, Sendable {
    associatedtype User: UserFields

    var createdBy: User { get set }
}
```

In the Fluent model, `@Parent` directly satisfies the protocol:

```swift
final class Idea: DataModel, IdeaFields, Hashable, @unchecked Sendable {
    @Parent(key: "created_by") var createdBy: User
    // No computed property needed - @Parent satisfies the associated type directly
}
```

In schema: `.field("created_by", .uuid, .required, .references(User.schema, "id", onDelete: .cascade))`

**When to use each pattern:**
- **Associated type** (`associatedtype User: UserFields`): Required relationships
- **Optional associated type**: Not supported - use `ModelIdType?` for optional FKs
- **Plain `ModelIdType`**: Optional FKs, external system references

### Migrations

- Schema migration named: `"{Model.schema}-initial"`
- Seed migration named: `"{Model.schema}-seed"`
- Seed is environment-aware (debug, test, release)
- Seed is idempotent: `guard count() == 0`

### Raw SQL in Migrations (PostgreSQL Features)

For PostgreSQL-specific features (tsvector, LTREE, etc.), use SQLKit:

```swift
import Fluent
import SQLKit  // Required for raw SQL

// In prepare():
guard let sql = database as? any SQLDatabase else { return }

let schema = Model.schema
try await sql.raw(SQLQueryString("ALTER TABLE \(unsafeRaw: schema) ADD COLUMN search_vector tsvector")).run()
```

Key points:
- Import `SQLKit` (not just `Fluent`)
- Cast database: `database as? any SQLDatabase`
- Use `SQLQueryString` with `\(unsafeRaw:)` for identifiers
- These columns are database-only (not in protocol or Fluent model)

### Tests

- Use `@Suite` annotation with descriptive name
- Conform to `LocalizableTestCase`
- Test all form fields
- Test validation with `@Test(arguments:)`
- Create private test struct implementing the Fields protocol

**Test structs with associated types:**

```swift
private struct TestIdea: IdeaFields {
    typealias User = TestUser  // Satisfy the associated type

    var id: ModelIdType?
    var createdBy: TestUser    // Concrete type, not existential
}

private struct TestUser: UserFields {
    var id: ModelIdType? = .init()
    var firstName: String = "Test"
    // ... other required fields with defaults
}
```

---

## Naming Conventions

| Concept | Convention | Example |
|---------|------------|---------|
| Model class | PascalCase singular | `User`, `Idea` |
| Table name | snake_case plural | `users`, `ideas` |
| Field keys | snake_case | `created_at`, `user_id` |
| Enum cases | camelCase | `searchLanguage`, `inProgress` |
| Enum raw values | snake_case | `"search_language"`, `"in_progress"` |
| Protocol | `{Model}Fields` | `UserFields`, `IdeaFields` |
| Messages struct | `{Model}FieldsMessages` | `UserFieldsMessages` |

## Common Field Types

| Swift Type | Fluent Type | Database |
|------------|-------------|----------|
| `String` | `.string` | `VARCHAR/TEXT` |
| `Int` | `.int` | `INTEGER` |
| `Bool` | `.bool` | `BOOLEAN` |
| `Date` | `.datetime` | `TIMESTAMPTZ` |
| `UUID` | `.uuid` | `UUID` |
| `[UUID]` | `.array(of: .uuid)` | `UUID[]` |
| Custom Enum | `.string` | `VARCHAR` (stored as raw value) |
| `JSONB` | `.json` | `JSONB` |

---

## Collaboration Protocol

**IMPORTANT**: Work WITH the user, not ahead of them:

1. Show the proposed file structure first
2. Generate one file at a time, getting feedback
3. Let the user review/modify patterns as needed
4. Don't assume - ask when uncertain
5. The user's patterns may differ from examples - learn from their code

---

## See Also

- [FOSMVVMArchitecture.md](../../docs/FOSMVVMArchitecture.md) - Full FOSMVVM architecture
- [fosmvvm-fields-generator](../fosmvvm-fields-generator/SKILL.md) - For form validation (Fields protocols)
- [fosmvvm-viewmodel-generator](../fosmvvm-viewmodel-generator/SKILL.md) - For ViewModels that project from DataModels
- [reference.md](reference.md) - Complete file templates

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-12-23 | Initial skill based on SystemConfig pattern |
| 1.1 | 2025-12-23 | Added relationship patterns (@Parent), initialization order, imports list |
| 1.2 | 2025-12-23 | Associated types for relationships (not existentials), raw SQL patterns, test struct patterns |
| 1.3 | 2025-12-24 | Factored out Fields layer to fields-generator skill |
| 2.0 | 2025-12-26 | Renamed to fosmvvm-fluent-datamodel-generator, added Scope Guard, generalized from Kairos-specific to FOSMVVM patterns, added architecture context |
