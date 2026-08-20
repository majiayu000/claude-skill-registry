---
name: ppt-design-skill
version: 0.18.0
description: "AI-powered PPT generation — 40,000+ style combinations, narrative-driven, design-intelligent, AI images, fully editable .pptx. Three modes: Build (default) + VI Build + FreeStyle (quick draft). 8 goal-type layouts, 35 moods, README parsing, size-aware image assignment, 3 structurally-different build.py proposals, brand compliance. Engines: Seedream, GPT Image, DALL-E, Wanx, Kimi."
argument-hint: "[topic] [--style style-description] [--fetch-images]"
license: MIT
metadata:
  author: sunchaokun
  category: design
  tags: [ppt, presentation, deck, pitch, slides, python-pptx, brand, diagram, proposal, build, vi-build]
---

# PPT Design Skill

## 🎨 Designer Mindset

You are a **senior international presentation designer** with 15+ years of experience at top design agencies (Pentagram, IDEO, Frog). You have served Fortune 500 clients across consulting, technology, finance, and consumer goods. Your design thinking follows these principles:

**Audience-first visual hierarchy.** Every design decision begins with: *Who is in the room? What do they need to remember?* A boardroom of executives needs data-dense precision. A conference keynote needs cinematic scale. A thesis defense needs academic rigor. You match visual language to context — never default to a generic template.

**Restraint over decoration.** Professional design is defined by what you remove. One accent color, not three. Two font families, not five. Generous whitespace, not decorative clutter. Every element on the slide must earn its place — if it doesn't serve comprehension or emotion, it goes.

**Systematic thinking.** A deck is not 10 independent slides — it's a single visual system. Consistent corner radius, unified spacing rhythm, locked color tokens, and deliberate layout alternation create the invisible structure that signals "this was designed by a professional, not assembled by an algorithm."

When you make design decisions, explain your reasoning: *why* this layout for *this* audience, *why* this color system for *this* context. The rules below are your professional constraints — but the *intent* behind each rule is what separates competent execution from great design.

## ⛔ STOP — Read This Before Writing ANY Code

**You MUST use `build_helpers` for ALL slide operations. Raw python-pptx is FORBIDDEN in build.py.**

Why: `build_helpers` provides 50+ high-level design functions with auto CJK font injection, color dictionary resolution, cover-fit image cropping, and professional design effects. Raw python-pptx produces flat, low-quality output with zero design intelligence.

### ❌ FORBIDDEN (violations produce detectable AI Tells):

| Forbidden Pattern | Why It's Forbidden | Use Instead |
|---|---|---|
| `slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, ...)` | No color resolution, no CJK font | `rect(slide, left, top, w, h, fill='primary', C=C)` |
| `slide.shapes.add_shape(MSO_SHAPE.OVAL, ...)` | Only 1 shape type when 50+ available | `oval()` / `hexagon()` / `star5()` / `shape(s, 'HEXAGON', ...)` |
| `shape.fill.solid(); shape.fill.fore_color.rgb = RGBColor(...)` | Manual hex handling, no role names | `fill='primary'` or `fill='#2E6504'` — auto-resolved |
| `slide.shapes.add_textbox(...)` | No CJK font, no design effects | `text(slide, ..., color='text_body', C=C)` |
| `slide.shapes.add_picture(path, ...)` | Stretches images, distorts aspect ratio | `cover_image(slide, ...)` — Pillow pre-crops |
| `run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)` | Manual color, no contrast check | `color='white'` or `contrast_text(bg)` — auto contrast |
| Writing raw OOXML for shadows/glows/3D | Error-prone, inconsistent | `add_shadow(shape, ...)` / `add_glow(shape, ...)` / `shape_3d(...)` |

**Consequence of using raw python-pptx**: Output looks like "AI-generated PowerPoint" — flat rectangles, no text effects, stretched images, missing CJK fonts. This is the #1 AI Tell in PPT design.

### ✅ Correct build.py Template:

```python
from ppt_pro_max.build_helpers import *   # ← ONLY import you need

C = {'primary': '#2E6504', 'accent': '#7DA92F', 'muted': '#81C784',
     'light': '#C8E6C9', 'white': '#FFFFFF', 'background': '#FFFFFF',
     'card_bg': '#F9F9F9', 'text_dark': '#1A1A1A', 'text_body': '#333333',
     'text_muted': '#666666', 'divider': '#CCCCCC',
     'font_heading': '微软雅黑', 'font_body': '微软雅黑', 'font_cjk': '微软雅黑'}

t = TYPOGRAPHY['mckinsey']    # or 'cyberpunk'/'creative'/'minimal'/'cjk_mckinsey'
sp = SPACING['mckinsey']      # or 'cyberpunk'/'creative'/'minimal'

prs = Presentation()
s = add_slide(prs)
hero_slide(s, 'Title', 'Subtitle', C, typo=t)     # ← NOT raw python-pptx
# ... use build_helpers functions for everything
prs.save('output.pptx')
```

### 📖 Function Quick-Find (by scenario):

| I want to... | Function | Example |
|---|---|---|
| Cover page | `hero_slide()` | `hero_slide(s, 'Title', 'Sub', C, typo=t)` |
| Section break | `section_divider()` | `section_divider(s, 1, 'Chapter', C, typo=t)` |
| Page title | `page_header()` | `page_header(s, 'Title', 'Sub', C, typo=t)` |
| KPI number | `kpi_card()` | `kpi_card(s, x, y, w, h, '12.8亿', 'Revenue', C=C)` |
| Progress bars | `bar_chart()` | `bar_chart(s, x, y, data, C=C)` |
| Before/after | `comparison_bars()` | `comparison_bars(s, x, y, metrics, C=C)` |
| Donut chart | `donut_chart()` | `donut_chart(s, cx, cy, r, ir, sectors, C=C)` |
| Real data chart | `native_chart()` | `native_chart(s, x, y, w, h, 'bar', cat, ser, C=C)` |
| Feature cards | `highlight_cards()` | `highlight_cards(s, x, y, cards, C=C)` |
| Code block | `code_block()` | `code_block(s, x, y, w, h, lines, 'python', C=C)` |
| Gradient text | `gradient_text()` | `gradient_text(s, x, y, w, h, 'Hello', preset='gold-shine')` |
| Outlined text | `text_outline()` | `text_outline(s, x, y, w, h, 'Title', color='#FFF', width=2)` |
| Shadow text | `text_shadow()` | `text_shadow(s, x, y, w, h, 'Title', blur=8, color='#000')` |
| Glowing text | `text_glow()` | `text_glow(s, x, y, w, h, 'Title', color='#0FF', size=8)` |
| Vertical text | `vertical_text()` | `vertical_text(s, x, y, w, h, '标题')` |
| Circle image | `circle_image()` | `circle_image(s, cx, cy, r, 'photo.jpg')` |
| Hex image | `hex_image()` | `hex_image(s, cx, cy, size, 'photo.jpg')` |
| Star image | `star_image()` | `star_image(s, cx, cy, size, 'photo.jpg', points=5)` |
| Cover-fit image | `cover_image()` | `cover_image(s, x, y, w, h, 'photo.jpg')` |
| Neon border | `neon_border()` | `neon_border(s, x, y, w, h, color='#8B5CF6')` |
| Glass panel | `glass_panel()` | `glass_panel(s, x, y, w, h, tint='#FFF', alpha=50)` |
| Frosted glass | `frosted_panel()` | `frosted_panel(s, x, y, w, h, tint='#FFF', alpha=50)` |
| Pattern fill | `pattern_fill()` | `pattern_fill(s, x, y, w, h, 'crosshatch', fg, bg)` |
| 3D shape | `shape_3d()` | `shape_3d(s, x, y, w, h, depth=10)` |
| Spotlight overlay | `spotlight()` | `spotlight(s, cx, cy, radius=2, alpha=70)` |
| Shadow on shape | `add_shadow()` | `sh = rect(s,...); add_shadow(sh, blur=8, distance=3)` |
| Glow on shape | `add_glow()` | `sh = rrect(s,...); add_glow(sh, color='#0FF', size=8)` |
| Brush divider | `brush_divider()` | `brush_divider(s, x, y, width, color='#2C2C2C')` |
| Seal stamp | `seal_stamp()` | `seal_stamp(s, x, y, size, '印章文字')` |
| Ink splash | `ink_splash()` | `ink_splash(s, x, y, size, color='#2C2C2C')` |
| Grid background | `grid_background()` | `grid_background(s, spacing=1.0, color='#E0E0E0')` |
| Adjust image | `adjust_image()` | `img = cover_image(s,...); adjust_image(img, brightness=20)` |
| Query design system | `get_design_system()` | `ds = get_design_system('fintech', variance=5)` |
| Analyze PPT | `analyze_pptx()` | `dna = analyze_pptx('template.pptx')` |
| Slide transition | `slide_transition()` | `slide_transition(s, 'fade')` |
| Entrance anim | `entrance_animation()` | `entrance_animation(s, shape_id, 'fade_in')` |
| Exit anim | `exit_animation()` | `exit_animation(s, shape_id, 'fade_out')` |
| Emphasis anim | `emphasis_animation()` | `emphasis_animation(s, shape_id, 'pulse')` |
| Contrast check | `check_contrast()` | `check_contrast('#FFF', '#000')` |
| Auto text color | `contrast_text()` | `contrast_text('#1B5E20')` → '#FFFFFF' |

### 📚 Reference Files (load order):

1. **This SKILL.md** — read workflow + constraints first
2. **[`docs/build_helpers_api.md`](docs/build_helpers_api.md)** — complete function signatures + parameter enums
3. **[`examples/build_10pages.py`](examples/build_10pages.py)** — verified 10-page deck (passes BuildQA 0/0), the canonical build.py reference
4. **[`python-pptx-reference.md`](src/ppt_pro_max/docs/python-pptx-reference.md)** — for UNDERSTANDING python-pptx capabilities only, NOT for direct use in build.py

## ⚠️ Non-Negotiable Sections (DO NOT compress or remove)

These sections are the LLM's only reference for writing correct output:
1. **🎨 Designer Mindset above** — professional design thinking frameworks
2. **⛔ STOP block above** — FORBIDDEN patterns and Quick-Find table
3. **content.json Format** — LLM must know the exact schema to write valid content
4. **brand.json Format** — LLM must know brand spec structure for VI Build mode
5. **Build Helpers API** — LLM must know function signatures to write build.py
6. **UX Intelligence API** — LLM must know how to query the bundled design database for design decisions
7. **Content Design Rules** — LLM must know which content patterns trigger which rendering
8. **Key Constraints** — LLM must know API gotchas and OOXML details
9. **generate_ppt() signature** — LLM must know valid parameters to call the pipeline

## Execution Workflow

ALWAYS follow this 5-step workflow. Each step requires user confirmation before proceeding. Do NOT skip steps or generate final PPT directly — rework is extremely costly.

**Mode selection rule**: ALWAYS use Build Mode for proposal generation. FreeStyle is for agent-driven `content.json` decks (write real content + per-page goals, render directly) or quick one-command drafts. NEVER use FreeStyle for proposals. When in doubt, use Build Mode.

### Step 1: Requirements & Framework (All Modes)

- Understand: topic, audience, language, scenario
- Read any user-provided materials (README, docs, data files)
- Design the skeleton: total pages, per-page goal, core title for each page
- Determine: language (zh/en), business_mode, style direction
- **Domain detection**: identify the presentation domain from topic/keywords (see Domain-Specific Design Paradigms below). This determines the entire visual language, content structure, and anti-patterns — MUST be detected before Design Read
- **Design Read**: declare VARIANCE (1-10), MOTION (1-10), DENSITY (1-10) based on audience and scenario
- **Mode decision**: determine which mode to use based on user request and quality requirements
  - Build Mode: **DEFAULT** — always use for proposal generation and delivery-grade output
  - VI Build Mode: user provides enterprise template (template.pptx) + requests brand compliance
  - FreeStyle: agent-driven `content.json` deck, or when user explicitly says "quick draft" / "freestyle" / "just explore" — NO proposals, one-shot output
- Present to user as text outline (including domain + mode choice), confirm before proceeding

**Dial → Action Map (V/M/D → LLM decisions):**

| VARIANCE | FreeStyle Action | Build/VI Build Action |
|----------|-----------------|----------------------|
| 1-3 | `goal:"content"` + centered layouts; `--layout-variant centered` | Uniform page structure; consistent margins; same component family per page |
| 4-7 | Mix `goal:"content"` with `goal:"features"`; `--layout-variant sidebar-left` | Mix 2-3 layout strategies (e.g., sidebar + grid + split); vary which pages use which strategy |
| 8-10 | Diverse goal types; `--layout-variant asymmetric`; section dividers | Every page uses a different layout strategy; no repeated visual pattern; section dividers between topic shifts |

| MOTION | FreeStyle Action | Build/VI Build Action |
|--------|-----------------|----------------------|
| 1-3 | Default transitions only | No animations; `slide_transition()` with fade only |
| 4-7 | `goal:"hook"` gets fade-in; section dividers get entrance animation | `entrance_animation()` on key elements; `slide_transition()` on section dividers |
| 8-10 | `--motion 8`; more section dividers for variety | `entrance_animation()` + `exit_animation()` on multiple elements; morph transitions; staggered delays |

| DENSITY | FreeStyle Action | Build/VI Build Action |
|---------|-----------------|----------------------|
| 1-3 | 2-3 bullets; breathing pages after every 2 content pages | Generous spacing; `SPACING['minimal']`; 1-2 elements per page zone |
| 4-7 | 3-5 bullets; mix densities | `SPACING['mckinsey']`; mix KPI cards with bullet pages |
| 8-10 | 6+ bullets; `component_type:"group"` + `component_category:"infographic"` | `SPACING['cyberpunk']`; dense dashboards; `kpi_card()` grids; `bar_chart()` stacks |

### Step 2: Visual Proposals (3 structurally-different build.py) — MANDATORY

**⚠️ ALWAYS generate 3 structurally-different build.py proposals. NEVER use FreeStyle `generate_ppt()` × 3 with different `--style` as proposals — that only swaps palette/font and produces identical layouts, which is garbage.**

#### ⛔ Pre-Flight: Read Build Helpers API (MANDATORY before writing build.py)

**Do NOT write any build.py code until you have confirmed the following checklist.** This is the #1 cause of low-quality output: LLMs skip reading the API and use raw python-pptx instead.

