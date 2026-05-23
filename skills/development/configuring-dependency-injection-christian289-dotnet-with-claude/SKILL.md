---
name: configuring-dependency-injection
description: "Configures Dependency Injection using Microsoft.Extensions.DependencyInjection and GenericHost. Use when setting up DI container, registering services, or implementing IoC patterns in .NET projects."
---

# Dependency Injection and GenericHost Usage

A guide on using Dependency Injection and GenericHost in .NET projects.

## Core Principles

- **Implement dependency injection using Microsoft.Extensions.DependencyInjection**
- **Use GenericHost (Microsoft.Extensions.Hosting) as the default**
- **Apply service injection through Constructor Injection**

## Console and General Projects - Program.cs

```csharp
// Program.cs
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

// Configure DI using GenericHost
var host = Host.CreateDefaultBuilder(args)
    .ConfigureServices((context, services) =>
    {
        // Register services
        services.AddSingleton<IUserRepository, UserRepository>();
        services.AddScoped<IUserService, UserService>();
        services.AddTransient<IEmailService, EmailService>();

        // Register main application service
        services.AddSingleton<App>();
    })
    .Build();

// Get service through ServiceProvider
var app = host.Services.GetRequiredService<App>();
await app.RunAsync();

// Application class - Constructor Injection
public sealed class App(IUserService userService, IEmailService emailService)
{
    private readonly IUserService _userService = userService;
    private readonly IEmailService _emailService = emailService;

    public async Task RunAsync()
    {
        // Use injected services
        var users = await _userService.GetAllUsersAsync();

        foreach (var user in users)
        {
            await _emailService.SendWelcomeEmailAsync(user.Email);
        }
    }
}
```

## WPF Project - App.xaml.cs

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
                services.AddTransient<SettingsViewModel>();

                // Register Views
                services.AddSingleton<MainWindow>();
            })
            .Build();
    }

    protected override async void OnStartup(StartupEventArgs e)
    {
        await _host.StartAsync();

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

    [ObservableProperty] private ObservableCollection<User> _users = [];

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
            await _dialogService.ShowErrorAsync("Error occurred", ex.Message);
        }
    }
}
```

## Service Lifetime Rules

### Singleton
Creates only one instance throughout the application
- Repository, global state management services
- `services.AddSingleton<IUserRepository, UserRepository>()`

### Scoped
Creates one instance per request (Scope)
- DbContext, transaction-based services
- `services.AddScoped<IUserService, UserService>()`
- ⚠️ Generally not used in WPF (mainly used in Web applications)

### Transient
Creates a new instance on every request
- ViewModel, one-time services
- `services.AddTransient<MainViewModel>()`

## Direct Use of ServiceProvider (Not Recommended)

### Anti-pattern: Service Locator

```csharp
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
        // ⚠️ Not recommended: Using ServiceProvider directly
        var service = _serviceProvider.GetRequiredService<IUserService>();
    }
}
```

### Recommended: Constructor Injection

```csharp
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
        // ✅ Recommended: Use service injected through Constructor Injection
        _userService.GetAllUsersAsync();
    }
}
```

## Required NuGet Packages

```xml
<ItemGroup>
  <PackageReference Include="Microsoft.Extensions.DependencyInjection" Version="9.0.0" />
  <PackageReference Include="Microsoft.Extensions.Hosting" Version="9.0.0" />
</ItemGroup>
```

