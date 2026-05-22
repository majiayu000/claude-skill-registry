---
name: developing-wpf-customcontrols
description: "Develops WPF CustomControls using Parts and States Model best practices. Use when creating templatable controls with TemplatePart, TemplateVisualState, OnApplyTemplate, or VisualStateManager."
---

# WPF CustomControl Development - Parts and States Model

Workflow for developing WPF CustomControls with appearance customization capability.

## Development Flow

### 1. Control Inheritance Decision

```
UserControl Selection Criteria:
- Need rapid development
- ControlTemplate customization not required
- Complex theme support not required

Control Inheritance Selection Criteria:
- Need appearance customization via ControlTemplate
- Need various theme support
- Need same extensibility as WPF built-in controls
```

### 2. Define Control Contract

Declare `TemplatePart` and `TemplateVisualState` attributes on the class:

```csharp
[TemplatePart(Name = PartUpButton, Type = typeof(RepeatButton))]
[TemplatePart(Name = PartDownButton, Type = typeof(RepeatButton))]
[TemplateVisualState(Name = StatePositive, GroupName = GroupValueStates)]
[TemplateVisualState(Name = StateNegative, GroupName = GroupValueStates)]
[TemplateVisualState(Name = StateFocused, GroupName = GroupFocusStates)]
[TemplateVisualState(Name = StateUnfocused, GroupName = GroupFocusStates)]
public class NumericUpDown : Control
{
    // Define Part/State names as const
    private const string PartUpButton = "PART_UpButton";
    private const string PartDownButton = "PART_DownButton";
    private const string GroupValueStates = "ValueStates";
    private const string GroupFocusStates = "FocusStates";
    private const string StatePositive = "Positive";
    private const string StateNegative = "Negative";
    private const string StateFocused = "Focused";
    private const string StateUnfocused = "Unfocused";
}
```

### 3. Template Part Property Pattern

Wrap Part elements as private properties, subscribe/unsubscribe events in setter:

```csharp
private RepeatButton? _upButton;
private RepeatButton? UpButtonElement
{
    get => _upButton;
    set
    {
        // Unsubscribe from existing element's events
        if (_upButton is not null)
            _upButton.Click -= OnUpButtonClick;

        _upButton = value;

        // Subscribe to new element's events
        if (_upButton is not null)
            _upButton.Click += OnUpButtonClick;
    }
}
```

### 4. OnApplyTemplate Implementation

```csharp
public override void OnApplyTemplate()
{
    base.OnApplyTemplate();

    // GetTemplateChild + as cast (null on type mismatch)
    UpButtonElement = GetTemplateChild(PartUpButton) as RepeatButton;
    DownButtonElement = GetTemplateChild(PartDownButton) as RepeatButton;

    // Set initial state (without transition)
    UpdateStates(useTransitions: false);
}
```

**Core Principles:**

- If Part is missing or type differs, it's null → don't cause errors
- Control must work even with incomplete ControlTemplate

### 5. UpdateStates Helper Method

Centralize state transition logic in a single method:

```csharp
private void UpdateStates(bool useTransitions)
{
    // ValueStates group
    VisualStateManager.GoToState(this,
        Value >= 0 ? StatePositive : StateNegative,
        useTransitions);

    // FocusStates group
    VisualStateManager.GoToState(this,
        IsFocused ? StateFocused : StateUnfocused,
        useTransitions);
}
```

**When to call UpdateStates:**

- `OnApplyTemplate` - Initial state (useTransitions: false)
- Property changed callback - Reflect value change (useTransitions: true)
- `OnGotFocus`/`OnLostFocus` - Focus state (useTransitions: true)

### 6. Property Changed Callback

```csharp
private static void OnValueChanged(DependencyObject d,
    DependencyPropertyChangedEventArgs e)
{
    var control = (NumericUpDown)d;
    control.UpdateStates(useTransitions: true);
    control.OnValueChanged(new ValueChangedEventArgs((int)e.NewValue));
}
```

### 7. ControlTemplate Structure (Generic.xaml)

```xml
<Style TargetType="{x:Type local:NumericUpDown}">
  <Setter Property="Template">
    <Setter.Value>
      <ControlTemplate TargetType="{x:Type local:NumericUpDown}">
        <Grid Background="{TemplateBinding Background}">

          <!-- Place VisualStateGroups on root element -->
          <VisualStateManager.VisualStateGroups>
            <VisualStateGroup x:Name="ValueStates">
              <VisualState x:Name="Positive"/>
              <VisualState x:Name="Negative">
                <Storyboard>
                  <ColorAnimation To="Red"
                    Storyboard.TargetName="ValueText"
                    Storyboard.TargetProperty="(Foreground).(SolidColorBrush.Color)"/>
                </Storyboard>
              </VisualState>
            </VisualStateGroup>

            <VisualStateGroup x:Name="FocusStates">
              <VisualState x:Name="Focused">
                <Storyboard>
                  <ObjectAnimationUsingKeyFrames
                    Storyboard.TargetName="FocusVisual"
                    Storyboard.TargetProperty="Visibility">
                    <DiscreteObjectKeyFrame KeyTime="0" Value="{x:Static Visibility.Visible}"/>
                  </ObjectAnimationUsingKeyFrames>
                </Storyboard>
              </VisualState>
              <VisualState x:Name="Unfocused"/>
            </VisualStateGroup>
          </VisualStateManager.VisualStateGroups>

          <!-- Define Part elements with x:Name -->
          <RepeatButton x:Name="PART_UpButton" Content="▲"/>
          <TextBlock x:Name="ValueText" Text="{TemplateBinding Value}"/>
          <RepeatButton x:Name="PART_DownButton" Content="▼"/>

        </Grid>
      </ControlTemplate>
    </Setter.Value>
  </Setter>
</Style>
```

## Checklist

- [ ] Inherit from Control class (not UserControl)
- [ ] Declare required Parts with `TemplatePart` attribute
- [ ] Declare states with `TemplateVisualState` attribute
- [ ] Define Part/State names as const strings
- [ ] Subscribe/unsubscribe events in Part property setter
- [ ] Use `GetTemplateChild` + allow null in `OnApplyTemplate`
- [ ] Centralize state transitions with `UpdateStates` helper
- [ ] Place `VisualStateManager.VisualStateGroups` on ControlTemplate root
- [ ] Place default style in Themes/Generic.xaml
- [ ] Call `DefaultStyleKeyProperty.OverrideMetadata` in static constructor
