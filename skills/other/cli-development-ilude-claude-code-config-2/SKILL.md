---
name: cli-development
description: Best practices for building CLI applications across languages. Covers CLI design principles (Unix philosophy, command structure, subcommands vs flags), argument parsing (required/optional args, flags, environment variables, config files, precedence), user interface (help text, version info, progress indicators, color output, interactive prompts), output formatting (human-readable vs machine-readable JSON/YAML, exit codes), error handling (clear messages, suggestions, debug mode), cross-platform considerations (paths, line endings, terminal capabilities), testing strategies (integration tests, output verification, exit codes), documentation (README, man pages, built-in help), and language-specific libraries. Activate when working with CLI applications, command-line tools, argument parsing, CLI utilities, argument handling, commands, subcommands, CLI frameworks, or building command-line interfaces.
---

# CLI Development Guidelines

Best practices for designing and implementing command-line interface (CLI) applications across programming languages.

## CLI Design Principles

### Unix Philosophy
Follow the core Unix philosophy for robust, composable CLIs:

- **Do one thing well** - Each command should have a single, well-defined responsibility
- **Make it composable** - Design output to work as input to other programs
- **Handle text streams** - CLIs work with stdin/stdout/stderr
- **Exit cleanly** - Use appropriate exit codes (0 for success, non-zero for errors)
- **Fail fast** - Detect and report problems immediately
- **Be scriptable** - All functionality must be accessible from non-interactive contexts

### Command Structure

#### Verb-Noun Pattern
Organize commands using verb-noun relationships:

```
# Good: clear action and object
git add <file>           # verb: add, noun: file
docker run <image>       # verb: run, noun: image
npm install <package>    # verb: install, noun: package

# Avoid: unclear structure
git foo                  # ambiguous
docker something         # unclear what happens
```

#### Subcommands vs Flags

**Use subcommands when:**
- Commands have distinct behaviors or workflows
- Different sets of options apply to different operations
- You want clear logical grouping

```
git branch                    # subcommand
git branch --list             # subcommand with flag
git branch --delete <name>    # subcommand with flag and argument
```

**Use flags when:**
- Modifying behavior of a single operation
- Toggling optional features
- Providing configuration

```
ls --color          # flag modifies ls behavior
grep -r --include   # flags modify search behavior
```

**Never mix deeply:**
```
# Avoid: unclear hierarchy
tool --verbose subcommand --debug --mode strict

# Better: clear structure
tool subcommand --verbose --debug --mode strict
```

### Command Hierarchy
Keep hierarchy shallow (max 2-3 levels):

```
# Good: clear, discoverable
aws s3 ls
aws ec2 describe-instances

# Avoid: too deep
cloud provider storage list all buckets
```

## Argument Parsing

### Argument Types

**Positional Arguments**
- Required by default
- Appear in specific positions
- Use for primary input/object

```bash
cp <source> <destination>   # Two required positional arguments
docker run <image>          # One required positional argument
```

**Optional Arguments (with defaults)**
- Used less frequently
- Should have sensible defaults
- Clearly documented

```bash
npm install [directory]     # Optional, defaults to current directory
grep [options] <pattern> [file]  # File argument optional
```

### Flags and Options

**Short Flags (-f)**
- Single letter, used frequently
- For common operations

```bash
ls -l          # long format
grep -r        # recursive
tar -xvf       # combined flags
```

**Long Flags (--flag)**
- Verbose, self-documenting
- For less-common operations
- Preferred in scripts

```bash
docker run --detach --name myapp
npm install --save-dev
grep --recursive --include="*.js"
```

**Flag Styles**
```
# Boolean flags
--verbose              # boolean true/false
--color=always         # explicit value

# Flags with values
--output file.txt      # space-separated
--output=file.txt      # equals-separated

# Accept both styles when possible
--timeout 30 or --timeout=30
```

### Environment Variables

**Convention:** Use SCREAMING_SNAKE_CASE for environment variables

