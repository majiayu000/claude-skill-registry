---
name: llm-self-loop
description: 'Restructure Web-UI / human-triggered tasks into CLI + file-output loops the LLM can iterate alone. Open LLM-side observability — structured logs, file dumps, addressable scratchpads. Apply the trap-or-abandon decision: if a step cannot be looped, improve the harness rather than babysit. Trigger when the user mentions iterative grunt-work, "I have to push a button in a web UI to trigger this", monitoring dashboards, designing Claude-driven automation, or any workflow whose inner loop currently requires a human in the middle.'
---

The job: turn workflows that need a human in the inner loop into workflows the LLM closes itself. The two halves are *removing the trigger gate* and *opening observability*.

## Surface the gate first

Before proposing changes, name the trigger gate explicitly:

- *What action requires a human right now?* (button click, screenshot inspection, terminal interaction, web-form submission)
- *What signal does the human provide that the LLM cannot get on its own?* (visual confirmation, copy-paste, secret value, eyeball verdict)
- *Where does the result go?* (chat memory, screenshot, mental note)

Most loops have one or two gates that, removed, collapse the cycle to seconds. Pick the smallest gate first.

## Structural fixes

### Web-UI trigger → CLI trigger

If the workflow is gated by clicking in a web app, find or build the equivalent CLI command. Webhooks, REST endpoints, `gh` / `aws` / `gcloud` CLI subcommands, internal `just` targets — anything programmatically invokable. The LLM can then loop without leaving its session.

### Stdout-only output → file-based output

If the workflow's result lives in chat memory or a screenshot, redirect to a file the LLM can read back: structured JSON dumps, markdown reports, append-only logs with addressable offsets. *Why:* file outputs survive compaction, support diff, and are inspectable by future sessions without replaying context.

### Dashboards → structured logs

If verification requires eyeballing a Grafana / Datadog dashboard, surface the same metrics through a CLI query (PromQL, Datadog API, log aggregation tail). Anything that produces a `pass`/`fail`/`warn` verdict the LLM can read.

### Eyeball verdicts → contract assertions

If the human's role is "looks right to me", encode the criterion as a test, schema, or assertion. The contract becomes the loop's done-criterion (pair with `strict-validation-setup` for the bootstrap of those gates).

## Trap-or-abandon decision

After the structural fixes above, some steps still cannot be made autonomous — they involve genuine human judgment, external compliance, or capability the LLM lacks. For each remaining gate, apply this rule:

- **Trap** — if the step can be wrapped in a verification-and-iteration loop where the LLM proposes, the human approves once, and the LLM iterates until the contract passes, keep it. The human is at the *outer* loop, not the inner.
- **Abandon** — if a step requires the human in the *inner* loop and resists wrapping (e.g., new SOC2 review per iteration, real-time customer chat, hardware-mediated test), do not babysit. Either remove the step from the LLM's loop entirely (escalate to the human as a discrete handoff) or improve the harness so the step disappears (e.g., automate the SOC2 documentation pipeline).

Naming the rule: babysitting an unloopable step is the failure mode this skill exists to prevent. Pre-existing chat consensus: "what can't be looped — abandon firmly and improve the harness."

## What this skill does not do

- It does not author project rules — defer to `init` for AGENTS.md.
- It does not bootstrap strict-mode validation gates — defer to `strict-validation-setup`.
- It does not pick the test framework — defer to `test-driven` or the language's idiomatic tester.

## Cross-references

- `strict-validation-setup` — bootstrap the gates this skill verifies against. Pair: bootstrap once, run many.
- `odin:duet` — adjacent two-party working posture. Use `duet` when preserving the human as inner-loop director is the goal; use this skill when removing the human from the inner loop is the goal. Different ends of the same axis.

## Posture

Surgical, not architectural. Remove one gate at a time. After each fix, re-evaluate whether the loop now closes — sometimes one trigger removal is enough. Resist the temptation to redesign the whole system.
