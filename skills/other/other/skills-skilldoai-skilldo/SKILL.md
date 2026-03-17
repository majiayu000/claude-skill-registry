---
name: rich
description: Terminal rendering library for styled text, tables, progress bars, prompts, markdown, syntax highlighting, and tracebacks.
version: 14.3.3
ecosystem: python
license: MIT
generated_with: gpt-5.2
---

## Imports

```python
import rich
from rich import print, print_json, inspect
from rich.console import Console, Group
from rich.prompt import Prompt, IntPrompt, FloatPrompt, Confirm
from rich.table import Table
from rich.progress import track
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich import traceback, pretty
```

## Core Patterns

### Styled printing with `rich.print` ✅ Current
```python
from rich import print

def main() -> None:
    print("Hello, [bold magenta]World[/]!")
    print("[green]OK[/] [dim](dim text)[/]")
    print("A whole line styled via markup, plus an emoji: [bold]Done[/] ✅")

if __name__ == "__main__":
    main()
```
* Use `from rich import print` as a drop-in replacement for built-in `print`.
* Inline styling uses Rich markup tags (BBCode-like), e.g. `[bold magenta]...[/]`.

### Use a shared `Console` for app-wide output ✅ Current
```python
from __future__ import annotations

from rich.console import Console
from rich.table import Table

def build_table() -> Table:
    table = Table(title="Build Summary")
    table.add_column("Step", style="bold")
    table.add_column("Status", justify="right")
    table.add_row("Lint", "[green]pass[/]")
    table.add_row("Tests", "[green]pass[/]")
    table.add_row("Package", "[yellow]skipped[/]")
    return table

def main() -> None:
    console = Console()
    console.print("Starting build...", style="bold cyan")
    console.print(build_table())
    console.log("Build finished", log_locals=False)

if __name__ == "__main__":
    main()
```
* Prefer a single `rich.console.Console` instance for consistent width/color/logging configuration.
* Use `console.print(..., style="...")` to style an entire renderable/line (and markup for parts).

### JSON pretty printing with `print_json` ✅ Current
```python
from __future__ import annotations

from rich import print_json

def main() -> None:
    payload: dict[str, object] = {
        "name": "example",
        "ok": True,
        "count": 3,
        "items": ["a", "b", "c"],
        "meta": {"source": "unit-test"},
    }
    print_json(data=payload, indent=2, highlight=True, sort_keys=True)

if __name__ == "__main__":
    main()
```
* `print_json(json=...)` prints a JSON string; `print_json(data=...)` encodes Python data then prints.
* Useful for debugging structured output with syntax highlighting.

### Progress over an iterable with `track` ✅ Current
```python
from __future__ import annotations

import time
from rich.progress import track

def main() -> None:
    for _ in track(range(50), description="Working..."):
        time.sleep(0.01)

if __name__ == "__main__":
    main()
```
* `rich.progress.track(sequence, description=...)` is the quick pattern for a single progress bar.

### Prompts with validation (`Prompt.ask`, `Confirm.ask`) ✅ Current
```python
from __future__ import annotations

from rich.prompt import Prompt, IntPrompt, Confirm

def main() -> None:
    name: str = Prompt.ask("Name", default="Ada")
    color: str = Prompt.ask(
        "Favorite color",
        choices=["red", "green", "blue"],
        default="green",
        case_sensitive=False,
    )
    age: int = IntPrompt.ask("Age", default=30)
    proceed: bool = Confirm.ask("Proceed?", default=True)

    from rich import print
    print(f"Hello [bold]{name}[/], age={age}, color={color}, proceed={proceed}")

if __name__ == "__main__":
    main()
```
* `Prompt.ask(..., choices=[...])` loops until valid input; set `case_sensitive=False` if desired.
* `Confirm.ask(...)` is for yes/no prompts; `IntPrompt` / `FloatPrompt` parse numeric input.