```bash
export DEBUG=1
export LOG_LEVEL=debug
export API_TOKEN=secret
```

**Hierarchy (high to low precedence):**
1. Command-line flags (highest priority - most explicit)
2. Environment variables (middle - applies to multiple invocations)
3. Configuration file (lower - shared settings)
4. Built-in defaults (lowest priority - fallback)

**Example precedence:**
```bash
# If user runs with flag, it takes precedence
tool --timeout 10       # Uses 10, ignores TIMEOUT env var

# If no flag, check env var
export TIMEOUT=5
tool                    # Uses 5 from TIMEOUT

# If no flag or env var, use config file default
tool --config config.yaml  # Reads timeout from config.yaml

# If nothing specified, use built-in default
tool                    # Uses hardcoded default (e.g., 30)
```

### Configuration Files

**Location convention:**
- Linux/macOS: `~/.config/app/config.yaml` or `~/.apprc`
- Windows: `%APPDATA%\App\config.yaml` or `~\AppData\Local\App\config.yaml`
- All platforms: `./config.yaml` (current directory, highest priority)

**Format preference:** YAML > TOML > JSON > INI
- YAML is human-readable and concise
- TOML is simpler than YAML but supports nested structures
- JSON is universal but verbose
- INI is legacy

**Example config file:**
```yaml
# ~/.config/myapp/config.yaml
debug: false
log_level: info
timeout: 30
output_format: json
color: true

api:
  endpoint: https://api.example.com
  timeout: 10
```

**Load with proper precedence:**
```python
# Python example
import os
from pathlib import Path
import yaml

def load_config():
    # Built-in defaults
    config = {
        'debug': False,
        'timeout': 30,
        'color': True
    }

    # Load from config file
    config_path = Path.home() / '.config' / 'myapp' / 'config.yaml'
    if config_path.exists():
        with open(config_path) as f:
            file_config = yaml.safe_load(f)
            config.update(file_config)

    # Override with environment variables
    if os.getenv('DEBUG'):
        config['debug'] = os.getenv('DEBUG').lower() == 'true'
    if os.getenv('TIMEOUT'):
        config['timeout'] = int(os.getenv('TIMEOUT'))

    # Note: Command-line args handled by argument parser, applied after
    return config
```

## User Interface

### Help Text

**Provide comprehensive help:**

```bash
$ tool --help
Usage: tool [OPTIONS] COMMAND [ARGS]...

A brief description of what this tool does.

Options:
  -v, --verbose         Increase output verbosity
  -q, --quiet          Suppress non-error output
  -h, --help           Show this message and exit
  --version            Show version and exit

Commands:
  add                  Add a new item
  list                 List all items
  delete              Delete an item
  config              Manage configuration

Examples:
  tool add myitem
  tool list --format json
  tool delete --force

For more information: https://docs.example.com
```

**Help text structure:**
- Usage line: `Usage: tool [OPTIONS] COMMAND [ARGS]...`
- Brief description (1-2 lines)
- Options section (sorted: common first)
- Commands section (if subcommands exist)
- Examples section (show common patterns)
- Additional resources (docs link, contact info)

**Per-command help:**
```bash
$ tool add --help
Usage: tool add [OPTIONS] NAME

Add a new item to the collection.

Options:
  --description TEXT  Item description
  --tags TEXT        Comma-separated tags
  --priority INT     Priority level (1-10)
  -h, --help        Show this message and exit

Examples:
  tool add "My Item"
  tool add "Task" --priority 5 --tags work,urgent
```

### Version Information

**Provide version with --version / -v:**

```bash
$ tool --version
tool 1.2.3

# For complex tools, show component versions
$ tool --version
tool 1.2.3
  dependency-a: 2.1.0
  dependency-b: 5.4.3
```

