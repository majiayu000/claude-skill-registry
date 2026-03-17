---
name: reactiveui
description: >
  USE FOR: Building MVVM applications using Reactive Extensions with ReactiveObject, WhenAnyValue,
  ReactiveCommand, view model activation, and data binding for WPF, MAUI, Avalonia, and Blazor.
  DO NOT USE FOR: Simple applications without reactive data flows, server-side APIs without UI,
  or projects that prefer CommunityToolkit.Mvvm for a simpler MVVM approach.
license: MIT
metadata:
  displayName: ReactiveUI
  author: "Tyler-R-Kendrick"
  version: "1.0.0"
compatibility:
  - claude
  - copilot
  - cursor
references:
  - title: "ReactiveUI Official Documentation"
    url: "https://www.reactiveui.net/docs/"
  - title: "ReactiveUI GitHub Repository"
    url: "https://github.com/reactiveui/ReactiveUI"
  - title: "ReactiveUI NuGet Package"
    url: "https://www.nuget.org/packages/ReactiveUI"
---

# ReactiveUI

## Overview

ReactiveUI is a composable, cross-platform MVVM framework built on Reactive Extensions (Rx.NET). It provides `ReactiveObject` as a base class for view models with change notification, `WhenAnyValue` for observing property changes as `IObservable<T>`, `ReactiveCommand` for async command execution with built-in busy/error state, and `ObservableAsPropertyHelper<T>` (OAPH) for computed output properties driven by observables.

ReactiveUI supports WPF, WinUI, MAUI, Avalonia, Blazor, and Xamarin. It integrates with DynamicData for reactive collections and provides platform-specific binding extensions through `ReactiveUI.WPF`, `ReactiveUI.Maui`, etc.

## Installation

```bash
dotnet add package ReactiveUI
dotnet add package ReactiveUI.WPF       # For WPF
# OR
dotnet add package ReactiveUI.Maui      # For .NET MAUI
# OR
dotnet add package ReactiveUI.Blazor    # For Blazor
```

## ReactiveObject and Property Change Notification

```csharp
using ReactiveUI;

namespace MyApp.ViewModels;

public class LoginViewModel : ReactiveObject
{
    private string _username = string.Empty;
    public string Username
    {
        get => _username;
        set => this.RaiseAndSetIfChanged(ref _username, value);
    }

    private string _password = string.Empty;
    public string Password
    {
        get => _password;
        set => this.RaiseAndSetIfChanged(ref _password, value);
    }

    private bool _rememberMe;
    public bool RememberMe
    {
        get => _rememberMe;
        set => this.RaiseAndSetIfChanged(ref _rememberMe, value);
    }

    private string _errorMessage = string.Empty;
    public string ErrorMessage
    {
        get => _errorMessage;
        set => this.RaiseAndSetIfChanged(ref _errorMessage, value);
    }
}
```

## WhenAnyValue: Observing Property Changes

`WhenAnyValue` converts property changes into `IObservable<T>` streams.

```csharp
using System;
using System.Reactive.Linq;
using ReactiveUI;

namespace MyApp.ViewModels;

public class SearchViewModel : ReactiveObject
{
    private string _searchText = string.Empty;
    public string SearchText
    {
        get => _searchText;
        set => this.RaiseAndSetIfChanged(ref _searchText, value);
    }

    private readonly ObservableAsPropertyHelper<bool> _hasSearchText;
    public bool HasSearchText => _hasSearchText.Value;

    private readonly ObservableAsPropertyHelper<int> _characterCount;
    public int CharacterCount => _characterCount.Value;

    public SearchViewModel()
    {
        // Single property observation
        _hasSearchText = this.WhenAnyValue(x => x.SearchText)
            .Select(text => !string.IsNullOrWhiteSpace(text))
            .ToProperty(this, x => x.HasSearchText);

        _characterCount = this.WhenAnyValue(x => x.SearchText)
            .Select(text => text?.Length ?? 0)
            .ToProperty(this, x => x.CharacterCount);
    }
}
```

Combining multiple properties:

