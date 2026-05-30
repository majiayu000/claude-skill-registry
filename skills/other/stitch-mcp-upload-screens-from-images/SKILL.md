---
name: stitch-mcp-upload-screens-from-images
description: Uploads screenshots or mockup images into a Stitch project as new screens. Enables the "redesign from screenshot" workflow — import existing UI and then edit or convert.
allowed-tools:
  - "stitch*:*"
  - "Bash"
  - "Read"
---

# Stitch MCP — Upload Screens from Images

Uploads one or more images (screenshots, mockups, wireframes) into a Stitch project as new screens. This is the entry point for the "redesign existing UI" workflow — import what you have, then use `edit_screens` to iterate or convert directly to code.

## Critical prerequisite

**Only use this skill when the user explicitly mentions "Stitch".**

You must have a `projectId` before calling this. If you don't have one:
- Create a new project via `stitch-mcp-create-project`
- Or find an existing project via `stitch-mcp-list-projects`

## When to use

- User provides a screenshot and wants to redesign it in Stitch
- User wants to import existing mockups into Stitch for editing
- The orchestrator classifies intent as "Upload screenshot"
- User says "import this design", "upload this image", or "redesign this screen"

## Step 1: Encode the image to base64

Use the helper script to convert a local image file to base64:

```bash
bash scripts/encode-image.sh "path/to/screenshot.png"
```

The script outputs raw base64 to stdout. Capture it for the API call.

Supported formats and their MIME types:
| Extension | MIME type |
|-----------|----------|
| `.png` | `image/png` |
| `.jpg`, `.jpeg` | `image/jpeg` |
| `.webp` | `image/webp` |
| `.gif` | `image/gif` |

## Step 2: Call the MCP tool

```json
{
  "name": "upload_screens_from_images",
  "arguments": {
    "projectId": "3780309359108792857",
    "images": [
      {
        "fileContentBase64": "[base64-encoded-image-data]",
        "mimeType": "image/png"
      }
    ]
  }
}
```

### `projectId` — numeric ID only, no prefix

```
✅ "3780309359108792857"
❌ "projects/3780309359108792857"
```

### `images` — array of image objects

Each image needs:
| Field | Type | Description |
|-------|------|-------------|
| `fileContentBase64` | string | Base64-encoded image data (no `data:` prefix) |
| `mimeType` | string | MIME type matching the image format |

You can upload multiple images in a single call — each becomes a separate screen.

## Output

Returns session info similar to `generate_screen_from_text`. The uploaded images appear as new screens in the project.

## After uploading

1. Call `stitch-mcp-list-screens` to find the new screen IDs
2. Offer the user:
   - "Edit this screen (change colors, layout, content)?" → `stitch-mcp-edit-screens`
   - "Convert directly to code?" → `stitch-mcp-get-screen` → framework conversion
   - "Generate variants based on this design?" → `stitch-mcp-generate-variants`

## References

- `scripts/encode-image.sh` — Base64 encoding helper
