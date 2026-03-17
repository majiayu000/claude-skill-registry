---
name: implementing-wpf-adorners
description: Implements WPF Adorner decoration layers with AdornerLayer, AdornerDecorator, and custom Adorner patterns. Use when building drag handles, validation indicators, watermarks, selection visuals, or resize grips.
---

# WPF Adorner Patterns

Adorner is a mechanism for overlaying decorative visual elements on top of UIElements.

## 1. Adorner Concept

### 1.1 Characteristics

- **AdornerLayer**: Separate rendering layer that holds Adorners
- **Z-Order**: Always renders above the adorned element
- **Layout Independent**: No effect on target element's layout
- **Event Support**: Can receive mouse/keyboard events

### 1.2 Usage Scenarios

| Scenario | Description |
|----------|-------------|
| **Validation Display** | Input field error display |
| **Drag Handles** | Element move/resize handles |
| **Watermark** | Hint text for empty TextBox |
| **Selection Display** | Highlight selected elements |
| **Tooltip/Badge** | Additional info display on elements |
| **Drag and Drop** | Preview during drag |

---

## 2. Basic Adorner Implementation

### 2.1 Simple Adorner

```csharp
namespace MyApp.Adorners;

using System.Windows;
using System.Windows.Documents;
using System.Windows.Media;

/// <summary>
/// Adorner that draws border around element
/// </summary>
public sealed class BorderAdorner : Adorner
{
    private readonly Pen _borderPen;

    public BorderAdorner(UIElement adornedElement) : base(adornedElement)
    {
        _borderPen = new Pen(Brushes.Red, 2)
        {
            DashStyle = DashStyles.Dash
        };
        _borderPen.Freeze();

        // Disable mouse events (decoration only)
        IsHitTestVisible = false;
    }

    protected override void OnRender(DrawingContext drawingContext)
    {
        var rect = new Rect(AdornedElement.RenderSize);

        // Draw border
        drawingContext.DrawRectangle(null, _borderPen, rect);
    }
}
```

### 2.2 Applying Adorner

```csharp
// Get AdornerLayer
var adornerLayer = AdornerLayer.GetAdornerLayer(targetElement);

if (adornerLayer is not null)
{
    // Add Adorner
    var adorner = new BorderAdorner(targetElement);
    adornerLayer.Add(adorner);
}
```

### 2.3 Removing Adorner

```csharp
// Remove all Adorners from specific element
var adornerLayer = AdornerLayer.GetAdornerLayer(targetElement);
var adorners = adornerLayer?.GetAdorners(targetElement);

if (adorners is not null)
{
    foreach (var adorner in adorners)
    {
        adornerLayer!.Remove(adorner);
    }
}
```

---

## 3. AdornerDecorator

### 3.1 Default Location

```xml
<!-- Window default template includes AdornerDecorator -->
<Window>
    <!-- AdornerDecorator is automatically included -->
    <Grid>
        <TextBox x:Name="MyTextBox"/>
    </Grid>
</Window>
```

### 3.2 Explicit AdornerDecorator

```xml
<!-- Explicit AdornerDecorator in ControlTemplate -->
<ControlTemplate TargetType="{x:Type ContentControl}">
    <AdornerDecorator>
        <ContentPresenter/>
    </AdornerDecorator>
</ControlTemplate>

<!-- In Popup or special containers -->
<Popup>
    <AdornerDecorator>
        <Border>
            <StackPanel>
                <TextBox/>
                <Button Content="OK"/>
            </StackPanel>
        </Border>
    </AdornerDecorator>
</Popup>
```

---

## 4. Practical Adorner Examples

### 4.1 Watermark Adorner

