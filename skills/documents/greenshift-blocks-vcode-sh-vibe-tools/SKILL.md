---
name: greenshift-blocks
description: Generate WordPress Gutenberg blocks using Greenshift/GreenLight plugin.
  Use when user asks to create WordPress sections, blocks, layouts, hero sections,
  galleries, or any Gutenberg element. Triggers o
---

---
name: greenshift-blocks
description: Generate WordPress Gutenberg blocks using Greenshift/GreenLight plugin. Use when user asks to create WordPress sections, blocks, layouts, hero sections, galleries, or any Gutenberg element. Triggers on keywords: wordpress, gutenberg, greenshift, section, block, layout, hero, gallery, columns, element.
---

# Greenshift Block Generator

## Purpose

Generate production-ready WordPress Gutenberg blocks using Greenshift/GreenLight Element block system. All output is HTML with JSON parameters in block comments - ready to paste directly into WordPress Gutenberg code editor.

## Documentation Structure

Detailed documentation is split into modular files in the `docs/` directory:

| File | Topic |
|------|-------|
| `docs/00-index.md` | Navigation index |
| `docs/01-core-structure.md` | Block format, JSON parameters, content types, styleAttributes |
| `docs/02-attributes.md` | HTML attributes, links, images, forms, icons |
| `docs/03-layouts.md` | Sections, columns, flexbox configurations |
| `docs/04-styling-advanced.md` | Local classes (dynamicGClasses), gradients, background images, parallax |
| `docs/05-animations.md` | AOS animations, CSS keyframes, scroll animations |
| `docs/06-slider.md` | Swiper slider block configuration |
| `docs/07-dynamic-content.md` | Dynamic text, query grids, placeholders |
| `docs/08-variations.md` | Accordion, tabs, counter, countdown, etc. |
| `docs/09-css-variables.md` | All CSS variables (fonts, spacing, shadows, etc.) |
| `docs/10-scripts.md` | Custom JavaScript and GSAP integration |
| `docs/11-charts.md` | ApexCharts integration |
| `docs/12-migration-rules.md` | **CRITICAL** - Typography stripping, semantic headings, minimal styling |

**Read relevant docs files when you need detailed information on specific topics.**

**IMPORTANT:** Always read `docs/12-migration-rules.md` when migrating or cloning blocks - it contains critical rules about what styles to REMOVE.

---

## Quick Reference

### Core Block Structure

Every Greenshift element follows this pattern:

```html
<!-- wp:greenshift-blocks/element {JSON Parameters} -->
<html_tag class="optional classes" ...attributes>
  <!-- Inner content -->
</html_tag>
<!-- /wp:greenshift-blocks/element -->
```

### Critical Rules

1. **Block IDs**: Unique `id` starting with `gsbp-` + 7 alphanumeric chars (e.g., `gsbp-b3c761b`). `localId` must be identical to `id`.

2. **Content Types** (`type` parameter):
   - `"text"`: Text-only blocks - requires `textContent` with duplicated text
   - `"inner"`: Container blocks - wrap plain text in `<span>` element blocks
   - `"no"`: Empty/spacer elements
   - `"chart"`: ApexCharts

3. **Styling** (`styleAttributes`):
   - Never use inline `style="..."` attributes
   - Properties use camelCase (e.g., `backgroundColor`, `paddingTop`)
   - Values are arrays for responsive: `["desktop", "tablet", "mobile_landscape", "mobile_portrait"]`
   - Single value `["10px"]` applies to all breakpoints
   - Pseudo-states: `backgroundColor_hover`, `color_focus`
   - If `styleAttributes` exists, add `localId` to HTML `class` attribute

4. **HTML Tags**: Default is `div`. Prefer `tag: "a"` over `tag: "button"` for buttons (except forms).

5. **Images**: Always `loading="lazy"`. Use `https://placehold.co/WIDTHxHEIGHT`. When using `originalWidth` and `originalHeight` in JSON, you MUST also add matching `width` and `height` HTML attributes to the `<img>` tag.

6. **Links**: `linkNewWindow: true` = `target="_blank"` + auto `rel="noopener"`

