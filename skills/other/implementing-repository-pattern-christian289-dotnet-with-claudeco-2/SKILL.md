---
name: implementing-repository-pattern
description: "Implements the Repository pattern with Service Layer for data access abstraction in .NET. Use when separating data access logic from business logic or building testable data layers."
---

# .NET Repository Pattern

A guide for implementing the Repository pattern that abstracts the data access layer.

## 1. Project Structure

```
MyApp/
├── Program.cs
├── App.cs
├── Models/
│   └── User.cs
├── Repositories/
│   ├── IUserRepository.cs
│   └── UserRepository.cs
├── Services/
│   ├── IUserService.cs
│   └── UserService.cs
└── GlobalUsings.cs
```

## 2. Model Definition

```csharp
namespace MyApp.Models;

public sealed record User(int Id, string Name, string Email);
```

## 3. Repository Layer

### 3.1 Interface

```csharp
namespace MyApp.Repositories;

public interface IUserRepository
{
    Task<List<User>> GetAllAsync();
    Task<User?> GetByIdAsync(int id);
    Task AddAsync(User user);
    Task UpdateAsync(User user);
    Task DeleteAsync(int id);
}
```

### 3.2 Implementation

```csharp
namespace MyApp.Repositories;

public sealed class UserRepository : IUserRepository
{
    private readonly List<User> _users = [];

    public Task<List<User>> GetAllAsync()
    {
        return Task.FromResult(_users.ToList());
    }

    public Task<User?> GetByIdAsync(int id)
    {
        return Task.FromResult(_users.FirstOrDefault(u => u.Id == id));
    }

    public Task AddAsync(User user)
    {
        _users.Add(user);
        return Task.CompletedTask;
    }

    public Task UpdateAsync(User user)
    {
        var index = _users.FindIndex(u => u.Id == user.Id);
        if (index >= 0) _users[index] = user;
        return Task.CompletedTask;
    }

    public Task DeleteAsync(int id)
    {
        _users.RemoveAll(u => u.Id == id);
        return Task.CompletedTask;
    }
}
```

## 4. Service Layer

### 4.1 Interface

```csharp
namespace MyApp.Services;

public interface IUserService
{
    Task<IReadOnlyList<User>> GetAllUsersAsync();
    Task<User?> GetUserByIdAsync(int id);
}
```

### 4.2 Implementation

```csharp
namespace MyApp.Services;

public sealed class UserService(IUserRepository repository) : IUserService
{
    private readonly IUserRepository _repository = repository;

    public async Task<IReadOnlyList<User>> GetAllUsersAsync()
    {
        var users = await _repository.GetAllAsync();
        return users.AsReadOnly();
    }

    public Task<User?> GetUserByIdAsync(int id)
    {
        return _repository.GetByIdAsync(id);
    }
}
```

## 5. DI Registration

```csharp
var host = Host.CreateDefaultBuilder(args)
    .ConfigureServices(services =>
    {
        // Register Repository
        services.AddSingleton<IUserRepository, UserRepository>();

        // Register Service
        services.AddSingleton<IUserService, UserService>();

        services.AddSingleton<App>();
    })
    .Build();
```

## 6. Generic Repository (Optional)

```csharp
public interface IRepository<T> where T : class
{
    Task<List<T>> GetAllAsync();
    Task<T?> GetByIdAsync(int id);
    Task AddAsync(T entity);
    Task UpdateAsync(T entity);
    Task DeleteAsync(int id);
}
```

## 7. Layer Structure

```
App (Presentation)
  ↓
Service Layer (Business Logic)
  ↓
Repository Layer (Data Access)
  ↓
Data Source (DB, API, File, etc.)
```

## 8. Core Principles

- Repository handles data access only
- Business logic goes in Service
- Abstract with interfaces for testability
- Use Constructor Injection for dependencies

