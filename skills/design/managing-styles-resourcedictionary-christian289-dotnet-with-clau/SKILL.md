---
name: managing-styles-resourcedictionary
description: "Manages WPF Style definitions and ResourceDictionary patterns including BasedOn inheritance and resource merging. Use when building theme systems, organizing resources, or choosing between StaticResource and DynamicResource."
---

# WPF Style & ResourceDictionary Patterns

Effectively managing Style and ResourceDictionary for consistent UI and maintainability.

## 1. Style Basic Structure

### 1.1 Explicit Style (With Key)

```xml
<Window.Resources>
    <!-- Explicit style: must reference by key to apply -->
    <Style x:Key="PrimaryButtonStyle" TargetType="{x:Type Button}">
        <Setter Property="Background" Value="#2196F3"/>
        <Setter Property="Foreground" Value="White"/>
        <Setter Property="Padding" Value="16,8"/>
        <Setter Property="FontWeight" Value="SemiBold"/>
    </Style>
</Window.Resources>

<Button Style="{StaticResource PrimaryButtonStyle}" Content="Primary"/>
```

### 1.2 Implicit Style (Without Key)

```xml
<Window.Resources>
    <!-- Implicit style: auto-applied to all controls of that type -->
    <Style TargetType="{x:Type Button}">
        <Setter Property="Margin" Value="5"/>
        <Setter Property="Cursor" Value="Hand"/>
    </Style>
</Window.Resources>

<!-- Style automatically applied -->
<Button Content="Auto Styled"/>
```

---

## 2. Style Inheritance (BasedOn)

### 2.1 Basic Inheritance

```xml
<!-- Base button style -->
<Style x:Key="BaseButtonStyle" TargetType="{x:Type Button}">
    <Setter Property="Padding" Value="12,6"/>
    <Setter Property="BorderThickness" Value="0"/>
    <Setter Property="Cursor" Value="Hand"/>
</Style>

<!-- Primary button: inherits base style -->
<Style x:Key="PrimaryButtonStyle" TargetType="{x:Type Button}"
       BasedOn="{StaticResource BaseButtonStyle}">
    <Setter Property="Background" Value="#2196F3"/>
    <Setter Property="Foreground" Value="White"/>
</Style>

<!-- Secondary button: inherits base style -->
<Style x:Key="SecondaryButtonStyle" TargetType="{x:Type Button}"
       BasedOn="{StaticResource BaseButtonStyle}">
    <Setter Property="Background" Value="#E0E0E0"/>
    <Setter Property="Foreground" Value="#424242"/>
</Style>
```

### 2.2 Implicit Style Inheritance

```xml
<!-- Explicit style inheriting from implicit style -->
<Style TargetType="{x:Type Button}">
    <Setter Property="Margin" Value="5"/>
</Style>

<Style x:Key="SpecialButtonStyle" TargetType="{x:Type Button}"
       BasedOn="{StaticResource {x:Type Button}}">
    <Setter Property="Background" Value="Gold"/>
</Style>
```

---

## 3. ResourceDictionary

### 3.1 File Structure

```
📁 Themes/
├── 📄 Colors.xaml          (Color definitions)
├── 📄 Brushes.xaml         (Brush definitions)
├── 📄 Converters.xaml      (Converter definitions)
├── 📄 Controls/
│   ├── 📄 Button.xaml      (Button styles)
│   ├── 📄 TextBox.xaml     (TextBox styles)
│   └── 📄 ListBox.xaml     (ListBox styles)
└── 📄 Generic.xaml         (Merged dictionary)
```

### 3.2 Colors.xaml

