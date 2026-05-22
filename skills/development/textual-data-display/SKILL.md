---
name: textual-data-display
description: |
  Display structured data in Textual using tables, lists, trees, and scrollable containers.
  Use when rendering data tables, building list views, displaying hierarchical data,
  scrolling large content, pagination, and efficient rendering of large datasets.
  Covers DataTable, ListView, Tree, and scrolling patterns.
allowed-tools: Read, Write, Edit, Bash
---

# Textual Data Display

## Purpose
Efficiently display and interact with structured data using Textual's data widgets. These widgets handle selection, scrolling, and large datasets with excellent performance.

## Quick Start

```python
from textual.widgets import DataTable, Static
from textual.app import ComposeResult

class TableWidget(Static):
    """Display data in a table."""

    def compose(self) -> ComposeResult:
        yield DataTable()

    async def on_mount(self) -> None:
        """Initialize table with data."""
        table = self.query_one(DataTable)

        # Add columns
        table.add_column("Name", key="name")
        table.add_column("Status", key="status")
        table.add_column("CPU %", key="cpu")

        # Add rows
        table.add_row("Agent-1", "Running", "45.2", key="agent-1")
        table.add_row("Agent-2", "Idle", "12.5", key="agent-2")
        table.add_row("Agent-3", "Running", "78.9", key="agent-3")
```

## Instructions

### Step 1: Use DataTable for Tabular Data

DataTable is the most powerful widget for structured data:

```python
from textual.widgets import DataTable
from textual.app import ComposeResult
from typing import Callable

class DataTableWidget(Static):
    """Widget for displaying tabular data."""

    def compose(self) -> ComposeResult:
        yield DataTable(id="data-table")

    async def on_mount(self) -> None:
        """Initialize table."""
        table = self.query_one("#data-table", DataTable)

        # Configure table
        table.show_header = True        # Show column headers
        table.show_row_labels = True    # Show row numbers
        table.fixed_rows = 1            # Fix header row

        # Add columns with optional width
        table.add_column("ID", key="id", width=8)
        table.add_column("Name", key="name", width=20)
        table.add_column("Status", key="status", width=15)
        table.add_column("Updated", key="updated", width=20)

        # Add rows
        data = [
            ("1", "Agent-1", "Running", "2024-01-15 10:30:45"),
            ("2", "Agent-2", "Idle", "2024-01-15 09:15:20"),
            ("3", "Agent-3", "Error", "2024-01-15 08:45:10"),
        ]

        for row_data in data:
            table.add_row(*row_data, key=row_data[0])

    async def get_selected_row(self) -> tuple | None:
        """Get currently selected row data.

        Returns:
            Tuple of row values or None if no selection.
        """
        table = self.query_one("#data-table", DataTable)

        if table.cursor_row is not None:
            row_key = table.cursor_row
            row = table.get_row(row_key)
            return row if row else None

        return None

    async def clear_table(self) -> None:
        """Clear all data rows (keeps header)."""
        table = self.query_one("#data-table", DataTable)
        table.clear()

    async def add_row(self, *values: str, key: str | None = None) -> None:
        """Add a row to table."""
        table = self.query_one("#data-table", DataTable)
        table.add_row(*values, key=key)

    async def update_row(self, row_key: str, *values: str) -> None:
        """Update existing row."""
        table = self.query_one("#data-table", DataTable)
        table.update_row(row_key, *values)
```

**DataTable Features:**
- Columns with optional widths and keys
- Row keys for easy lookup
- Cursor movement (up/down arrows)
- Single/multiple selection modes
- Sortable columns
- Fixed header rows
- Efficient rendering of large datasets

### Step 2: Handle DataTable Selection Events

Respond to user interactions:

