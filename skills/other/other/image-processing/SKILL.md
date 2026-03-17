---
name: image-processing
description: Image decoding, encoding, and manipulation using the `image` crate
---

# image-processing

The `image` crate provides native Rust implementations for image encoding/decoding. In script-kit-gpui, it's used for PNG encoding/decoding for app icons and clipboard images.

**Crate version**: `0.25` with features `["png"]` only (no default features for minimal binary size)

## Key Types

### DynamicImage
Enum over supported buffer formats with automatic format conversion:
```rust
let img = image::load_from_memory(png_data)?;        // -> DynamicImage
let rgba = img.to_rgba8();                           // -> RgbaImage (ImageBuffer<Rgba<u8>>)
let (width, height) = img.dimensions();              // GenericImageView trait
```

### RgbaImage (ImageBuffer<Rgba<u8>, Vec<u8>>)
Fixed-format buffer for RGBA pixels:
```rust
// Create from raw bytes (must be exactly width * height * 4 bytes)
let buffer = image::RgbaImage::from_raw(width, height, rgba_bytes)
    .expect("Invalid dimensions or byte count");

// Create new empty
let mut img = image::RgbaImage::new(width, height);
```

### Frame
Animation frame wrapper used by GPUI's RenderImage:
```rust
let frame = image::Frame::new(rgba_image);
let render_image = RenderImage::new(smallvec![frame]);
```

### Pixel Types
```rust
image::Rgba([255, 0, 0, 255])  // Red pixel
image::Rgb([255, 255, 255])    // White pixel (no alpha)
image::Luma([128])             // Grayscale
```

## Usage in script-kit-gpui

### PNG Decoding for App Icons (`list_item.rs`)
```rust
pub fn decode_png_to_render_image(png_data: &[u8]) -> Result<Arc<RenderImage>, image::ImageError> {
    use image::GenericImageView;
    
    let img = image::load_from_memory(png_data)?;
    let mut rgba = img.to_rgba8();
    let (width, height) = img.dimensions();
    
    // IMPORTANT: GPUI/Metal expects BGRA format
    // Must swap R and B channels when creating RenderImage directly
    for pixel in rgba.chunks_exact_mut(4) {
        pixel.swap(0, 2); // RGBA -> BGRA
    }
    
    let buffer = image::RgbaImage::from_raw(width, height, rgba.into_raw())
        .expect("Failed to create image buffer");
    let frame = image::Frame::new(buffer);
    
    Ok(Arc::new(RenderImage::new(SmallVec::from_elem(frame, 1))))
}
```

### PNG Encoding for Screenshots (`platform.rs`)
```rust
use image::codecs::png::PngEncoder;
use image::ImageEncoder;

let mut png_data = Vec::new();
let encoder = PngEncoder::new(&mut png_data);
encoder.write_image(
    &final_image,           // &[u8] or ImageBuffer
    width, 
    height, 
    image::ExtendedColorType::Rgba8
)?;
```

### Clipboard Image Handling (`clipboard_history/image.rs`)
```rust
// Encode clipboard to PNG
let rgba_image = image::RgbaImage::from_raw(
    image.width as u32,
    image.height as u32,
    image.bytes.to_vec(),
).context("Failed to create RGBA image")?;

let mut png_data = Vec::new();
rgba_image.write_to(&mut Cursor::new(&mut png_data), image::ImageFormat::Png)?;

// Decode PNG to clipboard format
let img = image::load_from_memory_with_format(&png_bytes, image::ImageFormat::Png)?;
let rgba = img.to_rgba8();
```

### Image Resizing for Screenshots
```rust
let resized = image::imageops::resize(
    &image,
    new_width,
    new_height,
    image::imageops::FilterType::Lanczos3,  // High-quality downscaling
);
```

## Loading Images

### From File
```rust
let img = image::open("path/to/image.png")?;  // Auto-detects format
```

### From Bytes (Most Common in script-kit-gpui)
```rust
// Auto-detect format
let img = image::load_from_memory(bytes)?;

// Explicit format (faster, no guessing)
let img = image::load_from_memory_with_format(bytes, image::ImageFormat::Png)?;
```

### Dimensions Only (No Full Decode)
```rust
let cursor = std::io::Cursor::new(&png_bytes);
let reader = image::ImageReader::with_format(cursor, image::ImageFormat::Png);
let (width, height) = reader.into_dimensions()?;  // Fast header-only parse
```

## Pixel Access

### Reading Pixels
```rust
use image::GenericImageView;

let pixel = img.get_pixel(x, y);  // Returns Rgba<u8> or similar
let (r, g, b, a) = (pixel[0], pixel[1], pixel[2], pixel[3]);
```

