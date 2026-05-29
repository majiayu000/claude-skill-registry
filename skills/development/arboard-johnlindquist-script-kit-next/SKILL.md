---
name: arboard
description: Cross-platform clipboard access for text and images
tags: [clipboard, cross-platform, images, text]
---

# arboard

Cross-platform clipboard library by 1Password for reading and writing text and images. Provides a unified API across macOS, Windows, and Linux (X11/Wayland).

**Crate**: https://crates.io/crates/arboard
**Docs**: https://docs.rs/arboard/latest/arboard/

## Key Types

### Clipboard

The main entry point. Create one instance to interact with the system clipboard.

```rust
use arboard::Clipboard;

let mut clipboard = Clipboard::new()?;
```

**Important**: `Clipboard::new()` returns `Result<Clipboard, Error>` - it can fail if:
- Clipboard is not supported on the platform/environment
- Another process is holding the clipboard (rare)

### ImageData

Stores raw RGBA pixel data for clipboard images.

```rust
use arboard::ImageData;
use std::borrow::Cow;

let image = ImageData {
    width: 100,
    height: 100,
    bytes: Cow::Owned(vec![0u8; 100 * 100 * 4]), // RGBA: 4 bytes per pixel
};
```

**Pixel Format**:
- Row-major order (left-to-right, top-to-bottom)
- 4 channels per pixel: Red, Green, Blue, Alpha
- Each channel is 1 byte (0-255)
- Total bytes = `width * height * 4`

### Error

Non-exhaustive enum with these variants:
- `ContentNotAvailable` - Clipboard empty or wrong format
- `ClipboardNotSupported` - Platform/environment doesn't support clipboard
- `ClipboardOccupied` - Another process is using the clipboard
- `ConversionFailure` - Image/text couldn't be converted
- `Unknown { description }` - Catch-all for other errors

## Usage in script-kit-gpui

The codebase uses arboard for:

1. **Clipboard History Monitoring** (`src/clipboard_history/monitor.rs`)
   - Polls clipboard every 50-500ms
   - Captures both text and images
   - Uses content hashing for deduplication

2. **Copy to Clipboard** (`src/clipboard_history/clipboard.rs`)
   - Restores entries from history
   - Handles both text and image content types

3. **Selected Text Operations** (`src/selected_text.rs`)
   - Save/restore clipboard during text replacement
   - Clipboard-based paste simulation

4. **Text Injection** (`src/text_injector.rs`)
   - Snippet expansion via clipboard + Cmd+V
   - Preserves original clipboard contents

### Pattern: Save and Restore

script-kit-gpui consistently uses this pattern when temporarily using the clipboard:

```rust
use arboard::Clipboard;
use anyhow::{Context, Result};

fn paste_via_clipboard(text: &str) -> Result<()> {
    let mut clipboard = Clipboard::new().context("Failed to access clipboard")?;
    
    // 1. Save original contents
    let original = clipboard.get_text().ok();
    
    // 2. Set new content
    clipboard.set_text(text).context("Failed to set clipboard")?;
    
    // 3. Perform operation (e.g., simulate Cmd+V)
    simulate_paste()?;
    
    // 4. Restore original (best effort)
    if let Some(original_text) = original {
        let _ = clipboard.set_text(&original_text);
    }
    
    Ok(())
}
```

## Text Operations

### Get Text

```rust
let mut clipboard = Clipboard::new()?;
match clipboard.get_text() {
    Ok(text) => println!("Got: {}", text),
    Err(arboard::Error::ContentNotAvailable) => println!("Empty or not text"),
    Err(e) => eprintln!("Error: {}", e),
}
```

### Set Text

```rust
let mut clipboard = Clipboard::new()?;
clipboard.set_text("Hello, world!")?;

// Also accepts String, &String, Cow<str>
clipboard.set_text(String::from("owned"))?;
```

### Set HTML

```rust
// HTML with plain text fallback
clipboard.set_html(
    "<b>Bold</b> text",
    Some("Bold text"), // Alt text for apps that don't support HTML
)?;
```

## Image Operations

### Get Image

```rust
let mut clipboard = Clipboard::new()?;
match clipboard.get_image() {
    Ok(image) => {
        println!("{}x{} image, {} bytes", 
            image.width, image.height, image.bytes.len());
    }
    Err(arboard::Error::ContentNotAvailable) => {
        println!("No image on clipboard");
    }
    Err(e) => eprintln!("Error: {}", e),
}
```

### Set Image

```rust
use arboard::{Clipboard, ImageData};
use std::borrow::Cow;

let mut clipboard = Clipboard::new()?;

// Create a 2x2 red/green/blue/white test image
let pixels = vec![
    255, 0, 0, 255,    // Red pixel
    0, 255, 0, 255,    // Green pixel
    0, 0, 255, 255,    // Blue pixel
    255, 255, 255, 255, // White pixel
];

let image = ImageData {
    width: 2,
    height: 2,
    bytes: Cow::Owned(pixels),
};

clipboard.set_image(image)?;
```

### Convert to Owned

Use `to_owned_img()` when you need to store the image beyond the clipboard's lifetime:

