---
name: effect-testing-mocking
description: Testing patterns with layers, mocks, and deterministic time. Use when preparing testable services and small smoke tests.
allowed-tools: Read, Grep, Glob, Edit, Write
---

# Testing & Mocking

## When to use
- You need deterministic tests without external IO
- You want to inject mock services via layers

## Mock Layer
```ts
const RepoTest = Layer.succeed(Repo, Repo.of({ find: () => Effect.succeed(mock) }))
```

## Provide Test Impl
```ts
const result = yield* Effect.provide(program, RepoTest)
```

## Test Clock
```ts
// Provide a deterministic Clock or use platform TestClock layer if available
```

## Guidance
- Keep tests focused and fast; avoid network by mocking services
- Provide layers explicitly to match program requirements
- Keep tests close to real interfaces; do not reshape app code for tests
- Use `.Default` layers for quick wiring; add custom mock layers per test
- Favor small smoke tests that run quickly and fail fast

## Pitfalls
- Leaking real IO into tests → flakiness
- Over-mocking internals → brittle tests; mock at service boundary

## Cross-links
- Layers & Services for DI patterns
- Time/Logging for deterministic time and observable output

## Local Source Reference

**CRITICAL: Search local Effect source before implementing**

The full Effect source code is available at `docs/effect-source/`. Always search the actual implementation before writing Effect code.

### Key Source Files
- Layer: `docs/effect-source/effect/src/Layer.ts`
- TestClock: `docs/effect-source/effect/src/TestClock.ts`
- TestContext: `docs/effect-source/effect/src/TestContext.ts`

### Example Searches
```bash
# Find Layer.succeed patterns for mocks
grep -F "Layer.succeed" docs/effect-source/effect/src/Layer.ts

# Study TestClock operations
grep -F "TestClock" docs/effect-source/effect/src/TestClock.ts

# Find test helpers
grep -F "TestContext" docs/effect-source/effect/src/TestContext.ts

# Look at Layer test examples
grep -F "Layer.succeed" docs/effect-source/effect/test/Layer.test.ts
```

### Workflow
1. Identify the testing API you need (e.g., Layer.succeed, TestClock)
2. Search `docs/effect-source/effect/src/Layer.ts` for the implementation
3. Study the types and testing patterns
4. Look at test files for usage examples
5. Write your code based on real implementations

**Real source code > documentation > assumptions**

## Real-world snippet: Build a comprehensive Test layer
```ts
export const TestLayer = (input?: TestLiveInput) =>
  Effect.gen(function* () {
    const tempDir = tempy.temporaryDirectory({ prefix: 'test' })
    const cwd = (yield* setupFixtureFolder({ fixture: input?.fixture, tempDir })) ?? tempDir

    const NodeOsTest = Layer.succeed(NodeOs, new NodeOs({ homedir: cwd, arch: 'arm64', platform: 'darwin' }))
    const NodeProcessTest = Layer.succeed(NodeProcess, new NodeProcess({ cwd, platform: 'darwin', arch: 'arm64' }))

    const ToolkitsRepoTest = Layer.succeed(ComposioToolkitsRepository, new ComposioToolkitsRepository({
      getToolkits: () => Effect.succeed([]),
      getToolsAsEnums: () => Effect.succeed([])
    }))

    const layers = Layer.mergeAll(
      Console.setConsole(yield* MockConsole.effect),
      CliConfig.layer(ComposioCliConfig),
      NodeProcessTest,
      Layer.provideMerge(ComposioUserContextLive, Layer.merge(BunFileSystem.layer, NodeOsTest)),
      ToolkitsRepoTest,
      EnvLangDetector.Default,
      JsPackageManagerDetector.Default,
      BunFileSystem.layer,
      BunContext.layer,
      MockTerminal.layer,
      BunPath.layer
    )

    return layers
  }).pipe(
    Logger.withMinimumLogLevel(LogLevel.Debug),
    Effect.scoped,
    Layer.unwrapEffect,
    Layer.provide(Layer.setConfigProvider(input?.baseConfigProvider ?? ConfigProvider.fromMap(new Map([]))))
  )
```

## References
- Agent Skills overview: https://www.anthropic.com/news/skills
- Skills guide: https://docs.claude.com/en/docs/claude-code/skills

