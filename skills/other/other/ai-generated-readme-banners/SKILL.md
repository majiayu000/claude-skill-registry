---
name: "ai-generated-readme-banners"
description: "Create professional ultra-wide cinematic banners for GitHub READMEs using Flux and Ideogram models with typography options"
---

# AI-Generated README Banners

> Ultra-wide cinematic project branding — from ASCII art to professional visuals in minutes.

---

## Core Pattern

**Problem**: ASCII art and SVG banners are limited; professional banner design is expensive and time-consuming.

**Solution**: Generate ultra-wide photorealistic banners using Ideogram v2 with crystal-clear typography, professional composition, and project-specific branding in minutes.

**Quality**: Ideogram v2 produces stunning photorealistic results with perfect text rendering — far exceeding expectations for AI-generated imagery.

---

## Implementation Strategy

### 1. Aspect Ratio Selection

**Flux-supported ratios** (2026):
- ✅ `21:9` — Ultra-wide cinematic (best for README banners)
- ✅ `16:9` — Standard widescreen
- ❌ `16:3` — NOT supported (causes 422 validation error)

**Recommendation**: Use `21:9` for maximum banner width within API constraints.

### 2. Model Selection

| Model | Cost | Best For | Typography | Quality |
|-------|------|----------|------------|----------|
| **Flux Schnell** | $0.003 | Testing, iteration | No text | Good |
| **Flux 1.1 Pro** | $0.04 | Production (clean) | No text | Excellent |
| **Ideogram v2** | $0.08 | Production (with text) | ✅ Crystal clear | **Stunning** |

**Workflow**:
- **Clean banners**: Test with Schnell → Refine → Generate with Pro
- **Typography banners**: Use Ideogram v2 (exceptional quality, perfect text rendering)

**Reality Check**: Ideogram v2 quality is amazing — photorealistic 3D rendering with perfect typography integration. The $0.08 cost is a bargain for professional-grade output.

---

## Banner Prompt Engineering

### Compositional Structure for Ultra-Wide Format

```
- Left side: Main character/protagonist (1/3)
- Center: Thematic element/focal point (1/3)
- Right side: Environmental/world context (1/3)
```

### Example Prompt Structure

```
Cinematic ultra-wide banner illustration for "[PROJECT NAME]" header.
[Genre/aesthetic description]

COMPOSITION (21:9 ultra-wide cinematic format):
- Left: [Character with specific details]
- Center: [Thematic focal point]
- Right: [Environment, atmosphere]

LIGHTING:
- [Specific techniques for each zone]

STYLE:
- [Art direction, realism level]

COLOR PALETTE:
- [Dominant colors, accents]

MOOD: [Emotional tone]
```

---

## Typography Banners (Ideogram)

### When to Add Text

- ✅ Project title needs immediate visibility
- ✅ Brand recognition through typography
- ✅ Standalone banner for social sharing
- ❌ Text changes frequently
- ❌ Multi-language support needed

### Ideogram-Specific Parameters

**Critical**: Case-sensitive parameter values!

```javascript
const input = {
  prompt: BANNER_PROMPT,
  aspect_ratio: '3:1',                  // Ideogram's widest (NOT '21:9')
  magic_prompt_option: 'On',            // Must be 'On', 'Off', or 'Auto' (capitalized!)
  style_type: 'Realistic',              // Options: 'Realistic', 'General', 'Design', etc.
  resolution: '1536x512',               // Specific dimensions (not '1440p')
  output_format: 'png',
};
```

### Common Ideogram Mistakes

- ❌ `magic_prompt_option: 'ON'` → Must be `'On'` (case-sensitive)
- ❌ `style_type: 'CINEMATIC'` → Invalid, use `'Realistic'`
- ❌ `aspect_ratio: '21:9'` → Ideogram doesn't support this, use `'3:1'`

### Ideogram URL Handling Quirk

```javascript
// Ideogram returns URL as getter function, not string
let imageUrl;
if (output && typeof output.url === 'function') {
  imageUrl = output.url().toString();
} else if (typeof imageUrl === 'object' && imageUrl.href) {
  imageUrl = imageUrl.href;
}
```

