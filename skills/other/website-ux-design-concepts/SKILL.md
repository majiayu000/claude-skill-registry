---
name: website-ux-design-concepts
description: This skill should be used when the user asks to "create design mockups", "generate UI concepts", "visualize UX improvements", "create wireframes", "design concept images", or needs to generate visual design mockups based on UX recommendations. Supports two engines: Stitch MCP (default, produces HTML/CSS + screenshots) and Gemini 3 Pro Image API (creative exploration fallback).
version: 1.0.0
title: "Website Ux Design Concepts"
status: active
---

# Website UX Design Concepts

Generate visual design mockups, HTML/CSS code, and UI concepts based on UX audit recommendations or design briefs. Supports two engines: Stitch MCP (default, produces HTML/CSS + screenshots) and Gemini 3 Pro Image API (creative exploration fallback).

## Overview

This skill transforms text-based UX recommendations into visual design concepts, creating mockup images and optionally HTML/CSS code that can be used as input for the design-to-code workflow. The default Stitch MCP engine produces actual HTML/CSS alongside screenshots, eliminating lossy visual re-interpretation during the design-to-code phase. The Gemini engine is retained as a fallback for creative exploration.

**Primary use case:** Bridge between UX audit findings and code implementation by generating visual representations of improvements.

## Parameters

| Parameter | Values | Default | Purpose |
|-----------|--------|---------|---------|
| `--engine` | `stitch` \| `gemini` | `stitch` | Design generation engine |
| `--resolution` | `1K` \| `2K` \| `4K` | `1K` | Image resolution (Gemini only) |

## Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Design brief | UX audit Tier 1 recommendations OR user description | What to visualize |
| Existing screenshots (optional) | Captured during UX audit | Reference for editing/improvement |
| Resolution | User preference (default: 1K) | Output quality level (Gemini only) |

## Stitch Workflow (Default)

The Stitch MCP engine produces actual HTML/CSS code alongside screenshots, providing pixel-perfect design fidelity for the design-to-code phase.

### Step 1: Load Stitch Tools

```python
# Make Stitch MCP tools available in the session
ToolSearch("stitch")
# This loads: mcp__stitch__create_project, mcp__stitch__generate_screen_from_text,
# mcp__stitch__fetch_screen_code, mcp__stitch__fetch_screen_image,
# mcp__stitch__edit_screens, mcp__stitch__list_projects, etc.
```

### Step 2: Create Project

```python
# Create a Stitch project scoped to the site
mcp__stitch__create_project(name="{site-name}-ux-improvements")
# Returns: projectId — save this for all subsequent screen generation
```

### Step 3: Generate Screens Per Section

For each website section identified in the UX audit:

1. **Generate screen** from UX recommendations:
   ```python
   mcp__stitch__generate_screen_from_text(
       prompt="[design prompt derived from Tier 1 recommendations]",
       projectId="{projectId}",
       deviceType="DESKTOP"
   )
   # Returns: screenId
   ```

2. **Fetch HTML/CSS code** for the generated screen:
   ```python
   mcp__stitch__fetch_screen_code(screenId="{screenId}")
   # Save output as: {output_dir}/design-concepts/{section}-code.html
   ```

3. **Fetch screenshot** for visual review:
   ```python
   mcp__stitch__fetch_screen_image(screenId="{screenId}")
   # Save output as: {output_dir}/design-concepts/{section}-mockup.png
   ```

### Step 4: Save Project Manifest

After generating all screens, save a manifest for downstream consumption:

```json
// {output_dir}/design-concepts/stitch-project.json
{
  "projectId": "proj_abc123",
  "engine": "stitch",
  "screens": {
    "homepage": { "screenId": "scr_001", "codeFile": "homepage-code.html", "imageFile": "homepage-mockup.png" },
    "navigation": { "screenId": "scr_002", "codeFile": "navigation-code.html", "imageFile": "navigation-mockup.png" }
  }
}
```

### Iteration

Use `mcp__stitch__edit_screens` to refine designs based on feedback without regenerating from scratch:

```python
mcp__stitch__edit_screens(
    screenId="{screenId}",
    prompt="Make the CTA button more prominent and increase header contrast"
)
# Then re-fetch code and image to update artifacts
```

### Parallel Stitch Generation (Recommended)

