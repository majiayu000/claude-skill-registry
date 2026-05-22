---
name: cli-builder
description: Expert guide for building command-line interfaces with Node.js (Commander, Inquirer, Ora) or Python (Click, Typer, Rich). Use when creating CLI tools, terminal UX, argument parsing, or interactive prompts.
---

# CLI Builder Skill

## Overview

This skill helps you build professional command-line interfaces with excellent user experience. Covers argument parsing, interactive prompts, progress indicators, colored output, and cross-platform compatibility.

## CLI Design Philosophy

### Principles of Good CLI Design
1. **Predictable**: Follow conventions users expect
2. **Helpful**: Provide clear help text and error messages
3. **Composable**: Work well with pipes and other tools
4. **Forgiving**: Accept common variations in input

### Design Guidelines
- **DO**: Use conventional flag names (`-v`, `--verbose`, `-h`, `--help`)
- **DO**: Provide meaningful exit codes
- **DO**: Support `--version` and `--help` on all commands
- **DO**: Use colors meaningfully (errors=red, success=green)
- **DON'T**: Require interactive input when running in pipes
- **DON'T**: Print to stdout when outputting errors
- **DON'T**: Ignore signals (Ctrl+C should exit cleanly)

## Node.js CLI Development

### Project Setup

```bash
# Initialize CLI project
mkdir my-cli && cd my-cli
npm init -y

# Install core dependencies
npm install commander chalk ora inquirer

# Optional: TypeScript support
npm install -D typescript @types/node @types/inquirer ts-node
```

### Package.json Configuration

```json
{
  "name": "my-cli",
  "version": "1.0.0",
  "description": "A powerful CLI tool",
  "bin": {
    "mycli": "./bin/cli.js"
  },
  "files": [
    "bin",
    "dist"
  ],
  "scripts": {
    "build": "tsc",
    "dev": "ts-node src/cli.ts",
    "link": "npm link"
  },
  "engines": {
    "node": ">=18.0.0"
  }
}
```

### Commander.js - Command Structure

```typescript
// src/cli.ts
import { Command } from 'commander';
import { version } from '../package.json';

const program = new Command();

program
  .name('mycli')
  .description('A powerful CLI for doing awesome things')
  .version(version, '-v, --version', 'Display version number');

// Simple command
program
  .command('init')
  .description('Initialize a new project')
  .argument('[name]', 'Project name', 'my-project')
  .option('-t, --template <type>', 'Template to use', 'default')
  .option('--no-git', 'Skip git initialization')
  .option('-f, --force', 'Overwrite existing files')
  .action(async (name, options) => {
    console.log(`Creating project: ${name}`);
    console.log(`Template: ${options.template}`);
    console.log(`Git: ${options.git}`);
  });

// Command with subcommands
const config = program
  .command('config')
  .description('Manage configuration');

config
  .command('get <key>')
  .description('Get a configuration value')
  .action((key) => {
    console.log(`Getting config: ${key}`);
  });

config
  .command('set <key> <value>')
  .description('Set a configuration value')
  .action((key, value) => {
    console.log(`Setting ${key} = ${value}`);
  });

config
  .command('list')
  .description('List all configuration')
  .option('--json', 'Output as JSON')
  .action((options) => {
    if (options.json) {
      console.log(JSON.stringify({ key: 'value' }, null, 2));
    } else {
      console.log('key = value');
    }
  });

// Parse arguments
program.parse();
```

### Chalk - Colored Output

