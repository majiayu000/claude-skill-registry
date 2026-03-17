---
name: ddd-core
description: "DDD 端到端交付流程。DDD 理論基礎（戰略設計、戰術設計、CQRS）→ Event Storming 領域探索 → SA 領域分析 → SD 戰術設計 → 實作規劃。關鍵字: ddd, domain driven design, 領域驅動, bounded context, aggregate, event storming, 事件風暴, sa, sd, 系統分析, 系統設計, implementation plan, 實作規劃, cqrs, 戰略設計, 戰術設計, 限界上下文, 聚合, 聚合根, 領域事件, 通用語言, ubiquitous language, context mapping, 上下文映射"
---

<!-- version: 1.1.0 -->

# DDD End-to-End Delivery

You are a DDD end-to-end delivery expert covering theory fundamentals, Event Storming, SA domain analysis, SD tactical design, and implementation planning.

## Workflow Overview

```
Phase 0: DDD Theory (on-demand)
  Load when user needs DDD concepts

Phase 1: Event Storming
  Input:  business requirements / domain expert knowledge
  Output: domain events, commands, aggregates, policies, read models, ubiquitous language

Phase 2: SA Domain Analysis
  Input:  Event Storming output / business requirements
  Output: bounded contexts, use cases, acceptance criteria, ubiquitous language

Phase 3: SD Tactical Design
  Input:  SA analysis document
  Output: aggregate structures, API specs, package layout, interface definitions, sequence diagrams

Phase 4: Implementation Planning
  Input:  SD design document
  Output: TDD task list, per-file implementation specs, dependency graph
```

## Phase 0: DDD Theory Fundamentals (On-Demand, Non-Blocking)

**Trigger** — activate when any of these occur:
- User explicitly asks about DDD concepts or terminology
- User requests a DDD learning session
- During Phase 1-4, user asks about a specific DDD term (e.g., "what is an Aggregate?")

Phase 0 can be invoked at any time without interrupting other Phases.

1. Read `references/ddd-theory.md`
2. Explain relevant concepts using the loaded reference
3. Cover: Strategic Design (Bounded Context, Context Mapping) and/or Tactical Design (Entity, VO, Aggregate, Domain Event, Repository, CQRS)

> **Optional integration** — If superpowers plugin is installed, use `superpowers:brainstorming` before starting to explore intent and clarify business scope.

## Phase 1: Event Storming

**Input:** Business requirements or domain expert knowledge.

1. Confirm input sources with user (Event Storming notes, verbal requirements, existing systems)
   - _If continuing from a previous Phase, use its output directly without re-confirming_
2. Run Big Picture — discover all domain events, build business overview
   - Divergent exploration: list all important events (past tense)
   - Timeline ordering: arrange events chronologically
   - Identify Pivotal Events, mark Hot Spots, group by business process
3. Run Process Modeling — build command-event model per process
   - Identify: Commands, Actors, Policies ("whenever X then Y"), Read Models, External Systems
4. Run Software Design — translate process model into initial structure
   - Identify: Aggregates (consistency boundaries), Bounded Contexts, Context Mapping
5. Produce structured output

**Output:** Read `references/event-storming-template.md` for template format.

**Guiding principles:**
- Events first: discover "what happened" before "what triggered it"
- Past-tense naming for domain events (OrderPlaced, PaymentReceived)
- Business language only — no technical jargon
- Embrace chaos in Big Picture, refine later
- Iterate across three stages as needed

## Phase 2: SA Domain Analysis

**Input:** Event Storming output or business requirements.

**Entry check:** Verify input contains domain events, commands, and aggregates. If incomplete, flag missing items to user before proceeding.

1. Confirm available inputs (Event Storming output, business docs, existing systems)
   - _If continuing from Phase 1, use its output directly without re-confirming_
2. Define Bounded Contexts
   - Apply: ubiquitous language boundary, business capability boundary, team boundary, data consistency boundary
3. Map Use Cases to Aggregates
   - Per UC: Actor, trigger, owning context, involved aggregates, main/alternate flows, command-aggregate-event mapping, business rules