```csharp
using System;
using System.Reactive.Linq;
using ReactiveUI;

namespace MyApp.ViewModels;

public class RegistrationViewModel : ReactiveObject
{
    private string _email = string.Empty;
    public string Email
    {
        get => _email;
        set => this.RaiseAndSetIfChanged(ref _email, value);
    }

    private string _password = string.Empty;
    public string Password
    {
        get => _password;
        set => this.RaiseAndSetIfChanged(ref _password, value);
    }

    private string _confirmPassword = string.Empty;
    public string ConfirmPassword
    {
        get => _confirmPassword;
        set => this.RaiseAndSetIfChanged(ref _confirmPassword, value);
    }

    private readonly ObservableAsPropertyHelper<bool> _isFormValid;
    public bool IsFormValid => _isFormValid.Value;

    private readonly ObservableAsPropertyHelper<string> _passwordStrength;
    public string PasswordStrength => _passwordStrength.Value;

    public RegistrationViewModel()
    {
        // Combine multiple properties for validation
        _isFormValid = this.WhenAnyValue(
                x => x.Email,
                x => x.Password,
                x => x.ConfirmPassword,
                (email, pass, confirm) =>
                    !string.IsNullOrWhiteSpace(email) &&
                    email.Contains('@') &&
                    pass.Length >= 8 &&
                    pass == confirm)
            .ToProperty(this, x => x.IsFormValid);

        _passwordStrength = this.WhenAnyValue(x => x.Password)
            .Select(EvaluatePasswordStrength)
            .ToProperty(this, x => x.PasswordStrength, initialValue: "None");
    }

    private static string EvaluatePasswordStrength(string password)
    {
        if (string.IsNullOrEmpty(password)) return "None";
        if (password.Length < 8) return "Weak";
        bool hasUpper = password.Any(char.IsUpper);
        bool hasDigit = password.Any(char.IsDigit);
        bool hasSpecial = password.Any(c => !char.IsLetterOrDigit(c));
        int score = (hasUpper ? 1 : 0) + (hasDigit ? 1 : 0) + (hasSpecial ? 1 : 0);
        return score switch
        {
            >= 3 => "Strong",
            2 => "Medium",
            _ => "Weak"
        };
    }
}
```

## ReactiveCommand

`ReactiveCommand` wraps async operations with built-in `IsExecuting`, error handling, and `canExecute` observable guards.

```csharp
using System;
using System.Reactive;
using System.Reactive.Linq;
using System.Threading.Tasks;
using ReactiveUI;

namespace MyApp.ViewModels;

public class OrderViewModel : ReactiveObject
{
    private string _productName = string.Empty;
    public string ProductName
    {
        get => _productName;
        set => this.RaiseAndSetIfChanged(ref _productName, value);
    }

    private int _quantity = 1;
    public int Quantity
    {
        get => _quantity;
        set => this.RaiseAndSetIfChanged(ref _quantity, value);
    }

    private readonly ObservableAsPropertyHelper<bool> _isSubmitting;
    public bool IsSubmitting => _isSubmitting.Value;

    public ReactiveCommand<Unit, OrderResult> SubmitCommand { get; }
    public ReactiveCommand<Unit, Unit> CancelCommand { get; }

    private readonly IOrderService _orderService;

    public OrderViewModel(IOrderService orderService)
    {
        _orderService = orderService;

        // CanExecute observable: only when form is valid and not already submitting
        var canSubmit = this.WhenAnyValue(
            x => x.ProductName,
            x => x.Quantity,
            (name, qty) =>
                !string.IsNullOrWhiteSpace(name) && qty > 0);

        // Create async command with canExecute guard
        SubmitCommand = ReactiveCommand.CreateFromTask(
            SubmitOrderAsync,
            canSubmit);

        // Track IsExecuting as a property
        _isSubmitting = SubmitCommand.IsExecuting
            .ToProperty(this, x => x.IsSubmitting);

        // Handle errors
        SubmitCommand.ThrownExceptions
            .Subscribe(ex =>
                Console.WriteLine($"Order failed: {ex.Message}"));

        CancelCommand = ReactiveCommand.Create(() =>
        {
            ProductName = string.Empty;
            Quantity = 1;
        });
    }

    private async Task<OrderResult> SubmitOrderAsync()
    {
        return await _orderService.PlaceOrderAsync(ProductName, Quantity);
    }
}

public record OrderResult(string OrderId, string Status);

public interface IOrderService
{
    Task<OrderResult> PlaceOrderAsync(string productName, int quantity);
}
```

## View Model Activation

ReactiveUI provides `IActivatableViewModel` for managing resources that should only exist when the view is visible.

```csharp
using System;
using System.Reactive;
using System.Reactive.Disposables;
using System.Reactive.Linq;
using ReactiveUI;

namespace MyApp.ViewModels;

public class DashboardViewModel : ReactiveObject, IActivatableViewModel
{
    public ViewModelActivator Activator { get; } = new();

    private readonly ObservableAsPropertyHelper<string> _currentTime;
    public string CurrentTime => _currentTime.Value;

    private readonly ObservableAsPropertyHelper<int> _activeUsers;
    public int ActiveUsers => _activeUsers.Value;

    public DashboardViewModel()
    {
        _currentTime = ObservableAsPropertyHelper<string>
            .Default(initialValue: "Loading...");
        _activeUsers = ObservableAsPropertyHelper<int>.Default();

        this.WhenActivated(disposables =>
        {
            // Timer that only runs when the view is active
            Observable.Interval(TimeSpan.FromSeconds(1))
                .Select(_ => DateTime.Now.ToString("HH:mm:ss"))
                .ToProperty(this, x => x.CurrentTime, out _currentTime)
                .DisposeWith(disposables);

            // Poll for active users while view is visible
            Observable.Interval(TimeSpan.FromSeconds(30))
                .SelectMany(_ => Observable.FromAsync(FetchActiveUsersAsync))
                .ToProperty(this, x => x.ActiveUsers, out _activeUsers)
                .DisposeWith(disposables);
        });
    }

    private async Task<int> FetchActiveUsersAsync()
    {
        await Task.Delay(100);
        return Random.Shared.Next(50, 200);
    }
}
```

