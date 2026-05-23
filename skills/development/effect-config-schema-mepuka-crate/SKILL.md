---
name: effect-config-schema
description: Config loading and Schema validation/transform. Use when defining configuration or validating inputs.
allowed-tools: Read, Grep, Glob, Edit, Write, mcp__effect-docs__effect_docs_search
---

# Config & Schema

## When to use
- Validating request bodies, params, or external inputs
- Loading environment configuration with types

## Config (example)
```ts
import { Config } from "effect"

const Server = Config.nested("SERVER")(Config.all({
  host: Config.string("HOST"),
  port: Config.number("PORT")
}))
```

## Schema Validate
```ts
import { Schema as S } from "effect"

const User = S.Struct({ id: S.Number, name: S.String })
const decodeUser = (u: unknown) => S.decodeUnknown(User)(u)
```

## Transform
```ts
const IsoDate = S.String // then transform to Date in pipeline where needed
```

## Real-world snippet: Layer selecting AWS credentials via Config options
```ts
class AwsCredentials extends Effect.Service<AwsCredentials>()("AwsCredentials", {
  effect: Effect.gen(function* () {
    const accessKeys = yield* Config.option(
      Config.all([Config.string("CAP_AWS_ACCESS_KEY"), Config.string("CAP_AWS_SECRET_KEY")])
    )
    const vercelAwsRole = yield* Config.option(Config.string("VERCEL_AWS_ROLE_ARN"))

    const credentials = yield* Effect.gen(function* () {
      if (Option.isSome(vercelAwsRole)) return awsCredentialsProvider({ roleArn: vercelAwsRole.value })
      if (Option.isSome(accessKeys)) {
        const [accessKeyId, secretAccessKey] = accessKeys.value
        return { accessKeyId, secretAccessKey }
      }
      return fromContainerMetadata()
    })

    return { credentials }
  })
})
```

## Guidance
- Prefer schemas close to boundaries; keep core logic typed
- For branded types (Email, PositiveInt), use transform/brand helpers
- Validate early, map to domain errors in one place

## Pitfalls
- Accepting `unknown` into core → always decode first
- Large ad-hoc validation code → centralize in Schema

## Cross-links
- HTTP & Routing for endpoint validation
- Foundations for operator style

## Local Source Reference

**CRITICAL: Search local Effect source before implementing**

The full Effect source code is available at `docs/effect-source/`. Always search the actual implementation before writing Effect code.

### Key Source Files
- Config: `docs/effect-source/effect/src/Config.ts`
- Schema: `docs/effect-source/schema/src/Schema.ts`

### Example Searches
```bash
# Find Config patterns and options
grep -F "Config.string" docs/effect-source/effect/src/Config.ts
grep -F "Config.number" docs/effect-source/effect/src/Config.ts
grep -F "Config.option" docs/effect-source/effect/src/Config.ts

# Study Schema validation
grep -F "Struct" docs/effect-source/schema/src/Schema.ts
grep -F "decodeUnknown" docs/effect-source/schema/src/Schema.ts

# Find Schema transforms
grep -rF "transform" docs/effect-source/schema/src/
grep -rF "brand" docs/effect-source/schema/src/

# Look at Config test examples
grep -F "Config." docs/effect-source/effect/test/Config.test.ts
```

### Workflow
1. Identify the Config or Schema API you need
2. Search `docs/effect-source/effect/src/Config.ts` or `docs/effect-source/schema/src/Schema.ts`
3. Study the types and validation patterns
4. Look at test files for usage examples
5. Write your code based on real implementations

**Real source code > documentation > assumptions**

## References
- Agent Skills overview: https://www.anthropic.com/news/skills
- Skills guide: https://docs.claude.com/en/docs/claude-code/skills