```typescript
// src/utils/logger.ts
import chalk from 'chalk';

export const logger = {
  info: (msg: string) => console.log(chalk.blue('info'), msg),
  success: (msg: string) => console.log(chalk.green('success'), msg),
  warning: (msg: string) => console.log(chalk.yellow('warning'), msg),
  error: (msg: string) => console.error(chalk.red('error'), msg),

  // Styled output
  title: (msg: string) => console.log(chalk.bold.underline(msg)),
  dim: (msg: string) => console.log(chalk.dim(msg)),

  // Formatted output
  list: (items: string[]) => {
    items.forEach(item => console.log(chalk.gray('  -'), item));
  },

  // Table-like output
  keyValue: (pairs: Record<string, string>) => {
    const maxKeyLen = Math.max(...Object.keys(pairs).map(k => k.length));
    Object.entries(pairs).forEach(([key, value]) => {
      console.log(
        chalk.cyan(key.padEnd(maxKeyLen)),
        chalk.gray(':'),
        value
      );
    });
  }
};

// Usage
logger.title('Project Configuration');
logger.keyValue({
  'Name': 'my-project',
  'Template': 'typescript',
  'Version': '1.0.0'
});
```

### Ora - Progress Spinners

```typescript
// src/utils/spinner.ts
import ora, { Ora } from 'ora';

export function createSpinner(text: string): Ora {
  return ora({
    text,
    spinner: 'dots',
    color: 'cyan'
  });
}

// Usage patterns
async function downloadWithProgress() {
  const spinner = createSpinner('Downloading dependencies...');
  spinner.start();

  try {
    await downloadFiles();
    spinner.succeed('Dependencies downloaded');
  } catch (error) {
    spinner.fail('Download failed');
    throw error;
  }
}

// Sequential spinners
async function setupProject() {
  const steps = [
    { text: 'Creating directory structure', fn: createDirs },
    { text: 'Installing dependencies', fn: installDeps },
    { text: 'Initializing git', fn: initGit },
    { text: 'Configuring project', fn: configure }
  ];

  for (const step of steps) {
    const spinner = createSpinner(step.text);
    spinner.start();
    try {
      await step.fn();
      spinner.succeed();
    } catch (error) {
      spinner.fail();
      throw error;
    }
  }
}
```

### Inquirer - Interactive Prompts

```typescript
// src/prompts/init.ts
import inquirer from 'inquirer';

interface ProjectAnswers {
  name: string;
  template: string;
  features: string[];
  initGit: boolean;
  installDeps: boolean;
}

export async function promptProjectSetup(): Promise<ProjectAnswers> {
  return inquirer.prompt([
    {
      type: 'input',
      name: 'name',
      message: 'Project name:',
      default: 'my-project',
      validate: (input) => {
        if (!/^[a-z0-9-]+$/.test(input)) {
          return 'Name must be lowercase alphanumeric with dashes';
        }
        return true;
      }
    },
    {
      type: 'list',
      name: 'template',
      message: 'Select a template:',
      choices: [
        { name: 'Minimal - Basic setup', value: 'minimal' },
        { name: 'Standard - Recommended defaults', value: 'standard' },
        { name: 'Full - Kitchen sink', value: 'full' }
      ],
      default: 'standard'
    },
    {
      type: 'checkbox',
      name: 'features',
      message: 'Select features:',
      choices: [
        { name: 'TypeScript', value: 'typescript', checked: true },
        { name: 'ESLint', value: 'eslint', checked: true },
        { name: 'Prettier', value: 'prettier', checked: true },
        { name: 'Testing (Jest)', value: 'jest' },
        { name: 'CI/CD (GitHub Actions)', value: 'github-actions' }
      ]
    },
    {
      type: 'confirm',
      name: 'initGit',
      message: 'Initialize git repository?',
      default: true
    },
    {
      type: 'confirm',
      name: 'installDeps',
      message: 'Install dependencies now?',
      default: true,
      when: (answers) => answers.template !== 'minimal'
    }
  ]);
}

// Advanced: Dynamic prompts
export async function promptWithContext(context: { hasExisting: boolean }) {
  const questions = [];

  if (context.hasExisting) {
    questions.push({
      type: 'confirm',
      name: 'overwrite',
      message: 'Directory exists. Overwrite?',
      default: false
    });
  }

  // Add more questions...

  return inquirer.prompt(questions);
}
```

