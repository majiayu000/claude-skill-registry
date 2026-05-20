---
name: web-files-image-handling
description: Client-side image handling - preview generation, Canvas API resizing, compression, EXIF orientation, format conversion, memory management with object URL cleanup
---

# Image Handling Patterns

> **Quick Guide:** Use `URL.createObjectURL()` for image previews (most efficient). Resize/compress with Canvas API before upload. Always cleanup object URLs with `URL.revokeObjectURL()` to prevent memory leaks. Handle EXIF orientation for mobile photos. Use step-down scaling for quality preservation on large reductions.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST cleanup object URLs with `URL.revokeObjectURL()` in useEffect cleanup or when replacing URLs)**

**(You MUST check browser context before applying EXIF orientation - modern browsers auto-rotate, manual handling may cause double rotation)**

**(You MUST use step-down scaling when reducing images by more than 50% - single-pass resize loses quality)**

**(You MUST limit canvas dimensions to browser maximums (typically 4096px) - larger canvases crash browsers)**

**(You MUST use Web Workers for compression of large images - main thread blocking causes UI freeze)**

</critical_requirements>

---

**Auto-detection:** image preview, URL.createObjectURL, revokeObjectURL, canvas resize, image compression, EXIF orientation, toBlob, toDataURL, FileReader image, image thumbnail, client-side resize, image crop, canvas drawImage, createImageBitmap, image quality

**When to use:**

- Creating image previews before upload
- Resizing or compressing images client-side
- Handling EXIF orientation from mobile photos
- Converting between image formats (JPEG/PNG/WebP)
- Generating thumbnails from user-selected images
- Implementing image cropping interfaces

**Key patterns covered:**

- Object URL preview with proper cleanup
- Canvas API resize with quality preservation
- EXIF orientation normalization
- Step-down scaling for large reductions
- Format detection and conversion
- Memory management for image processing

**When NOT to use:**

- Server-side image processing (use backend skills)
- Image CDN/optimization services (use infrastructure skills)
- Complex image editing (consider dedicated libraries)

**Detailed Resources:**

- For code examples, see [examples/](examples/)
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

---

<philosophy>

## Philosophy

Client-side image handling improves UX by providing instant previews and reducing upload sizes before they hit your server. The key insight is that **preview and processing have different optimal approaches** - `URL.createObjectURL()` for previews (fast, memory-efficient), Canvas API for processing (resize, compress, convert).

**Core Principles:**

1. **Object URLs for preview** - No file reading, instant display, must cleanup
2. **Canvas for processing** - Resize, compress, convert formats
3. **Memory management is critical** - Leaked object URLs accumulate indefinitely
4. **EXIF awareness** - Mobile photos have orientation metadata
5. **Progressive quality** - Step-down scaling preserves sharpness

**Preview Method Comparison:**

| Method                       | Speed   | Memory             | Use Case             |
| ---------------------------- | ------- | ------------------ | -------------------- |
| `URL.createObjectURL()`      | Instant | Low (reference)    | Display previews     |
| `FileReader.readAsDataURL()` | Slow    | High (full Base64) | Need data URL string |
| Canvas `toDataURL()`         | Medium  | Medium             | After processing     |

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Object URL Preview with Cleanup

Use `URL.createObjectURL()` for instant image previews. **Always cleanup** to prevent memory leaks.

#### Constants

```typescript
// image-preview.ts
const ACCEPTED_IMAGE_TYPES = [
  "image/jpeg",
  "image/png",
  "image/webp",
  "image/gif",
];
```

#### Implementation

```typescript
// use-image-preview.ts
import { useState, useEffect, useCallback } from "react";

interface ImagePreviewState {
  file: File | null;
  previewUrl: string | null;
}

export function useImagePreview() {
  const [state, setState] = useState<ImagePreviewState>({
    file: null,
    previewUrl: null,
  });

  // Cleanup: Revoke URL to prevent memory leaks
  useEffect(() => {
    return () => {
      if (state.previewUrl) {
        URL.revokeObjectURL(state.previewUrl);
      }
    };
  }, [state.previewUrl]);

  const setFile = useCallback(
    (file: File | null) => {
      // Revoke previous URL if exists
      if (state.previewUrl) {
        URL.revokeObjectURL(state.previewUrl);
      }

      if (file) {
        const previewUrl = URL.createObjectURL(file);
        setState({ file, previewUrl });
      } else {
        setState({ file: null, previewUrl: null });
      }
    },
    [state.previewUrl],
  );

  const clear = useCallback(() => {
    if (state.previewUrl) {
      URL.revokeObjectURL(state.previewUrl);
    }
    setState({ file: null, previewUrl: null });
  }, [state.previewUrl]);

  return {
    file: state.file,
    previewUrl: state.previewUrl,
    setFile,
    clear,
  };
}
```

