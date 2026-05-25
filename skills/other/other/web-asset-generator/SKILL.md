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


## Extended Reference

Detailed material starting at `## Delivering Assets to User` has been moved to [`reference/extended.md`](reference/extended.md) to keep this skill concise. Load that reference when the task requires the moved examples, command catalogs, checklists, platform details, or implementation templates.
