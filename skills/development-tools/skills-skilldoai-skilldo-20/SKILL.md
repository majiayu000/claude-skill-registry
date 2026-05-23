---
name: click
description: A Python library for building command line interfaces with composable commands, options, and arguments.
version: 8.3.1
ecosystem: python
license: BSD-3-Clause
generated_with: gpt-5.2
---

## Imports

```python
import click
from click import (
    Abort,
    BadParameter,
    ClickException,
    UsageError,
    argument,
    command,
    confirm,
    echo,
    group,
    option,
    pass_context,
    pass_obj,
    prompt,
    secho,
    style,
)
from click.testing import CliRunner
from click.shell_completion import CompletionItem, ShellComplete, add_completion_class
```

## Core Patterns

### Single command with options and arguments ✅ Current
```python
import click


@click.command()
@click.argument("name")
@click.option("--times", "-t", type=click.INT, default=1, show_default=True)
@click.option("--loud/--quiet", default=False, help="Toggle uppercase output.")
def hello(name: str, times: int, loud: bool) -> None:
    """Greet NAME a number of TIMES."""
    msg = f"Hello, {name}!"
    if loud:
        msg = msg.upper()

    for _ in range(times):
        click.echo(msg)


if __name__ == "__main__":
    hello()
```
* Use `@click.command()` to define a CLI entry point; add inputs with `@click.argument()` and `@click.option()`.
* Prefer `click.echo()` over `print()` for consistent terminal behavior; use `err=True` for stderr.

### Command groups and subcommands ✅ Current
```python
import click


@click.group()
def cli() -> None:
    """Top-level command group."""
    pass


@cli.command()
@click.option("--path", type=click.Path(dir_okay=False, readable=True), required=True)
def show(path: str) -> None:
    """Print a file to stdout."""
    with click.open_file(path, mode="r", encoding="utf-8") as f:
        click.echo(f.read(), nl=False)


@cli.command()
@click.argument("words", nargs=-1)
def join(words: tuple[str, ...]) -> None:
    """Join WORDS with spaces."""
    click.echo(" ".join(words))


if __name__ == "__main__":
    cli()
```
* Use `@click.group()` for multi-command CLIs; register subcommands via `@group.command()`.
* Use `click.Path(...)` and `click.open_file(...)` for validated paths and robust file opening.

### Context and object passing (`pass_context`, `pass_obj`, `make_pass_decorator`) ✅ Current
```python
from __future__ import annotations

from dataclasses import dataclass

import click


@dataclass
class AppState:
    verbose: bool


pass_state = click.make_pass_decorator(AppState)


@click.group()
@click.option("--verbose/--no-verbose", default=False)
@click.pass_context
def cli(ctx: click.Context, verbose: bool) -> None:
    ctx.obj = AppState(verbose=verbose)


@cli.command()
@pass_state
def status(state: AppState) -> None:
    click.echo(f"verbose={state.verbose}")


@cli.command()
@click.pass_context
def where(ctx: click.Context) -> None:
    # Direct access to context when needed
    click.echo(f"command={ctx.command.name}")


if __name__ == "__main__":
    cli()
```
* Use `ctx.obj` to store application state; `click.make_pass_decorator()` provides typed access to that object.
* `@click.pass_context` and `@click.pass_obj` are for dependency injection across command layers.

### Prompts, confirmation, and secure input ✅ Current
```python
import click


@click.command()
@click.option("--username", prompt=True)
@click.password_option("--password", confirmation_prompt=True)
@click.confirmation_option("--confirm", prompt="Proceed with login?")
def login(username: str, password: str, confirm: bool) -> None:
    # Never echo passwords; Click handles masking for password options.
    if not confirm:
        raise click.Abort()
    click.echo(f"Logging in as {username} (password length={len(password)})")


if __name__ == "__main__":
    login()
```
* `click.prompt()` / `prompt=True` collects interactive input; `click.password_option()` masks input and can confirm.
* `click.confirmation_option()` is a reusable “are you sure?” pattern; raise `click.Abort` to stop cleanly.

### Testing commands with `CliRunner` ✅ Current
```python
import click
from click.testing import CliRunner


@click.command()
@click.option("--count", type=click.INT, default=1)
def repeat(count: int) -> None:
    for i in range(count):
        click.echo(f"line {i + 1}")


def main() -> None:
    runner = CliRunner()
    result = runner.invoke(repeat, ["--count", "3"])
    assert result.exit_code == 0
    assert "line 3" in result.output


if __name__ == "__main__":
    main()
```
* Use `click.testing.CliRunner.invoke()` to run commands without spawning subprocesses.
* Inspect `Result.exit_code`, `Result.output`, and `Result.exception` for assertions.

