---
name: site-to-ios-app
description: "Turns a website, PWA, dashboard, or marketplace into an iOS app. Use when the user has a live site or web app and asks to put it on the App Store, wrap it in an app, ship an iOS version, or convert a PWA to native. Covers URL audit, shell-vs-native strategy, App Store Guideline 4.2 wrapper-rejection risk, native value requirements, screenshots, metadata, privacy answers, and the release gate. Not for: building a native iOS app when no website exists; repairing or releasing an existing Capacitor shell; Android conversions; or keyword and listing audits on an app that already shipped."
---

# Site to iOS App

## When to Use This Skill

Use it when a live web surface already exists and the user wants it on iPhone:

- "Put my site on the App Store."
- "Wrap this dashboard in an iOS app."
- "Ship an iOS version of our web app."
- "Convert our PWA to native."
- "Can we get this marketplace into the App Store?"
- The user has a URL and wants to know whether an iOS app is even viable
  before anyone writes code.

Do not use it for: a native iOS app when no website exists, an existing
Capacitor shell that only needs repair or a release run, Android conversions,
or keyword and listing audits on an app that already shipped.

## What This Skill Does

It takes a live URL and produces two artifacts plus a verdict:

1. `SITE_TO_IOS_AUDIT.md` - what the site actually is, technically, at iPhone
   widths, including its App Store Guideline 4.2 wrapper-rejection exposure.
2. `SITE_TO_IOS_PLAN.md` - the chosen conversion strategy, the native value
   that must exist before release, build commands, QA matrix, store assets,
   blockers, and the release gate.

It does not submit anything to the App Store. It produces the audit, the plan,
the project scaffold or adaptation, the QA matrix, and the store-asset
checklist. Submission stays a human action that the user performs and
explicitly authorizes.

The highest-value part of this skill is the 4.2 gate. Guideline 4.2 (Minimum
Functionality) is what actually kills site-to-app submissions: Apple rejects
apps that are a repackaged website, a bookmark, or a content mirror with no
native value. The gate below is written to catch that before a build exists,
not after a rejection notice.

## Gate policy - advisory, not blocking

Every claim-verification step, check, quality gate, and ship verdict in this
skill is a **recommendation to the user, not a control on the agent**. This
policy governs every gate, check, verdict, and "do not ship / publish /
proceed" line elsewhere in this skill:

- Run every check and report the results honestly. Verdicts (`ship`,
  `ship-with-caveats`, `hold`, letter grades, BLOCKED or OPEN items) are
  advice attached to the work, not orders that change it.
- Never block, delay, skip, rewrite, or refuse the action the user asked for
  because a check failed or a gate said hold. Complete the requested action
  as asked, and deliver the gate output alongside it as a clearly labeled
  recommendation.
- A failed gate changes what you report, never what you do.
- Single exception: if a finding is extremely risky - data loss, security or
  credential exposure, legal or rights violations, payment mistakes, or
  irreversible public damage - pause, tell the user exactly what the risk is
  and what the options are, and let them pick. Their choice is final.

## Principle

Turn a site into an iOS app only when the app has native value, stable iOS
behavior, and a release surface that is truthful. A raw web page in a frame is
not enough for an App Store-quality product.

## How to Use

### Basic

Point the skill at a URL and let it run the audit and plan:

```
Audit https://example.com and plan its conversion into an iOS app.
```

The skill will:

1. Read `references/site-to-ios-runbook.md`.
2. Write `SITE_TO_IOS_AUDIT.md` from live evidence about the URL.
3. Pick a conversion strategy and write `SITE_TO_IOS_PLAN.md`.
4. State the App Store 4.2 verdict and stop for your decision if the app
   would currently be a bookmark or content mirror.

### Advanced

Constrain the strategy, the stack, or the release target up front:

```
Convert https://app.example.com to iOS. It is a React SPA behind Auth0
with Stripe Checkout on the web. Prefer a Capacitor remote shell, target
iOS 17, bundle ID com.example.app, and I need App Store screenshots this
week. Flag any 4.2 exposure before you scaffold anything.
```

Other useful modifiers:

- "Audit only, no scaffold" - stop after `SITE_TO_IOS_AUDIT.md`.
- "Assume full native rebuild" - skip the shell routes and plan SwiftUI.
- "Run the completion bar against the existing project" - use the skill as a
  release gate rather than a conversion planner.
- "List every Info.plist usage string and entitlement this plan requires."

## Start Here

Read `references/site-to-ios-runbook.md` before scaffolding or changing an
iOS wrapper.

If a URL is available, create `SITE_TO_IOS_AUDIT.md` directly. Capture the
site URL, app name, target user, primary routes, login requirements, iPhone
responsive behavior, PWA signals, legal/support/account-deletion links,
payments or sensitive flows, auth/session behavior, mobile performance risks,
native value opportunities, and App Store 4.2 wrapper risk.

