---
name: gemini-3-multimodal
description: Process multimodal inputs (images, video, audio, PDFs) with Gemini 3 Pro. Covers image understanding, video analysis, audio processing, document extraction, media resolution control, OCR, and token optimization. Use when analyzing images, processing video, transcribing audio, extracting PDF content, or working with multimodal data.
---

# Gemini 3 Pro Multimodal Input Processing

Comprehensive guide for processing multimodal inputs with Gemini 3 Pro, including image understanding, video analysis, audio processing, and PDF document extraction. This skill focuses on INPUT processing (analyzing media) - see `gemini-3-image-generation` for OUTPUT (generating images).

## Overview

**Gemini 3 Pro** provides native multimodal capabilities for understanding and analyzing various media types. This skill covers all input processing operations with granular control over quality, performance, and token consumption.

### Key Capabilities

- **Image Understanding:** Object detection, OCR, visual Q&A, code from screenshots
- **Video Processing:** Up to 1 hour of video, frame analysis, OCR
- **Audio Processing:** Up to 9.5 hours of audio, speech understanding
- **PDF Documents:** Native PDF support, multi-page analysis, text extraction
- **Media Resolution Control:** Low/medium/high resolution for token optimization
- **Token Optimization:** Granular control over processing costs

### When to Use This Skill

- Analyzing images, photos, or screenshots
- Processing video content for insights
- Transcribing or understanding audio/speech
- Extracting information from PDF documents
- Building multimodal applications
- Optimizing media processing costs

---

## Quick Start

### Prerequisites

- **Gemini API setup** (see `gemini-3-pro-api` skill)
- **Media files** in supported formats

### Python Quick Start

```python
import google.generativeai as genai
from pathlib import Path

genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel("gemini-3-pro-preview")

# Upload and analyze image
image_file = genai.upload_file(Path("photo.jpg"))
response = model.generate_content([
    "What's in this image?",
    image_file
])
print(response.text)
```

### Node.js Quick Start

```typescript
import { GoogleGenerativeAI } from "@google/generative-ai";
import { GoogleAIFileManager } from "@google/generative-ai/server";
import fs from "fs";

const genAI = new GoogleGenerativeAI("YOUR_API_KEY");
const fileManager = new GoogleAIFileManager("YOUR_API_KEY");

// Upload and analyze image
const uploadResult = await fileManager.uploadFile("photo.jpg", {
  mimeType: "image/jpeg"
});

const model = genAI.getGenerativeModel({ model: "gemini-3-pro-preview" });
const result = await model.generateContent([
  "What's in this image?",
  { fileData: { fileUri: uploadResult.file.uri, mimeType: uploadResult.file.mimeType } }
]);

console.log(result.response.text());
```

---

## Core Tasks

### Task 1: Analyze Image Content

**Goal:** Extract information, objects, text, or insights from images.

**Use Cases:**
- Object detection and recognition
- OCR (text extraction from images)
- Visual Q&A
- Code generation from UI screenshots
- Chart/diagram analysis
- Product identification

**Python Example:**

```python
import google.generativeai as genai
from pathlib import Path

genai.configure(api_key="YOUR_API_KEY")

# Configure model with high resolution for best quality
model = genai.GenerativeModel(
    "gemini-3-pro-preview",
    generation_config={
        "thinking_level": "high",
        "media_resolution": "high"  # 1,120 tokens per image
    }
)

# Upload image
image_path = Path("screenshot.png")
image_file = genai.upload_file(image_path)

# Analyze with specific prompt
response = model.generate_content([
    """Analyze this image and provide:
    1. Main objects and their locations
    2. Any visible text (OCR)
    3. Overall context and purpose
    4. If code/UI: describe the functionality
    """,
    image_file
])

print(response.text)

# Check token usage
print(f"Tokens used: {response.usage_metadata.total_token_count}")
```

**Node.js Example:**

```typescript
import { GoogleGenerativeAI } from "@google/generative-ai";
import { GoogleAIFileManager } from "@google/generative-ai/server";

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY!);
const fileManager = new GoogleAIFileManager(process.env.GEMINI_API_KEY!);

// Upload image
const uploadResult = await fileManager.uploadFile("screenshot.png", {
  mimeType: "image/png"
});

// Configure model with high resolution
const model = genAI.getGenerativeModel({
  model: "gemini-3-pro-preview",
  generationConfig: {
    thinking_level: "high",
    media_resolution: "high"  // Best quality for OCR
  }
});

const result = await model.generateContent([
  `Analyze this image and provide:
  1. Main objects and their locations
  2. Any visible text (OCR)
  3. Overall context and purpose`,
  { fileData: { fileUri: uploadResult.file.uri, mimeType: uploadResult.file.mimeType } }
]);

console.log(result.response.text());
```

