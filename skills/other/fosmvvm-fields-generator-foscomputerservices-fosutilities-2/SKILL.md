---
name: fosmvvm-fields-generator
description: Generate FOSMVVM Form Specifications (Fields protocols) with validation and localization. Use when defining user input contracts for forms, request bodies, or any ValidatableModel.
---

# FOSMVVM Fields Generator

Generate Form Specifications following FOSMVVM patterns.

## Conceptual Foundation

> For full architecture context, see [FOSMVVMArchitecture.md](../../docs/FOSMVVMArchitecture.md)

A **Form Specification** (implemented as a `{Name}Fields` protocol) is the **single source of truth** for user input. It answers:

1. **What data** can the user provide? (properties)
2. **How should it be presented?** (FormField with type, keyboard, autofill semantics)
3. **What constraints apply?** (validation rules)
4. **What messages should be shown?** (localized titles, placeholders, errors)

### Why This Matters

The Form Specification is **defined once, used everywhere**:

```swift
// Same protocol adopted by different consumers:
struct CreateIdeaRequestBody: ServerRequestBody, IdeaFields { ... }  // HTTP transmission
@ViewModel struct IdeaFormViewModel: IdeaFields { ... }              // Form rendering
final class Idea: Model, IdeaFields { ... }                          // Persistence validation
```

This ensures:
- **Consistent validation** - Same rules on client and server
- **Shared localization** - One YAML file, used everywhere
- **Single source of truth** - Change once, applies everywhere

### Connection to FOSMVVM

Form Specifications integrate with:
- **Localization System** - FormField titles/placeholders and validation messages use `LocalizableString`
- **Validation System** - Implements `ValidatableModel` protocol
- **Request System** - RequestBody types adopt Fields for validated transmission
- **ViewModel System** - ViewModels adopt Fields for form rendering

## When to Use This Skill

- Defining a new form (create, edit, filter, search)
- Adding validation to a request body
- Any type that needs to conform to `ValidatableModel`
- When `fosmvvm-fluent-datamodel-generator` needs form fields for a DataModel

## What This Skill Generates

A complete Form Specification consists of **3 files**:

| File | Purpose |
|------|---------|
| `{Name}Fields.swift` | Protocol + FormField definitions + validation methods |
| `{Name}FieldsMessages.swift` | `@FieldValidationModel` struct with `@LocalizedString` properties |
| `{Name}FieldsMessages.yml` | YAML localization (titles, placeholders, error messages) |

## Project Structure Configuration

Replace placeholders with your project's actual paths:

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `{ViewModelsTarget}` | Shared ViewModels SPM target | `ViewModels`, `SharedViewModels` |
| `{ResourcesPath}` | Localization resources path | `Sources/Resources` |

**Expected Structure:**
```
Sources/
  {ViewModelsTarget}/
    FieldModels/
      {Name}Fields.swift
      {Name}FieldsMessages.swift
  {ResourcesPath}/
    FieldModels/
      {Name}FieldsMessages.yml
```

## How to Use This Skill

**Invocation:**
/fosmvvm-fields-generator

**Prerequisites:**
- Form purpose understood from conversation context
- Field requirements discussed (names, types, constraints)
- Entity relationship identified (what is this form creating/editing)

**Workflow integration:**
This skill is used when defining form validation and user input contracts. The skill references conversation context automatically—no file paths or Q&A needed. Often precedes fosmvvm-fluent-datamodel-generator for form-backed models.

## Pattern Implementation

This skill references conversation context to determine Fields protocol structure:

### Form Analysis

