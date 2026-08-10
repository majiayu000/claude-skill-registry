---
name: qa-persona-testing
description: "Tests apps as an Ideal Customer Profile persona via Playwright/Chrome browser automation and reports friction, fixes, and risks. Use for persona-based, ICP, or synthetic-user testing."
compatibility: Portable core. Works on Claude Code and Codex; browser execution requires a Playwright MCP or Chrome DevTools MCP toolset (or a Playwright script fallback).
version: "1.1"
last_validated: 2026-08-01
---

# QA Persona Testing

Test a solution or app **as a specific person from a specific group** — an Ideal Customer Profile (ICP) or defined user segment — rather than as a QA engineer. The skill covers the full loop: find the profile (using sibling skills), set the persona up as an executable specification, drive the app through browser automation like that person would, and produce an improvement report with what to fix, what to avoid, and what to keep.

This is **persona simulation, not E2E test authoring**. It finds friction, confusion, trust breaks, and abandonment; it does not replace assertion-based regression tests (`qa-testing-playwright`) or research with real users (`software-ux-research`).

## Quick Reference

| Task | Read or use | Outcome |
|------|-------------|---------|
| Find/derive the ICP or persona group | `## Phase 1 — DEFINE` + sibling skills table | Evidence-backed persona candidates |
| Turn a persona into an executable spec | [assets/persona-profile.md](assets/persona-profile.md) + [references/persona-construction.md](references/persona-construction.md) | Persona profile with behavioral traits and scenario pack |
| Run a browser test session as the persona | [references/browser-execution.md](references/browser-execution.md) | Filled [assets/session-log.md](assets/session-log.md) per scenario |
| Keep the simulation honest (anti-sycophancy) | [references/persona-construction.md](references/persona-construction.md#anti-sycophancy) | Persona that abandons, complains, and stays in character |
| Write the improvement report | [assets/findings-report.md](assets/findings-report.md) + [references/reporting-and-validity.md](references/reporting-and-validity.md) | Ranked findings, prioritized fixes, validity caveats |
| Decide what simulation can and cannot claim | [references/reporting-and-validity.md](references/reporting-and-validity.md#validity-limits) | Correctly-hedged conclusions |

## When to Use

- "Test this app like a {{first-time user / busy accountant / 60-year-old iPad user / our ICP}}"
- "Would our target customer actually get through onboarding?"
- "Run a synthetic user / persona-based walkthrough and tell me what to improve"
- Pre-launch UX sanity pass when real-user testing is not yet feasible
- Regression of a redesigned flow against the personas that matter commercially

## When NOT to Use

| Situation | Use instead |
|-----------|-------------|
| Writing assertion-based E2E/regression tests | `qa-testing-playwright` |
| Research with real users (interviews, usability tests, surveys) | `software-ux-research` |
| Heuristic/accessibility audit without persona framing | `software-ui-ux-design`, `qa-testing-accessibility` |
| Validating whether the ICP itself is right for the business | `startup-idea-validation` |
| Testing an LLM agent or bot (agent is the system under test) | `qa-agent-testing` |
| Load, performance, or security testing | `qa-testing-performance`, `qa-security-testing` |

## ASCII Flow

```text
persona-testing request
  -> Phase 1 DEFINE: find ICP / segment (sibling skills + evidence) -> persona candidates
  -> Phase 2 SETUP:  persona profile (traits, budgets, scenario pack, anti-sycophancy contract)
  -> Phase 3 EXECUTE: browser session per scenario as the persona
       +-- Playwright MCP or Chrome DevTools MCP (preferred)
       +-- Playwright script fallback (headless CI)
       -> session log: step trace, think-aloud, friction events, screenshots
  -> Phase 4 REPORT: rank findings by severity x frequency
       -> improvements / avoid-list / keep-list / validity caveats
  -> Hand off: severity>=3 -> qa-testing-playwright regression tests
              preference findings -> software-ux-research real-user validation
```

## Workflow

### Phase 1 — DEFINE the profile

Goal: an evidence-backed persona, not an invented stereotype.

1. Ask (or infer from context) what decision the test must inform: launch readiness, redesign check, conversion friction, accessibility fit.
2. Source the ICP with the smallest sufficient chain of sibling skills:

| Evidence you need | Skill to invoke |
|---|---|
| Who the ICP is at all (segment, JTBD, willingness to pay) | `startup-idea-validation`, `startup-gtm-strategy` |
| What real users complain about in this category | `startup-review-mining`, `startup-painpoint-scanner` |
| Behavioral data from an existing product (funnels, drop-offs) | `marketing-product-analytics` |
| Persona craft, research method, bias control | `software-ux-research` |
| Product context: roadmap, target users already defined | `product-management`, project-specific skills |

3. Pick 1-3 personas maximum per run. Prefer one primary ICP plus one edge persona (low tech fluency or accessibility needs) — more personas dilute session depth.
4. Record provenance and confidence in the persona profile. An assumed persona is allowed but must be labeled `assumed` and its findings hedged accordingly.

### Phase 2 — SETUP the persona

1. Copy [assets/persona-profile.md](assets/persona-profile.md); fill every field. Behavioral traits (patience, tech fluency, reading style, trust posture, error reaction) are the levers that make the simulation diverge from generic QA — do not leave them at defaults.
2. Write the scenario pack: 3-7 tasks phrased **in the persona's words**, each with an entry point, an observable success criterion, and the persona-specific risk it probes.
3. Adopt the anti-sycophancy contract (in the profile): patience budgets, mandatory abandonment, in-character confusion, no tester knowledge. See [references/persona-construction.md](references/persona-construction.md) for calibration and persona-drift checks.
4. Configure the environment to match the persona: viewport/device emulation, locale, network throttling if the persona is mobile/low-bandwidth.

### Phase 3 — EXECUTE browser sessions

1. One session = one persona x one scenario. Start each session from the persona's real entry point (marketing page, app store link, shared URL) — not from a deep link the persona would never have.
2. Drive the app with browser tooling per [references/browser-execution.md](references/browser-execution.md):
   - **Playwright MCP** (`browser_navigate`, `browser_snapshot`, `browser_find`, `browser_click`, ...) — default.
   - **Chrome DevTools MCP** — when you also need console/network/performance evidence, device/network emulation, or isolated browser contexts per scenario.
   - **Playwright script** — fallback for CI or when no MCP browser is available.
3. At every step, log the dual-channel trace into [assets/session-log.md](assets/session-log.md): in-character think-aloud + out-of-character observation + evidence (screenshot, console error, latency).
4. Enforce the persona: act only on what is visible in the snapshot, respect patience budgets, abandon when the persona would. An agent that always completes every task is a broken simulation.
5. Capture friction events with Nielsen severity 0-4 as they happen.

### Phase 4 — REPORT and improve

1. Aggregate session logs into [assets/findings-report.md](assets/findings-report.md): rank by severity, then by how many personas hit the issue.
2. Every finding must cite a logged step and, where possible, a persona quote and evidence artifact. No finding without a trace.
3. Separate three lists: **improve** (prioritized fixes with expected effect), **avoid** (changes that would hurt this ICP), **keep** (flows that passed — protect with regression tests).
4. Apply the validity rules in [references/reporting-and-validity.md](references/reporting-and-validity.md): mechanical failures (broken flows, errors, dead ends) are real findings; emotional/preference findings are hypotheses for real-user validation.
5. Hand off follow-ups: severity ≥3 → `qa-testing-playwright` regression tests; top preference hypotheses → `software-ux-research`; ICP doubts surfaced by testing → `startup-idea-validation`.

## Known Traps

- **Sycophantic persona**: the LLM completes every task and praises the app. Counter: patience budgets, mandatory abandonment rules, and severity quotas are in the profile contract — enforce them.
- **Persona drift**: after ~10-15 steps the agent slides back into QA-engineer voice. Counter: re-read the profile at each scenario start; keep the dual-channel log, and flag any step where the persona voice used tester vocabulary.
- **Tester knowledge leak**: persona "finds" a page via URL guessing or dev shortcuts. Counter: navigation only via visible UI from the declared entry point.
- **Over-claiming**: presenting simulated emotions as user research. Counter: the report's Validity section is mandatory, and preference findings are labeled hypotheses.
- **Persona flattening / stereotyping**: demographic caricature instead of behavioral spec. Counter: traits must map to observable behaviors (see profile trait table), and provenance must name evidence.
- **The fidelity trap**: flawless persona adherence reads as success but correlates with caricature — models with the highest persona fidelity produce the most stereotyped populations (arXiv:2604.24698). Counter: check sessions for stereotyped behavior as well as drift; discount findings that reduce to "this demographic behaved as expected". See [references/persona-construction.md](references/persona-construction.md#the-fidelity-trap).
- **One giant session**: testing all scenarios in one browser context bleeds state (auth, carts, cookies) between scenarios. Counter: fresh context per session.

## Navigation

Resources:

- [references/persona-construction.md](references/persona-construction.md) — ICP-to-persona conversion, behavioral trait calibration, anti-sycophancy contract, drift checks
- [references/browser-execution.md](references/browser-execution.md) — Playwright MCP / Chrome DevTools MCP / script execution patterns, evidence capture, environment emulation
- [references/reporting-and-validity.md](references/reporting-and-validity.md) — severity model, ranking, report assembly, what simulation can and cannot claim
- [data/sources.json](data/sources.json) — primary sources (research + tooling docs) with verification dates

Assets:

- [assets/persona-profile.md](assets/persona-profile.md) — executable persona specification template
- [assets/session-log.md](assets/session-log.md) — dual-channel (in/out of character) session trace template
- [assets/findings-report.md](assets/findings-report.md) — final report template (improve / avoid / keep / validity)

Related skills:

- [../qa-testing-playwright/SKILL.md](../qa-testing-playwright/SKILL.md) — converts findings into durable E2E regression tests
- [../software-ux-research/SKILL.md](../software-ux-research/SKILL.md) — real-user validation of simulated findings; persona research methods
- [../software-ui-ux-design/SKILL.md](../software-ui-ux-design/SKILL.md) — heuristic/WCAG framing for design-level fixes
- `startup-idea-validation` — ICP discovery and validation upstream of testing
- `startup-review-mining` — real-user pain evidence to ground persona traits
- [../qa-agent-testing/SKILL.md](../qa-agent-testing/SKILL.md) — when the system under test is itself an agent
- [../qa-testing-accessibility/SKILL.md](../qa-testing-accessibility/SKILL.md) — deep accessibility audit beyond persona-level signals

## Fact-Checking

- Browser tooling behavior (Playwright MCP tool names, Chrome DevTools MCP capabilities, emulation flags) drifts fast — verify against current official docs before prescribing exact tool calls.
- Research claims about synthetic-user validity (what LLM personas do and do not reproduce) must cite the specific study; do not generalize a single benchmark result.
- Known bugs, framework footguns, and version-specific workarounds must be verified against current primary sources before being treated as current fact.
- Never present simulated persona reactions as evidence from real users.

## Learnings Loop

Before applying this skill on a non-trivial task, read `learnings.consolidated.md` in this directory (and `learnings.md` if present).

After applying it, if you encountered a pattern worth remembering, a mistake worth preventing, or a domain fact that surprised you, append one dated bullet to `learnings.md` via `agents-skills-feedback-loop/scripts/append_learning.py`. Do not modify `SKILL.md` itself.