## Configuration

- **Defaults and display**
  - Use `default=...` on `@click.option(...)`.
  - Use `show_default=True` to show defaults in `--help`.
- **Types and validation**
  - Built-in types: `click.STRING`, `click.INT`, `click.FLOAT`, `click.BOOL`, `click.UUID`.
  - Structured types: `click.Path`, `click.File`, `click.Choice`, `click.IntRange`, `click.FloatRange`, `click.DateTime`, `click.Tuple`.
- **Environment variables**
  - Options can read from environment variables using `@click.option(..., envvar="NAME")`.
- **Help and version**
  - `click.help_option()` and `click.version_option()` can be used to add standardized `--help` / `--version` behavior.
- **Embedding vs standalone**
  - `Command.main(..., standalone_mode=False)` prevents Click from calling `sys.exit` and swallowing exceptions—preferred when embedding in a larger app.

## Pitfalls

### Wrong: Calling a Click command like a normal function with argv
```python
import click


@click.command()
@click.option("--count", default=1)
def cmd(count: int) -> None:
    click.echo(str(count))


cmd(["--count", "3"])  # WRONG: bypasses Click's CLI parsing
```

### Right: Use `.main()` (or run under `__main__`) to parse argv
```python
import click


@click.command()
@click.option("--count", default=1, type=click.INT)
def cmd(count: int) -> None:
    click.echo(str(count))


if __name__ == "__main__":
    cmd()  # parses sys.argv

# Programmatic invocation:
# cmd.main(["--count", "3"], standalone_mode=False)
```

### Wrong: Parameter name mismatch between decorator and function signature
```python
import click


@click.command()
@click.argument("filename")
def show(file_name: str) -> None:  # WRONG: Click expects "filename"
    click.echo(file_name)
```

### Right: Match the Python argument name to the Click parameter name
```python
import click


@click.command()
@click.argument("filename")
def show(filename: str) -> None:
    click.echo(filename)


if __name__ == "__main__":
    show()
```

### Wrong: Embedding a CLI but letting Click exit the process
```python
import click


@click.command()
def cmd() -> None:
    raise click.UsageError("bad input")


def main() -> None:
    cmd.main(["cmd"])  # WRONG for embedding: may call sys.exit
```

### Right: Use `standalone_mode=False` and handle `ClickException`
```python
import click


@click.command()
def cmd() -> None:
    raise click.UsageError("bad input")


def main() -> None:
    try:
        cmd.main(["cmd"], standalone_mode=False)
    except click.ClickException as e:
        # Your app decides how to report errors.
        e.show()
        raise


if __name__ == "__main__":
    main()
```

### Wrong: Callback depending on internal “missing” sentinel behavior (8.3.x sensitive)
```python
import click


@click.command()
@click.option("--a", callback=lambda ctx, param, value: ctx.params.get("b"))
@click.option("--b")
def cmd(a: str | None, b: str | None) -> None:
    click.echo(f"a={a!r} b={b!r}")
```

### Right: Treat missing values as `None`/falsey; avoid relying on internal sentinel states
```python
import click


@click.command()
@click.option("--b")
@click.option("--a", callback=lambda ctx, param, value: (ctx.params.get("b") or value))
def cmd(a: str | None, b: str | None) -> None:
    click.echo(f"a={a!r} b={b!r}")


if __name__ == "__main__":
    cmd()
```

## References