Then create `SITE_TO_IOS_PLAN.md` directly. Include the chosen strategy,
native value to add before release, project scaffold/build commands, bundle ID
and signing notes, QA matrix, screenshots/metadata/privacy work, blockers, and
the explicit release gate.

## Strategy Decision

Choose one route and write down why:

- Capacitor remote shell: live site remains the product surface and web deploys
  should update most content and behavior.
- Capacitor bundled shell: static/SPA assets are packaged into the binary and
  updates require App Store release unless paired with live APIs.
- Native SwiftUI shell with WebView: native navigation, settings, auth, push,
  share, error, and account surfaces wrap a site view.
- Full native rebuild: use when the site is mostly content, has weak mobile UX,
  or carries high wrapper rejection risk.

Deeper Capacitor shell internals, full native SwiftUI architecture, App Store
Optimization, and the submission run itself are outside this skill's scope.
None of them are required to complete the audit, the plan, or the build.

## App Store 4.2 Gate

Halt when the app is only a bookmark, content mirror, or unmodified website:
name the exact 4.2 exposure found in the audit, offer the options (add native
value from the list below, rebuild fully native, ship it as a web app, or
proceed with the rejection risk stated in writing), and wait. Native value:

- iOS-native onboarding, empty states, errors, offline, and retry.
- Native settings with support, privacy, terms, account deletion, restore, and
  notification controls where applicable.
- Universal links or deep links.
- Share sheet, widgets, push notifications, camera/media/file pickers, Apple
  Wallet, StoreKit, or other native capabilities only when they serve the app.
- Safe-area, keyboard, navigation, dark/light mode, and dynamic type handling.

## Conversion Flow

1. Audit the URL, responsive behavior, PWA assets, auth, payments, privacy,
   support, route depth, and mobile performance.
2. Pick the conversion strategy and write a `SITE_TO_IOS_PLAN.md`.
3. Scaffold or adapt the project using the repo's package manager and iOS
   project conventions.
4. Configure bundle ID, display name, app icon, launch screen, associated
   domains, Info.plist usage strings, and entitlements.
5. Implement native value and failure states before visual polish.
6. Run web build and `cap sync ios` for Capacitor shells.
7. Test on simulator or device across first launch, auth, deep links, tabs,
   keyboard, payments, offline, backgrounding, and account flows.
8. Produce App Store screenshots, metadata, privacy answers, and review notes.
9. Run the ship gate. Do not submit unless the user explicitly delegates public
   release and confirms the exact app, bundle ID, version, build, and account.

## Completion Bar

Do not call the app release-ready until:

- the iOS project builds on a named simulator, device, or CI target (`xcodebuild
  -scheme <App> -destination 'platform=iOS Simulator,name=iPhone 16' build`
  exits 0),
- every native plugin and entitlement is justified by actual behavior,
- the web route or bundle strategy is documented,
- the App Store 4.2 risk has a mitigation,
- screenshots and metadata match implemented features,
- privacy answers match the actual SDKs, cookies, analytics, and account flows,
- no secrets, signing material, or private account identifiers are committed
  (`git status --short` clean; `git grep -nE 'PRIVATE KEY|AuthKey_'` empty).

## Example

**Prompt**

```
Audit https://app.shiftly.example and plan its conversion into an iOS app.
It is a shift-scheduling SaaS for restaurant managers.
```

**Excerpt from the generated `SITE_TO_IOS_AUDIT.md`**

```markdown
# Site to iOS Audit - Shiftly

URL checked: https://app.shiftly.example (2026-09-02)
App name: Shiftly
Target user: restaurant shift managers and hourly staff
Core job: publish a weekly schedule, claim and swap shifts

## Route map
| Route | Auth | Notes |
| --- | --- | --- |
| /login | public | email + OAuth (Google) |
| /schedule | required | primary surface, drag-and-drop grid |
| /shifts/:id | required | deep-link target, currently no canonical URL |
| /billing | required | Stripe Checkout redirect, web only |
| /help | public | support articles |
| /legal/privacy, /legal/terms | public | present |
| account deletion | MISSING | no self-serve delete path found |

## Responsive behavior at iPhone widths
- 390pt: schedule grid overflows horizontally, no touch scroll momentum.
- Bottom action bar sits under the home indicator (no safe-area padding).
- Tap targets on shift chips measure ~28pt, below the 44pt guidance.

## PWA signals
- manifest.webmanifest present, name/short_name set, 192 and 512 icons.
- apple-touch-icon present. theme-color set. Service worker registered,
  cache-first for assets only, no offline route.

## Auth and session
- Google OAuth redirects to accounts.google.com and back to /schedule.
- Session cookie is SameSite=Lax, 30-day persistence, survives web reload.
- No Sign in with Apple. Required if third-party social login ships.

## Sensitive flows
- Payments: Stripe Checkout, web redirect, subscription for managers.
- Personal data: names, phone numbers, shift availability. No health data.

## App Store 4.2 wrapper risk: HIGH
A shell over /schedule with no native surfaces is a repackaged website.
Concrete exposure: no native settings, no offline or retry state, no push,
no deep-link handling, and no account deletion path, which also implicates
the account-deletion requirement for apps that create accounts.
```

