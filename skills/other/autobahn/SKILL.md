---
name: autobahn
description: 'Carve the unsafe part out of a task up front, then run the safe remainder at full strength instead of running the whole thing timidly. Use when a task mixes reversible work with something irreversible or out of scope, such as a schema migration, a deletion, or a change to credentials or data at rest, or when the user says "autobahn this". The descope is logged as an explicit ledger, never a silent narrowing.'
---
# Autobahn

Carve guardrail-adjacent scope out of a task, then run the safe remainder at full strength in a fresh subagent that only ever sees the carved prompt.

## Method

1. **Frame.** Read the task and inputs. If the user already authorized descoping, proceed. Otherwise propose the carve, make the split explicit, and wait for approval on every gray-zone item. Bright-line exclusions are never negotiable; if the user disputes one, hand its abstract description to a fresh context for re-evaluation and record the appeal either way.
2. **Carve.** Sweep for guardrail-adjacent items. For each, class it bright-line or gray-zone, give one risk-free alternative, and name an archive destination per `../clean-and-true/references/idioms.md`. A gray-zone item the user keeps stays in scope and enters the ledger as kept-by-owner.
3. **Guard.** Distill the carve into a compact scope-guard block (absolute exclusions, allowed alternatives, authorizing context) and fold it into the carved prompt verbatim. Where the run shares filesystem or memory, tell it not to consult decision logs, notes, or transcript search. Instruct the run to build the safe scope at full strength, without hedging.
4. **Run.** Spawn a fresh, context-clean subagent with only the carved prompt. Route any new risky material back through Carve.
5. **Verify.** Run an adversarial pass over the returned deliverable across five directions and diff an independent re-sweep of the original task against the ledger, capped at one pass.
6. **Ledger.** After the run closes, report the deliverable with a descope ledger per item: class, verdict, reason, safe alternative, archive destination. Write the archive only now, after the window is closed. See `../clean-and-true/references/idioms.md` for negatives-as-corpus.

## Completion

Every guardrail-adjacent item carries a class, a verdict, a safe alternative, and an archive destination. The ledger is visible. The executing subagent saw only the carved prompt and its guard held. No safe work was diluted and no excluded material was elaborated.