```python
from textual.widgets import DataTable, Static
from textual import on

class SelectableTableWidget(Static):
    """Table with selection handling."""

    def compose(self) -> ComposeResult:
        yield DataTable(id="table")

    async def on_mount(self) -> None:
        """Initialize table."""
        table = self.query_one("#table", DataTable)
        table.add_column("Item")
        table.add_column("Value")

        for i in range(5):
            table.add_row(f"Item {i}", f"Value {i}", key=str(i))

    @on(DataTable.RowSelected)
    async def on_row_selected(self, event: DataTable.RowSelected) -> None:
        """Handle row selection."""
        row_key = event.cursor_row
        table = self.query_one("#table", DataTable)

        # Get row data
        row_data = table.get_row(row_key)
        self.app.notify(f"Selected: {row_data}")

    @on(DataTable.RowHighlighted)
    async def on_row_highlighted(self, event: DataTable.RowHighlighted) -> None:
        """Called as cursor moves (preview)."""
        row_key = event.cursor_row
        # Can use for hovering effects

    @on(DataTable.CellSelected)
    async def on_cell_selected(self, event: DataTable.CellSelected) -> None:
        """Handle specific cell selection."""
        row_key = event.cursor_row
        column_key = event.cursor_column
```

**DataTable Events:**
- `RowSelected` - Row clicked/selected
- `RowHighlighted` - Row cursor moved over
- `CellSelected` - Specific cell selected
- `CellHighlighted` - Cell cursor moved over

### Step 3: Use ListView for Simple Lists

For simple lists with less overhead:

```python
from textual.widgets import ListView, ListItem, Static
from textual.app import ComposeResult
from textual import on

class ListViewWidget(Static):
    """Simple list view."""

    def compose(self) -> ComposeResult:
        yield ListView(id="list")

    async def on_mount(self) -> None:
        """Populate list."""
        list_view = self.query_one("#list", ListView)

        items = ["Item 1", "Item 2", "Item 3", "Item 4"]

        for item_text in items:
            await list_view.append(
                ListItem(Static(item_text))
            )

    @on(ListView.Selected)
    async def on_item_selected(self, event: ListView.Selected) -> None:
        """Handle item selection."""
        selected_item = event.item
        index = event.selection_index

        self.app.notify(f"Selected item {index}")

    async def get_selected(self) -> str | None:
        """Get selected item."""
        list_view = self.query_one("#list", ListView)

        if list_view.index is not None:
            item = list(list_view.children)[list_view.index]
            if isinstance(item, ListItem):
                # Extract text from ListItem
                child = list(item.children)[0]
                if isinstance(child, Static):
                    return child.render_str()

        return None
```

**ListView vs DataTable:**
- `ListView` - Simpler, lighter weight, for lists of items
- `DataTable` - More powerful, columnar data, selection handling

### Step 4: Use Tree for Hierarchical Data

Display tree/nested structures:

```python
from textual.widgets import Tree, Static
from textual.app import ComposeResult
from textual import on

class TreeWidget(Static):
    """Display hierarchical data."""

    def compose(self) -> ComposeResult:
        tree = Tree("Root")
        tree.root.expand()

        # Add branches
        agents_branch = tree.root.add("Agents")
        agents_branch.add("Agent-1")
        agents_branch.add("Agent-2")
        agents_branch.add("Agent-3")

        settings_branch = tree.root.add("Settings")
        settings_branch.add("General")
        settings_branch.add("Advanced")
        settings_branch.add("About")

        yield tree

    @on(Tree.NodeSelected)
    async def on_node_selected(self, event: Tree.NodeSelected) -> None:
        """Handle node selection."""
        node = event.node
        label = node.label
        self.app.notify(f"Selected: {label}")

    @on(Tree.NodeExpanded)
    async def on_node_expanded(self, event: Tree.NodeExpanded) -> None:
        """Handle node expansion."""
        node = event.node
        # Load children on demand
        pass

    @on(Tree.NodeCollapsed)
    async def on_node_collapsed(self, event: Tree.NodeCollapsed) -> None:
        """Handle node collapse."""
        pass
```

**Tree Features:**
- Expandable/collapsible nodes
- Lazy loading with `NodeExpanded` event
- Node selection handling
- Hierarchical display with indentation

### Step 5: Implement Scrollable Containers

Create scrollable areas for large content:

```python
from textual.containers import VerticalScroll, HorizontalScroll
from textual.widgets import Static
from textual.app import ComposeResult

class ScrollableWidget(Static):
    """Widget with scrollable content."""

    DEFAULT_CSS = """
    ScrollableWidget VerticalScroll {
        height: 1fr;
        border: solid $primary;
    }
    """

    def compose(self) -> ComposeResult:
        """Create scrollable content area."""
        with VerticalScroll(id="scroll-area"):
            for i in range(100):
                yield Static(f"Line {i}: " + "x" * 50)

    async def on_mount(self) -> None:
        """Setup after mount."""
        scroll_area = self.query_one("#scroll-area", VerticalScroll)

        # Scroll to specific position
        scroll_area.scroll_to(y=50)

    async def scroll_to_bottom(self) -> None:
        """Scroll to bottom of content."""
        scroll_area = self.query_one("#scroll-area", VerticalScroll)
        scroll_area.scroll_end()

    async def scroll_to_top(self) -> None:
        """Scroll to top of content."""
        scroll_area = self.query_one("#scroll-area", VerticalScroll)
        scroll_area.scroll_home()

    async def append_line(self, text: str) -> None:
        """Append text and auto-scroll to bottom."""
        scroll_area = self.query_one("#scroll-area", VerticalScroll)
        line_num = len(list(scroll_area.children))
        await scroll_area.mount(Static(f"Line {line_num}: {text}"))
        scroll_area.scroll_end(animate=False)
```

**Scrolling Methods:**
- `scroll_to(y=N)` - Scroll to position
- `scroll_end()` - Scroll to bottom
- `scroll_home()` - Scroll to top
- `scroll_page_up()` / `scroll_page_down()` - Page scrolling
- `scroll_visible()` - Scroll to make widget visible

### Step 6: Handle Large Datasets Efficiently

Optimize rendering for thousands of items:

```python
import asyncio
from textual.widgets import DataTable, Static
from textual.app import ComposeResult

class LargeDatasetWidget(Static):
    """Efficiently handle large datasets."""

    DEFAULT_CSS = """
    LargeDatasetWidget DataTable {
        height: 1fr;
    }
    """

    def compose(self) -> ComposeResult:
        table = DataTable()
        table.add_column("ID", key="id", width=8)
        table.add_column("Data", key="data", width=40)
        yield table

    async def on_mount(self) -> None:
        """Lazy load data."""
        table = self.query_one(DataTable)

        # Load data in chunks to avoid blocking UI
        async def load_data() -> None:
            for chunk in range(0, 10000, 100):
                for i in range(chunk, min(chunk + 100, 10000)):
                    table.add_row(str(i), f"Data item {i}")

                # Yield to event loop every 100 rows
                await asyncio.sleep(0)

        self.app.run_worker(load_data())

    async def filter_rows(self, predicate: callable) -> None:
        """Filter table by predicate."""
        table = self.query_one(DataTable)

        # Get all rows
        rows_to_keep = []
        for row_key in list(table.row_keys):
            row_data = table.get_row(row_key)
            if predicate(row_data):
                rows_to_keep.append((row_key, row_data))

        # Rebuild table
        table.clear()
        for row_key, row_data in rows_to_keep:
            table.add_row(*row_data, key=row_key)
```

**Performance Tips:**
- Load data in chunks with `await asyncio.sleep(0)`
- Use row keys for efficient updates
- Avoid clearing/rebuilding entire table
- Use DataTable cursor for navigation (efficient)
- Lazy load TreeView nodes on expand

## Examples

### Example 1: Agent Status Table