```xml
<ResourceDictionary xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
                    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">

    <!-- Base color palette -->
    <Color x:Key="PrimaryColor">#2196F3</Color>
    <Color x:Key="PrimaryDarkColor">#1976D2</Color>
    <Color x:Key="PrimaryLightColor">#BBDEFB</Color>

    <Color x:Key="AccentColor">#FF4081</Color>

    <Color x:Key="TextPrimaryColor">#212121</Color>
    <Color x:Key="TextSecondaryColor">#757575</Color>

    <Color x:Key="BackgroundColor">#FAFAFA</Color>
    <Color x:Key="SurfaceColor">#FFFFFF</Color>

    <Color x:Key="ErrorColor">#F44336</Color>
    <Color x:Key="SuccessColor">#4CAF50</Color>
    <Color x:Key="WarningColor">#FFC107</Color>

</ResourceDictionary>
```

### 3.3 Brushes.xaml

```xml
<ResourceDictionary xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
                    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">

    <!-- Merge Colors.xaml -->
    <ResourceDictionary.MergedDictionaries>
        <ResourceDictionary Source="Colors.xaml"/>
    </ResourceDictionary.MergedDictionaries>

    <!-- SolidColorBrush definitions -->
    <SolidColorBrush x:Key="PrimaryBrush" Color="{StaticResource PrimaryColor}"/>
    <SolidColorBrush x:Key="PrimaryDarkBrush" Color="{StaticResource PrimaryDarkColor}"/>
    <SolidColorBrush x:Key="PrimaryLightBrush" Color="{StaticResource PrimaryLightColor}"/>

    <SolidColorBrush x:Key="AccentBrush" Color="{StaticResource AccentColor}"/>

    <SolidColorBrush x:Key="TextPrimaryBrush" Color="{StaticResource TextPrimaryColor}"/>
    <SolidColorBrush x:Key="TextSecondaryBrush" Color="{StaticResource TextSecondaryColor}"/>

    <SolidColorBrush x:Key="BackgroundBrush" Color="{StaticResource BackgroundColor}"/>
    <SolidColorBrush x:Key="SurfaceBrush" Color="{StaticResource SurfaceColor}"/>

</ResourceDictionary>
```

### 3.4 Generic.xaml (Merged Dictionary)

```xml
<ResourceDictionary xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
                    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">

    <ResourceDictionary.MergedDictionaries>
        <!-- Order matters: merge in dependency order -->
        <ResourceDictionary Source="Colors.xaml"/>
        <ResourceDictionary Source="Brushes.xaml"/>
        <ResourceDictionary Source="Converters.xaml"/>
        <ResourceDictionary Source="Controls/Button.xaml"/>
        <ResourceDictionary Source="Controls/TextBox.xaml"/>
        <ResourceDictionary Source="Controls/ListBox.xaml"/>
    </ResourceDictionary.MergedDictionaries>

</ResourceDictionary>
```

### 3.5 Loading in App.xaml

```xml
<Application x:Class="MyApp.App"
             xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
    <Application.Resources>
        <ResourceDictionary>
            <ResourceDictionary.MergedDictionaries>
                <ResourceDictionary Source="/Themes/Generic.xaml"/>
            </ResourceDictionary.MergedDictionaries>
        </ResourceDictionary>
    </Application.Resources>
</Application>
```

---

## 4. StaticResource vs DynamicResource

### 4.1 Comparison

| Aspect | StaticResource | DynamicResource |
|--------|----------------|-----------------|
| **Evaluation time** | Once at XAML load | Every time at runtime |
| **Performance** | Fast | Relatively slower |
| **Change reflection** | No | Auto-reflected |
| **Forward reference** | Not available | Available |
| **Use case** | Fixed resources | Theme changes, dynamic resources |

### 4.2 Usage Examples

```xml
<!-- StaticResource: immutable resources -->
<Button Background="{StaticResource PrimaryBrush}"/>

<!-- DynamicResource: when runtime changes needed -->
<Border Background="{DynamicResource ThemeBackgroundBrush}"/>
```

### 4.3 Theme Switching Implementation

