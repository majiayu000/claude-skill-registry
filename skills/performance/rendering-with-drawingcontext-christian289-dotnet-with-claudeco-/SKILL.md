---
name: rendering-with-drawingcontext
description: "Renders high-performance graphics using WPF DrawingContext for 10-50x improvement over Shape. Use when drawing large numbers of shapes or optimizing rendering performance."
---

# WPF DrawingContext High-Performance Rendering

A pattern for achieving 10-50x performance improvement over Shape objects when rendering large numbers of shapes in WPF using DrawingContext.

## 1. Core Concepts

### Shape vs DrawingContext Approach

| Item | Shape (Polygon, Rectangle, etc.) | DrawingContext |
|------|----------------------------------|----------------|
| **Inheritance** | Canvas | FrameworkElement |
| **Visual count** | One per shape (n) | 1 |
| **Layout calculation** | O(n) Measure/Arrange | O(1) |
| **Memory usage** | Very high (WPF object overhead) | Very low (data only) |
| **Performance** | Baseline | **10-50x faster** |
| **Suitable for** | Few interactive shapes (tens to hundreds) | Large static shapes (thousands to tens of thousands) |

### Why is DrawingContext Fast?

1. **Single Visual**: Only 1 FrameworkElement registered in Visual Tree
2. **Layout bypass**: No Measure/Arrange calculations needed
3. **Batch rendering**: Sent to GPU as single batch
4. **Memory efficiency**: Only stores shape metadata

---

## 2. Basic Implementation Pattern

### 2.1 DrawingContext-Based Custom Control

```csharp
namespace MyApp.Controls;

using System.Windows;
using System.Windows.Media;

public sealed class HighPerformanceCanvas : FrameworkElement
{
    // 1. Struct for storing shape data (lightweight)
    private readonly record struct ShapeData(
        Point Position,
        double Width,
        double Height,
        Brush Fill);

    // 2. Only rendering data stored in memory
    private readonly List<ShapeData> _shapes = [];

    // 3. Optimized Pen (Freeze applied)
    private readonly Pen _pen = new(Brushes.Black, 1);

    public HighPerformanceCanvas()
    {
        // Freeze Pen for performance optimization
        _pen.Freeze();
    }

    // 4. Shape addition method
    public void AddShape(Point position, double width, double height, Color color)
    {
        var brush = new SolidColorBrush(color);
        brush.Freeze();  // Freeze for performance optimization

        _shapes.Add(new ShapeData(position, width, height, brush));
    }

    // 5. Trigger rendering (call once after data addition is complete)
    public void Render()
    {
        InvalidateVisual();
    }

    // 6. Actual rendering - direct drawing in OnRender
    protected override void OnRender(DrawingContext dc)
    {
        base.OnRender(dc);

        foreach (var shape in _shapes)
        {
            dc.DrawRectangle(
                shape.Fill,
                _pen,
                new Rect(shape.Position, new Size(shape.Width, shape.Height)));
        }
    }

    // 7. Clear shapes
    public void Clear()
    {
        _shapes.Clear();
        InvalidateVisual();
    }
}
```

---

## 3. Complex Shapes (Using StreamGeometry)

Use StreamGeometry for complex shapes like triangles and polygons.

### 3.1 Triangle Rendering Example

```csharp
namespace MyApp.Controls;

using System.Windows;
using System.Windows.Media;

public sealed class TriangleCanvas : FrameworkElement
{
    private readonly record struct TriangleData(
        Point Point1, Point Point2, Point Point3, Brush Fill);

    private readonly List<TriangleData> _triangles = [];
    private readonly Pen _pen = new(Brushes.Black, 1);

    public TriangleCanvas()
    {
        _pen.Freeze();
    }

    public void AddTriangle(Point p1, Point p2, Point p3, Color color)
    {
        var brush = new SolidColorBrush(color);
        brush.Freeze();

        _triangles.Add(new TriangleData(p1, p2, p3, brush));
    }

    public void Render()
    {
        InvalidateVisual();
    }

    protected override void OnRender(DrawingContext dc)
    {
        base.OnRender(dc);

        foreach (var triangle in _triangles)
        {
            // Create lightweight geometry using StreamGeometry
            var geometry = new StreamGeometry();

            using (var ctx = geometry.Open())
            {
                ctx.BeginFigure(triangle.Point1, isFilled: true, isClosed: true);
                ctx.LineTo(triangle.Point2, isStroked: true, isSmoothJoin: false);
                ctx.LineTo(triangle.Point3, isStroked: true, isSmoothJoin: false);
            }

            geometry.Freeze();  // Optimize by making immutable

            dc.DrawGeometry(triangle.Fill, _pen, geometry);
        }
    }

    public void Clear()
    {
        _triangles.Clear();
        InvalidateVisual();
    }
}
```

