---
name: dependency-injection
description: "Microsoft.Extensions.DependencyInjection과 GenericHost를 사용한 의존성 주입 패턴"
---

# Dependency Injection 및 GenericHost 사용

.NET 프로젝트에서 Dependency Injection과 GenericHost를 사용하는 방법에 대한 가이드입니다.

## 프로젝트 구조

templates 폴더에 .NET 9 WPF 프로젝트 예제가 포함되어 있습니다.

```
templates/
├── WpfDISample.App/           ← WPF Application Project
│   ├── Views/
│   │   ├── MainWindow.xaml
│   │   └── MainWindow.xaml.cs
│   ├── App.xaml
│   ├── App.xaml.cs
│   ├── GlobalUsings.cs
│   └── WpfDISample.App.csproj
└── WpfDISample.ViewModels/    ← ViewModel Class Library (UI 프레임워크 독립)
    ├── MainViewModel.cs
    ├── GlobalUsings.cs
    └── WpfDISample.ViewModels.csproj
```

## 핵심 원칙

- **Microsoft.Extensions.DependencyInjection을 사용하여 의존성 주입 구현**
- **GenericHost (Microsoft.Extensions.Hosting)를 기본으로 사용**
- **Constructor Injection을 통한 서비스 주입 방식 적용**

## Console 및 일반 프로젝트 - Program.cs

```csharp
// Program.cs
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

// GenericHost를 사용한 DI 설정
// Configure DI using GenericHost
var host = Host.CreateDefaultBuilder(args)
    .ConfigureServices((context, services) =>
    {
        // 서비스 등록
        // Register services
        services.AddSingleton<IUserRepository, UserRepository>();
        services.AddScoped<IUserService, UserService>();
        services.AddTransient<IEmailService, EmailService>();

        // 메인 애플리케이션 서비스 등록
        // Register main application service
        services.AddSingleton<App>();
    })
    .Build();

// ServiceProvider를 통해 서비스 가져오기
// Get service through ServiceProvider
var app = host.Services.GetRequiredService<App>();
await app.RunAsync();

// 애플리케이션 클래스 - Constructor Injection
// Application class - Constructor Injection
public sealed class App(IUserService userService, IEmailService emailService)
{
    private readonly IUserService _userService = userService;
    private readonly IEmailService _emailService = emailService;

    public async Task RunAsync()
    {
        // 주입된 서비스 사용
        // Use injected services
        var users = await _userService.GetAllUsersAsync();

        foreach (var user in users)
        {
            await _emailService.SendWelcomeEmailAsync(user.Email);
        }
    }
}
```

## WPF 프로젝트 - App.xaml.cs

```csharp
// App.xaml.cs
namespace MyApp;

using System.Windows;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

public partial class App : Application
{
    private readonly IHost _host;

    public App()
    {
        // GenericHost 생성 및 서비스 등록
        // Create GenericHost and register services
        _host = Host.CreateDefaultBuilder()
            .ConfigureServices((context, services) =>
            {
                // Services 등록
                // Register services
                services.AddSingleton<IUserRepository, UserRepository>();
                services.AddSingleton<IUserService, UserService>();
                services.AddTransient<IDialogService, DialogService>();

                // ViewModels 등록
                // Register ViewModels
                services.AddTransient<MainViewModel>();
                services.AddTransient<SettingsViewModel>();

                // Views 등록
                // Register Views
                services.AddSingleton<MainWindow>();
            })
            .Build();
    }

    protected override async void OnStartup(StartupEventArgs e)
    {
        await _host.StartAsync();

        // MainWindow를 ServiceProvider로부터 가져오기
        // Get MainWindow from ServiceProvider
        var mainWindow = _host.Services.GetRequiredService<MainWindow>();
        mainWindow.Show();

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

## MainWindow.xaml.cs - Constructor Injection

```csharp
// MainWindow.xaml.cs
namespace MyApp;

using System.Windows;

public partial class MainWindow : Window
{
    // Constructor Injection을 통한 ViewModel 주입
    // ViewModel injection through Constructor Injection
    public MainWindow(MainViewModel viewModel)
    {
        InitializeComponent();
        DataContext = viewModel;
    }
}
```

## ViewModel - Constructor Injection

```csharp
// ViewModels/MainViewModel.cs
namespace MyApp.ViewModels;

using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;

public sealed partial class MainViewModel : ObservableObject
{
    private readonly IUserService _userService;
    private readonly IDialogService _dialogService;

    // Constructor Injection
    public MainViewModel(IUserService userService, IDialogService dialogService)
    {
        _userService = userService;
        _dialogService = dialogService;

        LoadDataAsync();
    }

    [ObservableProperty]
    private ObservableCollection<User> users = [];

    [RelayCommand]
    private async Task LoadDataAsync()
    {
        try
        {
            var userList = await _userService.GetAllUsersAsync();
            Users = new ObservableCollection<User>(userList);
        }
        catch (Exception ex)
        {
            await _dialogService.ShowErrorAsync("오류 발생", ex.Message);
            // Error occurred
        }
    }
}
```

## 서비스 Lifetime 규칙

### Singleton
애플리케이션 전체에서 하나의 인스턴스만 생성
- Repository, 전역 상태 관리 서비스
- `services.AddSingleton<IUserRepository, UserRepository>()`

### Scoped
요청(Scope)당 하나의 인스턴스 생성
- DbContext, 트랜잭션 단위 서비스
- `services.AddScoped<IUserService, UserService>()`
- ⚠️ WPF에서는 일반적으로 사용하지 않음 (Web 애플리케이션에서 주로 사용)

### Transient
요청할 때마다 새 인스턴스 생성
- ViewModel, 일회성 서비스
- `services.AddTransient<MainViewModel>()`

## ServiceProvider 직접 사용 (권장하지 않음)

### 안티패턴: Service Locator

```csharp
// Service Locator 패턴 (안티패턴)
// Service Locator pattern (anti-pattern)
public sealed class SomeClass
{
    private readonly IServiceProvider _serviceProvider;

    public SomeClass(IServiceProvider serviceProvider)
    {
        _serviceProvider = serviceProvider;
    }

    public void DoSomething()
    {
        // ⚠️ 권장하지 않음: ServiceProvider를 직접 사용
        // Not recommended: Using ServiceProvider directly
        var service = _serviceProvider.GetRequiredService<IUserService>();
    }
}
```

### 권장: Constructor Injection

```csharp
// 올바른 방법: Constructor Injection 사용
// Correct way: Use Constructor Injection
public sealed class SomeClass
{
    private readonly IUserService _userService;

    public SomeClass(IUserService userService)
    {
        _userService = userService;
    }

    public void DoSomething()
    {
        // ✅ 권장: Constructor Injection으로 주입받은 서비스 사용
        // Recommended: Use service injected through Constructor Injection
        _userService.GetAllUsersAsync();
    }
}
```

## 필수 NuGet 패키지

```xml
<ItemGroup>
  <PackageReference Include="Microsoft.Extensions.DependencyInjection" Version="9.0.0" />
  <PackageReference Include="Microsoft.Extensions.Hosting" Version="9.0.0" />
</ItemGroup>
```