### Typography Prompt Pattern (Validated)

**Structure**: Use clear labeled sections in your prompt for best results.

```
Professional technology banner (3:1 ultra-wide format).

TITLE TEXT (large, centered):
"[EXACT TEXT]"
- Bold modern sans-serif, uppercase
- [Color specification or gradient]
- Crystal clear, perfectly legible
- Sharp crisp lettering

SUBTITLE TEXT (below title):
"[Exact subtitle]"
- Clean font, [color]
- Readable professional typography

[VISUAL ELEMENTS]:
- [Specific objects, positioned where]
- [Prominent features, branding elements]
- Photorealistic 3D rendering

BOTTOM [CORNER] (optional):
- [Logo mark description]
- "[Brand text]" in [color]

BACKGROUND COMPOSITION (3:1 ultra-wide):
- [Gradient colors with hex codes]
- [Atmospheric elements: stars, particles, etc.]
- [Lighting effects: glows, halos]

LIGHTING:
- [Specific lighting techniques]
- [Glow sources and colors]
- Modern cinematic quality

COLOR PALETTE:
- Background: [hex codes]
- Accents: [hex codes]
- Text: [color with effects]

STYLE:
- Photorealistic 3D rendering
- [Aesthetic description]
- Sharp detail, cinematic quality

TEXT QUALITY CRITICAL:
- Crystal clear text rendering
- No distortion whatsoever
- Perfect spelling: "[EXACT TEXT]"
- Professional typographic hierarchy

MOOD: [Emotional tone, brand feeling]
```