When working with multiple website sections, **launch parallel sub-agents** for each section:

```python
sections = ["homepage", "advertise", "knowledge-center", "publications"]

for section in sections:
    Task(
        subagent_type="general-purpose",
        prompt=f"""Generate Stitch design for {section} page.

First: Load Stitch tools via ToolSearch("stitch")
Then:
1. Read UX audit: {output_dir}/ux-audit/{section}.md
2. Extract Tier 1 recommendations and create design prompt
3. Generate screen: mcp__stitch__generate_screen_from_text
   - prompt: [design prompt from recommendations]
   - projectId: [from stitch-project.json]
   - deviceType: "DESKTOP"
4. Fetch code: mcp__stitch__fetch_screen_code → save to {output_dir}/design-concepts/{section}-code.html
5. Fetch image: mcp__stitch__fetch_screen_image → save to {output_dir}/design-concepts/{section}-mockup.png
6. Update stitch-project.json with screen mapping""",
        run_in_background=True
    )
```

**Why parallel?**
- Process 5+ sections simultaneously
- Each sub-agent loads Stitch tools independently via ToolSearch
- HTML/CSS output eliminates visual re-interpretation in design-to-code phase
- Much faster than sequential generation

---

## Gemini Workflow (`--engine=gemini`)

### Usage

Run the script using absolute path (do NOT cd to skill directory first):

**Generate new design concept:**
```bash
uv run ~/.claude/skills/website-ux-design-concepts/scripts/generate_image.py \
  --prompt "UI mockup: [design description]" \
  --filename "yyyy-mm-dd-hh-mm-ss-concept-name.png" \
  --resolution 1K|2K|4K
```

**Edit existing screenshot to show improvements:**
```bash
uv run ~/.claude/skills/website-ux-design-concepts/scripts/generate_image.py \
  --prompt "Improve this UI: [specific improvements]" \
  --filename "yyyy-mm-dd-hh-mm-ss-improved-name.png" \
  --input-image "path/to/original-screenshot.png" \
  --resolution 2K
```

**Important:** Always run from user's current working directory so images are saved where the user is working.

### Workflow Integration

#### From UX Audit → Design Concepts

Transform Tier 1 recommendations into design prompts:

```
UX Audit Recommendation:
"Simplify navigation by consolidating 12 top-level items into 5 categories"

Design Prompt:
"UI mockup: Modern website header with 5-item horizontal navigation bar.
Clean typography, clear hover states, mobile hamburger menu icon visible.
Color scheme: professional blue and white. Style: minimal, modern SaaS."
```

#### Parallel Mockup Generation (Recommended)

When working with multiple website sections, **launch parallel sub-agents** for each section:

```python
# Example: Generate mockups for all sections in parallel
sections = ["homepage", "advertise", "knowledge-center", "publications"]

for section in sections:
    Task(
        subagent_type="general-purpose",
        prompt=f"""Generate 1K mockup for {section} page.
Read UX audit: {output_dir}/ux-audit/{section}.md
Extract Tier 1 recommendations and create design prompt.
Generate mockup to: {output_dir}/design-concepts/{section}-mockup.png""",
        run_in_background=True
    )
```

**Why parallel?**
- Process 5+ sections simultaneously
- 1K resolution is sufficient for specs
- Much faster than sequential generation

#### Single Section Workflow

For individual sections or iterations:

```bash
uv run ~/.claude/skills/website-ux-design-concepts/scripts/generate_image.py \
  --prompt "<design prompt from Tier 1 recommendations>" \
  --filename "{output_dir}/design-concepts/{section}-mockup.png" \
  --resolution 1K
```

**Note:** 4K resolution is not needed for specification generation. 1K mockups provide sufficient detail for creating briefs and JSONC specs.

## Prompt Engineering for UI Mockups

### Generation Template (New Designs)

```
UI mockup: [component/page type].
Layout: [structure description].
Components: [list key UI elements].
Style: [design aesthetic - modern/minimal/corporate/playful].
Color palette: [primary, secondary, accent colors].
Typography: [font style - clean/bold/elegant].
Special elements: [icons, images, animations].
Avoid: [unwanted elements].
```

### Editing Template (Improve Existing)

