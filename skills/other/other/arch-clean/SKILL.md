---
name: arch-clean
cluster: se-architecture
description: "Clean/hexagonal architecture: ports/adapters, dependency inversion, use cases, entities, testability"
tags: ["clean-architecture","hexagonal","ports-adapters","architecture"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "clean architecture hexagonal ports adapters use case dependency inversion"
---

# arch-clean

## Purpose
This skill implements Clean Architecture principles in codebases, focusing on hexagonal patterns with ports/adapters, dependency inversion, use cases, entities, and testability. It refactors or generates code to enforce separation of concerns, making systems modular and easier to test.

## When to Use
Use this skill when refactoring monolithic apps to improve maintainability, starting new projects requiring high testability, or integrating external dependencies without tight coupling. Apply it in scenarios with complex business logic, such as e-commerce backends, or when adapting legacy code to modern architectures like microservices.

## Key Capabilities
- Generate port interfaces for adapters, ensuring dependency inversion (e.g., defines contracts like `interface UserPort { fetchUser(id: string): User; }`).
- Create use case classes that orchestrate entities and ports, promoting single responsibility.
- Invert dependencies by wrapping external libraries in adapters, e.g., converting a direct database call to a port implementation.
- Enforce testability by structuring code for unit testing, such as mocking ports in use cases.
- Validate architecture rules, like checking that inner layers don't depend on outer ones, via static analysis.

## Usage Patterns
Invoke this skill via OpenClaw's CLI for quick refactoring or through API for automated pipelines. Start by analyzing the codebase with a scan command, then apply transformations. For scripts, pipe outputs to build tools like Make or Gradle. Always specify the target directory and language (e.g., TypeScript or Java) to avoid defaults. Use in CI/CD for pre-commit hooks to enforce architecture.

## Common Commands/API
Use the OpenClaw CLI with subcommands prefixed by `arch-clean`. Authentication requires setting `$OPENCLAW_API_KEY` as an environment variable.

- **Generate a port interface:**
  ```
  openclaw arch-clean generate-port --name UserPort --methods "fetchUser(id: string)" --lang ts
  ```
  This creates a file like `UserPort.ts` with the interface.

- **Invert dependencies in a module:**
  ```
  openclaw arch-clean invert-dep --path src/services --adapter DatabaseAdapter
  ```
  Scans the specified path and wraps dependencies, e.g., replacing direct imports with adapter calls.

- **Create a use case:**
  ```
  openclaw arch-clean create-usecase --name FetchUser --ports UserPort --entities User
  ```
  Generates a class like `FetchUserUseCase.ts` with injected ports.

API endpoints for programmatic use:
- POST /api/arch-clean/generate: Body { "type": "port", "name": "UserPort", "methods": ["fetchUser(id: string)"] }, requires `$OPENCLAW_API_KEY` in headers.
- PUT /api/arch-clean/invert: Body { "path": "src/services", "adapter": "DatabaseAdapter" }.

Config formats: Use JSON files for custom rules, e.g., `.openclaw-arch.json` with { "layers": { "domain": ["entities", "usecases"], "adapters": ["http", "db"] } }.

## Integration Notes
Integrate by adding OpenClaw as a dependency in your project (e.g., npm install openclaw or via Docker image). Set `$OPENCLAW_API_KEY` for authenticated requests. For IDE plugins, configure via settings like { "arch-clean": { "defaultLang": "ts", "excludePaths": ["tests/**"] } }. Combine with linters like ESLint by piping output, e.g., `openclaw arch-clean scan | eslint --fix`. Ensure your codebase uses a supported structure, such as folders for "domain", "application", and "infrastructure", to match hexagonal patterns.

## Error Handling
Check command outputs for errors; CLI returns non-zero exit codes with JSON error messages, e.g., { "error": "Dependency not inverted: invalid path" }. For API, expect HTTP 4xx/5xx responses with bodies like { "code": 400, "message": "Missing required field: methods" }. Handle by wrapping calls in try-catch blocks, e.g.:
```
try {
  const response = await fetch('/api/arch-clean/generate', { headers: { 'X-API-Key': process.env.OPENCLAW_API_KEY } });
  if (!response.ok) throw new Error(response.statusText);
} catch (error) {
  console.error('Arch error:', error.message);
}
```
Retry transient errors (e.g., network issues) up to 3 times with exponential backoff.

## Usage Examples
1. **Refactor a simple service to use ports:** For a Node.js app, run `openclaw arch-clean invert-dep --path src/userService.js --adapter HttpAdapter`. This transforms a direct HTTP call into a port, e.g., changing `axios.get('/user')` to `this.userPort.fetchUser(id)`, improving testability by allowing mocks.

2. **Generate a use case for business logic:** In a Java project, execute `openclaw arch-clean create-usecase --name OrderProcessor --ports PaymentPort --entities Order`. This produces `OrderProcessor.java` with a method like `public void process(Order order) { this.paymentPort.charge(order); }`, enabling dependency injection for better architecture.

## Graph Relationships
- Related to: se-architecture cluster (e.g., links to skills like code-refactor for broader refactoring).
- Depends on: ports-adapters tag (connects to hexagonal-architecture for adapter implementations).
- Conflicts with: monolithic patterns (avoids tight couplings in legacy systems).
