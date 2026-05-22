---
name: architecture-patterns
description: "Software architecture patterns (SOLID, DDD, Clean/Hexagonal Architecture, Mediator, Result). Backend-first, frontend when context justifies. Trigger: When designing maintainable systems, complex state management, or project specifies architectural requirements in AGENTS.md."
skills:
  - conventions
  - typescript
dependencies:
  typescript: ">=4.5.0"
allowed-tools:
  - documentation-reader
  - read-file
---

# Architecture Patterns

## Overview

Comprehensive guide for software architecture patterns including SOLID principles, Domain-Driven Design, Clean Architecture, Hexagonal Architecture, and behavioral patterns (Mediator, Result). **Primary application: Backend services**. Frontend application: Enterprise-scale applications with complex domain logic when specified in project's AGENTS.md.

## Objective

Enable creation of maintainable, testable, scalable code through proven architectural patterns. Guide backend developers in applying patterns by default; guide frontend developers in conditional application when project context demands it.

---

## When to Use

### Backend Projects

**Apply when**:

- Codebase already uses these patterns (folders: `domain/`, `application/`, `infrastructure/`)
- AGENTS.md specifies architecture patterns
- Project >500 LOC with business logic
- Building microservices or services with multiple layers
- User explicitly requests architectural patterns

**Don't apply when**:

- Simple scripts or utilities (<200 LOC)
- Prototypes or proof-of-concepts
- Basic CRUD APIs without business logic
- Codebase doesn't use patterns and user hasn't requested them

### Frontend Projects

**Apply when**:

- AGENTS.md explicitly mentions architecture patterns
- Codebase already uses these patterns (folders exist: `domain/`, `application/`, `infrastructure/`)
- User requests architectural patterns: "aplica arquitectura aquí", "usa SOLID", "implementa con DDD"
  - **Note**: AI must evaluate if pattern is applicable to the frontend technology (React/Vue/HTML/CSS). Some patterns don't make sense in certain contexts.

**Don't apply when**:

- AGENTS.md doesn't mention architecture patterns
- Codebase doesn't follow these patterns
- User hasn't requested architectural approach
- **Pattern is not applicable** to the technology (e.g., DDD in plain HTML)

---

## Quick Reference

| Pattern                | Best For                                 | Read Reference                                                             |
| ---------------------- | ---------------------------------------- | -------------------------------------------------------------------------- |
| SOLID Principles       | Class design, component structure        | **MUST** [solid-principles.md](references/solid-principles.md)             |
| Clean Architecture     | Layer separation, dependency management  | **MUST** [clean-architecture.md](references/clean-architecture.md)         |
| Hexagonal Architecture | Port/adapter design, testing             | **MUST** [hexagonal-architecture.md](references/hexagonal-architecture.md) |
| Domain-Driven Design   | Complex domain modeling, bounded context | **MUST** [domain-driven-design.md](references/domain-driven-design.md)     |
| Mediator Pattern       | Decoupled communication                  | **CHECK** [mediator-pattern.md](references/mediator-pattern.md)            |
| Result Pattern         | Explicit error handling                  | **CHECK** [result-pattern.md](references/result-pattern.md)                |

**For backend integration examples**: [backend-integration.md](references/backend-integration.md)  
**For frontend integration examples**: [frontend-integration.md](references/frontend-integration.md)

---

## Critical Patterns

### ✅ REQUIRED [CRITICAL]: Verify Context Before Applying

**For Backend Projects**:

Check these signals in order:

1. **Codebase structure**: Folders like `domain/`, `application/`, `infrastructure/` exist? → Apply patterns consistently
2. **AGENTS.md mentions patterns**: "Clean Architecture", "SOLID", "DDD"? → Apply patterns
3. **Project size + logic**: >500 LOC with business logic? → Consider applying (ask user first)
4. **None of above**: → Use simple patterns, don't introduce architecture

**For Frontend Projects**:

Check these signals in order:

1. **AGENTS.md explicitly requires**: "follows Clean Architecture", "uses SOLID"? → Apply patterns
2. **Codebase already structured**: Folders `domain/`, `application/`, `infrastructure/` exist? → Continue using patterns
3. **User requests architecture**: "aplica arquitectura", "usa SOLID aquí", "implementa con DDD"? → **Evaluate applicability first**:
   - ✅ **Applicable**: SOLID in React components, Result Pattern in hooks, DIP with Context API → Apply
   - ⚠️ **Partially applicable**: DDD in React (entities/value objects yes, full DDD no) → Apply what makes sense
   - ❌ **Not applicable**: DDD in plain HTML, Clean Architecture in static CSS → Inform user it's not applicable and suggest alternatives
