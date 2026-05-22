---
name: wpf-project-structure
description: "WPF 솔루션 및 프로젝트 구조 설계 가이드 (Clean Architecture 기반)"
---

# WPF 솔루션 및 프로젝트 구조

Clean Architecture 기반 WPF 프로젝트의 솔루션 및 프로젝트 구조 설계 가이드입니다.

## 템플릿 프로젝트

templates 폴더에 .NET 9 기반 Clean Architecture WPF 솔루션 예제가 포함되어 있습니다.

```
templates/
├── GameDataTool.sln                    ← 솔루션 파일
├── Directory.Build.props               ← 공통 빌드 설정
├── src/
│   ├── GameDataTool.Domain/            ← 🔵 Core - 순수 도메인 모델
│   ├── GameDataTool.Application/       ← 🟢 Core - Use Cases
│   ├── GameDataTool.Infrastructure/    ← 🟡 Infrastructure - 외부 시스템
│   ├── GameDataTool.ViewModels/        ← 🟠 Presentation - ViewModel
│   ├── GameDataTool.WpfServices/       ← 🟠 Presentation - WPF 서비스
│   ├── GameDataTool.UI/                ← 🔴 Presentation - Custom Controls
│   └── GameDataTool.WpfApp/            ← 🔴 Composition Root
└── tests/
    ├── GameDataTool.Domain.Tests/
    ├── GameDataTool.Application.Tests/
    └── GameDataTool.ViewModels.Tests/
```

## 솔루션 구조 원칙

**솔루션 이름은 애플리케이션 이름**
- 예시: `GameDataTool` 솔루션 = 실행 가능한 .NET Assembly 이름

## 프로젝트 구조 (Clean Architecture)

```
SolutionName/
├── src/
│   │
│   │  ══════════════ Core (의존성 없음) ══════════════
│   │
│   ├── SolutionName.Domain              // 🔵 Entities - 순수 도메인 모델
│   │   ├── Entities/
│   │   ├── ValueObjects/
│   │   └── Interfaces/                  //    - 도메인 서비스 인터페이스만
│   │
│   ├── SolutionName.Application         // 🟢 Use Cases - 비즈니스 로직 조율
│   │   ├── Interfaces/                  //    - IRepository, IExternalService 등
│   │   ├── Services/                    //    - 애플리케이션 서비스
│   │   └── DTOs/
│   │
│   │  ══════════════ Infrastructure ══════════════
│   │
│   ├── SolutionName.Infrastructure      // 🟡 외부 시스템 구현
│   │   ├── Persistence/                 //    - 데이터 접근 구현
│   │   ├── FileSystem/                  //    - 파일 시스템 접근
│   │   └── ExternalServices/            //    - HTTP, API 등
│   │
│   │  ══════════════ Presentation (WPF) ══════════════
│   │
│   ├── SolutionName.ViewModels          // 🟠 ViewModels (Interface Adapter 역할)
│   │   └── (Application에만 의존)
│   │
│   ├── SolutionName.WpfServices         // 🟠 WPF 전용 서비스
│   │   └── (Dialog, Navigation 등)
│   │
│   ├── SolutionName.UI                  // 🔴 Custom Controls & Styles
│   │
│   └── SolutionName.WpfApp              // 🔴 Composition Root (진입점)
│       └── App.xaml.cs                  //    - DI 설정, 모든 구현체 연결
│
└── tests/
    ├── SolutionName.Domain.Tests
    ├── SolutionName.Application.Tests
    └── SolutionName.ViewModels.Tests
```

## 프로젝트 타입별 역할

### Core Layer (의존성 없음)

| 프로젝트 | 역할 | 포함 내용 |
|---------|------|----------|
| `.Domain` | 🔵 Entities | 순수 도메인 모델, ValueObjects, 도메인 인터페이스 |
| `.Application` | 🟢 Use Cases | 비즈니스 로직 조율, IRepository/IService 인터페이스, DTOs |

### Infrastructure Layer

| 프로젝트 | 역할 | 포함 내용 |
|---------|------|----------|
| `.Infrastructure` | 🟡 외부 시스템 | Repository 구현, 파일 시스템, HTTP/API 클라이언트 |