### Pretty printing with `pretty.pprint` ✅ Current
```python
from __future__ import annotations

from rich.pretty import pprint

def main() -> None:
    data = {
        "name": "example",
        "items": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "nested": {"foo": "bar", "baz": [True, False]},
    }
    
    # Basic pretty print
    pprint(data)
    
    # With max_length to truncate sequences/dicts
    pprint(data, max_length=3)
    
    # With max_string to truncate long strings
    pprint({"long": "Hello" * 50}, max_string=20)

if __name__ == "__main__":
    main()
```
* `pprint(obj, ...)` pretty prints objects with automatic layout and syntax highlighting.
* Use `max_length=N` to limit items shown in sequences/dicts; use `max_string=N` to truncate strings.
* Use `expand_all=True` to force multi-line layout even for small objects.

### Trees for hierarchical data ✅ Current
```python
from __future__ import annotations

from rich.tree import Tree
from rich.console import Console

def main() -> None:
    console = Console()
    
    tree = Tree("Project Root")
    tree.add("README.md")
    src = tree.add("src/", style="bold blue")
    src.add("main.py")
    src.add("utils.py")
    tree.add("tests/", style="bold green")
    
    console.print(tree)

if __name__ == "__main__":
    main()
```
* `Tree(label)` creates a tree structure for hierarchical data visualization.
* Use `.add(item, style=..., guide_style=...)` to add branches; returns a `Tree` for nesting.

### Columns for multi-column layout ✅ Current
```python
from __future__ import annotations

from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel

def main() -> None:
    console = Console()
    
    panels = [Panel(f"Item {i}", expand=True) for i in range(6)]
    columns = Columns(panels, equal=True, expand=True)
    
    console.print(columns)

if __name__ == "__main__":
    main()
```
* `Columns(renderables, ...)` arranges items in columns.
* Use `equal=True` for equal-width columns; `expand=True` to fill available width.
* Use `align="left"`, `"center"`, or `"right"` to control alignment.

## Configuration

- **Console configuration**
  - Prefer constructing a `Console()` and passing it through your app.
  - If you rely on Rich's global console, you can access it via:
    - `rich.get_console() -> Console`
    - `rich.reconfigure(*args, **kwargs) -> None` (reconfigures the global console)
- **Environment variables (behavior change in 14.0.0)**
  - `NO_COLOR`: if set to a **non-empty** value, disables color output; **empty** is treated as disabled (i.e., does not disable colors).
  - `FORCE_COLOR`: if set to a **non-empty** value, forces color output; **empty** is treated as disabled.
  - `UNICODE_VERSION`: control Unicode version used for cell width calculations (added in 14.3.0).
  - `TTY_COMPATIBLE`: override auto-detection of TTY support (added in 14.0.0).
- **Unicode width handling**
  - Rich has internal support for Unicode cell width tables; avoid relying on internal loaders.
  - If using `rich.cells.cell_len`, prefer keyword args (not positional), especially after signature changes in 14.3.0.
- **Pretty printing in REPL / IPython**
  - `rich.pretty.install()` enables pretty-printing in the Python REPL.
  - On 14.3.0+, IPython respects a `Console` passed to `pretty.install(console=...)`.

## Pitfalls

### Wrong: Using built-in `print` and expecting Rich markup to render
```python
def main() -> None:
    # Built-in print will output markup tags literally.
    print("Hello, [bold magenta]World[/]!")

if __name__ == "__main__":
    main()
```

### Right: Import `rich.print` (or use `Console.print`)
```python
from rich import print

def main() -> None:
    print("Hello, [bold magenta]World[/]!")

if __name__ == "__main__":
    main()
```

### Wrong: `Prompt.ask` choices are case-sensitive by default
```python
from rich.prompt import Prompt

def main() -> None:
    # User typing "paul" will be rejected.
    name = Prompt.ask(
        "Enter your name",
        choices=["Paul", "Jessica", "Duncan"],
        default="Paul",
    )
    from rich import print
    print(name)

if __name__ == "__main__":
    main()
```

