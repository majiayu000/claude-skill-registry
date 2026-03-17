---
name: rendering-with-drawingvisual
description: Implements lightweight rendering using WPF DrawingVisual with ContainerVisual, VisualCollection, and DrawingContext. Use when rendering large-scale graphics, charts, game graphics, or custom visuals.
---

# WPF DrawingVisual Patterns

DrawingVisual is a lightweight visual element faster than Shape, suitable for large-scale rendering.

## 1. Visual Hierarchy

```
Visual (abstract)
├── UIElement
│   └── FrameworkElement
│       └── Shape (heavyweight, event support)
│
├── DrawingVisual       ← Lightweight, no events, direct rendering
├── ContainerVisual     ← Groups multiple Visuals
└── HostVisual          ← Cross-thread Visual
```

---

## 2. DrawingVisual vs Shape

| Aspect | DrawingVisual | Shape |
|--------|--------------|-------|
| **Overhead** | Low | High |
| **Layout** | Non-participating | Participating |
| **Events** | Manual implementation | Built-in support |
| **Data binding** | Not available | Available |
| **Use case** | Large elements, performance critical | Interactive UI |

---

## 3. Basic DrawingVisual Host

### 3.1 FrameworkElement Host

```csharp
namespace MyApp.Controls;

using System.Collections.Generic;
using System.Windows;
using System.Windows.Media;

/// <summary>
/// Control that hosts DrawingVisual
/// </summary>
public sealed class DrawingVisualHost : FrameworkElement
{
    private readonly List<Visual> _visuals = [];

    protected override int VisualChildrenCount => _visuals.Count;

    protected override Visual GetVisualChild(int index)
    {
        return _visuals[index];
    }

    /// <summary>
    /// Add Visual
    /// </summary>
    public void AddVisual(Visual visual)
    {
        _visuals.Add(visual);
        AddVisualChild(visual);
        AddLogicalChild(visual);
    }

    /// <summary>
    /// Remove Visual
    /// </summary>
    public void RemoveVisual(Visual visual)
    {
        _visuals.Remove(visual);
        RemoveVisualChild(visual);
        RemoveLogicalChild(visual);
    }

    /// <summary>
    /// Remove all Visuals
    /// </summary>
    public void ClearVisuals()
    {
        foreach (var visual in _visuals)
        {
            RemoveVisualChild(visual);
            RemoveLogicalChild(visual);
        }
        _visuals.Clear();
    }

    /// <summary>
    /// Find Visual at coordinate (Hit Testing)
    /// </summary>
    public Visual? GetVisualAt(Point point)
    {
        var hitResult = VisualTreeHelper.HitTest(this, point);
        return hitResult?.VisualHit;
    }
}
```

### 3.2 Creating DrawingVisual

```csharp
namespace MyApp.Graphics;

using System.Windows;
using System.Windows.Media;

public static class DrawingVisualFactory
{
    /// <summary>
    /// Create circular DrawingVisual
    /// </summary>
    public static DrawingVisual CreateCircle(
        Point center,
        double radius,
        Brush fill,
        Pen? stroke = null)
    {
        var visual = new DrawingVisual();

        using (var dc = visual.RenderOpen())
        {
            dc.DrawEllipse(fill, stroke, center, radius, radius);
        }

        return visual;
    }

    /// <summary>
    /// Create rectangle DrawingVisual
    /// </summary>
    public static DrawingVisual CreateRectangle(
        Rect rect,
        Brush fill,
        Pen? stroke = null)
    {
        var visual = new DrawingVisual();

        using (var dc = visual.RenderOpen())
        {
            dc.DrawRectangle(fill, stroke, rect);
        }

        return visual;
    }

    /// <summary>
    /// Create text DrawingVisual
    /// </summary>
    public static DrawingVisual CreateText(
        string text,
        Point origin,
        Brush foreground,
        double fontSize = 12)
    {
        var visual = new DrawingVisual();

        var formattedText = new FormattedText(
            text,
            System.Globalization.CultureInfo.CurrentCulture,
            FlowDirection.LeftToRight,
            new Typeface("Segoe UI"),
            fontSize,
            foreground,
            VisualTreeHelper.GetDpi(visual).PixelsPerDip);

        using (var dc = visual.RenderOpen())
        {
            dc.DrawText(formattedText, origin);
        }

        return visual;
    }

    /// <summary>
    /// Create image DrawingVisual
    /// </summary>
    public static DrawingVisual CreateImage(
        ImageSource image,
        Rect rect)
    {
        var visual = new DrawingVisual();

        using (var dc = visual.RenderOpen())
        {
            dc.DrawImage(image, rect);
        }

        return visual;
    }
}
```

---

## 4. ContainerVisual (Grouping)

### 4.1 Using ContainerVisual

```csharp
namespace MyApp.Graphics;

using System.Windows;
using System.Windows.Media;

public sealed class VisualGroup
{
    public ContainerVisual Container { get; } = new();

    /// <summary>
    /// Add child Visual
    /// </summary>
    public void Add(Visual visual)
    {
        Container.Children.Add(visual);
    }

    /// <summary>
    /// Remove child Visual
    /// </summary>
    public void Remove(Visual visual)
    {
        Container.Children.Remove(visual);
    }

    /// <summary>
    /// Move entire group
    /// </summary>
    public void SetOffset(double x, double y)
    {
        Container.Offset = new Vector(x, y);
    }

    /// <summary>
    /// Transform entire group
    /// </summary>
    public void SetTransform(Transform transform)
    {
        Container.Transform = transform;
    }

    /// <summary>
    /// Set opacity for entire group
    /// </summary>
    public void SetOpacity(double opacity)
    {
        Container.Opacity = opacity;
    }
}
```