**Store version in configuration:**
```python
# __version__.py or __init__.py
__version__ = "1.2.3"

# In main CLI file
import sys
from . import __version__

@click.command()
@click.option('--version', is_flag=True, help='Show version and exit')
def main(version):
    if version:
        click.echo(f"tool {__version__}")
        sys.exit(0)
```

### Progress Indicators

**For long operations, show progress:**

```python
# Python: using rich library
from rich.progress import track
import time

for i in track(range(100), description="Processing..."):
    time.sleep(0.1)  # Long operation
```

**Output format:**
```
Processing... [████████░░] 80%
or
Processing... ⠏ (spinning indicator)
```

### Spinners and Progress Bars

**Use spinners for indeterminate progress:**
```
Connecting to server... ⠋
Uploading file... ⠙
Waiting for response... ⠹
```

**Use progress bars for determinate progress:**
```
Downloading [████████░░░░░░] 40% (2.1 MB / 5.3 MB)
Processing  [██████████████████░░] 90%
```

**Implement responsibly:**
- Disable in non-interactive environments (detect piped output)
- Respect `--no-progress` flag
- Never output progress to stdout (use stderr)

### Color Output

**Support color with disable option:**

```python
# Python: using rich or click
import click

@click.command()
@click.option('--color', type=click.Choice(['always', 'auto', 'never']),
              default='auto', help='Color output mode')
def main(color):
    # auto: color if terminal supports it
    # always: force color (for piping to less -R)
    # never: disable color
    use_color = color == 'always' or (color == 'auto' and is_terminal())
```

**Environment variable override:**
```bash
# User can disable via environment
NO_COLOR=1 tool           # Disable color
FORCE_COLOR=1 tool        # Force color
```

**Terminal detection:**
```python
import sys
import os

def supports_color():
    # Check NO_COLOR env var
    if os.getenv('NO_COLOR'):
        return False

    # Check FORCE_COLOR env var
    if os.getenv('FORCE_COLOR'):
        return True

    # Check if stdout is a TTY
    return sys.stdout.isatty()
```

### Interactive Prompts

**Use for confirmations and user input:**

```python
# Python: using click
import click

@click.command()
@click.option('--force', is_flag=True, help='Skip confirmations')
def delete_item(force):
    if not force:
        if not click.confirm('Are you sure you want to delete?'):
            click.echo("Cancelled")
            return

    # Proceed with deletion
    click.echo("Deleted")

# Interactive selection
choice = click.prompt(
    'Choose an option',
    type=click.Choice(['a', 'b', 'c']),
    default='a'
)
```

**Guidelines:**
- Ask for confirmation before destructive operations
- Provide sensible defaults
- Allow bypassing with `--force` flag
- Never prompt in non-interactive contexts (detect piped input)

## Output Formatting

### Human-Readable Output

**Default format for interactive use:**

```
$ tool list
Name          Status    Modified
────────────────────────────────
Project A     Active    2 hours ago
Project B     Inactive  3 days ago
Project C     Active    1 week ago
```

**Characteristics:**
- Table format with clear columns
- Natural language (e.g., "2 hours ago")
- Colors for emphasis (when supported)
- Sorted intelligently

### Machine-Readable Output

**JSON format for scripting:**

```bash
$ tool list --format json
[
  {
    "name": "Project A",
    "status": "active",
    "modified": "2024-01-15T14:30:00Z"
  },
  {
    "name": "Project B",
    "status": "inactive",
    "modified": "2024-01-12T09:15:00Z"
  }
]
```

**YAML format (compact, readable):**

```bash
$ tool list --format yaml
- name: Project A
  status: active
  modified: 2024-01-15T14:30:00Z
- name: Project B
  status: inactive
  modified: 2024-01-12T09:15:00Z
```

**CSV format (for spreadsheets):**

```bash
$ tool list --format csv
name,status,modified
"Project A",active,2024-01-15T14:30:00Z
"Project B",inactive,2024-01-12T09:15:00Z
```

