---
name: cli-core
description: Core patterns for Effect CLI - Command.make, Args, Options, subcommands, and program structure. Foundation skill for TMNL CLI framework.
model_invoked: true
triggers:
  - "CLI"
  - "Command.make"
  - "effect/cli"
  - "@effect/cli"
  - "Args"
  - "Options"
  - "subcommand"
  - "create CLI"
  - "build CLI"
---

# CLI Core Patterns

Foundation patterns for building CLIs with `@effect/cli`. Part of the TMNL CLI Framework.

## Quick Start

```typescript
#!/usr/bin/env bun
import { Args, Command, Options } from "@effect/cli"
import { NodeContext, NodeRuntime } from "@effect/platform-node"
import { Console, Effect, pipe } from "effect"

// Define command
const greet = Command.make(
  "greet",
  { name: Args.text({ name: "name" }) },
  ({ name }) => Console.log(`Hello, ${name}!`)
)

// Run
pipe(
  Command.run(greet, { name: "myapp", version: "1.0.0" }),
  (cli) => cli(process.argv),
  Effect.provide(NodeContext.layer),
  NodeRuntime.runMain
)
```

---

## Command Definition

### Basic Command

```typescript
const myCommand = Command.make(
  "command-name",           // Command name (used in help)
  { /* config object */ },  // Args and Options
  (config) => Effect.gen(function* () {
    // Handler receives parsed config
    yield* Console.log(`Got: ${config.someArg}`)
  })
)
```

### Config Object Structure

The second parameter defines what the command accepts:

```typescript
{
  // Positional arguments
  target: Args.text({ name: "target" }),

  // Named options
  verbose: Options.boolean("verbose").pipe(Options.withAlias("v")),

  // Optional values
  count: Options.integer("count").pipe(Options.optional),
}
```

---

## Arguments (Args)

Positional parameters passed after the command.

### Text Argument

```typescript
const target = Args.text({ name: "target" })
// Usage: mycli <target>
```

### Integer Argument

```typescript
const count = Args.integer({ name: "count" })
// Usage: mycli <count>
```

### Optional Argument

```typescript
const maybeFile = Args.text({ name: "file" }).pipe(Args.optional)
// Usage: mycli [file]
// Returns: Option<string>
```

### Repeated Arguments

```typescript
const files = Args.text({ name: "files" }).pipe(Args.repeated)
// Usage: mycli file1.txt file2.txt file3.txt
// Returns: Chunk<string>
```

### With Description

```typescript
const target = Args.text({ name: "target" }).pipe(
  Args.withDescription("The target file or directory")
)
```

### With Default

```typescript
const format = Args.text({ name: "format" }).pipe(
  Args.withDefault("json")
)
```

---

## Options

Named flags and parameters.

### Boolean Flag

```typescript
const verbose = Options.boolean("verbose").pipe(
  Options.withAlias("v"),
  Options.withDefault(false)
)
// Usage: --verbose or -v
```

### Text Option

```typescript
const output = Options.text("output").pipe(
  Options.withAlias("o"),
  Options.optional
)
// Usage: --output file.txt or -o file.txt
// Returns: Option<string>
```

### Integer Option

```typescript
const limit = Options.integer("limit").pipe(
  Options.withAlias("n"),
  Options.withDefault(10)
)
// Usage: --limit 20 or -n 20
```

### Choice Option (Enum)

```typescript
const FORMATS = ["json", "yaml", "toml"] as const

const format = Options.choice("format", FORMATS).pipe(
  Options.withAlias("f"),
  Options.withDefault("json" as const)
)
// Usage: --format yaml or -f yaml
```

### Optional vs Required

```typescript
// Required (error if missing)
const required = Options.text("api-key")

// Optional (returns Option<string>)
const optional = Options.text("api-key").pipe(Options.optional)

// Optional with default (returns string)
const withDefault = Options.text("api-key").pipe(
  Options.withDefault("default-key")
)
```

---

## Subcommands

Compose commands into hierarchies.

### Basic Subcommands

```typescript
const add = Command.make("add", { file: Args.text({ name: "file" }) },
  ({ file }) => Console.log(`Adding ${file}`)
)

const remove = Command.make("remove", { file: Args.text({ name: "file" }) },
  ({ file }) => Console.log(`Removing ${file}`)
)

const main = Command.make("git", {}, () =>
  Console.log("Usage: git <add|remove> <file>")
).pipe(
  Command.withSubcommands([add, remove])
)

// Usage: git add file.txt
// Usage: git remove file.txt
```

### Nested Subcommands

```typescript
const dbMigrate = Command.make("migrate", {}, () => Console.log("Migrating..."))
const dbSeed = Command.make("seed", {}, () => Console.log("Seeding..."))

const db = Command.make("db", {}, () => Console.log("Usage: app db <migrate|seed>"))
  .pipe(Command.withSubcommands([dbMigrate, dbSeed]))

const main = Command.make("app", {}, () => Console.log("Usage: app <db>"))
  .pipe(Command.withSubcommands([db]))

// Usage: app db migrate
```

---

## Program Structure

### Standard CLI Template

