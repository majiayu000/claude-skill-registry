---
name: implementing-2d-graphics
description: "Implements WPF 2D graphics using Shape, Geometry, Brush, and Pen classes. Use when building vector graphic UIs, icons, charts, or diagrams in WPF applications."
---

# WPF 2D Graphics Patterns

Implement vector-based visual elements using WPF's 2D graphics system.

## 1. Graphics Hierarchy

```
UIElement
└── Shape (FrameworkElement)        ← Participates in layout, supports events
    ├── Ellipse
    ├── Rectangle
    ├── Line
    ├── Polyline
    ├── Polygon
    └── Path

Drawing                             ← Lightweight, no events
├── GeometryDrawing
├── ImageDrawing
├── VideoDrawing
└── GlyphRunDrawing
```

---

## 2. Shape Basics

### 2.1 Basic Shapes

```xml
<!-- Ellipse -->
<Ellipse Width="100" Height="100"
         Fill="Blue"
         Stroke="Black"
         StrokeThickness="2"/>

<!-- Rectangle -->
<Rectangle Width="100" Height="50"
           Fill="Red"
           Stroke="Black"
           StrokeThickness="1"
           RadiusX="10" RadiusY="10"/>

<!-- Line -->
<Line X1="0" Y1="0" X2="100" Y2="100"
      Stroke="Green"
      StrokeThickness="3"/>

<!-- Polyline (connected lines) -->
<Polyline Points="0,0 50,50 100,0 150,50"
          Stroke="Purple"
          StrokeThickness="2"
          Fill="Transparent"/>

<!-- Polygon (closed shape) -->
<Polygon Points="50,0 100,100 0,100"
         Fill="Yellow"
         Stroke="Orange"
         StrokeThickness="2"/>
```

### 2.2 Path and Geometry

```xml
<!-- Path: complex shapes -->
<Path Fill="LightBlue" Stroke="DarkBlue" StrokeThickness="2">
    <Path.Data>
        <PathGeometry>
            <PathFigure StartPoint="10,10" IsClosed="True">
                <LineSegment Point="100,10"/>
                <ArcSegment Point="100,100" Size="50,50"
                            SweepDirection="Clockwise"/>
                <LineSegment Point="10,100"/>
            </PathFigure>
        </PathGeometry>
    </Path.Data>
</Path>

<!-- Mini-Language syntax -->
<Path Data="M 10,10 L 100,10 A 50,50 0 0 1 100,100 L 10,100 Z"
      Fill="LightGreen" Stroke="DarkGreen"/>
```

### 2.3 Path Mini-Language

| Command | Description | Example |
|---------|-------------|---------|
| **M** | MoveTo (start point) | M 10,10 |
| **L** | LineTo (straight line) | L 100,100 |
| **H** | Horizontal LineTo | H 100 |
| **V** | Vertical LineTo | V 100 |
| **A** | ArcTo (arc) | A 50,50 0 0 1 100,100 |
| **C** | Cubic Bezier | C 20,20 40,60 100,100 |
| **Q** | Quadratic Bezier | Q 50,50 100,100 |
| **Z** | ClosePath | Z |

Lowercase = relative coordinates, Uppercase = absolute coordinates

---

## 3. Geometry

### 3.1 Basic Geometry

```xml
<Path Stroke="Black" StrokeThickness="2">
    <Path.Data>
        <!-- Rectangle Geometry -->
        <RectangleGeometry Rect="10,10,80,60" RadiusX="5" RadiusY="5"/>
    </Path.Data>
</Path>

<Path Stroke="Black" Fill="Yellow">
    <Path.Data>
        <!-- Ellipse Geometry -->
        <EllipseGeometry Center="50,50" RadiusX="40" RadiusY="30"/>
    </Path.Data>
</Path>

<Path Stroke="Black">
    <Path.Data>
        <!-- Line Geometry -->
        <LineGeometry StartPoint="10,10" EndPoint="90,90"/>
    </Path.Data>
</Path>
```

### 3.2 CombinedGeometry (Shape Combination)

