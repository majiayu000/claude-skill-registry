---
name: customizing-controltemplate
description: "Customizes WPF control appearance using ControlTemplate with TemplateBinding and ContentPresenter. Use when completely changing control visuals, implementing state-based feedback, or TemplatedParent binding."
---

# WPF ControlTemplate Patterns

All controls inherited from the Control class can completely redefine their visual structure through ControlTemplate.

## 1. Core Concepts

### ControlTemplate vs Style

| Aspect | Style | ControlTemplate |
|--------|-------|-----------------|
| **Role** | Batch property value setting | Visual structure redefinition |
| **Scope** | Property changes only | Full appearance change possible |
| **Target** | All FrameworkElements | Control-derived classes only |

### ControlTemplate Components

- **TargetType**: Control type to which the template applies
- **TemplateBinding**: Connection to TemplatedParent properties
- **ContentPresenter**: Specifies where Content property is rendered
- **Triggers**: State-based visual changes

---

## 2. Basic Implementation Patterns

### 2.1 Button ControlTemplate (XAML)

```xml
<ResourceDictionary xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
                    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">

    <Style TargetType="{x:Type Button}" x:Key="RoundedButtonStyle">
        <Setter Property="Template">
            <Setter.Value>
                <ControlTemplate TargetType="{x:Type Button}">
                    <!-- Visual structure definition -->
                    <Border x:Name="PART_Border"
                            CornerRadius="10"
                            BorderThickness="{TemplateBinding BorderThickness}"
                            BorderBrush="{TemplateBinding BorderBrush}"
                            Background="{TemplateBinding Background}"
                            Padding="{TemplateBinding Padding}">

                        <!-- Content rendering location -->
                        <ContentPresenter HorizontalAlignment="{TemplateBinding HorizontalContentAlignment}"
                                          VerticalAlignment="{TemplateBinding VerticalContentAlignment}"
                                          RecognizesAccessKey="True"/>
                    </Border>

                    <!-- State-based triggers -->
                    <ControlTemplate.Triggers>
                        <Trigger Property="IsMouseOver" Value="True">
                            <Setter TargetName="PART_Border" Property="Background" Value="#E3F2FD"/>
                        </Trigger>
                        <Trigger Property="IsPressed" Value="True">
                            <Setter TargetName="PART_Border" Property="Background" Value="#BBDEFB"/>
                        </Trigger>
                        <Trigger Property="IsEnabled" Value="False">
                            <Setter TargetName="PART_Border" Property="Opacity" Value="0.5"/>
                        </Trigger>
                    </ControlTemplate.Triggers>
                </ControlTemplate>
            </Setter.Value>
        </Setter>

        <!-- Default property values -->
        <Setter Property="Background" Value="#2196F3"/>
        <Setter Property="Foreground" Value="White"/>
        <Setter Property="BorderThickness" Value="0"/>
        <Setter Property="Padding" Value="16,8"/>
        <Setter Property="Cursor" Value="Hand"/>
    </Style>

</ResourceDictionary>
```

### 2.2 Applying ControlTemplate in Code

```csharp
namespace MyApp.Helpers;

using System.IO;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Markup;

public static class TemplateHelper
{
    /// <summary>
    /// Create ControlTemplate from XAML string
    /// </summary>
    public static ControlTemplate CreateTemplate(string xaml)
    {
        using var stream = new MemoryStream(Encoding.UTF8.GetBytes(xaml));

        var context = new ParserContext();
        context.XmlnsDictionary.Add("", "http://schemas.microsoft.com/winfx/2006/xaml/presentation");
        context.XmlnsDictionary.Add("x", "http://schemas.microsoft.com/winfx/2006/xaml");

        return (ControlTemplate)XamlReader.Load(stream, context);
    }
}
```

---

## 3. TemplateBinding vs Binding

### 3.1 TemplateBinding (Recommended)

```xml
<!-- Compile-time binding, one-way, better performance -->
<Border Background="{TemplateBinding Background}"/>
```

### 3.2 RelativeSource TemplatedParent (When Two-Way Needed)

```xml
<!-- Runtime binding, two-way possible, relatively slower -->
<Border Background="{Binding Background, RelativeSource={RelativeSource TemplatedParent}}"/>
```

### Comparison

| Aspect | TemplateBinding | RelativeSource TemplatedParent |
|--------|-----------------|-------------------------------|
| **Direction** | One-way (OneWay) | Two-way possible |
| **Performance** | Fast | Relatively slower |
| **Converter** | Not available | Available |
| **Use case** | Most cases | When two-way/converter needed |

---

## 4. ContentPresenter Details

### 4.1 Key Properties