From conversation context, the skill identifies:
- **Form purpose** (create, edit, filter, login, settings)
- **Entity relation** (User, Idea, Document - what's being created/edited)
- **Protocol naming** (CreateIdeaFields, UpdateProfile, LoginCredentials)

### Field Design

For each field from requirements:
- **Property specification** (name, type, optional vs required)
- **Presentation type** (FormFieldType: text, textArea, select, checkbox)
- **Input semantics** (FormInputType: email, password, tel, date)
- **Constraints** (required, length range, value range, date range)
- **Localization** (title, placeholder, validation error messages)

### File Generation Order

1. Fields protocol with FormField definitions and validation
2. FieldsMessages struct with @LocalizedString properties
3. FieldsMessages YAML with localized strings

### Context Sources

Skill references information from:
- **Prior conversation**: Form requirements, field specifications discussed
- **Specification files**: If Claude has read form specs into context
- **Existing patterns**: From codebase analysis of similar Fields protocols

## Key Patterns

### Protocol Structure

```swift
public protocol {Name}Fields: ValidatableModel, Codable, Sendable {
    var fieldName: FieldType { get set }
    var {name}ValidationMessages: {Name}FieldsMessages { get }
}
```

### FormField Definition

```swift
static var contentField: FormField<String?> { .init(
    fieldId: .init(id: "content"),
    title: .localized(for: {Name}FieldsMessages.self, propertyName: "content", messageKey: "title"),
    placeholder: .localized(for: {Name}FieldsMessages.self, propertyName: "content", messageKey: "placeholder"),
    type: .textArea(inputType: .text),
    options: [
        .required(value: true)
    ] + FormInputOption.rangeLength(contentRange)
) }
```

### FormField Types Reference

| FormFieldType | Use Case |
|---------------|----------|
| `.text(inputType:)` | Single-line input |
| `.textArea(inputType:)` | Multi-line input |
| `.checkbox` | Boolean toggle |
| `.select` | Dropdown selection |
| `.colorPicker` | Color selection |

### FormInputType Reference (common ones)

| FormInputType | Keyboard/Autofill |
|---------------|-------------------|
| `.text` | Default keyboard |
| `.emailAddress` | Email keyboard, email autofill |
| `.password` | Secure entry |
| `.tel` | Phone keyboard |
| `.url` | URL keyboard |
| `.date`, `.datetimeLocal` | Date picker |
| `.givenName`, `.familyName` | Name autofill |

### Validation Method Pattern

```swift
internal func validateContent(_ fields: [FormFieldBase]?) -> [ValidationResult]? {
    guard fields == nil || (fields?.contains(Self.contentField) == true) else {
        return nil
    }

    var result = [ValidationResult]()

    if content.isEmpty {
        result.append(.init(
            status: .error,
            field: Self.contentField,
            message: {name}ValidationMessages.contentRequiredMessage
        ))
    } else if !Self.contentRange.contains(NSString(string: content).length) {
        result.append(.init(
            status: .error,
            field: Self.contentField,
            message: {name}ValidationMessages.contentOutOfRangeMessage
        ))
    }

    return result.isEmpty ? nil : result
}
```

### Messages Struct Pattern

```swift
@FieldValidationModel public struct {Name}FieldsMessages {
    @LocalizedString("content", messageGroup: "validationMessages", messageKey: "required")
    public var contentRequiredMessage

    @LocalizedString("content", messageGroup: "validationMessages", messageKey: "outOfRange")
    public var contentOutOfRangeMessage
}
```

### YAML Structure

```yaml
en:
  {Name}FieldsMessages:
    content:
      title: "Content"
      placeholder: "Enter your content..."
      validationMessages:
        required: "Content is required"
        outOfRange: "Content must be between 1 and 10,000 characters"
```

## Naming Conventions

| Concept | Convention | Example |
|---------|------------|---------|
| Protocol | `{Name}Fields` | `IdeaFields`, `CreateIdeaFields` |
| Messages struct | `{Name}FieldsMessages` | `IdeaFieldsMessages` |
| Messages property | `{name}ValidationMessages` | `ideaValidationMessages` |
| Field definition | `{fieldName}Field` | `contentField` |
| Range constant | `{fieldName}Range` | `contentRange` |
| Validate method | `validate{FieldName}` | `validateContent` |
| Required message | `{fieldName}RequiredMessage` | `contentRequiredMessage` |
| OutOfRange message | `{fieldName}OutOfRangeMessage` | `contentOutOfRangeMessage` |

## See Also

- [FOSMVVMArchitecture.md](../../docs/FOSMVVMArchitecture.md) - Full FOSMVVM architecture reference
- [fosmvvm-viewmodel-generator](../fosmvvm-viewmodel-generator/SKILL.md) - For ViewModels that adopt Fields
- [fosmvvm-fluent-datamodel-generator](../fosmvvm-fluent-datamodel-generator/SKILL.md) - For Fluent DataModels that implement Fields
- [reference.md](reference.md) - Complete file templates

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-12-24 | Initial skill |
| 2.0 | 2024-12-26 | Rewritten with conceptual foundation; generalized from Kairos-specific |
| 2.1 | 2026-01-24 | Update to context-aware approach (remove file-parsing/Q&A). Skill references conversation context instead of asking questions or accepting file paths. |
