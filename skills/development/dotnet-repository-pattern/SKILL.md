---
name: dotnet-repository-pattern
description: '.NET Repository 패턴과 Service Layer 구현'
---

# .NET Repository 패턴

데이터 접근 계층을 추상화하는 Repository 패턴 구현 가이드입니다.

## 1. 프로젝트 구조

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

## 2. Model 정의

```csharp
namespace MyApp.Models;

public sealed record User(int Id, string Name, string Email);
```

## 3. Repository 계층

### 3.1 인터페이스

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

### 3.2 구현체

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

## 4. Service 계층

### 4.1 인터페이스

```csharp
namespace MyApp.Services;

public interface IUserService
{
    Task<IReadOnlyList<User>> GetAllUsersAsync();
    Task<User?> GetUserByIdAsync(int id);
}
```

### 4.2 구현체

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

## 5. DI 등록

```csharp
var host = Host.CreateDefaultBuilder(args)
    .ConfigureServices(services =>
    {
        // Repository 등록
        services.AddSingleton<IUserRepository, UserRepository>();

        // Service 등록
        services.AddSingleton<IUserService, UserService>();

        services.AddSingleton<App>();
    })
    .Build();
```

## 6. Generic Repository (선택적)

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

## 7. 계층 구조

```
App (Presentation)
  ↓
Service Layer (비즈니스 로직)
  ↓
Repository Layer (데이터 접근)
  ↓
Data Source (DB, API, File 등)
```

## 8. 핵심 원칙

- Repository는 데이터 접근만 담당
- 비즈니스 로직은 Service에 작성
- 인터페이스로 추상화하여 테스트 용이성 확보
- Constructor Injection으로 의존성 주입
