---
name: manage-fake
description: Create or update Fake test doubles for TypeScript interfaces. Use when user asks to "create a fake", "update a fake", "generate test fake", "fix fake", "manage fake", or mentions needing a fake for testing. Generates Initializer interface, Fake class, and Builder class following the testing pattern with getMockingFunction, FakeEntity inheritance, and EventBroker support.
---

# Manage Fake Skill

This skill helps you create or update a Fake class for testing purposes. Fakes are test doubles that implement interfaces with configurable behavior.

## When to Use This Skill

Use this skill when you need to:
- **Create** a new Fake implementation for testing an interface
- **Update** an existing Fake to match interface changes

The skill will generate/update:
- A Fake class that implements the interface
- An Initializer interface for required parameters
- A Builder class for easy test instantiation

## Usage

Invoke this skill when the user asks to:
- "Create a fake for [InterfaceName]"
- "Generate a test fake for [InterfaceName]"
- "I need a fake [InterfaceName]"
- "Update the fake for [InterfaceName]"
- "The [InterfaceName] interface changed, update its fake"
- "Fix the Fake[ClassName] to match the interface"

## Prerequisites

Before creating/updating a fake:
1. **Verify the interface exists** - The interface you're faking must already be defined
2. **Check for existing fake** - Use Glob to search for existing `Fake[ClassName]` files
3. **Identify if interface extends IEntity** - This affects the pattern used

## Create vs Update Decision

**If fake file exists:** Update mode
- Read the existing fake file
- Read the interface definition
- Compare and identify differences
- Update the fake to match the interface

**If fake file does NOT exist:** Create mode
- Read the interface definition
- Generate all three components from scratch

## Naming Convention

For an interface named `IMyClass`, create:
- File: `FakeMyClass.ts`
- Initializer: `FakeMyClassInitializer`
- Fake class: `FakeMyClass`
- Builder class: `FakeMyClassBuilder`

**Pattern:** Remove the `I` prefix from the interface name and add `Fake` prefix.

## Required Imports

```typescript
import { getMockingFunction } from '@zdr-tools/zdr-testing-tools';
import { FakeEntity, FakeEntityBuilder, FakesFactory, type IFakeEntityInitialData } from '@zdr-tools/zdr-entities/fakes';
import type { IEntity, IPropEventBroker, IReadablePropEventBroker, IEntityCollection, IOrderedEntityCollection, IRestorablePropEventBroker } from '@zdr-tools/zdr-entities';
```

## Structure

### 1. Initializer Interface

**Purpose:** Defines all required parameters for creating the fake.

**Rules:**
- All fields are MANDATORY (no optional fields with `?`)
- One field per interface field
- One field per interface method (for return values only, named `[methodName]ReturnValue`)

**Standard Pattern:**
```typescript
export interface FakeMyClassInitializer {
  someField: string;
  anotherField: number;
  someMethodReturnValue: boolean;
}
```

**If interface extends IEntity:**
```typescript
export interface FakeMyClassInitializer extends IFakeEntityInitialData {
  someField: string;
  anotherField: number;
  someMethodReturnValue: boolean;
}
```

### 2. Fake Class

**Purpose:** The actual fake implementation of the interface.

**Standard Pattern:**
```typescript
export class FakeMyClass implements IMyClass {
  public someField: string;
  public anotherField: number;

  constructor(private fakeMyClassInitialData: FakeMyClassInitializer) {
    this.someField = fakeMyClassInitialData.someField;
    this.anotherField = fakeMyClassInitialData.anotherField;
  }

  someMethod = getMockingFunction<(arg: string) => boolean>(() => {
    return this.fakeMyClassInitialData.someMethodReturnValue;
  });
}
```

**If interface extends IEntity:**
```typescript
export class FakeMyClass extends FakeEntity implements IMyClass {
  public someField: string;
  public anotherField: number;

  constructor(private fakeMyClassInitialData: FakeMyClassInitializer) {
    super(fakeMyClassInitialData);

    this.someField = fakeMyClassInitialData.someField;
    this.anotherField = fakeMyClassInitialData.anotherField;
  }

  someMethod = getMockingFunction<(arg: string) => boolean>(() => {
    return this.fakeMyClassInitialData.someMethodReturnValue;
  });
}
```

