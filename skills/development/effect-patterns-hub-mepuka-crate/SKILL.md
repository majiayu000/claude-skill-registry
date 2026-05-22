---
name: effect-patterns-hub
description: Complete catalog of 130+ Effect-TS patterns from EffectPatterns repository. Use when looking for specific implementation patterns, best practices, or real-world examples. Complements other skills with concrete, curated patterns.
allowed-tools: Read, Grep, Glob, Edit, Write
---

# Effect Patterns Hub

Purpose: Provide quick access to 130+ curated Effect-TS patterns from the EffectPatterns repository. Use this skill to find specific implementation patterns, compare approaches, and reference best practices.

## Triggers

- Looking for a specific Effect pattern or idiom
- Need real-world examples of Effect concepts
- Want to see multiple approaches to the same problem
- Comparing implementation strategies
- Learning new Effect features

## Pattern Library Location

**Local Patterns**: `.claude/skills/effect-patterns-hub/patterns/`  
**Documentation**: `docs/effect-patterns/`  
**Count**: 130+ patterns in MDX format

## Quick Decision Tree

### I need to...

#### **Create Effects**
- From value → [`constructor-succeed-some-right.mdx`](patterns/constructor-succeed-some-right.mdx)
- From sync code → [`constructor-sync-async.mdx`](patterns/constructor-sync-async.mdx)
- From promise → [`constructor-try-trypromise.mdx`](patterns/constructor-try-trypromise.mdx)
- From nullable → [`constructor-from-nullable-option-either.mdx`](patterns/constructor-from-nullable-option-either.mdx)
- Pre-resolved → [`create-pre-resolved-effect.mdx`](patterns/create-pre-resolved-effect.mdx)

#### **Transform & Compose**
- Map values → [`combinator-map.mdx`](patterns/combinator-map.mdx)
- Chain effects → [`combinator-flatmap.mdx`](patterns/combinator-flatmap.mdx)
- Sequence operations → [`combinator-sequencing.mdx`](patterns/combinator-sequencing.mdx)
- Combine values → [`combinator-zip.mdx`](patterns/combinator-zip.mdx)
- Filter → [`combinator-filter.mdx`](patterns/combinator-filter.mdx)
- Conditional logic → [`combinator-conditional.mdx`](patterns/combinator-conditional.mdx)
- Process collections → [`combinator-foreach-all.mdx`](patterns/combinator-foreach-all.mdx)

#### **Control Flow**
- Sequential logic → [`write-sequential-code-with-gen.mdx`](patterns/write-sequential-code-with-gen.mdx)
- Business logic → [`use-gen-for-business-logic.mdx`](patterns/use-gen-for-business-logic.mdx)
- Pipe composition → [`use-pipe-for-composition.mdx`](patterns/use-pipe-for-composition.mdx)
- Branching workflows → [`conditionally-branching-workflows.mdx`](patterns/conditionally-branching-workflows.mdx)
- Combinators → [`control-flow-with-combinators.mdx`](patterns/control-flow-with-combinators.mdx)
- Repetition → [`control-repetition-with-schedule.mdx`](patterns/control-repetition-with-schedule.mdx)

#### **Error Handling**
- Define errors → [`define-tagged-errors.mdx`](patterns/define-tagged-errors.mdx)
- Catch specific errors → [`pattern-catchtag.mdx`](patterns/pattern-catchtag.mdx)
- Handle all errors → [`handle-errors-with-catch.mdx`](patterns/handle-errors-with-catch.mdx)
- Retry operations → [`retry-based-on-specific-errors.mdx`](patterns/retry-based-on-specific-errors.mdx)
- Flaky operations → [`handle-flaky-operations-with-retry-timeout.mdx`](patterns/handle-flaky-operations-with-retry-timeout.mdx)
- Map errors → [`mapping-errors-to-fit-your-domain.mdx`](patterns/mapping-errors-to-fit-your-domain.mdx)
- Handle unexpected → [`handle-unexpected-errors-with-cause.mdx`](patterns/handle-unexpected-errors-with-cause.mdx)
- API errors → [`handle-api-errors.mdx`](patterns/handle-api-errors.mdx)