7. **Column Children with Padding**: Always add `boxSizing: ["border-box"]` to column children that have padding. Without this, padding adds to width and causes columns to wrap unexpectedly. See `docs/03-layouts.md` for details.

**See `docs/01-core-structure.md` and `docs/02-attributes.md` for full details.**

---

## Minimal Intervention Philosophy

### Core Principle: Less is More

When generating or migrating blocks, apply **minimal styling intervention**. Let the WordPress theme handle defaults.

**See `docs/12-migration-rules.md` for comprehensive migration-specific rules.**

### What NOT to Do

| Avoid | Why |
|-------|-----|
| Adding `fontSize` to headings (h1-h6) | Theme typography handles heading sizes |
| Adding `color` to headings/paragraphs | Theme colors cascade from settings |
| Adding `fontWeight` to headings | Theme defines heading weights |
| Adding `fontWeight: ["400"]` anywhere | It's the default - remove it |
| Adding `lineHeight` to headings | Theme handles heading line-heights |
| Setting responsive fontSize on headings | Theme's heading styles are already responsive |
| Using generic background colors | Use theme palette variables (palette-color-6, etc.) |

### Typography Rules (CRITICAL)

**Headings (h1, h2, h3, h4, h5, h6) - NEVER SET:**
- `fontSize` - theme handles heading sizes (even responsive ones)
- `fontWeight` - theme handles heading weights
- `color` - theme handles text colors (unless on dark background)
- `lineHeight` - theme handles heading line-heights

**Headings - OKAY TO SET:**
- `marginTop`, `marginBottom` - for spacing control
- `textAlign` - for layout/centering

**WRONG - Over-styled heading:**
```json
{
  "tag": "h2",
  "styleAttributes": {
    "fontSize": ["3rem", "2.7rem"],
    "fontWeight": ["700"],
    "lineHeight": ["1.2"]
  }
}
```

**CORRECT - Minimal heading:**
```json
{
  "tag": "h2",
  "styleAttributes": {
    "marginBottom": ["1rem"],
    "textAlign": ["center"]
  }
}
```

**Paragraphs and text - NEVER SET:**
- `color` - unless on dark/colored background
- `fontWeight: ["400"]` or `fontWeight: ["normal"]` - these are defaults
- `lineHeight` - unless custom fontSize requires adjustment

**Paragraphs and text - OKAY TO SET:**
- `fontSize` - ONLY for intentional accent/lead text (e.g., `["1.2rem"]`)
- `fontFamily` - for specific font choices
- `fontWeight: ["700"]` - for intentionally bold body text
- `maxWidth` - for constraining text width

**Exception - Text on dark backgrounds:**
When text is over a dark background (hero overlays, dark sections, card overlays):
- White text: `"color":["var(--wp--preset--color--white, #ffffff)"]`
- Semi-transparent white: `"color":["rgba(255,255,255,0.9)"]`

### Semantic Heading Hierarchy

Use proper HTML heading levels based on content structure:

```
h1 - Page title (usually in theme header)
h2 - Main section titles (one per section)
h3 - Subsection/card titles
h4 - Minor headings within cards/subsections
```

**Example - Step Cards:**
- Section intro: `h2`
- Grid/subsection title: `h3`
- Individual step headings: `h4`

**DON'T:** Use multiple h2s in same section or h3 for minor card headings.

### Background Colors - Use Theme Palette

**WRONG - Generic variables:**
```json
"backgroundColor": ["var(--wp--preset--color--white, #ffffff)"]
"backgroundColor": ["var(--wp--preset--color--light-grey, #f8f8f8)"]
```

**CORRECT - Theme palette:**
```json
"backgroundColor": ["var(--wp--preset--color--palette-color-6, var(--theme-palette-color-6, #f5f5f4))"]
"backgroundColor": ["var(--wp--preset--color--palette-color-7, var(--theme-palette-color-7, #fafaf9))"]
"backgroundColor": ["var(--wp--preset--color--palette-color-8, var(--theme-palette-color-8, #fffffe))"]
```

