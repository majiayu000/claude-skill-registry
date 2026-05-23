---
name: Configuration
description: This skill should be used when the user asks about "Effect Config", "environment variables", "configuration management", "Config.string", "Config.number", "ConfigProvider", "Config.nested", "Config.withDefault", "Config.redacted", "sensitive values", "config validation", "loading config from JSON", "config schema", or needs to understand how Effect handles application configuration.
version: 1.0.0
---

# Configuration in Effect

## Overview

Effect provides type-safe configuration loading with:

- Automatic environment variable reading
- Validation and type conversion
- Default values and composition
- Sensitive value handling
- Multiple config sources (env, JSON, custom)

## Basic Configuration Types

```typescript
import { Config, Effect } from "effect"

const host = Config.string("HOST")

const port = Config.number("PORT")

const debug = Config.boolean("DEBUG")

const maxConnections = Config.integer("MAX_CONNECTIONS")
```

## Using Config in Effects

```typescript
const program = Effect.gen(function* () {
  const host = yield* Config.string("DATABASE_HOST")
  const port = yield* Config.number("DATABASE_PORT")

  return { host, port }
})

// Runs and reads from environment
await Effect.runPromise(program)
```

## Default Values

```typescript
const port = Config.number("PORT").pipe(
  Config.withDefault(3000)
)

const debug = Config.boolean("DEBUG").pipe(
  Config.withDefault(false)
)
```

## Optional Configuration

```typescript
const apiKey = Config.string("API_KEY").pipe(
  Config.option
)
// Type: Effect<Option<string>>
```

## Combining Configurations

### Using Config.all

```typescript
const dbConfig = Config.all({
  host: Config.string("DB_HOST"),
  port: Config.number("DB_PORT"),
  database: Config.string("DB_NAME"),
  maxConnections: Config.number("DB_MAX_CONN").pipe(
    Config.withDefault(10)
  )
})

const program = Effect.gen(function* () {
  const config = yield* dbConfig
  // config: { host: string, port: number, database: string, maxConnections: number }
})
```

### Nested Configurations

```typescript
const dbConfig = Config.nested("DB")(
  Config.all({
    host: Config.string("HOST"),      // Reads DB_HOST
    port: Config.number("PORT"),      // Reads DB_PORT
    name: Config.string("NAME")       // Reads DB_NAME
  })
)
```

## Config with Schema Validation

Use Effect Schema for complex validation:

```typescript
import { Config, Schema } from "effect"

const PortSchema = Schema.Number.pipe(
  Schema.int(),
  Schema.between(1, 65535)
)

const port = Config.number("PORT").pipe(
  Config.mapOrFail((n) =>
    Schema.decodeUnknownEither(PortSchema)(n).pipe(
      Either.mapLeft((e) => ConfigError.InvalidData([], `Invalid port: ${n}`))
    )
  )
)
```

## Handling Sensitive Values

### Config.redacted

Prevents accidental logging of sensitive values:

```typescript
const apiKey = Config.redacted("API_KEY")
// Type: Effect<Redacted<string>>

const program = Effect.gen(function* () {
  const key = yield* apiKey

  // Safe to log - shows "<redacted>"
  yield* Effect.log(`Key: ${key}`)

  // Get actual value when needed
  const actual = Redacted.value(key)
})
```

### Secret Type

```typescript
const dbPassword = Config.secret("DB_PASSWORD")
// Type: Effect<Secret.Secret>

const program = Effect.gen(function* () {
  const password = yield* dbPassword
  const value = Secret.value(password) // Get actual string
})
```

## Config Operators

### Transforming Values

```typescript
const upperHost = Config.string("HOST").pipe(
  Config.map((s) => s.toUpperCase())
)

const port = Config.string("PORT").pipe(
  Config.mapOrFail((s) => {
    const n = parseInt(s)
    return isNaN(n)
      ? Either.left(ConfigError.InvalidData([], "Not a number"))
      : Either.right(n)
  })
)
```

### Fallback Values