**Implementation:**
```python
import click
import json
import csv
import io

@click.command()
@click.option('--format', type=click.Choice(['table', 'json', 'yaml', 'csv']),
              default='table', help='Output format')
def list_items(format):
    items = get_items()

    if format == 'json':
        click.echo(json.dumps(items, indent=2))
    elif format == 'csv':
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=items[0].keys())
        writer.writeheader()
        writer.writerows(items)
        click.echo(output.getvalue())
    elif format == 'yaml':
        import yaml
        click.echo(yaml.dump(items, default_flow_style=False))
    else:  # table
        display_table(items)
```

### Exit Codes

**Standard exit codes:**

```
0   - Success, no errors
1   - General error
2   - Misuse of shell command (invalid arguments)
3-125 - Application-specific errors
126 - Command cannot execute
127 - Command not found
128+130 - Fatal signal "N"
130 - Script terminated by Ctrl+C
```

**Common application codes:**
```
0   - Success
1   - General/unspecified error
2   - Misuse of command syntax
64  - Bad input data
65  - Data format error
66  - No input file
69  - Service unavailable
70  - Internal software error
71  - System error
77  - Permission denied
78  - Configuration error
```

**Implementation:**
```python
import click
import sys

@click.command()
def main():
    try:
        result = do_work()
        if not result:
            sys.exit(1)  # Error condition
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(2)  # Bad input
    except PermissionError as e:
        click.echo(f"Permission denied: {e}", err=True)
        sys.exit(77)
    except Exception as e:
        click.echo(f"Internal error: {e}", err=True)
        sys.exit(70)

    sys.exit(0)  # Success
```

**Always exit explicitly:**
```bash
# Good: script can detect success/failure
tool && echo "Success" || echo "Failed"

# Bad: unclear exit status
tool
echo "Done"  # Prints regardless of success
```

## Error Handling

### Clear Error Messages

**Good error messages:**
- Concise (one line if possible)
- Specific about what went wrong
- Suggest how to fix it

```bash
# Good
$ tool add --priority invalid
Error: --priority must be a number (1-10), got 'invalid'

# Bad
$ tool add --priority invalid
Error: Invalid argument

# Good
$ tool delete nonexistent
Error: Item 'nonexistent' not found. Use 'tool list' to see available items.

# Bad
$ tool delete nonexistent
File not found
```

**Error format:**
```
Error: [what happened]. [How to fix it or where to learn more].
```

### Suggestions for Fixes

Provide actionable suggestions:

```python
import click

@click.command()
@click.argument('command')
def main(command):
    valid_commands = ['add', 'list', 'delete']

    if command not in valid_commands:
        # Suggest closest match
        from difflib import get_close_matches
        suggestions = get_close_matches(command, valid_commands, n=1)

        msg = f"Unknown command '{command}'."
        if suggestions:
            msg += f" Did you mean '{suggestions[0]}'?"
        else:
            msg += f" Available commands: {', '.join(valid_commands)}"

        click.echo(f"Error: {msg}", err=True)
        raise SystemExit(1)
```

### Debug Mode

**Provide --debug flag for detailed output:**

```python
import click
import sys
import traceback

@click.command()
@click.option('--debug', is_flag=True, help='Show detailed error information')
def main(debug):
    try:
        do_work()
    except Exception as e:
        if debug:
            # Show full traceback
            traceback.print_exc(file=sys.stderr)
        else:
            # Show user-friendly message
            click.echo(f"Error: {str(e)}", err=True)
            click.echo("Use --debug to see details", err=True)
        sys.exit(1)
```

**Example output:**
```bash
$ tool --debug
Error: Connection failed
Traceback (most recent call last):
  File "tool.py", line 42, in main
    connect_to_server()
  File "tool.py", line 15, in connect_to_server
    raise ConnectionError("Timeout after 30s")
ConnectionError: Timeout after 30s
```

## Cross-Platform Considerations

### Path Separators

