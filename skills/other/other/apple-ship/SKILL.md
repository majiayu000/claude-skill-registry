---
name: apple-ship
description: Apple release gate for iOS, macOS, TestFlight, App Store, entitlements, signing, privacy disclosures, crash risk, and review-sensitive product changes. Use when shipping an Apple-platform app or update and you want a provider-specific read on release blockers and rollback reality.
user-invocable: true
argument-hint: "[iOS/macOS app, TestFlight build, or App Store release]"
---

Read `../_house-style/house-style.md` before starting.

## Anchor phrases

- If signing is shaky, nothing ships.
- An entitlement mistake is a release blocker, not cleanup.
- TestFlight is not proof. It's pre-impact.
- App Review friction ignored early becomes deadline panic later.

## What to interrogate

### 1. Release surface

State what is shipping:
- iOS app
- macOS app
- TestFlight build
- App Store update
- entitlement, privacy, or background behavior change

### 2. Platform blockers

Check:
- signing and provisioning assumptions
- entitlement correctness
- privacy strings and declared behavior
- login, push, background, purchase, camera, microphone, files, or location usage

### 3. Review-sensitive changes

Ask:
- did the product behavior change in a way App Review will care about?
- are account deletion, subscription, tracking, or external payment rules implicated?
- is there hidden functionality or admin behavior likely to trigger review questions?

### 4. Crash and upgrade realism

Review:
- migration behavior across app versions
- startup failure risk
- permission denial paths
- offline/interrupted flows
- what happens for existing users updating in place

### 5. Rollback honesty

Apple rollback is slow compared to server rollback.
Name what can be mitigated server-side and what cannot.

## Output format

### Apple release surface

What is changing in this build/release.

### Release blockers

Crash, signing, entitlement, privacy, or review blockers.

### Upgrade and review risk

What breaks for existing users or during review.

### Mitigations and rollback reality

Server-side mitigations, phased release advice, and what cannot be undone quickly.

### Verdict

- **Safe for TestFlight/App Store**
- **Fix before submission**
- **Apple release red flag**
