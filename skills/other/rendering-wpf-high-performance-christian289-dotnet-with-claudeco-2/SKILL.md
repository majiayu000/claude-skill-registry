---
name: rendering-wpf-high-performance
description: Provides high-performance WPF rendering techniques including DrawingVisual, WriteableBitmap, CompositionTarget.Rendering, and BitmapCache. Use when implementing real-time graphics, game loops, particle systems, charts, or when Shape controls cause performance issues.
---

# High-Performance WPF Rendering

## Quick Reference

| Technique | Use Case | Performance |
|-----------|----------|-------------|
| DrawingVisual | 1K-100K shapes | 10-50x faster than Shape |
| WriteableBitmap | Pixel manipulation, heatmaps | Fastest for raw pixels |
| CompositionTarget.Rendering | Game loops, real-time animation | ~60 FPS frame callback |
| BitmapCache | Complex static visuals | GPU texture caching |

## 1. DrawingVisual Pattern

Lightweight visual for high-volume rendering without layout overhead.
```csharp
public class ChartVisual : FrameworkElement
{
    private readonly VisualCollection _visuals;

    public ChartVisual() => _visuals = new VisualCollection(this);

    public void Render(IEnumerable<Point> points)
    {
        _visuals.Clear();
        var visual = new DrawingVisual();

        using (var dc = visual.RenderOpen())
        {
            var pen = new Pen(Brushes.Blue, 1);
            pen.Freeze();

            var prev = points.First();
            foreach (var pt in points.Skip(1))
            {
                dc.DrawLine(pen, prev, pt);
                prev = pt;
            }
        }

        _visuals.Add(visual);
    }

    protected override int VisualChildrenCount => _visuals.Count;
    protected override Visual GetVisualChild(int index) => _visuals[index];
}
```

**Key Points:**
- Always `Freeze()` Brush/Pen for thread safety and performance
- Use `StreamGeometry` instead of `PathGeometry` for read-only paths
- Override `VisualChildrenCount` and `GetVisualChild`

## 2. WriteableBitmap Pattern

Direct pixel manipulation for maximum performance.
```csharp
public class PixelCanvas : Image
{
    private WriteableBitmap _bitmap;

    public void Initialize(int width, int height)
    {
        _bitmap = new WriteableBitmap(width, height, 96, 96, PixelFormats.Bgra32, null);
        Source = _bitmap;
    }

    public unsafe void DrawPixel(int x, int y, Color color)
    {
        _bitmap.Lock();
        try
        {
            var ptr = (byte*)_bitmap.BackBuffer;
            int stride = _bitmap.BackBufferStride;
            int offset = y * stride + x * 4;

            ptr[offset + 0] = color.B;
            ptr[offset + 1] = color.G;
            ptr[offset + 2] = color.R;
            ptr[offset + 3] = color.A;

            _bitmap.AddDirtyRect(new Int32Rect(x, y, 1, 1));
        }
        finally { _bitmap.Unlock(); }
    }
}
```

**Key Points:**
- Enable `<AllowUnsafeBlocks>true</AllowUnsafeBlocks>` in .csproj
- Use `AddDirtyRect` for partial updates
- BGRA32 format: Blue, Green, Red, Alpha order

## 3. CompositionTarget.Rendering

Per-frame callback for game loops and real-time updates.
```csharp
public class GameLoop
{
    private TimeSpan _lastRender;

    public void Start()
    {
        CompositionTarget.Rendering += OnRendering;
    }

    public void Stop()
    {
        CompositionTarget.Rendering -= OnRendering;
    }

    private void OnRendering(object sender, EventArgs e)
    {
        var args = (RenderingEventArgs)e;

        // Skip duplicate frames
        if (args.RenderingTime == _lastRender) return;

        var deltaTime = (args.RenderingTime - _lastRender).TotalSeconds;
        _lastRender = args.RenderingTime;

        Update(deltaTime);
        Render();
    }

    private void Update(double dt) { /* Physics, AI */ }
    private void Render() { /* Drawing */ }
}
```

**Critical:** Always unsubscribe in `Unloaded` event to prevent memory leaks.

## 4. BitmapCache

GPU-cached rendering for complex but static visuals.
```xml
<Border>
    <Border.CacheMode>
        <BitmapCache RenderAtScale="1" EnableClearType="False"/>
    </Border.CacheMode>
    <!-- Complex content here -->
</Border>
```
```csharp
element.CacheMode = new BitmapCache { RenderAtScale = 1.0 };
```

**When to Use:**
- ✅ Transform animations (rotate, scale, translate)
- ✅ Complex PathGeometry, DrawingVisual
- ❌ Frequently changing content
- ❌ Simple shapes (Rectangle, Ellipse)

## Performance Comparison

| Method | 10K Points | Use Case |
|--------|-----------|----------|
| Shape (Ellipse) | ~500ms | <100 elements |
| DrawingVisual | ~20ms | 1K-100K shapes |
| WriteableBitmap (managed) | ~5ms | Pixel grids |
| WriteableBitmap (unsafe) | ~1ms | Real-time heatmaps |

## Related References

For detailed implementation patterns, see:
- [reference/drawingvisual-advanced.md](reference/drawingvisual-advanced.md) - Hit testing, transforms
- [reference/writeablebitmap-algorithms.md](reference/writeablebitmap-algorithms.md) - Bresenham, flood fill
- [reference/compositiontarget-examples.md](reference/compositiontarget-examples.md) - Particle systems
- [reference/bitmapcache-optimization.md](reference/bitmapcache-optimization.md) - Memory management