---
name: gemini-files
description: Upload and manage files using Google Gemini File API via scripts/. Use for uploading images, audio, video, PDFs, and other files for use with Gemini models. Supports file upload, status checking, and file management. Triggers on "upload file", "file API", "upload image", "upload PDF", "upload video", "file management".
license: MIT
version: 1.0.0
keywords: file upload, image upload, video upload, PDF upload, audio upload, file API, multimodal, document processing
---

# Gemini File API

Upload and manage files for use with Gemini models through executable scripts, supporting images, audio, video, PDFs, and other file types.

## When to Use This Skill

Use this skill when you need to:
- Upload images for multimodal analysis
- Upload videos for content processing
- Upload PDFs for document analysis
- Upload audio for transcription or processing
- Pre-upload files for batch operations
- Check file processing status
- List and manage uploaded files
- Use files with other Gemini skills (text, image, etc.)

## Available Scripts

### scripts/upload.py
**Purpose**: Upload files to Gemini File API

**When to use**:
- Uploading any file for Gemini processing
- Preparing files for multimodal generation
- Uploading documents for analysis
- Batch file preparation

**Key parameters**:
| Parameter | Description | Example |
|-----------|-------------|---------|
| `path` | File path (required) | `image.jpg` |
| `--name`, `-n` | Display name | `"my-document"` |
| `--wait`, `-w` | Wait for processing | Flag |

**Output**: File name, URI, and status information

## Workflows

### Workflow 1: Basic File Upload
```bash
python scripts/upload.py image.jpg
```
- Best for: Quick uploads, simple files
- Output: File name and URI for API use
- State: PROCESSING or ACTIVE

### Workflow 2: Upload with Custom Name
```bash
python scripts/upload.py document.pdf --name "Quarterly Report Q4 2026"
```
- Best for: Organizing files, tracking uploads
- Use when: Original filename not descriptive enough
- Display name appears in file listings

### Workflow 3: Upload and Wait for Processing
```bash
python scripts/upload.py video.mp4 --wait
```
- Best for: Large files, videos, audio
- Waits for file to be ACTIVE state
- Use when: You need to use file immediately after upload

### Workflow 4: Upload Image for Analysis
```bash
# 1. Upload image
python scripts/upload.py photo.png --name "product-shot"

# 2. Use with gemini-text for analysis
python skills/gemini-text/scripts/generate.py "Describe this image" --image photo.png
```
- Best for: Image analysis, captioning, visual Q&A
- Combines with: gemini-text for multimodal processing

### Workflow 5: Upload PDF for Content Extraction
```bash
# 1. Upload PDF
python scripts/upload.py research-paper.pdf --name "AI-Research-Paper" --wait

# 2. Extract content with gemini-text
python skills/gemini-text/scripts/generate.py "Extract key findings from this document" --image research-paper.pdf
```
- Best for: Document processing, content extraction
- Combines with: gemini-text for analysis

### Workflow 6: Upload Multiple Files for Batch
```bash
# 1. Upload multiple files
for file in *.jpg; do
    python scripts/upload.py "$file"
done

# 2. Create batch job using uploaded files (gemini-batch skill)
```
- Best for: Preparing files for batch processing
- Combines with: gemini-batch for bulk operations

### Workflow 7: Upload Audio for Transcription
```bash
# 1. Upload audio
python scripts/upload.py interview.mp3 --name "interview-001" --wait

# 2. Process with gemini-text (if transcription available)
python skills/gemini-text/scripts/generate.py "Transcribe and summarize this audio" --image interview.mp3
```
- Best for: Audio processing, transcription, podcast analysis
- Combines with: gemini-text for audio analysis

### Workflow 8: Upload Video for Content Analysis
```bash
# 1. Upload video (may take time)
python scripts/upload.py product-demo.mp4 --name "demo-video" --wait

# 2. Analyze with gemini-text
python skills/gemini-text/scripts/generate.py "Analyze this product demo video" --image product-demo.mp4
```
- Best for: Video analysis, content summarization
- Note: Videos may require significant processing time

## Parameters Reference

### Supported File Types

| Type | Extensions | Max Size | Processing Time |
|------|------------|----------|-----------------|
| Images | jpg, jpeg, png, gif, webp | 20MB | Seconds |
| Audio | mp3, wav, aac, flac | 25MB | Seconds-minutes |
| Video | mp4, mov, avi, webm | 2GB | Minutes-hours |
| Documents | pdf, txt | 50MB | Seconds-minutes |

