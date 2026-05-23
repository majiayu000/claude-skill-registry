---
name: sentient-brand-guidelines
description: Applies Sentient.io's official brand colors, typography, and logo standards to product marketing materials including brochures, landing pages, presentations, and digital assets. Use when creating any Sentient.io branded content.
license: Proprietary - Sentient.io Brand Guidelines v1.5-AI
---

# Sentient.io Brand Styling

## Overview

This skill provides access to Sentient.io's official brand identity, color system, typography, logo usage rules, and document composition standards for AI-driven design generation.

**Keywords**: Sentient.io branding, corporate identity, visual identity, brand colors, typography, logo guidelines, AI platform branding, product marketing, design system

---

## Brand Guidelines

### 1. Logo Usage

**Approved Logo Variants:**

- **Horizontal with tagline**: Default for cover pages, main banners, posters
- **Vertical with tagline**: Use when space is limited
- **Horizontal no tagline**: Internal pages, small spaces, alongside third-party logos
- **Vertical no tagline**: Compact placements or secondary contexts

**Safe Margin:**
- Maintain clear space ≥ height of "S" in "Sentient.io"

**Minimum Sizes:**

| Use Case | On Screen | Print |
|----------|-----------|-------|
| Horizontal w/ tagline | 258 px | 50 mm |
| Horizontal no tagline | 200 px | 35 mm |
| Vertical w/ tagline | 120 px | 30 mm |
| Vertical no tagline | 86 px | 22 mm |

