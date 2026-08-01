---
name: wayfinder
description: 'Chart a route through a problem too big for one session: name the destination, map the fog, and graduate it into decision tickets on the frontier. Use when planning a greenfield project or a large feature build that will not fit in a single agent session.'
---

A loose idea has arrived — too big for one agent session, and wrapped in fog: the way from here to the **destination** is not visible yet. Wayfinding charts that route step by step rather than charging blindly at the goal. This skill charts the way as a **shared map** on the issue tracker, then works its **decision tickets** — questions whose resolution is a decision, not slices of a build to execute — one at a time until the route is clear.

The destination varies per effort, and naming it is the first act of charting — it shapes every ticket. It might be a spec to hand off, an architectural decision to lock before planning, or a structural change made in place. The map is domain-agnostic — engineering work, documentation suites, or system designs.

## Plan, don't do

Wayfinder is **planning** by default: each ticket resolves a decision, and the map is done when the way is clear — nothing left to decide before someone builds. The pull to implement is the signal that you have reached the edge of the map and it is time to hand off. An effort can override this in its **Notes** section to carry execution into the map itself, but absent that instruction, produce decisions, not deliverables.

## Refer by name

Every map and ticket has a **name** — its title. In all user-facing prose — narration, summaries, and the map's Decisions-so-far — refer to tickets by title, never by bare issue numbers, IDs, or slugs. The link wraps the name (e.g. `[Define authentication schema](#12)`), keeping the tracker context legible at a glance.

## The Map

The map is the canonical index for the effort. It determines tracker storage automatically based on repository context — never ask the user:

- **GitHub repository**: If a GitHub remote exists, the map is a single GitHub issue labeled `wayfinder:map`, with decision tickets created as child issues via `gh`.
- **Local workspace**: If no GitHub remote exists, the map is stored locally at `.outline/wayfinder/map.md`, with tickets placed in `.outline/wayfinder/tickets/<id>.md`.

The map is an **index**, not a store. It lists the decisions made and links to the tickets holding their details. A decision lives in exactly one place — its ticket — so the map only gists and links it.

### The map body

The low-resolution overview loaded at the start of every session. Open tickets are not listed in the map body — they are queried dynamically from the tracker.

```markdown
## Destination

<what reaching the end of this map looks like — the spec, decision, or change this effort is finding its way to. One or two lines; every session orients to it before choosing a ticket.>

## Notes

<domain; skills every session should consult; standing preferences for this effort>

## Decisions so far

<!-- the index — one line per closed ticket: enough to judge relevance, then follow the link for full details -->

- [<closed ticket title>](link) — <one-line gist of the decision>

## Not yet specified

<!-- see "Fog of war": in-scope fog you cannot ticket yet; graduates as the frontier advances -->

## Out of scope

<!-- see "Out of scope": work ruled beyond the destination; closed, never graduates -->
```

### Tickets

Each ticket is a child issue or dedicated ticket file representing one decision or investigation sized for a single session.

```markdown
## Question

<the decision or investigation this ticket resolves>

## Blocked by

<!-- tickets or issues that must close before this ticket is on the frontier -->
- [<blocking ticket title>](link)
```
GitHub issues encode their workflow state in tracker fields: `wayfinder:<type>` label, assignee, and open/closed state. Local ticket files prepend the equivalent state:

```yaml
---
type: research # research | prototype | grilling | task
claimed_by: null
status: open # open | closed
---
```

