---
name: router
description: Use when routing an incoming request to Simple, Standard, or Full tier. Also detects specialized command intents before tier computation.
invocation: agent
---

# Router

Compute a tier score and confidence level to route incoming requests to the correct Arc pipeline: Simple, Standard, or Full.

## Invocation Contract

Inputs:
- Task description and constraints
- Optional explicit tier override from user

Outputs:
- Tier decision (`simple|standard|full`)
- Confidence level and routing rationale

## Scoring Dimensions

Evaluate each dimension on a 0-10 scale:

1. **Scope breadth** - How many files, modules, or systems does the change touch? A single-file tweak scores 0-2. Cross-module refactors score 6-8. Full-stack features with migrations score 8-10.

2. **Requirement clarity** - How well-defined is the ask? Exact spec with acceptance criteria scores 0-2 (low ambiguity = low complexity). Vague "make it better" requests score 7-10 because discovery work is needed.

3. **Architecture impact** - Does the change introduce new patterns, modify boundaries, or alter data flow? Cosmetic changes score 0-1. New service boundaries or API contracts score 7-10.

4. **Execution complexity** - How many sequential steps, coordination points, or failure modes exist? Single-step changes score 0-2. Multi-phase rollouts with feature flags score 7-10.

5. **Validation risk** - How hard is it to verify correctness? Adding a unit test scores 0-2. Changes requiring manual QA, staging deployment, or cross-browser testing score 7-10.

## Tier Mapping

Compute the average of all five dimensions:

- **0-3 → Simple** — Direct implementation. No plan needed. Execute and verify.
- **4-7 → Standard** — Plan first, then execute. Review the plan before implementation begins.
- **8-10 → Full** — Optional brainstorm/debate, then plan, spec (OpenSpec), review, beads, execute, verify.

## Confidence and Routing Policy

After computing the tier score, assign a confidence level (0-100) based on how clearly the dimensions map to a single tier:

- **>=80 confidence** — Auto-route to the computed tier. Announce the tier and proceed.
- **60-79 confidence** — Confirm with the user. Present the tier recommendation with reasoning and ask for approval before proceeding.
- **<60 confidence** — Ask the user. The request is too ambiguous to classify reliably. Present the scoring breakdown and ask the user to choose.

## Edge Cases

- When the score falls on a boundary (e.g., 3.5), prefer the higher tier and confirm with the user.
- When individual dimensions vary widely (e.g., scope=2 but architecture=9), flag the imbalance and recommend the higher tier.
- When the user explicitly requests a tier ("just do it" implies Simple, "let's plan this out" implies Standard), honor the explicit request regardless of the computed score.

Confidence boundary definitions: 80 is the auto-route threshold (>=80 auto-routes), 60 is the confirm threshold (60-79 confirms). A confidence of exactly 60 falls in the confirm band; a confidence of exactly 80 falls in the auto-route band.

## Intent Detection for Specialized Commands

Before computing tier scores, check whether the request matches a specialized command intent. If a match is detected with high confidence (>=80), route directly to the specialized command instead of a tier.

| Intent Pattern | Route To | Examples |
|---|---|---|
| Research, investigate, explore topic | `/arc:specialized:research` | "research OAuth patterns", "investigate caching strategies" |
| Bug, error, fix, broken, failing | `/arc:specialized:bug` | "fix the auth bug", "debug the login error" |
| Quality, refactor, improve, clean up | `/arc:specialized:quality` | "improve code quality in src/", "refactor auth module" |
| Test, TDD, test-driven, coverage | `/arc:specialized:tdd` | "add tests for auth", "implement with TDD" |
| Debug, trace, diagnose, root cause | `/arc:specialized:debug` | "debug the null pointer", "trace the timeout" |
| PRD, requirements, product spec | `/arc:specialized:prd` | "write a PRD for user auth", "define requirements" |
| Code map, map, document structure | `/arc:specialized:codemap` | "map the codebase", "generate code map" |
| PR, pull request, MR, merge request | `/arc:specialized:pr` | "create a PR", "write MR description" |
| Docs, documentation, devguide | `/arc:specialized:docs` | "generate docs for src/", "document the API" |

If the intent is ambiguous or overlaps with tier routing, fall through to normal tier computation.

## Related Skills

- After routing to **Standard** or **Full**, hand off to `plan-schema` for plan structure.
- After routing to **Full**, `brainstorm` or `debate` may precede planning.
- Execution skills (`loop`, `swarm`, `team`) activate after planning is complete.
- Specialized commands (`research`, `bug`, `quality`, `tdd`, `debug`, `prd`, `codemap`, `pr`, `docs`) bypass tier routing when intent is clear.