**Resolution Options:**

| Resolution | Tokens per Image | Best For |
|-----------|------------------|----------|
| `low` | 280 tokens | Quick analysis, low detail |
| `medium` | 560 tokens | Balanced quality/cost |
| `high` | 1,120 tokens | OCR, fine details, small text |

**Supported Formats:** JPEG, PNG, WEBP, HEIC, HEIF

**See:** `references/image-understanding.md` for advanced patterns

---

### Task 2: Process Video Content

**Goal:** Analyze video content, extract insights, perform frame-by-frame analysis.

**Use Cases:**
- Video summarization
- Object tracking
- Scene detection
- Video OCR
- Content moderation
- Educational video analysis

**Python Example:**

```python
import google.generativeai as genai
from pathlib import Path

genai.configure(api_key="YOUR_API_KEY")

# Configure for video processing
model = genai.GenerativeModel(
    "gemini-3-pro-preview",
    generation_config={
        "thinking_level": "high",
        "media_resolution": "medium"  # 70 tokens/frame (balanced)
    }
)

# Upload video (up to 1 hour supported)
video_path = Path("tutorial.mp4")
video_file = genai.upload_file(video_path)

# Wait for processing
import time
while video_file.state.name == "PROCESSING":
    time.sleep(5)
    video_file = genai.get_file(video_file.name)

if video_file.state.name == "FAILED":
    raise ValueError("Video processing failed")

# Analyze video
response = model.generate_content([
    """Analyze this video and provide:
    1. Overall summary of content
    2. Key scenes and timestamps
    3. Main topics covered
    4. Any visible text throughout the video
    """,
    video_file
])

print(response.text)
print(f"Tokens used: {response.usage_metadata.total_token_count}")
```

**Node.js Example:**

```typescript
import { GoogleGenerativeAI } from "@google/generative-ai";
import { GoogleAIFileManager, FileState } from "@google/generative-ai/server";

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY!);
const fileManager = new GoogleAIFileManager(process.env.GEMINI_API_KEY!);

// Upload video
const uploadResult = await fileManager.uploadFile("tutorial.mp4", {
  mimeType: "video/mp4"
});

// Wait for processing
let file = await fileManager.getFile(uploadResult.file.name);
while (file.state === FileState.PROCESSING) {
  await new Promise(resolve => setTimeout(resolve, 5000));
  file = await fileManager.getFile(uploadResult.file.name);
}

if (file.state === FileState.FAILED) {
  throw new Error("Video processing failed");
}

// Analyze video
const model = genAI.getGenerativeModel({
  model: "gemini-3-pro-preview",
  generationConfig: {
    media_resolution: "medium"
  }
});

const result = await model.generateContent([
  `Analyze this video and provide:
  1. Overall summary
  2. Key scenes and timestamps
  3. Main topics covered`,
  { fileData: { fileUri: file.uri, mimeType: file.mimeType } }
]);

console.log(result.response.text());
```

**Video Specs:**
- **Max Duration:** 1 hour
- **Formats:** MP4, MOV, AVI, etc.
- **Resolution Options:** Low (70 tokens/frame), Medium (70 tokens/frame), High (280 tokens/frame)
- **OCR:** Available with high resolution

**See:** `references/video-processing.md` for advanced patterns

---

### Task 3: Process Audio/Speech

**Goal:** Transcribe and understand audio content, process speech.

**Use Cases:**
- Audio transcription
- Speech analysis
- Podcast summarization
- Meeting notes
- Language understanding
- Audio classification

**Python Example:**

```python
import google.generativeai as genai
from pathlib import Path

genai.configure(api_key="YOUR_API_KEY")

model = genai.GenerativeModel("gemini-3-pro-preview")

# Upload audio file (up to 9.5 hours supported)
audio_path = Path("podcast.mp3")
audio_file = genai.upload_file(audio_path)

# Wait for processing
import time
while audio_file.state.name == "PROCESSING":
    time.sleep(5)
    audio_file = genai.get_file(audio_file.name)

# Process audio
response = model.generate_content([
    """Process this audio and provide:
    1. Full transcription
    2. Summary of main points
    3. Key speakers (if multiple)
    4. Important timestamps
    5. Action items or conclusions
    """,
    audio_file
])

print(response.text)
print(f"Tokens used: {response.usage_metadata.total_token_count}")
```

**Node.js Example:**

