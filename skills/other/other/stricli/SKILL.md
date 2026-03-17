---
name: stricli
description: Build type-safe CLI applications with Stricli. Use when creating command-line tools with TypeScript, defining commands with flags/positional args, organizing multi-command CLIs with route maps, or needing compile-time parameter validation.
---

# Stricli CLI Framework

Stricli is Bloomberg's type-safe CLI framework for TypeScript. It provides compile-time type checking for command parameters, automatic help generation, and flexible command routing.

**Multi-Runtime Support:** Works with Node.js, Bun, and Deno.

## Quick Start

Create a minimal single-command CLI:

### 1. Installation

```bash
bun add @stricli/core
```

Optional packages:
```bash
bun add @stricli/auto-complete  # Shell completion support
```

### 2. Project Structure

```text
my-cli/
├── src/
│   ├── commands/
│   │   └── greet.ts      # Command implementation
│   ├── app.ts            # Application entry point
│   └── index.ts          # CLI runner
├── package.json
└── tsconfig.json
```

### 3. Define a Command (src/commands/greet.ts)

```typescript
import { buildCommand } from "@stricli/core";

export interface GreetFlags {
    readonly name: string;
    readonly shout: boolean;
}

export const greet = buildCommand({
    docs: {
        brief: "Greet a user",
        description: "Prints a greeting message to the console"
    },
    parameters: {
        flags: {
            name: {
                kind: "parsed",
                brief: "Name to greet",
                parse: String,
                default: "World"
            },
            shout: {
                kind: "boolean",
                brief: "Use uppercase",
                default: false
            }
        }
    },
    func(flags: GreetFlags) {
        const message = "Hello, " + flags.name + "!";
        console.log(flags.shout ? message.toUpperCase() : message);
    }
});
```

### 4. Build Application (src/app.ts)

```typescript
import { buildApplication } from "@stricli/core";
import { name, version, description } from "../package.json";
import { greet } from "./commands/greet";

export const app = buildApplication({
    name,
    version,
    description,
    command: greet
});
```

### 5. Run CLI (src/index.ts)

```typescript
import { run } from "@stricli/core";
import { app } from "./app";

await run(app, process.argv.slice(2));
```

### 6. Configure package.json

```json
{
  "name": "my-cli",
  "version": "1.0.0",
  "type": "module",
  "bin": {
    "my-cli": "./src/index.ts"
  },
  "scripts": {
    "start": "bun run src/index.ts"
  }
}
```

**Note:** With Bun, you can run TypeScript directly without compilation. For distribution, use `bun build` to create a standalone executable.

## Core Concepts

### buildCommand

Creates a command with typed parameters and an execution function.

```typescript
buildCommand({
    docs: { brief, description },
    parameters: { flags, positional },
    func(flags, positional, context) {
        // Implementation
    }
});
```

### buildRouteMap

Organizes multiple commands into a routed structure.

```typescript
buildRouteMap({
    routes: {
        create: createCommand,
        delete: deleteCommand,
        list: listCommand
    },
    docs: {
        brief: "Manage resources"
    }
});
```

### buildApplication

Wraps a command or route map into an executable application.

```typescript
buildApplication({
    name: "my-cli",
    version: "1.0.0",
    description: "CLI description",
    command: routeMap  // or single command
});
```

### run

Executes the application with provided arguments.

```typescript
await run(app, process.argv.slice(2), context);
```

## Parameter Types

### Flag Parameters

Flags are named parameters using `--flag-name` or `-f` syntax.

#### Boolean Flags

```typescript
flags: {
    verbose: {
        kind: "boolean",
        brief: "Enable verbose output",
        default: false
    }
}
```

Usage: `--verbose` or `--no-verbose`

#### Counter Flags

```typescript
flags: {
    verbose: {
        kind: "counter",
        brief: "Verbosity level"
    }
}
```

Usage: `-v`, `-vv`, `-vvv` (counts occurrences)

#### Enum Flags

```typescript
flags: {
    format: {
        kind: "enum",
        values: ["json", "yaml", "text"],
        brief: "Output format",
        default: "text"
    }
}
```

#### Parsed Flags

```typescript
flags: {
    port: {
        kind: "parsed",
        parse: Number,
        brief: "Port number",
        default: 3000
    }
}
```

Built-in parsers: `String`, `Number`, `numberParser`, `booleanParser`

#### Variadic Flags

```typescript
flags: {
    include: {
        kind: "variadic",
        parse: String,
        brief: "Files to include"
    }
}
```

Usage: `--include file1.ts --include file2.ts`
Result: `flags.include` is `string[]`

### Positional Parameters

Positional parameters are unnamed arguments passed by position.

#### Tuple Positional (Fixed Count)

```typescript
positional: {
    kind: "tuple",
    parameters: [
        {
            brief: "Source file",
            parse: String
        },
        {
            brief: "Destination file",
            parse: String
        }
    ]
}
```

Usage: `my-cli source.txt dest.txt`

#### Array Positional (Variable Count)

