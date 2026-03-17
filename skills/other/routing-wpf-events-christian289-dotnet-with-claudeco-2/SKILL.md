---
name: routing-wpf-events
description: Implements WPF routed events including Bubbling, Tunneling, and Direct strategies. Use when creating custom routed events, handling event propagation, or understanding Preview events.
---

# WPF Routed Events Patterns

Understanding and implementing WPF's routed event system for event propagation through element trees.

## 1. Routing Strategies Overview

```
                    Window (Root)
                       │
    ┌──────────────────┼──────────────────┐
    │                  │                  │
  Grid              Border            StackPanel
    │                  │                  │
 Button             TextBox           ListBox
    │
ContentPresenter
    │
 TextBlock (Event Source)

Tunneling (Preview): Window → Grid → Button → ContentPresenter → TextBlock
Bubbling:            TextBlock → ContentPresenter → Button → Grid → Window
Direct:              Only TextBlock
```

---

## 2. Routing Strategy Types

| Strategy | Direction | Event Name Pattern | Use Case |
|----------|-----------|-------------------|----------|
| **Tunneling** | Root → Source (downward) | PreviewXxx | Input validation, cancellation before processing |
| **Bubbling** | Source → Root (upward) | Xxx | Normal event handling |
| **Direct** | Source only | Xxx | Events that don't propagate (MouseEnter, MouseLeave) |

---

## 3. Tunneling and Bubbling Example

### 3.1 XAML Setup

```xml
<Window PreviewMouseDown="Window_PreviewMouseDown"
        MouseDown="Window_MouseDown">
    <Grid PreviewMouseDown="Grid_PreviewMouseDown"
          MouseDown="Grid_MouseDown">
        <Button PreviewMouseDown="Button_PreviewMouseDown"
                MouseDown="Button_MouseDown"
                Content="Click Me"/>
    </Grid>
</Window>
```

### 3.2 Event Handler Order

```csharp
// Execution order when Button is clicked:
// 1. Window_PreviewMouseDown  (Tunneling)
// 2. Grid_PreviewMouseDown    (Tunneling)
// 3. Button_PreviewMouseDown  (Tunneling)
// 4. Button_MouseDown         (Bubbling)
// 5. Grid_MouseDown           (Bubbling)
// 6. Window_MouseDown         (Bubbling)

private void Window_PreviewMouseDown(object sender, MouseButtonEventArgs e)
{
    Debug.WriteLine("1. Window PreviewMouseDown (Tunneling)");
}

private void Grid_PreviewMouseDown(object sender, MouseButtonEventArgs e)
{
    Debug.WriteLine("2. Grid PreviewMouseDown (Tunneling)");
}

private void Button_PreviewMouseDown(object sender, MouseButtonEventArgs e)
{
    Debug.WriteLine("3. Button PreviewMouseDown (Tunneling)");
}

private void Button_MouseDown(object sender, MouseButtonEventArgs e)
{
    Debug.WriteLine("4. Button MouseDown (Bubbling)");
}

private void Grid_MouseDown(object sender, MouseButtonEventArgs e)
{
    Debug.WriteLine("5. Grid MouseDown (Bubbling)");
}

private void Window_MouseDown(object sender, MouseButtonEventArgs e)
{
    Debug.WriteLine("6. Window MouseDown (Bubbling)");
}
```

---

## 4. Stopping Event Propagation

### 4.1 Using Handled Property

```csharp
private void Button_PreviewMouseDown(object sender, MouseButtonEventArgs e)
{
    // Stop further propagation
    e.Handled = true;

    // Only events 1, 2, 3 will fire
}

private void Grid_MouseDown(object sender, MouseButtonEventArgs e)
{
    // Stop bubbling to parent
    e.Handled = true;

    // Window_MouseDown won't fire
}
```

### 4.2 Handling Already-Handled Events