**Why good:** Instant preview without reading file into memory, proper cleanup prevents memory leaks, callback updates revoke previous URL before creating new one

```typescript
// BAD: No cleanup - memory leak
function BadImagePreview({ file }: { file: File }) {
  const [preview] = useState(() => URL.createObjectURL(file));
  // Memory leak - URL never revoked!
  return <img src={preview} alt="Preview" />;
}
```

**Why bad:** Object URL never revoked, memory accumulates with each new file, browser holds reference indefinitely

---

### Pattern 2: Multiple Image Preview Management

Track multiple images with individual cleanup.

#### Implementation

```typescript
// use-multiple-image-preview.ts
import { useState, useCallback, useEffect } from "react";

interface ImageFile {
  id: string;
  file: File;
  previewUrl: string;
}

const DEFAULT_MAX_IMAGES = 10;

export function useMultipleImagePreview(maxImages = DEFAULT_MAX_IMAGES) {
  const [images, setImages] = useState<ImageFile[]>([]);

  const addImages = useCallback(
    (files: File[]) => {
      setImages((current) => {
        const availableSlots = maxImages - current.length;
        const filesToAdd = files.slice(0, availableSlots);

        const newImages: ImageFile[] = filesToAdd.map((file) => ({
          id: crypto.randomUUID(),
          file,
          previewUrl: URL.createObjectURL(file),
        }));

        return [...current, ...newImages];
      });
    },
    [maxImages],
  );

  const removeImage = useCallback((id: string) => {
    setImages((current) => {
      const image = current.find((img) => img.id === id);
      if (image) {
        URL.revokeObjectURL(image.previewUrl);
      }
      return current.filter((img) => img.id !== id);
    });
  }, []);

  const clearAll = useCallback(() => {
    setImages((current) => {
      current.forEach((img) => URL.revokeObjectURL(img.previewUrl));
      return [];
    });
  }, []);

  // Cleanup all on unmount
  useEffect(() => {
    return () => {
      images.forEach((img) => URL.revokeObjectURL(img.previewUrl));
    };
  }, []); // Empty deps - only cleanup on unmount

  return {
    images,
    addImages,
    removeImage,
    clearAll,
    canAddMore: images.length < maxImages,
  };
}
```

**Why good:** Individual URL cleanup on remove, batch cleanup on clear/unmount, enforces max limit, unique IDs for React keys

---

### Pattern 3: Canvas Resize with Quality Preservation

Resize images using Canvas API with proper quality settings.

#### Constants

```typescript
// image-resize.ts
const DEFAULT_MAX_WIDTH = 1920;
const DEFAULT_MAX_HEIGHT = 1080;
const DEFAULT_QUALITY = 0.85;
const MAX_CANVAS_DIMENSION = 4096;
```

#### Implementation

```typescript
// image-resize.ts
interface ResizeOptions {
  maxWidth?: number;
  maxHeight?: number;
  quality?: number;
  mimeType?: "image/jpeg" | "image/png" | "image/webp";
}

export async function resizeImage(
  file: File,
  options: ResizeOptions = {},
): Promise<Blob> {
  const {
    maxWidth = DEFAULT_MAX_WIDTH,
    maxHeight = DEFAULT_MAX_HEIGHT,
    quality = DEFAULT_QUALITY,
    mimeType = "image/jpeg",
  } = options;

  const img = await createImageFromFile(file);
  const { width, height } = calculateDimensions(
    img.width,
    img.height,
    maxWidth,
    maxHeight,
  );

  const canvas = document.createElement("canvas");
  canvas.width = width;
  canvas.height = height;

  const ctx = canvas.getContext("2d");
  if (!ctx) {
    throw new Error("Failed to get canvas context");
  }

  // Enable high-quality image smoothing
  ctx.imageSmoothingEnabled = true;
  ctx.imageSmoothingQuality = "high";

  ctx.drawImage(img, 0, 0, width, height);

  return new Promise((resolve, reject) => {
    canvas.toBlob(
      (blob) => {
        if (blob) {
          resolve(blob);
        } else {
          reject(new Error("Failed to create blob"));
        }
      },
      mimeType,
      quality,
    );
  });
}

function createImageFromFile(file: File): Promise<HTMLImageElement> {
  return new Promise((resolve, reject) => {
    const img = new Image();
    const url = URL.createObjectURL(file);

    img.onload = () => {
      URL.revokeObjectURL(url);
      resolve(img);
    };

    img.onerror = () => {
      URL.revokeObjectURL(url);
      reject(new Error("Failed to load image"));
    };

    img.src = url;
  });
}

function calculateDimensions(
  originalWidth: number,
  originalHeight: number,
  maxWidth: number,
  maxHeight: number,
): { width: number; height: number } {
  // Clamp to browser canvas limits
  const safeMaxWidth = Math.min(maxWidth, MAX_CANVAS_DIMENSION);
  const safeMaxHeight = Math.min(maxHeight, MAX_CANVAS_DIMENSION);

  let width = originalWidth;
  let height = originalHeight;

  if (width > safeMaxWidth || height > safeMaxHeight) {
    const widthRatio = safeMaxWidth / width;
    const heightRatio = safeMaxHeight / height;
    const ratio = Math.min(widthRatio, heightRatio);

    width = Math.round(width * ratio);
    height = Math.round(height * ratio);
  }

  return { width, height };
}
```

