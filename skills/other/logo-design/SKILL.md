---
name: logo-design
description: Design professional, scalable logos with complete brand identity deliverables including color palettes, typography, format variations, and usage guidelines. Use when the user requests logo design or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: AI Agent Skills Community
  version: 1.0.0
---

# Logo Design

This skill enables the agent to guide the complete logo design process — from creative brief through final deliverables. The agent produces design specifications covering symbol concepts, color palettes, typography selections, and file format requirements. It applies core design principles (simplicity, scalability, memorability, versatility) to ensure logos work across digital screens, print media, favicons, and social avatars.

## Workflow

1. **Gather Brand Context**: Collect the brand name, industry, target audience, competitors, and personality attributes (e.g., "modern and approachable" vs. "luxurious and exclusive"). Ask about existing brand colors, fonts, or visual assets that must be incorporated. Determine where the logo will primarily appear — website, mobile app, packaging, signage — since this shapes format and scalability requirements.

2. **Define the Design Brief**: Synthesize the gathered information into a structured design brief that includes brand values, visual direction keywords, color preferences, and mandatory constraints. Specify the logo types needed: icon/symbol mark, wordmark (logotype), combination mark, and favicon/app icon. List required file formats and sizes upfront so deliverables are clear.

3. **Generate Concept Directions**: Produce 2-3 distinct concept directions, each with a rationale explaining how it reflects the brand. For each direction, describe the symbol or letterform treatment, the color palette (primary, secondary, accent with hex codes), and the recommended typeface pairing. Explain the visual metaphor or design logic behind each concept.

4. **Refine the Selected Concept**: Once the user selects a direction, iterate on it. Adjust proportions, letter-spacing, icon weight, and color balance. Test the design at multiple sizes — a 16x16 favicon, a 48x48 app icon, a 200px web header, and a large-format print version — to confirm legibility and visual impact at every scale.

5. **Produce Final Deliverables**: Output the complete file specification: SVG (vector master), PNG at 512x512, 256x256, 128x128, and 64x64, plus a 16x16 and 32x32 ICO favicon. Provide light-background and dark-background versions, a monochrome version, and a minimum-size guideline. Include a one-page brand mark usage guide covering clear space, minimum size, and color placement rules.

6. **Document Brand Guidelines**: Deliver a concise style reference listing the exact hex/RGB/HSL color values, the typeface names and weights, the logo safe zone (clear space equal to the height of a key letter), and explicit misuse examples (stretching, recoloring outside the palette, placing on busy backgrounds).

## Usage

Provide the agent with your brand name, a description of your business or product, your target audience, and any visual preferences. The agent will walk through the workflow above and produce a design brief, concept options, and a final specification document with all deliverables listed.

## Examples

### Example 1: Tech Startup Logo Brief and Specification

**User Request**: "Design a logo for 'NovaByte', a cloud infrastructure startup targeting enterprise DevOps teams. We want something modern, technical, and trustworthy. No specific colors yet."

**Agent Response**:

**Design Brief — NovaByte**

- **Brand personality**: Technical precision, reliability, forward-thinking innovation
- **Audience**: Enterprise DevOps engineers and CTOs
- **Competitors**: AWS, Vercel, Cloudflare — clean, geometric marks

**Concept A — Orbital Node**
A hexagonal node with three orbital paths forming an abstract "N". Conveys distributed systems and connectivity.
- Primary: `#0A2540` (deep navy) / Secondary: `#00D4AA` (electric teal) / Accent: `#F5F7FA` (cloud white)
- Typeface: Inter Bold for wordmark, Inter Regular for tagline
- Style: Geometric, minimal, flat

**Concept B — Byte Stack**
Three stacked parallelograms forming an upward arrow, representing layered infrastructure and growth.
- Primary: `#1A1A2E` (midnight) / Secondary: `#6C63FF` (vibrant indigo) / Accent: `#E0E7FF` (soft lavender)
- Typeface: Space Grotesk Bold for wordmark

**Deliverables specification**:
| Format | Sizes | Variants |
|--------|-------|----------|
| SVG | Vector master | Full color, monochrome, reversed |
| PNG | 512, 256, 128, 64 px | Light bg, dark bg |
| ICO | 32x32, 16x16 | Favicon |

**Minimum size**: Icon mark must not be rendered below 24px. Wordmark must not appear below 80px wide.
**Clear space**: Maintain padding equal to the height of the "o" in "Nova" on all sides.

### Example 2: Logo Variations for an Existing Brand

**User Request**: "We have a primary logo for 'GreenLeaf Organics' (a leaf inside a circle with the company name). Generate a complete set of variations we need for all use cases."

**Agent Response**:

**GreenLeaf Organics — Logo Variation Set**

1. **Primary combination mark**: Full circle-leaf icon + "GreenLeaf Organics" wordmark to the right. Use on website headers, business cards, and letterheads.
2. **Stacked combination mark**: Icon centered above the wordmark. Use on social media profiles, signage, and packaging labels where vertical space is available.
3. **Icon-only mark**: Circle-leaf symbol without text. Use at sizes below 48px, as app icons, and for watermarks. Ensure the icon is recognizable without the wordmark at 32x32.
4. **Wordmark only**: "GreenLeaf Organics" in the brand typeface without the icon. Use in email signatures, footer text, and inline document references.
5. **Favicon**: Simplified leaf silhouette (no circle) optimized for 16x16 and 32x32. Remove fine details that disappear at small sizes.
6. **Monochrome versions**: Solid black and solid white versions of all marks above for single-color printing, embossing, and engraving.

**File deliverables per variation**: SVG vector, PNG @1x and @2x, and for the favicon an ICO file containing both 16x16 and 32x32 sizes.

## Best Practices

- **Design for the smallest size first**: If the logo is not legible as a 16x16 favicon, it is too complex. Simplify the icon until it reads clearly at tiny sizes, then scale up.
- **Limit the color palette to 2-3 colors**: Fewer colors improve recognition, reduce printing costs, and make the monochrome version more coherent.
- **Choose typefaces that match the icon weight**: A heavy geometric icon paired with an ultra-thin serif creates visual tension. Match stroke weights between symbol and wordmark.
- **Always provide a reversed (light-on-dark) version**: Logos appear on dark backgrounds frequently — hero sections, dark mode UIs, merchandise. A reversed variant is not optional.
- **Test against competitors side by side**: Place the proposed logo next to 3-4 competitors at the same size. It should be immediately distinguishable in silhouette alone.
- **Avoid trends with short shelf lives**: Gradients, drop shadows, and hyper-detailed illustrations date quickly. Flat geometric marks and clean wordmarks age well.

## Edge Cases

- **Brand name is very long**: For names exceeding 20 characters, prioritize a strong icon mark and abbreviate or stack the wordmark. Provide a short-form version (initials or acronym) for constrained spaces.
- **Logo must work on busy photographic backgrounds**: Supply a version with a subtle knockout shape (solid background pill or circle behind the mark) so the logo remains legible on varied imagery.
- **Client has no color preference at all**: Default to a neutral palette (navy/charcoal + one accent color) and present 2-3 accent options. Avoid defaulting to blue — it is overused in tech.
- **Logo will be embroidered or engraved**: Provide a simplified version with no gradients, no strokes thinner than 1mm at production size, and a minimum of 3mm letter height.
- **Multiple sub-brands need visual cohesion**: Establish a master icon system where each sub-brand uses the same structural grid and typeface but varies in color or icon detail.
