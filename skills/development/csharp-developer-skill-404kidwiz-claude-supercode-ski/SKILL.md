---
name: csharp-developer
description: .NET 8 and C# 12 specialist with expertise in ASP.NET Core, EF Core, and modern enterprise development. Use when building C# applications, working with .NET, implementing ASP.NET Core APIs, or using Entity Framework.
---

# C# Developer

## Purpose
Provides expertise in modern C# and .NET development, including ASP.NET Core web applications, Entity Framework Core data access, and enterprise application patterns. Covers C# 12 features and .NET 8 best practices.

## When to Use
- Building C# applications with .NET 8
- Developing ASP.NET Core web APIs
- Implementing Entity Framework Core data access
- Using modern C# features (records, patterns, etc.)
- Building enterprise .NET applications
- Writing unit tests with xUnit/NUnit
- Implementing dependency injection patterns

## Quick Start
**Invoke this skill when:**
- Building C# applications with .NET 8
- Developing ASP.NET Core web APIs
- Implementing Entity Framework Core data access
- Using modern C# features
- Building enterprise .NET applications

**Do NOT invoke when:**
- Building cross-platform .NET MAUI apps (use dotnet-core-expert)
- Working with .NET Framework 4.8 (use dotnet-framework-4.8-expert)
- Building Windows desktop apps (use windows-app-developer)
- Azure-specific infrastructure (use azure-infra-engineer)

## Decision Framework
```
Project Type:
├── Web API → ASP.NET Core Minimal API or Controllers
├── Web App → Blazor or Razor Pages
├── Background service → Worker Service
├── Desktop → WPF, WinUI, or MAUI
└── Library → .NET Standard or .NET 8

Data Access:
├── SQL with ORM → Entity Framework Core
├── SQL with control → Dapper
├── NoSQL → MongoDB driver or Cosmos SDK
└── Multiple DBs → Repository pattern
```

## Core Workflows

### 1. ASP.NET Core API Development
1. Create project with appropriate template
2. Configure dependency injection
3. Implement domain models
4. Set up EF Core with migrations
5. Create controllers or minimal API endpoints
6. Add validation and error handling
7. Implement authentication/authorization
8. Add OpenAPI documentation

### 2. Entity Framework Core Setup
1. Define entity models
2. Configure DbContext
3. Set up relationships and constraints
4. Create initial migration
5. Implement repository pattern if needed
6. Add query optimization
7. Configure connection resilience

### 3. Testing Strategy
1. Set up xUnit or NUnit project
2. Create unit tests with mocks
3. Implement integration tests
4. Use WebApplicationFactory for API tests
5. Add test database fixtures
6. Configure CI test pipeline

## Best Practices
- Use records for DTOs and immutable data
- Leverage pattern matching for cleaner code
- Use nullable reference types
- Implement IAsyncDisposable for async cleanup
- Use primary constructors in C# 12
- Configure EF Core query splitting for includes

## Anti-Patterns
| Anti-Pattern | Problem | Correct Approach |
|--------------|---------|------------------|
| Service locator | Hidden dependencies | Constructor injection |
| Async void | Unhandled exceptions | async Task everywhere |
| N+1 queries | Performance issues | Use Include() or projection |
| Throwing from constructors | Hard to handle | Use factory methods |
| String-based config | Runtime errors | Strongly-typed options |
