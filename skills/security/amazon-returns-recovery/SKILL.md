---
name: amazon-returns-recovery
description: "Use when the user wants to audit Amazon returns or Amazon-billed subscriptions, mentions a restocking fee, short or denied refund, forgotten Prime Video Channel, Audible, Kindle Unlimited, or Prime charge, or asks whether Amazon still owes or bills them. Read order, refund, and subscription evidence first; report findings and require confirmation before chat, cancellation, or dispute. The documented cases recovered $448.31, but never promise recovery. Requires an authenticated Claude in Chrome session. NOT FOR: bank chargebacks, marketplace A-to-z seller claims, price-protection claims, or subscriptions billed outside Amazon — use subscription-recovery for those."
---

# Amazon Returns Recovery

## Why this exists

This started as a test of a general-purpose contract/customer-service negotiation
tool — the goal was just to see if it could hold its own in a dispute. Pointed at a
live Amazon account, it surfaced two restocking fees ($44.99 and $28.50) the account
owner had no idea existed, on returns processed weeks earlier. Both got waived in the
same sitting — the first refunded exactly the $44.99 fee, the second came back at
$30.63 (the associate rounded up past the $28.50 fee as a goodwill gesture). Total
recovered from fees alone: **$75.62**, on charges the account owner never would have
gone looking for. The lesson: money like this doesn't announce itself — restocking
fees, partial refunds, and price-protection differences sit quietly in order history
unless something goes and checks. That's what this skill automates.

Treat this as a metal detector, not an autopilot: it surfaces what's buried and drafts
the case, but every dispute goes through the account owner before anything gets sent.

The same account also had a third case worth knowing about, even though it's outside
this skill's default restocking-fee scope: a $372.69 electric shaver the account
owner had already been **denied a refund on once — while still inside the return
window**. Re-disputed two days after the window closed, hands-off, the case ended in
a full **$372.69** refund with no return required — the associate just let the account
owner keep it. Overturning an existing denial after the window shut is the ceiling of
what a well-reasoned exception ask can get, not just fee waivers. See
[references/example-cases.md](references/example-cases.md) for the full writeup of
all three real cases, including exactly what was said and what worked.

## Prerequisites

- Claude in Chrome browser extension connected to the browser, and the user already
  signed into the target Amazon account. If `mcp__claude-in-chrome__*` tools aren't
  loaded yet, fetch them via ToolSearch first (see the extension's own MCP
  instructions for the batch-load query).
- This runs against a real account. If the account is shared (family members with
  separate shipping addresses on the same login), be ready to see orders that aren't
  the user's — flag those, don't just fold them into the same batch without asking.

## Phase 1a — Order/return discovery (read-only, no side effects)

Goal: find every completed return where Amazon deducted a restocking fee, without
touching anything.

1. Search order history broadly by category keyword, not just exact terms — Amazon's
   `your-orders/search` matches loosely, so one keyword (e.g. "razor") surfaces
   adjacent items (shavers, trimmers) too. Restocking fees concentrate on
   higher-value electronics/appliances, so prioritize checking those over
   consumables or clothing.
   - `https://www.amazon.com/your-orders/search/ref=ppx_yo2ov_dt_b_search?opt=ab&search=<keyword>`
   - Paginate through all result pages — don't stop at page 1. Older orders (a year+
     back) still show up here even though they've long since dropped off `Your
     Returns`.
2. For faster coverage of *recent* activity, also check
   `https://www.amazon.com/your-returns` — but note it only shows roughly the last
   3 months, so it's a supplement to the search sweep, not a replacement for it.
3. For each order that shows "Return complete" / "Refund Complete" / "Refund issued",
   open its detail page:
   `https://www.amazon.com/your-orders/order-details?orderID=<orderID>`
   Find the **Refund Total** line — it has a small chevron that expands to an
   itemized breakdown (Item(s) refund / Tax refund / Restocking fee / Refund Total).
   Click it. Orders with no fee just show item + tax = refund total; orders with a
   fee show the deduction explicitly.
4. Record every hit: order #, item name, item price, restocking fee amount, who it
   shipped to, and whether it was sold by Amazon.com directly or a third-party
   seller (first-party listings are the strongest cases — Amazon's own chat agents
   can waive those without looping in a marketplace seller).
5. Don't try to make this exhaustive on the first pass if the account has a long
   history — report what's found so far and note that more may be scattered across
   older years if the user wants a deeper sweep.

**Stop here.** Do not open the dispute chat yet.

## Phase 1b — Digital subscription audit (read-only, no side effects)

**Unvalidated click-path** — the exact URLs below are the best-known entry points as
of this writing, not yet confirmed live like the Phase 1a flow. If a URL 404s or
redirects somewhere unexpected, navigate from the account menu instead (Amazon moves
these pages periodically) and note the working path back into this file once
confirmed.