```python
from textual.widgets import DataTable, Static
from textual.app import ComposeResult
from textual import on
from typing import Literal

class AgentStatusTable(Static):
    """Display agent status in a table."""

    DEFAULT_CSS = """
    AgentStatusTable {
        height: 1fr;
    }

    AgentStatusTable DataTable {
        height: 1fr;
    }

    AgentStatusTable .status-running {
        color: $success;
    }

    AgentStatusTable .status-idle {
        color: $warning;
    }

    AgentStatusTable .status-error {
        color: $error;
    }
    """

    def compose(self) -> ComposeResult:
        yield DataTable(id="agents-table")

    async def on_mount(self) -> None:
        """Initialize agent table."""
        table = self.query_one("#agents-table", DataTable)

        # Configure
        table.show_header = True
        table.show_row_labels = False

        # Add columns
        table.add_column("Agent ID", key="agent_id", width=15)
        table.add_column("Status", key="status", width=12)
        table.add_column("Tasks", key="tasks", width=8)
        table.add_column("CPU %", key="cpu", width=8)
        table.add_column("Memory %", key="memory", width=10)
        table.add_column("Updated", key="updated", width=20)

    async def add_agent(
        self,
        agent_id: str,
        status: Literal["idle", "running", "error"],
        tasks: int,
        cpu: float,
        memory: float,
        updated: str,
    ) -> None:
        """Add agent row."""
        table = self.query_one("#agents-table", DataTable)
        table.add_row(
            agent_id,
            status.upper(),
            str(tasks),
            f"{cpu:.1f}",
            f"{memory:.1f}",
            updated,
            key=agent_id,
        )

    async def update_agent(
        self,
        agent_id: str,
        status: Literal["idle", "running", "error"],
        tasks: int,
        cpu: float,
        memory: float,
        updated: str,
    ) -> None:
        """Update agent row."""
        table = self.query_one("#agents-table", DataTable)
        table.update_row(
            agent_id,
            agent_id,
            status.upper(),
            str(tasks),
            f"{cpu:.1f}",
            f"{memory:.1f}",
            updated,
        )

    @on(DataTable.RowSelected)
    async def on_agent_selected(self, event: DataTable.RowSelected) -> None:
        """Handle agent selection."""
        agent_id = event.cursor_row
        self.app.notify(f"Selected agent: {agent_id}")
```

### Example 2: Log Viewer with Scrolling

```python
from textual.containers import VerticalScroll
from textual.widgets import Static, RichLog
from textual.app import ComposeResult
from rich.console import Console
from rich.text import Text

class LogViewerWidget(Static):
    """Real-time log viewer."""

    DEFAULT_CSS = """
    LogViewerWidget {
        height: 1fr;
        border: solid $primary;
    }

    LogViewerWidget RichLog {
        height: 1fr;
        overflow-y: auto;
    }

    LogViewerWidget .log-header {
        height: 1;
        text-style: bold;
        background: $boost;
    }
    """

    def compose(self) -> ComposeResult:
        yield Static("Logs", classes="log-header")
        yield RichLog(id="log-output")

    async def add_log_line(self, message: str, level: str = "INFO") -> None:
        """Add a log line."""
        log = self.query_one("#log-output", RichLog)

        # Color by level
        color = {
            "DEBUG": "dim",
            "INFO": "blue",
            "WARNING": "yellow",
            "ERROR": "red",
        }.get(level, "default")

        text = Text(f"[{level}] {message}", style=color)
        log.write(text)

    async def clear_logs(self) -> None:
        """Clear all logs."""
        log = self.query_one("#log-output", RichLog)
        log.clear()
```

## Requirements
- Textual >= 0.45.0
- Rich (for advanced rendering)
- Python 3.9+

## Best Practices

**1. Choose the right widget:**
```python
# For columns/rows of data
DataTable()

# For simple lists
ListView()

# For hierarchical data
Tree()

# For text with scrolling
RichLog() or VerticalScroll()
```

**2. Lazy load large datasets:**
```python
# ❌ WRONG - blocks UI
for i in range(100000):
    table.add_row(...)

# ✅ CORRECT - yields to event loop
async def load():
    for i in range(100000):
        table.add_row(...)
        if i % 100 == 0:
            await asyncio.sleep(0)
```

**3. Use keys for efficient updates:**
```python
# ❌ WRONG - clears and rebuilds
table.clear()
table.add_row(...)

# ✅ CORRECT - updates specific row
table.update_row(key, ...)
```

## See Also
- [textual-widget-development.md](../textual-widget-development) - Widget basics
- [textual-event-messages.md](../textual-event-messages) - Event handling for tables/lists
- [textual-layout-styling.md](../textual-layout-styling) - Styling table appearance
