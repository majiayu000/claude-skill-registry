---
name: wordpress-ai-image-optimizer
description: AI-powered image optimization that downloads images from WordPress, processes locally (compress, WebP conversion, resize, rename), uploads optimized versions, and updates all content references. Handles hundreds of images automatically in AI code editor. Use when user says "optimize my wordpress images with ai", "run ai image optimization", "compress and optimize all images", or "improve image performance".
license: MIT
metadata:
  author: Respira for WordPress
  author_url: https://respira.press
  version: 1.0.0
  mcp-server: respira-wordpress
  category: performance
---

# WordPress AI Image Optimizer

AI-powered image optimization for WordPress sites. Downloads images, processes locally in AI code editor (compression, format conversion, resizing, renaming), uploads optimized versions, and updates all content references automatically.

## What This Skill Does

**Scans:**
- All media library images
- Images in posts and pages content
- Featured images
- Images in page builder elements (Elementor, Divi, Bricks, etc.)
- WooCommerce product images

**Detects:**
- File sizes (actual KB/MB on disk)
- Image dimensions (width x height in pixels)
- Format (JPG, PNG, GIF, WebP, AVIF, SVG)
- Whether alt text exists (and quality)
- Whether responsive image sizes exist (srcset)
- Non-SEO-friendly filenames (IMG_1234.jpg, screenshot.png)
- Oversized originals (5000px uploaded when 2000px is max needed)

**Optimizes via AI Code Editor:**
- Downloads images from WordPress
- Compresses with optimal quality (80-85% for JPG)
- Converts to modern formats (WebP preferred)
- Resizes oversized originals to optimal dimensions
- Renames with SEO-friendly descriptive filenames
- Generates missing alt text using AI
- Regenerates WordPress responsive image sizes
- Uploads optimized versions back to WordPress
- Creates new media entries (keeps old files safe)
- Updates all content references in duplicates

## Requirements

- Respira for WordPress plugin installed
- MCP connection active
- AI code editor with image processing tools (Claude Code, Cursor, etc.)
- ImageMagick, Sharp, or Pillow available in container
- WooCommerce add-on (optional - for product images)

## How to Use

### Trigger Phrases
- "optimize my wordpress images with ai"
- "run ai image optimization"
- "compress and optimize all images"
- "audit my media library"
- "improve image performance"

### Workflow

**Phase 1: Comprehensive Image Audit**
1. Scans all images across site
2. Analyzes file size, format, dimensions, alt text, usage
3. Detects optimization plugins/CDN
4. Scores opportunities by impact (file size x page traffic)
5. Generates comprehensive report

**Phase 2: User Approval**
Asks which optimizations to run:
- "Optimize everything" (all images)
- "Critical images only" (top 20 highest impact)
- "Homepage images first" (critical pages)
- "Product images only" (WooCommerce products)

**Phase 3: AI Processing**
7. AI downloads images from WordPress
8. Processes locally:
   - Compression (ImageMagick/Sharp/Pillow)
   - Format conversion (JPG/PNG -> WebP)
   - Resizing (oversized -> optimal dimensions)
   - Renaming (SEO-friendly filenames)
   - Alt text generation (AI-powered)
9. Uploads optimized versions as new media entries
10. Updates content references in duplicates
11. Regenerates responsive image sizes

**Phase 4: Review & Publish**
12. Provides before/after comparison
13. User reviews duplicates
14. Approves to publish
15. Old files remain for safety

For detailed workflow and processing details, see `references/processing-workflow.md`

## Key Difference from Plugins

Unlike plugins that optimize on upload or via queue, this skill:
- Retroactively optimizes everything in one batch
- AI code editor processes locally (full control, no API limits)
- Creates new optimized files, keeps originals for safety
- Updates all content references automatically
- Generates AI-powered SEO-friendly filenames and alt text

## Safety Model (Option B)

- **Non-destructive:** Creates NEW optimized images, keeps old files
- **Duplicate-first:** Updates content in duplicates, never live pages
- **User approval required:** Review before publishing any changes
- **Rollback ready:** Old files preserved, can revert all changes
- **No live site impact:** Nothing changes until you explicitly approve

## Honest Disclaimer

**What this skill CANNOT do:**
- Guarantee perfect quality (compression is lossy, review recommended)
- Fix broken or corrupted images
- Optimize CSS background images (only content images)
- Process images on external CDNs

**What this skill CAN do:**
- Process hundreds of images in minutes
- Compress without visible quality loss (80-85% quality)
- Convert to modern formats (WebP, 25-35% smaller)
- Rename with SEO-friendly names
- Generate AI alt text
- Update all references automatically
- Preserve originals for safety

## Technical Details

**Processing tools in AI code editor container:**
- ImageMagick: `convert input.jpg -resize 2000x -quality 80 output.webp`
- Sharp (Node.js): `sharp('input.jpg').resize(2000).webp({quality:80})`
- Pillow (Python): `img.thumbnail((2000,2000)); img.save('out.webp')`

**Respira MCP tools used:**
- `wordpress_list_media` - get all media library images
- `wordpress_get_media` - download image file
- `wordpress_upload_media` - upload processed image
- `wordpress_update_media` - update metadata
- `wordpress_list_pages` / `wordpress_list_posts` - find usage
- `wordpress_create_duplicate` - duplicate pages/posts
- `wordpress_update_page` / `wordpress_update_post` - update references

For complete processing workflow and format selection logic, see `references/processing-workflow.md`

## Plugin & CDN Detection

Detects and integrates with:
- Smush, ShortPixel, EWWW, Imagify, Optimole
- Cloudflare, BunnyCDN auto-optimization

Provides plugin-specific recommendations and can work alongside plugins for future uploads.

## Related Skills

- SEO & AEO Amplifier - on-page SEO and schema optimization
- WordPress Site DNA - comprehensive site analysis
- Mobile Experience Report - mobile performance

---

Built by Respira for WordPress
https://respira.press
