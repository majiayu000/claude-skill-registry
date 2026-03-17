---
name: cli-developer
description: Expert in building Command Line Interfaces (CLIs), Terminal User Interfaces (TUIs), and shell automation tools. Use when creating CLI applications, building interactive terminal UIs, parsing command-line arguments, or developing shell scripts and automation tools.
---

# CLI Developer

## Purpose
Provides expertise in building robust, user-friendly command-line applications and terminal interfaces. Covers argument parsing, interactive prompts, TUI frameworks, and shell automation across multiple languages.

## When to Use
- Building CLI applications in any language
- Creating interactive terminal user interfaces
- Implementing command-line argument parsing
- Building shell scripts and automation tools
- Adding progress bars, spinners, and colors
- Creating REPL-style applications
- Distributing CLI tools as packages

## Quick Start
**Invoke this skill when:**
- Building CLI applications in any language
- Creating interactive terminal user interfaces
- Implementing command-line argument parsing
- Building shell scripts and automation tools
- Creating REPL-style applications

**Do NOT invoke when:**
- Building GUI desktop applications (use windows-app-developer)
- Creating web-based interfaces (use frontend skills)
- Writing PowerShell-specific tools (use powershell skills)
- Building mobile applications (use mobile-developer)

## Decision Framework
```
CLI Framework Selection:
├── Node.js → Commander.js, Yargs, Oclif
├── Python → Click, Typer, argparse
├── Go → Cobra, urfave/cli
├── Rust → Clap, structopt
├── TUI needed
│   ├── Node.js → Ink, Blessed
│   ├── Python → Textual, Rich
│   ├── Go → Bubbletea, tview
│   └── Rust → Ratatui, crossterm
└── Simple script → Shell (bash/zsh)
```

## Core Workflows

### 1. CLI Application Setup
1. Choose framework based on language/needs
2. Define command structure and subcommands
3. Implement argument and option parsing
4. Add input validation and help text
5. Implement core command logic
6. Add output formatting (JSON, table, etc.)
7. Package for distribution

### 2. Interactive TUI Development
1. Select TUI framework
2. Design screen layout and components
3. Implement input handling and navigation
4. Add state management
5. Handle terminal resize events
6. Test across different terminal emulators

### 3. CLI Distribution
1. Add proper versioning
2. Create man pages or help docs
3. Package for target platforms
4. Set up installation via package managers
5. Create shell completions
6. Add update mechanism

## Best Practices
- Follow POSIX conventions for flags and arguments
- Provide both short (-v) and long (--verbose) options
- Include --help and --version flags
- Use exit codes properly (0 for success)
- Support piping and stdin input
- Add shell completion scripts

## Anti-Patterns
| Anti-Pattern | Problem | Correct Approach |
|--------------|---------|------------------|
| No help text | Users can't discover commands | Add comprehensive --help |
| Silent failures | Users don't know what went wrong | Clear error messages + exit codes |
| Hard-coded paths | Breaks on other systems | Use environment variables, XDG |
| No stdin support | Can't pipe data | Support reading from stdin |
| Colored output to pipes | Breaks parsing | Detect TTY, disable colors for pipes |