4. **None of above**: → Don't apply. Use React/Redux/Astro patterns only

**Rule**: Evaluate if requested pattern makes sense for the technology stack. Don't blindly apply inappropriate patterns.

See [backend-integration.md](references/backend-integration.md) and [frontend-integration.md](references/frontend-integration.md) for detailed guidelines.

---

### ✅ REQUIRED [CRITICAL]: Single Responsibility Principle (SRP)

Each module/class/component should have ONE reason to change.

```typescript
// ✅ CORRECT: Separated concerns

// userRepository.ts - Data access only
export class UserRepository {
  async findById(id: string): Promise<User | null> {
    return await db.users.findUnique({ where: { id } });
  }

  async save(user: User): Promise<void> {
    await db.users.create({ data: user });
  }
}

// userValidator.ts - Validation only
export class UserValidator {
  validate(user: User): ValidationResult {
    if (!user.email.includes("@")) {
      return { valid: false, errors: ["Invalid email"] };
    }
    return { valid: true, errors: [] };
  }
}

// userService.ts - Business logic only
export class UserService {
  constructor(
    private repo: UserRepository,
    private validator: UserValidator,
  ) {}

  async createUser(user: User): Promise<Result<User>> {
    const validation = this.validator.validate(user);
    if (!validation.valid) {
      return Result.fail(validation.errors);
    }
    await this.repo.save(user);
    return Result.ok(user);
  }
}

// ❌ WRONG: Everything in one class
export class UserManager {
  async createUser(user: User) {
    // Validation
    if (!user.email.includes("@")) throw new Error("Invalid");

    // Data access
    await db.users.create({ data: user });

    // Email sending
    await sendEmail(user.email, "Welcome");

    // Logging
    console.log("User created");
  }
}
```

**Backend**: Apply to all services, repositories, controllers.  
**Frontend**: Apply to complex components, state slices, API services.

See [solid-principles.md](references/solid-principles.md) for all 5 SOLID principles.

---

### ✅ REQUIRED: Dependency Inversion Principle (DIP)

Depend on abstractions, not concretions. High-level modules should not depend on low-level modules.

```typescript
// ✅ CORRECT: Depend on interface

// port (abstraction)
export interface IEmailService {
  send(to: string, subject: string, body: string): Promise<void>;
}

// high-level module depends on interface
export class UserService {
  constructor(private emailService: IEmailService) {}

  async registerUser(user: User) {
    await this.repo.save(user);
    await this.emailService.send(user.email, "Welcome", "...");
  }
}

// adapter (concrete implementation)
export class SendGridEmailService implements IEmailService {
  async send(to: string, subject: string, body: string) {
    await sendgrid.send({ to, subject, html: body });
  }
}

// ❌ WRONG: Direct dependency on concrete class
export class UserService {
  private emailService = new SendGridEmailService(); // Tightly coupled

  async registerUser(user: User) {
    await this.emailService.send(user.email, "Welcome", "...");
  }
}
```

**Why**: Easy to swap implementations (SendGrid → AWS SES), easy to test (mock interface).