**Why good:** Maintains aspect ratio, clamps to browser limits, high-quality smoothing enabled, cleans up temporary URL immediately

```typescript
// BAD: May crash browser with large images
async function badResize(file: File) {
  const img = await createImageFromFile(file);
  const canvas = document.createElement("canvas");
  // No dimension limit - can exceed 32k pixels and crash
  canvas.width = img.width;
  canvas.height = img.height;
}
```

**Why bad:** No dimension limits, very large images crash the browser, canvas context allocation fails

---

### Pattern 4: Step-Down Scaling for Large Reductions

For significant size reductions (>50%), scale in multiple steps to preserve quality.

#### Implementation

```typescript
// step-down-resize.ts
const DEFAULT_STEPS = 2;
const STEP_THRESHOLD_RATIO = 0.5;

export async function stepDownResize(
  file: File,
  targetWidth: number,
  targetHeight: number,
  steps = DEFAULT_STEPS,
): Promise<Blob> {
  const img = await createImageFromFile(file);

  // Calculate if step-down is needed
  const widthRatio = targetWidth / img.width;
  const heightRatio = targetHeight / img.height;
  const minRatio = Math.min(widthRatio, heightRatio);

  // Single-pass if reduction is less than 50%
  if (minRatio > STEP_THRESHOLD_RATIO) {
    return resizeImage(file, {
      maxWidth: targetWidth,
      maxHeight: targetHeight,
    });
  }

  let currentWidth = img.width;
  let currentHeight = img.height;
  let source: HTMLImageElement | HTMLCanvasElement = img;

  const widthFactor = Math.pow(targetWidth / currentWidth, 1 / steps);
  const heightFactor = Math.pow(targetHeight / currentHeight, 1 / steps);

  for (let i = 0; i < steps; i++) {
    const isLastStep = i === steps - 1;

    currentWidth = isLastStep
      ? targetWidth
      : Math.round(currentWidth * widthFactor);
    currentHeight = isLastStep
      ? targetHeight
      : Math.round(currentHeight * heightFactor);

    const canvas = document.createElement("canvas");
    canvas.width = currentWidth;
    canvas.height = currentHeight;

    const ctx = canvas.getContext("2d");
    if (!ctx) throw new Error("Failed to get context");

    ctx.imageSmoothingEnabled = true;
    ctx.imageSmoothingQuality = "high";
    ctx.drawImage(source, 0, 0, currentWidth, currentHeight);

    source = canvas;
  }

  const finalCanvas = source as HTMLCanvasElement;
  return new Promise((resolve, reject) => {
    finalCanvas.toBlob(
      (blob) =>
        blob ? resolve(blob) : reject(new Error("Blob creation failed")),
      "image/jpeg",
      DEFAULT_QUALITY,
    );
  });
}
```

**Why good:** Gradual scaling preserves sharpness, auto-detects when step-down is needed, configurable step count

---

### Pattern 5: EXIF Orientation Handling

Normalize image orientation from mobile photo metadata.

