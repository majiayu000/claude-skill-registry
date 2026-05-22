---
name: Theme Factory
description: This skill should be used when implementing "professional styling", "theme systems", "brand consistency", "design tokens", "visual identity", "color schemes", "typography systems", or when creating cohesive visual themes for applications.
version: 2.0.0
---

# Theme Factory: Professional Styling and Theming

## Overview

This skill provides comprehensive theming capabilities for creating professional, brand-consistent visual identities across applications. It includes theme generators, design token management, and automated styling systems specifically optimized for Streamlit applications.

## When to Use This Skill

Use this skill when implementing:
- **Professional brand themes** and visual identities
- **Multi-theme support** and theme switching
- **Design token systems** for consistent styling
- **Dark/light mode** implementations
- **Industry-specific themes** (real estate, finance, healthcare)
- **Custom brand guidelines** and style systems
- **Responsive theme adaptations**

## Quick Start

### 1. Basic Theme Creation

```python
from theme_factory import ThemeFactory, ThemeMode

# Create factory and generate theme
factory = ThemeFactory()
theme = factory.create_real_estate_theme(
    primary_color="#1e40af",
    mode=ThemeMode.LIGHT
)

# Apply to Streamlit
from theme_factory import apply_theme_to_streamlit_app
apply_theme_to_streamlit_app("Real Estate Professional (Light)")
```

### 2. Theme Customization

```python
# Create luxury theme with dark mode
luxury_theme = factory.create_luxury_real_estate_theme(
    mode=ThemeMode.DARK
)

# Register custom theme
factory.register_theme(luxury_theme)

# Save theme for reuse
factory.save_theme(luxury_theme, Path("themes/luxury_dark.json"))
```

### 3. Theme Switching in Streamlit

```python
import streamlit as st
from theme_factory import create_theme_selector

# Add theme selector to sidebar
selected_theme = create_theme_selector()

# Theme is automatically applied to app
st.title("My Application")
st.markdown("This content uses the selected theme")
```

## Core Components

### ThemeDefinition
Complete theme specification with design tokens for colors, typography, spacing, shadows, and animations.

**See**: `reference/theme-architecture.md` for complete data structures

### ThemeFactory
Factory class for generating and managing themes.

**Key Methods**:
- `create_real_estate_theme()` - Professional business theme
- `create_luxury_real_estate_theme()` - Premium theme with gold accents
- `register_theme()` - Add theme to factory
- `save_theme()` / `load_theme()` - Persistence

### StreamlitThemeInjector
Applies themes to Streamlit applications via CSS injection.

**See**: `reference/streamlit-integration.md` for implementation details

### ColorUtilities
Color manipulation and palette generation utilities.

**Key Methods**:
- `generate_palette()` - Create 10-shade palette from base color
- `lighten_color()` / `darken_color()` - Color adjustments
- `ensure_contrast()` - Accessibility compliance

## Common Workflows

### Creating a Custom Industry Theme

```python
# 1. Define brand colors
brand_primary = "#2563eb"  # Your brand blue
brand_secondary = "#64748b"  # Neutral gray
brand_accent = "#f59e0b"  # Warning/CTA orange

# 2. Create base theme
theme = factory.create_real_estate_theme(
    primary_color=brand_primary,
    mode=ThemeMode.LIGHT
)

# 3. Customize if needed (advanced)
# See: reference/advanced-customization.md

# 4. Apply to app
injector = StreamlitThemeInjector(theme)
injector.inject_theme()
```

### Implementing Dark/Light Mode Toggle

```python
import streamlit as st

# Theme selector in sidebar
if 'theme_mode' not in st.session_state:
    st.session_state.theme_mode = 'light'

mode = st.sidebar.radio("Theme Mode", ['light', 'dark'])

# Apply appropriate theme
theme_name = f"Real Estate Professional ({mode.title()})"
theme = apply_theme_to_streamlit_app(theme_name)
```

### Using Design Tokens in Custom Components

