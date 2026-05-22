---
name: test-repository
description: Guide for testing repository layer. Use when asked to test repositories or data access layer. Directs to implementation-specific testing skills.
---

# Test Repository

## Important: We Test Implementations, Not Interfaces

Repository interfaces (`I{Entity}Repository`) define contracts but contain no logic to test. We test the **implementations** that fulfill these contracts.

## When to Test

Test repository implementations **after** you have:

1. Created the repository interface (`create-repository` skill)
2. Implemented at least one concrete implementation

## Which Skill to Use

| Implementation     | Skill                     | Location                                                 |
| ------------------ | ------------------------- | -------------------------------------------------------- |
| MockDB (in-memory) | `test-mockdb-repository`  | `tests/repositories/{entity}.mockdb.repository.test.ts`  |
| MongoDB            | `test-mongodb-repository` | `tests/repositories/{entity}.mongodb.repository.test.ts` |

## Testing Strategy

Each implementation should be tested to verify it correctly fulfills the interface contract:

- **CRUD operations**: create, findById, findAll, update, remove
- **Query features**: filtering, pagination, sorting, search
- **Edge cases**: not found returns null, delete non-existent returns false
- **Implementation-specific**: MongoDB indexes, MockDB in-memory behavior

## See Also

- `test-mockdb-repository` - Testing MockDB implementations
- `test-mongodb-repository` - Testing MongoDB implementations (includes test infrastructure setup)
