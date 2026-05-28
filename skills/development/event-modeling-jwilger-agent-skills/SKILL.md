---
name: event-modeling
description: >-
  Event modeling facilitation for discovering and designing event-sourced
  systems. Four phases: domain discovery, workflow design (9-step process),
  GWT scenario generation, and model validation. Activate when starting a
  new project, designing features, modeling domains, writing Given/When/Then
  scenarios, or discussing event sourcing and domain-driven design.
license: CC0-1.0
metadata:
  author: jwilger
  version: "1.0"
  requires: []
  context: [event-model]
  phase: understand
  standalone: true
---

# Event Modeling

**Value:** Communication -- event modeling is a structured conversation that
surfaces hidden domain knowledge and creates shared understanding between
humans and agents before any code is written.

## Purpose

Teaches the agent to facilitate event modeling sessions following Martin
Dilger's "Understanding Eventsourcing" methodology. Produces a complete
event model (actors, events, commands, read models, automations, slices)
that drives all downstream implementation. The model lives in
`docs/event_model/`.

## Practices

### Two-Phase Process: Discovery Then Design

Never jump into detailed workflow design without broad domain understanding
first. Phase 1 maps the territory; Phase 2 explores each region.

**Phase 1 -- Domain Discovery.** Identify what the business does, who the
actors are, what major processes exist, what external systems integrate, and
which workflows to model. Ask these questions of the user; do not assume
answers. Output: `docs/event_model/domain/overview.md`.

**Phase 2 -- Workflow Design.** For each workflow, follow the 9-step
process (see `references/nine-steps.md` for the full methodology). Design
one workflow at a time. Complete all 9 steps before starting the next
workflow. Output: `docs/event_model/workflows/<name>/overview.md` plus
individual slice files in `slices/`.

### The Prime Directive: Not Losing Information

Store what happened (events), not just current state. Events are immutable
past-tense facts in business language. Every read model field must trace
back to an event. If a field has no source event, something is missing from
the model.

### Event Design Rules

1. Name events in past tense using business language: `OrderPlaced`, not
   `PlaceOrder` or `CreateOrderDTO`
2. Events are immutable facts -- never modify or delete
3. Include relevant data: what happened, when, who/what caused it
4. Find the right granularity -- not `DataUpdated` (too broad) and not
   `FieldXChanged` (too narrow)

### The Four Patterns

Every event-sourced system uses these patterns. Each pattern maps to one
vertical slice.

1. **State Change:** Command -> Event. The only way to modify state.
2. **State View:** Events -> Read Model. How the system answers queries.
3. **Automation:** Event -> Process -> Command -> Event. Background work
   triggered by events. Must have clear termination conditions.
4. **Translation:** External Data -> Internal Event. Anti-corruption layer
   for external integrations.

### GWT Scenarios

After workflow design, generate Given/When/Then scenarios for each slice.
These become acceptance criteria for implementation.

**Command scenarios:** Given = prior events establishing state. When = the
command with concrete data. Then = events produced OR an error (never both).

**View scenarios:** Given = current projection state. When = one new event.
Then = resulting projection state. Views cannot reject events.

**Critical distinction:** GWT scenarios test business rules (state-dependent
policies), not data validation (format/structure checks that belong in the
type system). If the type system can make the invalid state unrepresentable,
it is not a GWT scenario.

See `references/gwt-template.md` for the full scenario format and examples.

### Model Validation

After GWT scenarios are written, validate the model for completeness:

1. Every read model field traces to an event
2. Every event has a triggering command, automation, or translation
3. Every command has documented rejection conditions (business rules)
4. Every automation has a termination condition
5. GWT Given/When/Then clauses do not reference undefined elements

When gaps are found, ask the user to clarify, create the missing element,
and re-validate. Do not proceed with gaps remaining.

### Facilitation Mindset

You are a facilitator, not a stenographer. Ask probing questions. Challenge
assumptions. Keep asking "And then what happens?" after every event, every
command, every answer. Use business language, not technical jargon. Do not
discuss databases, APIs, frameworks, or implementation during event modeling.
The only exception: note mandatory third-party integrations by name and
purpose.

**Do:**
- Follow all steps in order -- the process reveals understanding
- Ask "And then what happens?" relentlessly
- Use concrete, realistic data in all examples and scenarios
- Design one workflow at a time
- Ensure information completeness before proceeding

**Do not:**
- Skip steps because you think you know enough
- Make architecture or implementation decisions during modeling
- Write GWT scenarios for data validation (use the type system)
- Design multiple workflows simultaneously
- Proceed with gaps in the model

## Enforcement Note

This skill provides advisory guidance. It instructs the agent on the event
modeling methodology but cannot mechanically prevent skipping steps or
producing incomplete models. On harnesses with plugin support, enforcement
plugins can add workflow gates. On other harnesses, the agent follows these
practices by convention. If you observe steps being skipped, point it out.
For available enforcement plugins, see the
[Harness Plugin Availability](../../README.md#harness-plugin-availability) table.

## Verification

After completing event modeling work, verify:

- [ ] Domain overview exists at `docs/event_model/domain/overview.md` with
      actors, workflows, external integrations, and recommended starting
      workflow
- [ ] Each designed workflow has `docs/event_model/workflows/<name>/overview.md`
      with all 9 steps completed
- [ ] All events are past tense, business language, immutable facts
- [ ] Every read model field traces to a source event
- [ ] Every event has a trigger (command, automation, or translation)
- [ ] GWT scenarios exist for each slice with concrete data
- [ ] GWT error scenarios test business rules only, not data validation
- [ ] No gaps remain in the model after validation

If any criterion is not met, revisit the relevant practice before proceeding.

## Dependencies

This skill works standalone. For enhanced workflows, it integrates with:

- **domain-modeling:** Events reveal domain types (Email, Money, OrderStatus)
  that the domain modeling skill refines
- **tdd-cycle:** Each vertical slice maps to one TDD cycle
- **architecture-decisions:** Event model informs architecture; ADRs should
  not be written during event modeling itself
- **task-management:** Workflows map to epics, slices map to tasks

Missing a dependency? Install with:
```
npx skills add jwilger/agent-skills --skill domain-modeling
```
