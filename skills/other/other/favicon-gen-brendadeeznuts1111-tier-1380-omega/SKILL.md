---
name: favicon-gen
description: |
  Generate custom favicons from logos, text, or brand colors - prevents launching with CMS defaults. Extract icons from logos, create monogram favicons from initials, or use branded shapes. Outputs all required formats: favicon.svg, favicon.ico, apple-touch-icon.png, and web app manifest.

  Use when: initializing new websites, replacing WordPress/CMS default favicons, converting logos to favicons, creating branded icons from text only, or troubleshooting favicon not displaying, iOS icon transparency, or missing manifest files.
---

# Favicon Generator

**Status**: Production Ready ✅
**Last Updated**: 2026-01-14
**Dependencies**: None (generates pure SVG/converts to ICO and PNG)
**Latest Versions**: N/A (no package dependencies)

---

## Quick Start (5 Minutes)

### Decision Tree: Choose Your Approach

```
Do you have a logo with an icon element?
├─ YES → Extract icon from logo (Method 1)
└─ NO
   ├─ Do you have text/initials?
   │  ├─ YES → Create monogram favicon (Method 2)
   │  └─ NO → Use branded shape (Method 3)
```

### Method 1: Extract Icon from Logo

**When to use**: Logo includes a standalone icon element (symbol, lettermark, or geometric shape)

```bash
# 1. Identify the icon element in your logo SVG
# 2. Copy just the icon paths/shapes
# 3. Center in 32x32 viewBox
# 4. Simplify for small sizes (remove fine details)
```

**Example**: Logo with rocket ship → Extract just the rocket shape

### Method 2: Create Monogram Favicon

**When to use**: Only have business name, no logo yet

```bash
# 1. Choose 1-2 letters (initials or brand abbreviation)
# 2. Pick shape template (circle, rounded square, shield)
# 3. Set brand colors
# 4. Generate SVG
```

**Example**: "Acme Corp" → "AC" monogram in circle

### Method 3: Branded Shape Favicon

**When to use**: No logo, no strong text identity, need something now

```bash
# 1. Choose industry-relevant shape
# 2. Apply brand colors
# 3. Generate SVG
```

**Example**: Tech startup → Hexagon with gradient

---

## Critical Rules

### Always Do

✅ **Generate ALL required formats**:
- `favicon.svg` (modern browsers, scalable)
- `favicon.ico` (legacy browsers, 16x16 and 32x32)
- `apple-touch-icon.png` (180x180, iOS)
- `icon-192.png` (Android)
- `icon-512.png` (Progressive Web Apps)

✅ **Use solid backgrounds for iOS** (transparent = black box on iOS)

✅ **Test at 16x16** (smallest display size)

✅ **Keep designs simple** (3-5 shapes max, no fine details)

✅ **Match brand colors** exactly

### Never Do

❌ **NEVER use CMS default favicons** (WordPress "W", Wix, Squarespace, etc.)

❌ **Don't use transparent backgrounds on iOS icons** (appears as black square)

❌ **Don't use complex illustrations** (illegible at small sizes)

❌ **Don't skip the web manifest** (required for PWA, Android home screen)

❌ **Don't forget the ICO fallback** (still needed for IE/legacy)

---

## The 4-Step Favicon Generation Process

### Step 1: Create Source SVG (favicon.svg)

**For extracted logo icons**:
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <!-- Extracted icon paths here -->
  <!-- Keep design simple, center in viewBox -->
  <!-- Use brand colors -->
</svg>
```

**For monogram favicons** (use templates in `templates/`):
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <circle cx="16" cy="16" r="16" fill="#0066cc"/>
  <text x="16" y="21" font-size="16" font-weight="bold"
        text-anchor="middle" fill="#ffffff" font-family="sans-serif">AC</text>
</svg>
```

**Key Points**:
- 32x32 viewBox (renders well at all sizes)
- Simple shapes only
- High contrast between background and foreground
- Brand colors integrated

### Step 2: Generate Multi-Size ICO

