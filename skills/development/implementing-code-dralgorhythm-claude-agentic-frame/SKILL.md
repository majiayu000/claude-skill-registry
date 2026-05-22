---
name: implementing-code
description: Write clean, efficient, maintainable code. Use when implementing features, writing functions, or creating new modules. Covers SOLID principles, error handling, and code organization.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Implementing Code

## Workflows

- [ ] **Security Check**: Injection flaws, auth issues, sensitive data exposure
- [ ] **Performance Check**: N+1 queries, memory leaks, inefficient algorithms
- [ ] **Readability Check**: SOLID principles, naming conventions, comments
- [ ] **Testing Check**: Edge cases, error paths, happy paths

## Feedback Loops

1. Implement feature or fix
2. Run local tests (unit/integration)
3. Run linter/formatter
4. If failure, fix and repeat

## Reference Implementation

### SOLID Compliant Class (TypeScript)

```typescript
// Abstraction (Interface Segregation)
interface ILogger {
  log(message: string): void;
}

interface IUserRepository {
  save(user: User): Promise<void>;
}

// Domain Entity
class User {
  constructor(public readonly id: string, public readonly email: string) {}
}

// Implementation (Single Responsibility)
class UserService {
  constructor(
    private readonly userRepository: IUserRepository,
    private readonly logger: ILogger
  ) {}

  public async registerUser(email: string): Promise<User> {
    if (!email.includes('@')) {
      throw new Error("Invalid email format");
    }

    const user = new User(crypto.randomUUID(), email);
    await this.userRepository.save(user);
    this.logger.log(`User registered: ${user.id}`);

    return user;
  }
}
```

## Code Review Checklist

- [ ] No hardcoded secrets or credentials
- [ ] Input validation on all external data
- [ ] Proper error handling with meaningful messages
- [ ] No N+1 query patterns
- [ ] Functions follow single responsibility principle
- [ ] Dependencies injected, not instantiated inline
- [ ] Tests cover happy path and edge cases
