---
name: sc-create-slide-template
description: "Extract visual styling from screenshots to create reusable ScriptCast slide templates, with validation for bundled templates."
license: MIT
compatibility: [opencode, claude, cursor]

metadata:
  category: utility
  related: [agent-ops-interview, agent-ops-planning]

---

# ScriptCast Template Creation Workflow

## Purpose

Enable users to create slide templates by:
1. Uploading screenshots/mockups of desired visual style
2. Extracting colors, fonts, spacing, and layout from images
3. Generating a complete template covering all ScriptCast features
4. Storing templates for reuse via CLI `--template <name>` option
5. Validating all bundled templates work correctly

## Template Scope

A complete ScriptCast template must define styling for ALL visual elements:

### Slide Styling (`SlideStyle`)
| Property | Description | Extracted From |
|----------|-------------|----------------|
| `background_color` | Default slide background | Dominant background color |
| `gradient_start`/`gradient_end` | Optional gradient | Gradient detection |
| `title_color`, `title_size` | Title typography | Header text analysis |
| `text_color`, `text_size` | Body text styling | Body text analysis |
| `bullet_color`, `bullet_size`, `bullet_char` | Bullet point styling | List detection |
| `margin`, `line_spacing` | Layout spacing | Edge/padding analysis |
| `vertical_align`, `title_align`, `text_align` | Alignment | Content positioning |

### Carbon Code Block Styling (`CarbonConfig`)
| Property | Description | Default |
|----------|-------------|---------|
| `gradient` | Background gradient preset | From GRADIENTS dict |
| `theme` | Pygments syntax theme | monokai, dracula, etc. |
| `window_bg` | Editor window background | Dark color from palette |
| `show_titlebar` | macOS-style titlebar | true |
| `corner_radius` | Window corner rounding | 16 |

### Transition Defaults (`TransitionConfig`)
| Property | Description | Default |
|----------|-------------|---------|
| `type` | Default transition type | fade, crossfade, etc. |
| `duration` | Transition duration | 0.5s |
| `color` | Fade color | black |

### Video Settings
| Property | Description | Options |
|----------|-------------|---------|
| `resolution` | Default resolution | 4K (3840x2160), 1080p (1920x1080) |
| `frame_rate` | Video frame rate | 30, 60 |

## Template Storage

### Location
```
src/scriptcast/assets/templates/
├── __init__.py          # Template registry
├── default.yaml         # Default template (Catppuccin-based)
├── minimal.yaml         # Clean minimal style
├── corporate.yaml       # Professional/business style
├── neon.yaml            # Vibrant colors
└── ...
```

### Template File Format (YAML)
```yaml
# Template: {name}
# Description: {description}
# Author: {author}
# Created: {date}

metadata:
  name: "{template_name}"
  description: "{description}"
  version: "1.0.0"

slide_style:
  background_color: "#1e1e2e"
  gradient_start: null
  gradient_end: null
  
  title_color: "#cdd6f4"
  title_size: 72
  title_align: center
  
  text_color: "#bac2de"
  text_size: 56
  text_align: left
  
  bullet_color: "#bac2de"
  bullet_size: 52
  bullet_char: "•"
  bullet_indent: 60
  
  margin: 100
  title_margin_bottom: 60
  line_spacing: 1.4
  bullet_spacing: 20
  vertical_align: middle

carbon_style:
  gradient: "carbon"
  theme: "monokai"
  window_bg: [30, 30, 40]
  show_titlebar: true
  corner_radius: 16
  shadow_blur: 30
  font_ratio: null  # auto-scale

transition:
  type: "fade"
  duration: 0.5
  color: "black"

video:
  resolution: "4K"
  frame_rate: 30
```

## Procedure: Screenshot-to-Template

### Phase 1: Image Analysis

When user provides screenshot:

1. **Color Extraction**
   - Identify dominant colors (background, text, accent)
   - Detect gradients (linear, radial, diagonal)
   - Extract color palette (5-8 colors)

2. **Layout Analysis**
   - Measure margins and padding
   - Identify text alignment patterns
   - Detect content vertical positioning

3. **Typography Detection**
   - Estimate font sizes from visual proportions
   - Identify weight (bold headers, regular body)
   - Note spacing (line height, paragraph gaps)

### Phase 2: Style Mapping

Map extracted values to ScriptCast components:

```
Screenshot Element → ScriptCast Property
─────────────────────────────────────────
Header text color → title_color
Body text color   → text_color
Background        → background_color OR gradient_*
Bullet/list style → bullet_char, bullet_color
Edge padding      → margin
Line gaps         → line_spacing
```

### Phase 3: Template Generation

