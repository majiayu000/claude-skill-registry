# deterministic-design

*deterministic-design is a Claude Code skill that renders your UI and proves it's balanced + usable: a deterministic layout audit plus a vision-judged usability score.*

![License: MIT](https://img.shields.io/badge/license-MIT-blue) ![Claude Code skill](https://img.shields.io/badge/Claude%20Code-skill-d97757) ![Numbers, not vibes](https://img.shields.io/badge/numbers-not%20vibes-46d39a) ![Layout audit](https://img.shields.io/badge/layout-audit-111)

**A model can't trust its own eye on layout — so don't. Render the UI and *measure* it: balance is an ink-weighted centroid vs the optical center (a number, not a vibe), an annotated overlay flags low contrast, sub-44px tap targets, spacing and alignment, and a separate fresh-eyes vision judge scores usability against Nielsen's heuristics.**

![deterministic-design: a balance-beam diagram — a light, tall text block (w=46) on the left vs a heavy, compact portrait (w=80) on the right, sitting on a beam that tilts over an optical-center fulcrum, with left/right moment numbers and the net tilt shown below](docs/demo.gif)

*Balance as physics, not taste: each element's visual weight is a moment about the optical center; the layout "tips" toward the heavier side by a measured amount. The audit computes this on a real screenshot — here the portrait (right, heavy) outweighs the text column (left, tall but light), so the net tilts right.*

## 🤔 Why

AI-generated UI often "looks off" — misaligned, centered-mush, a tap target a thumb can't hit — and the model that built it is the worst judge of whether it did, because it's grading its own eye. Default design skills advise on *taste*; none of them **render the output and check it**. deterministic-design adds exactly that missing layer: it measures what's measurable deterministically, and for the genuinely subjective part it brings in a *separate* judge that never saw the design being made.

> **What this is:** a measurement + judgment layer that composes with any design skill (including the default). It doesn't replace taste advice — it proves or disproves it on the rendered artifact.

## ✨ What it does

- ⚖️ **Deterministic balance** — `layout-audit.js` computes the ink-weighted **centroid** and compares it to the **optical center** (and a pixel-oracle check). Balance becomes a number you can fail, not a feeling.
- 🖍️ **Annotated overlay** — draws the findings back onto the screenshot: low **contrast** pairs, **sub-44px** tap targets, **spacing** off the 8-pt grid, **alignment** breaks. The check is legible — you can point at the box that's wrong.
- 📐 **Explicit grid + 8-pt spacing** — the layout is held to a stated grid, so "misaligned" is defined, not eyeballed.
- 👁️ **Separate usability pass** — a **fresh-eyes vision judge** scores the rendered UI against Nielsen's 10 + interaction heuristics → a prioritized fix list. Independent of whatever made the design.
- 🧩 **Composable** — layers on top of any design skill; the audit runs on the final render regardless of how it was produced.

## 🧭 Two sub-skills

| | 📐 design-spatial | 👁️ design-ux |
|---|---|---|
| What it does | deterministic layout audit (centroid / optical-center / pixel-oracle balance) + annotated screenshot + a render-then-critique vision loop | usability audit vs Nielsen's heuristics by a separate fresh-eyes judge |
| Output | numbers + an annotated overlay | a prioritized fix list |
| Trust model | math you can re-run | an independent judge, not the design's author |

## 📦 Install (Claude Code plugin)

```
/plugin marketplace add connerkward/ckw-skills
/plugin install deterministic-design@connerkward
```

Standalone (this repo only):

```
/plugin marketplace add connerkward/deterministic-design-skill
/plugin install deterministic-design@deterministic-design
```

Or drop this repo's `SKILL.md` into your agent's skills directory.

## 🗂️ Part of [ckw-skills](https://github.com/connerkward/ckw-skills)

One of two flagship narratives — the **determinism** one (measure the output). Its siblings trust an eye instead: [`lookdev`](https://github.com/connerkward/lookdev-studio-skill) puts a **human** in the loop, [`lookdev-auto`](https://github.com/connerkward/lookdev-auto-skill) puts a **vision model** in the loop.

## License

MIT © Conner K Ward

---

🧭 **[ckw-skills](https://github.com/connerkward/ckw-skills)** — part of Conner K. Ward's collection of Claude Code skills & MCP servers.