### MIME Types

Script auto-detects based on extension:
- Images: image/jpeg, image/png, image/gif, image/webp
- Audio: audio/mpeg, audio/wav
- Video: video/mp4, video/quicktime, video/webm
- Documents: application/pdf, text/plain

### File States

| State | Description | Ready for Use |
|-------|-------------|-----------------|
| `PROCESSING` | File is being analyzed | No |
| `ACTIVE` | File is ready | Yes |
| `FAILED` | Processing failed | No |

## Output Interpretation

### Upload Response
```
Uploading photo.png...
Uploaded: files/abc123...
URI: gs://generation-tmp/abc123...
State: PROCESSING
```
- File name: Use in API calls
- URI: Internal Google Cloud Storage reference
- State: PROCESSING = wait, ACTIVE = ready

### With --wait Flag
```
Uploading video.mp4...
Uploaded: files/xyz789...
URI: gs://generation-tmp/xyz789...
State: PROCESSING
Waiting for processing...
Still processing...
File ready!
```
- Script polls until state is ACTIVE
- Use for large files requiring processing
- May take minutes for videos

### Using Uploaded Files
Once uploaded, reference file by name:
```bash
# With gemini-text
python skills/gemini-text/scripts/generate.py "Analyze" --image <uploaded-file-path>
```

## Common Issues

### "google-genai not installed"
```bash
pip install google-genai
```

### "File not found"
- Verify file path is correct
- Use absolute paths if relative paths fail
- Check file extension matches supported types

### "File too large"
- Check size limits for file type
- Compress images/videos if possible
- Split large files into smaller parts

### "Unsupported file type"
- Check supported extensions
- Convert to supported format if possible
- Images: jpg, png, gif, webp
- Videos: mp4, mov, avi, webm

### "Processing failed"
- Check file is not corrupted
- Try re-uploading the file
- Verify file format is valid
- Check API quota limits

### "File still processing" (without --wait)
- File state is PROCESSING, not ACTIVE
- Use `--wait` flag or check status later
- Large files (especially videos) take time
- Processing can take minutes to hours

## Best Practices

### Upload Strategy
- Use `--wait` for files you'll use immediately
- Skip `--wait` for batch uploads to save time
- Use descriptive `--name` for organization
- Keep track of file names for later use

### File Organization
- Use consistent naming conventions
- Include dates or versions in names
- Group related files together
- Document file names in your code

### Performance Tips
- Upload multiple files in parallel (separate processes)
- Pre-upload files for batch operations
- Check file state before using in API calls
- Delete old files to manage storage

### Error Handling
- Check return state after upload
- Retry failed uploads
- Verify file integrity before upload
- Log file names for audit trails

### Integration with Other Skills
- **gemini-text**: Multimodal analysis, document processing
- **gemini-image**: Generate images based on uploaded reference
- **gemini-batch**: Use uploaded files in batch jobs
- **gemini-embeddings**: Create embeddings from file content

### File Lifecycle
- Upload → PROCESSING → ACTIVE → Use in API
- Delete old files to free storage
- Files may expire after certain period
- Download important files for backup

## Related Skills

- **gemini-text**: Analyze uploaded files with text generation
- **gemini-image**: Create images based on uploaded references
- **gemini-batch**: Use uploaded files in batch processing
- **gemini-embeddings**: Generate embeddings from file content

## Quick Reference

```bash
# Basic upload
python scripts/upload.py image.jpg

# With custom name
python scripts/upload.py document.pdf --name "My Document"

# Wait for processing
python scripts/upload.py video.mp4 --wait

# Multiple files
for file in *.jpg; do python scripts/upload.py "$file"; done
```

## File Management API

While not in scripts, you can also manage files via Python:

```python
from google import genai

client = genai.Client()

# List all files
for file in client.files.list():
    print(f"{file.name}: {file.display_name} ({file.state})")

# Get file info
file = client.files.get(name="files/abc123...")
print(f"State: {file.state}")

# Delete file
client.files.delete(name="files/abc123...")
```

## Reference

- Get API key: https://aistudio.google.com/apikey
- Documentation: https://ai.google.dev/gemini-api/docs/file-upload
- File API: https://ai.google.dev/gemini-api/docs/files
- Supported formats: Images, audio, video, documents (see table above)