```
Improve this UI design:
Change ONLY: [specific improvement].
Keep identical: overall layout, brand colors, existing content.
Add: [new elements if any].
Remove: [elements to simplify].
Style adjustments: [subtle changes].
```

### Example Prompts by UX Issue

**Navigation Improvement:**
```
UI mockup: Website header with simplified navigation.
Layout: Logo left, 5 main nav items center, CTA button right.
Components: Logo placeholder, text links, dropdown indicator, search icon, primary button.
Style: Modern SaaS, clean lines, plenty of whitespace.
Color palette: #1E3A8A primary blue, white background, #3B82F6 hover state.
Typography: Sans-serif, medium weight for nav items.
```

**Hero Section Redesign:**
```
UI mockup: Hero section with strong value proposition.
Layout: Split layout - headline and CTA left, product image right.
Components: H1 headline, subheadline paragraph, two CTA buttons, hero image placeholder.
Style: Bold, confident, enterprise software aesthetic.
Color palette: Dark blue background, white text, orange accent CTAs.
Special elements: Subtle gradient background, floating UI element decorations.
```

**Card Grid Layout:**
```
UI mockup: Feature cards grid section.
Layout: 3-column grid with equal cards, responsive hints.
Components: Icon, heading, description, link for each card.
Style: Minimal, flat design, generous padding.
Color palette: Light gray background, white cards, blue icons.
Typography: Bold headings, regular body text.
```

## Resolution Guide (Gemini Only)

| Resolution | Use Case | When to Use |
|------------|----------|-------------|
| **1K** (default) | Spec generation | Sufficient for briefs and JSONC specs |
| **2K** | Client review | Higher detail for presentations |
| **4K** | Final assets | Only if high-res deliverables needed |

**Recommendation:** Use 1K for all `/website-upgraded` pipeline mockups. Higher resolutions add generation time without improving spec quality.

## API Configuration (`--engine=gemini` Only)

The Gemini engine script checks for API key in this order:
1. `--api-key` argument (highest priority)
2. `.env` file in current working directory
3. `GEMINI_API_KEY` environment variable

**Recommended: Use .env file**
```bash
# Create .env file in your project root
echo 'GEMINI_API_KEY=your-api-key-here' >> .env
```

The script auto-loads `.env` from the directory where you run the command.

**Alternative: Environment variable**
```bash
export GEMINI_API_KEY="your-api-key"
```

**Note:** The Stitch engine (default) does not require any API key -- it uses the Stitch MCP server configured in `.mcp.json`.

## Output Structure

### Stitch Engine (Default)
```
design-concepts/
├── stitch-project.json       # Project ID + screen ID mappings
├── homepage-mockup.png       # Screenshot (fetch_screen_image)
├── homepage-code.html        # HTML/CSS (fetch_screen_code)
├── navigation-mockup.png
├── navigation-code.html
└── ...
```

### Gemini Engine
```
design-concepts/
├── homepage-mockup.png
├── navigation-mockup.png
└── ...
```

## Preflight Checks

Before running:
```bash
# For Stitch engine (default): Verify MCP server is configured
# No API key needed — Stitch uses .mcp.json configuration

# For Gemini engine (--engine=gemini):
# Check uv is available
command -v uv

# Check API key is set
test -n "$GEMINI_API_KEY"

# If editing, verify input image exists
test -f "path/to/input.png"
```

## Common Issues

| Error | Cause | Fix |
|-------|-------|-----|
| `No API key provided` | Missing GEMINI_API_KEY | Set env var or pass --api-key |
| `Error loading input image` | Wrong path | Verify --input-image path |
| `quota/403 errors` | API limits | Check quota or use different key |

## Integration with Workflow Chain

This skill is designed to work in a 3-stage pipeline:

```
┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│  website-ux-audit   │───▶│ website-ux-design-  │───▶│   design-to-code    │
│                     │    │      concepts       │    │                     │
│  URL → UX Report    │    │ Recommendations →   │    │ Mockups (PNG) +     │
│  + Recommendations  │    │ Visual Mockups +     │    │ Code (HTML/CSS) →   │
│                     │    │ Code (HTML/CSS)      │    │ React Components    │
└─────────────────────┘    └─────────────────────┘    └─────────────────────┘
```

Use `/website-upgraded` command to execute the full pipeline automatically.
