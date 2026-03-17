---
name: avalonia
description: |
  USE FOR: Building cross-platform desktop and mobile applications with XAML-based UI using Avalonia on .NET. Use when targeting Windows, macOS, Linux, iOS, Android, or WebAssembly with a single codebase and MVVM architecture.
  DO NOT USE FOR: Web-only applications (use Blazor), game development (use MonoGame/Unity), or projects that only need to target Windows (consider WPF for tighter Windows integration).
license: MIT
metadata:
  displayName: Avalonia
  author: "Tyler-R-Kendrick"
  version: "1.0.0"
compatibility:
  - claude
  - copilot
  - cursor
references:
  - title: "Avalonia UI Official Documentation"
    url: "https://docs.avaloniaui.net/"
  - title: "Avalonia GitHub Repository"
    url: "https://github.com/AvaloniaUI/Avalonia"
  - title: "Avalonia NuGet Package"
    url: "https://www.nuget.org/packages/Avalonia"
---

# Avalonia

## Overview

Avalonia is an open-source, cross-platform UI framework for .NET that enables developers to build desktop and mobile applications from a single C# and XAML codebase. It supports Windows, macOS, Linux, iOS, Android, and WebAssembly. Avalonia draws heavily from WPF concepts such as styles, data templates, and data binding but introduces its own styling system and rendering pipeline built on Skia. It supports the MVVM pattern natively and integrates well with ReactiveUI and CommunityToolkit.Mvvm.

## Project Setup and Application Bootstrap

Create a new Avalonia application and configure the application entry point with platform-specific initialization.

```csharp
using Avalonia;
using Avalonia.Controls.ApplicationLifetimes;
using Avalonia.Markup.Xaml;

namespace MyAvaloniaApp;

public class App : Application
{
    public override void Initialize()
    {
        AvaloniaXamlLoader.Load(this);
    }

    public override void OnFrameworkInitializationCompleted()
    {
        if (ApplicationLifetime is IClassicDesktopStyleApplicationLifetime desktop)
        {
            desktop.MainWindow = new MainWindow
            {
                DataContext = new MainWindowViewModel()
            };
        }
        else if (ApplicationLifetime is ISingleViewApplicationLifetime singleView)
        {
            singleView.MainView = new MainView
            {
                DataContext = new MainWindowViewModel()
            };
        }

        base.OnFrameworkInitializationCompleted();
    }
}

public static class Program
{
    [STAThread]
    public static void Main(string[] args) => BuildAvaloniaApp()
        .StartWithClassicDesktopLifetime(args);

    public static AppBuilder BuildAvaloniaApp()
        => AppBuilder.Configure<App>()
            .UsePlatformDetect()
            .WithInterFont()
            .LogToTrace();
}
```

## MVVM with Data Binding

Avalonia has first-class support for the MVVM pattern. Use `CommunityToolkit.Mvvm` source generators or `ReactiveUI` for view models.

```csharp
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using System.Collections.ObjectModel;

namespace MyAvaloniaApp.ViewModels;

public partial class TodoViewModel : ObservableObject
{
    [ObservableProperty]
    private string _newItemText = string.Empty;

    [ObservableProperty]
    private ObservableCollection<TodoItem> _items = new();

    [RelayCommand(CanExecute = nameof(CanAddItem))]
    private void AddItem()
    {
        Items.Add(new TodoItem { Title = NewItemText, IsCompleted = false });
        NewItemText = string.Empty;
    }

    private bool CanAddItem() => !string.IsNullOrWhiteSpace(NewItemText);

    [RelayCommand]
    private void RemoveItem(TodoItem item)
    {
        Items.Remove(item);
    }
}

public partial class TodoItem : ObservableObject
{
    [ObservableProperty]
    private string _title = string.Empty;

    [ObservableProperty]
    private bool _isCompleted;
}
```

The corresponding AXAML view binds to the view model:

```xml
<UserControl xmlns="https://github.com/avaloniaui"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
             xmlns:vm="using:MyAvaloniaApp.ViewModels"
             x:Class="MyAvaloniaApp.Views.TodoView"
             x:DataType="vm:TodoViewModel">
  <DockPanel Margin="16">
    <StackPanel DockPanel.Dock="Top" Orientation="Horizontal" Spacing="8">
      <TextBox Text="{Binding NewItemText}" Watermark="Enter a task..." Width="300"/>
      <Button Content="Add" Command="{Binding AddItemCommand}"/>
    </StackPanel>
    <ListBox ItemsSource="{Binding Items}" Margin="0,12,0,0">
      <ListBox.ItemTemplate>
        <DataTemplate x:DataType="vm:TodoItem">
          <StackPanel Orientation="Horizontal" Spacing="8">
            <CheckBox IsChecked="{Binding IsCompleted}"/>
            <TextBlock Text="{Binding Title}" VerticalAlignment="Center"/>
            <Button Content="X" Command="{Binding $parent[UserControl].((vm:TodoViewModel)DataContext).RemoveItemCommand}"
                    CommandParameter="{Binding}"/>
          </StackPanel>
        </DataTemplate>
      </ListBox.ItemTemplate>
    </ListBox>
  </DockPanel>
</UserControl>
```

## Custom Controls and Styling

Avalonia uses a CSS-inspired styling system rather than WPF's resource-dictionary approach. You can create custom styled controls with template parts.

