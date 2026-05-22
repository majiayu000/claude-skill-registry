---
name: cli-config
description: Configuration patterns for Effect CLI using Context.Tag and Config. Covers environment variables, config files, command-line overrides, and layered configuration.
model_invoked: true
triggers:
  - "CLI config"
  - "configuration"
  - "environment variables"
  - "Config.Provider"
  - "config file"
  - "settings"
---

# CLI Configuration Patterns

Configuration patterns for Effect CLI using Context.Tag, Config, and layered configuration sources.

## Quick Start

```typescript
import { Config, Context, Effect, Layer } from "effect"

// Define config schema
interface AppConfig {
  readonly dbPath: string
  readonly logLevel: "debug" | "info" | "warn" | "error"
  readonly prettyPrint: boolean
}

// Create config tag
class AppConfig extends Context.Tag("AppConfig")<AppConfig, AppConfig>() {}

// Load from environment
const AppConfigLive = Layer.effect(
  AppConfig,
  Effect.gen(function* () {
    return {
      dbPath: yield* Config.string("DB_PATH").pipe(
        Config.withDefault(`${process.env.HOME}/.myapp/data.db`)
      ),
      logLevel: yield* Config.literal("debug", "info", "warn", "error")("LOG_LEVEL").pipe(
        Config.withDefault("info")
      ),
      prettyPrint: yield* Config.boolean("PRETTY_PRINT").pipe(
        Config.withDefault(true)
      ),
    }
  })
)

// Use in commands
const myCommand = Command.make("cmd", {}, () =>
  Effect.gen(function* () {
    const config = yield* AppConfig
    yield* Console.log(`DB: ${config.dbPath}`)
  })
)
```

---

## Config Sources

### Environment Variables

```typescript
// Simple string
const apiKey = yield* Config.string("API_KEY")

// With default
const host = yield* Config.string("HOST").pipe(
  Config.withDefault("localhost")
)

// Optional (returns Option)
const debugMode = yield* Config.string("DEBUG").pipe(
  Config.option
)

// Required with custom error
const secret = yield* Config.string("SECRET").pipe(
  Config.mapError(() => new ConfigError({ key: "SECRET", message: "Required for auth" }))
)
```

### Typed Config Values

```typescript
// Boolean
const verbose = yield* Config.boolean("VERBOSE").pipe(
  Config.withDefault(false)
)

// Integer
const port = yield* Config.integer("PORT").pipe(
  Config.withDefault(3000)
)

// Number (float)
const timeout = yield* Config.number("TIMEOUT_SECONDS").pipe(
  Config.withDefault(30.0)
)

// Literal union (enum)
const env = yield* Config.literal("dev", "staging", "prod")("ENV").pipe(
  Config.withDefault("dev")
)

// URL
const apiUrl = yield* Config.url("API_URL").pipe(
  Config.withDefault(new URL("http://localhost:8080"))
)
```

### Config File Loading

```typescript
import { FileSystem } from "@effect/platform"
import * as path from "node:path"

interface ConfigFile {
  dbPath?: string
  logLevel?: string
  features?: {
    cache?: boolean
    metrics?: boolean
  }
}

const loadConfigFile = Effect.gen(function* () {
  const fs = yield* FileSystem.FileSystem
  const configPath = path.join(process.env.HOME!, ".myapp", "config.json")

  const exists = yield* fs.exists(configPath)
  if (!exists) {
    return {} as ConfigFile
  }

  const content = yield* fs.readFileString(configPath)
  return JSON.parse(content) as ConfigFile
})

const AppConfigLive = Layer.effect(
  AppConfig,
  Effect.gen(function* () {
    // Load file first
    const file = yield* loadConfigFile

    // Environment overrides file
    return {
      dbPath: yield* Config.string("DB_PATH").pipe(
        Config.withDefault(file.dbPath ?? `${process.env.HOME}/.myapp/data.db`)
      ),
      logLevel: yield* Config.literal("debug", "info", "warn", "error")("LOG_LEVEL").pipe(
        Config.withDefault((file.logLevel as any) ?? "info")
      ),
      cacheEnabled: yield* Config.boolean("CACHE_ENABLED").pipe(
        Config.withDefault(file.features?.cache ?? true)
      ),
    }
  })
)
```

