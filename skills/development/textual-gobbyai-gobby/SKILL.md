---
name: textual
description: Build Python TUI applications using the Textual framework. Use this skill when the user asks to create terminal user interfaces, CLI dashboards, TUI apps, or interactive terminal applications in Python. Generates production-grade Textual code with proper structure, styling, and event handling.
---

# /textual - Python TUI Builder

Build sophisticated terminal user interfaces using the Textual framework. This skill guides creation of production-grade TUI applications with proper architecture, TCSS styling, event handling, and reactive patterns.

## When to Use

Invoke this skill when the user asks to:
- Build a terminal/TUI application in Python
- Create a CLI dashboard or interactive terminal interface
- Build a data viewer, form, file browser, or any TUI component
- Convert a CLI script to an interactive TUI

## Design Process

Before coding, understand the requirements:

1. **Purpose**: What does this TUI do? What problem does it solve?
2. **Users**: Who will use it? Developers? End users? Power users?
3. **Interactions**: What actions can users take? What data do they view/edit?
4. **Layout**: Single screen? Multiple screens? Modal dialogs?
5. **Data**: What data sources? Real-time updates? File I/O?

## Architecture Guidelines

### Project Structure

```
my_tui_app/
├── __init__.py
├── app.py              # Main App class
├── screens/            # Screen classes (if multi-screen)
│   ├── __init__.py
│   ├── main.py
│   └── settings.py
├── widgets/            # Custom widgets
│   ├── __init__.py
│   └── custom_widget.py
├── styles/             # TCSS stylesheets
│   └── app.tcss
└── __main__.py         # Entry point
```

For simple apps, a single file is acceptable.

### Core App Pattern

```python
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from textual.binding import Binding

class MyApp(App):
    """A Textual application."""

    CSS_PATH = "styles/app.tcss"  # External stylesheet
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("d", "toggle_dark", "Dark mode"),
        Binding("?", "show_help", "Help"),
    ]

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Header()
        # Your content here
        yield Footer()

    def on_mount(self) -> None:
        """Called when app is mounted."""
        pass

    def action_toggle_dark(self) -> None:
        """Toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

if __name__ == "__main__":
    MyApp().run()
```

## Widget Reference

### Layout Containers

```python
from textual.containers import (
    Container,      # Generic container
    Horizontal,     # Horizontal layout (flex row)
    Vertical,       # Vertical layout (flex column)
    Grid,           # CSS Grid layout
    ScrollableContainer,  # Scrollable content
    VerticalScroll, # Vertical scrolling
    HorizontalScroll,  # Horizontal scrolling
    Center,         # Center content
    Middle,         # Vertically center
)

# Example: Split layout
def compose(self) -> ComposeResult:
    with Horizontal():
        yield Sidebar(id="sidebar")
        with Vertical(id="main"):
            yield ContentArea()
            yield StatusBar()
```

### Common Widgets

```python
from textual.widgets import (
    # Text display
    Static,         # Static text/markup
    Label,          # Simple text label
    Markdown,       # Rendered markdown
    RichLog,        # Scrolling log output

    # Input
    Input,          # Text input field
    TextArea,       # Multi-line text editor

    # Selection
    Button,         # Clickable button
    Select,         # Dropdown selection
    SelectionList,  # Multi-select list
    RadioSet,       # Radio buttons
    RadioButton,    # Single radio button
    Checkbox,       # Checkbox
    Switch,         # Toggle switch

    # Data display
    DataTable,      # Tabular data
    Tree,           # Tree view
    DirectoryTree,  # File browser
    ListView,       # Vertical list
    ListItem,       # List item

    # Progress
    ProgressBar,    # Progress indicator
    LoadingIndicator,  # Spinner

    # Navigation
    Tabs,           # Tab container
    Tab,            # Single tab
    TabbedContent,  # Tabbed panels
    TabPane,        # Tab panel

    # Layout
    Header,         # App header
    Footer,         # App footer with bindings
    Rule,           # Horizontal/vertical rule
    Placeholder,    # Debug placeholder

    # Display
    Digits,         # Large digit display
    Sparkline,      # Mini chart
    Log,            # Append-only log
)
```

### Widget Variants

```python
# Button variants
Button("Primary", variant="primary")
Button("Success", variant="success")
Button("Warning", variant="warning")
Button("Error", variant="error")
Button("Default", variant="default")
Button("Disabled", disabled=True)

# Input validation
from textual.validation import Number, Length, Regex

Input(
    placeholder="Enter email",
    validators=[Regex(r"^[\w.-]+@[\w.-]+\.\w+$", "Invalid email")]
)
```

