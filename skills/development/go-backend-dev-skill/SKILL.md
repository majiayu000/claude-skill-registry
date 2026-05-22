---
name: Golang Backend Development
description: Architectural standards and coding practices for the Go backend.
---

# Golang Backend Development Standards

This skill defines the architectural requirements, coding standards, and best practices for the Golang backend. AI agents must adhere to these guidelines to ensure consistency, maintainability, and extensibility.

## 1. Project Organization
- See `references/PROJECT_ORGANIZATION.md` for examples.

- `backend/cmd/`: Application entry points. Keep `main.go` slim; use it for configuration and component initialization.
- `backend/internal/`: Project-internal code.
    - `handler/`: HTTP layer. Uses `Handler` generic wrapper. Defers logic to `service`.
    - `service/`: Domain logic layer. Orchestrates business rules and repository calls.
    - `repository/`: Data layer. Handles raw SQL queries via `pgxpool`.
    - `models/`: Data structures (DB models, DTOs, request/response types).
- `backend/pkg/`: Shared utility packages (e.g., custom `statemachine`).
- `backend/migrations/`: SQL migration scripts.

## 2. Core Architectural Patterns

### Layered Responsibility
- See `references/LAYERED_RESPONSIBILITY.md` for examples.
- **Handlers** must NOT contain business logic. They decode requests, call services, and encode responses.
- **Services** are the source of truth for business rules. They must be agnostic to the delivery method (HTTP).
- **Repositories** bridge the domain models and the database.

### Interface Design
- Keep interfaces small with minimal methods to provide maximum flexibility for implementers.
- **Return Structs, Accept Interfaces**: Functions should return concrete types even if they implement an interface. Parameters should be interfaces to reduce coupling.

### Request Validation
- See `references/VALIDATOR_INTERFACE.md` for examples.
- When request parameters require validation, implement a `Validator` interface pattern.
- Use a composable approach (e.g., `AllPassValidator`) to combine multiple validation rules.
- Inject the validator into the service to keep validation logic decoupled from business logic.

### The `Handler` Wrapper
- See `references/THE_HANDLER_WRAPPER.md` for examples.
Every HTTP endpoint should be wrapped using the `Handler[REQ, RESP]`. This ensures consistent:
- Request decoding (`DecodeFunc`, `DefaultDecoder`)
- **Pre-handling**: Logic executed before the main handler (e.g., validation)
- **Post-handling**: Logic executed after the main handler (e.g., logging)
- Response encoding (`EncodeFunc`, `DefaultEncoder`)
- Error handling (`DefaultErrorHandler`)

### Dependency Injection
Dependencies must be injected via constructors:
- See `references/DEPENDENCY_INJECTION.md` for examples.

## 3. Coding Standards & Tooling

### Standard Library First
- See `references/STANDARD_LIBRARY_FIRST.md` for examples.
- Always prioritize using the Go standard library to implement functionality unless strictly necessary. Keep external dependencies to a minimum.

### Context First
- See `references/CONTEXT_USAGE.md` for examples.
- Pass `context.Context` to all `service` and `repository` methods to support cancellation and timeouts.

### Database: Raw SQL with `pgx` or `sqlx`
- See `references/DATABASE_ACCESS.md` for examples.
- Prefer raw SQL over ORMs for performance and transparency.
- Use `github.com/jackc/pgx/v5` and `pgxpool`, or `github.com/jmoiron/sqlx`.
- Scan results into structs defined in `internal/models`.

### HTTP Middleware
Apply cross-cutting concerns via middleware:
- See `references/MIDDLEWARE.md` for examples.
- `LoggingMiddleware`: Records full request/response details for debugging.
- `AuthMiddleware`: Validates JWT and extracts `userID`.
- `CORSMiddleware`: Standard CORS headers.

### Function Parameter Design
- See `references/FUNCTION_PARAMETER_DESIGN.md` for examples.
- **Backward Compatibility**: Design function parameters with backward compatibility in mind. Use patterns like **Functional Options** or wrap multiple parameters into a **Request/Options Struct** to avoid breaking changes when extending functionality.
- **Avoid Parameter Mutation**:
  - See `references/AVOID_MUTATING_PARAMETERS.md` for examples.
  - Avoid modifying input parameters within a function, even if they are pointer types. This reduces side effects and makes call-site behavior more predictable.
  - **Exception**: Mutation is only permissible when justified by severe performance requirements (e.g., high-frequency hot paths, extremely large structs).