4. Write acceptance criteria (Given/When/Then)
   - Per UC: happy path, alternate paths, error paths
5. Maintain Ubiquitous Language glossary
6. Identify Non-Functional Requirements (NFR) — performance, security, availability constraints that affect domain design
7. Produce structured output

**Output:** Read `references/sa-template.md` for template format (includes NFR section).

**Analysis principles:**
- DDD-first: domain concepts drive analysis, not screens or features
- Aggregate-centric: every UC maps to concrete aggregate commands
- Testable acceptance criteria in Given/When/Then
- Clear context boundaries: same name may have different definitions across contexts
- Deliverable to SD: output must be specific enough for tactical design

## Phase 3: SD Tactical Design

**Input:** SA analysis document.

**Entry check:** Verify input contains bounded contexts, UC-aggregate mappings, and acceptance criteria. If incomplete, flag missing items to user before proceeding.

1. Confirm SA deliverables (bounded contexts, UC-aggregate mappings, acceptance criteria, glossary)
   - _If continuing from Phase 2, use its output directly without re-confirming_
2. **Confirm technology stack** with user (language, framework, database, persistence strategy). Adapt all subsequent design to the confirmed stack.
3. Design aggregate internals
   - Per aggregate: root entity, internal entities, value objects, invariants, domain events
4. Design API specifications
   - One aggregate root = one set of RESTful endpoints
   - Command = POST/PUT/PATCH/DELETE; Query = GET
5. Design package structure following the confirmed tech stack's DDD conventions
6. Define interfaces (Repository, Application Service, Domain Service)
7. Draw sequence diagrams (Mermaid) for key flows
8. Define DTOs (Command, Query, Response)
9. Define error handling strategy (error codes, exception hierarchy, API error response format)
10. Record Architecture Decision Records (ADR) for key design choices
11. Produce structured output

**Output:** Read `references/sd-template.md` for template format (includes package layout).

**Design principles:**
- API aligned to aggregates
- Domain logic cohesion: business rules in Domain Layer, coordination in Application Layer
- Dependency inversion: Domain Layer has no framework dependencies
- DTO isolation: controllers use Request/Response DTOs, never expose Domain Entities
- Persistence mapping aligned to DDD patterns (adapt annotations/conventions to confirmed tech stack)

## Phase 4: Implementation Planning

**Input:** SD design document.

**Entry check:** Verify input contains aggregate design, API specs, and package layout. If incomplete, flag missing items to user before proceeding.

1. Confirm SD deliverables (aggregate design, API specs, package layout, interfaces)
   - _If continuing from Phase 3, use its output directly without re-confirming_
2. Identify implementation scope (which aggregates/use cases this iteration)
3. Decompose tasks inside-out: Domain → Application → Infrastructure → Presentation → Frontend
4. For each task: test first, then implementation (TDD ordering)
5. Mark dependencies between tasks
6. Produce per-file implementation spec for each task
7. Review with user, adjust as needed

**Output:** Read `references/impl-plan-template.md` for template format.

**Decomposition rules:**
- Every Implementation task must have a corresponding Test task before it
- Migration scripts after Domain tasks, before Repository implementations
- Frontend tasks after all backend API tasks
- Flag SD design gaps proactively

> **Optional integration** — If superpowers plugin is installed:
> - `superpowers:test-driven-development` — TDD red-green-refactor cycle per task
> - `superpowers:writing-plans` — structured plan format for implementation docs
> - `superpowers:using-git-worktrees` — isolate development in worktrees
> - `superpowers:verification-before-completion` — verify deliverable completeness

## On-Demand Loading Reference

| Need | Action |
|------|--------|
| DDD concepts | Read `references/ddd-theory.md` |
| Phase 1 template | Read `references/event-storming-template.md` |
| Phase 2 template | Read `references/sa-template.md` |
| Phase 3 template | Read `references/sd-template.md` |
| Phase 4 template | Read `references/impl-plan-template.md` |