```typescript
import { GoogleGenerativeAI } from "@google/generative-ai";
import { GoogleAIFileManager, FileState } from "@google/generative-ai/server";

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY!);
const fileManager = new GoogleAIFileManager(process.env.GEMINI_API_KEY!);

// Upload audio
const uploadResult = await fileManager.uploadFile("podcast.mp3", {
  mimeType: "audio/mp3"
});

// Wait for processing
let file = await fileManager.getFile(uploadResult.file.name);
while (file.state === FileState.PROCESSING) {
  await new Promise(resolve => setTimeout(resolve, 5000));
  file = await fileManager.getFile(uploadResult.file.name);
}

const model = genAI.getGenerativeModel({ model: "gemini-3-pro-preview" });

const result = await model.generateContent([
  `Process this audio and provide:
  1. Full transcription
  2. Summary of main points
  3. Key timestamps`,
  { fileData: { fileUri: file.uri, mimeType: file.mimeType } }
]);

console.log(result.response.text());
```

**Audio Specs:**
- **Max Duration:** 9.5 hours
- **Formats:** WAV, MP3, FLAC, AAC, etc.
- **Languages:** Supports multiple languages

**See:** `references/audio-processing.md` for advanced patterns

---

### Task 4: Process PDF Documents

**Goal:** Extract and analyze content from PDF documents.

**Use Cases:**
- Document analysis
- Information extraction
- Form processing
- Research paper analysis
- Contract review
- Multi-page document understanding

**Python Example:**

```python
import google.generativeai as genai
from pathlib import Path

genai.configure(api_key="YOUR_API_KEY")

# Configure with medium resolution (recommended for PDFs)
model = genai.GenerativeModel(
    "gemini-3-pro-preview",
    generation_config={
        "thinking_level": "high",
        "media_resolution": "medium"  # 560 tokens/page (saturation point)
    }
)

# Upload PDF
pdf_path = Path("research_paper.pdf")
pdf_file = genai.upload_file(pdf_path)

# Wait for processing
import time
while pdf_file.state.name == "PROCESSING":
    time.sleep(5)
    pdf_file = genai.get_file(pdf_file.name)

# Analyze PDF
response = model.generate_content([
    """Analyze this PDF document and provide:
    1. Document type and purpose
    2. Main sections and structure
    3. Key findings or arguments
    4. Important data or statistics
    5. Conclusions or recommendations
    """,
    pdf_file
])

print(response.text)
print(f"Tokens used: {response.usage_metadata.total_token_count}")
```

**Node.js Example:**

```typescript
import { GoogleGenerativeAI } from "@google/generative-ai";
import { GoogleAIFileManager, FileState } from "@google/generative-ai/server";

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY!);
const fileManager = new GoogleAIFileManager(process.env.GEMINI_API_KEY!);

// Upload PDF
const uploadResult = await fileManager.uploadFile("research_paper.pdf", {
  mimeType: "application/pdf"
});

// Wait for processing
let file = await fileManager.getFile(uploadResult.file.name);
while (file.state === FileState.PROCESSING) {
  await new Promise(resolve => setTimeout(resolve, 5000));
  file = await fileManager.getFile(uploadResult.file.name);
}

// Analyze with medium resolution (recommended)
const model = genAI.getGenerativeModel({
  model: "gemini-3-pro-preview",
  generationConfig: {
    media_resolution: "medium"
  }
});

const result = await model.generateContent([
  `Analyze this PDF and extract:
  1. Main sections
  2. Key findings
  3. Important data`,
  { fileData: { fileUri: file.uri, mimeType: file.mimeType } }
]);

console.log(result.response.text());
```

**PDF Processing Tips:**
- **Recommended Resolution:** `medium` (560 tokens/page) - saturation point for quality
- **Multi-page:** Automatically processes all pages
- **Native Support:** No conversion to images needed
- **Text Extraction:** High-quality text extraction built-in

**See:** `references/document-processing.md` for advanced patterns

---

### Task 5: Optimize Media Processing Costs

**Goal:** Balance quality and token consumption based on use case.

**Strategy:**

| Media Type | Resolution | Tokens | Use Case |
|-----------|-----------|---------|----------|
| **Images** | `low` | 280 | Quick scan, thumbnails |
| **Images** | `medium` | 560 | General analysis |
| **Images** | `high` | 1,120 | OCR, fine details, code |
| **PDFs** | `medium` | 560/page | **Recommended** (saturation point) |
| **PDFs** | `high` | 1,120/page | Diminishing returns |
| **Video** | `low`/`medium` | 70/frame | Most use cases |
| **Video** | `high` | 280/frame | OCR from video |

**Python Optimization Example:**