### Right: Set `case_sensitive=False` when appropriate
```python
from rich.prompt import Prompt

def main() -> None:
    name = Prompt.ask(
        "Enter your name",
        choices=["Paul", "Jessica", "Duncan"],
        default="Paul",
        case_sensitive=False,
    )
    from rich import print
    print(name)

if __name__ == "__main__":
    main()
```

### Wrong: Passing multiple renderables where a single renderable is expected (e.g., `Panel`)
```python
from rich import print
from rich.panel import Panel

def main() -> None:
    # Panel expects a single renderable as its content.
    print(Panel("Hello", "World"))

if __name__ == "__main__":
    main()
```

### Right: Combine multiple renderables with `Group`
```python
from rich import print
from rich.console import Group
from rich.panel import Panel

def main() -> None:
    content = Group(
        "Hello",
        "World",
    )
    print(Panel(content, title="Greeting"))

if __name__ == "__main__":
    main()
```

### Wrong: Relying on exact traceback formatting in snapshot tests across versions
```python
from rich import traceback

def main() -> None:
    traceback.install()
    raise ValueError("boom")

if __name__ == "__main__":
    main()
```

### Right: Assert on stable substrings / exception types, not exact rendered frames
```python
from __future__ import annotations

from rich import traceback

def main() -> None:
    traceback.install()
    try:
        raise ValueError("boom")
    except ValueError as exc:
        # In tests, assert on message/type rather than exact terminal rendering.
        assert "boom" in str(exc)

if __name__ == "__main__":
    main()
```

### Wrong: Expecting empty environment variables to enable features
```python
from __future__ import annotations

import os

def main() -> None:
    # Empty NO_COLOR will NOT disable colors in Rich 14.0.0+
    os.environ["NO_COLOR"] = ""
    from rich import print
    print("[red]This will still be colored[/]")

if __name__ == "__main__":
    main()
```

### Right: Set environment variables to non-empty values
```python
from __future__ import annotations

import os

def main() -> None:
    # Set to non-empty value to disable colors
    os.environ["NO_COLOR"] = "1"
    from rich import print
    print("[red]This will not be colored[/]")

if __name__ == "__main__":
    main()
```

## References

