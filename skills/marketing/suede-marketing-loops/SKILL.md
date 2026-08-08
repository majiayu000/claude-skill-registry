---
name: suede-marketing-loops
description: "Suede-affiliated recurring marketing workflow design for cadence, inputs, decision rules, checkpoints, failure states, and measurable outputs. Use when the user wants repeatable ad-fatigue, content-refresh, churn-watch, ranking-drop, or weekly-review loops. NOT FOR: one-off tactic ideation (use suede-marketing-ideas), experiment design (use suede-ab-testing), or creating a live automation without explicit scheduling authority."
metadata:
  version: 1.2.0
---

# Suede Marketing Loops

Suede turns repeatable marketing work into bounded loops with a defined trigger, cadence, input contract, self-check, durable state, human checkpoint, and stopping condition. A loop may watch SEO opportunities, ad fatigue, or churn signals, but it never earns permission to publish, spend, or mutate production merely because it runs on a schedule.

This is the operational counterpart to `suede-marketing-ideas`: ideas identify what may be worth trying once; Suede loops define what approved work should repeat and how public Suede skills coordinate it.

## How to Use This Skill

**Check for product marketing context first:** if `.agents/product-marketing.md` exists (or `.claude/product-marketing.md`, or the legacy `product-marketing-context.md`), read it before asking questions. Use that context and only ask for what's missing.

Then:
1. **Clarify the job.** What outcome should this loop protect or grow? (rankings, ad efficiency, activation, retention, revenue, referrals)
2. **Pick a loop** from the catalog in `references/loop-catalog.md` — or adapt the closest one.
3. **Tune the cadence** to how fast the underlying signal actually changes (see the cadence rule below).
4. **Confirm the human checkpoint.** Decide what the loop does autonomously vs. what it stages for human approval before publishing or spending — see `references/loop-guardrails.md`.
5. **Schedule it** (see "Scheduling a loop" below).