### Presentation Layer (WPF)

| 프로젝트 | 역할 | 포함 내용 |
|---------|------|----------|
| `.ViewModels` | 🟠 Interface Adapter | MVVM ViewModel (Application에만 의존, WPF 참조 X) |
| `.WpfServices` | 🟠 WPF 서비스 | DialogService, NavigationService, WindowService |
| `.UI` | 🔴 Custom Controls | ResourceDictionary, CustomControl, Themes |
| `.WpfApp` | 🔴 Composition Root | App.xaml, DI 설정, Views, 진입점 |

## 프로젝트 의존성 계층

```
                    ┌─────────────────────────────────────┐
                    │         SolutionName.WpfApp         │  ← Composition Root
                    │      (모든 프로젝트 참조, DI 설정)      │
                    └─────────────────────────────────────┘
                                      │
          ┌───────────────────────────┼───────────────────────────┐
          ▼                           ▼                           ▼
┌─────────────────┐       ┌─────────────────────┐       ┌─────────────────┐
│  .ViewModels    │       │   .Infrastructure   │       │  .WpfServices   │
│  (Application   │       │   (Application 참조) │       │  (Application   │
│     참조)        │       │                     │       │     참조)        │
└────────┬────────┘       └──────────┬──────────┘       └────────┬────────┘
         │                           │                           │
         └───────────────────────────┼───────────────────────────┘
                                     ▼
                    ┌─────────────────────────────────────┐
                    │       SolutionName.Application      │  ← Use Cases
                    │         (Domain만 참조)              │
                    └─────────────────────────────────────┘
                                      │
                                      ▼
                    ┌─────────────────────────────────────┐
                    │         SolutionName.Domain         │  ← Core (의존성 없음)
                    │           (참조 없음)                │
                    └─────────────────────────────────────┘
```

## 각 레이어 상세 설명

### Domain Layer (순수 도메인)

```csharp
// Domain/Entities/User.cs
namespace GameDataTool.Domain.Entities;

public sealed class User
{
    public Guid Id { get; init; }
    public string Name { get; private set; } = string.Empty;
    public Email Email { get; private set; } = null!;

    public void UpdateName(string name)
    {
        // 도메인 비즈니스 규칙 검증
        // Domain business rule validation
        if (string.IsNullOrWhiteSpace(name))
            throw new DomainException("이름은 필수입니다.");
            // Name is required.

        Name = name;
    }
}
```

```csharp
// Domain/ValueObjects/Email.cs
namespace GameDataTool.Domain.ValueObjects;

public sealed record Email
{
    public string Value { get; }

    public Email(string value)
    {
        if (!IsValid(value))
            throw new DomainException("유효하지 않은 이메일 형식입니다.");
            // Invalid email format.

        Value = value;
    }

    private static bool IsValid(string email) =>
        !string.IsNullOrWhiteSpace(email) && email.Contains('@');
}
```

### Application Layer (Use Cases)

```csharp
// Application/Interfaces/IUserRepository.cs
namespace GameDataTool.Application.Interfaces;

public interface IUserRepository
{
    Task<User?> GetByIdAsync(Guid id, CancellationToken cancellationToken = default);
    Task<IReadOnlyList<User>> GetAllAsync(CancellationToken cancellationToken = default);
    Task AddAsync(User user, CancellationToken cancellationToken = default);
    Task UpdateAsync(User user, CancellationToken cancellationToken = default);
}
```

```csharp
// Application/Services/UserService.cs
namespace GameDataTool.Application.Services;

public sealed class UserService(IUserRepository userRepository)
{
    private readonly IUserRepository _userRepository = userRepository;

    public async Task<UserDto?> GetUserAsync(Guid id, CancellationToken cancellationToken = default)
    {
        var user = await _userRepository.GetByIdAsync(id, cancellationToken);
        return user is null ? null : new UserDto(user.Id, user.Name, user.Email.Value);
    }

    public async Task UpdateUserNameAsync(Guid id, string newName, CancellationToken cancellationToken = default)
    {
        var user = await _userRepository.GetByIdAsync(id, cancellationToken)
            ?? throw new NotFoundException("사용자를 찾을 수 없습니다.");
            // User not found.

        user.UpdateName(newName);
        await _userRepository.UpdateAsync(user, cancellationToken);
    }
}
```

