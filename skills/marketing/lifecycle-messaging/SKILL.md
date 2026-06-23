---
name: lifecycle-messaging
description: Email/SMS lifecycle and deliverability framework for SMB Product-Builder products that send transactional or lifecycle messages (booking reminders, CRM sequences, receipts, win-back). Codifies provider selection (Resend/Postmark/Twilio/SendGrid), domain auth (SPF/DKIM/DMARC), consent and compliance (TCPA, CAN-SPAM, CASL, quiet hours, double opt-in), suppression-list discipline, and the transactional-vs-marketing split. Applied by integrations-engineer and senior-dev whenever a feature sends messages — so deliverability and consent are designed in, not bolted on after the first spam complaint.
when_to_use: |
  Apply when a feature sends email or SMS:
  - integrations-engineer designing a Twilio / email-provider integration
  - senior-dev implementing booking reminders, CRM sequences, receipts, or win-back
  - architect deciding the messaging provider + domain-auth setup for a crm/booking product
  Do NOT apply for purely in-app notifications with no email/SMS leg.
effort: medium
allowed-tools: Read, Write, Grep, Glob, WebFetch
paths:
  - "docs/integrations/**"
  - "docs/architecture/**"
---

# Lifecycle messaging — deliverable, consented, compliant

Messages that don't arrive (poor deliverability) or that arrive without consent (TCPA/
CAN-SPAM violations) are both fatal for an SMB product. This skill makes both correct by
construction. **Design the consent + deliverability posture before the first send.**

## 1. Transactional vs marketing — split them

Decide per message which bucket it is; they have different rules and should use different
sending identities (often different subdomains / providers):

| | Transactional | Marketing / lifecycle |
|---|---|---|
| Examples | receipt, booking confirm/reminder, password reset | win-back, promo, newsletter, nurture step |
| Consent | implied by the transaction | **explicit opt-in required** |
| Unsubscribe | not required (but honor STOP) | **required**, one-click, honored fast |
| Sending domain | `txn.` subdomain | `mail.`/`news.` subdomain |

Never send marketing content on the transactional channel "because it delivers better" —
that's how the transactional domain gets burned.

## 2. Provider selection (pick one, justify it)

- **Email** — Postmark (best transactional deliverability, strict on marketing), Resend
  (DX-first, good default), SendGrid (scale). Default: **Resend for transactional**,
  add a marketing-grade ESP only when lifecycle volume justifies it.
- **SMS** — Twilio (messaging service + sender pool), or Telnyx. Use a Messaging Service,
  not a single number, for scale + failover. A2P 10DLC registration is **required** for
  US application-to-person SMS — register the brand/campaign before sending.

## 3. Domain authentication (non-negotiable for email)

- **SPF** — sender IP authorized in DNS.
- **DKIM** — provider signing key published; messages signed.
- **DMARC** — start `p=none` with rua reporting, ramp to `p=quarantine`→`p=reject` once
  aligned. Without DMARC alignment, lifecycle mail lands in spam.
- Warm up a new sending domain gradually; never blast from a cold domain.

## 4. Consent + compliance (US-first)

- **CAN-SPAM (email)** — valid physical postal address, accurate From/Subject, working
  one-click unsubscribe honored within 10 days.
- **TCPA (SMS/voice)** — prior express written consent for marketing SMS; honor STOP/UNSTOP/
  HELP keywords automatically; respect **quiet hours** (no marketing 9pm–8am recipient
  local time). Keep proof of consent (timestamp, source).
- **CASL** (if CA recipients) — express opt-in + identification + unsubscribe.
- **Double opt-in** for marketing lists where feasible — protects deliverability and proves
  consent.

## 5. Suppression discipline (the deliverability lifeline)

Maintain a single **suppression list** the sender checks before every send:
- hard bounces → suppress permanently
- spam complaints (FBL) → suppress + investigate
- unsubscribes / STOP → suppress for that channel immediately
- never re-import a suppressed address from a migration without re-consent

A send that ignores suppression is the fastest path to a blocklist.

## 6. Reliability patterns

- Idempotent sends keyed on the domain event (a reminder for booking X sends once, even on
  retry) — coordinate the key with integrations-engineer.
- Status-callback / webhook reconciliation: record delivered/bounced/failed; surface
  failures, don't swallow them.
- Rate-limit + queue lifecycle sends; never loop-send.
- Quiet-hours + timezone are computed from the **recipient's** locale, not the server's.

## Output

When applied, contribute a **Messaging** section to the integration contract
(`docs/integrations/INTEGRATE-{slug}.md`):

```
## Messaging
- channels: email <provider> / sms <provider>
- identities: txn = <subdomain>, marketing = <subdomain/ESP>
- domain auth: SPF/DKIM/DMARC plan = <state>
- consent: <implied/explicit per message type>; STOP/HELP = handled
- quiet hours: <recipient-local window>; 10DLC: <registered?>
- suppression: <store> checked pre-send
- idempotency key: <derivation>
```
