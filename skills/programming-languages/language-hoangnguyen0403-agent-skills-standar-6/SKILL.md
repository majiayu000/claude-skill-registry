---
name: TypeScript Language Patterns
description: Modern TypeScript standards for type safety, performance, and maintainability.
metadata:
  labels: [typescript, language, types, generics]
  triggers:
    files: ['**/*.ts', '**/*.tsx', 'tsconfig.json']
    keywords:
      [
        type,
        interface,
        generic,
        enum,
        union,
        intersection,
        readonly,
        const,
        namespace,
      ]
---

# TypeScript Language Patterns

## **Priority: P0 (CRITICAL)**

## Implementation Guidelines

- **Type Annotations**: Explicit params/returns. Infer locals.
- **Interfaces vs Types**: `interface` for APIs. `type` for unions.
- **Strict Mode**: `strict: true`. Null Safety: `?.` and `??`.
- **Enums**: Literal unions or `as const`. **No runtime `enum`**.
- **Generics**: Reusable, type-safe code.
- **Type Guards**: `typeof`, `instanceof`, predicates.
- **Utility Types**: `Partial`, `Pick`, `Omit`, `Record`.
- **Immutability**: `readonly` arrays/objects. Const Assertions: `as const`, `satisfies`.
- **Template Literals**: `on${Capitalize<string>}`.
- **Discriminated Unions**: Literal `kind` property.
- **Advanced**: Mapped, Conditional, Indexed types.
- **Access**: Default `public`. Use `private`/`protected` or `#private`.
- **Branded Types**: `string & { __brand: 'Id' }`.

## Anti-Patterns

- **No `any`**: NEVER use `any`. Use `unknown` or specific interfaces.
- **No `Function`**: Use signature `() => void`.
- **No `enum`**: Runtime cost.
- **No `!`**: Use narrowing.
- **NO LINT DISABLE**: PROHIBITED. Fix issues properly.

## Testing Patterns

- **Mock Types**: Use `jest.Mocked<T>` or `as unknown as T`. Never use `any`.
- **Enum Usage**: Always use enum values (`AppointmentStatus.UPCOMING`) instead of string literals (`'UPCOMING'`).
- **DTO Validation**: Ensure test data includes all required fields to match DTO validation.
- **Repository Mocks**: Mock all repository methods used by services (`findOne`, `create`, `save`, `findAndCount`, `createQueryBuilder`).

## Common Test Issues & Solutions

### Service Method Mismatches

**Problem**: Tests call methods that don't exist on services (e.g., `findByEmailWithPassword` not mocked).
**Solution**: Always check service implementation for actual method names before writing tests. Mock all methods that the service actually calls.

### Error Message Mismatches

**Problem**: Tests expect error messages that don't match the actual messages thrown by services.
**Solution**: Use the exact error messages from `ErrorMessages` constants instead of hardcoded strings.

### Type Safety Violations

**Problem**: Mock objects don't satisfy interface requirements (missing required properties).
**Solution**: Provide complete mock objects with all required properties, or use `as unknown as Type` casting for complex mocks.

### CurrentUser Interface Issues

**Problem**: Mock user objects missing required `CurrentUser` properties (`id`, `email`, `subscriptionTier`, `createdAt`, `updatedAt`).
**Solution**: Always include all required `CurrentUser` properties in test mocks. Import `SubscriptionTier` enum for proper typing.

### Auth Guard Mocking

**Problem**: Using `Partial<UsersService>` doesn't satisfy constructor requirements.
**Solution**: Provide complete service mocks with required properties (`logger`, `userRepository`) or cast to `unknown` first.

### Controller Parameter Issues

**Problem**: Tests pass wrong parameter types to controller methods (e.g., passing request objects instead of `CurrentUser`).
**Solution**: Check controller method signatures and decorator usage (`@CurrentUserDecorator()`) to pass correct parameter types.

## Code

```typescript
// Branded Type
type UserId = string & { __brand: 'Id' };

// Satisfies (Validate + Infer)
const cfg = { port: 3000 } satisfies Record<string, number>;

// Discriminated Union
type Result<T> = { kind: 'ok'; data: T } | { kind: 'err'; error: Error };
```

## Reference & Examples

For advanced type patterns and utility types:
See [references/REFERENCE.md](references/REFERENCE.md).

## Related Topics

best-practices | security | tooling