See [solid-principles.md](references/solid-principles.md#dependency-inversion) for advanced examples.

---

### ✅ REQUIRED: Layer Separation (Clean Architecture)

Organize code in concentric layers with dependency direction: outer → inner.

```
┌─────────────────────────────────────┐
│  Infrastructure (Adapters)          │  ← Frameworks, DB, HTTP
│  ┌───────────────────────────────┐  │
│  │  Application (Use Cases)      │  │  ← Business workflows
│  │  ┌─────────────────────────┐  │  │
│  │  │  Domain (Entities)      │  │  │  ← Business rules
│  │  └─────────────────────────┘  │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

```typescript
// ✅ CORRECT: Layer separation

// Domain layer (core business rules)
// domain/entities/User.ts
export class User {
  constructor(
    public readonly id: string,
    public readonly email: string,
    private status: UserStatus,
  ) {}

  activate(): void {
    if (this.status === "banned") {
      throw new Error("Cannot activate banned user");
    }
    this.status = "active";
  }
}

// Application layer (use cases)
// application/useCases/RegisterUser.ts
export class RegisterUserUseCase {
  constructor(private userRepo: IUserRepository) {} // ← Depends on port

  async execute(email: string): Promise<Result<User>> {
    const user = new User(generateId(), email, "pending");
    await this.userRepo.save(user);
    return Result.ok(user);
  }
}

// Infrastructure layer (adapters)
// infrastructure/repositories/PostgresUserRepository.ts
export class PostgresUserRepository implements IUserRepository {
  async save(user: User): Promise<void> {
    await this.db.query("INSERT INTO users...");
  }
}

// ❌ WRONG: No layer separation
export class UserController {
  async register(req, res) {
    // Domain logic mixed with HTTP
    const user = { id: uuid(), email: req.body.email };

    // Data access mixed with controller
    await db.query("INSERT INTO users VALUES ($1, $2)", [user.id, user.email]);

    res.json(user);
  }
}
```

See [clean-architecture.md](references/clean-architecture.md) for complete layer guidelines.

---

### ✅ REQUIRED: Port and Adapter Pattern (Hexagonal)

Define ports (interfaces) for external dependencies; create adapters for each implementation.

```typescript
// ✅ CORRECT: Port and adapter

// Port (interface - core defines this)
export interface IPaymentGateway {
  charge(amount: number, token: string): Promise<PaymentResult>;
}

// Core business logic depends on port
export class OrderService {
  constructor(private payment: IPaymentGateway) {}

  async placeOrder(order: Order): Promise<Result<Order>> {
    const result = await this.payment.charge(order.total, order.token);
    if (!result.success) return Result.fail("Payment failed");
    return Result.ok(order);
  }
}

// Adapter 1: Stripe
export class StripeAdapter implements IPaymentGateway {
  async charge(amount: number, token: string): Promise<PaymentResult> {
    const result = await stripe.charges.create({ amount, source: token });
    return { success: result.status === "succeeded" };
  }
}

// Adapter 2: PayPal
export class PayPalAdapter implements IPaymentGateway {
  async charge(amount: number, token: string): Promise<PaymentResult> {
    const result = await paypal.payment.create({ amount, token });
    return { success: result.state === "approved" };
  }
}

// ❌ WRONG: Directly using vendor SDK
export class OrderService {
  async placeOrder(order: Order) {
    const result = await stripe.charges.create({
      /* ... */
    }); // Coupled to Stripe
  }
}
```

**Benefits**: Swap payment providers without changing core logic; test with mock adapter.

See [hexagonal-architecture.md](references/hexagonal-architecture.md) for testing strategies.

---

### ✅ REQUIRED: Result Pattern for Error Handling

Return Result<T> instead of throwing exceptions for expected errors.

```typescript
// ✅ CORRECT: Result pattern

export class Result<T> {
  private constructor(
    public readonly isSuccess: boolean,
    public readonly value?: T,
    public readonly error?: string,
  ) {}

  static ok<T>(value: T): Result<T> {
    return new Result(true, value);
  }

  static fail<T>(error: string): Result<T> {
    return new Result(false, undefined, error);
  }
}

// Usage
export class UserService {
  async getUser(id: string): Promise<Result<User>> {
    const user = await this.repo.findById(id);

    if (!user) {
      return Result.fail("User not found"); // Expected error
    }

    return Result.ok(user);
  }
}

// Consumer
const result = await userService.getUser("123");
if (result.isSuccess) {
  console.log(result.value); // Type-safe access
} else {
  console.error(result.error); // Handle error
}

// ❌ WRONG: Throwing for expected errors
export class UserService {
  async getUser(id: string): Promise<User> {
    const user = await this.repo.findById(id);
    if (!user) throw new Error("User not found"); // Caller must remember to catch
    return user;
  }
}
```

See [result-pattern.md](references/result-pattern.md) for advanced patterns (Either, Option).

---

### ❌ NEVER: Mix Domain Logic with Infrastructure

```typescript
// ❌ WRONG: Domain entity knows about database
export class User {
  async save() {
    await db.users.update({ where: { id: this.id }, data: this });
  }
}

// ✅ CORRECT: Repository handles persistence
export class User {
  // Pure domain logic only
  promote(): void {
    this.role = "admin";
  }
}

export class UserRepository {
  async save(user: User): Promise<void> {
    await db.users.update({ where: { id: user.id }, data: user });
  }
}
```

---

## Decision Tree

```
Is this a backend project?
  → Yes → Apply patterns by default (SOLID, Clean/Hexagonal Architecture)
  → No → Is this a frontend project?
    → Check AGENTS.md:
      → Mentions "architecture", "SOLID", "clean", "DDD"? → Apply patterns
      → No mention? → Is project complex?
        → >50 components + heavy business logic? → Consider applying
        → Otherwise → Use technology-specific patterns only

Which pattern to use?
  → Need class/component design guidance? → MUST read solid-principles.md
  → Need layer organization? → MUST read clean-architecture.md
  → Need port/adapter (testing, swapping dependencies)? → MUST read hexagonal-architecture.md
  → Complex domain modeling? → MUST read domain-driven-design.md
  → Decoupled component communication? → CHECK mediator-pattern.md
  → Explicit error handling? → CHECK result-pattern.md

Backend or frontend examples?
  → Backend → READ backend-integration.md
  → Frontend → READ frontend-integration.md
```

---

## Conventions

Refer to [conventions](../conventions/SKILL.md) for:

- Naming patterns (camelCase, PascalCase, UPPER_SNAKE_CASE)
- File organization
- Import grouping

Refer to [typescript](../typescript/SKILL.md) for:

- Interface definitions
- Type safety
- Generic constraints

### Architecture-Patterns-Specific

- Use `I` prefix for interfaces (ports): `IUserRepository`, `IEmailService`
- One class per file: `UserService.ts`, `UserRepository.ts`
- Organize by layer: `domain/`, `application/`, `infrastructure/`
- Use dependency injection (constructor injection preferred)
- Ports in `domain/` or `application/`, adapters in `infrastructure/`

---

## Example

For complete working examples showing SOLID + Clean Architecture + Hexagonal:

- **Backend**: See [backend-integration.md](references/backend-integration.md) - Complete Order Service with NestJS, Express, Fastify examples
- **Frontend**: See [frontend-integration.md](references/frontend-integration.md) - React components with architecture patterns

Examples include:

- Full folder structure (domain/, application/, infrastructure/)
- Complete implementations with dependency injection
- Testing strategies (unit + integration)
- Multiple framework examples (NestJS, Express, React)

---

## Edge Cases

### When Frontend Projects Resist Architecture

**Symptom**: Team pushes back on "over-engineering"

**Solution**:

- Start small: Apply Result pattern first (low friction)
- Show value: Demonstrate testability improvements
- Iterate: Add layer separation gradually
- Document: Update AGENTS.md with rationale

### Mixing Multiple Architecture Styles

**Symptom**: Trying to use Clean + Hexagonal + DDD simultaneously

**Solution**:

- Choose primary pattern (usually Clean Architecture)
- Use others as complements (Hexagonal for ports, DDD for domain modeling)
- See [clean-architecture.md](references/clean-architecture.md#integration-with-other-patterns)

### Legacy Code Migration

**Symptom**: Existing codebase doesn't follow any pattern

**Solution**:

- Start with new features (apply patterns to new code)
- Create anti-corruption layer for legacy integration
- Refactor incrementally (one module at a time)
- See [backend-integration.md](references/backend-integration.md#legacy-migration)

### Over-Abstraction

**Symptom**: 5 layers of indirection for simple CRUD

**Solution**:

- Skip architecture for simple CRUD (direct controller → repository)
- Apply only when logic is complex
- Use pragmatism: "Is this abstraction paying for itself?"

---

## Resources

### Reference Files

All references in [references/](references/) directory:

- **MUST read for specific pattern**: [solid-principles.md](references/solid-principles.md), [clean-architecture.md](references/clean-architecture.md), [hexagonal-architecture.md](references/hexagonal-architecture.md), [domain-driven-design.md](references/domain-driven-design.md)
- **CHECK for behavioral patterns**: [mediator-pattern.md](references/mediator-pattern.md), [result-pattern.md](references/result-pattern.md)
- **Integration guides**: [backend-integration.md](references/backend-integration.md), [frontend-integration.md](references/frontend-integration.md)
- **Navigation**: [README.md](references/README.md)

### Related Skills

- [conventions](../conventions/SKILL.md) - General coding standards
- [typescript](../typescript/SKILL.md) - Type safety and interfaces
- [react](../react/SKILL.md) - Frontend integration (see "Advanced Architecture Patterns" section)
- [redux-toolkit](../redux-toolkit/SKILL.md) - State architecture (see "Architecture Integration" section)