**Method Implementation Rules:**
- Use `getMockingFunction` to wrap methods
- Generic type matches the method signature
- Return value comes from `[methodName]ReturnValue` field in initializer
- Method arguments are NOT stored in initializer, only return values

### 3. Builder Class

**Purpose:** Provides a fluent API for creating fakes with sensible defaults.

**Standard Pattern:**
```typescript
export class FakeMyClassBuilder {
  private someField: string = '';
  private anotherField: number = 0;
  private someMethodReturnValue: boolean = false;

  withSomeField(value: string): this {
    this.someField = value;
    return this;
  }

  withAnotherField(value: number): this {
    this.anotherField = value;
    return this;
  }

  withSomeMethodReturnValue(value: boolean): this {
    this.someMethodReturnValue = value;
    return this;
  }

  protected getFakeMyClassInitializer(): FakeMyClassInitializer {
    return {
      someField: this.someField,
      anotherField: this.anotherField,
      someMethodReturnValue: this.someMethodReturnValue,
    };
  }

  build(): FakeMyClass {
    return new FakeMyClass(this.getFakeMyClassInitializer());
  }
}
```

**If interface extends IEntity:**
```typescript
export class FakeMyClassBuilder extends FakeEntityBuilder {
  private someField: string = '';
  private anotherField: number = 0;
  private someMethodReturnValue: boolean = false;

  withSomeField(value: string): this {
    this.someField = value;
    return this;
  }

  withAnotherField(value: number): this {
    this.anotherField = value;
    return this;
  }

  withSomeMethodReturnValue(value: boolean): this {
    this.someMethodReturnValue = value;
    return this;
  }

  protected getFakeMyClassInitializer(): FakeMyClassInitializer {
    return {
      ...this.getInitialData(), // From FakeEntityBuilder
      someField: this.someField,
      anotherField: this.anotherField,
      someMethodReturnValue: this.someMethodReturnValue,
    };
  }

  build(): FakeMyClass {
    return new FakeMyClass(this.getFakeMyClassInitializer());
  }
}
```

## Default Values for Builder Fields

Use these default values for different field types:

| Type | Default Value |
|------|---------------|
| Fields that can be undefined | `undefined` |
| `string` | `''` |
| `number` | `0` |
| `boolean` | `false` |
| `IReadablePropEventBroker<T>` | `FakesFactory.createReadablePropEventBroker<T>(defaultValueForT)` |
| `IPropEventBroker<T>` | `FakesFactory.createPropEventBroker<T>(defaultValueForT)` |
| `IRestorablePropEventBroker<T>` | `FakesFactory.createFakeRestorablePropEventBroker<T>(defaultValueForT)` |
| `IEntityCollection<T>` | `FakesFactory.createEntityCollection<T>([])` |
| `IOrderedEntityCollection<T>` | `FakesFactory.createOrderedEntityCollection<T>([])` |
| Entity/Model types | `new Fake[EntityName]Builder().build()` |

## EventBroker Special Handling

For EventBroker fields, create TWO "with" methods:

```typescript
// Field definition
private name: IPropEventBroker<string> = FakesFactory.createPropEventBroker<string>('');

// Method 1: Accept the full EventBroker
withName(value: IPropEventBroker<string>): this {
  this.name = value;
  return this;
}

// Method 2: Accept just the value (convenience method)
withNameValue(value: string): this {
  return this.withName(FakesFactory.createPropEventBroker<string>(value));
}
```

## File Location and Export Structure

**IMPORTANT**: All fakes MUST be organized in a `/fakes` folder at the package root level (sibling to `/src`):

### Directory Structure
```
packages/
  my-package/
    src/
      IMyClass.ts        # Interface definitions
      MyClass.ts
    fakes/               # Sibling to src, NOT inside src
      index.ts           # Exports all fakes
      FakeMyClass.ts     # Fake implementation
      FakeOtherClass.ts
```

