---
name: binding-enum-command-parameters
description: "Binds enum values to WPF CommandParameter using x:Static markup extension. Use when passing enum types to commands or avoiding string-based command parameter errors."
---

# WPF Command Parameter Enum Type Binding

## Problem Scenario

When binding enum values to `CommandParameter` in WPF, **passing as string causes type mismatch error**.

### Error Message
```
System.ArgumentException: 'Parameter "parameter" (object) cannot be of type System.String,
as the command type requires an argument of type MyNamespace.MyEnum.'
```

### Cause
When specifying `CommandParameter="Pan"` as a string in XAML, WPF passes it as `System.String` type. However, if the Command expects a specific enum type, automatic type conversion does not occur.

---

## Solution

### Use `x:Static` to Directly Reference Enum Value

```xml
<!-- Namespace declaration -->
xmlns:viewmodels="clr-namespace:MyApp.ViewModels;assembly=MyApp.ViewModels"

<!-- Wrong method (passed as String) -->
<Button Command="{Binding SelectToolCommand}"
        CommandParameter="Pan" />

<!-- Correct method (passed as Enum type) -->
<Button Command="{Binding SelectToolCommand}"
        CommandParameter="{x:Static viewmodels:ViewerTool.Pan}" />
```

---

## Complete Example

### ViewModel (C#)
```csharp
public enum ViewerTool
{
    None,
    Pan,
    Zoom,
    WindowLevel
}

public partial class ViewerViewModel : ObservableObject
{
    [ObservableProperty] private ViewerTool _currentTool = ViewerTool.Pan;

    [RelayCommand]
    private void SelectTool(ViewerTool tool)
    {
        CurrentTool = tool;
    }
}
```

### View (XAML)
```xml
<UserControl xmlns:viewmodels="clr-namespace:MyApp.ViewModels;assembly=MyApp.ViewModels">

    <StackPanel Orientation="Horizontal">
        <!-- Select Pan tool -->
        <ToggleButton Content="Pan"
                      Command="{Binding SelectToolCommand}"
                      CommandParameter="{x:Static viewmodels:ViewerTool.Pan}"
                      IsChecked="{Binding CurrentTool,
                                 Converter={StaticResource EnumToBoolConverter},
                                 ConverterParameter={x:Static viewmodels:ViewerTool.Pan}}" />

        <!-- Select Zoom tool -->
        <ToggleButton Content="Zoom"
                      Command="{Binding SelectToolCommand}"
                      CommandParameter="{x:Static viewmodels:ViewerTool.Zoom}"
                      IsChecked="{Binding CurrentTool,
                                 Converter={StaticResource EnumToBoolConverter},
                                 ConverterParameter={x:Static viewmodels:ViewerTool.Zoom}}" />

        <!-- Select Window/Level tool -->
        <ToggleButton Content="W/L"
                      Command="{Binding SelectToolCommand}"
                      CommandParameter="{x:Static viewmodels:ViewerTool.WindowLevel}"
                      IsChecked="{Binding CurrentTool,
                                 Converter={StaticResource EnumToBoolConverter},
                                 ConverterParameter={x:Static viewmodels:ViewerTool.WindowLevel}}" />
    </StackPanel>

</UserControl>
```

---

## Important Notes

1. **Namespace declaration required**: Must declare the assembly and namespace where enum is defined in XAML
2. **Assembly reference**: Specify `assembly=` when using enum from different project
3. **Also applies to Converter**: Use `x:Static` for `ConverterParameter` as well

---

## Related Pattern

### EnumToBoolConverter (for checking selection state)
```csharp
public class EnumToBoolConverter : IValueConverter
{
    public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
    {
        return value?.Equals(parameter) ?? false;
    }

    public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
    {
        return (bool)value ? parameter : Binding.DoNothing;
    }
}
```
