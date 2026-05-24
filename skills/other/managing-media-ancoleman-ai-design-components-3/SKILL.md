---
name: managing-media
description: Implements media and file management components including file upload (drag-drop, multi-file, resumable), image galleries (lightbox, carousel, masonry), video players (custom controls, captions, adaptive streaming), audio players (waveform, playlists), document viewers (PDF, Office), and optimization strategies (compression, responsive images, lazy loading, CDN). Use when handling files, displaying media, or building rich content experiences.
---

# Managing Media & Files

## Purpose

This skill provides systematic patterns for implementing media and file management components across all formats (images, videos, audio, documents). It covers upload workflows, display patterns, player controls, optimization strategies, and accessibility requirements to ensure performant, accessible, and user-friendly media experiences.

## When to Use

Activate this skill when:
- Implementing file upload (single, multiple, drag-and-drop)
- Building image galleries, carousels, or lightboxes
- Creating video or audio players
- Displaying PDF or document viewers
- Optimizing media for performance (responsive images, lazy loading)
- Handling large file uploads (chunked, resumable)
- Integrating cloud storage (S3, Cloudinary)
- Implementing media accessibility (alt text, captions, transcripts)
- Designing empty states for missing media

## Quick Decision Framework

Select implementation based on media type and requirements:

```
Images                  → Gallery pattern + lazy loading + responsive srcset
Videos                  → Player with controls + captions + adaptive streaming
Audio                   → Player with waveform + playlist support
Documents (PDF)         → Viewer with navigation + search + download
File Upload (<10MB)     → Basic drag-drop with preview
File Upload (>10MB)     → Chunked upload with progress + resume
Multiple Files          → Queue management + parallel uploads
```

For detailed selection criteria, reference `references/implementation-guide.md`.

## File Upload Patterns

### Basic Upload (<10MB)

For small files with simple requirements:
- Drag-and-drop zone with visual feedback
- Click to browse fallback
- File type and size validation
- Preview thumbnails for images
- Progress indicator
- Reference `references/upload-patterns.md`

Example: `examples/basic-upload.tsx`

### Advanced Upload (>10MB)

For large files requiring reliability:
- Chunked uploads (resume on failure)
- Parallel uploads for multiple files
- Upload queue management
- Cancel and retry controls
- Client-side compression
- Reference `references/advanced-upload.md`

Example: `examples/chunked-upload.tsx`

### Image-Specific Upload

For image files with editing requirements:
- Crop and rotate tools
- Client-side resize before upload
- Format conversion (PNG → WebP)
- Alt text input field (accessibility)
- Reference `references/image-upload.md`

Example: `examples/image-upload-crop.tsx`

## Image Display Components

### Image Gallery

For collections of images:
- Grid or masonry layout
- Lazy loading (native or custom)
- Lightbox on click
- Zoom and pan controls
- Keyboard navigation (arrow keys)
- Responsive design
- Reference `references/gallery-patterns.md`

Example: `examples/image-gallery.tsx`

### Carousel/Slider

For sequential image display:
- Auto-play (optional, pausable for accessibility)
- Dot or thumbnail navigation
- Touch/swipe support
- ARIA roles for accessibility
- Infinite loop option
- Reference `references/carousel-patterns.md`

Example: `examples/carousel.tsx`

### Image Optimization

Essential optimization strategies:
- Responsive images using `srcset` and `sizes`
- Modern formats (WebP with JPG fallback)
- Progressive JPEGs
- Blur-up placeholders
- CDN integration
- Reference `references/image-optimization.md`

## Video Components

### Video Player

For custom video playback:
- Custom controls or native
- Play/pause, volume, fullscreen
- Captions/subtitles (VTT format)
- Playback speed control
- Picture-in-picture support
- Keyboard shortcuts
- Reference `references/video-player.md`

Example: `examples/video-player.tsx`

### Video Optimization

Performance strategies for video:
- Adaptive streaming (HLS, DASH)
- Thumbnail preview on hover
- Lazy loading off-screen videos
- Preload strategies (`metadata`, `auto`, `none`)
- Multiple quality levels
- Reference `references/video-optimization.md`

## Audio Components

### Audio Player