```python
import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")

# Different resolutions for different use cases
def analyze_image_optimized(image_path, need_ocr=False):
    """Analyze image with appropriate resolution"""
    resolution = "high" if need_ocr else "medium"

    model = genai.GenerativeModel(
        "gemini-3-pro-preview",
        generation_config={
            "media_resolution": resolution
        }
    )

    image_file = genai.upload_file(image_path)
    response = model.generate_content([
        "Describe this image" if not need_ocr else "Extract all text from this image",
        image_file
    ])

    # Log token usage for cost tracking
    tokens = response.usage_metadata.total_token_count
    cost = (tokens / 1_000_000) * 2.00  # Input pricing
    print(f"Resolution: {resolution}, Tokens: {tokens}, Cost: ${cost:.6f}")

    return response.text

# Use appropriate resolution
analyze_image_optimized("photo.jpg", need_ocr=False)  # medium
analyze_image_optimized("document.png", need_ocr=True)  # high
```

**Per-Item Resolution Control:**

```python
# Set different resolutions for different media in same request
response = model.generate_content([
    "Compare these images",
    {"file": image1, "media_resolution": "high"},  # High detail
    {"file": image2, "media_resolution": "low"},   # Low detail OK
])
```

**Cost Monitoring:**

```python
def log_media_costs(response):
    """Log media processing costs"""
    usage = response.usage_metadata

    # Pricing for ≤200k context
    input_cost = (usage.prompt_token_count / 1_000_000) * 2.00
    output_cost = (usage.candidates_token_count / 1_000_000) * 12.00

    print(f"Input tokens: {usage.prompt_token_count} (${input_cost:.6f})")
    print(f"Output tokens: {usage.candidates_token_count} (${output_cost:.6f})")
    print(f"Total cost: ${input_cost + output_cost:.6f}")
```

**See:** `references/token-optimization.md` for comprehensive strategies

---

## Media Resolution Control

### Resolution Options

| Setting | Images | PDFs | Video (per frame) | Recommendation |
|---------|--------|------|-------------------|----------------|
| `low` | 280 tokens | 280 tokens | 70 tokens | Quick analysis, low detail |
| `medium` | 560 tokens | 560 tokens | 70 tokens | Balanced quality/cost |
| `high` | 1,120 tokens | 1,120 tokens | 280 tokens | OCR, fine text, details |

### Configuration

**Global Setting (all media):**

```python
model = genai.GenerativeModel(
    "gemini-3-pro-preview",
    generation_config={
        "media_resolution": "high"  # Applies to all media
    }
)
```

**Per-Item Setting (mixed resolutions):**

```python
response = model.generate_content([
    "Analyze these files",
    {"file": high_detail_image, "media_resolution": "high"},
    {"file": low_detail_image, "media_resolution": "low"}
])
```

### Best Practices

1. **Images:** Use `high` for OCR/text extraction, `medium` for general analysis
2. **PDFs:** Use `medium` (saturation point - higher resolutions show diminishing returns)
3. **Video:** Use `low` or `medium` unless OCR needed
4. **Cost Control:** Start with `low`, increase only if quality insufficient

**See:** `references/media-resolution.md` for detailed guide

---

## File Management

### Upload Files

```python
import google.generativeai as genai

# Upload file
file = genai.upload_file("path/to/file.jpg")
print(f"Uploaded: {file.name}")

# Check processing status
while file.state.name == "PROCESSING":
    time.sleep(5)
    file = genai.get_file(file.name)

print(f"Status: {file.state.name}")
```

### List Uploaded Files

```python
# List all files
for file in genai.list_files():
    print(f"{file.name} - {file.display_name}")
```

### Delete Files

```python
# Delete specific file
genai.delete_file(file.name)

# Delete all files
for file in genai.list_files():
    genai.delete_file(file.name)
    print(f"Deleted: {file.name}")
```

### File Lifecycle

- **Upload:** Immediate
- **Processing:** Async (especially for video/audio)
- **Storage:** Files persist until deleted
- **Expiration:** Files may expire after period (check docs)

---

## Multi-File Processing

### Process Multiple Images

```python
# Upload multiple images
images = [
    genai.upload_file("photo1.jpg"),
    genai.upload_file("photo2.jpg"),
    genai.upload_file("photo3.jpg")
]

# Analyze together
response = model.generate_content([
    "Compare these images and identify common elements",
    *images
])

print(response.text)
```

### Mixed Media Types

```python
# Combine different media types
image = genai.upload_file("chart.png")
pdf = genai.upload_file("report.pdf")

response = model.generate_content([
    "Does the chart match the data in the report?",
    image,
    pdf
])
```

---

## References

