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

## 4. Brush

### 4.1 SolidColorBrush

```xml
<Rectangle Fill="Blue"/>
<Rectangle Fill="#FF2196F3"/>
<Rectangle>
    <Rectangle.Fill>
        <SolidColorBrush Color="Blue" Opacity="0.5"/>
    </Rectangle.Fill>
</Rectangle>
```

### 4.2 LinearGradientBrush

```xml
<Rectangle Width="200" Height="100">
    <Rectangle.Fill>
        <LinearGradientBrush StartPoint="0,0" EndPoint="1,1">
            <GradientStop Color="#2196F3" Offset="0"/>
            <GradientStop Color="#4CAF50" Offset="0.5"/>
            <GradientStop Color="#FF9800" Offset="1"/>
        </LinearGradientBrush>
    </Rectangle.Fill>
</Rectangle>
```

### 4.3 RadialGradientBrush

```xml
<Ellipse Width="200" Height="200">
    <Ellipse.Fill>
        <RadialGradientBrush GradientOrigin="0.3,0.3">
            <GradientStop Color="White" Offset="0"/>
            <GradientStop Color="Blue" Offset="1"/>
        </RadialGradientBrush>
    </Ellipse.Fill>
</Ellipse>
```

### 4.4 ImageBrush

```xml
<Rectangle Width="200" Height="200">
    <Rectangle.Fill>
        <ImageBrush ImageSource="/Assets/pattern.png"
                    TileMode="Tile"
                    Viewport="0,0,0.25,0.25"
                    ViewportUnits="RelativeToBoundingBox"/>
    </Rectangle.Fill>
</Rectangle>
```

### 4.5 VisualBrush

```xml
<Rectangle Width="200" Height="200">
    <Rectangle.Fill>
        <VisualBrush TileMode="Tile" Viewport="0,0,0.5,0.5">
            <VisualBrush.Visual>
                <StackPanel>
                    <Ellipse Width="20" Height="20" Fill="Red"/>
                    <Ellipse Width="20" Height="20" Fill="Blue"/>
                </StackPanel>
            </VisualBrush.Visual>
        </VisualBrush>
    </Rectangle.Fill>
</Rectangle>
```

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

## 6. Creating Graphics in Code

### 6.1 Dynamic Shape Creation

```csharp
namespace MyApp.Graphics;

using System.Windows;
using System.Windows.Media;
using System.Windows.Shapes;

public static class ShapeFactory
{
    /// <summary>
    /// Create circular marker
    /// </summary>
    public static Ellipse CreateCircleMarker(double size, Brush fill)
    {
        return new Ellipse
        {
            Width = size,
            Height = size,
            Fill = fill,
            Stroke = Brushes.Black,
            StrokeThickness = 1
        };
    }

    /// <summary>
    /// Create arrow Path
    /// </summary>
    public static Path CreateArrow(Point start, Point end, Brush stroke)
    {
        var geometry = new PathGeometry();

        // Arrow body
        var bodyFigure = new PathFigure { StartPoint = start };
        bodyFigure.Segments.Add(new LineSegment(end, isStroked: true));
        geometry.Figures.Add(bodyFigure);

        // Calculate arrow head
        var direction = end - start;
        direction.Normalize();
        var perpendicular = new Vector(-direction.Y, direction.X);

        const double headLength = 10;
        const double headWidth = 5;

        var headBase = end - direction * headLength;
        var headLeft = headBase + perpendicular * headWidth;
        var headRight = headBase - perpendicular * headWidth;

        var headFigure = new PathFigure { StartPoint = end };
        headFigure.Segments.Add(new LineSegment(headLeft, isStroked: true));
        headFigure.Segments.Add(new LineSegment(headRight, isStroked: true));
        headFigure.IsClosed = true;
        geometry.Figures.Add(headFigure);

        return new Path
        {
            Data = geometry,
            Stroke = stroke,
            StrokeThickness = 2,
            Fill = stroke
        };
    }
}
```

### 6.2 Dynamic PathGeometry Creation

```csharp
namespace MyApp.Graphics;

using System.Collections.Generic;
using System.Windows;
using System.Windows.Media;

public static class GeometryBuilder
{
    /// <summary>
    /// Create polygon Geometry from point list
    /// </summary>
    public static PathGeometry CreatePolygon(IReadOnlyList<Point> points)
    {
        if (points.Count < 3)
        {
            return new PathGeometry();
        }

        var figure = new PathFigure
        {
            StartPoint = points[0],
            IsClosed = true,
            IsFilled = true
        };

        for (var i = 1; i < points.Count; i++)
        {
            figure.Segments.Add(new LineSegment(points[i], isStroked: true));
        }

        var geometry = new PathGeometry();
        geometry.Figures.Add(figure);

        return geometry;
    }

    /// <summary>
    /// Create Bezier curve Geometry
    /// </summary>
    public static PathGeometry CreateBezierCurve(
        Point start,
        Point control1,
        Point control2,
        Point end)
    {
        var figure = new PathFigure { StartPoint = start };
        figure.Segments.Add(new BezierSegment(control1, control2, end, isStroked: true));

        var geometry = new PathGeometry();
        geometry.Figures.Add(figure);

        return geometry;
    }
}
```

---

## 7. Icon Implementation

### 7.1 XAML Vector Icons

```xml
<ResourceDictionary xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
                    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">

    <!-- Check mark icon -->
    <PathGeometry x:Key="CheckIconGeometry">
        M 2,7 L 5,10 L 10,3
    </PathGeometry>

    <!-- Close icon -->
    <PathGeometry x:Key="CloseIconGeometry">
        M 2,2 L 10,10 M 10,2 L 2,10
    </PathGeometry>

    <!-- Menu icon (hamburger) -->
    <GeometryGroup x:Key="MenuIconGeometry">
        <RectangleGeometry Rect="0,0,16,2"/>
        <RectangleGeometry Rect="0,6,16,2"/>
        <RectangleGeometry Rect="0,12,16,2"/>
    </GeometryGroup>

</ResourceDictionary>
```

### 7.2 Icon Button Style

```xml
<Style x:Key="IconButtonStyle" TargetType="{x:Type Button}">
    <Setter Property="Width" Value="32"/>
    <Setter Property="Height" Value="32"/>
    <Setter Property="Background" Value="Transparent"/>
    <Setter Property="Template">
        <Setter.Value>
            <ControlTemplate TargetType="{x:Type Button}">
                <Border Background="{TemplateBinding Background}">
                    <Path x:Name="IconPath"
                          Data="{TemplateBinding Content}"
                          Fill="{TemplateBinding Foreground}"
                          Stretch="Uniform"
                          HorizontalAlignment="Center"
                          VerticalAlignment="Center"
                          Width="16" Height="16"/>
                </Border>
                <ControlTemplate.Triggers>
                    <Trigger Property="IsMouseOver" Value="True">
                        <Setter TargetName="IconPath" Property="Fill" Value="#2196F3"/>
                    </Trigger>
                </ControlTemplate.Triggers>
            </ControlTemplate>
        </Setter.Value>
    </Setter>
</Style>

<!-- Usage -->
<Button Style="{StaticResource IconButtonStyle}"
        Content="{StaticResource CloseIconGeometry}"/>
```

---

## 8. Performance Considerations

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

## 9. References

- [Shapes and Basic Drawing - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/graphics-multimedia/shapes-and-basic-drawing-in-wpf-overview)
- [Geometry Overview - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/graphics-multimedia/geometry-overview)
- [Painting with Brushes - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/graphics-multimedia/painting-with-solid-colors-and-gradients-overview)