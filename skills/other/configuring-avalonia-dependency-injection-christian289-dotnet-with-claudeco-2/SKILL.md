---
name: configuring-avalonia-dependency-injection
description: "Configures GenericHost and Dependency Injection in AvaloniaUI applications. Use when setting up DI container, registering services, or implementing IoC patterns in AvaloniaUI projects."
---

# 6.6 Dependency Injection and GenericHost Usage

Apply the same GenericHost pattern in AvaloniaUI as in WPF

## Project Structure

The templates folder contains a .NET 9 AvaloniaUI project example.

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
└── AvaloniaDISample.ViewModels/    ← ViewModel Class Library (UI framework independent)
    ├── MainViewModel.cs
    ├── GlobalUsings.cs
    └── AvaloniaDISample.ViewModels.csproj
```

## App.axaml.cs Example:

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
        // Create GenericHost and register services
        _host = Host.CreateDefaultBuilder()
            .ConfigureServices((context, services) =>
            {
                // Register services
                services.AddSingleton<IUserRepository, UserRepository>();
                services.AddSingleton<IUserService, UserService>();
                services.AddTransient<IDialogService, DialogService>();

                // Register ViewModels
                services.AddTransient<MainViewModel>();

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

