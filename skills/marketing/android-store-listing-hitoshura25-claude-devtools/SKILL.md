---
name: android-store-listing
description: Create feature graphic and complete store listing metadata
category: android
version: 1.0.0
inputs:
  - app_name: App name
  - tagline: Short tagline for feature graphic
  - primary_color: Primary brand color (hex, optional)
  - description: Full app description (optional)
outputs:
  - fastlane/metadata/android/en-US/images/featureGraphic.png
  - docs/STORE_LISTING_GUIDE.md
  - fastlane/metadata/android/en-US/*.txt (metadata templates)
verify: "test -f fastlane/metadata/android/en-US/images/featureGraphic.png && file fastlane/metadata/android/en-US/images/featureGraphic.png | grep '1024 x 500'"
---

# Android Store Listing

Create feature graphic and complete store listing metadata for Google Play Store.

## Prerequisites

- `/devtools:android-fastlane-setup` completed
- `/devtools:android-app-icon` completed (for icon assets)

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| app_name | Yes | - | App name |
| tagline | Yes | - | Short tagline for feature graphic |
| primary_color | No | #6200EE | Primary brand color (hex) |
| description | No | Template | Full app description |

## Play Store Asset Requirements

| Asset | Dimensions | Format | Required |
|-------|------------|--------|----------|
| App Icon | 512 x 512 px | PNG | Yes |
| Feature Graphic | 1024 x 500 px | PNG/JPEG | Yes |
| Phone Screenshots | 320-3840 px (16:9 or 9:16) | PNG/JPEG | 2-8 required |
| 7" Tablet Screenshots | 320-3840 px (16:9 or 9:16) | PNG/JPEG | Up to 8 |
| 10" Tablet Screenshots | 320-3840 px (16:9 or 9:16) | PNG/JPEG | Up to 8 |
| Promo Video | YouTube URL | - | Optional |

## Process

### Step 1: Generate Store Listing Guide

Create `docs/STORE_LISTING_GUIDE.md` with comprehensive instructions.

### Step 2: Feature Graphic Creation Options

The feature graphic (1024 x 500 px) is displayed at the top of your Play Store listing.

**Option A: Canva (Easiest)**
1. Go to [canva.com](https://canva.com)
2. Create custom design: 1024 x 500 px
3. Search templates for "app feature graphic" or "banner"
4. Customize with app name and colors
5. Download as PNG

**Option B: Figma (More Control)**
1. Open [Figma Community Template](https://www.figma.com/community/file/1090631890869514577)
2. Duplicate to your account
3. Customize the feature graphic frame
4. Export as PNG at 1x

**Option C: Simple Python Script**
Use `scripts/generate-feature-graphic.py` to create a basic feature graphic:

```bash
python3 scripts/generate-feature-graphic.py "App Name" "Tagline" "#6200EE"
```

This creates a simple text-based graphic. For production, use Canva or Figma for a more polished result.

### Step 3: Feature Graphic Best Practices

✅ **Do:**
- Use high contrast text
- Keep text minimal (3-5 words)
- Show your app's primary screen
- Use your brand colors
- Leave space for Play Store overlay

❌ **Don't:**
- Include pricing or "free" text
- Use excessive text
- Make it too busy/cluttered
- Use low-resolution images

### Step 4: Update Metadata Files

Ensure all metadata files exist in `fastlane/metadata/android/en-US/`:

#### `title.txt` (Max 30 characters)
```
Your App Name
```

#### `short_description.txt` (Max 80 characters)
```
Short tagline that highlights main benefit
```

#### `full_description.txt` (Max 4000 characters)
```
Full description of your app.

Key Features:
• Feature 1 description
• Feature 2 description
• Feature 3 description
• Feature 4 description

Why Choose This App?
Explain what makes your app unique and valuable.

Download now and start [doing something valuable]!
```

#### `changelogs/default.txt` (Max 500 characters)
```
• New: [Feature name]
• Improved: [Enhancement description]
• Fixed: [Bug fix description]
```

#### `video.txt` (Optional)
```
https://www.youtube.com/watch?v=YOUR_VIDEO_ID
```

### Step 5: Asset Validation

Run validation checks:

```bash
# Check icon dimensions
file fastlane/metadata/android/en-US/images/icon.png
# Expected: PNG image data, 512 x 512

# Check feature graphic dimensions
file fastlane/metadata/android/en-US/images/featureGraphic.png
# Expected: PNG image data, 1024 x 500

# Check screenshot count
ls fastlane/metadata/android/en-US/images/phoneScreenshots/ | wc -l
# Expected: 2-8 files

# Check metadata character limits
wc -c fastlane/metadata/android/en-US/title.txt
# Must be <= 30 characters

wc -c fastlane/metadata/android/en-US/short_description.txt
# Must be <= 80 characters

wc -c fastlane/metadata/android/en-US/full_description.txt
# Must be <= 4000 characters
```

## Multi-Language Support

To add additional languages:

```bash
# Create locale directory
mkdir -p fastlane/metadata/android/de-DE/images/phoneScreenshots
mkdir -p fastlane/metadata/android/de-DE/changelogs

# Copy and translate metadata files
cp fastlane/metadata/android/en-US/*.txt fastlane/metadata/android/de-DE/
# Edit files with German translations

# Update Screengrabfile to capture additional locales
# In fastlane/Screengrabfile:
# locales(["en-US", "de-DE"])

# Run screenshot automation for all locales
bundle exec fastlane screenshots
```

## Uploading to Play Store

Once all assets are ready:

```bash
# Upload metadata only (no build)
bundle exec fastlane upload_metadata

# Upload screenshots only
bundle exec fastlane upload_screenshots

# Full release (includes everything)
bundle exec fastlane deploy_internal
```

## Verification

**MANDATORY:** Run these commands:

```bash
# Check all metadata files exist
ls -la fastlane/metadata/android/en-US/

# Check images exist
ls -la fastlane/metadata/android/en-US/images/

# Validate feature graphic
file fastlane/metadata/android/en-US/images/featureGraphic.png
# Should be: PNG image data, 1024 x 500

# Test metadata upload (dry run)
# bundle exec fastlane upload_metadata --skip_upload_images
```

## Completion Criteria

- [ ] `docs/STORE_LISTING_GUIDE.md` created with full instructions
- [ ] Feature graphic at `fastlane/metadata/android/en-US/images/featureGraphic.png`
- [ ] Feature graphic is 1024x500 PNG
- [ ] All metadata files in `fastlane/metadata/android/en-US/`:
  - [ ] `title.txt` (max 30 chars)
  - [ ] `short_description.txt` (max 80 chars)
  - [ ] `full_description.txt` (max 4000 chars)
  - [ ] `changelogs/default.txt`
  - [ ] `video.txt` (empty is OK)

## Outputs

| Output | Location | Description |
|--------|----------|-------------|
| Store listing guide | docs/STORE_LISTING_GUIDE.md | Complete setup instructions |
| Feature graphic | fastlane/metadata/android/en-US/images/featureGraphic.png | 1024x500 banner |
| Title | fastlane/metadata/android/en-US/title.txt | App title |
| Short description | fastlane/metadata/android/en-US/short_description.txt | 80 char tagline |
| Full description | fastlane/metadata/android/en-US/full_description.txt | Complete description |
| Changelogs | fastlane/metadata/android/en-US/changelogs/default.txt | Release notes |

## Troubleshooting

### "Metadata upload fails"
**Cause:** Character limits exceeded or invalid format
**Fix:** Validate all text files with `wc -c`

### "Feature graphic rejected"
**Cause:** Wrong dimensions or contains prohibited content
**Fix:** Ensure exactly 1024x500, no pricing/ratings/review text

### "Screenshots not showing"
**Cause:** Wrong format or dimensions
**Fix:** Ensure PNG/JPEG, min 320px, aspect ratio 16:9 or 9:16

## Next Steps

After completing this skill:
1. Review all metadata for accuracy and appeal
2. Run `/devtools:android-workflow-internal` to setup deployment
3. Upload to Play Store: `bundle exec fastlane deploy_internal`
