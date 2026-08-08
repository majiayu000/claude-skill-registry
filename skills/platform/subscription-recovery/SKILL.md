---
name: subscription-recovery
description: "Use when the user wants to find, audit, cancel, or dispute recurring charges billed outside Amazon, including App Store, Google Play, PayPal, direct-bill streaming, gyms, news, and SaaS. Discover charges from evidence the user directly provides or authenticated service pages, report findings first, and require confirmation before cancellation or refund contact. Never enter payment credentials or promise recovery. Requires Claude in Chrome for browser actions. NOT FOR: Amazon returns, restocking fees, or Amazon-billed Prime Video Channels, Audible, Kindle Unlimited, or Prime — use amazon-returns-recovery for those."
---

# Subscription Recovery

## Why this exists

The [amazon-returns-recovery](../amazon-returns-recovery/SKILL.md) skill proved the
underlying idea on Amazon: money doesn't announce itself when it's still being
charged, only when someone goes and checks. Restocking fees and Amazon-billed
subscriptions (Prime Video Channels routes Britbox, Starz, AMC+, and friends through
one Amazon bill) are one slice of that. Most people's actual subscription sprawl is
bigger and more scattered — a streaming service billed directly by its own app, a gym
membership, a SaaS tool from a free trial that converted, a magazine, an App
Store subscription bought once and forgotten. None of that goes through Amazon at
all. This skill is the same negotiation discipline — build the case from real facts,
confirm before acting, hold the line under a counteroffer, get the outcome confirmed
in writing — pointed at *anything* recurring, not just an Amazon account.

Treat this as a metal detector, not an autopilot: it surfaces what's being charged
and drafts the case, but every cancellation and every dispute goes through the
account owner before anything gets sent or clicked.

**Scope split with amazon-returns-recovery**: if a subscription is billed through
Amazon (Prime Video Channels, Audible, Kindle Unlimited, Prime itself), hand off to
that skill instead of duplicating its Phase 1b — it already documents the Amazon-
specific pages and chat flow. This skill covers everything billed *outside* Amazon.

## Prerequisites

- Claude in Chrome browser extension connected, for any service checked or acted on
  in-browser. If `mcp__claude-in-chrome__*` tools aren't loaded yet, fetch them via
  ToolSearch first.
- Unlike amazon-returns-recovery, there is no single account to sweep — discovery
  depends on what the user can provide (a bank/card statement, app access, or just
  naming what they remember paying for) and what platform-level subscription hubs
  are available (App Store, Google Play, PayPal).
- **Unvalidated click-paths.** Only the App Store, Google Play, and PayPal hub pages
  in Phase 1a are close to a fixed, checkable URL. Every individual service's own
  billing/cancellation page (Netflix, Spotify, a gym's member portal, etc.) has to be
  discovered live and should be recorded in
  [references/service-playbook.md](references/service-playbook.md) once confirmed,
  so the next run doesn't rediscover it from scratch.

## Phase 1a — Platform subscription hubs (read-only, no side effects)

These three cover a large share of subscriptions in one page each, because the
platform (not the individual service) is the merchant of record:

1. **Apple App Store** (iOS/iPadOS/Mac subscriptions bought through Apple's
   in-app-purchase flow — many streaming apps route here instead of billing
   directly): `https://apps.apple.com/account/subscriptions` (requires Apple ID
   sign-in) or on-device: Settings → [Apple ID] → Subscriptions.
2. **Google Play**: `https://play.google.com/store/account/subscriptions` — same
   idea for Android-purchased subscriptions.
3. **PayPal recurring payments**: `https://www.paypal.com/myaccount/autopay/` —
   lists every merchant with standing authorization to charge the account, including
   ones that don't show up anywhere else (a common blind spot: an old free trial that
   converted, billed via PayPal, with no reminder email ever opened).

Each of these lists service name, price, billing cadence, and next charge date, and
each has a **direct cancel button on the same page** — no negotiation needed for a
straight cancellation found here.