- [Official Documentation](https://rich.readthedocs.io/)
- [GitHub Repository](https://github.com/Textualize/rich)

## Migration from v13.x

- **14.0.0: Environment variable semantics changed**
  - Empty `NO_COLOR` is now considered disabled (does not disable colors).
  - Empty `FORCE_COLOR` is now considered disabled (does not force colors).
  - Migration: ensure CI/container environments either unset these variables or set them to a non-empty value to activate behavior.

```python
from __future__ import annotations

import os
from rich.console import Console

def main() -> None:
    # Prefer explicit configuration over relying on possibly-empty env vars.
    os.environ.pop("NO_COLOR", None)
    os.environ.pop("FORCE_COLOR", None)
    console = Console()
    console.print("Color behavior is now consistent with env var semantics.")

if __name__ == "__main__":
    main()
```

- **14.0.0: Traceback rendering output changed**
  - Notes (Py3.11+), Exception Groups, and formatting differences may break snapshot tests.
  - Migration: update golden files or switch to assertions on stable content.

- **13.9.0: Python 3.7 dropped**
  - Migration: run on Python 3.8+ (or pin Rich < 13.9.0 if you must stay on 3.7).

- **14.3.0: `rich.cells.cell_len` signature changed**
  - Migration: prefer keyword arguments when calling `cell_len` to avoid positional mismatch.

- **14.3.0: IPython Console support**
  - `pretty.install(console=...)` now respects the Console instance in IPython environments.
  - Migration: if you pass a custom Console to `pretty.install()`, it will now be used in IPython.

- **14.3.0: Markdown styling changes**
  - Markdown headers, tables, and rules have updated styling.
  - New styles added: `markdown.table.header` and `markdown.table.border`.
  - Migration: review Markdown rendering output; customize styles if needed to match previous appearance.

## API Reference

- **rich.print(*objects, sep=" ", end="\\n", file=None, flush=False)** - Rich-enhanced print with markup rendering.
- **rich.print_json(json=None, *, data=None, indent=2, highlight=True, skip_keys=False, ensure_ascii=False, check_circular=True, allow_nan=True, default=None, sort_keys=False)** - Pretty-print JSON (string or data) with optional highlighting.
- **rich.inspect(obj, *, console=None, title=None, help=False, methods=False, docs=True, private=False, dunder=False, sort=True, all=False, value=True)** - Introspect and render object details to the console.
- **rich.get_console()** - Get the global `Console` instance used by top-level helpers.
- **rich.reconfigure(*args, **kwargs)** - Reconfigure the global `Console` (use sparingly; prefer explicit `Console()`).
- **rich.console.Console(...)** - Primary output object; controls width, color system, recording, etc.
- **rich.console.Console.print(*renderables, style=None, markup=True, highlight=None, emoji=True, ...)**
  - Print renderables (strings, Tables, Markdown, Syntax, Panels, etc.) with styling.
- **rich.console.Console.log(*objects, log_locals=False, ...)**
  - Log with timestamps and optional locals capture for debugging.
- **rich.console.Console.status(status, spinner="dots")**
  - Context manager for a live status spinner while work runs.
- **rich.console.Group(*renderables)** - Combine multiple renderables into one for containers expecting a single renderable.
- **rich.prompt.Prompt.ask(prompt, *, choices=None, default=None, case_sensitive=True, ...)**
  - Prompt for text input with optional validation and looping.
- **rich.prompt.IntPrompt.ask(...) / rich.prompt.FloatPrompt.ask(...)**
  - Prompt for numeric input with parsing and validation.
- **rich.prompt.Confirm.ask(prompt, *, default=False, ...)**
  - Prompt for yes/no input.
- **rich.table.Table(title=None, ...)** - Build tables for console rendering.
- **rich.table.Table.add_column(header, *, style=None, justify=None, ...) / Table.add_row(*cells, ...)**
  - Define columns and add rows.
- **rich.progress.track(sequence, description=None, total=None, ...)**
  - Iterate with a progress bar.
- **rich.markdown.Markdown(markdown_text)** - Render Markdown as a Rich renderable.
- **rich.syntax.Syntax(code, lexer, theme="monokai", line_numbers=False, ...)** - Render syntax-highlighted code.
- **rich.pretty.install(console=None, ...)**
  - Enable Rich pretty-printing in REPL/IPython contexts.
- **rich.pretty.pprint(obj, *, console=None, indent_guides=True, max_length=None, max_string=None, max_depth=None, expand_all=False, ...)**
  - Pretty print an object to the console with Rich formatting.
- **rich.pretty.pretty_repr(obj, *, max_width=80, indent_size=4, max_length=None, max_string=None, max_depth=None, expand_all=False, ...)**
  - Generate a pretty string representation of an object.
- **rich.traceback.install(...)**
  - Install Rich traceback handler (note output format changed in 14.0.0).
- **rich.tree.Tree(label, *, guide_style="tree.line", ...)**
  - Create a tree structure for hierarchical data.
- **rich.tree.Tree.add(label, *, style=None, guide_style=None, ...)**
  - Add a branch to the tree; returns a `Tree` for nesting.
- **rich.columns.Columns(renderables, *, equal=False, expand=False, align="left", ...)**
  - Arrange renderables in columns.
- **rich.filesize.decimal(size, *, precision=1, separator=" ")**
  - Format file size in decimal units (base 1000: bytes, kB, MB, etc.).