```csharp
namespace MyApp.Services;

using System;
using System.Windows;

public sealed class ThemeService
{
    private const string LightThemePath = "/Themes/LightTheme.xaml";
    private const string DarkThemePath = "/Themes/DarkTheme.xaml";

    /// <summary>
    /// Switch theme
    /// </summary>
    public void SwitchTheme(bool isDark)
    {
        var themePath = isDark ? DarkThemePath : LightThemePath;
        var themeUri = new Uri(themePath, UriKind.Relative);

        var app = Application.Current;
        var mergedDicts = app.Resources.MergedDictionaries;

        // Remove existing theme
        for (var i = mergedDicts.Count - 1; i >= 0; i--)
        {
            var dict = mergedDicts[i];
            if (dict.Source?.OriginalString.Contains("Theme") == true)
            {
                mergedDicts.RemoveAt(i);
            }
        }

        // Add new theme
        mergedDicts.Add(new ResourceDictionary { Source = themeUri });
    }
}
```

---

## 5. Accessing Resources from Code

### 5.1 Resource Lookup

```csharp
namespace MyApp.Helpers;

using System.Windows;
using System.Windows.Media;

public static class ResourceHelper
{
    /// <summary>
    /// Find resource (FindResource - throws if not found)
    /// </summary>
    public static Brush GetBrush(string key)
    {
        return (Brush)Application.Current.FindResource(key);
    }

    /// <summary>
    /// Find resource (TryFindResource - returns null if not found)
    /// </summary>
    public static Brush? TryGetBrush(string key)
    {
        return Application.Current.TryFindResource(key) as Brush;
    }

    /// <summary>
    /// Find resource from element (searches upward)
    /// </summary>
    public static T? FindResource<T>(FrameworkElement element, string key) where T : class
    {
        return element.TryFindResource(key) as T;
    }
}
```

### 5.2 Setting Dynamic Resource

```csharp
// Set DynamicResource from code
button.SetResourceReference(Button.BackgroundProperty, "PrimaryBrush");

// Set StaticResource from code (direct resource assignment)
button.Background = (Brush)FindResource("PrimaryBrush");
```

---

## 6. ComponentResourceKey (For External Libraries)

### 6.1 Definition

```csharp
namespace MyLib.Controls;

using System.Windows;

public static class MyLibResources
{
    // Define component resource key
    public static readonly ComponentResourceKey PrimaryBrushKey =
        new(typeof(MyLibResources), "PrimaryBrush");

    public static readonly ComponentResourceKey ButtonStyleKey =
        new(typeof(MyLibResources), "ButtonStyle");
}
```

### 6.2 Usage

```xml
<!-- Generic.xaml (in Themes folder) -->
<ResourceDictionary xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
                    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
                    xmlns:local="clr-namespace:MyLib.Controls">

    <SolidColorBrush x:Key="{ComponentResourceKey TypeInTargetAssembly={x:Type local:MyLibResources}, ResourceId=PrimaryBrush}"
                     Color="#2196F3"/>

</ResourceDictionary>
```

```xml
<!-- Consumer side -->
<Button Background="{StaticResource {x:Static local:MyLibResources.PrimaryBrushKey}}"/>
```

---

## 7. Resource Lookup Order

```
1. Element's own Resources
2. Parent element Resources (searching upward in Visual Tree)
3. Window/Page Resources
4. Application.Resources
5. Theme resources (Generic.xaml)
6. System resources (SystemColors, SystemFonts)
```

---

## 8. Checklist

- [ ] Define colors as Color type, Brushes in separate file
- [ ] Separate style files per control
- [ ] Use StaticResource for fixed resources, DynamicResource for theme resources
- [ ] Verify ResourceDictionary merge order (dependency order)
- [ ] Inherit common styles with BasedOn
- [ ] Expose library resources with ComponentResourceKey

---

## 9. References

- [Resources Overview - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/systems/xaml-resources-overview)
- [Styles and Templates - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/controls/styles-templates-overview)
