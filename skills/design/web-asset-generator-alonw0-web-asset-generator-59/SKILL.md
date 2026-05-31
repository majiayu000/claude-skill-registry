---
name: web-asset-generator
description: Generate web assets including favicons, app icons (PWA), and social media meta images (Open Graph) for Facebook, Twitter, WhatsApp, and LinkedIn. Use when users need icons, favicons, social sharing images, or Open Graph images from logos or text slogans. Handles image resizing, text-to-image generation, and provides proper HTML meta tags.
---

# Web Asset Generator

Generate professional web assets from logos or text slogans, including favicons, app icons, and social media meta images.

## Quick Start

When a user requests web assets:

1. **Use AskUserQuestion tool to clarify needs** if not specified:
   - What type of assets they need (favicons, app icons, social images, or everything)
   - Whether they have source material (logo image vs text/slogan)
   - For text-based images: color preferences

2. **Check for source material**:
   - If user uploaded an image: use it as the source
   - If user provides text/slogan: generate text-based images

3. **Run the appropriate script(s)**:
   - Favicons/icons: `scripts/generate_favicons.py`
   - Social media images: `scripts/generate_og_images.py`

4. **Provide the generated assets and HTML tags** to the user

## Using Interactive Questions

**IMPORTANT**: Always use the AskUserQuestion tool to gather requirements instead of plain text questions. This provides a better user experience with visual selection UI.

### Why Use AskUserQuestion?

✅ **Visual UI**: Users see options as clickable chips/tags instead of typing responses
✅ **Faster**: Click to select instead of typing out answers
✅ **Clearer**: Descriptions explain what each option means
✅ **Fewer errors**: No typos or misunderstandings from free-form text
✅ **Professional**: Consistent with modern Claude Code experience

### Example Flow

**User request**: "I need web assets"

**Claude uses AskUserQuestion** (not plain text):
```
What type of web assets do you need?                    [Asset type]
○ Favicons only - Browser tab icons (16x16, 32x32, 96x96) and favicon.ico
○ App icons only - PWA icons for iOS/Android (180x180, 192x192, 512x512)
○ Social images only - Open Graph images for Facebook, Twitter, WhatsApp, LinkedIn
● Everything - Complete package: favicons + app icons + social images
```

User clicks → Claude immediately knows what to generate

### Question Patterns

Below are the standard question patterns to use in various scenarios. Copy the structure and adapt as needed.

### Question Pattern 1: Asset Type Selection

When the user's request is vague (e.g., "create web assets", "I need icons"), use AskUserQuestion:

**Question**: "What type of web assets do you need?"
**Header**: "Asset type"
**Options**:
- **"Favicons only"** - Description: "Browser tab icons (16x16, 32x32, 96x96) and favicon.ico"
- **"App icons only"** - Description: "PWA icons for iOS/Android (180x180, 192x192, 512x512)"
- **"Social images only"** - Description: "Open Graph images for Facebook, Twitter, WhatsApp, LinkedIn"
- **"Everything"** - Description: "Complete package: favicons + app icons + social images"

### Question Pattern 2: Source Material

When the asset type is determined but source is unclear:

**Question**: "What source material will you provide?"
**Header**: "Source"
**Options**:
- **"Logo image"** - Description: "I have or will upload a logo/image file"
- **"Emoji"** - Description: "Generate favicon from an emoji character"
- **"Text/slogan"** - Description: "Create images from text only"
- **"Logo + text"** - Description: "Combine logo with text overlay (for social images)"

### Question Pattern 3: Platform Selection (for social images)

When user requests social images but doesn't specify platforms:

**Question**: "Which social media platforms do you need images for?"
**Header**: "Platforms"
**Multi-select**: true
**Options**:
- **"Facebook/WhatsApp/LinkedIn"** - Description: "Standard 1200x630 Open Graph format"
- **"Twitter"** - Description: "1200x675 (16:9 ratio) for large image cards"
- **"All platforms"** - Description: "Generate all variants including square format"

### Question Pattern 4: Color Preferences (for text-based images)

When generating text-based social images:

**Question**: "What colors should we use for your social images?"
**Header**: "Colors"
**Options**:
- **"I'll provide colors"** - Description: "Let me specify exact hex codes for brand colors"
- **"Default theme"** - Description: "Use default purple background (#4F46E5) with white text"
- **"Extract from logo"** - Description: "Auto-detect brand colors from uploaded logo"
- **"Custom gradient"** - Description: "Let me choose gradient colors"

