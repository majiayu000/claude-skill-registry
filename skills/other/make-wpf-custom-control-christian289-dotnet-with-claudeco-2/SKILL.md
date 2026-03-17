---
name: make-wpf-custom-control
description: WPF CustomControl generation wizard. Specify control name and base class to auto-generate C# class and XAML style.
disable-model-invocation: true
argument-hint: [ControlName] [BaseClass]
---

# WPF CustomControl Generation

User input: $ARGUMENTS

## Workflow

### Step 1: Parse Arguments

Extract control name and base class from `$ARGUMENTS`:
- Format: `ControlName BaseClass` (e.g., `MyButton Button`, `CircularProgress Control`)
- If base class is omitted, default to `Control`

### Step 2: Validate Input

- Control name must be PascalCase
- Base class must be valid WPF control (Button, Control, ContentControl, ItemsControl, etc.)

### Step 3: Generate C# Class File

Create `[ControlName].cs`:

```csharp
using System.Windows;
using System.Windows.Controls;

namespace [ProjectNamespace].Controls;

/// <summary>
/// [ControlName] - Custom WPF control based on [BaseClass]
/// </summary>
[TemplatePart(Name = "PART_Root", Type = typeof(Border))]
[TemplateVisualState(GroupName = "CommonStates", Name = "Normal")]
[TemplateVisualState(GroupName = "CommonStates", Name = "MouseOver")]
[TemplateVisualState(GroupName = "CommonStates", Name = "Pressed")]
[TemplateVisualState(GroupName = "CommonStates", Name = "Disabled")]
public class [ControlName] : [BaseClass]
{
    #region Static Constructor

    static [ControlName]()
    {
        DefaultStyleKeyProperty.OverrideMetadata(
            typeof([ControlName]),
            new FrameworkPropertyMetadata(typeof([ControlName])));
    }

    #endregion

    #region Dependency Properties

    /// <summary>
    /// Example dependency property
    /// </summary>
    public static readonly DependencyProperty ExampleProperty =
        DependencyProperty.Register(
            nameof(Example),
            typeof(string),
            typeof([ControlName]),
            new FrameworkPropertyMetadata(
                defaultValue: string.Empty,
                flags: FrameworkPropertyMetadataOptions.AffectsRender,
                propertyChangedCallback: OnExampleChanged));

    public string Example
    {
        get => (string)GetValue(ExampleProperty);
        set => SetValue(ExampleProperty, value);
    }

    private static void OnExampleChanged(DependencyObject d, DependencyPropertyChangedEventArgs e)
    {
        if (d is [ControlName] control)
        {
            control.OnExampleChanged((string)e.OldValue, (string)e.NewValue);
        }
    }

    protected virtual void OnExampleChanged(string oldValue, string newValue)
    {
        // Handle property change
    }

    #endregion

    #region Template Parts

    private Border? _partRoot;

    public override void OnApplyTemplate()
    {
        base.OnApplyTemplate();

        _partRoot = GetTemplateChild("PART_Root") as Border;

        UpdateVisualState(false);
    }

    #endregion

    #region Visual States

    private void UpdateVisualState(bool useTransitions)
    {
        if (!IsEnabled)
        {
            VisualStateManager.GoToState(this, "Disabled", useTransitions);
        }
        else if (IsMouseOver)
        {
            VisualStateManager.GoToState(this, "MouseOver", useTransitions);
        }
        else
        {
            VisualStateManager.GoToState(this, "Normal", useTransitions);
        }
    }

    protected override void OnMouseEnter(System.Windows.Input.MouseEventArgs e)
    {
        base.OnMouseEnter(e);
        UpdateVisualState(true);
    }

    protected override void OnMouseLeave(System.Windows.Input.MouseEventArgs e)
    {
        base.OnMouseLeave(e);
        UpdateVisualState(true);
    }

    #endregion
}
```

### Step 4: Generate XAML Style File

Create `Themes/[ControlName].xaml`:

```xml
<ResourceDictionary xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
                    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
                    xmlns:local="clr-namespace:[ProjectNamespace].Controls">

    <!-- Resources -->
    <SolidColorBrush x:Key="[ControlName]Background" Color="#FFFFFF"/>
    <SolidColorBrush x:Key="[ControlName]Foreground" Color="#000000"/>
    <SolidColorBrush x:Key="[ControlName]BorderBrush" Color="#CCCCCC"/>
    <SolidColorBrush x:Key="[ControlName]MouseOverBackground" Color="#E5F3FF"/>

    <!-- Style -->
    <Style TargetType="{x:Type local:[ControlName]}">
        <Setter Property="Background" Value="{StaticResource [ControlName]Background}"/>
        <Setter Property="Foreground" Value="{StaticResource [ControlName]Foreground}"/>
        <Setter Property="BorderBrush" Value="{StaticResource [ControlName]BorderBrush}"/>
        <Setter Property="BorderThickness" Value="1"/>
        <Setter Property="Padding" Value="8,4"/>
        <Setter Property="Template">
            <Setter.Value>
                <ControlTemplate TargetType="{x:Type local:[ControlName]}">
                    <Border x:Name="PART_Root"
                            Background="{TemplateBinding Background}"
                            BorderBrush="{TemplateBinding BorderBrush}"
                            BorderThickness="{TemplateBinding BorderThickness}"
                            Padding="{TemplateBinding Padding}"
                            CornerRadius="4">
                        <VisualStateManager.VisualStateGroups>
                            <VisualStateGroup x:Name="CommonStates">
                                <VisualState x:Name="Normal"/>
                                <VisualState x:Name="MouseOver">
                                    <Storyboard>
                                        <ColorAnimation
                                            Storyboard.TargetName="PART_Root"
                                            Storyboard.TargetProperty="(Border.Background).(SolidColorBrush.Color)"
                                            To="#E5F3FF"
                                            Duration="0:0:0.2"/>
                                    </Storyboard>
                                </VisualState>
                                <VisualState x:Name="Pressed">
                                    <Storyboard>
                                        <ColorAnimation
                                            Storyboard.TargetName="PART_Root"
                                            Storyboard.TargetProperty="(Border.Background).(SolidColorBrush.Color)"
                                            To="#CCE4FF"
                                            Duration="0:0:0.1"/>
                                    </Storyboard>
                                </VisualState>
                                <VisualState x:Name="Disabled">
                                    <Storyboard>
                                        <DoubleAnimation
                                            Storyboard.TargetName="PART_Root"
                                            Storyboard.TargetProperty="Opacity"
                                            To="0.5"
                                            Duration="0:0:0"/>
                                    </Storyboard>
                                </VisualState>
                            </VisualStateGroup>
                        </VisualStateManager.VisualStateGroups>

                        <ContentPresenter
                            HorizontalAlignment="{TemplateBinding HorizontalContentAlignment}"
                            VerticalAlignment="{TemplateBinding VerticalContentAlignment}"/>
                    </Border>
                </ControlTemplate>
            </Setter.Value>
        </Setter>
    </Style>
</ResourceDictionary>
```

### Step 5: Update Generic.xaml

Add to `Themes/Generic.xaml` MergedDictionaries:

```xml
<ResourceDictionary.MergedDictionaries>
    <!-- Existing entries -->
    <ResourceDictionary Source="/Themes/[ControlName].xaml"/>
</ResourceDictionary.MergedDictionaries>
```

## Output Summary

After generation, provide:
1. Created files list
2. Next steps for customization
3. Usage example in XAML

```xml
<!-- Usage Example -->
<local:[ControlName] Example="Hello World"/>
```