## TCSS Styling

Textual uses TCSS (Textual CSS), similar to web CSS:

### Common Properties

```css
/* Layout */
width: 100%;           /* Full width */
width: 50;             /* Fixed 50 cells */
width: 1fr;            /* Fraction of available */
width: auto;           /* Content-sized */
height: 100%;
min-width: 20;
max-height: 50%;

/* Spacing */
padding: 1 2;          /* Vertical Horizontal */
margin: 1;             /* All sides */
margin: 1 2 1 2;       /* Top Right Bottom Left */

/* Positioning */
dock: top;             /* top, bottom, left, right */
layer: above;          /* Layer ordering */
offset: 5 10;          /* X Y offset */

/* Flexbox */
layout: horizontal;    /* or vertical, grid */
align: center middle;  /* Horizontal Vertical */
content-align: center middle;

/* Grid */
layout: grid;
grid-size: 3 2;        /* Columns Rows */
grid-columns: 1fr 2fr; /* Column sizes */
grid-rows: auto 1fr;   /* Row sizes */
grid-gutter: 1;        /* Gap between cells */
column-span: 2;        /* Span columns */
row-span: 2;           /* Span rows */

/* Appearance */
background: $surface;  /* Use theme colors */
background: #1a1a2e;   /* Hex colors */
color: $text;
border: solid $primary;
border: round $accent;
border: double green;
border-title-align: center;

/* Text */
text-align: center;
text-style: bold italic;
content-align: center middle;

/* Scrolling */
overflow: auto;        /* auto, hidden, scroll */
overflow-x: hidden;
overflow-y: auto;

/* Visibility */
display: none;         /* Hide element */
visibility: hidden;    /* Hide but keep space */
opacity: 0.5;          /* Transparency */
```

### Selectors

```css
/* Type selector */
Button { ... }
DataTable { ... }

/* ID selector */
#sidebar { ... }
#main-content { ... }

/* Class selector */
.highlighted { ... }
.error-text { ... }

/* Pseudo-classes */
Button:hover { ... }
Button:focus { ... }
Button:disabled { ... }
Input:focus { ... }
ListItem.-selected { ... }  /* Note: dash prefix for component state */

/* Descendant */
#sidebar Button { ... }

/* Child */
Container > Static { ... }

/* Universal */
* { ... }
```

### Theme Colors

Use theme variables for consistency:

```css
background: $surface;
background: $surface-darken-1;
background: $surface-lighten-2;
color: $text;
color: $text-muted;
border: solid $primary;
border: solid $secondary;
border: solid $accent;
border: solid $success;
border: solid $warning;
border: solid $error;
background: $panel;
background: $boost;
```

### Example Stylesheet

```css
/* app.tcss */
Screen {
    background: $surface;
}

#sidebar {
    width: 30;
    dock: left;
    background: $panel;
    border-right: solid $primary;
    padding: 1;
}

#main {
    padding: 1 2;
}

.title {
    text-style: bold;
    color: $text;
    margin-bottom: 1;
}

DataTable {
    height: 1fr;
}

DataTable > .datatable--header {
    background: $primary;
    color: $text;
    text-style: bold;
}

DataTable > .datatable--cursor {
    background: $accent;
}

Button {
    margin: 1 0;
}

Button:focus {
    text-style: bold reverse;
}

Input {
    margin: 1 0;
}

Input:focus {
    border: tall $accent;
}

.error {
    color: $error;
    text-style: bold;
}

Footer {
    background: $primary-darken-2;
}
```

## Event Handling

### Message Handlers

```python
from textual.widgets import Button, Input, DataTable

class MyApp(App):
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle any button press."""
        if event.button.id == "submit":
            self.submit_form()
        elif event.button.id == "cancel":
            self.app.pop_screen()

    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle input text changes."""
        self.query_one("#preview", Static).update(event.value)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle Enter key in input."""
        self.process_input(event.value)

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        """Handle row selection in DataTable."""
        row = event.data_table.get_row(event.row_key)
        self.show_details(row)
```

### Decorator Syntax

