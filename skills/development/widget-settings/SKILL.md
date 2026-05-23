---
name: widget-settings
description: Widget settings persistence and UI patterns for the .NET 8 WPF widget host app. Use when adding settings to widgets, persisting configuration, or building settings dialogs.
---

# Widget Settings

## Overview

Standardize how widgets store, retrieve, and expose their configuration settings.

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│ Settings Dialog │────▶│ WidgetViewModel  │────▶│ SettingsService │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                                                          │
                                                          ▼
                                                  ┌───────────────┐
                                                  │ WidgetInstance│
                                                  │ (SettingsJson)│
                                                  └───────────────┘
```

---

## Implementation Pattern

### 1. Define Settings Value Object (Domain)

```csharp
// 3SC.Domain/ValueObjects/ClockWidgetSettings.cs
public sealed class ClockWidgetSettings
{
    public string TimeZoneId { get; init; } = TimeZoneInfo.Local.Id;
    public bool Use24HourFormat { get; init; } = true;
    public bool ShowSeconds { get; init; } = true;
    public bool ShowTimeZoneLabel { get; init; } = false;

    public static ClockWidgetSettings Default() => new();
}
```

### 2. Use JsonHelper for Serialization

```csharp
// Save settings
var json = JsonHelper.Serialize(settings);
instance.SettingsJson = json;

// Load settings
var settings = JsonHelper.Deserialize<ClockWidgetSettings>(instance.SettingsJson)
    ?? ClockWidgetSettings.Default();
```

### 3. ViewModel Settings Property

```csharp
public partial class ClockWidgetViewModel : ObservableObject
{
    [ObservableProperty]
    private ClockWidgetSettings _settings;

    public void ApplySettings(ClockWidgetSettings newSettings)
    {
        Settings = newSettings;
        // Reinitialize any services that depend on settings
        InitializeClockService(newSettings);
    }
}
```

### 4. Settings Dialog ViewModel

```csharp
public partial class ClockSettingsViewModel : ObservableValidator
{
    private readonly ClockWidgetSettings _original;

    [ObservableProperty]
    [NotifyPropertyChangedFor(nameof(HasChanges))]
    private string _timeZoneId;

    [ObservableProperty]
    [NotifyPropertyChangedFor(nameof(HasChanges))]
    private bool _use24HourFormat;

    public bool HasChanges => 
        TimeZoneId != _original.TimeZoneId ||
        Use24HourFormat != _original.Use24HourFormat;

    public ClockWidgetSettings ToSettings() => new()
    {
        TimeZoneId = TimeZoneId,
        Use24HourFormat = Use24HourFormat,
        // ...
    };
}
```

---

## Widget Settings Service

```csharp
// 3SC/Services/WidgetSettingsService.cs
public class WidgetSettingsService
{
    public T? GetSettings<T>(Guid widgetInstanceId) where T : class
    {
        // Load from DB and deserialize
    }

    public async Task SaveSettingsAsync<T>(Guid widgetInstanceId, T settings)
    {
        // Serialize and save to DB
    }
}
```

---

## Settings UI Pattern

### Context Menu Entry
```xaml
<MenuItem Header="Settings"
          Click="OpenSettings_Click">
    <MenuItem.Icon>
        <TextBlock Text="&#xE713;" FontFamily="Segoe MDL2 Assets"/>
    </MenuItem.Icon>
</MenuItem>
```

### Settings Dialog Structure
```xaml
<Window Title="Clock Settings" Width="400" Height="300">
    <Grid Margin="20">
        <Grid.RowDefinitions>
            <RowDefinition Height="*"/>
            <RowDefinition Height="Auto"/>
        </Grid.RowDefinitions>
        
        <!-- Settings Form -->
        <StackPanel Grid.Row="0">
            <CheckBox Content="Use 24-hour format"
                      IsChecked="{Binding Use24HourFormat}"/>
            <!-- More settings... -->
        </StackPanel>
        
        <!-- Actions -->
        <StackPanel Grid.Row="1" Orientation="Horizontal" 
                    HorizontalAlignment="Right">
            <Button Content="Cancel" Command="{Binding CancelCommand}"/>
            <Button Content="Save" Command="{Binding SaveCommand}"
                    IsEnabled="{Binding HasChanges}"/>
        </StackPanel>
    </Grid>
</Window>
```

---

## Definition of Done (DoD)

- [ ] Settings defined as immutable value object in Domain
- [ ] Settings serialized as JSON in WidgetInstance.SettingsJson
- [ ] Default settings provided when none exist
- [ ] Settings dialog uses separate ViewModel
- [ ] Changes require explicit Save action
- [ ] Cancel discards unsaved changes
- [ ] Settings validated before save
- [ ] Widget refreshes when settings change

---

## Key Files

| File | Purpose |
|------|---------|
| `3SC.Domain/ValueObjects/*Settings.cs` | Settings value objects |
| `3SC/Services/WidgetSettingsService.cs` | Load/save orchestration |
| `3SC/Helpers/JsonHelper.cs` | JSON serialization |
| `3SC/ViewModels/*SettingsViewModel.cs` | Settings dialog VMs |

---

## Anti-Patterns

- ❌ Storing settings in separate files per widget
- ❌ Mutable settings objects shared across threads
- ❌ Auto-saving on every change (use explicit save)
- ❌ Settings logic in code-behind
- ❌ Missing default values