Goal: find every recurring digital subscription billed through the Amazon account —
Prime Video Channels, Audible, Kindle Unlimited, Prime itself — and flag ones that
look forgotten, unused, or worth reconsidering. This is a different shape of "money
Amazon is quietly taking" than restocking fees: it's ongoing, not a one-time
deduction, so the fix is usually "cancel it" rather than "waive it," with a refund
ask reserved for genuinely forgotten charges.

1. **Prime Video Channels** (this is how Britbox, Starz, AMC+, Paramount+, Shudder,
   MGM+, etc. actually bill — they're not separate Amazon relationships, they're
   add-on channels on top of Prime Video):
   `https://www.primevideo.com/settings/channels` — lists every active channel
   subscription, price, and next billing date. If that redirects, go to Prime
   Video → Account & Settings (top right) → Channels.
2. **Audible membership**: `https://www.audible.com/account/membership-overview` —
   same Amazon login, separate billing page. Shows plan tier, price, next charge
   date, and credit balance (unused credits are themselves worth flagging — they
   don't expire immediately but do eventually).
3. **Kindle Unlimited**: `https://www.amazon.com/kindle-dbs/subscribe/kindle_unlimited`
   or via Account → Digital Services and Devices → Kindle Unlimited.
4. **Prime membership itself**: `https://www.amazon.com/manageprime` — for cases
   where the user isn't using Prime shipping/video/music benefits and it's worth
   flagging (this one is more consequential to cancel than a $9 channel add-on, so
   treat it as report-only unless the user specifically asks about it).
5. For each subscription found, record: name, monthly/annual price, next billing
   date, and — if the page shows it — last-used or last-watched date. If usage data
   isn't visible on the billing page, ask the user directly whether they still use
   it rather than guessing.
6. Don't cancel or touch anything in this phase. Just build the list.

## Phase 2 — Confirm with the user

Report the findings as a plain list: for fees, item / order # / fee amount / who it
shipped to / first-party or third-party; for subscriptions, name / price / billing
cadence / next charge date / whether it looks used or forgotten. Ask which ones to
pursue and what outcome they want for each (waive a fee, dispute a charge, cancel a
subscription, or cancel *and* ask for the last charge back). Some fees are legitimate
(e.g. an opened-item policy the seller disclosed at return time) and some
subscriptions may turn out to still be wanted — don't assume every finding is worth
acting on, and say so if one looks earned or intentional rather than a mistake.

## Phase 3 — Dispute or cancel (one item at a time, only after confirmation)

For fee/refund disputes, drive Amazon's live chat to request a waiver. The exact
click-path, a critical popup-window workaround, and the escalation flow to a human
associate are documented in
[references/dispute-chat-flow.md](references/dispute-chat-flow.md) — read that file
before starting this phase, since Amazon's chat UI has a specific gotcha (it opens in
a popup window Claude in Chrome's tab tracking can't see) that will silently strand
the flow if skipped. The same chat flow and associate-facing script apply whether the
ask is "waive this restocking fee" or "cancel this channel and refund the last
charge" — only the specifics of the ask change.

For subscription cancellations, note the two distinct asks are not equally strong:
- **"Cancel this subscription"** is unconditional — the user is entitled to cancel
  anytime, no negotiation needed. This can usually be done directly on the
  subscription's own settings page (the URLs in Phase 1b) without needing chat at
  all — try that first, it's faster than a chat dispute.
- **"Refund the last charge because I forgot to cancel / wasn't using it"** is a
  goodwill ask, same as a restocking-fee waiver — reasonable to make once, but don't
  push past a single polite counter if declined, and don't claim you tried to cancel
  earlier if that isn't true.

Ground rules while chatting with the associate:
- State only true facts: order number or subscription name, item, price, fee amount
  (or subscription charge amount), and that it was sold/billed by Amazon.com (when
  true). Don't invent a prior contact attempt or a return/cancellation reason that
  didn't happen — the ask itself is reasonable on its own and doesn't need
  embellishment to land.
- When offered a refund method, default to original payment method unless the user
  said otherwise.
- Confirm the exact refund amount and stated timeline, or the exact cancellation
  effective date, before ending the chat.

## Phase 4 — Report

After each dispute or cancellation resolves (or if the associate declines), tell the
user: amount recovered or subscription canceled, refund method, stated ETA or
effective date, and associate name if given. If several items were pursued in one
session, summarize as a running total across fees, refunds, and subscriptions
canceled (report subscription savings as "$X/month going forward" separately from
one-time dollars recovered — they're not the same kind of money).

## Stretch goal — not yet built

**Price-protection refunds**: some categories/sellers refund the difference if a
listing's price drops within the return window after purchase. This would mean
comparing paid price vs. current listing price on recent (still-returnable) orders
and flagging drops worth claiming. Worth building once the restocking-fee and
subscription flows are both solid, but out of scope for now — don't attempt it
without discussing it with the user first, since it's unvalidated.
