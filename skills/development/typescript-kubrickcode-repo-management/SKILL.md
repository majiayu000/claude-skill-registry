---
name: typescript
description: |
  Provides comprehensive TypeScript development expertise and coding standards. Ensures type safety through strict type checking, implements clean code patterns, and maintains consistent architectural decisions. Specializes in advanced type system features including generics, conditional types, mapped types, and template literal types.
  Use when: working with TypeScript files (.ts/.tsx), defining type definitions and interfaces, implementing generic programming patterns, designing type-safe APIs, handling complex type transformations, integrating TypeScript with React/Vue/Angular frameworks, configuring strict mode settings, resolving type errors, or optimizing type performance in large codebases.
---

# TypeScript Coding Standards

## Basic Principles

### One Function, One Responsibility

- If function name connects with "and" or "or", it's a signal to split
- If test cases are needed for each if branch, it's a signal to split

### Conditional and Loop Depth Limited to 2 Levels

- Minimize depth using early return whenever possible
- If still heavy, extract into separate functions

### Make Function Side Effects Explicit

- Example: If `getUser` also runs `updateLastAccess()`, specify it in the function name

### Convert Magic Numbers/Strings to Constants When Possible

- Declare at the top of the file or class where used
- Consider separating into a constants file if there are many

### Function Order by Call Order

- Follow class access modifier declaration order rules if clear
- Otherwise, order top-to-bottom for easy reading by call order

### Review External Libraries for Complex Implementations

- When logic is complex and tests become bloated
- If industry-standard libraries exist, use them
- When security, accuracy, or performance optimization is critical
- When browser/platform compatibility or edge cases are numerous

### Modularization (Prevent Code Duplication and Pattern Repetition)

- Absolutely forbid code repetition
- Modularize similar patterns into reusable forms
- Allow pre-modularization if reuse is confirmed
- Avoid excessive abstraction
- Modularization levels:
  - Same file: Extract into separate function
  - Multiple files: Separate into different file
  - Multiple projects/domains: Separate into package

### Variable and Function Names

- Clear purpose while being concise
- Forbid abbreviations outside industry standards (id, api, db, err, etc.)
- Don't repeat context from the parent scope
- Boolean variables use `is`, `has`, `should` prefixes
- Function names are verbs or verb+noun forms
- Plural rules:
  - Pure arrays: "s" suffix (`users`)
  - Wrapped object: "list" suffix (`userList`)
  - Specific data structure: Explicit (`userSet`, `userMap`)
  - Already plural words: Use as-is

### Field Order

- Alphabetically ascending by default
- Maintain consistency in usage
- Also alphabetically ordered in destructuring assignment

### Error Handling

- Error handling level: Handle where meaningful response is possible
- Error messages: Technical details for logs, actionable guidance for users
- Error classification: Distinguish between expected and unexpected errors
- Error propagation: Add context when propagating up the call stack
- Recovery vs. fast fail: Recover from expected errors with fallback
- Error types: For domain-specific failures, create custom error classes extending `Error`. Never throw non-Error objects
- Async errors: Always handle Promise rejection. Use try-catch for async/await, .catch() for promise chains

## Package Management

### Package Manager

- Use pnpm as default package manager
- Forbid npm, yarn (prevent lock file conflicts)

## File Structure

### Common for All Files

1. Import statements (grouped)
2. Constant definitions (alphabetically ordered if multiple)
3. Type/Interface definitions (alphabetically ordered if multiple)
4. Main content (see below)

### Inside Classes

- Decorators
- private readonly members
- readonly members
- constructor
- public methods (alphabetically ordered)
- protected methods (alphabetically ordered)
- private methods (alphabetically ordered)

### Function Placement in Function-Based Files

- Main exported function
- Additional exported functions (alphabetically ordered, avoid many)
- Helper functions

## Function Writing

### Use Arrow Functions

- Always use arrow functions except for class methods
- Forbid function keyword entirely (exceptions: generator function\*, function hoisting etc. technically impossible cases only)

### Function Arguments: Flat vs Object

- Use flat if single argument or uncertain of future additions
- Use object form for 2+ arguments in most cases. Allow flat form when:
  - All required arguments without boolean arguments
  - All required arguments with clear order (e.g., (width,height), (start,end), (min,max), (from,to))

## Type System

### Type Safety

- Forbid unsafe type bypasses like any, as, !, @ts-ignore, @ts-expect-error
- Exceptions: Missing or incorrect external library types, rapid development needed (clarify reason in comments)
- Allow some unknown type when type guard is clear
- Allow as assertion when literal type (as const) needed
- Allow as assertion when widening literal/HTML types to broader types
- Allow "!" assertion when type narrowing impossible after type guard due to TypeScript limitation
- Allow @ts-ignore, @ts-expect-error in test code (absolutely forbid in production)

### Interface vs Type

- Prioritize Type in all cases by default
- Use Interface only for these exceptions:
  - Public API provided to external users like library public API
  - Need to extend existing interface like external libraries
  - Designing OOP-style classes where implementation contract must be clearly defined

### null/undefined Handling

- Actively use Optional Chaining (`?.`)
- Provide defaults with Nullish Coalescing (`??`)
- Distinguish between `null` and `undefined` by semantic meaning:
  - `undefined`: Uninitialized state, optional parameters, value not assigned yet
  - `null`: Intentional absence of value (similar to Go's nil)
- Examples:
  - Optional field: `{ name?: string }` → can be `undefined`
  - Intentionally cleared value: `user.profileImage = null`
  - External API responses may use either convention

## Code Style

### Maintain Immutability

- Use `const` whenever possible, minimize `let`
- Create new values instead of directly modifying arrays/objects
- Use `spread`, `filter`, `map` instead of `push`, `splice`
- Exceptions: Extremely performance-critical cases

## Recommended Libraries

- Testing: Jest, Playwright
- Utilities: es-toolkit, dayjs
- HTTP: ky, @tanstack/query, @apollo/client
- Form: React Hook Form
- Type validation: zod
- UI: Tailwind + shadcn/ui
- ORM: Prisma (Drizzle if edge support important)
- State management: zustand
- Code formatting: prettier, eslint
- Build: tsup