Palette colors (6, 7, 8) adapt to user's theme settings. Generic colors override theme customization.

### When TO Style

- **Text on dark backgrounds** - white/light colors needed for readability
- **Structural necessity** - flexbox layouts, positioning
- **Spacing control** - gaps between sections, margins for element separation
- **Explicit design override** - screenshot shows specific non-default styling

### Hardcoded Values vs CSS Variables

**WRONG - Over-styled:**
```json
{
  "styleAttributes": {
    "fontSize": ["16px"],
    "fontWeight": ["400"],
    "lineHeight": ["1.5"],
    "color": ["#333333"],
    "marginBottom": ["20px"]
  }
}
```

**CORRECT - Minimal:**
```json
{
  "styleAttributes": {
    "marginBottom": ["var(--wp--preset--spacing--50)"]
  }
}
```
Or even better - **no styleAttributes at all** if theme defaults are acceptable.

### Column/Flexbox Spacing

For column gaps, use CSS variables:
```json
{
  "styleAttributes": {
    "columnGap": ["var(--wp--preset--spacing--60, 2rem)"],
    "rowGap": ["var(--wp--preset--spacing--60, 2rem)"]
  }
}
```

**AVOID** hardcoded gaps like `"columnGap": ["25px"]` unless specifically required.

### Migration/Cloning Rule

When migrating or cloning:
1. **Preserve structure** - keep the layout working
2. **Remove unnecessary styles** - strip redundant fontSize, fontWeight, color
3. **Convert hardcoded to variables** - but only if the value is being kept
4. **Don't add styles** - if original didn't have it, don't add it

---

## Block Types Guide

### Always Use GreenLight Element

Always use `greenshift-blocks/element` for most content. Convert old blocks to GreenLight Element:

| Old Block (AVOID) | Replace With |
|-------------------|--------------|
| `greenshift-blocks/row` | `greenshift-blocks/element` with `tag:"section"`, `align:"full"` |
| `greenshift-blocks/row-column` | `greenshift-blocks/element` with `type:"inner"` or remove entirely |
| `greenshift-blocks/heading` | `greenshift-blocks/element` with `tag:"h1/h2/h3"`, `textContent` |

### Specialized Blocks (OK to use)

These specialized blocks are acceptable:

- `greenshift-blocks/element` - GreenLight Element (primary block)
- `greenshift-blocks/swiper` - Slider/carousel
- `greenshift-blocks/querygrid` - Query loop for posts
- `greenshift-blocks/dynamic-post-image` - Dynamic featured image
- `greenshift-blocks/dynamic-post-title` - Dynamic post title
- `greenshift-blocks/meta` - Post meta data

### Heading Conversion Example

**WRONG (old `greenshift-blocks/heading`):**
```html
<!-- wp:greenshift-blocks/heading {"id":"gsbp-xxx","headingContent":"Title","spacing":{...},"typography":{...}} -->
<h2 id="gspb_heading-id-gsbp-xxx" class="gspb_heading gspb_heading-id-gsbp-xxx">Title</h2>
<!-- /wp:greenshift-blocks/heading -->
```

**CORRECT (GreenLight Element - minimal):**
```html
<!-- wp:greenshift-blocks/element {"id":"gsbp-xxx","textContent":"Title","tag":"h2","localId":"gsbp-xxx","styleAttributes":{"marginBottom":["var(\u002d\u002dwp\u002d\u002dpreset\u002d\u002dspacing\u002d\u002d50, 1.5rem)"]}} -->
<h2 class="gsbp-xxx">Title</h2>
<!-- /wp:greenshift-blocks/element -->
```

**Key differences:**
- Use `textContent` instead of `headingContent`
- Use `tag:"h2"` instead of default div
- **NO fontSize** - theme handles heading sizes
- **NO color** - theme handles text colors
- Only add `marginBottom` if spacing control needed
- Class is `gsbp-xxx` not `gspb_heading gspb_heading-id-gsbp-xxx`
- No `id` attribute in HTML, only `class`

---

## SVG Icons Encoding

SVG content inside the JSON `icon.icon.svg` parameter MUST use Unicode escape sequences, not raw HTML or escaped quotes.