### Concurrency & Goroutines
- See `references/GOROUTINE_POOLS.md` for examples.
- If dynamic generation of a large number of goroutines is required (e.g., in a heavily called handler), you **must** use a goroutine pool for management.
- Unbounded goroutine creation can lead to memory leaks. See [issue #9869](https://github.com/golang/go/issues/9869).
- When starting a new task using a goroutine, if the task involves an infinite loop, ensure that the goroutine accepts a `context.Context` parameter. This allows the use of `context.Context` to terminate the loop, avoiding memory leaks.
- **Channel Ownership**: The goroutine that writes to a channel should be the one responsible for closing it. This prevents panic scenarios where a channel is closed while being written to.
- **Mutex Locking**:
  - See `references/MUTEX_LOCKING.md` for examples.
  - Minimize the duration mutex locks are held.
  - When multiple independent resources require locking, use fine-grained locking (one mutex per resource) to avoid unnecessary blocking. Use the generic `Mutex[T]` pattern to enforce this.

### Design Principles
- See `references/DESIGN_PRINCIPLES.md` for examples.
- **KISS (Keep It Simple and Stupid)**: Prioritize simplicity over complexity. Avoid over-engineering.
- **SOLID**: Follow SOLID principles to ensure maintainable and scalable code, but always prioritize KISS:
    - **S - Single Responsibility Principle (SRP)**: A class or function should have one, and only one, reason to change.
    - **O - Open/Closed Principle (OCP)**: Entities should be open for extension, but closed for modification.
    - **L - Liskov Substitution Principle (LSP)**: Derived types must be completely substitutable for their base types.
    - **I - Interface Segregation Principle (ISP)**: Clients should not be forced to depend on interfaces they do not use.
    - **D - Dependency Inversion Principle (DIP)**: Depend on abstractions, not on concretions.

### Testing & Coverage
- See `references/TESTING.md` for examples.
- All service, repository, and package implementations must have test case coverage.
- **Mocking**: Use the [mockery](https://github.com/vektra/mockery) library to generate mock files for interfaces. This facilitates consistent and easy unit testing.
- Prioritize testability in all implementations.

### 4. Code Quality & Linting
- **Configuration**: If `.golangci.yml` does not exist in the project root, create one using the reference configuration from [golangci-lint reference](https://raw.githubusercontent.com/golangci/golangci-lint/master/.golangci.reference.yml).
- **Enforcement**: Run `golangci-lint run ./...` on the entire project after making changes or fixing issues to ensure code quality and consistency.

## 4. Error Handling & Return Values
- See `references/ERROR_HANDLING.md` for examples.
- **Handle All Errors**: Ensure all errors are properly handled. Ignoring errors or only checking them without action can lead to silent failures.
- Return clear, typed errors from services (e.g., `ErrUnauthorized`).
- Ensure all JSON-serialized fields have appropriate `json` tags.

### Must-Prefix Functions & Panic Safety
- See `references/MUST_FUNCTIONS.md` for examples.
- **Must-prefix functions** (e.g., `template.Must`, `regexp.MustCompile`) and helper functions like `func Must[T any](t T, err error) T` that panic on error **must only be used in safe contexts**:
  1. **Initialization in `main.go`**: Where immediate failure is acceptable and expected (e.g., loading critical configuration, compiling static regexes)
  2. **Guaranteed safe inputs**: Where you can manually verify that the input will never cause an error (e.g., hardcoded valid regex patterns, compile-time constants)
- **Never use** Must-functions with:
  - User input or external data
  - Runtime-generated values that could be invalid
  - Any operation in request handlers, services, or repositories where recovery is possible
- **Rationale**: Panics in production services cause crashes and service disruption. Proper error handling allows graceful degradation and better observability.

### Constructor Error Handling
- See `references/CONSTRUCTOR_ERROR_HANDLING.md` for examples.
- If a constructor executes logic that returns an error (e.g., parsing config, opening DB), the constructor **must** return `(*Type, error)` instead of panicking.

## 5. Extensibility Goal
- See `references/EXTENSIBILITY.md` for examples.
- When implementing new features, consider how side effects (notifications, logs, state transitions) can be hooked into the existing flow without tightly coupling the core business logic.

## 6. Performance Optimization
- See `references/PERFORMANCE_OPTIMIZATION.md` for examples.
- **Object Pooling**: For objects that are frequently allocated and deallocated, use `sync.Pool` to reduce GC pressure.
- **Stack Allocation**: Prefer returning concrete objects (values) rather than pointers when the object is small or where stack allocation is possible, reducing the burden on the heap and GC.
- **Hot Paths**: Only apply aggressive optimizations in verified hot paths where performance issues are significant.

## Summary of Key Patterns

### ✅ Always Do:
1. Use constructor-based dependency injection
2. Pass `context.Context` as the first parameter
3. Use raw SQL with pgx/sqlx instead of ORMs
4. Return concrete types, accept interfaces
5. Use `uuid.UUID` for identifiers
6. Define typed errors as package variables
7. Add proper `json` tags to all models
8. Write tests with mockery-generated mocks
9. Use functional options or request structs for extensibility
10. Avoid parameter mutation (unless strictly required for performance)
11. Apply middleware for cross-cutting concerns
12. Keep handlers thin - defer to services
13. Use event-driven or hook patterns for extensibility
14. Use goroutine pools for high-concurrency dynamic tasks
15. Limit Must-functions to main.go initialization or guaranteed-safe inputs
16. Ensure infinite loop goroutines are cancellable via context
17. Handle all errors explicitly; do not ignore them
18. Close channels from the writer side
19. Use composable Validator interface for request validation

### ❌ Never Do:
1. Put business logic in handlers or main.go
2. Use global variables for dependencies
3. Forget context in service/repository methods
4. Use ORMs instead of raw SQL
5. Use string IDs instead of UUIDs
6. Return generic string errors
7. Expose sensitive fields (like passwords) in JSON
8. Write untestable code with tight coupling
9. Add too many positional parameters
10. Mutate input parameters (pointers) within functions without performance justification
11. Hardcode side effects in core business logic
12. Over-engineer simple solutions
13. Add unnecessary external dependencies
14. Create unbounded goroutines in hot paths
15. Use Must-prefix functions or panic helpers with user input or in request paths
16. Run infinite loop goroutines without a cancellation mechanism
17. Ignore errors or use `_` to suppress them
18. Close channels from the receiver side

---

**Remember**: Follow KISS principle first, then apply SOLID where it adds clear value. Prioritize testability, maintainability, and extensibility in all implementations.