```xml
<ContentPresenter
    Content="{TemplateBinding Content}"
    ContentTemplate="{TemplateBinding ContentTemplate}"
    ContentTemplateSelector="{TemplateBinding ContentTemplateSelector}"
    ContentStringFormat="{TemplateBinding ContentStringFormat}"
    HorizontalAlignment="{TemplateBinding HorizontalContentAlignment}"
    VerticalAlignment="{TemplateBinding VerticalContentAlignment}"
    Margin="{TemplateBinding Padding}"
    RecognizesAccessKey="True"/>
```

### 4.2 RecognizesAccessKey

```xml
<!-- Enable button activation with Alt + underlined character -->
<Button Content="_Save"/>  <!-- Activate with Alt+S -->
```

---

## 5. Trigger Patterns

### 5.1 Property Trigger

```xml
<ControlTemplate.Triggers>
    <!-- Single property condition -->
    <Trigger Property="IsMouseOver" Value="True">
        <Setter TargetName="PART_Border" Property="Background" Value="LightBlue"/>
    </Trigger>
</ControlTemplate.Triggers>
```

### 5.2 MultiTrigger

```xml
<ControlTemplate.Triggers>
    <!-- Multiple property conditions (AND) -->
    <MultiTrigger>
        <MultiTrigger.Conditions>
            <Condition Property="IsMouseOver" Value="True"/>
            <Condition Property="IsEnabled" Value="True"/>
        </MultiTrigger.Conditions>
        <Setter TargetName="PART_Border" Property="Background" Value="LightGreen"/>
    </MultiTrigger>
</ControlTemplate.Triggers>
```

### 5.3 EventTrigger (Animation)

```xml
<ControlTemplate.Triggers>
    <EventTrigger RoutedEvent="MouseEnter">
        <BeginStoryboard>
            <Storyboard>
                <DoubleAnimation Storyboard.TargetName="PART_Border"
                                 Storyboard.TargetProperty="Opacity"
                                 To="0.8" Duration="0:0:0.2"/>
            </Storyboard>
        </BeginStoryboard>
    </EventTrigger>
</ControlTemplate.Triggers>
```

---

## 6. Practical Example: Toggle Button

```xml
<Style TargetType="{x:Type ToggleButton}" x:Key="SwitchToggleStyle">
    <Setter Property="Template">
        <Setter.Value>
            <ControlTemplate TargetType="{x:Type ToggleButton}">
                <Grid>
                    <!-- Background track -->
                    <Border x:Name="PART_Track"
                            Width="50" Height="26"
                            CornerRadius="13"
                            Background="#E0E0E0"/>

                    <!-- Sliding thumb -->
                    <Border x:Name="PART_Thumb"
                            Width="22" Height="22"
                            CornerRadius="11"
                            Background="White"
                            HorizontalAlignment="Left"
                            Margin="2,0,0,0">
                        <Border.Effect>
                            <DropShadowEffect ShadowDepth="1" BlurRadius="3" Opacity="0.3"/>
                        </Border.Effect>
                    </Border>
                </Grid>

                <ControlTemplate.Triggers>
                    <!-- Checked state -->
                    <Trigger Property="IsChecked" Value="True">
                        <Setter TargetName="PART_Track" Property="Background" Value="#4CAF50"/>
                        <Setter TargetName="PART_Thumb" Property="HorizontalAlignment" Value="Right"/>
                        <Setter TargetName="PART_Thumb" Property="Margin" Value="0,0,2,0"/>
                    </Trigger>

                    <!-- Disabled state -->
                    <Trigger Property="IsEnabled" Value="False">
                        <Setter Property="Opacity" Value="0.5"/>
                    </Trigger>
                </ControlTemplate.Triggers>
            </ControlTemplate>
        </Setter.Value>
    </Setter>
</Style>
```

---

## 7. PART_ Naming Convention

Used when code-behind in CustomControl needs to access specific elements:

```xml
<!-- Mark required elements with PART_ prefix -->
<Border x:Name="PART_Border"/>
<ContentPresenter x:Name="PART_ContentHost"/>
<Popup x:Name="PART_Popup"/>
```

```csharp
// Find PART_ elements in OnApplyTemplate
public override void OnApplyTemplate()
{
    base.OnApplyTemplate();

    var border = GetTemplateChild("PART_Border") as Border;
    var popup = GetTemplateChild("PART_Popup") as Popup;
}
```

---

## 8. Checklist

- [ ] Specify TargetType
- [ ] Connect properties with TemplateBinding
- [ ] Set RecognizesAccessKey="True" on ContentPresenter
- [ ] Handle IsMouseOver, IsPressed, IsEnabled, IsFocused triggers
- [ ] Mark required elements with PART_ naming
- [ ] Specify default property values with Style's Setter

---

## 9. References

- [ControlTemplate - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/controls/controltemplate)
- [Styling and Templating - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/controls/styles-templates-overview)