**Key Principles**:
1. **Explicit spelling in quotes** — always specify exact text
2. **Structured sections** — TITLE TEXT, SUBTITLE TEXT, BACKGROUND, etc.
3. **Crystal clear demands** — "crystal clear", "sharp", "perfectly legible"
4. **Hex color codes** — specific colors (#0078d4) for brand consistency
5. **Layout variations** — left-aligned, centered, right-aligned for variety
6. **Photorealistic 3D** — emphasize render quality in prompt
7. **TEXT QUALITY CRITICAL section** — reinforces typography requirements

---

## Layout Variations Strategy

**Generate multiple composition variations** for visual comparison:

1. **Left-aligned** — Visual element on left, text on right
2. **Centered** — Centered focal point, text below
3. **Right-aligned** — Visual element on right, text on left

**Benefits**:
- Side-by-side comparison for stakeholder review
- Audience targeting (different focus areas per banner)
- A/B testing on social media
- Seasonal/campaign variations

**Cost**: 3 variations × $0.08 = $0.24 (validated)

**Example**: Alex Cognitive Architecture generated:
- Typography focus: ALEX, LEARN·REMEMBER·GROW, COGNITIVE SYMBIOSIS
- Audience focus: CODE (developers), LEARNING (students), CAREER (professionals)
- Layout variations: Left, centered, right rocket compositions

---

## Cost Comparison

### With Typography (Ideogram)
- Single generation: $0.08
- Three layout variations: $0.24
- **Quality**: Stunning photorealistic output
- **Use case**: Fixed branding, professional presence, social sharing

### Without Typography (Flux + Markdown)
- Banner: $0.003-$0.04
- Text: Free (markdown overlay)
- **Quality**: Excellent clean visuals
- **Use case**: Frequent text changes, multi-language support

**Recommendation**:
- **Professional branding**: Ideogram with text ($0.08-$0.24, exceptional quality)
- **Iterative projects**: Flux clean + markdown ($0.003-$0.04, flexible)
- **Comparison shopping**: Generate 3 variations for visual selection

---

## Script Templates

### Clean Banner (Flux)

```javascript
const input = {
  prompt: BANNER_PROMPT,
  aspect_ratio: '21:9',
  output_format: 'png',
  output_quality: 100,
};

const output = await replicate.run('black-forest-labs/flux-schnell', { input });
```

### Typography Banner (Ideogram) — Validated Production Pattern

```javascript
import Replicate from 'replicate';
import fs from 'fs-extra';
import https from 'https';

const replicate = new Replicate({
  auth: process.env.REPLICATE_API_TOKEN,
});

const BANNERS = [
  {
    id: 'banner-variant-1',
    filename: 'banner-1.png',
    title: 'MAIN TITLE',
    subtitle: 'Subtitle text',
    prompt: `Professional technology banner (3:1 ultra-wide format).

TITLE TEXT (large, centered):
"MAIN TITLE"
- Bold modern sans-serif, uppercase
- Gradient from deep blue to vibrant purple
- Crystal clear, perfectly legible

SUBTITLE TEXT (below title):
"Subtitle text"
- Clean font, white text
- Readable professional typography

[VISUAL ELEMENTS]:
- [Describe specific visuals]
- Photorealistic 3D rendering

BACKGROUND COMPOSITION:
- Deep space gradient (#080810 → #0d1520)
- Scattered white stars
- Radial glow effects

COLOR PALETTE:
- Background: Deep blue (#0078d4), purple (#7c3aed)
- Text: White with blue glow

STYLE:
- Photorealistic 3D rendering
- Modern tech aesthetic
- Sharp detail, cinematic quality

TEXT QUALITY CRITICAL:
- Crystal clear sharp letterforms
- Perfect spelling: "MAIN TITLE"

MOOD: Inspiring, professional, cutting-edge technology`,
  },
  // Add more variations...
];

async function downloadImage(url, filepath) {
  return new Promise((resolve, reject) => {
    const file = fs.createWriteStream(filepath);
    https.get(url, (response) => {
      response.pipe(file);
      file.on('finish', () => {
        file.close();
        resolve();
      });
    }).on('error', (err) => {
      fs.unlink(filepath, () => {});
      reject(err);
    });
  });
}

async function generateBanner(banner) {
  console.log(`🎨 Generating: ${banner.title}`);
  
  const input = {
    prompt: banner.prompt,
    aspect_ratio: '3:1',
    magic_prompt_option: 'On',  // Case-sensitive!
    style_type: 'Realistic',
    resolution: '1536x512',
    output_format: 'png',
  };

  const output = await replicate.run('ideogram-ai/ideogram-v2', { input });

  // Handle Ideogram URL getter function quirk
  let imageUrl;
  if (output && typeof output.url === 'function') {
    imageUrl = output.url().toString();
  } else if (Array.isArray(output)) {
    imageUrl = output[0];
  } else if (typeof output === 'string') {
    imageUrl = output;
  } else if (output && output.url) {
    imageUrl = output.url;
  }
  
  if (typeof imageUrl === 'object' && imageUrl.href) {
    imageUrl = imageUrl.href;
  }

  await downloadImage(imageUrl, `assets/${banner.filename}`);
  console.log(`✅ Saved: ${banner.filename}`);
  
  return { ...banner, url: imageUrl };
}

// Generate all banners with rate limiting
const results = [];
for (const banner of BANNERS) {
  const result = await generateBanner(banner);
  results.push(result);
  
  // Rate limiting: 2 seconds between requests
  if (BANNERS.indexOf(banner) < BANNERS.length - 1) {
    await new Promise(resolve => setTimeout(resolve, 2000));
  }
}

// Save generation report
fs.writeJsonSync('assets/banner-generation-report.json', {
  generatedAt: new Date().toISOString(),
  model: 'ideogram-ai/ideogram-v2',
  results,
  totalCost: results.length * 0.08,
}, { spaces: 2 });

console.log(`\n✅ Generated ${results.length} banners`);
console.log(`💰 Total cost: $${(results.length * 0.08).toFixed(2)}`);
```

### Package.json Integration

```json
"scripts": {
  "generate:banner": "node scripts/generate-banner.js",
  "generate:banner-text": "node scripts/generate-banner-with-text.js"
}
```

---

## README Integration

### With Typography

```markdown
<div align="center">

![Project Name](assets/banner-with-text-ideogram.png)

**[Tagline]**

</div>

> Generate new: `npm run generate:banner-text`
```

### Without Typography

```markdown
<div align="center">

![Project Name](assets/banner-flux-schnell.png)

# Project Name

**[Tagline]**

</div>

> Generate new: `npm run generate:banner`
```

---

## Key Insights

### Structured Prompts = Better Results

**Pattern**: Use labeled sections (TITLE TEXT, BACKGROUND, LIGHTING, etc.)

**Why it works**:
- Ideogram parses structured input more reliably
- Clear hierarchy produces professional composition
- Explicit requirements prevent ambiguity
- Easier to iterate and refine specific sections

**Validated**: All 6 Alex banners used this structure with 100% success rate.

### Brand Consistency Through Hex Codes

**Technique**: Specify exact hex codes in prompts
- Background: Deep space blue (#080810 → #0d1520)
- Primary: Azure blue (#0078d4)
- Accent: Vibrant purple (#7c3aed)
- Highlight: Electric teal (#14b8a6)

**Result**: Consistent brand identity across all banner variations.

### Layout Variations for Audience Targeting

**Strategy**: Generate multiple compositions with different focus areas
- **Developer focus**: "Take Your CODE to New Heights"
- **Student focus**: "Take Your LEARNING to New Heights"  
- **Professional focus**: "Take Your CAREER to New Heights"

**Benefit**: Different banners appeal to different audience segments while maintaining cohesive brand.

### Logo Integration in Corners

**Pattern**: Position branding in bottom corners (left, center, or right)
- Small logo mark (e.g., "CX" symbol)
- Brand text nearby in gray
- Low opacity (0.6-0.7) for subtlety

**Purpose**: Professional touch without overwhelming main composition.

### Rate Limiting Best Practice

**Requirement**: 2-second delay between Replicate API calls
```javascript
await new Promise(resolve => setTimeout(resolve, 2000));
```

**Why**: Prevents rate limit errors during batch generation.

### Cost-Quality Sweet Spot

**Finding**: $0.08 per Ideogram banner is exceptional value
- Quality: Photorealistic, professional-grade output
- Speed: 10-20 seconds per generation
- Reliability: Consistent high-quality results
- ROI: 100-1000× cheaper than custom illustration

**Comparison**: Stock photo licenses ($10-$100+) vs Ideogram ($0.08)

---

## Cross-Project Applicability

✅ **Ideal use cases**:
- **GitHub README headers** — 3:1 aspect ratio perfect for repository branding
- **Project landing pages** — Professional hero sections
- **Documentation portals** — Branded headers for doc sites
- **Marketing materials** — Social sharing images, blog headers
- **Multi-variant campaigns** — A/B testing with different audience focus
- **Personal branding** — LinkedIn banners, portfolio headers

✅ **Success patterns**:
- Technology projects (modern tech aesthetic)
- Professional services (photorealistic quality)
- Open source projects (cost-effective branding)
- Startups (rapid iteration, multiple variants)

❌ **Not ideal**:
- Social media posts (need 1:1, 4:5, 16:9 ratios)
- Book covers (need portrait 2:3, 4:5)
- Character references (need square 1:1)
- Frequent text changes (use Flux + markdown instead)

**Adaptation tip**: For social media, generate 3:1 banner first, then crop/resize to other aspect ratios in post-production.

---

## Real-World Validation

**Alex Cognitive Architecture** (February 2026):
- ✅ 6 Ideogram v2 banners generated
- ✅ Typography banners: ALEX, LEARN·REMEMBER·GROW, COGNITIVE SYMBIOSIS
- ✅ Rocket banners: CODE, LEARNING, CAREER focus areas
- ✅ Multiple layout variations: left, center, right compositions
- ✅ Perfect text rendering with brand colors (#0078d4, #7c3aed, #14b8a6)
- ✅ Total cost: $0.48 for 6 stunning photorealistic banners
- ✅ Quality assessment: **Amazing** — far exceeded expectations

**Alex in Wonderland** (January 2026):
- ✅ Character illustration with Flux
- ✅ Genre blending experimentation
- ✅ Cost optimization workflow

**Key Learning**: Ideogram v2 is the gold standard for typography banners. The quality is worth every penny of the $0.08 cost.