#### **Concurrency**
- Parallel execution → [`run-effects-in-parallel-with-all.mdx`](patterns/run-effects-in-parallel-with-all.mdx)
- Background tasks → [`run-background-tasks-with-fork.mdx`](patterns/run-background-tasks-with-fork.mdx)
- Process collections → [`process-collection-in-parallel-with-foreach.mdx`](patterns/process-collection-in-parallel-with-foreach.mdx)
- Race effects → [`race-concurrent-effects.mdx`](patterns/race-concurrent-effects.mdx)
- Fibers explained → [`understand-fibers-as-lightweight-threads.mdx`](patterns/understand-fibers-as-lightweight-threads.mdx)
- Decouple with queues → [`decouple-fibers-with-queue-pubsub.mdx`](patterns/decouple-fibers-with-queue-pubsub.mdx)
- Polling → [`poll-for-status-until-task-completes.mdx`](patterns/poll-for-status-until-task-completes.mdx)
- Graceful shutdown → [`implement-graceful-shutdown.mdx`](patterns/implement-graceful-shutdown.mdx)

#### **Services & Dependency Injection**
- Model dependencies → [`model-dependencies-as-services.mdx`](patterns/model-dependencies-as-services.mdx)
- Understand layers → [`understand-layers-for-dependency-injection.mdx`](patterns/understand-layers-for-dependency-injection.mdx)
- Scoped services → [`scoped-service-layer.mdx`](patterns/scoped-service-layer.mdx)
- Composable modules → [`organize-layers-into-composable-modules.mdx`](patterns/organize-layers-into-composable-modules.mdx)
- Compose scoped layers → [`compose-scoped-layers.mdx`](patterns/compose-scoped-layers.mdx)
- Provide config → [`provide-config-layer.mdx`](patterns/provide-config-layer.mdx)
- Caching wrapper → [`add-caching-by-wrapping-a-layer.mdx`](patterns/add-caching-by-wrapping-a-layer.mdx)

#### **Resource Management**
- Bracket pattern → [`safely-bracket-resource-usage.mdx`](patterns/safely-bracket-resource-usage.mdx)
- Scope management → [`manage-resource-lifecycles-with-scope.mdx`](patterns/manage-resource-lifecycles-with-scope.mdx)
- Manual scope → [`manual-scope-management.mdx`](patterns/manual-scope-management.mdx)
- Scoped resources runtime → [`create-managed-runtime-for-scoped-resources.mdx`](patterns/create-managed-runtime-for-scoped-resources.mdx)

#### **Streaming**
- Process streaming data → [`process-streaming-data-with-stream.mdx`](patterns/process-streaming-data-with-stream.mdx)
- From iterable → [`stream-from-iterable.mdx`](patterns/stream-from-iterable.mdx)
- From file → [`stream-from-file.mdx`](patterns/stream-from-file.mdx)
- From paginated API → [`stream-from-paginated-api.mdx`](patterns/stream-from-paginated-api.mdx)
- Concurrent processing → [`stream-process-concurrently.mdx`](patterns/stream-process-concurrently.mdx)
- Batch processing → [`stream-process-in-batches.mdx`](patterns/stream-process-in-batches.mdx)
- Collect results → [`stream-collect-results.mdx`](patterns/stream-collect-results.mdx)
- Run for effects → [`stream-run-for-effects.mdx`](patterns/stream-run-for-effects.mdx)
- Manage resources → [`stream-manage-resources.mdx`](patterns/stream-manage-resources.mdx)
- Retry on failure → [`stream-retry-on-failure.mdx`](patterns/stream-retry-on-failure.mdx)

#### **Schema & Validation**
- Define contracts → [`define-contracts-with-schema.mdx`](patterns/define-contracts-with-schema.mdx)
- Parse/decode → [`parse-with-schema-decode.mdx`](patterns/parse-with-schema-decode.mdx)
- Transform data → [`transform-data-with-schema.mdx`](patterns/transform-data-with-schema.mdx)
- Validate body → [`validate-request-body.mdx`](patterns/validate-request-body.mdx)
- Brand types → [`brand-model-domain-type.mdx`](patterns/brand-model-domain-type.mdx)
- Brand validation → [`brand-validate-parse.mdx`](patterns/brand-validate-parse.mdx)
- Config schema → [`define-config-schema.mdx`](patterns/define-config-schema.mdx)

