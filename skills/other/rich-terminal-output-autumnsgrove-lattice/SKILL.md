---
name: rich-terminal-output
description: Create beautiful terminal output with Rich library including tables, progress bars, panels, and syntax highlighting. Use when building CLI applications or enhancing terminal output in Python.
---

# Rich Terminal Output Skill

## When to Activate

Activate this skill when:
- Building CLI applications
- Displaying structured data (tables)
- Showing progress for long operations
- Creating error/status panels
- Pretty-printing objects for debugging
- Enhancing logging output

## Installation

```bash
uv add rich

# Quick test
python -c "from rich import print; print('[bold green]Rich working![/]')"
```

## Core Concepts

### Console Object

```python
from rich.console import Console

console = Console()

# Basic output
console.print("Hello, World!")

# Styled output
console.print("[bold red]Error:[/] Something went wrong")
console.print("[green]Success![/] Operation completed")
```

### Markup Syntax

```python
"[bold]Bold[/]"
"[italic]Italic[/]"
"[red]Red text[/]"
"[blue on white]Blue on white background[/]"
"[bold red]Combined styles[/]"
"[link=https://example.com]Click here[/]"
```

### Drop-in Print Replacement

```python
from rich import print

print("[bold cyan]Styled text[/]")
print({"key": "value"})  # Auto-pretty-prints
```

## Tables

```python
from rich.console import Console
from rich.table import Table

console = Console()

table = Table(title="User List")

table.add_column("ID", style="cyan", justify="right")
table.add_column("Name", style="magenta")
table.add_column("Email", style="green")
table.add_column("Status", justify="center")

table.add_row("1", "Alice", "alice@example.com", "✓ Active")
table.add_row("2", "Bob", "bob@example.com", "✓ Active")
table.add_row("3", "Charlie", "charlie@example.com", "✗ Inactive")

console.print(table)
```

## Panels

```python
from rich.console import Console
from rich.panel import Panel

console = Console()

# Simple panel
console.print(Panel("Operation completed!"))

# Styled panel
console.print(Panel(
    "[green]All tests passed![/]\n\n"
    "Total: 42 tests\n"
    "Time: 3.2s",
    title="Test Results",
    border_style="green"
))

# Error panel
console.print(Panel(
    "[red]Connection refused[/]\n\n"
    "Host: localhost:5432",
    title="[bold red]Error[/]",
    border_style="red"
))
```

## Progress Bars

### Simple Progress

```python
from rich.progress import track
import time

for item in track(range(100), description="Processing..."):
    time.sleep(0.01)
```

### Multiple Tasks

```python
from rich.progress import Progress

with Progress() as progress:
    task1 = progress.add_task("[red]Downloading...", total=100)
    task2 = progress.add_task("[green]Processing...", total=100)

    while not progress.finished:
        progress.update(task1, advance=0.9)
        progress.update(task2, advance=0.6)
        time.sleep(0.02)
```

## Syntax Highlighting

```python
from rich.console import Console
from rich.syntax import Syntax

console = Console()

code = '''
def hello():
    print("Hello, World!")
'''

syntax = Syntax(code, "python", theme="monokai", line_numbers=True)
console.print(syntax)
```

## Tree Displays

```python
from rich.console import Console
from rich.tree import Tree

console = Console()

tree = Tree("[bold blue]MyProject/[/]")
src = tree.add("[bold]src/[/]")
src.add("main.py")
src.add("config.py")

tests = tree.add("[bold]tests/[/]")
tests.add("test_main.py")

console.print(tree)
```

## Logging Integration

```python
import logging
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)]
)

logger = logging.getLogger("myapp")
logger.info("Application started")
logger.error("Connection failed")
```

## Pretty Tracebacks

```python
from rich.traceback import install

# Call once at startup
install(show_locals=True)

# All exceptions now have beautiful tracebacks
```

## Common Pitfalls

### Reuse Console Instance

```python
# ❌ Bad
def show(msg):
    Console().print(msg)  # Creates new instance each time

# ✅ Good
console = Console()
def show(msg):
    console.print(msg)
```

### Escape User Input

```python
from rich.markup import escape

username = "user[admin]"

# ❌ Bad - brackets break markup
console.print(f"[blue]{username}[/]")

# ✅ Good
console.print(f"[blue]{escape(username)}[/]")
```

### Handle Non-TTY

```python
import sys

console = Console(force_terminal=sys.stdout.isatty())
```

## CLI Application Pattern

```python
import click
from rich.console import Console
from rich.panel import Panel

console = Console()

@click.command()
@click.argument('filename')
def process(filename):
    console.print(f"[bold]Processing:[/] {filename}")

    with console.status("[bold green]Working..."):
        result = do_work(filename)

    if result.success:
        console.print(Panel(
            f"[green]Processed {result.count} items[/]",
            title="Success"
        ))
    else:
        console.print(f"[red]Error:[/] {result.error}")
```

## When NOT to Use Rich

- Non-interactive scripts (output piped)
- Server-side logging
- Performance-critical loops
- Minimal dependency requirements

## Related Resources

See `AgentUsage/rich_formatting.md` for complete documentation including:
- Advanced table customization
- Spinner and status displays
- Console recording
- Integration patterns
