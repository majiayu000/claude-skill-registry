---
name: synapse-file-conversion
description: >
  Use when source files need format conversion before upload.
  Triggers on: "convert", "tiff to png", "file format", "unsupported extension".
---

# File Conversion for Synapse Upload

Knowledge about when and how to convert files before uploading to a data collection.

## When Conversion Is Needed

Conversion is required when source file extensions don't match the data collection's file specification allowed extensions.

**Example**: Spec `image_1` allows `[".png", ".jpg"]` but the source directory contains `.tiff` files. The TIFFs must be converted to PNG or JPG before upload.

### Detection Logic

1. Get the file specs from the data collection (each spec has `extensions` list)
2. Scan the source directory for actual file extensions
3. For each spec, check if source extensions are in the allowed list
4. If not, determine if a supported conversion exists

## Supported Conversions

### Image Conversions (via Pillow)

| Source | Target | Notes |
|--------|--------|-------|
| `.tiff`, `.tif` | `.png` | Lossless conversion |
| `.tiff`, `.tif` | `.jpg`, `.jpeg` | RGBA/P modes auto-converted to RGB |
| `.bmp` | `.png` | Lossless conversion |
| `.bmp` | `.jpg`, `.jpeg` | Mode conversion applied |
| `.webp` | `.png` | Lossless conversion |
| `.webp` | `.jpg`, `.jpeg` | Mode conversion applied |
| `.gif` | `.png` | First frame only |

**Requirement**: `Pillow>=10.0` must be installed in the upload plugin environment.

### Video Conversions (via ffmpeg)

| Source | Target | Notes |
|--------|--------|-------|
| `.mov` | `.mp4` | H.264 + AAC, faststart |
| `.avi` | `.mp4` | H.264 + AAC, faststart |
| `.mkv` | `.mp4` | H.264 + AAC, faststart |
| `.webm` | `.mp4` | H.264 + AAC, faststart |
| `.flv` | `.mp4` | H.264 + AAC, faststart |
| `.wmv` | `.mp4` | H.264 + AAC, faststart |

**Requirement**: `ffmpeg` must be available in PATH. Timeout: 600 seconds per file.

### Audio Conversions (via ffmpeg)

| Source | Target | Notes |
|--------|--------|-------|
| `.wav` | `.mp3` | Default quality |
| `.flac` | `.mp3` | Lossy conversion |
| `.ogg` | `.mp3` | Lossy conversion |
| `.m4a` | `.mp3` | Lossy conversion |
| `.wma` | `.mp3` | Lossy conversion |
| `.wav` | `.aac` | Default quality |
| `.flac` | `.aac` | Lossy conversion |
| `.ogg` | `.aac` | Lossy conversion |

**Requirement**: `ffmpeg` must be available in PATH. Timeout: 300 seconds per file.

## Conversion in the Upload Workflow

### Using the ai-upload-plugin's Built-in Conversion

The `ai-upload-plugin` has a `convert_file` tool that handles conversion automatically:

```json
{
  "name": "convert_file",
  "input": {
    "source_path": "/data/patient_001/scan.tiff",
    "target_format": ".png"
  }
}
```

Converted files are stored in a temp directory and automatically cleaned up after upload.

### Manual Conversion Before Upload

If not using the ai-upload-plugin, convert files beforehand:

**Images (Pillow):**
```bash
python3 -c "
from PIL import Image
from pathlib import Path
import sys

src = Path(sys.argv[1])
dst = src.with_suffix('.png')
with Image.open(src) as img:
    img.save(dst)
print(f'Converted: {dst}')
" /path/to/image.tiff
```

**Batch image conversion:**
```bash
python3 -c "
from PIL import Image
from pathlib import Path
import sys

src_dir = Path(sys.argv[1])
for tiff in src_dir.rglob('*.tiff'):
    dst = tiff.with_suffix('.png')
    with Image.open(tiff) as img:
        img.save(dst)
    print(f'Converted: {dst}')
" /path/to/directory
```

**Video (ffmpeg):**
```bash
ffmpeg -i input.mov -c:v libx264 -c:a aac -movflags +faststart output.mp4
```

**Audio (ffmpeg):**
```bash
ffmpeg -i input.wav output.mp3
```

## Conversion Decision Tree

```
Source file extension NOT in spec's allowed extensions?
├── YES → Check if a supported conversion exists
│   ├── YES → Convert the file, use converted path for upload
│   └── NO → Report error: unsupported file format
└── NO → No conversion needed, use source file directly
```

## Important Notes

- Converted files use a temporary directory that is cleaned up after the upload completes
- For large datasets, conversion can be the bottleneck — consider pre-converting files outside the upload workflow
- Image conversion preserves the original filename stem, only changing the extension
- RGBA/Palette mode images are automatically converted to RGB when targeting JPEG format
- If ffmpeg is not installed, video/audio conversions will fail gracefully with a warning