#### **Data Types**
- Option → [`data-option.mdx`](patterns/data-option.mdx), [`model-optional-values-with-option.mdx`](patterns/model-optional-values-with-option.mdx)
- Either → [`data-either.mdx`](patterns/data-either.mdx), [`accumulate-multiple-errors-with-either.mdx`](patterns/accumulate-multiple-errors-with-either.mdx)
- Chunk → [`data-chunk.mdx`](patterns/data-chunk.mdx), [`use-chunk-for-high-performance-collections.mdx`](patterns/use-chunk-for-high-performance-collections.mdx)
- Array → [`data-array.mdx`](patterns/data-array.mdx)
- HashSet → [`data-hashset.mdx`](patterns/data-hashset.mdx)
- Duration → [`data-duration.mdx`](patterns/data-duration.mdx), [`representing-time-spans-with-duration.mdx`](patterns/representing-time-spans-with-duration.mdx)
- DateTime → [`data-datetime.mdx`](patterns/data-datetime.mdx), [`beyond-the-date-type.mdx`](patterns/beyond-the-date-type.mdx)
- BigDecimal → [`data-bigdecimal.mdx`](patterns/data-bigdecimal.mdx)
- Cause → [`data-cause.mdx`](patterns/data-cause.mdx)
- Exit → [`data-exit.mdx`](patterns/data-exit.mdx)
- Ref → [`data-ref.mdx`](patterns/data-ref.mdx), [`manage-shared-state-with-ref.mdx`](patterns/manage-shared-state-with-ref.mdx)
- Redacted → [`data-redacted.mdx`](patterns/data-redacted.mdx)
- Case → [`data-case.mdx`](patterns/data-case.mdx)
- Class → [`data-class.mdx`](patterns/data-class.mdx)
- Struct → [`data-struct.mdx`](patterns/data-struct.mdx)
- Tuple → [`data-tuple.mdx`](patterns/data-tuple.mdx)

#### **Pattern Matching**
- Match API → [`pattern-match.mdx`](patterns/pattern-match.mdx)
- Effectful match → [`pattern-matcheffect.mdx`](patterns/pattern-matcheffect.mdx)
- Tag matching → [`pattern-matchtag.mdx`](patterns/pattern-matchtag.mdx)
- Option/Either checks → [`pattern-option-either-checks.mdx`](patterns/pattern-option-either-checks.mdx)

#### **HTTP & Web**
- Basic HTTP server → [`build-a-basic-http-server.mdx`](patterns/build-a-basic-http-server.mdx)
- Launch server → [`launch-http-server.mdx`](patterns/launch-http-server.mdx)
- Handle GET → [`handle-get-request.mdx`](patterns/handle-get-request.mdx)
- HTTP client request → [`make-http-client-request.mdx`](patterns/make-http-client-request.mdx)
- Testable HTTP client → [`create-a-testable-http-client-service.mdx`](patterns/create-a-testable-http-client-service.mdx)
- JSON response → [`send-json-response.mdx`](patterns/send-json-response.mdx)
- Path parameters → [`extract-path-parameters.mdx`](patterns/extract-path-parameters.mdx)
- Provide dependencies to routes → [`provide-dependencies-to-routes.mdx`](patterns/provide-dependencies-to-routes.mdx)

#### **Testing**
- Mocking dependencies → [`mocking-dependencies-in-tests.mdx`](patterns/mocking-dependencies-in-tests.mdx)
- Use Default layer → [`use-default-layer-for-tests.mdx`](patterns/use-default-layer-for-tests.mdx)
- Tests adapt to code → [`write-tests-that-adapt-to-application-code.mdx`](patterns/write-tests-that-adapt-to-application-code.mdx)

#### **Observability**
- Structured logging → [`leverage-structured-logging.mdx`](patterns/leverage-structured-logging.mdx), [`observability-structured-logging.mdx`](patterns/observability-structured-logging.mdx)
- Tracing spans → [`trace-operations-with-spans.mdx`](patterns/trace-operations-with-spans.mdx), [`observability-tracing-spans.mdx`](patterns/observability-tracing-spans.mdx)
- Custom metrics → [`add-custom-metrics.mdx`](patterns/add-custom-metrics.mdx), [`observability-custom-metrics.mdx`](patterns/observability-custom-metrics.mdx)
- OpenTelemetry → [`observability-opentelemetry.mdx`](patterns/observability-opentelemetry.mdx)
- Effect.fn instrumentation → [`observability-effect-fn.mdx`](patterns/observability-effect-fn.mdx)

