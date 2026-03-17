---
name: defining-wpf-dependencyproperty
description: Defines WPF DependencyProperty with Register, PropertyMetadata, callbacks, and validation. Use when creating custom controls, attached properties, or properties that support data binding and styling.
---

# WPF DependencyProperty Patterns

Defining dependency properties for data binding, styling, animation, and property value inheritance.

**Advanced Patterns:** See [ADVANCED.md](ADVANCED.md) for value inheritance, metadata override, and event integration.

## 1. DependencyProperty Overview

```
Standard CLR Property:
    private string _name;
    public string Name { get => _name; set => _name = value; }

DependencyProperty:
    public static readonly DependencyProperty NameProperty = ...
    public string Name { get => (string)GetValue(NameProperty); set => SetValue(NameProperty, value); }

Benefits:
    ✅ Data Binding
    ✅ Styling & Templating
    ✅ Animation
    ✅ Property Value Inheritance
    ✅ Default Values
    ✅ Change Notifications
    ✅ Value Coercion
    ✅ Validation
```

---

## 2. Basic DependencyProperty

### 2.1 Standard Registration

```csharp
namespace MyApp.Controls;

using System.Windows;
using System.Windows.Controls;

public class MyControl : Control
{
    // 1. Register DependencyProperty
    public static readonly DependencyProperty TitleProperty = DependencyProperty.Register(
        name: nameof(Title),
        propertyType: typeof(string),
        ownerType: typeof(MyControl),
        typeMetadata: new PropertyMetadata(defaultValue: string.Empty));

    // 2. CLR property wrapper
    public string Title
    {
        get => (string)GetValue(TitleProperty);
        set => SetValue(TitleProperty, value);
    }
}
```

### 2.2 With FrameworkPropertyMetadata

```csharp
public static readonly DependencyProperty ValueProperty = DependencyProperty.Register(
    name: nameof(Value),
    propertyType: typeof(double),
    ownerType: typeof(MyControl),
    typeMetadata: new FrameworkPropertyMetadata(
        defaultValue: 0.0,
        flags: FrameworkPropertyMetadataOptions.AffectsRender |
               FrameworkPropertyMetadataOptions.BindsTwoWayByDefault,
        propertyChangedCallback: OnValueChanged,
        coerceValueCallback: CoerceValue),
    validateValueCallback: ValidateValue);

public double Value
{
    get => (double)GetValue(ValueProperty);
    set => SetValue(ValueProperty, value);
}
```

---

## 3. FrameworkPropertyMetadataOptions

| Flag | Description |
|------|-------------|
| **None** | No special behavior |
| **AffectsMeasure** | Triggers Measure pass on change |
| **AffectsArrange** | Triggers Arrange pass on change |
| **AffectsRender** | Triggers Render on change |
| **Inherits** | Value inherits to child elements |
| **BindsTwoWayByDefault** | Default binding mode is TwoWay |

### Common Combinations

```csharp
// Read-only display property (AffectsRender)
new FrameworkPropertyMetadata(
    defaultValue: null,
    flags: FrameworkPropertyMetadataOptions.AffectsRender);

// Layout-affecting property (AffectsMeasure)
new FrameworkPropertyMetadata(
    defaultValue: 100.0,
    flags: FrameworkPropertyMetadataOptions.AffectsMeasure |
           FrameworkPropertyMetadataOptions.AffectsArrange);

// Two-way bindable property
new FrameworkPropertyMetadata(
    defaultValue: false,
    flags: FrameworkPropertyMetadataOptions.BindsTwoWayByDefault);
```

---

## 4. Callbacks

### 4.1 PropertyChangedCallback

```csharp
public static readonly DependencyProperty IsActiveProperty = DependencyProperty.Register(
    nameof(IsActive),
    typeof(bool),
    typeof(MyControl),
    new PropertyMetadata(false, OnIsActiveChanged));

private static void OnIsActiveChanged(DependencyObject d, DependencyPropertyChangedEventArgs e)
{
    var control = (MyControl)d;
    var oldValue = (bool)e.OldValue;
    var newValue = (bool)e.NewValue;

    // Handle property change
    control.UpdateVisualState(newValue);
}
```