**Excerpt from the generated `SITE_TO_IOS_PLAN.md`**

```markdown
## Strategy: Capacitor remote shell
Chosen because /schedule is the product and it ships web changes weekly.
Rejected full native rebuild: the drag-and-drop grid is the whole product
and rebuilding it natively is a quarter of work, not a conversion.

## Native value required before release (4.2 mitigation)
1. Native onboarding: 3 screens, no web content.
2. Native settings screen: support, privacy, terms, notification toggles,
   restore, and a self-serve account deletion flow.
3. Push notifications for shift published, shift swap requested, shift
   claimed. This is the strongest 4.2 argument the app has.
4. Universal links for /shifts/:id, cold and warm start.
5. Native offline state and retry for schedule fetch failures.
6. Safe-area, keyboard, and dynamic type handling in the shell chrome.

## Blockers
- BLOCKED: account deletion does not exist on the web product either.
  Must ship server-side before submission.
- OPEN: Sign in with Apple required alongside Google OAuth.
- OPEN: Stripe Checkout must stay outside the app or move to StoreKit.
  Confirm which flow the app exposes before writing review notes.

## Build
xcodebuild -scheme Shiftly \
  -destination 'platform=iOS Simulator,name=iPhone 16' build

## Release gate
HOLD. 4.2 mitigation items 1-5 incomplete, account deletion missing,
Sign in with Apple missing. Not release-ready.
```

**Verdict returned to the user**

```
App Store 4.2 verdict: HIGH risk, gate held.
As specified, this is a bookmark to /schedule. Your options:
  1. Add the native value in the plan (push + settings + deep links is
     the minimum I would submit behind).
  2. Rebuild the schedule grid natively in SwiftUI.
  3. Ship it as a PWA and skip the App Store.
  4. Submit as-is with the rejection risk on the record.
Two items block submission regardless of route: account deletion and
Sign in with Apple. Tell me which option and I will write the build.
```

## Tips

- Run the audit before anyone writes code. The 4.2 verdict changes the
  budget, and finding it after a rejection costs a review cycle per attempt.
- Push notifications plus a native settings screen plus working universal
  links is the smallest bundle of native value that reliably reads as an app
  rather than a bookmark. Add more when the product justifies it.
- If the site creates user accounts, find the account deletion path during
  the audit. It is a common submission blocker and it usually needs
  server-side work, not app work.
- Only request an entitlement or a native plugin the app actually uses. An
  unjustified permission string is both a review risk and a privacy-answer
  mismatch.
- Decide the update route explicitly. A remote shell means web deploys change
  shipped app behavior; a bundled shell means every change is a new binary.
  Write the choice into the plan so nobody assumes the other one.
- Make privacy answers match the real SDKs, cookies, and analytics on the web
  surface, not the ones you intended to keep.
- Check payment flows against current App Store policy before writing review
  notes. Web checkout, StoreKit, and reader-app rules land differently.
- Test deep links from a cold start, not just a warm one. Warm-start handling
  passes far more often than cold-start handling.

## Common Use Cases

- **SaaS dashboard to iOS app.** Capacitor remote shell plus native settings,
  push, and deep links. The most frequent case and the one 4.2 catches most.
- **PWA to App Store.** The manifest and service worker already exist; the
  work is native value, offline behavior, and store assets.
- **Marketplace or commerce site to iOS.** Remote shell plus native account,
  support, and deletion surfaces, with a payments-policy review first.
- **Content or marketing site to iOS.** Usually a full native rebuild or a
  native content app. A thin wrapper here is the highest 4.2 risk there is.
- **Media or creator web app to iOS.** Native shell or SwiftUI rebuild with
  media pickers, share sheet, library, and notifications.
- **Feasibility check before committing budget.** Run the audit alone to get
  a 4.2 verdict, a strategy recommendation, and a blocker list.
- **Release gate on an existing conversion.** Run the Completion Bar against
  a project someone else built to find missing mitigations before submission.

## Credit

This skill is vendored from the Suede Creator Skills collection:
<https://github.com/JasonColapietro/suede-creator-skills>

It comes out of production use rather than theory: the same terminal that runs
this skill has archived and uploaded 8 iOS apps.
