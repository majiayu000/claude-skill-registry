---
name: Web Artifacts Builder
description: This skill should be used when creating "interactive web components", "live demos", "prototype interfaces", "component showcases", "interactive examples", "web-based tools", or when building dynamic web artifacts for testing and demonstration purposes.
version: 1.0.0
---

# Web Artifacts Builder: Interactive Component Generation

## Overview

This skill provides tools and patterns for creating interactive web artifacts, including live component demos, prototype interfaces, and dynamic web-based tools. Particularly useful for showcasing Streamlit components and creating interactive examples.

## When to Use This Skill

Use this skill when creating:
- **Interactive component demos** and showcases
- **Prototype interfaces** for user testing
- **Live documentation** with working examples
- **Web-based tools** and utilities
- **A/B testing interfaces**
- **Component galleries** and design systems
- **Interactive tutorials** and onboarding flows

## Core Artifact Types

### 1. Interactive Component Showcase

```python
"""
Interactive showcase for demonstrating component variations
"""

import streamlit as st
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import json
import inspect
from pathlib import Path


class ArtifactType(Enum):
    """Types of web artifacts that can be built."""
    COMPONENT_SHOWCASE = "component_showcase"
    INTERACTIVE_DEMO = "interactive_demo"
    PROTOTYPE_INTERFACE = "prototype_interface"
    DESIGN_SYSTEM_GALLERY = "design_system_gallery"
    TUTORIAL_FLOW = "tutorial_flow"
    A_B_TEST_INTERFACE = "ab_test_interface"


@dataclass
class ComponentVariation:
    """Represents a variation of a component for showcase."""
    name: str
    description: str
    props: Dict[str, Any]
    code_example: Optional[str] = None
    notes: Optional[str] = None


@dataclass
class ArtifactConfiguration:
    """Configuration for building web artifacts."""
    title: str
    description: str
    artifact_type: ArtifactType
    components: List[str] = field(default_factory=list)
    variations: List[ComponentVariation] = field(default_factory=list)
    interactive_controls: Dict[str, Any] = field(default_factory=dict)
    code_display: bool = True
    live_preview: bool = True
    responsive_preview: bool = False


class ComponentShowcaseBuilder:
    """Builder for interactive component showcases."""

    def __init__(self, design_system, ui_components):
        self.design_system = design_system
        self.ui_components = ui_components
        self.current_config = None

    def create_showcase(self, config: ArtifactConfiguration):
        """Create an interactive component showcase."""
        self.current_config = config

        # Inject showcase-specific styles
        self._inject_showcase_styles()

        # Main showcase layout
        st.title(config.title)
        st.markdown(config.description)

        # Create main layout
        if config.code_display:
            preview_col, code_col = st.columns([2, 1])
        else:
            preview_col = st.container()
            code_col = None

        # Interactive controls sidebar
        self._render_interactive_controls()

        # Component variations
        with preview_col:
            self._render_component_variations()

        # Code display
        if code_col:
            with code_col:
                self._render_code_examples()

        # Responsive preview if enabled
        if config.responsive_preview:
            self._render_responsive_preview()

    def _inject_showcase_styles(self):
        """Inject showcase-specific styling."""
        showcase_css = f"""
        <style>
        .showcase-container {{
            background: {self.design_system.tokens.surface};
            border: 1px solid {self.design_system.tokens.border};
            border-radius: {self.design_system.tokens.radius_medium};
            padding: {self.design_system.tokens.spacing_lg};
            margin: {self.design_system.tokens.spacing_md} 0;
        }}

        .variation-preview {{
            background: {self.design_system.tokens.background};
            border: 1px solid {self.design_system.tokens.border_light};
            border-radius: {self.design_system.tokens.radius_small};
            padding: {self.design_system.tokens.spacing_md};
            margin: {self.design_system.tokens.spacing_sm} 0;
            min-height: 100px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .code-preview {{
            background: #f8f9fa;
            border: 1px solid {self.design_system.tokens.border};
            border-radius: {self.design_system.tokens.radius_small};
            padding: {self.design_system.tokens.spacing_md};
            font-family: 'Monaco', 'Consolas', monospace;
            font-size: 12px;
            overflow-x: auto;
        }}

        .variation-tabs {{
            display: flex;
            border-bottom: 1px solid {self.design_system.tokens.border};
            margin-bottom: {self.design_system.tokens.spacing_md};
        }}

        .variation-tab {{
            padding: {self.design_system.tokens.spacing_sm} {self.design_system.tokens.spacing_md};
            border: none;
            background: transparent;
            cursor: pointer;
            border-bottom: 2px solid transparent;
            transition: {self.design_system.tokens.transition_fast};
        }}

        .variation-tab.active {{
            border-bottom-color: {self.design_system.tokens.accent};
            color: {self.design_system.tokens.accent};
        }}

        .device-preview {{
            border: 3px solid #333;
            border-radius: 20px;
            padding: 20px;
            background: #000;
            margin: {self.design_system.tokens.spacing_md} 0;
        }}

        .device-preview.mobile {{
            width: 375px;
            height: 667px;
        }}

        .device-preview.tablet {{
            width: 768px;
            height: 1024px;
        }}

        .device-preview.desktop {{
            width: 100%;
            height: 600px;
        }}
        </style>
        """

        st.markdown(showcase_css, unsafe_allow_html=True)

    def _render_interactive_controls(self):
        """Render interactive controls in sidebar."""
        st.sidebar.markdown("### Interactive Controls")

        # Render configured controls
        for control_key, control_config in self.current_config.interactive_controls.items():
            control_type = control_config.get('type', 'text')
            control_label = control_config.get('label', control_key)
            default_value = control_config.get('default')

            if control_type == 'text':
                value = st.sidebar.text_input(control_label, value=default_value)
            elif control_type == 'number':
                min_val = control_config.get('min', 0)
                max_val = control_config.get('max', 100)
                value = st.sidebar.slider(control_label, min_val, max_val, default_value)
            elif control_type == 'select':
                options = control_config.get('options', [])
                value = st.sidebar.selectbox(control_label, options, index=0)
            elif control_type == 'checkbox':
                value = st.sidebar.checkbox(control_label, value=default_value)
            elif control_type == 'color':
                value = st.sidebar.color_picker(control_label, value=default_value)

            # Store in session state for component access
            st.session_state[f"control_{control_key}"] = value

    def _render_component_variations(self):
        """Render component variations with live preview."""
        st.markdown("### Component Variations")

        # Create tabs for variations
        if len(self.current_config.variations) > 1:
            tab_names = [var.name for var in self.current_config.variations]
            tabs = st.tabs(tab_names)

            for i, variation in enumerate(self.current_config.variations):
                with tabs[i]:
                    self._render_single_variation(variation)
        else:
            for variation in self.current_config.variations:
                self._render_single_variation(variation)

    def _render_single_variation(self, variation: ComponentVariation):
        """Render a single component variation."""
        st.markdown(f"**{variation.name}**")
        st.markdown(variation.description)

        # Live preview container
        st.markdown('<div class="variation-preview">', unsafe_allow_html=True)

        # Apply interactive control values to props
        modified_props = variation.props.copy()
        for key, value in st.session_state.items():
            if key.startswith("control_"):
                prop_key = key.replace("control_", "")
                if prop_key in modified_props:
                    modified_props[prop_key] = value

        # Render the component with modified props
        self._render_component_with_props(modified_props)

        st.markdown('</div>', unsafe_allow_html=True)

        # Show notes if available
        if variation.notes:
            st.info(variation.notes)

    def _render_component_with_props(self, props: Dict[str, Any]):
        """Render component based on props configuration."""
        # This would be customized based on your component library
        component_type = props.get('_type', 'button')

        if component_type == 'button':
            self.ui_components.button(
                label=props.get('label', 'Button'),
                variant=props.get('variant', 'PRIMARY'),
                size=props.get('size', 'MEDIUM'),
                disabled=props.get('disabled', False)
            )

        elif component_type == 'alert':
            self.ui_components.alert(
                message=props.get('message', 'Alert message'),
                alert_type=props.get('alert_type', 'INFO'),
                dismissible=props.get('dismissible', False)
            )

        elif component_type == 'metric_card':
            self.ui_components.metric_card(
                title=props.get('title', 'Metric'),
                value=props.get('value', 100),
                change=props.get('change'),
                change_type=props.get('change_type'),
                description=props.get('description')
            )

    def _render_code_examples(self):
        """Render code examples for current variations."""
        st.markdown("### Code Examples")

        for variation in self.current_config.variations:
            if variation.code_example:
                st.markdown(f"**{variation.name}**")
                st.code(variation.code_example, language='python')


class InteractiveDemoBuilder:
    """Builder for interactive demos and prototypes."""

    def __init__(self, design_system):
        self.design_system = design_system
        self.demo_state = {}

    def create_property_search_demo(self):
        """Create an interactive property search demo."""
        st.title("🏠 Property Search Demo")
        st.markdown("Interactive demo of the property search functionality")

        # Demo configuration
        with st.expander("Demo Configuration", expanded=False):
            col1, col2 = st.columns(2)

            with col1:
                max_price = st.slider("Max Budget", 100000, 2000000, 500000, 50000)
                bedrooms = st.selectbox("Bedrooms", [1, 2, 3, 4, 5], index=2)

            with col2:
                location = st.text_input("Location", value="Rancho Cucamonga, CA")
                property_type = st.selectbox("Property Type", ["House", "Condo", "Townhouse"])

        # Search results simulation
        st.markdown("### Search Results")

        # Generate mock properties based on search criteria
        mock_properties = self._generate_mock_properties(max_price, bedrooms, location)

        # Display properties in grid
        cols = st.columns(2)
        for i, property_data in enumerate(mock_properties):
            with cols[i % 2]:
                self._render_property_demo_card(property_data)

        # Search analytics
        st.markdown("### Search Analytics")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Properties Found", len(mock_properties))
        with col2:
            avg_price = sum(p['price'] for p in mock_properties) / len(mock_properties)
            st.metric("Average Price", f"${avg_price:,.0f}")
        with col3:
            st.metric("Search Time", "0.3s")

    def create_lead_scoring_demo(self):
        """Create an interactive lead scoring demo."""
        st.title("🎯 Lead Scoring Demo")
        st.markdown("Interactive demo of AI-powered lead scoring")

        # Lead information input
        with st.expander("Lead Information", expanded=True):
            col1, col2 = st.columns(2)

            with col1:
                lead_name = st.text_input("Lead Name", value="John Smith")
                email = st.text_input("Email", value="john.smith@email.com")
                phone = st.text_input("Phone", value="(555) 123-4567")

            with col2:
                budget = st.slider("Budget Range", 100000, 2000000, 750000, 50000)
                timeline = st.selectbox("Timeline", ["Immediately", "Within 3 months", "Within 6 months", "Just browsing"])
                property_type = st.selectbox("Interest", ["First-time buyer", "Upgrading", "Investment", "Downsizing"])

        # Calculate mock lead score
        score = self._calculate_mock_lead_score(budget, timeline, property_type)

        # Display lead score
        st.markdown("### Lead Score Analysis")

        col1, col2 = st.columns([1, 2])

        with col1:
            # Lead score indicator (would use real component)
            self._render_lead_score_indicator(score)

        with col2:
            # Score factors
            st.markdown("**Score Factors:**")
            factors = [
                ("Budget Alignment", 85, "High budget indicates serious buyer"),
                ("Timeline Urgency", 70, "Immediate timeline shows readiness"),
                ("Property Type Match", 90, "Interest aligns with available inventory"),
                ("Contact Information", 100, "Complete contact details provided"),
            ]

            for factor, factor_score, description in factors:
                st.metric(factor, f"{factor_score}/100", help=description)

    def _generate_mock_properties(self, max_price: int, bedrooms: int, location: str) -> List[Dict[str, Any]]:
        """Generate mock property data based on search criteria."""
        import random

        properties = []
        for i in range(6):
            # Generate price within range
            price = random.randint(int(max_price * 0.7), max_price)

            # Generate other attributes
            bathrooms = random.choice([1, 1.5, 2, 2.5, 3]) if bedrooms <= 3 else random.choice([2.5, 3, 3.5, 4])
            sqft = random.randint(bedrooms * 400, bedrooms * 800)

            properties.append({
                'id': i,
                'address': f"{random.randint(100, 9999)} {random.choice(['Oak', 'Pine', 'Maple', 'Cedar'])} St, {location}",
                'price': price,
                'bedrooms': bedrooms,
                'bathrooms': bathrooms,
                'square_feet': sqft,
                'status': random.choice(['available', 'pending', 'available', 'available']),  # Bias toward available
                'image_url': f"https://picsum.photos/400/300?random={i}"
            })

        return properties

    def _calculate_mock_lead_score(self, budget: int, timeline: str, property_type: str) -> float:
        """Calculate a mock lead score based on inputs."""
        base_score = 50

        # Budget factor
        if budget >= 500000:
            base_score += 25
        elif budget >= 300000:
            base_score += 15
        else:
            base_score += 5

        # Timeline factor
        timeline_scores = {
            "Immediately": 30,
            "Within 3 months": 20,
            "Within 6 months": 10,
            "Just browsing": 2
        }
        base_score += timeline_scores.get(timeline, 0)

        # Property type factor
        type_scores = {
            "First-time buyer": 15,
            "Upgrading": 20,
            "Investment": 10,
            "Downsizing": 25
        }
        base_score += type_scores.get(property_type, 0)

        return min(base_score, 100)

    def _render_property_demo_card(self, property_data: Dict[str, Any]):
        """Render a property card for the demo."""
        # Simplified property card for demo
        with st.container():
            st.image(property_data['image_url'], use_container_width=True)
            st.markdown(f"**${property_data['price']:,}**")
            st.markdown(f"{property_data['address']}")
            st.markdown(f"🛏️ {property_data['bedrooms']} bed • 🚿 {property_data['bathrooms']} bath • 📐 {property_data['square_feet']:,} sqft")

            if st.button("View Details", key=f"demo_view_{property_data['id']}"):
                st.success(f"Viewing details for {property_data['address']}")

    def _render_lead_score_indicator(self, score: float):
        """Render lead score indicator for demo."""
        # Simplified version of the real component
        if score >= 80:
            color = "#10b981"  # Green
            status = "Hot"
        elif score >= 60:
            color = "#f59e0b"  # Amber
            status = "Warm"
        else:
            color = "#ef4444"  # Red
            status = "Cold"

        st.markdown(f"""
        <div style="
            text-align: center;
            padding: 20px;
            border: 2px solid {color};
            border-radius: 10px;
            background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
        ">
            <div style="
                font-size: 3em;
                font-weight: bold;
                color: {color};
            ">{score:.0f}</div>
            <div style="
                font-size: 1.2em;
                color: {color};
                font-weight: 600;
                margin-top: 10px;
            ">{status} Lead</div>
        </div>
        """, unsafe_allow_html=True)


class DesignSystemGallery:
    """Gallery showcasing design system components."""

    def __init__(self, design_system, ui_components):
        self.design_system = design_system
        self.ui_components = ui_components

    def create_design_gallery(self):
        """Create a comprehensive design system gallery."""
        st.title("🎨 Design System Gallery")
        st.markdown("Comprehensive showcase of all design system components")

        # Design system overview
        with st.expander("Design System Overview", expanded=False):
            self._render_design_tokens_overview()

        # Component categories
        gallery_sections = [
            ("Typography", self._render_typography_gallery),
            ("Colors", self._render_color_gallery),
            ("Buttons", self._render_button_gallery),
            ("Forms", self._render_form_gallery),
            ("Cards", self._render_card_gallery),
            ("Alerts", self._render_alert_gallery),
            ("Data Display", self._render_data_gallery),
            ("Layout", self._render_layout_gallery),
        ]

        tabs = st.tabs([section[0] for section in gallery_sections])

        for i, (_, render_func) in enumerate(gallery_sections):
            with tabs[i]:
                render_func()

    def _render_design_tokens_overview(self):
        """Render design tokens overview."""
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Color Tokens")
            colors = [
                ("Primary", self.design_system.tokens.primary),
                ("Secondary", self.design_system.tokens.secondary),
                ("Accent", self.design_system.tokens.accent),
                ("Success", self.design_system.tokens.success),
                ("Warning", self.design_system.tokens.warning),
                ("Error", self.design_system.tokens.error),
            ]

            for name, color in colors:
                st.markdown(f"""
                <div style="
                    display: flex;
                    align-items: center;
                    margin: 8px 0;
                ">
                    <div style="
                        width: 30px;
                        height: 30px;
                        background: {color};
                        border-radius: 4px;
                        margin-right: 12px;
                        border: 1px solid #e5e7eb;
                    "></div>
                    <span>{name}: <code>{color}</code></span>
                </div>
                """, unsafe_allow_html=True)

        with col2:
            st.markdown("### Spacing Tokens")
            spacing = [
                ("XS", self.design_system.tokens.spacing_xs),
                ("SM", self.design_system.tokens.spacing_sm),
                ("MD", self.design_system.tokens.spacing_md),
                ("LG", self.design_system.tokens.spacing_lg),
                ("XL", self.design_system.tokens.spacing_xl),
            ]

            for name, size in spacing:
                st.markdown(f"""
                <div style="
                    display: flex;
                    align-items: center;
                    margin: 8px 0;
                ">
                    <div style="
                        width: {size};
                        height: 20px;
                        background: {self.design_system.tokens.accent};
                        margin-right: 12px;
                    "></div>
                    <span>{name}: <code>{size}</code></span>
                </div>
                """, unsafe_allow_html=True)

    def _render_typography_gallery(self):
        """Render typography gallery."""
        st.markdown("### Typography Examples")

        typography_examples = [
            ("Title", "design-title", "Main page titles and headers"),
            ("Subtitle", "design-subtitle", "Section headers and subheadings"),
            ("Body", "design-body", "Regular body text and paragraphs"),
            ("Caption", "design-caption", "Small text and captions"),
        ]

        for name, css_class, description in typography_examples:
            st.markdown(f'<div class="{css_class}">Sample {name} Text</div>', unsafe_allow_html=True)
            st.markdown(f"*{description}*")
            st.markdown("---")

    def _render_color_gallery(self):
        """Render color palette gallery."""
        st.markdown("### Color Palette")

        color_groups = [
            ("Brand Colors", [
                ("Primary", self.design_system.tokens.primary),
                ("Secondary", self.design_system.tokens.secondary),
                ("Accent", self.design_system.tokens.accent),
            ]),
            ("Status Colors", [
                ("Success", self.design_system.tokens.success),
                ("Warning", self.design_system.tokens.warning),
                ("Error", self.design_system.tokens.error),
                ("Info", self.design_system.tokens.info),
            ]),
            ("Neutral Colors", [
                ("Background", self.design_system.tokens.background),
                ("Surface", self.design_system.tokens.surface),
                ("Text Primary", self.design_system.tokens.text_primary),
                ("Text Secondary", self.design_system.tokens.text_secondary),
                ("Text Muted", self.design_system.tokens.text_muted),
                ("Border", self.design_system.tokens.border),
            ])
        ]

        for group_name, colors in color_groups:
            st.markdown(f"#### {group_name}")
            cols = st.columns(len(colors))

            for i, (name, color) in enumerate(colors):
                with cols[i]:
                    st.markdown(f"""
                    <div style="
                        background: {color};
                        height: 80px;
                        border-radius: 8px;
                        border: 1px solid #e5e7eb;
                        margin-bottom: 8px;
                    "></div>
                    <div style="text-align: center;">
                        <strong>{name}</strong><br>
                        <code>{color}</code>
                    </div>
                    """, unsafe_allow_html=True)

    def _render_button_gallery(self):
        """Render button variations gallery."""
        st.markdown("### Button Variations")

        # Button variants
        variants = ["PRIMARY", "SECONDARY", "SUCCESS", "WARNING", "ERROR", "GHOST"]
        sizes = ["SMALL", "MEDIUM", "LARGE"]

        st.markdown("#### By Variant")
        cols = st.columns(len(variants))
        for i, variant in enumerate(variants):
            with cols[i]:
                st.button(f"{variant.title()} Button", key=f"btn_variant_{variant}")

        st.markdown("#### By Size")
        cols = st.columns(len(sizes))
        for i, size in enumerate(sizes):
            with cols[i]:
                st.button(f"{size.title()} Button", key=f"btn_size_{size}")

    def _render_form_gallery(self):
        """Render form components gallery."""
        st.markdown("### Form Components")

        col1, col2 = st.columns(2)

        with col1:
            st.text_input("Text Input", placeholder="Enter text here")
            st.number_input("Number Input", value=100)
            st.selectbox("Select Box", ["Option 1", "Option 2", "Option 3"])

        with col2:
            st.text_area("Text Area", placeholder="Enter longer text here")
            st.checkbox("Checkbox Option")
            st.radio("Radio Options", ["Option A", "Option B", "Option C"])

    def _render_card_gallery(self):
        """Render card components gallery."""
        st.markdown("### Card Components")

        col1, col2 = st.columns(2)

        with col1:
            self.ui_components.card(
                title="Basic Card",
                content="This is a basic card component with title and content."
            )

        with col2:
            self.ui_components.card(
                title="Card with Actions",
                content="This card includes action buttons.",
                actions=[
                    {"type": "button", "label": "Primary Action", "key": "card_action_1"},
                    {"type": "button", "label": "Secondary", "key": "card_action_2"}
                ]
            )

    def _render_alert_gallery(self):
        """Render alert components gallery."""
        st.markdown("### Alert Components")

        alert_types = ["INFO", "SUCCESS", "WARNING", "ERROR"]
        messages = {
            "INFO": "This is an informational alert.",
            "SUCCESS": "This is a success alert.",
            "WARNING": "This is a warning alert.",
            "ERROR": "This is an error alert."
        }

        for alert_type in alert_types:
            self.ui_components.alert(messages[alert_type], getattr(st, alert_type.lower(), st.info))

    def _render_data_gallery(self):
        """Render data display components gallery."""
        st.markdown("### Data Display Components")

        # Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            self.ui_components.metric_card("Total Sales", "$125,430", "+12%", "positive")
        with col2:
            self.ui_components.metric_card("New Leads", "245", "-5%", "negative")
        with col3:
            self.ui_components.metric_card("Conversion Rate", "18.5%", "+2.3%", "positive")

        # Progress bar
        st.markdown("#### Progress Indicators")
        self.ui_components.progress_bar(75, label="Project Progress", show_percentage=True)

        # Data table
        st.markdown("#### Data Table")
        sample_data = [
            {"Name": "John Doe", "Email": "john@example.com", "Score": 85},
            {"Name": "Jane Smith", "Email": "jane@example.com", "Score": 92},
            {"Name": "Bob Johnson", "Email": "bob@example.com", "Score": 78},
        ]
        self.ui_components.data_table(sample_data)

    def _render_layout_gallery(self):
        """Render layout components gallery."""
        st.markdown("### Layout Components")

        st.markdown("#### Two Column Layout")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("Left column content")
        with col2:
            st.markdown("Right column content")

        st.markdown("#### Three Column Layout")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("Column 1")
        with col2:
            st.markdown("Column 2")
        with col3:
            st.markdown("Column 3")


# Usage Examples
def create_component_showcase_example():
    """Example of creating a component showcase."""
    from design.frontend_design import DesignSystem, UIComponents

    design_system = DesignSystem()
    ui_components = UIComponents(design_system)
    showcase_builder = ComponentShowcaseBuilder(design_system, ui_components)

    # Configure showcase
    config = ArtifactConfiguration(
        title="Button Component Showcase",
        description="Interactive showcase of button component variations",
        artifact_type=ArtifactType.COMPONENT_SHOWCASE,
        interactive_controls={
            'label': {
                'type': 'text',
                'label': 'Button Label',
                'default': 'Click Me'
            },
            'disabled': {
                'type': 'checkbox',
                'label': 'Disabled',
                'default': False
            }
        },
        variations=[
            ComponentVariation(
                name="Primary Button",
                description="Main action button with primary styling",
                props={'_type': 'button', 'variant': 'PRIMARY', 'label': 'Primary'},
                code_example='ui_components.button("Primary", variant=ButtonVariant.PRIMARY)'
            ),
            ComponentVariation(
                name="Secondary Button",
                description="Secondary action button with outline styling",
                props={'_type': 'button', 'variant': 'SECONDARY', 'label': 'Secondary'},
                code_example='ui_components.button("Secondary", variant=ButtonVariant.SECONDARY)'
            )
        ],
        code_display=True,
        live_preview=True,
        responsive_preview=True
    )

    # Create showcase
    showcase_builder.create_showcase(config)

def create_interactive_demo_example():
    """Example of creating an interactive demo."""
    design_system = DesignSystem()
    demo_builder = InteractiveDemoBuilder(design_system)

    # Create property search demo
    demo_builder.create_property_search_demo()

def create_design_gallery_example():
    """Example of creating a design system gallery."""
    from design.frontend_design import DesignSystem, UIComponents

    design_system = DesignSystem()
    ui_components = UIComponents(design_system)
    gallery = DesignSystemGallery(design_system, ui_components)

    # Create gallery
    gallery.create_design_gallery()
```