### Complete CLI Example

```typescript
#!/usr/bin/env node
// bin/cli.ts

import { Command } from 'commander';
import chalk from 'chalk';
import ora from 'ora';
import inquirer from 'inquirer';
import { existsSync, mkdirSync, writeFileSync } from 'fs';
import { join } from 'path';

const program = new Command();

program
  .name('create-app')
  .description('Create a new application')
  .version('1.0.0');

program
  .command('create')
  .argument('[name]', 'Project name')
  .option('-t, --template <template>', 'Template to use')
  .option('-y, --yes', 'Skip prompts with defaults')
  .action(async (name, options) => {
    try {
      // Get project name if not provided
      if (!name) {
        const { projectName } = await inquirer.prompt([{
          type: 'input',
          name: 'projectName',
          message: 'Project name:',
          default: 'my-app'
        }]);
        name = projectName;
      }

      // Check if directory exists
      const projectDir = join(process.cwd(), name);
      if (existsSync(projectDir)) {
        const { overwrite } = await inquirer.prompt([{
          type: 'confirm',
          name: 'overwrite',
          message: `Directory ${name} exists. Overwrite?`,
          default: false
        }]);

        if (!overwrite) {
          console.log(chalk.yellow('Aborted.'));
          process.exit(0);
        }
      }

      // Get template if not provided
      let template = options.template;
      if (!template && !options.yes) {
        const { selectedTemplate } = await inquirer.prompt([{
          type: 'list',
          name: 'selectedTemplate',
          message: 'Select template:',
          choices: ['minimal', 'standard', 'typescript']
        }]);
        template = selectedTemplate;
      }
      template = template || 'standard';

      console.log();
      console.log(chalk.bold(`Creating ${name} with ${template} template...`));
      console.log();

      // Create project
      const spinner = ora('Creating directory structure').start();
      mkdirSync(projectDir, { recursive: true });
      spinner.succeed();

      spinner.start('Generating files');
      writeFileSync(
        join(projectDir, 'package.json'),
        JSON.stringify({ name, version: '1.0.0' }, null, 2)
      );
      spinner.succeed();

      // Success message
      console.log();
      console.log(chalk.green.bold('Success!'), `Created ${name}`);
      console.log();
      console.log('Next steps:');
      console.log(chalk.cyan(`  cd ${name}`));
      console.log(chalk.cyan('  npm install'));
      console.log(chalk.cyan('  npm start'));
      console.log();

    } catch (error) {
      console.error(chalk.red('Error:'), error.message);
      process.exit(1);
    }
  });

// Handle unknown commands
program.on('command:*', () => {
  console.error(chalk.red('Unknown command:'), program.args.join(' '));
  console.log('Run', chalk.cyan('create-app --help'), 'for usage');
  process.exit(1);
});

// Parse and handle no command
program.parse();

if (!process.argv.slice(2).length) {
  program.help();
}
```

## Python CLI Development

### Typer - Modern Python CLI