### Character Encoding Table

| Character | Escape Sequence |
|-----------|-----------------|
| `<`       | `\u003c`        |
| `>`       | `\u003e`        |
| `"`       | `\u0022`        |

### Example

**WRONG:**
```json
"icon":{"icon":{"svg":"<svg viewBox=\"0 0 24 24\"><path d=\"M8 12l2 2\"/></svg>"},...}
```

**CORRECT:**
```json
"icon":{"icon":{"svg":"\u003csvg viewBox=\u00220 0 24 24\u0022\u003e\u003cpath d=\u0022M8 12l2 2\u0022/\u003e\u003c/svg\u003e"},...}
```

---

## Card Design Pattern: Inset Rounded Images

When creating cards with images that have rounded corners INSIDE the card (with visible margin/padding around them):

### Structure
```
Card Wrapper (white bg, border-radius: 15px, overflow: hidden)
├── Image Container (padding: 8px top/left/right, 0px bottom)
│   └── Image (border-radius: 10px on ALL 4 corners, object-fit: cover)
└── Footer/Label Area (padding for content)
```

### Key Points

1. **Card wrapper**: `overflow: hidden` + larger border-radius (e.g., 15px)
2. **Image container**: padding on 3 sides, `paddingBottom: 0px` (no gap to footer)
3. **Image itself**: SMALLER border-radius than card (e.g., 10px) on ALL 4 corners
4. This creates the "inset" look where white card background shows as margin around image

### Image styleAttributes for Inset Cards

```json
"styleAttributes": {
  "width": ["100%"],
  "aspectRatio": ["16/10"],
  "objectFit": ["cover"],
  "borderTopLeftRadius": ["var(--wp--custom--border-radius--small, 10px)"],
  "borderTopRightRadius": ["var(--wp--custom--border-radius--small, 10px)"],
  "borderBottomLeftRadius": ["var(--wp--custom--border-radius--small, 10px)"],
  "borderBottomRightRadius": ["var(--wp--custom--border-radius--small, 10px)"],
  "borderRadiusLink_Extra": true
}
```

---

## Common CSS Variables

### Font Sizes
```
var(--wp--preset--font-size--mini, 11px)
var(--wp--preset--font-size--xs, 0.85rem)
var(--wp--preset--font-size--s, 1rem)
var(--wp--preset--font-size--m, 1.35rem)
var(--wp--preset--font-size--l, 1.55rem)
var(--wp--preset--font-size--xl, clamp(1.6rem, 2.75vw, 1.9rem))
var(--wp--preset--font-size--grand, clamp(2.2rem, 4vw, 2.8rem))
var(--wp--preset--font-size--giga, clamp(3rem, 5vw, 4.5rem))
var(--wp--preset--font-size--giant, clamp(3.2rem, 6.2vw, 6.5rem))
```

### Spacing
```
var(--wp--preset--spacing--40, 1rem)
var(--wp--preset--spacing--50, 1.5rem)
var(--wp--preset--spacing--60, 2.25rem)
var(--wp--preset--spacing--70, 3.38rem)
var(--wp--preset--spacing--80, 5.06rem)
```

### Border Radius
```
var(--wp--custom--border-radius--mini, 5px)
var(--wp--custom--border-radius--small, 10px)
var(--wp--custom--border-radius--medium, 15px)
var(--wp--custom--border-radius--large, 20px)
```

### Shadows & Transitions
```
var(--wp--preset--shadow--soft, 0px 15px 30px 0px rgba(119, 123, 146, 0.1))
var(--wp--preset--shadow--elegant, 0px 5px 23px 0px rgba(188, 207, 219, 0.35))
var(--wp--custom--transition--ease, all 0.5s ease)
var(--wp--custom--transition--smooth, all 1s cubic-bezier(0.66,0,0.34,1))
```

**See `docs/09-css-variables.md` for complete list.**

---

## Common Patterns

### Page Wrapper (for multi-section pages)

**ALWAYS** wrap full pages in a single container. This is critical for controlling spacing.

