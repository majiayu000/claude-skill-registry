# WordPress AI Image Optimizer - Processing Workflow

## Detailed Processing Steps

1. Download originals from media library
2. Analyze dimensions, format, and usage context
3. Resize oversized files
4. Convert to WebP when beneficial
5. Apply tuned compression
6. Generate SEO-friendly filename and alt text
7. Upload optimized file as new media item
8. Update references in duplicates
9. Preserve old files as rollback fallback

## Format Selection Logic

- Prefer WebP for most photo/content images
- Keep SVG untouched
- Preserve animated GIF where needed
- Keep original when conversion gives no practical gain

## Filename Generation

Pattern: `[context]-[subject]-[descriptor].[format]`

Examples:
- `IMG_1234.jpg` -> `homepage-marketing-team-hero.webp`
- `screenshot.png` -> `dashboard-features-screenshot.webp`

## Alt Text Generation

- Uses image context + surrounding page content
- Keeps descriptions concise and descriptive
- Avoids redundant prefixes like "image of"
