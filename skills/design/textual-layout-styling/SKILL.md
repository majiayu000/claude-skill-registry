---
name: textual-layout-styling
description: |
  Style and layout Textual widgets using CSS-like syntax for responsive design.
  Use when implementing responsive layouts, CSS styling, color schemes, spacing, sizing,
  alignment, grid layouts, flexbox-like containers, and theme customization.
  Covers Textual's CSS pseudo-language and theming system.
allowed-tools: Read, Write, Edit, Bash
---

# Textual Layout and Styling

## Purpose
Master Textual's CSS-like styling system for building responsive, visually polished TUI applications. Textual styling supports CSS concepts adapted for terminal environments.

## Quick Start

```python
from textual.widgets import Static
from textual.containers import Container, Vertical, Horizontal

class StyledWidget(Container):
    """Widget with comprehensive styling."""

    CSS = """
    Screen {
        layout: vertical;
        background: $surface;
    }

    #header {
        height: 3;
        background: $boost;
        text-style: bold;
    }

    #content {
        height: 1fr;
        border: solid $primary;
        padding: 1;
    }

    #footer {
        height: auto;
        border-top: solid $primary;
        padding: 1;
    }
    """

    def compose(self) -> ComposeResult:
        """Compose layout."""
        yield Static("Header", id="header")
        yield Static("Content", id="content")
        yield Static("Footer", id="footer")
```

## Instructions

### Step 1: Understand Textual's CSS Properties

Learn the CSS properties available in Textual:

```python
# Layout properties
width: 100% | 50 | 1fr | auto
height: 100% | 10 | 1fr | auto
layout: vertical | horizontal | grid

# Spacing
padding: 1                      # All sides
padding: 1 2                    # Vertical Horizontal
padding: 1 2 3 4                # Top Right Bottom Left

margin: 1                       # All sides
margin: 1 2                     # Vertical Horizontal

# Borders
border: solid $primary          # border: {style} {color}
border-left: solid $primary
border-right: dashed $error
border-top: double $success
border-bottom: solid $warning
# Styles: solid, dashed, double, thick, tall, wide

# Background and foreground colors
background: $surface
color: $text
background: #ff0000 (hex)
color: rgb(255, 0, 0)

# Text styling
text-style: bold
text-style: italic
text-style: underline
text-style: bold italic underline
text-style: dim                 # Dimmed/faded

# Alignment
align: left | center | right
align-horizontal: left | center | right
align-vertical: top | middle | bottom
content-align: center middle    # Shorthand for both

# Opacity
opacity: 1.0                    # 0.0 (transparent) to 1.0 (opaque)

# Display
display: block | none           # Hide widget if 'none'

# Offset
offset: 1 2                     # x y offset from position

# Text overflow
text-overflow: fold | crop | ellipsis
overflow: auto | hidden         # x y overflow for containers

# Layers (stacking)
layer: overlay                  # Stacking order
z-index: 1                      # Numeric layer order
```

### Step 2: Define Inline CSS in Widgets

Add DEFAULT_CSS to widgets for styling:

```python
from textual.widgets import Static
from textual.containers import Vertical, Horizontal

class FormWidget(Vertical):
    """Form with styled fields."""

    DEFAULT_CSS = """
    FormWidget {
        height: auto;
        width: 50;
        border: solid $primary;
        padding: 1;
        background: $surface;
    }

    FormWidget > Static {
        width: 100%;
    }

    FormWidget .label {
        text-style: bold;
        color: $text;
        margin: 0 0 0 0;
    }

    FormWidget Input {
        width: 100%;
        height: 3;
        margin: 0 0 1 0;
    }

    FormWidget Button {
        width: 100%;
        margin-top: 1;
    }

    FormWidget Button:focus {
        background: $accent;
    }
    """

    def compose(self) -> ComposeResult:
        yield Static("Username", classes="label")
        yield Input(id="username")
        yield Static("Password", classes="label")
        yield Input(id="password", password=True)
        yield Button("Login")
```