---

## Layered Configuration

### Pattern: Priority Order

```
CLI args > Environment > Config file > Defaults
```

```typescript
// Define option that can override config
const verboseOption = Options.boolean("verbose").pipe(
  Options.withAlias("v"),
  Options.optional
)

const myCommand = Command.make(
  "cmd",
  { verbose: verboseOption },
  ({ verbose }) =>
    Effect.gen(function* () {
      const config = yield* AppConfig

      // CLI option overrides config
      const isVerbose = Option.getOrElse(verbose, () => config.verbose)

      if (isVerbose) {
        yield* Console.log("Verbose mode enabled")
      }
    })
)
```

### Pattern: Config Service with Overrides

```typescript
interface AppConfig {
  readonly dbPath: string
  readonly logLevel: string
  readonly verbose: boolean
}

class AppConfig extends Context.Tag("AppConfig")<AppConfig, AppConfig>() {}

// Base config from env/file
const baseConfig = Effect.gen(function* () {
  const file = yield* loadConfigFile
  return {
    dbPath: yield* Config.string("DB_PATH").pipe(
      Config.withDefault(file.dbPath ?? DEFAULT_DB_PATH)
    ),
    logLevel: yield* Config.string("LOG_LEVEL").pipe(
      Config.withDefault(file.logLevel ?? "info")
    ),
    verbose: yield* Config.boolean("VERBOSE").pipe(
      Config.withDefault(file.verbose ?? false)
    ),
  }
})

// Factory that accepts CLI overrides
const makeAppConfigLayer = (overrides: Partial<AppConfig>) =>
  Layer.effect(
    AppConfig,
    Effect.gen(function* () {
      const base = yield* baseConfig
      return { ...base, ...overrides }
    })
  )

// In main command, capture options and create layer
const mainCommand = Command.make(
  "app",
  {
    verbose: Options.boolean("verbose").pipe(Options.optional),
    logLevel: Options.text("log-level").pipe(Options.optional),
  },
  ({ verbose, logLevel }) =>
    Effect.gen(function* () {
      // Build overrides from CLI options
      const overrides: Partial<AppConfig> = {}
      if (Option.isSome(verbose)) overrides.verbose = verbose.value
      if (Option.isSome(logLevel)) overrides.logLevel = logLevel.value

      // Create config layer with overrides
      const configLayer = makeAppConfigLayer(overrides)

      // Run subcommand with this config
      yield* subcommandProgram.pipe(Effect.provide(configLayer))
    })
)
```

---

## Config Schemas with Effect Schema

### Pattern: Validated Config

```typescript
import { Schema } from "effect"

// Define config schema
const AppConfigSchema = Schema.Struct({
  database: Schema.Struct({
    path: Schema.String.pipe(Schema.nonEmptyString()),
    poolSize: Schema.Number.pipe(Schema.int(), Schema.positive()),
  }),
  logging: Schema.Struct({
    level: Schema.Literal("debug", "info", "warn", "error"),
    format: Schema.Literal("json", "text"),
  }),
  features: Schema.Struct({
    cache: Schema.Boolean,
    metrics: Schema.Boolean,
  }),
})

type AppConfig = Schema.Schema.Type<typeof AppConfigSchema>

// Parse and validate
const loadConfig = Effect.gen(function* () {
  const fs = yield* FileSystem.FileSystem
  const configPath = `${process.env.HOME}/.myapp/config.json`

  const content = yield* fs.readFileString(configPath).pipe(
    Effect.mapError(() => new ConfigFileNotFoundError({ path: configPath }))
  )

  const json = yield* Effect.try({
    try: () => JSON.parse(content),
    catch: () => new ConfigParseError({ path: configPath }),
  })

  return yield* Schema.decodeUnknown(AppConfigSchema)(json).pipe(
    Effect.mapError((e) => new ConfigValidationError({ errors: e.errors }))
  )
})
```