**Why Page Wrapper is essential:**
- **Eliminates unwanted gaps** - WordPress/themes often add margins between blocks
- **Unified control** - one place to manage page-level spacing
- **Prevents theme interference** - overrides default block margins
- **Consistent structure** - predictable behavior across themes

```html
<!-- wp:greenshift-blocks/element {"id":"gsbp-page001","type":"inner","localId":"gsbp-page001","align":"full","styleAttributes":{"marginBlockStart":["0px"]},"metadata":{"name":"Page Wrapper"}} -->
<div class="gsbp-page001 alignfull">
  <!-- All sections go here -->
</div>
<!-- /wp:greenshift-blocks/element -->
```

**Key points:**
- `align:"full"` in JSON + `alignfull` in HTML class
- `marginBlockStart:["0px"]` removes top margin forced by themes
- All section wrappers go inside this container
- Sections inside should NOT have extra top/bottom margins

### Full-Width Section Wrapper
```html
<!-- wp:greenshift-blocks/element {"id":"gsbp-XXXXXXX","tag":"section","type":"inner","localId":"gsbp-XXXXXXX","align":"full","styleAttributes":{"display":["flex"],"justifyContent":["center"],"flexDirection":["column"],"alignItems":["center"],"paddingRight":["var(\u002d\u002dwp\u002d\u002dcustom\u002d\u002dspacing\u002d\u002dside, min(3vw, 20px))"],"paddingLeft":["var(\u002d\u002dwp\u002d\u002dcustom\u002d\u002dspacing\u002d\u002dside, min(3vw, 20px))"],"paddingTop":["var(\u002d\u002dwp\u002d\u002dpreset\u002d\u002dspacing\u002d\u002d80, 5rem)"],"paddingBottom":["var(\u002d\u002dwp\u002d\u002dpreset\u002d\u002dspacing\u002d\u002d80, 5rem)"],"marginBlockStart":["0px"]},"isVariation":"contentwrapper"} -->
<section class="gsbp-XXXXXXX alignfull">
  <!-- Content Area -->
</section>
<!-- /wp:greenshift-blocks/element -->
```

### Content Area (Centered Container)

**IMPORTANT:** Use `content-size` (not `wide-size`) for content width:

```html
<!-- wp:greenshift-blocks/element {"id":"gsbp-XXXXXXX","type":"inner","localId":"gsbp-XXXXXXX","styleAttributes":{"maxWidth":["100%"],"width":["var(\u002d\u002dwp\u002d\u002dstyle\u002d\u002dglobal\u002d\u002dcontent-size, 1290px)"]},"isVariation":"nocolumncontent","metadata":{"name":"Content Area"}} -->
<div class="gsbp-XXXXXXX">
  <!-- Inner content -->
</div>
<!-- /wp:greenshift-blocks/element -->
```

### Two-Column Layout
```html
<!-- wp:greenshift-blocks/element {"id":"gsbp-XXXXXXX","type":"inner","localId":"gsbp-XXXXXXX","styleAttributes":{"display":["flex"],"flexColumns_Extra":2,"flexWidths_Extra":{"desktop":{"name":"50/50","widths":[50,50]},"tablet":{"name":"50/50","widths":[50,50]},"mobile":{"name":"100/100","widths":[100,100]}},"flexDirection":["row"],"columnGap":["var(\u002d\u002dwp\u002d\u002dpreset\u002d\u002dspacing\u002d\u002d60, 2rem)"],"rowGap":["var(\u002d\u002dwp\u002d\u002dpreset\u002d\u002dspacing\u002d\u002d60, 2rem)"],"flexWrap":["wrap"]},"isVariation":"contentarea"} -->
<div class="gsbp-XXXXXXX">
  <!-- Column 1 -->
  <!-- Column 2 -->
</div>
<!-- /wp:greenshift-blocks/element -->
```

**See `docs/03-layouts.md` for more layout patterns.**