```typescript
const host = Config.string("PRIMARY_HOST").pipe(
  Config.orElse(() => Config.string("SECONDARY_HOST")),
  Config.orElse(() => Config.succeed("localhost"))
)
```

## Custom Config Providers

### From Environment (Default)

```typescript
const program = Effect.gen(function* () {
  const host = yield* Config.string("HOST")
})
```

### From JSON/Object

```typescript
import { ConfigProvider, Layer } from "effect"

const config = {
  host: "localhost",
  port: "3000",
  database: {
    host: "db.example.com",
    port: "5432"
  }
}

const JsonConfigProvider = ConfigProvider.fromJson(config)

const program = Effect.gen(function* () {
  const host = yield* Config.string("host")
  const dbHost = yield* Config.nested("database")(Config.string("host"))
})

const runnable = program.pipe(
  Effect.provide(Layer.setConfigProvider(JsonConfigProvider))
)
```

### From Map

```typescript
const MapProvider = ConfigProvider.fromMap(
  new Map([
    ["HOST", "localhost"],
    ["PORT", "3000"]
  ])
)
```

### Combining Providers

```typescript
const CombinedProvider = ConfigProvider.orElse(
  ConfigProvider.fromEnv(),
  () => ConfigProvider.fromJson(defaultConfig)
)
```

## Config in Layers

```typescript
const AppConfigLive = Layer.effect(
  AppConfig,
  Effect.gen(function* () {
    const host = yield* Config.string("HOST")
    const port = yield* Config.number("PORT")
    const debug = yield* Config.boolean("DEBUG").pipe(Config.withDefault(false))

    return { host, port, debug }
  })
)
```

## Testing Configuration

### Mock Config Provider

```typescript
const TestConfigProvider = ConfigProvider.fromMap(
  new Map([
    ["HOST", "test-host"],
    ["PORT", "9999"]
  ])
)

const testProgram = program.pipe(
  Effect.provide(Layer.setConfigProvider(TestConfigProvider))
)
```

### Config.succeed for Hardcoded

```typescript
const testConfig = Config.succeed({
  host: "localhost",
  port: 3000
})
```

## Error Handling

Config failures produce `ConfigError`:

```typescript
const program = Effect.gen(function* () {
  const host = yield* Config.string("REQUIRED_HOST")
}).pipe(
  Effect.catchTag("ConfigError", (error) =>
    Effect.fail(new StartupError({ cause: error }))
  )
)
```

## Complete Example

```typescript
import { Config, Effect, Layer, Schema } from "effect"

// Define config shape
const AppConfig = Config.all({
  server: Config.nested("SERVER")(
    Config.all({
      host: Config.string("HOST").pipe(Config.withDefault("0.0.0.0")),
      port: Config.number("PORT").pipe(Config.withDefault(3000))
    })
  ),
  database: Config.nested("DATABASE")(
    Config.all({
      url: Config.redacted("URL"),
      maxConnections: Config.number("MAX_CONN").pipe(Config.withDefault(10))
    })
  ),
  features: Config.all({
    debug: Config.boolean("DEBUG").pipe(Config.withDefault(false)),
    metrics: Config.boolean("METRICS_ENABLED").pipe(Config.withDefault(true))
  })
})

// Use in application
const program = Effect.gen(function* () {
  const config = yield* AppConfig
  yield* Effect.log(`Starting server on ${config.server.host}:${config.server.port}`)
})
```

## Best Practices

1. **Use Config.withDefault for optional values** - Avoid runtime errors
2. **Use Config.redacted for secrets** - Prevents accidental logging
3. **Use Config.nested for structure** - Organizes related config
4. **Validate with Schema** - Catch invalid config early
5. **Test with mock providers** - Deterministic tests

## Additional Resources

For comprehensive configuration documentation, consult `${CLAUDE_PLUGIN_ROOT}/references/llms-full.txt`.

Search for these sections:
- "Configuration" for full API reference
- "ConfigProvider" for custom providers
- "Handling Sensitive Values" for security