Every ticket records one type: a `wayfinder:<type>` label on GitHub, or the local `type` field. The valid types are `research`, `prototype`, `grilling`, and `task` (see [Ticket Types](#ticket-types)).

A session **claims** a ticket before starting work: assign the GitHub issue to the driver, or set the local `claimed_by` field. An open issue with no assignee, or local ticket with `status: open` and `claimed_by: null`, is unclaimed.

Blocking uses native issue relationships on GitHub when available, falling back to the `## Blocked by` section when native dependencies are absent or when using local markdown. A ticket is **unblocked** when every ticket listed as blocking it is closed. The **frontier** consists of all open, unblocked, unclaimed tickets, calculated from issue state on GitHub or the three local fields above.

Record the resolution as a GitHub comment or local closing entry, linking any created assets. Close the issue on GitHub; locally, set `status: closed` and clear `claimed_by`.

## Ticket Types

Every ticket is classified as either **HITL** (Human In The Loop — worked interactively with the user) or **AFK** (Away From Keyboard — driven autonomously by the agent).

- **Research** (AFK): Reading documentation, third-party APIs, or codebase references to uncover facts that a decision depends on. Executed by spinning up a `research` skill subagent via `task`. Research tickets are the **one exception** to the single-ticket-per-session rule: burn them down in parallel using background subagents.
- **Prototype** (HITL): Build a rough, concrete artifact (sketch, interface mockup, minimal logic slice) to give the user something tangible to evaluate. Links the created artifact as an asset.
- **Grilling** (HITL): Interactive decision mapping and requirement clarification. Uses the `batch-ask-me` skill for batched frontier-rounds interviewing.
- **Task** (HITL or AFK): Prerequisites required before a decision can be made — provisioning, data migration, or account setup. Sized to unblock a decision, not to build the destination. Driven AFK by the agent if possible; otherwise presents the user with a structured HITL checklist.

## Fog of war

The map is deliberately incomplete: do not attempt to chart what cannot yet be seen. Beyond the live tickets lies the **fog of war** — decisions that are clearly approaching but cannot yet be specified because they depend on open questions. Resolving a ticket clears the fog ahead, graduating newly specifiable items into fresh tickets.

The map's `## Not yet specified` section captures this coarse view: suspected questions and areas to revisit later. Everything here is in scope, just not sharp enough to ticket yet.

**Fog or ticket?** Test whether the question can be phrased precisely right now:

- **Ticket when** the question is sharp — even if it is blocked by other work.
- **Not yet specified when** the question cannot yet be phrased precisely. Avoid pre-slicing the fog into premature tickets.

`## Not yet specified` excludes already-closed decisions (`## Decisions so far`), active tickets, and out-of-scope items.

## Out of scope

Fog only gathers *toward* the destination. Work beyond the destination is **out of scope** and belongs in `## Out of scope`.

Out-of-scope items never graduate. If a live ticket turns out to sit past the destination:

1. Close the ticket on the tracker.
2. Record it in `## Out of scope` with a one-line explanation of why it was ruled out, linking the closed ticket.
3. Keep it out of `## Decisions so far`, which tracks the path actually walked.

## Invocation

Work flows through two distinct modes. Never resolve more than one ticket per session — except for research tickets, which burn down in parallel.

### Chart the map

Invoked with a loose idea or request.

1. **Name the destination.** Use `askme` or `batch-ask-me` to pin down the target spec, decision, or state change that defines completion.
2. **Map the frontier.** Conduct a breadth-first interview using `batch-ask-me` to surface open decisions and immediate first steps.
   - **No-fog early exit**: If this interview reveals that the route is already clear and the journey fits in a single session, **stop**. Ask the user how they wish to proceed instead of creating an unnecessary map.
3. **Create the map.** Fill in `## Destination` and `## Notes`, leave `## Decisions so far` empty, and sketch the remaining fog in `## Not yet specified`. Use a `wayfinder:map` issue on GitHub or `.outline/wayfinder/map.md` locally.
4. **Create tickets.** Create child issues or local ticket files with appropriate `wayfinder:<type>` labels. Wire blocking edges in a second pass once IDs exist.
5. **Fire research subagents.** For every `research` ticket created, launch a parallel `task` subagent running the `research` skill to resolve it immediately.
6. Stop — initial charting completes the session.

### Work through the map

Invoked with an existing map reference.

1. Load the map body to review the destination, notes, and decisions so far.
2. Select a ticket from the frontier (or take the ticket specified by the user). **Claim it** by assigning it before beginning work.
3. Resolve the decision. Access closed ticket details as needed, consult skills listed in `## Notes`, and use `batch-ask-me` for grilling tickets.
4. Record the resolution as a comment or entry, close the ticket, and append a one-line summary link to `## Decisions so far`.
5. Graduate specifiable items from `## Not yet specified` into new tickets, clearing them from the fog list. Move any invalidated or out-of-scope items to `## Out of scope`.
