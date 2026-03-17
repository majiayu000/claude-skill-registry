---
name: cli-development
description: CLI tool development patterns - Click, Typer, argparse, output formatting, configuration files, and distribution. Auto-triggers when building command-line tools.
---

# CLI Development Skill

## Framework Selection

| Framework    | Best For                    | Pros                               | Cons                        |
| ------------ | --------------------------- | ---------------------------------- | --------------------------- |
| **Typer**    | Modern Python CLIs          | Type hints, auto-docs, Click-based | Requires Python 3.7+        |
| **Click**    | Complex CLIs                | Battle-tested, composable, plugins | More boilerplate than Typer |
| **argparse** | Simple scripts, stdlib only | No dependencies, always available  | Verbose, no auto-docs       |

## Typer (Recommended)

### Basic CLI

```python
import typer

app = typer.Typer(help="My awesome CLI tool")

@app.command()
def greet(
    name: str = typer.Argument(help="Name to greet"),
    formal: bool = typer.Option(False, "--formal", "-f", help="Use formal greeting"),
    count: int = typer.Option(1, "--count", "-c", help="Number of greetings"),
):
    """Greet someone by name."""
    greeting = "Good day" if formal else "Hello"
    for _ in range(count):
        typer.echo(f"{greeting}, {name}!")

if __name__ == "__main__":
    app()
```

### Subcommands

```python
app = typer.Typer()
users_app = typer.Typer(help="User management")
app.add_typer(users_app, name="users")

@users_app.command("list")
def list_users(
    active: bool = typer.Option(True, help="Show only active users"),
):
    """List all users."""
    ...

@users_app.command("create")
def create_user(
    name: str = typer.Argument(help="Username"),
    email: str = typer.Option(..., prompt=True, help="User email"),
):
    """Create a new user."""
    ...

# Usage: my-cli users list --active
# Usage: my-cli users create john --email john@example.com
```

### Progress and Status

```python
import typer
from rich.progress import track

@app.command()
def process(files: list[str] = typer.Argument(help="Files to process")):
    """Process files with progress bar."""
    results = []
    for f in track(files, description="Processing..."):
        results.append(process_file(f))

    typer.echo(f"Processed {len(results)} files")
```

## Click

### Basic CLI

```python
import click

@click.group()
@click.version_option()
def cli():
    """My CLI tool."""
    pass

@cli.command()
@click.argument("name")
@click.option("--count", "-c", default=1, help="Number of greetings")
def greet(name: str, count: int):
    """Greet someone."""
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

### Click Callbacks and Validation

```python
def validate_email(ctx, param, value):
    if value and "@" not in value:
        raise click.BadParameter("Must be a valid email")
    return value

@cli.command()
@click.option("--email", callback=validate_email)
def register(email):
    ...
```

## Output Formatting

### Rich Tables

```python
from rich.console import Console
from rich.table import Table

console = Console()

def show_results(items: list[dict]):
    table = Table(title="Results")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Status", style="bold")

    for item in items:
        status_style = "green" if item["status"] == "active" else "red"
        table.add_row(
            str(item["id"]),
            item["name"],
            f"[{status_style}]{item['status']}[/]",
        )

    console.print(table)
```

### JSON Output Mode

```python
import json

@app.command()
def list_items(
    output: str = typer.Option("table", help="Output format: table, json, csv"),
):
    """List items in various formats."""
    items = fetch_items()

    if output == "json":
        typer.echo(json.dumps(items, indent=2))
    elif output == "csv":
        typer.echo("id,name,status")
        for item in items:
            typer.echo(f"{item['id']},{item['name']},{item['status']}")
    else:
        show_table(items)
```

### Color and Styling

```python
# Typer/Click
typer.echo(typer.style("Success!", fg=typer.colors.GREEN, bold=True))
typer.echo(typer.style("Error!", fg=typer.colors.RED))

# Rich (more powerful)
from rich.console import Console
console = Console()
console.print("[green]Success![/green]")
console.print("[red bold]Error![/red bold]")
console.print("[yellow]Warning:[/yellow] check your config")
```

## Configuration Files

### TOML Config (Recommended)

```python
import tomllib
from pathlib import Path

DEFAULT_CONFIG = {
    "output_format": "table",
    "verbose": False,
    "api_url": "https://api.example.com",
}

def load_config(path: Path | None = None) -> dict:
    config = DEFAULT_CONFIG.copy()

    # Check standard locations
    locations = [
        path,
        Path.cwd() / ".my-tool.toml",
        Path.home() / ".config" / "my-tool" / "config.toml",
    ]

    for loc in locations:
        if loc and loc.exists():
            with open(loc, "rb") as f:
                file_config = tomllib.load(f)
            config.update(file_config)
            break

    return config
```

### Config File Format

```toml
# .my-tool.toml
output_format = "json"
verbose = true

[api]
url = "https://api.example.com"
timeout = 30
```

## Exit Codes

| Code | Meaning                       |
| ---- | ----------------------------- |
| 0    | Success                       |
| 1    | General error                 |
| 2    | Invalid usage / bad arguments |
| 130  | Interrupted (Ctrl+C)          |

```python
import sys

@app.command()
def check(strict: bool = typer.Option(False)):
    issues = run_checks()
    if issues:
        for issue in issues:
            typer.echo(f"Issue: {issue}", err=True)
        raise typer.Exit(code=1)
    typer.echo("All checks passed")
```

## Distribution

### pyproject.toml Entry Points

```toml
[project.scripts]
my-cli = "my_package.cli:app"
```

### Install and Run

```bash
# Development install
uv pip install -e .

# Run
my-cli --help
my-cli greet "World"
```

## Testing CLIs

```python
from typer.testing import CliRunner
from my_package.cli import app

runner = CliRunner()

def test_greet():
    result = runner.invoke(app, ["greet", "World"])
    assert result.exit_code == 0
    assert "Hello, World!" in result.output

def test_greet_formal():
    result = runner.invoke(app, ["greet", "World", "--formal"])
    assert "Good day, World!" in result.output

def test_invalid_args():
    result = runner.invoke(app, ["greet"])  # Missing required arg
    assert result.exit_code != 0
```

## Activation Triggers

This skill auto-activates when prompts contain:

- "cli", "command line", "command-line"
- "typer", "click", "argparse"
- "terminal tool", "cli tool"
- "subcommand", "argument", "option flag"

## Integration

- **python-ecosystem** skill: Python packaging and tooling
- **testing-patterns** skill: CLI testing strategies
- **@python-pro** agent: Python expertise
