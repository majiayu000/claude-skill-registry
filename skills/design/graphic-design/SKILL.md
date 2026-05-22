---
name: graphic-design
description: Professional graphic design principles for digital and print media. Use when creating visual designs, choosing color palettes, typography, layouts, or providing design feedback.
---

# Graphic Design

Comprehensive guide for creating professional visual designs across digital and print media.

## Design Fundamentals

### The 7 Principles of Design

| Principle    | Definition                  | Application                       |
| ------------ | --------------------------- | --------------------------------- |
| **Balance**  | Visual equilibrium          | Symmetrical, asymmetrical, radial |
| **Contrast** | Difference between elements | Size, color, shape, texture       |
| **Emphasis** | Focal point creation        | Hierarchy guides the eye          |
| **Movement** | Visual flow direction       | Leading lines, repetition         |
| **Pattern**  | Repetition of elements      | Creates rhythm and unity          |
| **Rhythm**   | Visual tempo                | Regular, flowing, progressive     |
| **Unity**    | Cohesive whole              | Consistent style throughout       |

---

## Color Theory

### Color Models

| Model    | Use Case        | Components                       |
| -------- | --------------- | -------------------------------- |
| **RGB**  | Digital screens | Red, Green, Blue (0-255)         |
| **CMYK** | Print media     | Cyan, Magenta, Yellow, Key/Black |
| **HSL**  | Design tools    | Hue, Saturation, Lightness       |
| **Hex**  | Web/CSS         | #RRGGBB format                   |

### Color Harmonies

```
Complementary:    Opposite on wheel (high contrast)
Analogous:        Adjacent colors (harmonious)
Triadic:          3 equidistant colors (vibrant)
Split-Comp:       Base + 2 adjacent to complement
Tetradic:         4 colors forming rectangle
Monochromatic:    Single hue, varying saturation/lightness
```

### Color Psychology

| Color      | Associations                | Use For                  |
| ---------- | --------------------------- | ------------------------ |
| **Red**    | Energy, urgency, passion    | CTAs, sales, warnings    |
| **Blue**   | Trust, calm, professional   | Corporate, tech, finance |
| **Green**  | Growth, nature, health      | Eco, wellness, money     |
| **Yellow** | Optimism, attention, warmth | Highlights, caution      |
| **Purple** | Luxury, creativity, wisdom  | Premium, creative        |
| **Orange** | Enthusiasm, confidence      | CTAs, youth brands       |
| **Black**  | Sophistication, power       | Luxury, editorial        |
| **White**  | Clean, minimal, pure        | Modern, healthcare       |

### Accessible Color Contrast

```
WCAG AA Requirements:
- Normal text: 4.5:1 minimum contrast ratio
- Large text (18pt+): 3:1 minimum
- UI components: 3:1 minimum

WCAG AAA Requirements:
- Normal text: 7:1 minimum
- Large text: 4.5:1 minimum

Tools: WebAIM Contrast Checker, Stark, Color Safe
```

---

## Typography

### Type Classification

| Category       | Characteristics     | Use Cases                |
| -------------- | ------------------- | ------------------------ |
| **Serif**      | Decorative strokes  | Print, editorial, formal |
| **Sans-serif** | Clean, no strokes   | Digital, modern, UI      |
| **Slab Serif** | Bold, blocky serifs | Headlines, branding      |
| **Script**     | Handwritten feel    | Invitations, logos       |
| **Display**    | Decorative, unique  | Headlines only           |
| **Monospace**  | Fixed-width         | Code, technical          |

### Type Hierarchy

```
Display:     48-72px  (Hero headlines)
H1:          32-48px  (Page titles)
H2:          24-32px  (Section headers)
H3:          20-24px  (Subsections)
Body:        16-18px  (Readable text)
Caption:     12-14px  (Secondary info)
Micro:       10-12px  (Legal, footnotes)
```

### Typography Rules

1. **Limit fonts**: 2-3 maximum per project
2. **Contrast pairing**: Serif + Sans-serif works well
3. **Line height**: 1.4-1.6 for body text
4. **Line length**: 45-75 characters optimal
5. **Letter spacing**: Increase for all-caps text
6. **Alignment**: Left-align body text (easier to read)

### Font Pairing Examples

```
Headlines + Body:
- Playfair Display + Source Sans Pro
- Montserrat + Merriweather
- Oswald + Lato
- Roboto Slab + Roboto
- DM Serif Display + DM Sans
```

---

## Layout & Composition

### Grid Systems

```
12-Column Grid (Most Common):
├─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┤
│1│2│3│4│5│6│7│8│9│10│11│12│

Common Column Spans:
- Full width: 12 columns
- Two-thirds: 8 columns
- Half: 6 columns
- One-third: 4 columns
- One-quarter: 3 columns
- Sidebar: 3-4 columns
```

### Spacing System (8pt Grid)

```css
/* Base unit: 8px */
--space-1: 4px; /* 0.5x - tight */
--space-2: 8px; /* 1x - base */
--space-3: 16px; /* 2x - comfortable */
--space-4: 24px; /* 3x - section gap */
--space-5: 32px; /* 4x - group separation */
--space-6: 48px; /* 6x - major sections */
--space-7: 64px; /* 8x - page sections */
--space-8: 96px; /* 12x - hero spacing */
```

