---
name: imagesharp
description: >
  Guidance for SixLabors ImageSharp cross-platform image processing library.
  USE FOR: image resizing, cropping, format conversion, watermarking, thumbnail generation, applying filters and effects, drawing text and shapes on images, metadata reading.
  DO NOT USE FOR: video processing, real-time computer vision (use OpenCV), GPU-accelerated rendering, PDF generation (use PdfSharpCore), 3D graphics.
license: MIT
metadata:
  displayName: ImageSharp
  author: "Tyler-R-Kendrick"
  version: "1.0.0"
compatibility:
  - claude
  - copilot
  - cursor
references:
  - title: "ImageSharp Documentation"
    url: "https://docs.sixlabors.com/articles/imagesharp/"
  - title: "ImageSharp GitHub Repository"
    url: "https://github.com/SixLabors/ImageSharp"
  - title: "SixLabors.ImageSharp NuGet Package"
    url: "https://www.nuget.org/packages/SixLabors.ImageSharp"
---

# ImageSharp

## Overview

ImageSharp is a fully managed, cross-platform 2D graphics library for .NET. Unlike `System.Drawing` (which depends on GDI+ on Windows and libgdiplus on Linux), ImageSharp has zero native dependencies and works identically across Windows, Linux, macOS, and containerized environments.

ImageSharp supports loading, manipulating, and saving images in JPEG, PNG, GIF, BMP, TIFF, TGA, and WebP formats. It provides a fluent `Mutate` API for chaining operations like resize, crop, rotate, blur, and color adjustment. The library also includes drawing capabilities for text, shapes, and compositing.

Install via NuGet:
```
dotnet add package SixLabors.ImageSharp
dotnet add package SixLabors.ImageSharp.Drawing
```

## Loading and Saving Images

Load images from files, streams, or byte arrays and save in any supported format.

```csharp
using SixLabors.ImageSharp;
using SixLabors.ImageSharp.Formats.Jpeg;
using SixLabors.ImageSharp.Formats.Png;
using SixLabors.ImageSharp.Formats.Webp;

// Load from file
using var image = await Image.LoadAsync("photo.jpg");

// Load from stream
using var stream = File.OpenRead("photo.png");
using var imageFromStream = await Image.LoadAsync(stream);

// Load from byte array
byte[] imageBytes = await File.ReadAllBytesAsync("photo.jpg");
using var imageFromBytes = Image.Load(imageBytes);

// Save in different formats
await image.SaveAsync("output.png", new PngEncoder());
await image.SaveAsync("output.webp", new WebpEncoder { Quality = 80 });
await image.SaveAsync("output.jpg", new JpegEncoder { Quality = 85 });

// Save to a stream
using var outputStream = new MemoryStream();
await image.SaveAsJpegAsync(outputStream);
byte[] resultBytes = outputStream.ToArray();
```

## Resizing and Cropping

Resize images with different modes (stretch, crop, pad) and crop to specific regions.

```csharp
using SixLabors.ImageSharp;
using SixLabors.ImageSharp.Processing;

using var image = await Image.LoadAsync("photo.jpg");

// Resize to exact dimensions
image.Mutate(x => x.Resize(800, 600));

// Resize maintaining aspect ratio (width-based)
image.Mutate(x => x.Resize(new ResizeOptions
{
    Size = new Size(400, 0), // height auto-calculated
    Mode = ResizeMode.Max
}));

// Resize and pad to fit exact dimensions with letterboxing
image.Mutate(x => x.Resize(new ResizeOptions
{
    Size = new Size(500, 500),
    Mode = ResizeMode.Pad,
    PadColor = Color.White
}));

// Crop to a region
image.Mutate(x => x.Crop(new Rectangle(100, 50, 300, 200)));

// Auto-crop and resize for thumbnails
image.Mutate(x => x.Resize(new ResizeOptions
{
    Size = new Size(150, 150),
    Mode = ResizeMode.Crop,
    Position = AnchorPositionMode.Center
}));

await image.SaveAsync("thumbnail.jpg");
```

## Applying Filters and Effects

Chain multiple processing operations in a single `Mutate` call.

```csharp
using SixLabors.ImageSharp;
using SixLabors.ImageSharp.Processing;

using var image = await Image.LoadAsync("photo.jpg");

// Single effect
image.Mutate(x => x.GaussianBlur(5));

// Chain multiple effects
image.Mutate(x => x
    .Resize(800, 600)
    .Grayscale()
    .Contrast(1.2f)
    .Brightness(1.1f)
    .GaussianSharpen(2));

// Rotate and flip
image.Mutate(x => x
    .Rotate(90)
    .Flip(FlipMode.Horizontal));

// Sepia tone
image.Mutate(x => x
    .Resize(800, 600)
    .Sepia()
    .Vignette());

// Pixelate for privacy
image.Mutate(x => x.Pixelate(10));

await image.SaveAsync("processed.jpg");
```