- [Donate](https://palletsprojects.com/donate)
- [Documentation](https://click.palletsprojects.com/)
- [Changes](https://click.palletsprojects.com/page/changes/)
- [Source](https://github.com/pallets/click/)
- [Chat](https://discord.gg/pallets)

## Migration from v8.1.x

- **Python version support change (8.2.0)** ❌ Hard Deprecation (runtime constraint)
  - **Change**: Click 8.2.0+ requires Python 3.10+ (3.7–3.9 dropped).
  - **Migration guidance**: upgrade runtime to Python 3.10+ or pin Click `<8.2.0`.

- **`click.__version__` deprecated (8.2.0, ⚠️ hard deprecation in 8.3.1)** ⚠️
  - **Deprecated since**: 8.2.0 (hard deprecation/removal in 9.1)
  - **Still works**: Yes (deprecated)
  - **Modern alternative**:
    ```python
    import importlib.metadata

    version = importlib.metadata.version("click")
    print(version)
    ```
  - **Migration guidance**: stop reading `click.__version__`; use `importlib.metadata.version("click")` or feature detection.

- **`click.BaseCommand` deprecated (8.2.0, ⚠️ hard deprecation in 8.3.1)** ⚠️
  - **Deprecated since**: 8.2.0 (will be removed in 9.0)
  - **Still works**: Yes (deprecated)
  - **Modern alternative**: subclass `click.Command` (or `click.Group` for multi-command).
  - **Migration guidance**: update type checks and subclassing targets to `click.Command`.

- **`click.MultiCommand` deprecated (8.2.0, ⚠️ hard deprecation in 8.3.1)** ⚠️
  - **Deprecated since**: 8.2.0 (will be removed in 9.0)
  - **Still works**: Yes (deprecated)
  - **Modern alternative**: use `click.Group`.
  - **Migration guidance**: prefer `Group` for custom multi-command behavior.

- **Flag option handling rework (8.3.0)** ✅ Current behavior change
  - **Change**: flag option defaults are preserved and passed as-is more consistently; special-case compatibility for `default=True`.
  - **Migration guidance**: review boolean flags and explicitly set `default`, `flag_value`, and `type` to match intended runtime values.

- **Sentinel/UNSET propagation fixes (8.3.1)** ✅ Current behavior fix
  - **Change**: fixes around internal sentinel values during parsing and callbacks.
  - **Migration guidance**: callbacks should not depend on internal missing-value sentinels; treat missing values as `None`/falsey and validate explicitly.

## API Reference

- **`click.command()`** - Decorator to define a single command; supports `help`, `no_args_is_help`, etc.
- **`click.group()`** - Decorator to define a command group for subcommands.
- **`click.option()`** - Add an option; key params: `type`, `default`, `required`, `multiple`, `envvar`, `callback`, `is_flag`, `flag_value`.
- **`click.argument()`** - Add a positional argument; key params: `nargs`, `type`, `required`.
- **`click.echo()`** - Write text safely to stdout/stderr; key params: `err`, `nl`, `color`.
- **`click.secho()`** - `echo()` with styling; key params: `fg`, `bg`, `bold`, `underline`, `err`.
- **`click.style()` / `click.unstyle()`** - Apply/remove ANSI styling to strings.
- **`click.prompt()`** - Interactive prompt for input; key params: `default`, `type`, `hide_input`, `confirmation_prompt`.
- **`click.confirm()`** - Yes/no prompt; key params: `default`, `abort`.
- **`click.password_option()`** - Option decorator for masked password input; supports confirmation.
- **`click.version_option()`** - Add `--version` option; key params: `version`, `prog_name`, `message`.
- **`click.help_option()`** - Add `--help` option; key params: `help`, `hidden`.
- **`click.open_file()`** - Open files with Click-friendly behavior; key params: `mode`, `encoding`, `errors`, `atomic`.
- **`click.Path` / `click.File`** - Parameter types for paths/files with validation and automatic opening (for `File`).
- **`click.Context` / `click.get_current_context()`** - Runtime context; access params, obj, command, and manage resources via `Context.with_resource`.
- **`click.Command.main()`** - CLI entry runner; key params: `args`, `prog_name`, `standalone_mode`.
- **`click.testing.CliRunner.invoke()`** - Run a command in tests; key params: `args`, `input`, `env`, `catch_exceptions`.
- ⚠️ **`click.BaseCommand`** (deprecated; will be removed in v9.0) — use `click.Command`.
- ⚠️ **`click.MultiCommand`** (deprecated; will be removed in v9.0) — use `click.Group`.
- ⚠️ **`click.OptionParser`** (deprecated; will be removed in v9.0).
- ⚠️ **`click.__version__`** (deprecated; will be removed in v9.1) — use `importlib.metadata.version("click")`.

## Migration

**From Click v8.2.x to v8.3.1:**

- **Flag option default handling**: In v8.3.0+, the `default` value for flag options (`is_flag=True`) is now preserved and passed through as-is to your callback/functions. For legacy code, review your usage of `default` and `flag_value` on flag options. If you relied on older transformations, update your logic and tests to expect the new behavior.
- **Deprecations (hard)**: `BaseCommand`, `MultiCommand`, `OptionParser`, and `__version__` are now _hard_ deprecated and will be removed in Click 9.x. Update code to use `Command`, `Group`, and `importlib.metadata.version("click")` instead.
- **Python compatibility**: You must use Python 3.10+ for Click 8.2.0 and newer.
- **Sentinel/UNSET propagation (callbacks)**: If you use parameter callbacks, do not rely on Click's internal missing-value sentinels. Always treat missing values as `None` or another explicit value.

See [Click's changelog](https://click.palletsprojects.com/page/changes/) for full migration details.

---

**Security note:**  
All included patterns are safe for use by AI agents within the user's project directory. No destructive, exfiltrative, or privilege-modifying actions are present or permitted.