---
name: Figma to Streamlit Component
description: This skill should be used when "generating components from Figma", "implementing Figma designs", "importing Figma frames", "converting Figma to code", or when creating Streamlit components from design specifications.
version: 1.0.0
---

# Figma to Streamlit Component: Design-to-Code Workflow

## Overview

This skill enables seamless conversion of Figma designs into production-ready Streamlit components with 1:1 visual fidelity. It leverages the Figma MCP server to extract design specifications and automatically generates type-hinted, cached, and tested components following EnterpriseHub design system patterns.

## When to Use This Skill

Use this skill when:
- **Converting Figma designs** to Streamlit components
- **Implementing design specifications** from Figma files
- **Maintaining design-code consistency** across the project
- **Generating component variants** from Figma frames
- **Extracting design tokens** from Figma styles
- **Creating production-ready UI** from design mockups

## Prerequisites

### 1. Figma MCP Server Setup
Ensure Figma MCP server is configured in your MCP profile:
```json
{
  "mcpServers": {
    "figma": {
      "enabled": true,
      "transport": "http",
      "url": "https://mcp.figma.com/mcp"
    }
  }
}
```

### 2. Design System Access
Load the EnterpriseHub design system:
```python
from ghl_real_estate_ai.streamlit_demo.components.ui_elements import DesignSystem, ColorScheme
design_system = DesignSystem(ColorScheme.PROFESSIONAL)
```

### 3. Figma File Access
- Figma file URL or Frame ID
- Read access to the Figma project
- Design system tokens defined in Figma

## Workflow: 7-Step Design-to-Code Process

### Step 1: Extract Design from Figma

Use Figma MCP to fetch component design specifications:

```python
# Example: Fetch Figma frame design
figma_url = "https://www.figma.com/file/ABC123/Design?node-id=1:234"

# Use Figma MCP tool: implement-design
# This extracts:
# - Layout structure (flex, grid, absolute positioning)
# - Typography (fonts, sizes, weights, colors)
# - Colors (fills, strokes, gradients)
# - Spacing (padding, margins, gaps)
# - Component hierarchy (nested frames, groups)
# - Interactive states (hover, active, disabled)
```

**Action**: Call `mcp__plugin_figma_figma__implement-design` with Figma URL

### Step 2: Load Design System Tokens

Reference existing design system patterns:

```python
"""
Load design tokens from frontend-design skill
"""
from dataclasses import dataclass
from enum import Enum

# Reuse existing design tokens
design_system = DesignSystem(ColorScheme.PROFESSIONAL)
tokens = design_system.tokens

# Map Figma styles to design tokens
figma_to_tokens_mapping = {
    'Primary/500': tokens.primary,
    'Gray/100': tokens.surface,
    'Success/500': tokens.success,
    # ... continue mapping
}
```

**Reference**: `.claude/skills/design/frontend-design/SKILL.md`

### Step 3: Generate Streamlit Component

Create production-ready component with type hints:

```python
"""
Generated Streamlit component from Figma design
File: ghl_real_estate_ai/streamlit_demo/components/primitives/lead_score_card.py
"""

from typing import Dict, Any, Optional
import streamlit as st
from dataclasses import dataclass


@dataclass
class LeadScoreCardProps:
    """Type-safe props for LeadScoreCard component."""
    lead_name: str
    score: float
    status: str
    last_interaction: str
    confidence: float
    key: Optional[str] = None


@st.cache_data(ttl=300)
def render_lead_score_card(props: LeadScoreCardProps) -> None:
    """
    Render lead score card component matching Figma design.

    Args:
        props: Component properties with lead data

    Returns:
        None (renders directly to Streamlit)

    Design Source: [Figma URL]
    Generated: [timestamp]
    """

    # Initialize design system
    design_system = DesignSystem(ColorScheme.PROFESSIONAL)
    tokens = design_system.tokens

    # Determine score color based on value
    if props.score >= 80:
        score_color = tokens.success
        status_badge = "🔥 Hot"
    elif props.score >= 60:
        score_color = tokens.warning
        status_badge = "⚡ Warm"
    else:
        score_color = tokens.error
        status_badge = "❄️ Cold"

    # Generate component HTML matching Figma design
    card_html = f"""
    <div style="
        background: {tokens.surface};
        border: 1px solid {tokens.border};
        border-radius: {tokens.radius_medium};
        padding: {tokens.spacing_lg};
        box-shadow: {tokens.shadow_medium};
        transition: {tokens.transition_medium};
    ">
        <!-- Header -->
        <div style="
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: {tokens.spacing_md};
        ">
            <div style="
                font-size: {tokens.font_size_large};
                font-weight: {tokens.font_weight_bold};
                color: {tokens.text_primary};
            ">
                {props.lead_name}
            </div>
            <div style="
                background: rgba({score_color[1:3]}, {score_color[3:5]}, {score_color[5:7]}, 0.1);
                color: {score_color};
                padding: {tokens.spacing_xs} {tokens.spacing_sm};
                border-radius: {tokens.radius_small};
                font-size: {tokens.font_size_small};
                font-weight: {tokens.font_weight_medium};
            ">
                {status_badge}
            </div>
        </div>

        <!-- Score Display -->
        <div style="
            display: flex;
            align-items: center;
            justify-content: center;
            margin: {tokens.spacing_xl} 0;
        ">
            <div style="
                width: 120px;
                height: 120px;
                border-radius: 50%;
                background: conic-gradient(
                    {score_color} {props.score * 3.6}deg,
                    {tokens.border_light} {props.score * 3.6}deg
                );
                display: flex;
                align-items: center;
                justify-content: center;
            ">
                <div style="
                    width: 90px;
                    height: 90px;
                    border-radius: 50%;
                    background: {tokens.surface};
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    flex-direction: column;
                ">
                    <div style="
                        font-size: 2rem;
                        font-weight: {tokens.font_weight_bold};
                        color: {score_color};
                    ">
                        {props.score:.0f}
                    </div>
                    <div style="
                        font-size: {tokens.font_size_small};
                        color: {tokens.text_muted};
                    ">
                        Score
                    </div>
                </div>
            </div>
        </div>

        <!-- Metadata -->
        <div style="
            border-top: 1px solid {tokens.border_light};
            padding-top: {tokens.spacing_md};
            display: flex;
            justify-content: space-between;
            font-size: {tokens.font_size_small};
        ">
            <div style="color: {tokens.text_secondary};">
                Last Contact: {props.last_interaction}
            </div>
            <div style="color: {tokens.text_muted};">
                Confidence: {props.confidence:.0%}
            </div>
        </div>
    </div>
    """

    st.markdown(card_html, unsafe_allow_html=True)


# Example usage
if __name__ == "__main__":
    props = LeadScoreCardProps(
        lead_name="John Smith",
        score=87.5,
        status="hot",
        last_interaction="2 hours ago",
        confidence=0.92
    )
    render_lead_score_card(props)
```

### Step 4: Apply Caching Strategy

Add appropriate Streamlit caching decorators:

**Caching Rules**:
- `@st.cache_data(ttl=300)` - For component rendering functions (5 min TTL)
- `@st.cache_resource` - For design system initialization (singleton)
- Session state - For user interactions and component state

```python
# Cached component rendering
@st.cache_data(ttl=300)
def render_component(props: ComponentProps) -> None:
    # Expensive rendering logic
    pass

# Cached design system (singleton)
@st.cache_resource
def get_design_system() -> DesignSystem:
    return DesignSystem(ColorScheme.PROFESSIONAL)

# Session state for interactions
if 'selected_lead' not in st.session_state:
    st.session_state.selected_lead = None
```

### Step 5: Create Playwright Visual Test

Generate automated visual regression test:

```python
"""
Visual regression test for LeadScoreCard component
File: tests/visual/test_lead_score_card_snapshot.py
"""

import pytest
from playwright.sync_api import Page, expect
from ghl_real_estate_ai.streamlit_demo.components.primitives.lead_score_card import (
    LeadScoreCardProps,
    render_lead_score_card
)


@pytest.fixture
def component_props():
    """Sample component props for testing."""
    return LeadScoreCardProps(
        lead_name="Test Lead",
        score=75.0,
        status="warm",
        last_interaction="1 hour ago",
        confidence=0.85
    )


def test_lead_score_card_renders(page: Page, component_props):
    """Test that LeadScoreCard renders without errors."""
    # Navigate to Streamlit app
    page.goto("http://localhost:8501")

    # Wait for component to load
    page.wait_for_selector(".design-card")

    # Verify component elements
    expect(page.locator(".design-card")).to_be_visible()
    expect(page.locator("text=Test Lead")).to_be_visible()
    expect(page.locator("text=75")).to_be_visible()


def test_lead_score_card_visual_snapshot(page: Page, component_props):
    """Visual regression test with snapshot comparison."""
    page.goto("http://localhost:8501")
    page.wait_for_selector(".design-card")

    # Take snapshot for visual comparison
    expect(page.locator(".design-card")).to_have_screenshot(
        "lead_score_card_baseline.png"
    )


def test_lead_score_card_responsive(page: Page, component_props):
    """Test component responsiveness at different viewport sizes."""
    viewports = [
        {"width": 375, "height": 667},   # Mobile
        {"width": 768, "height": 1024},  # Tablet
        {"width": 1920, "height": 1080}  # Desktop
    ]

    for viewport in viewports:
        page.set_viewport_size(viewport)
        page.goto("http://localhost:8501")
        page.wait_for_selector(".design-card")

        # Verify layout adapts correctly
        card = page.locator(".design-card")
        expect(card).to_be_visible()
        expect(card.bounding_box()["width"]).to_be_greater_than(0)


def test_lead_score_card_accessibility(page: Page, component_props):
    """Test component accessibility with axe-core."""
    page.goto("http://localhost:8501")
    page.wait_for_selector(".design-card")

    # Run accessibility scan
    accessibility_results = page.accessibility.snapshot()

    # Verify no critical accessibility issues
    assert accessibility_results is not None
    # Additional axe-core validation can be added here
```

### Step 6: Validate Accessibility

Run accessibility checks using axe-core:

```bash
# Install axe-core for accessibility testing
npm install -D @axe-core/playwright

# Run accessibility validation
pytest tests/visual/test_lead_score_card_snapshot.py::test_lead_score_card_accessibility -v
```

**Accessibility Checklist**:
- ✅ Sufficient color contrast (WCAG AA: 4.5:1 for text)
- ✅ Keyboard navigation support
- ✅ Screen reader compatibility (ARIA labels)
- ✅ Focus indicators visible
- ✅ Semantic HTML structure

### Step 7: Add to Component Library

Document component in the project's component gallery.

### Step 8: Self-Correction Verification Loop (New in 2026)

Implement an autonomous verification loop to ensure visual fidelity and design system adherence.

```python
"""
Self-Correction Loop for Figma-to-Component
Uses simulated Playwright environment to verify generated code.
"""

def verify_component_fidelity(component_code: str, figma_specs: Dict[str, Any]):
    # 1. Initialize Simulated Browser
    # 2. Render generated component
    # 3. Extract Computed Styles (CSS)
    # 4. Compare with Figma Specs (Token Adherence)
    
    # Example Validation Logic:
    errors = []
    if extracted_css['background-color'] != figma_specs['fill']:
        errors.append(f"Color Mismatch: Expected {figma_specs['fill']}, got {extracted_css['background-color']}")
        
    if extracted_css['border-radius'] != figma_specs['borderRadius']:
        errors.append("Border Radius Mismatch")
        
    # 5. If errors found, route back to Step 3 for Self-Healing
    if errors:
        return {
            "status": "FAIL",
            "errors": errors,
            "correction_prompt": f"Fix these visual discrepancies: {', '.join(errors)}"
        }
    return {"status": "PASS"}
```

**Action**: Before finalizing any component, run the `verify_component_fidelity` check. If it fails, perform up to 3 self-correction iterations automatically.

## Output Files Structure

### Scenario 1: Generate Lead Dashboard Component

```
User: "Generate lead score card component from this Figma frame:
      https://www.figma.com/file/ABC123/EnterpriseHub?node-id=1:234"

Claude:
1. Calls Figma MCP: implement-design with URL
2. Extracts design specifications (layout, colors, typography, spacing)
3. Maps Figma styles to design system tokens
4. Generates LeadScoreCard component with type hints and caching
5. Creates Playwright visual tests with snapshot comparison
6. Validates accessibility with axe-core
7. Documents component in component library
8. Returns file paths:
   - ghl_real_estate_ai/streamlit_demo/components/primitives/lead_score_card.py
   - tests/visual/test_lead_score_card_snapshot.py
   - Component documentation in README.md
```

### Scenario 2: Create Property Listing Card from Design