## Project-Specific Artifacts for EnterpriseHub

### Real Estate Demo Artifacts

```python
"""
Real estate specific web artifacts and demos
"""

class RealEstateArtifactBuilder:
    """Builder for real estate specific web artifacts."""

    def __init__(self, design_system):
        self.design_system = design_system

    def create_property_matching_demo(self):
        """Create interactive property matching demo."""
        st.title("🔍 AI Property Matching Demo")
        st.markdown("See how our AI matches properties to buyer preferences")

        # Buyer persona setup
        with st.expander("Buyer Persona", expanded=True):
            col1, col2, col3 = st.columns(3)

            with col1:
                buyer_name = st.text_input("Buyer Name", "Sarah Johnson")
                family_size = st.selectbox("Family Size", [1, 2, 3, 4, 5], index=2)
                lifestyle = st.selectbox("Lifestyle", ["Urban Professional", "Growing Family", "Empty Nester", "First-time Buyer"])

            with col2:
                budget_min = st.number_input("Min Budget", 200000, 2000000, 400000, 50000)
                budget_max = st.number_input("Max Budget", 300000, 3000000, 600000, 50000)
                preferred_areas = st.multiselect("Preferred Areas", ["Downtown", "Suburbs", "Waterfront", "Hills"])

            with col3:
                must_haves = st.multiselect("Must Haves", ["Pool", "Garage", "Garden", "Modern Kitchen", "Home Office"])
                nice_to_haves = st.multiselect("Nice to Haves", ["Fireplace", "Balcony", "Walk-in Closet", "Guest Room"])

        # AI Matching Process Visualization
        st.markdown("### AI Matching Process")

        if st.button("Run AI Matching"):
            # Simulate AI matching process
            with st.spinner("AI analyzing buyer preferences..."):
                import time
                time.sleep(1)

            with st.spinner("Searching property database..."):
                time.sleep(1)

            with st.spinner("Calculating compatibility scores..."):
                time.sleep(1)

            # Show results
            st.success("Matching complete! Found 8 compatible properties.")

            # Display matching results
            self._display_matching_results(buyer_name, budget_max, preferred_areas, must_haves)

    def create_ghl_workflow_demo(self):
        """Create GHL automation workflow demo."""
        st.title("⚡ GHL Automation Workflow Demo")
        st.markdown("Interactive demonstration of lead nurturing automation")

        # Workflow configuration
        workflow_steps = [
            {"name": "Lead Capture", "status": "completed"},
            {"name": "Initial Contact", "status": "completed"},
            {"name": "Lead Qualification", "status": "active"},
            {"name": "Property Matching", "status": "pending"},
            {"name": "Showing Scheduled", "status": "pending"},
            {"name": "Follow-up Sequence", "status": "pending"}
        ]

        # Create workflow visualization
        st.markdown("### Current Workflow Status")
        self._render_workflow_tracker(workflow_steps)

        # Lead information
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Lead Information")
            lead_data = {
                "Name": "Michael Chen",
                "Email": "michael.chen@email.com",
                "Phone": "(555) 987-6543",
                "Source": "Website Form",
                "Interest": "Investment Property",
                "Budget": "$500K - $750K"
            }

            for key, value in lead_data.items():
                st.write(f"**{key}:** {value}")

        with col2:
            st.markdown("#### Automation Actions")

            # Simulate automation actions
            if st.button("Send Welcome Email"):
                st.success("✅ Welcome email sent automatically")

            if st.button("Schedule Follow-up Call"):
                st.success("✅ Follow-up call scheduled for tomorrow 2 PM")

            if st.button("Trigger Property Matching"):
                st.success("✅ AI property matching initiated")

        # Activity Timeline
        st.markdown("### Activity Timeline")
        activities = [
            {"time": "2 minutes ago", "action": "Form submitted", "details": "Lead filled out contact form on website"},
            {"time": "1 minute ago", "action": "Welcome email sent", "details": "Automatic welcome email delivered"},
            {"time": "30 seconds ago", "action": "Lead scored", "details": "AI assigned lead score of 85/100"},
            {"time": "Just now", "action": "Property matching started", "details": "AI analyzing preferences for property matches"}
        ]

        for activity in activities:
            st.markdown(f"""
            <div style="
                padding: 12px;
                border-left: 3px solid {self.design_system.tokens.accent};
                background: {self.design_system.tokens.surface};
                margin: 8px 0;
                border-radius: 0 8px 8px 0;
            ">
                <div style="font-weight: 600; color: {self.design_system.tokens.text_primary};">
                    {activity['action']} <span style="color: {self.design_system.tokens.text_muted}; font-size: 0.9em;">({activity['time']})</span>
                </div>
                <div style="color: {self.design_system.tokens.text_secondary}; margin-top: 4px;">
                    {activity['details']}
                </div>
            </div>
            """, unsafe_allow_html=True)

    def create_ai_insights_demo(self):
        """Create AI insights and analytics demo."""
        st.title("🤖 AI Insights Demo")
        st.markdown("Real-time AI-powered insights and recommendations")

        # Market insights
        st.markdown("### Market Insights")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Market Trend", "↗️ Rising", "5.2% vs last month")
        with col2:
            st.metric("Avg. Days on Market", "28 days", "-3 days vs last month")
        with col3:
            st.metric("Price per Sq Ft", "$285", "+$12 vs last month")

        # AI Recommendations
        st.markdown("### AI Recommendations")

        recommendations = [
            {
                "type": "opportunity",
                "title": "Pricing Opportunity Detected",
                "message": "Property at 123 Oak St is priced 8% below market value. Consider immediate showing.",
                "confidence": 0.92,
                "action": "Schedule Viewing"
            },
            {
                "type": "warning",
                "title": "Market Shift Alert",
                "message": "Interest rates expected to rise next month. Advise pre-approval acceleration.",
                "confidence": 0.85,
                "action": "Contact Lender"
            },
            {
                "type": "recommendation",
                "title": "Lead Nurturing Suggestion",
                "message": "3 leads showing similar patterns to recent conversions. Increase contact frequency.",
                "confidence": 0.78,
                "action": "Update Campaign"
            }
        ]

        for rec in recommendations:
            self._render_ai_recommendation(rec)

        # Predictive Analytics
        st.markdown("### Predictive Analytics")

        # Lead conversion prediction
        st.markdown("#### Lead Conversion Predictions")
        lead_predictions = [
            {"name": "Sarah Johnson", "score": 92, "conversion_probability": 85, "expected_close": "2-3 weeks"},
            {"name": "David Kim", "score": 78, "conversion_probability": 65, "expected_close": "1-2 months"},
            {"name": "Maria Rodriguez", "score": 65, "conversion_probability": 45, "expected_close": "2-3 months"},
        ]

        for lead in lead_predictions:
            self._render_lead_prediction(lead)

    def _display_matching_results(self, buyer_name: str, budget: int, areas: List[str], must_haves: List[str]):
        """Display AI property matching results."""
        st.markdown("### Matching Results")

        # Generate mock properties with compatibility scores
        mock_properties = [
            {
                "address": "456 Elm Street",
                "price": 485000,
                "bedrooms": 3,
                "bathrooms": 2,
                "compatibility": 96,
                "highlights": ["Modern Kitchen", "Garage", "Garden"],
                "concerns": []
            },
            {
                "address": "789 Pine Avenue",
                "price": 525000,
                "bedrooms": 4,
                "bathrooms": 3,
                "compatibility": 89,
                "highlights": ["Pool", "Home Office", "Modern Kitchen"],
                "concerns": ["Slightly over budget"]
            },
            {
                "address": "321 Oak Drive",
                "price": 445000,
                "bedrooms": 3,
                "bathrooms": 2,
                "compatibility": 82,
                "highlights": ["Garden", "Garage", "Fireplace"],
                "concerns": ["No pool"]
            }
        ]

        for prop in mock_properties:
            self._render_property_match_card(prop)

    def _render_property_match_card(self, property_data: Dict[str, Any]):
        """Render a property match card with compatibility score."""
        compatibility = property_data['compatibility']

        # Determine compatibility color
        if compatibility >= 90:
            compat_color = self.design_system.tokens.success
        elif compatibility >= 75:
            compat_color = self.design_system.tokens.warning
        else:
            compat_color = self.design_system.tokens.error

        st.markdown(f"""
        <div style="
            border: 2px solid {compat_color};
            border-radius: {self.design_system.tokens.radius_medium};
            padding: {self.design_system.tokens.spacing_md};
            margin: {self.design_system.tokens.spacing_sm} 0;
            background: {self.design_system.tokens.surface};
        ">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <h4 style="margin: 0; color: {self.design_system.tokens.text_primary};">{property_data['address']}</h4>
                <div style="
                    background: {compat_color};
                    color: white;
                    padding: 4px 12px;
                    border-radius: 20px;
                    font-weight: bold;
                ">
                    {compatibility}% Match
                </div>
            </div>

            <div style="margin-bottom: 12px; color: {self.design_system.tokens.text_secondary};">
                <strong>${property_data['price']:,}</strong> • {property_data['bedrooms']} bed • {property_data['bathrooms']} bath
            </div>

            <div style="display: flex; gap: 20px;">
                <div style="flex: 1;">
                    <strong style="color: {self.design_system.tokens.success};">Highlights:</strong>
                    <ul style="margin: 4px 0 0 0; padding-left: 20px;">
                        {' '.join([f'<li>{highlight}</li>' for highlight in property_data['highlights']])}
                    </ul>
                </div>
                {f'<div style="flex: 1;"><strong style="color: {self.design_system.tokens.warning};">Considerations:</strong><ul style="margin: 4px 0 0 0; padding-left: 20px;">{" ".join([f"<li>{concern}</li>" for concern in property_data["concerns"]])}</ul></div>' if property_data['concerns'] else ''}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Action buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button(f"Schedule Tour", key=f"tour_{hash(property_data['address'])}"):
                st.success(f"Tour scheduled for {property_data['address']}")
        with col2:
            if st.button(f"Get Details", key=f"details_{hash(property_data['address'])}"):
                st.info(f"Detailed information for {property_data['address']}")
        with col3:
            if st.button(f"Save Property", key=f"save_{hash(property_data['address'])}"):
                st.success(f"Property saved to favorites")

    def _render_workflow_tracker(self, steps: List[Dict[str, Any]]):
        """Render workflow progress tracker."""
        # Implementation would be similar to the workflow status tracker
        # from the frontend-design skill, but customized for GHL workflows
        pass

    def _render_ai_recommendation(self, recommendation: Dict[str, Any]):
        """Render AI recommendation card."""
        rec_type = recommendation['type']

        # Map recommendation types to colors
        type_colors = {
            'opportunity': self.design_system.tokens.success,
            'warning': self.design_system.tokens.warning,
            'recommendation': self.design_system.tokens.info
        }

        color = type_colors.get(rec_type, self.design_system.tokens.info)
        confidence = recommendation['confidence']

        st.markdown(f"""
        <div style="
            border: 1px solid {color};
            border-left: 4px solid {color};
            border-radius: {self.design_system.tokens.radius_small};
            padding: {self.design_system.tokens.spacing_md};
            margin: {self.design_system.tokens.spacing_sm} 0;
            background: rgba({color[1:3]}, {color[3:5]}, {color[5:7]}, 0.05);
        ">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <h5 style="margin: 0; color: {color};">{recommendation['title']}</h5>
                <span style="font-size: 0.9em; color: {self.design_system.tokens.text_muted};">
                    Confidence: {confidence:.0%}
                </span>
            </div>
            <p style="margin: 8px 0; color: {self.design_system.tokens.text_primary};">
                {recommendation['message']}
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button(recommendation['action'], key=f"rec_action_{hash(recommendation['title'])}"):
            st.success(f"Action '{recommendation['action']}' triggered")

    def _render_lead_prediction(self, lead_data: Dict[str, Any]):
        """Render lead conversion prediction."""
        probability = lead_data['conversion_probability']

        # Determine probability color
        if probability >= 80:
            prob_color = self.design_system.tokens.success
        elif probability >= 60:
            prob_color = self.design_system.tokens.warning
        else:
            prob_color = self.design_system.tokens.error

        st.markdown(f"""
        <div style="
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: {self.design_system.tokens.spacing_sm} {self.design_system.tokens.spacing_md};
            border: 1px solid {self.design_system.tokens.border};
            border-radius: {self.design_system.tokens.radius_small};
            margin: {self.design_system.tokens.spacing_xs} 0;
            background: {self.design_system.tokens.surface};
        ">
            <div>
                <strong>{lead_data['name']}</strong> (Score: {lead_data['score']})
            </div>
            <div style="text-align: right;">
                <div style="color: {prob_color}; font-weight: bold;">
                    {probability}% likely to convert
                </div>
                <div style="font-size: 0.9em; color: {self.design_system.tokens.text_muted};">
                    Expected: {lead_data['expected_close']}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
```

## Best Practices

1. **Interactive Controls**: Provide meaningful controls that demonstrate component flexibility
2. **Live Preview**: Show real-time updates as users modify controls
3. **Code Examples**: Include copy-pasteable code examples
4. **Responsive Testing**: Test artifacts across different screen sizes
5. **Performance**: Optimize for fast loading and smooth interactions
6. **Accessibility**: Ensure artifacts work with screen readers and keyboards
7. **Documentation**: Include clear descriptions and usage notes

This web artifacts builder skill provides comprehensive tools for creating interactive demos, component showcases, and prototype interfaces that effectively demonstrate the capabilities of the EnterpriseHub GHL Real Estate AI system.