**Core Guides**
- [Image Understanding](references/image-understanding.md) - Complete image analysis patterns
- [Video Processing](references/video-processing.md) - Video analysis and frame extraction
- [Audio Processing](references/audio-processing.md) - Audio transcription and analysis
- [Document Processing](references/document-processing.md) - PDF and document extraction

**Optimization**
- [Media Resolution](references/media-resolution.md) - Resolution control and quality tuning
- [OCR Extraction](references/ocr-extraction.md) - Text extraction best practices
- [Token Optimization](references/token-optimization.md) - Cost control and efficiency

**Scripts**
- [Analyze Image Script](scripts/analyze-image.py) - Production-ready image analysis
- [Process Video Script](scripts/process-video.py) - Video processing automation
- [Process Audio Script](scripts/process-audio.py) - Audio transcription
- [Process PDF Script](scripts/process-pdf.py) - PDF extraction

**Official Resources**
- [Vision Capabilities](https://ai.google.dev/gemini-api/docs/vision)
- [Prompting with Media](https://ai.google.dev/gemini-api/docs/prompting_with_media)
- [File API](https://ai.google.dev/gemini-api/docs/file-api)

---

## Related Skills

- **gemini-3-pro-api** - Basic setup, authentication, text generation
- **gemini-3-image-generation** - Image OUTPUT (generating images)
- **gemini-3-advanced** - Function calling, tools, caching, batch processing

---

## Common Use Cases

### Visual Q&A Application

Combine image understanding with chat:

```python
model = genai.GenerativeModel("gemini-3-pro-preview")
chat = model.start_chat()

# Upload image
image = genai.upload_file("product.jpg")

# Ask questions about it
response1 = chat.send_message(["What product is this?", image])
response2 = chat.send_message("What are its main features?")
response3 = chat.send_message("What's the price range for similar products?")
```

### Document Analysis Pipeline

Process multiple PDFs and extract insights:

```python
import google.generativeai as genai
from pathlib import Path

genai.configure(api_key="YOUR_API_KEY")

model = genai.GenerativeModel(
    "gemini-3-pro-preview",
    generation_config={"media_resolution": "medium"}
)

# Process all PDFs in directory
pdf_dir = Path("documents/")
results = {}

for pdf_path in pdf_dir.glob("*.pdf"):
    pdf_file = genai.upload_file(pdf_path)

    # Wait for processing
    while pdf_file.state.name == "PROCESSING":
        time.sleep(5)
        pdf_file = genai.get_file(pdf_file.name)

    # Extract key information
    response = model.generate_content([
        "Extract: 1) Document type, 2) Key dates, 3) Important numbers, 4) Summary",
        pdf_file
    ])

    results[pdf_path.name] = response.text

    # Clean up
    genai.delete_file(pdf_file.name)

# Save results
import json
with open("analysis_results.json", "w") as f:
    json.dump(results, f, indent=2)
```

### Video Content Moderation

Analyze video for specific content:

```python
video = genai.upload_file("user_upload.mp4")

# Wait for processing
while video.state.name == "PROCESSING":
    time.sleep(10)
    video = genai.get_file(video.name)

response = model.generate_content([
    """Analyze this video for:
    1. Inappropriate content (yes/no)
    2. Violence or harmful content (yes/no)
    3. Overall content rating (G/PG/PG-13/R)
    4. Brief justification

    Provide structured response.
    """,
    video
])

print(response.text)
```

---

## Troubleshooting

### Issue: File processing stuck at "PROCESSING"

**Solution:** Large files (especially video) can take time. Wait 30-60 seconds between checks. If stuck > 5 minutes, file may have failed.

### Issue: Low quality OCR results

**Solution:** Use `media_resolution: "high"` for images with text. Ensure image is clear and high resolution.

### Issue: High token costs

**Solution:** Use appropriate media resolution. Start with `low`, increase only if needed. For PDFs, `medium` is usually sufficient.

### Issue: Video analysis missing details

**Solution:** Use `media_resolution: "high"` for better frame analysis, or provide more specific prompts about what to look for.

### Issue: Audio transcription inaccurate

**Solution:** Ensure audio quality is good (no excessive background noise). Provide context in prompt about accent, language, or domain.

---

## Summary

This skill provides comprehensive multimodal input processing capabilities:

✅ Image analysis with OCR and object detection
✅ Video processing up to 1 hour
✅ Audio transcription up to 9.5 hours
✅ Native PDF document processing
✅ Granular media resolution control
✅ Token optimization strategies
✅ Multi-file processing
✅ Production-ready examples

**Ready to analyze multimodal content?** Start with the task that matches your use case above!
