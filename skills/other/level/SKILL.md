---
name: level
version: '1.0'
last_updated: 2026-06-04
author: genesys-growth
description: Score your Claude Code environment on a fun 0-10 ladder (Tourist → Swarm) calibrated to the quickstart's 4 systems — Context, Skills, Integrations, Orchestration. Two front doors - an interactive quiz (zero setup, shareable) or a silent scan of your repo. Outputs a next-level roadmap plus a branded HTML dashboard or a paste-anywhere ASCII card. The default mastery skill of this quickstart. Triggers - "level", "what's my claude code level", "claude code level quiz", "assess my setup", "how good is my setup", "claude code maturity"
goal: Score a Claude Code setup 0-10 (with a per-pillar breakdown) and hand back a focused next-level roadmap + a shareable card.
outcome: A scored assessment (quiz or scan) + 4-pillar sub-scores + single-next-level roadmap + a re-runnable, shareable output (HTML dashboard or ASCII card). Level 10 is anchored to a documented ceiling, so the score is honest.
---

# level — the 10 levels of Claude Code

Most people using Claude Code have no idea how much of it they're actually using. This skill scores you 0-10 on a ladder calibrated to the **4 systems** this quickstart teaches — Context · Skills · Integrations · Orchestration — benchmarked against a fully-built setup + the latest Anthropic features, then hands you a focused roadmap and a shareable card.

It's the quickstart's **mastery skill**: the 8 research skills build your marketing OS; `/level` tells you how far along the Claude Code curve you are and what to build next. Level 0 is "just installed it." Level 10 is genuinely rare — the documented ceiling in [`references/benchmark.md`](references/benchmark.md).

```
Pick a front door → Score it → Show the roadmap → Render output → Build first step
       ↓                ↓             ↓               ↓               ↓
   quiz or scan    0-10 + 4 pillars  next level only  html / ascii    optional
```

Re-run it whenever you want — the score updates as you level up.

---

## Modes and flags

| Flag | Effect |
|------|--------|
| `--mode beginner` (default) | "Knowledgeable friend" voice — explain *why* each thing matters, define jargon. Default front door = **quiz**. |
| `--mode internal` | Terser, for auditing your own / your team's setup. Default front door = **scan**. |
| `--brand-kit <path>` | Brand the HTML dashboard from a brand kit (a DESIGN.md with token frontmatter). Default = your `marketing/brand/brand-kit.md` once populated, else plain dark. `--brand-kit none` forces plain dark. |
| `--format html` (default) `\| ascii \| both` | Output shape. `html` = branded dashboard. `ascii` = paste-anywhere card (Slack / LinkedIn / a code block). `both` = each. |
| `--quiz` / `--assess` | Force the quiz, or the silent scan (then stop after the assessment). |
| `--build` | Skip assessment; jump to building the next step. |

No flag → `--mode beginner`, and offer both front doors ("Want the quick **quiz**, or should I **scan** your repo?").

---

## Phase 1 — pick a front door, then score

Both doors converge on the same result: a level (0-10) + a 0-4 sub-score per pillar. [`references/levels.md`](references/levels.md) is the source of truth — the ladder, the 4-pillar mapping, the scan checklist, and the scoring rule.

### Quiz (default in beginner mode)

Read [`references/quiz.md`](references/quiz.md). Ask the ~8 questions in **one** `AskUserQuestion` call (clean clickable options — fun and fast). Map each answer to its pillar + level band, then reconcile to a level + 4 pillar sub-scores per the rule in `quiz.md`. Needs nothing on disk, so it works before you've built anything — and the result is screenshot-shareable.

### Scan (default in internal mode)

Silently inspect the repo using the scan checklist in `levels.md` — CLAUDE.md, `.claude/skills`, `.mcp.json` + plugins, memory / rules, hooks + agents, headless / browser signals, worktrees, scheduled tasks. Then ask the 3 context questions (what you use Claude for / biggest friction / one thing you'd automate). Determine the level. **Quantity ≠ level** — 50 trivial skills is still Level 3; integration + complexity move the rungs.

### Present the assessment

Anchor the ceiling with [`references/benchmark.md`](references/benchmark.md). Present, in the mode's voice: the level + its fun name + vibe; the dual lens (which pillars are strong, which is the gap); a bottom-to-top walk of the rungs cleared, then the first rung that stops you and **why it matters** (plain language). Most marketers land 1-4; 5 is strong; 7+ is rare. If `--assess`, stop here.

---

## Phase 2 — the roadmap (next level only)

Show ONLY the next-level transition — focus is everything. Read the matching section in [`references/roadmaps.md`](references/roadmaps.md) for the assessed level and present its 3-4 steps with time estimates.

---

## Generate the output

Always produce output after Phase 1 (+ Phase 2 unless `--assess`). Pick the shape from `--format` (default `html`). For sharing, offer the ASCII card.

### HTML dashboard (`--format html`, default — or `both`)

1. Read [`references/dashboard-template.html`](references/dashboard-template.html).
2. **Resolve the brand:** `--brand-kit <path>` if given; else your `marketing/brand/brand-kit.md` (once populated); else `--brand-kit none` / the template's dark defaults.
3. **Map brand-kit tokens → dashboard tokens** per the template's comment: `colors.accent`→`{{ACCENT}}` (primary), `colors.tertiary`/`success`→`{{DONE}}`, `colors.background`/`surface`→`{{BG}}`/`{{SURFACE}}`, `colors.on-background*`→text tokens, `typography.*.fontFamily`→`{{FONT}}` (+ its web `<link>` as `{{FONT_LINK}}`), `name`/domain→`{{BRAND_NAME}}`/`{{BRAND_URL}}`. Use the kit's exact hex — never approximate.
4. Replace every `{{TOKEN}}` with real assessment data — per-pillar bars + the shareable result card.
5. Write to `~/Desktop/claude-code-level.html`, open it (`open` macOS / `xdg-open` Linux / `start` Windows), tell the user the path + the brand applied.

### ASCII card (`--format ascii` — or `both`)

A fixed-width, paste-anywhere card. Build a JSON payload and pipe it to the generator (it asserts every line is identical width, so the box never misaligns):

```bash
echo '{"level":N,"name":"<level name>","vibe":"<vibe>",
"pillars":{"Context":c,"Skills":s,"Integrations":i,"Orchestration":o},
"takeaway":["short line 1 (≤48 chars)","line 2"],
"brand_name":"<your brand>","brand_url":"<your domain>"}' \
  | python3 references/ascii-card.py
```

It prints the card and saves `~/Desktop/claude-code-level.txt`. Also **paste the card inline in a fenced code block** so the user can copy it from chat. `brand_name`/`brand_url` come from your brand kit's `name` + domain.

---

## Phase 3 — build it now (optional)

Ask: "Want me to build the first step of your roadmap right now?" If yes, execute the matching step in [`references/build-steps.md`](references/build-steps.md). Adapt to the person — don't paste templates verbatim. If they score 0-2, point them at the quickstart's 15-minute tour and the 8 research skills to build context fast.

---

## Self-roast (run before delivering)

- Is the level honest, or inflated? Quantity ≠ maturity — did I check integration + complexity?
- Did I anchor Level 10 to `benchmark.md`?
- Beginner mode: did I explain *why* each gap matters and define jargon?
- Did I show only the NEXT level's roadmap, not all 10?
- Did the output actually render (dashboard opened, or ASCII card pasted inline)?