## Watermarking and Compositing

Overlay images and draw text for watermarks, logos, and annotations.

```csharp
using SixLabors.ImageSharp;
using SixLabors.ImageSharp.Drawing.Processing;
using SixLabors.ImageSharp.PixelFormats;
using SixLabors.ImageSharp.Processing;
using SixLabors.Fonts;

using var image = await Image.LoadAsync("photo.jpg");
using var logo = await Image.LoadAsync("logo.png");

// Resize logo and overlay with opacity
logo.Mutate(x => x.Resize(100, 100));
image.Mutate(x => x.DrawImage(logo, new Point(10, 10), opacity: 0.5f));

// Add text watermark
var fontCollection = new FontCollection();
var fontFamily = fontCollection.Add("fonts/Roboto-Regular.ttf");
var font = fontFamily.CreateFont(24, FontStyle.Bold);

image.Mutate(x => x.DrawText(
    "Copyright 2025",
    font,
    Color.FromRgba(255, 255, 255, 128), // semi-transparent white
    new PointF(image.Width - 200, image.Height - 40)));

await image.SaveAsync("watermarked.jpg");
```

## Creating Images from Scratch

Generate images programmatically with solid backgrounds, gradients, and shapes.

```csharp
using SixLabors.ImageSharp;
using SixLabors.ImageSharp.Drawing.Processing;
using SixLabors.ImageSharp.PixelFormats;
using SixLabors.ImageSharp.Processing;

// Create a blank image with a background color
using var image = new Image<Rgba32>(800, 400, Color.DarkSlateBlue);

// Draw shapes
image.Mutate(x =>
{
    // Draw a filled rectangle
    x.Fill(Color.White, new RectangleF(50, 50, 300, 200));

    // Draw a circle outline
    var pen = Pens.Solid(Color.Yellow, 3);
    x.Draw(pen, new EllipsePolygon(600, 200, 100));

    // Draw a line
    x.DrawLine(Color.Red, 2, new PointF(0, 200), new PointF(800, 200));
});

await image.SaveAsync("generated.png");
```

## Configuring Memory Limits

For production workloads, configure memory allocation limits to prevent unbounded memory use from large images.

```csharp
using SixLabors.ImageSharp;
using SixLabors.ImageSharp.Memory;

// Configure global memory limits
Configuration.Default.MemoryAllocator = MemoryAllocator.Create(new MemoryAllocatorOptions
{
    MaximumPoolSizeMegabytes = 128
});

// Set maximum image dimensions
Configuration.Default.ImageOperationsProvider
    .MaxDegreeOfParallelism = Environment.ProcessorCount;

// Per-operation configuration
var config = new Configuration();
config.MemoryAllocator = MemoryAllocator.Create(new MemoryAllocatorOptions
{
    MaximumPoolSizeMegabytes = 64
});

using var image = await Image.LoadAsync(config, "large-photo.jpg");
```

## Format Comparison

| Format | Read | Write | Transparency | Animation | Lossy | Best For |
|--------|------|-------|-------------|-----------|-------|----------|
| JPEG | Yes | Yes | No | No | Yes | Photos |
| PNG | Yes | Yes | Yes | No | No | Screenshots, logos |
| WebP | Yes | Yes | Yes | Yes | Both | Web delivery |
| GIF | Yes | Yes | Yes (1-bit) | Yes | No | Simple animations |
| BMP | Yes | Yes | No | No | No | Uncompressed data |
| TIFF | Yes | Yes | Yes | No | Both | Print, archival |

## Best Practices

1. **Always wrap `Image` instances in `using` statements** because they allocate large pixel buffers that must be returned to the memory pool on dispose.
2. **Use `Image.LoadAsync` and `SaveAsync`** for I/O-bound operations to avoid blocking threads in web applications and worker services.
3. **Chain operations in a single `Mutate` call** rather than calling `Mutate` multiple times, because each call may trigger intermediate buffer allocations.
4. **Resize before applying effects** to reduce the pixel count that blur, sharpen, and color adjustment operations must process.
5. **Configure `MemoryAllocator` limits in production** to prevent out-of-memory conditions when processing user-uploaded images of unknown size.
6. **Validate image dimensions before processing** by checking `image.Width` and `image.Height` against application-specific maximums to reject absurdly large uploads.
7. **Use `ResizeMode.Max` for responsive thumbnails** to maintain aspect ratio while fitting within a bounding box, and `ResizeMode.Crop` for fixed-size avatars.
8. **Prefer WebP output for web delivery** because it provides smaller file sizes than JPEG and PNG at equivalent quality, with transparency support.
9. **Avoid loading images from untrusted sources without size limits** -- malicious files can declare enormous dimensions in headers while being small on disk.
10. **Use `SixLabors.ImageSharp.Drawing` for text and shape rendering** rather than pixel-level manipulation, which is error-prone and not optimized.
