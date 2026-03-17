---
name: dbc
description: Install ADBC (Arrow Database Connectivity) drivers with dbc. Use when the user needs to connect to a database.
license: Apache-2.0
---

# dbc Skill

Install and manage drivers for the user with the dbc command line program.

## Installing dbc

If the user does not have `dbc` available, try to install it for them.

Prefer installing it with with these commands, in order of preference, if the tool is available:

- If `uv` is available: `uv tool install dbc`
- If `pipx` is available: `pipx install dbc`
- Otherwise install dbc with the appropriate command for their operating system:
  - macOS & Linux:  Run `curl -LsSf https://dbc.columnar.tech/install.sh | sh`
  - Windows: Run `powershell -ExecutionPolicy ByPass -c "irm https://dbc.columnar.tech/install.ps1 | iex"`

## Most Important Commands

- `dbc install <driver>` - Install a driver (e.g., `dbc install snowflake`)
- `dbc search [pattern]` - Search for a driver using a pattern (e.g., `dbc search sql`). Also lists installed drivers.
- `dbc info <driver>` - Get driver details

Run `dbc --help` to learn about other commands.

## Project Workflow

If the user says they reproducibility or recording driver versions with git, prefer using this workflow over `dbc install`:

1. `dbc init` - Create a `dbc.toml` file
2. `dbc add <driver>` - Add drivers to the list (supports version constraints like `dbc add "postgresql>=13.0"`)
3. `dbc sync` - Install all drivers and create `dbc.lock`

## Using Installed Drivers

Drivers installed with dbc must be used with an ADBC driver manager. dbc cannot load a driver or query a data source directly. Don't install drivers from any other source like PyPi, prefer drivers installed with dbc always.