```csharp
// Application/DTOs/UserDto.cs
namespace GameDataTool.Application.DTOs;

public sealed record UserDto(Guid Id, string Name, string Email);
```

### Infrastructure Layer (외부 시스템 구현)

```csharp
// Infrastructure/Persistence/UserRepository.cs
namespace GameDataTool.Infrastructure.Persistence;

public sealed class UserRepository(AppDbContext dbContext) : IUserRepository
{
    private readonly AppDbContext _dbContext = dbContext;

    public async Task<User?> GetByIdAsync(Guid id, CancellationToken cancellationToken = default) =>
        await _dbContext.Users.FindAsync([id], cancellationToken);

    public async Task<IReadOnlyList<User>> GetAllAsync(CancellationToken cancellationToken = default) =>
        await _dbContext.Users.ToListAsync(cancellationToken);

    public async Task AddAsync(User user, CancellationToken cancellationToken = default)
    {
        await _dbContext.Users.AddAsync(user, cancellationToken);
        await _dbContext.SaveChangesAsync(cancellationToken);
    }

    public async Task UpdateAsync(User user, CancellationToken cancellationToken = default)
    {
        _dbContext.Users.Update(user);
        await _dbContext.SaveChangesAsync(cancellationToken);
    }
}
```

### ViewModels Layer (Presentation - Application만 의존)

```csharp
// ViewModels/UserViewModel.cs
namespace GameDataTool.ViewModels;

public sealed partial class UserViewModel(UserService userService) : ObservableObject
{
    private readonly UserService _userService = userService;

    [ObservableProperty] private string _userName = string.Empty;
    [ObservableProperty] private string _userEmail = string.Empty;

    [RelayCommand]
    private async Task LoadUserAsync(Guid userId)
    {
        var user = await _userService.GetUserAsync(userId);
        if (user is null) return;

        UserName = user.Name;
        UserEmail = user.Email;
    }
}
```

### WpfApp Layer (Composition Root - DI 설정)

```csharp
// WpfApp/App.xaml.cs
namespace GameDataTool.WpfApp;

public partial class App : Application
{
    private readonly IHost _host;

    public App()
    {
        _host = Host.CreateDefaultBuilder()
            .ConfigureServices((context, services) =>
            {
                // Domain - 등록 불필요 (순수 모델)
                // Domain - No registration needed (pure models)

                // Application Layer
                services.AddTransient<UserService>();

                // Infrastructure Layer
                services.AddDbContext<AppDbContext>();
                services.AddScoped<IUserRepository, UserRepository>();

                // Presentation Layer
                services.AddTransient<UserViewModel>();
                services.AddTransient<MainViewModel>();

                // WPF Services
                services.AddSingleton<IDialogService, DialogService>();
                services.AddSingleton<INavigationService, NavigationService>();

                // Views
                services.AddSingleton<MainWindow>();
            })
            .Build();
    }

    protected override async void OnStartup(StartupEventArgs e)
    {
        await _host.StartAsync();
        _host.Services.GetRequiredService<MainWindow>().Show();
        base.OnStartup(e);
    }

    protected override async void OnExit(ExitEventArgs e)
    {
        using (_host)
        {
            await _host.StopAsync();
        }
        base.OnExit(e);
    }
}
```

## 실제 폴더 구조 예시

