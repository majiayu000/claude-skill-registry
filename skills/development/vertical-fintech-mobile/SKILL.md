---
name: vertical-fintech-mobile
description: 'Domain-knowledge pack for money on a phone — wallets, payments, custody and signing, transaction lifecycle, KYC/AML gates, and offline reconciliation. The rules that separate a payments app from a CRUD app with a currency symbol: a balance is a claim about a server, an idempotency key must outlive the process that made it, keys never enter JavaScript memory, and a device clock may not order financial events. Applied by architect/pm/design-advisor when specing a mobile product that moves money, and by mobile-app-builder while implementing it.'
when_to_use: |
  Apply when a mobile product holds, moves, or reports money or assets:
  - architect writes ARCH-*.md for a wallet, payments, trading, remittance, or account product with a phone client
  - pm decomposes it and must not under-scope the transaction lifecycle (this is where naive specs fail)
  - design-advisor wireframes a balance, a send flow, a signing confirmation, or a blocked-account state
  - mobile-app-builder implements any screen where a number is money
  Do NOT apply to the server-side money rules — pci-reviewer owns payment scope,
  accounting-reviewer owns ledger integrity, oracle-reviewer owns on-chain
  oracles and MEV. This pack is what the PHONE gets wrong.
effort: low
allowed-tools: Read, Write, Grep, Glob
paths:
  - "docs/architecture/**"
  - "docs/plans/**"
  - "docs/design/**"
---

# Money on a phone — spec it like the network will fail mid-transfer

A field app that loses a photo is annoying. A money app that loses — or
duplicates — a transfer is a loss, a support case, and sometimes a regulator.
Everything in the generic mobile contract still applies (offline queue,
idempotency, permissions); this pack is the part that is different **because it
is money**, and it is the part community skill sets do not carry, because it is
domain knowledge rather than framework knowledge.

The through-line: **the phone is not the ledger.** It is a client with an
opinion, and every screen must be honest about how strong that opinion is.

## 1. A balance has three states, never two

`confirmed` · `pending` · `unknown`. A number rendered without which of the three
it is, is a lie the user will act on.

- **confirmed** — the server said so, and the app has heard from the server
  recently enough to say when.
- **pending** — the app has applied its own optimistic change on top. It is a
  *display*, not a fact, and it is labelled.
- **unknown** — the app has not reached the server. This is NOT the last
  confirmed number rendered as though it were current. A stale balance shown as
  live is the defect this whole pack exists to prevent.

Every balance carries **as of when**. "£1,240.55" is not an answer; "£1,240.55,
as of 14:02" is.

## 2. The idempotency key must outlive the process

The generic rule is "client-generated id so a re-sync never duplicates". For
money that is not enough, because the process dies.

- Mint the key **before** the intent leaves the screen, and **persist it with the
  intent** in the same durable write. A key held in memory is a key that a crash
  turns into a second payment.
- The key belongs to the user's *intent*, not to the attempt. Ten retries of one
  "send £50" share one key. A second tap of the button is a new intent — or it is
  a double-send, and the UI decides which by disabling or by asking.
- The server contract must state how long it honours a key. An idempotency window
  shorter than the app's retry backoff is the same as no idempotency.

## 3. Keys never enter JavaScript memory

For any product that signs — custody, non-custodial wallets, hardware-backed auth:

- Signing happens in the platform's secure hardware (Keychain/Secure Enclave,
  Keystore/StrongBox). The app asks for a signature; it never holds the key.
- A seed phrase or private key in a JS variable is in the crash dump, the
  debugger, the redux devtools, and the error reporter. Assume all four.
- **Non-custodial means non-recoverable.** If the product cannot restore a lost
  key, the onboarding must say so before the key exists, not in a support
  article afterwards.
- The signing confirmation shows what is actually being signed, decoded. A
  hex blob the user cannot read is consent theatre.

## 4. A transaction is a state machine, and it is written down

Not "sent/failed". At minimum:

```
drafted → submitted → accepted → settled
                   ↘ rejected
                   ↘ unknown ──(reconcile)──→ settled | rejected
```

- **`unknown` is a real state**, and the one that matters. The request left and
  no answer came back. The app may not guess, may not retry blindly (see §2), and
  may not show it as failed — a payment shown as failed that actually settled is
  how a user sends it twice.
- Every non-terminal state has a **timeout and an owner**: what checks it, how
  often, and what it does when the answer never comes.
- Terminal states are terminal. A settled transaction is not re-driven by a
  retry queue that woke up late.

## 5. The device clock may not order financial events

A phone with a wrong clock silently wins every last-write-wins conflict.

- Ordering comes from the server, or from a logical clock the server issues.
- Device time may be recorded as *observed* metadata — never as the ordering key,
  never as the audit timestamp.
- The same applies to "which offline edit is newer" for anything money-adjacent.

## 6. Reconciliation is a feature, not an error path

When the app reconnects after an offline stretch:

- The server's view of money **wins**, always.
- The difference is **surfaced**, never silently overwritten. A user who saw a
  balance and then sees a different one, with no explanation, files a fraud
  report.
- Reconciliation is idempotent and resumable: it runs on a flaky connection, so
  it must survive being interrupted halfway.
- Pending local intents that the server never received are re-offered to the
  user, not auto-sent. Auto-sending an hour-old payment intent is a surprise
  the user did not consent to.

## 7. A blocked account is a designed state

KYC/AML is not an error dialog.

- The states are real product states with real screens: `unverified`,
  `pending review`, `verified`, `limited`, `frozen`. Each says what the user can
  still do and what happens next.
- The app must be able to **stop**. A limit or a freeze arriving mid-session has
  to be honoured on the next action, not at next launch.
- Never explain a freeze in terms the user can use to evade it. "Under review"
  is the whole message; the reason belongs in the case file, not the UI.
- Re-verification prompts must survive an app reinstall — the state lives on the
  server.

## 8. The screenshot the OS takes without asking

Both platforms snapshot the app when it backgrounds, and that image goes to disk.

- Balances, account numbers, and anything key-shaped are masked on background.
- Screen-recording and screenshot detection where the platform offers it, at
  least for seed-phrase and full-PAN screens.
- The clipboard is shared and, on some platforms, synced across devices. An
  address or code copied to it is not private; expire it.

## 9. What to model (or the spec is naive)

| Entity | Non-obvious part |
|---|---|
| Intent | Distinct from the transaction. Carries the idempotency key, persisted before send. |
| Transaction | The state machine of §4, with `unknown` and per-state timeouts. |
| Balance snapshot | Value + state + `as of`. Never a bare number. |
| Reconciliation run | Resumable, idempotent, with a record of what differed. |
| Verification status | The §7 states, server-owned, survives reinstall. |
| Key reference | A handle to hardware-held material. Never the material. |
| Limit | Per-period, server-evaluated, honoured mid-session. |

## 10. Where this pack stops

- **Payment scope and PSP mechanics** → `pci-reviewer`.
- **Ledger integrity and double-entry** → `accounting-reviewer`.
- **On-chain oracles, MEV, upgradeability** → `oracle-reviewer`.
- **Store policy for financial apps** → `mobile-store-reviewer`.
- **Framework performance** → the mobile performance invariant in
  `agents/mobile-app-builder.md`.

This pack is the phone's own share of the problem, and it is the share that gets
skipped because it looks like plumbing that the backend already handled.