**CSS Inline vs External:**
- `DEFAULT_CSS` - String in widget class
- Separate `.tcss` file - Can be loaded with `CSS_PATH = "file.tcss"`
- App-level `CSS` - In App class for global styles

### Step 3: Use Colors and Themes

Leverage Textual's color system:

```python
from textual.app import App

class ThemedApp(App):
    """App with colors and themes."""

    # Select theme
    THEME = "dracula"  # Built-in themes:
    # nord, dracula, monokai, solarized-dark,
    # solarized-light, one-dark, one-light, etc.

    CSS = """
    Screen {
        background: $surface;       # Surface color
        color: $text;               # Text color
    }

    .header {
        background: $boost;         # Boost (lighter surface)
        color: $text;
    }

    .success {
        color: $success;            # Green
    }

    .error {
        color: $error;              # Red
    }

    .warning {
        color: $warning;            # Yellow
    }

    .info {
        color: $info;               # Blue
    }

    .accent {
        color: $accent;             # Accent color
    }

    .primary {
        color: $primary;            # Primary color
        border: solid $primary;
    }

    .muted {
        color: $text-muted;         # Muted text
        text-style: dim;
    }
    """
```

**Color Variables:**
- `$primary` - Primary accent color
- `$secondary` - Secondary accent color
- `$accent` - Accent color
- `$success` - Success (green)
- `$error` - Error (red)
- `$warning` - Warning (yellow)
- `$info` - Info (blue)
- `$surface` - Background surface
- `$boost` - Lighter background
- `$panel` - Panel background
- `$text` - Primary text color
- `$text-muted` - Muted text

**Built-in Themes:**
- nord, dracula, monokai, solarized-dark, solarized-light
- one-dark, one-light, gruvbox, nord-deep
- Preview with demo app: `python -m textual`

### Step 4: Implement Responsive Layouts

Create layouts that adapt to window size:

```python
from textual.containers import Vertical, Horizontal, Container
from textual.widgets import Static

class ResponsiveLayout(Container):
    """Layout adapting to screen size."""

    CSS = """
    ResponsiveLayout {
        height: 100%;
        width: 100%;
    }

    ResponsiveLayout > Vertical {
        width: 1fr;
        height: 1fr;
    }

    ResponsiveLayout > Horizontal {
        width: 1fr;
        height: 1fr;
    }

    /* On small screens (< 80 columns) - stacked layout */
    @media (max-width: 80) {
        ResponsiveLayout {
            layout: vertical;
        }

        ResponsiveLayout > #sidebar {
            width: 100%;
            height: auto;
            border-bottom: solid $primary;
        }

        ResponsiveLayout > #content {
            width: 100%;
            height: 1fr;
        }
    }

    /* On large screens (>= 80 columns) - side-by-side layout */
    @media (min-width: 80) {
        ResponsiveLayout {
            layout: horizontal;
        }

        ResponsiveLayout > #sidebar {
            width: 25%;
            height: 100%;
            border-right: solid $primary;
        }

        ResponsiveLayout > #content {
            width: 75%;
            height: 100%;
        }
    }
    """

    def compose(self) -> ComposeResult:
        yield Vertical(
            Static("Sidebar", id="sidebar-title"),
            Static("Navigation items here"),
            id="sidebar",
        )
        yield Vertical(
            Static("Main content", id="content-title"),
            Static("Content area"),
            id="content",
        )
```

**Media Queries:**
```
@media (condition) {
    /* CSS rules for condition */
}

Conditions:
- (max-width: N)     - Maximum width in cells
- (min-width: N)     - Minimum width in cells
- (max-height: N)    - Maximum height in cells
- (min-height: N)    - Minimum height in cells
- (width: N)         - Exact width
- (height: N)        - Exact height
```

