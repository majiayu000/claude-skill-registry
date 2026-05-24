---
name: elite-powerpoint-designer
description: Create world-class PowerPoint presentations with professional design, consistent branding, sophisticated animations, and polished visual hierarchy. Use when users request presentations, slide decks, pitches, reports, or want to convert markdown to professionally designed PowerPoint with Apple/Microsoft/Google-level quality.
---

# Elite PowerPoint Designer

Transform content into world-class presentations with the design quality of Apple keynotes, Microsoft product launches, and Google I/O. This skill applies 2024-2025 presentation design trends and brand-level consistency to create stunning, professional slide decks.

## Core Design Philosophy

**Principles:**
1. **Minimalism First** - Remove everything that doesn't serve a clear purpose
2. **Bold & Clear** - Large typography, high contrast, confident colors
3. **Visual Hierarchy** - Guide attention through size, color, and spacing
4. **Consistent Branding** - Every element follows the design system
5. **Purposeful Motion** - Animations only where they add clarity or emphasis

## When to Use This Skill

- User requests a "professional presentation" or "pitch deck"
- Converting markdown or text to PowerPoint
- User mentions "world-class," "high-quality," or "brand-level" design
- Creating presentations for business, sales, product launches, or keynotes
- User wants "Apple/Microsoft/Google style" presentations
- Request includes terms: slides, deck, presentation, PowerPoint, PPTX

## Design System & Brand Styles

### Available Brand Styles