## Interaction: View Model to View Communication

```csharp
using System;
using System.Reactive;
using System.Reactive.Linq;
using System.Threading.Tasks;
using ReactiveUI;

namespace MyApp.ViewModels;

public class FileViewModel : ReactiveObject
{
    // Interaction: VM asks the view a question and gets an answer
    public Interaction<string, bool> ConfirmDelete { get; } = new();
    public Interaction<Unit, string?> SelectFile { get; } = new();

    public ReactiveCommand<string, Unit> DeleteCommand { get; }
    public ReactiveCommand<Unit, Unit> OpenCommand { get; }

    public FileViewModel()
    {
        DeleteCommand = ReactiveCommand.CreateFromTask<string>(async (fileName) =>
        {
            // Ask the view for confirmation
            bool confirmed = await ConfirmDelete.Handle(fileName);
            if (confirmed)
            {
                // Perform deletion
                Console.WriteLine($"Deleted: {fileName}");
            }
        });

        OpenCommand = ReactiveCommand.CreateFromTask(async () =>
        {
            string? path = await SelectFile.Handle(Unit.Default);
            if (path is not null)
            {
                Console.WriteLine($"Opening: {path}");
            }
        });
    }
}

// In the View (WPF example):
// ViewModel.ConfirmDelete.RegisterHandler(async interaction =>
// {
//     var result = MessageBox.Show(
//         $"Delete {interaction.Input}?", "Confirm",
//         MessageBoxButton.YesNo);
//     interaction.SetOutput(result == MessageBoxResult.Yes);
// });
```

## ReactiveUI vs. CommunityToolkit.Mvvm

| Feature                   | ReactiveUI                            | CommunityToolkit.Mvvm              |
|---------------------------|---------------------------------------|------------------------------------|
| Change notification       | `RaiseAndSetIfChanged` (manual)       | `[ObservableProperty]` (generated) |
| Computed properties       | `ObservableAsPropertyHelper<T>`       | `[NotifyPropertyChangedFor]`       |
| Commands                  | `ReactiveCommand` (Rx-based)          | `[RelayCommand]` (generated)       |
| Async command state       | Built-in `IsExecuting`, errors        | `AsyncRelayCommand.IsRunning`      |
| Property observation      | `WhenAnyValue` (observable streams)   | Partial method notifications       |
| Activation lifecycle      | `IActivatableViewModel`               | Not built-in                       |
| View-VM interaction       | `Interaction<TInput, TOutput>`        | `IMessenger.Send/Register`         |
| Reactive collections      | DynamicData integration               | `ObservableCollection`             |
| Learning curve            | Higher (Rx knowledge required)        | Lower (attribute-based)            |
| Best for                  | Complex reactive data flows           | Simple MVVM with code generation   |

## Best Practices

1. **Use `this.RaiseAndSetIfChanged(ref _field, value)` for every mutable property** instead of manually calling `OnPropertyChanged` because it handles equality comparison, backing field assignment, and notification in a single atomic call.

2. **Use `ObservableAsPropertyHelper<T>` (OAPH) for computed/derived properties** instead of subscribing and setting a property manually; OAPH integrates with ReactiveUI's scheduler and property-change notification automatically.

3. **Pass a `canExecute` observable to `ReactiveCommand.Create`** so that the command automatically disables bound buttons when the condition is false, and automatically disables during execution to prevent double-submission.

4. **Subscribe to `command.ThrownExceptions` for every `ReactiveCommand`** because unobserved exceptions in commands are routed to `RxApp.DefaultExceptionHandler` which terminates the application by default.

5. **Use `IActivatableViewModel` with `this.WhenActivated(disposables => { ... })` for subscriptions that should only run while the view is visible** to prevent background timers, network polls, and event handlers from running when the view is navigated away.

6. **Apply `Throttle` to `WhenAnyValue` streams for search text inputs** to avoid executing an API call on every keystroke; `Throttle(TimeSpan.FromMilliseconds(300))` waits for the user to stop typing before emitting.

7. **Use `Interaction<TInput, TOutput>` instead of injecting view-layer services into view models** to keep view models testable; in tests, register a handler that returns a predetermined response without showing UI.

8. **Call `.DisposeWith(disposables)` on every subscription inside `WhenActivated`** to ensure subscriptions are cleaned up when the view is deactivated, preventing memory leaks and stale data updates.

9. **Use `WhenAnyValue` with multiple property overloads (up to 12 properties)** to combine multiple inputs into a single derived value rather than subscribing to each property individually, which simplifies synchronization.

10. **Keep view model constructors synchronous and move async initialization into a `ReactiveCommand` or `WhenActivated` block** because constructors cannot be awaited and async void constructors crash on unhandled exceptions.