```python
from textual import on

class MyApp(App):
    @on(Button.Pressed, "#submit")
    def handle_submit(self) -> None:
        """Handle submit button specifically."""
        self.submit_form()

    @on(Button.Pressed, "#cancel")
    def handle_cancel(self) -> None:
        """Handle cancel button."""
        self.app.pop_screen()

    @on(Input.Submitted, "#search")
    def handle_search(self, event: Input.Submitted) -> None:
        """Handle search input."""
        self.search(event.value)
```

### Custom Messages

```python
from textual.message import Message
from textual.widget import Widget

class SearchWidget(Widget):
    class SearchSubmitted(Message):
        """Emitted when search is submitted."""
        def __init__(self, query: str) -> None:
            self.query = query
            super().__init__()

    def submit_search(self, query: str) -> None:
        self.post_message(self.SearchSubmitted(query))

# Handle in parent
class MyApp(App):
    def on_search_widget_search_submitted(
        self, event: SearchWidget.SearchSubmitted
    ) -> None:
        self.perform_search(event.query)
```

## Reactive Attributes

```python
from textual.reactive import reactive, var

class MyWidget(Widget):
    # Reactive: triggers watch method and refresh
    count = reactive(0)

    # Var: no automatic refresh
    data = var([])

    def watch_count(self, old_value: int, new_value: int) -> None:
        """Called when count changes."""
        self.query_one("#counter", Static).update(str(new_value))

    def increment(self) -> None:
        self.count += 1  # Triggers watch_count
```

## Screens

### Basic Screens

```python
from textual.screen import Screen, ModalScreen

class SettingsScreen(Screen):
    """Settings screen."""

    BINDINGS = [("escape", "pop_screen", "Back")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Settings")
        # Settings content
        yield Footer()

class ConfirmDialog(ModalScreen[bool]):
    """Modal confirmation dialog."""

    def compose(self) -> ComposeResult:
        yield Grid(
            Label("Are you sure?", id="question"),
            Button("Yes", variant="success", id="yes"),
            Button("No", variant="error", id="no"),
            id="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(event.button.id == "yes")
```

### Screen Navigation

```python
class MyApp(App):
    SCREENS = {
        "settings": SettingsScreen,
        "help": HelpScreen,
    }

    def action_show_settings(self) -> None:
        self.push_screen("settings")

    def action_confirm_quit(self) -> None:
        def handle_response(confirmed: bool) -> None:
            if confirmed:
                self.exit()

        self.push_screen(ConfirmDialog(), handle_response)

    # Async version
    @work
    async def action_ask_question(self) -> None:
        result = await self.push_screen_wait(
            QuestionScreen("Continue?")
        )
        if result:
            self.notify("Continuing...")
```

## Workers (Async Operations)

```python
from textual import work
from textual.worker import Worker, get_current_worker

class MyApp(App):
    @work(exclusive=True)
    async def fetch_data(self, url: str) -> None:
        """Fetch data in background."""
        worker = get_current_worker()

        # Show loading state
        self.query_one("#status", Static).update("Loading...")

        async with httpx.AsyncClient() as client:
            if worker.is_cancelled:
                return
            response = await client.get(url)
            data = response.json()

        # Update UI (runs on main thread)
        if not worker.is_cancelled:
            self.display_data(data)

    def on_worker_state_changed(
        self, event: Worker.StateChanged
    ) -> None:
        """Handle worker state changes."""
        if event.state == WorkerState.ERROR:
            self.notify(f"Error: {event.worker.error}", severity="error")
```

## DataTable Patterns

```python
from textual.widgets import DataTable

class TableApp(App):
    def compose(self) -> ComposeResult:
        yield DataTable(id="table", cursor_type="row")
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)

        # Add columns with keys
        table.add_column("ID", key="id", width=8)
        table.add_column("Name", key="name", width=20)
        table.add_column("Status", key="status", width=12)

        # Add rows with keys (useful for updates)
        for item in self.data:
            table.add_row(
                item["id"],
                item["name"],
                item["status"],
                key=str(item["id"])
            )

        # Styling
        table.cursor_type = "row"  # row, cell, column
        table.zebra_stripes = True
        table.fixed_rows = 1  # Fixed header rows
        table.fixed_columns = 1  # Fixed left columns

    def update_row(self, row_id: str, new_data: dict) -> None:
        """Update a specific row."""
        table = self.query_one(DataTable)
        table.update_cell(row_id, "status", new_data["status"])

    def on_data_table_row_selected(
        self, event: DataTable.RowSelected
    ) -> None:
        """Handle row selection."""
        row = event.data_table.get_row(event.row_key)
        self.show_details(row)
```