#### **Runtime & Execution**
- runPromise → [`execute-with-runpromise.mdx`](patterns/execute-with-runpromise.mdx)
- runSync → [`execute-with-runsync.mdx`](patterns/execute-with-runsync.mdx)
- runFork → [`execute-long-running-apps-with-runfork.mdx`](patterns/execute-long-running-apps-with-runfork.mdx)
- Reusable runtime → [`create-reusable-runtime-from-layers.mdx`](patterns/create-reusable-runtime-from-layers.mdx)

#### **Configuration**
- Access config → [`access-config-in-context.mdx`](patterns/access-config-in-context.mdx)
- Define schema → [`define-config-schema.mdx`](patterns/define-config-schema.mdx)
- Provide layer → [`provide-config-layer.mdx`](patterns/provide-config-layer.mdx)

#### **Time & Scheduling**
- Current time → [`accessing-current-time-with-clock.mdx`](patterns/accessing-current-time-with-clock.mdx)
- Duration → [`representing-time-spans-with-duration.mdx`](patterns/representing-time-spans-with-duration.mdx)
- DateTime → [`beyond-the-date-type.mdx`](patterns/beyond-the-date-type.mdx)
- Schedule repetition → [`control-repetition-with-schedule.mdx`](patterns/control-repetition-with-schedule.mdx)

#### **Project Setup**
- New project → [`setup-new-project.mdx`](patterns/setup-new-project.mdx)
- Editor LSP → [`supercharge-your-editor-with-the-effect-lsp.mdx`](patterns/supercharge-your-editor-with-the-effect-lsp.mdx)
- AI agents MCP → [`teach-your-ai-agents-effect-with-the-mcp-server.mdx`](patterns/teach-your-ai-agents-effect-with-the-mcp-server.mdx)

#### **Advanced Concepts**
- Structural equality → [`comparing-data-by-value-with-structural-equality.mdx`](patterns/comparing-data-by-value-with-structural-equality.mdx)
- Effect channels → [`understand-effect-channels.mdx`](patterns/understand-effect-channels.mdx)
- Effects are lazy → [`effects-are-lazy.mdx`](patterns/effects-are-lazy.mdx)
- Not found vs errors → [`distinguish-not-found-from-errors.mdx`](patterns/distinguish-not-found-from-errors.mdx)
- Promise problems → [`solve-promise-problems-with-effect.mdx`](patterns/solve-promise-problems-with-effect.mdx)
- Avoid long chains → [`avoid-long-andthen-chains.mdx`](patterns/avoid-long-andthen-chains.mdx)

## Pattern Categories

### By Skill Level

**Beginner** (Getting Started)
- Constructor patterns (succeed, fail, sync, async)
- Basic combinators (map, flatMap, tap)
- Simple error handling (catch, catchTag)
- Effect.gen basics
- runPromise/runSync

**Intermediate** (Building Applications)
- Services and layers
- Schema validation
- HTTP servers and clients
- Resource management
- Concurrency basics (Effect.all, fork)
- Testing with mocks

**Advanced** (Production Systems)
- Complex layer composition
- Custom runtimes
- Streaming pipelines
- Graceful shutdown
- OpenTelemetry integration
- Performance optimization (Chunk, Ref)

### By Use Case

**Domain Modeling**
- Schema definitions
- Brand types
- Tagged errors
- Option/Either for optional/fallible values

**API Development**
- HTTP server setup
- Route handling
- Request validation
- Error handling
- Response formatting

**Data Processing**
- Stream processing
- Batch operations
- Parallel processing
- Resource-safe pipelines

**Application Architecture**
- Service layer design
- Dependency injection
- Module composition
- Configuration management

**Testing**
- Mock layers
- Test utilities
- Testable services

**Observability**
- Structured logging
- Distributed tracing
- Custom metrics
- Performance monitoring

## Search Patterns

### By Keyword

Use `Grep` to search patterns by keyword:

```bash
# Find patterns about error handling
grep -l "error" patterns/*.mdx

# Find patterns about concurrency
grep -l "concurrent\|parallel\|fiber" patterns/*.mdx

# Find patterns about HTTP
grep -l "http\|server\|client" patterns/*.mdx

# Find patterns about testing
grep -l "test\|mock" patterns/*.mdx
```

### By Frontmatter Tags

All patterns include metadata:
- `title`: Human-readable name
- `id`: Unique identifier (filename without extension)
- `skillLevel`: beginner, intermediate, advanced
- `useCase`: domain-modeling, error-handling, concurrency, etc.
- `summary`: Brief description
- `tags`: Keywords for searching
- `related`: Links to related patterns

