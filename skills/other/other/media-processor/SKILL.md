---
name: media-processor
description: "Process multimedia content — audio transcription, video analysis, PDF data extraction, image generation. Use for deeper image analysis when implementing from UI designs, analyzing charts for data, reading dense screenshots, or studying artworks and visual references."
---

# Media Processor

Process audio, images, videos, documents, and generate images using Google Gemini's multimodal API. Unified interface for all multimedia content understanding and generation.

## Core Capabilities

### Image Understanding
- Image captioning and description
- Object detection with bounding boxes (2.0+)
- Pixel-level segmentation (2.5+)
- Visual question answering
- Multi-image comparison (up to 3,600 images)
- OCR and text extraction

### Video Analysis
- Scene detection and summarization
- Video Q&A with temporal understanding
- Transcription with visual descriptions
- YouTube URL support
- Long video processing (up to 6 hours)
- Frame-level analysis

### Document Extraction
- Native PDF vision processing (up to 1,000 pages)
- Table and form extraction
- Chart and diagram analysis
- Multi-page document understanding
- Structured data output (JSON schema)
- Format conversion (PDF to HTML/JSON)

### Image Generation
- Text-to-image generation
- High-quality generation variant (`generate-hq`) for detailed outputs
- Image editing and modification
- Multi-image composition (up to 3 images)
- Iterative refinement
- Multiple aspect ratios (1:1, 16:9, 9:16, 4:3, 3:4)
- Controllable style and quality

### Audio Processing
- Transcription with timestamps (up to 9.5 hours)
- Audio summarization and analysis
- Speech understanding and speaker identification
- Music and environmental sound analysis
- Text-to-speech generation with controllable voice

## Supported Tasks

| Task | Description |
|------|-------------|
| `transcribe` | Audio/video transcription with timestamps |
| `analyze` | Image, video, or audio analysis with custom prompts |
| `extract` | Structured data extraction from PDFs and documents |
| `generate` | Text-to-image generation |
| `generate-hq` | High-quality image generation with enhanced detail |

See [model routing](./references/model-routing.md) for model selection per task.

## Pasted Images

When user pastes images in chat, they are auto-saved to:
```
$CLAUDE_DIR/image-cache/<current_session_id>/<image_number>.png
```
Example: Image #1 → `$CLAUDE_DIR/image-cache/<session_id>/1.png`

**To process pasted images**, find files in this directory and pass them to the scripts. Use `ls "$CLAUDE_DIR/image-cache/"` to discover the current session ID, then list its contents for available images.

## Quick Start

### Prerequisites

**API Key Setup**: Supports both Google AI Studio and Vertex AI.

Set `GEMINI_API_KEY` via environment or `.claude/skills/media-processor/.env`.

**Get API key**: https://aistudio.google.com/apikey

**For Vertex AI**:
```bash
export GEMINI_USE_VERTEX=true
export VERTEX_PROJECT_ID=your-gcp-project-id
export VERTEX_LOCATION=us-central1  # Optional
```

**Install SDK**:
```bash
pip install google-genai python-dotenv pillow
```

### Common Patterns

**Transcribe Audio**:
```bash
python scripts/gemini_batch_process.py \
  --files audio.mp3 \
  --task transcribe
```

**Analyze Image**:
```bash
python scripts/gemini_batch_process.py \
  --files image.jpg \
  --task analyze \
  --prompt "Describe this image" \
  --output docs/assets/<output-name>.md
```

**Process Video**:
```bash
python scripts/gemini_batch_process.py \
  --files video.mp4 \
  --task analyze \
  --prompt "Summarize key points with timestamps" \
  --output docs/assets/<output-name>.md
```

**Extract from PDF**:
```bash
python scripts/gemini_batch_process.py \
  --files document.pdf \
  --task extract \
  --prompt "Extract table data as JSON" \
  --output docs/assets/<output-name>.md \
  --format json
```

**Generate Image**:
```bash
python scripts/image_gen.py \
  --prompt "A futuristic city at sunset" \
  --output docs/assets/<output-file-name>.png \
  --aspect-ratio 16:9
```