### Heading with Animation
```html
<!-- wp:greenshift-blocks/element {"id":"gsbp-XXXXXXX","textContent":"Your Heading","tag":"h2","animation":{"duration":800,"easing":"ease","type":"fade-up","onlyonce":true},"localId":"gsbp-XXXXXXX","styleAttributes":{"marginBottom":["var(\u002d\u002dwp\u002d\u002dpreset\u002d\u002dspacing\u002d\u002d50, 1.5rem)"]}} -->
<h2 data-aos="fade-up" data-aos-easing="ease" data-aos-duration="800" data-aos-once="true" class="gsbp-XXXXXXX">Your Heading</h2>
<!-- /wp:greenshift-blocks/element -->
```

**Note:** No `fontSize` or `color` on heading - theme handles typography. Only `marginBottom` for spacing.

**See `docs/05-animations.md` for all animation options.**

### Button/Link
```html
<!-- wp:greenshift-blocks/element {"id":"gsbp-XXXXXXX","textContent":"Click Here","tag":"a","localId":"gsbp-XXXXXXX","href":"#","styleAttributes":{"display":["inline-flex"],"paddingTop":["var(\u002d\u002dwp\u002d\u002dcustom\u002d\u002dbutton\u002d\u002dspacing\u002d\u002dvertical, 1rem)"],"paddingBottom":["var(\u002d\u002dwp\u002d\u002dcustom\u002d\u002dbutton\u002d\u002dspacing\u002d\u002dvertical, 1rem)"],"paddingLeft":["var(\u002d\u002dwp\u002d\u002dcustom\u002d\u002dbutton\u002d\u002dspacing\u002d\u002dhorizontal, 2rem)"],"paddingRight":["var(\u002d\u002dwp\u002d\u002dcustom\u002d\u002dbutton\u002d\u002dspacing\u002d\u002dhorizontal, 2rem)"],"backgroundColor":["var(\u002d\u002dwp\u002d\u002dpreset\u002d\u002dcolor\u002d\u002dprimary, #000)"],"color":["#fff"],"borderRadius":["var(\u002d\u002dwp\u002d\u002dcustom\u002d\u002dborder-radius\u002d\u002dmedium, 15px)"],"textDecoration":["none"],"transition":["var(\u002d\u002dwp\u002d\u002dcustom\u002d\u002dtransition\u002d\u002dease, all 0.5s ease)"],"backgroundColor_hover":["var(\u002d\u002dwp\u002d\u002dpreset\u002d\u002dcolor\u002d\u002dsecondary, #333)"]}} -->
<a class="gsbp-XXXXXXX" href="#">Click Here</a>
<!-- /wp:greenshift-blocks/element -->
```

### Image
```html
<!-- wp:greenshift-blocks/element {"id":"gsbp-XXXXXXX","tag":"img","localId":"gsbp-XXXXXXX","src":"https://placehold.co/800x600","alt":"Description","originalWidth":800,"originalHeight":600,"styleAttributes":{"width":["100%"],"height":["auto"],"objectFit":["cover"],"borderRadius":["var(\u002d\u002dwp\u002d\u002dcustom\u002d\u002dborder-radius\u002d\u002dsmall, 10px)"]}} -->
<img class="gsbp-XXXXXXX" src="https://placehold.co/800x600" alt="Description" width="800" height="600" loading="lazy"/>
<!-- /wp:greenshift-blocks/element -->
```

---

## Block Variations (`isVariation`)

| Variation | Use Case | Details |
|-----------|----------|---------|
| `"contentwrapper"` | Full-width section wrapper | See `docs/03-layouts.md` |
| `"nocolumncontent"` | Centered content area | See `docs/03-layouts.md` |
| `"contentcolumns"` / `"contentarea"` | Column layouts | See `docs/03-layouts.md` |
| `"accordion"` | Collapsible accordion | See `docs/08-variations.md` |
| `"tabs"` | Tab interface | See `docs/08-variations.md` |
| `"counter"` | Animated number counter | See `docs/08-variations.md` |
| `"countdown"` | Countdown timer | See `docs/08-variations.md` |
| `"marquee"` | Scrolling marquee | See `docs/08-variations.md` |
| `"buttoncomponent"` | Styled button | See `docs/08-variations.md` |
| `"videolightbox"` | Video with lightbox | See `docs/08-variations.md` |

