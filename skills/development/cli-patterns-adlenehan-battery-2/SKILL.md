---
name: cli-patterns
description: Patterns for building Battery CLI commands with Commander.js. Use this skill when creating new CLI commands, adding options/flags, formatting output, handling errors, or implementing interactive prompts.
---

# CLI Patterns

## Command Structure

Use Commander.js for all CLI commands. Commands live in `packages/cli/src/commands/`.

### Basic Command

```typescript
import { Command } from 'commander'

export const deployCommand = new Command('deploy')
  .description('Deploy an application to Battery')
  .argument('<path>', 'Path to the application directory')
  .option('-e, --env <environment>', 'Target environment', 'production')
  .option('--dry-run', 'Show what would be deployed without deploying')
  .action(async (path, options) => {
    // Implementation
  })
```

### Command with Subcommands

```typescript
export const configCommand = new Command('config')
  .description('Manage Battery configuration')

configCommand
  .command('set <key> <value>')
  .description('Set a configuration value')
  .action(async (key, value) => {})

configCommand
  .command('get <key>')
  .description('Get a configuration value')
  .action(async (key) => {})
```

## Output Formatting

### Chalk for Colors

```typescript
import chalk from 'chalk'

// Status messages
console.log(chalk.green('✓'), 'Deployment successful')
console.log(chalk.yellow('!'), 'Warning: No auth detected')
console.log(chalk.red('✗'), 'Error: Invalid credentials')

// Emphasis
console.log(chalk.bold('Scanning...'))
console.log(chalk.dim('Press Ctrl+C to cancel'))

// URLs and paths
console.log(chalk.cyan('https://app.battery.dev'))
console.log(chalk.gray('./src/config.ts'))
```

### Ora for Spinners

```typescript
import ora from 'ora'

const spinner = ora('Scanning for credentials...').start()

try {
  const results = await scan(path)
  spinner.succeed('Scan complete')
} catch (error) {
  spinner.fail('Scan failed')
  throw error
}
```

### Tree Output

```typescript
function printTree(items: string[], indent = 0): void {
  const prefix = '  '.repeat(indent)
  items.forEach((item, i) => {
    const isLast = i === items.length - 1
    const branch = isLast ? '└──' : '├──'
    console.log(`${prefix}${branch} ${item}`)
  })
}

// Output:
// ├── Detected: Next.js
// ├── Found credentials:
// │   ├── SNOWFLAKE_PASSWORD in .env
// │   └── SALESFORCE_TOKEN in lib/api.ts
// └── Deploying...
```

## Error Handling

### Exit Codes

```typescript
export const ExitCode = {
  Success: 0,
  GeneralError: 1,
  InvalidArgument: 2,
  ConfigError: 3,
  NetworkError: 4,
  AuthError: 5,
} as const

process.exit(ExitCode.InvalidArgument)
```

### Error Display

```typescript
import chalk from 'chalk'

function handleError(error: Error): never {
  console.error()
  console.error(chalk.red('Error:'), error.message)

  if (error.cause) {
    console.error(chalk.dim('Cause:'), String(error.cause))
  }

  if (process.env.DEBUG) {
    console.error(chalk.dim(error.stack))
  }

  process.exit(ExitCode.GeneralError)
}
```

### Graceful Shutdown

```typescript
process.on('SIGINT', () => {
  console.log()
  console.log(chalk.dim('Cancelled'))
  process.exit(130)
})
```

## Interactive Prompts

Use @inquirer/prompts for user input.

### Confirmation

```typescript
import { confirm } from '@inquirer/prompts'

const proceed = await confirm({
  message: 'Deploy to production?',
  default: false,
})
```

### Selection

```typescript
import { select } from '@inquirer/prompts'

const environment = await select({
  message: 'Select environment',
  choices: [
    { name: 'Production', value: 'production' },
    { name: 'Staging', value: 'staging' },
    { name: 'Development', value: 'development' },
  ],
})
```

### Text Input

```typescript
import { input } from '@inquirer/prompts'

const projectName = await input({
  message: 'Project name',
  default: path.basename(process.cwd()),
  validate: (value) => {
    if (!/^[a-z0-9-]+$/.test(value)) {
      return 'Must be lowercase alphanumeric with hyphens'
    }
    return true
  },
})
```

### Password Input

```typescript
import { password } from '@inquirer/prompts'

const token = await password({
  message: 'Enter your API token',
  mask: '*',
})
```

## Configuration Files

### Config Location

```typescript
import { homedir } from 'os'
import { join } from 'path'

const CONFIG_DIR = join(homedir(), '.battery')
const CONFIG_FILE = join(CONFIG_DIR, 'config.json')
const CREDENTIALS_FILE = join(CONFIG_DIR, 'credentials.json')
```

### Config Schema

```typescript
interface BatteryConfig {
  defaultOrg?: string
  defaultEnvironment?: 'production' | 'staging'
  telemetry?: boolean
}
```

## Patterns to Follow

1. **Always show progress** - Use spinners for operations > 500ms
2. **Confirm destructive actions** - Prompt before deleting or overwriting
3. **Support --json flag** - For programmatic output
4. **Respect NO_COLOR** - Disable colors when env var is set
5. **Use stderr for errors** - Keep stdout clean for piping