**Generate High-Quality Image**:
```bash
python scripts/image_gen.py \
  --prompt "Detailed architectural blueprint of a modern house" \
  --output docs/assets/<output-file-name>.png \
  --mode generate-hq
```

**Edit an Existing Image**:
```bash
python scripts/image_gen.py \
  --prompt "Make the sky sunset colors" \
  --input photo.jpg \
  --output docs/assets/edited.png
```

**Convert Documents to Markdown**:
```bash
# Convert to PDF
python scripts/document_converter.py \
  --input document.docx \
  --output docs/assets/document.md

# Extract pages
python scripts/document_converter.py \
  --input large.pdf \
  --output docs/assets/chapter1.md \
  --pages 1-20
```

## Supported Formats

### Audio
- WAV, MP3, AAC, FLAC, OGG Vorbis, AIFF
- Max 9.5 hours per request
- Auto-downsampled to 16 Kbps mono

### Images
- PNG, JPEG, WEBP, HEIC, HEIF
- Max 3,600 images per request
- Resolution: <=384px = 258 tokens, larger = tiled

### Video
- MP4, MPEG, MOV, AVI, FLV, MPG, WebM, WMV, 3GPP
- Max 6 hours (low-res) or 2 hours (default)
- YouTube URLs supported (public only)

### Documents
- PDF only for vision processing
- Max 1,000 pages
- TXT, HTML, Markdown supported (text-only)

### Size Limits
- **Inline**: <20MB total request
- **File API**: 2GB per file, 20GB project quota
- **Retention**: 48 hours auto-delete

## Reference Navigation

For detailed implementation guidance, see:

| Reference | Description |
|-----------|-------------|
| [audio-processing.md](./references/audio-processing.md) | Transcription, analysis, TTS, timestamps, multi-speaker |
| [vision-understanding.md](./references/vision-understanding.md) | Captioning, detection, segmentation, OCR, multi-image |
| [video-analysis.md](./references/video-analysis.md) | Scene detection, YouTube, timestamps, long video |
| [image-generation.md](./references/image-generation.md) | Text-to-image, editing, composition, aspect ratios |
| [model-routing.md](./references/model-routing.md) | Model selection per task, pricing, context windows |
| [document-extraction.md](./references/document-extraction.md) | PDF processing, table extraction, structured output |
| [media-optimization.md](./references/media-optimization.md) | ffmpeg recipes for compressing/resizing before upload |

## Scripts Overview

All scripts support unified API key detection and error handling:

**gemini_batch_process.py**: Batch process multiple media files
- Supports file-based modalities (audio, image, video, PDF)
- Tasks: transcribe, analyze, extract
- Progress tracking and error recovery
- Output formats: JSON, Markdown, CSV
- Rate limiting and retry logic
- Dry-run mode

**image_gen.py**: Generate images from text prompts
- Modes: generate (standard) and generate-hq (high quality)
- Image editing with optional input image
- Aspect ratio control
- Retry logic and error handling

**document_converter.py**: Convert documents to PDF
- Convert DOCX, XLSX, PPTX to PDF
- Extract page ranges
- Optimize PDFs for Gemini
- Extract images from PDFs
- Batch conversion support

Run any script with `--help` for detailed usage.

## Error Handling

Common errors and solutions:
- **400**: Invalid format/size - validate before upload
- **401**: Invalid API key - check configuration
- **403**: Permission denied - verify API key restrictions
- **404**: File not found - ensure file uploaded and active
- **429**: Rate limit exceeded - implement exponential backoff
- **500**: Server error - retry with backoff

## Resources

- [Audio API Docs](https://ai.google.dev/gemini-api/docs/audio)
- [Image API Docs](https://ai.google.dev/gemini-api/docs/image-understanding)
- [Video API Docs](https://ai.google.dev/gemini-api/docs/video-understanding)
- [Document API Docs](https://ai.google.dev/gemini-api/docs/document-processing)
- [Image Gen Docs](https://ai.google.dev/gemini-api/docs/image-generation)
- [Get API Key](https://aistudio.google.com/apikey)
- [Pricing](https://ai.google.dev/pricing)