### Question Pattern 5: Icon Type Clarification

When user says "create icons" or "generate icons" (ambiguous):

**Question**: "What kind of icons do you need?"
**Header**: "Icon type"
**Options**:
- **"Website favicon"** - Description: "Small browser tab icon"
- **"App icons (PWA)"** - Description: "Mobile home screen icons"
- **"Both"** - Description: "Favicon + app icons"

### Question Pattern 6: Emoji Selection

When user selects "Emoji" as source material:

**Step 1**: Ask for project description (free text):
- "What is your website/app about?"
- Use this to generate emoji suggestions

**Step 2**: Use AskUserQuestion to present the 4 suggested emojis:

**Question**: "Which emoji best represents your project?"
**Header**: "Emoji"
**Options**: (Dynamically generated based on project description)
- Example: **"🚀 Rocket"** - Description: "Rocket, launch, startup, space"
- Example: **"☕ Coffee"** - Description: "Coffee, cafe, beverage, drink"
- Example: **"💻 Laptop"** - Description: "Computer, laptop, code, dev"
- Example: **"🎨 Art"** - Description: "Art, design, creative, paint"

**Implementation**:
```bash
# Get suggestions
python scripts/generate_favicons.py --suggest "coffee shop" output/ all

# Then generate with selected emoji
python scripts/generate_favicons.py --emoji "☕" output/ all
```

**Optional**: Ask about background color for app icons:

**Question**: "Do you want a background color for app icons?"
**Header**: "Background"
**Options**:
- **"Transparent"** - Description: "No background (favicons only)"
- **"White"** - Description: "White background (recommended for app icons)"
- **"Custom color"** - Description: "I'll provide a color"

### Question Pattern 7: Code Integration Offer

**When to use**: After generating assets and showing HTML tags to the user

**Question**: "Would you like me to add these HTML tags to your codebase?"
**Header**: "Integration"
**Options**:
- **"Yes, auto-detect my setup"** - Description: "Find and update my HTML/framework files automatically"
- **"Yes, I'll tell you where"** - Description: "I'll specify which file to update"
- **"No, I'll do it manually"** - Description: "Just show me the code, I'll add it myself"

**If user selects "Yes, auto-detect":**
1. Search for framework config files (next.config.js, astro.config.mjs, etc.)
2. Detect framework type
3. Find appropriate target file (layout.tsx, index.html, etc.)
4. Show detected file and ask for confirmation
5. Show diff of proposed changes
6. Insert tags if user confirms

**If user selects "Yes, I'll tell you where":**
1. Ask user for file path
2. Verify file exists
3. Show diff of proposed changes
4. Insert tags if user confirms

**Framework Detection Priority:**
- Next.js: Look for `next.config.js`, update `app/layout.tsx` or `pages/_app.tsx`
- Astro: Look for `astro.config.mjs`, update layout files in `src/layouts/`
- SvelteKit: Look for `svelte.config.js`, update `src/app.html`
- Vue/Nuxt: Look for `nuxt.config.js`, update `app.vue` or `nuxt.config.ts`
- Plain HTML: Look for `index.html` or `*.html` files
- Gatsby: Look for `gatsby-config.js`, update `gatsby-ssr.js`

### Question Pattern 8: Testing Links Offer

**When to use**: After code integration (or if user declined integration)

**Question**: "Would you like to test your meta tags now?"
**Header**: "Testing"
**Options**:
- **"Facebook Debugger"** - Description: "Test Open Graph tags on Facebook"
- **"Twitter Card Validator"** - Description: "Test Twitter card appearance"
- **"LinkedIn Post Inspector"** - Description: "Test LinkedIn sharing preview"
- **"All testing tools"** - Description: "Get links to all validators"
- **"No, skip testing"** - Description: "I'll test later myself"

**Provide appropriate testing URLs:**
- Facebook: https://developers.facebook.com/tools/debug/
- Twitter: https://cards-dev.twitter.com/validator
- LinkedIn: https://www.linkedin.com/post-inspector/
- Generic OG validator: https://www.opengraph.xyz/

## Workflows

### Generate Favicons and App Icons from Logo

When user has a logo image:

```bash
python scripts/generate_favicons.py <source_image> <output_dir> [icon_type]
```

