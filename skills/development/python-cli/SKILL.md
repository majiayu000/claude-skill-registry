---
name: python-cli
description: Annotated[str, typer.Option(
---

# Skill: Python CLI Development

## Overview
Patterns and best practices for building Python CLI applications with Click or Typer.

## Basic CLI Structure

### Using Click
```python
import click

@click.group()
def cli():
    """Evolution Todo CLI"""
    pass

@cli.command()
@click.argument('title')
@click.option('--priority', type=click.Choice(['low', 'medium', 'high']), default='medium')
@click.option('--description', '-d', default='')
def add(title, priority, description):
    """Add a new task"""
    # Implementation
    click.echo(f"Created task: {title}")

if __name__ == '__main__':
    cli()
```

### Using Typer
```python
import typer
from typing_extensions import Annotated

app = typer.Typer()

@app.command()
def add(
    title: str,
    priority: Annotated[str, typer.Option()] = "medium",
    description: Annotated[str, typer.Option("--description", "-d")] = ""
):
    """Add a new task"""
    typer.echo(f"Created task: {title}")

if __name__ == "__main__":
    app()
```

## Best Practices

### 1. Command Organization
```python
# Group related commands
@cli.group()
def task():
    """Task management commands"""
    pass

@task.command()
def list():
    """List all tasks"""
    pass

@task.command()
def add():
    """Add a task"""
    pass
```

### 2. Output Formatting
```python
from rich.console import Console
from rich.table import Table

console = Console()

def display_tasks(tasks):
    table = Table(title="Tasks")
    table.add_column("ID", style="cyan")
    table.add_column("Title", style="white")
    table.add_column("Priority", style="yellow")
    table.add_column("Status", style="green")

    for task in tasks:
        table.add_row(
            str(task.id),
            task.title,
            task.priority,
            task.status
        )

    console.print(table)
```

### 3. Error Handling
```python
try:
    # Command logic
    pass
except Exception as e:
    typer.secho(f"Error: {str(e)}", fg=typer.colors.RED)
    raise typer.Exit(code=1)
```

### 4. Configuration
```python
import os
from pathlib import Path

def get_config_dir():
    return Path.home() / '.evolution-todo'

def get_db_path():
    config_dir = get_config_dir()
    config_dir.mkdir(exist_ok=True)
    return config_dir / 'todos.db'
```

### 5. Interactive Prompts
```python
if typer.confirm("Are you sure you want to delete this task?"):
    # Delete task
    typer.echo("Task deleted")
else:
    typer.echo("Cancelled")
```

## Common Patterns

### Pagination
```python
def paginate(items, page=1, per_page=20):
    start = (page - 1) * per_page
    end = start + per_page
    return items[start:end]
```

### Color Coding by Priority
```python
PRIORITY_COLORS = {
    'low': 'green',
    'medium': 'yellow',
    'high': 'red'
}

def format_priority(priority):
    color = PRIORITY_COLORS.get(priority, 'white')
    return typer.style(priority.upper(), fg=color, bold=True)
```

## Testing CLI Commands
```python
from click.testing import CliRunner

def test_add_task():
    runner = CliRunner()
    result = runner.invoke(cli, ['add', 'Test task', '--priority', 'high'])
    assert result.exit_code == 0
    assert 'Created task' in result.output
```

## Phase 1 Application
Use this skill when implementing `/phase-1-console/`
