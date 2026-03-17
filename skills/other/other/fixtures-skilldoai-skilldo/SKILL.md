---
name: click
description: Command Line Interface Creation Kit
version: 8.1.7
ecosystem: python
license: BSD-3-Clause
---

## Imports

```python
import click
from click import command, option, argument
```

## Core Patterns

### Basic Command

Create a simple CLI command with Click.

```python
import click

@click.command()
def hello():
    click.echo('Hello World!')

if __name__ == '__main__':
    hello()
```

### Command with Options

Add options to your CLI command.

```python
import click

@click.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name', help='The person to greet.')
def hello(count, name):
    for _ in range(count):
        click.echo(f'Hello {name}!')

if __name__ == '__main__':
    hello()
```

### Command with Arguments

Use positional arguments in your CLI.

```python
import click

@click.command()
@click.argument('name')
def hello(name):
    click.echo(f'Hello {name}!')

if __name__ == '__main__':
    hello()
```

## Configuration

Click commands are decorated with `@click.command()` and options with `@click.option()`.

Use `click.echo()` instead of `print()` for consistent output across platforms.

## Pitfalls

**Wrong**: Using `print()` instead of `click.echo()`
```python
@click.command()
def hello():
    print("Hello")  # May have encoding issues
```

**Right**: Always use `click.echo()`
```python
@click.command()
def hello():
    click.echo("Hello")  # Handles encoding properly
```

## References

- Official Documentation: https://click.palletsprojects.com/
- GitHub: https://github.com/pallets/click
- PyPI: https://pypi.org/project/click/