**Always use proper path handling:**

```python
# Good: use pathlib (cross-platform)
from pathlib import Path

config_path = Path.home() / '.config' / 'app' / 'config.yaml'
output_path = Path('output') / 'result.txt'

# Also good: use os.path
import os
config_path = os.path.join(os.path.expanduser('~'), '.config', 'app', 'config.yaml')

# Avoid: hardcoded separators
config_path = '~/.config/app/config.yaml'  # Wrong on Windows
```

**Node.js example:**
```javascript
const path = require('path');
const os = require('os');

const configPath = path.join(os.homedir(), '.config', 'app', 'config.yaml');
const outputPath = path.join('output', 'result.txt');
```

### Line Endings

**Normalize line endings:**

```python
# Python: open files with universal newline support (default)
with open('file.txt', 'r') as f:  # Automatically handles \r\n, \n, \r
    content = f.read()

# When writing, use default newline handling
with open('file.txt', 'w') as f:
    f.write(content)  # Uses platform default newline
```

**Git configuration:**
```bash
# Set in .gitattributes to normalize line endings
* text=auto
*.py text eol=lf
*.json text eol=lf
```

### Terminal Capabilities

**Detect terminal capabilities:**

```python
import sys
import os

def get_terminal_width():
    """Get terminal width, default to 80."""
    try:
        return os.get_terminal_size().columns
    except (AttributeError, ValueError):
        return 80

def supports_unicode():
    """Check if terminal supports Unicode."""
    encoding = sys.stdout.encoding or 'utf-8'
    return encoding.lower() in ('utf-8', 'utf8')

def supports_color():
    """Check if terminal supports colors."""
    # Already covered above
    return True

# Use capabilities to adjust output
if supports_unicode():
    symbol = '✓'  # Check mark
else:
    symbol = '✔'  # Alternative
```

**Avoid assumptions:**
```python
# Bad: assumes capabilities
output = "✓ Success\n"

# Good: checks capabilities
symbol = '✓' if supports_unicode() else '✔'
output = f"{symbol} Success\n"
```

## Testing CLI Applications

### Integration Tests

**Test the complete CLI, not just functions:**

```python
import subprocess
import json

def test_list_command():
    """Test list command output."""
    result = subprocess.run(
        ['tool', 'list', '--format', 'json'],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0
    output = json.loads(result.stdout)
    assert isinstance(output, list)

def test_list_command_human_readable():
    """Test list command with default format."""
    result = subprocess.run(
        ['tool', 'list'],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0
    assert 'Name' in result.stdout  # Table header
```

**Test with Click (Python):**
```python
from click.testing import CliRunner
from tool.cli import main

def test_list_command():
    runner = CliRunner()
    result = runner.invoke(main, ['list', '--format', 'json'])

    assert result.exit_code == 0
    output = json.loads(result.output)
    assert isinstance(output, list)
```

### Output Verification

**Verify output format and content:**

```python
import subprocess

def test_add_command_success():
    """Test successful add operation."""
    result = subprocess.run(
        ['tool', 'add', 'Test Item', '--priority', '5'],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0
    assert 'Added' in result.stdout or 'Success' in result.stdout

def test_add_command_invalid_priority():
    """Test validation of priority argument."""
    result = subprocess.run(
        ['tool', 'add', 'Test Item', '--priority', 'invalid'],
        capture_output=True,
        text=True
    )

    assert result.returncode != 0
    assert 'Error' in result.stderr
    assert 'priority' in result.stderr.lower()
```

### Exit Code Checks

**Verify proper exit codes:**

```python
import subprocess

def test_help_flag_exit_code():
    """Test --help returns success."""
    result = subprocess.run(['tool', '--help'], capture_output=True)
    assert result.returncode == 0

def test_invalid_command_exit_code():
    """Test invalid command returns error code."""
    result = subprocess.run(['tool', 'invalid'], capture_output=True)
    assert result.returncode != 0

def test_missing_required_arg():
    """Test missing required argument returns error."""
    result = subprocess.run(['tool', 'delete'], capture_output=True)
    assert result.returncode == 2  # Misuse of command syntax
```

