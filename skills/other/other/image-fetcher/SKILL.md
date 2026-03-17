---
name: image-fetcher
description: Fetch and download images from the internet in various formats (JPG, PNG, GIF, WebP, BMP, SVG, etc.). Use when users ask to download images, fetch images from URLs, save images from the web, or get images for embedding in documents or chats. Supports single and batch downloads with automatic format detection.
---

# Image Fetcher Skill

This skill enables Claude to fetch and download images from the internet with support for multiple image formats and batch downloading capabilities.

## When to Use This Skill

Use this skill when the user requests:
- Downloading images from specific URLs
- Fetching images from the web to embed in documents
- Saving images locally from internet sources
- Batch downloading multiple images
- Converting or processing images that need to be downloaded first

## Supported Image Formats

The skill automatically detects and handles these formats:
- JPG/JPEG
- PNG
- GIF
- WebP
- BMP
- SVG
- ICO
- TIFF/TIF

## Core Workflows

### Single Image Download

To download a single image from a URL:

```bash
python scripts/fetch_image.py <image_url> [output_directory] [filename]
```

**Parameters:**
- `image_url` (required): URL of the image to download
- `output_directory` (optional): Directory to save the image (defaults to current directory)
- `filename` (optional): Custom filename for the saved image (defaults to URL filename)

**Examples:**
```bash
# Basic download to current directory
python scripts/fetch_image.py https://example.com/photo.jpg

# Download to specific directory
python scripts/fetch_image.py https://example.com/photo.jpg ./downloads

# Download with custom filename
python scripts/fetch_image.py https://example.com/photo.jpg ./downloads myimage.jpg
```

### Batch Image Download

To download multiple images from a list of URLs:

```bash
python scripts/fetch_images_batch.py <urls_file> [output_directory]
```

**Input file formats:**
1. Text file with one URL per line
2. JSON file with array of URLs: `["url1", "url2", ...]`

**Examples:**
```bash
# Download from text file
python scripts/fetch_images_batch.py urls.txt

# Download to specific directory
python scripts/fetch_images_batch.py urls.json ./images

# Create a URL list on the fly
echo -e "https://example.com/img1.jpg\nhttps://example.com/img2.png" > urls.txt
python scripts/fetch_images_batch.py urls.txt ./downloads
```

The batch script creates a `fetch_results.json` file with detailed results for each download.

## Integration with Claude Workflow

### For Document Embedding

When fetching images to embed in documents (DOCX, PPTX, etc.):

1. Download the image to a temporary location
2. Use the returned file path to embed the image in the document
3. Clean up temporary files if needed

```bash
# Download image
python scripts/fetch_image.py https://example.com/chart.png /home/claude/temp

# The script outputs the full path which can be used for embedding
# Example output: /home/claude/temp/chart.png
```

### For Chat Display

When downloading images to display in chat:

1. Download to `/mnt/user-data/outputs/` directory
2. Provide the user with a link to the downloaded image

```bash
python scripts/fetch_image.py https://example.com/image.jpg /mnt/user-data/outputs
```

### Search Integration

When combined with web search:

1. Search for images using web_search tool
2. Extract image URLs from search results
3. Use this skill to download the images

## Error Handling

The scripts handle common scenarios:
- Invalid URLs
- Network timeouts
- Unsupported formats
- Permission errors
- Missing directories (auto-created)

Failed downloads are reported with clear error messages.

## Output Information

Each successful download provides:
- Full path to saved file
- File size in KB
- Content-Type from server
- Success confirmation

## Best Practices

1. **Always validate URLs** before attempting download
2. **Use batch downloading** for multiple images to improve efficiency
3. **Specify output directory** to organize downloads properly
4. **Check file extensions** - the script auto-detects format from headers if URL lacks extension
5. **Handle errors gracefully** - inform users of any failed downloads

## Common Use Cases

**Use Case 1: Embedding web images in presentations**
```bash
# User: "Add this chart to my presentation: https://data.com/chart.png"
python scripts/fetch_image.py https://data.com/chart.png /home/claude/temp
# Then use the path to embed in PPTX
```

**Use Case 2: Creating image gallery from URLs**
```bash
# User: "Download these product images and save them"
# Create urls.txt with image URLs
python scripts/fetch_images_batch.py urls.txt /mnt/user-data/outputs/gallery
```

**Use Case 3: Logo download for branding**
```bash
# User: "Get the company logo from their website"
python scripts/fetch_image.py https://company.com/logo.svg /home/claude/assets logo.svg
```

## Technical Notes

- Uses `requests` library with appropriate headers to avoid being blocked
- Streams large files to handle memory efficiently
- 30-second timeout for each download
- Automatic content-type detection and extension mapping
- Creates output directories automatically if they don't exist