### Pattern: Config with Defaults via Schema

```typescript
const AppConfigSchema = Schema.Struct({
  dbPath: Schema.optionalWith(Schema.String, {
    default: () => `${process.env.HOME}/.myapp/data.db`,
  }),
  logLevel: Schema.optionalWith(
    Schema.Literal("debug", "info", "warn", "error"),
    { default: () => "info" as const }
  ),
  maxRetries: Schema.optionalWith(Schema.Number, { default: () => 3 }),
})
```

---

## XDG Base Directory Support

### Pattern: Standard Paths

```typescript
const XDG = {
  config: process.env.XDG_CONFIG_HOME ?? `${process.env.HOME}/.config`,
  data: process.env.XDG_DATA_HOME ?? `${process.env.HOME}/.local/share`,
  cache: process.env.XDG_CACHE_HOME ?? `${process.env.HOME}/.cache`,
}

const APP_PATHS = {
  config: `${XDG.config}/myapp/config.json`,
  db: `${XDG.data}/myapp/data.db`,
  cache: `${XDG.cache}/myapp/`,
  logs: `${XDG.data}/myapp/logs/`,
}
```

### Pattern: Path Service

```typescript
interface PathService {
  readonly config: string
  readonly data: string
  readonly cache: string
  readonly logs: string
  readonly db: string
}

class PathService extends Context.Tag("PathService")<PathService, PathService>() {}

const PathServiceLive = Layer.succeed(
  PathService,
  PathService.of({
    config: process.env.MYAPP_CONFIG ?? `${XDG.config}/myapp/config.json`,
    data: process.env.MYAPP_DATA ?? `${XDG.data}/myapp/`,
    cache: process.env.MYAPP_CACHE ?? `${XDG.cache}/myapp/`,
    logs: process.env.MYAPP_LOGS ?? `${XDG.data}/myapp/logs/`,
    db: process.env.MYAPP_DB ?? `${XDG.data}/myapp/data.db`,
  })
)
```

---

## Init Command Pattern

### Pattern: Config Initialization

```typescript
const initCommand = Command.make(
  "init",
  {
    force: Options.boolean("force").pipe(
      Options.withAlias("f"),
      Options.withDefault(false)
    ),
  },
  ({ force }) =>
    Effect.gen(function* () {
      const fs = yield* FileSystem.FileSystem
      const paths = yield* PathService

      // Check if already initialized
      const configExists = yield* fs.exists(paths.config)
      if (configExists && !force) {
        yield* Console.log(`
[ALREADY_INITIALIZED] Config exists at ${paths.config}

Use --force to overwrite existing configuration.
`)
        return
      }

      // Create directories
      yield* fs.makeDirectory(path.dirname(paths.config), { recursive: true })
      yield* fs.makeDirectory(path.dirname(paths.db), { recursive: true })

      // Write default config
      const defaultConfig = {
        database: {
          path: paths.db,
          poolSize: 5,
        },
        logging: {
          level: "info",
          format: "text",
        },
        features: {
          cache: true,
          metrics: false,
        },
      }

      yield* fs.writeFileString(
        paths.config,
        JSON.stringify(defaultConfig, null, 2)
      )

      yield* Console.log(`
[SUCCESS] Initialized myapp configuration.

  Config: ${paths.config}
  Database: ${paths.db}

Edit ${paths.config} to customize settings.
`)
    })
)
```

---

## Runtime Config Updates

### Pattern: Reloadable Config

```typescript
import { Ref, Schedule } from "effect"

interface ConfigService {
  readonly get: Effect.Effect<AppConfig>
  readonly reload: Effect.Effect<void>
}

class ConfigService extends Context.Tag("ConfigService")<
  ConfigService,
  ConfigService
>() {}

const ConfigServiceLive = Layer.effect(
  ConfigService,
  Effect.gen(function* () {
    const initial = yield* loadConfig
    const ref = yield* Ref.make(initial)

    return ConfigService.of({
      get: Ref.get(ref),

      reload: Effect.gen(function* () {
        const newConfig = yield* loadConfig
        yield* Ref.set(ref, newConfig)
        yield* Console.log("[CONFIG] Reloaded configuration")
      }),
    })
  })
)

// Auto-reload on SIGHUP
const withConfigReload = <A, E>(program: Effect.Effect<A, E>) =>
  Effect.gen(function* () {
    const config = yield* ConfigService

    // Watch for reload signal
    yield* Effect.async<void>((resume) => {
      process.on("SIGHUP", () => {
        Effect.runPromise(config.reload)
      })
    }).pipe(Effect.fork)

    return yield* program
  })
```