## Form Patterns

```python
from textual.validation import Number, Length, Regex, ValidationResult, Validator

class EmailValidator(Validator):
    def validate(self, value: str) -> ValidationResult:
        if "@" in value and "." in value.split("@")[-1]:
            return self.success()
        return self.failure("Invalid email format")

class FormApp(App):
    CSS = """
    .form-field { margin: 1 0; }
    .error { color: $error; }
    """

    def compose(self) -> ComposeResult:
        yield Label("Name:", classes="form-field")
        yield Input(
            placeholder="Enter name",
            id="name",
            validators=[Length(minimum=2, maximum=50)]
        )

        yield Label("Email:", classes="form-field")
        yield Input(
            placeholder="email@example.com",
            id="email",
            validators=[EmailValidator()]
        )

        yield Label("Age:", classes="form-field")
        yield Input(
            placeholder="18",
            id="age",
            validators=[Number(minimum=0, maximum=150)]
        )

        yield Button("Submit", variant="primary", id="submit")
        yield Static("", id="errors", classes="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "submit":
            self.validate_and_submit()

    def validate_and_submit(self) -> None:
        errors = []

        for input_id in ["name", "email", "age"]:
            input_widget = self.query_one(f"#{input_id}", Input)
            if not input_widget.is_valid:
                errors.append(f"{input_id}: invalid")

        if errors:
            self.query_one("#errors", Static).update("\n".join(errors))
        else:
            self.submit_form()
```

## Complete Example: Dashboard App