---

## 4. Pattern with Performance Measurement

### 4.1 Async Rendering + Performance Measurement

```csharp
namespace MyApp.Controls;

using System.Diagnostics;
using System.Windows;
using System.Windows.Media;
using System.Windows.Threading;

public sealed class BenchmarkCanvas : FrameworkElement
{
    private readonly record struct RectData(Rect Bounds, Brush Fill);

    private readonly List<RectData> _items = [];
    private readonly Pen _pen = new(Brushes.Black, 1);

    public BenchmarkCanvas()
    {
        _pen.Freeze();
    }

    /// <summary>
    /// Renders a large number of shapes and returns the elapsed time.
    /// </summary>
    public async Task<TimeSpan> DrawItemsAsync(int count)
    {
        _items.Clear();

        double width = ActualWidth > 0 ? ActualWidth : 400;
        double height = ActualHeight > 0 ? ActualHeight : 400;

        var random = new Random();

        // Step 1: Generate data only (before measurement)
        for (int i = 0; i < count; i++)
        {
            double x = random.NextDouble() * (width - 20);
            double y = random.NextDouble() * (height - 20);
            double size = 10 + random.NextDouble() * 20;

            var brush = new SolidColorBrush(Color.FromRgb(
                (byte)random.Next(256),
                (byte)random.Next(256),
                (byte)random.Next(256)));
            brush.Freeze();

            _items.Add(new RectData(new Rect(x, y, size, size), brush));

            // Yield periodically to prevent UI hang
            if (i % 100 == 0)
            {
                await Dispatcher.InvokeAsync(() => { }, DispatcherPriority.Background);
            }
        }

        // Step 2: Measure rendering only (call once)
        var stopwatch = Stopwatch.StartNew();
        InvalidateVisual();
        await Dispatcher.InvokeAsync(() => { }, DispatcherPriority.Render);
        stopwatch.Stop();

        return stopwatch.Elapsed;
    }

    protected override void OnRender(DrawingContext dc)
    {
        base.OnRender(dc);

        foreach (var item in _items)
        {
            dc.DrawRectangle(item.Fill, _pen, item.Bounds);
        }
    }

    public void Clear()
    {
        _items.Clear();
        InvalidateVisual();
    }
}
```

---

## 5. Key Optimization Techniques

### 5.1 Freeze() - Making Objects Immutable

```csharp
// ✅ Pen optimization
private readonly Pen _pen = new(Brushes.Black, 1);
public MyControl()
{
    _pen.Freeze();  // WPF can optimize internally
}

// ✅ Brush optimization
var brush = new SolidColorBrush(Color.FromRgb(255, 0, 0));
brush.Freeze();  // Can be shared in memory

// ✅ Geometry optimization
var geometry = new StreamGeometry();
// ... configure geometry ...
geometry.Freeze();  // Rendering pipeline optimization
```

### 5.2 Using record struct

```csharp
// ✅ Value type (stack allocation) → Memory efficient
private readonly record struct ShapeData(
    Point Position,
    Size Size,
    Brush Fill);

// Auto-generated Equals, GetHashCode
// Immutable semantics enforced
```

### 5.3 StreamGeometry vs PathGeometry

```csharp
// ✅ StreamGeometry - Lightweight, write-only
var geometry = new StreamGeometry();
using (var ctx = geometry.Open())
{
    ctx.BeginFigure(startPoint, true, true);
    ctx.LineTo(point2, true, false);
}

// ❌ PathGeometry - Relatively heavyweight
var geometry = new PathGeometry();
var figure = new PathFigure { StartPoint = startPoint };
figure.Segments.Add(new LineSegment(point2, true));
```

---

## 6. InvalidateVisual() Cautions

