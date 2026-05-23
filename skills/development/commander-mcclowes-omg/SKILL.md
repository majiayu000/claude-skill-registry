---
name: commander
# prettier-ignore
description: Use when building CLI tools with Commander.js - commands, options, arguments, and help text for Node.js command-line applications
---

# Commander.js CLI Framework

## Quick Start

```typescript
import { Command } from 'commander';

const program = new Command();

program
  .name('mycli')
  .version('1.0.0')
  .description('My CLI tool');

program
  .command('build <input>')
  .description('Build the project')
  .option('-o, --output <file>', 'Output file', 'output.json')
  .option('-w, --watch', 'Watch mode')
  .option('-v, --verbose', 'Verbose output')
  .action((input, options) => {
    console.log(`Building ${input} to ${options.output}`);
    if (options.watch) startWatcher();
  });

program.parse();
```

## Command Patterns

| Pattern | Syntax | Description |
|---------|--------|-------------|
| Required arg | `<name>` | Must be provided |
| Optional arg | `[name]` | Can be omitted |
| Variadic | `<files...>` | Multiple values |
| Option value | `-o, --out <file>` | Option with value |
| Boolean flag | `-v, --verbose` | True when present |
| Negatable | `--no-cache` | Sets cache=false |

## Subcommands

```typescript
const build = program.command('build');

build
  .command('dev')
  .description('Development build')
  .action(() => { /* ... */ });

build
  .command('prod')
  .description('Production build')
  .action(() => { /* ... */ });
```

## Key Features

```typescript
// Default values
.option('-p, --port <number>', 'Port', '3000')

// Coercion
.option('-n, --number <n>', 'A number', parseInt)

// Required options
.requiredOption('-c, --config <path>', 'Config file')

// Choices
.option('-e, --env <env>', 'Environment').choices(['dev', 'prod'])

// Error handling
program.exitOverride(); // Throw instead of process.exit
program.configureOutput({ writeErr: (str) => logger.error(str) });
```

## Tips

- Use `program.parse()` at the end, or `program.parseAsync()` for async
- Access args via action callback or `program.args`
- Use `.alias('b')` for command shortcuts
- Add examples with `.addHelpText('after', 'Examples:\n  $ mycli build src/')`