Building more than one loop, or a whole marketing operating system? See `references/loop-orchestration.md` for how loops compose and the order to adopt them (start with tracking + a weekly review; don't build 45 at once).

## Anatomy of a Marketing Loop

Every loop in the catalog has these nine parts. When you author or adapt one, fill all of them — a loop missing a stop condition, a self-check, or its state handling is a liability, not an asset.

| Part | What it defines |
|------|-----------------|
| **Check cadence** | How often the loop *looks* (weekly / daily / on-trigger). Match it to signal speed. |
| **Acts when** | The action condition — what must be true to actually *do* something, vs. just check and skip. Most runs of a good loop are "checked, nothing to do." |
| **Purpose** | The one outcome this loop exists to move. |
| **Skills used** | Which marketing skills the loop orchestrates each iteration. |
| **Loop body** | The ordered steps run each iteration. |
| **Self-check** | The verification done *before* acting — so the loop doesn't act on noise, seasonality, or a tracking bug. |
| **State / idempotency** | What the loop remembers between runs: last-run marker, dedupe key, cooldown window, "already handled" set. Without this, loops double-act, re-nag the same people, or re-alert the same thing. Non-negotiable for anything scheduled — see `references/loop-state.md` for where state lives and the idempotency patterns. |
| **Stop / bail-out** | When the loop skips, halts, escalates to a human, or disables itself — plus what it does on error. Every loop needs one, including heartbeat loops (their stop is "manual disable + error-halt," never "n/a"). |
| **Output** | Where results go: a file, a PR, a staged draft, a notification, a report. |

The **Check cadence / Acts when** split matters: a churn-signal loop might *check* daily but only *act* when an account crosses a risk threshold it hasn't been contacted about inside the cooldown window. Conflating the two produces loops that either miss the window or spam.

## The cadence rule

Match cadence to how fast the signal actually changes — not to how often you'd *like* an update.

| Signal | Realistic cadence | Why |
|--------|-------------------|-----|
| Rankings, backlinks, domain authority | Weekly | Move slowly; daily checks are noise |
| Ad creative fatigue, CPA drift | Every 2–3 days | Meta/Google feedback loops are days, not hours |
| Activation / onboarding funnel | Weekly | Needs enough signups to be significant |
| Churn signals | Daily or on-trigger | Early intervention window is short |
| Content / copy decay | Monthly | Traffic erosion is gradual |
| Competitor changes | Weekly | Pricing/positioning shifts are infrequent but matter |
| Social listening / mentions | Daily | Engagement windows close fast |

Over-frequent loops are the most common failure mode: they generate busywork, burn budget, and train you to ignore the output.

## When NOT to loop

Not everything should be automated on a cadence. Skip a loop — or add a mandatory human checkpoint — when:

- **Strategy or creative direction is the real work.** Loops maintain and optimize; they don't set positioning, invent campaigns, or make brand calls.
- **The action publishes or spends without review.** Auto-*drafting* an ad, email, or post is fine. Auto-*publishing* or auto-*shifting budget* needs a human checkpoint unless the user has explicitly authorized autonomous action and set guardrails (caps, allowlists).
- **The signal is too sparse to be significant.** A weekly conversion-rate loop on 40 visitors/week is measuring noise.
- **It's a vanity loop.** If nobody acts on the output, delete the loop. A loop that emails a dashboard nobody reads is worse than nothing.

For any loop that sends, spends, publishes, or touches personal data, apply `references/loop-guardrails.md` — the two-tier action model (autonomous-safe vs. gated), spend/send caps, CAN-SPAM/GDPR/FTC/ToS rules, the always-escalate list, and a required kill switch.

## Scheduling a loop

These loops are agent-agnostic — the *body* works in any agent. The *scheduling* depends on your environment:

- **Scheduling-capable environment** — discover the installed scheduler, automation connector, or native scheduling primitives first and read their current instructions. Use them only when they are actually available and the user authorizes scheduling.
- **Cron-capable host** — when cron is available, wrap the loop body as a scheduled prompt or script (`0 9 * * 1` for Mondays at 9am, for example).
- **Manual cadence** — for high-judgment loops, "run this skill every Monday" is a perfectly good loop. The value is the repeatable *body*, not the automation.

If no scheduling mechanism is available, return the complete loop body plus a copyable cadence instruction and mark scheduling as not created.

Default to time-of-day cron for review-style loops (weekly review, ranking watch) and dynamic pacing for monitor-until-threshold loops (churn watch, launch-day tracking).

## The Catalog

`references/loop-catalog.md` holds the full library — 45 marketing loops with thorough funnel coverage: SEO & Content, Paid, Earned/Social/Partnerships, Activation, Retention, Revenue, Referral & Advocacy, and Ongoing Ops. Each is a complete, adaptable spec. Start there, pick the closest match, and tune it to the user's product, stage, and tooling.

## Authoring a new loop

When nothing in the catalog fits, author a new loop from `references/loop-template.md` — a copy-paste template with fill-in prompts, a worked before/after example, and a ship checklist. Fill all nine anatomy parts; if you can't answer the self-check, state/idempotency, and stop/bail-out concretely, the loop isn't ready to run.

## Anti-patterns

- Looping without a stop condition → runaway spend or infinite churn.
- Same cadence for every loop → most run too often and get ignored.
- No self-check → the loop acts on noise, seasonality, or a tracking bug.
- No human checkpoint on spend/publish actions.
- Building 10 loops at once → start with one, prove it earns its keep, then add the next.

## Banned vocabulary

Avoid: "set it and forget it," "fully autonomous marketing," "AI does everything," "10x on autopilot," "growth hacking machine." Loops are disciplined systems with checkpoints, not magic. Describe them honestly.

## Boundaries

- Do not create, enable, schedule, or modify a recurring automation without explicit authorization.
- Do not let a loop publish, spend, message, delete, or change production state without a named human checkpoint.
- Do not claim a loop ran, detected a condition, or improved a metric without a current execution record.
- Do not hide missing data, permissions, thresholds, owners, or stop conditions behind "autonomous" language, and do not decide those controls for the user.

## Routing

- Use `suede-marketing-ideas` for one-off tactics and `suede-ab-testing` for experimentation.
- Use `suede-analytics` for measurement inputs.
- Route channel actions to `suede-ads`, `suede-seo-audit`, `suede-emails`, `suede-social`, `suede-churn-prevention`, `suede-pricing`, or `suede-referrals`.