```python
# cli.py
import typer
from typing import Optional, List
from enum import Enum
from rich.console import Console
from rich.table import Table
from rich.progress import track

app = typer.Typer(
    name="mycli",
    help="A powerful CLI for doing awesome things",
    add_completion=True
)
console = Console()


class Template(str, Enum):
    minimal = "minimal"
    standard = "standard"
    full = "full"


@app.command()
def init(
    name: str = typer.Argument("my-project", help="Project name"),
    template: Template = typer.Option(
        Template.standard,
        "--template", "-t",
        help="Template to use"
    ),
    features: List[str] = typer.Option(
        [],
        "--feature", "-f",
        help="Features to include"
    ),
    no_git: bool = typer.Option(
        False,
        "--no-git",
        help="Skip git initialization"
    ),
    force: bool = typer.Option(
        False,
        "--force", "-f",
        help="Overwrite existing files"
    )
):
    """Initialize a new project."""
    console.print(f"[bold]Creating project:[/bold] {name}")
    console.print(f"[dim]Template:[/dim] {template.value}")

    # Progress indicator
    for step in track(range(5), description="Setting up..."):
        # Do work
        pass

    console.print("[green]Success![/green] Project created")


@app.command()
def config(
    key: str = typer.Argument(..., help="Configuration key"),
    value: Optional[str] = typer.Argument(None, help="Value to set")
):
    """Get or set configuration values."""
    if value is None:
        # Get config
        console.print(f"{key} = some_value")
    else:
        # Set config
        console.print(f"Set {key} = {value}")


@app.command()
def status():
    """Show project status."""
    table = Table(title="Project Status")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Name", "my-project")
    table.add_row("Version", "1.0.0")
    table.add_row("Template", "standard")

    console.print(table)


# Subcommand group
db_app = typer.Typer(help="Database operations")
app.add_typer(db_app, name="db")


@db_app.command("migrate")
def db_migrate(
    direction: str = typer.Option("up", "--direction", "-d"),
    steps: int = typer.Option(1, "--steps", "-n")
):
    """Run database migrations."""
    console.print(f"Running {steps} migration(s) {direction}")


@db_app.command("seed")
def db_seed():
    """Seed the database."""
    console.print("Seeding database...")


if __name__ == "__main__":
    app()
```

### Click - Flexible Python CLI

```python
# cli_click.py
import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


@click.group()
@click.version_option(version="1.0.0")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.pass_context
def cli(ctx, verbose):
    """A powerful CLI for doing awesome things."""
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose


@cli.command()
@click.argument("name", default="my-project")
@click.option(
    "--template", "-t",
    type=click.Choice(["minimal", "standard", "full"]),
    default="standard",
    help="Template to use"
)
@click.option("--no-git", is_flag=True, help="Skip git initialization")
@click.confirmation_option(prompt="Create project?")
@click.pass_context
def init(ctx, name, template, no_git):
    """Initialize a new project."""
    if ctx.obj["verbose"]:
        console.print(f"[dim]Verbose mode enabled[/dim]")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task("Creating project...", total=None)
        # Do work
        import time
        time.sleep(1)

    console.print(f"[green]Created {name} with {template} template[/green]")


@cli.group()
def config():
    """Manage configuration."""
    pass


@config.command("get")
@click.argument("key")
def config_get(key):
    """Get a configuration value."""
    console.print(f"{key} = value")


@config.command("set")
@click.argument("key")
@click.argument("value")
def config_set(key, value):
    """Set a configuration value."""
    console.print(f"Set {key} = {value}")


@cli.command()
@click.option("--format", "-f", type=click.Choice(["text", "json"]), default="text")
def status(format):
    """Show project status."""
    if format == "json":
        click.echo('{"status": "ok"}')
    else:
        console.print("[bold]Status:[/bold] OK")


if __name__ == "__main__":
    cli()
```

## Advanced Patterns

### Configuration Management

```typescript
// src/config.ts
import { homedir } from 'os';
import { join } from 'path';
import { existsSync, readFileSync, writeFileSync, mkdirSync } from 'fs';

interface Config {
  apiKey?: string;
  defaultTemplate?: string;
  analytics?: boolean;
}

class ConfigManager {
  private configDir: string;
  private configPath: string;
  private config: Config;

  constructor() {
    this.configDir = join(homedir(), '.mycli');
    this.configPath = join(this.configDir, 'config.json');
    this.config = this.load();
  }

  private load(): Config {
    if (!existsSync(this.configPath)) {
      return {};
    }
    try {
      return JSON.parse(readFileSync(this.configPath, 'utf-8'));
    } catch {
      return {};
    }
  }

  private save(): void {
    if (!existsSync(this.configDir)) {
      mkdirSync(this.configDir, { recursive: true });
    }
    writeFileSync(this.configPath, JSON.stringify(this.config, null, 2));
  }

  get<K extends keyof Config>(key: K): Config[K] {
    return this.config[key];
  }

  set<K extends keyof Config>(key: K, value: Config[K]): void {
    this.config[key] = value;
    this.save();
  }

  getAll(): Config {
    return { ...this.config };
  }

  clear(): void {
    this.config = {};
    this.save();
  }
}

export const config = new ConfigManager();
```