## Phase 1b — Bank/card statement scan (read-only, no side effects)

If the user can share a recent statement (PDF, CSV export, or even a screenshot of
the transaction list), scan for recurring merchant names and amounts — the same
charge appearing monthly/annually from the same merchant is the signal. This catches
services that bill directly (Netflix, Hulu, Disney+, HBO Max, a gym, a SaaS tool)
and aren't visible through the Phase 1a hubs. Ask for the statement rather than
guessing; don't assume access to financial accounts.

## Phase 1c — Ask directly

Ask the user what else they know they're paying for that Phase 1a/1b didn't surface
— people usually remember 60-70% of their subscriptions when prompted but forget the
rest until specifically asked. This is often faster than a statement scan for a first
pass, and worth doing even after one.

## Phase 1d — Amazon carve-out

If a subscription turns out to be Amazon-billed (Prime Video Channels, Audible,
Kindle Unlimited, Prime itself), don't handle it here — hand off to
[amazon-returns-recovery](../amazon-returns-recovery/SKILL.md)'s Phase 1b, which
already documents those pages.

**Stop here.** Do not cancel or contact anything yet.

## Phase 2 — Confirm with the user

Report every subscription found as a plain list: service, price, billing cadence,
next charge date, and usage signal if known (last opened, last watched, last
attended). Ask which ones to pursue and what outcome they want per service: cancel
only, cancel *and* ask for the last charge back, or dispute a specific charge without
canceling (e.g. billed twice in one month). Some subscriptions may turn out to still
be wanted — don't assume every finding is a mistake, and say so if one looks
intentional.

## Phase 3 — Execute (one service at a time, only after confirmation)

**Straight cancellation, no negotiation needed:**
- If found via Phase 1a (App Store, Google Play, or PayPal), cancel directly on that
  same hub page — fastest path, no chat required.
- Otherwise navigate to the service's own account/billing settings and look for a
  direct cancel option before resorting to chat or a phone call.

**Refund/goodwill ask** (forgot to cancel, charged after a cancellation attempt,
billed twice, or genuinely unused for months):
- Use the same ground rules as amazon-returns-recovery: state only true facts
  (service name, price, charge date, and the real reason), don't invent a prior
  contact attempt or cancellation date that didn't happen, ask plainly for the
  specific outcome wanted, and accept one polite counteroffer round at most before
  reporting back rather than escalating with anything untrue.
- Apple and Google have their own self-service refund-request flows separate from
  the subscription hub itself — Apple: `https://reportaproblem.apple.com`; Google
  Play: order history → "Report a problem" (or `support.google.com` refund request).
  These are usually faster than chat for App Store/Play Store charges and worth
  trying first.
- For direct-bill services, most have either a support chat or a cancellation
  retention flow (which sometimes offers a discount or partial refund unprompted
  when the user tries to cancel) — take the retention offer only if the user
  actually wants to keep the service at the lower price; otherwise decline and
  proceed with cancellation.

**Record the working path.** Once a service's actual cancellation/dispute flow is
confirmed live, add it to
[references/service-playbook.md](references/service-playbook.md) with the exact URL
and click-path, the same way amazon-returns-recovery documents its own chat flow —
this is what turns "unvalidated" into "validated" over time.

## Phase 4 — Report

After each cancellation or dispute resolves, tell the user: what happened (canceled,
refunded, disputed and declined), effective date or refund amount, and method. If
several services were pursued in one session, summarize as a running total — keep
one-time dollars recovered separate from ongoing monthly/annual savings from
cancellations, since they're not the same kind of money.

## Stretch goal — not yet built

**Automated statement parsing**: right now Phase 1b relies on the user sharing a
statement and a manual scan. A more systematic pass (categorizing every recurring
merchant automatically, flagging amount changes over time as a sign of stealth price
increases) would need either a bank-connection integration or a more structured
statement format than "share a screenshot" — out of scope until there's a validated
way to do it without touching credentials directly, which conflicts with this
skill's own safety rules.