### Step 5: Create Grid Layouts

Use CSS Grid for complex layouts:

```python
from textual.containers import Container
from textual.widgets import Static

class GridLayout(Container):
    """Grid-based layout."""

    CSS = """
    GridLayout {
        layout: grid;
        grid-size: 3 3;             # 3 columns, 3 rows
        grid-gutter: 1 2;           # vertical horizontal gutter
        width: 100%;
        height: 100%;
    }

    GridLayout > Static {
        border: solid $primary;
        content-align: center middle;
    }

    #item1 { grid-column: 1; grid-row: 1; }
    #item2 { grid-column: 2; grid-row: 1; }
    #item3 { grid-column: 3; grid-row: 1; }
    #item4 { grid-column: 1 / 3; grid-row: 2; }  /* Span 2 columns */
    #item5 { grid-column: 3; grid-row: 2 / 4; }  /* Span 2 rows */
    """

    def compose(self) -> ComposeResult:
        for i in range(1, 6):
            yield Static(f"Item {i}", id=f"item{i}")
```

**Grid Properties:**
```
grid-size: cols rows            # Grid dimensions
grid-gutter: v h                # Space between items
grid-column: start [/ end]      # Column position/span
grid-row: start [/ end]         # Row position/span
```

### Step 6: Use Classes and Pseudo-Classes

Style variants with CSS classes:

```python
from textual.widgets import Button, Static

class VariantWidget(Static):
    """Widget with CSS class variants."""

    DEFAULT_CSS = """
    VariantWidget Button {
        margin: 0 1;
    }

    VariantWidget Button.primary {
        background: $primary;
        color: $text;
    }

    VariantWidget Button.success {
        background: $success;
        color: $text;
    }

    VariantWidget Button.danger {
        background: $error;
        color: $text;
    }

    VariantWidget Button:focus {
        background: $accent;
        text-style: bold;
    }

    VariantWidget Button:disabled {
        opacity: 0.5;
    }

    VariantWidget .muted {
        color: $text-muted;
        text-style: dim;
    }
    """

    def compose(self) -> ComposeResult:
        yield Button("Primary", classes="primary")
        yield Button("Success", classes="success")
        yield Button("Danger", classes="danger")
        yield Static("Muted text", classes="muted")

# Apply classes from Python
button = Button("Click me")
button.add_class("primary")      # Add class
button.remove_class("primary")   # Remove class
button.toggle_class("primary")   # Toggle class
button.has_class("primary")      # Check if has class
```

**Pseudo-Classes:**
```
:focus              - Widget has focus
:hover              - Mouse over (terminal dependent)
:disabled           - Widget is disabled
:dark               - Dark theme active
:light              - Light theme active
```

## Examples

### Example 1: Dashboard Layout with Styling

```python
from textual.app import App, ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Static, Header, Footer

class DashboardApp(App):
    """Styled dashboard application."""

    CSS = """
    Screen {
        layout: vertical;
        background: $surface;
    }

    Header {
        height: 1;
        background: $boost;
        dock: top;
    }

    Footer {
        height: auto;
        background: $boost;
        dock: bottom;
    }

    .main-container {
        height: 1fr;
        layout: horizontal;
        padding: 0;
    }

    .sidebar {
        width: 25%;
        height: 1fr;
        border-right: solid $primary;
        background: $boost;
        padding: 1;
    }

    .content {
        width: 75%;
        height: 1fr;
        padding: 1;
        overflow: auto;
    }

    .section-header {
        text-style: bold;
        color: $primary;
        margin: 1 0 0 0;
    }

    .stat-box {
        width: 1fr;
        height: auto;
        border: solid $primary;
        padding: 1;
        margin: 0 1 1 0;
    }

    .stat-value {
        color: $success;
        text-style: bold;
    }

    .stat-label {
        color: $text-muted;
        text-style: dim;
    }

    @media (max-width: 80) {
        .main-container {
            layout: vertical;
        }

        .sidebar {
            width: 100%;
            height: auto;
            border-right: none;
            border-bottom: solid $primary;
        }

        .content {
            width: 100%;
            height: 1fr;
        }
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()

        with Container(classes="main-container"):
            with Vertical(classes="sidebar"):
                yield Static("Navigation", classes="section-header")
                yield Static("● Dashboard")
                yield Static("● Agents")
                yield Static("● Settings")

            with Vertical(classes="content"):
                yield Static("Dashboard", classes="section-header")

                # Statistics grid
                yield Static("Stat 1\n", classes="stat-box")
                yield Static("Stat 2\n", classes="stat-box")

        yield Footer()
```