For audio playback:
- Play/pause, seek, volume controls
- Waveform visualization (optional)
- Playlist support
- Download option
- Playback speed control
- Visual indicators for accessibility
- Reference `references/audio-player.md`

Example: `examples/audio-player.tsx`

## Document Viewers

### PDF Viewer

For PDF document display:
- Page navigation (prev/next, jump to page)
- Zoom in/out controls
- Text search within document
- Download and print options
- Thumbnail sidebar
- Reference `references/pdf-viewer.md`

Example: `examples/pdf-viewer.tsx`

### Office Document Preview

For DOCX, XLSX, PPTX files:
- Read-only preview or editable
- Cloud-based rendering (Google Docs Viewer, Office Online)
- Local rendering (limited support)
- Download option
- Reference `references/office-viewer.md`

## Performance Optimization

### File Size Guidelines

Validate client-side before upload:
- Images: <5MB recommended
- Videos: <100MB for web, larger for cloud
- Audio: <10MB
- Documents: <25MB
- Provide clear error messages
- Suggest compression tools

### Image Optimization Checklist

```bash
# Generate optimized image set
python scripts/optimize_images.py --input image.jpg --formats webp,jpg,avif
```

Strategies:
- Compress before upload (client or server)
- Generate multiple sizes (thumbnails, medium, large)
- Use responsive `srcset` for device targeting
- Convert to modern formats (WebP, AVIF)
- Serve via CDN with edge caching

Reference `references/performance-optimization.md` for complete guide.

### Video Optimization Checklist

Strategies:
- Transcode to multiple qualities (360p, 720p, 1080p)
- Implement adaptive bitrate streaming
- Use CDN with edge caching
- Lazy load videos outside viewport
- Provide poster images

## Accessibility Requirements

### Images

Essential patterns:
- Alt text required for meaningful images
- Empty alt (`alt=""`) for decorative images
- Use `<figure>` and `<figcaption>` for context
- Sufficient color contrast for overlays
- Reference `references/accessibility-images.md`

### Videos

Essential patterns:
- Captions/subtitles for all speech
- Transcript link provided
- Keyboard controls (space, arrows, M for mute)
- Pause auto-play (WCAG requirement)
- Audio description track (if applicable)
- Reference `references/accessibility-video.md`

### Audio

Essential patterns:
- Transcripts available
- Visual indicators (playing, paused, volume)
- Keyboard controls
- ARIA labels for controls
- Reference `references/accessibility-audio.md`

To validate accessibility:
```bash
node scripts/validate_media_accessibility.js
```

For complete requirements, reference `references/accessibility-patterns.md`.

## Library Recommendations

### Image Gallery: react-image-gallery

Best for feature-complete galleries:
- Mobile swipe support
- Fullscreen mode
- Thumbnail navigation
- Lazy loading built-in
- Responsive out of the box

```bash
npm install react-image-gallery
```

See `examples/gallery-react-image.tsx` for implementation.
Reference `/xiaolin/react-image-gallery` for documentation.

**Alternative:** LightGallery (more features, larger bundle)

### Video: video.js

Best for custom video players:
- Plugin ecosystem
- HLS and DASH support
- Accessible controls
- Theming support
- Extensive documentation

```bash
npm install video.js
```

See `examples/video-js-player.tsx` for implementation.

### Audio: wavesurfer.js

Best for waveform visualization:
- Beautiful waveform display
- Timeline interactions
- Plugin support
- Responsive
- Lightweight

```bash
npm install wavesurfer.js
```

See `examples/audio-waveform.tsx` for implementation.

### PDF: react-pdf

Best for PDF rendering in React:
- Page-by-page rendering
- Text selection support
- Annotations (premium)
- Worker-based for performance

```bash
npm install react-pdf
```

See `examples/pdf-react.tsx` for implementation.

For detailed comparison, reference `references/library-comparison.md`.

## Design Token Integration

All media components use the design-tokens skill for theming:
- Color tokens for backgrounds, overlays, controls
- Spacing tokens for padding and gaps
- Border tokens for thumbnails and containers
- Shadow tokens for elevation
- Motion tokens for animations

Supports light, dark, high-contrast, and custom themes.
Reference the design-tokens skill for theme switching.

