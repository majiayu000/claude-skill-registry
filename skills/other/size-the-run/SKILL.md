---
name: size-the-run
description: 'Size the cheapest sufficient capability tier and reasoning effort for a task before it starts, on a neutral two-dial scale rather than a vendor model name. Use when a run could be over- or under-powered, before dispatching a subagent, or when the user asks "how hard should I think about this", "is this worth a deep run", or "size this task". It recommends a tier and an effort and pins no vendor model.'
---
# Size the run

Size the run before you spend it: which capability tier, and how hard it should think. Read-only and advisory.

## Tier

The cheapest class whose ceiling covers the work:

- `fast` - local, mechanical, reversible work with cheap, complete verification.
- `standard` - ordinary repo-grounded reasoning, multi-step drafting, normal coding and docs.
- `frontier` - architecture, high ambiguity, safety or security risk, release-critical review, or work where one wrong assumption wastes a large run.

## Effort

How hard that mind should deliberate, as intent not a vendor level:

- `glance` - minimal deliberation, the direct path.
- `measured` - ordinary, everyday deliberation.
- `thorough` - deliberate extra: alternatives and assumptions checked.
- `exhaustive` - maximal deliberation, the search exhausted and re-checked.

Tier and effort move together by default (`fast` to `glance`, `standard` to `measured`, `frontier` to `thorough`, reserving `exhaustive` for the hardest stakes), then part where deliberation-hunger and capability-need part.

## Method

1. **Frame the unit.** Name the exact work being sized.
2. **Score once.** Read risk and complexity: ownership boundaries, reversibility and blast radius, safety or privacy risk, ambiguity and synthesis load, need for research or adversarial review, cost of a wrong answer.
3. **Read off tier.** The cheapest whose ceiling covers the judgment and risk. Risk beats size: one high-risk file can want `frontier`, a broad mechanical rename can stay `fast`.
4. **Read off effort.** Default to track tier, then raise for ambiguity or long multi-step reasoning, lower for a bounded task under a strong model. Effort buys deliberation, never capability.
5. **Report both coordinates**, one shared rationale, `move up if` and `move down if` triggers for each dial, and the proof surface the work still needs regardless of tier or effort.
6. **Stop.** Do not execute the sized task, change config, or switch models.

## Completion

The report names exactly one tier and one effort, states the cheapest sufficient pair, gives move-up and move-down triggers for both dials, names the proof surface, and makes no routing, vendor, or orchestration claim.

## Machine-readable output

```text
recommended_tier: fast|standard|frontier
recommended_effort: glance|measured|thorough|exhaustive
rationale: <one sentence, covering both dials>
move_up_if: <signals that would justify a stronger tier or higher effort>
move_down_if: <signals that would justify a cheaper tier or lower effort>
proof_surface: <verification still required>
```