## Documentation

### README

**CLI tools need clear README documentation:**

```markdown
# Tool Name

Brief description of what the tool does.

## Installation

Installation instructions (package manager, build from source, etc.)

## Usage

### Basic Usage

```bash
tool [COMMAND] [OPTIONS] [ARGUMENTS]
```

### Examples

```bash
# List all items
tool list

# Add new item
tool add "My Item" --priority 5

# Delete with confirmation
tool delete "My Item"

# Suppress confirmation
tool delete "My Item" --force
```

### Commands

- `add [NAME]` - Add a new item
- `list` - List all items
- `delete [NAME]` - Delete an item
- `config` - Manage configuration

### Options

- `-v, --verbose` - Increase output verbosity
- `--format [json|yaml|csv]` - Output format
- `--debug` - Show debug information
- `-h, --help` - Show help message
- `--version` - Show version

### Configuration

Settings can be configured via:
1. Command-line flags (highest priority)
2. Environment variables
3. Config file at `~/.config/tool/config.yaml`
4. Built-in defaults

### Environment Variables

- `DEBUG` - Enable debug mode
- `TOOL_CONFIG` - Path to config file
- `NO_COLOR` - Disable colored output

### Configuration File

Create `~/.config/tool/config.yaml`:

```yaml
debug: false
format: table
color: true
```

## Troubleshooting

### Common Issues

**Issue: "command not found"**
- Ensure tool is installed and in PATH
- Check: `which tool`

**Issue: Permission denied**
- Make script executable: `chmod +x tool`

## Development

Build and test instructions.
```

### Man Pages

**Create man pages for Unix systems:**

```
TOOL(1)                    User Commands                    TOOL(1)

NAME
    tool - A tool that does one thing well

SYNOPSIS
    tool [OPTIONS] COMMAND [ARGS]...

DESCRIPTION
    Detailed description of what the tool does.

COMMANDS
    add NAME          Add a new item
    list             List all items
    delete NAME      Delete an item

OPTIONS
    -v, --verbose    Increase output verbosity
    --format FMT     Output format (json, yaml, csv)
    -h, --help       Show help message
    --version        Show version

EXAMPLES
    Add a new item:
        tool add "My Item"

    List items as JSON:
        tool list --format json

EXIT STATUS
    0    Success
    1    General error
    2    Invalid arguments

FILES
    ~/.config/tool/config.yaml
        Configuration file

SEE ALSO
    tool-add(1), tool-delete(1)
```

### Built-in Help

**Make help accessible and comprehensive:**

```python
@click.group()
def main():
    """Main CLI tool."""
    pass

@main.command()
def help():
    """Show detailed help information."""
    click.echo(click.get_current_context().get_help())
```

## Common CLI Libraries

### Python

**Click** - Most popular, decorator-based
```python
import click

@click.command()
@click.option('--name', prompt='Your name', help='Name of person')
@click.option('--count', default=1, help='Number of greetings')
def hello(name, count):
    """Simple program that greets NAME COUNT times."""
    for _ in range(count):
        click.echo(f'Hello {name}!')

if __name__ == '__main__':
    hello()
```

**Typer** - Built on Click, modern with async support
```python
import typer

app = typer.Typer()

@app.command()
def add(name: str, priority: int = typer.Option(5, min=1, max=10)):
    """Add a new item."""
    print(f"Added {name} with priority {priority}")

if __name__ == "__main__":
    app()
```

**Argparse** - Built-in to Python, more verbose
```python
import argparse

parser = argparse.ArgumentParser(description='Process some integers')
parser.add_argument('--name', required=True, help='Name')
parser.add_argument('--count', type=int, default=1, help='Count')
args = parser.parse_args()
```