```typescript
#!/usr/bin/env bun
import { Args, Command, Options } from "@effect/cli"
import { NodeContext, NodeRuntime } from "@effect/platform-node"
import { Console, Effect, Layer, pipe } from "effect"

// =============================================================================
// OPTIONS & ARGS (define reusable pieces)
// =============================================================================

const verboseOption = Options.boolean("verbose").pipe(
  Options.withAlias("v"),
  Options.withDefault(false)
)

const formatOption = Options.choice("format", ["json", "text"] as const).pipe(
  Options.withAlias("f"),
  Options.withDefault("text" as const)
)

// =============================================================================
// COMMANDS
// =============================================================================

const listCommand = Command.make(
  "list",
  { verbose: verboseOption, format: formatOption },
  ({ verbose, format }) =>
    Effect.gen(function* () {
      yield* Console.log(`Listing (verbose=${verbose}, format=${format})`)
    })
)

const addCommand = Command.make(
  "add",
  { name: Args.text({ name: "name" }) },
  ({ name }) =>
    Effect.gen(function* () {
      yield* Console.log(`Adding: ${name}`)
    })
)

// =============================================================================
// MAIN COMMAND
// =============================================================================

const mainCommand = Command.make("mycli", {}, () =>
  Console.log(`
mycli - My CLI Tool

COMMANDS:
  list    List items
  add     Add an item

OPTIONS:
  --help, -h     Show help
  --version, -V  Show version
`)
).pipe(
  Command.withSubcommands([listCommand, addCommand])
)

// =============================================================================
// RUN
// =============================================================================

const cli = Command.run(mainCommand, {
  name: "mycli",
  version: "1.0.0",
})

pipe(
  Effect.sync(() => process.argv),
  Effect.flatMap(cli),
  Effect.provide(NodeContext.layer),
  NodeRuntime.runMain
)
```

### With Custom Layers

```typescript
// Define your service layers
const AppLayer = Layer.mergeAll(
  NodeContext.layer,
  DatabaseLayer,
  ConfigLayer
)

pipe(
  program,
  Effect.catchAll(handleError),
  Effect.provide(AppLayer),
  NodeRuntime.runMain
)
```

---

## Handler Patterns

### Effectful Handler

```typescript
const myCommand = Command.make("cmd", { id: Args.text({ name: "id" }) },
  ({ id }) =>
    Effect.gen(function* () {
      const service = yield* MyService
      const result = yield* service.findById(id)
      yield* Console.log(JSON.stringify(result, null, 2))
    })
)
```

### With Error Handling

```typescript
const myCommand = Command.make("cmd", { id: Args.text({ name: "id" }) },
  ({ id }) =>
    Effect.gen(function* () {
      const result = yield* findById(id)
      yield* Console.log(result)
    }).pipe(
      Effect.catchTag("NotFoundError", (e) =>
        Console.error(`Not found: ${e.id}`)
      )
    )
)
```

### Returning Exit Code

```typescript
const myCommand = Command.make("cmd", {},
  () =>
    Effect.gen(function* () {
      const success = yield* doSomething()
      if (!success) {
        yield* Effect.fail(new Error("Operation failed"))
      }
    })
)
```

---

## Help Text

### Automatic Help

`@effect/cli` generates help automatically from:
- Command names
- Arg/Option names
- Descriptions via `.withDescription()`

```typescript
const cmd = Command.make("greet",
  {
    name: Args.text({ name: "name" }).pipe(
      Args.withDescription("Name of person to greet")
    ),
    loud: Options.boolean("loud").pipe(
      Options.withAlias("l"),
      Options.withDescription("Greet loudly with exclamation")
    ),
  },
  handler
)
```

### Custom Main Help

```typescript
const main = Command.make("mycli", {}, () =>
  Console.log(`
mycli v1.0.0 - Description here

USAGE:
  mycli <command> [options]

COMMANDS:
  list      List all items
  add       Add new item
  remove    Remove item

GLOBAL OPTIONS:
  --help, -h      Show help
  --version, -V   Show version

EXAMPLES:
  mycli list --format json
  mycli add "new item"
`)
)
```

---

## Anti-Patterns

### DON'T: Sync handlers for async work

```typescript
// WRONG
Command.make("cmd", {}, () => {
  const result = fetchSync() // Blocking!
  return Console.log(result)
})

// CORRECT
Command.make("cmd", {}, () =>
  Effect.gen(function* () {
    const result = yield* fetchEffect()
    yield* Console.log(result)
  })
)
```

### DON'T: Forget to provide layers

```typescript
// WRONG - Will fail with missing service
pipe(program, NodeRuntime.runMain)

// CORRECT
pipe(program, Effect.provide(AppLayer), NodeRuntime.runMain)
```

### DON'T: Use console.log directly

```typescript
// WRONG
Command.make("cmd", {}, () => {
  console.log("Hello") // Not Effect-native
  return Effect.void
})

// CORRECT
Command.make("cmd", {}, () => Console.log("Hello"))
```

---

## Related Skills

| Skill | Purpose |
|-------|---------|
| `cli/persistence` | SQLite storage patterns |
| `cli/messaging` | Agent-guiding output |
| `cli/services` | Effect.Service for CLI |
| `cli/config` | Configuration patterns |

---

## Quick Reference

| Pattern | Import | Example |
|---------|--------|---------|
| Command | `@effect/cli` | `Command.make("name", {}, handler)` |
| Text arg | `@effect/cli` | `Args.text({ name: "x" })` |
| Bool option | `@effect/cli` | `Options.boolean("x")` |
| Choice option | `@effect/cli` | `Options.choice("x", [...])` |
| Subcommands | `@effect/cli` | `Command.withSubcommands([...])` |
| Run | `@effect/cli` | `Command.run(cmd, { name, version })` |
| Runtime | `@effect/platform-node` | `NodeRuntime.runMain` |