1. **Validate completeness**: Ensure all required properties have values
2. **Apply sensible defaults**: Fill gaps with complementary values
3. **Generate YAML**: Create template file content
4. **Preview confirmation**: Show user the interpreted style

### Phase 4: Template Installation

1. Save to `src/scriptcast/assets/templates/{name}.yaml`
2. Update template registry in `__init__.py`
3. Generate validation test in `tests/test_templates.py`

## Procedure: Template Validation

### For Bundled Templates

Every template shipped with ScriptCast MUST pass validation:

```python
# tests/test_templates.py

@pytest.mark.parametrize("template_name", list_bundled_templates())
def test_template_valid(template_name: str) -> None:
    """Ensure template loads and has all required fields."""
    template = load_template(template_name)
    assert template.metadata.name
    assert template.slide_style.background_color
    # ... validate all required fields

@pytest.mark.parametrize("template_name", list_bundled_templates())
def test_template_renders_slide(template_name: str, tmp_path: Path) -> None:
    """Ensure template can render all slide types."""
    template = load_template(template_name)
    style = template.to_slide_style()
    
    for slide_type in SlideType:
        content = create_test_content(slide_type)
        img = render_slide(content, style)
        assert img.size == (1920, 1080)

@pytest.mark.parametrize("template_name", list_bundled_templates())  
def test_template_renders_carbon(template_name: str) -> None:
    """Ensure template can render Carbon code blocks."""
    template = load_template(template_name)
    config = template.to_carbon_config()
    
    img = render_carbon_code_block("print('hello')", config=config)
    assert img is not None
```

### Validation Checklist

- [ ] YAML syntax valid
- [ ] All required fields present
- [ ] Color values are valid hex (#RRGGBB)
- [ ] Numeric values in valid ranges
- [ ] Renders title slide without error
- [ ] Renders bullet slide without error
- [ ] Renders code slide without error
- [ ] Renders split-screen without error
- [ ] Transitions work with template colors

## CLI Integration

### Using Templates

```bash
# Use named template
scriptcast manuscript render script.yaml --template corporate

# Use template file path
scriptcast manuscript render script.yaml --template ./my-template.yaml

# List available templates
scriptcast templates list

# Preview template
scriptcast templates preview corporate
```

### Implementation Requirements

1. **Add `--template` option** to:
   - `manuscript render`
   - `slides render`

2. **Template resolution order**:
   - Absolute/relative path → load directly
   - Name → search `src/scriptcast/assets/templates/`
   - Not found → error with suggestions

3. **Template loading function**:
```python
def load_template(name_or_path: str) -> Template:
    """Load template by name or path."""
    ...
```

## Interview Questions (for custom template)

If user wants to create template WITHOUT a screenshot:

| # | Question | Purpose |
|---|----------|---------|
| 1 | "What visual style are you going for? (dark/light/vibrant/minimal/custom)" | Base palette |
| 2 | "Primary brand color (hex) or 'none'?" | Accent color |
| 3 | "Code block style preference? (carbon/plain)" | CarbonConfig |
| 4 | "Default transition between slides? (fade/crossfade/wipe/none)" | TransitionConfig |
| 5 | "Target resolution? (4K/1080p)" | Video settings |

## Completion Criteria

Template creation is complete when:

- [ ] Template YAML file created in `assets/templates/`
- [ ] All ScriptCast visual elements have defined styles
- [ ] Template registered in `__init__.py`
- [ ] Validation test added to `test_templates.py`
- [ ] Test passes: `uv run pytest tests/test_templates.py -k {template_name}`
- [ ] User confirms preview looks correct

## Anti-patterns (avoid)

- ❌ Creating template with missing required fields
- ❌ Guessing colors without showing user for confirmation
- ❌ Skipping validation tests for new templates
- ❌ Hardcoding pixel values that don't scale with resolution
- ❌ Creating template that only works for one slide type
- ❌ Ignoring accessibility (low contrast text)

## Example: Screenshot Analysis

**User uploads**: Dark theme slide screenshot

**Agent analysis**:
```
Color Extraction:
  - Background: #0d1117 (GitHub dark)
  - Text primary: #c9d1d9
  - Text secondary: #8b949e
  - Accent: #58a6ff (blue links)
  - Code background: #161b22

Layout Analysis:
  - Margins: ~80px (4% of 1920)
  - Title size: ~64px
  - Body size: ~32px
  - Line spacing: ~1.5

Recommendations:
  - gradient: none (solid dark)
  - theme: github-dark (Pygments)
  - transition: fade (subtle for dark theme)
```

**Generated template preview** → User confirms → Save as `github-dark.yaml`