### Node.js / JavaScript

**Commander** - Minimal and clean
```javascript
const { Command } = require('commander');

const program = new Command();

program
  .command('add <name>')
  .option('--priority <number>', 'Item priority', '5')
  .action((name, options) => {
    console.log(`Added ${name} with priority ${options.priority}`);
  });

program.parse(process.argv);
```

**Yargs** - Feature-rich
```javascript
const yargs = require('yargs/yargs');
const { hideBin } = require('yargs/helpers');

yargs(hideBin(process.argv))
  .command('add <name>', 'Add item', (yargs) => {
    return yargs.option('priority', { type: 'number', default: 5 });
  }, (argv) => {
    console.log(`Added ${argv.name} with priority ${argv.priority}`);
  })
  .argv;
```

**Oclif** - Full-featured framework for complex CLIs
```javascript
const {Command, flags} = require('@oclif/command');

class AddCommand extends Command {
  static description = 'Add a new item';

  static args = [{ name: 'name' }];

  static flags = {
    priority: flags.integer({ default: 5 })
  };

  async run() {
    const { args, flags } = this.parse(AddCommand);
    this.log(`Added ${args.name} with priority ${flags.priority}`);
  }
}

module.exports = AddCommand;
```

### Go

**Cobra** - Popular Go CLI framework
```go
var rootCmd = &cobra.Command{
  Use:   "tool",
  Short: "A brief description",
  Long:  "A longer description...",
  Run: func(cmd *cobra.Command, args []string) {
    fmt.Println("Hello World!")
  },
}

var addCmd = &cobra.Command{
  Use:   "add [name]",
  Short: "Add a new item",
  Args:  cobra.MinimumNArgs(1),
  Run: func(cmd *cobra.Command, args []string) {
    fmt.Printf("Added %s\n", args[0])
  },
}

func init() {
  rootCmd.AddCommand(addCmd)
  addCmd.Flags().IntP("priority", "p", 5, "Priority level")
}
```

### Rust

**Clap** - Powerful and flexible
```rust
use clap::{Parser, Subcommand};

#[derive(Parser)]
#[clap(name = "tool")]
#[clap(about = "A tool that does one thing well")]
struct Cli {
    #[clap(subcommand)]
    command: Option<Commands>,

    #[clap(short, long)]
    debug: bool,
}

#[derive(Subcommand)]
enum Commands {
    Add {
        name: String,
        #[clap(short, long, default_value = "5")]
        priority: u8,
    },
    List,
}

fn main() {
    let cli = Cli::parse();
    // Handle commands...
}
```

## Common Patterns and Examples

### Pattern: Global Options vs Subcommand Options

```
# Global options apply to tool
tool --verbose add item

# Subcommand options apply to subcommand
tool add item --priority 5

# Mix of both
tool --verbose add item --priority 5
```

### Pattern: Piping and Composition

```bash
# Pipe output to other tools
tool list --format json | jq '.[] | select(.status == "active")'

# Use as input to other commands
tool export > backup.json
tool import < backup.json

# Chain commands
tool list | grep important | while read item; do tool process "$item"; done
```

### Pattern: Interactive vs Non-interactive

```python
import sys
import click

@click.command()
@click.option('--force', is_flag=True, help='Skip confirmations')
def delete_item(force):
    if sys.stdin.isatty() and not force:
        # Interactive - prompt for confirmation
        if not click.confirm('Delete this item?'):
            click.echo('Cancelled')
            return

    # Non-interactive or confirmed
    perform_deletion()
```

### Pattern: Timeout Handling

```python
import signal
import sys

def timeout_handler(signum, frame):
    print("Operation timed out")
    sys.exit(124)

signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(30)  # 30 second timeout

try:
    result = long_running_operation()
finally:
    signal.alarm(0)  # Cancel alarm
```

---

**Note:** For project-specific CLI patterns, check `.claude/CLAUDE.md` in the project directory.