---

## Animation Options

Available `animation.type` values:
- `fade`, `fade-up`, `fade-down`, `fade-left`, `fade-right`
- `zoom-in`, `zoom-in-up`, `zoom-in-down`, `zoom-out`
- `slide-up`, `slide-down`, `slide-left`, `slide-right`
- `flip-up`, `flip-down`, `flip-left`, `flip-right`
- `clip-right`, `clip-left`, `clip-up`, `clip-down`

Animation parameters: `duration` (ms), `delay` (ms), `easing`, `onlyonce` (boolean)

**See `docs/05-animations.md` for keyframe animations and scroll-linked animations.**

---

## Dynamic Content

For blocks displaying WordPress data (posts, users, taxonomies):

```html
<!-- wp:greenshift-blocks/element {"id":"gsbp-xxx","textContent":"<dynamictext></dynamictext>","dynamictext":{"dynamicEnable":true,"dynamicType":"postdata","dynamicSource":"latest_item","dynamicPostData":"post_title"},"localId":"gsbp-xxx"} -->
<div class="gsbp-xxx"><dynamictext></dynamictext></div>
<!-- /wp:greenshift-blocks/element -->
```

**See `docs/07-dynamic-content.md` for all dynamic types and query grids.**

---

## Slider Blocks

Use `greenshift-blocks/swiper` for image galleries and hero sliders.

**CRITICAL:** For image gallery slides, use `greenshift-blocks/element` with `tag:"img"` inside `slider-content-zone`. Do NOT put images directly in `slider-image-wrapper`.

**See `docs/06-slider.md` for complete slider documentation and correct structure.**

---

## Design Detail Attention Checklist

Before generating output, verify these visual details from the reference design:

### 1. Border Radius
- Card/container radius vs image/inner element radius (usually different)
- Are corners rounded on all 4 sides or specific corners only?
- Is it subtle (5-10px), medium (15px), large (20-30px), or pill (50px+)?

### 2. Padding/Margins
- Is image edge-to-edge or inset with visible container background?
- Gap between image and footer/content below
- Internal padding of content areas

### 3. Image Handling
- Does image fill container (`object-fit: cover`) or maintain aspect ratio (`object-fit: contain`)?
- Does image have its own rounded corners separate from container?
- Aspect ratio of image area
- `originalWidth`/`originalHeight` in JSON → matching `width`/`height` in HTML

### 4. Shadows
- Subtle vs prominent shadow
- Shadow on card vs shadow on image

### 5. Background Relationships
- Section background vs card background vs image background
- Overlay effects or gradients

---

## Output Validation Rules

Before outputting Greenshift blocks, verify these critical rules:

1. **No HTML comments** - Use `metadata:{"name":"..."}` instead of `<!-- Section Name -->`
2. **Page wrapper required** - Multi-section pages MUST be wrapped in element with `align:"full"` and `<div class="... alignfull">`
3. **Image dimensions** - When `originalWidth`/`originalHeight` in JSON, add matching `width`/`height` to HTML `<img>` tag
4. **SVG attributes** - Don't include `fill="none"` on outer `<svg>` element (WordPress strips it - put on `<path>` elements)
5. **Slider images** - Use `greenshift-blocks/element` blocks in `slider-content-zone`, NOT direct `<img>` in `slider-image-wrapper`
6. **Slider swipe JSON** - Use `imageurl:""` (empty string), add `bgContain:false`

---

## Output Requirements

- Return **only** the generated block code
- Block names: `wp:greenshift-blocks/element` (or specialized like `swiper`, `querygrid`)
- No explanations or surrounding text
- **No HTML comments** - WordPress strips them; use `metadata:{"name":"..."}` for organization
- Ready to paste directly into WordPress Gutenberg code editor
- Save output as `.html` files

---

## Example Templates

Reference templates are in the `templates/` directory:
- `section-wrapper.html` - Full-width section wrapper
- `two-columns.html` - Two-column responsive layout
- `hero-section.html` - Hero section with background
- `card-grid.html` - Card grid layout
