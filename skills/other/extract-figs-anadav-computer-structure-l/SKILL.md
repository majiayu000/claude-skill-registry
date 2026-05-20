---
name: extract-figs
description: Extract images from talk.pptx PowerPoint file to images_out/ directory.
allowed-tools: Bash
---

# Extract Figures from PowerPoint Tool

Use `tools/extract_figs.py` to extract all images from the PowerPoint presentation.

## Usage

```bash
python tools/extract_figs.py
```

## Output

Images are extracted to: `images_out/ppt/media/`

## Notes

- Extracts from `talk.pptx` in the current directory
- Creates `images_out/` directory if it doesn't exist
- Extracts all media files from the PowerPoint's internal structure