```
GameDataTool/
├── src/
│   ├── GameDataTool.Domain/
│   │   ├── Entities/
│   │   │   ├── User.cs
│   │   │   └── GameData.cs
│   │   ├── ValueObjects/
│   │   │   ├── Email.cs
│   │   │   └── GameVersion.cs
│   │   ├── Interfaces/
│   │   │   └── IDomainEventPublisher.cs
│   │   ├── Exceptions/
│   │   │   └── DomainException.cs
│   │   ├── GlobalUsings.cs
│   │   └── GameDataTool.Domain.csproj
│   │
│   ├── GameDataTool.Application/
│   │   ├── Interfaces/
│   │   │   ├── IUserRepository.cs
│   │   │   ├── IGameDataRepository.cs
│   │   │   └── IFileExportService.cs
│   │   ├── Services/
│   │   │   ├── UserService.cs
│   │   │   └── GameDataService.cs
│   │   ├── DTOs/
│   │   │   ├── UserDto.cs
│   │   │   └── GameDataDto.cs
│   │   ├── Exceptions/
│   │   │   └── NotFoundException.cs
│   │   ├── GlobalUsings.cs
│   │   └── GameDataTool.Application.csproj
│   │
│   ├── GameDataTool.Infrastructure/
│   │   ├── Persistence/
│   │   │   ├── AppDbContext.cs
│   │   │   ├── UserRepository.cs
│   │   │   └── GameDataRepository.cs
│   │   ├── FileSystem/
│   │   │   └── ExcelExportService.cs
│   │   ├── ExternalServices/
│   │   │   └── ApiClient.cs
│   │   ├── GlobalUsings.cs
│   │   └── GameDataTool.Infrastructure.csproj
│   │
│   ├── GameDataTool.ViewModels/
│   │   ├── MainViewModel.cs
│   │   ├── UserViewModel.cs
│   │   ├── GameDataViewModel.cs
│   │   ├── GlobalUsings.cs
│   │   └── GameDataTool.ViewModels.csproj
│   │
│   ├── GameDataTool.WpfServices/
│   │   ├── DialogService.cs
│   │   ├── NavigationService.cs
│   │   ├── WindowService.cs
│   │   ├── GlobalUsings.cs
│   │   └── GameDataTool.WpfServices.csproj
│   │
│   ├── GameDataTool.UI/
│   │   ├── Themes/
│   │   │   ├── Generic.xaml
│   │   │   └── CustomButton.xaml
│   │   ├── CustomControls/
│   │   │   └── CustomButton.cs
│   │   ├── Properties/
│   │   │   └── AssemblyInfo.cs
│   │   └── GameDataTool.UI.csproj
│   │
│   └── GameDataTool.WpfApp/
│       ├── Views/
│       │   ├── MainWindow.xaml
│       │   ├── MainWindow.xaml.cs
│       │   ├── UserView.xaml
│       │   └── UserView.xaml.cs
│       ├── App.xaml
│       ├── App.xaml.cs
│       ├── Mappings.xaml
│       ├── GlobalUsings.cs
│       └── GameDataTool.WpfApp.csproj
│
├── tests/
│   ├── GameDataTool.Domain.Tests/
│   │   ├── Entities/
│   │   │   └── UserTests.cs
│   │   └── GameDataTool.Domain.Tests.csproj
│   │
│   ├── GameDataTool.Application.Tests/
│   │   ├── Services/
│   │   │   └── UserServiceTests.cs
│   │   └── GameDataTool.Application.Tests.csproj
│   │
│   └── GameDataTool.ViewModels.Tests/
│       ├── UserViewModelTests.cs
│       └── GameDataTool.ViewModels.Tests.csproj
│
├── GameDataTool.sln
└── Directory.Build.props
```

## 참조 어셈블리 규칙

### Domain 프로젝트
- ❌ 어떤 프로젝트도 참조하지 않음
- ✅ 순수 C# BCL만 사용

### Application 프로젝트
- ✅ Domain만 참조
- ❌ Infrastructure, Presentation 참조 금지

### Infrastructure 프로젝트
- ✅ Domain, Application 참조
- ✅ 외부 NuGet 패키지 사용 가능 (EF Core, HttpClient 등)

### ViewModels 프로젝트
- ✅ Application만 참조
- ❌ WPF 어셈블리 참조 금지 (WindowsBase, PresentationFramework 등)
- ✅ CommunityToolkit.Mvvm 사용 가능

### WpfApp 프로젝트 (Composition Root)
- ✅ 모든 프로젝트 참조
- ✅ DI 컨테이너에서 모든 구현체 연결

## Clean Architecture 장점

1. **독립성**: Core 레이어는 외부 프레임워크에 독립적
2. **테스트 용이성**: 각 레이어를 독립적으로 테스트 가능
3. **유지보수성**: 변경 영향 범위가 명확함
4. **유연성**: Infrastructure 교체 용이 (DB, API 등)