### Rules
1. **Fakes folder location**: Always create fakes in `/fakes/` at the package root (sibling to `/src`)
   - If interface is in `packages/my-package/src/IMyClass.ts`
   - Create fake in `packages/my-package/fakes/FakeMyClass.ts` (NOT in `src/fakes/`)

2. **Index file**: The `/fakes` folder MUST contain an `index.ts` file that exports all fakes
   - If `index.ts` doesn't exist, create it
   - Export pattern: `export * from './FakeMyClass';`

3. **After creating/updating a fake**: Always add/verify the export in `/fakes/index.ts`

### Example index.ts
```typescript
// fakes/index.ts (at package root, sibling to src/)
export * from './FakeReport';
export * from './FakeUser';
export * from './FakeWorkspace';
```

## Workflow

### Create Workflow (No existing fake)

1. **Identify the interface** - Ask user which interface to fake if not clear
2. **Locate the interface file** - Use Glob to find the interface definition
3. **Read the interface** - Get all fields and methods
4. **Check if interface extends IEntity** - This affects the pattern used
5. **Ensure `/fakes` folder exists** - Check if `/fakes/` directory exists at package root (sibling to `/src`), create if needed
6. **Create the fake file** in `/fakes/FakeMyClass.ts` with all three components:
   - Initializer interface
   - Fake class
   - Builder class
7. **Update the exports index**:
   - Check if `/fakes/index.ts` exists, create if it doesn't
   - Add export line: `export * from './FakeMyClass';`
   - Keep exports alphabetically sorted

### Update Workflow (Fake exists)

1. **Identify the interface and fake** - Determine which interface/fake to update
2. **Read both files**:
   - Read the interface definition
   - Read the existing fake file
3. **Compare and identify changes**:
   - **Added fields** - Add to initializer, fake class constructor, and builder (with default value and `with*` method)
   - **Removed fields** - Remove from all three components
   - **Changed field types** - Update type in all three components and adjust default value in builder
   - **Added methods** - Add `[methodName]ReturnValue` to initializer, add method implementation in fake class with `getMockingFunction`, add field and `with*` method to builder
   - **Removed methods** - Remove `[methodName]ReturnValue` and all related code
   - **Changed method signatures** - Update the generic type in `getMockingFunction` and the return value type
4. **Apply updates using Edit tool**:
   - Update the Initializer interface
   - Update the Fake class fields, constructor, and methods
   - Update the Builder class fields, `with*` methods, and the protected getter method
5. **Verify completeness** - Ensure all interface members are represented in the fake

### Update Guidelines

When updating an existing fake:
- **Preserve existing structure** - Don't rewrite the entire file, use Edit tool for targeted changes
- **Maintain consistency** - Follow the same patterns used in the existing fake
- **Keep default values sensible** - When adding new builder fields, use appropriate defaults from the table below
- **Handle EventBrokers correctly** - If adding an EventBroker field, remember to create BOTH `with*` methods
- **Check inheritance** - If the interface extends IEntity and the fake doesn't extend FakeEntity, this is a structural change that may require a larger refactor

## Common Update Scenarios

### Scenario 1: Adding a New Field

**Interface change:**
```typescript
export interface IReport extends IEntity {
  title: string;
  status: string;
  description: string; // NEW FIELD
}
```

**Required updates:**
1. Add to `FakeReportInitializer`: `description: string;`
2. Add to `FakeReport` class: `public description: string;`
3. Add to constructor: `this.description = fakeReportInitialData.description;`
4. Add to `FakeReportBuilder`: `private description: string = '';`
5. Add builder method:
```typescript
withDescription(value: string): this {
  this.description = value;
  return this;
}
```
6. Add to builder's `getFakeReportInitializer()` return object: `description: this.description,`

### Scenario 2: Adding a New Method

**Interface change:**
```typescript
export interface IReport extends IEntity {
  // ... existing fields
  validate(): Promise<boolean>; // NEW METHOD
}
```

