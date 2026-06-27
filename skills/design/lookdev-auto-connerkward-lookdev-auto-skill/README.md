# lookdev-auto

*lookdev-auto is a Claude Code skill for automated visual tuning: a vision model rates rendered variants and suggests better values in a loop.*

![License: MIT](https://img.shields.io/badge/license-MIT-blue) ![Claude Code skill](https://img.shields.io/badge/Claude%20Code-skill-d97757) ![Judge: vision model](https://img.shields.io/badge/judge-vision%20model-46d39a) ![Loop](https://img.shields.io/badge/optimize-loop-111)

**When "looks/feels right" is the only metric, make a vision/video model the judge: render a few labeled variants into ONE contact sheet — params burned onto each — ask the model to rate them and suggest better values as JSON, render the suggestions, pick the best, repeat. Usually ~2 rounds.**

![lookdev-auto: a 6-cell contact sheet of color-grade variants A–F, each a sky/mountain render with its params burned in (warm offset, gamma) and a score pill; cell D is marked BEST · APPLY, and the model's per-variant ratings + suggested next values appear as JSON at the top](docs/contact-sheet.png)

*One round of a color-grade tune. Six variants → **one** upload → **one** inference: the judge scores each cell (the labels are burned on, so it sees param + result together) and returns `{"ratings":…,"best_so_far":"D","suggest":[[warm,γ]…]}`. Render the suggestions next round, ask it to pick the single best. (Scores here are an illustrative round, not a live API call.)*

## 🤔 Why

Claude Code is text-first, so for anything where success is "does this **look** or **feel** right" — easing, zoom feel, a color grade, spacing — it tends to guess a number and ask you to react in prose. Slow and lossy. When a real numeric metric exists, optimize that. When one doesn't, a vision model (for spatial looks) or a video-understanding model (for motion/timing) can stand in as the eye, *inside a tight loop*, so you stop hand-tuning by trial and error.

> **What this is:** not a new technique — it structures an ability Claude already has (look at the output, iterate) into a disciplined, repeatable harness. The model is the eye; you do the rendering and run the loop.

## ✨ What it does

- 🖼️ **One artifact per round, not one call per variant** — montage N variants into a single contact sheet (images) or a labeled sequence (video/motion). A 6-variant round is **1 upload + 1 inference**, not 6.
- 🏷️ **Params burned onto the artifact** — each cell carries its own label (`A · warm −10 · γ1.2`), so the judge sees label + result together; no separate "variant A used X" context to carry, fewer tokens, fewer mistakes.
- 📊 **Structured JSON out** — the model returns per-variant ratings + concrete suggested next values (`{"ratings":{…},"best_so_far":"X","suggest":[[p1,p2]…]}`); parse it, no free-text wrangling.
- 🎯 **Coarse → fine** — round 1 is a wide, sparse spread to locate the region; round 2 renders the model's suggestions (plus the carried best) and asks it to pick the single best. Converges in ~2 rounds.
- ⚓ **Calibration anchors** — include one deliberately-bad and one safe-default variant each round, so the judge has a reference scale and a bad recommendation is caught (its "best" worse than the safe default = stop).
- 🧪 **Independent rubric, stated up front** — define "good" / "too much" / "too little" concretely instead of "which do you like", so the judge stays independent of your framing.
- ⏭️ **Early-exit** — if round-1 top rates ≥9/10 and the suggestions cluster, skip round 2 and apply the winner.

## 🧭 When to use it (and when not)

| Use it when | Don't — instead |
|---|---|
| "Looks/feels right" is the bar and there's **no cheap numeric metric** | A real metric correlates with quality → optimize that directly |
| The judgment generalizes (smooth easing, clean grade, balanced layout) | The judgment is **the user's** taste/brand → show them the variants, let *them* pick |
| ~3–6 variants worth comparing | One or two variants → just look yourself |

⚠️ The model's pick is an *opinion*, not ground truth — anchor it and sanity-check the winner against the safe default before committing. Vision/video models see gross differences well and fine ones poorly, so keep variant spacing perceptible.

## 📦 Install (Claude Code plugin)

```
/plugin marketplace add connerkward/ckw-skills
/plugin install lookdev-auto@connerkward
```

Standalone (this repo only):

```
/plugin marketplace add connerkward/lookdev-auto-skill
/plugin install lookdev-auto@lookdev-auto
```

Or drop this repo's `SKILL.md` into your agent's skills directory.

## 🗂️ Part of [ckw-skills](https://github.com/connerkward/ckw-skills)

The automated-eye sibling of [`lookdev`](https://github.com/connerkward/lookdev-studio-skill) (a **human** dials it in by eye) and [`deterministic-design`](https://github.com/connerkward/deterministic-design-skill) (**measure** the UI instead of trusting any eye). Here a **vision model** is the eye.

## License

MIT © Conner K Ward

---

🧭 **[ckw-skills](https://github.com/connerkward/ckw-skills)** — part of Conner K. Ward's collection of Claude Code skills & MCP servers.
