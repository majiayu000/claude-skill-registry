---
name: implementing-communitytoolkit-mvvm
description: "Implements MVVM pattern using CommunityToolkit.Mvvm with ObservableProperty attributes. Use when building ViewModels with source generators or implementing commands in WPF."
---

# CommunityToolkit.Mvvm Code Guidelines

A guide for implementing MVVM pattern using CommunityToolkit.Mvvm in WPF.

## Project Structure

The templates folder contains a WPF project example (use latest .NET per version mapping).

```
templates/
├── WpfMvvmSample.App/           ← WPF Application Project
│   ├── Views/
│   │   ├── MainWindow.xaml
│   │   └── MainWindow.xaml.cs
│   ├── App.xaml
│   ├── App.xaml.cs
│   ├── GlobalUsings.cs
│   └── WpfMvvmSample.App.csproj
└── WpfMvvmSample.ViewModels/    ← ViewModel Class Library (UI framework independent)
    ├── UserViewModel.cs
    ├── GlobalUsings.cs
    └── WpfMvvmSample.ViewModels.csproj
```

## Basic Principle

**Use CommunityToolkit.Mvvm as the default for MVVM structure**

## ObservableProperty Attribute Writing Rules

### Single Attribute - Write Inline

```csharp
// ✅ Good: Single attribute written inline
[ObservableProperty] private string _userName = string.Empty;

[ObservableProperty] private int _age;

[ObservableProperty] private bool _isActive;
```

### Multiple Attributes - ObservableProperty Always Inline

```csharp
// ✅ Good: Multiple attributes, ObservableProperty always inline
[NotifyPropertyChangedRecipients]
[NotifyCanExecuteChangedFor(nameof(SaveCommand))]
[ObservableProperty] private string _email = string.Empty;

[NotifyDataErrorInfo]
[Required(ErrorMessage = "Name is required.")]
[MinLength(2, ErrorMessage = "Name must be at least 2 characters.")]
[ObservableProperty] private string _name = string.Empty;

[NotifyPropertyChangedRecipients]
[NotifyCanExecuteChangedFor(nameof(DeleteCommand))]
[NotifyCanExecuteChangedFor(nameof(UpdateCommand))]
[ObservableProperty] private User? _selectedUser;
```

### Bad Example

```csharp
// ❌ Bad: ObservableProperty on separate line
[NotifyPropertyChangedRecipients]
[NotifyCanExecuteChangedFor(nameof(SaveCommand))]
[ObservableProperty]
private string _email = string.Empty;
```

## Complete ViewModel Example

```csharp
namespace MyApp.ViewModels;

using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;

public sealed partial class UserViewModel : ObservableObject
{
    // Single attribute
    [ObservableProperty] private string _firstName = string.Empty;
    [ObservableProperty] private string _lastName = string.Empty;
    [ObservableProperty] private int _age;

    // Multiple attributes - ObservableProperty inline
    [NotifyPropertyChangedRecipients]
    [NotifyCanExecuteChangedFor(nameof(SaveCommand))]
    [ObservableProperty] private string _email = string.Empty;

    [NotifyCanExecuteChangedFor(nameof(DeleteCommand))]
    [NotifyCanExecuteChangedFor(nameof(UpdateCommand))]
    [ObservableProperty] private User? _selectedUser;

    [RelayCommand(CanExecute = nameof(CanSave))]
    private async Task SaveAsync()
    {
        // Save logic
    }

    private bool CanSave() => !string.IsNullOrWhiteSpace(Email);
}
```

## Key Rules

- **Single Attribute**: Write `[ObservableProperty]` inline right before the field declaration
- **Multiple Attributes**: Write other attributes on separate lines, but `[ObservableProperty]` is **always inline at the end**
- **Purpose**: Improve code readability and maintain consistent coding style