### Rule of Thirds

```
┌───────┬───────┬───────┐
│       │       │       │
│   ●───┼───●   │       │  Place key elements
├───────┼───────┼───────┤  at intersection
│       │       │       │  points (●)
│   ●───┼───●   │       │
├───────┼───────┼───────┤
│       │       │       │
└───────┴───────┴───────┘
```

### Visual Hierarchy Techniques

1. **Size**: Larger = more important
2. **Color**: Bright/saturated draws attention
3. **Contrast**: High contrast = focal point
4. **Whitespace**: Isolation creates emphasis
5. **Position**: Top-left (F-pattern) or center
6. **Typography**: Bold, different font, caps

---

## File Formats

### Raster (Pixel-Based)

| Format       | Best For               | Notes                     |
| ------------ | ---------------------- | ------------------------- |
| **JPG/JPEG** | Photos, gradients      | Lossy, no transparency    |
| **PNG**      | Graphics, transparency | Lossless, larger files    |
| **GIF**      | Simple animations      | 256 colors max            |
| **WebP**     | Web images             | Best compression, modern  |
| **AVIF**     | Web images             | Newest, best quality/size |

### Vector (Math-Based)

| Format  | Best For            | Notes                |
| ------- | ------------------- | -------------------- |
| **SVG** | Web graphics, icons | Scalable, animatable |
| **AI**  | Adobe Illustrator   | Native format        |
| **EPS** | Print, legacy       | Universal vector     |
| **PDF** | Print, documents    | Preserves vectors    |

### Export Guidelines

```
Web Graphics:
- Icons: SVG (or PNG fallback)
- Photos: WebP with JPG fallback
- Illustrations: SVG or WebP
- Resolution: 72 DPI minimum, 2x for retina

Print Graphics:
- Resolution: 300 DPI minimum
- Color: CMYK mode
- Format: PDF/X or TIFF
- Bleed: 0.125" (3mm) on all sides
```

---

## Design Tools

### Industry Standard

| Tool                  | Best For                 | Platform     |
| --------------------- | ------------------------ | ------------ |
| **Figma**             | UI/UX, collaboration     | Web, Desktop |
| **Adobe Photoshop**   | Photo editing, raster    | Desktop      |
| **Adobe Illustrator** | Vector graphics          | Desktop      |
| **Sketch**            | UI design                | macOS only   |
| **Affinity Designer** | Vector (Illustrator alt) | Desktop      |
| **Canva**             | Quick designs            | Web          |

### Free Alternatives

| Tool         | Replaces    | Platform |
| ------------ | ----------- | -------- |
| **GIMP**     | Photoshop   | Desktop  |
| **Inkscape** | Illustrator | Desktop  |
| **Photopea** | Photoshop   | Web      |
| **Vectr**    | Illustrator | Web      |

---

## Design Systems

### Component Structure

```
Atoms:
- Colors, typography, icons
- Buttons, inputs, labels

Molecules:
- Form fields (label + input + helper)
- Cards (image + title + description)
- Navigation items

Organisms:
- Header (logo + nav + actions)
- Forms (multiple fields + submit)
- Product cards grid

Templates:
- Page layouts
- Grid structures

Pages:
- Specific instances with real content
```

### Naming Conventions

```
Colors:
- primary, secondary, accent
- success, warning, error, info
- gray-100 through gray-900
- background, surface, text

Components:
- btn-primary, btn-secondary, btn-ghost
- card-default, card-elevated, card-outlined
- input-default, input-error, input-disabled
```

---

## Print Design Specifics

### Standard Print Sizes

```
US Paper:
- Letter: 8.5" × 11"
- Legal: 8.5" × 14"
- Tabloid: 11" × 17"

International (ISO):
- A4: 210 × 297mm
- A3: 297 × 420mm
- A5: 148 × 210mm

Business Cards:
- US: 3.5" × 2"
- EU: 85 × 55mm
```

### Print Checklist

- [ ] CMYK color mode
- [ ] 300 DPI resolution minimum
- [ ] Bleed area included (0.125")
- [ ] Safe zone for text (0.25" from trim)
- [ ] Fonts outlined or embedded
- [ ] Rich black for large areas: C60 M40 Y40 K100

---

## Best Practices

### DO:

- Start with sketches/wireframes
- Use consistent spacing system
- Test designs at actual size
- Get feedback early and often
- Design for accessibility first
- Use real content when possible
- Create style guides/design systems

### DON'T:

- Use more than 3 fonts
- Rely on color alone for meaning
- Ignore whitespace
- Stretch or distort images
- Use low-resolution images
- Center-align long paragraphs
- Forget mobile/responsive design

---

## Design Review Checklist

- [ ] Visual hierarchy clear
- [ ] Color contrast passes WCAG
- [ ] Typography readable at all sizes
- [ ] Consistent spacing throughout
- [ ] Alignment precise (use grids)
- [ ] Images high quality and appropriate
- [ ] Brand consistency maintained
- [ ] Responsive/adaptive design considered
