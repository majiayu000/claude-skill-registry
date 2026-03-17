---
name: checking-image-bounds-transform
description: "Checks and clamps mouse coordinates within transformed image bounds in WPF. Use when implementing measurement tools or annotations that should only work inside Pan/Zoom/Rotate transformed images."
---

# WPF Image Bounds Checking (With Transforms)

A pattern for checking if mouse coordinates are within the image area and clamping coordinates to image bounds when Pan, Zoom, Rotate transforms are applied.

## 1. Problem Scenario

### Requirements
- Measurement tools, annotation tools in image viewers should only work **within the image area**
- Need accurate boundary detection even when image is zoomed, panned, or rotated

### Complexity
- `Image` control position varies based on `Stretch="None"`, `HorizontalAlignment="Center"` settings
- When `RenderTransform` applies Pan, Zoom, Rotate, calculating actual image position becomes complex

---

## 2. Solution Pattern

### 2.1 Image Bounds Check Method

```csharp
namespace MyApp.Controls;

using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;

public class ImageViewer : Control
{
    // DependencyProperties (omitted)
    public ImageSource? ImageSource { get; set; }
    public double ZoomFactor { get; set; } = 1.0;
    public double PanX { get; set; }
    public double PanY { get; set; }
    public double RotationAngle { get; set; }

    /// <summary>
    /// Check if the given point is within the image area.
    /// </summary>
    /// <param name="point">Point in parent container coordinates</param>
    /// <returns>True if within image area</returns>
    public bool IsPointWithinImage(Point point)
    {
        if (ImageSource is null)
            return false;

        // 1. Original image size
        var imageWidth = ImageSource.Width;
        var imageHeight = ImageSource.Height;

        // 2. Transformed image size (with zoom)
        var transformedWidth = imageWidth * ZoomFactor;
        var transformedHeight = imageHeight * ZoomFactor;

        // 3. Viewer center (if image is center-aligned)
        var viewerCenterX = ActualWidth / 2;
        var viewerCenterY = ActualHeight / 2;

        // 4. Image center (with pan)
        var imageCenterX = viewerCenterX + PanX;
        var imageCenterY = viewerCenterY + PanY;

        // 5. Image bounds (without rotation)
        var left = imageCenterX - transformedWidth / 2;
        var top = imageCenterY - transformedHeight / 2;
        var right = imageCenterX + transformedWidth / 2;
        var bottom = imageCenterY + transformedHeight / 2;

        // 6. If rotated, check by inverse-rotating the point
        if (RotationAngle != 0)
        {
            // Inverse-rotate point around image center
            var radians = -RotationAngle * Math.PI / 180;
            var cos = Math.Cos(radians);
            var sin = Math.Sin(radians);

            var dx = point.X - imageCenterX;
            var dy = point.Y - imageCenterY;

            var rotatedX = dx * cos - dy * sin + imageCenterX;
            var rotatedY = dx * sin + dy * cos + imageCenterY;

            return rotatedX >= left && rotatedX <= right &&
                   rotatedY >= top && rotatedY <= bottom;
        }

        return point.X >= left && point.X <= right &&
               point.Y >= top && point.Y <= bottom;
    }
}
```

---

### 2.2 Coordinate Clamping Method

```csharp
/// <summary>
/// Clamp the given point to be within the image bounds.
/// </summary>
/// <param name="point">Point in parent container coordinates</param>
/// <returns>Point clamped to image bounds</returns>
public Point ClampPointToImage(Point point)
{
    if (ImageSource is null)
        return point;

    // Original image size
    var imageWidth = ImageSource.Width;
    var imageHeight = ImageSource.Height;

    // Transformed image size (with zoom)
    var transformedWidth = imageWidth * ZoomFactor;
    var transformedHeight = imageHeight * ZoomFactor;

    // Viewer center
    var viewerCenterX = ActualWidth / 2;
    var viewerCenterY = ActualHeight / 2;

    // Image center (with pan)
    var imageCenterX = viewerCenterX + PanX;
    var imageCenterY = viewerCenterY + PanY;

    // Image bounds
    var left = imageCenterX - transformedWidth / 2;
    var top = imageCenterY - transformedHeight / 2;
    var right = imageCenterX + transformedWidth / 2;
    var bottom = imageCenterY + transformedHeight / 2;

    // Clamp point within bounds
    var clampedX = Math.Clamp(point.X, left, right);
    var clampedY = Math.Clamp(point.Y, top, bottom);

    return new Point(clampedX, clampedY);
}
```

---

## 3. Usage Example

### 3.1 Using in Measurement Tool

