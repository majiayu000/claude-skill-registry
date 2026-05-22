---
name: cli-tool-development
description: Build polished CLI tools with Typer, Rich TUI components, and Python packaging
---

# CLI Tool Development

Typer app patterns, Rich TUI components, configuration handling, and packaging for distribution.

## CLI Framework Decision Table

| Complexity | Framework | Why |
|------------|-----------|-----|
| Single command, few options | `argparse` | Stdlib, zero deps, sufficient for scripts |
| Multi-command app, type hints | **Typer** | Auto-generates help from type hints, Click under the hood |
| Complex middleware, plugins | **Click** | Decorators, context passing, plugin groups |
| High-perf arg parsing only | `cyclopts` | Faster than Typer, similar API |
| Interactive wizard / forms | **Rich** + Typer | Prompts, panels, progress bars |
| Full TUI (ncurses-style) | `Textual` | Widget-based, reactive, from Rich team |

## Typer App Patterns

### Basic Structure

```python
import typer
from typing import Annotated, Optional
from pathlib import Path
from enum import Enum

app = typer.Typer(
    name="mytool",
    help="A polished CLI tool.",
    no_args_is_help=True,        # show help when no args given
    rich_markup_mode="rich",     # enable Rich formatting in help text
)

class OutputFormat(str, Enum):
    json = "json"
    table = "table"
    csv = "csv"

@app.command()
def process(
    input_file: Annotated[Path, typer.Argument(help="Input file path")],
    output: Annotated[Path, typer.Option("--output", "-o")] = Path("out.json"),
    verbose: Annotated[bool, typer.Option("--verbose", "-v")] = False,
    fmt: Annotated[OutputFormat, typer.Option("--format", "-f")] = OutputFormat.table,
):
    """Process input data and write results."""
    if not input_file.exists():
        typer.echo(f"Error: {input_file} not found", err=True)
        raise typer.Exit(code=1)
```

### Subgroups and Callbacks

```python
db_app = typer.Typer(help="Database operations")

@db_app.command()
def migrate(
    revision: Annotated[str, typer.Argument()] = "head",
    dry_run: Annotated[bool, typer.Option("--dry-run")] = False,
):
    """Run database migrations."""
    ...

app = typer.Typer()
app.add_typer(db_app, name="db")  # mytool db migrate

@app.callback()
def main(
    ctx: typer.Context,
    config: Annotated[Path, typer.Option("--config", "-c")] = Path("~/.mytool.toml"),
    debug: Annotated[bool, typer.Option("--debug")] = False,
):
    """Global options applied before any command."""
    ctx.ensure_object(dict)
    ctx.obj["debug"] = debug
    ctx.obj["config"] = load_config(config.expanduser())
```

## Rich TUI Components

### Tables and Progress

```python
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

console = Console()

def show_results(items: list[dict]):
    table = Table(title="Results", show_lines=False)
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Name", style="green")
    table.add_column("Status", justify="center")
    for item in items:
        status = "[bold red]FAIL[/]" if item["failed"] else "[green]OK[/]"
        table.add_row(str(item["id"]), item["name"], status)
    console.print(table)

def process_files(files: list[Path]):
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("{task.completed}/{task.total}"),
    ) as progress:
        task = progress.add_task("Processing...", total=len(files))
        for f in files:
            do_work(f)
            progress.update(task, advance=1)
```

### Live Display, Prompts, and Tree

```python
from rich.live import Live
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.tree import Tree

def monitor(stream):
    with Live(Panel("Starting..."), refresh_per_second=4) as live:
        for event in stream:
            live.update(Panel(f"[bold]{event.status}[/]\n{event.message}"))

name = Prompt.ask("Project name", default="my-project")
overwrite = Confirm.ask(f"[yellow]{name}[/] exists. Overwrite?", default=False)

def show_structure(root_path: Path):
    tree = Tree(f"[bold]{root_path.name}[/]")
    for child in sorted(root_path.iterdir()):
        if child.is_dir():
            branch = tree.add(f"[blue]{child.name}/[/]")
            for sub in sorted(child.iterdir()):
                branch.add(sub.name)
        else:
            tree.add(child.name)
    console.print(tree)
```

## Configuration File Handling

```python
import tomllib
from dataclasses import dataclass, field

@dataclass
class AppConfig:
    host: str = "localhost"
    port: int = 8080
    verbose: bool = False
    tags: list[str] = field(default_factory=list)

def load_config(paths: list[Path], overrides: dict | None = None) -> AppConfig:
    """Merge configs: defaults < file (lowest priority first) < CLI overrides."""
    merged: dict = {}
    for p in paths:
        if p.exists():
            with open(p, "rb") as f:
                merged |= tomllib.load(f)
    if overrides:
        merged |= {k: v for k, v in overrides.items() if v is not None}
    return AppConfig(**{k: v for k, v in merged.items() if k in AppConfig.__dataclass_fields__})
# Resolution: /etc/mytool/ < ~/.config/mytool/ < ./mytool.toml < CLI flags
```

## Packaging for PyPI

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "mytool"
version = "0.1.0"
description = "A polished CLI tool"
requires-python = ">=3.11"
license = "MIT"
dependencies = ["typer>=0.9", "rich>=13.0"]

[project.scripts]
mytool = "mytool.cli:app"

[tool.hatch.build.targets.wheel]
packages = ["src/mytool"]
```

### Homebrew Formula

```ruby
class Mytool < Formula
  desc "A polished CLI tool"
  homepage "https://github.com/user/mytool"
  url "https://files.pythonhosted.org/packages/.../mytool-0.1.0.tar.gz"
  sha256 "abc123..."
  license "MIT"
  depends_on "python@3.12"

  def install
    virtualenv_install_with_resources
  end

  test do
    assert_match "0.1.0", shell_output("#{bin}/mytool --version")
  end
end
```

### Version Command Pattern

```python
from importlib.metadata import version

def version_callback(value: bool):
    if value:
        typer.echo(f"mytool {version('mytool')}")
        raise typer.Exit()

@app.callback()
def main(
    version: Annotated[
        bool, typer.Option("--version", callback=version_callback, is_eager=True)
    ] = False,
):
    pass
```

## Gotchas

- **Typer requires `typing.Annotated`** for clean option/argument syntax. Without it, fall back to `typer.Option(default=...)` positional style.
- **`no_args_is_help=True`** belongs on the `Typer()` constructor, not on individual commands.
- **Rich markup in help text**: enable `rich_markup_mode="rich"` on Typer app, then use `[bold]`, `[green]` in docstrings.
- **Exit codes**: use `raise typer.Exit(code=1)` not `sys.exit()`. Typer catches `Exit` for cleanup.
- **`tomllib` is read-only** (stdlib, 3.11+). To write TOML, use `tomli-w`. For Python < 3.11, use `tomli`.
- **Config discovery**: follow XDG on Linux, `~/Library/Application Support/` on macOS. Use `platformdirs` for cross-platform.
- **Progress with unknown totals**: `progress.add_task("Working...", total=None)` for indeterminate spinner.
- **Entry points**: `project.scripts` maps CLI name to callable. Typer implements `__call__`, point directly to `app`.
- **Click compat**: access underlying Click command via `typer.main.get_command(app)` for advanced customization.
