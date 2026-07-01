---
name: parallel-design-variants
description: Use when you want several genuinely different design directions to choose from instead of one design you will iterate on — a page or UI redesign, a hero, a landing, a thumbnail layout — or a live/stream design bake-off where an audience votes. Triggers on "дай варианты дизайна", "несколько вариантов на выбор", "редизайн", "design options", "design bake-off", "/parallel-design-variants".
---

# Parallel Design Variants

## Overview

Generate **N genuinely different** design directions at once, each built by its own subagent locked to a **distinct visual reference**, collect them in one gallery, pick winners, then run a **second round that mixes the winning styles**.

**Core principle: divergence comes from reference anchors, not from asking "be creative."** Ten subagents told "make a nice hero" produce ten similar heroes. Ten subagents anchored to terminal / broadsheet / brutalist / swiss / zine produce ten different worlds. Same content, different reference → real choice.

## When to Use

- You'd otherwise build one design and iterate — but you don't yet know the direction.
- Redesign, landing, hero, thumbnail layout, email, slide system, any visual surface.
- Live/stream or team bake-off where people vote on options.

**Not for:** a single known direction (just build it), or pixel-level refinement of one chosen design (that's normal iteration).

## The Loop

```text
ask how many variants (N)
  → spec issue (constant content + N reference anchors + briefs)
  → N subagents in parallel (blind to each other)
  → gallery index.html (side by side)
  → pick winners (optionally by vote)
  → second round: mix winning styles
```

## Workflow

1. **Ask how many variants (N) — first, before anything else.** Don't silently pick a number; ask the user. Suggest **6–10** as the sweet spot (enough for real divergence, few enough to review side by side) and offer the default, but the count is theirs. Their answer is N for the rest of the flow.
2. **Write ONE spec issue** — it is the orchestration doc, not a throwaway prompt. It contains:
   - **Constant content**: the real data and the required sections every variant must render (identical across all). You compare *style*, never completeness.
   - **Result layout**: `redesign/index.html` (gallery) + `redesign/{slug}/index.html` per direction. Self-contained HTML — inline CSS, vanilla JS, Google Fonts ok, **no build step, no framework** (so the gallery just opens).
   - **A table of N directions**: `slug · name · reference / media-analog`.
   - **A shared prompt scaffold** (identity, required sections, real data, output files) — every subagent gets the same scaffold + its own brief.
   - **Per-direction briefs**: 2–4 sentences each, naming the reference and its concrete cues (fonts, palette, layout move).
3. **Pick N divergent anchors** (the N the user chose). Each anchor a recognizable, *different* reference — adjacent styles waste a variant. Starter palette:

   | slug | reference | slug | reference |
   |------|-----------|------|-----------|
   | `terminal` | TUI dashboard (btop, lazygit) | `swiss` | Int'l Typographic grid |
   | `broadsheet` | newspaper (NYT) | `teletext` | Ceefax / VT323 |
   | `neon-wire` | tech tabloid (The Verge) | `ticker` | Bloomberg terminal |
   | `brutalist` | raw web brutalism | `zine` | photocopy punk zine |
   | `magazine` | print Wired spread | `wire-feed` | Hacker News / teletype |

4. **Dispatch N subagents in parallel** (one message, N tool calls), each: shared scaffold + its brief. Blind to each other — that independence is what produces divergence. Use `sonnet` for design-build subagents.
5. **Build the gallery** `redesign/index.html` linking + previewing all N. Review side by side: `python3 -m http.server` → `/redesign/`.
6. **Pick winners (1–3).** For live/team: the gallery carries a real-time vote (emoji / poll) so the audience picks — the engagement payoff of doing it in public.
7. **Second round — mix winners.** Combine the strongest elements of the top styles into 1–2 refined variants (e.g. swiss grid + zine accents). **Converge by remixing, not by restarting** and not by polishing only one.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Picking N yourself without asking | Ask the user how many variants first; suggest 6–10, but the count is theirs. |
| 2–3 variants in adjacent styles | ≥6, each a distinct *named* reference. No real choice otherwise. |
| Building variants serially yourself | Parallel subagents, blind to each other — speed + true divergence. |
| Different content per variant | Lock the data and required sections; vary only the visual system. |
| "Refine the one I liked" as the whole ending | Second round *mixes* winning elements — runners-up have good ideas too. |
| Frameworks / build steps | Self-contained HTML so the gallery opens with no toolchain. |
| Prompts thrown away in chat | One spec issue = scaffold + briefs → reproducible and reviewable. |

## Real-World Impact

Proven live on the **sereja.tech redesign** (YouTube stream "Claude Fable 5, day 2"): a single spec issue → **10 directions, 10 subagents in parallel** → gallery → **audience voted in chat** → second round mixed the winning styles. One session, ten fully-realized directions, a real decision instead of a guess.