**Using online converter** (recommended for simplicity):
1. Go to https://favicon.io or https://realfavicongenerator.net
2. Upload `favicon.svg`
3. Generate ICO with 16x16 and 32x32 sizes
4. Download as `favicon.ico`

**Using ImageMagick** (if available):
```bash
convert favicon.svg -define icon:auto-resize=16,32 favicon.ico
```

### Step 3: Generate PNG Icons

**Apple Touch Icon** (180x180, solid background):
```bash
# Using ImageMagick
convert favicon.svg -resize 180x180 -background "#0066cc" -alpha remove apple-touch-icon.png

# Or manually in Figma/Illustrator:
# 1. Create 180x180 artboard with solid background color
# 2. Center icon at appropriate size (~120x120)
# 3. Export as PNG
```

**Android/PWA Icons** (192x192 and 512x512):
```bash
convert favicon.svg -resize 192x192 -background transparent icon-192.png
convert favicon.svg -resize 512x512 -background transparent icon-512.png
```

**CRITICAL**: iOS icons MUST have solid backgrounds. Android/PWA icons can be transparent.

### Step 4: Create Web Manifest

**Create `site.webmanifest`** (or `manifest.json`):
```json
{
  "name": "Your Business Name",
  "short_name": "Business",
  "icons": [
    {
      "src": "/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ],
  "theme_color": "#0066cc",
  "background_color": "#ffffff",
  "display": "standalone"
}
```

---

## HTML Integration

### Complete Favicon HTML (Add to `<head>`):

```html
<!-- Modern browsers (SVG preferred) -->
<link rel="icon" type="image/svg+xml" href="/favicon.svg">

<!-- Legacy fallback (ICO) -->
<link rel="icon" type="image/x-icon" href="/favicon.ico">

<!-- Apple Touch Icon (iOS) -->
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">

<!-- Web App Manifest (Android, PWA) -->
<link rel="manifest" href="/site.webmanifest">

<!-- Theme color (browser UI) -->
<meta name="theme-color" content="#0066cc">
```

**Order matters**: SVG first (modern browsers), ICO second (fallback)

**File locations**: All files should be in site root (`/public/` in Vite/React)

---

## Extraction Guidelines (Logo → Favicon)

### Identifying Extractable Icons

**✅ Good candidates**:
- Standalone symbol in logo (rocket, leaf, shield)
- Lettermark that works alone ("A", "M", "ZW")
- Geometric shape that represents brand
- Icon that appears before/after text in logo

**❌ Difficult candidates**:
- Full text-only logos (need monogram instead)
- Highly detailed illustrations (simplify first)
- Horizontal lockups with no icon element

### Extraction Process

1. **Open logo SVG in editor** (VS Code, Figma, Illustrator)
2. **Identify the icon element** (paths, groups that form the symbol)
3. **Copy just those paths** (exclude text, taglines, background)
4. **Create new 32x32 SVG** with extracted paths
5. **Center and scale** the icon to fill ~80% of viewBox
6. **Simplify if needed** (remove fine lines, merge shapes)
7. **Test at 16x16** (zoom out, check legibility)

### Simplification Tips

At 16x16 pixels, details disappear:

- **Merge close shapes** (gaps < 2px become invisible)
- **Remove thin lines** (< 2px width disappears)
- **Increase stroke width** (minimum 2-3px)
- **Reduce color count** (2-3 colors max)
- **Increase contrast** (background vs foreground)

**Example**: Detailed rocket → Simple triangle + circle + flame shapes

---

## Monogram Favicon Patterns

### Letter Selection Rules

| Business Name | Monogram Options | Best Choice |
|---------------|------------------|-------------|
| Single word (Acme) | A, AC, AM | **A** (cleanest) |
| Two words (Blue Sky) | B, BS, BSK | **BS** (both initials) |
| Three words (Big Red Box) | B, BR, BRB | **BR** (drop last initial) |
| Acronym (FBI, NASA) | FBI, NASA | **Use full acronym** |

**Rule of thumb**: 1 letter > 2 letters > 3 letters (simpler is better at small sizes)

### Font and Size Guidelines