---

## Config Command

### Pattern: View/Edit Config

```typescript
const configCommand = Command.make("config", {}, () =>
  Console.log("Usage: myapp config <get|set|path>")
).pipe(
  Command.withSubcommands([
    // Get config value
    Command.make(
      "get",
      { key: Args.text({ name: "key" }).pipe(Args.optional) },
      ({ key }) =>
        Effect.gen(function* () {
          const config = yield* AppConfig

          if (Option.isNone(key)) {
            yield* Console.log(JSON.stringify(config, null, 2))
            return
          }

          const value = (config as any)[key.value]
          if (value === undefined) {
            yield* Console.error(`Unknown config key: ${key.value}`)
            return
          }

          yield* Console.log(String(value))
        })
    ),

    // Set config value
    Command.make(
      "set",
      {
        key: Args.text({ name: "key" }),
        value: Args.text({ name: "value" }),
      },
      ({ key, value }) =>
        Effect.gen(function* () {
          const fs = yield* FileSystem.FileSystem
          const paths = yield* PathService

          const content = yield* fs.readFileString(paths.config)
          const config = JSON.parse(content)

          config[key] = value
          yield* fs.writeFileString(paths.config, JSON.stringify(config, null, 2))
          yield* Console.log(`Set ${key} = ${value}`)
        })
    ),

    // Show config path
    Command.make("path", {}, () =>
      Effect.gen(function* () {
        const paths = yield* PathService
        yield* Console.log(paths.config)
      })
    ),
  ])
)
```

---

## Anti-Patterns

### DON'T: Hardcode paths

```typescript
// WRONG
const DB_PATH = "/home/user/.myapp/data.db"

// CORRECT - Use environment with fallback
const DB_PATH = process.env.MYAPP_DB ?? `${process.env.HOME}/.myapp/data.db`
```

### DON'T: Fail silently on missing config

```typescript
// WRONG
const config = JSON.parse(fs.readFileSync(path) || "{}")

// CORRECT - Clear error with guidance
const config = yield* loadConfig.pipe(
  Effect.catchTag("ConfigNotFound", () =>
    Effect.fail(new Error(`
[CONFIG_NOT_FOUND] No configuration file found.

Run 'myapp init' to create default configuration.
`))
  )
)
```

### DON'T: Mix config sources inconsistently

```typescript
// WRONG - Some from env, some from file, confusing
const dbPath = process.env.DB_PATH
const logLevel = config.logging.level
const port = 3000  // Hardcoded!

// CORRECT - Consistent layered approach
const config = yield* AppConfig  // All config in one place
```

---

## Related Skills

| Skill | Purpose |
|-------|---------|
| `cli/core` | Command definition |
| `cli/persistence` | Storage patterns |
| `cli/messaging` | Error formatting |
| `cli/services` | Service composition |

---

## Quick Reference

| Config Type | Code |
|-------------|------|
| String | `Config.string("KEY")` |
| Boolean | `Config.boolean("KEY")` |
| Integer | `Config.integer("KEY")` |
| Number | `Config.number("KEY")` |
| Literal | `Config.literal("a", "b")("KEY")` |
| Optional | `Config.option(Config.string("KEY"))` |
| Default | `Config.withDefault(config, "default")` |
| Nested | `Config.nested(config, "PREFIX")` |

| Path Pattern | Value |
|--------------|-------|
| Config file | `~/.config/app/config.json` |
| Database | `~/.local/share/app/data.db` |
| Cache | `~/.cache/app/` |
| Logs | `~/.local/share/app/logs/` |
