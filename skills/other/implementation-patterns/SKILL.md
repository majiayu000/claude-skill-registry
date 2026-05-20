---
name: implementation-patterns
description: Use when the Developer is implementing features from task specifications, translating architecture into code, integrating with APIs, managing state, or choosing design patterns. Activates when building new functionality from requirements.
version: 1.0.0
---

# Implementation Patterns

## When This Applies

Apply this guidance when:
- Translating a task specification into working code
- Choosing design patterns for a feature
- Integrating with external APIs or services
- Implementing business logic from requirements

## Implementation Workflow

### Before Writing Code

1. **Read the task** — Understand requirements and acceptance criteria
2. **Read the architecture** — Check ARCHITECTURE.md for design guidance
3. **Read existing code** — Understand patterns already used in the project
4. **Plan the approach** — Which files to create/modify, what order

### While Writing Code

1. **Follow existing patterns** — If the codebase uses MVC, don't introduce MVVM
2. **Build incrementally** — Get the simplest version working, then add complexity
3. **Test as you go** — Verify each piece before building the next
4. **Stay in scope** — Only implement what the task asks for

## Common Design Patterns

### Repository Pattern
Use when: Abstracting data access from business logic
```
DataSource → Repository → Service → Controller
```
The repository provides a clean interface for data operations, hiding storage details.

### Strategy Pattern
Use when: Multiple algorithms or behaviors that should be interchangeable
```
Context uses Strategy interface
  → ConcreteStrategyA
  → ConcreteStrategyB
```

### Observer/Event Pattern
Use when: Multiple parts of the system need to react to changes
```
EventEmitter.emit("userCreated", user)
  → Logger.onUserCreated(user)
  → EmailService.onUserCreated(user)
```

### Middleware/Pipeline Pattern
Use when: Processing requests through a chain of handlers
```
Request → Auth → Validate → RateLimit → Handler → Response
```

## API Integration Guidelines

When integrating with external APIs:
1. **Wrap the client** — Create a service layer, don't call APIs directly from business logic
2. **Handle errors** — Network timeouts, rate limits, 4xx/5xx responses
3. **Validate responses** — Don't trust external data; validate shape and types
4. **Add retries** — For transient failures (network issues, 503s)
5. **Log requests** — Log URL, method, status code (never log secrets or PII)

## State Management

- Keep state as close to where it's used as possible
- Use immutable patterns where the language supports it
- Centralize shared state; avoid passing it through many layers
- Document state transitions (what triggers changes)

## File Organization

When creating new files for a feature:
```
projects/<project>/src/
├── models/          # Data structures
├── services/        # Business logic
├── controllers/     # API handlers / entry points
├── utils/           # Shared utilities
└── config/          # Configuration
```

Follow whatever structure the project already uses. Don't introduce a new organization scheme within a task.

## Scope Discipline

- If you discover something that needs fixing but is outside your task, don't fix it — send a message to the Manager or Architect via queue describing what you found
- If the task requirements are ambiguous, ask via queue before guessing
- If you need an architecture change, send to Architect — don't change ARCHITECTURE.md yourself
