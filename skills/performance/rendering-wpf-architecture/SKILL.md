---
name: rendering-wpf-architecture
description: Explains WPF rendering pipeline (Measure/Arrange/Render passes) and hardware acceleration tiers. Use when debugging layout issues, optimizing render performance, or understanding why software rendering occurs.
---

# WPF Rendering Architecture

## Rendering Pipeline Overview
```
User Input → Property Change → InvalidateXxx()
                ↓
        ┌───────────────┐
        │ Measure Pass  │ → Determines DesiredSize
        ├───────────────┤
        │ Arrange Pass  │ → Determines ActualSize/Position
        ├───────────────┤
        │ Render Pass   │ → OnRender() / DrawingContext
        └───────────────┘
                ↓
    Composition Tree → MILCore → DirectX → GPU
```

## 1. Layout Passes

### Invalidation Methods

| Method | Triggers | Use When |
|--------|----------|----------|
| `InvalidateMeasure()` | Measure + Arrange + Render | Size might change |
| `InvalidateArrange()` | Arrange + Render | Position might change |
| `InvalidateVisual()` | Render only | Visual appearance change |

### FrameworkPropertyMetadata Flags
```csharp
public static readonly DependencyProperty RadiusProperty =
    DependencyProperty.Register("Radius", typeof(double), typeof(MyControl),
        new FrameworkPropertyMetadata(10.0,
            FrameworkPropertyMetadataOptions.AffectsRender |
            FrameworkPropertyMetadataOptions.AffectsMeasure));
```

| Flag | Effect |
|------|--------|
| `AffectsMeasure` | Triggers Measure pass |
| `AffectsArrange` | Triggers Arrange pass |
| `AffectsRender` | Triggers Render pass |
| `AffectsParentMeasure` | Parent re-measures |
| `AffectsParentArrange` | Parent re-arranges |

### Custom Control Layout
```csharp
protected override Size MeasureOverride(Size availableSize)
{
    // Calculate desired size based on content
    double width = Math.Min(200, availableSize.Width);
    double height = Math.Min(100, availableSize.Height);
    return new Size(width, height);
}

protected override Size ArrangeOverride(Size finalSize)
{
    // Position children within finalSize
    foreach (UIElement child in Children)
    {
        child.Arrange(new Rect(0, 0, finalSize.Width, finalSize.Height));
    }
    return finalSize;
}

protected override void OnRender(DrawingContext dc)
{
    dc.DrawRectangle(Background, null, new Rect(RenderSize));
}
```

## 2. Hardware Acceleration

### Rendering Tiers

| Tier | GPU Memory | Features |
|------|-----------|----------|
| 0 | < 30MB | Software rendering |
| 1 | 30-120MB | Partial hardware (no PS 2.0) |
| 2 | ≥ 120MB | Full hardware acceleration |
```csharp
int tier = RenderCapability.Tier >> 16;
// 0 = Software, 1 = Partial, 2 = Full GPU
```

### Software Fallback Conditions

WPF falls back to software rendering when:
- GPU memory insufficient
- Texture > 8192px
- Remote Desktop (RDP) session
- `AllowsTransparency="True"` on Window
- Legacy `BitmapEffect` used

### RenderOptions Optimization
```csharp
// For images that will be scaled
RenderOptions.SetBitmapScalingMode(image, BitmapScalingMode.LowQuality);

// For pixel-perfect lines
RenderOptions.SetEdgeMode(element, EdgeMode.Aliased);

// For tiled brushes
RenderOptions.SetCachingHint(brush, CachingHint.Cache);
RenderOptions.SetCacheInvalidationThresholdMinimum(brush, 0.5);
RenderOptions.SetCacheInvalidationThresholdMaximum(brush, 2.0);
```

## 3. Performance Optimization

### Batch Updates Pattern
```csharp
// Bad: Multiple layout passes
for (int i = 0; i < 100; i++)
{
    items[i].Width = newWidths[i]; // Each triggers layout
}

// Good: Single layout pass
using (Dispatcher.DisableProcessing())
{
    for (int i = 0; i < 100; i++)
    {
        items[i].Width = newWidths[i];
    }
} // Layout happens once here
```

### Common Performance Issues

| Problem | Cause | Solution |
|---------|-------|----------|
| Slow scrolling | Deep Visual Tree | Virtualization |
| Layout thrashing | Frequent InvalidateMeasure | Batch updates |
| Slow startup | Complex Grid | Simplify layout |
| Memory growth | BitmapEffect | Use Effect class |

## 4. Tier-Adaptive Rendering
```csharp
public void ConfigureForTier()
{
    int tier = RenderCapability.Tier >> 16;

    if (tier < 2)
    {
        // Disable expensive effects
        DisableDropShadows();
        DisableAnimations();
        UseSimplifiedVisuals();
    }
}
```