### 4.2 Hierarchical Visual Structure

```csharp
// Hierarchical structure example
//
// ContainerVisual (root)
// ├── ContainerVisual (layer 1 - background)
// │   ├── DrawingVisual (grid)
// │   └── DrawingVisual (background image)
// ├── ContainerVisual (layer 2 - content)
// │   ├── DrawingVisual (node 1)
// │   ├── DrawingVisual (node 2)
// │   └── DrawingVisual (connections)
// └── ContainerVisual (layer 3 - overlay)
//     └── DrawingVisual (selection area)

public sealed class LayeredCanvas : FrameworkElement
{
    private readonly ContainerVisual _rootVisual = new();
    private readonly ContainerVisual _backgroundLayer = new();
    private readonly ContainerVisual _contentLayer = new();
    private readonly ContainerVisual _overlayLayer = new();

    public LayeredCanvas()
    {
        _rootVisual.Children.Add(_backgroundLayer);
        _rootVisual.Children.Add(_contentLayer);
        _rootVisual.Children.Add(_overlayLayer);

        AddVisualChild(_rootVisual);
    }

    protected override int VisualChildrenCount => 1;

    protected override Visual GetVisualChild(int index) => _rootVisual;

    public void AddToBackground(DrawingVisual visual)
    {
        _backgroundLayer.Children.Add(visual);
    }

    public void AddToContent(DrawingVisual visual)
    {
        _contentLayer.Children.Add(visual);
    }

    public void AddToOverlay(DrawingVisual visual)
    {
        _overlayLayer.Children.Add(visual);
    }
}
```

---

## 5. Hit Testing

### 5.1 Basic Hit Testing

```csharp
namespace MyApp.Controls;

using System.Windows;
using System.Windows.Input;
using System.Windows.Media;

public sealed class InteractiveDrawingHost : FrameworkElement
{
    private readonly List<DrawingVisual> _visuals = [];
    private DrawingVisual? _hoveredVisual;
    private DrawingVisual? _selectedVisual;

    public InteractiveDrawingHost()
    {
        MouseMove += OnMouseMove;
        MouseLeftButtonDown += OnMouseLeftButtonDown;
    }

    // ... VisualChildrenCount, GetVisualChild implementation omitted ...

    private void OnMouseMove(object sender, MouseEventArgs e)
    {
        var position = e.GetPosition(this);
        var hitVisual = HitTestVisual(position);

        if (hitVisual != _hoveredVisual)
        {
            // Hover state changed
            _hoveredVisual = hitVisual;
            Cursor = hitVisual is not null ? Cursors.Hand : Cursors.Arrow;
        }
    }

    private void OnMouseLeftButtonDown(object sender, MouseButtonEventArgs e)
    {
        var position = e.GetPosition(this);
        _selectedVisual = HitTestVisual(position);

        if (_selectedVisual is not null)
        {
            // Handle selected Visual
            OnVisualSelected(_selectedVisual);
        }
    }

    private DrawingVisual? HitTestVisual(Point point)
    {
        DrawingVisual? result = null;

        VisualTreeHelper.HitTest(
            this,
            null,
            hitResult =>
            {
                if (hitResult.VisualHit is DrawingVisual visual)
                {
                    result = visual;
                    return HitTestResultBehavior.Stop;
                }
                return HitTestResultBehavior.Continue;
            },
            new PointHitTestParameters(point));

        return result;
    }

    private void OnVisualSelected(DrawingVisual visual)
    {
        // Raise selection event
    }
}
```

### 5.2 Geometry-based Hit Testing

```csharp
/// <summary>
/// Find all Visuals within specific area
/// </summary>
public List<DrawingVisual> HitTestArea(Rect area)
{
    var results = new List<DrawingVisual>();
    var geometry = new RectangleGeometry(area);

    VisualTreeHelper.HitTest(
        this,
        null,
        hitResult =>
        {
            if (hitResult.VisualHit is DrawingVisual visual)
            {
                results.Add(visual);
            }
            return HitTestResultBehavior.Continue;
        },
        new GeometryHitTestParameters(geometry));

    return results;
}
```

---

## 6. Advanced Rendering

For advanced patterns, see [references/advanced-rendering.md](references/advanced-rendering.md):
- **Large-scale Rendering (Scatter Plot)**: 10,000+ point rendering example
- **RenderTargetBitmap**: Off-screen rendering and PNG export
- **Performance Optimization Tips**: Freeze, StreamGeometry, DrawingGroup

---

## 7. References

- [DrawingVisual Class - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/api/system.windows.media.drawingvisual)
- [Using DrawingVisual Objects - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/graphics-multimedia/using-drawingvisual-objects)
- [Hit Testing in the Visual Layer - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/graphics-multimedia/hit-testing-in-the-visual-layer)
