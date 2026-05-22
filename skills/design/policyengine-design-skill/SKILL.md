---
name: policyengine-design
description: PolicyEngine visual identity - colors, fonts, logos, and branding for web apps, calculators, charts, and research
---

# PolicyEngine Design System

PolicyEngine's visual identity and branding guidelines for creating consistent user experiences across web apps, calculators, charts, and research outputs.

## For Users 👥

### PolicyEngine Visual Identity

**Brand colors:**
- **Teal** (#39C6C0) - Primary accent color (buttons, highlights, interactive elements)
- **Blue** (#2C6496) - Secondary color (links, charts, headers)

**Typography:**
- **Charts:** Roboto Serif
- **Web app:** System fonts (sans-serif)
- **Streamlit apps:** Default sans-serif

**Logo:**
- Used in charts (bottom right)
- Blue version for light backgrounds
- White version for dark backgrounds

### Recognizing PolicyEngine Content

**You can identify PolicyEngine content by:**
- Teal accent color (#39C6C0) on buttons and interactive elements
- Blue (#2C6496) in charts and links
- Roboto Serif font in charts
- PolicyEngine logo in chart footer
- Clean, minimal white backgrounds
- Data-focused, quantitative presentation

## For Analysts 📊

### Chart Branding

When creating charts for PolicyEngine analysis, follow these guidelines:

#### Color Palette

**Primary colors:**
```python
TEAL_ACCENT = "#39C6C0"   # Primary color (teal)
BLUE_PRIMARY = "#2C6496"  # Secondary color (blue)
DARK_GRAY = "#616161"     # Text color
```

**Extended palette:**
```python
# Blues
BLUE = "#2C6496"
BLUE_LIGHT = "#D8E6F3"
BLUE_PRESSED = "#17354F"
BLUE_98 = "#F7FAFD"
DARK_BLUE_HOVER = "#1d3e5e"
DARKEST_BLUE = "#0C1A27"

# Teals
TEAL_ACCENT = "#39C6C0"
TEAL_LIGHT = "#F7FDFC"
TEAL_PRESSED = "#227773"

# Grays
DARK_GRAY = "#616161"
GRAY = "#808080"
MEDIUM_LIGHT_GRAY = "#BDBDBD"
MEDIUM_DARK_GRAY = "#D2D2D2"
LIGHT_GRAY = "#F2F2F2"

# Accents
WHITE = "#FFFFFF"
BLACK = "#000000"
DARK_RED = "#b50d0d"  # For negative values
```

**See current colors:**
```bash
cat policyengine-app/src/style/colors.js
```

#### Plotly Chart Formatting

**Standard PolicyEngine chart:**

```python
import plotly.graph_objects as go

def format_fig(fig):
    """Format chart with PolicyEngine branding."""
    fig.update_layout(
        # Typography
        font=dict(
            family="Roboto Serif",
            color="black"
        ),

        # Background
        plot_bgcolor="white",
        template="plotly_white",

        # Margins (leave room for logo)
        margin=dict(
            l=50,
            r=100,
            t=50,
            b=120,
            pad=4
        ),

        # Chart size
        height=600,
        width=800,
    )

    # Add PolicyEngine logo (bottom right)
    fig.add_layout_image(
        dict(
            source="https://raw.githubusercontent.com/PolicyEngine/policyengine-app-v2/main/app/public/assets/logos/policyengine/teal.png",
            xref="paper",
            yref="paper",
            x=1.0,
            y=-0.10,
            sizex=0.10,
            sizey=0.10,
            xanchor="right",
            yanchor="bottom"
        )
    )

    # Clean modebar
    fig.update_layout(
        modebar=dict(
            bgcolor="rgba(0,0,0,0)",
            color="rgba(0,0,0,0)"
        )
    )

    return fig

# Usage
fig = go.Figure()
fig.add_trace(go.Scatter(x=x_data, y=y_data, line=dict(color=TEAL_ACCENT)))
fig = format_fig(fig)
```

**Current implementation:**
```bash
# See format_fig in action
cat givecalc/ui/visualization.py
cat policyengine-app/src/pages/policy/output/...
```

#### Blog Post Charts (Standalone HTML)

When creating standalone Plotly HTML files for blog posts, use these specific settings:

**Font:** Use "Roboto" (not "Roboto Serif") with Google Fonts embed:
```python
FONT_FAMILY = "Roboto, Arial, sans-serif"

# After generating HTML, embed font
html = fig.to_html(include_plotlyjs='cdn')
html_with_font = html.replace('</head>',
    '<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet"></head>')
with open('chart.html', 'w') as f:
    f.write(html_with_font)
```

**Background:** LIGHT_GRAY (#F2F2F2) for better blog integration:
```python
fig.update_layout(
    plot_bgcolor="#F2F2F2",
    paper_bgcolor="#F2F2F2"
)
```

**Logo positioning:** x=0.95, y=-0.2 avoids cutoff:
```python
images=[{
    "source": "https://raw.githubusercontent.com/PolicyEngine/policyengine-app-v2/main/app/public/assets/logos/policyengine/teal.png",
    "xref": "paper", "yref": "paper",
    "x": 0.95,  # Not 1.0 - prevents cutoff
    "y": -0.2,
    "sizex": 0.15, "sizey": 0.15,
    "xanchor": "right", "yanchor": "bottom"
}]
```

**Margins:** Increase right margin when x-axis extends to boundary:
```python
# For charts showing $0-$2B or similar
margin=dict(t=120, b=120, l=120, r=80)  # r=80 ensures last tick visible
```

**Grid and axes:**
```python
xaxis=dict(
    gridcolor="#FFFFFF",      # White grid on LIGHT_GRAY background
    zerolinecolor="#FFFFFF",
    tickformat='$,.1f',       # Units in tick labels
    ticksuffix='B'            # Not in axis title
),
yaxis=dict(
    gridcolor="#FFFFFF",
    zerolinecolor="#FFFFFF",
    ticksuffix='%'
)
```

**Colors for reference lines:** Use GRAY (#808080), not red:
```python
# Reference/statutory lines
line=dict(color="#808080", width=2, dash='dash')
```

**Stepwise patterns:** Use 10,000+ points for discrete boundaries:
```python
# For charts showing $2M increments
wealth = np.linspace(0, 2.0, 10000)  # Fine granularity
line=dict(shape='hv')  # Horizontal-vertical steps
```

**Legend:** Position inside chart when needed:
```python
legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
# Or remove entirely if obvious: showlegend=False
```

#### Chart Colors

**For line charts:**
- Primary line: Teal (#39C6C0) or Blue (#2C6496)
- Background lines: Light gray (rgb(180, 180, 180))
- Markers: Teal with 70% opacity

**For bar charts:**
- Positive values: Teal (#39C6C0)
- Negative values: Dark red (#b50d0d)
- Neutral: Gray

**For multiple series:**
Use variations of blue and teal, or discrete color scale:
```python
colors = ["#2C6496", "#39C6C0", "#17354F", "#227773"]
```

#### Typography

**Charts:**
```python
font=dict(family="Roboto Serif", size=14, color="black")
```

**Axis labels:**
```python
xaxis=dict(
    title=dict(text="Label", font=dict(size=14)),
    tickfont=dict(size=12)
)
```

**Load Roboto font:**
```python
# In Streamlit apps
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)
```

### Streamlit App Branding

**Streamlit configuration (.streamlit/config.toml):**

```toml
[theme]
base = "light"
primaryColor = "#39C6C0"          # Teal accent
backgroundColor = "#FFFFFF"        # White background
secondaryBackgroundColor = "#F7FDFC"  # Teal light
textColor = "#616161"              # Dark gray

[client]
toolbarMode = "minimal"
```

**Current implementation:**
```bash
cat givecalc/.streamlit/config.toml
cat salt-amt-calculator/.streamlit/config.toml  # Other calculators
```

### Logo Usage

**Logo URLs (app-v2 - current):**

```python
# Teal logo (for light backgrounds) - PREFERRED
LOGO_TEAL = "https://raw.githubusercontent.com/PolicyEngine/policyengine-app-v2/main/app/public/assets/logos/policyengine/teal.png"
LOGO_TEAL_SQUARE = "https://raw.githubusercontent.com/PolicyEngine/policyengine-app-v2/main/app/public/assets/logos/policyengine/teal-square.png"

# White logo (for dark backgrounds)
LOGO_WHITE = "https://raw.githubusercontent.com/PolicyEngine/policyengine-app-v2/main/app/public/assets/logos/policyengine/white.png"

# SVG versions (scalable)
LOGO_TEAL_SVG = "https://raw.githubusercontent.com/PolicyEngine/policyengine-app-v2/main/app/public/assets/logos/policyengine/teal.svg"
LOGO_WHITE_SVG = "https://raw.githubusercontent.com/PolicyEngine/policyengine-app-v2/main/app/public/assets/logos/policyengine/white.svg"
```

**Logo placement in charts:**
- Bottom right corner
- 10% of chart width
- Slightly below bottom edge (y=-0.10)

**Current logos:**
```bash
ls policyengine-app-v2/app/public/assets/logos/policyengine/
# teal.png, teal.svg (wide)
# teal-square.png, teal-square.svg (square)
# white.png, white.svg (wide)
# white-square.svg (square)
```

### Complete Example: Branded Chart

```python
import plotly.graph_objects as go

# PolicyEngine colors
TEAL_ACCENT = "#39C6C0"
BLUE_PRIMARY = "#2C6496"

# Create chart
fig = go.Figure()

# Add data
fig.add_trace(go.Scatter(
    x=incomes,
    y=taxes,
    mode='lines',
    name='Tax liability',
    line=dict(color=TEAL_ACCENT, width=3)
))

# Apply PolicyEngine branding
fig.update_layout(
    # Typography
    font=dict(family="Roboto Serif", size=14, color="black"),

    # Title and labels
    title="Tax liability by income",
    xaxis_title="Income",
    yaxis_title="Tax ($)",

    # Formatting
    xaxis_tickformat="$,.0f",
    yaxis_tickformat="$,.0f",

    # Appearance
    plot_bgcolor="white",
    template="plotly_white",

    # Size and margins
    height=600,
    width=800,
    margin=dict(l=50, r=100, t=50, b=120, pad=4)
)

# Add logo
fig.add_layout_image(
    dict(
        source="https://raw.githubusercontent.com/PolicyEngine/policyengine-app-v2/main/app/public/assets/logos/policyengine/teal.png",
        xref="paper",
        yref="paper",
        x=1.0,
        y=-0.10,
        sizex=0.10,
        sizey=0.10,
        xanchor="right",
        yanchor="bottom"
    )
)

# Show
fig.show()
```

## For Contributors 💻

### Brand Assets

**Repository:** PolicyEngine/policyengine-app-v2 (current), PolicyEngine/policyengine-app (legacy)

**Logo files:**
```bash
# Logos in app (both v1 and v2 use same logos)
ls policyengine-app/src/images/logos/policyengine/
# - blue.png - For light backgrounds
# - white.png - For dark backgrounds
# - blue.svg - Scalable blue logo
# - white.svg - Scalable white logo
# - banners/ - Banner variations
# - profile/ - Profile/avatar versions
```

**Access logos:**
```bash
# View logo files (v1 repo has the assets)
cd policyengine-app/src/images/logos/policyengine/
ls -la
```

### Color Definitions

**⚠️ IMPORTANT: Design System Package**

PolicyEngine has a centralized design system package: `@policyengine/design-system` (available on npm). This package provides design tokens (colors, spacing, typography) for consistent styling across all PolicyEngine projects.

**For new projects (API v2, documentation sites, etc.):**
- Install: `npm install @policyengine/design-system`
- Import tokens from the package instead of hardcoding colors
- See the package README for usage patterns

**For legacy projects:**
- Use app-v2 colors for new projects not yet using the design system package
- Gradually migrate to use `@policyengine/design-system` when possible

### Using @policyengine/design-system Package

**Installation:**
```bash
npm install @policyengine/design-system
```

**Usage in documentation sites (Docusaurus, etc.):**
```javascript
// Import design tokens
import { tokens } from '@policyengine/design-system';

// Use in custom CSS
:root {
  --primary-color: var(--pe-color-primary-500);
  --secondary-color: var(--pe-color-blue-700);
}

// Or import CSS directly
import '@policyengine/design-system/dist/tokens.css';
```

**Current implementation:**
```bash
# See how API v2 uses design tokens
cat policyengine-api-v2/docs/docusaurus.config.js
cat policyengine-api-v2/docs/src/css/custom.css
```

**Package repository:**
```bash
# For reference implementation and available tokens
# See: https://www.npmjs.com/package/@policyengine/design-system
# Source: PolicyEngine/design-system (GitHub)
```

**Current colors (policyengine-app-v2):**

```typescript
// policyengine-app-v2/app/src/designTokens/colors.ts

// Primary (teal) - 50 to 900 scale
primary[500]: "#319795"  // Main teal
primary[400]: "#38B2AC"  // Lighter teal
primary[600]: "#2C7A7B"  // Darker teal

// Blue scale
blue[700]: "#026AA2"     // Primary blue
blue[500]: "#0EA5E9"     // Lighter blue

// Gray scale
gray[700]: "#344054"     // Dark text
gray[100]: "#F2F4F7"     // Light backgrounds

// Semantic
success: "#22C55E"
warning: "#FEC601"
error: "#EF4444"

// Background
background.primary: "#FFFFFF"
background.secondary: "#F5F9FF"

// Text
text.primary: "#000000"
text.secondary: "#5A5A5A"
```

**To see current design tokens:**
```bash
cat policyengine-app-v2/app/src/designTokens/colors.ts
cat policyengine-app-v2/app/src/styles/colors.ts  # Mantine integration
```

**Legacy colors (policyengine-app - still used in some projects):**

```javascript
// policyengine-app/src/style/colors.js
TEAL_ACCENT = "#39C6C0"  // Old teal (slightly different from v2)
BLUE = "#2C6496"         // Old blue
DARK_GRAY = "#616161"    // Old dark gray
```

**To see legacy colors:**
```bash
cat policyengine-app/src/style/colors.js
```

**Usage in React (app-v2):**
```typescript
import { colors } from 'designTokens';

<Button style={{ backgroundColor: colors.primary[500] }} />
<Text style={{ color: colors.text.primary }} />
```

**Usage in Python/Plotly (use legacy colors for now):**
```python
# For charts, continue using legacy colors until officially migrated
TEAL_ACCENT = "#39C6C0"  # From original app
BLUE_PRIMARY = "#2C6496"  # From original app

# Or use app-v2 colors
TEAL_PRIMARY = "#319795"  # From app-v2
BLUE_PRIMARY_V2 = "#026AA2"  # From app-v2
```

### Typography

**Fonts:**

**For charts (Plotly):**
```python
font=dict(family="Roboto Serif")
```

**For web apps:**
```javascript
// System font stack
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, ...
```

**Loading Google Fonts:**
```html
<!-- In Streamlit or HTML -->
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&family=Roboto+Serif:wght@300;400;500;700&display=swap" rel="stylesheet">
```

### Chart Formatting Function

**Reference implementation:**

```bash
# GiveCalc format_fig function
cat givecalc/ui/visualization.py

# Shows:
# - Roboto Serif font
# - White background
# - Logo placement
# - Margin configuration
```

**Pattern to follow:**
```python
def format_fig(fig: go.Figure) -> go.Figure:
    """Format figure with PolicyEngine branding.

    This function is used across PolicyEngine projects to ensure
    consistent chart appearance.
    """
    # Font
    fig.update_layout(
        font=dict(family="Roboto Serif", color="black")
    )

    # Background
    fig.update_layout(
        template="plotly_white",
        plot_bgcolor="white"
    )

    # Size
    fig.update_layout(height=600, width=800)

    # Margins (room for logo)
    fig.update_layout(
        margin=dict(l=50, r=100, t=50, b=120, pad=4)
    )

    # Logo
    fig.add_layout_image(
        dict(
            source="https://raw.githubusercontent.com/PolicyEngine/policyengine-app-v2/main/app/public/assets/logos/policyengine/teal.png",
            xref="paper",
            yref="paper",
            x=1.0,
            y=-0.10,
            sizex=0.10,
            sizey=0.10,
            xanchor="right",
            yanchor="bottom"
        )
    )

    # Clean modebar
    fig.update_layout(
        modebar=dict(
            bgcolor="rgba(0,0,0,0)",
            color="rgba(0,0,0,0)"
        )
    )

    return fig
```

### Streamlit Theme Configuration

**Standard .streamlit/config.toml:**

```toml
[theme]
base = "light"
primaryColor = "#39C6C0"              # Teal accent
backgroundColor = "#FFFFFF"            # White
secondaryBackgroundColor = "#F7FDFC"  # Teal light
textColor = "#616161"                  # Dark gray
font = "sans serif"

[client]
toolbarMode = "minimal"
showErrorDetails = true
```

**Usage:**
```bash
# Create .streamlit directory in your project
mkdir .streamlit

# Copy configuration
cat > .streamlit/config.toml << 'EOF'
[theme]
base = "light"
primaryColor = "#39C6C0"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F7FDFC"
textColor = "#616161"
font = "sans serif"
EOF
```

**Current examples:**
```bash
cat givecalc/.streamlit/config.toml
```

## Design Patterns by Project Type

### Streamlit Calculators (GiveCalc, SALT Calculator, etc.)

**Required branding:**
1. ✅ .streamlit/config.toml with PolicyEngine theme
2. ✅ Charts use format_fig() function with logo
3. ✅ Teal accent color for interactive elements
4. ✅ Roboto Serif for charts

**Example:**
```python
import streamlit as st
import plotly.graph_objects as go

# Constants
TEAL_ACCENT = "#39C6C0"

# Streamlit UI
st.title("Calculator Name")  # Uses theme colors automatically
st.button("Calculate", type="primary")  # Teal accent from theme

# Charts
fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y, line=dict(color=TEAL_ACCENT)))
fig = format_fig(fig)  # Add branding
st.plotly_chart(fig)
```

### Jupyter Notebooks / Analysis Scripts

**Required branding:**
1. ✅ Charts use format_fig() with logo
2. ✅ PolicyEngine color palette
3. ✅ Roboto Serif font

**Example:**
```python
import plotly.graph_objects as go

TEAL_ACCENT = "#39C6C0"
BLUE_PRIMARY = "#2C6496"

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=data.income,
    y=data.tax_change,
    line=dict(color=TEAL_ACCENT, width=3)
))

fig.update_layout(
    font=dict(family="Roboto Serif", size=14),
    title="Tax impact by income",
    xaxis_title="Income",
    yaxis_title="Tax change ($)",
    plot_bgcolor="white"
)

# Add logo
fig.add_layout_image(...)
```

### React App Components

**Color usage:**
```javascript
import colors from "style/colors";

// Interactive elements
<Button style={{ backgroundColor: colors.TEAL_ACCENT }}>
  Click me
</Button>

// Links
<a style={{ color: colors.BLUE }}>Learn more</a>

// Text
<p style={{ color: colors.DARK_GRAY }}>Description</p>
```

**Current colors:**
```bash
cat policyengine-app/src/style/colors.js
```

## Visual Guidelines

### Chart Design Principles

1. **Minimal decoration** - Let data speak
2. **White backgrounds** - Clean, print-friendly
3. **Clear axis labels** - Always include units
4. **Formatted numbers** - Currency ($), percentages (%), etc.
5. **Logo inclusion** - Bottom right, never intrusive
6. **Consistent sizing** - 800x600 standard
7. **Roboto Serif** - Professional, readable font

### Color Usage Rules

**Primary actions:**
- Use TEAL_ACCENT (#39C6C0)
- Buttons, highlights, current selection

**Chart lines:**
- Primary data: TEAL_ACCENT or BLUE_PRIMARY
- Secondary data: BLUE_LIGHT or GRAY
- Negative values: DARK_RED (#b50d0d)

**Backgrounds:**
- Main: WHITE (#FFFFFF)
- Secondary: TEAL_LIGHT (#F7FDFC) or BLUE_98 (#F7FAFD)
- Plot area: WHITE

**Text:**
- Primary: BLACK (#000000)
- Secondary: DARK_GRAY (#616161)
- Muted: GRAY (#808080)

### Accessibility

**Color contrast requirements:**
- Text on background: 4.5:1 minimum (WCAG AA)
- DARK_GRAY on WHITE: ✅ Passes
- TEAL_ACCENT on WHITE: ✅ Passes for large text
- Use sufficient line weights for visibility

**Don't rely on color alone:**
- Use patterns or labels for different data series
- Ensure charts work in grayscale

## Common Branding Tasks

### Task 1: Create Branded Plotly Chart

1. **Define colors:**
   ```python
   TEAL_ACCENT = "#39C6C0"
   BLUE_PRIMARY = "#2C6496"
   ```

2. **Create chart:**
   ```python
   fig = go.Figure()
   fig.add_trace(go.Scatter(x=x, y=y, line=dict(color=TEAL_ACCENT)))
   ```

3. **Apply branding:**
   ```python
   fig = format_fig(fig)  # See implementation above
   ```

### Task 2: Setup Streamlit Branding

1. **Create config directory:**
   ```bash
   mkdir .streamlit
   ```

2. **Copy theme config:**
   ```bash
   cat givecalc/.streamlit/config.toml > .streamlit/config.toml
   ```

3. **Verify in app:**
   ```python
   import streamlit as st

   st.button("Test", type="primary")  # Should be teal
   ```

### Task 3: Brand Consistency Check

**Checklist:**
- [ ] Charts use Roboto Serif font
- [ ] Primary color is TEAL_ACCENT (#39C6C0)
- [ ] Secondary color is BLUE_PRIMARY (#2C6496)
- [ ] White backgrounds
- [ ] Logo in charts (bottom right)
- [ ] Currency formatted with $ and commas
- [ ] Percentages formatted with %
- [ ] Streamlit config.toml uses PolicyEngine theme

## Reference Implementations

### Excellent Examples

**Streamlit calculators:**
```bash
# GiveCalc - Complete example
cat givecalc/ui/visualization.py
cat givecalc/.streamlit/config.toml

# Other calculators
ls salt-amt-calculator/
ls ctc-calculator/
```

**Blog post charts:**
```bash
# Analysis with branded charts
cat policyengine-app/src/posts/articles/harris-eitc.md
cat policyengine-app/src/posts/articles/montana-tax-cuts-2026.md
```

**React app components:**
```bash
# Charts in app
cat policyengine-app/src/pages/policy/output/DistributionalImpact.jsx
```

### Don't Use These

**❌ Wrong colors:**
```python
# Don't use random colors
color = "#FF5733"
color = "red"
color = "green"
```

**❌ Wrong fonts:**
```python
# Don't use other fonts for charts
font = dict(family="Arial")
font = dict(family="Times New Roman")
```

**❌ Missing logo:**
```python
# Don't skip the logo in charts for publication
# All published charts should include PolicyEngine logo
```

## Assets and Resources

### Logo Files

**In policyengine-app repository:**
```bash
policyengine-app/src/images/logos/policyengine/
├── blue.png      # Primary logo (light backgrounds)
├── white.png     # Logo for dark backgrounds
├── blue.svg      # Scalable blue logo
├── white.svg     # Scalable white logo
├── banners/      # Banner variations
└── profile/      # Profile/avatar versions
```

**Raw URLs for direct use:**
```python
# Use these URLs in code
LOGO_URL = "https://raw.githubusercontent.com/PolicyEngine/policyengine-app-v2/main/app/public/assets/logos/policyengine/teal.png"
```

### Font Files

**Roboto (charts):**
- Google Fonts: https://fonts.google.com/specimen/Roboto
- Family: Roboto Serif
- Weights: 300 (light), 400 (regular), 500 (medium), 700 (bold)

**Loading:**
```html
<link href="https://fonts.googleapis.com/css2?family=Roboto+Serif:wght@300;400;500;700&display=swap" rel="stylesheet">
```

### Color Reference Files

**JavaScript (React app):**
```bash
cat policyengine-app/src/style/colors.js
```

**Python (calculators, analysis):**
```python
# Define in constants.py or at top of file
TEAL_ACCENT = "#39C6C0"
BLUE_PRIMARY = "#2C6496"
DARK_GRAY = "#616161"
WHITE = "#FFFFFF"
```

## Brand Evolution

**Current identity (2025):**
- Teal primary (#39C6C0)
- Blue secondary (#2C6496)
- Roboto Serif for charts
- Minimal, data-focused design

**If brand evolves:**
- Colors defined in policyengine-app/src/style/colors.js are source of truth
- Update this skill to point to current definitions
- Never hardcode - always reference colors.js

## Quick Reference

### Color Codes

| Color | Hex | Usage |
|-------|-----|-------|
| Teal Accent | #39C6C0 | Primary interactive elements |
| Blue Primary | #2C6496 | Secondary, links, charts |
| Dark Gray | #616161 | Body text |
| White | #FFFFFF | Backgrounds |
| Teal Light | #F7FDFC | Secondary backgrounds |
| Dark Red | #b50d0d | Negative values, errors |

### Font Families

| Context | Font |
|---------|------|
| Charts | Roboto Serif |
| Web app | System sans-serif |
| Streamlit | Default sans-serif |
| Code blocks | Monospace |

### Logo URLs

| Background | Format | URL |
|------------|--------|-----|
| Light | PNG | https://raw.githubusercontent.com/PolicyEngine/policyengine-app-v2/main/app/public/assets/logos/policyengine/teal.png |
| Light | SVG | https://raw.githubusercontent.com/PolicyEngine/policyengine-app-v2/main/app/public/assets/logos/policyengine/teal.svg |
| Dark | PNG | https://raw.githubusercontent.com/PolicyEngine/policyengine-app-v2/main/app/public/assets/logos/policyengine/white.png |
| Dark | SVG | https://raw.githubusercontent.com/PolicyEngine/policyengine-app-v2/main/app/public/assets/logos/policyengine/white.svg |

## Related Skills

- **policyengine-app-skill** - React component styling
- **policyengine-analysis-skill** - Chart creation patterns
- **policyengine-writing-skill** - Content style (complements visual style)

## Resources

**Brand assets:** PolicyEngine/policyengine-app/src/images/
**Color definitions:** PolicyEngine/policyengine-app/src/style/colors.js
**Examples:** givecalc, salt-amt-calculator, crfb-tob-impacts