**Required updates:**
1. Add to `FakeReportInitializer`: `validateReturnValue: Promise<boolean>;`
2. Add to `FakeReport` class:
```typescript
validate = getMockingFunction<() => Promise<boolean>>(() => {
  return this.fakeReportInitialData.validateReturnValue;
});
```
3. Add to `FakeReportBuilder`: `private validateReturnValue: Promise<boolean> = Promise.resolve(false);`
4. Add builder method:
```typescript
withValidateReturnValue(value: Promise<boolean>): this {
  this.validateReturnValue = value;
  return this;
}
```
5. Add to builder's `getFakeReportInitializer()` return object: `validateReturnValue: this.validateReturnValue,`

### Scenario 3: Removing a Field

**Interface change:**
```typescript
export interface IReport extends IEntity {
  title: string;
  // status: string; // REMOVED
}
```

**Required updates:**
1. Remove from `FakeReportInitializer`: `status: string;`
2. Remove from `FakeReport` class: `public status: string;`
3. Remove from constructor: `this.status = fakeReportInitialData.status;`
4. Remove from `FakeReportBuilder`: `private status: string = '';`
5. Remove builder method: `withStatus(...)`
6. Remove from builder's `getFakeReportInitializer()` return object: `status: this.status,`

### Scenario 4: Changing a Field Type

**Interface change:**
```typescript
export interface IReport extends IEntity {
  title: string;
  status: ReportStatus; // Changed from string to enum/type
}
```

**Required updates:**
1. Update in `FakeReportInitializer`: `status: ReportStatus;`
2. Update in `FakeReport` class: `public status: ReportStatus;`
3. Constructor assignment stays the same: `this.status = fakeReportInitialData.status;`
4. Update in `FakeReportBuilder` with appropriate default: `private status: ReportStatus = ReportStatus.Draft;`
5. Update builder method parameter: `withStatus(value: ReportStatus): this`
6. Builder's getter stays the same: `status: this.status,`

### Scenario 5: Adding an EventBroker Field

**Interface change:**
```typescript
export interface IReport extends IEntity {
  title: IPropEventBroker<string>; // Changed from string to EventBroker
}
```

**Required updates:**
1. Update in `FakeReportInitializer`: `title: IPropEventBroker<string>;`
2. Update in `FakeReport` class: `public title: IPropEventBroker<string>;`
3. Constructor assignment stays the same: `this.title = fakeReportInitialData.title;`
4. Update in `FakeReportBuilder`: `private title: IPropEventBroker<string> = FakesFactory.createPropEventBroker<string>('');`
5. Add/update TWO builder methods:
```typescript
withTitle(value: IPropEventBroker<string>): this {
  this.title = value;
  return this;
}

withTitleValue(value: string): this {
  return this.withTitle(FakesFactory.createPropEventBroker<string>(value));
}
```
6. Builder's getter stays the same: `title: this.title,`

## Example Reference

See `examples.md` in the same directory as this skill for complete working examples.

## Important Notes

### File Organization (CRITICAL)
- **All fakes MUST be in `/fakes/` directory at package root** (sibling to `/src`, NOT inside `/src`)
- **All fakes MUST be exported from `/fakes/index.ts`**
- After creating or updating any fake, verify the export exists in `index.ts`
- Keep exports in `index.ts` alphabetically sorted for maintainability

### General Patterns
- All initializer fields are MANDATORY (never use optional `?`)
- Methods only track return values, not arguments
- Use `getMockingFunction` for all method implementations
- Builder fields should have sensible defaults
- EventBroker fields need two "with" methods
- Always return `this` from builder "with" methods for chaining
- Protected `getFake[ClassName]Initializer()` returns the initializer object
- Public `build()` creates the fake instance

### When Updating
- Always use the Edit tool for updates, not Write (which overwrites the entire file)
- Update all three components (Initializer, Fake class, Builder) for consistency
- When adding fields/methods, follow the exact same pattern as existing ones
- Check for TypeScript errors after updates to ensure completeness
- If the interface structure changed significantly (e.g., now extends IEntity), consider regenerating instead of updating
- Verify the export still exists in `/fakes/index.ts` after updates