### O(n²) Complexity Pattern

```csharp
// ❌ Bad example: Calling InvalidateVisual() inside loop
for (int i = 0; i < count; i++)
{
    _items.Add(data);
    if (i % 10 == 0)
    {
        InvalidateVisual();  // OnRender iterates entire _items!
    }
}
// Result: 10 + 20 + ... + n = O(n²)
```

### ✅ Correct Pattern: Call Once at the End

```csharp
// ✅ Good example: Render only once after data collection
for (int i = 0; i < count; i++)
{
    _items.Add(data);
}

// Render only once at the end
InvalidateVisual();
```

**Performance Difference**:
- Bad pattern: 10,000 items takes **several seconds**
- Correct pattern: 10,000 items takes **tens of ms**

---

## 7. Integration with MVVM Pattern

### 7.1 ViewModel - Delegate Pattern

Pattern allowing ViewModel to call rendering methods without directly referencing View type:

```csharp
namespace MyApp.ViewModels;

using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;

public sealed partial class RenderViewModel : ObservableObject
{
    // Store only delegates without View type reference
    private Func<int, Task<TimeSpan>>? _drawItems;
    private Action? _clearCanvas;

    [ObservableProperty] private bool _isRendering;

    [ObservableProperty] private string _elapsedTime = "Waiting...";

    // Inject required methods from View
    public void SetRenderActions(
        Func<int, Task<TimeSpan>> drawItems,
        Action clearCanvas)
    {
        _drawItems = drawItems;
        _clearCanvas = clearCanvas;
    }

    [RelayCommand]
    private async Task RenderAsync()
    {
        if (_drawItems is null)
        {
            return;
        }

        IsRendering = true;
        _clearCanvas?.Invoke();

        var elapsed = await _drawItems(10000);
        ElapsedTime = $"{elapsed.TotalMilliseconds:F2} ms";

        IsRendering = false;
    }
}
```

### 7.2 View - Delegate Connection

```csharp
namespace MyApp.Views;

using System.Windows;
using MyApp.ViewModels;

public partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();

        Loaded += (_, _) =>
        {
            if (DataContext is RenderViewModel vm)
            {
                vm.SetRenderActions(
                    MyCanvas.DrawItemsAsync,
                    MyCanvas.Clear);
            }
        };
    }
}
```

---

## 8. Comparison with Shape Approach (Reference)

There are cases where Shape approach is needed:

```csharp
// Shape approach - suitable for few shapes requiring interaction
public sealed class ShapeBasedPanel : Canvas
{
    public void AddInteractiveShape()
    {
        var polygon = new Polygon
        {
            Points = [new Point(0, 0), new Point(50, 0), new Point(25, 50)],
            Fill = Brushes.Blue,
            Stroke = Brushes.Black,
            StrokeThickness = 1
        };

        // Can attach events to individual shapes
        polygon.MouseEnter += (s, e) => polygon.Fill = Brushes.Red;
        polygon.MouseLeave += (s, e) => polygon.Fill = Brushes.Blue;

        Children.Add(polygon);
    }
}
```

**When to Choose Shape Approach**:
- Number of shapes is tens to hundreds or less
- Mouse events needed on individual shapes
- Drag and drop functionality required

---

## 9. Performance Comparison Example

**Based on 10,000 triangles**:

| Method | Expected Time | Notes |
|--------|---------------|-------|
| Shape (Polygon) | 500-2000ms | Visual Tree overhead |
| DrawingContext | 20-50ms | Direct drawing |
| **Performance Ratio** | **10-50x** | Varies by environment |

---

## 10. Checklist

- [ ] Inherit from FrameworkElement (instead of Canvas)
- [ ] Apply Freeze() to Pen, Brush
- [ ] Store shape data as record struct
- [ ] Use StreamGeometry for complex shapes
- [ ] Call InvalidateVisual() **only once** after data addition is complete
- [ ] Use Dispatcher.InvokeAsync to yield UI during large data generation
- [ ] ViewModel uses delegate pattern without View type reference

---

## 11. References

- [DrawingContext - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/api/system.windows.media.drawingcontext)
- [StreamGeometry - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/api/system.windows.media.streamgeometry)
- [Optimizing WPF Performance - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/optimizing-performance-2d-graphics-and-imaging)