```rust
let image = clipboard.get_image()?;
let owned: ImageData<'static> = image.to_owned_img();
// Now safe to use after clipboard is dropped
```

## Platform Specifics

### macOS

- Uses `NSPasteboard` via `objc2`
- Images stored as `NSImage` objects
- Most reliable platform for clipboard operations
- Efficient change detection via `changeCount`

### Windows

- Uses `clipboard-win` crate
- **Important**: Clipboard is a global object, only one thread can open it at a time
- Parallel operations may fail with `ClipboardOccupied`
- Image formats: `CF_DIB`, `CF_BITMAP`
- Recommended: Avoid creating Clipboard objects on multiple threads

### Linux (X11/Wayland)

- **Critical**: Clipboard content is "hosted" by the application
- When last `Clipboard` instance is dropped, content may become unavailable to other apps!
- Use `SetExtLinux` trait for persistence options:

```rust
use arboard::{Clipboard, SetExtLinux};

let mut clipboard = Clipboard::new()?;
clipboard.set()
    .wait()  // Keep clipboard available after app exits (forks background process)
    .text("Persistent text")?;
```

- Primary vs Clipboard selections (X11):
  - `LinuxClipboardKind::Clipboard` - Ctrl+C/Ctrl+V (default)
  - `LinuxClipboardKind::Primary` - Middle-click paste

## Builder API

For advanced operations, use the builder pattern:

```rust
let mut clipboard = Clipboard::new()?;

// Get with options
let text = clipboard.get()
    .text()?;

// Set with options  
clipboard.set()
    .text("content")?;

// Clear
clipboard.clear()?;
```

## Integration with `image` Crate

script-kit-gpui converts between `arboard::ImageData` and the `image` crate:

```rust
use arboard::ImageData;
use image::RgbaImage;
use std::borrow::Cow;

// ImageData -> RgbaImage
fn to_rgba_image(img: &ImageData) -> Option<RgbaImage> {
    RgbaImage::from_raw(
        img.width as u32,
        img.height as u32,
        img.bytes.to_vec(),
    )
}

// RgbaImage -> ImageData
fn from_rgba_image(rgba: &RgbaImage) -> ImageData<'static> {
    ImageData {
        width: rgba.width() as usize,
        height: rgba.height() as usize,
        bytes: Cow::Owned(rgba.as_raw().clone()),
    }
}
```

## Anti-patterns

### Don't hold Clipboard across await points

```rust
// BAD: Clipboard held during async operation
let mut clipboard = Clipboard::new()?;
let text = clipboard.get_text()?;
some_async_operation().await; // Other processes blocked!
clipboard.set_text(&modified)?;

// GOOD: Drop clipboard before await
let text = {
    let mut clipboard = Clipboard::new()?;
    clipboard.get_text()?
};
some_async_operation().await;
{
    let mut clipboard = Clipboard::new()?;
    clipboard.set_text(&modified)?;
}
```

### Don't assume content type

```rust
// BAD: Panics if clipboard has image
let text = clipboard.get_text().unwrap();

// GOOD: Handle both content types
if let Ok(text) = clipboard.get_text() {
    handle_text(&text);
} else if let Ok(image) = clipboard.get_image() {
    handle_image(&image);
}
```

### Don't poll clipboard content directly on Linux

```rust
// BAD: Expensive on Linux (reads full payload)
loop {
    let content = clipboard.get_text();
    thread::sleep(Duration::from_millis(100));
}

// GOOD: Use OS-level change detection when available
// (macOS: NSPasteboard.changeCount, Windows: clipboard sequence number)
```

### Don't forget to handle errors

```rust
// BAD: Silent failure
let _ = clipboard.set_text("text");

// GOOD: Log or propagate errors
clipboard.set_text("text").context("Failed to set clipboard")?;
```

### Don't create ImageData with wrong byte count

```rust
// BAD: Bytes don't match dimensions
let image = ImageData {
    width: 100,
    height: 100,
    bytes: Cow::Owned(vec![0u8; 1000]), // Should be 40000!
};

// GOOD: Validate or compute correctly
let width = 100;
let height = 100;
let bytes = vec![0u8; width * height * 4];
let image = ImageData { width, height, bytes: Cow::Owned(bytes) };
```

## Error Handling Best Practices

```rust
use arboard::{Clipboard, Error};
use anyhow::{Context, Result};

fn clipboard_operation() -> Result<String> {
    let mut clipboard = Clipboard::new()
        .context("Failed to access clipboard")?;
    
    match clipboard.get_text() {
        Ok(text) => Ok(text),
        Err(Error::ContentNotAvailable) => {
            // Empty clipboard is often expected
            Ok(String::new())
        }
        Err(Error::ClipboardOccupied) => {
            // Retry logic might help
            anyhow::bail!("Clipboard busy, try again")
        }
        Err(e) => {
            anyhow::bail!("Clipboard error: {}", e)
        }
    }
}
```

## Feature Flags

- `image-data` (default) - Enable image support
- `wayland-data-control` - Use wl-clipboard protocol on Wayland

```toml
[dependencies]
arboard = { version = "3.6", default-features = false }  # Text only
arboard = { version = "3.6", features = ["image-data"] }  # With images
```