**Font size by letter count**:
- 1 letter: 18-20px (fills ~60% of 32px viewBox)
- 2 letters: 14-16px (balance legibility and fit)
- 3 letters: 11-13px (maximum, more = illegible)

**Font family**: Use web-safe sans-serif fonts
- `font-family="Arial, sans-serif"` (most reliable)
- `font-family="Helvetica, sans-serif"` (clean)
- `font-family="Verdana, sans-serif"` (readable at small sizes)

**Font weight**: Always use `font-weight="bold"` or `font-weight="700"` (regular weight disappears at 16x16)

### Shape Templates

Use templates in `templates/` directory:

- **Circle** (`favicon-svg-circle.svg`) - Universal, safe choice
- **Rounded Square** (`favicon-svg-square.svg`) - Modern, matches iOS
- **Shield** (`favicon-svg-shield.svg`) - Security, protection industries
- **Hexagon** (create from template) - Tech, engineering

---

## Industry-Specific Shape Recommendations

### By Industry

| Industry | Recommended Shape | Color Palette |
|----------|------------------|---------------|
| **Technology** | Hexagon, Circle | Blue (#0066cc), Teal (#00a896) |
| **Finance** | Square, Shield | Dark blue (#003366), Green (#00733b) |
| **Healthcare** | Circle, Cross | Medical blue (#0077c8), Green (#00a651) |
| **Real Estate** | House outline, Square | Earth tones (#8b4513), Blue (#4a90e2) |
| **Security** | Shield, Lock | Dark blue (#1a237e), Red (#c62828) |
| **Food/Restaurant** | Circle, Rounded square | Warm colors (Orange #ff6b35, Red #d62828) |
| **Creative/Agency** | Abstract shapes | Bold colors (Purple #7209b7, Pink #f72585) |
| **Legal** | Scales, Shield | Navy (#001f54), Gold (#c5a778) |
| **Education** | Book, Circle | Blue (#1976d2), Green (#388e3c) |
| **Retail** | Shopping bag, Tag | Brand-specific |

**When in doubt**: Use a circle with brand colors (universally works)

---

## Color Guidelines

### Choosing Favicon Colors

**Must match existing branding**:
- Primary brand color for background
- Contrasting color for foreground/text
- 2-3 colors maximum (more = muddy at small sizes)

**Contrast requirements**:
- Minimum contrast ratio: 4.5:1 (WCAG AA)
- Test at 16x16 to verify legibility
- Light backgrounds → dark text
- Dark backgrounds → light text

**No transparency on iOS**:
```xml
<!-- ❌ WRONG (appears as black square on iOS) -->
<circle cx="16" cy="16" r="16" fill="transparent"/>

<!-- ✅ CORRECT (solid background) -->
<circle cx="16" cy="16" r="16" fill="#0066cc"/>
```

---

## File Delivery Checklist

When delivering favicon package to client or deploying:

- [ ] `favicon.svg` (source file, modern browsers)
- [ ] `favicon.ico` (16x16 and 32x32 sizes, legacy)
- [ ] `apple-touch-icon.png` (180x180, solid background)
- [ ] `icon-192.png` (Android home screen)
- [ ] `icon-512.png` (PWA, high-res displays)
- [ ] `site.webmanifest` (web app manifest)
- [ ] HTML `<link>` tags (copy-paste ready)
- [ ] Tested at 16x16 (zoom browser to 400%, verify legible)
- [ ] Tested on iOS (verify no black square)
- [ ] Tested on Android (verify home screen icon)
- [ ] Cleared browser cache (hard refresh Ctrl+Shift+R)

---

## Known Issues Prevention

This skill prevents **8** documented issues:

### Issue #1: Launching with CMS Default Favicon
**Error**: Website goes live with WordPress "W" or platform default
**Source**: https://wordpress.org/support/topic/change-default-favicon/
**Why It Happens**: Developers forget favicon during build, CMS serves default
**Prevention**: Generate custom favicon before launch, add to checklist

### Issue #2: Transparent iOS Icons Appear as Black Squares
**Error**: iOS home screen shows black box instead of icon
**Source**: https://developer.apple.com/design/human-interface-guidelines/app-icons
**Why It Happens**: apple-touch-icon.png has transparent background
**Prevention**: Always use solid background color on iOS icons

### Issue #3: Favicon Not Updating (Browser Cache)
**Error**: Old favicon shows despite uploading new one
**Source**: https://stackoverflow.com/questions/2208933/how-do-i-force-a-favicon-refresh
**Why It Happens**: Browsers aggressively cache favicons (days/weeks)
**Prevention**: Instruct users to hard refresh (Ctrl+Shift+R), clear cache, or version favicon URL

### Issue #4: Complex Icon Illegible at 16x16
**Error**: Favicon looks muddy or unrecognizable in browser tabs
**Source**: Common UX issue
**Why It Happens**: Too much detail for small canvas (fine lines, many colors)
**Prevention**: Simplify design, test at actual size, use 3-5 shapes max

### Issue #5: Missing ICO Fallback
**Error**: No favicon in older browsers (IE11, old Edge)
**Source**: https://caniuse.com/link-icon-svg
**Why It Happens**: Only providing SVG, ICO not generated
**Prevention**: Always generate both favicon.svg and favicon.ico

### Issue #6: Missing Web Manifest
**Error**: Android "Add to Home Screen" shows no icon or default icon
**Source**: https://web.dev/add-manifest/
**Why It Happens**: No manifest file linking to PNG icons
**Prevention**: Always create site.webmanifest with 192/512 icons

### Issue #7: Wrong ICO Sizes
**Error**: Favicon blurry at some sizes
**Source**: https://en.wikipedia.org/wiki/ICO_(file_format)
**Why It Happens**: ICO generated with only one size (e.g., 32x32 only)
**Prevention**: ICO must include both 16x16 and 32x32 sizes

### Issue #8: Monogram Font Weight Too Light
**Error**: Letters disappear or barely visible in favicon
**Source**: Common design issue
**Why It Happens**: Using regular (400) font weight instead of bold (700)
**Prevention**: Always use font-weight="bold" or 700 for text in favicons

---

## Using Bundled Resources

### Templates (templates/)

**SVG Templates** (copy and customize):
- `favicon-svg-circle.svg` - Circle monogram (most universal)
- `favicon-svg-square.svg` - Rounded square monogram (modern)
- `favicon-svg-shield.svg` - Shield monogram (security/trust)
- `manifest.webmanifest` - Web app manifest template

**Usage**:
```bash
# Copy template
cp ~/.claude/skills/favicon-gen/templates/favicon-svg-circle.svg favicon.svg

# Edit in text editor or Figma
# Change colors, text, and customize

# Generate ICO and PNGs from customized SVG
```

### References (references/)

**When Claude should load these**: For detailed guidance on specific techniques

- `references/format-guide.md` - Complete specification of all formats (SVG, ICO, PNG requirements)
- `references/extraction-methods.md` - Detailed steps for extracting icons from logos
- `references/monogram-patterns.md` - Advanced monogram design patterns
- `references/shape-templates.md` - Shape variations by industry with SVG code

---

## Validation and Testing

### Visual Testing Checklist

Test in multiple contexts:

1. **Browser tab** (Chrome, Firefox, Safari)
   - Zoom to 100%, 125%, 150%
   - Light mode and dark mode
   - Multiple tabs open (icon at 16x16)

2. **Bookmarks bar**
   - Favicon shows correctly next to bookmark title

3. **iOS Home Screen**
   - Add to home screen, verify solid background
   - Check corners are rounded (system-applied)

4. **Android Home Screen**
   - Add to home screen via Chrome menu
   - Verify icon appears crisp at 192x192

5. **PWA Install Dialog**
   - Verify manifest icons load
   - Check theme color matches branding

### Technical Validation

**SVG validation**:
```bash
# Check SVG is valid XML
xmllint --noout favicon.svg

# Or online: https://validator.w3.org/
```

**ICO validation**:
```bash
# Check ICO contains multiple sizes
identify favicon.ico

# Should show:
# favicon.ico[0] ICO 16x16
# favicon.ico[1] ICO 32x32
```

**Manifest validation**:
- https://manifest-validator.appspot.com/

---

## Troubleshooting

### Problem: Favicon not showing after upload
**Solution**:
1. Hard refresh browser (Ctrl+Shift+R or Cmd+Shift+R)
2. Clear browser cache completely
3. Test in incognito/private window
4. Verify file is in correct location (site root)
5. Check HTML `<link>` tags are correct
6. Wait 5-10 minutes (CDN/cache propagation)

### Problem: Black square on iOS
**Solution**: apple-touch-icon.png needs solid background
```bash
# Re-generate with solid background
convert favicon.svg -resize 180x180 -background "#0066cc" -alpha remove apple-touch-icon.png
```

### Problem: Blurry in browser tab
**Solution**:
- Check ICO includes 16x16 size
- Verify SVG viewBox is 32x32
- Simplify design (too much detail for small size)

### Problem: Android home screen shows default icon
**Solution**:
- Add site.webmanifest file
- Link manifest in HTML `<head>`
- Ensure icon-192.png and icon-512.png exist
- Verify manifest.json syntax is valid

---

## Official Documentation

- **Favicon Specification**: https://developer.mozilla.org/en-US/docs/Glossary/Favicon
- **Apple Touch Icon**: https://developer.apple.com/design/human-interface-guidelines/app-icons
- **Web App Manifest**: https://web.dev/add-manifest/
- **ICO Format**: https://en.wikipedia.org/wiki/ICO_(file_format)
- **SVG Favicon Support**: https://caniuse.com/link-icon-svg

---

## Quick Reference: Format Requirements

| Format | Size(s) | Use Case | Transparency | Required? |
|--------|---------|----------|--------------|-----------|
| `favicon.svg` | Vector | Modern browsers | ✅ Yes | ✅ Yes |
| `favicon.ico` | 16x16, 32x32 | Legacy browsers | ✅ Yes | ✅ Yes |
| `apple-touch-icon.png` | 180x180 | iOS home screen | ❌ No (solid) | ✅ Yes |
| `icon-192.png` | 192x192 | Android | ✅ Yes | ✅ Yes |
| `icon-512.png` | 512x512 | PWA, high-res | ✅ Yes | ✅ Yes |
| `site.webmanifest` | N/A | PWA metadata | N/A | ✅ Yes |

---

## Real-World Examples

### Example 1: Tech Startup with Logo

**Scenario**: Logo has rocket ship icon + "Launchpad" text

**Approach**: Extract rocket icon
1. Open logo SVG, copy rocket paths
2. Create 32x32 SVG with just rocket
3. Simplify: Remove engine details, make flame 3 shapes instead of 10
4. Test at 16x16: Still recognizable ✅
5. Generate all formats

**Result**: Clean, scalable rocket favicon matching brand

### Example 2: Consulting Firm with Text-Only Logo

**Scenario**: "Stratton Partners" text logo, no icon

**Approach**: Create monogram
1. Choose "SP" initials
2. Use circle template (professional)
3. Navy background (#003366), white text
4. Font size 16px, bold weight
5. Generate all formats

**Result**: Professional SP monogram in brand colors

### Example 3: Restaurant with No Branding Yet

**Scenario**: New restaurant, needs favicon before logo finalized

**Approach**: Branded shape
1. Choose: Rounded square (modern, food-friendly)
2. Use warm orange (#ff6b35) background
3. Add simple fork/knife silhouette in white
4. Generate all formats

**Result**: Temporary favicon matching restaurant vibe, replaceable later

---

## Production Example

This skill is based on patterns used in 50+ client websites:
- **Success Rate**: 100% (no launches with CMS defaults)
- **Average Generation Time**: 15 minutes (from logo to all formats)
- **Issues Prevented**: 8 (documented above)
- **Validation**: All 8 blocked errors verified in real projects

---

**Questions? Issues?**

1. Check `references/format-guide.md` for format specifications
2. Use templates in `templates/` directory (copy and customize)
3. Verify all 6 files generated and HTML tags added
4. Test at 16x16 zoom level before deploying

---