### Common Searches

**"How do I create an Effect from..."**
- → Search constructor patterns: `grep -l "constructor" patterns/*.mdx`
- → Check `constructor-*.mdx` files

**"How do I handle errors when..."**
- → Search error handling: `grep -l "error\|catch\|retry" patterns/*.mdx`
- → Check `handle-*.mdx` and `pattern-catchtag.mdx`

**"How do I run multiple things concurrently?"**
- → Search concurrency: `grep -l "concurrent\|parallel\|all\|fork" patterns/*.mdx`
- → Check `run-effects-in-parallel-with-all.mdx`

**"How do I work with services?"**
- → Search services: `grep -l "service\|layer\|dependency" patterns/*.mdx`
- → Check `model-dependencies-as-services.mdx`, `understand-layers-for-dependency-injection.mdx`

**"How do I validate data?"**
- → Search schema: `grep -l "schema\|validate\|parse" patterns/*.mdx`
- → Check `define-contracts-with-schema.mdx`, `parse-with-schema-decode.mdx`

## Integration with Other Skills

### Foundations → Patterns Hub
When you need concrete examples for foundation concepts, check patterns:
- `effect-foundations` teaches concepts → patterns show implementation

### Architect → Patterns Hub
When designing systems, reference architectural patterns:
- Layer composition → `organize-layers-into-composable-modules.mdx`
- Service design → `model-dependencies-as-services.mdx`
- Scoped resources → `scoped-service-layer.mdx`

### Engineer → Patterns Hub
When implementing features, find relevant patterns:
- HTTP endpoints → `handle-get-request.mdx`, `validate-request-body.mdx`
- Error handling → `retry-based-on-specific-errors.mdx`
- Concurrency → `run-effects-in-parallel-with-all.mdx`

### Tester → Patterns Hub
When writing tests, reference testing patterns:
- Mock services → `mocking-dependencies-in-tests.mdx`
- Test layers → `use-default-layer-for-tests.mdx`
- Testable design → `write-tests-that-adapt-to-application-code.mdx`

## Usage Workflow

1. **Identify Need**: "I need to [do something] with Effect"
2. **Check Decision Tree**: Find relevant section above
3. **Read Pattern**: Use `Read` tool on the pattern file
4. **Adapt to Context**: Apply pattern to your specific use case
5. **Check Related**: Follow `related` links in pattern frontmatter
6. **Consult Agent**: If unclear, use `@effect-engineer` or `@effect-architect`

## Anti-Pattern Detection

If you find yourself:
- Using imperative loops → Check `process-collection-in-parallel-with-foreach.mdx`
- Mixing promises and Effects → Check `constructor-try-trypromise.mdx`, `solve-promise-problems-with-effect.mdx`
- Long andThen chains → Check `avoid-long-andthen-chains.mdx`, `use-gen-for-business-logic.mdx`
- Leaking requirements → Check `model-dependencies-as-services.mdx`
- Manual resource cleanup → Check `safely-bracket-resource-usage.mdx`

## Pattern File Structure

Each pattern file follows this structure:

```mdx
---
title: Human-readable title
id: kebab-case-id
skillLevel: beginner | intermediate | advanced
useCase: primary-use-case
summary: Brief description
tags:
  - keyword1
  - keyword2
related:
  - related-pattern-id-1
  - related-pattern-id-2
author: Author name
---

# Title

## Guideline
What to do

## Rationale
Why do it this way

## Good Example
✅ Recommended approach

## Bad Example
❌ What to avoid

## Related Patterns
Links to related patterns
```

## Maintenance

Patterns are synced from [EffectPatterns repository](https://github.com/PaulJPhilp/EffectPatterns).

To update patterns:
```bash
cd /tmp
git clone --depth=1 https://github.com/PaulJPhilp/EffectPatterns.git
cp -r EffectPatterns/content/published/* /Users/pooks/Dev/crate/.claude/skills/effect-patterns-hub/patterns/
cp -r EffectPatterns/content/published/* /Users/pooks/Dev/crate/docs/effect-patterns/
```

## Summary

- **130+ patterns** covering all Effect-TS concepts
- **Decision tree** for quick pattern lookup
- **Integration** with existing skills and agents
- **Searchable** by keyword, use case, skill level
- **Examples** showing good and bad practices
- **Related patterns** for deeper exploration

Use this skill as your go-to reference for "How do I... with Effect?"