```csharp
// Register handler that receives even handled events
public MainWindow()
{
    InitializeComponent();

    // handledEventsToo: true - receives events even if Handled = true
    AddHandler(
        MouseDownEvent,
        new MouseButtonEventHandler(OnMouseDownHandledToo),
        handledEventsToo: true);
}

private void OnMouseDownHandledToo(object sender, MouseButtonEventArgs e)
{
    // This handler is called even if e.Handled = true elsewhere
    Debug.WriteLine($"MouseDown received, Handled: {e.Handled}");
}
```

---

## 5. RoutedEventArgs Properties

```csharp
private void Element_MouseDown(object sender, MouseButtonEventArgs e)
{
    // Source: Element that raised the event (logical tree)
    var source = e.Source;

    // OriginalSource: Actual element clicked (visual tree)
    var originalSource = e.OriginalSource;

    // Example: Click on TextBlock inside Button
    // Source = Button (logical source)
    // OriginalSource = TextBlock (visual source)

    // RoutedEvent: The routed event being handled
    var routedEvent = e.RoutedEvent;

    // Handled: Whether the event has been handled
    var handled = e.Handled;
}
```

---

## 6. Creating Custom Routed Events

### 6.1 Bubbling Event

```csharp
namespace MyApp.Controls;

using System.Windows;

public class CustomSlider : Control
{
    // Register routed event
    public static readonly RoutedEvent ValueChangedEvent = EventManager.RegisterRoutedEvent(
        name: "ValueChanged",
        routingStrategy: RoutingStrategy.Bubble,
        handlerType: typeof(RoutedPropertyChangedEventHandler<double>),
        ownerType: typeof(CustomSlider));

    // CLR event wrapper
    public event RoutedPropertyChangedEventHandler<double> ValueChanged
    {
        add => AddHandler(ValueChangedEvent, value);
        remove => RemoveHandler(ValueChangedEvent, value);
    }

    // Raise the event
    protected virtual void OnValueChanged(double oldValue, double newValue)
    {
        var args = new RoutedPropertyChangedEventArgs<double>(oldValue, newValue, ValueChangedEvent);
        RaiseEvent(args);
    }
}
```

### 6.2 Tunneling Event (with Preview)

```csharp
namespace MyApp.Controls;

using System.Windows;

public class CustomButton : Button
{
    // Tunneling (Preview) event
    public static readonly RoutedEvent PreviewClickedEvent = EventManager.RegisterRoutedEvent(
        name: "PreviewClicked",
        routingStrategy: RoutingStrategy.Tunnel,
        handlerType: typeof(RoutedEventHandler),
        ownerType: typeof(CustomButton));

    // Bubbling event
    public static readonly RoutedEvent ClickedEvent = EventManager.RegisterRoutedEvent(
        name: "Clicked",
        routingStrategy: RoutingStrategy.Bubble,
        handlerType: typeof(RoutedEventHandler),
        ownerType: typeof(CustomButton));

    public event RoutedEventHandler PreviewClicked
    {
        add => AddHandler(PreviewClickedEvent, value);
        remove => RemoveHandler(PreviewClickedEvent, value);
    }

    public event RoutedEventHandler Clicked
    {
        add => AddHandler(ClickedEvent, value);
        remove => RemoveHandler(ClickedEvent, value);
    }

    protected override void OnClick()
    {
        // Raise Preview (Tunneling) first
        var previewArgs = new RoutedEventArgs(PreviewClickedEvent, this);
        RaiseEvent(previewArgs);

        // If not handled, raise Bubbling event
        if (!previewArgs.Handled)
        {
            var args = new RoutedEventArgs(ClickedEvent, this);
            RaiseEvent(args);
        }

        base.OnClick();
    }
}
```

### 6.3 Custom EventArgs

```csharp
namespace MyApp.Events;

using System.Windows;

public class ItemSelectedEventArgs : RoutedEventArgs
{
    public object SelectedItem { get; }
    public int SelectedIndex { get; }

    public ItemSelectedEventArgs(RoutedEvent routedEvent, object source, object selectedItem, int selectedIndex)
        : base(routedEvent, source)
    {
        SelectedItem = selectedItem;
        SelectedIndex = selectedIndex;
    }
}

public delegate void ItemSelectedEventHandler(object sender, ItemSelectedEventArgs e);
```

