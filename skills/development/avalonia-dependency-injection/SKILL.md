---
name: avalonia-dependency-injection
description: "AvaloniaUI에서 GenericHost와 DI 사용 패턴"
---

# 6.6 Dependency Injection 및 GenericHost 사용

AvaloniaUI에서도 WPF와 동일하게 GenericHost 패턴 적용

## 프로젝트 구조

templates 폴더에 .NET 9 AvaloniaUI 프로젝트 예제가 포함되어 있습니다.

```
templates/
├── AvaloniaDISample.App/           ← Avalonia Application Project
│   ├── Views/
│   │   ├── MainWindow.axaml
│   │   └── MainWindow.axaml.cs
│   ├── App.axaml
│   ├── App.axaml.cs
│   ├── Program.cs
│   ├── GlobalUsings.cs
│   └── AvaloniaDISample.App.csproj
└── AvaloniaDISample.ViewModels/    ← ViewModel Class Library (UI 프레임워크 독립)
    ├── MainViewModel.cs
    ├── GlobalUsings.cs
    └── AvaloniaDISample.ViewModels.csproj
```

## App.axaml.cs 예시:

```csharp
// App.axaml.cs
namespace MyApp;

using Avalonia;
using Avalonia.Controls.ApplicationLifetimes;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

public partial class App : Application
{
    private IHost? _host;

    public override void Initialize()
    {
        AvaloniaXamlLoader.Load(this);
    }

    public override void OnFrameworkInitializationCompleted()
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

                // Views 등록
                // Register Views
                services.AddSingleton<MainWindow>();
            })
            .Build();

        if (ApplicationLifetime is IClassicDesktopStyleApplicationLifetime desktop)
        {
            desktop.MainWindow = _host.Services.GetRequiredService<MainWindow>();
        }

        base.OnFrameworkInitializationCompleted();
    }
}
```