Example token usage:
```css
.upload-zone {
  border: var(--upload-zone-border);
  background: var(--upload-zone-bg);
  padding: var(--upload-zone-padding);
  border-radius: var(--upload-zone-border-radius);
}

.image-gallery {
  gap: var(--gallery-gap);
}

.video-player {
  background: var(--video-player-bg);
  border-radius: var(--video-border-radius);
}
```

## Responsive Strategies

### Image Galleries

Four responsive approaches:
1. **Grid layout** - CSS Grid with auto-fit columns
2. **Masonry layout** - Pinterest-style with variable heights
3. **Carousel** - Single image on mobile, multiple on desktop
4. **Stack** - Vertical list on mobile, grid on desktop

See `examples/responsive-gallery.tsx` for implementations.

### Video Players

Responsive considerations:
- 16:9 aspect ratio container
- Full-width on mobile
- Constrained width on desktop
- Picture-in-picture for multitasking
- Touch-friendly controls (larger hit areas)

Reference `references/responsive-media.md` for patterns.

## Cloud Storage Integration

### Client-Side Direct Upload

For AWS S3, Cloudinary, etc.:
1. Request signed URL from backend
2. Upload directly to cloud storage
3. Notify backend of completion
4. Display uploaded media

Benefits:
- Reduces server load
- Faster uploads (direct to CDN)
- No file size limits on your server

See `examples/s3-direct-upload.tsx` for implementation.
Reference `references/cloud-storage.md` for setup.

## Testing Tools

Generate mock media:
```bash
# Generate test images
python scripts/generate_mock_images.py --count 50 --sizes thumb,medium,large

# Generate test video metadata
python scripts/generate_video_metadata.py --duration 300
```

Validate media accessibility:
```bash
node scripts/validate_media_accessibility.js
```

Analyze performance:
```bash
node scripts/analyze_media_performance.js --files images/*.jpg
```

## Working Examples

Start with the example matching the requirements:

```
basic-upload.tsx              # Simple drag-drop upload
chunked-upload.tsx            # Large file upload with resume
image-upload-crop.tsx         # Image upload with cropping
image-gallery.tsx             # Grid gallery with lightbox
carousel.tsx                  # Image carousel/slider
video-player.tsx              # Custom video player
audio-player.tsx              # Audio player with controls
audio-waveform.tsx            # Audio with waveform visualization
pdf-viewer.tsx                # PDF document viewer
s3-direct-upload.tsx          # Direct upload to S3
responsive-gallery.tsx        # Responsive image gallery patterns
```

## Resources

### Scripts (Token-Free Execution)
- `scripts/optimize_images.py` - Batch image optimization
- `scripts/generate_mock_images.py` - Test image generation
- `scripts/validate_media_accessibility.js` - Accessibility validation
- `scripts/analyze_media_performance.js` - Performance analysis

### References (Detailed Documentation)
- `references/upload-patterns.md` - File upload implementations
- `references/gallery-patterns.md` - Image gallery designs
- `references/video-player.md` - Video player features
- `references/audio-player.md` - Audio player patterns
- `references/pdf-viewer.md` - Document viewer setup
- `references/accessibility-patterns.md` - Media accessibility
- `references/performance-optimization.md` - Optimization strategies
- `references/cloud-storage.md` - Cloud integration guides
- `references/library-comparison.md` - Library analysis

### Examples (Implementation Code)
- See `examples/` directory for working implementations

### Assets (Templates and Configs)
- `assets/upload-config.json` - Upload constraints and settings
- `assets/media-templates/` - Placeholder images and icons

## Cross-Skill Integration

This skill works with other component skills:

- **Forms**: File input fields, validation, submission
- **Feedback**: Upload progress, success/error messages
- **AI Chat**: Image attachments, file sharing
- **Dashboards**: Media widgets, thumbnails
- **Design Tokens**: All visual styling via token system

## Next Steps

1. Identify the media type (images, video, audio, documents)
2. Determine upload requirements (size, quantity, editing)
3. Choose display pattern (gallery, carousel, player, viewer)
4. Select library or implement custom solution
5. Implement accessibility requirements
6. Apply optimization strategies
7. Test performance and responsive behavior
8. Integrate with cloud storage (optional)