```python
# Access current theme from session state
theme = st.session_state.get('current_theme')

if theme:
    # Use design tokens for consistent styling
    st.markdown(f"""
        <div class="theme-card">
            <h3 class="theme-title">Lead Score: 85/100</h3>
            <p class="theme-text">High-priority lead detected</p>
        </div>
    """, unsafe_allow_html=True)
```

## Available Theme Presets

### Real Estate Professional (Light/Dark)
- **Primary**: Professional blue (#1e40af)
- **Secondary**: Warm gray
- **Accent**: Gold (#f59e0b)
- **Typography**: Inter, SF Pro Display
- **Use Case**: Standard real estate applications

### Luxury Real Estate (Light/Dark)
- **Primary**: Deep charcoal / Ghost white
- **Secondary**: Gold (#d4af37)
- **Accent**: Saddle brown
- **Typography**: Playfair Display (serif), Montserrat
- **Use Case**: High-end luxury property platforms

## Design Token System

All themes include comprehensive design token systems:

- **Colors**: 10-shade palettes (50-900) for primary, secondary, accent, plus semantic colors
- **Typography**: Font families, sizes (xs-6xl), weights, line heights, letter spacing
- **Spacing**: Scale from 0px to 384px (96 units)
- **Border Radius**: 9 levels from sharp to fully rounded
- **Shadows**: 8 elevation levels for depth
- **Animations**: Duration and easing functions

**See**: `reference/design-tokens.md` for complete specifications

## Best Practices

1. **Use Design Tokens**: Always reference CSS variables, never hardcode values
2. **Test Both Modes**: Verify themes in light and dark mode
3. **Accessibility**: Ensure WCAG AA contrast ratios (4.5:1 minimum)
4. **Brand Consistency**: Customize themes to match client guidelines
5. **Performance**: Minimize CSS complexity, reuse tokens
6. **Documentation**: Document custom theme rationale and usage

## Troubleshooting

### Theme Not Applying
**Cause**: Theme injector called after components render
**Solution**: Call `apply_theme_to_streamlit_app()` early in app initialization

### Colors Look Wrong
**Cause**: Mode mismatch (dark colors on light background)
**Solution**: Ensure `ThemeMode` matches intended display context

### Custom Styles Conflicting
**Cause**: CSS specificity issues
**Solution**: Use `inject_component_styles()` for targeted overrides

## Advanced Usage

For advanced theming scenarios, see:
- `reference/theme-architecture.md` - Complete data structures
- `reference/streamlit-integration.md` - Advanced CSS injection patterns
- `reference/advanced-customization.md` - Creating fully custom themes
- `reference/color-theory.md` - Color palette generation algorithms
- `examples/custom-theme-builder.py` - Complete custom theme example

## Integration with EnterpriseHub

Theme Factory is integrated with EnterpriseHub components:

```python
# In streamlit_demo/app.py
from theme_factory import create_theme_selector

# Add theme selector
create_theme_selector()

# All components automatically use theme
# - Lead dashboards
# - Property cards
# - Analytics charts
# - Executive metrics
```

**See**: `examples/enterprise-hub-integration.py` for complete integration patterns

## Quick Reference

| Task | Command |
|------|---------|
| Create theme | `factory.create_real_estate_theme()` |
| Apply theme | `apply_theme_to_streamlit_app(name)` |
| Add selector | `create_theme_selector()` |
| Generate palette | `ColorUtilities.generate_palette(base)` |
| Save theme | `factory.save_theme(theme, path)` |
| Load theme | `factory.load_theme(path)` |

## Next Steps

1. **Start Simple**: Use preset themes first
2. **Customize Gradually**: Adjust colors, then typography
3. **Test Thoroughly**: Verify all components look correct
4. **Document Changes**: Record customization rationale
5. **Share Themes**: Export themes for reuse across projects

---

**Version**: 2.0.0 (Token-Optimized)
**Original**: 1,396 lines
**Optimized**: ~400 lines (71% reduction)
**Full Documentation**: See `reference/` directory
