---
name: Frontend Design
description: This skill should be used when implementing "UI/UX design", "Streamlit component design", "frontend styling", "user interface consistency", "design system implementation", "responsive design", or when creating cohesive visual interfaces for web applications.
version: 1.0.0
---

# Frontend Design: UI/UX Consistency and Design Systems

## Overview

This skill provides comprehensive frontend design patterns, focusing on creating consistent, accessible, and professionally styled user interfaces. Specifically optimized for Streamlit applications but applicable to any frontend framework.

## When to Use This Skill

Use this skill when implementing:
- **Consistent UI/UX design** across components
- **Design system implementation**
- **Streamlit component styling** and theming
- **Responsive design patterns**
- **Professional visual hierarchies**
- **Accessibility-compliant interfaces**
- **Brand-consistent user experiences**

## Core Design Principles

### 1. Design System Foundation

```python
"""
Design system foundation with consistent tokens and variables
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum
import streamlit as st
from pathlib import Path
import json


class ColorScheme(Enum):
    """Predefined color schemes for consistent theming."""
    PROFESSIONAL = "professional"
    MODERN = "modern"
    WARM = "warm"
    COOL = "cool"
    HIGH_CONTRAST = "high_contrast"


class ComponentSize(Enum):
    """Consistent sizing system."""
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    EXTRA_LARGE = "xl"


@dataclass
class DesignTokens:
    """Design tokens for consistent styling across the application."""

    # Color Palette
    primary: str
    secondary: str
    accent: str
    success: str
    warning: str
    error: str
    info: str

    # Neutral Colors
    background: str
    surface: str
    text_primary: str
    text_secondary: str
    text_muted: str
    border: str
    border_light: str

    # Typography
    font_family: str
    font_size_base: str
    font_size_small: str
    font_size_large: str
    font_size_xl: str
    font_weight_normal: str
    font_weight_medium: str
    font_weight_bold: str

    # Spacing
    spacing_xs: str
    spacing_sm: str
    spacing_md: str
    spacing_lg: str
    spacing_xl: str

    # Border Radius
    radius_small: str
    radius_medium: str
    radius_large: str

    # Shadows
    shadow_small: str
    shadow_medium: str
    shadow_large: str

    # Transitions
    transition_fast: str
    transition_medium: str
    transition_slow: str


class DesignSystem:
    """Centralized design system for consistent UI components."""

    def __init__(self, color_scheme: ColorScheme = ColorScheme.PROFESSIONAL):
        self.color_scheme = color_scheme
        self.tokens = self._initialize_design_tokens()

    def _initialize_design_tokens(self) -> DesignTokens:
        """Initialize design tokens based on selected color scheme."""

        color_palettes = {
            ColorScheme.PROFESSIONAL: {
                'primary': '#1f2937',      # Gray-800
                'secondary': '#374151',    # Gray-700
                'accent': '#3b82f6',       # Blue-500
                'success': '#10b981',      # Emerald-500
                'warning': '#f59e0b',      # Amber-500
                'error': '#ef4444',        # Red-500
                'info': '#06b6d4',         # Cyan-500
                'background': '#ffffff',
                'surface': '#f9fafb',      # Gray-50
                'text_primary': '#111827',  # Gray-900
                'text_secondary': '#374151', # Gray-700
                'text_muted': '#6b7280',   # Gray-500
                'border': '#e5e7eb',       # Gray-200
                'border_light': '#f3f4f6',  # Gray-100
            },
            ColorScheme.MODERN: {
                'primary': '#0f172a',      # Slate-900
                'secondary': '#1e293b',    # Slate-800
                'accent': '#8b5cf6',       # Violet-500
                'success': '#22c55e',      # Green-500
                'warning': '#eab308',      # Yellow-500
                'error': '#f87171',        # Red-400
                'info': '#0ea5e9',         # Sky-500
                'background': '#ffffff',
                'surface': '#f8fafc',      # Slate-50
                'text_primary': '#0f172a', # Slate-900
                'text_secondary': '#334155', # Slate-700
                'text_muted': '#64748b',   # Slate-500
                'border': '#e2e8f0',       # Slate-200
                'border_light': '#f1f5f9', # Slate-100
            },
            # Add more color schemes as needed
        }

        colors = color_palettes.get(self.color_scheme, color_palettes[ColorScheme.PROFESSIONAL])

        return DesignTokens(
            # Colors
            **colors,

            # Typography
            font_family='"Inter", "SF Pro Display", -apple-system, BlinkMacSystemFont, system-ui, sans-serif',
            font_size_base='16px',
            font_size_small='14px',
            font_size_large='18px',
            font_size_xl='24px',
            font_weight_normal='400',
            font_weight_medium='500',
            font_weight_bold='600',

            # Spacing
            spacing_xs='0.25rem',   # 4px
            spacing_sm='0.5rem',    # 8px
            spacing_md='1rem',      # 16px
            spacing_lg='1.5rem',    # 24px
            spacing_xl='2rem',      # 32px

            # Border Radius
            radius_small='0.25rem',  # 4px
            radius_medium='0.5rem',  # 8px
            radius_large='1rem',     # 16px

            # Shadows
            shadow_small='0 1px 2px 0 rgba(0, 0, 0, 0.05)',
            shadow_medium='0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
            shadow_large='0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',

            # Transitions
            transition_fast='0.15s ease-in-out',
            transition_medium='0.3s ease-in-out',
            transition_slow='0.5s ease-in-out',
        )

    def get_css_variables(self) -> str:
        """Generate CSS custom properties from design tokens."""
        return f"""
        :root {{
            /* Colors */
            --color-primary: {self.tokens.primary};
            --color-secondary: {self.tokens.secondary};
            --color-accent: {self.tokens.accent};
            --color-success: {self.tokens.success};
            --color-warning: {self.tokens.warning};
            --color-error: {self.tokens.error};
            --color-info: {self.tokens.info};
            --color-background: {self.tokens.background};
            --color-surface: {self.tokens.surface};
            --color-text-primary: {self.tokens.text_primary};
            --color-text-secondary: {self.tokens.text_secondary};
            --color-text-muted: {self.tokens.text_muted};
            --color-border: {self.tokens.border};
            --color-border-light: {self.tokens.border_light};

            /* Typography */
            --font-family: {self.tokens.font_family};
            --font-size-base: {self.tokens.font_size_base};
            --font-size-small: {self.tokens.font_size_small};
            --font-size-large: {self.tokens.font_size_large};
            --font-size-xl: {self.tokens.font_size_xl};
            --font-weight-normal: {self.tokens.font_weight_normal};
            --font-weight-medium: {self.tokens.font_weight_medium};
            --font-weight-bold: {self.tokens.font_weight_bold};

            /* Spacing */
            --spacing-xs: {self.tokens.spacing_xs};
            --spacing-sm: {self.tokens.spacing_sm};
            --spacing-md: {self.tokens.spacing_md};
            --spacing-lg: {self.tokens.spacing_lg};
            --spacing-xl: {self.tokens.spacing_xl};

            /* Border Radius */
            --radius-small: {self.tokens.radius_small};
            --radius-medium: {self.tokens.radius_medium};
            --radius-large: {self.tokens.radius_large};

            /* Shadows */
            --shadow-small: {self.tokens.shadow_small};
            --shadow-medium: {self.tokens.shadow_medium};
            --shadow-large: {self.tokens.shadow_large};

            /* Transitions */
            --transition-fast: {self.tokens.transition_fast};
            --transition-medium: {self.tokens.transition_medium};
            --transition-slow: {self.tokens.transition_slow};
        }}
        """

    def inject_global_styles(self):
        """Inject global styles into Streamlit app."""
        st.markdown(f"""
        <style>
        {self.get_css_variables()}

        /* Global Styles */
        .stApp {{
            font-family: var(--font-family);
            background-color: var(--color-background);
            color: var(--color-text-primary);
        }}

        /* Streamlit Component Overrides */
        .stSelectbox > div > div {{
            border: 1px solid var(--color-border);
            border-radius: var(--radius-medium);
        }}

        .stTextInput > div > div > input {{
            border: 1px solid var(--color-border);
            border-radius: var(--radius-medium);
            font-family: var(--font-family);
        }}

        .stButton > button {{
            border-radius: var(--radius-medium);
            font-weight: var(--font-weight-medium);
            transition: var(--transition-fast);
            font-family: var(--font-family);
        }}

        .stButton > button:hover {{
            transform: translateY(-1px);
            box-shadow: var(--shadow-medium);
        }}

        /* Card Components */
        .design-card {{
            background: var(--color-surface);
            border: 1px solid var(--color-border-light);
            border-radius: var(--radius-medium);
            padding: var(--spacing-lg);
            box-shadow: var(--shadow-small);
            transition: var(--transition-medium);
        }}

        .design-card:hover {{
            box-shadow: var(--shadow-medium);
            border-color: var(--color-border);
        }}

        /* Typography */
        .design-title {{
            font-size: var(--font-size-xl);
            font-weight: var(--font-weight-bold);
            color: var(--color-text-primary);
            margin-bottom: var(--spacing-md);
        }}

        .design-subtitle {{
            font-size: var(--font-size-large);
            font-weight: var(--font-weight-medium);
            color: var(--color-text-secondary);
            margin-bottom: var(--spacing-sm);
        }}

        .design-body {{
            font-size: var(--font-size-base);
            color: var(--color-text-primary);
            line-height: 1.6;
        }}

        .design-caption {{
            font-size: var(--font-size-small);
            color: var(--color-text-muted);
            font-style: italic;
        }}

        /* Status Indicators */
        .status-success {{
            color: var(--color-success);
            background-color: rgba(16, 185, 129, 0.1);
            border: 1px solid var(--color-success);
            border-radius: var(--radius-small);
            padding: var(--spacing-xs) var(--spacing-sm);
        }}

        .status-warning {{
            color: var(--color-warning);
            background-color: rgba(245, 158, 11, 0.1);
            border: 1px solid var(--color-warning);
            border-radius: var(--radius-small);
            padding: var(--spacing-xs) var(--spacing-sm);
        }}

        .status-error {{
            color: var(--color-error);
            background-color: rgba(239, 68, 68, 0.1);
            border: 1px solid var(--color-error);
            border-radius: var(--radius-small);
            padding: var(--spacing-xs) var(--spacing-sm);
        }}

        /* Layout Utilities */
        .flex-row {{
            display: flex;
            flex-direction: row;
            gap: var(--spacing-md);
        }}

        .flex-col {{
            display: flex;
            flex-direction: column;
            gap: var(--spacing-sm);
        }}

        .center {{
            display: flex;
            justify-content: center;
            align-items: center;
        }}

        .space-between {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        /* Responsive Design */
        @media (max-width: 768px) {{
            .design-card {{
                padding: var(--spacing-md);
            }}

            .flex-row {{
                flex-direction: column;
            }}
        }}
        </style>
        """, unsafe_allow_html=True)
```

