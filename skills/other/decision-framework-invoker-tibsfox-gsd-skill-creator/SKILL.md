---
name: decision-framework-invoker
description: "Triggers for automatically invoking the decision-framework skill before irreversible or high-blast-radius operations. Use as a checkpoint: when a proposed action matches a trigger pattern, pause and run the appropriate framework (first-principles, inversion, decision matrix, second-order thinking) before proceeding. Prevents ad-hoc calls from becoming regret."
format: 2025-10-02
version: 1.0.0
status: ACTIVE
updated: 2026-04-17
triggers:
  - for automatically invoking the decision-framework skill before irreversible or high-blast-radius operations
  - "pattern, pause and run the appropriate framework (first-principles, inversion, decision matrix, second-order thinking) before proceeding"
---

# Decision Framework Invoker

The `decision-framework` skill provides thinking frameworks (First Principles,
5 Whys, Eisenhower, Pareto, Inversion, Second-Order, Decision Matrix). This
invoker skill captures **when to use it** — the trigger patterns that should
prompt a pause-and-frame before proceeding.

## Trigger Patterns

Invoke a decision framework when the proposed action matches any of these:

### Irreversibility
- Destructive git operations: `push --force`, `reset --hard`, `branch -D`
- Committing generated content to a shared repo (N files where N > 100)
- Applying a schema migration to a production DB
- Sending a message (Slack, email, PR comment) that cannot be recalled

→ **Framework:** Inversion ("what's the worst outcome; can we back out?")

### Blast Radius
- Changes affecting multiple packages / projects
- Renaming public APIs, CLI flags, config keys
- Removing a feature that has downstream consumers
- Rewriting > 1,000 lines across a codebase

→ **Framework:** Second-Order Thinking ("what does this cause, and what does
  that cause?")

### Multi-Option Judgment Calls
- Choosing between 3+ architectural paths
- Picking a library/framework with long-tail commitment
- Prioritizing between competing feature requests

→ **Framework:** Decision Matrix (columns = options, rows = weighted criteria)

### Root Cause Debugging
- A bug has returned after being "fixed"
- A pattern keeps recurring across unrelated work
- A test failure has non-obvious cause

→ **Framework:** 5 Whys (keep asking until you hit the infrastructural cause)

### Scoping Ambition
- Feature spec has 20+ items; need to prioritize
- Time-boxed session; need to pick highest-leverage work

→ **Framework:** Pareto 80/20 ("which 20% delivers 80% of value?")

### Reframing Stuck
- Been spinning on an approach that isn't working
- Assumptions feel embedded but might not be true

→ **Framework:** First Principles (strip to the problem; rebuild from
  truths)

## Invocation Shape

When a trigger fires:

1. **Name the trigger** in plain language: "About to commit 1,881 generated
   chapter files — this is the `blast-radius: committing generated content`
   trigger."
2. **Pick the framework** from the mapping above.
3. **Apply it in-line** in the conversation — usually 3-5 sentences is enough
   to surface the tradeoff.
4. **Record the decision** via `observe.mjs event decision <label> <payload>`
   so the retrospective captures it.
5. **Proceed** with eyes open, or adjust the approach.

## Example — The 1,881-File Publish (v1.49 release-history work)

Trigger: "About to commit 1,881 auto-generated markdown files into
`docs/release-notes/v*/chapter/`."

This hit two trigger categories:
- **Blast radius:** large diff affecting 1,881 files
- **Irreversibility-ish:** git commit is reversible, but reverting a commit
  that size is painful

Framework applied (Inversion):
- *Worst case:* "These files are regenerable from the DB. If we commit them
  and hate the shape, we can `rm -rf` and regenerate. Cost: a revert commit."
- *Best case:* "Anyone browsing the repo on GitHub can read chapters without
  running the pipeline."
- *Hidden third option:* "Commit only the top-level index files (STORY.md,
  INDEX.md) and leave per-chapter files local."

Decision: commit all 1,881. Rationale: regenerable, reviewable on GitHub,
user asked. Recorded via `observe.mjs event decision`.

## What This Skill is NOT

- A mandatory gate — you don't need a framework for every tool call
- A substitute for doing the work — frame the decision, then act
- A bureaucratic checklist — most triggers take 30 seconds to resolve

## Related

- `decision-framework` — the actual frameworks this skill invokes
- `session-observatory-live` — record the decision via observe.mjs
