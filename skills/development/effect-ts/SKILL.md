---
name: effect-ts
description: Effect-TS snippets, templates, and examples for Effect usage.
---

# Effect-TS Skill

Use this skill to add or modify Effect-TS code. It provides quick patterns for
finding Effect usage and for composing, testing, and structuring Effect-based
modules.

## Find Effect usage fast

- `Effect` imports or type references.
- `Effect.gen` for generator-based composition.
- `Layer` for dependency wiring.
- `pipe` for functional composition.
- `Context.Tag` or `Context.GenericTag` for services.
- `Schedule`, `Stream`, `Fiber`, `Ref`, `Queue` for concurrency/streaming.

## Snippets

### Basic Effect

```ts
import { Effect } from "effect";

const program = Effect.succeed("ok");
```

### Generator composition

```ts
import { Effect } from "effect";

const program = Effect.gen(function* () {
  const value = yield* Effect.succeed(42);
  return value + 1;
});
```

### Error handling

```ts
import { Effect } from "effect";

const program = Effect.fail(new Error("boom"));
const recovered = Effect.catchAll(program, () => Effect.succeed("fallback"));
```

### Resource acquisition

```ts
import { Effect } from "effect";

const acquire = Effect.sync(() => ({ close: () => void 0 }));
const use = (resource: { close: () => void }) => Effect.succeed(resource);

const program = Effect.acquireUseRelease(
  acquire,
  use,
  (resource) => Effect.sync(() => resource.close()),
);
```

### Layer and service

```ts
import { Context, Effect, Layer } from "effect";

class Logger extends Context.Tag("Logger")<Logger, { log: (msg: string) => Effect.Effect<void> }>() {}

const LoggerLive = Layer.succeed(Logger, {
  log: (msg) => Effect.sync(() => console.log(msg)),
});

const program = Effect.gen(function* () {
  const logger = yield* Logger;
  yield* logger.log("hi");
});
```

## Templates

## Example with Contexts

We use Context tags to yield dependencies in our programs

```ts
import { Context, Effect, Layer } from "effect";

class Config extends Context.Tag("Config")<Config, { apiUrl: string }>() {}
class Api extends Context.Tag("Api")<Api, { 
  fetchStatus: () => Effect.Effect<string, Error> 
}>() {}

const ConfigLive = Layer.succeed(Config, { apiUrl: "https://api.example.com" });

const ApiLive = Layer.effect(Api, Effect.gen(function* () {
  const config = yield* Config;
  return {
    fetchStatus: () =>
      Effect.tryPromise({
        try: async () => {
          const res = await fetch(`${config.apiUrl}/status`);
          if (!res.ok) throw new Error("Bad status");
          return res.text();
        },
        catch: (cause) => cause as Error,
      }),
  };
}));

const program = Effect.gen(function* () {
  const api = yield* Api;
  return yield* api.fetchStatus();
});

Effect.runPromise(
  program.pipe(
    Effect.provide(ApiLive),
    Effect.provide(ConfigLive),
  ),
);
```

## Always use Effect.fn with Generator Functions

When converting a function to use `Effect.fn` and the generator function doesn't have any `yield` statements, add `yield* Effect.void` with a TODO comment:

```typescript
export const myFunction = Effect.fn('myFunction')(
  function* (props: {...}): Generator<any, ReturnType, any> {
    // TODO: yield something or remove function*
    yield* Effect.void;
    // ... rest of function
  }
);
```

## Always yield* in Effect.fn

If there is no OTHER yield* in the generator function scope, then use `yield* Effect.void`

## ManagedRuntime

See: https://effect.website/docs/runtime/

