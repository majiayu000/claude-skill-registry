---
name: dotnet-minimal-apis
description: Guide for building ASP.NET Core Minimal APIs with OpenAPI/Swagger integration in .NET 10
type: domain
enforcement: suggest
priority: medium
---

# ASP.NET Core Minimal APIs

This skill provides guidance for building **Minimal APIs** in ASP.NET Core .NET 10. Minimal APIs provide a simplified approach to building HTTP APIs with minimal dependencies and boilerplate.

## Table of Contents
1. [Overview](#overview)
2. [Project Structure](#project-structure)
3. [Basic Endpoints](#basic-endpoints)
4. [Route Groups](#route-groups)
5. [Parameter Binding](#parameter-binding)
6. [OpenAPI Integration](#openapi-integration)
7. [Best Practices](#best-practices)
8. [Quick Reference](#quick-reference)

---

## Overview

### What are Minimal APIs?

Minimal APIs are a simplified way to create HTTP APIs in ASP.NET Core without controllers. They provide:
- **Less code**: No controllers, no attribute routing
- **Fast development**: Define endpoints inline
- **Performance**: Lower overhead than MVC controllers
- **Ideal for**: Microservices, simple APIs, cloud-native apps

### When to Use Minimal APIs

**Use Minimal APIs when:**
- Building microservices
- Creating simple REST APIs
- Prototyping quickly
- Prioritizing performance

**Use MVC Controllers when:**
- Complex validation logic
- Heavy use of filters/middleware per endpoint
- Team prefers OOP patterns
- Large enterprise applications

---

## Project Structure

### ClaudeStack.API Project

This repository includes `src/ClaudeStack.API` demonstrating minimal API patterns.

**Current Program.cs structure:**
```csharp
using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

var builder = WebApplication.CreateBuilder(args);

// Add services
builder.Services.AddOpenApi();

var app = builder.Build();

// Configure middleware
if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();
}

app.UseHttpsRedirection();

// Define endpoints
app.MapGet("/weatherforecast", () => { /* ... */ })
   .WithName("GetWeatherForecast");

app.Run();
```

**Key components:**
1. `WebApplication.CreateBuilder(args)` - creates builder
2. `builder.Services` - dependency injection
3. `app.Build()` - builds application
4. `app.Map*()` - defines endpoints
5. `app.Run()` - starts server

---

## Basic Endpoints

### MapGet

**Simple GET endpoint:**
```csharp
app.MapGet("/hello", () => "Hello World!");
```

**With route parameters:**
```csharp
app.MapGet("/users/{id}", (int id) => $"User {id}");
```

**With query parameters:**
```csharp
app.MapGet("/search", (string? query) => $"Searching for: {query}");
```

**Async with return type:**
```csharp
app.MapGet("/users/{id}", async (int id, UserService service) =>
{
    var user = await service.GetUserAsync(id);
    return user is not null ? Results.Ok(user) : Results.NotFound();
});
```

### MapPost, MapPut, MapDelete

```csharp
app.MapPost("/users", (User user) => Results.Created($"/users/{user.Id}", user));
app.MapPut("/users/{id}", (int id, User user) => Results.NoContent());
app.MapDelete("/users/{id}", (int id) => Results.NoContent());
```

### Example from Project

From `src/ClaudeStack.API/Program.cs`:

```csharp
app.MapGet("/weatherforecast", () =>
{
    var forecast = Enumerable.Range(1, 5).Select(index =>
        new WeatherForecast
        (
            DateOnly.FromDateTime(DateTime.Now.AddDays(index)),
            Random.Shared.Next(-20, 55),
            summaries[Random.Shared.Next(summaries.Length)]
        ))
        .ToArray();
    return forecast;
})
.WithName("GetWeatherForecast");
```

**Key points:**
- Inline lambda
- Returns typed data (serialized as JSON)
- `.WithName()` for OpenAPI

---

## Route Groups

### Basic Route Group

Organize related endpoints:

```csharp
var users = app.MapGroup("/users");

users.MapGet("/", () => "All users");
users.MapGet("/{id}", (int id) => $"User {id}");
users.MapPost("/", (User user) => Results.Created($"/users/{user.Id}", user));
```

### Route Group with Prefix

```csharp
var api = app.MapGroup("/api/v1");

api.MapGet("/users", () => "All users");
api.MapGet("/products", () => "All products");
```

### Route Group with Filters

```csharp
var admin = app.MapGroup("/admin")
    .RequireAuthorization("AdminPolicy");

admin.MapGet("/users", () => "Admin: All users");
admin.MapDelete("/users/{id}", (int id) => Results.NoContent());
```

---

## Parameter Binding

### Binding Examples

```csharp
// Route parameters
app.MapGet("/users/{id}", (int id) => $"User {id}");

// Query string
app.MapGet("/search", (string? q, int page = 1) => $"{q}, Page {page}");

// Request body (JSON)
app.MapPost("/users", (User user) => Results.Created($"/users/{user.Id}", user));

// Dependency injection
app.MapGet("/users", (UserService service) => service.GetAllUsers());
// Register: builder.Services.AddScoped<UserService>();

// Multiple sources
app.MapPost("/users/{id}", (int id, User user, UserService service) =>
    service.UpdateUser(id, user));
```

---

## OpenAPI Integration

### Adding OpenAPI

This project uses OpenAPI (configured in Program.cs):

```csharp
// Add service
builder.Services.AddOpenApi();

// Map OpenAPI endpoint (development only)
if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();
}
```

**Access OpenAPI spec:** `https://localhost:5001/openapi/v1.json`

### Endpoint Metadata

**Naming endpoints:**
```csharp
app.MapGet("/users", () => "All users")
   .WithName("GetAllUsers");
```

**Adding descriptions:**
```csharp
app.MapGet("/users/{id}", (int id) => $"User {id}")
   .WithName("GetUser")
   .WithSummary("Get user by ID")
   .WithDescription("Returns a single user by their unique identifier");
```

**Adding tags:**
```csharp
app.MapGet("/users", () => "All users")
   .WithTags("Users");

app.MapGet("/products", () => "All products")
   .WithTags("Products");
```

### Response Types

```csharp
app.MapGet("/users/{id}", (int id) => Results.Ok(new User()))
   .Produces<User>(StatusCodes.Status200OK)
   .Produces(StatusCodes.Status404NotFound);
```

---

## Best Practices

### 1. Use Typed Results

**Prefer:**
```csharp
app.MapGet("/users/{id}", (int id) =>
    Results.Ok(user)
    // or Results.NotFound()
);
```

**Avoid:**
```csharp
app.MapGet("/users/{id}", (int id) => user); // Implicit 200 OK
```

### 2. Name All Endpoints

```csharp
app.MapGet("/users", () => "All users")
   .WithName("GetAllUsers");
```

Required for:
- URL generation
- OpenAPI documentation
- Testing

### 3. Organize with Route Groups

```csharp
var users = app.MapGroup("/users").WithTags("Users");
users.MapGet("/", GetAllUsers).WithName("GetAllUsers");
users.MapGet("/{id}", GetUser).WithName("GetUser");
users.MapPost("/", CreateUser).WithName("CreateUser");
```

### 4. Extract Handler Methods

**Instead of inline:**
```csharp
app.MapGet("/users", () => { /* 50 lines */ });
```

**Use local functions:**
```csharp
app.MapGet("/users", GetAllUsers);

static IResult GetAllUsers(UserService service)
{
    var users = service.GetAll();
    return Results.Ok(users);
}
```

### 5. Use Record Types

Perfect for DTOs:
```csharp
record User(int Id, string Name, string Email);
record CreateUserRequest(string Name, string Email);
```

ClaudeStack.API uses this pattern:
```csharp
record WeatherForecast(DateOnly Date, int TemperatureC, string Summary);
```

### 6. Explicit Using Statements

This project has ImplicitUsings disabled. Always include:
```csharp
using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
```

### 7. Validate Input

```csharp
app.MapPost("/users", (CreateUserRequest request) =>
{
    if (string.IsNullOrEmpty(request.Name))
        return Results.BadRequest("Name is required");

    if (string.IsNullOrEmpty(request.Email))
        return Results.BadRequest("Email is required");

    // Create user
    return Results.Created("/users/1", user);
});
```

### 8. Use Filters for Cross-Cutting Concerns

```csharp
app.MapGet("/admin/users", () => "Admin users")
   .RequireAuthorization("AdminPolicy");
```

---

## Quick Reference

### Endpoint Methods

```csharp
app.MapGet("/path", handler)       // GET
app.MapPost("/path", handler)      // POST
app.MapPut("/path", handler)       // PUT
app.MapPatch("/path", handler)     // PATCH
app.MapDelete("/path", handler)    // DELETE
app.MapMethods("/path", ["GET", "POST"], handler)  // Custom
```

### Results Helpers

```csharp
Results.Ok(value)                  // 200 OK
Results.Created("/path", value)    // 201 Created
Results.NoContent()                // 204 No Content
Results.BadRequest(error)          // 400 Bad Request
Results.NotFound()                 // 404 Not Found
Results.Problem(details)           // 500 Internal Server Error
```

### Endpoint Configuration

```csharp
.WithName("EndpointName")
.WithSummary("Short summary")
.WithDescription("Longer description")
.WithTags("Tag1", "Tag2")
.Produces<Type>(statusCode)
.RequireAuthorization(policy)
```

### Route Groups

```csharp
var group = app.MapGroup("/prefix");
group.MapGet("/path", handler);
```

### Parameter Binding Sources

```csharp
(int id)                    // Route parameter
(string? query)             // Query string
(User user)                 // Request body (JSON)
(HttpRequest request)       // HTTP request
(HttpContext context)       // HTTP context
(IService service)          // DI service
```

---

## Related Skills

- **dotnet-cli-essentials**: Running and building API projects
- **aspnet-configuration**: Configuring appsettings for APIs
- **mstest-testing-platform**: Testing minimal APIs

---

## Additional Resources

- [Minimal APIs Overview](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/minimal-apis/overview)
- [OpenAPI in ASP.NET Core](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/openapi/overview)
- [Minimal APIs Quick Reference](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/minimal-apis)
- [Route Groups](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/minimal-apis/route-handlers#route-groups)

---

## Version Information

- **.NET**: 10.0 RC 2
- **ASP.NET Core**: 10.0.0-rc.2.25502.107
- **OpenAPI Package**: Microsoft.AspNetCore.OpenApi 10.0.0-rc.2.25502.107

Minimal APIs are a stable feature as of .NET 6.0+. This project uses .NET 10 RC 2 patterns.
