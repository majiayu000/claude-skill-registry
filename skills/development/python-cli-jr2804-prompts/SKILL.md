---
name: python-cli
description: Universal Python CLI development patterns and best practices
license: MIT
compatibility: opencode
metadata:
    related_python_guidelines: For general Python development, use skill `python-guidelines`
    related_coding_principles: For overall coding standards, use skill `coding-principles`
---

# Python CLI

## What I Do

Provide universal patterns for developing command-line interfaces in Python that work across different projects and domains.

## Universal CLI Architecture

### Framework Selection

**Recommended Frameworks:**

- **Typer**: For simple, type-annotated CLIs
- **Click**: For more complex CLI applications
- **Argparse**: For standard library compatibility

```python
# Universal Typer CLI structure
import typer
from typing import Optional

def main(
    input_file: str = typer.Argument(..., help="Input file path"),
    output_file: Optional[str] = typer.Option(None, "-o", "--output", help="Output file path"),
    verbose: bool = typer.Option(False, "-v", "--verbose", help="Verbose output")
):
    """Universal CLI entry point"""
    # CLI logic here
    typer.echo(f"Processing {input_file}")

if __name__ == "__main__":
    typer.run(main)
```

### Parameter Handling Patterns

```python
# Universal parameter handling
class CLIParameters:
    def __init__(self):
        self.input_file = None
        self.output_file = None
        self.verbose = False

    def from_args(self, args):
        """Parse arguments into structured parameters"""
        self.input_file = args.input_file
        self.output_file = args.output_file or f"output_{args.input_file}"
        self.verbose = args.verbose
        return self

    def validate(self):
        """Validate parameters before execution"""
        if not os.path.exists(self.input_file):
            raise FileNotFoundError(f"Input file not found: {self.input_file}")
```

## When to Use Me

Use this skill when:

- Developing CLI applications in Python
- Standardizing CLI patterns across projects
- Creating reusable CLI components
- Implementing user-friendly command-line tools

## Universal CLI Examples

### Output Formatting

```python
# Universal output formatting with Rich
from rich.console import Console
from rich.panel import Panel

console = Console()

def format_output(result, title="Results"):
    """Universal output formatting"""
    panel = Panel.fit(
        str(result),
        title=title,
        border_style="blue",
        padding=(1, 2)
    )
    console.print(panel)

# Usage examples
console.print("[green]✓[/green] Operation completed successfully")
console.print("[red]✗[/red] Error: File not found")
console.print("[yellow]⚠[/yellow] Warning: Deprecated feature used")
console.print("[cyan]?[/cyan] Processing: file.txt")
```

### Environment Variable Integration

```python
# Universal environment variable patterns
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class EnvironmentConfig:
    def __init__(self):
        self.debug = os.getenv("DEBUG", "false").lower() == "true"
        self.timeout = int(os.getenv("TIMEOUT", "30"))
        self.api_key = os.getenv("API_KEY")

    def validate(self):
        """Validate required environment variables"""
        if not self.api_key and not self.debug:
            raise EnvironmentError("API_KEY environment variable required")
```

### Error Handling and User Feedback

```python
# Universal CLI error handling
def handle_cli_error(error, context="CLI"):
    """Handle errors with user-friendly messages"""
    console = Console()

    if isinstance(error, FileNotFoundError):
        console.print(f"[red]✗[/red] File not found: {error.filename}")
        suggest_similar_files(error.filename)
    elif isinstance(error, PermissionError):
        console.print(f"[red]✗[/red] Permission denied: {error.filename}")
        console.print("[yellow]⚠[/yellow] Try running with elevated privileges")
    else:
        console.print(f"[red]✗[/red] {context} error: {str(error)}")
        if console.width > 80:
            console.print_exception()
```

## Best Practices

1. **Consistency**: Use same CLI patterns across projects
2. **User Experience**: Provide clear, helpful error messages
3. **Documentation**: Include comprehensive help text
4. **Testing**: Test CLI applications thoroughly

## Compatibility

Works with:

- Any Python CLI application
- Cross-project CLI standardization
- Organizational tool development
- Universal command-line patterns