**1. Tech Keynote (Apple/Tesla Style)**
- **Colors**: Deep blacks (#000000), whites (#FFFFFF), accent blue (#0071E3)
- **Typography**: SF Pro Display (title 72-96pt), SF Pro Text (body 32-44pt)
- **Layout**: Extreme whitespace, single focal point per slide
- **Transitions**: Push, Fade (duration: 0.6s)
- **Style**: Minimalist, premium, product-focused

**2. Corporate Professional (Microsoft/IBM Style)**
- **Colors**: Navy (#003366), steel blue (#0078D4), warm gray (#F3F2F1)
- **Typography**: Segoe UI (title 54-72pt), body (24-32pt)
- **Layout**: Balanced, grid-based, data-friendly
- **Transitions**: Morph, Fade (duration: 0.8s)
- **Style**: Trustworthy, data-driven, enterprise-ready

**3. Creative Bold (Google/Airbnb Style)**
- **Colors**: Bright primaries, gradients, bold combinations
- **Typography**: Product Sans or Montserrat (title 64-84pt)
- **Layout**: Dynamic, asymmetric, playful spacing
- **Transitions**: Zoom, Reveal (duration: 0.5s)
- **Style**: Energetic, innovative, design-forward

**4. Financial Elite (Goldman Sachs/McKinsey Style)**
- **Colors**: Charcoal (#2C3E50), gold accent (#D4AF37), white
- **Typography**: Garamond or Georgia (serif, elegant)
- **Layout**: Traditional hierarchy, centered, balanced
- **Transitions**: Subtle Fade only (duration: 0.4s)
- **Style**: Sophisticated, authoritative, premium

**5. Startup Pitch (Y Combinator/500 Startups Style)**
- **Colors**: High contrast black/white with brand accent
- **Typography**: Inter or Roboto (modern sans-serif)
- **Layout**: Problem-solution focused, metric-heavy
- **Transitions**: Quick Push (duration: 0.3s)
- **Style**: Energetic, data-driven, founder-friendly

## Workflow Process

### Step 1: Analyze Content & Select Style

```python
python scripts/analyze_content.py input.md
```

**Analysis considers:**
- Content type (business, creative, technical, financial)
- Audience (executives, investors, customers, technical)
- Tone indicators in content (formal, energetic, innovative)
- Explicit style requests in frontmatter

**Auto-selects brand style** or asks user:
- Tech Keynote for product launches, demos
- Corporate Professional for business reports, proposals
- Creative Bold for marketing, design showcases
- Financial Elite for investor decks, financial reports
- Startup Pitch for fundraising, accelerator demos

### Step 2: Parse Content & Map to Templates

**Slide Type Detection:**
```markdown
# Title → title_slide (hero treatment)
## Section → chapter_intro (section divider)
### Main Points → key_message_slide (1-3 key points)
* Bullets → bullet_hierarchy_slide (visual bullets)
> Quote → quote_slide (large, impactful)
![image] → full_bleed_image (immersive)
| table | → data_visualization (auto-chart if numeric)
---metrics--- → metrics_dashboard (KPI showcase)
```

### Step 3: Apply Design System

**Typography Hierarchy:**
```
Hero Title: 72-96pt, Bold, 1.1x line height
Section Title: 54-72pt, Semibold, 1.2x line height
Slide Title: 44-54pt, Semibold, 1.3x line height
Body Large: 32-36pt, Regular, 1.4x line height
Body: 24-28pt, Regular, 1.5x line height
Caption: 18-20pt, Light, 1.6x line height
```

**Spacing System:**
```
Gutter: 100-120px from edges
Title margin-bottom: 60-80px
Section spacing: 40-60px
Paragraph spacing: 24-32px
Bullet indent: 40px
Element padding: 20-30px
```

**Color Application:**
```
Background: Brand background (usually white/black)
Primary: Titles, key elements, CTAs
Secondary: Subtitles, secondary text
Accent: Highlights, data points, emphasis
Text: 95% opacity for readability
```

### Step 4: Intelligent Template Selection

Use Office-PowerPoint-MCP-Server's 25+ templates with intelligent mapping:

**Content Type → Template**
```
Opening/Closing → title_slide, thank_you_slide
New Section → chapter_intro
Key Points (1-3) → key_metrics_dashboard
Comparison → before_after_comparison, chart_comparison
Process → process_flow, timeline_slide
Team → team_introduction
Data → data_table_slide, chart layouts
Mixed Content → two_column_text, three_column_layout
Full Image → full_image_slide
Quote/Testimonial → quote_testimonial
```

### Step 5: Apply Professional Polish

**Transitions & Animations:**
- **Slide Transitions**: 1-2 types max per deck, matching brand style
- **Duration**: 0.3s (fast), 0.6s (medium), 0.8s (slow) based on brand
- **Entrance Animations**: Fade In for text (0.4s), optional Wipe for images
- **Emphasis**: Pulse on key numbers/metrics (once, subtle)
- **Exit**: Fade Out only (0.3s)
- **Rule**: Never more than 3 animated elements per slide

**Visual Effects:**
```python
# Apply to all text boxes
shadow = {
    "distance": 2,
    "angle": 135,
    "blur": 4,
    "transparency": 60%
}

# Apply to images
overlay = {
    "gradient": "linear",
    "opacity": 20%  # for text readability
}
```

### Step 6: Consistency Validation

```python
python scripts/validate_consistency.py output.pptx
```

**Checks:**
- Font consistency (max 2 font families)
- Color palette adherence (all colors from design system)
- Spacing consistency (margins, gutters, padding)
- Template usage (appropriate for content)
- Animation timing (within brand guidelines)
- Image quality (minimum 1920x1080)

## Template Mapping Reference

### High-Impact Opening
```markdown
# Your Big Idea
## Transforming the Future of X

→ title_slide
- Title: 96pt, brand primary
- Subtitle: 36pt, brand secondary
- Background: Gradient or solid brand color
- Animation: Fade in title (0.8s), then subtitle (0.6s)
```

### Key Message (The "One Thing")
```markdown
### 94% Customer Satisfaction
Our users love the new experience

→ key_metrics_dashboard (single metric variation)
- Metric: 144pt, center, brand accent
- Context: 28pt, below metric
- Background: Clean, minimal
- Animation: Count up number (1.2s)
```

### Problem/Solution
```markdown
## The Challenge
Current systems are slow and complex

## Our Solution
Fast, simple, and intuitive

→ before_after_comparison
- Split screen: left (problem) vs right (solution)
- Visual contrast: muted left, bright right
- Icons or images to reinforce message
```

### Process or Timeline
```markdown
## Our Roadmap
1. Q1: Foundation
2. Q2: Growth
3. Q3: Scale
4. Q4: Leadership

→ timeline_slide or process_flow
- Horizontal flow with arrows
- Color progression (light to bold)
- Dates: 32pt, stages: 44pt
```

### Data Visualization
```markdown
| Quarter | Revenue | Growth |
|---------|---------|--------|
| Q1      | $2.4M   | 15%    |
| Q2      | $3.1M   | 29%    |

→ Auto-convert to chart_comparison or data_table_slide
- If trends: Line or column chart
- If comparisons: Bar chart
- If parts/whole: Pie chart (use sparingly)
- Keep it simple: 1 chart per slide
```

## Animation & Transition Guidelines

### Professional Transition Rules

**Tier 1: Always Safe (Use liberally)**
- Fade (0.6s) - Universal, elegant
- Push (0.4s) - Clean, directional
- Morph (0.8s) - PowerPoint only, sophisticated

**Tier 2: Use Sparingly (Special moments)**
- Zoom (0.5s) - Product reveals, before/after
- Reveal (0.6s) - Section transitions
- Wipe (0.5s) - Image-heavy decks

**Tier 3: Avoid (Unprofessional)**
- Ferris Wheel, Curtains, Dissolve, Origami - Never use

### Animation Best Practices

**The "AHA!" Moment Rule:**
- Pick 1-2 critical slides per deck
- Apply single emphasis animation (Pulse, Grow)
- Duration: 0.8-1.0s
- Happens once, not on loop

**Text Animation:**
```python
# Professional entrance
effect = "Fade In"
duration = 0.4
delay_between_bullets = 0.3  # If bullets, stagger
```

**Image Animation:**
```python
# Optional for product shots or key visuals
effect = "Wipe" or "Fade In"
duration = 0.6
direction = "From Bottom" # Natural, like rising
```

## Advanced Features

### Auto-Generated Section Dividers
```markdown
===
# Part Two: Growth Strategy
===

→ Auto-creates chapter_intro with:
- Full-screen background (brand gradient)
- Large centered text (84pt)
- Fade to black transition (1.0s)
```

### Smart Image Handling
```markdown
![hero](image.jpg)
![thumb](small.jpg) ![thumb](small2.jpg)

→ Detects image size/role:
- Large/hero: full_image_slide with overlay for text
- Multiple: two_column or grid layout
- Auto-crops to 16:9
- Applies subtle gradient overlay (20%) if text present
```

### Metrics Auto-Emphasis
```markdown
We achieved **94%** customer satisfaction and **$2.4M** in revenue.

→ Auto-detects numbers with emphasis:
- Extracts: 94%, $2.4M
- Creates: key_metrics_dashboard
- Animates: Count-up effect (1.2s)
- Styling: Large (144pt), brand accent color
```

## Quality Checklist

Before finalizing, ensure:

**Visual Consistency:**
- [ ] All slides use design system colors (no random colors)
- [ ] Typography follows hierarchy (no more than 4 font sizes)
- [ ] Spacing is consistent (same margins, padding throughout)
- [ ] Alignment is precise (everything lines up to grid)

**Content Clarity:**
- [ ] One main idea per slide
- [ ] Titles are clear and action-oriented
- [ ] No "walls of text" (max 6 lines body text)
- [ ] Images are high-resolution (min 1920x1080)

**Motion & Polish:**
- [ ] Transitions are consistent (1-2 types only)
- [ ] Animation duration feels natural (not too fast/slow)
- [ ] No distracting motion (failed the "boardroom test")
- [ ] Emphasis animations only on critical moments

**Brand Alignment:**
- [ ] Colors match selected brand style
- [ ] Typography matches brand style
- [ ] Layout follows brand conventions
- [ ] Overall aesthetic feels cohesive

## Examples

See `examples/` folder for:
- `tech-keynote-example.md` → `tech-keynote-output.pptx`
- `investor-pitch-example.md` → `investor-pitch-output.pptx`
- `corporate-report-example.md` → `corporate-report-output.pptx`

## Requirements

**MCP Server:** Office-PowerPoint-MCP-Server
```bash
# Install via Smithery
npx @smithery/cli install @gongrzhe/office-powerpoint-mcp-server

# Or local setup
pip install python-pptx
```

**Python Packages:**
```bash
pip install python-pptx pillow pyyaml
```

## Tips for Best Results

1. **Start with Style**: Add frontmatter to markdown with desired brand style
   ```yaml
   ---
   style: tech-keynote
   accent-color: "#0071E3"
   ---
   ```

2. **Less is More**: Aim for 1 slide per minute of presentation time

3. **Image Quality Matters**: Use high-res images (min 1920x1080, prefer 4K)

4. **Test Animations**: Preview deck to ensure transitions feel professional

5. **Print-Ready**: Design also works for PDF export (animations become static)

6. **Accessibility**: Maintain 4.5:1 contrast ratio for text readability

## Troubleshooting

**Issue**: Colors don't match brand exactly
**Solution**: Specify exact hex codes in frontmatter:
```yaml
---
colors:
  primary: "#003366"
  accent: "#0078D4"
  background: "#FFFFFF"
---
```

**Issue**: Too much animation
**Solution**: Set animation level in frontmatter:
```yaml
---
animations: minimal  # minimal, moderate, full
---
```

**Issue**: Slides too dense
**Solution**: Follow "6x6 rule" - max 6 bullets, max 6 words per bullet. Claude will auto-split content if needed.

## Next-Level Customization

Advanced users can:
- Create custom brand JSON in `templates/brands/`
- Define custom slide templates
- Add company logo to master slides
- Configure font embedding for portability

See `templates/CUSTOMIZATION.md` for details.