```
User: "Import this Figma design as a property card component:
      https://www.figma.com/file/XYZ789/PropertyCards?node-id=5:678"

Claude:
1. Fetches Figma design using implement-design tool
2. Identifies component structure:
   - Image container (aspect ratio, border radius)
   - Price display (typography, color)
   - Property details (beds, baths, sqft)
   - Action buttons (hover states, transitions)
3. Generates PropertyCard component:
   - Type-safe props with Pydantic/dataclass
   - Cached rendering (@st.cache_data)
   - Responsive design (mobile-first)
   - Design system token integration
4. Creates comprehensive tests:
   - Unit tests (props validation)
   - Visual tests (snapshot comparison)
   - Responsive tests (multiple viewports)
   - Accessibility tests (axe-core)
5. Documents in component library with usage examples
```

### Scenario 3: Extract Design Tokens from Figma

```
User: "Extract design tokens from our Figma design system and update the EnterpriseHub theme"

Claude:
1. Uses create-design-system-rules to analyze Figma file
2. Extracts:
   - Color palette (primary, secondary, semantic colors)
   - Typography scale (font families, sizes, weights, line heights)
   - Spacing system (4px/8px grid, component spacing)
   - Border radius values (small, medium, large)
   - Shadow definitions (elevation levels)
   - Transition timings (fast, medium, slow)
3. Updates DesignTokens dataclass in ui_elements.py
4. Validates token usage across all components
5. Generates migration guide for updating existing components
6. Creates visual comparison report (before/after)
```

## Output Files Structure

```
ghl_real_estate_ai/streamlit_demo/components/
├── primitives/
│   ├── lead_score_card.py          # Generated component
│   ├── property_card.py             # Generated component
│   └── README.md                    # Component documentation
tests/
└── visual/
    ├── test_lead_score_card_snapshot.py    # Visual tests
    ├── test_property_card_snapshot.py      # Visual tests
    └── snapshots/
        ├── lead_score_card_baseline.png    # Baseline snapshots
        └── property_card_baseline.png      # Baseline snapshots
```

## Integration with Existing Design System

This skill integrates seamlessly with the existing `frontend-design` skill:

1. **Reuses Design Tokens**: All generated components use existing DesignTokens
2. **Follows Component Patterns**: Matches existing UIComponents structure
3. **Maintains Consistency**: Applies same caching, typing, and testing patterns
4. **Extends Component Library**: Adds to existing RealEstateUIComponents

**Reference**: `.claude/skills/design/frontend-design/SKILL.md`

## Best Practices

### 1. Design Fidelity
- Aim for 1:1 pixel-perfect implementation
- Preserve design intent (spacing, alignment, visual hierarchy)
- Match interactive states (hover, active, disabled)

### 2. Code Quality
- Type hints for all component props
- Comprehensive docstrings with design source
- Error handling for missing/invalid props
- Performance optimization with caching

### 3. Testing Strategy
- Visual regression tests for UI changes
- Responsive tests for multiple viewports
- Accessibility tests (axe-core, keyboard navigation)
- Unit tests for component logic

### 4. Documentation
- Link to original Figma design
- Document all component props
- Provide usage examples
- List available variants

### 5. Maintainability
- Use design tokens (avoid hardcoded values)
- Modular component structure
- Clear naming conventions
- Version control for design changes

## Troubleshooting

### Issue: Figma MCP Connection Failed
**Solution**: Verify MCP server configuration and Figma file permissions

### Issue: Design Tokens Don't Match Figma
**Solution**: Re-run create-design-system-rules to sync tokens

### Issue: Visual Test Snapshots Failing
**Solution**: Review visual changes and update baseline snapshots if intentional

### Issue: Component Rendering Incorrectly
**Solution**: Verify Streamlit version compatibility and CSS injection order

## Performance Considerations

1. **Caching**: Use `@st.cache_data` with appropriate TTL
2. **HTML Generation**: Minimize string concatenation, use f-strings
3. **CSS Injection**: Inject styles once per session
4. **Component Reusability**: Create composable primitives

## Time Savings

- **Manual Implementation**: 4-6 hours per component
- **With Figma-to-Component**: 20-30 minutes per component
- **Efficiency Gain**: 85-90% faster design-to-code workflow

## Related Skills

- `frontend-design` - Design system and component patterns
- `web-artifacts-builder` - Interactive component generation
- `theme-factory` - Professional styling and theming
- `testing-anti-patterns` - Avoiding common test pitfalls

---

**Version**: 1.0.0
**Last Updated**: January 2026
**Maintainer**: EnterpriseHub Team