Arguments:
- `source_image`: Path to the logo/image file
- `output_dir`: Where to save generated icons
- `icon_type`: Optional - 'favicon', 'app', or 'all' (default: 'all')

Example:
```bash
python scripts/generate_favicons.py /mnt/user-data/uploads/logo.png /home/claude/output all
```

Generates:
- `favicon-16x16.png`, `favicon-32x32.png`, `favicon-96x96.png`
- `favicon.ico` (multi-resolution)
- `apple-touch-icon.png` (180x180)
- `android-chrome-192x192.png`, `android-chrome-512x512.png`

### Generate Favicons and App Icons from Emoji

**NEW FEATURE**: Create favicons from emoji characters with smart suggestions!

#### Step 1: Get Emoji Suggestions

When user wants emoji-based icons, first get suggestions:

```bash
python scripts/generate_favicons.py --suggest "coffee shop" /home/claude/output all
```

This returns 4 emoji suggestions based on the description:
```
1. ☕  Coffee               - coffee, cafe, beverage
2. 🌐  Globe                - web, website, global
3. 🏪  Store                - shop, store, retail
4. 🛒  Cart                 - shopping, cart, ecommerce
```

#### Step 2: Generate Icons from Selected Emoji

```bash
python scripts/generate_favicons.py --emoji "☕" <output_dir> [icon_type] [--emoji-bg COLOR]
```

Arguments:
- `--emoji`: Emoji character to use
- `output_dir`: Where to save generated icons
- `icon_type`: Optional - 'favicon', 'app', or 'all' (default: 'all')
- `--emoji-bg`: Optional background color (default: transparent for favicons, white for app icons)

Examples:
```bash
# Basic emoji favicon (transparent background)
python scripts/generate_favicons.py --emoji "🚀" /home/claude/output favicon

# Emoji with custom background for app icons
python scripts/generate_favicons.py --emoji "☕" --emoji-bg "#F5DEB3" /home/claude/output all

# Complete set with white background
python scripts/generate_favicons.py --emoji "💻" --emoji-bg "white" /home/claude/output all
```

Generates same files as logo-based generation:
- All standard favicon sizes (16x16, 32x32, 96x96)
- favicon.ico
- App icon sizes (180x180, 192x192, 512x512)

**Note**: Requires `pilmoji` library: `pip install pilmoji`

### Generate Social Media Meta Images from Logo

When user has a logo and needs Open Graph images:

```bash
python scripts/generate_og_images.py <output_dir> --image <source_image>
```

Example:
```bash
python scripts/generate_og_images.py /home/claude/output --image /mnt/user-data/uploads/logo.png
```

Generates:
- `og-image.png` (1200x630 - Facebook, WhatsApp, LinkedIn)
- `twitter-image.png` (1200x675 - Twitter)
- `og-square.png` (1200x1200 - Square variant)

### Generate Social Media Meta Images from Text

When user provides a text slogan or tagline:

```bash
python scripts/generate_og_images.py <output_dir> --text "Your text here" [options]
```

Options:
- `--logo <path>`: Include a logo with the text
- `--bg-color <color>`: Background color (hex or name, default: '#4F46E5')
- `--text-color <color>`: Text color (default: 'white')

Example:
```bash
python scripts/generate_og_images.py /home/claude/output \
  --text "Transform Your Business with AI" \
  --logo /mnt/user-data/uploads/logo.png \
  --bg-color "#4F46E5"
```

### Generate Everything

For users who want the complete package:

```bash
# Generate favicons and icons
python scripts/generate_favicons.py /mnt/user-data/uploads/logo.png /home/claude/output all

# Generate social media images
python scripts/generate_og_images.py /home/claude/output --image /mnt/user-data/uploads/logo.png
```

Or for text-based:
```bash
# Generate favicons from logo
python scripts/generate_favicons.py /mnt/user-data/uploads/logo.png /home/claude/output all

# Generate social media images with text + logo
python scripts/generate_og_images.py /home/claude/output \
  --text "Your Tagline Here" \
  --logo /mnt/user-data/uploads/logo.png
```

## Delivering Assets to User

After generating assets, follow this workflow:

### 1. Move to Outputs Directory
```bash
cp /home/claude/output/* /mnt/user-data/outputs/
```

### 2. Show Generated HTML Tags