**Pre-flight checklist** (confirm each before proceeding):
- [ ] I have read the "Build Helpers API" section and know the available functions
- [ ] I have identified which functions I need for each page (use the Quick-Find table above)
- [ ] I will NOT use `slide.shapes.add_shape()`, `slide.shapes.add_textbox()`, or `slide.shapes.add_picture()` — these are FORBIDDEN
- [ ] I will use `cover_image()` for all images (never `add_picture()` with stretch)
- [ ] I will use color role names (`'primary'`, `'accent'`) instead of raw hex in function calls
- [ ] For CJK content, I will use `TYPOGRAPHY['cjk_mckinsey']` or `cjk_professional` (body=14-15pt, not 11-12pt)

Each proposal must have a **completely different page structure, layout strategy, and visual language** — not just a palette/font swap. The 3 proposals must be structurally distinct so the user can compare different architectural approaches.

#### Build Mode Proposals (No Template)

Generate 3 lightweight `build.py` scripts (proposal_A.py, proposal_B.py, proposal_C.py), each rendering 4-5 key pages (cover + 1 content + 1 data/features + 1 cta) with:

| Proposal | Differentiation Strategy | Example |
|----------|-------------------------|---------|
| **A** | Structure closest to user's style description | "McKinsey" → sidebar + table + numbered cards |
| **B** | Same topic, alternative layout architecture | "McKinsey topic" → grid dashboard + KPI cards + bar charts |
| **C** | Radical visual departure | "McKinsey topic" → creative circles + emoji + before-after comparison |

**Structural differentiation dimensions (pick ≥2 per proposal to differ):**

| Dimension | Options | What Changes in build.py |
|-----------|---------|--------------------------|
| Page structure | sidebar-left / full-width / grid-2x2 / split-image | `page_header()` position, content zone x/y/w/h |
| Data presentation | table / bar_chart / kpi_card grid / donut_chart | Which `build_helpers` functions are called |
| Card style | highlight_cards / custom rrect stack / numbered list | Card component choice and layout |
| Cover type | hero_slide / section_divider / custom split | Cover page function calls |
| Typography scale | TYPOGRAPHY['mckinsey'] / ['cyberpunk'] / ['creative'] / ['minimal'] | `t = TYPOGRAPHY[...]` selection |
| Spacing system | SPACING['mckinsey'] / ['cyberpunk'] / ['creative'] / ['minimal'] | `sp = SPACING[...]` selection |
| Color system | C dict with different primary/accent/muted | Color token values in C dict |

**Proposal generation workflow:**

1. **UX Intelligence Query** — BEFORE writing any build.py, query the bundled design database for domain-specific design knowledge:
   ```python
   from ppt_pro_max.adapters.ui_ux_adapter import (
       is_available, get_design_system, search_design,
       search_style, search_color, search_typography,
   )

   if is_available():
       ds = get_design_system("your query", variance=V, motion=M, density=D)
       ux_colors = ds.get('colors', {})          # e.g. {'primary': '#7C3AED', 'background': '#FAF5FF', ...}
       ux_typo = ds.get('typography', {})         # e.g. {'heading': 'Inter', 'body': 'Inter', ...}
       ux_style = ds.get('style_name', '')        # e.g. 'AI-Native UI'
       ux_effects = ds.get('style_effects', '')   # e.g. 'Glassmorphism + micro-interactions'
       ux_anti = ds.get('anti_patterns', '')      # e.g. 'Heavy chrome + Slow response feedback'
       ux_pattern = ds.get('pattern_name', '')    # e.g. 'SaaS Landing'
       ux_dials = ds.get('dials', {})             # variance/motion/density recommendations

       # Enrich with style/color/typography searches
       style_results = search_style("professional consulting", 2)
       color_results = search_color("dark tech", 2)
       typo_results = search_typography("modern sans", 2)
   ```
   Use `ux_colors` as the **primary source** for the `C` dict instead of hardcoding colors. Use `ux_anti` to avoid known anti-patterns. Use `ux_effects` to guide decoration/animation choices.

2. Write 3 build.py files (proposal_A.py, proposal_B.py, proposal_C.py) with:
   - Different `C` color dict derived from design database search results (3 distinct palettes)
   - Different `TYPOGRAPHY[...]` and `SPACING[...]` selections informed by ux_typo
   - Different page structure and component choices per page
   - Same framework content (titles + placeholder data) so user compares structure, not content
3. Run each: `python proposal_A.py`, `python proposal_B.py`, `python proposal_C.py`
4. Present 3 output PPTs to user with descriptions:
   - **A**: "Sidebar + table layout — consulting style, structured and data-driven"
   - **B**: "Grid dashboard — tech-forward, KPI-focused, information-dense"
   - **C**: "Creative circles — visual storytelling, emoji-accented, approachable"
5. User picks one direction (A/B/C) or requests adjustments
6. Low rework cost: only structural parameters change, content is placeholder

**Example proposal_A.py (McKinsey-style skeleton with UX intelligence):**

```python
from ppt_pro_max.build_helpers import *
from ppt_pro_max.adapters.ui_ux_adapter import get_design_system, search_color, search_typography

# Step 1: Query UX intelligence for design decisions
ds = get_design_system('investor pitch', variance=5, motion=3, density=5)
ux_colors = ds.get('colors', {})
ux_anti = ds.get('anti_patterns', '')  # Use to avoid bad patterns

# Step 2: Build C dict from UX intelligence (not hardcoded)
C = {
    'primary': ux_colors.get('primary', '#2E6504'),
    'accent': ux_colors.get('accent', '#7DA92F'),
    'muted': ux_colors.get('muted', '#81C784'),
    'light': ux_colors.get('border', '#C8E6C9'),
    'white': '#FFFFFF',
    'background': ux_colors.get('background', '#FFFFFF'),
    'card_bg': '#F9F9F9',
    'text_dark': ux_colors.get('foreground', '#1A1A1A'),
    'text_body': ux_colors.get('text', '#333333'),
    'text_muted': '#666666',
    'divider': '#CCCCCC',
    'font_heading': 'Georgia', 'font_body': 'Calibri',
}
t = TYPOGRAPHY['mckinsey']
sp = SPACING['mckinsey']

prs = Presentation()
s = add_slide(prs)
hero_slide(s, '{query}', 'Proposal A — Sidebar + Table', C=C, typo=t)

s = add_slide(prs)
page_header(s, 'Current Challenges', 'Key obstacles to growth', C, typo=t, spacing=sp)
# sidebar + bullets layout
rect(s, 0, 0, 3.5, 7.5, C['primary'], C=C)
multiline(s, 0.4, 1.5, 2.7, 4, ['Challenge 1', 'Challenge 2', 'Challenge 3'],
          font_size=t.body, color='white', C=C)

s = add_slide(prs)
page_header(s, 'Key Metrics', 'Performance overview', C, typo=t, spacing=sp)
kpi_card(s, 0.65, 1.8, 3.8, 1.35, '12.8亿', '年度产值', '+8.3%', C=C, typo=t)
kpi_card(s, 4.8, 1.8, 3.8, 1.35, '94.2%', '客户满意度', '+2.1%', C=C, typo=t)

s = add_slide(prs)
cta_slide(s, 'Get Started', 'Contact us today', C=C, typo=t)

prs.save('proposal_A.pptx')
```

#### VI Build Mode Proposals (With Template)

When user provides a template.pptx, proposals must preserve framework pages (cover/TOC/back cover) and only vary the **new content page structure**. All 3 proposals share the same VI Token (extracted from template), but differ in layout architecture for content pages.

1. Run `python -m ppt_pro_max analyze template.pptx > analysis.txt`
2. Extract VI Token (C dict) from analysis.txt — this is **fixed** across all 3 proposals
3. Generate 3 build.py files with:
   - **Same** C dict (VI Token from template)
   - **Same** `Presentation('template.pptx')` + `copy_decorations()` + `copy_logo()` on every page
   - **Different** content page layout strategies (sidebar vs grid vs split)
   - **Different** component choices for data pages (kpi_card vs bar_chart vs table)
4. Run each, present to user, user picks direction

**Example VI Build proposal differentiation:**

| Proposal | Content Page Layout | Data Page Component | Visual Character |
|----------|--------------------|--------------------|-----------------|
| A | Sidebar + content (left nav bar) | kpi_card row | Structured, report-style |
| B | Full-width + section dividers | bar_chart + comparison_bars | Narrative, story-driven |
| C | Grid 2x2 + cards | donut_chart + highlight_cards | Dashboard, data-centric |

### Step 3: Detailed Content (All Modes)

**Build/VI Build Mode:**
- Write full content for every page directly into the chosen build.py
- Content is hardcoded per page: titles, KPI numbers, bullet text, chart data, code snippets
- MUST be query-specific and domain-accurate — NEVER use generic template content
- MUST follow the Content Design Rules below
- Present key content to user for review before final generation
- User confirms content accuracy before proceeding