### Error Handling

```typescript
// src/errors.ts
import chalk from 'chalk';

export class CLIError extends Error {
  constructor(
    message: string,
    public readonly code: string = 'ERROR',
    public readonly suggestion?: string
  ) {
    super(message);
    this.name = 'CLIError';
  }
}

export function handleError(error: unknown): never {
  if (error instanceof CLIError) {
    console.error(chalk.red(`Error [${error.code}]:`), error.message);
    if (error.suggestion) {
      console.error(chalk.yellow('Suggestion:'), error.suggestion);
    }
    process.exit(1);
  }

  if (error instanceof Error) {
    console.error(chalk.red('Unexpected error:'), error.message);
    if (process.env.DEBUG) {
      console.error(error.stack);
    }
    process.exit(1);
  }

  console.error(chalk.red('Unknown error occurred'));
  process.exit(1);
}

// Usage
process.on('uncaughtException', handleError);
process.on('unhandledRejection', handleError);
```

### Non-Interactive Mode Detection

```typescript
// src/utils/tty.ts
import { stdin, stdout } from 'process';

export function isInteractive(): boolean {
  return stdin.isTTY && stdout.isTTY;
}

export function requireInteractive(message?: string): void {
  if (!isInteractive()) {
    console.error(message || 'This command requires an interactive terminal');
    process.exit(1);
  }
}

// Usage in command
async function initCommand(options: { yes?: boolean }) {
  if (options.yes || !isInteractive()) {
    // Use defaults, skip prompts
    return runWithDefaults();
  }

  // Interactive prompts
  const answers = await promptUser();
  return runWithAnswers(answers);
}
```

### Output Formatting

```typescript
// src/utils/output.ts
import { stdout } from 'process';

export type OutputFormat = 'text' | 'json' | 'table';

export function output(data: unknown, format: OutputFormat = 'text'): void {
  switch (format) {
    case 'json':
      console.log(JSON.stringify(data, null, 2));
      break;
    case 'table':
      console.table(data);
      break;
    case 'text':
    default:
      if (typeof data === 'string') {
        console.log(data);
      } else {
        console.log(JSON.stringify(data, null, 2));
      }
  }
}

// Check if output is piped
export function isPiped(): boolean {
  return !stdout.isTTY;
}

// Suppress decorative output when piped
export function log(message: string): void {
  if (!isPiped()) {
    console.log(message);
  }
}
```

## CLI Checklist

### Core Features
- [ ] `--help` on all commands
- [ ] `--version` flag
- [ ] Meaningful exit codes
- [ ] Error messages to stderr
- [ ] Support for environment variables

### User Experience
- [ ] Progress indicators for long operations
- [ ] Colored output (with `NO_COLOR` support)
- [ ] Interactive prompts (with non-interactive fallback)
- [ ] Tab completion setup

### Best Practices
- [ ] Works in pipes (`echo "data" | mycli process`)
- [ ] Handles Ctrl+C gracefully
- [ ] Configuration file support
- [ ] Debug/verbose mode
- [ ] Consistent command structure

### Distribution
- [ ] npm/PyPI package configured
- [ ] Binary entry point set up
- [ ] README with installation and usage
- [ ] Changelog maintained

## When to Use This Skill

Invoke this skill when:
- Creating new CLI tools from scratch
- Adding commands to existing CLIs
- Building interactive prompts and wizards
- Implementing progress indicators
- Setting up argument parsing
- Creating configuration management
- Designing CLI UX patterns
- Publishing CLI tools to npm or PyPI
