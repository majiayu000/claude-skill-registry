---
name: c-sharp
description: Guidelines for C# development including Blazor, Unity game development, and .NET backend best practices
---

# C# Development Guidelines

You are an expert in C# development with deep knowledge of .NET, Blazor, Unity, and modern C# language features.

## Code Style and Structure

- Write concise, idiomatic C# code with accurate examples
- Follow .NET and C# conventions and best practices
- Use object-oriented and functional programming patterns as appropriate
- Prefer LINQ and lambda expressions for collection operations
- Use descriptive variable and method names (e.g., `IsUserLoggedIn`, `GetUserById`)
- Structure files according to .NET conventions (Controllers, Models, Services, etc.)

## Naming Conventions

- Use PascalCase for class names, method names, and public properties
- Use camelCase for local variables and private fields
- Use SCREAMING_SNAKE_CASE for constants
- Prefix interfaces with "I" (e.g., `IUserService`)
- Prefix private fields with underscore (e.g., `_userRepository`)

## C# Language Features

### C# 10+ Features
- Use file-scoped namespaces for cleaner code
- Use global usings for common namespaces
- Leverage records for immutable data types
- Use pattern matching for type checking and deconstruction
- Use nullable reference types with proper annotations

### Modern Syntax
- Use expression-bodied members for simple methods and properties
- Use target-typed new expressions (`new()`)
- Use switch expressions for concise conditional logic
- Use string interpolation over string concatenation

## Error Handling

- Use try-catch blocks for expected exceptions
- Create custom exception classes for domain-specific errors
- Use `ArgumentNullException.ThrowIfNull()` for parameter validation
- Implement the Result pattern for operation outcomes when appropriate
- Log exceptions with context information

## API Design

- Follow RESTful conventions for web APIs
- Use DTOs for data transfer between layers
- Implement proper HTTP status codes
- Use action filters for cross-cutting concerns
- Version APIs appropriately

## Performance

- Use `async/await` for I/O-bound operations
- Implement caching where appropriate
- Use `StringBuilder` for string concatenation in loops
- Avoid boxing/unboxing with generics
- Use `Span<T>` and `Memory<T>` for high-performance scenarios

## Dependency Injection

- Use constructor injection for dependencies
- Register services with appropriate lifetimes (Scoped, Transient, Singleton)
- Use interfaces for service abstractions
- Configure DI in `Program.cs` or `Startup.cs`

## Testing

- Write unit tests using xUnit or NUnit
- Use Moq or NSubstitute for mocking
- Follow Arrange-Act-Assert pattern
- Aim for high test coverage on business logic
- Use FluentAssertions for readable assertions

## Security

- Validate all user inputs
- Use parameterized queries or Entity Framework to prevent SQL injection
- Implement proper authentication and authorization
- Store secrets in configuration (User Secrets, Azure Key Vault)
- Use HTTPS for all communications

## Blazor-Specific Guidelines

- Use component-based architecture
- Implement proper state management
- Use cascading parameters for shared state
- Optimize rendering with `@key` and virtualization
- Handle component lifecycle events appropriately

## Unity-Specific Guidelines

- Use MonoBehaviour for game object behaviors
- Implement ScriptableObjects for data containers
- Follow the Component pattern for modularity
- Use coroutines for time-based operations
- Implement object pooling for frequently instantiated objects
