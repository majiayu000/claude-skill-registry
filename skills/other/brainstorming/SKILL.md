---
name: brainstorming
description: Structured idea generation + multi-LLM debate for the product-owner stage. Diverge (generate genuinely different bets), debate (a 4-persona panel on 4 models argues over 2 rounds), converge (synthesize a recommendation). Used by product-owner before architect; available to architect for design-space exploration.
when_to_use: |
  Apply when:
  - product-owner is turning a raw idea/problem into a validated brief
  - the decision is "what/whether to build", not "how to build it"
  - an idea needs adversarial pressure-testing before committing engineering time
  - architect wants to explore a wide design space before picking an approach
effort: medium
allowed-tools: Read, Write, Task, mcp__great_cto_llm_router__ask_kimi
---

# brainstorming

Idea work has three movements: **diverge → debate → converge**. Most teams skip
the middle one and converge on the first plausible idea. The debate panel is the
point of this skill.

## 1. Diverge — generate genuinely different bets

From a *framed problem* (who · cost-of-pain · why-now · success metric), produce
**3–5 distinct approaches** — different bets, not cosmetic variants. Force
diversity along at least one axis each:

- **different user** (who you serve first)
- **different wedge** (the one feature you lead with)
- **different scope** (concierge/manual vs full self-serve)
- **different business shape** (tool you sell vs outcome you deliver)

For each: *the core bet · the smallest version that tests it · the main risk.*
Reject near-duplicates — if two options share the same bet, drop one and push
for a more contrarian alternative.

## 2. Debate — the idea-debate panel

Four personas, **four different models**, two rounds. Model diversity matters:
different model families fail differently, so they catch different holes.

| Persona | Stance — argues… | Model | Invocation |
|---|---|---|---|
| **Visionary** | the strongest case FOR — the 10x outcome if it works | `claude-opus-4-8` | `Task`, `model: opus` |
| **Skeptic** | the strongest case AGAINST — why it fails / who tried & died | `claude-sonnet-4-6` | `Task`, `model: sonnet` |
| **User-Advocate** | the user's honest reaction — would I pay / switch / care? AND, for any product that messages or collects data from end-recipients, the recipient's consent/opt-in friction (TCPA / opt-out / spam fatigue / who refuses) | `claude-haiku-4-5` | `Task`, `model: haiku` |
| **Pragmatist** | cost, time-to-ship, build-vs-buy, unit economics | Kimi K2 | `mcp__great_cto_llm_router__ask_kimi` |

### Round 1 — opening positions (blind, parallel)

Spawn the three `Task` personas **in one message** (parallel) + call the Kimi
router for the Pragmatist. Each gets the framed problem + the diverge options and
**only its own stance**. Prompt template:

> You are the **{persona}** on a product debate panel. Stance: **{stance}**.
> Problem: {framing}. Options on the table: {options}.
> Make the strongest possible {for/against} case. Be specific and concrete — name
> the mechanism, the comparable, the number. End with: verdict (BUILD / DON'T /
> PIVOT-to-which-option) + your single biggest worry.

### Round 2 — rebuttal (informed)

Feed each persona the **other three's Round-1 positions**. Ask:

> Here are the other panelists' positions: {r1_others}. Rebut the one you most
> disagree with. Then give your updated verdict and **the one condition that
> would change your mind.**

### Convergence guard

If all four agree in Round 1, the framing was too soft — re-run with a sharper,
explicitly contrarian Skeptic ("assume this is a bad idea; prove it"). Genuine
consensus only counts when the Skeptic was given every chance to kill it.

## 3. Converge — synthesize (the chair decides)

The product-owner (Opus) is the **chair**, not a vote-counter. Read all eight
statements and produce:

- **The decisive consideration** — the one argument that actually settles it
- **Strongest FOR** and **strongest AGAINST** (steelmanned, attributed)
- **The call** — BUILD / DON'T BUILD / PIVOT, with the reason in one sentence
- **What would flip it** — the kill-criteria / the condition to revisit
- **Dissent preserved** — if a persona held a strong minority view, record it;
  don't launder it out. Tomorrow's "why didn't we think of X" lives here.

Feed this straight into the product brief's **Debate digest** section.

## Cost note

The panel is ~$0.30–0.60 per idea (one Opus + one Sonnet + one Haiku + one Kimi
call × 2 rounds). That is the cheapest insurance in the pipeline: it runs before
any engineering time is spent, at the stage where "no" is free and "yes" is
expensive.
