---
name: implementing-hit-testing
description: "Enables mouse event reception for WPF FrameworkElement using DrawingContext by drawing transparent backgrounds. Use when custom-drawn elements don't receive mouse events."
---

# WPF FrameworkElement Hit Testing

An essential pattern for receiving mouse events when rendering directly with `OnRender(DrawingContext)` in a class that inherits from `FrameworkElement`.

## 1. Problem Scenario

### Symptoms
- Events like `MouseLeftButtonDown`, `MouseMove` don't fire on controls inheriting from `FrameworkElement`
- Nothing happens when clicking

### Cause
WPF Hit Testing is performed based on rendered pixels. If nothing is drawn in `OnRender()` or there's no background, that area is considered "empty" and mouse events won't be delivered.

---

## 2. Solution

### 2.1 Draw Transparent Background (Required)

```csharp
namespace MyApp.Controls;

using System.Windows;
using System.Windows.Media;

public sealed class MyOverlay : FrameworkElement
{
    protected override void OnRender(DrawingContext dc)
    {
        base.OnRender(dc);

        // ⚠️ Required: Draw transparent background (for mouse event reception)
        dc.DrawRectangle(
            Brushes.Transparent,
            null,
            new Rect(0, 0, ActualWidth, ActualHeight));

        // Actual rendering logic follows
        DrawContent(dc);
    }

    private void DrawContent(DrawingContext dc)
    {
        // Draw actual content
    }
}
```

---

## 3. Why Transparent?

### Transparent vs null

| Setting | Hit Test Result | Visual Result |
|---------|-----------------|---------------|
| `Brushes.Transparent` | ✅ Success | Not visible |
| `null` | ❌ Failure | Not visible |
| `new SolidColorBrush(Color.FromArgb(0, 0, 0, 0))` | ✅ Success | Not visible |

`Transparent` is an "existing" brush with Alpha channel of 0. WPF Hit Testing checks if a brush **exists**, so it behaves differently from `null`.

---

## 4. Practical Example

### 4.1 Measurement Tool Overlay

```csharp
namespace MyApp.Controls;

using System.Windows;
using System.Windows.Media;

public sealed class RulerOverlay : FrameworkElement
{
    private static readonly Pen LinePen;
    private static readonly Brush TextBrush;

    static RulerOverlay()
    {
        // Frozen resources (performance optimization)
        LinePen = new Pen(Brushes.Yellow, 2);
        LinePen.Freeze();
        TextBrush = Brushes.Yellow;
    }

    public Point StartPoint { get; set; }
    public Point EndPoint { get; set; }
    public bool IsDrawing { get; set; }

    protected override void OnRender(DrawingContext dc)
    {
        base.OnRender(dc);

        // 1. Transparent background (required for hit testing)
        dc.DrawRectangle(
            Brushes.Transparent,
            null,
            new Rect(0, 0, ActualWidth, ActualHeight));

        // 2. Draw actual measurement line
        if (IsDrawing)
        {
            dc.DrawLine(LinePen, StartPoint, EndPoint);
        }
    }

    protected override void OnMouseLeftButtonDown(MouseButtonEventArgs e)
    {
        base.OnMouseLeftButtonDown(e);

        // Now events are received normally
        StartPoint = e.GetPosition(this);
        IsDrawing = true;
        CaptureMouse();
    }

    protected override void OnMouseMove(MouseEventArgs e)
    {
        base.OnMouseMove(e);

        if (IsDrawing)
        {
            EndPoint = e.GetPosition(this);
            InvalidateVisual();  // Redraw
        }
    }

    protected override void OnMouseLeftButtonUp(MouseButtonEventArgs e)
    {
        base.OnMouseLeftButtonUp(e);

        if (IsDrawing)
        {
            IsDrawing = false;
            ReleaseMouseCapture();
        }
    }
}
```

---

## 5. Connecting Events in Code-Behind

The same principle applies when connecting events in XAML:

```xml
<controls:RulerOverlay x:Name="RulerOverlay"
                       MouseLeftButtonDown="RulerOverlay_MouseLeftButtonDown"
                       MouseMove="RulerOverlay_MouseMove"
                       MouseLeftButtonUp="RulerOverlay_MouseLeftButtonUp" />
```

```csharp
// Code-behind
private void RulerOverlay_MouseLeftButtonDown(object sender, MouseButtonEventArgs e)
{
    if (sender is RulerOverlay overlay)
    {
        // Without transparent background, this event won't fire!
        var point = e.GetPosition(overlay);
        // ...
    }
}
```

---

## 6. Relationship with IsHitTestVisible Property

### Caution

```xml
<!-- IsHitTestVisible="False" blocks events regardless of transparent background -->
<controls:MyOverlay IsHitTestVisible="False" />
```

| Setting | Transparent Background | Hit Test Result |
|---------|------------------------|-----------------|
| `IsHitTestVisible="True"` (default) | Yes | ✅ Success |
| `IsHitTestVisible="True"` | No | ❌ Failure |
| `IsHitTestVisible="False"` | Yes | ❌ Failure |
| `IsHitTestVisible="False"` | No | ❌ Failure |

---

## 7. Checklist

- [ ] Draw entire area background with `Brushes.Transparent` in `OnRender()`
- [ ] Draw background **before** other content
- [ ] Verify `IsHitTestVisible` is `True` (default)
- [ ] Apply `Freeze()` to Pen, Brush (performance optimization)

---

## 8. Common Mistakes

### ❌ Wrong: No background

```csharp
protected override void OnRender(DrawingContext dc)
{
    base.OnRender(dc);

    // Draw content without background
    dc.DrawLine(LinePen, StartPoint, EndPoint);  // Hit Test succeeds only on the line
}
```

### ✅ Correct: Include transparent background

```csharp
protected override void OnRender(DrawingContext dc)
{
    base.OnRender(dc);

    // 1. Transparent background first
    dc.DrawRectangle(Brushes.Transparent, null,
        new Rect(0, 0, ActualWidth, ActualHeight));

    // 2. Then content
    dc.DrawLine(LinePen, StartPoint, EndPoint);
}
```

---

## 9. References

- [Hit Testing in the Visual Layer - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/graphics-multimedia/hit-testing-in-the-visual-layer)
- [FrameworkElement.OnRender - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/api/system.windows.frameworkelement.onrender)