---

## 7. Class Event Handlers

### 7.1 Registering Class Handler

```csharp
namespace MyApp.Controls;

using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;

public class EnhancedTextBox : TextBox
{
    static EnhancedTextBox()
    {
        // Class handler - called before instance handlers
        EventManager.RegisterClassHandler(
            typeof(EnhancedTextBox),
            PreviewKeyDownEvent,
            new KeyEventHandler(OnPreviewKeyDownClass));

        EventManager.RegisterClassHandler(
            typeof(EnhancedTextBox),
            GotFocusEvent,
            new RoutedEventHandler(OnGotFocusClass));
    }

    private static void OnPreviewKeyDownClass(object sender, KeyEventArgs e)
    {
        // Called for all EnhancedTextBox instances
        if (sender is EnhancedTextBox textBox)
        {
            // Common keyboard handling logic
        }
    }

    private static void OnGotFocusClass(object sender, RoutedEventArgs e)
    {
        // Auto-select all text on focus
        if (sender is EnhancedTextBox textBox)
        {
            textBox.SelectAll();
        }
    }
}
```

---

## 8. Attached Events

### 8.1 Using Attached Events

```xml
<!-- Handle Button.Click at Grid level (Bubbling) -->
<Grid Button.Click="Grid_ButtonClick">
    <StackPanel>
        <Button Content="Button 1"/>
        <Button Content="Button 2"/>
        <Button Content="Button 3"/>
    </StackPanel>
</Grid>
```

```csharp
private void Grid_ButtonClick(object sender, RoutedEventArgs e)
{
    // Handle clicks from any child button
    if (e.OriginalSource is Button button)
    {
        Debug.WriteLine($"Clicked: {button.Content}");
    }
}
```

### 8.2 Defining Attached Events

```csharp
namespace MyApp.Behaviors;

using System.Windows;

public static class ValidationBehavior
{
    // Attached routed event
    public static readonly RoutedEvent ValidationErrorEvent = EventManager.RegisterRoutedEvent(
        name: "ValidationError",
        routingStrategy: RoutingStrategy.Bubble,
        handlerType: typeof(RoutedEventHandler),
        ownerType: typeof(ValidationBehavior));

    public static void AddValidationErrorHandler(DependencyObject d, RoutedEventHandler handler)
    {
        if (d is UIElement element)
        {
            element.AddHandler(ValidationErrorEvent, handler);
        }
    }

    public static void RemoveValidationErrorHandler(DependencyObject d, RoutedEventHandler handler)
    {
        if (d is UIElement element)
        {
            element.RemoveHandler(ValidationErrorEvent, handler);
        }
    }

    // Raise the attached event
    public static void RaiseValidationError(UIElement element)
    {
        element.RaiseEvent(new RoutedEventArgs(ValidationErrorEvent, element));
    }
}
```

---

## 9. Common Event Handling Patterns

### 9.1 Event Aggregation

```csharp
// Handle events from multiple child elements at parent level
private void ParentPanel_PreviewMouseDown(object sender, MouseButtonEventArgs e)
{
    // Find the clicked element type
    var clickedElement = e.OriginalSource as FrameworkElement;

    switch (clickedElement)
    {
        case Button button:
            HandleButtonClick(button);
            break;
        case TextBlock textBlock:
            HandleTextBlockClick(textBlock);
            break;
        case Image image:
            HandleImageClick(image);
            break;
    }
}
```

### 9.2 Event Suppression

```csharp
// Suppress events for specific conditions
private void Element_PreviewMouseDown(object sender, MouseButtonEventArgs e)
{
    if (IsReadOnly || IsDisabled)
    {
        // Prevent all mouse handling
        e.Handled = true;
    }
}
```

---

## 10. References

- [Routed Events Overview - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/routed-events-overview)
- [How to: Create a Custom Routed Event - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/how-to-create-a-custom-routed-event)
- [Marking Routed Events as Handled - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/marking-routed-events-as-handled-and-class-handling)