```xml
<Path Fill="LightBlue" Stroke="DarkBlue" StrokeThickness="2">
    <Path.Data>
        <CombinedGeometry GeometryCombineMode="Union">
            <CombinedGeometry.Geometry1>
                <EllipseGeometry Center="50,50" RadiusX="40" RadiusY="40"/>
            </CombinedGeometry.Geometry1>
            <CombinedGeometry.Geometry2>
                <EllipseGeometry Center="80,50" RadiusX="40" RadiusY="40"/>
            </CombinedGeometry.Geometry2>
        </CombinedGeometry>
    </Path.Data>
</Path>
```

**GeometryCombineMode:**
- **Union**: Union of shapes
- **Intersect**: Intersection
- **Exclude**: Difference (Geometry1 - Geometry2)
- **Xor**: Exclusive union

### 3.3 GeometryGroup (Multiple Geometry)

```xml
<Path Fill="Coral" Stroke="DarkRed" StrokeThickness="1">
    <Path.Data>
        <GeometryGroup FillRule="EvenOdd">
            <EllipseGeometry Center="50,50" RadiusX="45" RadiusY="45"/>
            <EllipseGeometry Center="50,50" RadiusX="30" RadiusY="30"/>
        </GeometryGroup>
    </Path.Data>
</Path>
```

**FillRule:**
- **EvenOdd**: Even-odd rule (donut shape)
- **Nonzero**: Non-zero rule (filled)

---

## 4. Brush (Quick Reference)

```xml
<!-- SolidColorBrush -->
<Rectangle Fill="Blue"/>
<Rectangle Fill="#FF2196F3"/>

<!-- LinearGradientBrush -->
<Rectangle.Fill>
    <LinearGradientBrush StartPoint="0,0" EndPoint="1,1">
        <GradientStop Color="#2196F3" Offset="0"/>
        <GradientStop Color="#FF9800" Offset="1"/>
    </LinearGradientBrush>
</Rectangle.Fill>
```

> **📌 상세 가이드**: `/creating-wpf-brushes` skill 참조

---

## 5. Stroke Styling

### 5.1 StrokeDashArray

```xml
<!-- Dashed line patterns -->
<Line X1="0" Y1="10" X2="200" Y2="10"
      Stroke="Black" StrokeThickness="2"
      StrokeDashArray="4,2"/>

<!-- Dot-dash pattern -->
<Line X1="0" Y1="30" X2="200" Y2="30"
      Stroke="Black" StrokeThickness="2"
      StrokeDashArray="4,2,1,2"/>
```

### 5.2 StrokeLineCap / StrokeLineJoin

```xml
<Polyline Points="10,50 50,10 90,50"
          Stroke="Blue"
          StrokeThickness="10"
          StrokeStartLineCap="Round"
          StrokeEndLineCap="Triangle"
          StrokeLineJoin="Round"/>
```

**LineCap:** Flat, Round, Square, Triangle
**LineJoin:** Miter, Bevel, Round

---

## 6. Related Skills

| Skill | Description |
|-------|-------------|
| `/creating-wpf-brushes` | All Brush patterns (Solid, Linear, Radial, Image, Visual) |
| `/creating-wpf-vector-icons` | XAML vector icons, IconButton styles |
| `/creating-graphics-in-code` | C# dynamic graphics (ShapeFactory, GeometryBuilder) |

---

## 7. Performance Considerations

| Element | Complexity | Recommended Use |
|---------|------------|-----------------|
| **Shape** | High | Interactive elements (click, drag) |
| **DrawingVisual** | Low | Large static graphics |
| **StreamGeometry** | Lowest | Fixed complex paths |

```csharp
// StreamGeometry: immutable, optimized
var streamGeometry = new StreamGeometry();
using (var context = streamGeometry.Open())
{
    context.BeginFigure(new Point(0, 0), isFilled: true, isClosed: true);
    context.LineTo(new Point(100, 0), isStroked: true, isSmoothJoin: false);
    context.LineTo(new Point(100, 100), isStroked: true, isSmoothJoin: false);
}
streamGeometry.Freeze(); // Set immutable for performance improvement
```

---

## 8. References

- [Shapes and Basic Drawing - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/graphics-multimedia/shapes-and-basic-drawing-in-wpf-overview)
- [Geometry Overview - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/graphics-multimedia/geometry-overview)
- [Painting with Brushes - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/graphics-multimedia/painting-with-solid-colors-and-gradients-overview)