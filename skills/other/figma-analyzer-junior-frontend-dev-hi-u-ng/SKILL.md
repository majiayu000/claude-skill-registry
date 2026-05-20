---
name: figma-analyzer
description: Extract design assets and metadata from Figma using the Figma REST API.
  Supports exporting frames/components as images, extracting node metadata, design
  tokens, and file structure. Use with ai-multimodal skill for comprehensive UI research.
license: MIT
allowed-tools:
  - Bash
  - Read
  - Write
---

# Figma Analyzer Skill

Extract design assets, metadata, and specifications from Figma files using the Figma REST API.

## Core Capabilities

### Asset Export
- Export frames/components as PNG, JPG, SVG, PDF
- Configurable scale (1x, 2x, 3x, 4x)
- Batch export multiple nodes
- Download images to local filesystem

### Metadata Extraction
- File structure and page hierarchy
- Node properties (size, position, constraints)
- Component and style definitions
- Version history

### Design Token Extraction
- Color styles and palettes
- Typography styles
- Effect styles (shadows, blurs)
- Grid and layout styles

## Prerequisites

### API Key Setup

Obtain a Figma Personal Access Token:
1. Go to Figma Settings > Account
2. Scroll to "Personal access tokens"
3. Generate a new token with read permissions

The skill checks for `FIGMA_ACCESS_TOKEN` in this order:
1. Process environment: `export FIGMA_ACCESS_TOKEN="your-token"`
2. Project root: `.env`
3. `.claude/.env`
4. `.claude/skills/.env`
5. `.claude/skills/figma-analyzer/.env`

### Install Dependencies

```bash
pip install requests python-dotenv
```

## Figma URL Parsing

Figma URLs contain the file key and optional node ID:

```
https://www.figma.com/file/{file_key}/{file_name}?node-id={node_id}
https://www.figma.com/design/{file_key}/{file_name}?node-id={node_id}
```

Examples:
- Full file: `https://www.figma.com/file/ABC123/MyDesign`
- Specific frame: `https://www.figma.com/file/ABC123/MyDesign?node-id=1-234`

## Quick Start

### Export Design as Image

```bash
python scripts/figma_export.py \
  --url "https://www.figma.com/file/ABC123/Design?node-id=1-234" \
  --output docs/research/ui/design.png \
  --scale 2
```

### Get File Metadata

```bash
python scripts/figma_export.py \
  --url "https://www.figma.com/file/ABC123/Design" \
  --metadata-only \
  --output docs/research/ui/figma-metadata.json
```

### Extract Design Tokens

```bash
python scripts/figma_export.py \
  --url "https://www.figma.com/file/ABC123/Design" \
  --extract-tokens \
  --output docs/research/ui/design-tokens.json
```

### Batch Export Multiple Frames

```bash
python scripts/figma_export.py \
  --url "https://www.figma.com/file/ABC123/Design" \
  --node-ids "1-234,1-235,1-236" \
  --output docs/research/ui/frames/ \
  --scale 2
```

## API Reference

### Endpoints Used

| Endpoint | Purpose |
|----------|---------|
| GET /v1/files/:key | Get file metadata and structure |
| GET /v1/files/:key/nodes | Get specific node data |
| GET /v1/images/:key | Export nodes as images |
| GET /v1/files/:key/styles | Get published styles |
| GET /v1/files/:key/components | Get published components |

### Rate Limits

- **Free tier**: 300 requests/minute
- **Paid tier**: Higher limits based on plan
- Implement exponential backoff for retries

## Output Formats

### Metadata JSON Structure

```json
{
  "file_key": "ABC123",
  "name": "My Design",
  "last_modified": "2024-01-15T10:30:00Z",
  "thumbnail_url": "https://...",
  "nodes": {
    "1-234": {
      "name": "Hero Section",
      "type": "FRAME",
      "absoluteBoundingBox": {
        "x": 0, "y": 0,
        "width": 1440, "height": 800
      },
      "children": [...]
    }
  }
}
```

### Design Tokens JSON Structure

```json
{
  "colors": {
    "primary": {"value": "#3B82F6", "name": "Blue 500"},
    "secondary": {"value": "#10B981", "name": "Green 500"}
  },
  "typography": {
    "heading-1": {
      "fontFamily": "Inter",
      "fontSize": 48,
      "fontWeight": 700,
      "lineHeight": 1.2
    }
  },
  "effects": {
    "shadow-md": {
      "type": "DROP_SHADOW",
      "offset": {"x": 0, "y": 4},
      "radius": 6,
      "color": "rgba(0,0,0,0.1)"
    }
  },
  "spacing": {
    "xs": 4, "sm": 8, "md": 16, "lg": 24, "xl": 32
  }
}
```

## Integration with ai-multimodal

After exporting images, use ai-multimodal for visual analysis:

```bash
# Step 1: Export from Figma
python .claude/skills/figma-analyzer/scripts/figma_export.py \
  --url "$FIGMA_URL" \
  --output docs/research/ui/design.png \
  --scale 2

# Step 2: Analyze with Gemini Vision
python .claude/skills/ai-multimodal/scripts/gemini_batch_process.py \
  --files docs/research/ui/design.png \
  --task analyze \
  --prompt "Analyze layout and extract component specifications" \
  --output docs/research/ui/analysis.md \
  --model gemini-2.5-flash
```

## Error Handling

| Error Code | Meaning | Resolution |
|------------|---------|------------|
| 400 | Bad request | Check URL format and node IDs |
| 403 | Forbidden | Verify access token and file permissions |
| 404 | Not found | Check file key and node ID exist |
| 429 | Rate limited | Implement backoff, wait and retry |
| 500 | Server error | Retry with exponential backoff |

## Best Practices

### Image Export
1. Use 2x scale for high-quality analysis
2. Export specific frames, not entire files
3. Use PNG for UI elements with transparency
4. Use JPG for photo-heavy designs

### Token Extraction
1. Ensure styles are published in Figma
2. Use consistent naming conventions
3. Export both local and published styles
4. Map tokens to CSS custom properties

### Performance
1. Cache metadata to reduce API calls
2. Batch export multiple nodes at once
3. Use node-id filtering for large files
4. Implement request throttling

## Workflow Integration

This skill is designed to work with:
- **ui-researcher agent**: Primary consumer for UI research workflows
- **ai-multimodal skill**: For visual analysis of exported images
- **/ui-research command**: Orchestrates the full research workflow

## Scripts Overview

### figma_export.py

Main script for Figma API interaction:

```bash
python scripts/figma_export.py --help

Options:
  --url          Figma file or frame URL (required)
  --output       Output path for images/data
  --scale        Export scale (1, 2, 3, 4)
  --format       Export format (png, jpg, svg, pdf)
  --node-ids     Comma-separated node IDs to export
  --metadata-only  Only fetch metadata, no image export
  --extract-tokens Extract design tokens
  --verbose      Enable verbose output
```

## Resources

- [Figma REST API Documentation](https://www.figma.com/developers/api)
- [Figma Access Tokens](https://www.figma.com/developers/api#access-tokens)
- [Figma Node Types](https://www.figma.com/developers/api#node-types)
