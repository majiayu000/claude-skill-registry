---
name: to-tickets
description: 'Break a plan, spec, or conversation into tracer-bullet tickets, each declaring the tickets that block it, published as GitHub issues or local files. Use when a settled plan needs decomposing into implementation tickets, including wide refactors that need expand-contract sequencing.'
---

# To tickets

Turn a settled plan into implementation tickets before any code exists.

`wayfinder` charts decision tickets when the route is foggy. `atomic-issues-prs` publishes code that is already written. This skill starts only after the route is clear and before implementation begins.

## Draft vertical slices

- Cut each slice as a narrow but complete path through every layer it needs.
- Make each completed slice demoable or verifiable on its own.
- Size each slice to fit one fresh context window.
- Put prefactoring first. Make the change easy, then make the easy change.

Every ticket lists the tickets that must finish before it can start. A ticket with no blockers starts immediately. Work the frontier: any ticket whose blockers are all done.

## Handle wide refactors

A wide refactor is one mechanical change whose blast radius fans across the codebase, so no vertical slice can land green.

Sequence it as expand, migrate, then contract:

1. **Expand.** Add the new form beside the old form so nothing breaks.
2. **Migrate.** Move call sites in batches sized by blast radius. Make each batch a ticket blocked by the expand ticket. Keep CI green between batches because the old form still exists.
3. **Contract.** Delete the old form in a final ticket blocked by every migrate ticket.

When a migrate batch cannot stay green alone, keep the sequence but use a shared integration branch. Every batch then blocks one final integrate-and-verify ticket. Promise green only at that final ticket.

## Get approval

Present the draft as a numbered list. Show each ticket's title, blocked-by list, and delivered behavior. Ask:

- Is the granularity right?
- Does each blocking edge genuinely gate the ticket?
- Should any ticket merge with another or split further?

Iterate until the user approves. Publish nothing before approval.

## Resolve storage

Detect storage from the repository. Never ask when the repository answers it.

- **GitHub remote present.** Publish one issue per ticket in dependency order, blockers first, so each edge can reference a real identifier. Use native blocking or sub-issue links when GitHub provides them. Otherwise add a `Blocked by` section. Apply `ready-for-agent` only when the repository already defines that label.
- **No GitHub remote.** Write one file per ticket at `.outline/to-tickets/<feature-slug>/<NN>-<slug>.md`. Number files from `01` in dependency order, blockers first. Never combine tickets into one file.

## Local ticket template

```markdown
# <NN>: <Ticket title>

## What to build

<End-to-end behavior from the user's point of view, not a layer-by-layer list.>

## Blocked by

<Ticket numbers and titles, or "None, can start immediately".>

## Acceptance criteria

- [ ] Observable criterion one
- [ ] Observable criterion two
```

## GitHub issue template

```markdown
## Parent

<Optional parent issue reference. Omit this section when there is no parent.>

## What to build

<End-to-end behavior from the user's point of view, not a layer-by-layer list.>

## Blocked by

<Issue references, or "None, can start immediately".>

## Acceptance criteria

- [ ] Observable criterion one
- [ ] Observable criterion two
```

Omit file paths and code snippets because they go stale. A prototype-produced snippet may be inlined when it records a decision more precisely than prose, such as a state machine, reducer, schema, or type shape. Trim it to the decision-rich part and state that it came from a prototype.