### 4.2 CoerceValueCallback

```csharp
public static readonly DependencyProperty ProgressProperty = DependencyProperty.Register(
    nameof(Progress),
    typeof(double),
    typeof(ProgressControl),
    new FrameworkPropertyMetadata(
        0.0,
        propertyChangedCallback: null,
        coerceValueCallback: CoerceProgress));

private static object CoerceProgress(DependencyObject d, object baseValue)
{
    var value = (double)baseValue;

    // Clamp value to valid range
    if (value < 0.0) return 0.0;
    if (value > 100.0) return 100.0;

    return value;
}
```

### 4.3 ValidateValueCallback

```csharp
public static readonly DependencyProperty CountProperty = DependencyProperty.Register(
    nameof(Count),
    typeof(int),
    typeof(MyControl),
    new PropertyMetadata(0),
    ValidateCount);  // Note: Not part of PropertyMetadata

private static bool ValidateCount(object value)
{
    var count = (int)value;

    // Return false to reject the value (throws exception)
    return count >= 0;
}
```

### 4.4 Callback Execution Order

```
1. ValidateValueCallback - Can reject value (throw exception)
2. CoerceValueCallback   - Can modify value
3. PropertyChangedCallback - Handle the change
```

---

## 5. Read-Only DependencyProperty

```csharp
namespace MyApp.Controls;

using System.Windows;

public class StatusControl : Control
{
    // 1. Register read-only property key (private)
    private static readonly DependencyPropertyKey IsConnectedPropertyKey =
        DependencyProperty.RegisterReadOnly(
            nameof(IsConnected),
            typeof(bool),
            typeof(StatusControl),
            new FrameworkPropertyMetadata(false));

    // 2. Expose public DependencyProperty
    public static readonly DependencyProperty IsConnectedProperty =
        IsConnectedPropertyKey.DependencyProperty;

    // 3. Read-only CLR property
    public bool IsConnected => (bool)GetValue(IsConnectedProperty);

    // 4. Internal setter using key
    protected void SetIsConnected(bool value)
    {
        SetValue(IsConnectedPropertyKey, value);
    }
}
```

---

## 6. Attached Property

### 6.1 Defining Attached Property

```csharp
namespace MyApp.Attached;

using System.Windows;

public static class GridHelper
{
    // Register attached property
    public static readonly DependencyProperty ColumnSpacingProperty =
        DependencyProperty.RegisterAttached(
            name: "ColumnSpacing",
            propertyType: typeof(double),
            ownerType: typeof(GridHelper),
            defaultMetadata: new FrameworkPropertyMetadata(
                0.0,
                FrameworkPropertyMetadataOptions.AffectsMeasure,
                OnColumnSpacingChanged));

    // Getter
    public static double GetColumnSpacing(DependencyObject obj)
    {
        return (double)obj.GetValue(ColumnSpacingProperty);
    }

    // Setter
    public static void SetColumnSpacing(DependencyObject obj, double value)
    {
        obj.SetValue(ColumnSpacingProperty, value);
    }

    private static void OnColumnSpacingChanged(DependencyObject d, DependencyPropertyChangedEventArgs e)
    {
        if (d is Grid grid)
        {
            UpdateGridSpacing(grid, (double)e.NewValue);
        }
    }

    private static void UpdateGridSpacing(Grid grid, double spacing)
    {
        // Implementation
    }
}
```

### 6.2 Using Attached Property in XAML

```xml
<Grid local:GridHelper.ColumnSpacing="10">
    <Grid.ColumnDefinitions>
        <ColumnDefinition Width="*"/>
        <ColumnDefinition Width="*"/>
        <ColumnDefinition Width="*"/>
    </Grid.ColumnDefinitions>
    <!-- Children -->
</Grid>
```

---

## 7. References

- [Dependency Properties Overview - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/properties/dependency-properties-overview)
- [Custom Dependency Properties - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/properties/custom-dependency-properties)
- [Attached Properties Overview - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/properties/attached-properties-overview)
