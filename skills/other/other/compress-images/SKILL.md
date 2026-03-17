---
name: compress-images
description: Compress images for web/SEO performance using cwebp. Use when optimizing images for faster page loads, reducing file sizes, or converting JPG/PNG to WebP format.
argument-hint: "[directory]"
allowed-tools: Bash(cwebp:*), Bash(ls:*), Bash(mkdir:*), Bash(mv:*)
---

# Image Compression Skill

Compress all images in `$ARGUMENTS` (or `app/assets/images/content/` if no path provided) to WebP format, optimized for SEO performance (target: under 100KB per image).

## Process

1. **Create originals folder** - Create `originals/` subfolder inside the target directory and move source files there. Never destroy source files.
2. **Compress each image** (JPG, PNG, GIF) from `originals/` to the parent directory as `.webp`
3. **Iterate until all images are under 100KB** - check sizes after each pass, re-compress any that exceed the target
4. **Report results** with before/after sizes
5. **Update references** in content files from old extensions to `.webp`

## File Structure

```
target-directory/
├── originals/           # High-quality source files preserved here
│   ├── hero.jpg
│   └── feature.png
├── hero.webp            # Compressed, web-optimized
└── feature.webp
```

## Iterative Compression Algorithm

**IMPORTANT:** Keep compressing until ALL images are under 100KB. Check sizes after each pass and re-compress any that exceed the target.

### Step 1: Initial pass (q 70)
```bash
cwebp -q 70 -resize 1200 0 originals/image.jpg -o image.webp
ls -lh image.webp  # Check size
```

### Step 2: If still over 100KB, reduce quality progressively
```bash
# Try these in order until under 100KB:
cwebp -q 60 -resize 1200 0 originals/image.jpg -o image.webp
cwebp -q 50 -resize 1200 0 originals/image.jpg -o image.webp
cwebp -q 45 -resize 1200 0 originals/image.jpg -o image.webp
cwebp -q 40 -resize 1200 0 originals/image.jpg -o image.webp
cwebp -q 35 -resize 1200 0 originals/image.jpg -o image.webp
```

### Step 3: For stubborn images, also reduce dimensions
```bash
# If q 35 at 1200px is still over 100KB, reduce to 1000px:
cwebp -q 30 -resize 1000 0 originals/image.jpg -o image.webp
cwebp -q 25 -resize 1000 0 originals/image.jpg -o image.webp
```

## Real-World Results (Reference)

From actual compression run on content images:

| Image | Original | First Try | Final | Settings Used |
|-------|----------|-----------|-------|---------------|
| waves.jpg | 198KB | 33KB | 33KB | q 70, 1200px (1 pass) |
| calendar.jpg | 246KB | 42KB | 42KB | q 70, 1200px (1 pass) |
| floating.jpg | 230KB | 43KB | 43KB | q 70, 1200px (1 pass) |
| cash.jpg | 409KB | 88KB | 88KB | q 70, 1200px (1 pass) |
| knot.jpg | 395KB | 96KB | 96KB | q 70, 1200px (1 pass) |
| floating-dark.jpg | 414KB | 94KB | 94KB | q 70, 1200px (1 pass) |
| keyboard2.jpg | 459KB | 102KB | 102KB | q 70, 1200px (1 pass, acceptable) |
| **perpetual.jpg** | 565KB | 130KB | **96KB** | q 40, 1200px (3 passes) |
| **keyboard.jpg** | 718KB | 196KB | **98KB** | q 25, 1000px (5 passes) |

### Key Insights

1. **Most images** (under 500KB source) compress fine with default settings (q 70, 1200px)
2. **Large detailed images** (500KB+) often need multiple passes
3. **Very large images** (700KB+) may need both lower quality AND smaller dimensions
4. **Keyboard/tech photos** with fine detail are hardest to compress - expect 4-5 passes
5. **Soft/blurry images** compress much better than sharp detailed ones

## After Compression

1. **Verify ALL files under 100KB**: `ls -lh *.webp` - re-run compression on any exceeding target
2. Update content files referencing old extensions (.jpg, .png) to use .webp
3. Test that images render correctly in the application
4. Original files remain in `originals/` folder for future reference or re-compression
