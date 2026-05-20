---
name: e3
description: "East Execution Engine (e3) - durable dataflow execution for East programs. Use when: (1) Authoring e3 packages with @elaraai/e3 (e3.input, e3.task, e3.package, e3.export), (2) Running e3 CLI commands (e3 repo create, e3 start, e3 watch, e3 get, e3 set), (3) Working with workspaces and packages, (4) Content-addressable caching and dataflow execution."
---

# East Execution Engine (e3)

e3 is a durable dataflow execution engine for East programs with content-addressable caching.

## Quick Start

```typescript
// src/index.ts
import { East, StringType } from '@elaraai/east';
import e3 from '@elaraai/e3';

// Define an input
const name = e3.input('name', StringType, 'World');

// Define a task
const greet = e3.task(
  'greet',
  [name],
  East.function([StringType], StringType, ($, n) =>
    East.str`Hello, ${n}!`
  )
);

// Bundle and export
const pkg = e3.package('hello', '1.0.0', greet);
await e3.export(pkg, '/tmp/hello.zip');
export default pkg;
```

```bash
# Create repository
e3 repo create .

# Import and deploy
e3 package import . /tmp/hello.zip
e3 workspace create . dev
e3 workspace deploy . dev hello@1.0.0

# Execute dataflow
e3 start . dev

# Get result
e3 get . dev.tasks.greet.output
```

## SDK Reference (@elaraai/e3)

### e3.input(name, type, defaultValue?)

Define an input dataset at `.inputs.${name}`.

```typescript
const name = e3.input('name', StringType, 'default');
const count = e3.input('count', IntegerType);
```

### e3.task(name, inputs, fn, config?)

Define a task that runs an East function.

```typescript
const greet = e3.task(
  'greet',
  [name],  // dependencies (inputs or other task outputs)
  East.function([StringType], StringType, ($, n) =>
    East.str`Hello, ${n}!`
  )
);

// With custom runner
const pyTask = e3.task(
  'py_task',
  [input],
  East.function([IntegerType], IntegerType, ($, x) => x.multiply(2n)),
  { runner: ['uv', 'run', 'east-py', 'run', '-p', 'east-py-std'] }
);

// Chain tasks via .output
const shout = e3.task(
  'shout',
  [greet.output],
  East.function([StringType], StringType, ($, s) => s.toUpperCase())
);
```

### e3.customTask(name, inputs, outputType, command)

Define a task that runs a shell command.

```typescript
const process = e3.customTask(
  'process',
  [rawData],
  StringType,
  ($, input_paths, output_path) =>
    East.str`python script.py -i ${input_paths.get(0n)} -o ${output_path}`
);
```

### e3.package(name, version, ...items)

Bundle into a package. Dependencies are collected automatically.

```typescript
const pkg = e3.package('myapp', '1.0.0', finalTask);
```

### e3.export(pkg, zipPath)

Export package to a .zip file.

```typescript
await e3.export(pkg, '/tmp/myapp.zip');
```

## CLI Reference

### Repository Commands

```bash
e3 repo create <repo>             # Create a new repository
e3 repo status <repo>             # Show repository status
e3 repo remove <repo>             # Remove a repository
e3 repo gc <repo> [--dry-run]     # Garbage collect unreferenced objects
```

### Package Commands

```bash
e3 package import <repo> <zipPath>       # Import from .zip
e3 package export <repo> <pkg> <zipPath> # Export to .zip
e3 package list <repo>                   # List packages
e3 package remove <repo> <pkg>           # Remove package
```

### Workspace Commands

```bash
e3 workspace create <repo> <name>           # Create workspace
e3 workspace deploy <repo> <ws> <pkg[@ver]> # Deploy package
e3 workspace export <repo> <ws> <zipPath>   # Export workspace
e3 workspace list <repo>                    # List workspaces
e3 workspace status <repo> <ws>             # Show workspace status
e3 workspace remove <repo> <ws>             # Remove workspace
```

### Data Commands

```bash
e3 list <repo> [path]                       # List tree contents
e3 tree <repo> <path>                       # Show full tree structure
e3 get <repo> <path> [-f east|json|beast2]  # Get dataset value
e3 set <repo> <path> <file> [--type <spec>] # Set dataset from file
```

Path format: `workspace.path.to.dataset`

```bash
e3 get . dev.inputs.name
e3 get . dev.tasks.greet.output
e3 set . dev.inputs.name data.east
```

### Execution Commands

```bash
e3 start <repo> <ws> [--filter] [--concurrency <n>] [--force]
e3 run <repo> <pkg/task> [inputs...] -o <output>
e3 watch <repo> <ws> <source.ts> [--start] [--abort-on-change]
e3 logs <repo> <path> [--follow]
```

### Utility Commands

```bash
e3 convert [input] [--from <fmt>] [--to <fmt>] [-o <output>]
```

### Authentication (for remote servers)

```bash
e3 login <url>                    # Authenticate with remote server
e3 logout <url>                   # Clear stored credentials
e3 auth status                    # Show authentication status
```

### Remote URLs

All commands accept HTTP URLs instead of local paths:

```bash
# Start a server
e3-api-server --repos ./repos --port 3000

# Use remote repository
e3 repo create http://localhost:3000/repos/my-repo
e3 workspace list http://localhost:3000/repos/my-repo
e3 package import http://localhost:3000/repos/my-repo ./pkg.zip
```

## Development Workflow

### Watch Mode (recommended)

```bash
e3 watch . dev ./src/index.ts --start
```

Auto-compiles, deploys, and runs on file changes.

### Manual Workflow

```bash
npm run build && npm run main
e3 package import . /tmp/pkg.zip
e3 workspace deploy . dev myapp@1.0.0
e3 start . dev
```

## Packages

| Package | Description |
|---------|-------------|
| `@elaraai/e3` | SDK: e3.input, e3.task, e3.package, e3.export |
| `@elaraai/e3-types` | Shared type definitions |
| `@elaraai/e3-core` | Core library (workspaces, execution, caching) |
| `@elaraai/e3-cli` | CLI tool |
| `@elaraai/e3-api-client` | HTTP client for remote servers |
| `@elaraai/e3-api-server` | REST API server |

## Project Structure

```
my-project/
├── package.json
├── tsconfig.json
├── pyproject.toml      # For Python runner
├── src/
│   └── index.ts        # Package definition
└── repo/               # Repository (created by e3 repo create)
    ├── objects/        # Content-addressable object store
    ├── packages/       # Package metadata
    └── workspaces/     # Workspace state
```

## Caching

Tasks are cached by content hash. Re-runs only when:
- Task's East function IR changes
- Input values change

Use `--force` to bypass: `e3 start . dev --force`
