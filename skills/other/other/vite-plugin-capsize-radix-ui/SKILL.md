---
name: radix-typography
description: Set up pixel-perfect typography for Radix UI using vite-plugin-capsize-radix. Helps configure fonts, choose pairings, and integrate with your project.
---

# Radix Typography with Capsize

This skill helps you set up bulletproof typography for Radix UI applications using `vite-plugin-capsize-radix`. It generates CSS that trims the invisible whitespace above and below text (caused by font metrics), enabling pixel-perfect alignment.

## What This Plugin Does

Traditional CSS font rendering includes invisible space above and below text based on the font's ascender/descender metrics. This makes precise layouts difficult. Capsize calculates these metrics and applies CSS pseudo-elements to trim the excess, so your text sits exactly where you specify.

This plugin:
- Generates CSS that overrides Radix UI's typography variables
- Creates font stacks with metric-aware fallbacks
- Supports separate fonts for body text, headings, and code
- Handles responsive sizing (mobile vs desktop)

## Important: Spacing with Capsize

Because Capsize trims the invisible whitespace above and below text, **adjacent text elements will sit directly against each other** without any natural spacing. This is by design - it gives you precise control over layout.

You must explicitly add spacing between text elements using:
- **Flex with gap** (recommended): `<Flex direction="column" gap="2">`
- **margin/padding**: Apply to individual elements
- **Radix spacing props**: `mt`, `mb`, `my`, etc.

```tsx
// Without gap - heading and text will touch
<Flex direction="column">
  <Heading>Recipes</Heading>
  <Text>Define your chocolate recipes...</Text>
</Flex>

// With gap - natural spacing between elements
<Flex direction="column" gap="2">
  <Heading>Recipes</Heading>
  <Text>Define your chocolate recipes...</Text>
</Flex>
```

This explicit spacing model is more predictable than relying on font metrics and gives you pixel-perfect control over your layouts.

## Preserving Descenders

Capsize trims text to the cap-height (top) and alphabetic baseline (bottom). This can clip descenders (the tails of letters like "g", "y", "p") on large headings with tight line-heights.

Add the `preserve-descenders` class to keep descenders visible:

```tsx
<Heading size="9" className="preserve-descenders">
  Signal Sky
</Heading>
```

This disables the bottom trim while keeping the top tight. Use this on large display headings where you notice descender clipping.

## Installation

```bash
pnpm add vite-plugin-capsize-radix @capsizecss/metrics
```

## Quick Start

### 1. Configure the Plugin

In `vite.config.ts`:

```typescript
import { defineConfig } from "vite"
import react from "@vitejs/plugin-react"
import { capsizeRadixPlugin } from "vite-plugin-capsize-radix"

// Import metrics for your chosen fonts
import inter from "@capsizecss/metrics/inter"
import arial from "@capsizecss/metrics/arial"

export default defineConfig({
  plugins: [
    react(),
    capsizeRadixPlugin({
      outputPath: `./public/typography.css`,
      defaultFontStack: [inter, arial],
    }),
  ],
})
```

### 2. Install Fonts via Fontsource