**Background Rules:**
- Use **white** or **light gray** backgrounds whenever possible
- On **dark backgrounds**, use **white text (#FFFFFF)** inside the logo
- Ensure sufficient contrast

**Prohibited:**
- ❌ No stretching, warping, rotation, or visual effects
- ❌ Do not rearrange elements or use logo in a sentence
- ❌ Avoid busy or low-contrast backgrounds

**Available Logo Assets:**

The following official logo files are included in this skill:

| Logo Variant | File Path | Use Cases |
|--------------|-----------|-----------|
| **Horizontal No Tagline** | `logos/Sentient-io logo Horizontal No-Tagline.png` | Internal pages, small spaces, alongside third-party logos, footer placement |
| **Vertical with Tagline** | `logos/Sentient-io logo Vertical Tagline.png` | Space-limited layouts, cover pages (vertical format), main banners (vertical orientation) |

**AI Usage Instructions:**
- When generating designs, reference these file paths to insert the appropriate logo
- Choose **Horizontal No Tagline** for secondary placements (headers, footers, internal pages)
- Choose **Vertical with Tagline** for primary placements in vertical layouts or when space constraints require vertical orientation
- For missing variants (Horizontal with Tagline, Vertical No Tagline), request from user or note unavailability

---

### 2. Color System

**Primary Palette:**

| Color | RGB | HEX | CMYK | Usage |
|-------|-----|-----|------|-------|
| **Primary Red** | 160 / 2 / 2 | `#A00202` | 0 / 100 / 100 / 36 | Brand highlights, CTAs, headings |
| **Primary Beige** | 203 / 172 / 129 | `#CBAC81` | 0 / 20 / 50 / 20 | Accent backgrounds, secondary elements |
| **Primary Green** | 198 / 215 / 129 | `#C6D781` | 10 / 0 / 50 / 15 | Callouts, sidebars, accents |

**Supporting Colors:**

| Color | RGB | HEX | CMYK | Usage |
|-------|-----|-----|------|-------|
| **Dark Grey** | 66 / 65 / 67 | `#424143` | 0 / 0 / 0 / 90 | Body text, secondary headings |
| **Overlay Gold** | 174 / 152 / 66 | `#AE9842` | 32 / 38 / 78 / 8 | Highlights, overlays, accents |

**AI Design Rule:**
- Prioritize **Primary Red (#A00202) + Dark Grey (#424143)** pairing for emphasis
- Use **Primary Beige** and **Green** as accent or background tones
- Avoid overuse of red—use it sparingly for brand highlights or CTAs
- Backgrounds should remain **white or light beige (10–15% opacity)** for readability

---

### 3. Brand Name Usage

**Correct Format:**
- Always write as **Sentient.io** (uppercase "S", lowercase ".io")
- Use lowercase "sentient.io" only when preceded by the brand icon
- Do not stylize inconsistently

**Examples:**

✅ Correct: "We build with Sentient.io's AI & Data Cloud Platform."

❌ Incorrect: "We build with SentientIO" or "SENTIENT.IO"

---

### 4. Typography

**English & Latin Alphabets:**

- **Font Family**: Nunito Sans (Open Source)
- **Headings**: Nunito Sans Bold or SemiBold
- **Body Text**: Nunito Sans Regular
- **Captions**: Nunito Sans Light or Italic
- **Rule**: Maintain clean, modern, and readable text hierarchy. Avoid decorative fonts.

**Asian Languages:**

| Language | Typeface |
|----------|----------|
| Simplified Chinese | Noto Sans SC |
| Traditional Chinese | Noto Sans TC |
| Japanese | Noto Sans JP |
| Korean | Noto Sans KR |

**Important:**
- If document's primary language is Asian, use the corresponding Noto Sans font for **all characters**, including English text
- Avoid mixing Nunito Sans and Noto Sans in a single document

---

### 5. Document Composition Guidelines

**Layout Principles:**

- Maintain **consistent header/footer spacing** using Sentient.io logo (no tagline) in footers
- Use **Primary Red (#A00202)** for headings, **Dark Grey (#424143)** for body text
- Accent highlights (callouts, sidebars) may use **Primary Green (#C6D781)** or **Overlay Gold (#AE9842)**
- Backgrounds should remain **white or light beige (#CBAC81, 10–15% opacity)** for readability
- Maintain clear whitespace consistent with the logo's "S" height margin across all design elements

**Typography Hierarchy:**

| Element | Font | Size (pt) | Color | Notes |
|---------|------|-----------|-------|-------|
| **Title** | Nunito Sans Bold | 28–36 | #A00202 | Left aligned |
| **Heading 1** | Nunito Sans SemiBold | 20–24 | #424143 | Capitalize First Letters |
| **Heading 2** | Nunito Sans Medium | 16–18 | #424143 | Sentence case |
| **Body** | Nunito Sans Regular | 12–14 | #424143 | Normal spacing |
| **Caption** | Nunito Sans Light | 10 | #424143 | Italic optional |

---

## Features

### Smart Color Application

- Automatically applies Primary Red for emphasis and brand moments
- Uses Dark Grey for high-readability body text
- Cycles through Primary Beige, Green, and Overlay Gold for accents
- Maintains visual hierarchy and on-brand consistency

### Typography Management

- Applies Nunito Sans font family with appropriate weights
- Automatically detects language and switches to Noto Sans for Asian text
- Provides fallback to system fonts if Nunito Sans unavailable
- Preserves text hierarchy and readability

### Logo Placement

- Automatically places appropriate logo variant based on context
- Logo files available at: `logos/Sentient-io logo Horizontal No-Tagline.png` and `logos/Sentient-io logo Vertical Tagline.png`
- Ensures minimum size requirements are met (see Logo Usage section)
- Maintains safe margin around logo (≥ height of "S" in "Sentient.io")
- Adapts logo selection based on available space and layout orientation
- Use Horizontal No Tagline for secondary placements
- Use Vertical with Tagline for primary vertical layouts

### Layout Consistency

- Applies consistent spacing and margins
- Maintains professional symmetry across all materials
- Ensures legibility and technology-innovation company tone
- Optimizes whitespace for clean, modern aesthetic

---

## AI Compliance Rules

When generating **any document, deck, web copy, or image**:

1. ✅ Always display **Sentient.io logo** on first page or slide
   - Use `logos/Sentient-io logo Vertical Tagline.png` for vertical layouts or primary cover pages
   - Use `logos/Sentient-io logo Horizontal No-Tagline.png` for internal pages and secondary placements
   - Note: If Horizontal with Tagline is required but unavailable, request from user
2. ✅ Use **Nunito Sans** or **Noto Sans** exclusively
3. ✅ Conform all headings and color tones to this guide's defined palette
4. ✅ Reference **Sentient.io** consistently as per naming conventions
5. ✅ Ensure layout symmetry, legibility, and professional tone consistent with a **technology-innovation company**
6. ✅ Avoid overuse of red—use it sparingly for brand highlights or CTAs
7. ✅ Maintain clear whitespace consistent with the logo's "S" height margin across all design elements

---

## Technical Details

### Font Management

- **Primary Font**: Nunito Sans (weights: Light, Regular, Medium, SemiBold, Bold)
- **Asian Fonts**: Noto Sans (SC, TC, JP, KR variants)
- **Fallback**: Arial or system sans-serif for emergency cases
- For best results, ensure Nunito Sans is installed in your environment

### Color Application

- Uses RGB and HEX values for precise brand matching
- CMYK values provided for print production
- Applied via design tool's native color systems
- Maintains color fidelity across digital and print mediums

### Print Production

- Use CMYK values for all print materials
- Ensure minimum DPI of 300 for logo and images
- Include proper bleed and trim marks
- Maintain color calibration with Sentient.io's Pantone equivalents if available

### Logo Assets

**Available Files:**

1. **Horizontal No Tagline** (`logos/Sentient-io logo Horizontal No-Tagline.png`)
   - Format: PNG with transparent background
   - Minimum size: 200px (screen) / 35mm (print)
   - Best for: Internal pages, footers, secondary placements

2. **Vertical with Tagline** (`logos/Sentient-io logo Vertical Tagline.png`)
   - Format: PNG with transparent background
   - Minimum size: 120px (screen) / 30mm (print)
   - Best for: Cover pages (vertical), space-limited layouts, primary vertical placements

**Implementation Notes:**
- Always reference these file paths when inserting logos in designs
- Maintain aspect ratio at all times (no stretching or distortion)
- Ensure minimum size requirements are met for legibility
- Apply safe margin (≥ "S" height) around all logo placements
- For print production, ensure logos are at minimum 300 DPI

**Missing Variants:**
- Horizontal with Tagline (request from user if needed for cover pages/banners)
- Vertical No Tagline (request from user if needed for compact secondary placements)

---

## Usage Examples

### Presentation Slides
- Title slide: Horizontal logo with tagline, Primary Red title, white background
- Content slides: Logo in footer (no tagline), Dark Grey body text, Primary Red section headers
- Accent slides: Light Beige background (10% opacity), Primary Green for callouts

### Brochures
- Cover: Large horizontal logo with tagline, Primary Red headline
- Interior: Primary Beige accents, Dark Grey body copy, Nunito Sans hierarchy
- Back: Logo (no tagline), Primary Red CTA

### Landing Pages
- Hero: White background, Primary Red CTA buttons, Nunito Sans Bold headers
- Sections: Alternating white and light Beige backgrounds
- Trust elements: Overlay Gold for highlights, Primary Green for success states

### Documents
- Header: Sentient.io logo (horizontal, no tagline) in top-left
- Typography: Follow hierarchy table strictly
- Margins: Minimum equal to "S" height in logo
- Colors: Primary Red for emphasis only, Dark Grey for all text

---

## Brand Essence

**Positioning**: Technology-innovation company specializing in AI & Data Cloud Platform

**Visual Tone**: Professional, modern, trustworthy, technically sophisticated

**Emotional Goal**: Inspire confidence, demonstrate expertise, reduce complexity

**Differentiation**: Bold yet balanced use of red, clean typography, generous whitespace