> **Important (2020+):** Modern browsers automatically respect EXIF orientation:
>
> - `<img>` elements: CSS `image-orientation` defaults to `from-image`
> - Canvas `drawImage()`: Chromium browsers (Chrome 81+) auto-apply EXIF rotation
>
> **Only use manual EXIF handling when:**
>
> - Processing images for upload/output files (server may not handle EXIF)
> - Supporting legacy browsers (pre-2020)
> - Using Node.js canvas (doesn't auto-rotate)
> - You need to detect orientation without rendering

#### Constants

```typescript
// exif-orientation.ts
type Orientation = 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8;

const EXIF_MARKER = 0xffe1;
const ORIENTATION_TAG = 0x0112;
const ORIENTATIONS_NEEDING_SWAP = [5, 6, 7, 8];
```

#### Implementation

```typescript
// exif-orientation.ts
export async function getExifOrientation(file: File): Promise<Orientation> {
  const HEADER_SIZE = 65536;
  const buffer = await file.slice(0, HEADER_SIZE).arrayBuffer();
  const view = new DataView(buffer);

  // Check for JPEG
  if (view.getUint16(0) !== 0xffd8) {
    return 1; // Not JPEG, assume normal orientation
  }

  let offset = 2;
  while (offset < view.byteLength) {
    const marker = view.getUint16(offset);
    offset += 2;

    if (marker === EXIF_MARKER) {
      // Found EXIF segment
      const length = view.getUint16(offset);
      const exifData = new DataView(buffer, offset + 2, length - 2);
      return parseExifOrientation(exifData);
    }

    // Skip non-EXIF segments
    const segmentLength = view.getUint16(offset);
    offset += segmentLength;
  }

  return 1; // No EXIF found, assume normal
}

function parseExifOrientation(view: DataView): Orientation {
  // Simplified EXIF parsing - checks for orientation tag
  const littleEndian = view.getUint16(6) === 0x4949;
  const ifdOffset = view.getUint32(10, littleEndian);
  const numEntries = view.getUint16(14 + ifdOffset, littleEndian);

  for (let i = 0; i < numEntries; i++) {
    const entryOffset = 16 + ifdOffset + i * 12;
    const tag = view.getUint16(entryOffset, littleEndian);

    if (tag === ORIENTATION_TAG) {
      return view.getUint16(entryOffset + 8, littleEndian) as Orientation;
    }
  }

  return 1;
}

export async function normalizeOrientation(file: File): Promise<Blob> {
  const orientation = await getExifOrientation(file);

  // Normal orientation - no transform needed
  if (orientation === 1) {
    return file;
  }

  const img = await createImageFromFile(file);
  const canvas = document.createElement("canvas");
  const ctx = canvas.getContext("2d");
  if (!ctx) throw new Error("Failed to get context");

  // Swap dimensions for 90/270 degree rotations
  const needsSwap = ORIENTATIONS_NEEDING_SWAP.includes(orientation);
  canvas.width = needsSwap ? img.height : img.width;
  canvas.height = needsSwap ? img.width : img.height;

  applyOrientationTransform(ctx, orientation, img.width, img.height);
  ctx.drawImage(img, 0, 0);

  return new Promise((resolve, reject) => {
    canvas.toBlob(
      (blob) => (blob ? resolve(blob) : reject(new Error("Blob failed"))),
      file.type || "image/jpeg",
      DEFAULT_QUALITY,
    );
  });
}

function applyOrientationTransform(
  ctx: CanvasRenderingContext2D,
  orientation: Orientation,
  width: number,
  height: number,
): void {
  switch (orientation) {
    case 2:
      ctx.transform(-1, 0, 0, 1, width, 0);
      break; // Flip horizontal
    case 3:
      ctx.transform(-1, 0, 0, -1, width, height);
      break; // Rotate 180
    case 4:
      ctx.transform(1, 0, 0, -1, 0, height);
      break; // Flip vertical
    case 5:
      ctx.transform(0, 1, 1, 0, 0, 0);
      break; // Rotate 90 CW + flip
    case 6:
      ctx.transform(0, 1, -1, 0, height, 0);
      break; // Rotate 90 CW
    case 7:
      ctx.transform(0, -1, -1, 0, height, width);
      break; // Rotate 90 CCW + flip
    case 8:
      ctx.transform(0, -1, 1, 0, 0, width);
      break; // Rotate 90 CCW
  }
}
```

**Why good:** Reads EXIF without loading full image, handles all 8 orientations, preserves original quality setting

---

### Pattern 6: Format Conversion with Quality Control

Convert images to optimal formats for web delivery.

#### Constants

```typescript
// format-conversion.ts
const FORMAT_SUPPORT_CACHE = new Map<string, boolean>();

const WEBP_TEST_DATA =
  "data:image/webp;base64,UklGRh4AAABXRUJQVlA4TBEAAAAvAAAAAAfQ//73v/+BiOh/AAA=";

const FORMAT_QUALITY_DEFAULTS: Record<string, number> = {
  "image/jpeg": 0.85,
  "image/webp": 0.82,
  "image/png": 1, // PNG is lossless
};
```

#### Implementation

```typescript
// format-conversion.ts
export async function supportsWebP(): Promise<boolean> {
  if (FORMAT_SUPPORT_CACHE.has("webp")) {
    return FORMAT_SUPPORT_CACHE.get("webp")!;
  }

  const supported = await new Promise<boolean>((resolve) => {
    const img = new Image();
    img.onload = () => resolve(img.width > 0 && img.height > 0);
    img.onerror = () => resolve(false);
    img.src = WEBP_TEST_DATA;
  });

  FORMAT_SUPPORT_CACHE.set("webp", supported);
  return supported;
}

export async function convertToFormat(
  file: File,
  targetFormat: "image/jpeg" | "image/png" | "image/webp",
  quality?: number,
): Promise<Blob> {
  const img = await createImageFromFile(file);
  const canvas = document.createElement("canvas");
  canvas.width = img.width;
  canvas.height = img.height;

  const ctx = canvas.getContext("2d");
  if (!ctx) throw new Error("Failed to get context");

  // Fill white background for JPEG (no transparency)
  if (targetFormat === "image/jpeg") {
    ctx.fillStyle = "#ffffff";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
  }

  ctx.drawImage(img, 0, 0);

  const finalQuality =
    quality ?? FORMAT_QUALITY_DEFAULTS[targetFormat] ?? DEFAULT_QUALITY;

  return new Promise((resolve, reject) => {
    canvas.toBlob(
      (blob) => (blob ? resolve(blob) : reject(new Error("Conversion failed"))),
      targetFormat,
      finalQuality,
    );
  });
}

export async function convertToOptimalFormat(file: File): Promise<Blob> {
  const webpSupported = await supportsWebP();
  const targetFormat = webpSupported ? "image/webp" : "image/jpeg";
  return convertToFormat(file, targetFormat);
}
```

**Why good:** Caches format detection results, handles JPEG transparency correctly (white background), uses format-specific quality defaults

</patterns>

---

<integration>

## Integration Guide

**Styling Integration:**
Image preview components accept `className` prop for styling flexibility.
Use `data-loading` and `data-error` attributes for state-based styling.

**Component Integration:**
Image handling functions return Blobs/URLs that work with any component approach.
Preview URLs work directly with `<img>` elements.

**Processing Integration:**
All processing functions accept File objects and return Blobs.
Results can be converted to Files for form submission.

</integration>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Not calling `URL.revokeObjectURL()` - causes memory leaks that accumulate indefinitely
- Canvas dimensions exceeding 4096px - crashes browser tab or silently fails
- Processing images on main thread without Web Workers - UI freezes for large images
- Double EXIF rotation - applying manual rotation in browsers that auto-rotate (Chrome 81+, Safari, Firefox)

**Medium Priority Issues:**

- Using `FileReader.readAsDataURL()` for preview - slow and memory-intensive
- Single-pass resize for large reductions (>50%) - results in blurry images
- Not checking format support before WebP conversion - breaks on older browsers

**Common Mistakes:**

- Forgetting cleanup in useEffect return function
- Creating object URLs in render (creates new URL every render)
- Not handling image load errors gracefully
- Using toDataURL instead of toBlob (toBlob is async and more efficient)

**Gotchas & Edge Cases:**

- Object URLs are session-scoped - they work until page unload even without cleanup (but waste memory)
- Canvas `toBlob()` is async, `toDataURL()` is sync - use toBlob for better performance
- Modern browsers auto-rotate EXIF (since 2020) - manual rotation causes double-rotation issues
- Use `image-orientation: none` CSS to bypass auto-rotation when needed
- PNG with transparency converted to JPEG needs white background fill
- Very large images may exceed WebGL limits even within canvas limits
- Node.js canvas does NOT auto-rotate - still needs manual EXIF handling on server

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST cleanup object URLs with `URL.revokeObjectURL()` in useEffect cleanup or when replacing URLs)**

**(You MUST check browser context before applying EXIF orientation - modern browsers auto-rotate, manual handling may cause double rotation)**

**(You MUST use step-down scaling when reducing images by more than 50% - single-pass resize loses quality)**

**(You MUST limit canvas dimensions to browser maximums (typically 4096px) - larger canvases crash browsers)**

**(You MUST use Web Workers for compression of large images - main thread blocking causes UI freeze)**

**Failure to follow these rules will cause memory leaks, browser crashes, and poor image quality.**

</critical_reminders>