### Writing Pixels
```rust
use image::GenericImage;

img.put_pixel(x, y, image::Rgba([255, 0, 0, 255]));
```

### Iterating All Pixels
```rust
// Immutable iteration
for (x, y, pixel) in img.pixels() {
    // pixel is Rgba<u8>
}

// Direct buffer access (fastest)
for pixel in rgba.chunks_exact_mut(4) {
    pixel.swap(0, 2);  // Swap R and B
}
```

## Format Support

Features enabled in script-kit-gpui: **`png` only**

```toml
image = { version = "0.25", default-features = false, features = ["png"] }
```

Available formats (require feature flags):
- `png` - PNG decoding/encoding
- `jpeg` - JPEG decoding/encoding  
- `gif` - GIF decoding/encoding
- `webp` - WebP decoding/encoding
- `bmp`, `ico`, `tiff`, etc.

Default features include many formats - disable for smaller binaries.

## Memory Considerations

### Large Image Safety
```rust
// RgbaImage::from_raw returns None if dimensions don't match byte count
let buffer = image::RgbaImage::from_raw(width, height, bytes)
    .context("Dimension mismatch")?;

// Validate dimensions before allocation
let expected_bytes = (width as usize) * (height as usize) * 4;
if bytes.len() != expected_bytes {
    return Err(anyhow!("Invalid byte count"));
}
```

### Avoiding Copies with SmallVec
```rust
// BAD: SmallVec::from_elem clones the frame buffer
let render_image = RenderImage::new(SmallVec::from_elem(frame, 1));

// GOOD: Use smallvec! macro - no clone
use smallvec::smallvec;
let render_image = RenderImage::new(smallvec![frame]);
```

### Decode Once, Cache Forever
```rust
// WRONG: Decoding during render (called 60fps!)
fn render(&mut self, cx: &mut ViewContext<Self>) {
    let img = decode_png_to_render_image(&self.png_data);  // Slow!
}

// RIGHT: Decode once, store Arc<RenderImage>
fn new(png_data: &[u8]) -> Self {
    Self {
        cached_image: decode_png_to_render_image(png_data).ok(),
    }
}
```

## Anti-patterns

### Forgetting BGRA Conversion for Metal/GPUI
```rust
// WRONG: Assumes RGBA works
let frame = image::Frame::new(rgba_image);
let render_image = RenderImage::new(smallvec![frame]);  // Colors wrong!

// RIGHT: Convert RGBA -> BGRA for Metal
for pixel in rgba.chunks_exact_mut(4) {
    pixel.swap(0, 2);
}
```

### Not Validating Byte Length
```rust
// WRONG: Panics on invalid input
let img = image::RgbaImage::from_raw(w, h, bytes).unwrap();

// RIGHT: Handle gracefully
let img = image::RgbaImage::from_raw(w, h, bytes)
    .context("Invalid dimensions or corrupt data")?;
```

### Loading Same Image Multiple Times
```rust
// WRONG: Decodes same icon for every list item
for item in items {
    let icon = decode_png(&item.icon_path);  // N decodes!
}

// RIGHT: Cache decoded images by path/hash
let icon_cache: HashMap<String, Arc<RenderImage>> = HashMap::new();
```

### Using Default Features
```rust
# WRONG: Pulls in all decoders, huge binary
image = "0.25"

# RIGHT: Only what you need
image = { version = "0.25", default-features = false, features = ["png"] }
```

## Error Handling

All decode operations return `Result<_, image::ImageError>`:
```rust
use image::ImageError;

match image::load_from_memory(bytes) {
    Ok(img) => // success
    Err(ImageError::Decoding(_)) => // corrupt/invalid format
    Err(ImageError::IoError(_)) => // read failure
    Err(ImageError::Limits(_)) => // image too large
    Err(e) => // other error
}
```

## Quick Reference

| Operation | Code |
|-----------|------|
| Load PNG from bytes | `image::load_from_memory_with_format(bytes, ImageFormat::Png)?` |
| Convert to RGBA | `img.to_rgba8()` |
| Get dimensions | `img.dimensions()` or `(img.width(), img.height())` |
| Create from raw | `RgbaImage::from_raw(w, h, bytes)?` |
| Encode to PNG | `img.write_to(&mut cursor, ImageFormat::Png)?` |
| Resize | `imageops::resize(&img, w, h, FilterType::Lanczos3)` |
| Create Frame | `Frame::new(rgba_image)` |
| Dimensions only | `ImageReader::with_format(cursor, fmt).into_dimensions()?` |
