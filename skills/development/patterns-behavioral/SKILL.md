---
name: patterns-behavioral
description: "Implement behavioral design patterns (Strategy, Observer, State, Command, Chain of Responsibility, Mediator, Template Method, Iterator, Memento, Visitor). Use when you need pluggable algorithms, event/listener systems, state machines, middleware pipelines, undo/redo, or request chains. NOT for object creation (use patterns-creational); NOT for wrapping/composing objects (use patterns-structural)."
metadata: {"stage":"Mechanics","tags":["behavioral-patterns","strategy","state-machine","eventing","pipelines","middleware","pub-sub","observer","command","undo-redo"],"aliases":["strategy","observer","state-machine","command","middleware","pub-sub","event-system","pipeline","undo-redo"]}
---

# Patterns (Behavioral)

## Overview

Manage algorithms and collaboration without turning your code into nested conditionals and tight coupling. Behavioral patterns help you route requests, encapsulate actions, and swap behavior safely.

A note on scope: these guidelines assume **systemic** TypeScript (long‑lived apps/services). For short‑lived scripts, you can often simplify (fewer abstractions, more `throw`) as long as the blast radius stays small.

## Workflow

1. Decide “scriptic vs systemic” and set policies (error semantics, boundary validation, ownership/lifetimes).
2. Identify the interaction pressure: pipelines, events, undo, state machines, or algorithm selection.
3. Draw a quick responsibility map: who triggers actions, who owns state, who receives outcomes?
4. Pick a pattern that makes responsibilities explicit (interfaces + concrete behaviors).
5. Implement with clear contracts and tests for ordering, error semantics (Result vs throw), and lifetimes (unsubscribe/shutdown).

## Chooser

- **Chain of Responsibility**: configurable pipeline; each handler may handle or pass along.
- **Command**: represent actions as objects; queue/schedule/undo/retry.
- **Iterator**: traverse collections/graphs without exposing representation.
- **Mediator**: central coordinator to reduce many-to-many coupling.
- **Memento**: snapshot/restore object state; undo/redo without leaking internals.
- **Observer**: pub/sub updates; multiple listeners react to events.
- **State**: state machine; behavior varies by state; transitions are explicit.
- **Strategy**: swap algorithms behind a stable interface (runtime/config selection).
- **Template Method**: stable algorithm skeleton with overridable steps (often via hooks; use inheritance only when it already fits).
- **Visitor**: add new operations across a stable object structure without changing element classes.

## Implementation Checklist

- Make ordering explicit for pipelines and observers; define error semantics (what’s expected vs unknown).
- For expected failures, prefer typed unions/`Result`; reserve `throw` for unknown/unrecoverable and catch/convert at boundaries.
- Treat boundary inputs as `unknown` (events/requests) and validate/decode once near the edge.
- For async observers/pipelines, make ownership explicit: unsubscribe/shutdown, backpressure/queueing, and cancellation (`AbortSignal`).
- Keep strategies/states small and pure when possible; inject dependencies via context.
- Prefer composition for Strategy/State; reserve Template Method for cases where inheritance is already a fit.
- For Command/Memento: define serialization and persistence needs early (in-memory vs durable; versioned formats).

## Snippets (optional)

- TypeScript: [`references/snippets/typescript.md`](references/snippets/typescript.md)
- React: [`references/snippets/react.md`](references/snippets/react.md)

## References

Read the relevant reference file before implementing or refactoring toward the pattern:

- [`references/chain-of-responsibility.md`](references/chain-of-responsibility.md)
- [`references/command.md`](references/command.md)
- [`references/iterator.md`](references/iterator.md)
- [`references/mediator.md`](references/mediator.md)
- [`references/memento.md`](references/memento.md)
- [`references/observer.md`](references/observer.md)
- [`references/state.md`](references/state.md)
- [`references/strategy.md`](references/strategy.md)
- [`references/template-method.md`](references/template-method.md)
- [`references/visitor.md`](references/visitor.md)

Each reference includes: selection cues, minimal structure, pitfalls, and test ideas.

## Output Template

When applying a behavioral pattern, return:

- The pressure you’re addressing (pipeline/eventing/undo/state/algorithm selection) and why this pattern fits.
- The proposed seam (interfaces/contracts) and who owns state and lifetimes (subscribe/unsubscribe, start/stop).
- Verification steps (tests for ordering, expected failures, and shutdown/cancellation).