```csharp
namespace MyApp.Adorners;

using System.Windows;
using System.Windows.Controls;
using System.Windows.Documents;
using System.Windows.Media;

/// <summary>
/// Display watermark (hint text) on TextBox
/// </summary>
public sealed class WatermarkAdorner : Adorner
{
    private readonly TextBlock _watermarkText;

    public WatermarkAdorner(UIElement adornedElement, string watermark)
        : base(adornedElement)
    {
        _watermarkText = new TextBlock
        {
            Text = watermark,
            Foreground = Brushes.Gray,
            FontStyle = FontStyles.Italic,
            Margin = new Thickness(4, 2, 0, 0),
            IsHitTestVisible = false
        };

        AddVisualChild(_watermarkText);

        IsHitTestVisible = false;
    }

    protected override int VisualChildrenCount => 1;

    protected override Visual GetVisualChild(int index) => _watermarkText;

    protected override Size MeasureOverride(Size constraint)
    {
        _watermarkText.Measure(constraint);
        return _watermarkText.DesiredSize;
    }

    protected override Size ArrangeOverride(Size finalSize)
    {
        _watermarkText.Arrange(new Rect(finalSize));
        return finalSize;
    }
}
```

### 4.2 Watermark Attached Property

```csharp
namespace MyApp.Behaviors;

using System.Windows;
using System.Windows.Controls;
using System.Windows.Documents;
using MyApp.Adorners;

public static class Watermark
{
    public static readonly DependencyProperty TextProperty =
        DependencyProperty.RegisterAttached(
            "Text",
            typeof(string),
            typeof(Watermark),
            new PropertyMetadata(null, OnTextChanged));

    public static string GetText(DependencyObject obj) =>
        (string)obj.GetValue(TextProperty);

    public static void SetText(DependencyObject obj, string value) =>
        obj.SetValue(TextProperty, value);

    private static void OnTextChanged(DependencyObject d, DependencyPropertyChangedEventArgs e)
    {
        if (d is not TextBox textBox)
        {
            return;
        }

        textBox.Loaded -= OnTextBoxLoaded;
        textBox.Loaded += OnTextBoxLoaded;
        textBox.TextChanged -= OnTextBoxTextChanged;
        textBox.TextChanged += OnTextBoxTextChanged;
    }

    private static void OnTextBoxLoaded(object sender, RoutedEventArgs e)
    {
        if (sender is TextBox textBox)
        {
            UpdateWatermark(textBox);
        }
    }

    private static void OnTextBoxTextChanged(object sender, TextChangedEventArgs e)
    {
        if (sender is TextBox textBox)
        {
            UpdateWatermark(textBox);
        }
    }

    private static void UpdateWatermark(TextBox textBox)
    {
        var adornerLayer = AdornerLayer.GetAdornerLayer(textBox);
        if (adornerLayer is null)
        {
            return;
        }

        // Remove existing watermark
        RemoveWatermark(textBox, adornerLayer);

        // Add watermark if text is empty
        if (string.IsNullOrEmpty(textBox.Text))
        {
            var watermark = GetText(textBox);
            if (!string.IsNullOrEmpty(watermark))
            {
                adornerLayer.Add(new WatermarkAdorner(textBox, watermark));
            }
        }
    }

    private static void RemoveWatermark(TextBox textBox, AdornerLayer adornerLayer)
    {
        var adorners = adornerLayer.GetAdorners(textBox);
        if (adorners is null)
        {
            return;
        }

        foreach (var adorner in adorners)
        {
            if (adorner is WatermarkAdorner)
            {
                adornerLayer.Remove(adorner);
            }
        }
    }
}
```

### 4.3 Using Watermark in XAML

```xml
<TextBox local:Watermark.Text="Enter email address"/>
```

---

## 5. Advanced Adorner Patterns

For advanced patterns, see [references/advanced-adorners.md](references/advanced-adorners.md):
- **Resize Handle Adorner**: Element resizing with corner/edge handles
- **Validation Error Adorner**: Display validation errors with icons
- **Drag Preview Adorner**: Visual feedback during drag operations
- **Adorner Management Service**: Lifecycle management utilities

---

## 6. Checklist

- [ ] Verify AdornerLayer exists before adding Adorner
- [ ] Set `IsHitTestVisible = false` for decoration-only Adorners
- [ ] Correctly implement VisualChildrenCount and GetVisualChild
- [ ] Arrange children using MeasureOverride and ArrangeOverride
- [ ] Remove unnecessary Adorners (prevent memory leaks)
- [ ] Explicitly add AdornerDecorator in Popup, etc.

---

## 7. References

- [Adorners Overview - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/controls/adorners-overview)
- [Adorner Class - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/api/system.windows.documents.adorner)