For open source fonts, use [@fontsource](https://fontsource.org/):

```bash
pnpm add @fontsource/inter
```

### 3. Import CSS in Correct Order

In your entry file (e.g., `main.tsx`), the import order matters:

```typescript
// 1. Radix base styles FIRST
import "@radix-ui/themes/styles.css"

// 2. Your font CSS from Fontsource
import "@fontsource/inter/latin.css"

// 3. Generated typography CSS LAST (overrides Radix variables)
import "/typography.css"

// 4. Your app styles
import "./App.css"
```

**Critical**: The generated typography CSS must come AFTER `@radix-ui/themes/styles.css` to properly override the CSS variables.

## Using Fontsource Fonts

Fontsource provides npm packages for Google Fonts and other open source fonts. Each package includes the font files and CSS.

### Installation Pattern

```bash
# Install the font package
pnpm add @fontsource/[font-name]

# Install the metrics (usually same name, check @capsizecss/metrics)
# Metrics are included in @capsizecss/metrics
```

### Import Patterns

```typescript
// Full font (all weights, styles, subsets)
import "@fontsource/inter"

// Specific subset (recommended for performance)
import "@fontsource/inter/latin.css"

// Specific weight
import "@fontsource/inter/400.css"
import "@fontsource/inter/700.css"

// Variable font (if available)
import "@fontsource-variable/inter"
```

### Common Fontsource Packages

| Font | Package | Metrics Import |
|------|---------|----------------|
| Albert Sans | `@fontsource/albert-sans` | `@capsizecss/metrics/albertSans` |
| Alegreya | `@fontsource/alegreya` | `@capsizecss/metrics/alegreya` |
| Alegreya Sans | `@fontsource/alegreya-sans` | `@capsizecss/metrics/alegreyaSans` |
| Archivo | `@fontsource/archivo` | `@capsizecss/metrics/archivo` |
| Arvo | `@fontsource/arvo` | `@capsizecss/metrics/arvo` |
| Atkinson Hyperlegible | `@fontsource/atkinson-hyperlegible` | `@capsizecss/metrics/atkinsonHyperlegible` |
| Be Vietnam Pro | `@fontsource/be-vietnam-pro` | `@capsizecss/metrics/beVietnamPro` |
| Bodoni Moda | `@fontsource/bodoni-moda` | `@capsizecss/metrics/bodoniModa` |
| Bricolage Grotesque | `@fontsource/bricolage-grotesque` | `@capsizecss/metrics/bricolageGrotesque` |
| Cabin | `@fontsource/cabin` | `@capsizecss/metrics/cabin` |
| Cabin Condensed | `@fontsource/cabin-condensed` | `@capsizecss/metrics/cabinCondensed` |
| Commissioner | `@fontsource/commissioner` | `@capsizecss/metrics/commissioner` |
| Crimson Text | `@fontsource/crimson-text` | `@capsizecss/metrics/crimsonText` |
| DM Sans | `@fontsource/dm-sans` | `@capsizecss/metrics/dmSans` |
| DM Serif Display | `@fontsource/dm-serif-display` | `@capsizecss/metrics/dmSerifDisplay` |
| DM Serif Text | `@fontsource/dm-serif-text` | `@capsizecss/metrics/dmSerifText` |
| Domine | `@fontsource/domine` | `@capsizecss/metrics/domine` |
| Epilogue | `@fontsource/epilogue` | `@capsizecss/metrics/epilogue` |
| Exo | `@fontsource/exo` | `@capsizecss/metrics/exo` |
| Figtree | `@fontsource/figtree` | `@capsizecss/metrics/figtree` |
| Fira Sans | `@fontsource/fira-sans` | `@capsizecss/metrics/firaSans` |
| Fraunces | `@fontsource/fraunces` | `@capsizecss/metrics/fraunces` |
| Geist | `@fontsource/geist-sans` | `@capsizecss/metrics/geist` |
| Instrument Sans | `@fontsource/instrument-sans` | `@capsizecss/metrics/instrumentSans` |
| Instrument Serif | `@fontsource/instrument-serif` | `@capsizecss/metrics/instrumentSerif` |
| Inter | `@fontsource/inter` | `@capsizecss/metrics/inter` |
| Josefin Sans | `@fontsource/josefin-sans` | `@capsizecss/metrics/josefinSans` |
| Lato | `@fontsource/lato` | `@capsizecss/metrics/lato` |
| Lexend | `@fontsource/lexend` | `@capsizecss/metrics/lexend` |
| Libre Baskerville | `@fontsource/libre-baskerville` | `@capsizecss/metrics/libreBaskerville` |
| Literata | `@fontsource/literata` | `@capsizecss/metrics/literata` |
| Lora | `@fontsource/lora` | `@capsizecss/metrics/lora` |
| Manrope | `@fontsource/manrope` | `@capsizecss/metrics/manrope` |
| Merriweather | `@fontsource/merriweather` | `@capsizecss/metrics/merriweather` |
| Merriweather Sans | `@fontsource/merriweather-sans` | `@capsizecss/metrics/merriweatherSans` |
| Montserrat | `@fontsource/montserrat` | `@capsizecss/metrics/montserrat` |
| Neuton | `@fontsource/neuton` | `@capsizecss/metrics/neuton` |
| Newsreader | `@fontsource/newsreader` | `@capsizecss/metrics/newsreader` |
| Open Sans | `@fontsource/open-sans` | `@capsizecss/metrics/openSans` |
| Oswald | `@fontsource/oswald` | `@capsizecss/metrics/oswald` |
| Outfit | `@fontsource/outfit` | `@capsizecss/metrics/outfit` |
| Patua One | `@fontsource/patua-one` | `@capsizecss/metrics/patuaOne` |
| Playfair Display | `@fontsource/playfair-display` | `@capsizecss/metrics/playfairDisplay` |
| Plus Jakarta Sans | `@fontsource/plus-jakarta-sans` | `@capsizecss/metrics/plusJakartaSans` |
| PT Sans | `@fontsource/pt-sans` | `@capsizecss/metrics/pTSans` |
| Quattrocento Sans | `@fontsource/quattrocento-sans` | `@capsizecss/metrics/quattrocentoSans` |
| Raleway | `@fontsource/raleway` | `@capsizecss/metrics/raleway` |
| Roboto | `@fontsource/roboto` | `@capsizecss/metrics/roboto` |
| Roboto Condensed | `@fontsource/roboto-condensed` | `@capsizecss/metrics/robotoCondensed` |
| Roboto Slab | `@fontsource/roboto-slab` | `@capsizecss/metrics/robotoSlab` |
| Rosario | `@fontsource/rosario` | `@capsizecss/metrics/rosario` |
| Sora | `@fontsource/sora` | `@capsizecss/metrics/sora` |
| Source Sans 3 | `@fontsource/source-sans-3` | `@capsizecss/metrics/sourceSans3` |
| Source Serif 4 | `@fontsource/source-serif-4` | `@capsizecss/metrics/sourceSerif4` |
| Space Grotesk | `@fontsource/space-grotesk` | `@capsizecss/metrics/spaceGrotesk` |
| Varela Round | `@fontsource/varela-round` | `@capsizecss/metrics/varelaRound` |
| Vollkorn | `@fontsource/vollkorn` | `@capsizecss/metrics/vollkorn` |
| Work Sans | `@fontsource/work-sans` | `@capsizecss/metrics/workSans` |
| Yrsa | `@fontsource/yrsa` | `@capsizecss/metrics/yrsa` |

## Plugin Configuration Options

```typescript
capsizeRadixPlugin({
  // Required: where to write the generated CSS
  outputPath: `./public/typography.css`,

  // Body text font stack (first font = primary, rest = fallbacks)
  defaultFontStack: [inter, arial],

  // Heading font stack (defaults to defaultFontStack if not specified)
  headingFontStack: [playfairDisplay, arial],

  // Code/monospace font stack
  codingFontStack: [sourceCodePro],

  // Custom text sizes (fontSize = cap-height, lineHeight = total)
  textStyles: [
    { fontSize: 9, lineHeight: 19 },   // size 1
    { fontSize: 11, lineHeight: 23 },  // size 2
    { fontSize: 12, lineHeight: 25 },  // size 3 (mobile default)
    { fontSize: 14, lineHeight: 28 },  // size 4 (desktop default)
    { fontSize: 18, lineHeight: 30 },  // size 5
    { fontSize: 24, lineHeight: 36 },  // size 6
    { fontSize: 36, lineHeight: 44 },  // size 7
    { fontSize: 48, lineHeight: 52 },  // size 8
    { fontSize: 64, lineHeight: 64 },  // size 9
  ],
})
```

## Font Pairing Recommendations

These pairings are drawn from [typography.js themes](https://github.com/KyleAMathews/typography.js), a collection of carefully designed typographic systems. Choose based on your app's personality.

### Quick Reference Table

| Theme | Body | Heading | Vibe |
|-------|------|---------|------|
| Alton | Open Sans | Domine | Professional, authoritative |
| De Young | Alegreya | Alegreya Sans | Literary, sophisticated |
| Doelger | Cabin | Arvo | Friendly, sturdy |
| Elk Glen | PT Sans | Oswald | Bold, industrial |
| Fairy Gates | Quattrocento Sans | Work Sans | Warm, inviting |
| Funston | Cabin Condensed | Patua One | Playful, distinctive |
| Grand View | Arvo | Montserrat | Modern slab, geometric |
| Irving | Yrsa | Exo | Editorial, futuristic |
| Judah | Vollkorn | Roboto Condensed | Classic, efficient |
| Kirkham | Fira Sans | Playfair Display | Elegant contrast |
| Lawton | Libre Baskerville | Raleway | Traditional meets modern |
| Legible | Fira Sans | Merriweather | Highly readable |
| Lincoln | Lora | Varela Round | Bookish, friendly |
| Moraga | Source Sans Pro | Source Sans Pro | Clean, unified |
| Noriega | Lato | Lato | Simple, warm |
| Ocean Beach | Roboto | Roboto Slab | Technical, solid |
| Parnassus | Merriweather | Merriweather Sans | Literary, premium |
| St. Annes | Source Sans 3 | Source Serif 4 | Adobe superfamily |
| Stardust | Merriweather | Josefin Sans | Dreamy, vintage |
| Stern Grove | Georgia | Montserrat | Classic body, modern heads |
| Stow Lake | Lato | Neuton | Contemporary, refined |
| Sutro | Merriweather | Open Sans | Readable, friendly |
| Twin Peaks | Crimson Text | Rosario | Book typography |
| US Web Design | Source Sans 3 | Merriweather | Government standard |

---

### Clean & Modern (SaaS, Dashboards, Tools)

**Inter** - The gold standard for UI typography
```typescript
import inter from "@capsizecss/metrics/inter"
import arial from "@capsizecss/metrics/arial"
capsizeRadixPlugin({
  outputPath: `./public/typography.css`,
  defaultFontStack: [inter, arial],
})
```

**Lato** *(Noriega theme)* - Warm, humanist sans-serif
```typescript
import lato from "@capsizecss/metrics/lato"
```

**Roboto + Roboto Slab** *(Ocean Beach theme)* - Material Design inspired
```typescript
import roboto from "@capsizecss/metrics/roboto"
import robotoSlab from "@capsizecss/metrics/robotoSlab"
capsizeRadixPlugin({
  outputPath: `./public/typography.css`,
  defaultFontStack: [roboto, arial],
  headingFontStack: [robotoSlab, georgia],
})
```

---

### Editorial & Content-Heavy (Blogs, Documentation)

**Source Serif 4 + Source Sans 3** *(St. Annes theme)* - Adobe's superfamily
```typescript
import sourceSerif from "@capsizecss/metrics/sourceSerif4"
import sourceSans from "@capsizecss/metrics/sourceSans3"
capsizeRadixPlugin({
  outputPath: `./public/typography.css`,
  headingFontStack: [sourceSerif, georgia],
  defaultFontStack: [sourceSans, arial],
})
```

**Merriweather + Merriweather Sans** *(Parnassus theme)* - Screen-optimized serif
```typescript
import merriweather from "@capsizecss/metrics/merriweather"
import merriweatherSans from "@capsizecss/metrics/merriweatherSans"
capsizeRadixPlugin({
  outputPath: `./public/typography.css`,
  defaultFontStack: [merriweather, georgia],
  headingFontStack: [merriweatherSans, arial],
})
```

**Merriweather + Open Sans** *(Sutro theme)* - Readable body, friendly headings
```typescript
import merriweather from "@capsizecss/metrics/merriweather"
import openSans from "@capsizecss/metrics/openSans"
capsizeRadixPlugin({
  outputPath: `./public/typography.css`,
  defaultFontStack: [merriweather, georgia],
  headingFontStack: [openSans, arial],
})
```

**Source Sans 3 + Merriweather** *(US Web Design Standards)* - Government-grade clarity
```typescript
import sourceSans from "@capsizecss/metrics/sourceSans3"
import merriweather from "@capsizecss/metrics/merriweather"
capsizeRadixPlugin({
  outputPath: `./public/typography.css`,
  defaultFontStack: [sourceSans, arial],
  headingFontStack: [merriweather, georgia],
})
```

**Fira Sans + Merriweather** *(Legible theme)* - Maximum readability
```typescript
import firaSans from "@capsizecss/metrics/firaSans"
import merriweather from "@capsizecss/metrics/merriweather"
capsizeRadixPlugin({
  outputPath: `./public/typography.css`,
  defaultFontStack: [firaSans, arial],
  headingFontStack: [merriweather, georgia],
})
```

---

### Bold & Distinctive (Marketing, Landing Pages)

**Fira Sans + Playfair Display** *(Kirkham theme)* - Elegant contrast
```typescript
import firaSans from "@capsizecss/metrics/firaSans"
import playfairDisplay from "@capsizecss/metrics/playfairDisplay"
capsizeRadixPlugin({
  outputPath: `./public/typography.css`,
  defaultFontStack: [firaSans, arial],
  headingFontStack: [playfairDisplay, georgia],
})
```

**Arvo + Montserrat** *(Grand View theme)* - Slab serif meets geometric
```typescript
import arvo from "@capsizecss/metrics/arvo"
import montserrat from "@capsizecss/metrics/montserrat"
capsizeRadixPlugin({
  outputPath: `./public/typography.css`,
  defaultFontStack: [arvo, georgia],
  headingFontStack: [montserrat, arial],
})
```

**Libre Baskerville + Raleway** *(Lawton theme)* - Classic meets modern
```typescript
import libreBaskerville from "@capsizecss/metrics/libreBaskerville"
import raleway from "@capsizecss/metrics/raleway"
capsizeRadixPlugin({
  outputPath: `./public/typography.css`,
  defaultFontStack: [libreBaskerville, georgia],
  headingFontStack: [raleway, arial],
})
```

**Open Sans + Domine** *(Alton theme)* - Professional authority
```typescript
import openSans from "@capsizecss/metrics/openSans"
import domine from "@capsizecss/metrics/domine"
capsizeRadixPlugin({
  outputPath: `./public/typography.css`,
  defaultFontStack: [openSans, arial],
  headingFontStack: [domine, georgia],
})
```

---

### Literary & Sophisticated (Publishing, Portfolios)

**Alegreya + Alegreya Sans** *(De Young theme)* - Designed for literature
```typescript
import alegreya from "@capsizecss/metrics/alegreya"
import alegreyaSans from "@capsizecss/metrics/alegreyaSans"
capsizeRadixPlugin({
  outputPath: `./public/typography.css`,
  defaultFontStack: [alegreya, georgia],
  headingFontStack: [alegreyaSans, arial],
})
```

**Crimson Text + Rosario** *(Twin Peaks theme)* - Classic book typography
```typescript
import crimsonText from "@capsizecss/metrics/crimsonText"
import rosario from "@capsizecss/metrics/rosario"
capsizeRadixPlugin({
  outputPath: `./public/typography.css`,
  defaultFontStack: [crimsonText, georgia],
  headingFontStack: [rosario, arial],
})
```

**Vollkorn + Roboto Condensed** *(Judah theme)* - Old-style meets modern
```typescript
import vollkorn from "@capsizecss/metrics/vollkorn"
import robotoCondensed from "@capsizecss/metrics/robotoCondensed"
capsizeRadixPlugin({
  outputPath: `./public/typography.css`,
  defaultFontStack: [vollkorn, georgia],
  headingFontStack: [robotoCondensed, arial],
})
```

**Lora + Varela Round** *(Lincoln theme)* - Bookish warmth
```typescript
import lora from "@capsizecss/metrics/lora"
import varelaRound from "@capsizecss/metrics/varelaRound"
capsizeRadixPlugin({
  outputPath: `./public/typography.css`,
  defaultFontStack: [lora, georgia],
  headingFontStack: [varelaRound, arial],
})
```

**Merriweather + Josefin Sans** *(Stardust theme)* - Dreamy, vintage feel
```typescript
import merriweather from "@capsizecss/metrics/merriweather"
import josefinSans from "@capsizecss/metrics/josefinSans"
capsizeRadixPlugin({
  outputPath: `./public/typography.css`,
  defaultFontStack: [merriweather, georgia],
  headingFontStack: [josefinSans, arial],
})
```

**Yrsa + Exo** *(Irving theme)* - Editorial meets sci-fi
```typescript
import yrsa from "@capsizecss/metrics/yrsa"
import exo from "@capsizecss/metrics/exo"
capsizeRadixPlugin({
  outputPath: `./public/typography.css`,
  defaultFontStack: [yrsa, georgia],
  headingFontStack: [exo, arial],
})
```

---

### Technical & Industrial

**PT Sans + Oswald** *(Elk Glen theme)* - Bold, industrial feel
```typescript
import pTSans from "@capsizecss/metrics/pTSans"
import oswald from "@capsizecss/metrics/oswald"
capsizeRadixPlugin({
  outputPath: `./public/typography.css`,
  defaultFontStack: [pTSans, arial],
  headingFontStack: [oswald, arial],
})
```

**Lato + Neuton** *(Stow Lake theme)* - Contemporary refinement
```typescript
import lato from "@capsizecss/metrics/lato"
import neuton from "@capsizecss/metrics/neuton"
capsizeRadixPlugin({
  outputPath: `./public/typography.css`,
  defaultFontStack: [lato, arial],
  headingFontStack: [neuton, georgia],
})
```

---

### Approachable & Friendly (Consumer Apps)

**Quattrocento Sans + Work Sans** *(Fairy Gates theme)* - Warm and inviting
```typescript
import quattrocentoSans from "@capsizecss/metrics/quattrocentoSans"
import workSans from "@capsizecss/metrics/workSans"
capsizeRadixPlugin({
  outputPath: `./public/typography.css`,
  defaultFontStack: [quattrocentoSans, arial],
  headingFontStack: [workSans, arial],
})
```

**Cabin + Arvo** *(Doelger theme)* - Friendly humanist with sturdy slab
```typescript
import cabin from "@capsizecss/metrics/cabin"
import arvo from "@capsizecss/metrics/arvo"
capsizeRadixPlugin({
  outputPath: `./public/typography.css`,
  defaultFontStack: [cabin, arial],
  headingFontStack: [arvo, georgia],
})
```

**Cabin Condensed + Patua One** *(Funston theme)* - Playful, distinctive
```typescript
import cabinCondensed from "@capsizecss/metrics/cabinCondensed"
import patuaOne from "@capsizecss/metrics/patuaOne"
capsizeRadixPlugin({
  outputPath: `./public/typography.css`,
  defaultFontStack: [cabinCondensed, arial],
  headingFontStack: [patuaOne, georgia],
})
```

**Josefin Sans** - Geometric elegance with vintage charm
```typescript
import josefinSans from "@capsizecss/metrics/josefinSans"
capsizeRadixPlugin({
  outputPath: `./public/typography.css`,
  defaultFontStack: [josefinSans, arial],
})
```

---

## Modern Fonts (2015-2025)

These fonts represent the best typography additions from the last decade, featuring variable font support and modern design sensibilities.

### Modern Sans-Serifs

**Plus Jakarta Sans** - Geometric warmth, variable font
```typescript
import plusJakartaSans from "@capsizecss/metrics/plusJakartaSans"
capsizeRadixPlugin({
  outputPath: `./public/typography.css`,
  defaultFontStack: [plusJakartaSans, arial],
})
```

**Outfit** - Clean geometric, perfect for design systems
```typescript
import outfit from "@capsizecss/metrics/outfit"
```

**Manrope** - Humanist geometric, friendly and modern
```typescript
import manrope from "@capsizecss/metrics/manrope"
```

**Sora** - Futuristic, UI-optimized
```typescript
import sora from "@capsizecss/metrics/sora"
```

**Figtree** - Clean yet friendly, great for UI
```typescript
import figtree from "@capsizecss/metrics/figtree"
```

**Space Grotesk** - Tech-forward, futuristic
```typescript
import spaceGrotesk from "@capsizecss/metrics/spaceGrotesk"
```

**Geist** - Vercel's font, optimized for code/web apps
```typescript
import geist from "@capsizecss/metrics/geist"
```

---

### Modern Serifs

**Instrument Serif + Instrument Sans** - Rising star, editorial elegance
```typescript
import instrumentSerif from "@capsizecss/metrics/instrumentSerif"
import instrumentSans from "@capsizecss/metrics/instrumentSans"
capsizeRadixPlugin({
  outputPath: `./public/typography.css`,
  headingFontStack: [instrumentSerif, georgia],
  defaultFontStack: [instrumentSans, arial],
})
```

**DM Serif Display + DM Sans** - Google/DeepMind family, cohesive
```typescript
import dmSerifDisplay from "@capsizecss/metrics/dmSerifDisplay"
import dmSans from "@capsizecss/metrics/dmSans"
capsizeRadixPlugin({
  outputPath: `./public/typography.css`,
  headingFontStack: [dmSerifDisplay, georgia],
  defaultFontStack: [dmSans, arial],
})
```

**Newsreader + Figtree** - Designed for long-form reading
```typescript
import newsreader from "@capsizecss/metrics/newsreader"
import figtree from "@capsizecss/metrics/figtree"
capsizeRadixPlugin({
  outputPath: `./public/typography.css`,
  defaultFontStack: [newsreader, georgia],
  headingFontStack: [figtree, arial],
})
```

**Literata** - Google Play Books default, exceptional for reading
```typescript
import literata from "@capsizecss/metrics/literata"
```

**Fraunces + Epilogue** - Expressive soft-serif with unique "wonk" axis
```typescript
import fraunces from "@capsizecss/metrics/fraunces"
import epilogue from "@capsizecss/metrics/epilogue"
capsizeRadixPlugin({
  outputPath: `./public/typography.css`,
  headingFontStack: [fraunces, georgia],
  defaultFontStack: [epilogue, arial],
})
```

**Bodoni Moda + Outfit** - High-fashion luxury
```typescript
import bodoniModa from "@capsizecss/metrics/bodoniModa"
import outfit from "@capsizecss/metrics/outfit"
capsizeRadixPlugin({
  outputPath: `./public/typography.css`,
  headingFontStack: [bodoniModa, georgia],
  defaultFontStack: [outfit, arial],
})
```

---

### Tech & Developer

**Space Grotesk + Space Mono** - Cohesive tech aesthetic
```typescript
import spaceGrotesk from "@capsizecss/metrics/spaceGrotesk"
import spaceMono from "@capsizecss/metrics/spaceMono"
capsizeRadixPlugin({
  outputPath: `./public/typography.css`,
  defaultFontStack: [spaceGrotesk, arial],
  codingFontStack: [spaceMono],
})
```

**Geist + Geist Mono** - Vercel's Next.js default
```typescript
import geist from "@capsizecss/metrics/geist"
import geistMono from "@capsizecss/metrics/geistMono"
capsizeRadixPlugin({
  outputPath: `./public/typography.css`,
  defaultFontStack: [geist, arial],
  codingFontStack: [geistMono],
})
```

**Be Vietnam Pro** - Neo-grotesque for tech companies
```typescript
import beVietnamPro from "@capsizecss/metrics/beVietnamPro"
```

**Bricolage Grotesque** - Editorial tech, variable width
```typescript
import bricolageGrotesque from "@capsizecss/metrics/bricolageGrotesque"
```

---

### Accessibility-Focused

**Atkinson Hyperlegible** - Braille Institute, maximizes character recognition
```typescript
import atkinsonHyperlegible from "@capsizecss/metrics/atkinsonHyperlegible"
capsizeRadixPlugin({
  outputPath: `./public/typography.css`,
  defaultFontStack: [atkinsonHyperlegible, arial],
})
```

**Lexend** - Reduces visual stress, improves reading performance
```typescript
import lexend from "@capsizecss/metrics/lexend"
```

---

### Versatile Modern Choices

**Commissioner** - Humanist with unique "flair" axis
```typescript
import commissioner from "@capsizecss/metrics/commissioner"
```

**Epilogue** - Clean variable sans, works at all sizes
```typescript
import epilogue from "@capsizecss/metrics/epilogue"
```

**Albert Sans** - Contemporary humanist warmth
```typescript
import albertSans from "@capsizecss/metrics/albertSans"
```

**Archivo** - Neo-grotesque superfamily (normal, condensed, black)
```typescript
import archivo from "@capsizecss/metrics/archivo"
```

---

### Modern Quick Reference

| Font | Type | Year | Best For | Variable |
|------|------|------|----------|----------|
| Plus Jakarta Sans | Sans | 2020 | Body/UI | Yes |
| Outfit | Sans | 2021 | Branding | Yes |
| Manrope | Sans | 2019 | UI/Body | Yes |
| Sora | Sans | 2020 | Apps/UI | Yes |
| Figtree | Sans | 2022 | UI/Body | Yes |
| Space Grotesk | Sans | 2018 | Tech/Display | No |
| Geist | Sans | 2024 | Web Apps | Yes |
| DM Sans | Sans | 2019 | Small Text | Yes |
| Instrument Sans | Sans | 2023 | Branding | Yes |
| Be Vietnam Pro | Sans | 2021 | Tech | Yes |
| Bricolage Grotesque | Sans | 2023 | Editorial | Yes |
| Instrument Serif | Serif | 2023 | Display | No |
| Newsreader | Serif | 2020 | Long-form | Yes |
| Literata | Serif | 2015 | Reading | Yes |
| DM Serif Display | Serif | 2019 | Headlines | No |
| Bodoni Moda | Serif | 2020 | Luxury | Yes |
| Fraunces | Serif | 2020 | Expressive | Yes |
| Atkinson Hyperlegible | Sans | 2021 | Accessibility | Yes |
| Lexend | Sans | 2019 | Readability | Yes |
| Commissioner | Sans | 2020 | Multilingual | Yes |
| Epilogue | Sans | 2018 | Versatile | Yes |
| Albert Sans | Sans | 2022 | Body/Heads | Yes |
| Archivo | Sans | 2017 | Headlines | Yes |

---

### System Fonts (Zero Network Requests)

For maximum performance, use system fonts. The plugin defaults to a carefully ordered system font stack:

```typescript
// No font imports needed - plugin uses built-in system font metrics
capsizeRadixPlugin({
  outputPath: `./public/typography.css`,
  // omit defaultFontStack to use system fonts:
  // Apple System, Segoe UI, Roboto, Ubuntu, Noto Sans
})
```

## Adding Custom Fonts

For fonts not in Fontsource or proprietary fonts:

### 1. Get Font Metrics

Use `@capsizecss/unpack` to extract metrics from a font file:

```bash
pnpm add -D @capsizecss/unpack
```

```typescript
// scripts/extract-metrics.ts
import { fromFile } from "@capsizecss/unpack"

const metrics = await fromFile("./fonts/MyCustomFont.woff2")
console.log(JSON.stringify(metrics, null, 2))
```

### 2. Create a Metrics File

Save the output as a TypeScript file:

```typescript
// src/fonts/my-custom-font-metrics.ts
import type { FontMetrics } from "@capsizecss/core"

const myCustomFont: FontMetrics = {
  familyName: "My Custom Font",
  category: "sans-serif",
  capHeight: 700,
  ascent: 935,
  descent: -265,
  lineGap: 0,
  unitsPerEm: 1000,
  xHeight: 520,
  xWidthAvg: 500,
}

export default myCustomFont
```

### 3. Add Font-Face CSS

```css
/* src/fonts/my-custom-font.css */
@font-face {
  font-family: "My Custom Font";
  src: url("/fonts/MyCustomFont.woff2") format("woff2");
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}
```

### 4. Configure the Plugin

```typescript
import myCustomFont from "./src/fonts/my-custom-font-metrics"
import arial from "@capsizecss/metrics/arial"

capsizeRadixPlugin({
  outputPath: `./public/typography.css`,
  defaultFontStack: [myCustomFont, arial],
})
```

### 5. Import the Font CSS

```typescript
// main.tsx
import "@radix-ui/themes/styles.css"
import "./src/fonts/my-custom-font.css"  // Your @font-face rules
import "/typography.css"                  // Generated capsize CSS
```

## Validating Your Setup

After configuration, verify:

1. **Build succeeds**: `pnpm build` generates the CSS file
2. **CSS file exists**: Check `outputPath` location
3. **Variables are overridden**: Inspect `.radix-themes` in browser DevTools
4. **Text is trimmed**: Text should align precisely to grid lines

### Common Issues

**CSS not applying**: Check import order - typography CSS must come after Radix styles

**Font not loading**: Verify Fontsource import path and that font files are bundled

**Metrics mismatch**: Ensure the metrics package matches your font version

**Missing fallback**: Always include a fallback font (arial, georgia) for consistent rendering

## Code Font Configuration

For code blocks and inline code, choose a monospace font:

| Font | Package | Metrics Import | Notes |
|------|---------|----------------|-------|
| Source Code Pro | `@fontsource/source-code-pro` | `@capsizecss/metrics/sourceCodePro` | Adobe, clean |
| Fira Code | `@fontsource/fira-code` | `@capsizecss/metrics/firaCode` | Ligatures |
| JetBrains Mono | `@fontsource/jetbrains-mono` | `@capsizecss/metrics/jetBrainsMono` | IDE-optimized |
| Geist Mono | `@fontsource/geist-mono` | `@capsizecss/metrics/geistMono` | Vercel/Next.js |
| Space Mono | `@fontsource/space-mono` | `@capsizecss/metrics/spaceMono` | Retro-tech |
| DM Mono | `@fontsource/dm-mono` | `@capsizecss/metrics/dmMono` | DeepMind family |
| IBM Plex Mono | `@fontsource/ibm-plex-mono` | `@capsizecss/metrics/ibmPlexMono` | Corporate |
| Inconsolata | `@fontsource/inconsolata` | `@capsizecss/metrics/inconsolata` | Compact |
| Roboto Mono | `@fontsource/roboto-mono` | `@capsizecss/metrics/robotoMono` | Material Design |

```typescript
import sourceCodePro from "@capsizecss/metrics/sourceCodePro"

capsizeRadixPlugin({
  outputPath: `./public/typography.css`,
  defaultFontStack: [inter, arial],
  codingFontStack: [sourceCodePro],
})
```

Don't forget to import the font CSS:
```typescript
import "@fontsource/source-code-pro/latin.css"
```

## Full Example

```typescript
// vite.config.ts
import { defineConfig } from "vite"
import react from "@vitejs/plugin-react"
import { capsizeRadixPlugin } from "vite-plugin-capsize-radix"
import playfairDisplay from "@capsizecss/metrics/playfairDisplay"
import firaSans from "@capsizecss/metrics/firaSans"
import sourceCodePro from "@capsizecss/metrics/sourceCodePro"
import georgia from "@capsizecss/metrics/georgia"
import arial from "@capsizecss/metrics/arial"

export default defineConfig({
  plugins: [
    react(),
    capsizeRadixPlugin({
      outputPath: `./public/typography.css`,
      headingFontStack: [playfairDisplay, georgia],
      defaultFontStack: [firaSans, arial],
      codingFontStack: [sourceCodePro],
    }),
  ],
})
```

```typescript
// main.tsx
import React from "react"
import ReactDOM from "react-dom/client"
import { Theme } from "@radix-ui/themes"
import App from "./App"

// CSS imports in correct order
import "@radix-ui/themes/styles.css"
import "@fontsource/playfair-display/latin.css"
import "@fontsource/fira-sans/latin.css"
import "@fontsource/source-code-pro/latin.css"
import "/typography.css"
import "./App.css"

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <Theme accentColor="indigo">
      <App />
    </Theme>
  </React.StrictMode>
)
```