```python
"""A complete dashboard TUI application."""

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import (
    Header, Footer, Static, DataTable,
    Button, Input, Label, RichLog, ProgressBar
)
from textual.binding import Binding
from textual.screen import ModalScreen
from textual import on, work

class DetailsDialog(ModalScreen[None]):
    """Show item details."""

    CSS = """
    DetailsDialog {
        align: center middle;
    }
    #dialog {
        width: 60;
        height: auto;
        border: thick $primary;
        background: $surface;
        padding: 1 2;
    }
    #dialog Label {
        margin: 1 0;
    }
    """

    def __init__(self, title: str, details: str) -> None:
        self.title_text = title
        self.details = details
        super().__init__()

    def compose(self) -> ComposeResult:
        with Container(id="dialog"):
            yield Label(self.title_text, classes="title")
            yield Static(self.details)
            yield Button("Close", variant="primary", id="close")

    @on(Button.Pressed, "#close")
    def close_dialog(self) -> None:
        self.dismiss()

class DashboardApp(App):
    """Main dashboard application."""

    CSS = """
    Screen {
        background: $surface;
    }

    #sidebar {
        width: 25;
        dock: left;
        background: $panel;
        border-right: solid $primary;
        padding: 1;
    }

    #sidebar Button {
        width: 100%;
        margin: 0 0 1 0;
    }

    #main {
        padding: 1 2;
    }

    #search-bar {
        height: 3;
        margin-bottom: 1;
    }

    #search-bar Input {
        width: 1fr;
    }

    #content {
        height: 1fr;
    }

    #table-area {
        height: 2fr;
        border: solid $primary;
    }

    #log-area {
        height: 1fr;
        border: solid $secondary;
        margin-top: 1;
    }

    #status-bar {
        height: 3;
        margin-top: 1;
    }

    .title {
        text-style: bold;
        color: $text;
        margin-bottom: 1;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("r", "refresh", "Refresh"),
        Binding("d", "toggle_dark", "Dark"),
        Binding("/", "focus_search", "Search"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()

        with Horizontal():
            # Sidebar
            with Container(id="sidebar"):
                yield Label("Dashboard", classes="title")
                yield Button("Overview", id="nav-overview", variant="primary")
                yield Button("Analytics", id="nav-analytics")
                yield Button("Settings", id="nav-settings")

            # Main content
            with Vertical(id="main"):
                # Search bar
                with Horizontal(id="search-bar"):
                    yield Input(placeholder="Search...", id="search")
                    yield Button("Go", id="search-btn")

                # Content area
                with Container(id="content"):
                    with Container(id="table-area"):
                        yield Label("Data", classes="title")
                        yield DataTable(id="data-table", cursor_type="row")

                    with Container(id="log-area"):
                        yield Label("Activity Log", classes="title")
                        yield RichLog(id="log", highlight=True)

                # Status bar
                with Horizontal(id="status-bar"):
                    yield ProgressBar(id="progress", total=100)
                    yield Static("Ready", id="status")

        yield Footer()

    def on_mount(self) -> None:
        """Initialize the app."""
        self.setup_table()
        self.log_message("Dashboard initialized")

    def setup_table(self) -> None:
        """Set up the data table."""
        table = self.query_one("#data-table", DataTable)
        table.add_column("ID", key="id", width=8)
        table.add_column("Name", key="name", width=20)
        table.add_column("Status", key="status", width=12)
        table.add_column("Updated", key="updated", width=16)

        # Sample data
        data = [
            ("001", "Server Alpha", "Online", "2024-01-15"),
            ("002", "Server Beta", "Offline", "2024-01-14"),
            ("003", "Database Primary", "Online", "2024-01-15"),
            ("004", "Cache Node", "Warning", "2024-01-15"),
        ]

        for row in data:
            table.add_row(*row, key=row[0])

        table.zebra_stripes = True

    def log_message(self, message: str) -> None:
        """Add message to the log."""
        log = self.query_one("#log", RichLog)
        log.write(f"[dim]{self.get_time()}[/dim] {message}")

    def get_time(self) -> str:
        """Get current time string."""
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")

    @on(Button.Pressed, "#nav-overview")
    @on(Button.Pressed, "#nav-analytics")
    @on(Button.Pressed, "#nav-settings")
    def handle_nav(self, event: Button.Pressed) -> None:
        """Handle navigation button clicks."""
        # Update button states
        for btn in self.query("#sidebar Button"):
            btn.variant = "default"
        event.button.variant = "primary"

        nav = event.button.id.replace("nav-", "")
        self.log_message(f"Navigated to {nav}")

    @on(DataTable.RowSelected)
    def handle_row_select(self, event: DataTable.RowSelected) -> None:
        """Handle table row selection."""
        row = event.data_table.get_row(event.row_key)
        self.push_screen(
            DetailsDialog(
                f"Details: {row[1]}",
                f"ID: {row[0]}\nStatus: {row[2]}\nUpdated: {row[3]}"
            )
        )

    @on(Input.Submitted, "#search")
    @on(Button.Pressed, "#search-btn")
    def handle_search(self) -> None:
        """Handle search."""
        query = self.query_one("#search", Input).value
        if query:
            self.log_message(f"Searching: {query}")
            self.perform_search(query)

    @work(exclusive=True)
    async def perform_search(self, query: str) -> None:
        """Perform search operation."""
        import asyncio

        progress = self.query_one("#progress", ProgressBar)
        status = self.query_one("#status", Static)

        status.update("Searching...")
        progress.update(progress=0)

        # Simulate search
        for i in range(100):
            await asyncio.sleep(0.02)
            progress.update(progress=i + 1)

        status.update(f"Found results for '{query}'")
        self.log_message(f"Search complete: {query}")

    def action_refresh(self) -> None:
        """Refresh data."""
        self.log_message("Refreshing data...")
        self.notify("Data refreshed")

    def action_toggle_dark(self) -> None:
        """Toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

    def action_focus_search(self) -> None:
        """Focus the search input."""
        self.query_one("#search", Input).focus()

if __name__ == "__main__":
    DashboardApp().run()
```

## Best Practices

1. **Separate Concerns**: Split TCSS into external files for larger apps
2. **Use Keys**: Always use keys for DataTable rows/columns for stable references
3. **Handle Errors**: Use workers for I/O and handle errors gracefully
4. **Keyboard First**: Define bindings for all major actions
5. **Theme Variables**: Use `$primary`, `$surface`, etc. for theme compatibility
6. **Type Hints**: Always use type hints for compose() and handlers
7. **Docstrings**: Document custom widgets and their messages
8. **Testing**: Use `textual.pilot` for app testing

## Running Textual Apps

```bash
# Run directly
python app.py

# Run with dev mode (auto-reload CSS)
textual run --dev app.py

# Run with console (debug output)
textual run --dev app.py
# Press Ctrl+P to toggle console

# Generate CSS documentation
textual colors  # Show theme colors
textual keys    # Show key bindings
```

## Dependencies

```bash
# Install textual
pip install textual

# With dev tools
pip install textual[dev]

# Common companions
pip install httpx  # Async HTTP
pip install rich   # Rich text (included with textual)
```

When implementing, analyze the codebase first to understand existing patterns, then generate production-ready Textual code that integrates well with the project structure.