Display the HTML tags that were automatically generated by the scripts.

Example output for favicons:
```html
<!-- Favicons -->
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
<link rel="icon" type="image/png" sizes="96x96" href="/favicon-96x96.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="icon" type="image/png" sizes="192x192" href="/android-chrome-192x192.png">
<link rel="icon" type="image/png" sizes="512x512" href="/android-chrome-512x512.png">
```

Example output for Open Graph images:
```html
<!-- Open Graph / Facebook -->
<meta property="og:image" content="/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Your description here">

<!-- Twitter -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="/twitter-image.png">
<meta name="twitter:image:alt" content="Your description here">
```

### 3. Offer Code Integration (Use AskUserQuestion - Pattern 7)

**IMPORTANT**: Always ask if the user wants help adding the tags to their codebase.

**Question**: "Would you like me to add these HTML tags to your codebase?"
**Header**: "Integration"
**Options**:
- "Yes, auto-detect my setup"
- "Yes, I'll tell you where"
- "No, I'll do it manually"

#### If User Selects "Yes, auto-detect my setup":

**A. Detect Framework:**
```bash
# Search for framework config files
find . -maxdepth 2 -name "next.config.js" -o -name "astro.config.mjs" -o -name "svelte.config.js" -o -name "nuxt.config.js" -o -name "gatsby-config.js"

# Or check package.json
grep -E "next|astro|nuxt|svelte|gatsby" package.json
```

**B. Find Target Files Based on Framework:**

- **Next.js (App Router)**: `app/layout.tsx` or `app/layout.js`
- **Next.js (Pages Router)**: `pages/_app.tsx` or `pages/_document.tsx`
- **Astro**: `src/layouts/*.astro` (typically `BaseLayout.astro` or `Layout.astro`)
- **SvelteKit**: `src/app.html`
- **Vue/Nuxt**: `app.vue` or `nuxt.config.ts` (head section)
- **Gatsby**: `gatsby-ssr.js` or `src/components/seo.tsx`
- **Plain HTML**: `index.html`, `public/index.html`, or any `*.html` file

**C. Confirm with User:**

Use AskUserQuestion to confirm detected file:
```
Question: "I found [Framework Name]. Should I update [file_path]?"
Header: "Confirm"
Options:
- "Yes, update this file"
- "No, show me other options"
- "Cancel, I'll do it manually"
```

**D. Show Diff and Insert:**

1. Read the target file
2. Prepare the insertion (find `<head>` or appropriate section)
3. Show the diff to the user
4. If user confirms, use Edit tool to insert tags

**Framework-Specific Insertion Examples:**

**For Plain HTML** (insert before `</head>`):
```html
<head>
  <meta charset="UTF-8">
  <!-- INSERT TAGS HERE -->
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
  ...
</head>
```

**For Next.js App Router** (add to metadata export):
```typescript
export const metadata = {
  icons: {
    icon: [
      { url: '/favicon-32x32.png', sizes: '32x32', type: 'image/png' },
      { url: '/favicon-16x16.png', sizes: '16x16', type: 'image/png' },
    ],
    apple: [
      { url: '/apple-touch-icon.png', sizes: '180x180', type: 'image/png' },
    ],
  },
  openGraph: {
    images: ['/og-image.png'],
  },
  twitter: {
    card: 'summary_large_image',
    images: ['/twitter-image.png'],
  },
}
```

**For Astro** (insert in `<head>` of layout file):
```astro
<head>
  <meta charset="UTF-8">
  <!-- Favicons -->
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
  ...
</head>
```

#### If User Selects "Yes, I'll tell you where":

1. Ask user for the file path
2. Verify file exists using Read tool
3. Show where tags will be inserted
4. Show diff
5. Insert if user confirms

#### If User Selects "No, I'll do it manually":

Provide brief instructions:
- Place asset files in the public/static directory of your website
- Add the HTML tags to the `<head>` section of your HTML
- Update placeholder values (title, description, URL, alt text)

### 4. Offer Testing Links (Use AskUserQuestion - Pattern 8)

**Question**: "Would you like to test your meta tags now?"
**Header**: "Testing"
**Options**:
- "Facebook Debugger"
- "Twitter Card Validator"
- "LinkedIn Post Inspector"
- "All testing tools"
- "No, skip testing"

**Provide Testing URLs:**

