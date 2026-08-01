---
name: kai-gate
description: Run Kai CMO Harness quality gates on content. Scores Four U's (Unique/Useful/Ultra-specific/Urgent), checks for banned words and AI slop, runs SEO lint for search content. Use when "score this", "quality check", "run quality gates", "check this content", "four u's score", "banned word check", "SEO lint", or any request to validate content quality before publishing.
---

> **Kai root note:** `knowledge/`, `harness/`, and `scripts/` paths in this skill live in the Kai install, not the user's project. Resolve them against the first ancestor directory of this SKILL.md that contains a `knowledge/` folder (the Kai plugin root, `~/.claude/kai`, or the kai-cmo-harness repo). `MARKETING.md`, `memory/`, and any output files live in the current project. If a referenced `scripts/` command is not available in this install, say so, skip it, and continue with the file-based guidance — never fabricate its output.

## Objective

A verdict on a piece of content that the writer cannot argue with: a per-dimension Four U's score against the right threshold, every banned word and slop phrase located by line, every voice-pattern regex run, and SEO lint applied when the content targets search. The verdict is PASS or FAIL with the specific failing rule named — never a vague quality impression.

## Done when

Work type `internal-research` — floor **E2/C2/O0** (`harness/eco-floors.yaml`). The gate report is an internal artifact; nothing leaves the workspace, and SHIPPED is terminal.

- **E2** — the gate report exists and carries every section below: Four U's total plus each dimension with its reason, banned words, AI slop, voice patterns, SEO lint (or SKIPPED), and an overall verdict.
- **C2** — every declared check ran at its stated threshold. A skipped check is reported as SKIPPED with the reason, never silently omitted. **O0** — no outcome obligation.

This skill grades other people's work. It does not issue a completion verdict on its own gate report, and a gate PASS is Craft evidence only — it is not Execution or Outcome for the piece being gated. Promoting a recurring failure into a new lint rule or banned-word tier is a separate `harness-change` item (floor **E3/C3/O1**, gates `doctor`, `golden_check`, `pytest`) and requires a golden corpus case proving the new check.

## Constraints

All four checks run on every piece, each reported separately.

**Four U's.** Score each dimension 1-4. Thresholds: **12/16** for blog/SEO/articles, **10/16** for email/ads.

| U | Question | Score |
|---|----------|-------|
| **Unique** | Can only WE write this? Original data, perspective, or experience? | 1-4 |
| **Useful** | Can the reader take action immediately? | 1-4 |
| **Ultra-specific** | Numbers, named tools, concrete examples? | 1-4 |
| **Urgent** | Is there a reason to engage today? | 1-4 |

**Banned words — instant reject (Tier 1):** leverage, utilize, synergy, innovative, deep dive, circle back, touch base, moving forward, at the end of the day

**AI slop (also reject):** "In conclusion", "It's important to note", "In today's rapidly evolving", "This comprehensive guide", "Without further ado", "It's worth noting that"

Flag exact locations of every violation.

**Voice patterns (programmatic — DO NOT skip).** Binary clichés ("X-not-Y" / "It's not X, it's Y" / "isn't X — it's Y") read as LinkedIn slop and slip past subjective scoring. Run these regexes against the file with the Grep tool. Any match = FAIL.

| Pattern | Catches |
|---|---|
| `, not [a-z]` | "X, not Y" |
| `— not [a-z]` | "X — not Y" |
| `\bisn'?t [a-z][^.\n]+ — it'?s\b` | "isn't X — it's Y" |
| `\baren'?t [a-z][^.\n]+ — they'?re\b` | "aren't X — they're Y" |
| `\bIt'?s (a\|the\|an) [^.\n]+, not (a\|the\|an)\b` | "It's a/the X, not a/the Y" |
| `\bThat'?s (a\|the\|an) [^.\n]+, not (a\|the\|an)\b` | "That's a/the X, not a/the Y" |
| `\bIf you [a-z][^,.]+, [a-z]` | "If you X, Y" rhetorical |
| `\bHere'?s the thing\b` | LinkedIn slop |
| `\bI'?ll be honest\b` | LinkedIn slop |
| `\bLet that sink in\b` | LinkedIn slop |
| `\bHot take\b` | LinkedIn slop |

Skip matches inside HTML comments (`<!-- ... -->`) and code fences (```` ``` ````) — those are scorecard / metadata blocks.

**Replacements that work:** collapse to a single load-bearing claim; use parallel-positive contrast where both halves are positive (*"Description is passive. State is something the agent can act on."*); use a metaphor (*"expensive webhook"*) rather than symmetrical reversal.

**Project hook integration:** if the project has `.claude/hooks/voice-gate.py`, that hook fires PostToolUse on Edit/Write and catches these patterns at draft time. The gate step still runs the regexes — belt and suspenders.

**SEO lint (search content only).** Apply only if the content targets search engines. Check against Algorithmic Authorship rules: conditions after main clause; instructions start with verbs; sentences under 20 words; bold the answer, not query terms; no links in first sentence of paragraphs.

**Reporting.** Report Four U's as a total out of 16 **plus each dimension with its own score and reason**; report banned words, AI slop, voice patterns, and SEO lint each as PASS / FAIL / SKIPPED with line numbers for every violation. On FAIL, name the specific fixes needed and offer to auto-fix and re-score.

**Panel scoring is advisory and optional** — only when the user asks for a second opinion or the artifact is high-stakes. Roles: audience reviewer (persona fit, plain-language clarity), channel reviewer (platform fit, format, norms), proof reviewer (source locations, attribution, unsupported claims), conversion reviewer (CTA clarity, objection handling), each scored 1-5 with concern and suggested fix. Label panel output as simulated review, never expert validation. Do not create fake credentials, endorsements, or named reviewers. Treat missing source locations as a gate issue, not a panel preference. Run panel scoring on drafts first; publishing still requires approval. Panel output cannot override a hard fail from banned words, source gaps, policy risk, or missing approval.

## Context

| Need | Load |
|---|---|
| Full Algorithmic Authorship rule set for SEO lint | `knowledge/frameworks/content-copywriting/algorithmic-authorship.md` |
| Per-format thresholds and gate minimums | `harness/skill-contracts/` (the contract matching the piece's format) |
| Known loser patterns, and the write triggers for a repeat failure | `memory/what-doesnt-work.md`, `memory/lessons.md`, `memory/MEMORY.md` |

**Learning hook.** Gate script runs log to `data/learning/gate_runs.jsonl` automatically. If the **same diagnosis fails twice on one piece**, append a lesson to `memory/lessons.md` before escalating (write trigger #3 in `memory/MEMORY.md`). Recurring failures across pieces get mined by `/kai-retro` and promoted into new gate checks with golden corpus cases.

## Escalate when

- The same diagnosis fails twice on one piece — log the lesson, then hand the piece to a human with the specific failures listed.
- The content's format is unclear, so the correct Four U's threshold (12/16 vs 10/16) cannot be chosen.
- A violation sits in quoted source material or a client-supplied claim where rewriting changes the meaning.
- A check cannot run in this install — say so, report it SKIPPED, and never assume a pass.