```typescript
positional: {
    kind: "array",
    parameter: {
        brief: "Files to process",
        parse: String
    }
}
```

Usage: `my-cli file1.txt file2.txt file3.txt`
Result: `positional` is `string[]`

## Workflow

### Building a Single-Command CLI

1. **Define command** - Create command file with `buildCommand`
2. **Implement function** - Add business logic in `func` property
3. **Build application** - Wrap command with `buildApplication`
4. **Run** - Execute with `run(app, args)`

### Building a Multi-Command CLI

1. **Define commands** - Create multiple command files
2. **Create route map** - Organize commands with `buildRouteMap`
3. **Build application** - Pass route map to `buildApplication`
4. **Run** - Execute with command routing: `my-cli create ...`

### Adding Custom Parsers

```typescript
const urlParser = (input: string): URL => {
    try {
        return new URL(input);
    } catch (error) {
        throw new Error(`Invalid URL: ${input}`);
    }
};

flags: {
    endpoint: {
        kind: "parsed",
        parse: urlParser,
        brief: "API endpoint URL"
    }
}
```

### Using Custom Context

Pass shared state/dependencies to all commands:

```typescript
interface AppContext {
    readonly config: Config;
    readonly logger: Logger;
}

// In func
func(flags, positional, context: AppContext) {
    context.logger.info("Running command...");
}

// When running
await run(app, args, { config, logger });
```

## Multi-Command Structure

### Nested Routes

```typescript
const projectRoutes = buildRouteMap({
    routes: {
        create: createProjectCommand,
        delete: deleteProjectCommand,
        list: listProjectsCommand
    },
    docs: { brief: "Manage projects" }
});

const taskRoutes = buildRouteMap({
    routes: {
        add: addTaskCommand,
        complete: completeTaskCommand
    },
    docs: { brief: "Manage tasks" }
});

const rootRoutes = buildRouteMap({
    routes: {
        project: projectRoutes,
        task: taskRoutes
    }
});

const app = buildApplication({
    name: "pm",
    version: "1.0.0",
    command: rootRoutes
});
```

Usage:
- `pm project create myapp`
- `pm project list`
- `pm task add "Write docs"`

### Lazy Loading

For large CLIs, use lazy loading to improve startup time:

```typescript
const routes = buildRouteMap({
    routes: {
        heavy: {
            lazy: async () => {
                const mod = await import("./commands/heavy");
                return mod.heavyCommand;
            },
            brief: "Heavy operation"
        }
    }
});
```

## Built-in Features

### Automatic Help

Stricli generates help text from `docs.brief` and `docs.description`:

```bash
my-cli --help
my-cli command --help
```

### Version Display

```bash
my-cli --version
```

## Common Patterns

### Input Validation

```typescript
func(flags) {
    if (flags.port < 1 || flags.port > 65535) {
        throw new Error("Port must be between 1 and 65535");
    }
}
```

### Async Operations

```typescript
async func(flags) {
    const data = await fetchData(flags.url);
    console.log(data);
}
```

### Error Handling

```typescript
func(flags) {
    try {
        // Operation
    } catch (error) {
        console.error(`Error: ${error.message}`);
        process.exit(1);
    }
}
```

## Testing Commands

Commands are pure functions - easy to test:

```typescript
import { test, expect } from "bun:test";
import { greet } from "./commands/greet";

test("greet with default name", () => {
    const output: string[] = [];
    const mockConsole = {
        log: (msg: string) => output.push(msg)
    };

    greet.func.call(
        { console: mockConsole },
        { name: "World", shout: false },
        undefined,
        undefined
    );

    expect(output[0]).toBe("Hello, World!");
});
```

## Reference Documentation

For detailed API documentation and complete examples, see:

- **[Commands](./references/commands.md)** - buildCommand, func signature, aliases, type safety
- **[Parameters](./references/parameters.md)** - Flag types (boolean, counter, enum, parsed, variadic) and positional types (tuple, array)
- **[Parsers](./references/parsers.md)** - Built-in parsers, custom parsers, error handling
- **[Routing](./references/routing.md)** - buildRouteMap, buildApplication, run, lazy loading, scanner config
- **[Context](./references/context.md)** - Custom context, LocalContext, exit codes
- **[Auto-Complete](./references/auto-complete.md)** - Shell completion with @stricli/auto-complete
- **[Examples](./references/examples.md)** - Complete working examples including multi-command CLIs, custom parsers, and advanced patterns

## Additional Resources

- [Stricli GitHub](https://github.com/bloomberg/stricli)
- [Official Documentation](https://bloomberg.github.io/stricli/)
- [NPM Package](https://www.npmjs.com/package/@stricli/core)

## When to Use Stricli

**Use Stricli when:**
- Building TypeScript CLIs with type safety
- Need compile-time parameter validation
- Want automatic help generation
- Building multi-command CLIs with routing
- Need complex parameter parsing

**Consider alternatives when:**
- Building simple scripts (native process.argv may suffice)
- Working in pure JavaScript (no TypeScript)
- Need different paradigm (e.g., inquirer for prompts)