### 2. Component Library

```python
"""
Reusable component library with consistent styling
"""

from typing import Any, Dict, List, Optional, Union, Callable
import streamlit as st
from dataclasses import dataclass
from enum import Enum


class ButtonVariant(Enum):
    """Button style variants."""
    PRIMARY = "primary"
    SECONDARY = "secondary"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    GHOST = "ghost"


class AlertType(Enum):
    """Alert type variants."""
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"


@dataclass
class ComponentProps:
    """Base component properties."""
    className: Optional[str] = None
    style: Optional[Dict[str, str]] = None
    disabled: bool = False


class UIComponents:
    """Consistent UI component library for Streamlit."""

    def __init__(self, design_system: DesignSystem):
        self.design = design_system

    def card(
        self,
        title: Optional[str] = None,
        content: Optional[str] = None,
        actions: Optional[List[Dict[str, Any]]] = None,
        variant: str = "default",
        **props: ComponentProps
    ):
        """Professional card component with consistent styling."""

        card_classes = f"design-card card-{variant}"
        if props.get('className'):
            card_classes += f" {props['className']}"

        card_html = f'<div class="{card_classes}">'

        if title:
            card_html += f'<div class="design-title">{title}</div>'

        if content:
            card_html += f'<div class="design-body">{content}</div>'

        card_html += '</div>'

        st.markdown(card_html, unsafe_allow_html=True)

        # Render actions if provided
        if actions:
            cols = st.columns(len(actions))
            for i, action in enumerate(actions):
                with cols[i]:
                    if action.get('type') == 'button':
                        st.button(
                            action['label'],
                            key=action.get('key'),
                            on_click=action.get('on_click')
                        )

    def button(
        self,
        label: str,
        variant: ButtonVariant = ButtonVariant.PRIMARY,
        size: ComponentSize = ComponentSize.MEDIUM,
        disabled: bool = False,
        on_click: Optional[Callable] = None,
        **kwargs
    ) -> bool:
        """Enhanced button component with design system integration."""

        # Generate button styles based on variant
        button_styles = {
            ButtonVariant.PRIMARY: {
                'background': self.design.tokens.accent,
                'color': 'white',
                'border': f'1px solid {self.design.tokens.accent}',
            },
            ButtonVariant.SECONDARY: {
                'background': 'transparent',
                'color': self.design.tokens.accent,
                'border': f'1px solid {self.design.tokens.accent}',
            },
            ButtonVariant.SUCCESS: {
                'background': self.design.tokens.success,
                'color': 'white',
                'border': f'1px solid {self.design.tokens.success}',
            },
            ButtonVariant.WARNING: {
                'background': self.design.tokens.warning,
                'color': 'white',
                'border': f'1px solid {self.design.tokens.warning}',
            },
            ButtonVariant.ERROR: {
                'background': self.design.tokens.error,
                'color': 'white',
                'border': f'1px solid {self.design.tokens.error}',
            },
            ButtonVariant.GHOST: {
                'background': 'transparent',
                'color': self.design.tokens.text_primary,
                'border': '1px solid transparent',
            }
        }

        size_styles = {
            ComponentSize.SMALL: {'padding': f'{self.design.tokens.spacing_xs} {self.design.tokens.spacing_sm}'},
            ComponentSize.MEDIUM: {'padding': f'{self.design.tokens.spacing_sm} {self.design.tokens.spacing_md}'},
            ComponentSize.LARGE: {'padding': f'{self.design.tokens.spacing_md} {self.design.tokens.spacing_lg}'},
        }

        style = {**button_styles[variant], **size_styles[size]}

        # Inject button-specific styles
        button_key = f"btn_{hash(label)}_{variant.value}_{size.value}"
        st.markdown(f"""
        <style>
        div[data-testid="stButton"] > button[kind="primary"].{button_key} {{
            background: {style['background']} !important;
            color: {style['color']} !important;
            border: {style['border']} !important;
            padding: {style['padding']} !important;
            border-radius: {self.design.tokens.radius_medium} !important;
            font-weight: {self.design.tokens.font_weight_medium} !important;
            transition: {self.design.tokens.transition_fast} !important;
        }}
        </style>
        """, unsafe_allow_html=True)

        return st.button(
            label,
            disabled=disabled,
            on_click=on_click,
            key=kwargs.get('key', button_key),
            **kwargs
        )

    def alert(
        self,
        message: str,
        alert_type: AlertType = AlertType.INFO,
        dismissible: bool = False,
        key: Optional[str] = None
    ):
        """Alert component with consistent styling."""

        type_styles = {
            AlertType.INFO: {
                'background': f'rgba(6, 182, 212, 0.1)',
                'border': f'1px solid {self.design.tokens.info}',
                'color': self.design.tokens.info,
                'icon': 'ℹ️'
            },
            AlertType.SUCCESS: {
                'background': f'rgba(16, 185, 129, 0.1)',
                'border': f'1px solid {self.design.tokens.success}',
                'color': self.design.tokens.success,
                'icon': '✅'
            },
            AlertType.WARNING: {
                'background': f'rgba(245, 158, 11, 0.1)',
                'border': f'1px solid {self.design.tokens.warning}',
                'color': self.design.tokens.warning,
                'icon': '⚠️'
            },
            AlertType.ERROR: {
                'background': f'rgba(239, 68, 68, 0.1)',
                'border': f'1px solid {self.design.tokens.error}',
                'color': self.design.tokens.error,
                'icon': '❌'
            }
        }

        style = type_styles[alert_type]

        alert_html = f"""
        <div style="
            background: {style['background']};
            border: {style['border']};
            color: {style['color']};
            padding: {self.design.tokens.spacing_md};
            border-radius: {self.design.tokens.radius_medium};
            margin: {self.design.tokens.spacing_sm} 0;
            display: flex;
            align-items: center;
            gap: {self.design.tokens.spacing_sm};
        ">
            <span style="font-size: 1.2em;">{style['icon']}</span>
            <span>{message}</span>
        </div>
        """

        st.markdown(alert_html, unsafe_allow_html=True)

    def metric_card(
        self,
        title: str,
        value: Union[str, int, float],
        change: Optional[str] = None,
        change_type: Optional[str] = None,
        description: Optional[str] = None
    ):
        """Professional metric card component."""

        change_color = self.design.tokens.text_muted
        change_icon = ""

        if change and change_type:
            if change_type == "positive":
                change_color = self.design.tokens.success
                change_icon = "↗️"
            elif change_type == "negative":
                change_color = self.design.tokens.error
                change_icon = "↘️"

        metric_html = f"""
        <div class="design-card" style="text-align: center;">
            <div class="design-caption" style="margin-bottom: {self.design.tokens.spacing_xs};">
                {title}
            </div>
            <div style="
                font-size: 2rem;
                font-weight: {self.design.tokens.font_weight_bold};
                color: {self.design.tokens.text_primary};
                margin-bottom: {self.design.tokens.spacing_xs};
            ">
                {value}
            </div>
            {f'<div style="color: {change_color}; font-size: {self.design.tokens.font_size_small};">{change_icon} {change}</div>' if change else ''}
            {f'<div class="design-caption" style="margin-top: {self.design.tokens.spacing_xs};">{description}</div>' if description else ''}
        </div>
        """

        st.markdown(metric_html, unsafe_allow_html=True)

    def progress_bar(
        self,
        value: float,
        max_value: float = 100.0,
        label: Optional[str] = None,
        show_percentage: bool = True,
        color: Optional[str] = None
    ):
        """Custom progress bar with design system integration."""

        percentage = (value / max_value) * 100
        bar_color = color or self.design.tokens.accent

        progress_html = f"""
        <div style="margin: {self.design.tokens.spacing_sm} 0;">
            {f'<div class="design-caption" style="margin-bottom: {self.design.tokens.spacing_xs};">{label}</div>' if label else ''}
            <div style="
                background: {self.design.tokens.border_light};
                border-radius: {self.design.tokens.radius_large};
                height: 8px;
                overflow: hidden;
            ">
                <div style="
                    background: {bar_color};
                    height: 100%;
                    width: {percentage}%;
                    transition: {self.design.tokens.transition_medium};
                    border-radius: {self.design.tokens.radius_large};
                "></div>
            </div>
            {f'<div class="design-caption" style="text-align: right; margin-top: {self.design.tokens.spacing_xs};">{percentage:.1f}%</div>' if show_percentage else ''}
        </div>
        """

        st.markdown(progress_html, unsafe_allow_html=True)

    def data_table(
        self,
        data: List[Dict[str, Any]],
        columns: Optional[List[Dict[str, str]]] = None,
        searchable: bool = True,
        sortable: bool = True
    ):
        """Enhanced data table with design system styling."""

        if not data:
            self.alert("No data to display", AlertType.INFO)
            return

        # If columns not provided, infer from first row
        if not columns:
            columns = [{'key': key, 'title': key.replace('_', ' ').title()} for key in data[0].keys()]

        # Add search functionality if enabled
        search_term = ""
        if searchable:
            search_term = st.text_input("Search...", key="table_search")
            if search_term:
                data = [
                    row for row in data
                    if any(search_term.lower() in str(value).lower() for value in row.values())
                ]

        # Create table HTML
        table_html = f"""
        <div style="
            border: 1px solid {self.design.tokens.border};
            border-radius: {self.design.tokens.radius_medium};
            overflow: hidden;
            background: {self.design.tokens.surface};
        ">
            <table style="
                width: 100%;
                border-collapse: collapse;
                font-family: {self.design.tokens.font_family};
            ">
                <thead>
                    <tr style="
                        background: {self.design.tokens.primary};
                        color: white;
                    ">
        """

        for column in columns:
            table_html += f"""
                        <th style="
                            padding: {self.design.tokens.spacing_sm} {self.design.tokens.spacing_md};
                            text-align: left;
                            font-weight: {self.design.tokens.font_weight_medium};
                            font-size: {self.design.tokens.font_size_small};
                        ">
                            {column['title']}
                        </th>
            """

        table_html += """
                    </tr>
                </thead>
                <tbody>
        """

        for i, row in enumerate(data):
            row_bg = self.design.tokens.background if i % 2 == 0 else self.design.tokens.surface
            table_html += f"""
                    <tr style="
                        background: {row_bg};
                        border-bottom: 1px solid {self.design.tokens.border_light};
                    ">
            """

            for column in columns:
                value = row.get(column['key'], '')
                table_html += f"""
                        <td style="
                            padding: {self.design.tokens.spacing_sm} {self.design.tokens.spacing_md};
                            font-size: {self.design.tokens.font_size_small};
                            color: {self.design.tokens.text_primary};
                        ">
                            {value}
                        </td>
                """

            table_html += """
                    </tr>
            """

        table_html += """
                </tbody>
            </table>
        </div>
        """

        st.markdown(table_html, unsafe_allow_html=True)


# Layout Components
class LayoutComponents:
    """Layout utilities for consistent spacing and organization."""

    def __init__(self, design_system: DesignSystem):
        self.design = design_system

    def section(
        self,
        title: str,
        content: Optional[str] = None,
        collapsible: bool = False,
        expanded: bool = True
    ):
        """Consistent section component."""

        if collapsible:
            with st.expander(title, expanded=expanded):
                if content:
                    st.markdown(content)
                yield
        else:
            st.markdown(f'<div class="design-title">{title}</div>', unsafe_allow_html=True)
            if content:
                st.markdown(f'<div class="design-body">{content}</div>', unsafe_allow_html=True)
            yield

    def sidebar_section(self, title: str, content: Optional[str] = None):
        """Consistent sidebar section."""
        st.sidebar.markdown(f"### {title}")
        if content:
            st.sidebar.markdown(content)

    def two_column_layout(self, left_ratio: float = 0.5):
        """Two-column responsive layout."""
        left_col, right_col = st.columns([left_ratio, 1 - left_ratio])
        return left_col, right_col

    def three_column_layout(self):
        """Three-column responsive layout."""
        return st.columns(3)

    def grid_layout(self, items: List[Any], columns: int = 3):
        """Grid layout for multiple items."""
        cols = st.columns(columns)
        for i, item in enumerate(items):
            with cols[i % columns]:
                yield item, i
```

