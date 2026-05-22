---
name: wpf-mvvm
description: Build and maintain WPF MVVM patterns using CommunityToolkit.Mvvm for a .NET 8 widget-host app. Use when creating ViewModels, commands, observable state, validation, view bindings, and viewmodel-first navigation behaviors. Avoid Prism and heavy region managers; keep ViewModels testable and UI-agnostic.
---

# Wpf Mvvm

## Overview

Apply MVVM conventions with CommunityToolkit.Mvvm, ensuring view models are UI-agnostic and ready for the widget shell architecture.

## Constraints

- Target .NET 8
- CommunityToolkit.Mvvm
- ViewModel-first navigation (custom service)
- No Prism, no heavy region manager

## Definition of Done (DoD)

- [ ] ViewModel has no WPF dependencies (Window, UserControl, etc.)
- [ ] Commands use `[RelayCommand]` attribute from CommunityToolkit.Mvvm
- [ ] Observable properties use `[ObservableProperty]` attribute
- [ ] Async commands have proper cancellation support where applicable
- [ ] ViewModel behavior is covered by unit tests
- [ ] No `Application.Current` access in ViewModels
- [ ] Services injected via constructor (not resolved in methods)

---

## Core Patterns

### ViewModel Base Classes

| Base Class | Use Case |
|------------|----------|
| `ObservableObject` | Standard ViewModels |
| `ObservableValidator` | ViewModels with validation |
| `ObservableRecipient` | ViewModels needing messaging |

### Observable Properties

```csharp
[ObservableProperty]
private string _title = "Widget";

// With property change notification to other properties
[ObservableProperty]
[NotifyPropertyChangedFor(nameof(CanSave))]
private string _name = "";

// With can-execute change notification
[ObservableProperty]
[NotifyCanExecuteChangedFor(nameof(SaveCommand))]
private bool _isValid;
```

### Commands

```csharp
// Simple command
[RelayCommand]
private void Refresh() { }

// Async command with cancellation
[RelayCommand]
private async Task LoadDataAsync(CancellationToken token)
{
    Data = await _service.GetDataAsync(token);
}

// Command with can-execute
[RelayCommand(CanExecute = nameof(CanSave))]
private void Save() { }

private bool CanSave => !string.IsNullOrEmpty(Name);
```

### Async Command Patterns

```csharp
[RelayCommand]
private async Task LoadAsync(CancellationToken token)
{
    IsLoading = true;
    try
    {
        Items = await _service.GetItemsAsync(token);
    }
    catch (Exception ex) when (ex is not OperationCanceledException)
    {
        ErrorMessage = "Failed to load items";
        Log.Error(ex, "Load failed");
    }
    finally
    {
        IsLoading = false;
    }
}
```

---

## Validation

```csharp
public partial class SettingsViewModel : ObservableValidator
{
    [ObservableProperty]
    [NotifyDataErrorInfo]
    [Required(ErrorMessage = "Name is required")]
    [MinLength(3)]
    private string _name = "";

    [RelayCommand(CanExecute = nameof(CanSave))]
    private void Save()
    {
        ValidateAllProperties();
        if (!HasErrors)
        {
            // Proceed
        }
    }

    private bool CanSave => !HasErrors;
}
```

---

## Navigation (ViewModel-First)

```csharp
// In Shell or navigation service
public void Navigate<TViewModel>() where TViewModel : ObservableObject
{
    var vm = _serviceProvider.GetRequiredService<TViewModel>();
    CurrentContent = vm;  // DataTemplate maps VM to View
}
```

```xaml
<!-- In App.xaml or Resources -->
<DataTemplate DataType="{x:Type vm:SettingsViewModel}">
    <views:SettingsView/>
</DataTemplate>
```

---

## Anti-Patterns

| ❌ Don't | ✅ Do |
|----------|-------|
| Reference Window/UserControl in VM | Inject INavigationService |
| Call Application.Current | Inject IThemeService, IShellService |
| Create services in methods | Inject via constructor |
| Use code-behind for business logic | Keep logic in ViewModel |
| Expose ICommand directly | Use [RelayCommand] |

---

## Testing ViewModels

```csharp
[Fact]
public void Save_WhenValid_CallsService()
{
    var mockService = new Mock<IDataService>();
    var vm = new MyViewModel(mockService.Object);
    
    vm.Name = "Valid Name";
    vm.SaveCommand.Execute(null);
    
    mockService.Verify(s => s.Save(It.IsAny<Data>()), Times.Once);
}
```

---

## References

- CommunityToolkit.Mvvm documentation
- `3SC/ViewModels/` for examples
- `async-patterns` skill for async command details
- `input-validation` skill for validation patterns

## References

- `references/viewmodel-patterns.md` for structure patterns.
- `references/commands-and-async.md` for command and async guidance.
- `references/validation.md` for validation recipes.