### Example 2: Form with Validation Styling

```python
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static, Input, Button, Label

class FormWidget(Vertical):
    """Styled form with validation feedback."""

    CSS = """
    FormWidget {
        width: 60;
        height: auto;
        border: solid $primary;
        padding: 1;
        background: $surface;
    }

    FormWidget .form-header {
        width: 100%;
        height: 3;
        content-align: center middle;
        background: $boost;
        text-style: bold;
        margin: 0 0 1 0;
    }

    FormWidget .form-field {
        width: 100%;
        margin: 0 0 1 0;
    }

    FormWidget .field-label {
        text-style: bold;
        color: $text;
        margin: 0 0 0 0;
        height: 1;
    }

    FormWidget Input {
        width: 100%;
        height: 3;
    }

    FormWidget .field-error {
        color: $error;
        text-style: dim;
        height: 1;
        display: none;      /* Hidden by default */
    }

    FormWidget Input.invalid {
        border: solid $error;
    }

    FormWidget Input.invalid ~ .field-error {
        display: block;     /* Show error when field invalid */
    }

    FormWidget .form-footer {
        width: 100%;
        height: auto;
        margin-top: 1;
        layout: horizontal;
    }

    FormWidget Button {
        width: 1fr;
        margin: 0 1 0 0;
    }

    FormWidget Button.submit {
        background: $success;
    }

    FormWidget Button.cancel {
        background: $error;
    }
    """

    def compose(self) -> ComposeResult:
        yield Static("Login", classes="form-header")

        with Vertical(classes="form-field"):
            yield Static("Email", classes="field-label")
            yield Input(id="email-input")
            yield Static("Invalid email address", classes="field-error")

        with Vertical(classes="form-field"):
            yield Static("Password", classes="field-label")
            yield Input(id="password-input", password=True)
            yield Static("Password too short", classes="field-error")

        with Horizontal(classes="form-footer"):
            yield Button("Login", classes="submit", variant="primary")
            yield Button("Cancel", classes="cancel")
```

## Requirements
- Textual >= 0.45.0 with CSS support
- Understanding of CSS concepts (width, height, padding, borders)

## CSS Best Practices

**1. Use CSS variables for consistency:**
```python
# ✅ GOOD - Uses theme colors
.header {
    background: $boost;
    color: $text;
    border: solid $primary;
}

# ❌ WRONG - Hardcoded colors
.header {
    background: #1e1e1e;
}
```

**2. Organize CSS logically:**
```python
CSS = """
/* Layout structure */
Screen { layout: vertical; }

/* Component styling */
.card { border: solid $primary; }

/* State variants */
.card.active { background: $boost; }

/* Responsive adjustments */
@media (max-width: 80) { }
"""
```

**3. Use responsive design:**
```python
# Avoid fixed widths that don't fit terminals
# ❌ WRONG
.sidebar { width: 30; }  # Too wide for small terminals

# ✅ CORRECT - Uses fraction units
.sidebar { width: 25%; }  # Responsive to screen size
```

## See Also
- [textual-widget-development.md](../textual-widget-development) - CSS in widgets
- [textual-app-lifecycle.md](../textual-app-lifecycle) - App-level styling
