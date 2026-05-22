---
name: effect-layers-services
description: Define services, provide layers, compose dependencies, and switch live/test. Use for DI boundaries and app composition.
allowed-tools: Read, Grep, Glob, Edit, Write, mcp__effect-docs__effect_docs_search
---

# Layers & Services

## When to use
- You need DI boundaries or swapping test/live implementations
- You want to compose infra (logger, db, http) once for the app

## Define Service
```ts
class UserRepo extends Effect.Service<UserRepo>()("UserRepo", {
  sync: () => ({ find: (id: string) => Effect.succeed({ id }) })
}) {}
```

## Provide Layer
```ts
const program = Effect.gen(function* () {
  const repo = yield* UserRepo
  return yield* repo.find("123")
}).pipe(Effect.provide(UserRepo.Default))
```

## Compose
```ts
const AppLayer = Layer.merge(UserRepo.Default, Logger.Default)
```

## Test vs Live
```ts
const layer = process.env.NODE_ENV === "test" ? UserRepoTest : UserRepo.Default
```

## Guidance
- Services define interfaces; Layers bind implementations
- Compose layers at the app boundary; keep handlers unaware of wiring
- Use `.Default` for quick live/test setup; add custom layers as needed

## Pitfalls
- Circular layer dependencies → split modules, provide from above
- Providing layers too deep → centralize to avoid duplication and confusion

## Cross-links
- Foundations: requirement channel `R` and provisioning
- Resources: scoped resources exposed via layers
- EffectPatterns inspiration: https://github.com/PaulJPhilp/EffectPatterns

## Local Source Reference

**CRITICAL: Search local Effect source before implementing**

The full Effect source code is available at `docs/effect-source/`. Always search the actual implementation before writing Effect code.

### Key Source Files
- Layer: `docs/effect-source/effect/src/Layer.ts`
- Effect: `docs/effect-source/effect/src/Effect.ts`
- Context: `docs/effect-source/effect/src/Context.ts`

### Example Searches
```bash
# Find Layer composition patterns
grep -F "Layer.merge" docs/effect-source/effect/src/Layer.ts
grep -F "Layer.provide" docs/effect-source/effect/src/Layer.ts

# Study Effect.Service patterns
grep -F "Effect.Service" docs/effect-source/effect/src/Effect.ts

# Find Context usage
grep -F "Tag" docs/effect-source/effect/src/Context.ts
grep -F "make" docs/effect-source/effect/src/Context.ts

# Look at Layer test examples
grep -F "Layer." docs/effect-source/effect/test/Layer.test.ts
```

### Workflow
1. Identify the Layer or Service API you need
2. Search `docs/effect-source/effect/src/Layer.ts` for the implementation
3. Study the types and composition patterns
4. Look at test files for usage examples
5. Write your code based on real implementations

**Real source code > documentation > assumptions**

## References
- Agent Skills overview: https://www.anthropic.com/news/skills
- Skills guide: https://docs.claude.com/en/docs/claude-code/skills