- **Facebook Sharing Debugger**: https://developers.facebook.com/tools/debug/
  - Paste your URL and click "Debug" to see preview
  - Click "Scrape Again" to refresh cache

- **Twitter Card Validator**: https://cards-dev.twitter.com/validator
  - Paste your URL to see how Twitter card will appear

- **LinkedIn Post Inspector**: https://www.linkedin.com/post-inspector/
  - Check how links appear when shared on LinkedIn

- **OpenGraph.xyz**: https://www.opengraph.xyz/
  - Generic Open Graph validator for quick checks

### 5. Final Instructions

Remind user to:
- ✅ Copy asset files to their public/static directory
- ✅ Update dynamic values in meta tags (og:title, og:description, og:url)
- ✅ Test on actual platforms after deployment
- ✅ Update alt text to be descriptive and accessible

**Important Notes:**
- OG images must be accessible via HTTPS URLs (not localhost)
- URLs in meta tags should be absolute (https://yourdomain.com/og-image.png)
- Test after deploying to production/staging environment

## Best Practices

### Image Requirements
- **Logos**: Should be square or nearly square for best results
- **High resolution**: Provide largest available version (scripts will downscale)
- **Transparent backgrounds**: PNG with transparency works best for favicons
- **Solid backgrounds**: Recommended for app icons and social images

### Text Content
- **Text length affects font size automatically**:
  - Short text (≤20 chars): 144px font - Large and impactful
  - Medium text (21-40 chars): 120px font - Standard readable size
  - Long text (41-60 chars): 102px font - Reduced for fit
  - Very long text (>60 chars): 84px font - Minimal size
- Keep text concise for maximum impact
- Use 2-3 lines of text maximum for social images
- Avoid special characters that may not render well

### Color Choices
- Ensure sufficient contrast (4.5:1 minimum for readability)
- Use brand colors consistently
- Consider both light and dark mode contexts

## Validation and Quality Checks

Both `generate_og_images.py` and `generate_favicons.py` support automated validation with the `--validate` flag.

### When to Use Validation

**Always recommend validation** when:
- User is generating for production/deployment
- User asks about file sizes or quality
- User mentions platform requirements (Facebook, Twitter, etc.)
- User is new to web assets and may not know requirements

**Validation is optional** for:
- Quick prototypes or testing
- Users who explicitly decline
- When time is a concern

### What Gets Validated

#### For Social Media Images (OG Images)

**File Size Validation**:
- Facebook/LinkedIn/WhatsApp: Must be <8MB
- Twitter: Must be <5MB
- Warning if within 80% of limit

**Dimension Validation**:
- Checks against platform-specific recommended sizes:
  - Facebook/LinkedIn: 1200x630 (1.91:1 ratio)
  - Twitter: 1200x675 (16:9 ratio)
  - Square: 1200x1200 (1:1 ratio)
- Warns if aspect ratio is >10% off target
- Errors if below minimum dimensions

**Format Validation**:
- Facebook/LinkedIn: PNG, JPG, JPEG
- Twitter: PNG, JPG, JPEG, WebP
- Errors if unsupported format

**Accessibility (Contrast Ratio)**:
- Only for text-based images
- Calculates WCAG 2.0 contrast ratio
- Reports compliance level:
  - WCAG AAA: 7.0:1 (normal text) or 4.5:1 (large text)
  - WCAG AA: 4.5:1 (normal text) or 3.0:1 (large text)
  - Fails if below AA minimum

#### For Favicons and App Icons

**File Size Validation**:
- Favicons: Warns if >100KB (recommended for fast loading)
- App icons: Warns if >500KB (recommended for mobile)
- No hard limits, but warnings help optimize performance

**Dimension Validation**:
- Verifies each icon matches expected size (16x16, 32x32, etc.)
- Ensures square aspect ratio

**Format Validation**:
- Checks all files are PNG (or ICO for favicon.ico)

### How to Use Validation

**In generate_og_images.py**:
```bash
python scripts/generate_og_images.py output/ --text "My Site" --validate
```

**In generate_favicons.py**:
```bash
python scripts/generate_favicons.py logo.png output/ all --validate
```

**Output Format**:
- ✓ Success (green): All checks passed
- ⚠ Warning (yellow): Issues to consider but not critical
- ❌ Error (red): Must be fixed before deployment

### Example Validation Output

```
======================================================================
Running validation checks...
======================================================================

og-image.png:

Facebook Validation:
======================================================================
  ✓ File size 0.3MB is within Facebook limits
  ✓ Dimensions 1200x630 match Facebook recommended size
  ✓ Format PNG is supported by Facebook

LinkedIn Validation:
======================================================================
  ✓ File size 0.3MB is within LinkedIn limits
  ✓ Dimensions 1200x630 match LinkedIn recommended size
  ✓ Format PNG is supported by LinkedIn

======================================================================
Accessibility Checks:
======================================================================
  ✓ Contrast ratio 8.6:1 meets WCAG AAA standards (4.5:1 required)

======================================================================
Summary: 9/9 checks passed
✓ All validations passed!
```

### Integrating Validation into Workflows

**After generating assets**, if validation was NOT run:
1. Show the tip message: "💡 Tip: Use --validate to check file sizes, dimensions, and accessibility"
2. Optionally ask: "Would you like me to run validation on these files now?"

**If validation was run and issues found**:
1. Explain any errors or warnings
2. Offer to fix issues (e.g., resize, recompress, adjust colors)
3. Re-run generation with fixes if user agrees

**If validation passes**:
1. Confirm: "✅ All validation checks passed!"
2. Proceed with code integration and testing links

## Specifications and Platform Details

For detailed platform specifications, size requirements, and implementation guidelines, read:
- `references/specifications.md`: Comprehensive specs for all platforms

## Handling Common Requests

### "Create a favicon for my site"

**Use AskUserQuestion**:
- Question: "Do you have a logo image, or should I create a text-based favicon?"
- Header: "Source"
- Options:
  - "Logo image" - Description: "I have/will upload a logo file"
  - "Text-based" - Description: "Generate from text or initials"

**Then ask**:
- Question: "Do you also need PWA app icons for mobile devices?"
- Header: "Scope"
- Options:
  - "Favicon only" - Description: "Just browser tab icons (16x16, 32x32, 96x96)"
  - "Include app icons" - Description: "Add iOS/Android icons for home screen (180x180, 192x192, 512x512)"

**Generate**: Use `generate_favicons.py` with appropriate parameters

### "Make social sharing images"

**Use AskUserQuestion**:
- Question: "Which social media platforms do you need images for?"
- Header: "Platforms"
- Multi-select: true
- Options:
  - "Facebook/WhatsApp/LinkedIn" - Description: "Standard 1200x630 format"
  - "Twitter" - Description: "1200x675 (16:9 ratio)"
  - "All platforms" - Description: "Generate all variants"

**Then ask**:
- Question: "What should the images contain?"
- Header: "Content"
- Options:
  - "Logo only" - Description: "Resize my logo for social sharing"
  - "Text only" - Description: "Create images from text/slogan"
  - "Logo + text" - Description: "Combine logo with text overlay"

**Generate**: Use `generate_og_images.py` with appropriate parameters

### "I need everything for my website"

**Use AskUserQuestion**:
- Question: "What source material will you provide?"
- Header: "Source"
- Options:
  - "Logo image" - Description: "I have a logo to use for all assets"
  - "Logo + tagline" - Description: "Logo for icons, logo+text for social images"
  - "Text only" - Description: "Generate all assets from text/initials"

**Generate**:
- Both favicons and Open Graph images with complete HTML implementation
- Provide instructions for file placement and testing

### User provides both logo and tagline

**Use AskUserQuestion**:
- Question: "How should I use your logo and tagline?"
- Header: "Layout"
- Options:
  - "Logo above text" - Description: "Logo at top, tagline centered below"
  - "Logo + text side-by-side" - Description: "Logo on left, text on right"
  - "Text only on social images" - Description: "Use logo for icons, text-only for social sharing"
  - "Logo background with text" - Description: "Subtle logo background with prominent text"

**Generate**: Use `--text` and `--logo` parameters together in `generate_og_images.py`

## Dependencies

The scripts require:
- Python 3.6+
- Pillow (PIL): `pip install Pillow --break-system-packages`
- **Pilmoji** (for emoji support): `pip install pilmoji` (optional, only needed for emoji-based generation)
- **emoji** (for emoji suggestions): `pip install emoji` (optional, only needed for emoji suggestions)

Install if needed before running scripts.

**For emoji features**, install both:
```bash
pip install pilmoji emoji --break-system-packages
```