```csharp
using Avalonia;
using Avalonia.Controls;
using Avalonia.Controls.Primitives;
using Avalonia.Media;

namespace MyAvaloniaApp.Controls;

public class StatusBadge : TemplatedControl
{
    public static readonly StyledProperty<string> LabelProperty =
        AvaloniaProperty.Register<StatusBadge, string>(nameof(Label), "Status");

    public static readonly StyledProperty<IBrush> BadgeColorProperty =
        AvaloniaProperty.Register<StatusBadge, IBrush>(nameof(BadgeColor), Brushes.Gray);

    public static readonly StyledProperty<bool> IsActiveProperty =
        AvaloniaProperty.Register<StatusBadge, bool>(nameof(IsActive), false);

    public string Label
    {
        get => GetValue(LabelProperty);
        set => SetValue(LabelProperty, value);
    }

    public IBrush BadgeColor
    {
        get => GetValue(BadgeColorProperty);
        set => SetValue(BadgeColorProperty, value);
    }

    public bool IsActive
    {
        get => GetValue(IsActiveProperty);
        set => SetValue(IsActiveProperty, value);
    }

    protected override void OnApplyTemplate(TemplateAppliedEventArgs e)
    {
        base.OnApplyTemplate(e);
        PseudoClasses.Set(":active", IsActive);
    }
}
```

Style it in AXAML:

```xml
<Styles xmlns="https://github.com/avaloniaui">
  <Style Selector="local|StatusBadge">
    <Setter Property="Template">
      <ControlTemplate>
        <Border Background="{TemplateBinding BadgeColor}" CornerRadius="8" Padding="8,4">
          <TextBlock Text="{TemplateBinding Label}" Foreground="White" FontSize="12"/>
        </Border>
      </ControlTemplate>
    </Setter>
  </Style>
  <Style Selector="local|StatusBadge:active">
    <Setter Property="Opacity" Value="1.0"/>
  </Style>
  <Style Selector="local|StatusBadge:not(:active)">
    <Setter Property="Opacity" Value="0.5"/>
  </Style>
</Styles>
```

## Platform Comparison

| Feature | Avalonia | WPF | MAUI |
|---|---|---|---|
| Cross-platform desktop | Windows, macOS, Linux | Windows only | Windows, macOS |
| Mobile support | iOS, Android | No | iOS, Android |
| WebAssembly | Yes | No | Experimental |
| Styling system | CSS-like selectors | Resource dictionaries | Handlers + CSS-like |
| XAML dialect | AXAML | XAML | XAML |
| Rendering engine | Skia | DirectX/GDI | Platform-native |
| Hot reload | Yes | Yes | Yes |
| Open source | Yes (MIT) | No | Yes (MIT) |

## Dependency Injection and Services

Wire up services using the standard `Microsoft.Extensions.DependencyInjection` container and inject into view models.

```csharp
using Microsoft.Extensions.DependencyInjection;
using Avalonia.Controls.ApplicationLifetimes;
using Avalonia.Markup.Xaml;

namespace MyAvaloniaApp;

public class App : Application
{
    private IServiceProvider? _services;

    public override void Initialize()
    {
        AvaloniaXamlLoader.Load(this);
    }

    public override void OnFrameworkInitializationCompleted()
    {
        var services = new ServiceCollection();
        services.AddSingleton<IDataStore, SqliteDataStore>();
        services.AddTransient<TodoViewModel>();
        _services = services.BuildServiceProvider();

        if (ApplicationLifetime is IClassicDesktopStyleApplicationLifetime desktop)
        {
            desktop.MainWindow = new MainWindow
            {
                DataContext = _services.GetRequiredService<TodoViewModel>()
            };
        }

        base.OnFrameworkInitializationCompleted();
    }
}
```

## Best Practices

1. **Always set `x:DataType` on views and data templates** to enable compiled bindings, which provide compile-time type checking and eliminate reflection-based binding overhead that degrades performance on mobile and WASM targets.

2. **Separate platform-specific code behind `IPlatformService` abstractions** registered per-platform in the DI container rather than using `#if` preprocessor directives, so that shared view models remain testable without platform dependencies.

3. **Use `AvaloniaProperty.Register` with explicit default values** for every styled property on custom controls, and document the property type and purpose via XML doc comments so that consumers can discover behavior through IntelliSense.

4. **Prefer `ObservableCollection<T>` and `[ObservableProperty]` from CommunityToolkit.Mvvm** over manual `INotifyPropertyChanged` implementations; the source generator eliminates boilerplate and guarantees correct property-change notification naming.

5. **Apply the `Selector` specificity rules intentionally**: place global theme styles in `App.axaml`, page-level overrides in the view's `<UserControl.Styles>` block, and inline setters only for one-off adjustments, mirroring CSS specificity best practices.

6. **Test view models independently of the UI thread** by injecting `Avalonia.Threading.Dispatcher` behind an interface, or use `Dispatcher.UIThread.InvokeAsync` only at the view layer, keeping business logic synchronous and unit-testable.

7. **Configure `AppBuilder.UsePlatformDetect()` explicitly per target** in CI pipelines (e.g., `.UseX11()` on Linux, `.UseAvaloniaNative()` on macOS) so build failures surface immediately instead of falling back silently to an unsupported backend.

8. **Use `KeyFrame` animations sparingly on mobile and WASM** and measure frame rate with the built-in `PerformanceOverlay` diagnostic; Skia software rendering on lower-end devices can drop below 30 FPS with complex storyboard animations.

9. **Implement `IAsyncDisposable` on view models that hold subscriptions or open connections** and call `DisposeAsync` in the window's `OnClosed` override or via a behavior, preventing resource leaks across navigation events.

10. **Pin the Avalonia NuGet package versions across all projects using a `Directory.Packages.props` file** with central package management enabled, avoiding version skew between `Avalonia`, `Avalonia.Desktop`, and `Avalonia.Themes.Fluent` that causes runtime `TypeLoadException` errors.