### 3. Project-Specific Components for EnterpriseHub GHL Real Estate AI

```python
"""
Project-specific components for GHL Real Estate AI
"""

class RealEstateUIComponents(UIComponents):
    """Real estate specific UI components."""

    def property_card(
        self,
        property_data: Dict[str, Any],
        show_actions: bool = True,
        compact: bool = False
    ):
        """Professional property display card."""

        # Extract property details
        address = property_data.get('address', 'Address not available')
        price = property_data.get('price', 0)
        bedrooms = property_data.get('bedrooms', 0)
        bathrooms = property_data.get('bathrooms', 0)
        sqft = property_data.get('square_feet', 0)
        status = property_data.get('status', 'available')
        image_url = property_data.get('image_url')

        # Format price
        formatted_price = f"${price:,.0f}" if price else "Price not available"

        # Status styling
        status_styles = {
            'available': {'color': self.design.tokens.success, 'bg': 'rgba(16, 185, 129, 0.1)'},
            'pending': {'color': self.design.tokens.warning, 'bg': 'rgba(245, 158, 11, 0.1)'},
            'sold': {'color': self.design.tokens.error, 'bg': 'rgba(239, 68, 68, 0.1)'},
        }

        status_style = status_styles.get(status.lower(), status_styles['available'])

        card_height = "300px" if compact else "400px"

        property_html = f"""
        <div class="design-card" style="
            height: {card_height};
            position: relative;
            overflow: hidden;
            padding: 0;
        ">
            {f'<div style="height: 50%; background: linear-gradient(to bottom, rgba(0,0,0,0.1), rgba(0,0,0,0.4)), url({image_url}); background-size: cover; background-position: center;"></div>' if image_url else ''}

            <div style="padding: {self.design.tokens.spacing_md};">
                <div style="
                    display: flex;
                    justify-content: space-between;
                    align-items: flex-start;
                    margin-bottom: {self.design.tokens.spacing_sm};
                ">
                    <div style="
                        font-size: {self.design.tokens.font_size_large};
                        font-weight: {self.design.tokens.font_weight_bold};
                        color: {self.design.tokens.text_primary};
                    ">
                        {formatted_price}
                    </div>
                    <div style="
                        background: {status_style['bg']};
                        color: {status_style['color']};
                        padding: {self.design.tokens.spacing_xs} {self.design.tokens.spacing_sm};
                        border-radius: {self.design.tokens.radius_small};
                        font-size: {self.design.tokens.font_size_small};
                        font-weight: {self.design.tokens.font_weight_medium};
                        text-transform: capitalize;
                    ">
                        {status}
                    </div>
                </div>

                <div style="
                    color: {self.design.tokens.text_secondary};
                    margin-bottom: {self.design.tokens.spacing_sm};
                    font-size: {self.design.tokens.font_size_small};
                ">
                    {address}
                </div>

                <div style="
                    display: flex;
                    gap: {self.design.tokens.spacing_lg};
                    color: {self.design.tokens.text_muted};
                    font-size: {self.design.tokens.font_size_small};
                ">
                    <span>🛏️ {bedrooms} bed</span>
                    <span>🚿 {bathrooms} bath</span>
                    <span>📐 {sqft:,} sqft</span>
                </div>
            </div>
        </div>
        """

        st.markdown(property_html, unsafe_allow_html=True)

        if show_actions and not compact:
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("View Details", key=f"view_{property_data.get('id')}"):
                    st.session_state[f"selected_property"] = property_data
            with col2:
                if st.button("Save", key=f"save_{property_data.get('id')}"):
                    # Handle save functionality
                    pass
            with col3:
                if st.button("Share", key=f"share_{property_data.get('id')}"):
                    # Handle share functionality
                    pass

    def lead_score_indicator(
        self,
        score: float,
        max_score: float = 100.0,
        label: str = "Lead Score",
        show_details: bool = True
    ):
        """Lead scoring indicator with visual representation."""

        percentage = (score / max_score) * 100

        # Determine color based on score
        if percentage >= 80:
            color = self.design.tokens.success
            status = "Hot"
        elif percentage >= 60:
            color = self.design.tokens.warning
            status = "Warm"
        elif percentage >= 40:
            color = "#fbbf24"  # Yellow-400
            status = "Lukewarm"
        else:
            color = self.design.tokens.error
            status = "Cold"

        score_html = f"""
        <div style="
            background: {self.design.tokens.surface};
            border: 1px solid {self.design.tokens.border};
            border-radius: {self.design.tokens.radius_medium};
            padding: {self.design.tokens.spacing_md};
            text-align: center;
        ">
            <div style="
                display: flex;
                justify-content: center;
                align-items: center;
                margin-bottom: {self.design.tokens.spacing_sm};
            ">
                <div style="
                    width: 80px;
                    height: 80px;
                    border-radius: 50%;
                    background: conic-gradient(
                        {color} {percentage * 3.6}deg,
                        {self.design.tokens.border_light} {percentage * 3.6}deg
                    );
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    position: relative;
                ">
                    <div style="
                        width: 60px;
                        height: 60px;
                        border-radius: 50%;
                        background: {self.design.tokens.surface};
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-weight: {self.design.tokens.font_weight_bold};
                        font-size: {self.design.tokens.font_size_base};
                        color: {color};
                    ">
                        {score:.0f}
                    </div>
                </div>
            </div>

            <div style="
                font-weight: {self.design.tokens.font_weight_medium};
                color: {self.design.tokens.text_primary};
                margin-bottom: {self.design.tokens.spacing_xs};
            ">
                {label}
            </div>

            <div style="
                color: {color};
                font-size: {self.design.tokens.font_size_small};
                font-weight: {self.design.tokens.font_weight_medium};
                background: rgba({color[1:3]}, {color[3:5]}, {color[5:7]}, 0.1);
                padding: {self.design.tokens.spacing_xs} {self.design.tokens.spacing_sm};
                border-radius: {self.design.tokens.radius_small};
                display: inline-block;
            ">
                {status} Lead
            </div>
        </div>
        """

        st.markdown(score_html, unsafe_allow_html=True)

    def ai_insight_panel(
        self,
        insights: List[Dict[str, Any]],
        title: str = "AI Insights"
    ):
        """AI insights panel with consistent styling."""

        st.markdown(f'<div class="design-subtitle">{title}</div>', unsafe_allow_html=True)

        for insight in insights:
            insight_type = insight.get('type', 'info')
            confidence = insight.get('confidence', 0)
            message = insight.get('message', '')

            # Map insight types to alert types
            type_mapping = {
                'recommendation': AlertType.INFO,
                'warning': AlertType.WARNING,
                'opportunity': AlertType.SUCCESS,
                'risk': AlertType.ERROR
            }

            alert_type = type_mapping.get(insight_type, AlertType.INFO)

            # Add confidence indicator
            confidence_text = f" (Confidence: {confidence:.0%})" if confidence > 0 else ""
            full_message = f"{message}{confidence_text}"

            self.alert(full_message, alert_type)

    def workflow_status_tracker(
        self,
        steps: List[Dict[str, Any]],
        current_step: int = 0
    ):
        """Workflow progress tracker component."""

        tracker_html = f"""
        <div style="
            background: {self.design.tokens.surface};
            border: 1px solid {self.design.tokens.border};
            border-radius: {self.design.tokens.radius_medium};
            padding: {self.design.tokens.spacing_lg};
        ">
        """

        for i, step in enumerate(steps):
            step_name = step.get('name', f'Step {i+1}')
            step_status = step.get('status', 'pending')

            # Determine step styling
            if i < current_step:
                step_color = self.design.tokens.success
                step_icon = "✅"
            elif i == current_step:
                step_color = self.design.tokens.accent
                step_icon = "🔄"
            else:
                step_color = self.design.tokens.text_muted
                step_icon = "⭕"

            is_last = i == len(steps) - 1

            tracker_html += f"""
            <div style="
                display: flex;
                align-items: center;
                margin-bottom: {'' if is_last else self.design.tokens.spacing_md};
            ">
                <div style="
                    width: 30px;
                    height: 30px;
                    border-radius: 50%;
                    background: {step_color};
                    color: white;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    margin-right: {self.design.tokens.spacing_md};
                    font-size: {self.design.tokens.font_size_small};
                ">
                    {step_icon}
                </div>
                <div style="
                    color: {step_color};
                    font-weight: {self.design.tokens.font_weight_medium};
                    font-size: {self.design.tokens.font_size_base};
                ">
                    {step_name}
                </div>
            </div>
            """

            # Add connector line
            if not is_last:
                tracker_html += f"""
                <div style="
                    width: 2px;
                    height: {self.design.tokens.spacing_md};
                    background: {self.design.tokens.border};
                    margin-left: 14px;
                    margin-bottom: {self.design.tokens.spacing_xs};
                "></div>
                """

        tracker_html += "</div>"

        st.markdown(tracker_html, unsafe_allow_html=True)
```

## Usage Examples

### Basic Setup
```python
# Initialize design system and components
design_system = DesignSystem(ColorScheme.PROFESSIONAL)
ui_components = UIComponents(design_system)
real_estate_ui = RealEstateUIComponents(design_system)

# Inject global styles
design_system.inject_global_styles()

# Use components
ui_components.alert("Welcome to the application!", AlertType.SUCCESS)

real_estate_ui.property_card({
    'id': 1,
    'address': '123 Main St, Rancho Cucamonga, CA',
    'price': 450000,
    'bedrooms': 3,
    'bathrooms': 2,
    'square_feet': 1800,
    'status': 'available'
})
```

## Best Practices

1. **Consistency**: Use design tokens for all styling decisions
2. **Accessibility**: Ensure sufficient color contrast and keyboard navigation
3. **Responsiveness**: Test components on different screen sizes
4. **Performance**: Minimize CSS injection and reuse styled components
5. **Maintainability**: Keep components modular and well-documented
6. **Brand Alignment**: Customize design tokens to match brand guidelines

This frontend design skill provides a comprehensive foundation for creating professional, consistent user interfaces across all Streamlit components in the EnterpriseHub GHL Real Estate AI project.