```csharp
// Code-behind
private Point _measureStartPoint;
private bool _isDrawingMeasurement;

private void RulerOverlay_MouseLeftButtonDown(object sender, MouseButtonEventArgs e)
{
    if (sender is RulerOverlay overlay)
    {
        var clickPoint = e.GetPosition(overlay);

        // Only start measurement within image area
        if (!ImageViewer.IsPointWithinImage(clickPoint))
            return;

        _measureStartPoint = clickPoint;
        _isDrawingMeasurement = true;

        overlay.IsDrawing = true;
        overlay.CurrentStartPoint = _measureStartPoint;
        overlay.CurrentEndPoint = _measureStartPoint;

        overlay.CaptureMouse();
    }
}

private void RulerOverlay_MouseMove(object sender, MouseEventArgs e)
{
    if (_isDrawingMeasurement && sender is RulerOverlay overlay)
    {
        var currentPoint = e.GetPosition(overlay);

        // Clamp end point to image area
        var clampedPoint = ImageViewer.ClampPointToImage(currentPoint);
        overlay.CurrentEndPoint = clampedPoint;
    }
}

private void RulerOverlay_MouseLeftButtonUp(object sender, MouseButtonEventArgs e)
{
    if (_isDrawingMeasurement && sender is RulerOverlay overlay)
    {
        var endPoint = e.GetPosition(overlay);

        // Clamp end point to image area
        endPoint = ImageViewer.ClampPointToImage(endPoint);

        // Complete measurement
        overlay.AddMeasurement(_measureStartPoint, endPoint);

        overlay.IsDrawing = false;
        _isDrawingMeasurement = false;
        overlay.ReleaseMouseCapture();
    }
}
```

---

## 4. Rotation Transform Principle

### 4.1 Inverse Rotation

When an image is rotated, click coordinates must be transformed to the image's original coordinate system:

```
Actual click position → Inverse rotate → Check bounds in pre-rotation coordinate system
```

```csharp
// Check click position on 45-degree rotated image

// Relative coordinates from image center
var dx = point.X - imageCenterX;
var dy = point.Y - imageCenterY;

// Inverse rotation (-45 degrees)
var radians = -RotationAngle * Math.PI / 180;  // -45 → -0.785 rad
var cos = Math.Cos(radians);  // approx 0.707
var sin = Math.Sin(radians);  // approx -0.707

// Apply rotation matrix
var rotatedX = dx * cos - dy * sin + imageCenterX;
var rotatedY = dx * sin + dy * cos + imageCenterY;
```

### 4.2 Visual Explanation

```
        Rotated Image          After Inverse Rotation

          ◇                      □
         /  \                    |  |
        /    \                   |  |
        \    /       →           |  |
         \  /                    |  |
          ◇                      □

    Transform click coord    Check against rectangle
```

---

## 5. Combining with Other Transforms

### 5.1 Flip (Horizontal/Vertical)

Flip doesn't affect coordinate checking (bounds remain the same):

```csharp
// Flip only mirrors content, bounds remain the same
public bool FlipHorizontal { get; set; }
public bool FlipVertical { get; set; }

// Flip is ignored in bounds calculation
```

### 5.2 Scale (Zoom In/Out)

Already reflected via ZoomFactor:

```csharp
var transformedWidth = imageWidth * ZoomFactor;
var transformedHeight = imageHeight * ZoomFactor;
```

### 5.3 Pan (Translation)

Reflected in image center coordinates:

```csharp
var imageCenterX = viewerCenterX + PanX;
var imageCenterY = viewerCenterY + PanY;
```

---

## 6. Consistency with RenderTransform

### 6.1 Transform Order in XAML

```xml
<Image x:Name="PART_Image"
       RenderTransformOrigin="0.5,0.5">
    <Image.RenderTransform>
        <TransformGroup>
            <!-- 1. Flip -->
            <ScaleTransform ScaleX="{Binding FlipHorizontal, ...}"
                            ScaleY="{Binding FlipVertical, ...}" />
            <!-- 2. Rotate -->
            <RotateTransform Angle="{Binding RotationAngle, ...}" />
            <!-- 3. Zoom -->
            <ScaleTransform ScaleX="{Binding ZoomFactor, ...}"
                            ScaleY="{Binding ZoomFactor, ...}" />
            <!-- 4. Pan -->
            <TranslateTransform X="{Binding PanX, ...}"
                                Y="{Binding PanY, ...}" />
        </TransformGroup>
    </Image.RenderTransform>
</Image>
```

### 6.2 Order in Bounds Calculation

Apply transforms in the same order in code:

```csharp
// 1. Apply Zoom to original size
var transformedWidth = imageWidth * ZoomFactor;
var transformedHeight = imageHeight * ZoomFactor;

// 2. Apply Pan to center
var imageCenterX = viewerCenterX + PanX;
var imageCenterY = viewerCenterY + PanY;

// 3. Calculate bounds
var left = imageCenterX - transformedWidth / 2;
// ...

// 4. Apply Rotate (check coordinates via inverse transform)
if (RotationAngle != 0)
{
    // Inverse rotation...
}
```

---

## 7. Checklist

- [ ] `IsPointWithinImage()`: Check image area before starting click
- [ ] `ClampPointToImage()`: Clamp coordinates during/after drag
- [ ] Rotation handling: Transform coordinates via inverse rotation before bounds check
- [ ] Transform order consistency: Maintain same order in XAML and code
- [ ] Verify `RenderTransformOrigin="0.5,0.5"` setting

---

## 8. References

- [RenderTransform - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/api/system.windows.uielement.rendertransform)
- [RotateTransform - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/api/system.windows.media.rotatetransform)
- [Math.Clamp - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/api/system.math.clamp)