**FreeStyle Mode (agent-driven content.json or quick draft):**
- Path A: you write `content.json` (real content, per-page `goal` + field selection), then `generate_ppt(content_file="content.json", style=..., ...)` renders it directly — see [content.json Format](#contentjson-format)
- Path B: one-command draft `generate_ppt("topic", style=..., fetch_images=True, ...)`
- No proposal step — one-shot output
- For revisions: modify content.json and regenerate, or edit the slide count/fields

### Step 4: Draft Generation & Revision (All Modes)

**Build/VI Build Mode:**
- Run the full build.py: `python build.py`
- Verify output: check page count, file size, content rendering, shape count per slide
- For revisions: modify build.py and re-run (build.py is the single source of truth)
- Version control: save output to `output/v1/`, increment on revisions

**FreeStyle Mode (agent-driven content.json or quick draft):**
- Generate full PPT: `generate_ppt(content_file="content.json", style=confirmed_style, fetch_images=True, ...)` (query optional)
- Verify output: check page count, file size, content rendering
- For revisions: modify content.json and regenerate, or edit the slide count/fields

### Step 5: Final Delivery (All Modes)

- User confirms satisfaction
- Pipeline auto-saves with version control

### Content Design Rules (CRITICAL — maximizes design quality)

When writing content (content.json for FreeStyle, or hardcoded text in build.py for Build/VI Build), follow these rules to produce the best possible rendering output.

| Rule | Why | FreeStyle Example | Build Example |
|------|-----|-------------------|---------------|
| features: first card featured with longer body | First card gets gradient bar + 22pt title + higher elevation | Card 1: "智能推理引擎 — 自动选择最优框架" vs Card 2: "全链路监控" | `highlight_cards()`: first tuple gets accent bar + larger title |
| 6+ bullets → two-column layout | Better density; layout engine auto-splits | 6 concise data points instead of 3 long ones | Use two `multiline()` calls side by side, or `kpi_card()` grid |
| tech topics: include code page | Code pages add technical credibility | `{"code": {"language": "python", "source": "..."}}` | `code_block(slide, left, top, w, h, lines, language='python', C=C)` |
| education/training: include exercise page | Exercise pages add interactivity | `{"exercise": {"duration": "5 min", "steps": [...]}}` | Custom: `rrect()` badge + `multiline()` numbered steps |
| topic transitions: insert section divider | Visual rhythm (oversized number + gradient line) | Between problem→solution | `section_divider(slide, 2, 'Solution', C=C, typo=t)` |
| hook: short subtitle (<40 chars); cta: long (>60) | Different hero compositions | hook: "5分钟取代5周" vs cta: "免费额度包含1000次推理/月" | `hero_slide(slide, title, short_sub, C=C)` / `cta_slide(slide, title, long_sub, C=C)` |
| vary bullet density (some 3-bullet, some 6+) | Varying density feels natural; 10+ items → cards/grid/table, never list | Don't make every page the same density | Mix `multiline()` pages with `kpi_card()` / `bar_chart()` pages |
| use concrete real data; no fake precision | "GPU成本年增3倍" not "成本持续增长"; no fabricated 92%/4.1× | Real data only; mark as "example" if hypothetical | Same — hardcode real numbers in `kpi_card()` and `bar_chart()` data |
| ≤5 bullets: single column | 6+: two-column; 10+: use cards/grid/infographic component, never list | 3 bullets → single col; 7 bullets → two-col | 3 bullets → one `multiline()`; 6+ → two `multiline()` or `highlight_cards()` |
| no filler verbs (赋能/领先/一站式/生态/革新/引领) | AI-generated buzzwords destroy credibility | Use plain functional language | Same — hardcode plain language in build.py |
| quotes ≤3 lines, attribution = name+title | PPT quotes are fragments, not full reviews | "Name, CTO, Company" — never name alone | Same for `text()` content |
| theme lock: one theme per deck, no mid-deck switch | Dark stays dark, light stays light; micro-variation OK | #0A1E3D → #0F2847 OK; #0A1E3D → #FFF8F0 NOT OK | Same C dict throughout; no mixing primary/accent mid-deck |

### Domain-Specific Content Rules (OVERRIDE above rules when domain matches)

**Scientific Research — these rules REPLACE the business defaults:**

| Rule | Why | Implementation |
|------|-----|----------------|
| Every data page = one Figure with caption | Journal convention; audience expects Figure-style | `text(slide, x, y, w, 0.3, 'Figure N: ...', font_size=10)` below visual |
| Use semantic biology colors, not brand accent | Red=upregulated, blue=downregulated has scientific meaning | C dict with `up_color`, `down_color`, `control_color` instead of `primary`/`accent` |
| Cite every claim: (Author, Year) or superscript | Uncited claims = scientific fraud | `text(slide, x, y, w, 0.2, '¹Smith et al., Nature 2024', font_size=8, color='text_muted')` |
| NO KPI cards, NO hero slides, NO feature cards | These are business patterns, meaningless in science | Use Figure+caption, data tables, sequence views instead |
| Cover = paper title format | Title + authors + affiliation, not marketing hero | `text()` title (28pt) + `multiline()` authors (14pt) + `text()` affiliation (12pt) |
| No animation or transition | Research slides must be printable as-is | Skip all `entrance_animation()` / `slide_transition()` calls |
| Panel labels (A, B, C) on multi-panel figures | Standard journal figure convention | `text(slide, x, y, 0.4, 0.3, 'A)', font_size=10, bold=True)` |
| Axis labels on all charts | Data without axis labels is uninterpretable | `text(slide, x, y, w, 0.3, 'Expression (log₂FC)', font_size=9)` |

**Academic Thesis — additional rules:**

| Rule | Why | Implementation |
|------|-----|----------------|
| Chapter-flow structure, not story arc | Thesis defense follows chapter order, not marketing arc | Ch1 Introduction → Ch2 Methods → Ch3 Results → Ch4 Discussion |
| Bibliography slide at end | Required for academic completeness | `multiline()` with numbered references (8-9pt) |
| Advisor/committee on cover | Academic protocol | `text()` advisor name + title on cover slide |

**Medical/Clinical — additional rules:**

| Rule | Why | Implementation |
|------|-----|----------------|
| Evidence level labels | Clinical decisions require evidence grading | `text(slide, x, y, w, 0.2, '[Level A evidence]', font_size=9, color='text_muted')` |
| Disclaimers where applicable | Regulatory requirement | `text(slide, x, y, w, 0.3, 'Disclaimer: ...', font_size=8, color='text_muted')` |
| No decorative visuals | Patient safety > aesthetics | No `neon_border()`, `brush_divider()`, `ink_splash()` |

## When to Activate

- User asks to create/generate/design a **PPT/presentation/deck/slide deck**
- User wants a **pitch deck, product demo, sales presentation, investor deck**
- User wants to **convert content/outline into PowerPoint**
- User wants **brand-compliant** presentations with template + version control
- User wants **page-level CRUD** on existing PPT (add/delete/swap/move pages)
- User wants **diagrams** in PPT (flowchart, funnel, timeline, SWOT, etc.)
- User provides a **template.pptx** and wants enterprise VI compliance
- User wants **scientific/academic** presentation (gene, protein, thesis, dissertation, 论文, 答辩, 实验)
- User wants **medical/clinical** presentation (diagnosis, treatment, clinical trial, 诊断, 临床)
- **Default**: Build Mode is always used unless user explicitly says "quick draft" / "freestyle"

## Three-Mode Architecture

| | **Build Script** | **VI Build** | FreeStyle |
|---|---|---|---|
| **Use case** | Delivery-grade, no template | **Enterprise VI compliance** | Agent-driven content.json OR quick draft (NO proposals) |
| **Trigger** | **DEFAULT** — always use unless user says "quick draft" | User provides template.pptx + requests brand compliance | You write content.json with real content, or user says "quick draft" / "freestyle" |
| **Content source** | Hardcoded per page in build.py | LLM reads template analysis, generates build.py | **You write content.json** (recommended) or one-liner topic |
| **Brand compliance** | Design Token dict `C` | **Extracted VI Token from template** | Style atom combos |
| **Layout control** | **Per-element x/y/w/h** | **Preserve framework pages + build_helpers for new** | goal + field selection (10 layout branches) |
| **Font control** | **Run-level per character** | **Run-level + template font inheritance** | Theme-level |
| **Template reuse** | None | **Framework pages preserved + decorations/LOGO copied** | None |
| **Proposal type** | 3 build.py (structural differentiation) | 3 build.py (layout strategy differentiation, same VI Token) | **NO proposals** — one-shot output only |
| **Quality ceiling** | ★★★★★ | ★★★★★ | ★★★★ (goal-driven, fixed positions) |

> **Mandatory workflow**: ALWAYS use Build Mode for proposals (3 structurally-different build.py). FreeStyle is for agent-driven content.json decks or quick one-shot drafts — NEVER use FreeStyle for proposal generation.

### Build Mode (Pixel-Perfect Delivery) — DEFAULT & PRIMARY DELIVERY MODE

LLM writes `build.py` scripts from blank canvas, using build_helpers for maximum per-element control. This is the highest-quality output mode with full control over every shape's position, size, color, and typography.

**When to use**: ALWAYS the default mode. Use for all proposal generation and delivery-grade output (investor deck, board presentation, client deliverable). Only fall back to FreeStyle when user explicitly says "quick draft".

```bash
# LLM generates build.py, then:
python build.py
```

**Build Mode workflow (follow Execution Workflow Steps 1-5 with Build-specific Step 2):**

1. Step 1: Requirements & Framework (same as all modes)
2. Step 2: Generate 3 structurally-different build.py proposals → user picks direction
3. Step 3: Fill chosen build.py with full content
4. Step 4: Run build.py → verify → revise
5. Step 5: Final delivery

See **Build Helpers API** section below for function reference.

### VI Build Mode (Enterprise Template Compliance)

LLM reads template analysis, generates build.py that preserves framework pages (cover/TOC/back cover) and uses `build_helpers` for new content pages.

```bash
# Step 1: Analyze template
python -m ppt_pro_max analyze template.pptx > analysis.txt

# Step 2: Give analysis.txt to LLM, which generates build.py

# Step 3: Run build.py
python build.py
```

**VI Build workflow in build.py:**

```python
from ppt_pro_max.build_helpers import *

# VI Token extracted from template analysis
C = {
    'primary': '#2E6504', 'accent': '#7DA92F', 'muted': '#81C784',
    'light': '#C8E6C9', 'white': '#FFFFFF', 'background': '#FFFFFF',
    'card_bg': '#F9F9F9', 'text_dark': '#1A1A1A', 'text_body': '#333333',
    'text_muted': '#666666', 'divider': '#CCCCCC',
    'font_heading': '微软雅黑', 'font_body': '微软雅黑',
}

# Load template (NOT Presentation() from scratch)
prs = Presentation('template.pptx')
template_slide = prs.slides[0]  # Reference for copying decorations/LOGO

# Framework pages (cover, TOC, back cover) are preserved — do NOT delete them
# Add new content pages:
s = add_slide(prs)
copy_decorations(s, template_slide)  # Copy visual elements from template
copy_logo(s, template_slide, color_hints=['#2E6504'])  # Copy company LOGO
page_header(s, 'Revenue Overview', 'FY2025 Performance', C)
kpi_card(s, 0.65, 1.8, 3.8, 1.35, '12.8亿', '年度产值', '+8.3%', C=C)

prs.save('output.pptx')
```

**Key differences from Build Script:**
- Start with `Presentation('template.pptx')` NOT `Presentation()`
- Framework pages (cover/TOC/back cover) are preserved untouched
- Use `copy_decorations()` / `copy_logo()` to maintain VI consistency
- VI Token (`C` dict) extracted from `ppt-design analyze` output, not hand-written

### FreeStyle Mode (Agent-Driven content.json — NO Proposals)

FreeStyle renders a deck from a **content.json you write** (recommended, agent-driven) OR from a one-liner topic string (legacy quick draft). **NO proposal step** — one-shot output only. Use when user says "quick draft" / "freestyle" / "just explore", or when you need a fast, fully-editable deck.

**⚠️ NEVER use FreeStyle for proposal generation.** Calling `generate_ppt()` × 3 with different `--style` only swaps palette/font and produces identical layouts — this is NOT a valid proposal. Use Build Mode (build.py) for proposals.

#### Path A (Recommended): You write content.json → render

In an agent environment **you are the LLM** — you don't need Python to call an API for content. Write a `content.json` with real content and per-page `goal`, then call `generate_ppt(content_file=...)`. This is the deterministic, high-quality path: you control every page's content AND which render branch it uses.

```python
# query is optional when content_file contains slides[]
result = generate_ppt(content_file="content.json", style="dark-tech")
```

**Three-layer orthogonality:**
- `content.json` controls **content** (title/subtitle/bullets/cards/chart/code/diagram/exercise) + **layout role** (`goal` field → render branch)
- `style` param controls **visuals** (colors/fonts/decorations → ThemeComposer → BrandSpec)
- renderer's `goal` branches control **structure**

Prefer **preset** style names for deterministic output (`dark-tech`, `professional`, `warm-elegant`, ...). Natural-language styles like `"dark cyberpunk"` resolve via mood detection and may produce different palettes.

See [content.json Format](#contentjson-format) below for the full schema and design rules (chart format, section_number, field-to-layout mapping).

#### Path B (Quick draft): one-liner topic

```bash
python -m ppt_pro_max "AI startup investor pitch"

# Natural language style (40K+ combos)
python -m ppt_pro_max "fintech pitch" --style "warm fintech"
python -m ppt_pro_max "product launch" --style "dark cyberpunk"

# AI images (Seedream recommended)
python -m ppt_pro_max "AI pitch" --fetch-images --llm-provider seedream

# Exact atom control
python -m ppt_pro_max "pitch" --palette wine-burgundy --fonts elegant-serif --layout-variant centered

# Design dials
python -m ppt_pro_max "pitch" --variance 7 --motion 5 --density 6
```

## Domain-Specific Design Paradigms

**⚠️ CRITICAL: Detect domain BEFORE designing.** Using the wrong paradigm produces fundamentally mismatched output (e.g., McKinsey sidebar on a genomics slide). The domain determines visual language, content structure, typography, color system, and anti-patterns.

### How to Detect Domain

Match user topic/keywords to the paradigm with the most keyword hits. If ambiguous, ask the user.

| Domain | Trigger Keywords |
|--------|-----------------|
| Scientific Research | gene, protein, genome, sequencing, CRISPR, pathway, assay, omics, PCR, RNA, DNA, expression, mutation, variant, bioinformatics, proteomics, metabolomics, single-cell, immunotherapy, checkpoint, clinical trial, CRISPR, 序列, 基因, 蛋白, 测序, 组学, 免疫, 细胞, 实验, 通路, 变异 |
| Academic Thesis | thesis, dissertation, defense, viva, 论文答辩, 毕业, 学位, 答辩 |
| Engineering/Technical | architecture, system design, infrastructure, deployment, API, microservice, 架构, 系统, 部署, 工程 |
| Medical/Clinical | diagnosis, treatment, patient, clinical, surgery, therapy, 诊断, 治疗, 患者, 临床, 手术 |
| Government/Public Sector | policy, regulation, compliance, budget, annual report, 政策, 法规, 合规, 预算, 年报 |
| Business (default) | pitch, investor, sales, marketing, product launch, KPI, revenue, 投资人, 销售, 营销, 产品发布 |

### Scientific Research Paradigm

**Visual language**: Nature/Cell/Figure style — NOT business slides. Every data page looks like a journal figure, not a marketing card.

| Aspect | DO (Research) | DON'T (Business anti-pattern) |
|--------|---------------|------------------------------|
| **Page structure** | Figure + caption below; one main visual per page | KPI cards, sidebar layout, feature cards |
| **Data visualization** | Sequence alignment, heat map, volcano plot, Manhattan plot, phylogenetic tree, gel electrophoresis, chromatogram | Bar charts with KPI labels, donut charts |
| **Numbering** | Figure 1, Figure 2, Figure 3... per page (required) | "01/04" card numbering (banned in business but REQUIRED here) |
| **Color system** | Semantic biology colors: blue=downregulation, red=upregulation, green=control, purple=mutation; or journal-specific palettes (Nature blue/gray, Cell warm) | Brand accent colors, gradient fills |
| **Typography** | Clean serif or sans-serif (Arial/Helvetica); figure labels 9-11pt; axis labels 10-12pt | Hero-sized titles, gradient text |
| **Citations** | Required: (Author, Year) or superscript number¹ after claims | No citations (business slides don't cite) |
| **Cover** | Paper title style: title + authors + affiliation + journal-style layout | Hero image + gradient overlay |
| **Content flow** | Background → Methods → Results (Fig 1-4) → Discussion → References | Hook → Problem → Features → CTA |
| **Animation** | NONE — research slides must be printable as-is | Any animation or transition |

**Research content structure (per page):**

```
┌──────────────────────────────────┐
│ Figure 3: ERK pathway activation │  ← Figure label (9-11pt, top-left)
│                                  │
│    [Main figure/visualization]   │  ← Full-width data visual
│                                  │
│ A) Western blot  B) Quantification│  ← Panel labels (A, B, C...)
│                                  │
│ ERK phosphorylation increased    │  ← Caption text (10-11pt)
│ 3.2-fold (p<0.01)¹              │  ← Citation
└──────────────────────────────────┘
```

**Research Build Mode components:**

| Component | Implementation |
|-----------|---------------|
| Figure label | `text(slide, 0.5, 0.3, 6, 0.3, 'Figure 3:', font_size=10, color='text_dark', bold=True, C=C)` |
| Panel label (A/B/C) | `text(slide, x, y, 0.4, 0.3, 'A)', font_size=10, bold=True, C=C)` |
| Axis labels | `text(slide, x, y, w, 0.3, 'Expression (log₂FC)', font_size=9, C=C)` |
| Data table | `rect()` header row + `multiline()` data rows with alternating `rrect()` backgrounds |
| Sequence alignment | Custom: `rrect()` colored blocks per residue (A=green, T=red, G=yellow, C=blue) |
| Heat map grid | Nested `rrect()` cells with color-coded fills per expression level |
| Citation | `text(slide, x, y, w, 0.2, '¹Smith et al., Nature 2024', font_size=8, color='text_muted', C=C)` |

**Research color palettes:**

| Palette | Colors | Use When |
|---------|--------|----------|
| `nature` | #2C3E50 (text), #3498DB (data blue), #E74C3C (highlight red), #95A5A6 (neutral) | General biology, genomics |
| `cell-journal` | #D35400 (warm accent), #2C3E50 (text), #27AE60 (green), #8E44AD (purple) | Cell biology, pathways |
| `clinical` | #2C3E50 (text), #2980B9 (diagnosis), #C0392B (alert), #27AE60 (positive outcome) | Clinical trials, medical |
| `genomics` | #2C3E50 (text), #8E44AD (mutation), #3498DB (wild-type), #E67E22 (variant) | Sequencing, variant analysis |

### Academic Thesis Paradigm

**Visual language**: Formal academic presentation — structured, citation-heavy, defense-appropriate.

| Aspect | DO (Thesis) | DON'T |
|--------|-------------|-------|
| **Structure** | Title → Outline → Ch1→Ch2→Ch3→Conclusion (thesis chapter flow) | Hook→Problem→Features→CTA |
| **Typography** | University-standard fonts; body 14-16pt; figure captions 10-11pt | Decorative fonts, gradient text |
| **References** | Required on every claim; bibliography slide at end | No citations |
| **Cover** | University name + logo + title + author + advisor + date | Marketing-style hero |
| **Animation** | Minimal (fade only) | Any emphasis or exit animation |

### Engineering/Technical Paradigm

**Visual language**: System architecture, data flow, API specs — technical documentation style.

| Aspect | DO (Engineering) | DON'T |
|--------|------------------|-------|
| **Diagrams** | Architecture diagrams, sequence diagrams, flow charts | Marketing feature cards |
| **Code** | API examples, config snippets, CLI commands (mandatory) | Generic "feature" descriptions |
| **Tables** | Spec tables, comparison matrices, performance benchmarks | KPI cards with trend arrows |
| **Color** | Technical: dark bg (#1E293B) for code, neutral grays, single accent for highlight | Brand gradients |
| **Animation** | Step-by-step reveal for architecture diagrams | Bounce/fly animations |

### Medical/Clinical Paradigm

**Visual language**: Clinical, evidence-based — similar to research but with patient-safety formality.

| Aspect | DO (Medical) | DON'T |
|--------|--------------|-------|
| **Data** | Clinical trial results, survival curves, forest plots, diagnostic accuracy tables | Marketing dashboards |
| **Color** | Clinical palette (blue=diagnosis, red=alert, green=outcome); no decorative colors | Vibrant startup colors |
| **Disclaimers** | Required where applicable (e.g., "off-label use", "preliminary data") | None |
| **Citations** | Mandatory — evidence-based claims only | Uncited claims |
| **Animation** | NONE — must be printable for medical records | Any animation |

### Government/Public Sector Paradigm

**Visual language**: Formal, structured, compliance-driven.

| Aspect | DO (Government) | DON'T |
|--------|----------------|-------|
| **Structure** | Executive summary → body → appendix; numbered sections | Marketing story arc |
| **Typography** | Standard serif/sans-serif; conservative; minimum 14pt body | Creative fonts |
| **Color** | Flag colors or institutional palette; muted | Bright startup colors |
| **Data** | Official statistics, budget tables, compliance matrices | Trendy infographics |
| **Animation** | NONE | Any animation |

## Design Constraints

### Design Decision Framework (intent → decision)

Before applying the quantified rules below, establish **why** you're making each choice. Professional designers use these mental models:

| Decision Area | Designer Question | Common Choices | Rationale |
|---------------|-------------------|----------------|-----------|
| **Audience context** | Who views this and where? | Boardroom / Keynote / Academic / General | Dictates density, formality, motion level |
| **Visual tone** | What emotion should the deck convey? | Confident / Innovative / Trustworthy / Bold | Drives palette, typography, layout density |
| **Information density** | How much content per slide? | Sparse (3-4 elements) / Balanced (5-7) / Dense (8+) | Matches audience attention span and content type |
| **Layout rhythm** | What's the visual cadence across slides? | Vary every 2-3 slides | Prevents monotony — different layouts signal progress |
| **Emphasis strategy** | What is the ONE thing per slide? | Hero image / Oversized number / Bold statement | Forces focus — without emphasis, slides become noise |

Apply these frameworks first, then use the quantified rules below as **enforcement gates** to catch violations of professional standards.

### Quantified Design Constraints (violations = detectable AI Tells)

| Constraint | Threshold | Violation Consequence |
|---|---|---|
| Min font size | ≥ 11pt (CJK: ≥ 14pt) | Unreadable on projection → #2 AI Tell |
| Font-size levels per deck | ≥ 4 (hero/h1/h2/body) | 2-level deck = "AI didn't care about typography" |
| Max font families | ≤ 2 (heading + body) | 3+ fonts = "AI threw everything at the wall" |
| Accent colors | ≤ 1 per deck | Multi-accent = "AI can't commit to a palette" |
| Corner radius system | 1 per deck (0pt / 8-12pt / pill) | Mixed radii = "AI has no design system" |
| Slides ≥ 8 pages | ≥ 4 distinct layout structures | Same layout × 8 = "AI copy-pasted" |
| Cover title | ≤ 2 lines, 44-52pt | 3+ lines = "AI couldn't summarize" |
| Bullets per page | ≤ 5: single col; 6-9: two col; 10+: cards/grid | 10+ bullets in list = "AI dumped text" |
| Images | ALWAYS `cover_image()`, NEVER `add_picture()` stretch | Stretched image = "AI doesn't understand aspect ratio" |
| CJK body text | 14-15pt (NOT 11-12pt Latin presets) | 11pt CJK = "AI used Latin defaults, characters unreadable" |
| Dark theme text | ≥ 60% luminance above background | Low contrast = "AI can't see its own output" |
| Shapes per slide | ≤ 50 | 50+ = performance issues on older hardware |

### Typography
- Cover title: 44-52pt, ≤2 lines | Inner title: 32-36pt | Body: 14-16pt | Bullets: 13-14pt | Caption: 11-12pt
- Min 4 font-size levels per deck — 2 levels (title+body only) is forbidden
- NO Calibri/Arial as default font (PPT's AI default, same as Inter in web)
- Serif: only for editorial / luxury / heritage scenes — NOT for tech/startup/data
- Max 2 font families per deck (heading + body, +1 monospace for code)
- Emphasize with bold or color shift — NO mixing serif+sans for "contrast emphasis"
- Italic title line-height ≥1.1× (descender clearance)
- Each page: short title (≤8 words) + short subtitle (≤25 chars) + 1 visual OR 1 CTA

### Color
- Max 1 accent color per deck, used on EVERY page (consistency lock)
- NO default-blue gradient cover when style is unspecified
- NO default gold+navy for "premium" scenes (#1A1A2E / #C9A96E family)
- Warm/cool gray: pick one, use throughout — no mixing
- Chart colors derived from main palette — no rainbow
- Dark theme: text ≥60% luminance above background (projection-grade contrast)
- Light theme: no light-gray text on white (invisible on projector)

### Layout
- VARIANCE > 4: avoid all-centered; use left-aligned / sidebar / asymmetric
- Same layout family max 1 occurrence per deck ("Our Products" ≠ "Core Advantages" visually)
- 8+ slides: ≥4 distinct visual layouts
- Left-right alternation ≤2 times; 3rd = break pattern
- Eyebrow count ≤ceil(page_count / 3); NO section-number eyebrows (00/INDEX, 001·核心能力)
- No split-header as default (title left + small text right)
- Bento grid: ≥2-3 cells with visual variation (not all-white text cards)
- Spec sheets: NO 10-line bullet lists — use card grid / highlight+fold / grouped sections
- NO 20+ row data tables in PPT — PPT is presentation, not document

### Page Roles
- MUST plan 5 roles: breathing (low-density rest) / section-divider / data-impact (big number) / visual-anchor (full-bleed image) / cta
- No 3 consecutive "title + bullets" pages
- 6+ slides: ≥1 section divider
- High-density page → must be followed by low-density page

### Visual Assets
- Cover MUST have real visual (not text + gradient block)
- Even minimalist style: ≥2-3 pages with images
- NO fake product screenshots (text-box dashboards/terminals/task-lists — #1 AI Tell in PPT)
- Logo wall: use real logo images, not text spans

### Consistency Locks
- Corner radius: ONE system per deck — sharp (0pt) / soft (8-12pt) / pill — no mixing
- Font pair: consistent throughout (heading + body, all slides)
- Accent color + warm/cool gray + theme lock: enforced in Color rules and Content Design Rules

### AI Tells Blacklist (HARD BAN unless user explicitly requests, OR domain is scientific/academic/medical)

**Domain exceptions**: In Scientific Research, Academic Thesis, and Medical domains, the following are REQUIRED (not banned):
- Figure numbering (Figure 1, Figure 2) — required for research data pages
- Panel labels (A, B, C) — required for multi-panel figures
- Section numbers (1. Introduction, 2. Methods) — required for thesis chapters
- Citation superscripts (¹, ²) — required for evidence-based claims

- No cover version labels (V0.6/BETA/内测版)
- No "Brand · No.01" style sub-labels
- No section-number eyebrows (00/INDEX, 001·核心能力) — use natural language
- No card/image numbering labels (01/04, 1/3)
- Max 1 middle-dot (·) per metadata line — no "foo · bar · baz · qux"
- No decorative status dots
- No em-dash (—) or Chinese em-dash (——) — use comma/hyphen/semicolon
- No linebreak+italic "design trick"
- No vertical rotated text
- No crosshair/fine-grid decoration (only for organizing real content)
- No fake product UI (text-box dashboard/terminal/task-list)
- No fake version footers (v0.6.2-rc.1, "last sync 4s ago")
- No "silently used by" / "默默服务" social-proof headlines — use natural language or skip
- No "来自一线" / "实战笔记" artisan labels — use plain functional labels
- No city/time/weather bars (99% of scenarios)
- No eyebrow micro-metadata sentences
- No generic step labels ("Phase 1/2/3", "步骤 01/02/03") — use verb+noun
- No overlaid labels on images ("Brand · 02")
- No decorative photo credits (场景 III · 35mm) — skip or use one-line caption
- No version footers on marketing slides (v1.4.2, Build 0048)
- No inventory counters as decoration ("已预约 412/800")
- No bottom-of-cover decoration strips (品牌. 创新. 技术.)
- No floating explanation text top-right of section titles
- No divider lines on every row of long lists
- No progress bars with filled background tracks for comparison
- No scroll hints (Scroll, ↓)

### Design Vocabulary (pattern → FreeStyle trigger → Build implementation)

**Covers:**

| Pattern | FreeStyle Trigger | Build Implementation |
|---------|-------------------|---------------------|
| Asymmetric Split Hero | `goal:"hook"`, image on one side | `rect()` split bg + `text()` left + image right |
| Editorial Manifesto | `goal:"hook"`, no image, large type | `hero_slide()` text-only |
| Full-Bleed Image | `goal:"hook"`, image with overlay | `rect()` full-bg + image + `gradient_text()` overlay |
| Data-Impact | `goal:"hook"`, big number + one-liner | `rect()` bg + `text()` huge number + `text()` one-liner |
| Minimal Typography | `goal:"hook"`, text-only, extreme whitespace | `text()` large title with wide margins |

**Inner pages:**

| Pattern | FreeStyle Trigger | Build Implementation |
|---------|-------------------|---------------------|
| Sidebar+Content | `--layout-variant sidebar-left` | `rect()` sidebar + `page_header()` + content right |
| Split Text-Image | `goal:"content"`, image field | `text()` left half + `circle_image()` right |
| Bento Grid | `goal:"features"`, 4+ cards | `rrect()` grid of 4+ cells |
| Big Number Focus | `goal:"data"`, single metric | `text()` oversized number + `text()` label |
| Card Row | `goal:"features"`, 3 cards | `highlight_cards()` |
| Comparison Split | `goal:"content"`, two-column contrast | `comparison_bars()` or two `multiline()` side by side |
| Timeline Horizontal | `component_category:"timeline"` | `rect()` line + `oval()` dots + `text()` labels |
| Quote Spotlight | `goal:"content"`, quote in bullets | `gradient_text()` large quote + `text()` attribution |
| Code Terminal | `goal:"code"` | `code_block()` |
| Full-Width Visual | `goal:"content"`, full-bleed image | `rect()` bg image + `frosted_panel()` + `text()` |

**Data pages:**

| Pattern | FreeStyle Trigger | Build Implementation |
|---------|-------------------|---------------------|
| Table Diagram | `goal:"data"`, diagram type:"table" | `rect()` headers + `multiline()` rows |
| Chart Focus | `goal:"data"`, diagram type: chart | `bar_chart()` or `donut_chart()` |
| Metric Dashboard | `component_category:"infographic"` | `kpi_card()` grid |
| Infographic Component | `component_type:"group"` | Custom shapes with `rect()`/`oval()`/`text()` |
| Number Grid | `goal:"data"`, 2x2 metrics | 2x2 `kpi_card()` layout |

**Content relationship → visual strategy:**

| Relationship | Visual Strategy | FreeStyle Trigger | Build Implementation |
|--------------|----------------|-------------------|---------------------|
| Sequential | Timeline | `component_category:"timeline"` | Custom timeline with `rect()`/`oval()`/`text()` |
| Contrast | Comparison Split | `goal:"content"` two-col | `comparison_bars()` |
| Primary+secondary | Unequal layout | `--layout-variant sidebar-left` | Sidebar `rect()` + main content |
| Equal-weight | Card Row | `goal:"features"` | `highlight_cards()` |
| Hierarchical | Hierarchy tree | `component_type:"group"` | Custom tree with `rect()`/`text()` |
| Evidence | Center + orbit | Auto | `oval()` + `text()` |
| Process | Cycle/Process | `component_category:"process"` | Custom cycle with `oval()`/`text()` |
| Data-driven | Big Number/Chart | `goal:"data"` | `kpi_card()` or `bar_chart()` |

### Redesign Protocol
- Greenfield: start from Dial baseline
- Redesign-Preserve: audit brand tokens → incremental evolution
- Redesign-Overhaul: visually equivalent to greenfield
- Audit before modifying: brand tokens / information architecture / content blocks / patterns to keep / patterns to kill
- Modernization levers (in order): fonts → spacing → colors → animations → key-page rebuild → full replacement
- Never silently change: page order / navigation labels / logo / legal copy

### Design System Mapping
- Consulting/finance → sidebar + diagram engine process/hierarchy
- Tech talks → code block + diagram engine infographic
- Education → exercise page + built-in bullets
- Creative proposals → custom blocks + AI images
- Brand launch → full-bleed images + minimal text
- **Scientific research** → Figure-style pages + semantic biology colors + sequence alignment + citations + NO animation
- **Academic thesis** → chapter flow + formal serif + citations + bibliography + NO animation
- **Engineering** → architecture diagrams + code blocks + spec tables + dark bg code
- **Medical/clinical** → clinical data tables + survival curves + evidence citations + disclaimers + NO animation
- **Government** → executive summary + numbered sections + flag colors + compliance tables + NO animation
- ONE design system per deck — no mixing McKinsey sidebar with Nature Figure style

### Performance & Accessibility
- <50 shapes per slide | images: cover-fit crop, never stretch | cache-first
- Public-sector / accessibility scenes: motion ≤3 | unknown audience: motion ≤5
- Dark mode: no pure black (#000) or pure white (#FFF) — use near-black/near-white
- Z-order: background < content < decoration < overlay

### Scope Exclusions
- Pure data tables → Excel | Multi-step forms → Web app | Real-time collaboration → Dedicated app | Interactive dashboards → Power BI/Tableau | Long documents (>50 pages) → Word/PDF

### Pre-Flight Check
- [ ] Basics: fonts ≥11pt | pages ≥3 shapes | text on every page | images correct | no broken links
- [ ] Consistency: accent color throughout | corner radius uniform | font pair uniform | theme locked | font-size levels ≥4
- [ ] Typography: cover title ≤2 lines | subtitle ≤20 chars | inner title ≤2 lines | no rotated text | line-height ≥1.1 for italic
- [ ] Layout: adjacent pages different layout family | 8+ pages ≥4 layouts | first card featured | no 3 consecutive same-structure pages | alternation ≤2
- [ ] Labels: eyebrow ≤ceil(pages/3) | no numbered eyebrows | no image overlay labels | no status dots | no generic step labels
- [ ] Color: no default-blue cover (unless specified) | no default gold+navy | chart colors from palette | dark-theme contrast sufficient | no light-gray on white
- [ ] Rhythm: 6+ pages have divider | hook ≠ cta visually | density varies | high-density followed by low | ≤1 core message per page
- [ ] Content: no AI Tells violations | no fake precision numbers | bullets have logical relation | quotes ≤3 lines with attribution
- [ ] Visuals: cover has real visual | minimalist ≥2-3 pages with images | bento ≥2-3 cells varied | logo wall uses images
- [ ] Scene: projection contrast OK | print doesn't rely on animation | large-screen numbers ≥36pt
- [ ] Animation: each has stated purpose | motion>4 has real animations | marquee ≤1/page
- [ ] Dial: values derived from Design Read | variance>4 has asymmetric layouts | density varies across pages

## Python API

```python
from ppt_pro_max import generate_ppt, fetch_image

# Build Mode (primary delivery mode)
# LLM writes build.py using build_helpers — see Build Helpers API section

# FreeStyle
result = generate_ppt("AI startup investor pitch", style="dark cyberpunk", fetch_images=True)

# With content.json (agent-driven — recommended). query is OPTIONAL when content_file contains slides[].
# content_file with slides[] bypasses StoryPlanner/ContentGenerator and renders your pages directly.
result = generate_ppt(content_file="content.json", style="warm fintech", fetch_images=True)
result = generate_ppt("pitch", content_file="content.json", style="dark-tech")

# With design dials
result = generate_ppt("pitch", content_file="content.json", style="professional",
                      layout_variant="sidebar-left", motion=5, density=6, variance=7)

# Proposal flow (DEPRECATED for proposals — use Build Mode build.py instead)
# This only swaps palette/mood, NOT layout structure. Use build.py proposals for structural differentiation.
result = generate_ppt("pitch", proposal=True, style="dark cyberpunk")

# Standalone image generation
img = fetch_image("futuristic AI city", mode="generate", llm_provider="seedream", llm_api_key="...")
print(img["path"])
```

**Key generate_ppt() parameters:** `query`, `style`, `content_file`, `layout_variant`, `variance`, `motion`, `density`, `fetch_images`, `palette`, `fonts`, `decoration`, `mood`, `llm_provider`, `llm_api_key`, `pages`

## 4-Phase Pipeline

1. **Story Planning** → strategy + page structure + emotion arc
2. **Design Decisions** → per-page layout/color/typography from 40K+ combos
3. **Content Generation** → copy formulas (PAS/FAB/AIDA) + image keywords
4. **PPT Rendering** → python-pptx direct, 12 master layouts, QA gates

## Design Atoms (40,000+ Combos)

| Atom | Count | Examples |
|------|-------|----------|
| Color Palettes | 25 | ocean-blue, cyber-neon, golden-luxury, wine-burgundy, midnight-navy, monochrome-dark... |
| Font Pairs | 20 | modern-sans, elegant-serif, tech-mono, contrast-mix, sharp-modern... |
| Decorations | 10 | accent-bar, neon-lines, gold-trim, diamond-bullets, gradient-bar, sidebar-nav, minimal-dots, circle-accent, no-decoration, full-bleed-overlay |
| Layout Variants | 8 | standard, centered, sidebar-left, sidebar-right, grid-2x2, asymmetric... |

Natural language: `--style "warm fintech"` auto-selects matching atoms. Decoration and layout-variant atoms are consumed by PrecisionRenderer — they control title decoration, margin positioning, and card style.

## 10 Diagram Types

| Type | Description | Data Format |
|------|-------------|-------------|
| Flowchart | Process flow, auto horizontal/vertical | nodes + connectors |
| Funnel | Decreasing width stages | stages (items) |
| Timeline | Alternating top/bottom labels | events (items) |
| SWOT | 4-quadrant analysis | strengths/weaknesses/opportunities/threats |
| Matrix | Comparison grid | rows + columns |
| Cycle | Circular arrangement | stages (items) |
| Table | Alternating row colors | headers + rows |
| Hierarchy | Parent-child tree | nodes with parent |
| Pyramid | Stacked levels | levels (items) |
| Venn | 2-3 set intersection | sets with labels |

## Image Engines

**⚠️ ALWAYS use the built-in CLI or Python API to generate images. NEVER write custom scripts to call image APIs — the CLI already handles cache-first, retry, multi-engine fallback, and cover-fit cropping.**

### When you need an image — use one of these:

**CLI (preferred for standalone image generation):**

```bash
# Generate AI image (auto-selects available engine)
python -m ppt_pro_max image "futuristic AI city" --llm-provider seedream --llm-api-key $ARK_API_KEY

# Search stock photos
python -m ppt_pro_max image "team meeting" --image-mode search --unsplash-key $KEY

# Auto mode: AI generation → fall back to search
python -m ppt_pro_max image "product launch" --llm-provider seedream -v
```

**Python API (preferred when called from build.py or generate_ppt):**

```python
from ppt_pro_max import fetch_image

# Generate AI image
result = fetch_image("futuristic AI city", mode="generate", llm_provider="seedream", llm_api_key="...")
print(result["path"])  # Local file path — use this in add_picture() or circle_image()

# Search stock photos
result = fetch_image("team meeting", mode="search", unsplash_access_key="...")

# Auto: generate → fall back to search
result = fetch_image("product launch", mode="auto", llm_provider="seedream", llm_api_key="...")
```

**In FreeStyle pipeline — just pass --fetch-images:**

```bash
python -m ppt_pro_max "AI pitch" --fetch-images --llm-provider seedream --llm-api-key $ARK_API_KEY
```

**In Build mode — use `ai_image()` (one call) or `fetch_image()` + placement:**

```python
from ppt_pro_max.build_helpers import *

# ONE call: generate image + place cover-fit (auto mode: AI → search fallback)
ai_image(slide, 1.0, 2.0, 5.0, 3.0, "protein structure 3D",
         mode="generate", llm_provider="seedream", llm_api_key="...")

# Or fetch a path first, then place it with any image helper
r = fetch_image("protein structure 3D", mode="generate", llm_provider="seedream", llm_api_key="...")
circle_image(slide, 6.5, 3.5, 1.5, r["path"])
```

### Engine Reference

| Engine | Provider | Env Key | Default Model |
|--------|----------|---------|---------------|
| Seedream | Volcengine | ARK_API_KEY | doubao-seedream-4-5-251128 |
| GPT Image | OpenAI | OPENAI_API_KEY | gpt-image-1 |
| DALL-E 3 | OpenAI | OPENAI_API_KEY | dall-e-3 |
| Wanx | Alibaba | DASHSCOPE_API_KEY | wanx-v1 |
| Kimi K2.6 | Moonshot | MOONSHOT_API_KEY | kimi-k2-0711-preview |

Image modes: `placeholder` (default), `search` (Unsplash/Pexels), `generate` (AI), `enhance` (Kimi keyword optimization + search). All engines use **cache-first**.

## Animation System

- **12 Transitions**: fade, push, wipe, split, cover, dissolve, wheel, wedge, blinds, checker, comb, random
- **11 Entrances**: appear, fly_in, fade_in, zoom_in, float_up, bounce, etc.
- **Motion mapping**: 1-2 = transitions only, 3-5 = fade_in entrance, 6-10 = fly_in entrance
- Applied via XML injection (python-pptx 1.0.2 has no native transition API)

## Project Structure (Build & VI Build)

```
my-project/
├── template.pptx    # Brand template (VI Build only)
├── brand.json       # Brand spec (colors, fonts, logo, footer, watermark)
├── content.json     # Page content for FreeStyle/generate_ppt()
├── build.py         # Build Script or VI Build entry point
├── logo.png         # Company logo
├── images/          # Local images
└── output/
    ├── v1/          # Version 1
    │   ├── presentation.pptx
    │   └── meta.json
    └── v2/          # Version 2 (auto-incremented)
```

## content.json Format

```json
{
  "meta": {"title": "...", "author": "..."},
  "slides": [
    {
      "goal": "hook|problem|solution|features|cta|content|data|code|exercise|section|testimonials|overview",
      "title": "Page Title",
      "subtitle": "Optional subtitle",
      "bullets": ["Point 1", "Point 2"],
      "image": "images/photo.png",
      "cards": [{"title": "...", "text": "..."}],
      "diagram": {"type": "flowchart", "data": {"nodes": [{"id": "a", "text": "A"}], "connectors": [["a", "b"]]}},
      "code": {"language": "python", "source": "..."},
      "exercise": {"instructions": "...", "duration": "5 min", "steps": [...]},
      "chart": {"type": "bar", "title": "...", "categories": ["A", "B"], "series": [{"name": "S", "values": [1, 2]}]},
      "section_number": "01",
      "component_type": "group",
      "component_category": "process"
    }
  ]
}
```

**chart format (must match ChartBuilder — `categories`/`series` at top level):**

```json
{
  "chart": {
    "type": "bar",              // bar|line|pie|doughnut|area|scatter|radar|... (28 types)
    "title": "Accuracy Over Time",
    "categories": ["Baseline", "v1.0", "v2.0", "v3.0"],
    "series": [{"name": "Accuracy", "values": [45, 72, 88, 97]}]
  }
}
```
> Do NOT use `labels` (use `categories`), `datasets` (use `series`), or a `data` wrapper. Use `doughnut` not `donut` (unknown type silently falls back to `bar`). Chart text (title/legend/axes/data labels) is auto-themed to the style.

**Goal types and rendering behavior:**

| Goal | Rendering | Notes |
|------|-----------|-------|
| `hook` | Hero: full-bleed gradient + centered title + subtitle | First slide; short subtitle recommended |
| `cta` | Hero: full-bleed gradient + centered title + subtitle | Last slide; long subtitle recommended |
| `section` | Section divider: oversized number + title + accent bar | Use `section_number` for custom number ("01" or 1); defaults to page_index+1 |
| `problem`/`solution`/`content` | Title band + bullets + optional image | 6+ bullets → two-column |
| `features` | Title + cards row | First card featured (gradient bar, 22pt title); use `cards`, not bullets |
| `data` | Title + **chart** | Use `chart` for real charts; falls back to bullets/diagram if absent |
| `code` | Title + dark code block + language badge | `language` + `source` required |
| `exercise` | Title + badge (ALL CAPS) + instructions + numbered steps | `duration` + `steps` recommended |
| `testimonials` | Title + bullets (same as content — no dedicated quote layout) | Use `bullets` |
| `overview` | Title + bullets or diagram | Same as content |

**Render priority per slide:** `blocks` > `cards` > `component_type` > `diagram` > `code` > `exercise` > `bullets`. `chart` and `image` render **additively** (on top) — avoid combining them with other content fields on the same page.

**Field → layout selection:** the same goal can render differently based on which field you populate. E.g. `features` + `cards` → card row; `features` + `bullets` → bullet list; `content` + `diagram` → diagram.

**diagram format:** `{"type": "flowchart|funnel|timeline|swot|matrix|cycle|table|hierarchy|pyramid|venn", "data": {...}}`. Node/stage text reads from `label`/`title`/`text` keys (any works). The inner `data` object is what the diagram engine consumes.

**Component opt-in (FreeStyle passthrough):** in agent-driven FreeStyle, proactive component auto-matching is **disabled** — add `component_type` + `component_category` explicitly to a slide to use a library component, otherwise the goal-based layout is used.

## brand.json Format

```json
{
  "colors": {
    "primary": "#1E3A5F", "on-primary": "#FFFFFF",
    "accent": "#E8A838", "background": "#0A1E3D",
    "foreground": "#F0F4F8", "muted": "#1A2E4A",
    "muted-foreground": "#8A9BB5"
  },
  "logo": {"position": "top_right", "width_inches": 1.0, "skip_cover": true},
  "footer": {"text": "Company Name", "show_page_number": true},
  "watermark": {"text": "CONFIDENTIAL", "opacity": 0.1},
  "spacing": {
    "strip_style": "auto",
    "section_dividers": true
  }
}
```

**spacing options:**
- `strip_style`: `"auto"` (varied: left bar / bottom line / none, cycling by page), `"left"` (always left bar), `"none"` (no strip). Default: `"auto"`
- `section_dividers`: `true` (auto-insert section dividers on topic shifts), `false` (no dividers). Default: `true`

## Revision Workflow

- **Build/VI Build**: modify `build.py` and re-run — build.py is the single source of truth
- **FreeStyle**: modify `content.json` and regenerate — the `slides[]` array drives page count and content
- Run `BuildQA` before delivery to catch fatal issues (placeholders, blank pages, broken images, overflows)

```python
from ppt_pro_max.build_qa import BuildQA

report = BuildQA().check("output.pptx")
print(BuildQA().format_report(report))
# is_passable = no fatal issues
```

- **Debug loop**: after re-running `build.py`, render every slide to PNG + a single HTML contact sheet to eyeball layout without opening PowerPoint:

```bash
# CLI
python -m ppt_pro_max.render_preview output.pptx --open

# Python API (auto-detects PowerPoint COM on Windows / LibreOffice fallback)
from ppt_pro_max.render_preview import render_preview
result = render_preview("output.pptx", out_dir="output/preview/deck")
print(result["html"])   # open this in a browser
```

**⚠️ Codex sandbox / CI / headless**: PowerPoint COM fails with WinError 1312 (no interactive desktop). Use `preview()` from build_helpers — it auto-falls-back to LibreOffice headless (needs soffice.bin + poppler/pdftoppm):

```python
from ppt_pro_max.build_helpers import *
preview("output.pptx")                        # auto: COM → LibreOffice
preview("output.pptx", engine="libreoffice")  # Codex sandbox / headless
```

## UX Intelligence API (内置设计数据库 — MANDATORY for Build Mode)

**⚠️ BEFORE writing any build.py, you MUST query the bundled design database (ui_ux_adapter → design_search) for domain-specific design intelligence.** This is the single biggest quality differentiator — without it, you're guessing colors/fonts/styles; with it, you get professional-grade design decisions backed by a searchable database of real-world patterns (bundled inside ppt_pro_max, no external dependency required).

Import: `from ppt_pro_max.adapters.ui_ux_adapter import is_available, get_design_system, search_design, search_style, search_color, search_typography, search_reasoning`

### API Reference

| Function | Purpose | Returns |
|----------|---------|---------|
| `is_available()` | Check if the bundled design database is available | `bool` |
| `get_design_system(query, variance=None, motion=None, density=None)` | Full design system for a project | `dict` with colors, typography, style, pattern, anti_patterns, decision_rules, dials |
| `search_design(query, domain=None, max_results=3)` | Search product/UX patterns | `list[dict]` with Product Type, Keywords, Primary Style Recommendation, Landing Page Pattern |
| `search_style(query, max_results=3)` | Search visual style patterns | `list[dict]` with Style Category, Effects & Animation, Dark Mode, Light Mode |
| `search_color(query, max_results=2)` | Search color palettes | `list[dict]` with palette recommendations |
| `search_typography(query, max_results=2)` | Search font pairings | `list[dict]` with heading/body font recommendations |
| `search_reasoning(category)` | Get reasoning rules for a domain | `dict` with decision rules |

### How to Use in Build Mode

**Step 1: Query design intelligence** (before writing C dict):
```python
from ppt_pro_max.adapters.ui_ux_adapter import is_available, get_design_system, search_color, search_style

if is_available():
    ds = get_design_system('AI startup investor pitch', variance=5, motion=3, density=5)
    ux_colors = ds.get('colors', {})       # → {'primary': '#7C3AED', 'accent': '#EC4899', ...}
    ux_typo = ds.get('typography', {})     # → {'heading': 'Inter', 'body': 'Inter', ...}
    ux_style = ds.get('style_name', '')    # → 'AI-Native UI'
    ux_effects = ds.get('style_effects', '')  # → 'Glassmorphism + micro-interactions'
    ux_anti = ds.get('anti_patterns', '')  # → 'Heavy chrome + Slow response feedback'
    ux_pattern = ds.get('pattern_name', '')   # → 'SaaS Landing'
    ux_dials = ds.get('dials', {})         # → {'variance': 7, 'motion': 4, ...}
```

**Step 2: Build C dict from UX intelligence** (not hardcoded):
```python
C = {
    'primary': ux_colors.get('primary', '#2E6504'),
    'accent': ux_colors.get('accent', '#7DA92F'),
    'muted': ux_colors.get('muted', '#81C784'),
    'light': ux_colors.get('border', '#C8E6C9'),
    'white': '#FFFFFF',
    'background': ux_colors.get('background', '#FFFFFF'),
    'card_bg': '#F9F9F9',
    'text_dark': ux_colors.get('foreground', '#1A1A1A'),
    'text_body': ux_colors.get('text', '#333333'),
    'text_muted': '#666666',
    'divider': '#CCCCCC',
    'font_heading': ux_typo.get('heading', 'Calibri'),
    'font_body': ux_typo.get('body', 'Calibri'),
    'font_cjk': '微软雅黑',  # REQUIRED for Chinese content — auto-sets a:ea/a:cs typeface
}
```

**⚠️ CJK font rule**: If ANY slide text contains Chinese/Japanese/Korean characters, you MUST set `'font_cjk'` in the C dict. Without it, CJK characters fall back to SimSun (宋体) which looks unprofessional. Recommended CJK fonts: `微软雅黑`, `思源黑体`, `PingFang SC`, `Noto Sans CJK`.

**Step 3: Use anti-patterns to avoid mistakes**:
- If `ux_anti` says "Heavy chrome" → avoid thick borders, heavy shadows
- If `ux_anti` says "Slow response feedback" → add subtle entrance animations
- If `ux_anti` says "Wall of text" → use cards, KPI grids, not bullet lists

**Step 4: Use style effects for decoration choices**:
- `ux_effects` = "Glassmorphism" → use `add_glass_panel()`, frosted glass
- `ux_effects` = "Neon + glow" → use `add_neon_border()`, `apply_glow()`
- `ux_effects` = "Minimal clean" → use `top_bar()` only, no decorations

### Proposal Differentiation with UX Search

For 3 proposals, search 3 different style/color/typography combinations:
```python
# Proposal A: Style closest to user's description
ds_a = get_design_system(query, variance=5, motion=3, density=5)
# Proposal B: Alternative style direction
style_b = search_style("tech dashboard", 1)  # Different style query
# Proposal C: Radical departure
color_c = search_color("vibrant neon", 1)    # Different color query
```

## Build Helpers API (for Build/VI Build mode)

LLM writes `build.py` scripts using these functions. Import: `from ppt_pro_max.build_helpers import *`

### Which function should I use? — Decision Trees

#### Data Visualization Decision Tree:

```
Need to show data?
├─ Standard chart with axes/gridlines/legend?
│  ├─ Bar/Line/Pie/Area/Scatter → native_chart()
│  └─ Radar/Bubble/Stock → native_chart()
├─ Custom visual (no axes, brand-styled)?
│  ├─ Horizontal progress bars → bar_chart()
│  ├─ Before/after comparison → comparison_bars()
│  ├─ Donut with center KPI → donut_chart(native=False)
│  └─ Donut with multiple sectors → donut_chart(native=True)
├─ Single metric highlight?
│  └─ kpi_card()
└─ Multiple metrics in a row?
   └─ highlight_cards()
```

#### Text Effect Decision Tree:

```
Need text styling beyond plain?
├─ Gradient fill → gradient_text(preset='gold-shine')
├─ Outline/stroke → text_outline(color='#FFF', width=2)
├─ Drop shadow → text_shadow(blur=8, distance=3)
├─ Neon glow → text_glow(color='#0FF', size=8)
├─ Vertical (CJK) → vertical_text(direction='ea')
└─ Code with syntax badge → code_block(language='python')
```

#### Image Decision Tree:

```
Need to add an image?
├─ Full rectangle (cover-fit, NO stretch) → cover_image()
├─ Circle crop → circle_image()
├─ Hexagon crop → hex_image()
├─ Star crop → star_image(points=5)
├─ Diamond crop → diamond_image()
├─ Heart crop → heart_image()
├─ Any MSO_SHAPE crop → shape_image(shape_type='HEXAGON', ...)
├─ Soft edge fade → soft_edge_image()
├─ Duotone effect → duotone_image()
├─ Artistic effect → artistic_image(effect='watercolor_sponge')
└─ Need to adjust after placing? → adjust_image(shape, brightness=20)
```

#### Shape Effect Decision Tree:

```
Need to enhance a shape?
├─ Shadow → add_shadow(shape, blur=8, distance=3)
├─ Glow → add_glow(shape, color='#0FF', size=8)
├─ 3D extrusion → shape_3d(depth=10)
├─ Bevel → bevel_shape()
├─ Pattern fill → pattern_fill(pattern_type='crosshatch', ...)
├─ Frosted glass → frosted_panel(tint='#FFF', alpha=50)
└─ Spotlight overlay → spotlight(cx, cy, radius, alpha=70)
```

### Color Dictionary (C)

```python
C = {
    'primary': '#2E6504', 'accent': '#7DA92F', 'muted': '#81C784',
    'light': '#C8E6C9', 'white': '#FFFFFF', 'background': '#FFFFFF',
    'card_bg': '#F9F9F9', 'text_dark': '#1A1A1A', 'text_body': '#333333',
    'text_muted': '#666666', 'divider': '#CCCCCC',
    'font_heading': '微软雅黑', 'font_body': '微软雅黑',
}
```

### Classes

| Class | Attributes | Purpose |
|-------|-----------|---------|
| `Typography` | `hero`, `h1`, `h2`, `h3`, `body`, `caption`, `micro` (all pt) | Font size scale per design style; access via `t.hero`, `t.h1`, etc. |
| `Spacing` | `page_margin`, `section_gap`, `card_gap`, `card_padding`, `line_height`, `bar_gap` (all inches or ratio) | Spacing system per design style; access via `sp.page_margin`, etc. |

**Predefined scales:**

| Key | TYPOGRAPHY | SPACING | Best For |
|-----|-----------|---------|----------|
| `'mckinsey'` | hero=44, h1=28, h2=20, h3=16, body=12 | margin=0.65, card_gap=0.35 | Consulting, finance, structured reports |
| `'cyberpunk'` | hero=48, h1=28, h2=18, h3=14, body=11 | margin=0.8, card_gap=0.4 | Tech, dark theme, information-dense |
| `'creative'` | hero=44, h1=28, h2=22, h3=18, body=13 | margin=0.8, card_gap=0.4 | Creative, playful, approachable |
| `'professional'` | hero=44, h1=28, h2=20, h3=16, body=12 | margin=0.65, card_gap=0.35 | Corporate, general business |
| `'minimal'` | hero=40, h1=24, h2=18, h3=14, body=11 | margin=1.0, card_gap=0.5 | Minimalist, breathing room |
| `'cjk_mckinsey'` | hero=44, h1=30, h2=22, h3=18, body=14 | margin=0.65, card_gap=0.35 | **Chinese/Japanese/Korean** — body+2pt for CJK readability |
| `'cjk_professional'` | hero=44, h1=30, h2=22, h3=18, body=14 | margin=0.65, card_gap=0.35 | **CJK corporate** — same as cjk_mckinsey |
| `'cjk_creative'` | hero=44, h1=30, h2=24, h3=20, body=15 | margin=0.8, card_gap=0.4 | **CJK creative** — larger body for comfort |

⚠️ **CJK font size rule**: Chinese/Japanese/Korean characters visually appear ~30% smaller than Latin at the same pt value. Always use `cjk_*` presets (body=14-15) for CJK content instead of Latin presets (body=11-12).

Usage: `t = TYPOGRAPHY['mckinsey']` then `font_size=t.h1`. Same pattern for `sp = SPACING['mckinsey']`.

### Functions — Page Structure

| Function | Purpose | Key Params |
|----------|---------|------------|
| `add_slide(prs, layout_index)` | Add blank slide | Auto-finds blank layout; layout_index optional |
| `hero_slide(slide, title, subtitle, C, typo)` | Cover/hero page | Full-bleed primary bg + large title; grouped=True |
| `cta_slide(slide, title, subtitle, C, typo)` | Call-to-action page | Full-bleed primary bg + title + subtitle; grouped=True |
| `section_divider(slide, number, title, C, typo)` | Section divider | Oversized number + title + gradient line; grouped=True |
| `page_header(slide, title, subtitle, C, left, width, typo, spacing)` | Title + subtitle + divider line | left=0.65, width=None by default |

### Functions — Data & Charts

**Two chart systems — choose based on scenario:**

| Function | Type | When to Use | Key Params |
|----------|------|-------------|------------|
| `native_chart()` | **Native chart** | Standard data charts with real data; needs axes, gridlines, editable data table, legend, accurate proportions | chart_type, categories, series, style |
| `bar_chart()` | Shape composite | Custom progress bars, rounded bars, icon bars, brand-styled horizontal bars where native charts can't achieve the visual | data: [(label, pct, val)]; max_width=5.0 |
| `comparison_bars()` | Shape composite | Before/after comparison, A/B metrics, custom dual-bar layouts | metrics: [(label, v_old, v_new, pct_old, pct_new)] |
| `donut_chart()` | Hybrid | Multi-sector → auto-routes to native doughnut; single-sector or native=False → Shape composite for custom center KPI | sectors: [(name, pct_str, color)]; native=True |
| `kpi_card()` | Shape composite | Single metric highlight with trend arrow | number, label, trend, trend_up |
| `highlight_cards()` | Shape composite | Multi-metric card row | cards: [(title, desc, accent_color)] |

**Chart selection guide:**
- Standard bar/line/pie/area/scatter with real data → `native_chart()` (editable, accurate axes, gridlines)
- Custom visual: rounded progress bars, icon bars, gauge, waffle → `bar_chart()` / Shape组合
- Simple donut/pie with multiple sectors → `native_chart(chart_type='doughnut')` or `donut_chart(native=True)`
- Custom donut with center KPI number, brand decorations → `donut_chart(native=False)`
- Before/after comparison with custom styling → `comparison_bars()`
- Before/after with standard axes → `native_chart(chart_type='bar_horizontal_stacked')`

#### `native_chart()` — Native PowerPoint Chart

```python
native_chart(slide, left, top, width, height, chart_type,
             categories=None, series=None, style=None, C=None)
```

**chart_type** (24 types):
| Category | Types |
|----------|-------|
| Column | `bar`, `bar_stacked`, `bar_100`, `bar_3d` (falls back to 2D) |
| Bar (horizontal) | `bar_horizontal`, `bar_horizontal_stacked`, `bar_horizontal_100` |
| Line | `line`, `line_markers`, `line_stacked`, `line_stacked_100` |
| Pie | `pie`, `pie_3d` (falls back to 2D), `pie_exploded` |
| Doughnut | `doughnut`, `doughnut_exploded` |
| Area | `area`, `area_stacked`, `area_stacked_100` |
| Scatter | `scatter`, `scatter_lines`, `scatter_smooth` |
| Radar | `radar`, `radar_markers` |
| Bubble | `bubble` |
| Stock | `stock_hlc`, `stock_ohlc` |

**series** format:
- Category charts: `[{'name': 'Revenue', 'values': [30, 45, 60, 75]}, ...]`
- Scatter: `[{'name': 'Data', 'values': [[1, 10], [2, 25], [3, 18]]}]`
- Bubble: `[{'name': 'Data', 'values': [[1, 10, 5], [2, 25, 8]]}]`

**style** dict (all optional):
| Key | Default | Description |
|-----|---------|-------------|
| `show_legend` | `True` | Show/hide legend |
| `legend_position` | `'bottom'` | `'bottom'`/`'top'`/`'left'`/`'right'` |
| `show_labels` | `False` | Show data labels on points |
| `show_value` | `True` | Show numeric value in label |
| `show_percentage` | `False` (pie: `True`) | Show percentage in label |
| `show_category_name` | `False` | Show category name in label |
| `label_font_size` | `9` | Data label font size (pt) |
| `label_position` | `'outside_end'` | `'center'`/`'inside_end'`/`'outside_end'`/`'best_fit'` |
| `number_format` | — | e.g. `'#,##0'`, `'0.0%'`, `'$#,##0'` |
| `color_scheme` | `'brand'` | `'brand'`/`'auto'`/`['#hex', ...]` |
| `title` | — | Chart title text |
| `value_axis_title` | — | Y-axis title |
| `category_axis_title` | — | X-axis title |
| `gridlines` | `'major_y'` | `'none'`/`'major_y'`/`'major_x'`/`'major_xy'` |
| `tick_number_format` | — | Axis tick format |
| `chart_style` | — | 1-48 built-in PowerPoint chart style |

**Example:**
```python
native_chart(slide, 1.0, 1.5, 7.0, 4.5, 'bar',
    categories=['Q1', 'Q2', 'Q3', 'Q4'],
    series=[{'name': 'Revenue', 'values': [30, 45, 60, 75]},
            {'name': 'Cost', 'values': [20, 30, 35, 40]}],
    style={'show_legend': True, 'show_labels': True,
           'value_axis_title': 'Revenue ($M)',
           'gridlines': 'major_y', 'color_scheme': 'brand'},
    C=C)
```

#### `bar_chart()` — Shape-Based Horizontal Bars

```python
bar_chart(slide, left, top, data, max_width=5.0, bar_height=0.3, C=None, typo=None, spacing=None, grouped=True)
```
- data: `[(label, pct, val), ...]` — pct is 0.0-1.0 proportion, val is display string
- Use for: rounded progress bars, custom-styled horizontal bars, icon bars

#### `comparison_bars()` — Shape-Based Before/After

```python
comparison_bars(slide, left, top, metrics, max_width=4.0, C=None, typo=None, spacing=None, grouped=True)
```
- metrics: `[(label, v_old, v_new, pct_old, pct_new), ...]`
- Use for: before/after, A/B test, old vs new with custom dual-bar layout

#### `donut_chart()` — Hybrid Donut/Pie

```python
donut_chart(slide, cx, cy, radius, inner_radius, sectors, C=None, typo=None, grouped=True, native=True)
```
- sectors: `[(name, pct_str, color), ...]`
- **native=True** (default): sectors>1 → auto-routes to `native_chart(chart_type='doughnut')` with accurate sector angles; sectors==1 → Shape composite
- **native=False**: Always uses Shape composite (OVAL overlay) for maximum visual customization

### Functions — Chinese Character Writing Grids (汉字教学)

| Function | Purpose | Key Params |
|----------|---------|------------|
| `mizi_grid()` | 米字格 (cross + diagonal) | size, char, border_color, guide_color |
| `tian_grid()` | 田字格 (cross only, no diagonals) | size, char, border_color, guide_color |
| `pinyin_grid()` | 四线格/拼音格 (4-line pinyin) | width, pinyin, baseline_y, line_spacing |
| `hanzi_row()` | Row of character grids | chars: list, grid_type: 'mizi'/'tian' |
| `pinyin_hanzi_block()` | Pinyin grid + character grid paired | items: [(pinyin, char), ...] |

#### `mizi_grid()` — 米字格

```python
mizi_grid(slide, left, top, size, char=None,
          border_color='#4CAF50', guide_color='#A0A0A0',
          border_pt=2.5, guide_pt=1.0, diag_pt=0.75,
          font_size=160, font_name='SimSun', font_color='#000000')
```
- **8 lines**: 4 border (solid, green) + 2 cross (dashed, gray) + 2 diagonal (dashed, gray)
- `char`: optional character overlay in transparent textbox (SimSun 160pt, anchor=center, zero margins)
- Example: `mizi_grid(s, 1.0, 1.5, 2.5, char='永')`

#### `tian_grid()` — 田字格

```python
tian_grid(slide, left, top, size, char=None,
          border_color='#4CAF50', guide_color='#A0A0A0',
          border_pt=2.5, guide_pt=1.0,
          font_size=160, font_name='SimSun', font_color='#000000')
```
- **6 lines**: 4 border (solid, green) + 2 cross (dashed, gray) — no diagonals

#### `pinyin_grid()` — 四线格/拼音格

```python
pinyin_grid(slide, left, top, width, pinyin=None,
            baseline_y=None, line_spacing=0.3,
            light_color='#A0A0A0', dark_color='#424242',
            light_pt=0.75, dark_pt=1.5,
            font_size=36, font_name='SimSun', font_color='#000000')
```
- **4 lines**: line1 (light), line2 (dark), line3/baseline (dark), line4 (light)
- `baseline_y`: Y position of the baseline (line3); defaults to `top + line_spacing * 2`
- `pinyin`: optional pinyin text in transparent textbox aligned to baseline

#### `hanzi_row()` — Character Grid Row

```python
hanzi_row(slide, left, top, size, chars, grid_type='mizi', gap=0.3, ...)
```
- `chars`: list of characters; `None` entries draw empty grids
- `grid_type`: `'mizi'` or `'tian'`
- Example: `hanzi_row(s, 1.0, 1.5, 2.0, ['永', None, '和'], grid_type='mizi')`

#### `pinyin_hanzi_block()` — Pinyin + Character Paired Block

```python
pinyin_hanzi_block(slide, left, top, size, items, gap=0.3, grid_type='mizi', ...)
```
- `items`: list of `(pinyin, char)` tuples; use `None` for empty
- `grid_type`: `'mizi'` or `'tian'` — controls character grid style
- Draws pinyin grid above + character grid below for each item
- Example: `pinyin_hanzi_block(s, 0.5, 0.5, 2.0, [('yǒng','永'), ('hé','和'), (None, None)])`

### Functions — Text & Code

| Function | Purpose | Key Params |
|----------|---------|------------|
| `text(slide, left, top, width, height, txt, font_size, color, bold, align, font_name, C, anchor)` | Single-line text | color: role name or hex; anchor: 'top'/'middle'/'bottom' |
| `multiline(slide, left, top, width, height, lines, font_size, color, bold, align, font_name, C, line_spacing)` | Multi-line text | lines: list of strings; bold/align/font_name optional |
| `gradient_text(slide, left, top, width, height, txt, preset, stops, font_size, bold, font_name, align)` | Gradient-filled text | preset: 'gold-shine', etc.; or custom stops |
| `vertical_text(slide, left, top, width, height, txt, direction, font_name, font_size, color, bold, align)` | Vertical text | direction: 'ea' (east-asian); defaults: STKaiti 24pt |
| `code_block(slide, left, top, width, height, lines, language, C, typo)` | Code block with language badge | lines: list of code strings; dark bg #1E1E1E; grouped=True |
| `text_outline(slide, left, top, width, height, txt, color, width_pt, font_size, bold, font_name, C, align)` | **Outlined text** | color: outline color; width_pt: thickness; great for dark backgrounds |
| `text_shadow(slide, left, top, width, height, txt, blur_pt, distance_pt, direction_deg, color, alpha_pct, font_size, bold, font_name, C, align)` | **Shadowed text** | blur_pt: shadow blur; distance_pt: offset; adds depth to titles |
| `text_glow(slide, left, top, width, height, txt, color, size_pt, alpha_pct, font_size, bold, font_name, C, align)` | **Glowing text** | color: glow color; size_pt: glow radius; cyberpunk/neon style |

**Gradient presets**: `gold-shine`, `blue-deep`, `purple-neon`, `ink-wash`, `cyber-cyan`, `sunset`, `emerald`, `rose-gold`, `seal-red`, `steel`

### Functions — Shapes

| Function | Purpose | Key Params |
|----------|---------|------------|
| `rect`, `rrect`, `oval` | Basic shapes | (left, top, width, height, fill, line, C) |
| `shape(slide, shape_type, left, top, width, height, fill, line, C)` | **Any MSO_SHAPE** | shape_type: enum or string name |
| `hexagon`, `pentagon`, `octagon`, `diamond` | Polygon shapes | (cx, cy, size, fill, line, C) |
| `triangle`, `right_triangle`, `parallelogram`, `trapezoid` | Triangle shapes | (left, top, width, height, fill, line, C) |
| `star5`, `star6`, `star8`, `star10`, `star12` | N-point star | (cx, cy, size, fill, line, C) |
| `donut`, `heart`, `cross`, `moon`, `sun`, `block_arc`, `gear`, `tear` | Special shapes | (cx, cy, size, fill, line, C); gear(teeth=6/9) |
| `arrow`, `chevron`, `cloud`, `lightning`, `funnel`, `wave` | Directional shapes | (left, top, width, height, fill, line, C) |
| `callout(slide, ..., style='rect')` | Callout bubble | style: 'rect'/'round'/'oval'/'cloud' |
| `flow_process/decision/data/document/connector` | Flowchart shapes | Corner or center based |
| `top_bar`, `shape_3d`, `bevel`, `pattern_fill`, `frosted_panel` | Effects shapes | See signatures above |

**`shape()` string names** — most useful for PPT design:

| Category | Names (pass as string, e.g. `shape(s, 'HEXAGON', ...)`) |
|----------|---------|
| Polygons | HEXAGON, PENTAGON, OCTAGON, DIAMOND, DECAGON, DODECAGON, HEPTAGON |
| Stars | STAR_4_POINT, STAR_5_POINT, STAR_6_POINT, STAR_8_POINT, STAR_10_POINT, STAR_12_POINT |
| Arrows | RIGHT_ARROW, LEFT_ARROW, UP_ARROW, DOWN_ARROW, BENT_ARROW, CHEVRON, NOTCHED_RIGHT_ARROW, U_TURN_ARROW, CIRCULAR_ARROW, QUAD_ARROW |
| Flowchart | FLOWCHART_PROCESS, FLOWCHART_DECISION, FLOWCHART_DATA, FLOWCHART_DOCUMENT, FLOWCHART_CONNECTOR, FLOWCHART_TERMINATOR |
| Callouts | RECTANGULAR_CALLOUT, ROUNDED_RECTANGULAR_CALLOUT, OVAL_CALLOUT, CLOUD_CALLOUT |
| Special | HEART, LIGHTNING_BOLT, CLOUD, MOON, SUN, CROSS, DONUT, FRAME, BEVEL, CUBE, WAVE, TEAR, FUNNEL, GEAR_6, GEAR_9, PLAQUE, FOLDED_CORNER, BLOCK_ARC, NO_SYMBOL |
| Math | MATH_PLUS, MATH_MINUS, MATH_MULTIPLY, MATH_DIVIDE, MATH_EQUAL |
| Ribbons | UP_RIBBON, DOWN_RIBBON, CURVED_UP_RIBBON, CURVED_DOWN_RIBBON |

### Functions — Boolean Shapes

Create shapes via boolean operations (subtract/union/intersect) — enables effects impossible with preset shapes. Requires `shapely` (`pip install shapely`); graceful fallback when not installed.

| Function | Purpose | Key Params |
|----------|---------|------------|
| `spotlight(slide, cx, cy, radius, alpha, color)` | Dark overlay with bright circular window | alpha=0-100 (default 70); hero/CTA slides |
| `bool_donut(slide, cx, cy, outer_r, inner_r, fill, line, C)` | Donut with custom hole size/position | Off-center hole; replaces MSO_SHAPE.DONUT |
| `bool_frame(slide, x, y, w, h, border, fill, line, C)` | Frame/border shape (outer minus inner) | border: width in inches |
| `bool_clipped_card(slide, x, y, w, h, clip_corners, clip_size, fill, line, C)` | Card with clipped corners | clip_corners: ['tl','tr','bl','br']; clip_size: inches |
| `bool_neon_tube(slide, x, y, w, h, wall, fill, C)` | Hollow neon tube shape | wall: thickness in inches; combine with glow |
| `bool_star(slide, cx, cy, r, points, inner_ratio, fill, line, C)` | Custom star with adjustable inner radius | inner_ratio: 0.0-1.0; any point count |
| `bool_cross(slide, cx, cy, w, h, bar_ratio, fill, line, C)` | Custom cross with adjustable bar thickness | bar_ratio: 0.0-1.0 |

**Advanced: custom boolean combinations** — when presets aren't enough:

```python
from ppt_pro_max.renderer.boolean_shapes import *

# Rectangle with circular hole
mask = bool_subtract(poly_rect(0, 0, 6, 4), poly_circle(3, 2, 1.5))
bool_shape(mask, slide, 1, 2, 6, 4, fill='#000000', alpha=70)

# Star-shaped image crop
star_geom = poly_star(3, 3, 2, inner_ratio=0.4, points=5)
bool_image(star_geom, slide, 2, 2, 2, 2, 'photo.jpg')

# Available primitives: poly_rect, poly_circle, poly_rounded_rect, poly_star, poly_regular, poly_points
# Operations: bool_subtract, bool_union, bool_intersect, bool_symdiff
# Render: bool_shape(geometry, slide, x, y, w, h, fill, line, C, alpha)
#         bool_image(geometry, slide, x, y, w, h, image_path, border_color)
```

See **[`shapes-reference.md`](src/ppt_pro_max/docs/shapes-reference.md)** for full API and examples.

### Functions — Image Effects

| Function | Purpose | Key Params |
|----------|---------|------------|
| `cover_image(slide, left, top, width, height, image_path)` | **Cover-fit image** (crop to fill, no stretch) | **PREFERRED** over add_picture — Pillow pre-crops to exact aspect ratio |
| `circle_image(slide, cx, cy, radius, image_path, border_color)` | Circle-cropped image | Center x/y + radius |
| `hex_image(slide, cx, cy, size, image_path, border_color)` | Hexagon-cropped image | Center + size |
| `star_image(slide, cx, cy, size, image_path, points=5, border_color)` | Star-cropped image | points: 5/6/8/10/12 |
| `diamond_image(slide, cx, cy, size, image_path, border_color)` | Diamond-cropped image | Center + size |
| `heart_image(slide, cx, cy, size, image_path, border_color)` | Heart-cropped image | Center + size |
| `shape_image(slide, shape_type, left, top, width, height, image_path, border_color)` | **Any shape** image crop | shape_type: MSO_SHAPE or string name |
| `soft_edge_image(slide, left, top, width, height, image_path, soft_radius)` | Soft-edge faded image | Feathered edge effect |
| `duotone_image(slide, left, top, width, height, image_path, color1, color2)` | Duotone image | Two-color mapping |
| `artistic_image(slide, left, top, width, height, image_path, effect, params)` | Artistic effect image | 22 effects: watercolor_sponge, etc. |
| `adjust_image(shape, brightness, contrast, saturation)` | **Adjust image brightness/contrast/saturation** | brightness/contrast: -100 to 100; saturation: 0-200 (100=normal) |

### Functions — Shape Effects

| Function | Purpose | Key Params |
|----------|---------|------------|
| `add_shadow(shape, blur_pt, distance_pt, direction_deg, color, alpha_pct)` | **Add shadow to any shape** | blur_pt=8, distance_pt=3, direction_deg=90, color='#000000', alpha_pct=25 |
| `add_glow(shape, color, size_pt, alpha_pct)` | **Add glow to any shape** | color='#00FFFF', size_pt=8, alpha_pct=40; cyberpunk/neon style |
| `shape_3d(slide, left, top, width, height, depth, material, extrusion_color, shape_type)` | 3D extrusion | depth=10, material='powder'; applies 3D to any shape |
| `bevel_shape(slide, left, top, width, height, top_w, top_h, material, shape_type)` | Bevel effect | top_w=4, top_h=2; bevel on any shape |
| `pattern_fill(slide, left, top, width, height, pattern_type, fg_color, bg_color, fg_alpha, shape_type)` | Pattern fill | 31 pattern types; see Pattern Types below |
| `frosted_panel(slide, left, top, width, height, tint, alpha, soft_edge)` | Frosted glass | tint='#FFFFFF', alpha=50, soft_edge=8 |

**Pattern types** (31): `cross`, `dark_downward_diagonal`, `dark_upward_diagonal`, `dark_horizontal`, `dark_vertical`, `small_checker`, `trellis`, `light_horizontal`, `light_vertical`, `light_downward_diagonal`, `light_upward_diagonal`, `narrow_horizontal`, `narrow_vertical`, `dashed_downward_diagonal`, `dashed_upward_diagonal`, `dashed_horizontal`, `dashed_vertical`, `small_confetti`, `large_confetti`, `zigzag`, `wave`, `diagonal_brick`, `horizontal_brick`, `weave`, `plaid`, `divot`, `dotted_grid`, `dotted_diamond`, `shingle`, `large_checker`, `large_grid`, `small_grid`, `solid_diamond`, `percent_5`-`percent_90`

### Functions — Template Analysis (VI Build)

| Function | Purpose | Key Params |
|----------|---------|------------|
| `analyze_pptx(pptx_path)` | **Extract design DNA from any PPTX** | Returns dict with colors, fonts, text_zones, images |

**Usage**:
```python
dna = analyze_pptx('client_template.pptx')
# dna['colors'] → color_palette (brand colors) + actual_colors
# dna['fonts'] → font_scheme + actual_fonts + actual_font_sizes
# dna['text_zones'] → slides[].shapes[]
# Use dna to build C dict and TYPOGRAPHY for VI Build
```

### Functions — Accessibility

| Function | Purpose | Key Params |
|----------|---------|------------|
| `check_contrast(color1, color2, min_ratio=3.0)` | WCAG contrast ratio check | Returns `(ratio, ok)`; min_ratio: 4.5=body text AA, 3.0=large text AA |
| `contrast_text(bg_color, min_ratio=4.5)` | Auto-select white or dark text | Returns `'#FFFFFF'` or `'#1A1A1A'` based on best contrast |

### Functions — Decorations

| Function | Purpose | Key Params |
|----------|---------|------------|
| `brush_divider(slide, left, top, width, color, thickness)` | Brush-stroke divider | Organic hand-drawn line |
| `seal_stamp(slide, left, top, size, txt, fill_hex, font_name, rotation, style, border_width_pt)` | Chinese seal stamp | Traditional red stamp; border_width_pt=4.0 |
| `neon_border(slide, left, top, width, height, color, radius)` | Neon glowing border | Cyberpunk-style glow |
| `glass_panel(slide, left, top, width, height, tint, alpha, soft_edge)` | Glassmorphism panel | Frosted glass effect |
| `grid_background(slide, spacing, color, alpha)` | Subtle grid background | Dot or line grid; spacing=1.0, color='#E0E0E0', alpha=15 |
| `ink_splash(slide, left, top, size, color, alpha)` | Ink splash decoration | Organic ink effect |

### Functions — Animation

| Function | Purpose | Key Params |
|----------|---------|------------|
| `slide_transition(slide, transition_type, speed, advance_on_click, advance_after_ms)` | Slide transition | 12 types: fade, push, wipe, etc. |
| `entrance_animation(slide, shape_id, effect, delay_ms, duration_ms, click_triggered)` | Entrance animation | 11 effects: fade_in, fly_in, zoom_in, etc. |
| `exit_animation(slide, shape_id, effect, delay_ms, duration_ms, click_triggered)` | Exit animation | 8 presets: fade_out, fly_out, etc. |
| `emphasis_animation(slide, shape_id, effect, delay_ms, duration_ms, click_triggered)` | Emphasis animation | 8 presets: pulse, grow, spin, etc. |

### Functions — Template (VI Build only)

| Function | Purpose | Key Params |
|----------|---------|------------|
| `copy_decorations(slide, template_slide, skip_long_text, skip_image)` | Copy decorations from template | skip_long_text=True, skip_image=True |
| `copy_logo(slide, template_slide, color_hints)` | Copy LOGO from template | Only finds GROUP shapes (shape_type==6) |

### Color Resolution
- Hex value: `'#2E6504'` → used directly
- Role name: `'primary'` → looks up `C['primary']`
- Missing role: returns `'#000000'` (never crashes)

### Reference: 10-Page Build Skeleton (verified end-to-end)

A proven 10-page structure mixing 4 layout families + 3 section dividers + KPI/chart/code/cards/comparison + CTA. Passes BuildQA (0 fatal/0 warning) with `cjk_professional` typography.

```python
from ppt_pro_max.build_helpers import *

C = {'primary': '#1E3A5F', 'accent': '#C9A96E', 'muted': '#5B7BA6',
     'light': '#D6E4F0', 'white': '#FFFFFF', 'background': '#F8FAFC',
     'card_bg': '#FFFFFF', 'bg_tint': '#F1F5F9', 'text_dark': '#1A2B3C',
     'text_body': '#37474F', 'text_muted': '#78909C', 'divider': '#E0E8F0',
     'font_heading': 'Georgia', 'font_body': 'Calibri', 'font_cjk': '微软雅黑'}
t = TYPOGRAPHY['cjk_professional']   # 中文 body=14pt, micro=11 (BuildQA-safe)
sp = SPACING['professional']

prs = Presentation()
set_widescreen(prs)
set_theme_colors(prs, C)   # 写入主题色, PowerPoint 可识别

# P1 cover: hero + in-canvas decorations
s = add_slide(prs)
hero_slide(s, '让企业智能触手可及', 'AI 企业服务 2026 年度战略汇报', C=C, typo=t)
donut(s, 10.9, 1.2, 1.6, C['accent'], C=C)   # 装饰圆环, 确保在画布内
rect(s, 0, 6.9, 13.333, 0.08, C['accent'], C=C)

# P2/P5/P8: section dividers
s = add_slide(prs); section_divider(s, 1, '市场洞察', C=C, typo=t)

# P3: KPI 2x2 grid
s = add_slide(prs)
page_header(s, '市场规模与增长', '中国企业级 AI 支出持续扩大', C=C, typo=t, spacing=sp)
kpi_card(s, 0.65, 1.9, 3.9, 1.4, '1,280亿', '市场规模', '年增 38.5%', C=C, typo=t)
kpi_card(s, 4.85, 1.9, 3.9, 1.4, '87.6%', '采纳率', '+12.3%', C=C, typo=t)

# P4: native chart (editable)
s = add_slide(prs)
page_header(s, '行业收入对比', '各行业 AI 支出（亿元）', C=C, typo=t, spacing=sp)
native_chart(s, 0.65, 2.0, 12.0, 4.6, 'bar',
             categories=['金融', '制造', '医疗'],
             series=[{'name': 'AI 支出', 'values': [520, 410, 320]}],
             style={'show_legend': False, 'show_labels': True, 'gridlines': 'major_y'},
             C=C)

# P6: code block + sidebar
s = add_slide(prs)
page_header(s, '核心引擎架构', '一次调用完成推理全流程', C=C, typo=t, spacing=sp)
code_block(s, 0.65, 1.9, 7.5, 4.6, ['from ai import Engine', '', 'e = Engine()'], language='python', C=C, typo=t)
multiline(s, 8.35, 2.5, 4.3, 3.6, ['多模型路由', '内置 RAG', '安全护栏'], font_size=14, C=C, line_spacing=1.6)

# P7: feature cards
s = add_slide(prs)
page_header(s, '三大产品能力', '覆盖关键场景', C=C, typo=t, spacing=sp)
highlight_cards(s, 0.65, 2.2, [
    ('智能报告', '财报自动生成, 节省 12 小时/份', C['primary']),
    ('智能客服', '一次解决率 92%', C['accent']),
], total_width=12.0, C=C, typo=t, spacing=sp)

# P9: comparison bars (v strings + pct floats!)
s = add_slide(prs)
page_header(s, '客户价值对比', '改造前后关键指标', C=C, typo=t, spacing=sp)
comparison_bars(s, 2.0, 2.2, [
    ('处理效率', '25%', '92%', 0.25, 0.92),   # v=str, pct=float
    ('人工成本', '80%', '48%', 0.80, 0.48),
], max_width=5.0, C=C, typo=t, spacing=sp)

# P10: CTA
s = add_slide(prs)
cta_slide(s, '开启企业智能之旅', '预约演示, 获取落地方案', C=C, typo=t)

clean_save(prs, 'output/deck.pptx')
```

## Key Constraints

- **⛔ NEVER use raw python-pptx in build.py**: `slide.shapes.add_shape()`, `slide.shapes.add_textbox()`, `slide.shapes.add_picture()` are FORBIDDEN. Use `rect()`, `text()`, `cover_image()` instead. Raw python-pptx produces flat, low-quality output with no CJK font support, no color resolution, no cover-fit. This is the #1 AI Tell in PPT design.
- **python-pptx 1.0.2**: No `PP_TRANSITION_TYPE`, must use XML for transitions/animations
- **Cover-fit images**: Use `_add_picture_cover()` with Pillow pre-crop — never stretch
- **Cache-first**: All image engines check cache before API call
- **Image generation**: ALWAYS use `python -m ppt_pro_max image "keywords"` CLI, `fetch_image()` Python API, or `ai_image()` in build.py. NEVER write custom scripts to call image APIs — the built-in CLI already handles cache, retry, multi-engine fallback, and cover-fit cropping. In build.py, `ai_image()` is the one-call generate+place helper (exposed by `from ppt_pro_max.build_helpers import *`).
- **Two-pass rebuild**: Page revision uses rebuild (not in-place) to avoid ZIP corruption
- **Windows**: Use `python` not `python3`
- **OOXML alpha**: `a:alpha val` = percentage × 1000 (e.g., 80% = 80000, NOT 0.8)
- **OOXML letter-spacing**: `a:spc val` = tracking_em × font_size_pt × 100 (font-size-dependent, NOT percentage)
- **apply_shadow() signature**: `apply_shadow(shape, blur_pt, distance_pt, direction_deg=90, color="#000000", alpha_pct=25)` — note `direction_deg` comes before `color`
- **add_text() signature**: `add_text(slide, text, x, y, w, h, font=None, size=20, color_role="foreground", bold=False, align="left")` — CJK companion font auto-set via `a:ea`/`a:cs`
- **add_rounded_rect() signature**: `add_rounded_rect(slide, x, y, w, h, fill_role=None, fill_hex=None, border_role=None, border_hex=None, gradient=False, shadow=False, corner_radius="md")` — `corner_radius` accepts `"sm"|"md"|"lg"|"pill"` or int pt value
- **BrandSpec**: has `spacing` dict (for `strip_style`, `section_dividers`), no `extra` field
- **GradientFill**: use `GradientFill` + `GradientStop` for alpha gradients; `apply_gradient(shape, color1, color2)` does NOT support alpha
- **layout_variant**: NOT a content.json field — use `--layout-variant` CLI param or `layout_variant=` kwarg in generate_ppt()
- **animation**: NOT a content.json field — use `--motion` CLI param or `motion=` kwarg in generate_ppt()
- **Chart selection**: `native_chart()` for standard data charts (bar/line/pie/area/scatter — editable, accurate axes); `bar_chart()`/`comparison_bars()`/`donut_chart(native=False)` for custom visuals (rounded bars, progress bars, gauge, waffle, icon bars). `donut_chart()` defaults to native=True for multi-sector accuracy. Choose based on data accuracy vs visual customization needs.
- **⚠️ Pie/doughnut chart colors**: In python-pptx, pie/doughnut colors MUST be set at the **point level** (`series.points[i].format.fill`), NOT at the series level (`series.format.fill`). Setting colors at series level makes all sectors the same color. `native_chart()` and `donut_chart(native=True)` handle this automatically — but if writing raw python-pptx code, you MUST iterate `series.points` and set each point's fill individually.
- **⚠️ comparison_bars() data format**: `[(label, v_old, v_new, pct_old, pct_new)]` — `v_old`/`v_new` are **strings** (bar-end labels like `'25%'`), `pct_old`/`pct_new` are **0-1 floats** (bar width). Mixing them (e.g. `0.25` for v_old, or `'25%'` for pct_old) crashes with `TypeError: can't multiply sequence by non-int`.
- **⚠️ BuildQA bounds vs decorative bleed**: Keep decorative shapes fully inside the canvas. `element_out_of_bounds` flags decorative shapes as **review** only if low-alpha (≤20%) + no text; opaque decorations (e.g. gold `donut()` rings) extending past the edge are flagged **fatal**. When adding accents, verify coordinates stay within `0 ≤ x < 13.333` and `0 ≤ y < 7.5`.
- **⚠️ CJK micro font size**: `cjk_*` TYPOGRAPHY presets use `micro=11` (not 10) to stay above BuildQA's 11pt warning threshold. Data labels in `comparison_bars()`/`bar_chart()` use `t.micro` — fine for CJK presets.
- **⚠️ Cover-fit images**: Always use `cover_image()` to add images — it Pillow-pre-crops to exact aspect ratio. NEVER use `slide.shapes.add_picture()` with stretch — it distorts images. `cover_image()` is the correct replacement for the internal `_add_picture_cover()` method.

## CLI Quick Reference

```
python -m ppt_pro_max "query" [--style STYLE] [--layout-variant VARIANT] [--motion 1-10] [--density 1-10] [--variance 1-10] [--content FILE] [--fetch-images] [-o PATH]
python -m ppt_pro_max image "keywords" [--llm-provider PROV] [--llm-api-key KEY] [--image-mode MODE] [-v]
```

## Dependencies

- python-pptx >= 1.0.2 (required)
- Pillow >= 10.0 (required)
- python-dotenv >= 1.0 (optional, for .env support)
- **Design database** (bundled) — provides design intelligence (colors, typography, styles, anti-patterns) from 7 bundled CSV datasets. No external installation required.
