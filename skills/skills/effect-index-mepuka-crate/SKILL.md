---
name: effect-index
description: Skill index and decision guide. Use to pick the right Effect Skill quickly and follow a minimal decision tree.
allowed-tools: Read, Grep, Glob, Edit, Write
---

# Effect Skill Index

Use this as a quick router to the right Skill for your task. Each entry links to a focused Skill optimized for a coding agent’s limited context.

## Decision Tree

- I need to write or refactor some Effect code → [Foundations](../effect-foundations/SKILL.md)
- I need robust error handling/retries → [Errors & Retries](../effect-errors-retries/SKILL.md)
- I must run things in parallel / manage fibers → [Concurrency & Fibers](../effect-concurrency-fibers/SKILL.md)
- This is a data pipeline / batching / backpressure → [Streams & Pipelines](../effect-streams-pipelines/SKILL.md)
- I need DI/services/layers or test/live wiring → [Layers & Services](../effect-layers-services/SKILL.md)
- Opening files/sockets/servers with cleanup → [Resources & Scope](../effect-resources-scope/SKILL.md)
- Add HTTP endpoints / JSON responses → [HTTP & Routing](../effect-http-routing/SKILL.md)
- Validate inputs / parse config → [Config & Schema](../effect-config-schema/SKILL.md)
- Value-based equality / high-perf immutable collections → [Data Structures](../effect-collections-datastructs/SKILL.md)
- Time, logging, spans/tracing → [Time/Tracing/Logging](../effect-time-tracing-logging/SKILL.md)
- Queues, PubSub, background workers → [Queues & Background](../effect-queues-background/SKILL.md)
- Write tests/mocks for services → [Testing & Mocking](../effect-testing-mocking/SKILL.md)
- **Looking for specific patterns or examples** → [**Patterns Hub (130+ patterns)**](../effect-patterns-hub/SKILL.md)

## Cross-Skill Patterns

All patterns are now available locally in the [Patterns Hub](../effect-patterns-hub/SKILL.md) (130+ patterns):

- **Retry transient failures** → [Errors & Retries](../effect-errors-retries/SKILL.md) + [retry-based-on-specific-errors.mdx](../effect-patterns-hub/patterns/retry-based-on-specific-errors.mdx)
- **Resource-safe streaming** → [Streams & Pipelines](../effect-streams-pipelines/SKILL.md) + [stream-manage-resources.mdx](../effect-patterns-hub/patterns/stream-manage-resources.mdx)
- **Graceful shutdown** → [Queues & Background](../effect-queues-background/SKILL.md) + [execute-long-running-apps-with-runfork.mdx](../effect-patterns-hub/patterns/execute-long-running-apps-with-runfork.mdx)
- **Service layer design** → [Layers & Services](../effect-layers-services/SKILL.md) + [model-dependencies-as-services.mdx](../effect-patterns-hub/patterns/model-dependencies-as-services.mdx)
- **HTTP server setup** → [HTTP & Routing](../effect-http-routing/SKILL.md) + [build-a-basic-http-server.mdx](../effect-patterns-hub/patterns/build-a-basic-http-server.mdx)
- **Schema validation** → [Config & Schema](../effect-config-schema/SKILL.md) + [define-contracts-with-schema.mdx](../effect-patterns-hub/patterns/define-contracts-with-schema.mdx)
- **Testing with mocks** → [Testing & Mocking](../effect-testing-mocking/SKILL.md) + [mocking-dependencies-in-tests.mdx](../effect-patterns-hub/patterns/mocking-dependencies-in-tests.mdx)

**Tip**: For any "How do I...?" question, check the [Patterns Hub](../effect-patterns-hub/SKILL.md) decision tree first!

## Local Source Reference

**CRITICAL: Always search local Effect source before implementing**

The full Effect source code is available at `docs/effect-source/`. Every Effect skill now includes a "Local Source Reference" section with:

- Key source files for that skill's domain
- Example grep commands to find implementations
- Workflow for searching before coding

### Quick Access to Source
- All Effect packages: `docs/effect-source/`
- Core library: `docs/effect-source/effect/src/`
- Platform APIs: `docs/effect-source/platform/src/`
- SQL: `docs/effect-source/sql/src/`
- Schema: `docs/effect-source/schema/src/`

### Example: Finding Effect.gen
```bash
grep -F "Effect.gen" docs/effect-source/effect/src/Effect.ts
```

### Workflow Reminder
1. Read the relevant skill (from decision tree above)
2. Review the skill's "Local Source Reference" section
3. Search the Effect source code for the API you need
4. Study the implementation and types
5. Write your code based on real implementations

**See CLAUDE.local.md for complete source reference guide**

## References

- Agent Skills overview: [Introducing Agent Skills](https://www.anthropic.com/news/skills)
- Skills guide: [Claude Code Skills Documentation](https://docs.claude.com/en/docs/claude-code/skills)
- **Local Patterns Hub**: [../effect-patterns-hub/SKILL.md](../effect-patterns-hub/SKILL.md) (130+ patterns)
- **Pattern Documentation**: [../../docs/effect-patterns/](../../docs/effect-patterns/)
- **AGENTS.md**: [../../AGENTS.md](../../AGENTS.md) (Effect best practices for AI agents)
- EffectPatterns (upstream source): [PaulJPhilp/EffectPatterns](https://github.com/PaulJPhilp/EffectPatterns)


